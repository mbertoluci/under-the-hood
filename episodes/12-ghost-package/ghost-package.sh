#!/usr/bin/env bash
#
# The ghost package you never installed.
#
# The project below declares ONE dependency: express. But the code
# requires "debug", which express installs for itself. npm's flat
# node_modules hoists it where your code can reach it, so the ghost
# works. pnpm's strict layout only exposes what YOU declared, so the
# same code fails on day one instead of on "moving day".
#
# Run:
#   bash episodes/12-ghost-package/ghost-package.sh
#
# Requires: npm and pnpm on your PATH (corepack enable pnpm).

set -euo pipefail

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

PKG='{ "name": "app", "private": true, "dependencies": { "express": "^4" } }'
CODE='
// We never installed "debug". Express did, for itself.
const debug = require("debug");
const { version } = require("debug/package.json");
console.log(`ghost summoned: require("debug") worked, v${version}`);
'

for tool in npm pnpm; do
  mkdir -p "$WORK/$tool-app"
  echo "$PKG"  > "$WORK/$tool-app/package.json"
  echo "$CODE" > "$WORK/$tool-app/index.js"
done

echo "installing with npm..."
(cd "$WORK/npm-app" && npm install --silent --no-audit --no-fund)
echo "installing with pnpm..."
(cd "$WORK/pnpm-app" && pnpm install --silent --store-dir "$WORK/pnpm-store")

echo
echo "--- npm (flat node_modules) ---"
(cd "$WORK/npm-app" && node index.js)

echo
echo "--- pnpm (strict layout) ---"
(cd "$WORK/pnpm-app" && node index.js) || true
