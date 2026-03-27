---
name: list-event-sources-and-types
description: List all event sources and types you may receive, with descriptions of their fields and meaning. Note that event types are dynamic and new sources may appear.
---

# Listing all event sources

In order to list all possible sources of events, run:

```bash
( cd $MNGR_AGENT_STATE_DIR/events/ && find -name events.jsonl -printf '%h\n' | sed 's|^\./||' )
```

# Event schemas

All events follow a standard envelope format:

```json
{"timestamp": "...", "type": "...", "event_id": "...", "source": "<source>", ...additional fields}
```

where:

- `event_id` is a unique string for the event
- `timestamp` is the time at which the event happened (the output of running `date -u +"%Y-%m-%dT%H:%M:%S.%NZ"`, eg, something like "2026-03-14T11:14:57.000000000Z")
- `source` is where the event came from, and should match precisely to the folder (under `events/`) that the events file is located in
- `type` is the specific kind of event (which determines which additional fields will exist)

logs additionally define:

- `message`, the actual text of the log message
- `level`, the logging level, one of TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL, defining how important the message is

Logs often contain additional contextual fields as well.

Most sources define their full schema in `$MNGR_AGENT_STATE_DIR/events/<source>/schema.json`, so check to see if that file exists in order to learn more about the exact fields for any given source and event type.

If a `schema.json` does not exist for a source, check for an imputed one at `$MNGR_AGENT_STATE_DIR/events/<source>/schema.imputed.json`.

If that also doesn't exist, you should do a one-time exploration of the events in that source (using the field-size inspection technique from `search-event-history`) and create an imputed schema file, then save it for next time.
