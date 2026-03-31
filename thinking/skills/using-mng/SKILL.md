---
name: using-mngr
description: How to use the mngr command line tool correctly. Use this skill BEFORE running any mngr command you are not 100% sure about. If you are unsure how to do something with mngr, use "mngr ask" to find out.
---

# Using mngr

`mngr` is the command line tool for creating and managing agents. You use it extensively to delegate work, check agent status, and manage the agent lifecycle.

## Golden rule

**Never guess or invent mngr commands.** If you are not certain a command exists or what its flags are, use one of these two approaches:

### Option 1: Ask mngr

```bash
mngr ask "How do I <what you want to do>?"
```

This will give you the correct command and flags. Use this whenever you're unsure.

### Option 2: Check the help

```bash
mngr --help              # list all commands
mngr <command> --help    # see flags and usage for a specific command
```

## `mngr list` vs `mngr list --active`

`mngr list` shows **all** agents, including archived ones.
`mngr list --active` excludes archived agents and is what you almost always want.

Use `mngr list` (without `--active`) only when you specifically need to see archived agents, such as during cleanup operations.

## Commands you know

These are the commands you use regularly and can run confidently:

- `mngr create` -- create a new agent (see `delegate-task-to-agent` skill)
- `mngr list --active` -- list non-archived agents (see `check-agent-status` skill)
- `mngr message` -- send a message to an agent
- `mngr transcript` -- view an agent's message history
- `mngr capture` -- see the agent's tmux pane output
- `mngr archive` -- stop and archive an agent
- `mngr stop` -- stop an agent
- `mngr start` -- start a stopped agent
- `mngr exec` -- run a shell command on an agent's host
- `mngr events` -- view agent event files
- `mngr destroy` -- permanently destroy an agent
- `mngr ask` -- ask mngr how to do something

## When in doubt

Run `mngr ask "<your question>"`. It is always better to ask than to guess and fail.
