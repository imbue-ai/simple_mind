#!/usr/bin/env python3
"""Assemble relevant context for a Slack message or reply.

Usage: gather_slack_context.py <event_id> <channel_name> <message_ts>

Outputs a simplified JSON object to stdout with the message context.

Requires SLACK_EVENTS_DIR to be set (the directory containing slack event streams).
Falls back to $MNG_AGENT_STATE_DIR/events/slack if not set.
"""

import json
import os
import sys
from pathlib import Path

MAX_PREVIOUS_MESSAGES = 5


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


def build_user_map(slack_dir: Path) -> dict[str, str]:
    """Build a mapping from user_id -> display name."""
    user_map: dict[str, str] = {}
    for events_file in [
        slack_dir / "user" / "created" / "events.jsonl",
        slack_dir / "user" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            raw = event.get("raw", {})
            user_id = raw.get("id", event.get("user_id", ""))
            profile = raw.get("profile", {})
            name = (
                profile.get("display_name")
                or raw.get("name")
                or profile.get("real_name")
                or user_id
            )
            if user_id and name:
                user_map[user_id] = name
    return user_map


def find_event_by_id(slack_dir: Path, event_id: str) -> dict | None:
    """Find an event by its event_id across all message/reply sources."""
    for subdir in ["message", "reply"]:
        for stream in ["created", "updated"]:
            events_file = slack_dir / subdir / stream / "events.jsonl"
            for event in load_jsonl(events_file):
                if event.get("event_id") == event_id:
                    return event
    return None


def find_message(slack_dir: Path, channel_name: str, message_ts: str) -> dict | None:
    """Find a specific message by channel and timestamp."""
    for events_file in [
        slack_dir / "message" / "created" / "events.jsonl",
        slack_dir / "message" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") == channel_name and event.get("message_ts") == message_ts:
                return event
    for events_file in [
        slack_dir / "reply" / "created" / "events.jsonl",
        slack_dir / "reply" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") == channel_name and event.get("reply_ts") == message_ts:
                return event
    return None


def format_message(raw: dict, user_map: dict[str, str], self_user_id: str | None) -> dict:
    """Format a raw Slack message into the simplified output format."""
    sender_id = raw.get("user", "")
    msg: dict = {
        "user": user_map.get(sender_id, sender_id),
        "message": raw.get("text", ""),
        "time": raw.get("ts", ""),
    }
    if sender_id == self_user_id:
        msg["is_from_self"] = True
    attachments = raw.get("attachments", [])
    if attachments:
        msg["attachments"] = [
            {k: att[k] for k in ["title", "text", "from_url", "service_name"] if k in att}
            for att in attachments
        ]
    return msg


def get_channel_messages(
    slack_dir: Path, channel_name: str, before_ts: str
) -> list[dict]:
    """Get all top-level messages in a channel before a given timestamp, sorted by ts."""
    messages = []
    seen: set[str] = set()
    for events_file in [
        slack_dir / "message" / "created" / "events.jsonl",
        slack_dir / "message" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") != channel_name:
                continue
            ts = event.get("raw", {}).get("ts", event.get("message_ts", ""))
            if ts and ts < before_ts and ts not in seen:
                seen.add(ts)
                messages.append(event)
    messages.sort(key=lambda e: e.get("raw", {}).get("ts", ""))
    return messages


def get_thread_messages(
    slack_dir: Path, channel_name: str, thread_ts: str
) -> list[dict]:
    """Get all replies in a thread, sorted by ts. Does not include the parent."""
    replies = []
    seen: set[str] = set()
    for events_file in [
        slack_dir / "reply" / "created" / "events.jsonl",
        slack_dir / "reply" / "updated" / "events.jsonl",
    ]:
        for event in load_jsonl(events_file):
            if event.get("channel_name") != channel_name:
                continue
            if event.get("thread_ts") != thread_ts:
                continue
            ts = event.get("raw", {}).get("ts", event.get("reply_ts", ""))
            # Skip the parent message if it appears in replies
            if ts == thread_ts:
                continue
            if ts not in seen:
                seen.add(ts)
                replies.append(event)
    replies.sort(key=lambda e: e.get("raw", {}).get("ts", ""))
    return replies


def get_self_user_id(slack_dir: Path) -> str | None:
    """Get the authenticated user's ID."""
    events = load_jsonl(slack_dir / "self_identity" / "created" / "events.jsonl")
    if events:
        return events[-1].get("user_id")
    return None


def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: gather_slack_context.py <event_id> <channel_name> <message_ts>", file=sys.stderr)
        sys.exit(1)

    event_id = sys.argv[1]
    channel_name = sys.argv[2]
    message_ts = sys.argv[3]

    slack_dir_str = os.environ.get("SLACK_EVENTS_DIR") or os.path.join(
        os.environ.get("MNG_AGENT_STATE_DIR", ""), "events", "slack"
    )
    slack_dir = Path(slack_dir_str)

    if not slack_dir.is_dir():
        print(f"Error: Slack events directory not found: {slack_dir}", file=sys.stderr)
        sys.exit(1)

    user_map = build_user_map(slack_dir)
    self_user_id = get_self_user_id(slack_dir)

    # Find the event
    event = find_event_by_id(slack_dir, event_id)
    if event is None:
        event = find_message(slack_dir, channel_name, message_ts)
    if event is None:
        print(json.dumps({"error": f"Could not find event {event_id} in {channel_name}"}))
        sys.exit(1)

    raw = event.get("raw", {})
    is_reply = bool(
        event.get("type") == "reply"
        or (raw.get("thread_ts") and raw.get("thread_ts") != raw.get("ts"))
    )
    thread_ts = event.get("thread_ts") or raw.get("thread_ts")

    # Use a list of (key, value) pairs to control output ordering
    entries: list[tuple[str, object]] = [
        ("event_id", event.get("event_id", event_id)),
        ("channel", channel_name),
        ("is_reply", is_reply),
    ]

    new_message = format_message(raw, user_map, self_user_id)

    if is_reply and thread_ts:
        # For replies: show the original (parent) message, plus previous replies as context
        parent_event = find_message(slack_dir, channel_name, thread_ts)
        if parent_event:
            entries.append(("original_message", format_message(
                parent_event.get("raw", {}), user_map, self_user_id
            )))

        all_replies = get_thread_messages(slack_dir, channel_name, thread_ts)
        # Find replies strictly before the current message
        current_ts = raw.get("ts", message_ts)
        prior_replies = [r for r in all_replies if r.get("raw", {}).get("ts", "") < current_ts]

        if prior_replies:
            earlier: list[dict] = []
            for r in prior_replies:
                earlier.append(format_message(r.get("raw", {}), user_map, self_user_id))
            entries.append(("earlier_messages", earlier))
    else:
        # For top-level messages: show previous channel messages as context
        prior_events = get_channel_messages(slack_dir, channel_name, raw.get("ts", message_ts))

        if prior_events:
            earlier = []
            if len(prior_events) > MAX_PREVIOUS_MESSAGES:
                earlier.append({"...": f"{len(prior_events) - MAX_PREVIOUS_MESSAGES} earlier messages omitted"})
                prior_events = prior_events[-MAX_PREVIOUS_MESSAGES:]
            for e in prior_events:
                earlier.append(format_message(e.get("raw", {}), user_map, self_user_id))
            entries.append(("earlier_messages", earlier))

    entries.append(("new_message", new_message))

    # Build ordered dict from entries
    from collections import OrderedDict
    result = OrderedDict(entries)

    print(json.dumps(result, ensure_ascii=False))


main()
