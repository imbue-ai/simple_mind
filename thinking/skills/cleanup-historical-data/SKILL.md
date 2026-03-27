---
name: cleanup-historical-data
description: Clean up old agents, their output directories, and other historical data. Use during nightly cleanup or when the system has accumulated stale data.
---

# Cleaning up historical data

Over time, archived agents and their output directories accumulate.
This skill describes how to clean them up.

## Destroying old archived agents

Find agents that were archived more than a week ago and destroy them:

```bash
mngr list --include "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\"" --format jsonl
```

For each agent in the list, check the `archived_at` label.
If it is more than a week old, destroy the agent:

```bash
mngr destroy -f <agent-id>
```

## Cleaning up output directories

When destroying an agent, also remove its output directory:

```bash
rm -rf output/<agent-id>
```

**Before removing**, check if the output directory contains anything that should be preserved (e.g., reports, data files, or artifacts that haven't been moved to a permanent location).
If in doubt, leave it -- it's better to have stale data than to lose something important.
