# GitHub Workflow

This document describes how this mind interacts with GitHub. All skills that touch GitHub should reference this document for the shared conventions.

## The target repository

The GitHub repo you manage is stored in memory (set during onboarding via the `setup-target-repo` skill). A local checkout lives at `/data/local/<repo-name>/` for codebase reference. You should periodically fetch the latest changes so working agents always have up-to-date code to reference. You should **never** push to or edit files in this checkout.

```bash
git -C /data/local/<repo-name>/ fetch origin && git -C /data/local/<repo-name>/ pull --ff-only
```

## Tracking your issues

You must keep careful track of which GitHub issues you created. When you create an issue (with the user's approval), record the issue number in your memory. For now, restrict yourself to working with issues you created unless the user explicitly asks otherwise.

## Approval flow

**Nothing happens on GitHub without the user's explicit approval.** This applies to:
- Creating issues
- Applying or changing labels
- Posting comments
- Closing issues
- Any other modification

When you want to propose actions, send them as numbered messages to the user (via `send-message-to-user`). The user replies with the number and their decision (e.g., "1: yes", "2: change the title to X", "3: no").

When triaging notes into issues, always keep a few proposals outstanding so the user is never blocked waiting for you. When the user approves or responds to one, send the next. Start with 2-3 proposals, then maintain that buffer.

## Interacting with GitHub

Use the `gh` CLI for all GitHub operations. Common commands:

```bash
# Issues
gh issue list -R <repo> --state open --json number,title,labels,body --limit 200
gh issue view <number> -R <repo> --json number,title,body,labels,comments
gh issue create -R <repo> --title "<title>" --body "<body>" --label "<label1>" --label "<label2>"
gh issue edit <number> -R <repo> --add-label "<label>"
gh issue comment <number> -R <repo> --body "<comment>"
gh issue close <number> -R <repo>

# Labels
gh label list -R <repo> --json name,description,color --limit 200
gh label create "<name>" -R <repo> --description "<desc>" --color "<hex>"
```

Each label must be a separate `--label` flag. Never comma-separate labels in a single flag.
