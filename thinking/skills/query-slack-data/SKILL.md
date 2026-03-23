---
name: query-slack-data
description: Query or analyze Slack event data in ways not covered by existing scripts. Use when you need to answer a question about the Slack data that no existing script handles.
---

# Querying Slack data

When you need to answer a question or perform an analysis on the Slack event data that isn't covered by an existing script, write a new Python script to do it.

## Before writing a new script

Check if an existing script or skill already does what you need:

- **Channel activity**: `scripts/channel_activity.py` -- channels sorted by recent activity
- **Channel importance**: `scripts/channel_importance.py` -- channels ranked by triage importance scores
- **Channel unread counts**: `scripts/channel_unread.py` -- unread message counts per channel
- **Event filtering**: `scripts/filter_slack_events.py` -- filter event streams
- **Message context**: `skills/gather-slack-context/gather_slack_context.py` -- full context for a single message
- **Unread message IDs**: `skills/gather-slack-context/list_unread_messages.py` -- list unread event IDs for a channel
- **Message selection**: `skills/backfill-slack-triage/select_messages.py` -- select messages by unread/last N/since date

## Writing a new script

If none of the above cover your need, write a new script in `scripts/`. Follow these conventions from the existing scripts:

1. Read `SLACK_EVENTS_DIR` from the environment (fall back to `$MNG_AGENT_STATE_DIR/events/slack`)
2. Use the `load_jsonl(path)` pattern for reading event files
3. Event data lives under `$SLACK_EVENTS_DIR/<type>/<stream>/events.jsonl` where type is singular (e.g., `message`, `relevant_thread_reply`, `user`, `channel`, `reaction`, `unread_marker`, `self_identity`) and stream is `created` or `updated`
4. Output should be human-readable (one line per result) or JSON, depending on the use case
5. Keep it simple -- these scripts are tools, not frameworks

Look at the existing scripts for examples of common patterns like building user/channel maps, deduplicating events, and working with Slack timestamps.
