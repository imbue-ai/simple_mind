---
name: handle-github-events
description: Route GitHub events to the appropriate handler skill based on event type. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever you receive events from any "github/" source!
---

# Handling GitHub events

GitHub events arrive under various `github/` sources. Route each event based on its `type` field.

Note: The GitHub event source may not exist yet. If you receive events from `github/` sources, handle them as described below. If no event source has been set up yet, you may need to build one (delegate to a working agent).

Events from certain types (e.g., CI status checks, bot comments, dependabot) are pre-filtered by `scripts/filter_events.py` before they reach you. See that script for details.

## Event types and routing

### Issues

**Type:** `issue`

**Source:** `github/issue/created`, `github/issue/updated`

These are new or updated issues on the repository.

For issues created by others (not by you), use the **`label-issue`** skill to propose labels for user approval.

For issues that contain a question, also use the **`answer-issue-question`** skill.

For issues you created, check if any updates require your attention (e.g., someone added a comment, changed labels, or closed it).

### Issue comments

**Type:** `issue_comment`

**Source:** `github/issue_comment/created`

Comments on issues. Check if the comment contains a question that needs answering (use `answer-issue-question`).

If the comment is on an issue you created, pay special attention -- it may require updating the issue or notifying the user.

### Labels

**Type:** `label`

**Source:** `github/label/created`, `github/label/updated`, `github/label/deleted`

Changes to the repo's label taxonomy. Update your memory of available labels when you see these.

## Guidelines

- Always check the `type` field to route correctly
- For event types not listed above, use your `handle-unknown-events` skill
- Remember: no actions on GitHub without user approval
