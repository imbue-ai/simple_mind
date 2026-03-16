---
name: create-message-handling-skill
description: Create a new skill to handle a previously-unknown type of event (eg, from an unknown source). Use in order to generate the appropriate skill for the user, and ensure that such messages will be received (by removing the source name from the "ignored_sources.txt" file if it is there).
---

If instructed to handle a new "source" or type of events, you should ask the user how to do so.
Continue chatting with the user (via the `send-message-to-user` skill) to elicit the necessary information for you to make a *minimal* skill.
Once you have enough information, use the `delegate-task-to-agent` skill to create an agent whose task is to write the new skill.

**Be sure to pass all relevant context and information to the working agent** so that it can write the skill without needing to ask the user for more information.
