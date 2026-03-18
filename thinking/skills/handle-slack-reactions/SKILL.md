---
name: handle-slack-reactions
description: Handle emoji reactions from the user on Slack messages. When the user reacts to a message with an emoji from the emoji key, execute the corresponding action.
---

# Handling Slack reactions

When the user reacts to a Slack message with an emoji, the slack exporter captures it as a `reaction` event.
If the emoji matches one from the [emoji key](../../emoji_key.md), you must execute the corresponding action.

## Step 1: Identify the emoji

Check the reaction event's emoji name against the emoji key:

| Emoji name | Action |
|------------|--------|
| `bookmark` | Save for later |
| `writing_hand` | Draft reply |
| `memo` | Create task |
| `fire` | Urgent -- notify immediately |
| `star` | Save info |
| `calendar` | Schedule meeting |
| `arrow_right` | Delegate |

If the emoji does not match any of these, ignore the reaction -- the user is just reacting normally in Slack.

## Step 2: Find the referenced message

The reaction event contains the message that was reacted to.
Look up whether you have already triaged this message (check `handled_slack_messages/events.jsonl` for a matching `message_ts` and `channel`).

If you have already triaged it, you can use the existing triage context.
If not, gather context using the `handle-slack-messages` skill's context gathering step first.

## Step 3: Execute the action

Follow the action described in the [emoji key](../../emoji_key.md) for the matched emoji.
The user has explicitly requested this action, so execute it regardless of what your triage scores would have been.

## Step 4: Mark the event as handled

Use the `mark-events-handled` skill to mark the reaction event as handled:

```bash
./skills/mark-events-handled/handle_event.sh <event_id> \
  --summary "User reacted with :<emoji>: -- executed <action>" \
  --confidence 0.95
```
