# Heal a Failed Workflow

## 1. Deterministic retry

First, just rerun the workflow. Transient failures (network timeouts, rate limits) often resolve on their own.

## 2. Diagnose and fix

If retry fails, delegate using `steps/heal-workflow.md`. Append a Task Details section with:
- The current script
- The error traceback / stderr from the failed run
- Recent run history

```bash
cp ./skills/manage-workflows/steps/heal-workflow.md /tmp/task-heal-<workflow-name>.md
cat ./skills/manage-workflows/steps/produce-flow.md >> /tmp/task-heal-<workflow-name>.md
cat >> /tmp/task-heal-<workflow-name>.md << 'EOF'

---

## Task Details

### Current Script (main.py)
<paste current main.py>

### Error Output
<paste traceback / stderr from the failed run>

### Recent Run History
<summary of recent runs: when they ran, exit codes, any patterns>
EOF
```

Then delegate with task name `heal-<workflow-name>` and this message file.

## 3. Scope check

If the fix changes scope (needs new endpoints, services, or fundamentally different approach), flag this for the user before committing. Recommend using the update flow (`instructions/update.md`) instead.
