---
name: handle-mind-idle
description: Handle "idle" events for periodic housekeeping. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive a message from the "mind/idle" source!
---

# Events from the `mind/idle` source

These events are sent periodically when no real events have arrived for a configurable amount of time (set in `minds.toml` under `[watchers].idle_event_delay_minutes_schedule`). Each event includes:

- `minutes_since_last_event` -- how long it has been since the last real event
- `idle_event_number` -- which idle event this is (1st, 2nd, etc. -- resets when a real event arrives)
- `current_time_utc` -- current UTC time
- `current_time_local` -- current time in the user's configured timezone

## What to do when idle

You can use idle time for periodic housekeeping. 

**Do what make sense**.

Run through these checks:

1. **Crashed or stuck agents**: Run `mng list --exclude "has(labels.archived_at)" --exclude "id == \"$AGENT_ID\"" --format jsonl` and look for agents in unexpected states (crashed, stopped, waiting for too long). If you find any that you created, handle them using your `handle-mng-agent_states` skill.

2. **Unprocessed agents**: Check if any agents finished but you haven't yet verified their results or acted on their output. If so, handle them now.

3. **Unhandled events**: Check if there are any event batch files you haven't fully processed. If so, read and handle them.

4. **Pending tickets**: Run `tk ready` to check if there are tickets waiting to be picked up. If you have capacity (fewer than `max_concurrent_workers` active agents), launch the highest-priority ready ticket using your `list-tickets` skill.

5. **Cleanup**: Archive agents that are done and have been fully processed. This frees up capacity for new work.  Do this only if you've been idle for quite a while.

## Guidelines

- Keep idle handling lightweight. The goal is maintenance and catching things that fell through the cracks or continue with existing work, not starting major new initiatives (save that for `start_of_day` events).
- Early idle events (low `idle_event_number`) should do quick checks. Later ones (the system has been quiet for a long time) can do more thorough cleanup.
- If everything looks clean and there are no pending tickets, there is nothing to do--just finish your response and stop.
