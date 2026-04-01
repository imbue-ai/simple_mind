# Task: Evolve a Workflow Based on Runtime Data

You are improving a workflow based on accumulated runtime data. Unlike crystallize (which fixes known issues), evolution is about discovering improvement opportunities from patterns in the workflow's actual usage.

**Authentication**: Scripts should use `latchkey curl <service> <url>` for authenticated API calls — do not add custom auth logic.

## Inputs

You should have been provided:
- The current script (`main.py`, `task.yaml`, `requirements.txt`)
- `task.yaml` including the `assumptions` field
- Run history analysis or a pointer to the run history data

## Analyze run history

Look at the workflow's run history for patterns:

- **Recurring warnings or errors**: Are the same issues happening across runs?
- **Duration trends**: Is the script getting slower over time? (Could indicate growing data volumes or degrading API performance)
- **Retry frequency**: How often are retries needed? Is the backoff strategy working?
- **Output anomalies**: Unexpected empty results, duplicate events, missing data in recent runs
- **Assumption violations**: Check each assumption in `task.yaml` against the data. Are any no longer true?

## Make targeted improvements

Every change should be tied to a specific data point from the analysis. Don't make speculative improvements — if the data doesn't show a problem, there isn't one.

Examples of valid evolution:
- "Runs are hitting rate limits 40% of the time → increase base backoff from 1s to 3s"
- "Output shows duplicate events when pagination cursor resets → add deduplication by event_id"
- "Average run duration increased 3x over the last month → the 'fewer than 500 channels' assumption is violated, add channel filtering"

## Know when to stop

If the data shows the approach is fundamentally broken — cascading failures, systematic assumption violations, the API has changed significantly — say so and recommend re-exploration. Don't try to patch a script that needs to be rewritten.

## Verify

Run the improved script and compare output to recent successful runs. The output should be equivalent or better, not different in unexpected ways.

## Output

Place all files in `output/$MNGR_AGENT_ID/`:
- `summary.md` — each change with the specific data point that motivated it. If no changes were needed, explain why.
- Updated `main.py`
- Updated `requirements.txt` (if dependencies changed)
- Updated `task.yaml` (especially assumptions, if any were found to be wrong)
