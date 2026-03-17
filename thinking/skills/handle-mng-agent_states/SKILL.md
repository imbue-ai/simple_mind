---
name: handle-mng-agent_states
description: Handle events from the mng/agent_states source about sub-agent state transitions (finished, waiting, done, etc). You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive a message from the "mng/agent_states" source!
---

# Events from the `mng/agent_states` source

These events represent state changes for agents, including sub-agents that you have launched via `delegate-task-to-agent`.
Each event includes the `agent_id`, the new `state`, and any relevant metadata about the transition (eg, error message if it crashed).

Note that you may get events for agents that you did not create, and you should ignore those events.

The general, high level flow of this system is to "kick off the working agent", then when it finishes successfully, "kick off the verifying agent" (both done via using the `delegate-task-to-agent` skill).
Once the verifying agent task finishes successfully, then we handle the actions recommended by the verifing agent (either by delegating task(s) to new agent(s), or, if fast, taking the actions immediately).

How to respond to each event depends on both the state that the agent transitioned into, and the type of agent that was created.

# Possible agent states

While their host is running, agents can be in one of the following states (see `AgentLifecycleState` in `imbue/mng/primitives.py` and the [agent lifecycle docs](./vendor/mng/libs/mng/docs/concepts/agents.md#lifecycle)):

- **stopped**: the agent's tmux session does not exist (it has been stopped or not yet started)
- **running**: the agent process is actively running
- **waiting**: the agent is waiting (e.g., for user input or an external event)
- **done**: the agent's process has exited (the tmux session still exists but the process has finished)
- **replaced**: a different process is running in the agent's tmux pane (unusual)

Agents run on hosts, which can be in the following states (see `HostState` in `imbue/mng/primitives.py`) and the [host lifecycle docs](./vendor/mng/libs/mng/docs/concepts/hosts.md#lifecycle):

- **building**: Building the image, etc.
- **starting**: Creating and provisioning the host, starting the agent, etc.
- **running**: While any agent is running and considered active
- **stopping**: When all agents become idle, the host is being stopped (snapshotted, host shut down)
- **paused**: Host became idle and was snapshotted/shut down (can be restarted)
- **stopped**: All agents exited or user explicitly stopped the host (can be restarted)
- **crashed**: Host shut down unexpectedly without a controlled shutdown
- **failed**: Something went wrong before the host could be created
- **destroyed**: Host gone, resources freed

If the agent's host is not in the "running" state, the agent effectively "inherits" its state from the host (e.g., we could consider the agent itself to be paused, crashed, etc).

Note that there is no "archived" state for agents--an agent is simply considered archived if it has an "archived_at" label (and is stopped).

# How to handle each state

## State: "running", "starting", "building"

You can generally ignore these.
It just means that the agent is running or in the process of starting up.

You will get another event when it finishes or if it crashes.

## State: "stopped", "done", "paused", "waiting"

This is the most common state transition you will handle.
It means the agent's process has either exited ("stopped", "done", "paused") or has finished responding to your prompt and is waiting for either additional input / for you to stop it ("waiting").

First, determine if the task is actually complete, or if the agent had questions or needs input from you.
Check for the agent's output file first:

```bash
cat output/<agent-id>/summary.md 2>/dev/null || echo "No summary.md found"
```

If no `summary.md` exists, you can try reading the agent's transcript:

```bash
mng transcript --format=jsonl --role=assistant <agent-id> | tail -n 20
```

You're looking for the agent's final summary response, which most agents print when they finish their work.

Sometimes the agent may have had a bunch of pointless system messages at the end if there were some errors, in which case you may need to look a bit further back, or restrict to just the assistant messages:

```bash
mng transcript --format=jsonl --role=assistant <agent-id> | tail -n 20
```

Once you've found the final summary response, you can determine whether the task was completed successfully, or if there were errors or questions.

### If there were errors or questions

If the agent had questions or seems to have run into some problems, then it is effectively waiting for input.

**You must spend some time actually thinking hard about the purpose of this task, your purpose and priorities, and how this task fits into the broader context.**

Once you've done that, you should either:

1. Send a message to the agent with the information it needs to proceed (e.g., answers to its questions, or suggestions on how to fix the errors) by using `mng message <agent-id> --message "(put your message here)"`
2. Abandon the task, archive the agent, and try again with a new agent (after revising the instructions). It is often useful to retry a task with a fresh agent and updated instructions if you see that the task failed for some reason that you could have prevented with better instructions. In this case, simply call `mng archive -f <agent-id>` to clean up the old agent, revise the instructions, and then create a new agent using your `delegate-task-to-agent` skill with the updated instructions.
3. Ask the user for additional information. You should generally try to avoid doing this if possible, since it adds latency and friction, but sometimes the agent has failed and you simply don't have enough information to know what to do (or even to make a reasonable guess or assumption). In such a case, use your `send-message-to-user` skill to ask the user for additional information that can help you determine how to proceed.
4. Abandon the task, stop the agent, and either inform the user that you were unable to complete the task (if they requested it), or simply move on with your other priorities if the task was something you decided to do yourself without the user's explicit request. In this case, call `mng stop <agent-id>` to stop the agent, and then check if there is now capacity to launch a pending ticket (using `list-tickets` to check for ready tickets).

### If the agent believes the task is complete

If the agent seems to believe it has completed the task, then the next steps depend on what type of agent this is.

If this was a "working" agent, use the `verify-task-result` skill to check whether the task was completed successfully.
This will create a verifying agent to review the work.

If this was a "verifying" agent, use your `handle-verification-result` skill to review the verifier's recommendations and decide what to do next.

## State: "crashed"

This state indicates that the underlying infrastructure causes the agent's host to crash.

If a recent snapshot of the host is available (call `mng snapshot list <agent-id>` to check), you can restore from the snapshot and restart the agent, and then tell it to resume its work (by using something like `mng message <agent-id> --message "Please continue"`).

If there were no snapshots (rare), you should archive that agent (using `mng archive -f <agent-id>`) and then create a new agent to redo the work (using your `delegate-task-to-agent` skill with the same instructions, or revised instructions if you think that would help).

If this happens repeatedly, you should investigate the underlying cause of the crashes (if possible), or use your `dealing-with-the-unexpected` skill to submit a bug report to the developers so they can investigate and fix the underlying issue.

## State: "failed"

This state indicates that something went wrong before the host could be created, eg, while building the image or starting the host.

This is typically a problem with the dockerfile or other build instructions.
You should investigate your local `mng` logs and see what the actual error was, and then fix the underlying issue (e.g., by fixing the dockerfile or build instructions) before ultimately trying again (by creating a new agent with the same instructions using your `delegate-task-to-agent` skill).

## State: "stopping"

This state is transient and can be ignored.

## State: "destroyed"

This state is the result of calling `mng destroy`, and can be safely ignored.

## State: "replaced"

This is unusual and typically indicates that `mng` believes that the agent process ID has shifted since it was first launched.
This typically happens if there is a bug in the `mng` `Agent` class implementation.

You can investigate with `mng capture` and consider archiving and recreating the agent if necessary (eg, if this is transient)
You may need to fix the underlying agent or code so that `mng` is able to track the agent process (if this is a persistent issue).

## General guidelines

- When a task fails or crashes, review the error before retrying. Use `mng capture <agent-id> --full` to see what happened. Consider whether the instructions need to be revised.
- Clean up finished agents with `mng f archive` after you have processed their results.
- After processing any agent state event, check if there is capacity to launch a pending ticket (via `list-tickets`).
- Notify the user about significant state changes according to their notification preferences
- After some tasks have been stopped/archived/destroyed, remember to check if there is now capacity to launch a pending ticket (using `list-tickets` to check for ready tickets).
