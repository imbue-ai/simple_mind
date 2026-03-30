# Onboarding Checklist

Items are checked off (by changing "[ ]" to "[X]" in the list below) **when a ticket has been created for that item** (they don't need to be completed immediately).
The tickets themselves (tagged `onboarding`) track the actual completion of each item.

## Setup

- [ ] Once the user has defined their github repo, validate access by running `gh repo view <owner/repo>`. Clone it to `/data/local/<repo-name>/` for codebase reference. Save the repo owner/name to memory.  Note that you do **NOT** need to ask the user to provide the github repo URL--an initial message asking them for the URL will be automatically sent.

## Immediate (first session, after setup is complete)

- [ ] **Learn the user's GitHub identity**: Run `gh api user` to get the authenticated user's login and ID. Save both to memory so you can distinguish the user's issues and comments from others'.
- [ ] **Discover existing labels**: Run `gh label list -R <repo> --json name,description,color --limit 200` and save the label taxonomy to memory. If the repo lacks priority/size labels, propose creating them (with user approval).
- [ ] **Scan existing open issues**: Run `gh issue list -R <repo> --state open --json number,title,labels --limit 200` to get an overview of the current backlog. Summarize the state for the user.

## First hour

- [ ] **Learn the notes source**: Ask the user where their unstructured notes live. Options: a file path, a directory, or they can just paste notes directly into a conversation thread. Save the answer to memory. If it's a file/directory, set up a watcher (or create a ticket to build one).
- [ ] **Do an initial triage run**: Offer to triage the first few notes as a trial. Present 2-3 drafted issues (as separate numbered messages) for approval. Use this to calibrate the user's preferences for issue style, detail level, and labeling.

## First day

- [ ] **Learn prioritization criteria**: Ask what the user's current top priorities and goals are for the project. This shapes how you prioritize and label issues. Save to memory.
- [ ] **Learn notification preferences**: Ask how and when they want to be notified about issue updates, new external issues, questions on issues, etc.

## First week

- [ ] **Refine label taxonomy**: After seeing real usage, propose any missing labels or consolidation of existing ones (with user approval before any changes).
- [ ] **Learn communication style**: How formal should issue descriptions be? How much codebase context to include? Should issues reference specific files/functions?
- [ ] **Review and refine**: Ask the user how things are going. What's working? What's annoying? Adjust behavior accordingly.
