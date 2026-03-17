---
name: verify-task-result
description: Create a verifying agent to check whether a working agent's task was completed successfully. Use after a working agent finishes (transitions to "done", "stopped", "waiting", or "paused") and appears to believe its task is complete.
---

# Verifying a task result

Every completed task must be verified.
The verifying agent independently reviews what was done, judges whether it satisfies the original intent, and produces a concrete set of recommended next actions for you to execute.

You should **not** try to gather or summarize the working agent's output yourself -- that would pollute your context.
Instead, give the verifying agent all the *pointers* it needs to investigate the work on its own.

## What to include in the verification task message

Write a markdown file for the verifying agent that includes:

1. **The working agent's ID** so the verifier can inspect its transcript, artifacts, and state directly (e.g., via `mng transcript <working-agent-id>`)
2. **The original task description** -- what you asked the working agent to do, and why. Copy or closely paraphrase the original `--message` you sent when creating the worker. Include the success criteria.
3. **Any follow-up context** -- if you sent additional messages to the working agent during its run (e.g., answering its questions, providing clarifications, updating requirements), mention that you did so and what the key points were. The verifier can read the full transcript, but knowing what changed helps it focus.
4. **The user's original request** (if applicable) -- if this task was triggered by a user message, include any relevant conversation IDs and time-spans for each so the verifier can judge whether the result actually satisfies the user's intent (not just the task instructions as you interpreted them).
5. **High level purpose** -- if the task is part of a larger project (and *especially* if this was not a task that the user asked for directly), include a brief description of the overall purpose or goal of the project and how the task fits in.

Write the instructions to a temporary markdown file and pass via `--message-file`:

```bash
cat > /tmp/verify-<task-name>.md << 'EOF'
## Task to verify

**Working agent:** <working-agent-id>
**Original task:** <paste or paraphrase the original task description and success criteria>
**Follow-up context:** <any clarifications or additional messages you sent>
**User request:** <conversation ID and summary, if applicable>
**High level purpose:** <description of the overall project and how this task fits in>

Please review the working agent's transcript and any artifacts it produced, then provide your assessment and the recommended next action(s).
EOF
```

Then you can run a `mng create` command like the following to create the verifying agent (be sure to substitute the correct values for "<working-agent-id>" and "<task-name>"):

```bash
WORKING_AGENT_ID="<working-agent-id>"
WORKING_AGENT_BRANCH=mng/<task-name>
WORKING_AGENT_BASE_BRANCH=$(mng exec "$WORKING_AGENT_ID" 'echo $GIT_BASE_BRANCH' 2>/dev/null || echo "main")

mng create "$MIND_NAME-verify-<task-name>" \
  --env ROLE=verifying \
  --env WORKING_AGENT_ID="<working-agent-id>" \
  --env WORKING_AGENT_BRANCH="mng/<task-name>" \
  --env WORKING_AGENT_BASE_BRANCH="$(git rev-parse --abbrev-ref HEAD)" \
  --label role=verifying \
  --label mind=$MIND_NAME \
  --message-file /tmp/verify-<task-name>.md
```

## After creating the verifier

Post to the **Work Log** (see `send-message-to-user` skill):

```
Created verifying agent <agent-name> to verify: <brief description of what's being verified>
```

Then mark the relevant events as handled and move on.
You will receive a new `mng/agent_states` event when the verifying agent finishes -- at that point, use the `handle-verification-result` skill to act on its recommendations.

## What the verifier will do

The verifying agent (see `verifying/PROMPT.md`) will independently:
- Read the working agent's transcript to understand the original intent and what was actually done
- Inspect any artifacts that were created (files, branches, PRs, etc.)
- Judge whether the work satisfies the original intent and success criteria
- Produce a final response with a clear verdict and concrete recommended next actions (e.g., commands to run, messages to send, tasks to create, branches to merge)

You do **not** need to tell the verifier how to do its job -- it has its own prompt for that.
Just give it the pointers listed above so it can find everything it needs.

## Guidelines

- Always verify. The verifier catches things you would miss (and packages up the next actions so you don't have to).
- Keep your verification message focused on *what* to verify, not *how*. The verifier knows how to verify.
- Do not read the working agent's full transcript yourself! Pass the agent ID and let the verifier do the investigation. This keeps your context clean for handling other events.
- If you have already retried a task multiple times and it keeps failing verification, consider asking the user for help rather than retrying again.
