---
name: manage-workflows
description: >
  Load this skill VERY proactively — any time the user's request involves
  fetching data from, acting on, or integrating with an external service.
  This includes direct task requests like "summarize my Slack notifications",
  "check my GitHub PRs", or "what emails did I get today" — not just explicit
  "build a workflow" requests. Also covers setting up new integrations,
  automating recurring tasks, fixing broken workflows, updating or improving
  existing ones. If the request touches an external service, load this skill.
---

# Managing Workflows

Workflows are Python scripts that integrate with external services to fetch data and produce event streams (JSONL files). This skill covers the full lifecycle: creating new workflows, updating them for new requirements, evolving them based on runtime data, and healing them when they break.

Each workflow lives in `thinking/skills/<workflow-name>/` and contains:
- `main.py` — the script itself
- `task.yaml` — metadata: name, description, service, parameters, assumptions
- `requirements.txt` — Python dependencies
- `SKILL.md` — auto-generated, describes how to run the workflow

## Two modes of operation

Users interact with external services in two ways, and you should handle them differently:

1. **Direct task request** — The user wants something done *now*: "summarize my Slack notifications", "what PRs need my review", "check my email". They didn't ask for a workflow — they asked for results. Handle this with the **Direct task execution** flow below.

2. **Explicit workflow request** — The user specifically asks to build, set up, or automate something: "build a workflow for summarizing Slack", "automate my PR reviews". Handle this with the **Creating a new workflow** flow further below.

When in doubt, treat it as a direct task request. The user gets their answer faster, and you can always crystallize it into a reusable workflow afterward.

---

## Step 0 — Interview

Before delegating any work, clarify the user's intent via `send-message-to-user`. Keep it quick — the goal is understanding what they need, not comprehensive requirements. Ask about:

- What service and what data/action?
- What parameters matter (time ranges, filters, scope) and reasonable defaults?
- What does the output look like?
- Any known API docs or hints?
- What authentication method should be used?

If the user's request is clear enough that you already know the service, data, and rough parameters, you can skip the interview. But if there's ambiguity — e.g., "export my Slack data" could mean channels, DMs, threads, date ranges, specific users — interview first. The exploration agent needs to know what to target, and exploring the wrong thing wastes a full agent cycle.

For authentication, you can first check whether the user has the service setup using latchkey; if so, assume that that should be used. If not, you MUST ask the user what their preferred authentication method is; the response to this should be forwarded to the exploration agent.

For direct task requests, frame as: "Let me make sure I understand what you need before I go fetch this." For explicit workflow requests, frame as: "I'll start with a basic version and we can iterate."

---

## Direct task execution

When the user asks you to do something involving an external service (not explicitly asking to build a workflow), prioritize getting them results quickly.

### 1. Execute the task

Delegate using `steps/explore-workflow.md` in **full execution mode**. The explore agent will both figure out the APIs and actually complete the full task, producing user-facing results.

Append a Task Details section with:
- The user's request (verbatim)
- The service name
- Any parameters implied by the request (e.g., time ranges, filters)
- **Mode: full-execution** — this tells the explore agent to complete the entire task, not just small-scale testing

```bash
cp ./skills/manage-workflows/steps/explore-workflow.md /tmp/task-explore-<task-name>.md
cat >> /tmp/task-explore-<task-name>.md << 'EOF'

---

## Task Details

**Mode: full-execution**

### User's Request
<paste the user's request verbatim>

### Service
<service name>

### Parameters
<any parameters implied or stated by the user — time ranges, filters, scope, etc.>
EOF
```

Then delegate with task name `explore-<task-name>` and this message file.

### 2. Present results to user

Once the explore agent finishes, present the results to the user via `send-message-to-user`. Focus on the actual answer to their question — the data, the summary, whatever they asked for. Don't lead with API details or implementation notes.

### 3. Decide whether to crystallize

After presenting results, evaluate whether this task would benefit from being a reusable workflow:
- Is this the kind of thing the user would want to do again (recurring, periodic)?
- Is the integration non-trivial enough that re-discovering it each time would be wasteful?
- Does an existing workflow already cover this? (Check `thinking/skills/` for overlap.)

If yes: proceed to the **Refine** step (step 4 under "Creating a new workflow") using the explore agent's output. You can suggest this to the user: "This seems like something you'd want to run regularly — want me to save it as a reusable workflow?" You should err on the side of crystallizing if the task is relatively deterministic. If you skipped the interview initially, it may be helpful to do it now to confirm that the crystallized workflow will have the appropriate parameters, outputs, and process.

If no (one-off request, trivial, or already covered): you're done. 

---

## Creating a new workflow

Use this flow when the user explicitly asks to build or automate a workflow, OR when you've decided to crystallize a direct task (see above).

**If coming from a direct task execution**: skip straight to step 4 (Refine) — you already have the exploration output.

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

### 6–8. Evaluate → Present → Crystallize

Every evaluation must be followed by a crystallize step to address the findings and improve the script. Never evaluate without crystallizing — even if the evaluation looks clean, the crystallize agent will confirm there's nothing to change.

**6a. Evaluate**: Delegate using `steps/evaluate-workflow.md`. Append a Task Details section with:
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

**6b. Present to user**: Share the evaluation results with the user via `send-message-to-user`. Collect feedback.

**6c. Crystallize**: Delegate using `steps/crystallize-workflow.md`. Append a Task Details section with:
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

### 7. Iterate

Repeat the evaluate → present → crystallize cycle (step 6) up to 3 times or until quality stabilizes.

### 8. Finalize

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

- Run the evaluate → crystallize cycle (step 6 from "Creating") to validate and improve the changes.
- Present to user for re-approval.

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
