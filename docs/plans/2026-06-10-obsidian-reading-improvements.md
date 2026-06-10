# Obsidian Reading Improvements — Execution Plan

**Objective:** Improve Obsidian reading/navigation experience across 7 fronts: Dataview dashboards, templates, bookmarks, CSS snippets, community plugins, aliases, and canvas maps.
**Phase:** Implementation
**Dependencies:** None (greenfield Obsidian customization on existing vault)
**Estimated duration:** 2-3 sessions

---

## Front 1: Dataview Dashboards

**Artefacts:**
- Input: `docs/system-of-record.md` (tag taxonomy), `curriculum/INDEX.md` (navigation structure), existing frontmatter across `docs/canonical/`, `docs/analysis/`, `curriculum/`
- Output: `dashboards/obsidian-home.md` (or multiple dashboard files)

- [ ] **Step 1: Create dashboards/ directory**
  Command: `mkdir -p dashboards/`
  Expected: directory exists

- [ ] **Step 2: Create obsidian-home.md with dynamic MOC**
  Command: write file with dataview TABLE/FLATTEN queries listing docs by type, tags, and last_updated
  Expected: valid markdown with dataview code blocks, proper frontmatter (type: index, tags: ["index", "dashboard"])

- [ ] **Step 3: Create curriculum-progress.md dashboard**
  Command: write file with dataview TABLE grouping curriculum lessons by nivel
  Expected: valid markdown with dataview code blocks, proper frontmatter

- [ ] **Step 4: Create analysis-dashboard.md**
  Command: write file with dataview TABLE grouping analyses by domain and date
  Expected: valid markdown with dataview code blocks, proper frontmatter

- [ ] **Step 5: Verification**
  Criteria: all .md files have valid frontmatter with type and tags; `scripts/check-obsidian-conventions.sh` passes on new files; dataview code blocks are syntactically valid

---

## Front 2: Templates Configuration

**Artefacts:**
- Input: AGENTS.md frontmatter rules (lines 120-175), existing canonical/analysis/curriculum frontmatter examples
- Output: `templates/` directory with 4 template files

- [ ] **Step 1: Create templates/ directory**
  Command: `mkdir -p templates/`
  Expected: directory exists

- [ ] **Step 2: Create template-canonical.md**
  Command: write skeleton with frontmatter fields: title, type: canonical, aliases, tags, last_updated, relates-to, sources
  Expected: placeholder frontmatter with YAML list format, body with ## sections stubs

- [ ] **Step 3: Create template-analysis.md**
  Command: write skeleton with frontmatter fields: title, type: analise, aliases, tags, date, domain
  Expected: placeholder frontmatter, body with summary/analysis/recommendations stubs

- [ ] **Step 4: Create template-curriculum-lesson.md**
  Command: write skeleton with frontmatter fields: title, type: curriculo-conteudo, aliases, tags, nivel, last_updated
  Expected: placeholder frontmatter, body with lesson structure stubs

- [ ] **Step 5: Create template-curriculum-index.md**
  Command: write skeleton with frontmatter fields: title, type: curriculum-index, aliases, tags, last_updated
  Expected: placeholder frontmatter, body with navigation structure stubs

- [ ] **Step 6: Verification**
  Criteria: all 4 templates have valid frontmatter per AGENTS.md; `scripts/check-obsidian-conventions.sh` passes

---

## Front 5: Bookmarks

**Artefacts:**
- Input: `.obsidian/workspace.json` (current layout with empty bookmarks)
- Output: `.obsidian/workspace.json` (updated with bookmarks)

- [ ] **Step 1: Read current workspace.json**
  Command: read `.obsidian/workspace.json`
  Expected: understand bookmarks JSON structure

- [ ] **Step 2: Add bookmarks for key navigation pages**
  Command: edit workspace.json bookmarks section to include: index.md, curriculum/INDEX.md, curriculum/QUICK_START.md, docs/system-of-record.md, curriculum/MASTER_PLAN.md, curriculum/GLOSSARY.md, curriculum/FAQ.md
  Expected: bookmarks array populated with vault-relative paths

- [ ] **Step 3: Verification**
  Criteria: workspace.json is valid JSON; bookmarks section contains all 7 entries

---

## Front 6: CSS Snippets

**Artefacts:**
- Input: `.obsidian/appearance.json` (empty)
- Output: `.obsidian/snippets/` with CSS files, updated `.obsidian/appearance.json`

- [ ] **Step 1: Create .obsidian/snippets/ directory**
  Command: `mkdir -p .obsidian/snippets/`
  Expected: directory exists

- [ ] **Step 2: Create note-type-colors.css**
  Command: write CSS rules that style notes based on `cssclass` or `data-type` property — subtle left border colors for canonical, analysis, curriculum-content, curriculum-index
  Expected: valid CSS, no syntax errors

- [ ] **Step 3: Create readability.css**
  Command: write CSS for max reading width (~720px), comfortable line-height, heading hierarchy spacing
  Expected: valid CSS, no syntax errors

- [ ] **Step 4: Update appearance.json to enable snippets**
  Command: edit `.obsidian/appearance.json` to reference the snippet files
  Expected: valid JSON with cssSnippets array

- [ ] **Step 5: Verification**
  Criteria: CSS files are valid; appearance.json is valid JSON; snippets referenced correctly

---

## Front 7: Community Plugins

**Artefacts:**
- Input: `.obsidian/core-plugins.json` (baseline enabled plugins)
- Output: `.obsidian/community-plugins.json`, plugin directories populated

- [ ] **Step 1: Install Dataview plugin**
  Command: create `.obsidian/community-plugins.json` with dataview entry (ID: "dataview")
  Expected: valid JSON, plugin ID correct

- [ ] **Step 2: Install Waypoint plugin**
  Command: add waypoint entry (ID: "waypoint")
  Expected: valid JSON entry

- [ ] **Step 3: Install Tag Wrangler plugin**
  Command: add tag-wrangler entry (ID: "tag-wrangler")
  Expected: valid JSON entry

- [ ] **Step 4: Install Calendar plugin**
  Command: add calendar entry (ID: "calendar")
  Expected: valid JSON entry

- [ ] **Step 5: Verification**
  Criteria: community-plugins.json is valid JSON with all 4 plugin IDs; core-plugins.json unchanged

---

## Front 8: Strategic Aliases

**Artefacts:**
- Input: existing frontmatter in `curriculum/INDEX.md`, `docs/system-of-record.md`, `curriculum/QUICK_START.md`, `curriculum/MASTER_PLAN.md`, `curriculum/GLOSSARY.md`, `curriculum/FAQ.md`, `curriculum/README.md`
- Output: same files with updated `aliases:` field

- [ ] **Step 1: Read current frontmatter of all 7 target files**
  Command: read top 15 lines of each file
  Expected: capture current aliases values

- [ ] **Step 2: Add/update aliases in curriculum/INDEX.md**
  Command: edit frontmatter aliases to `["indice", "navegacao", "hub", "mapa do site"]`
  Expected: YAML list format, existing tags/type preserved

- [ ] **Step 3: Add/update aliases in docs/system-of-record.md**
  Command: edit frontmatter aliases to `["SOR", "system of record", "governanca", "precedencia", "taxonomia"]`
  Expected: YAML list format, existing fields preserved

- [ ] **Step 4: Add/update aliases in remaining index files**
  Command: edit QUICK_START, MASTER_PLAN, GLOSSARY, FAQ, README aliases per spec
  Expected: each file gets Portuguese aliases for fuzzy search

- [ ] **Step 5: Verification**
  Criteria: all 7 files have non-empty aliases; `scripts/check-obsidian-conventions.sh` passes; YAML list format `["a", "b"]` respected

---

## Front 9: Canvas Maps

**Artefacts:**
- Input: `docs/system-of-record.md` (domain/pattern relationships), `curriculum/INDEX.md` (navigation paths), existing wikilinks between docs
- Output: `.canvas` files in repo root

- [ ] **Step 1: Create document-architecture.canvas**
  Command: write canvas JSON with nodes for canonical patterns, analysis docs, and curriculum lessons — edges representing relates-to/wikilink connections
  Expected: valid JSON canvas format, nodes positioned for readability

- [ ] **Step 2: Create reading-flow.canvas**
  Command: write canvas JSON representing the navigation paths from curriculum/INDEX.md (by profile, by level, by content type)
  Expected: valid JSON canvas format, clear entry points and paths

- [ ] **Step 3: Verification**
  Criteria: both .canvas files are valid JSON; canvas nodes reference real file paths; visual layout is non-overlapping
