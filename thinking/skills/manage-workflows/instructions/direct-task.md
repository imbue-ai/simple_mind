# Direct Task Execution

When the user asks you to do something that involves a repeatable multi-step process (not explicitly asking to build a workflow), prioritize getting them results quickly. This includes external service interactions, data processing tasks, file transformations, or any other deterministic task.

## 1. Execute the task

Delegate using `steps/explore-workflow.md` in **full execution mode**. The explore agent will both figure out the APIs and actually complete the full task, producing user-facing results.

Append a Task Details section with:
- The user's request (verbatim)
- The service name (if applicable)
- Any parameters implied by the request (e.g., time ranges, filters, input paths)
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
<service name, or "N/A — local task">

### Parameters
<any parameters implied or stated by the user — time ranges, filters, scope, input paths, etc.>
EOF
```

Then delegate with task name `explore-<task-name>` and this message file.

## 2. Present results to user

Once the explore agent finishes, present the results to the user via `send-message-to-user`. Focus on the actual answer to their question — the data, the summary, whatever they asked for. Don't lead with API details or implementation notes.

## 3. Decide whether to crystallize

After presenting results, evaluate whether this task should be saved as a reusable workflow. The motivation for crystallizing is **not** just scheduled/recurring use — it's that any deterministic multi-step process is worth capturing as a script so that future invocations (whether scheduled, on-demand, or as part of a larger task) can reuse it instead of re-doing the same work from scratch. This applies to service integrations (avoid re-discovering APIs) and non-service tasks alike (avoid re-figuring-out the processing steps).

**Default to crystallizing — and do it immediately.** Don't wait for user confirmation or a follow-up message. As soon as results are presented, proceed to the Refine step unless one of these applies:
- The task is truly one-off and unlikely to ever be needed again, OR
- An existing workflow already covers this (check `thinking/skills/` for overlap), OR
- The integration is so trivial that re-discovering it would be negligible effort

If crystallizing: proceed to the **Refine** step (load `instructions/create-refine.md`) using the explore agent's output right away — in the same turn you present results, not after waiting for the user to respond. If you skipped the interview initially, it may be helpful to do it now to confirm that the crystallized workflow will have the appropriate parameters, outputs, and process.

When presenting results to the user, don't frame crystallization as a question or suggestion. Just tell them you're doing it: "I'll save this as a reusable workflow so future runs don't need to re-discover the APIs."

## Finishing up

If crystallizing, the Refine → Evaluate-Crystallize flow ends with [Confirm and Save](instructions/confirm-and-save.md), which handles presenting the new workflow for user approval, saving the files, and committing.

If not crystallizing, report to the user via `send-message-to-user` with a summary of the results and any issues encountered.
