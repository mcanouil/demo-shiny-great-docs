#!/usr/bin/env bash
set -euo pipefail

# Build the great-docs site and copy it into the committed docs/ directory
# that the Shiny app serves at /docs.

cd "$(dirname "$0")/.."

uv run great-docs build
rm -rf docs
cp -R great-docs/_site docs

echo "Documentation built and copied to docs/"
