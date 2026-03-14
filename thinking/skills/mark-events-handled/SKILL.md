---
name: mark-events-handled
description: Use to make a record of which events you handled. You *must* use this skill to mark messages as handled, otherwise you will not be allowed to stop.
---

When finished handling a group of events, simply call the `handle_event.sh` file in this folder and pass it all event ids that were handled:

```
# handle_event.sh -- Log handled-event acknowledgements as JSONL.
#
# Usage: handle_event.sh <handled_event_id> [handled_event_id ...]
# 
# Example:

handle_event.sh event-b7b64515081b7ebbd0af6e2e35d31a5b80bb160b event-f79a03dcc33fa2598385590aa28a1103c444447d
```
