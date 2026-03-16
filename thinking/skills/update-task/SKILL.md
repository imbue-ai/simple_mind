---
name: update-task
description: Forward new information to a running agent, or adjust a task based on changed requirements. Use when the user provides additional context, clarifications, or changed requirements for an in-flight task.
---

# Updating an in-flight task

When new information arrives that is relevant to a task that is already running (or waiting), you need to decide what to do with it. The right action depends on how significant the update is.

## Step 1: Identify the affected agent(s)

Figure out which running agent(s) the new information applies to. If you have multiple agents in flight, the update might apply to one, several, or none of them. Use `mng list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\" --format jsonl` and your memory of what each agent is working on to determine this.

If the update doesn't apply to any running task, it might be context for a future task -- store it in memory (if relevant) and move on.

## Step 2: Decide the severity of the update for each agent

### Minor update: forward the information

If the new information is supplementary (e.g., a clarification, an additional detail, a pointer to a resource), forward it to the agent via `mng message`:

```bash
mng message <agent-id> --message "<additional context>" >& /tmp/`cat /proc/sys/kernel/random/uuid`.message_output &
```

Note: if the agent is not currently running (e.g., it is stopped or paused), `mng message` will start it and deliver the message once it comes online. This may take a while, so run the command in the background and check that it succeeded afterward (the above command shoves the output somewhere so that it can be inspected later).

### Major update: restart the task

If the update fundamentally changes what the task should accomplish (e.g., different goals, different success criteria, "do Y instead of X"), then the running agent's work may no longer be relevant. In this case:

1. Archive the current agent: `mng archive -f <agent-id>`
2. Create a new agent with revised instructions using your `delegate-task` skill, incorporating the new information from the start
3. Notify the user that you're restarting the task with updated instructions

Use your judgment here -- if the agent is nearly done and the change is small enough to course-correct, forwarding a message may be better than restarting from scratch. But if the agent has been working under fundamentally wrong assumptions, a fresh start with correct instructions will be faster and produce better results.

### Cancellation: stop the task

If the user's message makes it clear the task is no longer needed (e.g., "never mind", "don't bother", "I already did it"), archive the agent and move on:

```bash
mng archive -f <agent-id>
```

Acknowledge the cancellation to the user via `send-message-to-user`, and check if there is now capacity to launch a pending ticket (via `list-tickets`).
