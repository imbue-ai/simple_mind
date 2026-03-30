---
name: delegate-task-to-agent
description: Create a sub-agent to perform a task. Use when you need to delegate work to another agent, for example, a working agent (for actually accomplishing some task) or a verifying agent (for deciding what to do about the output of a working agent).
---

# The process for delegating tasks to sub-agents

As the thinking agent, you should NEVER do work directly.
Instead, delegate all tasks to sub-agents via `mngr create`.

## 1. Check remaining worker capacity

Before creating a new task, first run:

```bash
mngr list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\" --format jsonl
```

In order to see how many agents (besides yourself) are currently active (ie, not archived).
If there are stopped agents in the list that no longer matter, they can be moved to the archive by running `mngr archive <agent-id>`

If there are more than `max_concurrent_workers` (see [minds.toml](../../../minds.toml)) workers running, create a ticket using your `create-ticket` skill **instead** of creating a new agent.
Be sure to save enough information and context in the ticket so that you will be able to delegate the work once there is more capacity.

If there are not too many workers already running, read on for how to create different types of agents.

## 2. Check for uncommitted changes

Note that you may need to commit first (if your working directory has uncommitted changes).

This ensures that the new agent's branch has the same base commit as the current agent, which allows the verifying agent to do a proper diff later on.

## 3. Creating the right type of agent

You need to create the right type of agent for the task at hand--either a working agent to do the work, or a verifying agent to check work that was done by a working agent.

### Creating a working agent

To delegate a task, create a sub-agent using `mngr`.
By default, sub-agents are created as copies of the current agent harness with a different role.
Use `--env ROLE=working` to create a working agent.

**Use the ticket file as the task message file.** Since tickets already contain the title, description, acceptance criteria, and context, pass the ticket's markdown file directly via `--message-file`. 
There is no need to create a separate instructions file.

Before passing the ticket file, make sure it has all the details the working agent will need:
- Clear description of what to do and why
- Relevant context (conversation IDs, prior attempts, constraints, links)
- Specific success/acceptance criteria

If the ticket is missing any of these, update it first with `tk edit <ticket-id>` or `tk add-note <ticket-id>`.

The ticket files live at `.tickets/<ticket-id>.md`. Pass this path directly:

```bash
./skills/delegate-task-to-agent/create_working_agent.sh <task-name> .tickets/<ticket-id>.md <ticket-id>
```

If you are creating a working agent for something that does **not** have a ticket (rare -- you should almost always create a ticket first), write a temporary instructions file:

```bash
cat > /tmp/task-<task-name>.md << 'EOF'
# Task: <title>

## What to do
<description of what needs to be done and why>

## Context
<any relevant context: conversation IDs, prior attempts, constraints, links>

## Success criteria
<what "done" looks like -- be specific>
EOF
```

Then:

```bash
./skills/delegate-task-to-agent/create_working_agent.sh <task-name> /tmp/task-<task-name>.md
```

The `create_working_agent.sh` script handles setting the correct env vars (`ROLE=working`), agent type ("worker") and labels (`role=working`, `mind=$MIND_NAME`, and `ticket=<ticket-id>` if provided).

#### Linking agents to tickets

If this task is being done for a ticket, you **must** link them bidirectionally:

1. **Agent -> ticket**: Pass the ticket ID as the third argument to `create_working_agent.sh`. This sets a `ticket=<ticket-id>` label on the agent.
2. **Ticket -> agent**: Add a note to the ticket with the agent ID:
   ```bash
   tk add-note <ticket-id> "Working agent <agent-id> created"
   ```

This bidirectional linking ensures that if the system restarts, you can always reconstruct what was happening by checking agent labels (to find the ticket) or ticket notes (to find the agents).

The `<task-name>` should be a descriptive name for the task (e.g. `fix-login-bug`, `add-search-feature`).
Note that the names *must* be unique because git branches are created for each task.
If the command fails because the name is taken, simply choose a more specific, longer name.

### Creating a verifying agent

When a working agent finishes successfully (you will receive an `mngr/agent_states` event), create a verifying agent to check the work.
Use `--env ROLE=verifying`.
See the `verify-task-result` skill for the full details on what to include in the message file.

### Dealing with errors

If there are any errors while creating an agent, go investigate them!
Don't simply try launching another agent--figure out what went wrong and fix it before trying again.

## 4. Logging the task

Whenever you create a new agent, post to the **Work Log** (see `send-message-to-user` skill) with a brief entry, e.g.:

```
Created working agent <agent-name> for: <short description of what it's doing>
```

or for verifiers:

```
Created verifying agent <agent-name> to verify: <what's being verified>
```

If the user asked for the task to be created, you should reply to the original conversation as well with something like:

```
<NEW_TASK name="(full-sub-agent-name)">(a short description of what you're trying to accomplish with the task)</NEW_TASK>
```

# Guidelines

- Always give tasks clear, descriptive names so they are easy to track.
- Always include success criteria in your task instructions.
- Never allow more than `max_concurrent_workers` tasks to be running concurrently.
- Remember to commit before creating any task
