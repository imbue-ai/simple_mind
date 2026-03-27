---
name: debugging-mngr-tasks
description: Run commands to explore the current state of mngr and any relevant running agents. Use this skill when you need to debug issues with mngr tasks, or understand what tasks are currently running and their states.
---

# Debugging mngr tasks

If something seems to have gone wrong with a given task, `mngr` provides a variety of commands that can make it easier to see what is happening.

You can always learn more about `mngr` and its commands by running `mngr --help` or `mngr <command> --help` for a specific command.

## Useful mngr commands

- `mngr list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\"" --format jsonl` - see all running agents and their states (and exclude all archived agents and yourself from the list so you can focus on the agents that matter)
- `mngr message <agent> -m "..."` - send a follow-up message to an agent
- `mngr archive <agent>` - stop an agent and remove it from the list of agents (note that an agent's logs and data will still be accessible after this)
- `mngr exec <agent> "command"` - run a shell command on an agent's host
- `mngr events <agent>` - see the logs or events for a given agent
- `mngr capture <agent>` - effectively calls `tmux capture-pane` on the agent's tmux pane, so you can see the most recent output from that agent

## Debugging process

Start by running `mngr list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\"" --format jsonl` to see all currently running agents (besides yourself) and their states, or `mngr capture <agent> --full` to see the full output from a given agent.
This can often give you a good sense of what is happening and where things might be going wrong.

**NEVER** run commands on any agents other than those that you created yourself!
