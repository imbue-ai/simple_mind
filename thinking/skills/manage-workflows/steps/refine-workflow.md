# Task: Refine Exploration into a Working Script

You are transforming API exploration findings into an initial working Python script. A previous agent explored the service's APIs and documented what works — your job is to turn that into a clean, runnable script.

**Authentication**: Use `latchkey curl <service> <url>` (via `subprocess`) for authenticated API calls. Latchkey handles token management automatically — do not implement auth logic in the script itself.

## Inputs

You should have been provided:
- An exploration summary (`summary.md`) describing what was discovered
- An API discovery document (`api_discovery.md`) with endpoint details, auth patterns, pagination, rate limits, etc.
- The exploration agent's ID (use `mngr transcript <agent-id>` if you need to check specific details that aren't in the summary)
- Any relevant existing workflows to reference for patterns

## Check for existing patterns

Look at existing workflows in `thinking/skills/` for the same or similar services. If there are any, reuse their patterns for auth, pagination, error handling, etc. Don't reinvent what's already working.

## Produce `main.py`

Write a Python script that:

- **Authenticated API calls**: Use `latchkey curl <service> <url>` (via `subprocess`) for any calls that require authentication. This handles auth automatically.
- **Event output**: Write output data as JSONL (one JSON object per line) to an output file. Each line should be a complete JSON event with at minimum: `timestamp`, `type`, `event_id`, `source`, and the payload data.
- **CLI arguments**: Use `argparse` for all configurable parameters. Include sensible defaults where possible.
- **Error handling**: Implement retries with exponential backoff for transient failures (rate limits, network errors). Log errors to stderr. Exit with non-zero code on unrecoverable failures.
- **Pagination**: Handle pagination completely — don't stop at the first page.
- **Rate limiting**: Respect rate limits. Watch for rate limit headers and back off appropriately.
- **Progress**: Print progress to stderr (e.g., "Fetched 150/500 messages from #general").

**Structure**: Organize the script so that each logical step of the workflow maps to a clearly named function. For example, a Slack export might have `fetch_channels()`, `fetch_messages(channel)`, `write_events(messages, output_file)`. This isn't about over-abstracting — it's about making the script readable and keeping a clean mapping between what the workflow *does* (documented in FLOW.md) and *how* it does it (the code). Avoid giant monolithic functions that do everything.

Keep the script simple and focused. Avoid unnecessary abstractions or over-engineering.

## Produce `requirements.txt`

List any Python packages the script needs beyond the standard library.

## Produce `task.yaml`

```yaml
name: <workflow-name>
description: >
  <What this workflow does and when to use it.>
latchkey_service: <service-name>
parameters:
  <param-name>:
    type: "<python type>"
    description: "<what this parameter controls>"
  # ... more parameters
assumptions:
  - "<assumption about the service or data that this script relies on>"
  - "<another assumption>"
```

The `assumptions` field is important — it documents things the script takes for granted that might change over time (rate limits, API behavior, data volumes). These are checked during evolution to see if the script needs updating.

## Produce `SKILL.md`

Write a skill file that describes how to run and use this workflow. This file will be loaded by the thinking agent when it needs to run the workflow, so it should contain everything needed to invoke the script correctly.

```markdown
---
name: <workflow-name>
description: >
  <When to load this skill — describe what the workflow does and what kinds of
  user requests should trigger it.>
---

# <Workflow Name>

<Brief description of what this workflow does.>

## Usage

<How to run the script: the command, required arguments, optional arguments with defaults, and what output to expect. Include a concrete example command.>

## Parameters

<Table or list of all parameters with their types, descriptions, and defaults.>

## Output

<What the script produces — file format, location, and structure of the output data.>
```

Keep it concise and practical — this is a reference for invocation, not documentation of internals.

## Produce `FLOW.md`

Follow the instructions in `steps/produce-flow.md` to create the FLOW.md file for this workflow.

## Output

Place all files in `output/$MNGR_AGENT_ID/`:
- `summary.md` — what you built, key decisions, any concerns
- `main.py`
- `requirements.txt`
- `task.yaml`
- `SKILL.md`
- `FLOW.md`
