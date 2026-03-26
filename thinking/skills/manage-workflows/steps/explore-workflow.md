# Task: Explore Service Integration

You are researching how to accomplish a service integration task. Your goal is to discover how the service's APIs work and actually perform the task at small scale. You are NOT writing a script — you are learning what works so that a future agent can write the script.

**Authentication**: Use `latchkey curl <service> <url>` for authenticated API calls. Latchkey handles token management automatically. Use `/latchkey` to discover available services and their capabilities.

## Approach

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

## Actually attempt the task

Don't just read docs — actually perform the task with small-scale test parameters. For example, if the task is "export messages from Slack channels," fetch messages from one channel with a small time window.

Save any output data to `output/$MNG_AGENT_ID/data/`.

## Output

Produce two files in `output/$MNG_AGENT_ID/`:

### `summary.md`

- Which API access tier was used and why
- Specific endpoints, methods, and parameters that worked
- Pagination patterns observed
- Rate limiting behavior encountered
- Data format and schema of responses
- What test parameters were used and what output was produced
- Decisions made and rationale
- Status: complete / partial / blocked

### `api_discovery.md`

A freeform document describing everything needed to write a script against this service's APIs. Not a rigid schema — different services have completely different API shapes. Write what's useful:

- Endpoint URLs, HTTP methods, required headers
- Auth patterns (tokens, cookies, OAuth flows)
- Pagination: how to get the next page, how to know you're done
- Rate limits: what the limits are, what headers to watch, how to back off
- Response structure: what fields matter, how data is nested
- Quirks and gotchas: unusual behavior, undocumented requirements, things that surprised you
- Example requests and responses (sanitized of sensitive data)
