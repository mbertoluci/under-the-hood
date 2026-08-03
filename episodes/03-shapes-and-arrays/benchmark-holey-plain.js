/**
 * The plain variant: same PACKED vs HOLEY comparison, simpler loop.
 *
 * Here the sum has no guard (`total += arr[i]`, nothing else) and the
 * holey array is fully filled. On modern V8 this variant often shows
 * NO measurable difference: the engine optimizes the cost away.
 *
 * Compare with benchmark-holey.js, where the same label costs ~2x.
 * That contrast is the point: HOLEY is a risk, not a fixed price.
 *
 * Run:
 *   node episodes/03-shapes-and-arrays/benchmark-holey-plain.js
 */

import { performance } from 'node:perf_hooks';

const SIZE = 1_000_000;
const ROUNDS = 100;

const packed = [];
for (let i = 0; i < SIZE; i++) packed.push(i);

const holeyFilled = new Array(SIZE);
for (let i = 0; i < SIZE; i++) holeyFilled[i] = i;

function makeSummer() {
  return function sum(arr) {
    let total = 0;
    for (let i = 0; i < arr.length; i++) total += arr[i];
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

console.log(`Summing ${SIZE.toLocaleString()} elements, ${ROUNDS} rounds (plain loop)\n`);

const p = measure('packed  ([] + push)', packed);
const f = measure('holey, fully filled', holeyFilled);

console.log(`\nholey filled vs packed: ${(f / p).toFixed(2)}x`);
