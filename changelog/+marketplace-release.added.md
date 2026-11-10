Schemas now reach the [Infrahub Marketplace](https://marketplace.infrahub.app) through a release
rather than a daily sync of `main`. Dispatching **Prepare release** opens a release pull request
showing what the Marketplace will receive; merging it tags `vX.Y.Z`, runs the full test suite
against the tag, and publishes every `base/` and `extensions/` schema whose content changed at
version `X.Y.Z`. A schema removed or renamed here is deprecated on the Marketplace, and
`experimental/` is never published. See "Releasing" in the contributing guide.
