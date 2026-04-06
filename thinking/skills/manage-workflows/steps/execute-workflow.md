# Task: Execute an Existing Workflow

You are running an existing workflow script to fulfill a user's request. The script is already written and tested — your job is to invoke it with the right parameters and present the results.

**Do not modify the script. Do not attempt to fix, patch, or work around any errors.** If it fails, report the failure clearly and completely so the orchestrating agent can follow the appropriate healing process.

## Running the script

1. Install dependencies if needed:
   ```bash
   cd thinking/skills/<workflow-name>
   uv pip install -r requirements.txt
   ```

2. Run the script with the parameters specified in the Task Details section. Use `uv run python main.py ...` from the workflow directory.

3. If the script requires authenticated API calls via latchkey, make sure the service is available by checking with `/latchkey` first.

## Handling failures

If the script fails:
- Capture the full error output (stderr and exit code)
- Note whether it looks transient (network timeout, rate limit) or structural (missing parameter, API change, auth failure)
- **Do NOT attempt to fix the script, modify it, or work around the issue.** Do not retry more than once for what looks like a transient error.
- Report the failure clearly and completely in your output — include the full error, your assessment of the cause category (transient vs. structural), and any relevant context. The orchestrating agent needs this information to decide whether to trigger the heal-workflow process.

## Output

Produce files in `output/$MNGR_AGENT_ID/`:

### `results.md`

The actual answer to the user's request. This will be shown directly to the user, so write it for them — not for a developer. Focus on clarity, useful structure, and the information they asked for. Don't include API details or implementation notes here.

If the script produced JSONL output, process it into a human-readable summary that answers what the user asked for.

### `summary.md`

- What command was run (with parameters)
- Whether it succeeded or failed
- If failed: the error output and your assessment of the cause
- Any warnings or anomalies observed during execution
- Output file location and size
- **Post-processing performed**: Describe any work you had to do beyond simply formatting the script's output — filtering, deduplication, diffing against previous results, date-range narrowing, aggregation, or any other transformation needed to bridge the gap between what the script produced and what the user actually asked for. Be specific about what the script gave you vs. what you had to compute yourself. If no post-processing was needed, say so explicitly.
