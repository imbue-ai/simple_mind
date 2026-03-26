#!/usr/bin/env python3
"""Filter events from stdin, outputting one line per input line.

Filtered events are replaced with "{}" (empty JSON object) so that line
numbers are preserved between input and output.

Filters:
  - Events whose source ends with "/created" (we only handle /updated events)
  - Events from sources listed in ignored_sources.txt

Usage: cat events.jsonl | filter_events.py [--ignored-sources <path>]

The --ignored-sources flag specifies the path to a file containing one
source name per line. Defaults to "ignored_sources.txt" in the same
directory as the thinking agent's working directory.
"""

import json
import os
import sys
from pathlib import Path


def load_ignored_sources(path: Path) -> set[str]:
    """Load source names from a file, one per line. Ignores blank lines."""
    if not path.exists():
        return set()
    sources: set[str] = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                sources.add(line)
    return sources


def main() -> None:
    # Determine ignored sources file path
    ignored_path = Path("ignored_sources.txt")
    args = sys.argv[1:]
    if "--ignored-sources" in args:
        idx = args.index("--ignored-sources")
        if idx + 1 < len(args):
            ignored_path = Path(args[idx + 1])

    ignored_sources = load_ignored_sources(ignored_path)

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

        if source.endswith("/created"):
            print("{}")
        elif source in ignored_sources:
            print("{}")
        else:
            print(line)


main()
