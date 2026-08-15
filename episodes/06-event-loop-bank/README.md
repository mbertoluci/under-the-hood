# Episode 06 — Node.js is a bank with ONE teller (Season 2 opener)

> Node runs your JavaScript on a single thread. It still serves thousands of
> users at once, because that thread never waits for slow work: network, disk,
> and database calls are delegated (the "back office"), and the thread moves
> on to the next customer. That scheduling is the event loop.

## Run it

```bash
node episodes/06-event-loop-bank/one-teller.js
```

## What I got (Node 22, Apple Silicon)

```
one teller, 1000 customers, 1s of back-office work each...
all 1000 served in 1.4s (not 1000s)
```

1,000 requests, each needing 1 full second of I/O-style work, served by one
thread in 1.4 seconds. Sequential waiting would take almost 17 minutes.

## The catch

Delegation only works for I/O. If the slow work happens *inside your
JavaScript* (heavy math, huge JSON parsing, sync crypto), the teller is stuck
at the counter and the whole line freezes. That failure mode is Episode 08.

## The one-liner

**Node isn't fast because it does everything at once. It's fast because it never waits.**
