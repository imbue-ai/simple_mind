---
name: using-mng
description: How to use the mng command line tool correctly. Use this skill BEFORE running any mng command you are not 100% sure about. If you are unsure how to do something with mng, use "mng ask" to find out.
---

# Using mng

`mng` is the command line tool for creating and managing agents. You use it extensively to delegate work, check agent status, and manage the agent lifecycle.

## Golden rule

**Never guess or invent mng commands.** If you are not certain a command exists or what its flags are, use one of these two approaches:

### Option 1: Ask mng

```bash
mng ask "How do I <what you want to do>?"
```

This will give you the correct command and flags. Use this whenever you're unsure.

### Option 2: Check the help

```bash
mng --help              # list all commands
mng <command> --help    # see flags and usage for a specific command
```

## Commands you know

These are the commands you use regularly and can run confidently:

- `mng create` -- create a new agent (see `delegate-task-to-agent` skill)
- `mng list` -- list agents with filtering (see `check-agent-status` skill)
- `mng message` -- send a message to an agent
- `mng transcript` -- view an agent's message history
- `mng capture` -- see the agent's tmux pane output
- `mng archive` -- stop and archive an agent
- `mng stop` -- stop an agent
- `mng start` -- start a stopped agent
- `mng exec` -- run a shell command on an agent's host
- `mng events` -- view agent event files
- `mng destroy` -- permanently destroy an agent
- `mng ask` -- ask mng how to do something

## When in doubt

Run `mng ask "<your question>"`. It is always better to ask than to guess and fail.
