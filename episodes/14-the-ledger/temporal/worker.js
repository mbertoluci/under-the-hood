// The worker hosts the workflow + activities. It is stateless and disposable:
// kill it with `kill -9` at any moment. The durable state lives on the Temporal
// server, so a fresh worker picks the conversation right back up.

import { Worker } from '@temporalio/worker';
import { fileURLToPath } from 'node:url';
import * as activities from './activities.js';

const worker = await Worker.create({
  workflowsPath: fileURLToPath(new URL('./workflows.js', import.meta.url)),
  activities,
  taskQueue: 'the-ledger',
});

console.log('worker up on task queue "the-ledger".');
console.log('→ try it: kill -9 this process while the payment step runs, then start it again.');

await worker.run();
