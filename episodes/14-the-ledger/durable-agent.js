#!/usr/bin/env node
// The Ledger — durable agents, from scratch (zero dependencies).
//
// An AI agent handling a real task (booking a flight) is a LONG-RUNNING
// conversation: many steps, one of which spends money. If the process dies
// mid-way (deploy, restart, crash) a naive agent forgets everything and, on
// restart, does it all AGAIN — including charging the card twice.
//
// The fix isn't a database you reload. It's DURABILITY: the state doesn't live
// in memory, it's event-sourced in an append-only ledger. Restart = replay the
// ledger, skip what's already done, continue on the exact same line.
//
// Run it yourself. Don't trust the description — kill it and watch it survive.
//
//   node durable-agent.js --session=42            # durable run (safe to kill)
//   node durable-agent.js --session=42            # run again → resumes, no double charge
//   node durable-agent.js --session=42 --naive    # the "before": forgets on restart
//   node durable-agent.js --session=42 --show     # print the ledger (audit trail)
//   node durable-agent.js --session=42 --reset    # wipe this session

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA = path.join(__dirname, '.data');
fs.mkdirSync(DATA, { recursive: true });

// ---- tiny arg parser ----
const args = process.argv.slice(2);
const flag = (name, def) => {
  const hit = args.find((a) => a === `--${name}` || a.startsWith(`--${name}=`));
  if (!hit) return def;
  const eq = hit.indexOf('=');
  return eq === -1 ? true : hit.slice(eq + 1);
};
const sessionId = String(flag('session', '42'));
const naive = flag('naive', false) === true;
const reset = flag('reset', false) === true;
const show = flag('show', false) === true;

const ledgerPath = path.join(DATA, `session-${sessionId}.ledger.jsonl`);
const chargesPath = path.join(DATA, `charges-${sessionId}.log`);

// ---- the conversation: the agent's plan (one of these spends money) ----
const STEPS = [
  { id: 'validate', label: 'validate the request' },
  { id: 'search',   label: 'search flights' },
  { id: 'select',   label: 'select the best flight' },
  { id: 'charge',   label: 'charge the payment', money: true }, // MUST fire exactly once
  { id: 'seat',     label: 'reserve the seat' },
  { id: 'ticket',   label: 'issue the ticket' },
  { id: 'confirm',  label: 'send the confirmation' },
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const stamp = () => new Date().toISOString();

// ---- the ledger: append-only, event-sourced history ----
function appendEvent(ev) {
  fs.appendFileSync(ledgerPath, JSON.stringify({ at: stamp(), ...ev }) + '\n');
}
function readHistory() {
  if (!fs.existsSync(ledgerPath)) return [];
  return fs
    .readFileSync(ledgerPath, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map((l) => JSON.parse(l));
}
function fireCharge() {
  // the real-world side effect we must never repeat
  fs.appendFileSync(chargesPath, `charged session ${sessionId} at ${stamp()}\n`);
}
function chargeCount() {
  if (!fs.existsSync(chargesPath)) return 0;
  return fs.readFileSync(chargesPath, 'utf8').split('\n').filter(Boolean).length;
}
function reportCharges() {
  const n = chargeCount();
  const ok = n <= 1;
  console.log(
    `\n💳 payment fired ${n} time(s) ` +
      (ok ? '→ correct (idempotent)' : '→ ⚠️  DOUBLE CHARGE — this is the bug')
  );
}

// ---- modes ----
function doReset() {
  for (const p of [ledgerPath, chargesPath]) if (fs.existsSync(p)) fs.unlinkSync(p);
  console.log(`🧹 session ${sessionId} wiped (ledger + charges).`);
}

function doShow() {
  const h = readHistory();
  if (!h.length) return console.log(`(ledger for session ${sessionId} is empty — nothing has happened yet)`);
  console.log(`\n📖 Ledger for session ${sessionId} — the full audit trail:\n`);
  h.forEach((e, i) => {
    const seq = String(i + 1).padStart(3, '0');
    const detail = e.step ? `  ${e.step}` : '';
    console.log(`  ${seq}  ${e.at}  ${e.type}${detail}`);
  });
  console.log(`\n(${h.length} events, append-only. In production, continueAsNew keeps this bounded.)`);
}

// The "before": state lives in memory only. On restart, memory is gone, so the
// agent has no idea it already charged the card — it starts the plan over.
async function runNaive() {
  console.log(`\n▶  [naive] session ${sessionId} — state lives in MEMORY only`);
  const done = new Set(); // dies with the process
  for (let i = 0; i < STEPS.length; i++) {
    const step = STEPS[i];
    const n = `${i + 1}/${STEPS.length}`;
    console.log(`   … step ${n}  ${step.label}`);
    await sleep(step.money ? 1200 : 700); // kill window
    if (step.money) fireCharge();
    done.add(step.id);
    console.log(`   ✓ step ${n}  ${step.label}`);
  }
  console.log(`\n🏁 [naive] done. But every restart begins at step 1 — including the payment.`);
  reportCharges();
}

// The fix: durability. History is the source of truth. We replay it, skip what
// is already recorded, and continue. Kill the process anywhere — rerun — it
// resumes on the exact same line, and the payment never fires twice.
async function runDurable() {
  const history = readHistory();
  const done = new Set(history.filter((e) => e.type === 'step.completed').map((e) => e.step));
  const finished = history.some((e) => e.type === 'workflow.completed');

  if (history.length === 0) {
    appendEvent({ type: 'workflow.started', session: sessionId });
    console.log(`\n▶  session ${sessionId} — starting as a durable workflow`);
  } else if (finished) {
    console.log(`\n✔  session ${sessionId} already completed. Replayed ${history.length} events, nothing left to do.`);
    reportCharges();
    return;
  } else {
    console.log(`\n↻  session ${sessionId} — resuming: replaying ${history.length} events from the ledger`);
    console.log(`   already in history: [${[...done].join(', ') || 'nothing'}]`);
  }

  for (let i = 0; i < STEPS.length; i++) {
    const step = STEPS[i];
    const n = `${i + 1}/${STEPS.length}`;
    if (done.has(step.id)) {
      console.log(`   ✓ step ${n}  ${step.label} — already in history, skipping (no double work)`);
      continue;
    }
    console.log(`   … step ${n}  ${step.label}   ${step.money ? '  ← kill me here (kill -9) and rerun' : ''}`);
    await sleep(step.money ? 1500 : 900); // kill window happens BEFORE the side effect
    if (step.money) fireCharge();
    appendEvent({ type: 'step.completed', step: step.id, index: i });
    console.log(`   ✓ step ${n}  ${step.label} — done, appended to ledger`);
  }

  appendEvent({ type: 'workflow.completed' });
  console.log(`\n✅ session ${sessionId} complete. Same context, no double reply.`);
  reportCharges();
}

// ---- entry ----
if (reset) {
  doReset();
} else if (show) {
  doShow();
} else if (naive) {
  await runNaive();
} else {
  await runDurable();
}
