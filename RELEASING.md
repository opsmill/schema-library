# Releasing Schema Library

Dispatch `auto-bump.yml` on `main` when the branch is ready to ship. The workflow calculates a version from the release labels on merged pull requests, or accepts an explicit `version`. It assembles the Towncrier changelog and opens a release pull request.

The published version comes from the `v<version>` Git tag. The `pyproject.toml` version belongs to helper tooling and is not bumped for a schema release.

Add a release-notes page under `docs/docs/release-notes/` to the release pull request. Review the version, changelog, and page before merging. Merging the release PR creates the tag and GitHub Release. Do not create the tag directly.

## Publishing to the Marketplace

Publishing the GitHub Release publishes the schemas to the [Infrahub Marketplace](https://marketplace.infrahub.app). Nothing reaches the Marketplace when an ordinary pull request merges.

Before merging, open the **Marketplace plan** check on the release pull request. Its job summary lists what the Marketplace will receive: which schemas get a new version, which are deprecated, and the payload diffs. The check fails when the plan has a problem that would block the publish.

After merging, `marketplace-publish.yml` runs:

1. It runs the full test suite against the `vX.Y.Z` tag. If any check fails, nothing is published. Fix the problem in a pull request and cut the next release.
2. It publishes every schema under `base/` and `extensions/` whose content changed since its last published version. The Marketplace version equals the release version. Unchanged schemas keep their current version. The run summary lists what changed.

What a release publishes:

- A schema removed from `base/` or `extensions/` is deprecated on the Marketplace. A renamed schema is deprecated with a pointer to its new name, which is published as a new schema. The Marketplace does not delete published versions.
- `experimental/` is never published. Experimental schemas already on the Marketplace stay as they are. To publish one, move it to `extensions/` in a pull request.
- Only plain `X.Y.Z` releases are published. A pre-release, or a release such as `X.Y.Z.post1`, does not reach the Marketplace.
- Collections are not changed by a release. If a schema belongs to a collection, align the collection in the Marketplace after the release.

If the publish itself fails, for example because the Marketplace is unavailable, run it again for the same tag. Schemas that already landed report as unchanged:

```bash
gh workflow run marketplace-publish.yml --ref v2.0.0 -f preview=false
```

To see what a release would publish without cutting one, run the plan on any branch. It reads public data only and writes nothing:

```bash
gh workflow run marketplace-publish.yml --ref main -f version=2.0.0
```

To run the plan locally:

```bash
uv run invoke marketplace.publish --version 2.0.0 --previous-tag v1.4.11 --preview --diff
```

## Infrahub version used by the tests

The `schema-test` job loads every non-experimental schema into a pinned Infrahub version. The pin is `infrahub-testcontainers` in the `integration` dependency group of `pyproject.toml`; the package version equals the Infrahub image version.

When Infrahub publishes a release, `opsmill/infrahub` sends a `trigger-infrahub-update` repository dispatch. `update-infrahub.yml` then updates the pin, adds a news fragment, and opens a pull request from the `infrahub-update/vX.Y.Z` branch with the `changes/patch` label. The SA team (`@opsmill/sa`) is the requested reviewer. Nothing merges automatically: the reviewer checks that `schema-test` passes against the new version, then merges.

To move the pin without a release dispatch, run the workflow by hand:

```bash
gh workflow run update-infrahub.yml -f version=1.12.1
```

To run the schema load test locally, start Docker and run:

```bash
uv sync --group dev --group integration
uv run pytest tests/integration -v
```

Set `INFRAHUB_TESTING_IMAGE_VER` to test against a different Infrahub version than the pin. `uv run pytest tests/unit` runs the unit tests and does not need Docker.
