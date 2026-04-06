# Create Workflow — Evaluate, Crystallize & Finalize

You are iterating on a workflow script through evaluation and improvement cycles, then finalizing it.

Every evaluation must be followed by a crystallize step to address the findings and improve the script. Never evaluate without crystallizing — even if the evaluation looks clean, the crystallize agent will confirm there's nothing to change.

## The evaluate → crystallize cycle

### 1. Evaluate

Delegate using `steps/evaluate-workflow.md`. Append a Task Details section with:
- The script files (copy `main.py` content)
- The `task.yaml` content
- The exploration output for comparison (if available)

```bash
cp ./skills/manage-workflows/steps/evaluate-workflow.md /tmp/task-evaluate-<workflow-name>.md
cat >> /tmp/task-evaluate-<workflow-name>.md << 'EOF'

---

## Task Details

### Script (main.py)
<paste main.py content>

### task.yaml
<paste task.yaml content>

### FLOW.md
<paste FLOW.md content>

### Exploration Output (for comparison)
<paste exploration data summary, or "Not available">
EOF
```

Then delegate with task name `evaluate-<workflow-name>` and this message file.

### 2. Present to user

Share the evaluation results with the user via `send-message-to-user`. Collect feedback.

### 3. Crystallize

Delegate using `steps/crystallize-workflow.md`. Append a Task Details section with:
- The current script files
- The evaluation report
- User feedback (if any)

```bash
cp ./skills/manage-workflows/steps/crystallize-workflow.md /tmp/task-crystallize-<workflow-name>.md
cat ./skills/manage-workflows/steps/produce-flow.md >> /tmp/task-crystallize-<workflow-name>.md
cat >> /tmp/task-crystallize-<workflow-name>.md << 'EOF'

---

## Task Details

### Current Script (main.py)
<paste main.py content>

### Current FLOW.md
<paste FLOW.md content>

### Evaluation Report
<paste evaluation summary.md content>

### User Feedback
<paste user feedback, or "No specific feedback">
EOF
```

Then delegate with task name `crystallize-<workflow-name>` and this message file.

## Iterate

Repeat the evaluate → present → crystallize cycle up to 3 times or until quality stabilizes.

## Finalize

On the final pass, present the script to the user for approval. Include the final `FLOW.md` content in your message to the user — this gives them a plain-language summary of what the workflow does without needing to read the code. Once approved, commit the workflow files to `thinking/skills/<workflow-name>/`.
