#!/usr/bin/env bash
set -euo pipefail
# create_verifying_agent.sh -- Create a verifying agent with the correct env vars and labels.
#
# Usage: create_verifying_agent.sh <task-name> <working-agent-id> <message-file>
#
# Example:
#   create_verifying_agent.sh fix-login-bug agent-abc123 /tmp/verify-fix-login-bug.md
#
# Sets these env vars for the verifying agent:
#   WORKING_AGENT_ID          - the working agent's ID
#   WORKING_AGENT_BRANCH      - the working agent's git branch (mng/<task-name>)
#   WORKING_AGENT_BASE_BRANCH - the current branch of this mind (ie, what the working agent branched from)

if (( $# != 3 )); then
    echo "Usage: create_verifying_agent.sh <task-name> <working-agent-id> <message-file>" >&2
    exit 1
fi

TASK_NAME="$1"
WORKING_AGENT_ID="$2"
MESSAGE_FILE="$3"

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "Error: message file not found: $MESSAGE_FILE" >&2
    exit 1
fi

AGENT_NAME="$MIND_NAME-verify-$TASK_NAME"
WORKING_AGENT_BRANCH="mng/$TASK_NAME"
WORKING_AGENT_BASE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

mng create "$AGENT_NAME" \
    --env ROLE=verifying \
    --env WORKING_AGENT_ID="$WORKING_AGENT_ID" \
    --env WORKING_AGENT_BRANCH="$WORKING_AGENT_BRANCH" \
    --env WORKING_AGENT_BASE_BRANCH="$WORKING_AGENT_BASE_BRANCH" \
    --label role=verifying \
    --label mind="$MIND_NAME" \
    --message-file "$MESSAGE_FILE"
