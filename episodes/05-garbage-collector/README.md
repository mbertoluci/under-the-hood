# Episode 05 — How V8 cleans up your mess (season finale)

> You never free memory by hand in JavaScript. The garbage collector does it
> for you, and it follows one rule: it only collects what became unreachable.
> If anything still points at an object, it stays. Every memory leak in Node
> is the same story: a forgotten reference.

## Run it

```bash
node episodes/05-garbage-collector/leak-demo.js healthy
node episodes/05-garbage-collector/leak-demo.js leaky
```

## What I got (Node 22, Apple Silicon)

Healthy mode (request-scoped objects, dropped after use):

```
batch  1     6 MB  █
batch  6    11 MB  ███
batch  7     7 MB  ██
batch 12    15 MB  ████
sawtooth: the GC is doing its job.
```

Leaky mode (every payload pushed into an unbounded module-level cache):

```
batch  1    53 MB  █████████████
batch  4   200 MB  ██████████████████████████████████████████████████
batch  8   397 MB  ███████████████████████████████████████████...
batch 12   594 MB  ██████████████████████████████████████████████...
staircase: this process is dying. it just does not know yet.
```

## The four classic leaks

1. **Listeners never removed**: `emitter.on(...)` without `off`. Symptom:
   `MaxListenersExceededWarning` in the logs.
2. **Unbounded caches**: a `Map` or array that only grows. Fix: LRU with a
   size limit, or `WeakMap` when the key's lifetime should control the entry.
3. **Closures capturing big objects**: a live callback keeps everything it
   captured alive.
4. **Forgotten timers**: `setInterval` without `clearInterval` keeps its
   callback (and captures) forever.

## Finding leaks in production

1. Watch `process.memoryUsage().heapUsed` on a dashboard. Read the shape:
   sawtooth is healthy, staircase is a leak.
2. Confirm with two heap snapshots in Chrome DevTools (`node --inspect`),
   using the Comparison view: what grew and never dies is your suspect.
3. In containers, the operational symptom is cyclic OOM restarts: memory
   climbs, the orchestrator kills the process, repeat.

📎 LinkedIn post: _coming soon_
