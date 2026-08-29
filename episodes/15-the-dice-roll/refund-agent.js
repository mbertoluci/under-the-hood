// Episode 15 — The Dice Roll
// AI proposes, code decides. A refund agent with a deterministic policy engine.
//
//   Safe flow (default):   node episodes/15-the-dice-roll/refund-agent.js
//   See the bug (unsafe):  node episodes/15-the-dice-roll/refund-agent.js --unsafe
//   Run the tests:         node --test episodes/15-the-dice-roll/refund-agent.test.mjs
//
// The mistake most people make: letting the AI DECIDE what only code should decide.
// A language model doesn't apply your rules — it improvises them, differently every
// time, and it can be talked into almost anything (see: Air Canada's chatbot, which
// invented a refund policy and a court made the airline honor it).
// The fix: the AI can propose; deterministic code — your real policy as rules — decides.

import { fileURLToPath } from "node:url";

const round2 = (n) => Math.round(n * 100) / 100;

// ── the real policy: the single source of truth (deterministic) ─────────────
export const POLICY = {
  "defective": { maxDays: 30, rate: 1.0 }, // full refund if defective, within 30 days
  "buyers-remorse": { maxDays: 14, rate: 0.5 }, // 50% within 14 days
};

export function evaluateRefund(order) {
  const rule = POLICY[order.reason];
  if (!rule) return { eligible: false, amount: 0, rule: "no-such-policy" };
  if (order.daysSincePurchase > rule.maxDays) return { eligible: false, amount: 0, rule: "past-window" };
  return { eligible: true, amount: round2(order.total * rule.rate), rule: order.reason };
}

// the AI can only PROPOSE; code APPROVES against policy — never more than allowed.
export function approve(order, proposal) {
  const decision = evaluateRefund(order); // ground truth
  if (!decision.eligible) return { approved: false, amount: 0, why: decision.rule };
  return { approved: true, amount: Math.min(proposal.amount ?? Infinity, decision.amount), why: decision.rule };
}

// idempotent refund — same key => exactly one refund
const ledger = new Map();
export function issueRefund(key, amount) {
  if (ledger.has(key)) return ledger.get(key);
  const receipt = { id: "rf_" + key, amount, issued: true };
  ledger.set(key, receipt);
  return receipt;
}
export function _reset() { ledger.clear(); }

// ── a MOCK "AI agent": it improvises. Same input, different output. ─────────
// Stands in for a real LLM call. The point is it's non-deterministic and easily
// talked into things — so you must never let it be the final authority on money.
export function askAgent(order, { pushy = false } = {}) {
  const options = pushy
    ? [order.total, order.total, round2(order.total * 0.75)] // a pushy customer gets over-generous offers
    : [round2(order.total * 0.5), 0, order.total]; // otherwise, all over the place
  return { reason: order.reason, amount: options[Math.floor(Math.random() * options.length)], note: "sure, happy to help!" };
}

// ── the demo ────────────────────────────────────────────────────────────────
function main() {
  const unsafe = process.argv.includes("--unsafe");
  const order = { total: 500, daysSincePurchase: 90, reason: "defective" }; // past the 30-day window → policy says $0

  console.log(`\nCase: "${order.reason}", $${order.total}, ${order.daysSincePurchase} days old`);
  console.log(`Policy: defective is refundable within ${POLICY.defective.maxDays} days — this order is past the window.\n`);

  if (unsafe) {
    console.log("❌ UNSAFE — the AI decides directly:\n");
    for (const who of ["Customer A", "Customer B"]) {
      const p = askAgent(order, { pushy: who === "Customer B" });
      console.log(`   ${who}: agent → refund $${p.amount}`);
    }
    console.log("\n   Same case, different answers — and it refunds money the policy forbids.");
    console.log("   This is the Air Canada bug: the model invents a policy that doesn't exist.\n");
    return;
  }

  console.log("✅ SAFE — the AI proposes, the code decides:\n");
  _reset();
  const key = `${order.reason}-${order.total}-${order.daysSincePurchase}`;
  for (const who of ["Customer A", "Customer B"]) {
    const proposal = askAgent(order, { pushy: who === "Customer B" }); // the model still improvises...
    const decision = approve(order, proposal); // ...but code has the final say
    if (decision.approved) issueRefund(key, decision.amount);
    console.log(`   ${who}: agent proposed $${proposal.amount} → code decided $${decision.amount}  (${decision.why})`);
  }
  console.log("\n   Same case, same answer, every time. Code caps and denies what the policy forbids.\n");
}

if (process.argv[1] === fileURLToPath(import.meta.url)) main();
