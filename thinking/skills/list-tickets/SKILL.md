---
name: list-tickets
description: Check for pending tickets that are ready to be worked on. Use when capacity opens up (e.g., after an agent finishes) to find the next highest-priority work to delegate.
---

# Listing tickets

Use this skill to check if there are pending tickets ready to be picked up, and to choose the next one to work on.

## Check for ready tickets

```bash
tk ready
```

This lists all open or in-progress tickets whose dependencies are resolved. Tickets are shown with their ID, priority, title, and tags.

## Pick the highest priority ticket

From the ready list, choose the ticket with the highest priority (lowest number -- 0 is critical, 4 is minimal). If there are ties, use your judgment based on your PURPOSE and the current context.

## Launch the ticket as a task

Once you've chosen a ticket:

1. Read the ticket details: `tk show <ticket-id>`
2. Mark it as in progress: `tk start <ticket-id>`
3. Add a note with the agent ID: `tk add-note <ticket-id> "Delegated to agent <agent-id>"`
4. Create the agent using your `delegate-task` skill, using the ticket's description and acceptance criteria as the task instructions
5. Notify the user in the "Work Log" conversation by using the `send-message-to-user` skill.

## Other useful commands

- `tk list` -- show all open tickets (not just ready ones)
- `tk blocked` -- show tickets that are waiting on dependencies
- `tk show <ticket-id>` -- show full details of a ticket
- `tk closed` -- show recently closed tickets

## When to check for tickets

Check for ready tickets whenever capacity opens up:
- After an agent finishes and is archived
- After a task is cancelled
- After processing agent state events (if the number of active agents is below `max_concurrent_workers`)
- When idle
- During any periodic cleanup operations (ex: nightly)
