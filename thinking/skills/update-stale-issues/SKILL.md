---
name: update-stale-issues
description: Scan for stale GitHub issues and propose updates or closure. Use during idle time or scheduled events to keep the backlog clean.
---

# Updating stale issues

Periodically scan for issues that may need attention -- stale issues, resolved issues, issues that need updated descriptions, etc. See [github_workflow.md](../../github_workflow.md) for general conventions on approval flow and `gh` CLI usage.

## Step 1: Find candidates

Check for issues with no recent activity:

```bash
gh issue list -R <repo> --state open --json number,title,labels,updatedAt --limit 200
```

Filter for issues that haven't been updated in a while (e.g., 30+ days). Focus on issues you created (check your memory for the list of issue numbers you own).

## Step 2: Assess each issue

For each stale issue:

- Has the underlying problem been fixed? Check recent git history and the codebase.
- Is the description still accurate? Has the codebase changed in ways that affect the issue?
- Is the issue still relevant given the user's current priorities (check memory)?

## Step 3: Propose actions

For each issue that needs attention, propose an action to the user:

- **Close**: "Issue #X appears to be resolved by commit abc123. Close it?"
- **Update**: "Issue #X description is outdated -- the file it references was renamed. Update it?"
- **Reprioritize**: "Issue #X hasn't been touched in 60 days. Lower priority or close?"

Send proposals as numbered messages. Wait for approval before taking any action.

## Guidelines

- Only scan issues you created, unless the user asks otherwise
- Don't be overly aggressive about closing things -- when in doubt, leave it open and ask
- Batch staleness checks during idle time; don't interrupt the user with these during active work
