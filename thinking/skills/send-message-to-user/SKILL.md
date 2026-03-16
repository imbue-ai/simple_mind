---
name: send-message-to-user
description: Send a message to the user in a conversation thread. You MUST use this skill to reply in an existing conversation, start a new conversation, or proactively reach out.
---

# Sending messages to the user

You communicate with users through conversation threads. Each thread has a unique `conversation_id` and a human-readable name.

Users may send messages in different conversation threads (with different `conversation_id`s), and you should always *reply* in the same thread.

If you are proactively sending a message (not directly replying to a user message), you should think carefully about whether to start a new one vs use an existing conversation (and if so, which one).

Be sure to any memories about user preferences around notifications and messaging are loaded. 

## Sending a message in an existing conversation

When you want to follow up in a conversation you already know about (e.g. responding to a user message in the same thread), inject your message directly using the `llm` tool:

```bash
$MNG_AGENT_STATE_DIR/commands/chat.sh chat --reply <conversation-id> "Your message here"
```

You can find the `conversation_id` from the event you are responding to (it is included in `messages` events), or use the `list-conversations` skill. The `model` should match the model used by that conversation (also visible in the event data or conversation list).

When replying to an existing conversation, you may wish to give the user the *option* to spin out one or more new threads about some specific topic(s).
In order to do so, simply enclose your reply like this: <SUGGEST_NEW_THREAD>...</SUGGEST_NEW_THREAD>
This will be rendered in a way that makes it easy for the user to split out a new conversation thread about that topic.
You should make these suggestions whenever you either find that the conversation has become about something very specific, or if you are making suggestion(s) for work that you could do for the user or help with (especially when it would be a larger chunk of work). 
You should generally only make these suggestions from the "daily thread" (since other threads are generally already about something more specific)

When replying within an existing conversation, you may also want to *link* to one or more other previous conversation(s).
In order to do so, simply enclose your reply like this: <THREAD_LINK conversation_id="<conversation-id>">...</THREAD_LINK>
Be sure to fill in the correct conversation id!

## Starting a new conversation

When you want to proactively reach out (e.g. to notify the user about completed work, ask a question, or share an update), create a new conversation by choosing an appropriate, descriptive name:

```bash
$MNG_AGENT_STATE_DIR/commands/chat.sh --new --name "<descriptive name>" --as-agent "Your message here"
```

Choose a name that clearly describes the topic or purpose of the conversation. For example:
- "Build failure in auth module" for a bug report
- "PR #42 ready for review" for a completed task
- "Question about database migration" for a question

If a conversation with the given name already exists, your message will be added to that thread. Otherwise, a new conversation is created.

This command prints the conversation ID to stdout.

## Choosing which approach to use

- If you are responding to a user message, use `llm inject` with the same `conversation_id` from the event so your reply appears in the same thread.
- If you are proactively notifying the user about something new (completed work, a question, an update), use `chat.sh --new --name "<name>" --as-agent` with a descriptive name.
- If you want to continue an existing topic, reuse the same name to add to the existing thread.
- If you are unsure, default to starting a new conversation with a descriptive name. Short, focused threads are easier for users to follow than long, multi-topic ones.

## Tone

Match the tone of the talking agent when writing your replies. Your messages appear in the same conversation as the talking agent's responses, so they should feel consistent. If the talking agent has been casual and friendly, your follow-ups should be too. If the user is talking like a pirate, your replies should fit in.

## Asking questions

When asking questions, always provide multiple-choice suggested short answers to make it easy for the user to reply quickly:

- When asking a **single question**, give lettered answer options, ordered from most likely to least likely:
  ```
  How often would you like status updates?
  A) Only when something important happens
  B) A daily summary
  C) Every time a task completes
  D) I'll ask when I want to know
  E) Something else (describe)
  ```

- When asking **multiple questions at once**, number the questions and give lettered options for each, so the user can reply concisely (e.g., "1: C, 2: A"):
  ```
  A couple quick questions:
  1. How often would you like status updates?
     A) Only when something important happens
     B) A daily summary
     C) Every time a task completes
     D) Something else (describe)
  2. Should I start on the refactor today?
     A) Yes, go ahead
     B) Not yet, let's discuss first
     C) Something else (describe)
  ```

**Always** include a final option that encourages the user to type their own response if they want

## Other guidelines

- Keep messages concise and actionable.
- When notifying about completed work, include a summary and any relevant URLs (e.g. links to sub-agents or PRs).
- Reference the event or context that triggered the message when it helps the user understand why you are reaching out.
