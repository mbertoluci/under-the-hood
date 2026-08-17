/**
 * Serving a 2 GB file with ~50 MB of RAM.
 *
 * Two ways to serve the same giant file:
 *   /gulp  - read the WHOLE file into one buffer, then respond
 *   /straw - fs.createReadStream().pipe(res): sip it, chunk by chunk
 *
 * Fun fact: fs.readFile flat out REFUSES files of 2 GiB or more
 * (ERR_FS_FILE_TOO_LARGE). Node knows gulping is a bad idea. For the
 * demo we gulp by hand (open + read loop into one giant Buffer).
 *
 * Three processes keep the measurement honest:
 *   - a child creates the 2 GiB file (so its RAM never taints the server)
 *   - the server samples its own peak RSS while serving
 *   - a client process streams the download and discards it
 *
 * Run:
 *   node episodes/13-the-straw/big-file-server.js
 *
 * Creates a temporary 2 GiB file and deletes it when done.
 */

import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fork } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const FILE = fileURLToPath(import.meta.url);
const BIG = path.join(os.tmpdir(), 'uth-big-file.bin');
const SIZE = 2 * 1024 ** 3; // 2 GiB
const mb = (b) => `${Math.round(b / 1024 / 1024)} MB`;

if (process.argv[2] === 'makefile') {
  // ---------- file-maker process ----------
  const chunk = Buffer.alloc(8 * 1024 * 1024);
  const fd = fs.openSync(BIG, 'w');
  for (let written = 0; written < SIZE; written += chunk.length) fs.writeSync(fd, chunk);
  fs.closeSync(fd);
  process.exit(0);
} else if (process.argv[2] === 'client') {
  // ---------- client process ----------
  const base = process.argv[3];

  const drain = async (route) => {
    const res = await fetch(`${base}${route}`);
    for await (const chunk of res.body) void chunk; // discard
  };
  const peak = async () => (await fetch(`${base}/peak`)).text();
  const reset = () => fetch(`${base}/reset`);

  await reset();
  console.log(`baseline RSS:                 ${await peak()}`);

  // straw first: RSS never shrinks back after the gulp commits 2 GiB
  await reset();
  await drain('/straw');
  console.log(`/straw (createReadStream):    peak ${await peak()}`);

  await reset();
  await drain('/gulp');
  console.log(`/gulp  (whole file in RAM):   peak ${await peak()}`);

  process.exit(0);
} else {
  // ---------- server process ----------
  console.log('creating a 2 GiB file in a child process...');
  const maker = fork(FILE, ['makefile']);
  maker.on('exit', () => {
    console.log(`file size: ${mb(SIZE)}`);

    let peak = 0;
    setInterval(() => { peak = Math.max(peak, process.memoryUsage().rss); }, 25).unref();

    const server = http.createServer((req, res) => {
      if (req.url === '/reset') { peak = process.memoryUsage().rss; return res.end('ok'); }
      if (req.url === '/peak')  { return res.end(mb(peak)); }
      if (req.url === '/gulp') {
        // fs.readFile refuses >= 2 GiB (ERR_FS_FILE_TOO_LARGE), so we
        // swallow the pool by hand: one giant Buffer, filled from disk.
        (async () => {
          const buf = Buffer.alloc(SIZE);
          const fd = fs.openSync(BIG, 'r');
          let read = 0;
          while (read < SIZE) read += fs.readSync(fd, buf, read, Math.min(1 << 30, SIZE - read), read);
          fs.closeSync(fd);
          // Irony: queueing 2 GiB of writes at once kills the socket.
          // Even the WRONG solution needs backpressure just to work.
          const CH = 512 * 1024 * 1024;
          for (let i = 0; i < SIZE; i += CH) {
            if (!res.write(buf.subarray(i, i + CH))) {
              await new Promise((ok) => res.once('drain', ok));
            }
          }
          res.end();
        })();
        return;
      }
      if (req.url === '/straw') {
        fs.createReadStream(BIG).pipe(res); // sip through the straw
        return;
      }
      res.end('hi');
    });

    server.listen(0, () => {
      const { port } = server.address();
      const client = fork(FILE, ['client', `http://localhost:${port}`]);
      client.on('exit', () => {
        fs.rmSync(BIG, { force: true });
        server.close();
      });
    });
  });
}
