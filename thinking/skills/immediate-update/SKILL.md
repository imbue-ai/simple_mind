---
name: immediate-update
description: Pull in updates from the parent branch to improve this Mind's skills, prompts, and configuration. Use only when prompted by the user.
---

# Pulling updates from the parent

This skill pulls changes from the parent repository (tracked in `.parent`) into this Mind.
This is how upstream improvements to skills, prompts, and configuration get incorporated.

## Step 1: Check for updates

```bash
PARENT_URL=$(git config --file .parent parent.url)
PARENT_BRANCH=$(git config --file .parent parent.branch)
PARENT_HASH=$(git config --file .parent parent.hash)

# Fetch the latest from the parent
git fetch "$PARENT_URL" "$PARENT_BRANCH"

# Check if there are new commits
NEW_HASH=$(git rev-parse FETCH_HEAD)
if [ "$NEW_HASH" = "$PARENT_HASH" ]; then
  echo "Already up to date."
  exit 0
fi

# See what changed
git log --oneline "$PARENT_HASH".."$NEW_HASH"
```

If there are no new commits, there is nothing to do.

## Step 2: Merge the changes

```bash
git merge FETCH_HEAD --no-edit
```

If the merge succeeds cleanly, skip to Step 4.

## Step 3: Resolve merge conflicts

If there are conflicts, they will typically be in files you have locally modified (e.g., memories, customized skills, configuration).

For each conflicted file, decide:
- **Keep upstream**: if the upstream change is an improvement and your local change is not important, accept theirs (`git checkout --theirs <file>`)
- **Keep local**: if your local change is a customization the user made or you made based on user feedback, keep yours (`git checkout --ours <file>`)
- **Merge manually**: if both changes matter, edit the file to combine them

After resolving all conflicts:

```bash
git add .
git commit --no-edit
```

## Step 4: Update the parent hash

```bash
git config --file .parent parent.hash "$NEW_HASH"
git add .parent
git commit -m "Update parent hash to $NEW_HASH"
```

## Step 5: Check for new onboarding items

After merging, check if `thinking/onboarding.md` has any new unchecked items.
If so, create tickets for them (see `handle-mind-onboarding`).

## Step 6: Notify the user

Post to the **Work Log**:

```
Pulled updates from parent ($PARENT_BRANCH): <N> new commits merged. Most important changes: <describe>
```

Also post to the conversation where the user asked for the update, and be sure to include:

- A summary of the most important new changes
- A link to where they can review the entire diff that was applied 
- Any changes that might affect their experience or customizations
- Anything important that they should review
- If there were any conflicts: which files had conflicts and how they were resolved

## Guidelines

- Always update the parent hash after a successful merge, even if there were conflicts.
- If you are unsure how to resolve a conflict (e.g., it involves a customization the user explicitly requested), ask the user before resolving it.
- After pulling updates, the self-improvement changelog in the next `start_of_day` should remind the user that they pulled updates and reference back to the conversation where they asked for it, so they can review the changes if they haven't already.
