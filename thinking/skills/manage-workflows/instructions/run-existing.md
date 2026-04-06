# Run an Existing Workflow

When the user's request matches an existing workflow, assess whether the current version can handle it, then act accordingly.

## 1. Review the workflow against the user's request

Read the workflow's `SKILL.md` (parameters, capabilities, output format) and compare it against what the user is asking for. Determine which category the request falls into:

- **A) Current version can handle it** — the workflow can produce the data the user needs, even if inefficiently. A missing parameter is NOT necessarily a reason to reject — that's just an inefficiency that Path A can flag as an optional update. The bar here is: can the existing script, combined with reasonable post-processing of its output, answer the user's question?

- **B) Current version literally cannot handle it** — the request is impossible with the current script even with post-processing. Examples: the script talks to the wrong API entirely, the data the user needs isn't accessible through any endpoint the script uses, or the script produces output that fundamentally doesn't contain the information requested. Only choose Path B when running the current script would be pointless.

## 2. Follow the appropriate path

- **Path A**: Load [instructions/run-existing-execute.md](run-existing-execute.md)
- **Path B**: Load [instructions/update.md](update.md) with **immediate results needed** — the update flow's explore step will fulfill the user's request while discovering what the workflow needs to change.
