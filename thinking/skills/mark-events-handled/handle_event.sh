#!/usr/bin/env bash
set -euo pipefail
# handle_event.sh -- Log a single handled-event acknowledgement as JSONL.
#
# Usage: handle_event.sh <handled_event_id> --summary <text> --confidence <float> [--ticket <id>]... [--message <id>]...
#
# Required:
#   <handled_event_id>    The event_id of the event that was handled
#   --summary <text>      Short description of how the event was handled
#   --confidence <float>  Confidence that the event was handled correctly (0.0 to 1.0)
#
# Optional (repeatable):
#   --ticket <id>         Ticket ID created as a result of handling this event
#   --message <id>        Message ID where clarification was requested

if (( $# < 5 )); then
    echo "Usage: handle_event.sh <handled_event_id> --summary <text> --confidence <float> [--ticket <id>]... [--message <id>]..." >&2
    exit 1
fi

# -- parse args --
HANDLED_ID="$1"
shift

SUMMARY=""
CONFIDENCE=""
TICKET_IDS=()
MESSAGE_IDS=()

while (( $# > 0 )); do
    case "$1" in
        --summary)
            SUMMARY="$2"
            shift 2
            ;;
        --confidence)
            CONFIDENCE="$2"
            shift 2
            ;;
        --ticket)
            TICKET_IDS+=("$2")
            shift 2
            ;;
        --message)
            MESSAGE_IDS+=("$2")
            shift 2
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

if [[ -z "$SUMMARY" ]]; then
    echo "Error: --summary is required" >&2
    exit 1
fi
if [[ -z "$CONFIDENCE" ]]; then
    echo "Error: --confidence is required" >&2
    exit 1
fi

# -- timestamp detection (from mng_log.sh) --
_MNG_TIMESTAMP_METHOD=""
_detect_ts() {
    local t
    t=$(date -u +"%Y-%m-%dT%H:%M:%S.%NZ" 2>/dev/null) || true
    if [[ "$t" != *"%N"* ]]; then _MNG_TIMESTAMP_METHOD="gnu"; return; fi
    if perl -MTime::HiRes=gettimeofday -e '1' 2>/dev/null; then _MNG_TIMESTAMP_METHOD="perl"; return; fi
    _MNG_TIMESTAMP_METHOD="basic"
}
_detect_ts

_ts() {
    case "$_MNG_TIMESTAMP_METHOD" in
        gnu)  date -u +"%Y-%m-%dT%H:%M:%S.%NZ" ;;
        perl) perl -MTime::HiRes=gettimeofday -MPOSIX=strftime \
                  -e '($s,$us)=gettimeofday();printf "%s.%09dZ\n",strftime("%Y-%m-%dT%H:%M:%S",gmtime($s)),$us*1000' ;;
        basic) date -u +"%Y-%m-%dT%H:%M:%S.000000000Z" ;;
    esac
}

_json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

# -- build JSON array helper --
_json_array() {
    local arr=("$@")
    if (( ${#arr[@]} == 0 )); then
        printf '[]'
        return
    fi
    printf '['
    local first=true
    for item in "${arr[@]}"; do
        if $first; then first=false; else printf ','; fi
        printf '"%s"' "$(_json_escape "$item")"
    done
    printf ']'
}

# -- main --
_MNG_LOG_FILE="$MNG_AGENT_STATE_DIR/events/handled_events/events.jsonl"

mkdir -p "$(dirname "$_MNG_LOG_FILE")"

ts=$(_ts)
eid="evt-$(head -c 16 /dev/urandom | xxd -p)"
escaped_handled_id=$(_json_escape "$HANDLED_ID")
escaped_summary=$(_json_escape "$SUMMARY")
ticket_ids_json=$(_json_array "${TICKET_IDS[@]+"${TICKET_IDS[@]}"}")
message_ids_json=$(_json_array "${MESSAGE_IDS[@]+"${MESSAGE_IDS[@]}"}")

printf '{"timestamp":"%s","type":"handled","event_id":"%s","source":"handled_events","handled_event_id":"%s","summary":"%s","confidence":%s,"ticket_ids":%s,"message_ids":%s,"pid":%s}\n' \
    "$ts" "$eid" "$escaped_handled_id" "$escaped_summary" "$CONFIDENCE" "$ticket_ids_json" "$message_ids_json" "$$" >> "$_MNG_LOG_FILE"
