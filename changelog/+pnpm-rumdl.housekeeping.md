Documentation tooling now matches the other OpsMill repositories. The docs site is built with
pnpm rather than npm (`docs/pnpm-lock.yaml` replaces `docs/package-lock.json`), and Markdown is
linted with [rumdl](https://github.com/rvben/rumdl), configured under `[tool.rumdl]` in
`pyproject.toml`, rather than a globally installed `markdownlint-cli`. CI no longer invokes `npm`
anywhere. Run `invoke docs.install` and `invoke docs.build` as before; both now shell out to pnpm.
