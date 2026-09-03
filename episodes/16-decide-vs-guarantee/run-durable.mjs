// run-durable.mjs — the durable executor: the Temporal role.
//
// SAME decisions, from the SAME graph (decide.mjs). What changes is the second
// kind of control: the GUARANTEE that the call actually ran, once. Each tool
// call is a durable step — an idempotency key (its call id) plus an append-only
// event log (event-sourced history that survives a crash). On replay, completed
// calls are SKIPPED → exactly-once. And a money-moving call above a threshold
// PAUSES for a human approval signal — durably, for as long as it takes.

import { decide } from "./decide.mjs";

export function makeBank() {
  return { totalRefunded: 0, calls: [] };
}

const APPROVAL_THRESHOLD = 100; // refunds above this need a human to approve

function applyEffect(bank, call) {
  if (call.tool === "refund") bank.totalRefunded += call.args.amount;
  bank.calls.push(call.tool);
}

// `log`       = the durable, append-only history (think Temporal workflow history).
//               It survives the crash — that is the whole point.
// `approvals` = the set of approved call ids (the human-in-the-loop signal).
export function runDurable(state, { crashAfter = null, log = [], approvals = new Set() } = {}) {
  const bank = makeBank();
  const { plan } = decide(state);
  const done = new Set(log.filter((e) => e.type === "completed").map((e) => e.id));

  // replay the durable history first: rebuild the world from what already ran.
  for (const e of log) if (e.type === "completed") applyEffect(bank, e.effect);

  for (const call of plan) {
    if (done.has(call.id)) continue; // already ran, per the history → skip. exactly-once.

    // human-in-the-loop: a big refund waits for a durable approval signal.
    const needsApproval = call.tool === "refund" && call.args.amount > APPROVAL_THRESHOLD;
    if (needsApproval && !approvals.has(call.id)) {
      if (!log.some((e) => e.type === "waiting" && e.id === call.id)) {
        log.push({ type: "waiting", id: call.id, amount: call.args.amount });
      }
      return { bank, log, status: "WAITING_HUMAN_APPROVAL", waitingOn: call.id };
    }

    applyEffect(bank, call); // the real side effect
    done.add(call.id);
    log.push({ type: "completed", id: call.id, effect: call }); // durably recorded

    if (crashAfter && call.tool === crashAfter) {
      throw { __crash: true, log }; // die AFTER the completion is in the durable log
    }
  }
  return { bank, log, status: "DONE" };
}

// CLI: `node run-durable.mjs` · `--crash` (kill mid-refund, then auto-replay) · `--big` (needs approval)
if (import.meta.url === `file://${process.argv[1]}`) {
  const crash = process.argv.includes("--crash");
  const big = process.argv.includes("--big");
  const state = { eligible: true, amount: big ? 5000 : 50 };

  if (crash) {
    const log = [];
    try {
      runDurable(state, { crashAfter: "refund", log });
    } catch (e) {
      if (!e.__crash) throw e;
      console.log("crashed mid-refund. restarting on the durable history...");
      const res = runDurable(state, { log: e.log });
      console.log(`total refunded after crash+replay: $${res.bank.totalRefunded}  (exactly once)`);
    }
  } else if (big) {
    const log = [];
    let res = runDurable(state, { log });
    console.log(`status: ${res.status} · moved so far: $${res.bank.totalRefunded}`);
    res = runDurable(state, { log, approvals: new Set([res.waitingOn]) });
    console.log(`after human approval: ${res.status} · total refunded: $${res.bank.totalRefunded}`);
  } else {
    const res = runDurable(state, {});
    console.log(`status: ${res.status} · total refunded: $${res.bank.totalRefunded}`);
  }
}
