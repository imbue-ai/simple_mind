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

### Messages

**Type:** `message`

**Source:** `slack/message/updated`

These are new or updated top-level messages in Slack channels.

Use the **`handle-slack-messages`** skill to handle these.

### Relevant thread replies

**Type:** `relevant_thread_reply`

**Source:** `slack/relevant_thread_reply/updated`

These are replies in threads that are relevant to the user -- specifically, threads where the user has replied or was @mentioned. Plain `reply` events (which cover *all* threads) are pre-filtered out; you will only see `relevant_thread_reply` events.

Use the **`handle-slack-messages`** skill to handle these (same as messages).

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

## Identifying the user

The user's Slack username and user ID can be found in the self identity event data at `$SLACK_EVENTS_DIR/self_identity/updated/events.jsonl`. Each event has `user_id` and `user_name` fields at the top level. For example:

```bash
tail -1 "$SLACK_EVENTS_DIR/self_identity/updated/events.jsonl" | python3 -c "import json,sys; e=json.loads(sys.stdin.read()); print(e['user_name'], e['user_id'])"
```

Scripts that need to know the user's identity (e.g., to detect `is_from_self`) should read it from this file. See `gather_slack_context.py`'s `get_self_user_id()` for an example.

## Guidelines

- Always check the `type` field to route correctly. Do not assume all slack events are messages!
- For event types not listed above, use your `handle-unknown-events` skill.
- Process messages and replies before reactions, since a reaction may reference a message you haven't triaged yet.
