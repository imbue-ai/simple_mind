# Task: Update a Workflow for New Requirements

You are modifying an existing workflow to accommodate new requirements or changed scope requested by the user. The key constraint: preserve existing functionality while adding the new capabilities.

## Inputs

You should have been provided:
- The current script (`main.py`, `task.yaml`, `requirements.txt`)
- A description of the new requirements
- Optionally: exploration output if the new requirements involve APIs or services the script doesn't currently use

## Process

### 1. Understand the current script

Read the current `main.py` and `task.yaml` thoroughly. Understand what it does, how it's structured, and what assumptions it makes.

### 2. Incorporate new requirements

Modify the script to support the new requirements. Key principles:
- **Preserve existing functionality**: Everything the script currently does should still work with the same parameters.
- **Add new parameters** in `task.yaml` for new capabilities. Keep existing parameters unchanged.
- **Reuse patterns**: If the script already handles pagination, auth, or rate limiting for this service, use the same patterns for new endpoints.
- **If exploration output is available**, use it to understand the new API endpoints and their behavior.

### 3. Update `task.yaml`

- Add new parameters if the new requirements introduce them
- Update the description if the scope has meaningfully changed
- Add new assumptions if the new functionality relies on them
- Don't remove existing assumptions unless they're actually wrong

### 4. Verify

Run the script to confirm:
- Existing functionality still works with the original parameters
- New functionality works with the new parameters
- Both can coexist (e.g., if the script now exports both messages and files, running with both parameters produces correct output)

## Output

Place all files in `output/$MNG_AGENT_ID/`:
- `summary.md` — what changed, why, and confirmation that existing functionality is preserved
- Updated `main.py`
- Updated `requirements.txt` (if new dependencies)
- Updated `task.yaml`
