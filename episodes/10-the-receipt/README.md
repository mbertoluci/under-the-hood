# Episode 10 — The receipt that saves your Friday deploy

> package.json is a wish: `"express": "^4.16.0"` names a RANGE, not a
> version. The lockfile is the receipt: the exact version, source and
> checksum of every package you actually installed and tested. Commit
> it, and every kitchen bakes the same cake.

## Run it

```bash
node episodes/10-the-receipt/what-can-change.js
```

(Needs network: it asks the npm registry.)

## What I got (August 2026)

```
package.json says:   "express": "^4.16.0"
versions that satisfy that range today: 23
oldest: 4.16.0   newest: 4.22.2
```

23 legal outcomes for one line of package.json. Multiply by hundreds of
dependencies, each with their own ranges, and their dependencies too.
Without a lockfile, every fresh install re-rolls those dice.

## The rules

1. **Commit the lockfile.** `package-lock.json`, `pnpm-lock.yaml`,
   `yarn.lock` — whichever your package manager writes. It is not
   clutter; it is the only thing that makes installs reproducible.
2. **Use `npm ci` in CI/production** (or `pnpm install --frozen-lockfile`,
   `yarn install --immutable`). It installs exactly what the receipt
   says and fails loudly if the wish and the receipt disagree, instead
   of quietly "fixing" it.
3. Update dependencies **on purpose** (`npm update`, Renovate,
   Dependabot), review the lockfile diff, run the tests, then commit
   the new receipt.

## The one-liner

**package.json is the wish. The lockfile is the receipt.**
