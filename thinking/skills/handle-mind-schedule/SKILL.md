---
name: handle-mind-schedule
description: Handle regularly scheduled time-of-day events (start_of_day, end_of_day, etc). You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive a message from the "mind/schedule" source!
---

# Events from the `mind/schedule` source

These events fire once per day at configured times (set in `minds.toml` under `[watchers].scheduled_events`).
Each event includes:

- `event_name` -- the name of the scheduled event (e.g., "start_of_day", "end_of_day")
- `scheduled_time` -- the time it was configured to fire (e.g., "09:00")
- `current_time_utc` -- current UTC time
- `current_time_local` -- current time in the user's configured timezone

## start_of_day

This fires at the configured start of the user's day.
Use it to set yourself up for the day:

1. **Summarize yesterday**: Briefly review what happened since the last start_of_day -- what tickets were completed, what tasks are still in progress, any issues that came up.
Use `tk closed` and `tk list` to gather this.
Also review `git log --since="yesterday" --oneline` to build the self-improvement changelog (see below).
2. **Plan today**: Look at `tk ready` and your current priorities. Think about the most important work to focus on today and in what order. If there are open `onboarding`-tagged tickets, consider weaving one into the daily conversation naturally (e.g., "It would help me to know your notification preferences -- how often do you want updates?").
3. **Make a suggestion**: Think about the most useful suggestion you could make for the user -- something that would help them get more value from you, or something you noticed that could be improved.
4. **Create a daily conversation**: Use `send-message-to-user` to start a new conversation with your summary, priorities, plans, and suggestion. The daily conversation is the natural place for ongoing general discussion throughout the day. Be sure to link to the previous day's conversation (if it exists) for continuity.

**It is critical that you create the daily conversation, and that it contain each of these sections:**
- Summary of yesterday (a short description of what was accomplished, what's still in progress, and anything that is blocked on the user's input or attention)
- Self-improvement changelog (see below)
- Your top priorities for the day (what you plan to work on)
- One useful suggestion for the user (either a suggestion to tell you more about something that is useful for onboarding / gathering more context, an idea about new capabilities the user could try, a suggestion for how to use you more effectively, etc.)

### Self-improvement changelog

Include a section in the daily conversation that shows how you changed since yesterday.
This makes your growth visible to the user and gives them a chance to review or correct changes they didn't explicitly approve.

To build this changelog, review:
- `git log --since="yesterday" --oneline` for commits to this repo (skill edits, config updates, prompt changes, etc.)
- New or updated memories (check your memory directory for recently modified files -- memory is not version controlled, so use `find thinking/memory/ -mtime -1` or similar)
- Any changes to your skills, prompts, or configuration files

Format it as a short list, sorted by importance, for example:
```
**What changed about me since yesterday:**
- Learned your notification preference: updates only when something important happens (memory)
- Updated `handle-messages` skill to better handle ambiguous requests ([PR #12](link))
- New memory: you prefer concise responses over detailed ones
- Refined daily conversation format based on your feedback (not yet reviewed)
```

Flag any changes that were **not reviewed or approved by the user** so they can easily spot things they might want to weigh in on.
If there are no changes, simply say "No changes to report."

Once you've sent the message, get started on the work that you proposed for yourself for the day by delegating to sub-agents via `delegate-task-to-agent`.
Obviously only start on work that you're sure the user would want you to work on--otherwise, ask the user for clarification or confirmation before you start.

A good general pattern is to say "If I don't hear back from you by [time], I'll assume you want me to proceed with these tasks: ..."
This gives the user a chance to intervene if they disagree, but also allows you to get started without unnecessary delays if they are busy.

## end_of_day

This fires at the configured end of the user's day.
Use it to wrap up:

1. **Check your budget**: Think about how much capacity and budget you have remaining for the day.
2. **High-leverage work**: If you have capacity left, think about the highest-leverage things you could do to help the user while they are away, and kick off that work (using `delegate-task-to-agent` or `list-tickets`).
3. **Clean up**: Archive any agents that are done but haven't been cleaned up yet. Check for stuck or crashed agents. Then use the `cleanup-historical-data` skill to destroy old archived agents and clean up their output directories.
4. **Kick off retrospectives**: If you have enough capacity, consider kicking off a "retrospective" agent to review any of the day's tasks that seem like they could have gone better.

## Custom scheduled events

Additional scheduled events may be configured in `minds.toml`.
When you receive an event with an `event_name` you don't recognize, check your memory and the settings file for context on what it should trigger.

If you still don't know what to do, you **MUST** ask the user about it.
