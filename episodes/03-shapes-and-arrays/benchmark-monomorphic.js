/**
 * Monomorphic vs megamorphic property access.
 *
 * Both scenarios sum the same values from 4 objects.
 * The only difference: in the monomorphic case all objects share
 * one hidden class (same properties, same order); in the megamorphic
 * case each object has a different shape.
 *
 * Run:
 *   node episodes/03-shapes-and-arrays/benchmark-monomorphic.js
 *
 * Results vary by machine and Node version — run it yourself.
 */

import { performance } from 'node:perf_hooks';

const ITERATIONS = 10_000_000;
const WARMUP_RUNS = 3;

// One shape: { x, y } created in the same order.
const monomorphic = Array.from({ length: 8 }, (_, i) => ({ x: i, y: i * 2 }));

// Same `x` values, but 8 DIFFERENT shapes: each object carries a unique
// set of extra properties, so `x` lives at a different slot every time.
// V8's inline caches handle up to 4 shapes (polymorphic) — beyond that
// the access site goes megamorphic and stays slow.
const megamorphic = Array.from({ length: 8 }, (_, i) => {
  const obj = {};
  for (let p = 0; p < i; p++) obj[`pad${p}`] = p; // unique prefix per object
  obj.x = i;
  obj.y = i * 2;
  return obj;
});

// A fresh function per scenario, so each one gets its own inline caches.
// Reusing a single function would let the first scenario pollute the
// type feedback of the second.
function makeSummer() {
  return function sumX(objects) {
    let total = 0;
    for (let i = 0; i < ITERATIONS; i++) {
      total += objects[i % objects.length].x;
    }
    return total;
  };
}

function measure(label, objects) {
  const sumX = makeSummer();

  // Warmup: let the profiler watch and TurboFan optimize.
  for (let i = 0; i < WARMUP_RUNS; i++) sumX(objects);

  const start = performance.now();
  sumX(objects);
  const ms = performance.now() - start;

  console.log(`${label.padEnd(14)} ${ms.toFixed(1)} ms`);
  return ms;
}

console.log(`Summing obj.x — ${ITERATIONS.toLocaleString()} iterations\n`);

const mono = measure('monomorphic', monomorphic);
const mega = measure('megamorphic', megamorphic);

console.log(`\nmegamorphic is ${(mega / mono).toFixed(1)}x slower`);
