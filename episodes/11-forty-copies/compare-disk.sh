#!/usr/bin/env bash
#
# Three identical projects, installed twice: npm vs pnpm.
#
# npm copies every package into every project's node_modules.
# pnpm keeps ONE content-addressed copy per package version in a store
# and hard-links it into each project. Same files, no photocopies.
#
# Run:
#   bash episodes/11-forty-copies/compare-disk.sh
#
# Requires: npm and pnpm on your PATH (corepack enable pnpm).

set -euo pipefail

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
echo "working in $WORK (auto-cleaned)"
echo

PKG='{
  "name": "app",
  "private": true,
  "dependencies": {
    "express": "^4",
    "axios": "^1",
    "lodash": "^4"
  }
}'

for i in 1 2 3; do
  mkdir -p "$WORK/npm-app-$i" "$WORK/pnpm-app-$i"
  echo "$PKG" > "$WORK/npm-app-$i/package.json"
  echo "$PKG" > "$WORK/pnpm-app-$i/package.json"
done

echo "installing 3 projects with npm..."
for i in 1 2 3; do
  (cd "$WORK/npm-app-$i" && npm install --silent --no-audit --no-fund)
done

echo "installing 3 projects with pnpm (shared store, hard links)..."
# --package-import-method=hardlink: on macOS (APFS) pnpm defaults to
# copy-on-write clones, which share disk blocks but look like full
# copies to `du`. Hard links (the default on Linux) make the sharing
# visible to the measurement.
for i in 1 2 3; do
  (cd "$WORK/pnpm-app-$i" && pnpm install --silent \
    --store-dir "$WORK/pnpm-store" \
    --package-import-method=hardlink)
done

echo
echo "each npm project carries a full copy:"
du -sh "$WORK"/npm-app-*/node_modules

echo
# du in a single invocation counts each hard-linked file only once,
# so these totals are what the disk actually pays.
NPM_TOTAL=$(du -shc "$WORK"/npm-app-*/node_modules | tail -1 | cut -f1)
PNPM_TOTAL=$(du -shc "$WORK"/pnpm-app-*/node_modules "$WORK/pnpm-store" | tail -1 | cut -f1)

echo "total disk, 3 projects with npm:            $NPM_TOTAL"
echo "total disk, 3 projects + store with pnpm:   $PNPM_TOTAL"
