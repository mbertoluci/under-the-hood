/**
 * Watch V8 optimize a function, and then give up on it, live.
 *
 * V8's optimizing compiler (TurboFan) doesn't compile generic code.
 * It compiles a SPECIALIZED version based on what it has observed:
 * "this function always receives numbers". If that assumption breaks,
 * V8 throws the optimized code away. That's called deoptimization.
 *
 * Run:
 *   node --trace-opt --trace-deopt episodes/02-jit-pipeline/deopt-live.js 2>&1 | grep -E "PHASE|add"
 *
 * You should see V8 marking `add` for optimization, compiling it with
 * TurboFan, and later "bailout / deoptimizing" right after the betrayal.
 * Output varies by Node version. Run it yourself.
 */

function add(a, b) {
  return a + b;
}

console.log('PHASE 1: feeding add() with numbers only...');
let total = 0;
for (let i = 0; i < 100_000; i++) {
  total += add(i, i + 1);
}
console.log(`PHASE 1 done (total: ${total})`);

console.log('PHASE 2: the betrayal. Passing strings now...');
const greeting = add('hello', ' world');
console.log(`PHASE 2 done (result: ${greeting})`);

console.log('PHASE 3: back to numbers...');
for (let i = 0; i < 100_000; i++) {
  total += add(i, i + 1);
}
console.log('PHASE 3 done');
