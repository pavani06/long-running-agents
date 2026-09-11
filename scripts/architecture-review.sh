#!/usr/bin/env bash
set -euo pipefail
architecture_install="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source "$architecture_install/runtime.env"
mkdir -p "$ARCHITECTURE_STATE"
exec /usr/bin/flock -n -E 75 "$ARCHITECTURE_STATE/run.lock" \
  "$ARCHITECTURE_NODE" "$architecture_install/scripts/architecture-scheduled.js" \
  --state "$ARCHITECTURE_STATE" --repo "$ARCHITECTURE_REPO" --model "$ARCHITECTURE_MODEL" "$@"
