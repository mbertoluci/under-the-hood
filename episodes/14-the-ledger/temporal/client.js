// Starts (or re-attaches to) one durable conversation and waits for the result.
// The workflowId makes it addressable: run this twice with the same session and
// Temporal returns the existing run instead of starting a second one.

import { Connection, Client } from '@temporalio/client';

const session = process.argv[2] || '42';

const connection = await Connection.connect(); // defaults to localhost:7233
const client = new Client({ connection });

const handle = await client.workflow.start('bookingWorkflow', {
  args: [session],
  taskQueue: 'the-ledger',
  workflowId: `booking-${session}`,
  workflowIdReusePolicy: 'ALLOW_DUPLICATE_FAILED_ONLY',
});

console.log(`started/attached workflow booking-${session}`);
console.log('waiting for result (safe to kill the WORKER now)...');
console.log('result:', await handle.result());
