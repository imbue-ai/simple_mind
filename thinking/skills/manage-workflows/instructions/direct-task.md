# Direct Task Execution

When the user asks you to do something involving an external service (not explicitly asking to build a workflow), prioritize getting them results quickly.

## 1. Execute the task

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

## 2. Present results to user

Once the explore agent finishes, present the results to the user via `send-message-to-user`. Focus on the actual answer to their question — the data, the summary, whatever they asked for. Don't lead with API details or implementation notes.

## 3. Decide whether to crystallize

After presenting results, evaluate whether this task should be saved as a reusable workflow. The motivation for crystallizing is **not** just scheduled/recurring use — it's that any deterministic service integration is worth capturing as a script so that future invocations (whether scheduled, on-demand, or as part of a larger task) can reuse it instead of re-discovering the APIs from scratch.

**Default to crystallizing — and do it immediately.** Don't wait for user confirmation or a follow-up message. As soon as results are presented, proceed to the Refine step unless one of these applies:
- The task is truly one-off and unlikely to ever be needed again, OR
- An existing workflow already covers this (check `thinking/skills/` for overlap), OR
- The integration is so trivial that re-discovering it would be negligible effort

If crystallizing: proceed to the **Refine** step (load `instructions/create-refine.md`) using the explore agent's output right away — in the same turn you present results, not after waiting for the user to respond. If you skipped the interview initially, it may be helpful to do it now to confirm that the crystallized workflow will have the appropriate parameters, outputs, and process.

When presenting results to the user, don't frame crystallization as a question or suggestion. Just tell them you're doing it: "I'll save this as a reusable workflow so future runs don't need to re-discover the APIs."

## Finishing up

Report to the user via `send-message-to-user` with a summary of:
- The results of their request
- Whether the task was crystallized into a reusable workflow (and its name)
- Any issues encountered along the way
