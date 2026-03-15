---
name: handle-mng-agent_states
description: Handle events from the mng/agent_states source. Use when you receive events about sub-agent state transitions (finished, waiting, done, etc).
---

If this was a "verifying" agent, review what the verifier recommended and act on it:
- If the task was completed successfully, notify the user if appropriate (using `send-message-to-user`), and clean up the working and verifying agents with `mng archive`.
- If the task needs to be retried, review the error and consider whether the instructions need to be revised before creating a new working agent.
- If the verifier recommends asking the user for clarification, do so via `send-message-to-user`.
