// decide.mjs — the LangGraph role: the REASONING GRAPH.
//
// This is what LangGraph controls: WHICH tool to call, WHEN, in what order,
// whether to loop again or stop. A tiny graph — plan -> (tools -> plan)* -> end —
// guarded by a recursion limit. Notice what is NOT here: nothing about retries,
// crashes, exactly-once, or waiting for a human. That is a different kind of
// control (see run-durable.mjs). The graph only DECIDES.

export const RECURSION_LIMIT = 20;

// The tools the agent is allowed to call. The graph only decides to CALL them;
// it makes no promise that they actually run, or run once.
export const TOOLS = {
  lookup_order: "read the order",
  check_policy: "read the refund policy",
  refund: "MOVE MONEY back to the customer",
  reply: "write the customer a message",
};

// planner node: given the current reasoning state, route to the next tool
// (or to __end__). This is the "which tool, when" decision.
function planner(state) {
  if (!state.order) return { tool: "lookup_order", args: {} };
  if (!state.policy) return { tool: "check_policy", args: {} };
  if (!state.refunded && state.eligible) return { tool: "refund", args: { amount: state.amount } };
  if (!state.replied) return { tool: "reply", args: {} };
  return { tool: "__end__", args: {} };
}

// Run the graph. Returns the ORDERED plan of tool calls the agent decided on.
// The recursion limit is the graph's safety rail against an infinite loop —
// LangGraph's real guardrail. Decision only; no side effects on the world.
export function decide(initialState) {
  const state = { ...initialState };
  const plan = [];
  for (let step = 0; step < RECURSION_LIMIT; step++) {
    const { tool, args } = planner(state);
    if (tool === "__end__") return { plan, stoppedBy: "route_to_end" };
    plan.push({ id: `${tool}#${step}`, tool, args });
    // advance only the agent's OWN reasoning state — not the outside world.
    if (tool === "lookup_order") state.order = true;
    if (tool === "check_policy") state.policy = true;
    if (tool === "refund") state.refunded = true;
    if (tool === "reply") state.replied = true;
  }
  return { plan, stoppedBy: "recursion_limit" };
}
