# Episode 14 — The Ledger (durable agents)

> Your AI agent has a secret: the moment you deploy, it forgets the
> whole conversation. And real conversations live for days, across
> deploys, restarts, crashes. The fix isn't a database you reload. It's
> durability: the state doesn't live in memory, it's event-sourced in an
> append-only ledger. Restart = replay the ledger, skip what's done,
> continue on the exact same line.

## Run it (zero setup)

The star demo has **no dependencies** — just Node. It books a flight in 7
steps, and one of those steps charges a card.

```bash
node episodes/14-the-ledger/durable-agent.js --session=42
```

Now prove it survives. In another terminal (or just hit `Ctrl+C`) kill it
while it's on **step 4/7, charge the payment**, then run the same command
again:

```bash
node episodes/14-the-ledger/durable-agent.js --session=42
```

It replays the ledger, skips the steps already recorded, resumes on the
exact same line, and finishes. Check the audit trail:

```bash
node episodes/14-the-ledger/durable-agent.js --session=42 --show
```

## The bug it fixes

Run the naive version — state in memory only — twice, as if a deploy
restarted it mid-flight:

```bash
node episodes/14-the-ledger/durable-agent.js --session=99 --naive
node episodes/14-the-ledger/durable-agent.js --session=99 --naive
```

```
💳 payment fired 2 time(s) → ⚠️  DOUBLE CHARGE — this is the bug
```

Same thing on the durable version fires the payment **once**, no matter
how many times you kill and rerun. That's idempotency, for free, because
history is the source of truth.

```
node durable-agent.js --session=42            durable run (safe to kill anywhere)
node durable-agent.js --session=42 --naive    the "before": forgets on restart
node durable-agent.js --session=42 --show     print the ledger (audit trail)
node durable-agent.js --session=42 --reset    wipe this session
```

## The real fix, in production: Temporal

The from-scratch ledger above is ~150 lines to make the idea tangible. In
production you don't hand-roll the log, the replay, the retries, the
timeouts — you let a durable execution engine do it. [`temporal/`](temporal)
is the same booking as a real Temporal workflow.

```bash
# 1. a local Temporal dev server (install the CLI: https://docs.temporal.io/cli)
temporal server start-dev

# 2. the worker (stateless, disposable — this is the one you kill -9)
cd episodes/14-the-ledger/temporal && npm install && npm run worker

# 3. start a conversation
npm start 42
```

Kill the worker with `kill -9` while the payment activity runs, then start
it again. The workflow history lives on the server, so the fresh worker
resumes exactly where it left off. Completed activities are never re-run;
the one activity that was in-flight is retried, which is why the `charge`
activity is idempotent on a stable key. Open the Web UI at
`http://localhost:8233` to watch the event history grow.

## Keywords worth searching

`durable workflow` · `event sourcing` · `workflow history` ·
`continueAsNew` · `idempotency` · `audit trail` · `long-running process`

## The one-liner

**Memory forgets on deploy. A ledger doesn't. Run the conversation as a
durable workflow and a kill -9 becomes a non-event.**
