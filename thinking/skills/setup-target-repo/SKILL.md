---
name: setup-target-repo
description: Set up the target GitHub repository that this mind manages. Use during onboarding to clone the repo, validate access, and discover the label taxonomy.
---

# Setting up the target repository

During onboarding, you need to configure which GitHub repository this mind manages.

## Step 1: Get the repo from the user

Ask the user which repository to manage. They should provide it in `owner/repo` format (e.g., `imbue-ai/mng`).

## Step 2: Validate access

```bash
gh repo view <owner/repo> --json name,owner,description,url
```

If this fails, the user may need to authenticate or grant access. Help them troubleshoot.

## Step 3: Clone the repo

Clone it to `/data/local/` for codebase reference:

```bash
mkdir -p /data/local/
git clone "https://github.com/<owner/repo>.git" "/data/local/<repo-name>/"
```

This checkout is read-only from the mind's perspective -- you fetch changes to keep it current, but never push or edit.

## Step 4: Save to memory

Save the following to memory:
- Repository: `<owner/repo>`
- Local checkout path: `/data/local/<repo-name>/`

## Step 5: Discover labels

```bash
gh label list -R <owner/repo> --json name,description,color --limit 200
```

Save the label taxonomy to memory. Note any gaps (e.g., no priority labels, no size labels) and propose creating them during onboarding.

## Step 6: Scan existing issues

```bash
gh issue list -R <owner/repo> --state open --json number,title,labels --limit 200
```

Summarize the current state for the user: how many open issues, label distribution, any obvious patterns.

## Keeping the checkout current

See [github_workflow.md](../../github_workflow.md) for how to keep the checkout up to date. This is also listed in [idle_activities.md](../../idle_activities.md) as a proactive idle task.
