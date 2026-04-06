# Create Workflow — Explore

This is the first step of creating a new workflow. You are delegating API exploration to a working agent.

## 1. Explore

Delegate using `steps/explore-workflow.md`. Append a Task Details section with:
- The user's description of what they want
- The service name
- Desired parameters and defaults
- Any API docs or hints the user provided

```bash
cp ./skills/manage-workflows/steps/explore-workflow.md /tmp/task-explore-<workflow-name>.md
cat >> /tmp/task-explore-<workflow-name>.md << 'EOF'

---

## Task Details

<user's description, service name, parameters, hints>
EOF
```

Then delegate with task name `explore-<workflow-name>` and this message file.

## 2. Verify exploration

Use standard verification (via `verify-task-result`).

## 3. Check for overlap

Review existing workflows in `thinking/skills/` for overlapping service access. If overlap exists, propose decomposition to the user before continuing.

## Next step

Once exploration is verified and overlap is resolved, proceed to `instructions/create-refine.md`.
