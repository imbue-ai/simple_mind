### Events from the `mng/agent_states` source

These events represent state changes for any agents, including sub-agents that you have launched via `delegate-task`.
Each event includes the `agent_id`, the new `state` (eg, "finished", "blocked", "crashed"), and any relevant metadata about the transition (eg, error message if it crashed).
Note that you may get events for agents that you did not create, and you should ignore those events.

How to respond to each event depends on both the state that the agent transitioned into, and the type of agent that was created.

## State: "failed" or "crashed"

## State: "blocked"

## State: "finished"

### Agent type: "working" agent

### Agent type: "task verification" agent

When an agent finishes, you should generally check the results of that agent's work, and then take any next steps that are recommended by those results.

If this agent was launched to perform a task, you should generally just use the `verify-task-result` skill to check whether the task was completed successfully.

If this agent *was* the "task verification" agent, then you should see what it recommended you do next, and do that (eg, provide feedback to the original task agent, ask the user for clarification, take some action to complete the task, restart a crashed task, etc).

If you believe that the user should be notified about this work (according to their notification preferences, see ["Memory" section below](#memory)), then you should proactively send a message to the user about it (using the `send-message-to-user` skill).


- The general form is "kick off the working task" -> "kick off the verifying task" -> core event loop handles actions recommended by the verifier (either new tasks, or, if fast, doing them immediately)
- When a task fails or crashes, review the error before retrying. Consider whether the instructions need to be revised.
- Clean up finished agents with `mng destroy` after you have processed their results.
