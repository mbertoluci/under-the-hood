/**
 * PACKED vs HOLEY arrays. With a twist.
 *
 * V8 labels every array internally by what's inside (its "elements kind").
 * The classic advice says: "new Array(n) creates a HOLEY array, and holey
 * arrays are slow". I put that to the test, and half of it is outdated.
 *
 * Three scenarios, same sum loop:
 *   1. packed:        built with [] + push, no holes ever
 *   2. holey, filled: born with new Array(n), then every index assigned
 *   3. holey, holes:  1% of the indexes never assigned (real holes)
 *
 * Run:
 *   node episodes/03-shapes-and-arrays/benchmark-holey.js
 *
 * Results vary by machine and Node version. Run it yourself.
 */

import { performance } from 'node:perf_hooks';

const SIZE = 1_000_000;
const ROUNDS = 100;

// 1. Fastest lane: created packed, stays packed.
//    (zeros at the same spots scenario 3 has holes, to keep sums comparable)
const packed = [];
for (let i = 0; i < SIZE; i++) packed.push(i % 100 === 0 ? 0 : i);

// 2. Born HOLEY (new Array allocates n holes), then fully filled.
//    The HOLEY label never goes away. Does it still cost anything?
const holeyFilled = new Array(SIZE);
for (let i = 0; i < SIZE; i++) holeyFilled[i] = i % 100 === 0 ? 0 : i;

// 3. Real holes: 1% of the indexes are never assigned.
//    Reading a hole forces V8 down the slow path (prototype chain check).
const holeyWithHoles = new Array(SIZE);
for (let i = 0; i < SIZE; i++) {
  if (i % 100 !== 0) holeyWithHoles[i] = i;
}

// A fresh function per scenario, so each gets its own type feedback.
function makeSummer() {
  return function sum(arr) {
    let total = 0;
    for (let i = 0; i < arr.length; i++) total += arr[i] || 0;
    return total;
  };
}

function measure(label, arr) {
  const sum = makeSummer();
  for (let i = 0; i < 3; i++) sum(arr); // warmup

  const start = performance.now();
  for (let i = 0; i < ROUNDS; i++) sum(arr);
  const ms = performance.now() - start;

  console.log(`${label.padEnd(26)} ${ms.toFixed(0)} ms`);
  return ms;
}

console.log(`Summing ${SIZE.toLocaleString()} elements, ${ROUNDS} rounds\n`);

const p = measure('1. packed  ([] + push)', packed);
const f = measure('2. holey, fully filled', holeyFilled);
const h = measure('3. holey, real holes', holeyWithHoles);

console.log(`\nholey filled vs packed: ${(f / p).toFixed(2)}x`);
console.log(`holey with holes vs packed: ${(h / p).toFixed(2)}x`);
