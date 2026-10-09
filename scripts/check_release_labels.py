"""Validate the explicit release bump label selected for a pull request."""

# ruff: noqa: INP001

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import cast

BUMP_LABELS = frozenset({"changes/major", "changes/minor", "changes/patch"})
RELEASE_PR_PREFIX = "chore(release):"
# The `release/v<version>` branch auto-bump.yml opens: a normalised three-part
# PEP 440 version, optionally with a pre-, post- or dev-release segment.
RELEASE_BRANCH = re.compile(r"release/v\d+\.\d+\.\d+(?:(?:a|b|rc)\d+)?(?:\.post\d+)?(?:\.dev\d+)?")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels-json", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--head-ref", required=True)
    parser.add_argument("--author-login", required=True)
    parser.add_argument("--head-repository", required=True)
    parser.add_argument("--repository", required=True)
    return parser


def main() -> int:
    """Validate that a normal pull request has exactly one release label."""
    args = build_parser().parse_args()

    # Head repository and branch identify a generated release PR; the
    # title is matched by prefix only, so a maintainer editing it (re-running
    # this check on `edited`) does not drop the exemption.
    if (
        args.head_repository == args.repository
        and RELEASE_BRANCH.fullmatch(args.head_ref)
        and args.title.startswith(RELEASE_PR_PREFIX)
    ):
        sys.stdout.write("Skipping label check for generated release pull request.\n")
        return 0

    try:
        raw_labels = json.loads(args.labels_json)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Invalid labels JSON: {exc}\n")
        return 1

    if not isinstance(raw_labels, list) or not all(isinstance(label, str) for label in raw_labels):
        sys.stderr.write("Labels JSON must be an array of strings.\n")
        return 1

    labels = cast("list[str]", raw_labels)
    selected = sorted(BUMP_LABELS.intersection(labels))
    if len(selected) != 1:
        choices = ", ".join(sorted(BUMP_LABELS))
        found = ", ".join(selected) if selected else "none"
        sys.stderr.write(f"Pull requests must have exactly one release bump label ({choices}); found: {found}.\n")
        return 1

    sys.stdout.write(f"Release bump label: {selected[0]}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
