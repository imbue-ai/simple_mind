---
name: search-event-history
description: Search through past events in the event log files. Use when you need to look up something that happened previously but didn't store in memory.
---

# Searching event history

Event logs are stored as JSONL files under `$MNG_AGENT_STATE_DIR/events/<source>/events.jsonl`. You can search them using standard tools like `grep` and `jq`.

**Be careful about how much data you load into context.** Event files can be very large, and individual events can contain large payloads. Always inspect the *shape and size* of the data before loading full content.

**You should generally prefer to use sub-agents or your `delegate-task-to-agent` skill for larger or more complex explorations of event history**, but for quick lookups or simple queries, see below for some tips on how to search event logs directly.

## Step 1: Find which sources exist

```bash
( cd $MNG_AGENT_STATE_DIR/events/ && find -name events.jsonl -printf '%h\n' | sed 's|^\./||' )
```

## Step 2: Understand the data before loading it

Before reading event content, check how large the fields are to avoid pulling huge payloads into context:

```bash
# See the size (in characters) of each field for each event
cat "$MNG_AGENT_STATE_DIR/events/<source>/events.jsonl" | tail -20 | jq -c '[to_entries[] | .value = (.value | tojson | length)] | from_entries'
```

This tells you which fields are small (IDs, timestamps) and which are large (content, data payloads). Only load the fields you actually need.

## Step 3: Search with targeted queries

### Find events matching a pattern

```bash
grep '<pattern>' "$MNG_AGENT_STATE_DIR/events/<source>/events.jsonl" | jq -c '[to_entries[] | .value = (.value | tojson | length)] | from_entries'
```

### Extract specific fields only

When you know which fields you need, use `jq` to select only those fields:

```bash
# Get just timestamps and event types from recent events
tail -50 "$MNG_AGENT_STATE_DIR/events/<source>/events.jsonl" | jq -c '{timestamp, type, event_id}'

# Get message metadata without loading content
tail -50 "$MNG_AGENT_STATE_DIR/events/messages/events.jsonl" | jq -c '{timestamp, conversation_id, role, event_id}'

# Get content only for a specific conversation
grep '<conversation-id>' "$MNG_AGENT_STATE_DIR/events/messages/events.jsonl" | jq -c '{role, content}'
```

### Find events for a specific agent

```bash
grep '"<agent-id>"' "$MNG_AGENT_STATE_DIR/events/mng/agent_states/events.jsonl" | jq -c '{timestamp, state, event_id, agent_id}'
```

### Find events in a time range

```bash
# Events after a specific timestamp
cat "$MNG_AGENT_STATE_DIR/events/<source>/events.jsonl" | jq -c 'select(.timestamp > "2026-03-15T00:00:00")' | jq -c '[to_entries[] | .value = (.value | tojson | length)] | from_entries'
```

## Guidelines

- **Always limit output.** Use `tail`, `head`, or `jq` `select()` to avoid loading entire log files into context, and use ` | jq -c '[to_entries[] | .value = (.value | tojson | length)] | from_entries'` to restrict to just field sizes.
- **Inspect field sizes first.** Use the field-size query (step 2) before deciding which fields to load. A `content` field might be thousands of characters or more.
- **Load only the fields you need.** Use `jq` to project specific fields rather than loading full events.
- **For aggregate event files** (referenced by `aggregate_events` paths in aggregate events), be especially cautious -- always inspect field sizes before loading content.
