#!/usr/bin/env bash
set -euo pipefail
# handle_event.sh -- Log handled-event acknowledgements as JSONL.
#
# Usage: handle_event.sh <handled_event_id> [handled_event_id ...]

if (( $# == 0 )); then
    echo "Usage: mng_log_handled.sh <handled_event_id> [...]" >&2
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

# -- main --
_MNG_LOG_FILE="$MNG_AGENT_STATE_DIR/events/handled_events/events.jsonl"
_MNG_LOG_TYPE="handled"
_MNG_LOG_SOURCE="handled_events"

mkdir -p "$(dirname "$_MNG_LOG_FILE")"

for handled_id in "$@"; do
    ts=$(_ts)
    eid="evt-$(head -c 16 /dev/urandom | xxd -p)"
    escaped_id=$(_json_escape "$handled_id")
    printf '{"timestamp":"%s","type":"%s","event_id":"%s","source":"%s","handled_event_id":"%s","pid":%s}\n' \
        "$ts" "$_MNG_LOG_TYPE" "$eid" "$_MNG_LOG_SOURCE" "$escaped_id" "$$" >> "$_MNG_LOG_FILE"
done
