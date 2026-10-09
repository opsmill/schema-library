# Releasing Schema Library

Dispatch `auto-bump.yml` on `main` when the branch is ready to ship. The workflow calculates a version from the release labels on merged pull requests, or accepts an explicit `version`. It assembles the Towncrier changelog and opens a release pull request.

The published version comes from the `v<version>` Git tag. The `pyproject.toml` version belongs to helper tooling and is not bumped for a schema release.

Add a release-notes page under `docs/docs/release-notes/` to the release pull request. Review the version, changelog, and page before merging. Merging the release PR creates the tag and GitHub Release. Do not create the tag directly.
