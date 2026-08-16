# Episode 12 — The ghost package you never installed

> A phantom dependency is a package your code imports but your
> package.json never declares. It works because npm's flat node_modules
> hoists your dependencies' dependencies where your code can reach
> them. It keeps working until "moving day": some innocent update swaps
> or drops the package, and your build dies on a commit that isn't
> yours.

## Run it

```bash
bash episodes/12-ghost-package/ghost-package.sh
```

Requires `npm` and `pnpm` on your PATH (`corepack enable pnpm`).

## What I got (Node 22)

```
--- npm (flat node_modules) ---
ghost summoned: require("debug") worked, v2.6.9

--- pnpm (strict layout) ---
Error: Cannot find module 'debug'
```

The project declares ONE dependency (express). The code requires
`debug`, which express installs for itself. npm hands it over; pnpm
refuses on day one.

The error is the good outcome. A crash on your machine, at install
time, is a gift. The same crash weeks later in production, caused by
someone else's changelog, is an incident.

## The rules

1. **If you import it, declare it** — even if it "already works".
2. **Let tooling police it**: pnpm blocks phantoms by layout; on
   npm/yarn, ESLint's `import/no-extraneous-dependencies` (or knip)
   catches them in CI.

## The one-liner

**A package you use but never declared isn't a dependency. It's a loan.**
