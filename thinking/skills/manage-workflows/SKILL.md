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

## Creating a new workflow

Follow these steps in order. For each delegation step, read the referenced step file and include its content in the working agent's task message (via `--message-file`).

1. **Explore**: Delegate a working agent with the explore-workflow step.
   Read `./skills/manage-workflows/steps/explore-workflow.md` and include it in the task message.
   Pass: user's description, parameters, hints, the service name.

2. **Verify exploration**: Use standard verification (via `verify-task-result`).

3. **Check for overlap**: Review existing workflows in `thinking/skills/` for overlapping service access. If overlap exists, propose decomposition to the user before continuing.

4. **Refine**: Delegate a working agent with the refine-workflow step.
   Read `./skills/manage-workflows/steps/refine-workflow.md` and include it in the task message.
   Pass: exploration summary, API discovery notes, exploration agent ID (for transcript access if needed), any relevant existing workflows.

5. **Verify the script**: Use standard verification.

6. **Evaluate**: Delegate a working agent with the evaluate-workflow step.
   Read `./skills/manage-workflows/steps/evaluate-workflow.md` and include it in the task message.
   Pass: the script, task.yaml, the exploration output for comparison.

7. **Present to user**: Share the evaluation results with the user via `send-message-to-user`. Collect feedback.

8. **Crystallize**: Delegate a working agent with the crystallize-workflow step.
   Read `./skills/manage-workflows/steps/crystallize-workflow.md` and include it in the task message.
   Pass: the script, evaluation feedback, known issues.

9. **Iterate**: Repeat steps 6-8 (evaluate → present → crystallize) up to 3 times or until quality stabilizes.

10. **Finalize**: On the final pass, present the script to the user for approval. Once approved, commit the workflow files to `thinking/skills/<workflow-name>/`.

---

## Updating an existing workflow (user-driven, new requirements)

- If the update touches APIs or services the script doesn't currently use, delegate `explore-workflow` for the new scope first.
- Delegate a working agent with the update-workflow step.
  Read `./skills/manage-workflows/steps/update-workflow.md` and include it in the task message.
  Pass: current script, new requirements, exploration output if applicable.
- Run the evaluate → crystallize cycle (steps 6-9 from "Creating").
- Present to user for re-approval. Regenerate SKILL.md if parameters changed.

---

## Evolving an existing workflow (data-driven improvement)

Triggered by noticing patterns in run history (recurring failures, degrading performance, assumption violations), or by direct user request.

- Delegate a working agent with the evolve-workflow step.
  Read `./skills/manage-workflows/steps/evolve-workflow.md` and include it in the task message.
  Pass: current script, task.yaml (including assumptions), run history analysis.
- Run the evaluate cycle (step 6 from "Creating").
- Present changes to user for re-approval.

---

## Healing a failed workflow

1. **Deterministic retry**: First, just rerun the workflow. Transient failures (network timeouts, rate limits) often resolve on their own.

2. **Diagnose and fix**: If retry fails, delegate a working agent with the heal-workflow step.
   Read `./skills/manage-workflows/steps/heal-workflow.md` and include it in the task message.
   Pass: current script, error traceback, recent run history.

3. **Scope check**: If the fix changes scope (needs new endpoints, services, or fundamentally different approach), flag this for the user before committing. Recommend using the update flow instead.
