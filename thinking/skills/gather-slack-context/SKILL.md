---
name: gather-slack-context
description: Gather relevant context for a Slack message or reply, including the message text, sender info, channel info, and thread context. Used by other slack-related skills before making decisions about a message.
---

# Gathering Slack context

Before triaging a message or acting on a reaction, you need context about the message and its surroundings.

## How to gather context

Run the context assembly script:

```bash
./skills/gather-slack-context/gather_slack_context.py <event_id> <channel_name> <message_ts>
```

This outputs relevant context as JSON, including:
- The full message text
- The sender's name and role
- The channel name and purpose
- Recent thread context (for replies)

## Additional context to consider

Beyond what the script provides, you should also check your memory for:
- User preferences about this channel (e.g., importance level, whether to triage it at all)
- Information about the sender (e.g., their relationship to the user, their role)
- Any prior triage results for related messages (e.g., other messages in the same thread)
