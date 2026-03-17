---
name: handle-verification-result
description: Act on the results of a verifying agent by reviewing its recommendations and taking the appropriate next actions. You **MUST** use this skill (and *carefully follow the process in this doc*) whenever a verifying agent finishes!
---

# Handling verification results

When a verifying agent finishes, read its `verdict.json` and `next_steps.md` files, and execute the recommended actions.

## Step 1: Read the verifier's verdict

```bash
cat outputs/<verifier-agent-id>/verdict.json
```

This file contains the verdict (PASSED / FAILED), confidence, and reasoning, which helps contextualize your next steps.

## Step 2: Read the next steps

Next, read the `next_steps.md` file:

```bash
cat outputs/<verifier-agent-id>/next_steps.md
```

These are the actions that were recommended by the verifying agent.

## Step 3: Verify the verifier's verdict

Think carefully about the verdict.
If you disagree, you can send a message to the verifying agent (by calling `mng message <verifying-agent-id> --message "Your message goes here"`) to ask for clarification, include new information, or point out anything you think it missed.
In such a case, you should *stop* executing this skill, and wait for the verifying agent to update its verdict (which will ultimately trigger this skill again)
Remember that a "FAILED" verdict does not necessarily mean that the work was bad or that the user will be unhappy--it just means that the verifying agent found some issue that it thinks should be followed up on.
Use your judgment to decide whether to challenge the verdict or move on to executing the next steps.

If not, and the verdict seems reasonable to you, then move on to the next step.

## Step 3: Execute each next step

Assuming the verdict and next steps seem reasonable, next you should work through the next steps list one by one. These may include:

- **Running commands** (e.g., `git merge`, shell commands)
- **Sending messages to the user** (via `send-message-to-user`)
- **Creating follow-up tickets** (via `create-ticket`)
- **Archiving agents** (via `mng archive`)
- **Closing tickets** (via `tk close`)
- **Retrying with revised instructions** (via `delegate-task-to-agent`)

Post each action to the **Work Log** as you execute it. For example:

```
Verification of <task-name>: PASSED.
- Merged branch feature/fix-auth
- Closed ticket tk-5c46
- Archived agents agent-abc and agent-def
- Sent completion notice to user
```

If any important data or artifacts need to be preserved beyond the outputs directory (e.g., a report the user should keep, configuration that should be committed), move or copy them to a permanent location now--the outputs directory will be cleaned up when the agents are eventually destroyed.

## Step 4: Clean up

After executing the next steps, you should also double-check if anything was missed by the verifying agent's recommendations, for example:

- Closing tickets
- Archiving agents (the verifying and/or working agent)
- Sending messages to the user (ex: `mng archive -f <agent-id>`)
- etc.
