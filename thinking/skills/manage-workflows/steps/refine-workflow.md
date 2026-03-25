# Task: Refine Exploration into a Working Script

You are transforming API exploration findings into an initial working Python script. A previous agent explored the service's APIs and documented what works — your job is to turn that into a clean, runnable script.

## Inputs

You should have been provided:
- An exploration summary (`summary.md`) describing what was discovered
- An API discovery document (`api_discovery.md`) with endpoint details, auth patterns, pagination, rate limits, etc.
- The exploration agent's ID (use `mng transcript <agent-id>` if you need to check specific details that aren't in the summary)
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

## Output

Place all files in `output/$MNG_AGENT_ID/`:
- `summary.md` — what you built, key decisions, any concerns
- `main.py`
- `requirements.txt`
- `task.yaml`
