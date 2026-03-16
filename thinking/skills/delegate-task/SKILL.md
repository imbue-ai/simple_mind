---
name: delegate-task
description: Create a sub-agent to perform a task. Use when you need to delegate work to another agent, for example, a working agent (for actually accomplishing some task) or a verifying agent (for deciding what to do about the output of a working agent).
---

# Delegating tasks to sub-agents

As the thinking agent, you should NEVER do work directly. Instead, delegate all tasks to sub-agents via `mng create`.

## Check remaining worker capacity

Before creating a new task, first run:

```bash
mng list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\" --format jsonl
```

In order to see how many agents (besides yourself) are currently active (ie, not archived).
If there are stopped agents in the list that no longer matter, they can be moved to the archive by running `mng archive <agent-id>`

If there are more than `max_concurrent_workers` (see [minds.toml](../../../minds.toml)) workers running, create a ticket using your `create-ticket` skill **instead** of creating a new agent.
Be sure to save enough information and context in the ticket so that you will be able to delegate the work once there is more capacity.

If there are not too many workers already running, read on for how to create different types of agents.

## Creating a working agent

To delegate a task, create a sub-agent using `mng`. By default, sub-agents are created as copies of the current agent harness with a different role. Use `--env ROLE=working` to create a working agent:

```bash
mng create "$MNG_AGENT_NAME-<task-name>" --env ROLE=working --message "Your task instructions here"
```

The `<task-name>` should be a descriptive name for the task (e.g. `fix-login-bug`, `add-search-feature`).
Note that the names *must* be unique because git branches are created for each task.
If the command fails because the name is taken, simply choose a more specific, longer name.

By convention (as shown above), the task name should start with your agent name (this helps make it more obvious which tasks belong to which minds)

The `--message` flag sends an initial prompt to the agent describing what work to do. Be specific and include:
- What the task is and why it needs to be done
- Any relevant context (e.g. related conversation IDs, prior attempts, constraints)
- Success criteria so the agent (and later the verifier) knows what "done" looks like

If the task description would be really long, you can use `--message-file` instead (and write to a random file in `/tmp`)

## Creating a verifying agent

When a working agent finishes successfully (you will receive an `mng/agent_states` event), create a verifying agent to check the work. Use `--env ROLE=verifying`:

```bash
mng create $MNG_AGENT_NAME-verify-<task-name> --env ROLE=verifying --message "Verify that the following task was completed successfully: <description>. The agent that performed the work was <agent-name>. Check <specific things to verify>."
```

The same comments above apply--if the message would be really long, use the `--message-file` argument instead, and be sure to include **everything** that the verification agent might need.

## Notifying the user

Whenever you create a new task, always use your `send-message-to-user` skill to send a special message like this:
```
<NEW_TASK name="(full-sub-agent-name)">(a short description of what you're trying to accomplish with the task)</NEW_TASK>
```

## Guidelines

- Always give tasks clear, descriptive names so they are easy to track.
- Always include success criteria in your task instructions.
- Never allow more than `max_concurrent_workers` tasks to be running concurrently.
