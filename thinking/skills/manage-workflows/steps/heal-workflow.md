# Task: Heal a Failed Workflow

You are diagnosing and fixing a workflow that failed during a run. The goal is to get the workflow working again within its existing scope. If the fix requires fundamentally new capabilities, report that rather than attempting it.

**Authentication**: Scripts should use `latchkey curl <service> <url>` for authenticated API calls. If a failure is auth-related, check whether latchkey itself is working (`latchkey curl <service> <test-url>`) before modifying the script.

## Inputs

You should have been provided:
- The current script (`main.py`, `task.yaml`, `requirements.txt`)
- The error traceback or stderr output from the failed run
- Recent run history (to see if this is a new failure or recurring)

## Diagnose the root cause

Don't guess — trace the actual failure. Common categories:

- **API change**: Endpoint moved, response format changed, new required parameters
- **Rate limit change**: Tighter limits, different backoff requirements
- **Data format shift**: Fields renamed, nested differently, new required fields
- **Auth expiration**: Tokens expired, OAuth flow changed, permissions revoked
- **Data volume growth**: Script assumes small datasets but volume has grown beyond what the approach handles
- **Transient infrastructure**: DNS issues, service outages (check if the service is currently having problems)

Look at the specific error, not just the type. "ConnectionError" could be a DNS issue, a firewall change, or a service outage — the fix is different for each.

## Fix within current scope

Once you've identified the root cause, fix the script. Stay within the current scope:

- If the fix is straightforward (handle a new response field, update a URL, adjust rate limiting), make the change.
- If the fix requires accessing new endpoints or services the script doesn't currently use, **don't attempt it**. Instead, report in your summary what's needed and recommend using the update-workflow process.
- If the fix reveals that a core assumption is broken (e.g., an API is deprecated), report that and recommend re-exploration.

## Verify

Run the fixed script to confirm the failure is resolved. Use similar parameters to the failed run.

## Output

Place all files in `output/$MNG_AGENT_ID/`:
- `summary.md` — the diagnosis (what failed and why), the fix (what you changed), and whether the fix is a complete resolution or a stopgap. If the fix requires new scope, describe what's needed.
- Updated `main.py`
- Updated `requirements.txt` (if dependencies changed)
- Updated `task.yaml` (if assumptions needed correction)
