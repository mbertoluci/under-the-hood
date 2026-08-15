/**
 * One slow customer freezes the whole bank.
 *
 * The teller only delegates I/O (vault work). If YOUR code does heavy
 * CPU work (counting coins at the counter), the teller is stuck and
 * every other request waits, no matter how "async" your code looks.
 *
 * This demo also busts a myth: wrapping CPU work in a Promise does NOT
 * move it off the thread. Async is syntax, not a second teller.
 *
 * The client runs in a separate process: if it lived in the server's
 * process, the block would freeze the stopwatch too.
 *
 * Run:
 *   node episodes/08-one-slow-customer/one-slow-customer.js
 */

import http from 'node:http';
import { fork } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const secs = (ms) => `${(ms / 1000).toFixed(2)}s`;

// ---------- client process ----------
if (process.argv[2] === 'client') {
  const base = process.argv[3];

  let start = Date.now();
  await fetch(`${base}/fast`);
  console.log(`/fast alone:                    ${secs(Date.now() - start)}`);

  // One slow customer walks in...
  const coins = fetch(`${base}/coins`);
  await new Promise((r) => setTimeout(r, 100)); // he reaches the counter
  start = Date.now();
  await fetch(`${base}/fast`); // ...and an innocent /fast walks in behind him
  console.log(`/fast behind the coins:         ${secs(Date.now() - start)}`);
  await coins;

  // Same coins, "wrapped in a Promise" this time
  const wrapped = fetch(`${base}/coins-promise`);
  await new Promise((r) => setTimeout(r, 100));
  start = Date.now();
  await fetch(`${base}/fast`);
  console.log(`/fast behind a Promise-wrapped: ${secs(Date.now() - start)}`);
  await wrapped;

  process.exit(0);
}

// ---------- server process ----------
function countCoins() {
  // ~3 seconds of pure CPU work: the teller counting coins himself
  const until = Date.now() + 3000;
  let coins = 0;
  while (Date.now() < until) coins++;
  return coins;
}

const server = http.createServer((req, res) => {
  if (req.url === '/coins') {
    countCoins();
    return res.end('coins counted');
  }
  if (req.url === '/coins-promise') {
    // The myth: "I wrapped it in a Promise, so it won't block"
    Promise.resolve().then(countCoins).then(() => res.end('coins counted'));
    return;
  }
  res.end('hi'); // instant for everyone else
});

server.listen(0, () => {
  const { port } = server.address();
  const client = fork(fileURLToPath(import.meta.url), ['client', `http://localhost:${port}`]);
  client.on('exit', () => server.close());
});
