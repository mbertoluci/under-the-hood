/**
 * One thread, a thousand customers.
 *
 * The server below has ONE JavaScript thread. Every request needs
 * 1 full second of "back office" work (I/O, simulated with a timer).
 *
 * If the thread waited for each customer, 1,000 requests would take
 * 1,000 seconds. Run it and see what actually happens.
 *
 * Run:
 *   node episodes/06-event-loop-bank/one-teller.js
 */

import http from 'node:http';

const server = http.createServer((req, res) => {
  // Slow I/O-style work: delegated, the thread does NOT wait here.
  setTimeout(() => res.end('done'), 1000);
});

server.listen(0, async () => {
  const { port } = server.address();
  const CUSTOMERS = 1000;

  console.log(`one teller, ${CUSTOMERS} customers, 1s of back-office work each...`);
  const start = Date.now();

  await Promise.all(
    Array.from({ length: CUSTOMERS }, () => fetch(`http://localhost:${port}`))
  );

  const secs = ((Date.now() - start) / 1000).toFixed(1);
  console.log(`all ${CUSTOMERS} served in ${secs}s (not ${CUSTOMERS}s)`);
  server.close();
});
