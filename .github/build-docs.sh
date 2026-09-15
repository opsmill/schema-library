#!/bin/sh

cd docs && pnpm install --frozen-lockfile && pnpm run build
