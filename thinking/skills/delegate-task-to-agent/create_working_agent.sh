#!/usr/bin/env bash
set -euo pipefail
# create_working_agent.sh -- Create a working agent with the correct env vars and labels.
#
# Usage: create_working_agent.sh <task-name> <message-file> [<ticket-id>]
#
# Example:
#   create_working_agent.sh fix-login-bug /tmp/task-fix-login-bug.md tk-5c46

if (( $# < 2 || $# > 3 )); then
    echo "Usage: create_working_agent.sh <task-name> <message-file> [<ticket-id>]" >&2
    exit 1
fi

TASK_NAME="$1"
MESSAGE_FILE="$2"
TICKET_ID="${3:-}"

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "Error: message file not found: $MESSAGE_FILE" >&2
    exit 1
fi

LABEL_ARGS=(
    --label role=working
    --label mind="$MIND_NAME"
)

if [ -n "$TICKET_ID" ]; then
    LABEL_ARGS+=(--label ticket="$TICKET_ID")
fi

mngr create "$TASK_NAME" worker \
    --env ROLE=working \
    "${LABEL_ARGS[@]}" \
    --message-file "$MESSAGE_FILE"
