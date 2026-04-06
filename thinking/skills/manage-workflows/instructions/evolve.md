# Evolve an Existing Workflow (Data-Driven Improvement)

Triggered by noticing patterns in run history (recurring failures, degrading performance, assumption violations), or by direct user request.

## Delegate the evolution

Delegate using `steps/evolve-workflow.md`. Append a Task Details section with:
- The current script and task.yaml
- Run history analysis (summary of patterns you've observed)

```bash
cp ./skills/manage-workflows/steps/evolve-workflow.md /tmp/task-evolve-<workflow-name>.md
cat ./skills/manage-workflows/steps/produce-flow.md >> /tmp/task-evolve-<workflow-name>.md
cat >> /tmp/task-evolve-<workflow-name>.md << 'EOF'

---

## Task Details

### Current Script (main.py)
<paste current main.py>

### Current task.yaml
<paste current task.yaml>

### Run History Analysis
<your analysis of patterns in run history: failures, duration trends, anomalies>
EOF
```

Then delegate with task name `evolve-<workflow-name>` and this message file.

## After the evolution

- Run the evaluate → crystallize cycle (see `instructions/create-evaluate-loop.md`) to validate and improve the changes.
- Present to user for re-approval.
