# Emoji Key

This document defines the emoji reactions that users can apply to Slack messages to trigger actions.

For all actions, be sure to link back to the original message for context.

## Save for later :bookmark:

- **When to use:** A message that contains content to read or watch (eg a linked article, video, or long message)
- **What to do:** Use your `save-for-later` skill to add to the user's content list (tagged as "from-slack", as well as with the channel, and the person who posted it)

## Draft reply :writing_hand:

- **When to use:** A message that needs requires a thoughtful written response from the user
- **What to do:** Use your `draft-reply` skill to draft a few alternative replies to the message that the user will be able to see later

## Create task :memo:

- **When to use:** A message either directly requires the user to do something, or which, by implication, would require me to do something
- **What to do:** Extract the action item(s) and use your `create-user-todo` skill to create the task(s).

## Urgent :fire:

- **When to use:** A message that needs immediate attention
- **What to do:** User your `notify-user` skill to notify the user immediately

## Save info :star:

- **When to use:** A message containing useful information worth remembering
- **What to do:** Extract the key information and use your `save-useful-information` skill to save it to the user's knowledge base / memory

## Schedule meeting :calendar:

- **When to use:** A message where a meeting or live chat would be the best next step
- **What to do:** Use your `send-slack-message` skill to send a message tagging @Brandi to schedule a meeting with the relevant people

## Delegate :arrow_right:

- **When to use:** A task that is nominally directed at me, but which doesn't strictly require me
- **What to do:** Use your `send-slack-message` skill to send a message tagging @Cathy to either get it done or hand it off to the right person
