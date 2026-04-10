# Create Workflow — Refine

You are transforming exploration output into an initial working script.

**If coming from a direct task execution** (crystallizing): the explore agent's output serves as your exploration summary.

## 1. Refine

Delegate using `steps/refine-workflow.md`. Append a Task Details section with:
- The exploration summary (copy the content of the exploration agent's `summary.md`)
- The discovery notes (copy `discovery.md`)
- The exploration agent's ID (so the refine agent can check its transcript if needed)
- Paths to any relevant existing workflows for the same task or service

```bash
cp ./skills/manage-workflows/steps/refine-workflow.md /tmp/task-refine-<workflow-name>.md
cat ./skills/manage-workflows/steps/produce-flow.md >> /tmp/task-refine-<workflow-name>.md
cat >> /tmp/task-refine-<workflow-name>.md << 'EOF'

---

## Task Details

### Exploration Summary
<paste exploration summary.md content>

### Discovery
<paste discovery.md content>

### Exploration Agent ID
<agent-id>

### Existing Workflows
<paths to relevant existing workflows, or "None">
EOF
```

Then delegate with task name `refine-<workflow-name>` and this message file.

## 2. Verify the script

Use standard verification, but scope the verification message to **structural completeness only**. The evaluate step that follows will test script correctness with actual test cases — the verifier should not duplicate that work.

Tell the verifier to check:
- All required files were produced (`main.py`, `requirements.txt`, `task.yaml`, `SKILL.md`, `FLOW.md`)
- Files follow the formats specified in the refine instructions (e.g., `main.py` uses argparse, JSONL output; `task.yaml` has required fields; `SKILL.md` has correct frontmatter)
- The script structurally reflects the exploration findings (it targets the right service/data/process, uses the right tools)

Tell the verifier **not** to assess:
- Whether the script logic is correct (pagination, error handling, edge cases, etc.)
- Whether the output data would be complete or accurate
- Script quality or style beyond structural requirements

These concerns are handled by the evaluate → crystallize cycle that follows.

## Next step

Once the script is verified, proceed to `instructions/create-evaluate-loop.md`.
