#!/usr/bin/env python3
"""Filter slack events from stdin, outputting one line per input line.

Filtered events are replaced with "{}" (empty JSON object) so that line
numbers are preserved between input and output.

Filters:
  - Events whose source ends with "/created" (we only handle /updated events)
  - Events with type: user, unread_marker, channel, reply
  - Events whose channel_id is listed in ignored_channel_ids.txt

Usage: cat events.jsonl | filter_slack_events.py [--ignored-channels <path>]

The --ignored-channels flag specifies the path to a file containing one
channel ID per line. Defaults to "ignored_channel_ids.txt" in the same
directory as the thinking agent's working directory.
"""

import json
import os
import sys
from pathlib import Path

FILTERED_TYPES = {"user", "unread_marker", "channel", "reply", "relevant_thread"}


def load_ignored_channels(path: Path) -> set[str]:
    """Load channel IDs from a file, one per line. Ignores blank lines."""
    if not path.exists():
        return set()
    ids: set[str] = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                ids.add(line)
    return ids


def main() -> None:
    # Determine ignored channels file path
    ignored_path = Path("ignored_channel_ids.txt")
    args = sys.argv[1:]
    if "--ignored-channels" in args:
        idx = args.index("--ignored-channels")
        if idx + 1 < len(args):
            ignored_path = Path(args[idx + 1])

    ignored_channels = load_ignored_channels(ignored_path)

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
        channel_id = event.get("channel_id", "")

        if source.endswith("/created"):
            print("{}")
        elif event_type in FILTERED_TYPES:
            print("{}")
        elif channel_id and channel_id in ignored_channels:
            print("{}")
        else:
            print(line)


main()
