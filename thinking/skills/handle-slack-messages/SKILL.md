---
name: handle-slack-messages
description: Triage Slack messages and relevant thread replies. You **MUST** use this skill whenever you receive `message` or `relevant_thread_reply` type events from a `slack/` source.
---

# Handling Slack messages

Events from `slack/message/updated` and `slack/relevant_thread_reply/updated` are routed here by the `handle-slack-events` skill. Each event is either a top-level channel message or a reply in a thread that is relevant to the user (i.e., threads where the user has replied or was @mentioned), along with metadata (channel, sender, timestamp, raw payload).

You may receive multiple events for the same message if it was edited -- just re-triage with the updated content.

You must triage each message/reply event by following the procedure below.

## Step 1: Gather context

Use the `gather-slack-context` skill to assemble the information you need to make a good triage decision for each message or reply event.

## Step 2: Score the message

For each message, you must produce the following scores (all floats from 0.00 to 1.00):

### Importance and urgency

- **importance** (0.00 - 1.00): How important is this message to the user? 0.0 = completely irrelevant, 1.0 = critically important.
- **urgency** (0.00 - 1.00): How time-sensitive is this message? 0.0 = no time pressure at all, 1.0 = needs attention right now.

### Emoji label probabilities

Score each emoji from the [emoji key](../../emoji_key.md) with the probability that it should be applied to this message. If the probability is greater than 0.5, you are saying that label *should* actually be applied.

The key for the emoji label should be the emoji name (including the leading and trailing ":"), and the values should be floats from 0.00 to 1.00

### Uncertainty

- **uncertainty** (0.00 - 1.00): How uncertain you are about your triage of this message overall. Consider: did you have enough context? Was the message ambiguous? Are you unsure about any of the scores?

If uncertainty is greater than 0.4, you **must** include one or more specific questions about what you were uncertain about (via the `--question` flag when recording the triage).

## Step 3: Record the triage result

Call the recording script once per message, passing the emoji label scores as a JSON object:

```bash
./skills/handle-slack-messages/record_slack_triage.sh <event_id> \
  --channel <channel_name> \
  --sender <sender_name> \
  --message-ts <message_ts> \
  --summary "<one-line summary of the message>" \
  --importance <0.00-1.00> \
  --urgency <0.00-1.00> \
  --labels '{ ":bookmark:": 0.10, ":writing_hand:": 0.85, ... }' \
  --uncertainty <0.00-1.00> \
  [--question "<what you were uncertain about>"]...
```

The `--labels` value is a JSON object whose keys are the emoji names from the [emoji key](../../emoji_key.md) (with colons) and whose values are the probability scores. Include an entry for every emoji in the key.

This writes a JSONL event to `$MNG_AGENT_STATE_DIR/events/handled_slack_messages/events.jsonl`.

## Step 4: Mark the original event as handled

After triaging and acting on a message, use the `mark-events-handled` skill to mark the original slack event as handled:

```bash
./skills/mark-events-handled/handle_event.sh <event_id> \
  --summary "Triaged slack message: <one-line summary>" \
  --confidence <1.0 - uncertainty>
```

## Guidelines

- Use your memory of user preferences (notification settings, channel importance, key people) to inform your scores.
- Be thoughtful about when you are applying an emoji--it could create real work for the user (e.g., creating a task, sending a notification, drafting a reply). Don't apply an emoji unless you think it's really warranted.
- Note that you should **NOT** take the actions described in the action key as part of using this skill! Your job is just to triage and label the message--the actions will happen later.
- If you notice a channel consistently producing irrelevant noise, suggest to the user that it be added to the ignore list (see the `ignore-channels` skill).
- Do not read the raw Slack event files directly. Use the existing scripts (see `query-slack-data` skill) or write a new script if needed.
