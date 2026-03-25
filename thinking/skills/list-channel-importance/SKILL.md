---
name: list-channel-importance
description: Rank channels by the importance of their unread messages (based on triage scores). Use when you need to decide which channel to focus on next, or to report on what needs attention.
---

# Listing channel importance

Run:

```bash
python3 scripts/channel_importance.py
```

Outputs one line per channel that has unread messages, sorted by the maximum importance score of any unread message in that channel. Channels whose messages have not yet been triaged are listed at the bottom.
