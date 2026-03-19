---
name: handle-slack-events
description: Route Slack events to the appropriate handler skill based on event type. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive events from any "slack/" source!
---

# Handling Slack events

The slack exporter produces events under various `slack/` sources. Each source follows the pattern `slack/<type>/<stream>`, for example `slack/message/updated` or `slack/reaction/updated`.

Events from `/created` streams, certain metadata types (`user`, `unread_marker`, `channel`), and channels listed in `ignored_channel_ids.txt` are all pre-filtered by `scripts/filter_slack_events.py` before they reach you. See the `ignore-channels` skill for how to manage the ignored channels list.

You may receive multiple events for the same message (e.g., if the message was edited). This is fine -- just triage the message again with the updated content. This should be fairly rare.

Route each event based on its `type` field.

## Event types and routing

### Messages and replies

**Types:** `message`, `reply`

**Sources:** `slack/message/updated`, `slack/reply/updated`

These are new or updated messages and thread replies from Slack channels.

Use the **`handle-slack-messages`** skill to handle these.

### Reactions

**Type:** `reaction`

**Source:** `slack/reaction/updated`

These are items the user has reacted to with an emoji in Slack.
This is how the user signals that they want one of the actions from the [emoji key](../../emoji_key.md) to be taken.

Use the **`handle-slack-reactions`** skill to handle these.

### Self identity

**Type:** `self_identity`

**Source:** `slack/self_identity/updated`

The authenticated user's own Slack identity.

**What to do:** Store this in memory if not already known -- it tells you who "the user" is in Slack so you can distinguish their own messages from others. No further action needed.

## Guidelines

- Always check the `type` field to route correctly. Do not assume all slack events are messages!
- For event types not listed above, use your `handle-unknown-events` skill.
- Process messages and replies before reactions, since a reaction may reference a message you haven't triaged yet.
