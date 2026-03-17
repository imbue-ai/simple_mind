#!/usr/bin/env bash
set -euo pipefail
# create_working_agent.sh -- Create a working agent with the correct env vars and labels.
#
# Usage: create_working_agent.sh <task-name> <message-file>
#
# Example:
#   create_working_agent.sh fix-login-bug /tmp/task-fix-login-bug.md

if (( $# != 2 )); then
    echo "Usage: create_working_agent.sh <task-name> <message-file>" >&2
    exit 1
fi

TASK_NAME="$1"
MESSAGE_FILE="$2"

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "Error: message file not found: $MESSAGE_FILE" >&2
    exit 1
fi

AGENT_NAME="$MIND_NAME-$TASK_NAME"

mng create "$AGENT_NAME" \
    --env ROLE=working \
    --label role=working \
    --label mind="$MIND_NAME" \
    --message-file "$MESSAGE_FILE"
