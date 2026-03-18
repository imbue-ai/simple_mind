---
name: handle-slack-events
description: Route Slack events to the appropriate handler skill based on event type. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive events from the "slack" source!
---

# Handling Slack events

The slack exporter produces events of various types under the `slack` source.
When you receive a batch of slack events, you must route each one to the appropriate handler skill based on its `type` field.

## Event types and routing

### Messages and replies

**Types:** `message`, `reply`

These are new or updated messages and thread replies from Slack channels.

Use the **`handle-slack-messages`** skill to handle these.

### Reactions

**Type:** `reaction`

These are items the user has reacted to with an emoji in Slack.
This is how the user signals that they want one of the actions from the [emoji key](../../emoji_key.md) to be taken.

Use the **`handle-slack-reactions`** skill to handle these.

### Channels

**Type:** `channel`

New or updated channel metadata (name, purpose, topic, membership).

**What to do:** ignore these events

### Users

**Type:** `user`

New or updated Slack user records.

**What to do:** ignore these events

### Unread markers

**Type:** `unread_marker`

Changes to the user's read position in a channel.

**What to do:** ignore these events

### Self identity

**Type:** `self_identity`

The authenticated user's own Slack identity.

**What to do:** Store this in memory if not already known -- it tells you who "the user" is in Slack so you can distinguish their own messages from others. No further action needed.

## Guidelines

- Always check the `type` field to route correctly. Do not assume all slack events are messages!
- For event types not listed above, use your `handle-unknown-events` skill.
- Process messages and replies before reactions, since a reaction may reference a message you haven't triaged yet.
