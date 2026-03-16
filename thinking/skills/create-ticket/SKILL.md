---
name: create-ticket
description: Create a ticket to track work that needs to be done. Use when you need to record some work or action that needs to be done later (e.g., when at capacity), track a multi-step project, or log follow-up work from a completed ticket.
---

# Creating a ticket

Tickets are how you logically track your own work that needs to be done. They are distinct from "agents" and "tasks" -- a "ticket" describes *what* needs to happen, while a "task" is the actual chunk of work assigned to an "agent" (often in order to accomplish a "ticket", though not always, and there will usually be multiple "tasks" for any given "ticket", eg, at least one for the working agent, and one for the verifying agent).

Tickets are managed using the `tk` command line tool, which stores them as markdown files with YAML frontmatter in `.tickets/`.
You can run `tk help` to see all available commands.

## When to create a ticket

- **At capacity**: You need to delegate work but have too many agents running (see `delegate-task` skill). Create a ticket so the work is not forgotten, and it can be picked up later when capacity opens up.
- **Follow-up work**: A verifier recommends additional work, or a completed task surfaced something that needs attention later.
- **Multi-step projects**: Break a larger goal into multiple tickets, using dependencies to track ordering.
- **User requests that can't start immediately**: The user asks for something but you are busy with higher-priority work.  Be sure to send them the ticket ID using your `send-message-to-user` skill, so they can refer to it later if needed.

## How to create a ticket

```bash
tk create "<title>" \
  --description "<description of what needs to be done, including any relevant context>" \
  --acceptance "<what 'done' looks like -- the success criteria>" \
  --priority <priority> \
  -type <type>
```

### Priority levels

Use these to determine which ticket to pick up first when capacity opens:

- `0` -- Critical. Must be done as soon as possible.
- `1` -- High. Important, should be done soon.
- `2` -- Normal (default). Standard work.
- `3` -- Low. Nice to have, do when convenient.
- `4` -- Minimal. Background/aspirational work.

### Types

- `task` (default) -- a unit of work to be done
- `bug` -- something is broken and needs fixing
- `feature` -- a new capability to add
- `epic` -- a large effort that will be broken into sub-tickets
- `chore` -- maintenance, cleanup, or operational work

### Tags

Use `--tags` to categorize tickets for easier filtering:

```bash
tk create "Refactor auth module" --description "..." --priority 2 --tags backend,refactor
```

## Including enough context

The most important part of a ticket is that it contains **everything** a future agent will need to start working on it without asking you questions. Include:

- **What** needs to be done and **why**
- **Success criteria** (via `--acceptance`) so the verifier knows what to check
- **Relevant context**: conversation IDs, prior attempts, related agent IDs, links to code or docs
- **The user's original request** (if applicable), including the conversation ID and a summary

Think of it this way: when you later use `list-tickets` to find work to do, you will read this ticket and immediately create an agent from it using `delegate-task`. The ticket must have enough detail for that to work smoothly.

## Dependencies

If a ticket depends on another ticket being completed first:

```bash
tk dep <this-ticket-id> <depends-on-ticket-id>
```

Use `tk ready` to see which tickets have all dependencies resolved and are ready to work on.

## After creating a ticket

If the ticket was created because the user asked for something and you couldn't start immediately, acknowledge this to the user via `send-message-to-user` -- let them know you've logged it and will get to it when capacity opens up (and be sure to include the ticket ID so they can refer to it later if needed).

## Closing tickets

When a ticket's work is complete (the agent finished and verification passed), close it:

```bash
tk close <ticket-id>
```

You can also add notes to tickets as work progresses:

```bash
tk add-note <ticket-id> "Working agent <agent-id> has been created for this ticket"
```
