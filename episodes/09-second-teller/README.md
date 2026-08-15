# Episode 09 — The bank hires a second teller

> Episode 08 showed CPU work freezing every request on the single main
> thread. The fix is a Worker Thread: a real second thread with its own
> JavaScript engine and its own memory, talking to the main thread by
> messages (postMessage). The main teller keeps serving the line while
> the second teller counts the coins in the back room.

## Run it

```bash
node episodes/09-second-teller/second-teller.js
```

## What I got (Node 22, Apple Silicon)

```
/fast while MAIN teller counts:   2.91s
/fast while SECOND teller counts: 0.00s
```

Same 3 seconds of CPU work. The only change is who does it.

## How the demo works

One file, three roles, picked at startup:

- **Worker thread** (`!isMainThread`): counts the coins, posts a message back
- **Server** (main thread): `/coins-main-teller` blocks like episode 08;
  `/coins-second-teller` spawns a Worker and stays free
- **Client** (forked process): measures `/fast` from outside, so the
  stopwatch can't be frozen by the block it is measuring (see episode 08)

## Honest caveats

- Spawning a Worker costs real time and memory (V8 isolate per worker).
  Production apps keep a **pool** of workers instead of one per request
  (see `piscina`, or roll your own with a queue).
- Workers are for **CPU-bound** work. Using them for I/O is waste: the
  event loop already delegates I/O for free (episode 06).
- Workers don't share variables by default. Data moves by message
  (structured clone), which has its own cost for huge payloads —
  `SharedArrayBuffer` and `transferList` exist for when that matters.

## The one-liner

**One teller serves. The other counts. The line never stops.**
