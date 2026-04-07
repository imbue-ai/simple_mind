# Confirm and Save Workflow

This is the final step for any flow that creates or modifies a workflow. **You cannot save workflow files without following this process.**

## 1. Present the workflow to the user

Present the workflow for the user's review via `send-message-to-user`. What to show depends on whether this is a new workflow or a modification:

**New workflow:**
- The full `FLOW.md` content (human-readable description of what the workflow does)
- The `SKILL.md` parameters and usage section
- A brief summary of what was created

**Updated/healed/evolved workflow:**
- A diff of what changed in `FLOW.md` — show old vs new steps, highlighting additions, removals, and modifications
- What triggered the change and why
- Confirmation that existing functionality is preserved (if applicable)

The user should be able to understand what's being proposed without reading code.

## 2. Wait for explicit user approval

**You must get explicit user approval before proceeding.** Ask the user directly whether they want to save this workflow. Do not assume approval. Do not proceed until the user confirms.

If the user requests changes, go back to the appropriate step (crystallize, update, etc.) to address their feedback, then return here.

If the user declines, discard the changes and report what happened.

## 3. Copy files to the workflow directory

Once approved, copy the workflow files from the agent's output directory to their final location in `thinking/skills/<workflow-name>/`:

```bash
cp output/<agent-id>/main.py thinking/skills/<workflow-name>/main.py
cp output/<agent-id>/requirements.txt thinking/skills/<workflow-name>/requirements.txt
cp output/<agent-id>/task.yaml thinking/skills/<workflow-name>/task.yaml
cp output/<agent-id>/SKILL.md thinking/skills/<workflow-name>/SKILL.md
cp output/<agent-id>/FLOW.md thinking/skills/<workflow-name>/FLOW.md
```

For new workflows, create the directory first. For updates, this overwrites the existing files.

## 4. Commit the changes

Commit the workflow files with a descriptive message.

## 5. Report to the user

Report to the user via `send-message-to-user` with a summary of:
- What was created or updated (workflow name, what it does)
- Any issues encountered or decisions made along the way
- How to invoke the workflow going forward
