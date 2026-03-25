# Task: Evaluate a Workflow Script

You are testing a crystallized workflow script against multiple inputs and compiling results for review. The goal is to find bugs, edge cases, and quality issues before the script is finalized.

## Inputs

You should have been provided:
- The workflow script (`main.py`) and its `task.yaml`
- Optionally: exploration output for comparison

## Generate test cases

Based on the script's parameters (from `task.yaml`) and your understanding of the service, create 2-4 test cases:

1. **Happy path**: Typical parameters that should produce clean output
2. **Edge case — empty results**: Parameters that should return little or no data (e.g., a channel with no messages, a date range with no activity)
3. **Edge case — larger dataset**: Parameters that exercise pagination and rate limiting
4. **Boundary conditions**: Special characters, very recent data, earliest possible dates, etc.

## Run each test case

For each test case:

1. Run the script with the test parameters
2. Check:
   - Did it exit cleanly (exit code 0)?
   - Were the expected output files produced?
   - Is the output valid JSONL (each line parseable as JSON)?
   - Does the data look complete and reasonable?
   - Are there any warnings or errors in stderr?
3. If exploration output is available, compare: does the script produce equivalent data for the same parameters?

Save per-case output in `output/$MNG_AGENT_ID/test_results/case_<N>/`.

## Output

Produce `summary.md` in `output/$MNG_AGENT_ID/` with:

### Per test case
- Test case name and parameters used
- Pass/fail on each check (exit code, output files, valid JSONL, data completeness)
- Notable observations (unexpected data, missing fields, slow performance)

### Overall assessment
- Which test cases passed, which failed
- Patterns across failures (e.g., "pagination breaks when there are exactly 100 results")
- Specific issues for the crystallize step to address — be concrete about what's wrong and where in the code

### Comparison with exploration (if applicable)
- Does the script produce the same data as the exploration agent found manually?
- Any discrepancies in data volume, format, or content
