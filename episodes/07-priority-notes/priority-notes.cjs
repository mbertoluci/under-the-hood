/**
 * Who gets served next?
 *
 * The teller (your JS thread) always finishes the current customer first.
 * Then, before calling the regular line, he checks two places:
 *
 *   1. the manager's post-it notes  -> process.nextTick
 *   2. the VIP queue                -> Promise callbacks (microtasks)
 *   3. only then, the regular line  -> timers and I/O (macrotasks)
 *
 * The trap: setTimeout(fn, 0) does NOT mean "run this next".
 *
 * Run:
 *   node episodes/07-priority-notes/priority-notes.js
 */

console.log('1. teller: serving you (your sync code runs first)');

setTimeout(() => {
  console.log('5. regular line: setTimeout(0) customer');
}, 0);

Promise.resolve().then(() => {
  console.log('4. VIP queue: promise callback');
});

process.nextTick(() => {
  console.log("3. manager's post-it: nextTick");
});

console.log('2. teller: finishing with you (sync code ends)');
