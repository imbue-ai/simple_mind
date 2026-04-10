---
name: handle-verification-result
description: Act on the results of a verifying agent by reviewing its recommendations and taking the appropriate next actions. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever a verifying agent finishes!
---

# Handling verification results

When a verifying agent finishes, read its `verdict.json` and `next_steps.md` files, and execute the recommended actions.

## Step 1: Read the verifier's verdict

```bash
cat $MNGR_HOST_DIR/agents/<verifier-agent-id>/outputs/verdict.json
```

This file contains the verdict (PASSED / FAILED), confidence, and reasoning, which helps contextualize your next steps.

## Step 2: Read the next steps

Next, read the `next_steps.md` file:

```bash
cat $MNGR_HOST_DIR/agents/<verifier-agent-id>/outputs/next_steps.md
```

These are the actions that were recommended by the verifying agent.

## Step 3: Verify the verifier's verdict

Think carefully about the verdict.
If you disagree, you can send a message to the verifying agent (by calling `mngr message <verifying-agent-id> --message "Your message goes here"`) to ask for clarification, include new information, or point out anything you think it missed.
In such a case, you should *stop* executing this skill, and wait for the verifying agent to update its verdict (which will ultimately trigger this skill again)
Remember that a "FAILED" verdict does not necessarily mean that the work was bad or that the user will be unhappy--it just means that the verifying agent found some issue that it thinks should be followed up on.
Use your judgment to decide whether to challenge the verdict or move on to executing the next steps.

If not, and the verdict seems reasonable to you, then move on to the next step.

## Step 4: Execute each next step

Assuming the verdict and next steps seem reasonable, next you should work through the next steps list one by one.
These may include:

- **Running commands** (e.g., `git merge`, shell commands)
- **Sending messages to the user** (via `send-message-to-user`)
- **Creating follow-up tickets** (via `create-ticket`)
- **Archiving agents** (via `mngr archive`)
- **Closing tickets** (via `tk close`)
- **Retrying with revised instructions** (via `delegate-task-to-agent`)

Post each action to the **Work Log** as you execute it.
For example:

```
Verification of <task-name>: PASSED.
- Merged branch feature/fix-auth
- Closed ticket tk-5c46
- Archived agents agent-abc and agent-def
- Sent completion notice to user
```

If any important data or artifacts need to be preserved beyond the output directory (e.g., a report the user should keep, configuration that should be committed), move or copy them to a permanent location now--the output directory will be cleaned up when the agents are eventually destroyed.

## Step 5: Archive the verifier

**Always archive the verifying agent** once you have read its output and executed the next steps:

```bash
mngr archive -f <verifier-agent-id>
```

## Step 6: Clean up and next steps

After executing the next steps, you should also double-check if anything was missed by the verifying agent's recommendations, for example:

- Closing tickets (use `close-ticket` skill)
- Archiving the working agent once the ticket is fully complete (verified and changes applied): `mngr archive -f <working-agent-id>`
- Sending messages to the user
- **Thinking about the next step**: after archiving a completed task, always consider what comes next -- is there follow-up work to create a ticket for? Is there now capacity to launch a pending ticket (check `tk ready`)? Should the user be notified?
- **Consider formalizing as a workflow**: If the completed task was *not* part of a `manage-workflows` process (i.e., not a workflow execution, exploration, refinement, evaluation, crystallization, update, evolution, or heal step), and the verdict was PASSED, assess whether the task involved a deterministic sequence of steps that could be automated. Signals to look for:
  - The working agent made 5 or more tool calls following a repeatable, deterministic pattern (not exploratory/debugging — a consistent sequence that would look the same every time this type of task is performed). It's fine if this pattern varies based on a set of parameters; that can still be deterministic.
  - The task involved an external service integration (API calls, data fetching, etc.)
  - The same type of task has been requested before, or is likely to recur
  
  If any of these apply, consider formalizing the task as a reusable workflow using the `manage-workflows` skill. You don't need to do this for every passing task — use judgment. But if the task's steps are clearly repeatable and non-trivial, a workflow saves re-discovery on future invocations. Start from the **Refine** step (the exploration was effectively already done by the working agent whose transcript you can reference). You can also send a message to the user letting them know you're saving the process as a reusable workflow.
