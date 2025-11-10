#!/usr/bin/env bash
set -euo pipefail

# Ensure dev env synced
if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed. See https://docs.astral.sh/uv/" >&2
  exit 1
fi

# Install dev deps (pre-commit, radon, ruff, pytest, etc.)
uv sync --group dev

# Use uv-managed environments for pre-commit hooks
export PRE_COMMIT_USE_UV=1

# Install hooks and show versions
uvx pre-commit install
uvx pre-commit --version

echo "Pre-commit hooks installed using uv (PRE_COMMIT_USE_UV=1)."
