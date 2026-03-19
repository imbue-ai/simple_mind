#!/usr/bin/env python3
"""List event IDs of unread messages in a channel, one per line.

Usage: list_unread_messages.py <channel_name>

Uses the unread marker (last_read position) for the channel to determine
which messages are unread. If no marker exists for the channel, all messages
are considered unread.

Requires SLACK_EVENTS_DIR to be set (the directory containing slack event streams).
Falls back to $MNG_AGENT_STATE_DIR/events/slack if not set.
"""

import json
import os
import sys
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


def get_last_read_ts(slack_dir: Path, channel_name: str) -> str | None:
    """Get the most recent last_read_ts for a channel, or None if no marker exists."""
    last_read: str | None = None
    for events_file in [
        slack_dir / "unread_markers" / "created" / "events.jsonl",
        slack_dir / "unread_markers" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") == channel_name:
                ts = event.get("last_read_ts", "")
                if ts and (last_read is None or ts > last_read):
                    last_read = ts
    return last_read


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: list_unread_messages.py <channel_name>", file=sys.stderr)
        sys.exit(1)

    channel_name = sys.argv[1]

    slack_dir_str = os.environ.get("SLACK_EVENTS_DIR") or os.path.join(
        os.environ.get("MNG_AGENT_STATE_DIR", ""), "events", "slack"
    )
    slack_dir = Path(slack_dir_str)

    if not slack_dir.is_dir():
        print(f"Error: Slack events directory not found: {slack_dir}", file=sys.stderr)
        sys.exit(1)

    last_read_ts = get_last_read_ts(slack_dir, channel_name)

    # Collect unread messages (ts > last_read_ts, or all if no marker)
    unread: list[tuple[str, str]] = []  # (ts, event_id)
    for events_file in [
        slack_dir / "messages" / "created" / "events.jsonl",
        slack_dir / "messages" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") != channel_name:
                continue
            ts = event.get("message_ts", event.get("raw", {}).get("ts", ""))
            event_id = event.get("event_id", "")
            if event_id and (last_read_ts is None or ts > last_read_ts):
                unread.append((ts, event_id))

    # Sort by timestamp and print event IDs
    unread.sort()
    seen: set[str] = set()
    for ts, event_id in unread:
        if event_id not in seen:
            seen.add(event_id)
            print(event_id)


main()
