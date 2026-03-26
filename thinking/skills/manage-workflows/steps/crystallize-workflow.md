# Task: Crystallize a Workflow Script

You are improving a workflow script based on evaluation feedback. Your job is to fix issues found during evaluation, simplify the code, and improve robustness — but only where there's a reason to.

**Authentication**: Scripts should use `latchkey curl <service> <url>` for authenticated API calls — do not add custom auth logic.

## Inputs

You should have been provided:
- The current script (`main.py`, `task.yaml`, `requirements.txt`)
- An evaluation report describing test results, failures, and specific issues
- Optionally: user feedback on the script

## Process

### 1. Address evaluation issues first

Go through each specific issue in the evaluation report and fix it. These are concrete, identified problems — they take priority.

### 2. General improvements (only if warranted)

After fixing evaluation issues, consider:
- **Simplify**: Remove unnecessary complexity, reduce dependencies, flatten abstractions
- **Harden error handling**: Add retries where missing, improve rate limit backoff, handle edge cases in responses
- **Cover the full parameter space**: Make sure all documented parameters actually work correctly
- **Improve output quality**: Ensure JSONL output is consistent and complete

### 3. Don't change things for the sake of it

If the evaluation and feedback indicate no issues, say so. A script that works correctly and handles its edge cases is done. Don't add complexity, refactor working code, or "improve" things that aren't broken.

## Verify your changes

Run the script with the same test cases from the evaluation to confirm:
- Previously failing cases now pass
- Previously passing cases still pass (no regressions)

## Output

Place all files in `output/$MNG_AGENT_ID/`:
- `summary.md` — what you changed and why, organized by issue. If nothing needed changing, say so.
- Updated `main.py`
- Updated `requirements.txt` (if dependencies changed)
- Updated `task.yaml` (if assumptions changed)
