---
name: answer-issue-question
description: Research and draft an answer to a question posted on a GitHub issue, then get user approval before posting. Use when an issue or comment contains a question that needs answering.
---

# Answering questions on GitHub issues

When someone posts a question on a GitHub issue (in the issue body or a comment), research an answer and present it to the user for approval before posting. See [github_workflow.md](../../github_workflow.md) for general conventions on approval flow and `gh` CLI usage.

## Step 1: Understand the question

Read the full issue and comment thread to understand the context:

```bash
gh issue view <number> -R <repo> --json number,title,body,comments
```

Identify the specific question being asked and who is asking it.

## Step 2: Research

- Search the codebase in `/data/local/<repo-name>/` for relevant code
- Check git history for related changes
- Check your memory for any relevant context
- Look at related issues for additional context

## Step 3: Draft a response

Write a clear, helpful answer. If you're confident in the answer, present it to the user:

```
Question on issue #<number> from @<username>:
> <the question>

Proposed response:
<your drafted answer>

Should I post this? (yes / edit / no / ask-user)
```

If you're **not confident**, tell the user what you found and ask them to provide the answer:

```
Question on issue #<number> from @<username>:
> <the question>

I'm not sure about the answer. Here's what I found:
<your research findings>

What should I reply with?
```

## Step 4: Post (after approval)

Once the user approves:

```bash
gh issue comment <number> -R <repo> --body "<approved response>"
```

Report the result.

## Guidelines

- Never post a comment without explicit user approval
- When unsure, always ask the user rather than guessing
- Keep responses concise and focused on the question
- If the question reveals that the issue description needs updating, propose that too (as a separate action)
