---
name: handle-messages
description: Handle events from the messages source about user or assistant messages in conversation threads. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive a message from the "messages" source!
---

### Events from the `messages` source

These events represent messages sent by the user in conversation threads. Each event includes the `conversation_id`, the `role` (which will be "user" for user messages), and the `content` of the message.

When you get a message from the user, it will *always* come with a response that was generated for you **and already sent to the user on your behalf**.

If this response is inappropriate or insufficient, you can use the `send-message-to-user` skill to follow up with the user and clarify, provide more information, or "change your mind".

Otherwise, you should treat the response as "the message you sent to the user" and **do whatever you told the user you were going to do in that message**.
For example, if you said "I'm going to start working on X now", then you should start working on X (by delegating to a sub-agent to do the work).
If you said "I need to ask you some clarifying questions before I can get started on X", then you should ask those clarifying questions (by sending a follow-up message to the user with those questions).

## Deciding what to do

When processing a user message, determine which of these categories it falls into:

**New task request**: The user is asking you to do something new. Delegate it using your `delegate-task` skill.

**Clarification or question**: The user asked something you don't understand, or the request is too complex to act on immediately. Ask clarifying questions via `send-message-to-user`.

**Update to an in-flight task**: The user is providing additional information, changed requirements, or a cancellation for work that is already in progress. Use the `update-task` skill, which covers how to forward info, restart tasks with revised instructions, or cancel them.

**Finish handling an event**: The user is responding to a question you asked or providing information you requested. The original event was probably already marked as handled, but make sure you ensure that everything was handled correctly given the new information from the user and the associated skill for handling such events.

**General conversation**: The user is chatting, providing context, or sharing information that doesn't require immediate action. Acknowledge if appropriate, and store anything useful in memory, but otherwise generally let the "talking" agent handle it.
