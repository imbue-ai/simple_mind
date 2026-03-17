---
name: mark-events-handled
description: Mark events as handled after processing them. You **MUST** use this skill (and *carefully follow the process in this doc*) after handling events, otherwise you will not be allowed to stop!
---

# Marking events as handled

After handling a group of events, you must mark each one as handled individually.
But first, **verify that you actually did the right thing for each event**.

## Step 1: Review what you did

Before marking anything as handled, go through each event and confirm:

- What action did you take for this event? (e.g., delegated a task, sent a message, ignored it, etc.)
- Was that the right action? Did you actually follow the appropriate skill for this event's source?

If you realize you missed something or took the wrong action for an event, **go do the right thing first** before marking it as handled.
Don't just claim you handled it.

## Step 2: Mark each event as handled

Call `handle_event.sh` **once per event**, providing metadata about how you handled it:

```bash
./skills/mark-events-handled/handle_event.sh <event_id> \
  --summary "<short description of what you did>" \
  --confidence <0.0-1.0> \
  [--ticket <ticket-id>] \
  [--message <message-id>]
```

### Required arguments

- `<event_id>` -- the `event_id` from the event you handled
- `--summary` -- a short description of *how* you handled the event (e.g., "Delegated fix-login-bug task to working agent", "Sent clarification question to user", "Ignored duplicate event")
- `--confidence` -- a float from 0.0 to 1.0 indicating how confident you are that you handled the event correctly. Use 0.9+ when you followed a clear skill and the action was straightforward. Use lower values when you had to improvise or are unsure.

### Optional arguments (repeatable)

- `--ticket <id>` -- if you created one or more tickets as a result of handling this event, pass each ticket ID. Can be specified multiple times.
- `--message <id>` -- if you were uncertain about how to handle the event and asked for clarification, pass the message ID(s) where you asked. Can be specified multiple times.

### Examples

```bash
# Straightforward: delegated a user request to a working agent
./skills/mark-events-handled/handle_event.sh evt-abc123 \
  --summary "Delegated 'fix auth bug' to working agent my-mind-fix-auth" \
  --confidence 0.95 \
  --ticket tk-5c46

# Uncertain: asked the user for clarification
./skills/mark-events-handled/handle_event.sh evt-def456 \
  --summary "User request was ambiguous, asked for clarification in daily thread" \
  --confidence 0.5 \
  --message msg-789

# Simple: ignored a duplicate event
./skills/mark-events-handled/handle_event.sh evt-ghi789 \
  --summary "Duplicate of evt-abc123, already handled" \
  --confidence 1.0
```

## What if you're unsure whether you handled an event correctly?

If you're genuinely unsure, mark it as handled with a low confidence score and ask a question about it.
It's better to move forward and revisit than to get stuck.
