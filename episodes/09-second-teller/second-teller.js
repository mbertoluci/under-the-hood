/**
 * The bank hires a second teller.
 *
 * Episode 08 showed CPU work freezing every request. The fix: move the
 * counting to a Worker Thread — a real second thread with its own
 * JavaScript engine — and let the main teller keep serving the line.
 *
 * One file, three roles:
 *   - worker thread: the second teller, counts the coins
 *   - server:        main teller, serves /fast and delegates /coins
 *   - client (fork): separate process, so the stopwatch stays honest
 *
 * Run:
 *   node episodes/09-second-teller/second-teller.js
 */

import http from 'node:http';
import { fork } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { Worker, isMainThread, parentPort } from 'node:worker_threads';

const FILE = fileURLToPath(import.meta.url);
const secs = (ms) => `${(ms / 1000).toFixed(2)}s`;

function countCoins() {
  // ~3 seconds of pure CPU work
  const until = Date.now() + 3000;
  let coins = 0;
  while (Date.now() < until) coins++;
  return coins;
}

if (!isMainThread) {
  // ---------- the second teller (worker thread) ----------
  countCoins();
  parentPort.postMessage('coins counted');
} else if (process.argv[2] === 'client') {
  // ---------- client process ----------
  const base = process.argv[3];

  const blocking = fetch(`${base}/coins-main-teller`);
  await new Promise((r) => setTimeout(r, 100));
  let start = Date.now();
  await fetch(`${base}/fast`);
  console.log(`/fast while MAIN teller counts:   ${secs(Date.now() - start)}`);
  await blocking;

  const delegated = fetch(`${base}/coins-second-teller`);
  await new Promise((r) => setTimeout(r, 100));
  start = Date.now();
  await fetch(`${base}/fast`);
  console.log(`/fast while SECOND teller counts: ${secs(Date.now() - start)}`);
  await delegated;

  process.exit(0);
} else {
  // ---------- server (main teller) ----------
  const server = http.createServer((req, res) => {
    if (req.url === '/coins-main-teller') {
      countCoins(); // episode 08 all over again
      return res.end('counted at the counter');
    }
    if (req.url === '/coins-second-teller') {
      const teller = new Worker(FILE); // hire the second teller
      teller.once('message', () => res.end('counted in the back room'));
      return;
    }
    res.end('hi');
  });

  server.listen(0, () => {
    const { port } = server.address();
    const client = fork(FILE, ['client', `http://localhost:${port}`]);
    client.on('exit', () => server.close());
  });
}
