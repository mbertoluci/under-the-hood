import { test } from "node:test";
import assert from "node:assert/strict";
import { evaluateRefund, approve, issueRefund, _reset } from "./refund-agent.js";

test("same case -> same answer, 100/100 (the policy is deterministic)", () => {
  const order = { total: 100, daysSincePurchase: 5, reason: "defective" };
  const first = evaluateRefund(order).amount;
  let same = 0;
  for (let i = 0; i < 100; i++) if (evaluateRefund(order).amount === first) same++;
  assert.equal(same, 100);
  console.log(`   determinism: ${same}/100 identical  ($${first})`);
});

test("the AI invents a policy -> code denies (the Air Canada case)", () => {
  const order = { total: 500, daysSincePurchase: 90, reason: "defective" }; // past the 30-day window
  const proposal = { reason: "defective", amount: 500 }; // the bot promised a full refund
  const r = approve(order, proposal);
  assert.equal(r.approved, false);
  assert.equal(r.amount, 0);
});

test("the AI over-promises -> code caps to the policy", () => {
  const order = { total: 100, daysSincePurchase: 3, reason: "buyers-remorse" }; // policy = 50%
  const proposal = { reason: "buyers-remorse", amount: 100 }; // the bot offered full
  assert.equal(approve(order, proposal).amount, 50); // capped by code
});

test("idempotent refund: same key -> exactly one refund", () => {
  _reset();
  const a = issueRefund("case-42", 50);
  const b = issueRefund("case-42", 50); // a retry
  assert.equal(a.id, b.id);
});
