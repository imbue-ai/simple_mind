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

## A.2. Evaluate whether an update is warranted

This evaluation happens in two passes: once while the workflow runs (based on what you can anticipate), and once after it completes (based on what actually happened).

### First pass: before results arrive

Compare the workflow's SKILL.md against the user's request. Consider:

- Does the user's request imply a parameter, filter, or mode that the workflow doesn't currently support?
- Is the user asking for output in a different format or level of detail than the workflow produces?
- Can you anticipate that the script will produce a superset of what's needed, requiring post-processing to narrow down?

### Second pass: after results arrive

Check for post-processing work at **both** levels:

1. **Execution agent**: Read the execution agent's `summary.md`, paying close attention to the **post-processing performed** section. If the agent had to do non-trivial work to bridge the script's output to the user's answer — filtering, diffing, date-range narrowing, deduplication, aggregation, or any other transformation — that's a signal.

2. **You (the thinking agent)**: When you receive the execution results and prepare the user-facing response, note whether you yourself have to do any additional processing — cross-referencing with prior results, extracting a subset, reframing the data to actually answer the question, etc. An optimal workflow should produce output that directly answers the user's request without requiring either agent to do substantive post-processing.

The key insight: **the user's request doesn't have to name a missing capability for one to exist.** Look at the work that was actually required to fulfill the request, not just the words the user used. Any substantive computation that either agent had to perform on the script's output is a candidate for being built into the workflow itself.

### Decision criteria

Not every variation in how a user phrases a request means the workflow needs to change. Flag an update if there's a clear, concrete improvement — a new parameter, a new operation mode, a missing filter — that would make future invocations meaningfully more efficient. The bar is: did either agent have to do work that the script itself could have handled? If so, consider canonizing that processing as part of the workflow rather than relying on ad-hoc post-processing each time.

If no update is warranted after both passes, skip to A.4.

## A.3. If an update is warranted, start the update process

If you identified a concrete improvement in A.2 — whether from the first pass (before execution) or the second pass (after execution) — start the update flow (load `instructions/update.md`). If the execution agent is still running, the update runs in parallel; if execution already finished, start the update now. The update agent works on its own branch and doesn't affect the execution results.

When delegating the update, be specific about:
- What the user's request revealed as a gap
- What the proposed change is (new parameter, new mode, etc.)
- If the improvement was identified from the second pass: what post-processing was required and how the workflow could eliminate it
- That existing functionality must be preserved

**Do not commit or finalize the update yet.** The update process (including evaluate-crystallize) should complete fully, but the result must be held for user approval.

## A.4. Present results to the user (or handle failure)

Once the execution agent finishes:

- **If it succeeded**: Present the results to the user via `send-message-to-user`. Focus on the actual answer to their question — the data, the summary, whatever they asked for.

- **If it failed**: Inform the user that the workflow encountered an error, then follow the [Heal](instructions/heal.md) flow to diagnose and fix the issue. The execution agent's summary will include the full error output and its assessment of the cause — pass this along to the heal process.

## A.5. If an update was started, confirm and save

After the update process finishes (including the evaluate-crystallize cycle), proceed to [Confirm and Save](instructions/confirm-and-save.md) to present the changes for user approval, save the files, and commit.

Frame it as: "While running your request, I noticed the workflow could be improved. Here's what would change: [FLOW.md diff]. Want me to save this?"
