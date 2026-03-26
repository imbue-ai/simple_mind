---
name: label-issue
description: Propose labels for a GitHub issue and wait for user approval before applying them. Use when a new issue is created by someone else, or when an existing issue needs label updates.
---

# Labeling GitHub issues

When an issue needs labels (new issue without labels, or existing issue with incorrect/missing labels), propose the appropriate labels and wait for user approval. See [github_workflow.md](../../github_workflow.md) for general conventions on approval flow and `gh` CLI usage.

## Step 1: Analyze the issue

Read the issue title, body, and any comments to understand what it's about:

```bash
gh issue view <number> -R <repo> --json number,title,body,labels,comments
```

If the issue references code, check the relevant files in the local checkout at `/data/local/<repo-name>/`.

## Step 2: Determine appropriate labels

Check your memory for the repo's label taxonomy. Consider:

- **Priority** (if the repo uses priority labels): How urgent/important is this?
- **Size** (if the repo uses size labels): How much work is this likely to be?
- **Category**: bug, enhancement, refactor, documentation, etc.
- **Area/project**: Which part of the codebase does this touch?

Only propose labels that already exist on the repo.

## Step 3: Propose to the user

Send a message to the user with your proposal:

```
Issue #<number>: "<title>"
Proposed labels: <label1>, <label2>, <label3>
Reasoning: <brief explanation of why these labels fit>
```

Wait for the user to approve, modify, or reject.

## Step 4: Apply (after approval)

Once the user approves:

```bash
gh issue edit <number> -R <repo> --add-label "<label1>" --add-label "<label2>"
```

Report the result to the user.

## Guidelines

- Never apply labels without explicit user approval
- If no existing labels seem to fit well, mention this to the user and suggest creating new ones
- Over time, the user may grant you autonomy for certain label types (e.g., "auto-label all issues with area labels"). Check memory for any such permissions before asking.
