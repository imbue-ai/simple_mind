---
name: summarize-project-status
description: Generate a summary of the GitHub project's current status. Use during daily conversations, when the user asks for a status update, or during scheduled events.
---

# Summarizing project status

Generate a concise overview of where the project stands.

## What to include

### Issue stats

```bash
# Open issues by label
gh issue list -R <repo> --state open --json number,title,labels --limit 200

# Recently closed
gh issue list -R <repo> --state closed --json number,title,closedAt --limit 20
```

Summarize:
- Total open issues (and breakdown by priority if the repo uses priority labels)
- Issues opened since last summary
- Issues closed since last summary
- Issues you created vs. issues created by others

### Recent activity

- New issues opened by others that may need your attention (labeling, questions)
- Issues with recent comments that may need responses
- Any issues that have become stale since the last check

### Your proposals

- Outstanding proposals waiting for user approval (issue drafts, label changes, etc.)
- Recently approved/rejected proposals

## When to summarize

- During `start_of_day` scheduled events
- When the user asks for a status update
- Optionally during `end_of_day` for a wrap-up

## Guidelines

- Keep it concise -- the user should be able to scan it in under a minute
- Highlight what needs the user's attention (outstanding proposals, questions, new external issues)
- Don't repeat information the user already knows from recent conversations
