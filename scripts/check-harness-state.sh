#!/usr/bin/env bash
# =============================================================================
# check-harness-state.sh — Pre-flight validator for harness-analyze-and-improve
#
# Validates consistency between PROGRESS.md and harness/test-results.json
# before starting the pipeline loop. Read-only — never modifies files.
#
# Exit codes:
#   0 — all checks pass (warnings are non-fatal)
#   1 — contract files missing or evidence files absent
#   2 — harness/test-results.json is not valid JSON
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PROGRESS_FILE="$REPO_ROOT/PROGRESS.md"
RESULTS_FILE="$REPO_ROOT/harness/test-results.json"
EVIDENCE_READS="$REPO_ROOT/harness/.evidence-reads"
CANONICAL_TEMPLATE="$REPO_ROOT/.opencode/skills/analyze-and-improve/harness/templates/test-results.json"
BASE_TEMPLATE="$REPO_ROOT/harness/templates/test-results.json"
STOP_FILE="$REPO_ROOT/AGENT_STOP"

ERRORS=0
WARNINGS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

report_ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
report_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; WARNINGS=$((WARNINGS + 1)); }
report_err()  { echo -e "${RED}[ERR]${NC} $1"; ERRORS=$((ERRORS + 1)); }

echo "=== check-harness-state.sh ==="
echo ""

# --- Check 1: Contract files exist ---
echo "--- Check 1: Contract files exist ---"
if [ -f "$PROGRESS_FILE" ]; then
    report_ok "PROGRESS.md exists"
else
    report_err "PROGRESS.md not found"
fi

if [ -f "$RESULTS_FILE" ]; then
    report_ok "harness/test-results.json exists"
else
    report_err "harness/test-results.json not found"
fi

# --- Check 2: Valid JSON ---
echo ""
echo "--- Check 2: JSON validity ---"
if [ -f "$RESULTS_FILE" ]; then
    if python3 -c "import json; json.load(open('$RESULTS_FILE'))" 2>/dev/null; then
        phase_count=$(python3 -c "import json; d=json.load(open('$RESULTS_FILE')); phases=[k for k in d if k.startswith('phase')]; print(len(phases))")
        report_ok "test-results.json is valid JSON ($phase_count phases)"
    else
        report_err "test-results.json is not valid JSON — cannot parse"
    fi
fi

# --- Check 3: PROGRESS.md ↔ test-results.json phase consistency ---
echo ""
echo "--- Check 3: Progress vs results consistency ---"
if [ -f "$PROGRESS_FILE" ] && [ -f "$RESULTS_FILE" ]; then
    # Extract phase slugs from PROGRESS.md Done section
    done_phases=$(sed -n '/^## Done/,/^##/{/^$/d;/^##/d;p}' "$PROGRESS_FILE" | grep -oP 'phase-\d+' || true)

    while IFS= read -r phase; do
        [ -z "$phase" ] && continue
        # Check if this phase has passes: false in test-results.json
        passes_val=$(python3 -c "
import json
d = json.load(open('$RESULTS_FILE'))
entry = d.get('$phase', {})
print(entry.get('passes', 'unknown'))
" 2>/dev/null)
        if [ "$passes_val" = "false" ]; then
            report_warn "Stale state: $phase in Done but passes=false in test-results.json"
        fi
    done <<< "$done_phases"
fi

# --- Check 4: Evidence files exist on disk ---
echo ""
echo "--- Check 4: Evidence file existence ---"
if [ -f "$RESULTS_FILE" ]; then
    python3 -c "
import json, os, sys
repo = r'''$REPO_ROOT'''
d = json.load(open(r'''$RESULTS_FILE'''))
for phase, entry in d.items():
    if not phase.startswith('phase'):
        continue
    ev = entry.get('evidence', [])
    passes = entry.get('passes', False)
    eval_by = entry.get('evaluated_by')
    if passes is True or (eval_by is not None and eval_by != ''):
        for path in ev:
            full = os.path.join(repo, path)
            if not os.path.exists(full):
                print(f'ERR:{phase}:{path}')
            elif not os.path.isfile(full):
                print(f'ERR:{phase}:{path} (not a file)')
            elif os.path.getsize(full) == 0:
                print(f'WARN:{phase}:{path} (empty)')
" 2>&1 | while IFS= read -r line; do
        case "$line" in
            ERR:*) report_err "${line#ERR:}" ;;
            WARN:*) report_warn "${line#WARN:}" ;;
        esac
    done
fi

# --- Check 5: Artifacts manifest (post-migration) ---
echo ""
echo "--- Check 5: Artifacts manifest ---"
if [ -f "$PROGRESS_FILE" ]; then
    if grep -q 'phase-4' <<< "$(sed -n '/^## Done/,/^##/{/^$/d;/^##/d;p}' "$PROGRESS_FILE")" 2>/dev/null; then
        # Phase 4 is done — check for artifacts.yaml/.md in analysis dirs
        found_manifest=false
        for dir in "$REPO_ROOT"/docs/analysis/*/; do
            [ -d "$dir" ] || continue
            if [ -f "$dir"/*-artifacts.yaml ] && [ -f "$dir"/*-artifacts.md ]; then
                found_manifest=true
                report_ok "artifacts manifest found in $(basename "$dir")"
                break
            fi
        done
        if ! $found_manifest; then
            report_warn "Phase 4 in Done but no artifacts manifest found (legacy format?)"
        fi
    fi
fi

# --- Check 6: AGENT_STOP status ---
echo ""
echo "--- Check 6: AGENT_STOP status ---"
if [ -f "$STOP_FILE" ]; then
    echo -e "${YELLOW}[INFO]${NC} AGENT_STOP detected — pipeline will pause on next iteration"
else
    report_ok "AGENT_STOP not detected"
fi

# --- Check 7: Template divergence ---
echo ""
echo "--- Check 7: Template divergence ---"
if [ -f "$CANONICAL_TEMPLATE" ] && [ -f "$BASE_TEMPLATE" ]; then
    if diff -q "$CANONICAL_TEMPLATE" "$BASE_TEMPLATE" >/dev/null 2>&1; then
        report_ok "Templates are identical"
    else
        report_warn "Templates diverge — run sync or check Task 5"
    fi
else
    if [ ! -f "$CANONICAL_TEMPLATE" ]; then
        report_warn "Canonical template missing: $CANONICAL_TEMPLATE"
    fi
    if [ ! -f "$BASE_TEMPLATE" ]; then
        report_warn "Base template missing: $BASE_TEMPLATE"
    fi
fi

# --- Summary ---
echo ""
echo "=== Summary ==="
echo -e "${GREEN}$ERRORS errors${NC}, ${YELLOW}$WARNINGS warnings${NC}"

if [ "$ERRORS" -gt 0 ]; then
    exit 1
else
    exit 0
fi
