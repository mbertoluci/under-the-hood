# Episode 07 — The teller's secret priority notes

> Before calling the next customer in the regular line, the teller always
> reads the manager's post-it notes (process.nextTick) and serves the whole
> VIP queue (promise callbacks). Only then a timer or I/O callback gets its
> turn. That is why `setTimeout(fn, 0)` never means "run this next".

## Run it

```bash
node episodes/07-priority-notes/priority-notes.cjs
```

## What I got (Node 22)

```
1. teller: serving you (your sync code runs first)
2. teller: finishing with you (sync code ends)
3. manager's post-it: nextTick
4. VIP queue: promise callback
5. regular line: setTimeout(0) customer
```

The timer asked first, and still got served last. Order in Node is
priority, not arrival.

## Bonus: why this file is .cjs

Rename it to `.js` (this repo is `"type": "module"`) and run it again:
lines 3 and 4 swap. In ES modules, the module body is evaluated inside a
promise, so promise callbacks scheduled at the top level run BEFORE
`process.nextTick`. In CommonJS, `nextTick` wins. Same engine, different
module system, different order — one more reason to never build logic on
top of scheduling order.

## The one-liner

**Nothing interrupts your running code. Priorities only decide who goes next.**
