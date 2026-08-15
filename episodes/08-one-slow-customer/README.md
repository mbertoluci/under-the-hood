# Episode 08 — One slow customer freezes the whole bank

> Node only delegates I/O (vault work). CPU work in your own code
> (counting coins at the counter) runs on the single main thread, and
> while it runs, every other request waits. Wrapping it in a Promise
> changes nothing: async is syntax, not a second teller.

## Run it

```bash
node episodes/08-one-slow-customer/one-slow-customer.js
```

## What I got (Node 22, Apple Silicon)

```
/fast alone:                    0.02s
/fast behind the coins:         2.90s
/fast behind a Promise-wrapped: 2.90s
```

The `/coins` route does ~3s of pure CPU work. An instant `/fast` request
arriving behind it pays the full 3 seconds. The `/coins-promise` route
wraps the same work in `Promise.resolve().then(...)` and the number is
identical: the same thread still does the counting.

## A demo-design detail worth knowing

The client runs in a **separate process** (`fork`). First version had
client and server in the same process, and the numbers came out clean
(0.00s) — because the CPU block froze the stopwatch along with the
server, so the measurement only started after the freeze had passed.
If you ever benchmark event-loop blocking, measure from outside.

## The real fix

Move CPU work off the main thread with Worker Threads — that's the next
episode — or break it into chunks, or push it to a queue/another service.

## The one-liner

**A Promise doesn't hire a second teller. It just gift-wraps the coins for the same one.**
