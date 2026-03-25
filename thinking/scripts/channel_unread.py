#!/usr/bin/env python3
"""List channels with their unread message counts, sorted by count descending.

Usage: channel_unread.py

Output: one line per channel that has unread messages:
  <unread_count>  #<channel_name>
"""

import json
import os
import sys
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    results = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def main() -> None:
    slack_dir = Path(os.environ["SLACK_EVENTS_DIR"])

    if not slack_dir.is_dir():
        print(f"Error: Slack events directory not found: {slack_dir}", file=sys.stderr)
        sys.exit(1)

    # Get unread markers
    markers: dict[str, str] = {}
    for events_file in [
        slack_dir / "unread_marker" / "created" / "events.jsonl",
        slack_dir / "unread_marker" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            name = event.get("channel_name", "")
            ts = event.get("last_read_ts", "")
            if name and ts:
                if name not in markers or ts > markers[name]:
                    markers[name] = ts

    # Count unread messages per channel
    counts: dict[str, int] = {}
    seen: dict[str, set[str]] = {}  # channel -> set of message_ts for dedup
    for events_file in [
        slack_dir / "message" / "created" / "events.jsonl",
        slack_dir / "message" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            channel = event.get("channel_name", "")
            ts = event.get("message_ts", event.get("raw", {}).get("ts", ""))
            if not channel or not ts:
                continue
            last_read = markers.get(channel)
            if last_read is not None and ts <= last_read:
                continue
            if channel not in seen:
                seen[channel] = set()
            if ts not in seen[channel]:
                seen[channel].add(ts)
                counts[channel] = counts.get(channel, 0) + 1

    # Sort by count descending
    for channel, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {count:4d}  #{channel}")


main()
