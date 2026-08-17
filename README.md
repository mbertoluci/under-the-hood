# Under the Hood 🔧

> **Complex engineering, explained for everyone.**

A series where I take the complex parts of software engineering and break them down so anyone can understand — no gatekeeping, no jargon walls. Just how things actually work.

Every episode ships with **runnable code**: benchmarks, demos, and experiments you can execute yourself. Don't trust my numbers — run them.

📌 Follow the series on [LinkedIn — Monan Bertoluci](https://www.linkedin.com/in/mbertoluci)

## Season 1 — The V8 Engine

| # | Episode | Code | Post |
|---|---------|------|------|
| 01 | **Meet V8** — the engine behind everything you ship | [`episodes/01-meet-v8`](episodes/01-meet-v8) | soon |
| 02 | **Your code gets faster while it runs** — the JIT pipeline | [`episodes/02-jit-pipeline`](episodes/02-jit-pipeline) | soon |
| 03 | **Write code the engine can bet on** — shapes, inline caches & array internals | [`episodes/03-shapes-and-arrays`](episodes/03-shapes-and-arrays) | soon |
| 04 | **Stop guessing, start measuring** — when optimization actually matters | [`episodes/04-measure-dont-guess`](episodes/04-measure-dont-guess) | soon |
| 05 | **How V8 cleans up your mess** — the garbage collector (season finale) | [`episodes/05-garbage-collector`](episodes/05-garbage-collector) | soon |

## Season 2 — Node.js, explained like everyday life

Shorter episodes, one idea at a time, everyday analogies first.

| # | Episode | Code | Post |
|---|---------|------|------|
| 06 | **Node.js is a bank with ONE teller** — the event loop | [`episodes/06-event-loop-bank`](episodes/06-event-loop-bank) | soon |
| 07 | **The teller's secret priority notes** — nextTick, promises & why setTimeout(0) runs last | [`episodes/07-priority-notes`](episodes/07-priority-notes) | soon |
| 08 | **One slow customer freezes the whole bank** — blocking the event loop & the Promise myth | [`episodes/08-one-slow-customer`](episodes/08-one-slow-customer) | soon |
| 09 | **The bank hires a second teller** — Worker Threads, the real fix for CPU work | [`episodes/09-second-teller`](episodes/09-second-teller) | soon |
| 10 | **The receipt that saves your Friday deploy** — lockfiles, wish vs receipt | [`episodes/10-the-receipt`](episodes/10-the-receipt) | soon |
| 11 | **You have 40 copies of the same book** — node_modules vs the pnpm store | [`episodes/11-forty-copies`](episodes/11-forty-copies) | soon |
| 12 | **The ghost package you never installed** — phantom dependencies | [`episodes/12-ghost-package`](episodes/12-ghost-package) | soon |
| 13 | **Serving 2 GB with ~50 MB of RAM** — streams, the pool and the straw | [`episodes/13-the-straw`](episodes/13-the-straw) | soon |

## Running the demos

```bash
npm install
node episodes/03-shapes-and-arrays/benchmark-monomorphic.js
```

Requirements: Node.js 20+

## Who writes this

I'm **Monan Bertoluci** — software engineer since 2008, founder of a mission-critical systems company, former Tech Lead rewriting AI engines. After years leading teams, I'm going back to the metal — and taking you with me.

## License

MIT — use everything, teach everyone.
