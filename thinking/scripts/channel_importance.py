#!/usr/bin/env python3
"""Rank channels by the importance of their unread messages.

For each channel that has unread messages, finds the maximum importance score
from triage results (handled_slack_messages). Channels are sorted by max
importance, highest first.

Usage: channel_importance.py

Requires:
  SLACK_EVENTS_DIR  -- directory containing slack event streams
  TRIAGE_EVENTS_DIR -- directory containing handled_slack_messages/events.jsonl
                       (falls back to $MNG_AGENT_STATE_DIR/events)

Output: one line per channel with unread messages, sorted by max importance:
  <max_importance>  <unread_count>/<triaged_count>  <channel_name>

Messages that have not been triaged yet are listed separately at the end.
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


def get_unread_markers(slack_dir: Path) -> dict[str, str]:
    """Get the most recent last_read_ts per channel_name."""
    markers: dict[str, str] = {}
    for events_file in [
        slack_dir / "unread_markers" / "created" / "events.jsonl",
        slack_dir / "unread_markers" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            name = event.get("channel_name", "")
            ts = event.get("last_read_ts", "")
            if name and ts:
                if name not in markers or ts > markers[name]:
                    markers[name] = ts
    return markers


def get_all_channel_messages(slack_dir: Path) -> dict[str, list[dict]]:
    """Get all messages grouped by channel_name, deduplicated by message_ts."""
    by_channel: dict[str, dict[str, dict]] = {}  # channel -> {ts -> event}
    for events_file in [
        slack_dir / "messages" / "created" / "events.jsonl",
        slack_dir / "messages" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            channel = event.get("channel_name", "")
            ts = event.get("message_ts", event.get("raw", {}).get("ts", ""))
            if channel and ts:
                by_channel.setdefault(channel, {})[ts] = event

    result: dict[str, list[dict]] = {}
    for channel, msgs in by_channel.items():
        result[channel] = sorted(msgs.values(), key=lambda e: e.get("message_ts", ""))
    return result


def get_triage_scores(triage_dir: Path) -> dict[tuple[str, str], float]:
    """Get importance scores from triage results, keyed by (channel, message_ts)."""
    scores: dict[tuple[str, str], float] = {}
    events_file = triage_dir / "handled_slack_messages" / "events.jsonl"
    for event in load_jsonl(events_file):
        channel = event.get("channel", "")
        ts = event.get("message_ts", "")
        importance = event.get("importance")
        if channel and ts and importance is not None:
            key = (channel, ts)
            # Keep the most recent triage score if triaged multiple times
            scores[key] = float(importance)
    return scores


def main() -> None:
    slack_dir_str = os.environ.get("SLACK_EVENTS_DIR") or os.path.join(
        os.environ.get("MNG_AGENT_STATE_DIR", ""), "events", "slack"
    )
    slack_dir = Path(slack_dir_str)

    triage_dir_str = os.environ.get("TRIAGE_EVENTS_DIR") or os.path.join(
        os.environ.get("MNG_AGENT_STATE_DIR", ""), "events"
    )
    triage_dir = Path(triage_dir_str)

    if not slack_dir.is_dir():
        print(f"Error: Slack events directory not found: {slack_dir}", file=sys.stderr)
        sys.exit(1)

    markers = get_unread_markers(slack_dir)
    all_messages = get_all_channel_messages(slack_dir)
    triage_scores = get_triage_scores(triage_dir)

    # For each channel, find unread messages and their triage scores
    channel_results: list[tuple[float, int, int, int, str]] = []
    # (max_importance, unread_count, triaged_count, untriaged_count, channel_name)

    for channel, messages in all_messages.items():
        last_read = markers.get(channel)

        # Determine unread messages
        if last_read is None:
            unread_messages = messages  # No marker = all unread
        else:
            unread_messages = [
                m for m in messages
                if m.get("message_ts", m.get("raw", {}).get("ts", "")) > last_read
            ]

        if not unread_messages:
            continue

        # Look up triage scores for unread messages
        max_importance = -1.0
        triaged = 0
        for msg in unread_messages:
            ts = msg.get("message_ts", msg.get("raw", {}).get("ts", ""))
            score = triage_scores.get((channel, ts))
            if score is not None:
                triaged += 1
                if score > max_importance:
                    max_importance = score

        untriaged = len(unread_messages) - triaged
        # If nothing was triaged, use -1 so it sorts to the bottom
        channel_results.append((
            max_importance,
            len(unread_messages),
            triaged,
            untriaged,
            channel,
        ))

    # Sort: triaged channels by max importance (desc), then untriaged channels
    channel_results.sort(key=lambda r: (-r[0], r[4]))

    # Print results
    for max_imp, unread, triaged, untriaged, channel in channel_results:
        if triaged > 0:
            print(f"  {max_imp:.2f}  {unread} unread ({triaged} triaged)  #{channel}")
        else:
            print(f"     -  {unread} unread (not triaged)  #{channel}")


main()
