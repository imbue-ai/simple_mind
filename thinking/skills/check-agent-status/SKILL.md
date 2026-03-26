---
name: check-agent-status
description: Check the current status of a specific mng agent. Use when you need to see an agent's state, labels, or other metadata.
---

# Checking agent status

To see the current status of a specific agent, use `mng list` with an `--include` filter:

```bash
mng list --include 'id == "<agent-id>"' --format jsonl
```

This returns the agent's full metadata as JSON, including its state, labels, host, and other details.

## Common queries

### Check a specific agent's state

```bash
mng list --include 'id == "<agent-id>"' --format jsonl
```

### List all your active (non-archived) agents

```bash
mng list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\"" --format jsonl
```

### Check an agent's labels (role, ticket, etc.)

```bash
mng list --include 'id == "<agent-id>"' --format jsonl | jq .labels
```

### See an agent's recent output

```bash
mng capture <agent-id>
```

### Read an agent's transcript

```bash
mng transcript --format=jsonl --role=user --role=assistant <agent-id> | tail -n 20
```

## Important

**Do NOT guess or invent `mng` commands.** If you're unsure how to do something with `mng`, use the `using-mng` skill to look it up.
