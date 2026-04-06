# Update an Existing Workflow (New Requirements)

This flow handles two scenarios:

1. **User explicitly asks for new capabilities** — "add a date filter to the Slack workflow", "make it also pull from DMs"
2. **Immediate results needed** — the user made a request that matches an existing workflow but the current version literally can't handle it (routed here from `instructions/run-existing.md`). In this case, the explore step must also fulfill the user's request while discovering what the workflow needs.

## 1. Explore new scope (if needed)

If the update touches APIs or services the script doesn't currently use, explore first.

- **Normal update**: Delegate `explore-workflow` in **exploration mode** (see `instructions/create-explore.md`).
- **Immediate results needed**: Delegate `explore-workflow` in **execution-with-update mode**. This gets the user their results right now while also documenting what the workflow needs. Present the results to the user via `send-message-to-user` as soon as the explore agent finishes — don't wait for the update to complete.

If the update is within existing scope (no new APIs or endpoints), skip this step.

## 2. Delegate the update

Delegate using `steps/update-workflow.md`. Append a Task Details section with:
- The current script (`main.py`, `task.yaml`, `requirements.txt`)
- The new requirements from the user
- Exploration output (if new scope was explored)

```bash
cp ./skills/manage-workflows/steps/update-workflow.md /tmp/task-update-<workflow-name>.md
cat ./skills/manage-workflows/steps/produce-flow.md >> /tmp/task-update-<workflow-name>.md
cat >> /tmp/task-update-<workflow-name>.md << 'EOF'

---

## Task Details

### Current Script (main.py)
<paste current main.py>

### Current task.yaml
<paste current task.yaml>

### New Requirements
<paste user's requirements>

### Exploration Output (if applicable)
<paste exploration summary, or "N/A — update is within existing scope">
EOF
```

Then delegate with task name `update-<workflow-name>` and this message file.

## 3. After the update

- Run the evaluate → crystallize cycle (see `instructions/create-evaluate-loop.md`).
- Present to user for re-approval. Regenerate SKILL.md if parameters changed. FLOW.md will be updated as part of the update and crystallize steps.

**You must get explicit user approval before committing the workflow update.** Present the changes using the FLOW.md diff as a human-readable summary — show what changed in terms of workflow steps (e.g., "Added step: Filter messages by date" or "Changed step 3 from 'Fetch all channels' to 'Fetch channels matching filter'"). The user shouldn't need to read code to understand what's being proposed.

## Finishing up

Report to the user via `send-message-to-user` with a summary of:
- What was updated and why
- What new parameters, modes, or behaviors were added
- Whether immediate results were delivered (if applicable)
- Any issues encountered along the way
