# Path A: Current Version Can Handle It

The existing workflow can produce the data the user needs (even if inefficiently). Run it immediately and consider improvements in parallel.

## A.1. Launch the workflow execution immediately

Don't delay — get the user their results using the current version of the workflow. Delegate using `steps/execute-workflow.md`, which is purpose-built for running existing scripts.

Append a Task Details section with:
- The user's request (verbatim)
- The workflow name and directory path
- The service name
- Any parameters implied by the request
- The SKILL.md usage section so the agent knows the correct invocation

```bash
cp ./skills/manage-workflows/steps/execute-workflow.md /tmp/task-run-<workflow-name>.md
cat >> /tmp/task-run-<workflow-name>.md << 'EOF'

---

## Task Details

### User's Request
<paste the user's request verbatim>

### Workflow
Name: <workflow-name>
Directory: thinking/skills/<workflow-name>/

### Service
<service name>

### Parameters
<any parameters implied or stated by the user — time ranges, filters, scope, etc.>

### How to Run
<paste SKILL.md usage section>
EOF
```

Then delegate with task name `run-<workflow-name>` and this message file.

## A.2. While the workflow runs, evaluate whether an update is warranted

Compare the workflow's SKILL.md against the user's request. Consider:

- Does the user's request imply a parameter, filter, or mode that the workflow doesn't currently support?
- Is the user asking for output in a different format or level of detail than the workflow produces?
- Does the request suggest a common use case that would benefit from being a first-class parameter rather than requiring manual post-processing?

Not every variation in how a user phrases a request means the workflow needs to change. Flag an update if there's a clear, concrete improvement — a new parameter, a new operation mode, a missing filter — that would make future invocations meaningfully more efficient. If any post-processing of the script output is needed to fit the user's request, it may make sense to canonize this processing as part of the workflow itself, rather than relying on the working agent to do it.

If no update is warranted, skip to A.4.

## A.3. If an update is warranted, start the update process in parallel

If you identified a concrete improvement in A.2, start the update flow (load `instructions/update.md`) **in parallel** with the running workflow execution agent. The update agent works on its own branch and doesn't affect the currently-running execution.

When delegating the update, be specific about:
- What the user's request revealed as a gap
- What the proposed change is (new parameter, new mode, etc.)
- That existing functionality must be preserved

**Do not commit or finalize the update yet.** The update process (including evaluate-crystallize) should complete fully, but the result must be held for user approval.

## A.4. Present results to the user (or handle failure)

Once the execution agent finishes:

- **If it succeeded**: Present the results to the user via `send-message-to-user`. Focus on the actual answer to their question — the data, the summary, whatever they asked for.

- **If it failed**: Inform the user that the workflow encountered an error, then follow the [Heal](instructions/heal.md) flow to diagnose and fix the issue. The execution agent's summary will include the full error output and its assessment of the cause — pass this along to the heal process.

## A.5. If an update was started, ask for user approval

After the update process finishes (including the evaluate-crystallize cycle), present the proposed changes to the user using the FLOW.md diff as a human-readable summary. Show what changed in terms of workflow steps — e.g., "Added step: Filter messages by date" or "Changed step 3 from 'Fetch all channels' to 'Fetch channels matching filter'". The user shouldn't need to read code to understand what's being proposed.

Frame it as: "While running your request, I noticed the workflow could be improved. Here's what would change: [FLOW.md diff]. Want me to save this?"

**You must get explicit user approval before committing the workflow update.** If the user approves, commit and finalize the updated workflow. If they decline, discard the update branch.

## Finishing up

Report to the user via `send-message-to-user` with a summary of:
- What was done (workflow executed, results delivered)
- Whether any workflow updates were proposed and their status (approved/declined/not needed)
- Any issues encountered along the way
