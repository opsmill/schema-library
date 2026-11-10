"""Tests for the Marketplace release publish in ``tasks.marketplace``.

No network: a fake marketplace records every call, and the library is a
temporary directory shaped like this repository. Ported from the
``infrahub-marketplace`` daily-sync tests, with the release behaviour on top:
version stamping, all-or-nothing planning, removals, renames and the frozen
experimental tier.
"""

# pytest fixtures are injected by parameter name, and an empty-collection
# comparison reads more plainly than `not x` in an assertion.
# pylint: disable=redefined-outer-name,use-implicit-booleaness-not-comparison

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tasks.marketplace import (
    DIFF_LINE_LIMIT,
    MarketplaceError,
    MarketplaceSchemaState,
    PreflightError,
    apply_release,
    detect_renames,
    key_for_path,
    load_entries,
    parse_release_version,
    plan_entry,
    plan_release,
    render,
    render_markdown,
    select,
    source_key,
)

VERSION = "1.5.0"

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def library(tmp_path: Path) -> Path:
    """A miniature schema-library with every awkward shape the real one has."""
    (tmp_path / "base").mkdir()
    (tmp_path / "base" / "dcim.yml").write_text("version: '1.0'\nnodes: []\n")
    (tmp_path / "base" / "ipam.yml").write_text("version: '1.0'\nnodes: [ipam]\n")
    (tmp_path / "base" / "README.md").write_text("# base\n")

    ext = tmp_path / "extensions"
    ext.mkdir()
    (ext / "cable").mkdir()
    (ext / "cable" / "cable.yml").write_text("nodes: [cable]\n")
    (ext / "qinq").mkdir()
    (ext / "qinq" / "qinq.yaml").write_text("nodes: [qinq]\n")
    # README-only directory.
    (ext / "meet_me_room").mkdir()
    (ext / "meet_me_room" / "README.md").write_text("# soon\n")
    (ext / "topology").mkdir()
    (ext / "topology" / "topology.yml").write_text("nodes: [topo]\n")

    # Never published: present only to prove it is never read.
    exp = tmp_path / "experimental"
    exp.mkdir()
    (exp / "security").mkdir()
    (exp / "security" / "security.yml").write_text("nodes: [security]\n")

    (tmp_path / ".metadata.yml").write_text(
        "base/dcim:\n"
        "  name: DCIM\n"
        "  description: Devices, racks, interfaces.\n"
        "extensions/cable:\n"
        "  name: Cable\n"
        "  description: Physical cable connections.\n"
        "experimental/security:\n"
        "  name: Security\n"
        "  description: Firewall policies.\n"
    )
    return tmp_path


@pytest.fixture
def entries(library: Path):
    return load_entries(library)


def entry(entries, name):
    return next(e for e in entries if e.name == name)


class FakeMarketplace:
    """Records every call. Write methods append to `writes`."""

    def __init__(
        self, schemas: dict[str, MarketplaceSchemaState] | None = None
    ) -> None:
        self.schemas = schemas or {}
        self.contents: dict[str, str] = {}
        self.writes: list[tuple] = []
        self.listed: list[dict] = []
        self.fail_submit_with: int | None = None

    def get_schema(self, namespace: str, name: str):
        return self.schemas.get(name)

    def get_version_content(self, version_id: str) -> str:
        return self.contents[version_id]

    def list_namespace_schemas(self, namespace: str) -> list[dict]:
        return self.listed

    def create_schema(self, namespace, name, display_name, description) -> str:
        self.writes.append(("create_schema", name, display_name, description))
        return f"id-{name}"

    def update_schema_metadata(self, schema_id, display_name, description) -> None:
        self.writes.append(("update_metadata", schema_id, display_name, description))

    def add_tags(self, schema_id, tags) -> None:
        self.writes.append(("add_tags", schema_id, tuple(tags)))

    def submit_version(
        self, *, namespace, name, version, changelog, payload, filename
    ) -> str:
        if self.fail_submit_with:
            raise MarketplaceError(self.fail_submit_with, "schema does not conform")
        self.writes.append(("submit", name, version, changelog))
        return f"v-{name}-{version}"

    def publish_version(self, version_id) -> None:
        self.writes.append(("publish", version_id))

    def deprecate_version(self, version_id, reason) -> None:
        self.writes.append(("deprecate", version_id, reason))


def state(name: str, versions: list[tuple], **kw) -> MarketplaceSchemaState:
    """Build marketplace state; `versions` is a list of (semver, status[, source key])."""
    built = []
    for version in versions:
        semver, status = version[0], version[1]
        source = version[2] if len(version) > 2 else None
        changelog = (
            f"Synced from opsmill/schema-library abc1234 ({source})" if source else None
        )
        built.append(
            {
                "id": f"v-{name}-{semver}",
                "semver": semver,
                "status": status,
                "changelog": changelog,
            }
        )
    return MarketplaceSchemaState(
        schema_id=f"id-{name}",
        display_name=kw.get("display_name", ""),
        description=kw.get("description", ""),
        tags=kw.get("tags", []),
        versions=built,
    )


def cable_state(*versions) -> MarketplaceSchemaState:
    return state(
        "cable",
        list(versions) or [("1.0.0", "published", "extensions/cable")],
        display_name="Cable",
        description="Physical cable connections.",
        tags=["extensions"],
    )


def listed(name: str, source: str | None) -> dict:
    changelog = (
        f"Synced from opsmill/schema-library abc1234 ({source})" if source else None
    )
    return {"name": name, "latest_version": {"changelog": changelog}}


def plan_one(mkt, item, **kw):
    return plan_entry(mkt, item, "infrahub", VERSION, **kw)


# ── Discovery ────────────────────────────────────────────────────────────────


def test_only_base_and_extensions_are_discovered(entries):
    assert {e.tier for e in entries} == {"base", "extensions"}
    assert not any(e.key.startswith("experimental/") for e in entries)


def test_discovers_both_yaml_extensions(entries):
    assert entry(entries, "cable").payload_path.name == "cable.yml"
    assert entry(entries, "qinq").payload_path.name == "qinq.yaml"


def test_base_tier_reads_files_not_directories(entries):
    assert {e.key for e in entries if e.tier == "base"} == {"base/dcim", "base/ipam"}


def test_directory_without_payload_is_a_blameless_skip(entries):
    item = entry(entries, "meet_me_room")
    outcome = plan_one(FakeMarketplace(), item)
    assert outcome.action == "skipped"
    assert outcome.blocking is False


def test_directory_with_several_payloads_blocks(library):
    (library / "extensions" / "cable" / "extra.yml").write_text("nodes: [x]\n")
    item = entry(load_entries(library), "cable")
    assert "2 payload files" in item.skip_reason
    assert plan_one(FakeMarketplace(), item).blocking is True


def test_names_match_production_and_are_unique(entries):
    names = [e.name for e in entries]
    assert len(names) == len(set(names))
    assert entry(entries, "topology").key == "extensions/topology"


def test_metadata_supplies_name_and_description(entries):
    dcim = entry(entries, "dcim")
    assert dcim.display_name == "DCIM"
    assert dcim.description == "Devices, racks, interfaces."
    assert entry(entries, "qinq").metadata_missing is True


def test_an_empty_tree_is_a_preflight_failure(tmp_path):
    with pytest.raises(PreflightError):
        load_entries(tmp_path)


# ── Release version ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("raw", ["1.5.0", "v1.5.0", " v1.5.0 "])
def test_release_version_is_normalised(raw):
    assert parse_release_version(raw) == "1.5.0"


@pytest.mark.parametrize("raw", ["1.5", "latest", ""])
def test_release_version_must_be_semver(raw):
    with pytest.raises(PreflightError):
        parse_release_version(raw)


# ── Planning one schema ──────────────────────────────────────────────────────


def test_identical_payload_is_unchanged(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace({"cable": cable_state()})
    mkt.contents["v-cable-1.0.0"] = cable.payload

    assert plan_one(mkt, cable).action == "unchanged"


def test_changed_payload_is_stamped_with_the_release_version(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {"cable": cable_state(("1.0.3", "published", "extensions/cable"))}
    )
    mkt.contents["v-cable-1.0.3"] = "nodes: [old]\n"

    outcome = plan_one(mkt, cable)

    assert outcome.action == "new_version"
    assert outcome.semver == VERSION
    assert outcome.previous == "1.0.3"


def test_absent_schema_is_created_at_the_release_version(entries):
    outcome = plan_one(FakeMarketplace(), entry(entries, "qinq"))
    assert outcome.action == "created"
    assert outcome.semver == VERSION


def test_release_version_must_exceed_every_existing_version(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {
            "cable": cable_state(
                ("1.0.0", "published", "extensions/cable"),
                # A rejected version never reached users but still holds its semver.
                ("2.0.0", "rejected", "extensions/cable"),
            )
        }
    )
    mkt.contents["v-cable-1.0.0"] = "nodes: [old]\n"

    outcome = plan_one(mkt, cable)

    assert outcome.action == "skipped"
    assert outcome.blocking is True
    assert "2.0.0" in outcome.reason


def test_a_pending_version_of_this_release_is_approved(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {
            "cable": cable_state(
                ("1.0.0", "published", "extensions/cable"),
                (VERSION, "pending_review", "extensions/cable"),
            )
        }
    )
    mkt.contents[f"v-cable-{VERSION}"] = cable.payload

    outcome = plan_one(mkt, cable)

    assert outcome.action == "approve_pending"
    assert outcome.pending_version_id == f"v-cable-{VERSION}"


def test_a_pending_version_from_elsewhere_blocks(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {"cable": cable_state(("1.0.4", "pending_review", "extensions/cable"))}
    )
    mkt.contents["v-cable-1.0.4"] = cable.payload

    outcome = plan_one(mkt, cable)

    assert outcome.blocking is True
    assert "pending review" in outcome.reason


def test_deprecated_identical_content_is_republished(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {"cable": cable_state(("1.0.0", "deprecated", "extensions/cable"))}
    )
    mkt.contents["v-cable-1.0.0"] = cable.payload

    assert plan_one(mkt, cable).action == "new_version"


def test_experimental_history_blocks_unless_adopted(entries):
    topology = entry(entries, "topology")
    mkt = FakeMarketplace(
        {
            "topology": state(
                "topology", [("1.0.1", "published", "experimental/topology")]
            )
        }
    )
    mkt.contents["v-topology-1.0.1"] = "nodes: [topo_exp]\n"

    blocked = plan_one(mkt, topology)
    assert blocked.blocking is True
    assert "--adopt topology" in blocked.reason

    adopted = plan_one(mkt, topology, adopt=["topology"])
    assert adopted.action == "new_version"


def test_metadata_refresh_and_missing_tag_are_planned(entries):
    dcim = entry(entries, "dcim")
    mkt = FakeMarketplace(
        {
            "dcim": state(
                "dcim",
                [("1.0.0", "published", "base/dcim")],
                display_name="DCIM",
                description="Typed by hand.",
            )
        }
    )
    mkt.contents["v-dcim-1.0.0"] = dcim.payload

    outcome = plan_one(mkt, dcim, want_diff=True)

    assert outcome.action == "unchanged"
    assert outcome.metadata_updated is True
    assert outcome.tag_added is True
    assert "Typed by hand." in outcome.diff


def test_payload_diff_shows_both_sides_and_is_capped(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace({"cable": cable_state()})
    mkt.contents["v-cable-1.0.0"] = "nodes: [old]\n"

    outcome = plan_one(mkt, cable, want_diff=True)
    assert "-nodes: [old]" in outcome.diff
    assert "+nodes: [cable]" in outcome.diff

    mkt.contents["v-cable-1.0.0"] = "\n".join(f"line {i}" for i in range(500))
    lines = plan_one(mkt, cable, want_diff=True).diff.splitlines()
    assert len(lines) == DIFF_LINE_LIMIT + 1
    assert "more diff lines" in lines[-1]


# ── Planning the release ─────────────────────────────────────────────────────


def test_planning_writes_nothing(entries):
    mkt = FakeMarketplace()
    report = plan_release(mkt, entries, "infrahub", VERSION)

    assert mkt.writes == []
    assert {o.action for o in report.outcomes} == {"created", "skipped"}
    assert report.ready is True


def test_an_api_error_while_planning_blocks_the_release(entries):
    class Broken(FakeMarketplace):
        def get_schema(self, namespace, name):
            raise MarketplaceError(500, "boom")

    report = plan_release(Broken(), entries, "infrahub", VERSION)

    assert report.ready is False
    assert all(o.action == "skipped" for o in report.outcomes)


def test_a_failed_removal_check_blocks_the_release(entries):
    class Unlistable(FakeMarketplace):
        def list_namespace_schemas(self, namespace):
            raise MarketplaceError(503, "unavailable")

    report = plan_release(Unlistable(), entries, "infrahub", VERSION)

    assert report.ready is False
    assert "NOT CHECKED" in render(report)


def test_removed_schema_is_deprecated_on_every_published_version(entries):
    mkt = FakeMarketplace(
        {
            "old_thing": state(
                "old_thing",
                [
                    ("1.0.0", "published", "extensions/old_thing"),
                    ("1.0.1", "published", "extensions/old_thing"),
                    ("1.0.2", "rejected", "extensions/old_thing"),
                ],
            )
        }
    )
    mkt.listed = [listed("old_thing", "extensions/old_thing")]

    report = plan_release(mkt, entries, "infrahub", VERSION)

    assert [r.name for r in report.removals] == ["old_thing"]
    assert report.removals[0].version_ids == ["v-old_thing-1.0.0", "v-old_thing-1.0.1"]
    assert report.removals[0].reason == f"Removed from schema-library in v{VERSION}"


def test_renamed_schema_points_at_its_new_name(entries):
    mkt = FakeMarketplace(
        {"wire": state("wire", [("1.0.0", "published", "extensions/wire")])}
    )
    mkt.listed = [listed("wire", "extensions/wire")]

    report = plan_release(
        mkt,
        entries,
        "infrahub",
        VERSION,
        renames={"extensions/wire": "extensions/cable"},
    )

    assert report.removals[0].renamed_to == "cable"
    assert report.removals[0].reason == f"Renamed to cable in schema-library v{VERSION}"


def test_experimental_and_untraceable_schemas_are_left_alone(entries):
    mkt = FakeMarketplace()
    mkt.listed = [
        listed("security", "experimental/security"),
        listed("hand_written", None),
        listed("cable", "extensions/cable"),
    ]

    report = plan_release(mkt, entries, "infrahub", VERSION)

    assert report.removals == []
    assert report.marketplace_only == ["hand_written", "security"]


def test_an_already_retired_schema_is_not_deprecated_again(entries):
    mkt = FakeMarketplace(
        {
            "old_thing": state(
                "old_thing", [("1.0.0", "deprecated", "extensions/old_thing")]
            )
        }
    )
    mkt.listed = [listed("old_thing", "extensions/old_thing")]

    assert plan_release(mkt, entries, "infrahub", VERSION).removals == []


def test_filtered_run_checks_no_removals(entries):
    mkt = FakeMarketplace(
        {
            "old_thing": state(
                "old_thing", [("1.0.0", "published", "extensions/old_thing")]
            )
        }
    )
    mkt.listed = [listed("old_thing", "extensions/old_thing")]

    report = plan_release(
        mkt, select(entries, ["qinq"]), "infrahub", VERSION, filtered=["qinq"]
    )

    assert report.removals == []
    assert "not checked (filtered run)" in render(report)


# ── Applying ─────────────────────────────────────────────────────────────────


def test_apply_creates_publishes_and_deprecates(entries):
    mkt = FakeMarketplace(
        {
            "cable": cable_state(),
            "old_thing": state(
                "old_thing", [("1.0.0", "published", "extensions/old_thing")]
            ),
        }
    )
    mkt.contents["v-cable-1.0.0"] = "nodes: [old]\n"
    mkt.listed = [listed("old_thing", "extensions/old_thing")]

    chosen = select(entries, ["cable", "qinq"])
    report = plan_release(mkt, chosen, "infrahub", VERSION)
    apply_release(mkt, report, chosen)

    assert (
        "submit",
        "cable",
        VERSION,
        f"Released in opsmill/schema-library v{VERSION} (extensions/cable)",
    ) in mkt.writes
    assert ("publish", f"v-cable-{VERSION}") in mkt.writes
    assert (
        "create_schema",
        "qinq",
        "Qinq",
        "Infrahub extensions schema: qinq",
    ) in mkt.writes
    assert ("add_tags", "id-qinq", ("extensions",)) in mkt.writes
    assert any(w[0] == "deprecate" and w[1] == "v-old_thing-1.0.0" for w in mkt.writes)
    assert report.ok is True
    assert report.applied is True


def test_apply_approves_a_pending_version_without_resubmitting(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {"cable": cable_state((VERSION, "pending_review", "extensions/cable"))}
    )
    mkt.contents[f"v-cable-{VERSION}"] = cable.payload

    report = plan_release(mkt, [cable], "infrahub", VERSION)
    apply_release(mkt, report, [cable])

    assert mkt.writes == [("publish", f"v-cable-{VERSION}")]


def test_apply_refuses_a_plan_with_blocking_skips(library):
    (library / "extensions" / "cable" / "extra.yml").write_text("nodes: [x]\n")
    found = load_entries(library)
    mkt = FakeMarketplace()
    report = plan_release(mkt, found, "infrahub", VERSION)

    with pytest.raises(PreflightError):
        apply_release(mkt, report, found)
    assert mkt.writes == []


@pytest.mark.parametrize(
    ("status_code", "fragment"),
    [
        (422, "validation"),
        (413, "file-size limit"),
        (409, "already exists"),
        (500, "API error"),
    ],
)
def test_a_failing_write_is_reported_and_the_rest_continue(
    entries, status_code, fragment
):
    mkt = FakeMarketplace()
    mkt.fail_submit_with = status_code
    report = plan_release(mkt, entries, "infrahub", VERSION)

    apply_release(mkt, report, entries)

    failed = [o for o in report.outcomes if o.error]
    assert failed
    assert all(fragment in o.error for o in failed)
    # Every creatable schema was still attempted.
    assert sum(1 for w in mkt.writes if w[0] == "create_schema") == len(failed)
    assert report.ok is False


def test_a_second_run_after_success_writes_nothing(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {"cable": cable_state((VERSION, "published", "extensions/cable"))}
    )
    mkt.contents[f"v-cable-{VERSION}"] = cable.payload

    report = plan_release(mkt, [cable], "infrahub", VERSION)
    apply_release(mkt, report, [cable])

    assert report.outcomes[0].action == "unchanged"
    assert mkt.writes == []


# ── Reporting ────────────────────────────────────────────────────────────────


def test_render_names_every_schema_and_counts(entries):
    report = plan_release(FakeMarketplace(), entries, "infrahub", VERSION)
    text = render(report)
    for item in entries:
        assert item.key in text
    assert f"{len(entries)} discovered" in text
    assert "1 skipped (0 blocking)" in text


def test_markdown_summary_lists_changes(entries):
    report = plan_release(FakeMarketplace(), entries, "infrahub", VERSION)
    text = render_markdown(report)
    assert f"schema-library v{VERSION}" in text
    assert "| `extensions/cable` | created |" in text


# ── History helpers ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("changelog", "expected"),
    [
        (
            "Synced from opsmill/schema-library 20ae95e (extensions/rack)",
            "extensions/rack",
        ),
        ("Released in opsmill/schema-library v1.5.0 (base/dcim)", "base/dcim"),
        ("Hand-written release notes", None),
        (None, None),
    ],
)
def test_source_key_reads_both_changelog_formats(changelog, expected):
    assert source_key(changelog) == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("base/dcim.yml", "base/dcim"),
        ("extensions/cable/cable.yml", "extensions/cable"),
        ("extensions/cable/README.md", None),
        ("experimental/qos/qos.yml", None),
    ],
)
def test_key_for_path(path, expected):
    assert key_for_path(path) == expected


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def test_detect_renames_from_git(library):
    _git(library, "init", "-q")
    _git(library, "-c", "user.name=t", "-c", "user.email=t@t", "add", ".")
    _git(library, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    _git(library, "tag", "v1.4.0")
    _git(library, "mv", "extensions/cable", "extensions/wire")
    _git(library, "mv", "extensions/wire/cable.yml", "extensions/wire/wire.yml")
    _git(
        library, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "rename"
    )

    assert detect_renames(library, "v1.4.0") == {"extensions/cable": "extensions/wire"}
    assert detect_renames(library, "") == {}
    with pytest.raises(PreflightError):
        detect_renames(library, "v0.0.0-missing")


# ── Empty releases ───────────────────────────────────────────────────────────


def test_a_release_that_changes_nothing_has_no_changes(entries):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace({"cable": cable_state()})
    mkt.contents["v-cable-1.0.0"] = cable.payload

    assert plan_release(mkt, [cable], "infrahub", VERSION).has_changes is False


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param("nodes: [old]\n", id="new-version"),
        pytest.param(None, id="metadata-only"),
    ],
)
def test_content_or_metadata_changes_count(entries, stored):
    cable = entry(entries, "cable")
    mkt = FakeMarketplace(
        {"cable": cable_state()}
        if stored
        else {
            "cable": state(
                "cable",
                [("1.0.0", "published", "extensions/cable")],
                tags=["extensions"],
            )
        }
    )
    mkt.contents["v-cable-1.0.0"] = stored or cable.payload

    assert plan_release(mkt, [cable], "infrahub", VERSION).has_changes is True
