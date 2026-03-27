---
name: check-agent-status
description: Check the current status of a specific mngr agent. Use when you need to see an agent's state, labels, or other metadata.
---

# Checking agent status

To see the current status of a specific agent, use `mngr list` with an `--include` filter:

```bash
mngr list --include 'id == "<agent-id>"' --format jsonl
```

This returns the agent's full metadata as JSON, including its state, labels, host, and other details.

## Common queries

### Check a specific agent's state

```bash
mngr list --include 'id == "<agent-id>"' --format jsonl
```

### List all your active (non-archived) agents

```bash
mngr list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\"" --format jsonl
```

### Check an agent's labels (role, ticket, etc.)

```bash
mngr list --include 'id == "<agent-id>"' --format jsonl | jq .labels
```

### See an agent's recent output

```bash
mngr capture <agent-id>
```

### Read an agent's transcript

```bash
mngr transcript --format=jsonl --role=user --role=assistant <agent-id> | tail -n 20
```

## Important

**Do NOT guess or invent `mngr` commands.** If you're unsure how to do something with `mngr`, use the `using-mngr` skill to look it up.
