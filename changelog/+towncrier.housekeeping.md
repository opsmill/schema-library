The changelog is now assembled from news fragments with [towncrier](https://towncrier.readthedocs.io/).
Add a file under `changelog/` named `<id>.<type>.md` describing your change, where `<type>` is one of
`security`, `removed`, `deprecated`, `added`, `changed`, `fixed` or `housekeeping`. A CI check fails a
pull request that carries none, unless it is labelled `ci/skip-changelog`. Assembling the fragments
into `CHANGELOG.md` at release time is a follow-up; existing releases are not back-filled.
