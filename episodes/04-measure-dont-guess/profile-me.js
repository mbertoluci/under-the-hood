/**
 * A fake API worker with three suspects. One of them is slow.
 *
 * Don't guess which one. Let the profiler count.
 *
 * Node ships with a sampling profiler: about 1,000 times per second it
 * checks which function is running and keeps a tally. No install needed.
 *
 * Run:
 *   node --prof episodes/04-measure-dont-guess/profile-me.js
 *   node --prof-process isolate-*.log > profile.txt
 *
 * Then open profile.txt and read the [JavaScript] section: the function
 * with the most ticks is your bottleneck. Delete the isolate-*.log after.
 */

const REQUESTS = 300_000;

// Suspect 1: validation
function validate(req) {
  if (typeof req.id !== 'number') throw new Error('bad id');
  if (typeof req.name !== 'string') throw new Error('bad name');
  if (!Array.isArray(req.items)) throw new Error('bad items');
  return true;
}

// Suspect 2: transformation
function transform(req) {
  return {
    id: req.id,
    name: req.name.toUpperCase(),
    items: req.items.map((item) => ({ ...item, total: item.price * item.qty })),
  };
}

// Suspect 3: serialization
function serialize(res) {
  // Innocent-looking call. A hand-rolled deep clone, on every request.
  const clone = deepClone(res);
  return JSON.stringify(clone);
}

// The kind of helper that hides in every legacy codebase.
function deepClone(value) {
  if (Array.isArray(value)) return value.map(deepClone);
  if (value !== null && typeof value === 'object') {
    const copy = {};
    for (const key of Object.keys(value)) {
      copy[key] = deepClone(value[key]);
    }
    return copy;
  }
  return value;
}

function makeRequest(i) {
  return {
    id: i,
    name: `customer-${i}`,
    items: [
      { sku: 'A', price: 10, qty: 2 },
      { sku: 'B', price: 5, qty: 4 },
      { sku: 'C', price: 8, qty: 1 },
    ],
  };
}

let bytes = 0;
for (let i = 0; i < REQUESTS; i++) {
  const req = makeRequest(i);
  validate(req);
  const res = transform(req);
  bytes += serialize(res).length;
}

console.log(`processed ${REQUESTS.toLocaleString()} requests (${bytes.toLocaleString()} bytes)`);
