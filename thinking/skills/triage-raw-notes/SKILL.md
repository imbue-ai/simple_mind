---
name: triage-raw-notes
description: Convert the user's unstructured notes into well-formed GitHub issues. Use when the user provides raw notes (via conversation, file, or other input) that should be turned into tracked issues.
---

# Triaging raw notes into GitHub issues

This skill guides you through converting the user's raw notes into GitHub issues, presenting them for approval before creating anything. See [github_workflow.md](../../github_workflow.md) for general conventions on interacting with GitHub (approval flow, `gh` CLI usage, issue tracking).

## Input

Notes can come from:
- A conversation message where the user pasted raw text
- A file or directory path stored in memory (see `manage-notes-source` skill)
- Any other source the user has configured

## Phase 1: Load context

Before drafting any issues:

1. **Parse the notes** into a list of entries. Each unindented line is a distinct idea; indented lines below it are sub-thoughts or details belonging to that idea.
2. **Fetch the latest code**: `git -C /data/local/<repo-name>/ pull`
3. **Read recent git history**: `git -C /data/local/<repo-name>/ log --oneline -30`
4. **Load existing GitHub issues**: `gh issue list -R <repo> --state open --json number,title,body,labels --limit 200`
5. **Check memory** for the user's label taxonomy, prioritization criteria, and communication style preferences.

## Phase 2: Prioritize

Scan all entries and produce a prioritized ordering:

- **Small important fixes first** -- config tweaks, one-line fixes, things that unblock other work
- **Important improvements next** -- real pain points, things that affect multiple people
- **New features and big ideas last** -- need the most discussion, lowest urgency
- **Already-done items noted** -- if an entry looks completed (based on git history or current code), flag it for removal

Present the prioritized list to the user with brief reasoning. Ask if they want to reorder before proceeding.

## Phase 3: Draft and propose issues

For each entry (in priority order), follow this cycle:

### Step 1: Research

- Search the codebase for relevant code, files, and patterns
- Check git log for recent related changes
- Cross-reference against existing GitHub issues for duplicates (use `find-related-issues` skill)
- Think about what the user likely meant, using surrounding entries for context

### Step 2: Draft the issue

Prepare a complete preview:

```
---
ISSUE #<incrementing number>
TITLE: <issue title>
PRIORITY: <priority:critical|high|medium|low>
SIZE: <size:xs|s|m|l|xl>
LABELS: <other labels, comma-separated>
---

<issue body in markdown>

---
Original note:
> <exact original text, preserving indentation>
---
```

**Label selection:** Check memory for the repo's label taxonomy. Every issue should have a priority label, a size label, and relevant category/area labels. Only use labels that already exist on the repo.

**Issue body guidelines:**
- Write a clear description of what needs to be done and why
- Include relevant context (file paths, function names, related systems) discovered during research
- Note any open questions or design decisions
- Incorporate sub-thoughts as context or a "Notes" section
- Keep it concise but complete enough that someone could pick it up without additional context
- The exact original text from the notes MUST appear at the bottom in a blockquote

### Step 3: Send for approval

Send each drafted issue as a separate numbered message to the user via `send-message-to-user`.

Start by sending 2-3 proposals. Then maintain that buffer: whenever the user responds to one, send the next.

The user can reply with:
- `<number>: yes` -- create the issue as shown
- `<number>: <edits>` -- modify before creating (e.g., "2: change title to X", "3: add label bug")
- `<number>: no` or `<number>: skip` -- skip this entry
- `stop` -- end the triage session

### Step 4: Create and record

Once approved:

1. **Check for duplicates** one more time with `find-related-issues`
2. **Create the issue**: `gh issue create -R <repo> --title "<title>" --body "<body>" --label "<label1>" --label "<label2>"`
3. **Record the issue number** in memory (you must track which issues you created)
4. **Remove the entry from the notes source** (if it came from a file)
5. **Report the created issue number and URL** to the user

## Phase 4: Wrap up

When all entries are processed (or the user says stop):

- Report a summary: how many created, how many skipped, how many remain
- If there are remaining entries, remind the user they can resume later

## Important rules

- **One entry at a time.** Never batch-create issues. The user must approve each individually.
- **Preserve original text.** Every created issue must contain the user's original note in a blockquote at the bottom.
- **Interruptible.** The user can stop at any point.
- **No fabrication.** If you cannot figure out what an entry means, say so honestly and provide your best guess.
- **Check for duplicates thoroughly.** Search existing issues by keyword, not just exact title match.
- **Do not create labels.** Only use labels that already exist on the repo (propose new ones separately if needed).
