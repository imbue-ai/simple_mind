#!/usr/bin/env python3
"""List all known channels sorted by most recent message activity.

Usage: channel_activity.py

Output: one line per channel, most recently active first:
  <last_message_time>  #<channel_name>
"""

import json
import os
import sys
from datetime import datetime
from datetime import timezone
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

    # Track the latest message ts per channel
    latest: dict[str, str] = {}
    for events_file in [
        slack_dir / "message" / "created" / "events.jsonl",
        slack_dir / "message" / "updated" / "events.jsonl",
        slack_dir / "relevant_thread_reply" / "created" / "events.jsonl",
        slack_dir / "relevant_thread_reply" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            channel = event.get("channel_name", "")
            ts = event.get("raw", {}).get("ts", event.get("message_ts", event.get("reply_ts", "")))
            if channel and ts:
                if channel not in latest or ts > latest[channel]:
                    latest[channel] = ts

    # Sort by latest ts descending
    channels = sorted(latest.items(), key=lambda x: x[1], reverse=True)

    for channel, ts in channels:
        dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
        time_str = dt.strftime("%Y-%m-%d %H:%M")
        print(f"  {time_str}  #{channel}")


main()
