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

After presenting results, evaluate whether this task would benefit from being a reusable workflow:
- Is this the kind of thing the user would want to do again (recurring, periodic)?
- Is the integration non-trivial enough that re-discovering it each time would be wasteful?
- Does an existing workflow already cover this? (Check `thinking/skills/` for overlap.)

If yes: proceed to the **Refine** step (load `instructions/create-refine.md`) using the explore agent's output. You can suggest this to the user: "This seems like something you'd want to run regularly — want me to save it as a reusable workflow?" You should err on the side of crystallizing if the task is relatively deterministic. If you skipped the interview initially, it may be helpful to do it now to confirm that the crystallized workflow will have the appropriate parameters, outputs, and process.

If no (one-off request, trivial, or already covered): you're done.
