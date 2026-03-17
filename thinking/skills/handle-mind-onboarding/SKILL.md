---
name: handle-mind-onboarding
description: Handle the one-time first-run event to set up onboarding tickets and introduce yourself to the user. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive a message from the "mind/onboarding" source!
---

# First-run onboarding

The `mind/onboarding` event fires exactly once -- the first time this mind starts.
Use it to bootstrap the onboarding process.

## What to do immediately

1. **Read the onboarding checklist**: Read `thinking/onboarding.md`, which contains a prioritized list of onboarding items grouped by when they should happen (first session, first day, first week, first month).

2. **Create tickets for each unchecked item**: For each unchecked (`- [ ]`) item in the checklist, create a ticket using `create-ticket`:

```bash
tk create "<item title>" \
  --description "<item description from the checklist>" \
  --tags onboarding \
  --priority <priority based on timing group> \
  --type task
```

Use priority levels that reflect the timing groups:
- **Immediate (first session)**: priority `0`
- **First day**: priority `1`
- **First week**: priority `2`
- **First month**: priority `3`

3. **Check off each item** in `thinking/onboarding.md` as soon as you've created its ticket (change `- [ ]` to `- [x]`).
The checklist tracks "ticket created", not "task completed" -- ticket closure is tracked separately by `tk`.

4. **Handle the most urgent item yourself**: The "Find a way to provide value immediately" item should be done immediately -- don't delegate it.
Use `send-message-to-user` to send any necessary messages and questions.

5. **Continue onboarding over time**: The other items will be handled over the first hours, days, and weeks of usage.
Don't try to do everything at once -- let the user get used to you gradually and avoid overwhelming them.

## After the first onboarding ticket is complete

Continue working through the other tickets tagged "onboarding" over time through the normal ticket workflow.
