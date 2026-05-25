#!/usr/bin/env bash
#
# Basic gate verification suite.
# Runs the four gate entrypoints, validates their exit codes,
# ensures they emit JSON, and checks for required top-level fields.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"
NC="\033[0m"

status_text() {
  case "$1" in
    pass) printf "%bPASS%b" "$GREEN" "$NC" ;;
    fail) printf "%bFAIL%b" "$RED" "$NC" ;;
    skip) printf "%bSKIP%b" "$YELLOW" "$NC" ;;
    *) printf "%s" "$1" ;;
  esac
}

compress_whitespace() {
  local input="$1"
  # Normalize whitespace and trim leading/trailing spaces.
  input="$(printf '%s' "$input" | tr '\r' ' ' | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')"
  # Remove leading/trailing spaces that may remain after sed.
  input="${input#"${input%%[![:space:]]*}"}"
  input="${input%"${input##*[![:space:]]}"}"
  printf '%s' "$input"
}

format_command() {
  local formatted=""
  local arg quoted
  for arg in "$@"; do
    printf -v quoted '%q' "$arg"
    if [[ -z "$formatted" ]]; then
      formatted="$quoted"
    else
      formatted+=" $quoted"
    fi
  done
  printf "%s" "$formatted"
}

GATES=("session_start" "pre_send_chat" "pre_consolidate" "pre_goal_transition")
declare -A SUMMARY_OUTCOME
declare -A SUMMARY_NOTES

overall_pass=1
required_fields=("gate" "status" "checks" "warnings" "errors" "timestamp")

for gate in "${GATES[@]}"; do
  case "$gate" in
    session_start)
      cmd=("$SCRIPT_DIR/session_start.sh")
      ;;
    pre_send_chat)
      cmd=("python3" "$SCRIPT_DIR/pre_send_chat.py" "This is a gate suite validation message to exercise the pre_send_chat checks.")
      ;;
    pre_consolidate)
      cmd=("python3" "$SCRIPT_DIR/pre_consolidate.py")
      ;;
    pre_goal_transition)
      cmd=("python3" "$SCRIPT_DIR/pre_goal_transition.py")
      ;;
    *)
      echo -e "${YELLOW}Unknown gate: ${gate}${NC}" >&2
      continue
      ;;
  esac

  stdout_file="$(mktemp)"
  stderr_file="$(mktemp)"

  if "${cmd[@]}" >"$stdout_file" 2>"$stderr_file"; then
    exit_code=0
  else
    exit_code=$?
  fi

  stdout_content="$(cat "$stdout_file")"
  stderr_content="$(cat "$stderr_file")"

  json_outcome="fail"
  json_message="No stdout captured"
  if [[ -s "$stdout_file" ]]; then
    json_message=$(python3 - "$stdout_file" <<'PY' 2>&1
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
try:
    raw = path.read_text()
except Exception as exc:  # noqa: BLE001
    print(f"Read error: {exc}")
    sys.exit(2)

try:
    json.loads(raw)
except json.JSONDecodeError as exc:
    print(f"JSONDecodeError: {exc}")
    sys.exit(1)

print("valid JSON")
PY
    )
    json_status=$?
    if [[ $json_status -eq 0 ]]; then
      json_outcome="pass"
    else
      json_outcome="fail"
    fi
  fi

  field_outcome="fail"
  field_message="Skipped (invalid JSON)"
  gate_status_value=""
  gate_name_value=""

  if [[ "$json_outcome" == "pass" ]]; then
    field_message=$(python3 - "$stdout_file" "${required_fields[@]}" <<'PY' 2>&1
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
expected = sys.argv[2:]
data = json.loads(path.read_text())
missing = [field for field in expected if field and field not in data]
if missing:
    print("Missing fields: " + ", ".join(missing))
    sys.exit(1)

print("all required fields present")
PY
    )
    field_status=$?
    if [[ $field_status -eq 0 ]]; then
      field_outcome="pass"
    else
      field_outcome="fail"
    fi

    gate_status_value=$(python3 - "$stdout_file" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text())
print(data.get("status", ""))
PY
    )

    gate_name_value=$(python3 - "$stdout_file" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text())
print(data.get("gate", ""))
PY
    )
  fi

  rm -f "$stdout_file" "$stderr_file"

  exit_outcome=$([[ $exit_code -eq 0 ]] && echo "pass" || echo "fail")
  gate_pass=1
  [[ "$exit_outcome" == "pass" ]] || gate_pass=0
  [[ "$json_outcome" == "pass" ]] || gate_pass=0
  [[ "$field_outcome" == "pass" ]] || gate_pass=0

  [[ $gate_pass -eq 1 ]] || overall_pass=0

  printf '%s\n' '----------------------------------------'
  printf 'Gate: %s\n' "$gate"
  printf '  Command: %s\n' "$(format_command "${cmd[@]}")"
  printf '  Exit Code: %s (%s)\n' "$(status_text "$exit_outcome")" "$exit_code"
  printf '  JSON Valid: %s' "$(status_text "$json_outcome")"
  if [[ -n "$json_message" ]]; then
    printf ' - %s' "$(compress_whitespace "$json_message")"
  fi
  printf '\n'
  printf '  Fields Check: %s' "$(status_text "$field_outcome")"
  if [[ -n "$field_message" ]]; then
    printf ' - %s' "$(compress_whitespace "$field_message")"
  fi
  printf '\n'
  if [[ -n "$gate_name_value" || -n "$gate_status_value" ]]; then
    printf '  Gate Reported: '
    [[ -n "$gate_name_value" ]] && printf '%s ' "$gate_name_value"
    [[ -n "$gate_status_value" ]] && printf '(status: %s)' "$gate_status_value"
    printf '\n'
  fi

  if [[ -n "$stdout_content" ]]; then
    printf '  Stdout:\n'
    printf '%s\n' "$stdout_content" | sed 's/^/    /'
  else
    printf '  Stdout: (empty)\n'
  fi

  if [[ -n "$stderr_content" ]]; then
    printf '  Stderr:\n'
    printf '%s\n' "$stderr_content" | sed 's/^/    /'
  else
    printf '  Stderr: (empty)\n'
  fi

  summary_reasons=()
  if [[ "$exit_outcome" != "pass" ]]; then
    summary_reasons+=("exit ${exit_code}")
  fi
  if [[ "$json_outcome" != "pass" ]]; then
    summary_reasons+=("json invalid")
  fi
  if [[ "$field_outcome" != "pass" ]]; then
    summary_reasons+=("fields check failed")
  fi
  if ((${#summary_reasons[@]})); then
    summary_note="$(IFS='; '; printf '%s' "${summary_reasons[*]}")"
  else
    summary_note=""
  fi
  summary_note="$(compress_whitespace "$summary_note")"

  SUMMARY_OUTCOME["$gate"]=$([[ $gate_pass -eq 1 ]] && echo "pass" || echo "fail")
  SUMMARY_NOTES["$gate"]="$summary_note"
done

printf '%s\n' '========================================'
printf 'Summary:\n'
for gate in "${GATES[@]}"; do
  outcome="${SUMMARY_OUTCOME[$gate]}"
  note="${SUMMARY_NOTES[$gate]}"
  [[ -z "$outcome" ]] && outcome="fail"
  printf '  - %s: %s' "$gate" "$(status_text "$outcome")"
  if [[ -n "$note" ]]; then
    printf ' (%s)' "$note"
  fi
  printf '\n'
done

if [[ $overall_pass -eq 1 ]]; then
  printf '%bAll gates passed basic checks.%b\n' "$GREEN" "$NC"
  exit 0
else
  printf '%bOne or more gates failed basic checks.%b\n' "$RED" "$NC"
  exit 1
fi
