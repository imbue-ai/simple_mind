#!/usr/bin/env python3
"""Select historical Slack messages for backfill triage.

Usage:
  select_messages.py <channel_name> --unread
  select_messages.py <channel_name> --last <N>
  select_messages.py <channel_name> --since <YYYY-MM-DD>

Prints one event ID per line to stdout.

Uses the SLACK_EVENTS_DIR environment variable.
"""

import json
import os
import sys
from datetime import datetime
from datetime import timezone
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    """Load all lines from a JSONL file."""
    if not path.exists():
        return []
    results = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def get_channel_messages(slack_dir: Path, channel_name: str) -> list[dict]:
    """Get all messages for a channel, deduplicated and sorted by ts."""
    messages = []
    seen: set[str] = set()
    for events_file in [
        slack_dir / "message" / "created" / "events.jsonl",
        slack_dir / "message" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") != channel_name:
                continue
            event_id = event.get("event_id", "")
            if event_id and event_id not in seen:
                seen.add(event_id)
                messages.append(event)
    messages.sort(key=lambda e: e.get("raw", {}).get("ts", e.get("message_ts", "")))
    return messages


def get_last_read_ts(slack_dir: Path, channel_name: str) -> str | None:
    """Get the most recent last_read_ts for a channel, or None if no marker exists."""
    last_read: str | None = None
    for events_file in [
        slack_dir / "unread_marker" / "created" / "events.jsonl",
        slack_dir / "unread_marker" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") == channel_name:
                ts = event.get("last_read_ts", "")
                if ts and (last_read is None or ts > last_read):
                    last_read = ts
    return last_read


def slack_ts_from_date(date_str: str) -> str:
    """Convert a YYYY-MM-DD date string to a Slack timestamp."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return f"{dt.timestamp():.6f}"


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: select_messages.py <channel_name> --unread | --last <N> | --since <YYYY-MM-DD>",
            file=sys.stderr,
        )
        sys.exit(1)

    channel_name = sys.argv[1]
    mode = sys.argv[2]

    slack_dir = Path(os.environ["SLACK_EVENTS_DIR"])

    if not slack_dir.is_dir():
        print(f"Error: Slack events directory not found: {slack_dir}", file=sys.stderr)
        sys.exit(1)

    all_messages = get_channel_messages(slack_dir, channel_name)

    if mode == "--unread":
        last_read_ts = get_last_read_ts(slack_dir, channel_name)
        if last_read_ts is None:
            selected = all_messages
        else:
            selected = [
                m for m in all_messages
                if m.get("message_ts", m.get("raw", {}).get("ts", "")) > last_read_ts
            ]

    elif mode == "--last":
        if len(sys.argv) < 4:
            print("Error: --last requires a count", file=sys.stderr)
            sys.exit(1)
        n = int(sys.argv[3])
        selected = all_messages[-n:]

    elif mode == "--since":
        if len(sys.argv) < 4:
            print("Error: --since requires a date (YYYY-MM-DD)", file=sys.stderr)
            sys.exit(1)
        cutoff_ts = slack_ts_from_date(sys.argv[3])
        selected = [
            m for m in all_messages
            if m.get("message_ts", m.get("raw", {}).get("ts", "")) >= cutoff_ts
        ]

    else:
        print(f"Error: unknown mode {mode}. Use --unread, --last <N>, or --since <YYYY-MM-DD>", file=sys.stderr)
        sys.exit(1)

    for msg in selected:
        print(msg["event_id"])


main()
