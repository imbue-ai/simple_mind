# Create Workflow — Refine

You are transforming exploration output into an initial working script.

**If coming from a direct task execution** (crystallizing): the explore agent's output serves as your exploration summary.

## 1. Refine

Delegate using `steps/refine-workflow.md`. Append a Task Details section with:
- The exploration summary (copy the content of the exploration agent's `summary.md`)
- The API discovery notes (copy `api_discovery.md`)
- The exploration agent's ID (so the refine agent can check its transcript if needed)
- Paths to any relevant existing workflows for the same service

```bash
cp ./skills/manage-workflows/steps/refine-workflow.md /tmp/task-refine-<workflow-name>.md
cat ./skills/manage-workflows/steps/produce-flow.md >> /tmp/task-refine-<workflow-name>.md
cat >> /tmp/task-refine-<workflow-name>.md << 'EOF'

---

## Task Details

### Exploration Summary
<paste exploration summary.md content>

### API Discovery
<paste api_discovery.md content>

### Exploration Agent ID
<agent-id>

### Existing Workflows
<paths to relevant existing workflows, or "None">
EOF
```

Then delegate with task name `refine-<workflow-name>` and this message file.

## 2. Verify the script

Use standard verification.

## Next step

Once the script is verified, proceed to `instructions/create-evaluate-loop.md`.
