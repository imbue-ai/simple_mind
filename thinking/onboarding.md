# Onboarding Checklist

Items are checked off (by changing "[ ]" to "[X]" in the list below) **when a ticket has been created for that item** (they don't need to be completed immediately).
The tickets themselves (tagged `onboarding`) track the actual completion of each item.

## Immediate (first session)

- [ ] **Ask the user which Slack channel they would like to triage first**
- [ ] **Learn the user's Slack identity**: Read the self identity event at `$SLACK_EVENTS_DIR/self_identity/updated/events.jsonl` to get the user's `user_name` and `user_id`, and save both to memory so all future agents know who the user is in Slack.
