# Episode 11 — You have 40 copies of the same book

> npm and yarn copy every package into every project's node_modules:
> forty projects, forty photocopies of the same encyclopedia. pnpm runs
> a library instead: one content-addressed copy of each package version
> per machine, hard-linked into every project that needs it.

## Run it

```bash
bash episodes/11-forty-copies/compare-disk.sh
```

Requires `npm` and `pnpm` on your PATH (`corepack enable pnpm`).
Installs three identical projects (express, axios, lodash) with each
tool and measures the total disk with `du`.

## What I got (Node 22, pnpm 10, Apple Silicon)

```
each npm project carries a full copy:
 11M  npm-app-1/node_modules
 11M  npm-app-2/node_modules
 11M  npm-app-3/node_modules

total disk, 3 projects with npm:            34M
total disk, 3 projects + store with pnpm:   12M
```

Three projects: 34 MB vs 12 MB. The gap grows linearly with every
project — 40 projects would cost ~440 MB the photocopy way and the
same ~12 MB the library way. Installs get faster too: a package
already in the store never touches the network again.

## Bonus: the day `du` lied to me

My first run showed pnpm using MORE disk than npm (46M vs 34M). The
reason: on macOS (APFS), pnpm's default import method is
**copy-on-write clones** — the disk shares the underlying blocks, but
`du` sees full-size files. The script forces
`--package-import-method=hardlink` (the default behavior on Linux) so
the sharing is visible to the measurement. If you benchmark disk usage
on a Mac, know which one you're measuring.

## The one-liner

**Don't photocopy the encyclopedia. Run a library.**
