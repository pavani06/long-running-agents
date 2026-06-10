#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VIOLATIONS=0
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

report_ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
report_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
report_err()  { echo -e "${RED}[ERR]${NC} $1"; VIOLATIONS=$((VIOLATIONS + 1)); }

echo "=== Obsidian Convention Check ==="
echo ""

# --- Check 1: Frontmatter in canonical docs ---
echo "--- Check 1: Frontmatter in docs/canonical/ ---"
for f in "$REPO_ROOT"/docs/canonical/*.md; do
    [ "$(basename "$f")" = ".gitkeep" ] && continue
    if head -1 "$f" | grep -q '^---$'; then
        if grep -q '^type:' "$f"; then
            report_ok "$(basename "$f")"
        else
            report_err "$(basename "$f") — has frontmatter delimiters but missing 'type:' field"
        fi
    else
        report_err "$(basename "$f") — missing YAML frontmatter (no '---' on line 1)"
    fi
done

# --- Check 2: Frontmatter in docs/analysis/ markdown files ---
echo ""
echo "--- Check 2: Frontmatter in docs/analysis/ ---"
while IFS= read -r -d '' f; do
    if head -1 "$f" | grep -q '^---$'; then
        if grep -q '^type:' "$f"; then
            report_ok "${f#$REPO_ROOT/}"
        else
            report_err "${f#$REPO_ROOT/} — missing 'type:' in frontmatter"
        fi
    else
        report_err "${f#$REPO_ROOT/} — missing YAML frontmatter"
    fi
done < <(find "$REPO_ROOT"/docs/analysis -name '*.md' -print0)

# --- Check 3: Frontmatter in curriculum index files ---
echo ""
echo "--- Check 3: Frontmatter in curriculum/ index files ---"
for f in "$REPO_ROOT"/curriculum/INDEX.md "$REPO_ROOT"/curriculum/MASTER_PLAN.md \
         "$REPO_ROOT"/curriculum/README.md "$REPO_ROOT"/curriculum/QUICK_START.md \
         "$REPO_ROOT"/curriculum/EXECUTION_PLAN.md "$REPO_ROOT"/curriculum/GLOSSARY.md \
         "$REPO_ROOT"/curriculum/FAQ.md; do
    if [ -f "$f" ]; then
        if head -1 "$f" | grep -q '^---$'; then
            if grep -q '^type:' "$f"; then
                report_ok "${f#$REPO_ROOT/}"
            else
                report_err "${f#$REPO_ROOT/} — missing 'type:' in frontmatter"
            fi
        else
            report_err "${f#$REPO_ROOT/} — missing YAML frontmatter"
        fi
    fi
done

# --- Check 4: Frontmatter in root index.md ---
echo ""
echo "--- Check 4: Frontmatter in root index.md ---"
if [ -f "$REPO_ROOT/index.md" ]; then
    if head -1 "$REPO_ROOT/index.md" | grep -q '^---$'; then
        if grep -q '^type:' "$REPO_ROOT/index.md"; then
            report_ok "index.md"
        else
            report_err "index.md — missing 'type:' in frontmatter"
        fi
    else
        report_err "index.md — missing YAML frontmatter"
    fi
else
    report_warn "index.md not found at repo root (not yet created?)"
fi

# --- Check 5: Raw markdown links in docs/canonical/ ---
echo ""
echo "--- Check 5: Raw markdown links in docs/canonical/ ---"
# Look for [text](path.md) that is NOT inside code blocks and NOT an external URL
for f in "$REPO_ROOT"/docs/canonical/*.md; do
    [ "$(basename "$f")" = ".gitkeep" ] && continue
    violations_in_file=$(grep -n '](.*\.md)' "$f" | grep -v 'http' | grep -v '^\s*`' || true)
    if [ -z "$violations_in_file" ]; then
        report_ok "$(basename "$f") — no raw markdown links"
    else
        while IFS= read -r line; do
            report_err "$(basename "$f"):$line — raw markdown link, should be [[wikilink]]"
        done <<< "$violations_in_file"
    fi
done

# --- Check 6: Broken wikilinks in docs/canonical/ ---
echo ""
echo "--- Check 6: Broken wikilinks in docs/canonical/ ---"
for f in "$REPO_ROOT"/docs/canonical/*.md; do
    [ "$(basename "$f")" = ".gitkeep" ] && continue
    # Extract [[target]] from each file, strip aliases after |
    wikilinks=$(grep -oP '\[\[\K[^\]|]+' "$f" || true)
    while IFS= read -r link; do
        [ -z "$link" ] && continue
        # Skip links that look external (contain ://)
        [[ "$link" =~ :// ]] && continue
        # The link is relative to repo root; resolve it
        target="$REPO_ROOT/${link}.md"
        if [ ! -f "$target" ]; then
            # Try without .md extension (maybe already has it)
            target="$REPO_ROOT/${link}"
            if [ ! -f "$target" ]; then
                report_err "$(basename "$f") — broken wikilink: [[$link]] (target not found)"
            fi
        fi
    done <<< "$wikilinks"
done

# --- Check 7: Cross-reference tag consistency (warning only) ---
echo ""
echo "--- Check 7: Cross-reference tag consistency in docs/canonical/ ---"
for f in "$REPO_ROOT"/docs/canonical/*.md; do
    [ "$(basename "$f")" = ".gitkeep" ] && continue
    # Extract tags from this file's frontmatter
    file_tags=$(sed -n '/^---$/,/^---$/p' "$f" | grep '^tags:' | sed 's/^tags: *//' | tr -d '[]"' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | grep -v '^$' || true)
    # Extract wikilinks
    wikilinks=$(grep -oP '\[\[\K[^\]|]+' "$f" || true)
    while IFS= read -r link; do
        [ -z "$link" ] && continue
        [[ "$link" =~ :// ]] && continue
        target="$REPO_ROOT/${link}.md"
        [ ! -f "$target" ] && target="$REPO_ROOT/${link}"
        [ ! -f "$target" ] && continue
        # Extract tags from linked file
        linked_tags=$(sed -n '/^---$/,/^---$/p' "$target" | grep '^tags:' | sed 's/^tags: *//' | tr -d '[]"' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | grep -v '^$' || true)
        # Check for at least one tag in common
        common=0
        for t in $file_tags; do
            for lt in $linked_tags; do
                [ "$t" = "$lt" ] && common=1 && break
            done
            [ "$common" -eq 1 ] && break
        done
        if [ "$common" -eq 0 ] && [ -n "$file_tags" ] && [ -n "$linked_tags" ]; then
            report_warn "$(basename "$f") — no tags in common with [[$link]]"
        fi
    done <<< "$wikilinks"
done

# --- Summary ---
echo ""
echo "=== Summary ==="
if [ "$VIOLATIONS" -eq 0 ]; then
    echo -e "${GREEN}All checks passed. Obsidian conventions are clean.${NC}"
    exit 0
else
    echo -e "${RED}$VIOLATIONS violation(s) found.${NC}"
    exit 1
fi
