# PROMPTS-08: Obsidian Governance — Frente 4

> Entrega este prompt APOS a execucao do PROMPTS-07 (adaptacao). Ele cria a camada de
> governanca que garante que documentos futuros nasçam Obsidian-ready.

```
TASK:
Create the governance layer that ensures all future documents in `long-running-agents` are born Obsidian-ready and existing documents stay compliant. This involves: (1) adding a document convention rule to AGENTS.md, (2) creating a validation script, (3) updating system-of-record.md to reference the new convention, and (4) updating the PR template with a compliance checklist.

EXPECTED OUTCOME:
- AGENTS.md gains a new `Rule 16: Obsidian Document Conventions` section defining frontmatter schemas, wikilink rules, tag derivation from system-of-record domains, and slug conventions
- A new `scripts/check-obsidian-conventions.sh` script that validates compliance and exits 0 (clean) or 1 (violations found) with a clear report
- `docs/system-of-record.md` gains a reference to the new convention in its Canonical Docs section
- `.github/PULL_REQUEST_TEMPLATE.md` gains a checkbox for Obsidian convention compliance
- After completion, any agent or contributor can create a new document following the conventions, and the script validates their work

REQUIRED TOOLS:
- Read (inspect AGENTS.md, system-of-record.md, PULL_REQUEST_TEMPLATE.md, and a few canonical docs for existing patterns)
- Edit (append/modify sections in AGENTS.md, system-of-record.md, PR template)
- Write (create scripts/check-obsidian-conventions.sh)
- Bash: `chmod +x scripts/check-obsidian-conventions.sh`, run the script to verify it works

MUST DO:

### PART 1 — Add Rule 16 to AGENTS.md

Insert a new rule section in `/mnt/c/Users/pavan/long-running-agents/AGENTS.md` after the existing Rule 15. The section must read:

```
## Rule 16: Obsidian Document Conventions

All documentation intended for human consumption through Obsidian MUST follow these
conventions. The validation script `scripts/check-obsidian-conventions.sh` enforces them.

### 16.1 Frontmatter is mandatory

Every markdown file under `docs/canonical/`, `docs/analysis/`, and `curriculum/` index
files MUST have YAML frontmatter with at minimum `type:` and `tags:`. The frontmatter
block is delimited by `---` on its own lines at the very start of the file (line 1).

### 16.2 Document types and their required fields

| type | Directories | Required fields | Optional fields |
|---|---|---|---|
| `canonical` | `docs/canonical/` | `title`, `type`, `tags` | `aliases`, `last_updated`, `relates-to`, `sources` |
| `analysis` | `docs/analysis/` | `title`, `type`, `tags`, `date` | `aliases`, `last_updated`, `relates-to`, `sources` |
| `system-of-record` | `docs/` | `title`, `type`, `tags`, `last_updated` | `aliases` |
| `plan` | `docs/plans/` | `title`, `type`, `tags`, `date` | `aliases`, `last_updated` |
| `curriculum-index` | `curriculum/` (top-level only) | `title`, `type`, `tags`, `last_updated` | `aliases` |
| `lesson` | `curriculum/0*-*/` | `title`, `type`, `tags`, `level` | `duration`, `aliases` |
| `exercise` | `curriculum/0*-*/exercises/` | `title`, `type`, `tags`, `level` | `duration`, `aliases` |
| `case-study` | `curriculum/0*-*/case-studies/` | `title`, `type`, `tags` | `aliases` |
| `index` | root | `title`, `type`, `tags` | `aliases`, `last_updated` |

All YAML list fields use `[]` for empty, `["single"]` for one value, `["a", "b"]` for
multiple. Fields not applicable to a document type MUST NOT be present.

### 16.3 Wikilinks for all cross-references

Use `[[path/relative/to/repo/root|Display Text]]` for every reference to another
markdown file in this repository. Never use `[text](path.md)`. Leave external URLs
(`https://...`) as standard markdown links. Do not convert links inside fenced code
blocks or inline code.

### 16.4 Tags — derivadas dos dominios do projeto

As tags de um documento DEVEM corresponder a um dominio documentado em
[[docs/system-of-record|system-of-record.md]], na secao "Dominios do projeto".

Use o nome do dominio em lowercase com hifens. Exemplos:
- "Agentes e orquestracao" → `agentes-orquestracao`
- "Curriculo e conteudo" → `curriculo-conteudo`
- "Stack e tooling" → `stack-tooling`
- "Governanca de repositorio" → `governanca`

Tags mais especificas que um dominio sao permitidas desde que ancoradas em um topico
existente no system-of-record ou em um canonical doc. Exemplos validos:
`context-engineering`, `evals`, `error-handling`, `harness`, `12-factor-agents`,
`production` — todos referenciam topicos tratados nos canonicos ou analises listados
no system-of-record.

Se um documento introduz um topico novo que nao esta no system-of-record, adicione-o
primeiro ao system-of-record (na secao do dominio correspondente) e depois use a tag
correspondente. Nao crie tags para topicos nao documentados.

Tags estruturais (independentes de dominio):
- `index` — catalogos, navegacao, mapas
- `reference` — glossarios, FAQs, referencias

### 16.5 Slug naming

Filenames use lowercase with hyphens: `error-context-hygiene.md`. No spaces, no
underscores (except `_moc-` prefix for Maps of Content), no special characters.
The filename is the canonical identifier — renaming breaks wikilinks.

### 16.6 Validation

Run `bash scripts/check-obsidian-conventions.sh` before committing documentation
changes. The script checks:
- Files in `docs/canonical/` and `docs/analysis/` have YAML frontmatter with `type`
- No raw `[text](path.md)` links remain in monitored directories
- No broken `[[wikilinks]]` point to nonexistent files
```

Insert this as a new section at the end of AGENTS.md, after Rule 15, with a blank line separating them.

### PART 2 — Create the validation script

Create `/mnt/c/Users/pavan/long-running-agents/scripts/check-obsidian-conventions.sh` with this behavior:

```bash
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
```

Make the script executable: `chmod +x scripts/check-obsidian-conventions.sh`.

### PART 3 — Update docs/system-of-record.md

Read `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md`. Find the "Documentacao canonica pendente" section (near the line that says `docs/canonical/ nao esta mais vazio. Ha 9 padroes canonicos ativos.`). Update the count from 9 to 15 to match the actual table (which has 15 entries).

In the Canonical Docs table (the table listing all canonical patterns), add a new row at the end:

```
| `obsidian-document-conventions.md` | Convencoes de frontmatter, wikilinks, tags e validacao para documentos Obsidian-ready (AGENTS.md Rule 16) |
```

Then find the "Documentos esperados quando o dominio correspondente amadurecer" table. Add a new row:

```
| `obsidian-document-conventions.md` | AGENTS.md Rule 16 ja cobre — documento canonico so precisa ser criado se a convencao crescer alem de uma regra |
```

### PART 4 — Update PR template

Read `/mnt/c/Users/pavan/long-running-agents/.github/PULL_REQUEST_TEMPLATE.md`. Add this checkbox as the last item in the existing checklist (or as a new standalone item if there is no checklist):

```
- [ ] Obsidian conventions: `bash scripts/check-obsidian-conventions.sh` passes
```

### VERIFICATION

After all edits:
1. Read the modified AGENTS.md to confirm Rule 16 is present and complete
2. Run `bash scripts/check-obsidian-conventions.sh` — it should execute without errors and report on the current state of the repo. Expect violations if PROMPTS-07 has not yet run.
3. Confirm the script is executable: `test -x scripts/check-obsidian-conventions.sh && echo "executable" || echo "not executable"`
4. Read the modified system-of-record.md to confirm the new rows are present and the count was updated
5. Read the modified PR template to confirm the checkbox is present

MUST NOT DO:
- Do NOT modify any existing rules in AGENTS.md (Rules 0-15 stay untouched)
- Do NOT modify the behavior or content of existing canonical docs, analysis docs, or curriculum files
- Do NOT run PROMPTS-07 (adding frontmatter to canonical docs, creating index.md, etc.) — this prompt is ONLY for governance
- Do NOT create `docs/canonical/obsidian-document-conventions.md` — the AGENTS.md rule is sufficient; a separate canonical doc would duplicate it
- Do NOT add npm dependencies or modify package.json
- Do NOT modify CI configs (.github/workflows/)
- Do NOT change file names or directory structure
- Do NOT enforce a closed tag vocabulary in the validation script — the script only checks that `tags:` is present in frontmatter, NOT the specific tag values. Tag consistency is a review concern, not an automated check.

CONTEXT:

Repository root: `/mnt/c/Users/pavan/long-running-agents`

This repo is being adapted for Obsidian compatibility. PROMPTS-07 handles adding frontmatter and wikilinks to existing files. This governance prompt (PROMPTS-08) ensures that future documents maintain that standard.

The existing AGENTS.md at `/mnt/c/Users/pavan/long-running-agents/AGENTS.md` has 15 rules (Rule 0 through Rule 15). Rule 16 is being added at the end.

The `raw-knowledge` repo at `/mnt/c/Users/pavan/Raw-Knowledge/AGENTS.md` is the reference for Obsidian conventions. Key patterns to mirror:
- Closed relationship vocabulary in YAML frontmatter
- `[[wikilinks]]` for all internal references
- Folders encode type, tags encode topic
- Mandatory frontmatter on every page
- Slug naming (lowercase-hyphens)

However, `long-running-agents` is a software project, not a pure knowledge base, so the conventions are adapted: fewer document types, simpler relationship vocabulary, and only monitored directories are enforced, not every markdown file in the repo.

**Key design decision — tags are derived from system-of-record, not a frozen list:**
The tag vocabulary is NOT hardcoded in AGENTS.md or the validation script. Instead, 16.4 establishes that tags must come from domains documented in `docs/system-of-record.md`. This means:
- When a new domain is added to system-of-record, new tags become valid automatically
- The script does NOT validate tag values — it only checks that `tags:` exists in frontmatter
- Tag consistency is reviewed by humans, not enforced by automation
- This avoids the fragility of a frozen tag list that rejects valid new topics

For the validation script's Check 5 (raw markdown links), the grep pattern `](.*\.md)` catches `[text](path.md)` patterns. The script excludes lines with `http` (external URLs) and lines starting with whitespace+backtick (inline code, heuristic). This is intentionally simple — false negatives are acceptable; false positives are not.
```
