# Episode 16 — Decide vs Guarantee (LangGraph × Temporal on tool control)

> "LangGraph or Temporal?" is the wrong question. When your agent calls a
> tool that moves money, two *different* things control that one call:
> LangGraph decides **which tool and when**; Temporal guarantees it
> **actually ran — once**, survived a crash, and paused for a human when it
> mattered. They aren't rivals. One is the decision, the other is the
> guarantee. Skip the second and your agent refunds the customer twice on
> restart.

## The two controls

| | LangGraph | Temporal |
|---|---|---|
| Controls | the **decision** | the **execution** |
| Answers | *which tool, when, loop or stop* | *did it truly run, exactly once* |
| Made of | planner/tools nodes, routing, recursion limit | durable activity, event-sourced history, idempotency key, signals |
| File here | `decide.mjs` | `run-durable.mjs` |

## Run it (zero setup — just Node 20+)

The graph decides the same plan every time. What changes is who *executes* it.

**LangGraph alone — great decision, no execution guarantee.** Kill the worker
right after the refund fires (a deploy, an OOM, a `kill -9`) and a naive
restart re-runs the tool:

```bash
node episodes/16-decide-vs-guarantee/run-naive.mjs          # clean:  $50
node episodes/16-decide-vs-guarantee/run-naive.mjs --crash  # crash:  $100  <-- paid twice
```

**Inside Temporal — same decision, now guaranteed.** The tool is a durable
step: its completion is in an append-only history, so replay after the crash
skips it. Exactly once:

```bash
node episodes/16-decide-vs-guarantee/run-durable.mjs --crash  # crash+replay: $50 (once)
```

**Human-in-the-loop.** A refund over the threshold pauses on a durable
approval signal — it can wait days without holding a thread — and only moves
money after the human approves:

```bash
node episodes/16-decide-vs-guarantee/run-durable.mjs --big
# WAITING_HUMAN_APPROVAL · $0  →  after approval: DONE · $5000
```

## Prove it yourself

```bash
node --test episodes/16-decide-vs-guarantee/
```

Five checks: the graph decides the right tools in order and stops by routing to
END (not by hitting the recursion limit); the naive path pays twice under a
crash but looks fine without one (the trap); the durable path pays exactly once
across a crash; and a big refund waits for a human signal before moving a cent.

## The point

This is not "pick one." In production you run the reasoning **graph inside the
durable workflow**: LangGraph picks the tool, Temporal makes the tool call
survive reality. The AI decides, the platform guarantees.

## Files

- `decide.mjs` — the reasoning graph (LangGraph's job): which tool, when, recursion limit.
- `run-naive.mjs` — executes the plan with no durability. Crashes into a double refund.
- `run-durable.mjs` — executes the same plan as durable, idempotent, human-gated steps.
- `test/tools.test.mjs` — the runnable proof.
