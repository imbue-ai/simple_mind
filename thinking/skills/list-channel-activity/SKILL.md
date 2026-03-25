---
name: list-channel-activity
description: List Slack channels sorted by most recent message activity. Use when you need to know which channels have been active recently, or to get an overview of channel activity.
---

# Listing channel activity

Run:

```bash
python3 scripts/channel_activity.py
```

Outputs one line per channel, sorted from most recently active to least, with the timestamp of the last message or reply.
