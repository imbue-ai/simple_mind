#!/usr/bin/env python3
"""Filter slack events from stdin, outputting one line per input line.

Filtered events are replaced with "{}" (empty JSON object) so that line
numbers are preserved between input and output.

Filters:
  - Events whose source ends with "/created" (we only handle /updated events)
  - Events with type: user, unread_marker, channel

Usage: cat events.jsonl | filter_slack_events.py
"""

import json
import sys

FILTERED_TYPES = {"user", "unread_marker", "channel"}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            print(line)
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            print(line)
            continue

        source = event.get("source", "")
        event_type = event.get("type", "")

        if source.endswith("/created"):
            print("{}")
        elif event_type in FILTERED_TYPES:
            print("{}")
        else:
            print(line)


main()
