# Update an Existing Workflow (User-Driven, New Requirements)

- If the update touches APIs or services the script doesn't currently use, delegate `explore-workflow` for the new scope first (see `instructions/create-explore.md`).

## Delegate the update

Delegate using `steps/update-workflow.md`. Append a Task Details section with:
- The current script (`main.py`, `task.yaml`, `requirements.txt`)
- The new requirements from the user
- Exploration output (if new scope was explored)

```bash
cp ./skills/manage-workflows/steps/update-workflow.md /tmp/task-update-<workflow-name>.md
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

## After the update

- Run the evaluate → crystallize cycle (see `instructions/create-evaluate-loop.md`).
- Present to user for re-approval. Regenerate SKILL.md if parameters changed. FLOW.md will be updated as part of the update and crystallize steps.
