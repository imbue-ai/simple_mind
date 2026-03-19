---
name: backfill-slack-triage
description: Replay the triage logic on historical Slack messages as if they were just arriving. Use when you want to test or backfill triage on messages that have already been exported (e.g., all unread messages, last N messages, messages from a time range).
---

# Backfilling Slack triage

This skill lets you run the triage logic from `handle-slack-messages` on historical messages, as if those messages were just being received. This is useful for:

- Testing how the triage logic handles real messages
- Backfilling triage data for messages that arrived before the mind was set up
- Verifying that changes to scoring or the emoji key produce reasonable results

## Step 1: Select messages

Use the selection script to get the event IDs of the messages you want to triage:

```bash
python3 ./skills/backfill-slack-triage/select_messages.py <channel_name> \
  [--unread] \
  [--last <N>] \
  [--since <YYYY-MM-DD>]
```

Options (pick one):
- `--unread` -- all unread messages (based on unread markers)
- `--last <N>` -- the most recent N messages
- `--since <YYYY-MM-DD>` -- all messages since a given date

The script prints one event ID per line to stdout.

## Step 2: Triage each message

For each event ID from step 1, follow the `handle-slack-messages` skill:

1. Use the `gather-slack-context` skill to get context for the message
2. Score it (importance, urgency, emoji labels, uncertainty)
3. Record the triage result via `record_slack_triage.sh`

**Do NOT mark these events as handled** via `mark-events-handled` -- they are historical messages being replayed, not live events. The triage results are still recorded to `handled_slack_messages/events.jsonl` so they can be reviewed.

As you are triaging messages, show each result to the user instead of marking as handled (eg, show them the importance, urgency, emoji labels, and uncertainty scores you assigned). This lets you get feedback on whether the triage logic is working as expected.

## Step 3: Review results

After triaging all of the events, print a little summary of the results, including:
- Total number of messages triaged
- Distribution of importance and urgency scores
- Most common emoji labels assigned
- Any messages that had high uncertainty (e.g., uncertainty score > 0.7) -- these are cases where the triage logic was unsure and may need improvement
