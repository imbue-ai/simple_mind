---
name: handle-mind-idle
description: Handle "idle" events for periodic housekeeping and proactive work. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive a message from the "mind/idle" source!
---

# Events from the `mind/idle` source

These events are sent periodically when no real events have arrived for a configurable amount of time (set in `minds.toml` under `[watchers].idle_event_delay_minutes_schedule`).
Each event includes:

- `minutes_since_last_event` -- how long it has been since the last real event
- `idle_event_number` -- which idle event this is (1st, 2nd, etc. -- resets when a real event arrives)
- `current_time_utc` -- current UTC time
- `current_time_local` -- current time in the user's configured timezone

## What to do when idle

First, check if you have agents currently running. If tasks are already in flight, be conservative -- you'll be notified when they finish, so there's no need to start a lot of new work.

Then run through these checks in order:

1. **Crashed or stuck agents**: Run `mngr list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\"" --format jsonl` and look for agents in unexpected states (crashed, stopped, waiting for too long).
If you find any that you created, handle them using your `handle-mngr-agent_states` skill.

2. **Unprocessed agents**: Check if any agents finished but you haven't yet verified their results or acted on their output.
If so, handle them now.

3. **Unhandled events**: Check if there are any event batch files you haven't fully processed.
If so, read and handle them.

4. **Pending tickets**: Run `tk ready` to check if there are tickets waiting to be picked up.
If you have capacity (fewer than `max_concurrent_workers` active agents), launch the highest-priority ready ticket using your `list-tickets` skill.

5. **Proactive work**: If nothing above needs attention and you have no agents in flight, consider whether there's something useful you could do proactively:
   - **Ask the user a question**: If there's something you've been uncertain about (e.g., how to handle a particular type of message, whether a channel is important), this is a good time to ask. Check your memory for any outstanding questions or gaps in your understanding. Be sure not to have too many outstanding questions at once -- you don't want to overwhelm the user.  If it's important and it's been a while though, you can ask again (or better yet, ask a variant)
   - **Onboarding**: If there are uncompleted onboarding items, pick one up.

6. **Cleanup**: Archive agents that are done and have been fully processed.
This frees up capacity for new work.
Do this only if you've been idle for quite a while.

## Guidelines

- If agents are already running, keep idle handling lightweight -- just do the maintenance checks (steps 1-4) and stop. You'll be notified when tasks complete.
- Early idle events (low `idle_event_number`) should do quick checks.
Later ones (the system has been quiet for a long time) can do more thorough work like proactive triage or cleanup.
- If everything looks clean, no pending tickets, and no proactive work to do -- just finish your response and stop.
