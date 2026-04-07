---
name: manage-workflows
description: >
  Load this skill VERY proactively — any time the user's request involves
  fetching data from, acting on, or integrating with an external service.
  This includes running existing workflows (any skill named *-workflow),
  direct task requests like "summarize my Slack notifications",
  "check my GitHub PRs", or "what emails did I get today" — not just explicit
  "build a workflow" requests. Also covers setting up new integrations,
  automating recurring tasks, fixing broken workflows, updating or improving
  existing ones. If the request touches an external service OR matches an
  existing *-workflow skill, load this skill.
---

# Managing Workflows

Workflows are Python scripts that integrate with external services to fetch data and produce event streams (JSONL files). This skill covers the full lifecycle: creating new workflows, updating them for new requirements, evolving them based on runtime data, and healing them when they break.

Each workflow lives in `thinking/skills/<workflow-name>/` and **must** be named with a `-workflow` suffix (e.g., `slack-export-workflow`, `github-pr-workflow`). This convention makes it easy to identify workflows among other skills. The directory contains:
- `main.py` — the script itself
- `task.yaml` — metadata: name, description, service, parameters, assumptions
- `requirements.txt` — Python dependencies
- `SKILL.md` — auto-generated, describes how to run the workflow
- `FLOW.md` — auto-generated, plain-language step-by-step explanation of what the workflow does (for non-technical readers)

## Modes of operation

Users interact with external services in three ways, and you should handle them differently:

1. **Run an existing workflow** — The user's request matches a workflow that already exists in `thinking/skills/` (any skill directory ending in `-workflow`). For example, if there's a `slack-export-workflow` and the user says "get my Slack messages from last week." **Always check for existing `*-workflow` skills first** — if one matches, use this mode.

2. **Direct task request** — The user wants something done *now* and no existing workflow covers it: "summarize my Slack notifications", "what PRs need my review", "check my email". They didn't ask for a workflow — they asked for results.

3. **Explicit workflow request** — The user specifically asks to build, set up, or automate something: "build a workflow for summarizing Slack", "automate my PR reviews".

When in doubt between (2) and (3), treat it as a direct task request. The user gets their answer faster, and you should almost always crystallize the result into a reusable workflow afterward (see the direct task flow for details).

## How to delegate workflow steps

Every delegation in this skill follows the same pattern: build a task message file by concatenating the step prompt with task-specific details, then delegate using your `delegate-task-to-agent` skill.

```bash
# 1. Start with the step prompt (contains all the general instructions)
cp ./skills/manage-workflows/steps/<step-name>.md /tmp/task-<step-name>-<workflow-name>.md

# 2. Append task-specific details
cat >> /tmp/task-<step-name>-<workflow-name>.md << 'EOF'

---

## Task Details

<task-specific context goes here — see each step's instruction file for what to include>
EOF
```

Then use your `delegate-task-to-agent` skill to create a working agent with `/tmp/task-<step-name>-<workflow-name>.md` as the message file. Use `<step-name>-<workflow-name>` as the task name (e.g., `explore-slack-export`).

**Do NOT summarize or rewrite the step prompt.** The step files contain the full instructions the working agent needs. You are only appending the specifics of the current task.

## Step 0 — Interview

Before delegating any work, clarify the user's intent via `send-message-to-user`. Keep it quick — the goal is understanding what they need, not comprehensive requirements. Ask about:

- What service and what data/action?
- What parameters matter (time ranges, filters, scope) and reasonable defaults?
- What does the output look like?
- Any known API docs or hints?
- What authentication method should be used?

If the user's request is clear enough that you already know the service, data, and rough parameters, you can skip the interview. But if there's ambiguity — e.g., "export my Slack data" could mean channels, DMs, threads, date ranges, specific users — interview first. The exploration agent needs to know what to target, and exploring the wrong thing wastes a full agent cycle.

For authentication, you can first check whether the user has the service setup using latchkey; if so, assume that that should be used. If not, you MUST ask the user what their preferred authentication method is; the response to this should be forwarded to the exploration agent. If the service in question has a dedicated CLI, you can also check whether this is installed and authenticated.

For direct task requests, frame as: "Let me make sure I understand what you need before I go fetch this." For explicit workflow requests, frame as: "I'll start with a basic version and we can iterate."

## Flows

Load instruction files as you reach each step — don't read ahead.

### Run an existing workflow
When the user's request matches an existing workflow in `thinking/skills/`:
- [Run, evaluate for improvements & present](instructions/run-existing.md)

### Direct task request
1. Interview *(if the request is ambiguous)*
2. [Execute, present & decide whether to crystallize](instructions/direct-task.md)

### Create a new workflow
1. Interview *(if the request is ambiguous)*
2. [Explore, verify & check overlap](instructions/create-explore.md)
3. [Refine & verify](instructions/create-refine.md)
4. [Evaluate, crystallize & finalize](instructions/create-evaluate-loop.md)

### Update an existing workflow
- [Update](instructions/update.md)

### Evolve an existing workflow
- [Evolve](instructions/evolve.md)

### Heal a failed workflow
- [Heal](instructions/heal.md)

## Finishing Up

Every flow that creates or modifies a workflow ends with [Confirm and Save](instructions/confirm-and-save.md). This step handles presenting the workflow for user approval, copying files to their final location, committing, and reporting. **Do not save workflow files or commit changes without going through this step** — the instruction file contains the full process.