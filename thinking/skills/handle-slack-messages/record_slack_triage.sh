#!/usr/bin/env bash
set -euo pipefail
# record_slack_triage.sh -- Log a single slack message triage result as JSONL.
#
# Usage: record_slack_triage.sh <event_id> --channel <name> --sender <name> --message-ts <ts>
#          --summary <text> --importance <float> --urgency <float>
#          --labels <json> --uncertainty <float> [--question <text>]...
#
# Required:
#   <event_id>              The event_id of the slack event being triaged
#   --channel <name>        Slack channel name
#   --sender <name>         Message sender name
#   --message-ts <ts>       Slack message timestamp
#   --summary <text>        One-line summary of the message
#   --importance <float>    Importance score (0.0 to 1.0)
#   --urgency <float>       Urgency score (0.0 to 1.0)
#   --labels <json>         JSON object of emoji label scores (keys are emoji names, values are floats)
#   --uncertainty <float>   Overall uncertainty about the triage
#
# Optional (repeatable):
#   --question <text>       A question about what you were uncertain about

if (( $# < 15 )); then
    echo "Usage: record_slack_triage.sh <event_id> --channel <name> --sender <name> --message-ts <ts> --summary <text> --importance <float> --urgency <float> --labels <json> --uncertainty <float> [--question <text>]..." >&2
    exit 1
fi

# -- parse args --
SLACK_EVENT_ID="$1"
shift

CHANNEL=""
SENDER=""
MESSAGE_TS=""
SUMMARY=""
IMPORTANCE=""
URGENCY=""
LABELS=""
UNCERTAINTY=""
QUESTIONS=()

while (( $# > 0 )); do
    case "$1" in
        --channel)        CHANNEL="$2";       shift 2 ;;
        --sender)         SENDER="$2";        shift 2 ;;
        --message-ts)     MESSAGE_TS="$2";    shift 2 ;;
        --summary)        SUMMARY="$2";       shift 2 ;;
        --importance)     IMPORTANCE="$2";    shift 2 ;;
        --urgency)        URGENCY="$2";       shift 2 ;;
        --labels)         LABELS="$2";        shift 2 ;;
        --uncertainty)    UNCERTAINTY="$2";   shift 2 ;;
        --question)       QUESTIONS+=("$2");  shift 2 ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

# -- validate required args --
for var_name in CHANNEL SENDER MESSAGE_TS SUMMARY IMPORTANCE URGENCY LABELS UNCERTAINTY; do
    if [[ -z "${!var_name}" ]]; then
        echo "Error: --$(echo "$var_name" | tr '[:upper:]' '[:lower:]' | tr '_' '-') is required" >&2
        exit 1
    fi
done

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
_MNG_LOG_FILE="$MNG_AGENT_STATE_DIR/events/handled_slack_messages/events.jsonl"

mkdir -p "$(dirname "$_MNG_LOG_FILE")"

ts=$(_ts)
eid="evt-$(head -c 16 /dev/urandom | xxd -p)"
escaped_slack_event_id=$(_json_escape "$SLACK_EVENT_ID")
escaped_channel=$(_json_escape "$CHANNEL")
escaped_sender=$(_json_escape "$SENDER")
escaped_message_ts=$(_json_escape "$MESSAGE_TS")
escaped_summary=$(_json_escape "$SUMMARY")
questions_json=$(_json_array "${QUESTIONS[@]+"${QUESTIONS[@]}"}")

printf '{"timestamp":"%s","type":"slack_triage","event_id":"%s","source":"handled_slack_messages","slack_event_id":"%s","channel":"%s","sender":"%s","message_ts":"%s","summary":"%s","importance":%s,"urgency":%s,"labels":%s,"uncertainty":%s,"questions":%s,"pid":%s}\n' \
    "$ts" "$eid" "$escaped_slack_event_id" "$escaped_channel" "$escaped_sender" "$escaped_message_ts" "$escaped_summary" \
    "$IMPORTANCE" "$URGENCY" \
    "$LABELS" \
    "$UNCERTAINTY" "$questions_json" "$$" >> "$_MNG_LOG_FILE"
