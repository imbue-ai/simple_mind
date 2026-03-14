---
name: debugging-mng-tasks
description: Run commands to explore the current state of mng and any relevant running agents. Use this skill when you need to debug issues with mng tasks, or understand what tasks are currently running and their states.
---

# Debugging mng tasks

If something seems to have gone wrong with a given task, `mng` provides a variety of commands that can make it easier to see what is happening.

You can always learn more about `mng` and its commands by running `mng --help` or `mng <command> --help` for a specific command.

## Useful mng commands

- `mng list` - see all running agents and their states
- `mng message <agent> -m "..."` - send a follow-up message to an agent
- `mng destroy <agent>` - clean up a finished or failed agent
- `mng exec <agent> "command"` - run a shell command on an agent's host
- `mng events <agent>` - see the logs or events for a given agent
- `mng capture <agent>` - effectively calls `tmux capture-pane` on the agent's tmux pane, so you can see the most recent output from that agent

## Debugging process

Start by running `mng list` to see all currently running agents and their states, or `mng capture <agent> --full` to see the full output from a given agent. This can often give you a good sense of what is happening and where things might be going wrong.

**NEVER** run commands on any agents other than those that you created yourself!
