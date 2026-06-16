#!/usr/bin/env -S npx tsx
/**
 * validate-obsidian.ts — Obsidian convention validator for long-running-agents.
 * Replaces scripts/check-obsidian-conventions.sh with typed queries over
 * the @pavani/obsidian-eval library.
 *
 * Usage:
 *   npx tsx scripts/validate-obsidian.ts [--json]
 *
 * Exit: 0 if clean, 1 if violations found (warnings do not cause exit 1).
 */

import { scan, parseFrontmatter, extractWikilinkTargets } from "@pavani/obsidian-eval";
import { resolve } from "node:path";
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";

// ── Path setup ─────────────────────────────────────────────────────────────

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");

// ── Types ──────────────────────────────────────────────────────────────────

interface Violation {
  file: string;
  line: number;
  check: string;
  message: string;
}

// ── Helpers ────────────────────────────────────────────────────────────────

const isDirectCanonical = (p: string) => /^docs\/canonical\/[^/]+\.md$/.test(p);

function frontmatterExists(absPath: string): boolean {
  try {
    return parseFrontmatter(absPath) !== null;
  } catch {
    return false;
  }
}

function getFrontmatter(relPath: string): Record<string, unknown> {
  const note = vault.notes.get(relPath);
  if (note) return note.frontmatter;
  const absPath = resolve(REPO_ROOT, relPath);
  try {
    const parsed = parseFrontmatter(absPath);
    return parsed?.frontmatter ?? {};
  } catch {
    return {};
  }
}

function collectTags(relPath: string): string[] {
  const fm = getFrontmatter(relPath);
  const tags = fm.tags;
  if (Array.isArray(tags)) return tags.filter((t): t is string => typeof t === "string");
  return [];
}

// ── Scan vault once ────────────────────────────────────────────────────────

const vault = scan(REPO_ROOT);
const violations: Violation[] = [];
const warnings: Violation[] = [];

// ── Check labels (human-readable) ──────────────────────────────────────────

const checkLabels: Record<string, string> = {
  "1": "Check 1: Frontmatter in docs/canonical/",
  "2": "Check 2: Frontmatter in docs/analysis/",
  "3": "Check 3: Frontmatter in curriculum/ index files",
  "4": "Check 4: Frontmatter in root index.md",
  "5": "Check 5: Raw markdown links in docs/canonical/",
  "6": "Check 6: Broken wikilinks in docs/canonical/",
  "7": "Check 7: Cross-reference tag consistency in docs/canonical/",
  "8": "Check 8: Canvas file paths (no broken references)",
  "9": "Check 9: Frontmatter in ALL curriculum/ .md files",
  "10": "Check 10: Tag taxonomy (unrecognized tags)",
  "11": "Check 11: relates-to presence in monitored files",
  "12": "Check 12: aliases presence in monitored files",
};

// ═══════════════════════════════════════════════════════════════════════════
// Check 1: Frontmatter in docs/canonical/*.md (non-recursive, type: required)
// ═══════════════════════════════════════════════════════════════════════════

for (const [path] of vault.notes) {
  if (!isDirectCanonical(path)) continue;
  const absPath = resolve(REPO_ROOT, path);
  if (!frontmatterExists(absPath)) {
    violations.push({
      file: path, line: 1, check: "1",
      message: "missing YAML frontmatter (no '---' on line 1)",
    });
  } else if (!getFrontmatter(path).type) {
    violations.push({
      file: path, line: 1, check: "1",
      message: "has frontmatter delimiters but missing 'type:' field",
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 2: Frontmatter in docs/analysis/**/*.md (type: required)
// ═══════════════════════════════════════════════════════════════════════════

for (const [path] of vault.notes) {
  if (!path.startsWith("docs/analysis/")) continue;
  const absPath = resolve(REPO_ROOT, path);
  if (!frontmatterExists(absPath)) {
    violations.push({
      file: path, line: 1, check: "2",
      message: "missing YAML frontmatter",
    });
  } else if (!getFrontmatter(path).type) {
    violations.push({
      file: path, line: 1, check: "2",
      message: "missing 'type:' in frontmatter",
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 3: Frontmatter in curriculum/ index files (type: required)
// ═══════════════════════════════════════════════════════════════════════════

const CURRICULUM_INDEX_FILES = [
  "curriculum/INDEX.md",
  "curriculum/MASTER_PLAN.md",
  "curriculum/README.md",
  "curriculum/QUICK_START.md",
  "curriculum/EXECUTION_PLAN.md",
  "curriculum/GLOSSARY.md",
  "curriculum/FAQ.md",
];

for (const relPath of CURRICULUM_INDEX_FILES) {
  const absPath = resolve(REPO_ROOT, relPath);
  if (!vault.notes.has(relPath)) continue; // file doesn't exist, skip
  if (!frontmatterExists(absPath)) {
    violations.push({
      file: relPath, line: 1, check: "3",
      message: "missing YAML frontmatter",
    });
  } else if (!getFrontmatter(relPath).type) {
    violations.push({
      file: relPath, line: 1, check: "3",
      message: "missing 'type:' in frontmatter",
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 4: Frontmatter in root index.md (type: required)
// ═══════════════════════════════════════════════════════════════════════════

{
  const relPath = "index.md";
  if (vault.notes.has(relPath)) {
    const absPath = resolve(REPO_ROOT, relPath);
    if (!frontmatterExists(absPath)) {
      violations.push({
        file: relPath, line: 1, check: "4",
        message: "missing YAML frontmatter",
      });
    } else if (!getFrontmatter(relPath).type) {
      violations.push({
        file: relPath, line: 1, check: "4",
        message: "missing 'type:' in frontmatter",
      });
    }
  } else {
    warnings.push({
      file: "index.md", line: 0, check: "4",
      message: "index.md not found at repo root (not yet created?)",
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 5: Raw markdown links [text](path.md) in docs/canonical/*.md
// ═══════════════════════════════════════════════════════════════════════════

const RAW_LINK_RE = /\[([^\]]+)\]\(([^)]+\.md)\)/g;

for (const [path] of vault.notes) {
  if (!isDirectCanonical(path)) continue;
  const absPath = resolve(REPO_ROOT, path);
  const content = readFileSync(absPath, "utf-8");
  const lines = content.split("\n");

  let inCodeBlock = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i] ?? "";
    const trimmed = line.trim();

    if (trimmed.startsWith("```")) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) continue;
    if (trimmed.startsWith("`")) continue; // approximate: inline code marker at start

    // Reset regex lastIndex
    RAW_LINK_RE.lastIndex = 0;
    let match: RegExpExecArray | null;
    while ((match = RAW_LINK_RE.exec(line)) !== null) {
      const url = match[2] ?? "";
      if (url.includes("://")) continue; // external URL
      violations.push({
        file: path,
        line: i + 1,
        check: "5",
        message: `raw markdown link "${match[0]}" — should be [[wikilink]]`,
      });
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 6: Broken wikilinks in docs/canonical/*.md (non-recursive)
// ═══════════════════════════════════════════════════════════════════════════

{
  const broken = vault.graph.brokenLinks();
  for (const edge of broken) {
    if (!isDirectCanonical(edge.from)) continue;

    const rawTarget = extractWikilinkTargets(edge.raw)[0] ?? edge.to;
    if (rawTarget.includes("://")) continue;

    // Check filesystem like bash: try resolve(path), then resolve(path).md
    const absPath = resolve(REPO_ROOT, edge.to);
    if (existsSync(absPath)) continue;
    if (existsSync(absPath + ".md")) continue;

    // Also try with .md if vault notes path differs from edge.to
    if (vault.notes.has(edge.to)) continue;
    if (vault.notes.has(edge.to + ".md")) continue;

    violations.push({
      file: edge.from,
      line: edge.line,
      check: "6",
      message: `broken wikilink: [[${rawTarget}]] (target not found)`,
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 7: Cross-reference tag consistency in docs/canonical/*.md (warning)
// ═══════════════════════════════════════════════════════════════════════════

for (const [path] of vault.notes) {
  if (!isDirectCanonical(path)) continue;
  const fileTags = collectTags(path);
  if (fileTags.length === 0) continue;

  const outboundEdges = vault.graph.outbound(path);
  for (const edge of outboundEdges) {
    const linkedTags = collectTags(edge.to);
    if (linkedTags.length === 0) continue;

    const hasCommonTag = fileTags.some((t) => linkedTags.includes(t));
    if (!hasCommonTag) {
      warnings.push({
        file: path,
        line: edge.line,
        check: "7",
        message: `no tags in common with [[${edge.to}]]`,
      });
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 8: Canvas file paths — check every file-type node exists on disk
// ═══════════════════════════════════════════════════════════════════════════

function walkCanvasFiles(dir: string): string[] {
  const results: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const fullPath = resolve(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walkCanvasFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith(".canvas")) {
      results.push(fullPath);
    }
  }
  return results;
}

const canvasFiles = walkCanvasFiles(REPO_ROOT);

for (const canvasPath of canvasFiles) {
  const canvasName = canvasPath.slice(REPO_ROOT.length + 1);
  let data: { nodes?: { type?: string; file?: string }[] };
  try {
    data = JSON.parse(readFileSync(canvasPath, "utf-8")) as typeof data;
  } catch {
    violations.push({
      file: canvasName, line: 1, check: "8",
      message: "invalid JSON in canvas file",
    });
    continue;
  }

  const nodes = Array.isArray(data.nodes) ? data.nodes : [];
  for (const node of nodes) {
    if (!node || typeof node !== "object") continue;
    if (node.type !== "file" || !node.file) continue;
    const resolvedPath = resolve(REPO_ROOT, node.file);
    if (!existsSync(resolvedPath)) {
      violations.push({
        file: canvasName, line: 1, check: "8",
        message: `broken path: ${node.file}`,
      });
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 9: Frontmatter in ALL curriculum/ .md files (type: + tags: required)
// ═══════════════════════════════════════════════════════════════════════════

for (const [path] of vault.notes) {
  if (!path.startsWith("curriculum/")) continue;
  const absPath = resolve(REPO_ROOT, path);
  if (!frontmatterExists(absPath)) {
    violations.push({
      file: path, line: 1, check: "9",
      message: "missing YAML frontmatter",
    });
    continue;
  }
  const fm = getFrontmatter(path);
  if (!fm.type) {
    violations.push({
      file: path, line: 1, check: "9",
      message: "missing 'type:' in frontmatter",
    });
  }
  if (!fm.tags) {
    violations.push({
      file: path, line: 1, check: "9",
      message: "missing 'tags:' in frontmatter",
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 10: Tag taxonomy — unrecognized tags (warning)
// ═══════════════════════════════════════════════════════════════════════════

{
  const DOMAIN_TAGS = new Set([
    "agentes-orquestracao",
    "curriculo-conteudo",
    "stack-tooling",
    "governanca",
    "portal-web",
  ]);
  const STRUCTURAL_TAGS = new Set(["index", "reference"]);

  // Collect tags from system-of-record.md
  const sorTags = new Set(collectTags("docs/system-of-record.md"));

  // Collect tags from all docs/canonical/
  const canonicalTags = new Set<string>();
  for (const [path] of vault.notes) {
    if (!path.startsWith("docs/canonical/")) continue;
    for (const t of collectTags(path)) canonicalTags.add(t);
  }

  // Collect tags from all docs/analysis/
  const analysisTags = new Set<string>();
  for (const [path] of vault.notes) {
    if (!path.startsWith("docs/analysis/")) continue;
    for (const t of collectTags(path)) analysisTags.add(t);
  }

  const allowed = new Set([
    ...DOMAIN_TAGS,
    ...STRUCTURAL_TAGS,
    ...sorTags,
    ...canonicalTags,
    ...analysisTags,
  ]);

  // Check docs/analysis/ and curriculum/ tags against allowed set
  const checkDirs = ["docs/analysis/", "curriculum/"];
  for (const [path] of vault.notes) {
    if (!checkDirs.some((d) => path.startsWith(d))) continue;
    for (const tag of collectTags(path)) {
      if (!allowed.has(tag)) {
        warnings.push({
          file: path,
          line: 1,
          check: "10",
          message: `unrecognized tag: ${JSON.stringify(tag)}`,
        });
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 11: relates-to presence in docs/canonical/, docs/analysis/, curriculum/
// ═══════════════════════════════════════════════════════════════════════════

const MONITORED_DIRS_C11 = ["docs/canonical/", "docs/analysis/", "curriculum/"];

for (const [path] of vault.notes) {
  if (!MONITORED_DIRS_C11.some((d) => path.startsWith(d))) continue;
  const fm = getFrontmatter(path);
  if (!("relates-to" in fm)) {
    violations.push({
      file: path,
      line: 1,
      check: "11",
      message: "missing 'relates-to:' in frontmatter",
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Check 12: aliases presence and non-empty in monitored directories
// ═══════════════════════════════════════════════════════════════════════════

for (const [path] of vault.notes) {
  if (!MONITORED_DIRS_C11.some((d) => path.startsWith(d))) continue;
  const fm = getFrontmatter(path);
  const aliases = fm.aliases;
  if (!("aliases" in fm)) {
    violations.push({
      file: path,
      line: 1,
      check: "12",
      message: "missing 'aliases:' in frontmatter",
    });
  } else if (Array.isArray(aliases) && aliases.length === 0) {
    violations.push({
      file: path,
      line: 1,
      check: "12",
      message: "'aliases:' is empty (must have at least one value)",
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Output
// ═══════════════════════════════════════════════════════════════════════════

const jsonMode = process.argv.includes("--json");

if (jsonMode) {
  // Merge violations and warnings into one output with severity
  const results = [
    ...violations.map((v) => ({ ...v, severity: "error" })),
    ...warnings.map((w) => ({ ...w, severity: "warning" })),
  ];
  console.log(JSON.stringify(results, null, 2));
} else {
  // Human-readable, grouped by check
  const ordered = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  for (const checkNum of ordered) {
    const checkStr = String(checkNum);
    // Violations for this check
    const errs = violations.filter((v) => v.check === checkStr);
    const wrns = warnings.filter((v) => v.check === checkStr);

    const label = checkLabels[checkStr] ?? `Check ${checkStr}`;
    const total = errs.length + wrns.length;
    if (total === 0) {
      console.log(`[OK] ${label}`);
      continue;
    }

    console.log(`--- ${label} ---`);
    for (const v of errs) {
      console.log(`[ERR] ${v.file}:${v.line} — ${v.message}`);
    }
    for (const w of wrns) {
      console.log(`[WARN] ${w.file}:${w.line} — ${w.message}`);
    }
    console.log("");
  }

  // Summary
  console.log("=== Summary ===");
  const errCount = violations.length;
  const warnCount = warnings.length;
  if (errCount === 0 && warnCount === 0) {
    console.log("All checks passed. Obsidian conventions are clean.");
  } else {
    if (errCount > 0) {
      console.log(`${errCount} violation(s) found.`);
    }
    if (warnCount > 0) {
      console.log(`${warnCount} warning(s) found.`);
    }
  }
}

process.exitCode = violations.length > 0 ? 1 : 0;
