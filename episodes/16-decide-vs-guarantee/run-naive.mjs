// run-naive.mjs — the naive executor.
//
// It just RUNS whatever the graph decided. No idempotency key, no record of
// what already ran. This is what you get when LangGraph is your ONLY control:
// great decisions, zero execution guarantee. Under a crash, it pays twice.

import { decide } from "./decide.mjs";

// the outside world: a bank that actually moves money.
export function makeBank() {
  return { totalRefunded: 0, calls: [] };
}

function applyEffect(bank, call) {
  if (call.tool === "refund") bank.totalRefunded += call.args.amount; // real side effect
  bank.calls.push(call.tool);
}

// Run the plan. `crashAfter` simulates the worker dying right after a tool's
// side effect but BEFORE the run is marked done. A supervisor then restarts
// the whole run — naively, with no memory of what already happened.
export function runNaive(state, { crashAfter = null } = {}) {
  const bank = makeBank();
  const { plan } = decide(state);

  const attempt = (isRestart) => {
    for (const call of plan) {
      applyEffect(bank, call);
      if (!isRestart && crashAfter && call.tool === crashAfter) {
        throw { __crash: true }; // die: the money already moved, nobody recorded it
      }
    }
  };

  try {
    attempt(false);
  } catch (e) {
    if (!e.__crash) throw e;
    attempt(true); // restart from scratch → re-runs refund → pays twice
  }
  return bank;
}

// CLI: `node run-naive.mjs` (clean) or `node run-naive.mjs --crash` (kill mid-refund)
if (import.meta.url === `file://${process.argv[1]}`) {
  const crash = process.argv.includes("--crash");
  const bank = runNaive({ eligible: true, amount: 50 }, { crashAfter: crash ? "refund" : null });
  console.log(`refund calls: ${bank.calls.filter((c) => c === "refund").length}`);
  console.log(`total refunded for a $50 case: $${bank.totalRefunded}${bank.totalRefunded > 50 ? "  <-- paid twice" : ""}`);
}
