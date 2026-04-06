# Producing / Updating FLOW.md

FLOW.md is a plain-language, non-technical step-by-step explanation of what the script does. Each step links to the function in `main.py` that implements it, creating a clear mapping between the workflow's behavior and the code.

## Format

Each step follows this pattern:

```markdown
1. **Fetch the list of channels** ([`fetch_channels()`](main.py#fetch_channels))
   Connects to Slack and gets all the channels the user has access to. If there are too many to get at once, it fetches them in batches.
```

## Guidelines

- Use numbered steps describing what happens in order when the script runs
- Each step links to exactly one function using the format `` [`function_name()`](main.py#function_name) ``. If a step maps to multiple functions, that's a sign either the step should be split or the functions should be consolidated.
- Describe actions in everyday language: "Connects to Slack", "Looks up messages in the channel", "Saves the results to a file" — not "makes a GET request to the conversations.history endpoint"
- Mention what inputs the workflow expects (in plain terms, not argparse flags) and what output it produces
- Include any important behaviors like "if there are too many results, it fetches them in batches" or "if something goes wrong, it waits and tries again"
- Do NOT include code snippets, variable names, or technical jargon (the function link in the header is the only code reference)
- Keep it concise — aim for a document someone could read in under a minute

## Structural constraint

The step↔function mapping is not just documentation — it's a structural constraint on `main.py`. If you can't map a step to a single function, refactor `main.py` until you can. Every logical step should have a corresponding function, and every significant function should appear as a step.

When updating an existing FLOW.md, check that any functions you added or renamed in `main.py` are reflected in the steps, and that any removed functions have their steps removed or remapped.
