#!/usr/bin/env bash
set -euo pipefail
# create_verifying_agent.sh -- Create a verifying agent with the correct env vars and labels.
#
# Usage: create_verifying_agent.sh <agent-name> <working-agent-id> <message-file> [<ticket-id>]
#
# The agent name must start with "verify-" and end with "-<number>" (e.g., verify-fix-login-bug-0).
#
# Example:
#   create_verifying_agent.sh verify-fix-login-bug-0 agent-abc123 /tmp/verify-fix-login-bug.md tk-5c46

if (( $# < 3 || $# > 4 )); then
    echo "Usage: create_verifying_agent.sh <agent-name> <working-agent-id> <message-file> [<ticket-id>]" >&2
    exit 1
fi

AGENT_NAME="$1"
WORKING_AGENT_ID="$2"
MESSAGE_FILE="$3"
TICKET_ID="${4:-}"

# Validate naming convention: must start with "verify-" and end with "-<number>"
if [[ ! "$AGENT_NAME" =~ ^verify-.*-[0-9]+$ ]]; then
    echo "Error: agent name must start with 'verify-' and end with '-<number>' (e.g., verify-fix-login-bug-0)" >&2
    echo "Got: $AGENT_NAME" >&2
    exit 1
fi

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "Error: message file not found: $MESSAGE_FILE" >&2
    exit 1
fi

# Extract the task name from the agent name (strip "verify-" prefix and "-<N>" suffix)
# to construct the expected branch name.
TASK_NAME=$(echo "$AGENT_NAME" | sed 's/^verify-//; s/-[0-9]*$//')
WORKING_AGENT_BRANCH="mngr/$TASK_NAME"
WORKING_AGENT_BASE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

LABEL_ARGS=(
    --label role=verifying
    --label mind="$MIND_NAME"
)

if [ -n "$TICKET_ID" ]; then
    LABEL_ARGS+=(--label ticket="$TICKET_ID")
fi

mngr create "$AGENT_NAME" verifier \
    --env ROLE=verifying \
    --env WORKING_AGENT_ID="$WORKING_AGENT_ID" \
    --env WORKING_AGENT_BRANCH="$WORKING_AGENT_BRANCH" \
    --env WORKING_AGENT_BASE_BRANCH="$WORKING_AGENT_BASE_BRANCH" \
    "${LABEL_ARGS[@]}" \
    --message-file "$MESSAGE_FILE"
