Schemas now reach the [Infrahub Marketplace](https://marketplace.infrahub.app) through a release
rather than a daily sync of `main`. Publishing the GitHub Release for `vX.Y.Z` runs the full test
suite against the tag, then publishes every `base/` and `extensions/` schema whose content changed
at version `X.Y.Z`. A schema removed or renamed here is deprecated on the Marketplace, and
`experimental/` is never published. The release pull request shows what the Marketplace will
receive before it is merged. See `RELEASING.md`.
