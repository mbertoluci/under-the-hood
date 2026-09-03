// The proof. Two kinds of control over the SAME tool call, side by side.
//   node --test episodes/16-decide-vs-guarantee/

import { test } from "node:test";
import assert from "node:assert/strict";
import { decide } from "../decide.mjs";
import { runNaive } from "../run-naive.mjs";
import { runDurable } from "../run-durable.mjs";

const CASE = { eligible: true, amount: 50 };

test("LangGraph controls the DECISION: which tools, in order, with a limit", () => {
  const { plan, stoppedBy } = decide(CASE);
  assert.deepEqual(plan.map((c) => c.tool), ["lookup_order", "check_policy", "refund", "reply"]);
  assert.equal(stoppedBy, "route_to_end"); // it stopped by routing to END, not by hitting the limit
});

test("LangGraph alone: crash right after refund → customer paid TWICE", () => {
  const bank = runNaive(CASE, { crashAfter: "refund" });
  assert.equal(bank.calls.filter((c) => c === "refund").length, 2);
  assert.equal(bank.totalRefunded, 100); // a $50 refund became $100
});

test("without a crash, the naive path looks perfectly fine (that's the trap)", () => {
  const bank = runNaive(CASE, { crashAfter: null });
  assert.equal(bank.totalRefunded, 50);
});

test("Temporal controls the GUARANTEE: crash after refund → exactly once", () => {
  let res;
  try {
    runDurable(CASE, { crashAfter: "refund" });
    assert.fail("expected the worker to crash");
  } catch (e) {
    assert.ok(e.__crash);
    res = runDurable(CASE, { log: e.log }); // restart on the durable history
  }
  assert.equal(res.status, "DONE");
  assert.equal(res.bank.totalRefunded, 50); // the refund did NOT run twice
});

test("Human-in-the-loop: a big refund PAUSES for a durable approval signal", () => {
  const BIG = { eligible: true, amount: 5000 };
  const log = [];

  let res = runDurable(BIG, { log });
  assert.equal(res.status, "WAITING_HUMAN_APPROVAL");
  assert.equal(res.bank.totalRefunded, 0); // nothing moved while it waits

  // days later, a human approves (the signal); we resume on the same history
  res = runDurable(BIG, { log, approvals: new Set([res.waitingOn]) });
  assert.equal(res.status, "DONE");
  assert.equal(res.bank.totalRefunded, 5000); // once, and only after approval
});
