/**
 * The sawtooth and the staircase.
 *
 * Healthy memory looks like a sawtooth: it rises, the garbage collector
 * drops it, it rises again. A leak looks like a staircase: it only goes
 * up, until the process dies out of memory.
 *
 * This demo processes "requests" in two modes and prints the heap after
 * every batch, as a bar chart you can read in the terminal.
 *
 *   healthy:  request-scoped objects, dropped after use
 *   leaky:    every payload pushed into a module-level "cache" with no
 *             size limit (one of the most common real-world leaks)
 *
 * Run:
 *   node episodes/05-garbage-collector/leak-demo.js healthy
 *   node episodes/05-garbage-collector/leak-demo.js leaky
 *
 * Results vary by machine and Node version. Run it yourself.
 */

const mode = process.argv[2] === 'leaky' ? 'leaky' : 'healthy';

const BATCHES = 12;
const REQUESTS_PER_BATCH = 20_000;

// The villain: a "cache" that only ever grows.
const cache = [];

function makePayload(i) {
  return {
    id: i,
    user: `customer-${i}`,
    items: new Array(50).fill(0).map((_, k) => ({ sku: k, price: k * 2 })),
  };
}

function handleRequest(i) {
  const payload = makePayload(i);
  const total = payload.items.reduce((acc, item) => acc + item.price, 0);

  if (mode === 'leaky') {
    cache.push(payload); // the forgotten reference. that's the whole bug.
  }

  return total;
}

function bar(mb) {
  return '█'.repeat(Math.max(1, Math.round(mb / 4)));
}

console.log(`mode: ${mode}\n`);

let n = 0;
for (let b = 1; b <= BATCHES; b++) {
  for (let i = 0; i < REQUESTS_PER_BATCH; i++) handleRequest(n++);

  const mb = process.memoryUsage().heapUsed / 1024 / 1024;
  console.log(`batch ${String(b).padStart(2)}  ${mb.toFixed(0).padStart(4)} MB  ${bar(mb)}`);
}

console.log(`\n${mode === 'leaky' ? 'staircase: this process is dying. it just does not know yet.' : 'sawtooth: the GC is doing its job.'}`);
