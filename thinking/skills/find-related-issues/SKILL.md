---
name: find-related-issues
description: Search for duplicate or related GitHub issues before creating a new one. Use before creating any new issue, and when you want to cross-link related issues.
---

# Finding related issues

Before creating any new issue, search for existing issues that might be duplicates or closely related.

## How to search

### By keyword

```bash
gh issue list -R <repo> --state all --search "<keywords>" --json number,title,state,labels --limit 20
```

Try multiple keyword variations -- the user's shorthand may not match the language used in existing issues.

### By label/area

```bash
gh issue list -R <repo> --state open --label "<area-label>" --json number,title --limit 50
```

### By scanning the full list

If the above searches don't feel sufficient, scan the full open issue list:

```bash
gh issue list -R <repo> --state open --json number,title,labels --limit 200
```

## What to do with results

### Exact duplicate found

Tell the user:

```
This looks like a duplicate of #<number>: "<title>"
Should I skip this note, or update the existing issue with the new context?
```

### Related issue found

Tell the user:

```
Related to #<number>: "<title>"
Should I create a new issue and cross-reference, or merge into the existing one?
```

### No matches

Proceed with creating the new issue.

## Guidelines

- Always search before creating. This is non-negotiable.
- Search both open and closed issues (a closed issue might need reopening).
- Use multiple search terms -- don't rely on a single keyword match.
- When in doubt about whether something is a duplicate, surface it to the user and let them decide.
