// The workflow IS the conversation. Its code runs deterministically and its
// progress is event-sourced in the Temporal history on the server — NOT in the
// worker's memory. Kill the worker mid-run and start it again: Temporal replays
// the history, skips every activity that already completed, and continues on the
// exact same line.

import * as wf from '@temporalio/workflow';

const { validate, search, select, charge, reserveSeat, issueTicket, sendConfirmation } =
  wf.proxyActivities({
    startToCloseTimeout: '1 minute',
    retry: { maximumAttempts: 5 },
  });

export async function bookingWorkflow(session) {
  wf.log.info(`booking ${session}: started`);

  await validate(session);
  const flights = await search();
  const flight = await select(flights);
  wf.log.info(`booking ${session}: selected ${flight}`);

  // Stable idempotency key for the money step. Survives worker restarts because
  // it is derived from the durable workflow id, not from process memory.
  const idemKey = `charge-${wf.workflowInfo().workflowId}`;
  const chargeResult = await charge(session, idemKey);
  wf.log.info(`booking ${session}: ${chargeResult}`);

  await reserveSeat();
  await issueTicket();
  await sendConfirmation(session);

  return `booking ${session} complete — same context, no double reply`;
}
