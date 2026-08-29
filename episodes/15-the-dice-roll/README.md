# Episode 15 — The Dice Roll (AI proposes, code decides)

> A startup gives its AI support agent the power to issue refunds. In
> testing, it's great. Then two customers write in with the exact same
> problem — one gets $50 back, the other nothing. Same case, different
> answer. And once, the bot agrees to a "full refund policy" that doesn't
> exist. This really happened: Air Canada's chatbot invented a refund
> rule, and a court made the airline pay it.
>
> The mistake is letting the AI **decide**. A model doesn't apply your
> rules — it improvises them, differently every time. The fix: the AI can
> **propose**; deterministic code — your real policy as rules — **decides**.

## Run it (zero setup)

No dependencies — just Node (>=20).

See the bug first — let the AI decide directly:

```bash
node episodes/15-the-dice-roll/refund-agent.js --unsafe
```

Two identical customers get different refunds, and it approves money the
policy forbids. Run it a few times — the answer changes.

Now the fix — the AI proposes, the code decides:

```bash
node episodes/15-the-dice-roll/refund-agent.js
```

Same case, same answer, every time. The model still improvises a proposal,
but `approve()` checks it against the real policy and caps or denies it.

## Prove it

```bash
node --test episodes/15-the-dice-roll/refund-agent.test.mjs
```

```
✓ same case -> same answer, 100/100 (the policy is deterministic)
✓ the AI invents a policy -> code denies (the Air Canada case)
✓ the AI over-promises -> code caps to the policy
✓ idempotent refund: same key -> exactly one refund
```

## The pattern

- **`evaluateRefund(order)`** — your real policy, as rules. The source of truth.
- **`approve(order, proposal)`** — the AI can only *propose*; code approves against
  the policy and never grants more than allowed.
- **`issueRefund(key, amount)`** — idempotent: a retry never pays twice.
- **`askAgent(order)`** — a stand-in for the LLM. It's non-deterministic on purpose —
  that's exactly why it must never be the final authority on money.

**AI proposes; code decides.** Let the model do what it's good at — read the
message, talk to the customer, draft the reply — and keep every decision that
touches money, auth, or data on deterministic, tested code.
