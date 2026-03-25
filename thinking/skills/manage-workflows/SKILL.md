---
name: manage-workflows
description: >
  Orchestrate the creation, evaluation, evolution, update, and repair of
  crystallized service workflows. Use when the user asks to set up a new
  integration, automate a recurring task involving an external service,
  fix a broken workflow, update an existing one, or improve one.
---

# Managing Workflows

Workflows are Python scripts that integrate with external services to fetch data and produce event streams (JSONL files). This skill covers the full lifecycle: creating new workflows, updating them for new requirements, evolving them based on runtime data, and healing them when they break.

Each workflow lives in `thinking/skills/<workflow-name>/` and contains:
- `main.py` — the script itself
- `task.yaml` — metadata: name, description, service, parameters, assumptions
- `requirements.txt` — Python dependencies
- `SKILL.md` — auto-generated, describes how to run the workflow

## Step 0 — Interview

Before delegating any work, clarify the user's intent via `send-message-to-user`. Keep it quick — the goal is establishing what the MVP looks like, not comprehensive requirements. Ask:

- What service and what data/action?
- What parameters should be configurable (and reasonable defaults)?
- What does the output look like?
- Any known API docs or hints?

Frame as: "I'll start with a basic version and we can iterate." The point is to minimize the chance that the script later has to be scrapped to support requirements that were foreseeable upfront.

---

## How to delegate workflow steps

Every delegation in this skill follows the same pattern: build a task message file by concatenating the step prompt with task-specific details, then delegate using your `delegate-task-to-agent` skill.

```bash
# 1. Start with the step prompt (contains all the general instructions)
cp ./skills/manage-workflows/steps/<step-name>.md /tmp/task-<step-name>-<workflow-name>.md

# 2. Append task-specific details
cat >> /tmp/task-<step-name>-<workflow-name>.md << 'EOF'

---

## Task Details

<task-specific context goes here — see each step below for what to include>
EOF
```

Then use your `delegate-task-to-agent` skill to create a working agent with `/tmp/task-<step-name>-<workflow-name>.md` as the message file. Use `<step-name>-<workflow-name>` as the task name (e.g., `explore-slack-export`).

**Do NOT summarize or rewrite the step prompt.** The step files contain the full instructions the working agent needs. You are only appending the specifics of the current task.

---

## Creating a new workflow

Follow these steps in order.

### 1. Explore

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

### 2. Verify exploration

Use standard verification (via `verify-task-result`).

### 3. Check for overlap

Review existing workflows in `thinking/skills/` for overlapping service access. If overlap exists, propose decomposition to the user before continuing.

### 4. Refine

Delegate using `steps/refine-workflow.md`. Append a Task Details section with:
- The exploration summary (copy the content of the exploration agent's `summary.md`)
- The API discovery notes (copy `api_discovery.md`)
- The exploration agent's ID (so the refine agent can check its transcript if needed)
- Paths to any relevant existing workflows for the same service

```bash
cp ./skills/manage-workflows/steps/refine-workflow.md /tmp/task-refine-<workflow-name>.md
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

### 5. Verify the script

Use standard verification.

### 6. Evaluate

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

### Exploration Output (for comparison)
<paste exploration data summary, or "Not available">
EOF
```

Then delegate with task name `evaluate-<workflow-name>` and this message file.

### 7. Present to user

Share the evaluation results with the user via `send-message-to-user`. Collect feedback.

### 8. Crystallize

Delegate using `steps/crystallize-workflow.md`. Append a Task Details section with:
- The current script files
- The evaluation report
- User feedback (if any)

```bash
cp ./skills/manage-workflows/steps/crystallize-workflow.md /tmp/task-crystallize-<workflow-name>.md
cat >> /tmp/task-crystallize-<workflow-name>.md << 'EOF'

---

## Task Details

### Current Script (main.py)
<paste main.py content>

### Evaluation Report
<paste evaluation summary.md content>

### User Feedback
<paste user feedback, or "No specific feedback">
EOF
```

Then delegate with task name `crystallize-<workflow-name>` and this message file.

### 9. Iterate

Repeat steps 6-8 (evaluate → present → crystallize) up to 3 times or until quality stabilizes.

### 10. Finalize

On the final pass, present the script to the user for approval. Once approved, commit the workflow files to `thinking/skills/<workflow-name>/`.

---

## Updating an existing workflow (user-driven, new requirements)

- If the update touches APIs or services the script doesn't currently use, delegate `explore-workflow` for the new scope first (see step 1 above).
- Delegate using `steps/update-workflow.md`. Append a Task Details section with:
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

- Run the evaluate → crystallize cycle (steps 6-9 from "Creating").
- Present to user for re-approval. Regenerate SKILL.md if parameters changed.

---

## Evolving an existing workflow (data-driven improvement)

Triggered by noticing patterns in run history (recurring failures, degrading performance, assumption violations), or by direct user request.

- Delegate using `steps/evolve-workflow.md`. Append a Task Details section with:
  - The current script and task.yaml
  - Run history analysis (summary of patterns you've observed)

```bash
cp ./skills/manage-workflows/steps/evolve-workflow.md /tmp/task-evolve-<workflow-name>.md
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

- Run the evaluate cycle (step 6 from "Creating").
- Present changes to user for re-approval.

---

## Healing a failed workflow

### 1. Deterministic retry

First, just rerun the workflow. Transient failures (network timeouts, rate limits) often resolve on their own.

### 2. Diagnose and fix

If retry fails, delegate using `steps/heal-workflow.md`. Append a Task Details section with:
- The current script
- The error traceback / stderr from the failed run
- Recent run history

```bash
cp ./skills/manage-workflows/steps/heal-workflow.md /tmp/task-heal-<workflow-name>.md
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

### 3. Scope check

If the fix changes scope (needs new endpoints, services, or fundamentally different approach), flag this for the user before committing. Recommend using the update flow instead.
