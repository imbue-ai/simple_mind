---
name: list-channel-unread
description: List channels with their unread message counts. Use when you need to see how many unread messages exist per channel, or to find channels with a backlog.
---

# Listing unread counts

Run:

```bash
python3 scripts/channel_unread.py
```

Requires `SLACK_EVENTS_DIR` to be set.

Outputs one line per channel that has unread messages, sorted by unread count (highest first).

To list the individual unread message event IDs for a specific channel, use:

```bash
python3 skills/gather-slack-context/list_unread_messages.py <channel_name>
```
