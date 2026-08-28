// Activities = the steps that touch the outside world (I/O, money, APIs).
// Temporal records each COMPLETED activity's result in the workflow history,
// so on replay they are NOT run again. The only re-run risk is an activity that
// was in-flight when the worker was killed — so money-moving activities must be
// idempotent. That's the real production lesson.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA = path.join(__dirname, '.data');
fs.mkdirSync(DATA, { recursive: true });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function validate(session) {
  await sleep(700);
  return `validated ${session}`;
}

export async function search() {
  await sleep(700);
  return ['AA123', 'UA456', 'DL789'];
}

export async function select(flights) {
  await sleep(700);
  return flights[0];
}

// The money step. Idempotent by construction: dedupe on a stable key so a retry
// after a crash can never charge twice.
export async function charge(session, idemKey) {
  await sleep(1500); // <- kill -9 the worker while this runs; Temporal will retry it
  const ledger = path.join(DATA, 'charges.log');
  const seen = fs.existsSync(ledger) ? fs.readFileSync(ledger, 'utf8') : '';
  if (seen.includes(idemKey)) return 'already charged (idempotent skip)';
  fs.appendFileSync(ledger, `${idemKey} :: charged ${session} at ${new Date().toISOString()}\n`);
  return 'charged once';
}

export async function reserveSeat() {
  await sleep(700);
  return '14C';
}

export async function issueTicket() {
  await sleep(700);
  return `TICKET-${Math.floor(Math.random() * 1e6)}`;
}

export async function sendConfirmation(session) {
  await sleep(700);
  return `confirmation sent for ${session}`;
}
