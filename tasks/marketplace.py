"""Publish a schema-library release to the Infrahub Marketplace.

Ported from ``opsmill/infrahub-marketplace`` ``scripts/sync_schema_library.py``,
which ran daily against ``main``. Publishing is now a release step: the
release workflow runs it once per ``vX.Y.Z`` tag, after the test gate.

Only ``base/`` and ``extensions/`` are published; ``experimental/`` is never
read. Every schema whose content changed is published at the release version,
so "library vX.Y.Z" is a pinnable set: each schema at its highest version
lower than or equal to X.Y.Z.

The run plans first, using reads only, and writes nothing unless the whole plan
is clean:

    uv run invoke marketplace.publish --version 1.5.0 --previous-tag v1.4.11 --preview --diff

Requires an API Token belonging to an **admin**: admins bypass namespace
authorisation and are the only role that may approve their own submission,
which is how a released version reaches users without the review queue.
"""

# One file on purpose: it is a port of a single-file script, read top to bottom.
# pylint: disable=too-many-lines

from __future__ import annotations

import difflib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import httpx
import semver
import yaml  # type: ignore
from invoke import Context, task  # type: ignore
from invoke.exceptions import Exit  # type: ignore

# ── Constants ────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent.resolve()
DEFAULT_API_URL = "https://marketplace.infrahub.app"
DEFAULT_NAMESPACE = "infrahub"
METADATA_FILE = ".metadata.yml"
PAYLOAD_SUFFIXES = (".yml", ".yaml")

# The tier becomes a Tag, and it breaks name collisions: `base/x` keeps `x`,
# so `extensions/x` becomes `x_ext`. These names are what production already
# holds — changing the order renames a live Schema and orphans its history.
# `experimental/` used to be the third tier; it was always lowest, so dropping
# it changes no name above it.
TIER_PRECEDENCE = {"base": 0, "extensions": 1}
TIER_SUFFIX = {"base": "", "extensions": "_ext"}

# Every version this task (and the daily sync before it) submits names its
# source path in brackets, e.g. "Synced from opsmill/schema-library <sha>
# (extensions/cable)". That is how a removal is traced back to the tree.
SOURCE_PATTERN = re.compile(r"opsmill/schema-library \S+ \((?P<key>[^)]+)\)")

# Diffs are hunk-based, so size tracks the change rather than the file. The cap
# only bites on a wholesale rewrite, and the report says how much it dropped.
DIFF_LINE_LIMIT = 200

EXIT_OK = 0
EXIT_INCOMPLETE = 1
EXIT_PREFLIGHT = 2

# Upstream ships at least one directory that holds only a README. That is a
# permanent, blameless condition and must not block a release.
NOTHING_TO_PUBLISH = "no schema payload in directory"

# Statuses the marketplace returns that mean "this schema needs a human", not
# "the run is broken". Anything else is reported as a plain API error.
SKIP_REASONS = {
    409: "version already exists (concurrent run?)",
    413: "payload exceeds the marketplace file-size limit",
    422: "rejected by validation",
}


class PreflightError(Exception):
    """The run cannot start. Nothing has been written."""


class MarketplaceError(Exception):
    """An API call failed. Carries the status so callers can branch on it."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message


# ── Structures ───────────────────────────────────────────────────────────────


@dataclass
class UpstreamEntry:
    """One schema as this repository publishes it."""

    tier: str
    key: str  # tier-qualified path, e.g. "extensions/cable" — the metadata key
    stem: str  # directory name, or file stem for base/
    name: str = ""  # marketplace Schema name, set by resolve_names()
    payload_path: Path | None = None
    payload: str | None = None
    display_name: str = ""
    description: str = ""
    metadata_missing: bool = False
    skip_reason: str | None = None


@dataclass
class MarketplaceSchemaState:
    """What the marketplace currently holds for one Schema."""

    schema_id: str
    display_name: str | None
    description: str
    tags: list[str]
    # {"id", "semver", "status", "changelog"} — every status
    versions: list[dict]


@dataclass
class Outcome:
    """Exactly one planned action per discovered entry."""

    key: str
    name: str
    tier: str
    # created | new_version | approve_pending | unchanged | skipped
    action: str
    semver: str | None = None
    previous: str | None = None
    reason: str | None = None
    metadata_updated: bool = False
    tag_added: bool = False
    diff: str | None = None
    # False when a skip is blameless (nothing to publish here) and so must not
    # block the release. Every other skip needs a human.
    blocking: bool = True
    schema_id: str | None = None
    pending_version_id: str | None = None
    error: str | None = None  # set when applying the plan failed


@dataclass
class Removal:
    """A live Schema whose source path is gone from the tree."""

    name: str
    source_key: str
    version_ids: list[str]
    reason: str
    renamed_to: str | None = None
    error: str | None = None


@dataclass
class Report:
    version: str
    namespace: str
    preview: bool
    outcomes: list[Outcome] = field(default_factory=list)
    removals: list[Removal] = field(default_factory=list)
    marketplace_only: list[str] = field(default_factory=list)
    marketplace_only_error: str | None = None
    filtered: list[str] | None = None
    applied: bool = False

    @property
    def blocked(self) -> list[Outcome]:
        return [o for o in self.outcomes if o.action == "skipped" and o.blocking]

    @property
    def ready(self) -> bool:
        """The plan is clean enough to apply. Checked before any write."""
        return not self.blocked and not self.marketplace_only_error

    @property
    def failed(self) -> int:
        return sum(1 for o in self.outcomes if o.error) + sum(
            1 for r in self.removals if r.error
        )

    @property
    def ok(self) -> bool:
        return self.ready and not self.failed

    def count(self, action: str) -> int:
        return sum(1 for o in self.outcomes if o.action == action)

    @property
    def has_changes(self) -> bool:
        """Applying the plan would change something users can see."""
        return bool(self.removals) or any(
            o.action in {"created", "new_version", "approve_pending"}
            or o.metadata_updated
            or o.tag_added
            for o in self.outcomes
        )


# ── Discovery ────────────────────────────────────────────────────────────────


def _payloads_in(directory: Path) -> list[Path]:
    return sorted(
        p for p in directory.iterdir() if p.is_file() and p.suffix in PAYLOAD_SUFFIXES
    )


def discover(root: Path) -> list[UpstreamEntry]:
    """Walk ``base/`` and ``extensions/`` into entries, one per schema.

    Entries that cannot be published still come back, carrying a
    ``skip_reason`` — every schema has to be accounted for in the report.
    """
    entries: list[UpstreamEntry] = []

    base_dir = root / "base"
    if base_dir.is_dir():
        for payload in _payloads_in(base_dir):
            entries.append(
                UpstreamEntry(
                    tier="base",
                    key=f"base/{payload.stem}",
                    stem=payload.stem,
                    payload_path=payload,
                )
            )

    ext_dir = root / "extensions"
    if ext_dir.is_dir():
        for subdir in sorted(p for p in ext_dir.iterdir() if p.is_dir()):
            entry = UpstreamEntry(
                tier="extensions", key=f"extensions/{subdir.name}", stem=subdir.name
            )
            payloads = _payloads_in(subdir)
            if not payloads:
                entry.skip_reason = NOTHING_TO_PUBLISH
            elif len(payloads) > 1:
                # A Schema Version is a single YAML document, so there is no
                # correct way to pick one or merge several. A human decides.
                names = ", ".join(p.name for p in payloads)
                entry.skip_reason = (
                    f"{len(payloads)} payload files in directory ({names})"
                )
            else:
                entry.payload_path = payloads[0]
            entries.append(entry)

    return entries


def resolve_names(entries: list[UpstreamEntry]) -> None:
    """Assign each entry its marketplace Schema name, in place.

    Names are the directory name verbatim — hyphens included, because a
    Schema's name is fixed at creation. Collisions are broken by tier.
    """
    claimed: set[str] = set()
    for entry in sorted(entries, key=lambda e: (TIER_PRECEDENCE[e.tier], e.stem)):
        name = entry.stem
        if name in claimed:
            name = f"{entry.stem}{TIER_SUFFIX[entry.tier]}"
            suffix = 2
            while name in claimed:
                name = f"{entry.stem}{TIER_SUFFIX[entry.tier]}{suffix}"
                suffix += 1
        claimed.add(name)
        entry.name = name


def _fallback_display_name(stem: str) -> str:
    return stem.replace("-", " ").replace("_", " ").title()


def load_metadata(root: Path) -> dict:
    """Read the per-schema metadata. A missing file is not fatal."""
    path = root / METADATA_FILE
    if not path.is_file():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def apply_metadata(entries: list[UpstreamEntry], metadata: dict) -> None:
    """Fill display name and description from metadata, with a derived fallback."""
    for entry in entries:
        meta = metadata.get(entry.key)
        if not isinstance(meta, dict):
            entry.metadata_missing = True
            entry.display_name = _fallback_display_name(entry.stem)
            entry.description = f"Infrahub {entry.tier} schema: {entry.stem}"
            continue
        entry.display_name = str(meta.get("name") or _fallback_display_name(entry.stem))
        description = meta.get("description")
        entry.description = " ".join(str(description).split()) if description else ""


def read_payloads(entries: list[UpstreamEntry]) -> None:
    """Load each entry's payload, turning an unreadable file into a skip."""
    for entry in entries:
        if entry.skip_reason or entry.payload_path is None:
            continue
        try:
            entry.payload = entry.payload_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            entry.skip_reason = f"cannot read {entry.payload_path.name}: {exc}"


def select(entries: list[UpstreamEntry], wanted: list[str]) -> list[UpstreamEntry]:
    """Narrow a run to named schemas, matching marketplace name or path.

    A name that matches nothing is a preflight failure rather than a quiet
    no-op: a typo that publishes zero schemas while exiting 0 would read as
    "everything is up to date".
    """
    chosen = [e for e in entries if e.name in wanted or e.key in wanted]
    matched = {e.name for e in chosen} | {e.key for e in chosen}
    unknown = sorted(set(wanted) - matched)
    if unknown:
        raise PreflightError(
            f"--only matched no schema: {', '.join(unknown)}. Use the marketplace name or the path."
        )
    return chosen


# ── Versions and history ─────────────────────────────────────────────────────


def parse_release_version(raw: str) -> str:
    """Normalise ``v1.5.0`` / ``1.5.0`` to ``1.5.0``, refusing anything else."""
    version = raw.strip().removeprefix("v")
    try:
        semver.Version.parse(version)
    except ValueError as exc:
        raise PreflightError(f"'{raw}' is not a semantic version (X.Y.Z).") from exc
    return version


def _semver_key(version: dict) -> semver.Version:
    return semver.Version.parse(version["semver"])


def source_key(changelog: str | None) -> str | None:
    """The path a version was published from, read back from its changelog."""
    if not changelog:
        return None
    match = SOURCE_PATTERN.search(changelog)
    return match.group("key") if match else None


def key_for_path(path: str) -> str | None:
    """Map a file path to its metadata key: base/x.yml → base/x, extensions/d/f.yml → extensions/d."""
    parts = Path(path).parts
    if Path(path).suffix not in PAYLOAD_SUFFIXES:
        return None
    if len(parts) == 2 and parts[0] == "base":
        return f"base/{Path(parts[1]).stem}"
    if len(parts) == 3 and parts[0] == "extensions":
        return f"extensions/{parts[1]}"
    return None


def detect_renames(root: Path, previous_tag: str) -> dict[str, str]:
    """Old key → new key for every schema git sees as renamed since the tag."""
    if not previous_tag:
        return {}

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    try:
        git("rev-parse", "--verify", "--quiet", f"{previous_tag}^{{commit}}")
        output = git(
            "diff",
            "--find-renames",
            "--name-status",
            previous_tag,
            "HEAD",
            "--",
            "base",
            "extensions",
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreflightError(
            f"Cannot compare against previous tag '{previous_tag}': {exc}"
        ) from exc

    renames: dict[str, str] = {}
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) != 3 or not fields[0].startswith("R"):
            continue
        old_key, new_key = key_for_path(fields[1]), key_for_path(fields[2])
        if old_key and new_key and old_key != new_key:
            renames[old_key] = new_key
    return renames


# ── Marketplace client ───────────────────────────────────────────────────────


class Marketplace:
    """Thin wrapper over the public REST API.

    Deliberately never calls ``/versions/{semver}/download``: that endpoint
    increments ``download_count``, which Browse sorts on by default.
    ``/versions/{id}/content`` returns the same payload with no side effect.
    """

    def __init__(self, api_url: str, token: str, timeout: float = 60.0) -> None:
        # Without a token the client is anonymous: every read used to plan a
        # release works on public Schemas, and every write is refused.
        self.client = httpx.Client(
            base_url=api_url.rstrip("/"),
            headers={"Authorization": f"Bearer {token}"} if token else {},
            timeout=timeout,
            follow_redirects=True,
        )

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> Marketplace:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # -- plumbing --

    @staticmethod
    def _decode(response: httpx.Response) -> dict:
        # Descriptions in the catalog contain raw control characters, which the
        # stdlib rejects under its default strict parsing.
        return json.loads(response.text, strict=False)

    def _request(self, method: str, path: str, **kwargs: object) -> dict:
        # A cold backend occasionally exceeds the read timeout. Retrying a read
        # once is enough in practice, and is safe because reads have no effect.
        # Writes are never retried — a retried submit could double-publish.
        attempts = 2 if method == "GET" else 1
        response: httpx.Response | None = None
        for attempt in range(attempts):
            try:
                response = self.client.request(method, path, **kwargs)  # type: ignore[arg-type]
                break
            except httpx.TimeoutException:
                if attempt == attempts - 1:
                    raise
        assert response is not None
        if response.status_code >= 400:
            raise MarketplaceError(response.status_code, response.text[:400])
        return self._decode(response) if response.text else {}

    # -- reads --

    def whoami(self) -> dict:
        return self._request("GET", "/api/v1/users/me")

    def list_namespace_schemas(self, namespace: str) -> list[dict]:
        items: list[dict] = []
        cursor: str | None = None
        while True:
            params: dict[str, object] = {"namespace": namespace, "limit": 100}
            if cursor:
                params["cursor"] = cursor
            page = self._request("GET", "/api/v1/schemas", params=params)
            items.extend(page.get("items", []))
            page_info = page.get("page_info") or {}
            cursor = page_info.get("end_cursor")
            if not page_info.get("has_next_page") or not cursor:
                return items

    def get_schema(self, namespace: str, name: str) -> MarketplaceSchemaState | None:
        try:
            data = self._request("GET", f"/api/v1/schemas/{namespace}/{name}")
        except MarketplaceError as exc:
            if exc.status_code == 404:
                return None
            raise
        return MarketplaceSchemaState(
            schema_id=data["id"],
            display_name=data.get("display_name"),
            description=data.get("description") or "",
            tags=[t["name"] for t in data.get("tags") or []],
            versions=[
                {
                    "id": v["id"],
                    "semver": v["semver"],
                    "status": v["status"],
                    "changelog": v.get("changelog"),
                }
                for v in data.get("versions") or []
            ],
        )

    def get_version_content(self, version_id: str) -> str:
        return self._request("GET", f"/api/v1/schemas/versions/{version_id}/content")[
            "content"
        ]

    # -- writes --

    def create_schema(
        self, namespace: str, name: str, display_name: str, description: str
    ) -> str:
        data = self._request(
            "POST",
            "/api/v1/schemas",
            json={
                "name": name,
                "namespace": namespace,
                "display_name": display_name,
                "description": description,
                "visibility": "public",
            },
        )
        return data["id"]

    def update_schema_metadata(
        self, schema_id: str, display_name: str, description: str
    ) -> None:
        self._request(
            "PATCH",
            f"/api/v1/schemas/{schema_id}",
            json={"display_name": display_name, "description": description},
        )

    def add_tags(self, schema_id: str, tags: list[str]) -> None:
        self._request(
            "POST", f"/api/v1/schemas/{schema_id}/tags", json={"tag_names": tags}
        )

    def submit_version(
        self,
        *,
        namespace: str,
        name: str,
        version: str,
        changelog: str,
        payload: str,
        filename: str,
    ) -> str:
        data = self._request(
            "POST",
            f"/api/v1/schemas/{namespace}/{name}/versions",
            data={"semver": version, "changelog": changelog},
            files={"schema_file": (filename, payload.encode("utf-8"), "text/yaml")},
        )
        return data["id"]

    def publish_version(self, version_id: str) -> None:
        self._request(
            "POST", f"/api/v1/reviews/{version_id}", json={"action": "approved"}
        )

    def deprecate_version(self, version_id: str, reason: str) -> None:
        self._request(
            "POST",
            f"/api/v1/schemas/versions/{version_id}/deprecate",
            json={"reason": reason},
        )


# ── Plan ─────────────────────────────────────────────────────────────────────


def payload_diff(before: str, after: str, name: str) -> str:
    """Unified diff of the stored payload against the release's."""
    lines = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"marketplace/{name}",
            tofile=f"release/{name}",
            lineterm="",
        )
    )
    if len(lines) > DIFF_LINE_LIMIT:
        dropped = len(lines) - DIFF_LINE_LIMIT
        lines = lines[:DIFF_LINE_LIMIT] + [f"… {dropped} more diff lines"]
    return "\n".join(lines)


def metadata_diff(state: MarketplaceSchemaState, entry: UpstreamEntry) -> list[str]:
    """Human-readable before/after for the catalog fields a release rewrites."""
    lines = []
    if (state.display_name or "") != entry.display_name:
        lines.append(f"- display_name: {state.display_name!r}")
        lines.append(f"+ display_name: {entry.display_name!r}")
    if state.description != entry.description:
        lines.append(f"- description: {state.description!r}")
        lines.append(f"+ description: {entry.description!r}")
    return lines


def changelog_for(version: str, key: str) -> str:
    return f"Released in opsmill/schema-library v{version} ({key})"


def _block(outcome: Outcome, reason: str) -> Outcome:
    outcome.action = "skipped"
    outcome.reason = reason
    outcome.blocking = True
    return outcome


def plan_entry(  # pylint: disable=too-many-return-statements  # one early return per case
    mkt: Marketplace,
    entry: UpstreamEntry,
    namespace: str,
    version: str,
    *,
    adopt: list[str] | None = None,
    want_diff: bool = False,
) -> Outcome:
    """Decide what one schema needs. Reads only — nothing is written here."""
    outcome = Outcome(key=entry.key, name=entry.name, tier=entry.tier, action="skipped")

    if entry.skip_reason:
        outcome.reason = entry.skip_reason
        outcome.blocking = entry.skip_reason != NOTHING_TO_PUBLISH
        return outcome

    state = mkt.get_schema(namespace, entry.name)
    if state is None:
        outcome.action = "created"
        outcome.semver = version
        outcome.tag_added = True
        return outcome

    outcome.schema_id = state.schema_id

    # Catalog metadata — this repository is the source of truth for it.
    if (
        state.display_name or ""
    ) != entry.display_name or state.description != entry.description:
        outcome.metadata_updated = True
        if want_diff:
            outcome.diff = "\n".join(metadata_diff(state, entry))
    outcome.tag_added = entry.tier not in state.tags

    # A rejected version never reached users, so it is not what this release
    # is compared against. It still holds its semver, which the conflict
    # check below accounts for.
    live = [v for v in state.versions if v["status"] != "rejected"]
    newest = max(live, key=_semver_key) if live else None

    if newest is not None:
        source = source_key(newest.get("changelog"))
        if (
            source
            and source.startswith("experimental/")
            and entry.name not in (adopt or [])
        ):
            # Experimental schemas are frozen. Publishing over one silently
            # would hand its users a different schema under the same name.
            return _block(
                outcome,
                f"live history comes from {source}; pass --adopt {entry.name} to publish {entry.key} over it",
            )

        stored = mkt.get_version_content(newest["id"])
        if stored == entry.payload:
            if newest["status"] == "published":
                outcome.action = "unchanged"
                return outcome
            if newest["status"] == "pending_review":
                if newest["semver"] != version:
                    return _block(
                        outcome,
                        f"{newest['semver']} is pending review with this content; approve or reject it first",
                    )
                # An earlier run of this release submitted it but did not get
                # as far as approving it.
                outcome.action = "approve_pending"
                outcome.semver = version
                outcome.pending_version_id = newest["id"]
                return outcome
            # Deprecated with identical content: the schema came back, so it is
            # published again at this release.

        outcome.previous = newest["semver"]
        if want_diff:
            body = payload_diff(stored, entry.payload or "", entry.name)
            outcome.diff = f"{outcome.diff}\n{body}" if outcome.diff else body

    # The marketplace keeps semver unique per Schema across every status.
    highest = max(state.versions, key=_semver_key)["semver"] if state.versions else None
    if highest and semver.Version.parse(version) <= semver.Version.parse(highest):
        return _block(outcome, f"v{version} does not exceed existing version {highest}")

    outcome.action = "new_version"
    outcome.semver = version
    return outcome


def plan_removals(
    mkt: Marketplace,
    entries: list[UpstreamEntry],
    namespace: str,
    version: str,
    renames: dict[str, str],
) -> tuple[list[Removal], list[str]]:
    """Find live Schemas published from a path that is gone from the tree.

    A Schema's source path is read from its latest version's changelog. Only
    ``base/`` and ``extensions/`` sources are considered: experimental schemas
    are frozen, and a Schema with no traceable source was not published from
    here, so both are reported as marketplace-only and left alone.
    """
    current_keys = {e.key for e in entries}
    name_for_key = {e.key: e.name for e in entries}
    removals: list[Removal] = []
    marketplace_only: list[str] = []

    for item in mkt.list_namespace_schemas(namespace):
        name = item["name"]
        if name in name_for_key.values():
            continue
        source = source_key((item.get("latest_version") or {}).get("changelog"))
        if (
            not source
            or not source.startswith(tuple(f"{tier}/" for tier in TIER_PRECEDENCE))
            or source in current_keys
        ):
            marketplace_only.append(name)
            continue

        state = mkt.get_schema(namespace, name)
        published = (
            [v["id"] for v in state.versions if v["status"] == "published"]
            if state
            else []
        )
        if not published:
            continue  # already retired by an earlier release

        renamed_to = name_for_key.get(renames.get(source, ""))
        reason = (
            f"Renamed to {renamed_to} in schema-library v{version}"
            if renamed_to
            else f"Removed from schema-library in v{version}"
        )
        removals.append(Removal(name, source, published, reason, renamed_to))

    return removals, sorted(marketplace_only)


def plan_release(
    mkt: Marketplace,
    entries: list[UpstreamEntry],
    namespace: str,
    version: str,
    *,
    renames: dict[str, str] | None = None,
    adopt: list[str] | None = None,
    filtered: list[str] | None = None,
    want_diff: bool = False,
) -> Report:
    report = Report(
        version=version, namespace=namespace, preview=True, filtered=filtered
    )

    for entry in entries:
        try:
            report.outcomes.append(
                plan_entry(
                    mkt, entry, namespace, version, adopt=adopt, want_diff=want_diff
                )
            )
        except MarketplaceError as exc:
            reason = SKIP_REASONS.get(exc.status_code, "API error")
            report.outcomes.append(
                _block(
                    Outcome(entry.key, entry.name, entry.tier, "skipped"),
                    f"{reason}: {exc.message}",
                )
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught  # containment is the point
            report.outcomes.append(
                _block(
                    Outcome(entry.key, entry.name, entry.tier, "skipped"),
                    f"{type(exc).__name__}: {exc}",
                )
            )

    # A filtered run sees only part of the tree, so every unselected Schema
    # would look removed.
    if not filtered:
        try:
            report.removals, report.marketplace_only = plan_removals(
                mkt, entries, namespace, version, renames or {}
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            report.marketplace_only_error = f"{type(exc).__name__}: {exc}"

    return report


# ── Apply ────────────────────────────────────────────────────────────────────


def _publish(
    mkt: Marketplace, entry: UpstreamEntry, namespace: str, version: str
) -> None:
    """Submit a version and approve it, so it reaches users immediately."""
    version_id = mkt.submit_version(
        namespace=namespace,
        name=entry.name,
        version=version,
        changelog=changelog_for(version, entry.key),
        payload=entry.payload or "",
        filename=entry.payload_path.name if entry.payload_path else f"{entry.name}.yml",
    )
    mkt.publish_version(version_id)


def _apply_outcome(
    mkt: Marketplace,
    outcome: Outcome,
    entry: UpstreamEntry,
    namespace: str,
    version: str,
) -> None:
    if outcome.action == "created":
        schema_id = mkt.create_schema(
            namespace, entry.name, entry.display_name, entry.description
        )
        mkt.add_tags(schema_id, [entry.tier])
        _publish(mkt, entry, namespace, version)
        return

    if outcome.schema_id is None:
        return
    if outcome.metadata_updated:
        mkt.update_schema_metadata(
            outcome.schema_id, entry.display_name, entry.description
        )
    if outcome.tag_added:
        mkt.add_tags(outcome.schema_id, [entry.tier])
    if outcome.action == "new_version":
        _publish(mkt, entry, namespace, version)
    elif outcome.action == "approve_pending" and outcome.pending_version_id:
        mkt.publish_version(outcome.pending_version_id)


def apply_release(
    mkt: Marketplace, report: Report, entries: list[UpstreamEntry]
) -> None:
    """Carry out a clean plan. One schema's failure never aborts the others."""
    if not report.ready:
        raise PreflightError("The plan has blocking skips; refusing to write anything.")

    by_key = {e.key: e for e in entries}
    for outcome in report.outcomes:
        if outcome.action == "skipped":
            continue
        try:
            _apply_outcome(
                mkt, outcome, by_key[outcome.key], report.namespace, report.version
            )
        except MarketplaceError as exc:
            outcome.error = (
                f"{SKIP_REASONS.get(exc.status_code, 'API error')}: {exc.message}"
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            outcome.error = f"{type(exc).__name__}: {exc}"

    for removal in report.removals:
        try:
            for version_id in removal.version_ids:
                mkt.deprecate_version(version_id, removal.reason)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            removal.error = f"{type(exc).__name__}: {exc}"

    report.preview = False
    report.applied = True


# ── Reporting ────────────────────────────────────────────────────────────────


def _detail(outcome: Outcome) -> str:
    if outcome.action == "skipped":
        return outcome.reason or "no reason given"
    detail = (
        f"{outcome.previous} → {outcome.semver}"
        if outcome.previous
        else outcome.semver or ""
    )
    if outcome.name != outcome.key.split("/")[-1]:
        detail = f"{detail} (as {outcome.name})".strip()
    flags = (" +metadata" if outcome.metadata_updated else "") + (
        " +tag" if outcome.tag_added else ""
    )
    return f"{detail}{flags}".strip()


def _summary_line(report: Report) -> str:
    return (
        f"{len(report.outcomes)} discovered · "
        f"{report.count('created')} created · "
        f"{report.count('new_version')} new version · "
        f"{report.count('approve_pending')} approved · "
        f"{report.count('unchanged')} unchanged · "
        f"{report.count('skipped')} skipped ({len(report.blocked)} blocking) · "
        f"{len(report.removals)} deprecated"
        + (f" · {report.failed} FAILED" if report.failed else "")
    )


def render(report: Report) -> str:
    state = "applied" if report.applied else "plan"
    lines = [
        "",
        f"schema-library v{report.version}  →  {report.namespace}  ({state})"
        + (f"  [only: {', '.join(report.filtered)}]" if report.filtered else ""),
        "",
    ]
    for outcome in report.outcomes:
        detail = _detail(outcome) + (
            f"  FAILED: {outcome.error}" if outcome.error else ""
        )
        lines.append(f"  {outcome.key:<40}{outcome.action:<16}{detail}".rstrip())

    for removal in report.removals:
        detail = f"{removal.reason} ({len(removal.version_ids)} version(s))"
        detail += f"  FAILED: {removal.error}" if removal.error else ""
        lines.append(f"  {removal.source_key:<40}{'deprecated':<16}{detail}")

    lines.append("")
    if report.filtered:
        lines.append("  marketplace-only: not checked (filtered run)")
    elif report.marketplace_only_error:
        lines.append(
            f"  marketplace-only: NOT CHECKED — {report.marketplace_only_error}"
        )
    else:
        lines.append(
            f"  marketplace-only (left untouched): {', '.join(report.marketplace_only) or 'none'}"
        )
    lines.append("")
    lines.append(f"  {_summary_line(report)}")

    diffs = [o for o in report.outcomes if o.diff]
    if diffs:
        lines.append("")
        for outcome in diffs:
            lines.append(f"  ── {outcome.key} " + "─" * max(0, 60 - len(outcome.key)))
            lines.extend(f"  {line}" for line in (outcome.diff or "").splitlines())
            lines.append("")

    lines.append("")
    return "\n".join(lines)


def render_markdown(report: Report) -> str:
    """The same report, shaped for ``$GITHUB_STEP_SUMMARY``."""
    state = "applied" if report.applied else "plan"
    lines = [
        f"### Marketplace — schema-library v{report.version} ({state})",
        "",
        _summary_line(report),
        "",
    ]
    changed = [
        o
        for o in report.outcomes
        if o.action not in {"unchanged"} or o.metadata_updated or o.tag_added
    ]
    if changed or report.removals:
        lines += ["| Path | Action | Detail |", "| --- | --- | --- |"]
        for outcome in changed:
            detail = _detail(outcome) + (
                f" — **FAILED**: {outcome.error}" if outcome.error else ""
            )
            lines.append(
                f"| `{outcome.key}` | {outcome.action} | {detail.replace('|', '/')} |"
            )
        for removal in report.removals:
            detail = removal.reason + (
                f" — **FAILED**: {removal.error}" if removal.error else ""
            )
            lines.append(f"| `{removal.source_key}` | deprecated | {detail} |")
        lines.append("")
    if report.marketplace_only:
        lines.append(
            f"Marketplace-only, left untouched: {', '.join(f'`{n}`' for n in report.marketplace_only)}"
        )
        lines.append("")
    return "\n".join(lines)


def _write_markdown(report: Report, path: str | None) -> None:
    if path:
        with open(path, "a", encoding="utf-8") as out:
            out.write(render_markdown(report) + "\n")


# ── Entry point ──────────────────────────────────────────────────────────────


def load_entries(root: Path, only: list[str] | None = None) -> list[UpstreamEntry]:
    entries = discover(root)
    if not entries:
        # An unreadable or restructured tree must never read as "everything
        # was removed".
        raise PreflightError(
            f"No schemas found under {root}. Refusing to treat an empty tree as a catalog-wide removal."
        )
    resolve_names(entries)
    apply_metadata(entries, load_metadata(root))
    read_payloads(entries)
    return select(entries, only) if only else entries


def _check_identity(mkt: Marketplace) -> None:
    try:
        identity = mkt.whoami()
    except (MarketplaceError, httpx.HTTPError) as exc:
        # A bad token and an unreachable API URL alike mean the run cannot start.
        raise PreflightError(f"could not identify the caller ({exc})") from exc
    if identity.get("role") != "admin":
        raise PreflightError(
            f"'{identity.get('username')}' has role '{identity.get('role')}'; the publishing identity must be an admin."
        )


@task(
    help={
        "version": "Release version, e.g. 1.5.0 (a leading v is accepted)",
        "previous_tag": "Previous release tag, used to tell renames from removals",
        "preview": "Plan only; write nothing. Runs anonymously when MARKETPLACE_TOKEN is unset",
        "diff": "Show payload diffs and catalog metadata before/after",
        "only": "Restrict the run to this schema (marketplace name or path); repeatable",
        "adopt": "Allow publishing over a Schema whose history comes from experimental/; repeatable",
        "require_changes": "Fail when the release would change nothing in the Marketplace",
        "markdown_out": "Also write the Markdown report to this file",
        "namespace": "Marketplace namespace",
    },
    iterable=["only", "adopt"],
)
def publish(  # pylint: disable=too-many-positional-arguments  # invoke maps each to a flag
    context: Context,
    version: str,
    previous_tag: str = "",
    preview: bool = False,
    diff: bool = False,
    only: list[str] | None = None,
    adopt: list[str] | None = None,
    require_changes: bool = False,
    markdown_out: str = "",
    namespace: str = DEFAULT_NAMESPACE,
) -> None:
    """Publish base/ and extensions/ to the Marketplace at the release version."""
    api_url = os.environ.get("MARKETPLACE_URL") or DEFAULT_API_URL
    token = os.environ.get("MARKETPLACE_TOKEN", "")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")

    def report_out(report: Report) -> None:
        _write_markdown(report, summary)
        _write_markdown(report, markdown_out or None)

    try:
        if not token and not preview:
            raise PreflightError("No API Token. Set MARKETPLACE_TOKEN.")
        release = parse_release_version(version)
        entries = load_entries(REPO_ROOT, only or None)
        renames = detect_renames(REPO_ROOT, previous_tag)
    except PreflightError as exc:
        raise Exit(f"error: {exc}", code=EXIT_PREFLIGHT) from exc

    with Marketplace(api_url, token) as mkt:
        if token:
            try:
                _check_identity(mkt)
            except PreflightError as exc:
                raise Exit(f"error: {exc}", code=EXIT_PREFLIGHT) from exc
        else:
            print("note: no MARKETPLACE_TOKEN — planning anonymously from public data.")

        report = plan_release(
            mkt,
            entries,
            namespace,
            release,
            renames=renames,
            adopt=adopt or None,
            filtered=only or None,
            want_diff=diff,
        )
        print(render(report))

        if not report.ready:
            report_out(report)
            raise Exit(
                "error: the plan has blocking skips; nothing was written.",
                code=EXIT_PREFLIGHT,
            )
        if require_changes and not report.has_changes:
            report_out(report)
            raise Exit(
                f"error: v{release} would change nothing in the Marketplace — "
                "nothing under base/ or extensions/ differs from what is published.",
                code=EXIT_PREFLIGHT,
            )
        if preview:
            report_out(report)
            return

        apply_release(mkt, report, entries)

    print(render(report))
    report_out(report)
    if not report.ok:
        raise Exit(
            f"error: {report.failed} write(s) failed; re-run the publish to retry.",
            code=EXIT_INCOMPLETE,
        )
