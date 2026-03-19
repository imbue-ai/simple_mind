---
name: ignore-channels
description: Manage which Slack channels are ignored by adding or removing channel IDs from the ignored channels list. Use when the user wants to stop receiving events from specific channels.
---

# Ignoring Slack channels

Some channels produce noise that the user doesn't want triaged (e.g., bot notification channels, high-volume channels they don't care about). You can suppress events from these channels by adding their channel IDs to `ignored_channel_ids.txt`.

## How it works

The file `ignored_channel_ids.txt` (in the `thinking/` directory) contains one Slack channel ID per line. The event filter script (`scripts/filter_slack_events.py`) drops all events from channels listed in this file before they reach you.

## Adding a channel to the ignore list

1. Find the channel ID. You can look it up from the slack event data -- channel events include both `channel_id` and `channel_name`. For example:

```bash
grep '"<channel_name>"' $SLACK_EVENTS_DIR/channel/created/events.jsonl | python3 -c "import json,sys; print(json.loads(sys.stdin.readline())['channel_id'])"
```

2. Add the channel ID to `ignored_channel_ids.txt`:

```bash
echo "<channel_id>" >> ignored_channel_ids.txt
```

3. Commit the change so it persists.

## Removing a channel from the ignore list

Edit `ignored_channel_ids.txt` and remove the channel ID. Commit the change.

## When to use

- The user explicitly asks to ignore a channel
- During onboarding, when discovering which channels are relevant
- When a channel is consistently producing low-importance noise (suggest to the user first before ignoring)
