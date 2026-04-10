# Task: Explore and Validate a Workflow

You are researching how to accomplish a task and validating the approach. Your goal is to figure out the concrete steps that work and actually perform the task. You are NOT writing a reusable script — you are learning what works and producing results.

The task may involve an external service (API calls, data fetching) or it may be a local/general-purpose process (data transformation, file processing, code analysis, etc.). Adapt your approach accordingly.

**Authentication (for service integrations)**: Use `latchkey curl <service> <url>` for authenticated API calls. Latchkey handles token management automatically. Use `/latchkey` to discover available services and their capabilities.

## Modes

Check the Task Details section for the mode:

- **Full-execution mode** (`Mode: full-execution`): The user asked for something to be done — "summarize my Slack notifications", "analyze these logs", etc. You must complete the *entire* task and produce user-facing results. Don't stop at small-scale testing. Fetch/process all the data needed and produce a clear, complete answer to the user's request.

- **Execution-with-update mode** (`Mode: execution-with-update`): Like full-execution — you must complete the entire task and produce user-facing results. However, an existing workflow script already handles *related* tasks but can't handle this specific request. Your Task Details will include the current script and an explanation of the gap. Your job is to: (1) fulfill the user's request right now, and (2) document what you discovered so the existing script can be updated. You are NOT writing a new script — focus on discovering the steps, endpoints, or process needed to fill the gap, and use that discovery to get the user their results. Your `discovery.md` and `summary.md` output will feed directly into the update step that modifies the actual script.

- **Exploration mode** (default, or `Mode: exploration`): You are scouting the approach so a future agent can write a script. Perform the task at small scale to validate the approach, but you don't need to produce complete results.

## Approach

### For tasks involving external services

Research the service's APIs. Consider three tiers in order of preference:

1. **Official/public APIs** with documented endpoints — always try this first. Search the web for the service's API documentation.
2. **Internal web APIs** via `latchkey curl <service> <url>` — the HTTP calls the service's web app makes. Use browser dev tools or documentation to discover these.
3. **Browser automation** via Playwright — last resort, only when no API access is feasible.

For whichever tier you use:

- Discover the specific endpoints, methods, and parameters needed for the task
- Understand authentication requirements and how they work
- Test pagination patterns (cursor-based, offset-based, etc.)
- Note rate limiting behavior (headers, backoff requirements)
- Understand the data format and schema of responses

### For general-purpose tasks (no external service)

Understand and validate the task's processing steps:

- Identify the inputs (files, data formats, arguments) and expected outputs
- Figure out the concrete sequence of operations — what tools, commands, or libraries are needed
- Test the approach on representative data to confirm it works
- Note edge cases, failure modes, and assumptions about the input data
- Document any dependencies (CLI tools, Python packages, etc.)

## Actually attempt the task

Don't just read docs or theorize — actually perform the task.

- **In full-execution mode**: Complete the entire task. Fetch/process all relevant data and produce the full result.
- **In exploration mode**: Perform the task with small-scale test parameters to validate the approach.

Save any output data to `output/$MNGR_AGENT_ID/data/`.

## Output

Produce files in `output/$MNGR_AGENT_ID/`:

### `results.md` (full-execution mode only)

The actual answer to the user's request. This will be shown directly to the user, so write it for them — not for a developer. Focus on clarity, useful structure, and the information they asked for. Don't include API details or implementation notes here.

### `summary.md`

- What approach was used and why
- The concrete steps/operations that worked
- What parameters were used and what output was produced
- For service integrations: endpoints, pagination patterns, rate limiting behavior, response schemas
- For general tasks: tools/libraries used, input/output formats, processing logic
- Decisions made and rationale
- Status: complete / partial / blocked

### `discovery.md`

A freeform document describing everything needed to write a script that automates this task. Not a rigid schema — different tasks have completely different shapes. Write what's useful.

For service integrations:
- Endpoint URLs, HTTP methods, required headers
- Auth patterns (tokens, cookies, OAuth flows)
- Pagination: how to get the next page, how to know you're done
- Rate limits: what the limits are, what headers to watch, how to back off
- Response structure: what fields matter, how data is nested
- Quirks and gotchas: unusual behavior, undocumented requirements, things that surprised you
- Example requests and responses (sanitized of sensitive data)

For general-purpose tasks:
- Input format and how to parse/read it
- The sequence of processing steps and the logic of each
- Libraries or tools required and how they're invoked
- Output format and how to produce it
- Edge cases and how to handle them
- Performance considerations (large files, memory, etc.)
