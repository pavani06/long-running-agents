#!/usr/bin/env -S npx tsx
/**
 * validate-obsidian.ts — Obsidian convention validator for long-running-agents.
 * Replaces scripts/check-obsidian-conventions.sh with typed queries over
 * the @pavani/obsidian-eval library.
 *
 * Usage:
 *   npx tsx scripts/validate-obsidian.ts [--checks <list>] [--paths <list>] [--json] [--no-cache]
 *
 * Flags:
 *   --checks <a,b,c>  Run only the named checks. Accepts check numbers (1-12),
 *                     stable slugs, and groups:
 *                       err  = all checks that emit errors (1,2,3,4,5,6,8,9,11,12)
 *                       warn = warning-only checks (7,10)
 *                       all  = every check (default)
 *                     Slugs:
 *                       1  canonical-frontmatter       7  tag-consistency
 *                       2  analysis-frontmatter        8  canvas-paths
 *                       3  curriculum-index-frontmatter 9  curriculum-frontmatter
 *                       4  root-index-frontmatter      10 tag-taxonomy
 *                       5  raw-links                   11 relates-to
 *                       6  broken-wikilinks            12 aliases
 *   --paths <globs>   Restrict scanned paths (comma-separated). Each entry is a
 *                     directory prefix ("curriculum/"), an exact path, or a glob
 *                     ("docs/canonical/*.md", "curriculum/**"). Checks only run
 *                     over files matching the filter.
 *   --json            Structured output (single run): summary + per-check counts
 *                     + items. Stdout is a single valid JSON document; cache and
 *                     timing info live inside the JSON, never as loose lines.
 *   --no-cache        Force full re-validation, ignoring .validator-cache/.
 *
 * Cache:
 *   Notes unchanged since the last run (same content hash) are not
 *   re-validated; their stored results are replayed. State lives in
 *   .validator-cache/ (gitignored). Checks that depend on more than the
 *   note's own content carry fingerprints that must also match:
 *     - 4/6/8 (index.md absence, wikilink and canvas target existence):
 *       fingerprint of the vault file list;
 *     - 10 (tag taxonomy): fingerprint of the tag inputs (system-of-record,
 *       docs/canonical/, docs/analysis/ contents);
 *     - 7 (tag consistency): per-note list of outbound link targets with
 *       their content hashes (the target set itself is pinned by the note's
 *       own content hash).
 *
 * Exit: 0 if clean, 1 if violations found (warnings do not cause exit 1),
 *       2 on CLI usage error.
 */

import { scan, parseFrontmatter, extractWikilinkTargets, walkMdFiles } from "@pavani/obsidian-eval";
import type { Vault } from "@pavani/obsidian-eval";
import { resolve, dirname, relative } from "node:path";
import { readFileSync, existsSync, readdirSync, writeFileSync, renameSync, mkdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

// ── Path setup ─────────────────────────────────────────────────────────────

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");

const CACHE_DIR = resolve(REPO_ROOT, ".validator-cache");
const CACHE_FILE = resolve(CACHE_DIR, "state.json");
const CACHE_VERSION = 1;

// ── Types ──────────────────────────────────────────────────────────────────

interface Violation {
  file: string;
  line: number;
  check: string;
  message: string;
}

interface CheckOutcome {
  violations: Violation[];
  warnings: Violation[];
}

type CachedItem = Violation & { severity: "error" | "warning" };

interface CacheEntry {
  hash: string;
  ctx: string;
  ctxTags?: string;
  deps?: Array<[string, string]>;
  results: Record<string, CachedItem[]>;
}

interface CacheState {
  version: number;
  scriptHash: string;
  entries: Record<string, CacheEntry>;
}

// ── CLI parsing ────────────────────────────────────────────────────────────

const CHECK_LABELS: Record<string, string> = {
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

const CHECK_NAMES: Record<string, string> = {
  "1": "canonical-frontmatter",
  "2": "analysis-frontmatter",
  "3": "curriculum-index-frontmatter",
  "4": "root-index-frontmatter",
  "5": "raw-links",
  "6": "broken-wikilinks",
  "7": "tag-consistency",
  "8": "canvas-paths",
  "9": "curriculum-frontmatter",
  "10": "tag-taxonomy",
  "11": "relates-to",
  "12": "aliases",
};

const CHECK_IDS = Object.keys(CHECK_NAMES);
const WARNING_ONLY_CHECKS = ["7", "10"];
const CHECK_GROUPS: Record<string, string[]> = {
  err: CHECK_IDS.filter((id) => !WARNING_ONLY_CHECKS.includes(id)),
  warn: WARNING_ONLY_CHECKS,
  all: CHECK_IDS,
};

// Checks whose results depend on which files exist in the vault (link/canvas
// target existence, index.md absence): cache entries must also match the
// file-list fingerprint.
const FILE_LIST_CHECKS = new Set(["4", "6", "8"]);

const CHECK_ALIASES: Record<string, string> = {};
for (const id of CHECK_IDS) CHECK_ALIASES[id] = id;
for (const [id, slug] of Object.entries(CHECK_NAMES)) CHECK_ALIASES[slug] = id;

function usage(message: string): never {
  console.error(`Error: ${message}`);
  console.error("");
  console.error("Usage: npx tsx scripts/validate-obsidian.ts [--checks <list>] [--paths <globs>] [--json] [--no-cache]");
  console.error("");
  console.error(`Valid --checks values: numbers (1-12), slugs (${Object.values(CHECK_NAMES).join(", ")}), groups (err, warn, all).`);
  process.exit(2);
  throw new Error("unreachable: process.exit above terminates the process");
}

interface CliOptions {
  checks: string[];
  paths: string[];
  json: boolean;
  noCache: boolean;
}

function parseArgs(argv: string[]): CliOptions {
  const opts: CliOptions = { checks: [], paths: [], json: false, noCache: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--json") {
      opts.json = true;
    } else if (arg === "--no-cache") {
      opts.noCache = true;
    } else if (arg === "--checks" || arg === "--paths") {
      const value = argv[++i];
      if (value === undefined) usage(`missing value for ${arg}`);
      const list = value.split(",").map((s) => s.trim()).filter((s) => s.length > 0);
      if (list.length === 0) usage(`empty value for ${arg}`);
      if (arg === "--checks") opts.checks.push(...list);
      else opts.paths.push(...list);
    } else {
      usage(`unknown flag: ${arg}`);
    }
  }
  return opts;
}

function resolveChecks(names: string[]): string[] {
  const selected = new Set<string>();
  for (const name of names) {
    const group = CHECK_GROUPS[name];
    if (group) {
      for (const id of group) selected.add(id);
      continue;
    }
    const id = CHECK_ALIASES[name];
    if (id) {
      selected.add(id);
      continue;
    }
    usage(`unknown check "${name}"`);
  }
  return CHECK_IDS.filter((id) => selected.has(id)); // stable numeric order
}

const opts = parseArgs(process.argv.slice(2));
const selectedChecks = opts.checks.length > 0 ? resolveChecks(opts.checks) : CHECK_IDS;

// ── Scope (--paths) ────────────────────────────────────────────────────────

function globToRegExp(glob: string): RegExp {
  let source = "^";
  for (let i = 0; i < glob.length; i++) {
    const char = glob[i];
    if (char === "*") {
      if (glob[i + 1] === "*") {
        while (glob[i + 1] === "*") i++;
        if (glob[i + 1] === "/") {
          source += "(?:[^/]+/)*";
          i++;
        } else {
          source += ".*";
        }
      } else {
        source += "[^/]*";
      }
    } else if (char === "?") {
      source += "[^/]";
    } else {
      source += char.replace(/[.+^${}()|[\]\\]/g, "\\$&");
    }
  }
  return new RegExp(source + "$");
}

function compileScope(patterns: string[]): (relPath: string) => boolean {
  const matchers = patterns.map((pattern) => {
    if (pattern.endsWith("/")) {
      return (rel: string) => rel.startsWith(pattern);
    }
    if (!/[*?]/.test(pattern)) {
      return (rel: string) => rel === pattern || rel.startsWith(pattern + "/");
    }
    const regExp = globToRegExp(pattern);
    return (rel: string) => regExp.test(rel);
  });
  return (relPath) => matchers.some((match) => match(relPath));
}

const scopeMatches = opts.paths.length > 0 ? compileScope(opts.paths) : () => true;

// ── Helpers ────────────────────────────────────────────────────────────────

const isDirectCanonical = (p: string) => /^docs\/canonical\/[^/]+\.md$/.test(p);

const CURRICULUM_INDEX_FILES = [
  "curriculum/INDEX.md",
  "curriculum/MASTER_PLAN.md",
  "curriculum/README.md",
  "curriculum/QUICK_START.md",
  "curriculum/EXECUTION_PLAN.md",
  "curriculum/GLOSSARY.md",
  "curriculum/FAQ.md",
];

const MONITORED_DIRS = ["docs/canonical/", "docs/analysis/", "curriculum/"];

function frontmatterExists(absPath: string): boolean {
  try {
    return parseFrontmatter(absPath) !== null;
  } catch {
    return false;
  }
}

function getFrontmatter(relPath: string): Record<string, unknown> {
  const note = vault?.notes.get(relPath);
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

// ── File discovery ─────────────────────────────────────────────────────────

function toRel(absPath: string): string {
  return relative(REPO_ROOT, absPath);
}

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

const startedAtMs = Date.now();
const allMdPaths = walkMdFiles(REPO_ROOT).map(toRel).sort();
const allCanvasPaths = walkCanvasFiles(REPO_ROOT).map(toRel).sort();
const scopedMdPaths = allMdPaths.filter(scopeMatches);
const scopedCanvasPaths = allCanvasPaths.filter(scopeMatches);

// The wikilink graph is only needed for checks 6/7, and only when the scope
// can contain docs/canonical/ sources (both checks read canonical files only).
// Outside that, runs avoid the full vault scan entirely.
const needsGraph =
  (selectedChecks.includes("6") || selectedChecks.includes("7")) &&
  scopedMdPaths.some(isDirectCanonical);
const vault: Vault | undefined = needsGraph ? scan(REPO_ROOT) : undefined;

function noteExists(relPath: string): boolean {
  return vault ? vault.notes.has(relPath) : existsSync(resolve(REPO_ROOT, relPath));
}

/** Files a check iterates over in this run (scope + applicability filtered). */
function checkFiles(checkId: string): string[] {
  if (checkId === "4") return scopeMatches("index.md") ? ["index.md"] : [];
  if (checkId === "8") return scopedCanvasPaths;
  return scopedMdPaths.filter((p) => checkAppliesTo(checkId, p));
}

function checkAppliesTo(checkId: string, relPath: string): boolean {
  switch (checkId) {
    case "1":
    case "5":
    case "6":
    case "7":
      return isDirectCanonical(relPath);
    case "2":
      return relPath.startsWith("docs/analysis/");
    case "3":
      return CURRICULUM_INDEX_FILES.includes(relPath);
    case "4":
      return relPath === "index.md";
    case "8":
      return relPath.endsWith(".canvas");
    case "9":
      return relPath.startsWith("curriculum/");
    case "10":
      return relPath.startsWith("docs/analysis/") || relPath.startsWith("curriculum/");
    case "11":
    case "12":
      return MONITORED_DIRS.some((d) => relPath.startsWith(d));
    default:
      return false;
  }
}

// ── Cache ──────────────────────────────────────────────────────────────────

function sha256OfScript(): string {
  return createHash("sha256").update(readFileSync(fileURLToPath(import.meta.url))).digest("hex");
}

function loadCache(): CacheState | null {
  if (opts.noCache) return null;
  try {
    const raw: unknown = JSON.parse(readFileSync(CACHE_FILE, "utf-8"));
    if (typeof raw !== "object" || raw === null) return null;
    const state = raw as CacheState;
    if (state.version !== CACHE_VERSION || state.scriptHash !== sha256OfScript()) return null;
    if (typeof state.entries !== "object" || state.entries === null) return null;
    return state;
  } catch {
    return null; // missing or corrupt cache behaves like a miss
  }
}

const cache = loadCache();
const fileListFingerprint = createHash("sha256")
  .update(JSON.stringify([...allMdPaths, ...allCanvasPaths]))
  .digest("hex");

let tagsFingerprintMemo: string | null = null;

/** Fingerprint of the tag-taxonomy inputs (system-of-record + canonical + analysis). */
function tagsFingerprint(): string {
  const memoized = tagsFingerprintMemo;
  if (memoized !== null) return memoized;
  const inputs = [
    "docs/system-of-record.md",
    ...allMdPaths.filter((p) => p.startsWith("docs/canonical/") || p.startsWith("docs/analysis/")),
  ].filter((p) => allMdPaths.includes(p));
  const parts = inputs.map((p) => `${p}:${fileStateHash(p)}`).sort();
  const digest = createHash("sha256").update(parts.join("\n")).digest("hex");
  tagsFingerprintMemo = digest;
  return digest;
}

const hashMemo = new Map<string, string>();

function contentHash(relPath: string): string {
  const memoized = hashMemo.get(relPath);
  if (memoized) return memoized;
  const digest = createHash("sha256")
    .update(readFileSync(resolve(REPO_ROOT, relPath)))
    .digest("hex");
  hashMemo.set(relPath, digest);
  return digest;
}

/** Content hash for existing files; "" (never a real digest) marks absence. */
function fileStateHash(relPath: string): string {
  return allMdPaths.includes(relPath) || allCanvasPaths.includes(relPath)
    ? contentHash(relPath)
    : "";
}

/**
 * Context requirement of a check beyond the note's own content hash. For
 * check 7, the stored deps are sound because an unchanged note content
 * implies the same outbound target set; only target contents can drift.
 */
function replayContextMatches(checkId: string, entry: CacheEntry): boolean {
  if (FILE_LIST_CHECKS.has(checkId)) return entry.ctx === fileListFingerprint;
  if (checkId === "10") return entry.ctxTags === tagsFingerprint();
  if (checkId === "7") {
    const deps = entry.deps;
    if (!deps) return false;
    return deps.every(([target, hash]) => fileStateHash(target) === hash);
  }
  return true;
}

/**
 * Attempt to satisfy every selected (check, file) pair from cached entries.
 * Returns per-check items on full hit, or null on any miss (the run then
 * recomputes the whole scope, which also refreshes the cache).
 */
function tryReplay(): Record<string, CachedItem[]> | null {
  if (!cache) return null;

  const perCheck: Record<string, CachedItem[]> = {};
  for (const checkId of selectedChecks) {
    const items: CachedItem[] = [];
    for (const file of checkFiles(checkId)) {
      const entry = cache.entries[file];
      if (!entry || entry.hash !== fileStateHash(file)) return null;
      if (!replayContextMatches(checkId, entry)) return null;
      const cached = entry.results[checkId];
      if (!Array.isArray(cached)) return null;
      items.push(...cached);
    }
    perCheck[checkId] = items;
  }
  return perCheck;
}

function storeResults(outcomes: Record<string, CheckOutcome>): Record<string, CacheEntry> {
  const entries: Record<string, CacheEntry> = { ...(cache?.entries ?? {}) };
  for (const checkId of selectedChecks) {
    for (const file of checkFiles(checkId)) {
      const currentHash = fileStateHash(file);
      let entry = entries[file];
      // A changed file invalidates every cached result for it; an unchanged
      // file keeps results from other check selections (cross-selection reuse).
      if (!entry || entry.hash !== currentHash) {
        entry = { hash: currentHash, ctx: fileListFingerprint, results: {} };
        entries[file] = entry;
      }
      if (FILE_LIST_CHECKS.has(checkId)) entry.ctx = fileListFingerprint;
      if (checkId === "10") entry.ctxTags = tagsFingerprint();
      if (checkId === "7") entry.deps = check7Deps.get(file) ?? [];
      entry.results[checkId] = [];
    }
    const outcome = outcomes[checkId];
    const stored: CachedItem[] = [
      ...outcome.violations.map((v) => ({ ...v, severity: "error" as const })),
      ...outcome.warnings.map((w) => ({ ...w, severity: "warning" as const })),
    ];
    for (const item of stored) {
      entries[item.file]?.results[checkId]?.push(item);
    }
  }
  // Prune entries for files that no longer exist. Entries with an empty hash
  // track the absence of a file (e.g. root index.md) and are valid states.
  const known = new Set([...allMdPaths, ...allCanvasPaths]);
  for (const key of Object.keys(entries)) {
    if (!known.has(key) && entries[key].hash !== "") delete entries[key];
  }
  return entries;
}

function saveCache(entries: Record<string, CacheEntry>): void {
  mkdirSync(CACHE_DIR, { recursive: true });
  const state: CacheState = { version: CACHE_VERSION, scriptHash: sha256OfScript(), entries };
  const tmpFile = CACHE_FILE + ".tmp";
  writeFileSync(tmpFile, JSON.stringify(state));
  renameSync(tmpFile, CACHE_FILE);
}

// ── Check implementations ──────────────────────────────────────────────────

// Check 1: Frontmatter in docs/canonical/*.md (non-recursive, type: required)
function runCheck1(): CheckOutcome {
  const violations: Violation[] = [];
  for (const path of checkFiles("1")) {
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
  return { violations, warnings: [] };
}

// Check 2: Frontmatter in docs/analysis/**/*.md (type: required)
function runCheck2(): CheckOutcome {
  const violations: Violation[] = [];
  for (const path of checkFiles("2")) {
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
  return { violations, warnings: [] };
}

// Check 3: Frontmatter in curriculum/ index files (type: required)
function runCheck3(): CheckOutcome {
  const violations: Violation[] = [];
  for (const relPath of CURRICULUM_INDEX_FILES) {
    if (!scopeMatches(relPath)) continue;
    const absPath = resolve(REPO_ROOT, relPath);
    if (!noteExists(relPath)) continue; // file doesn't exist, skip
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
  return { violations, warnings: [] };
}

// Check 4: Frontmatter in root index.md (type: required)
function runCheck4(): CheckOutcome {
  const violations: Violation[] = [];
  const warnings: Violation[] = [];
  const relPath = "index.md";
  if (!scopeMatches(relPath)) return { violations, warnings };
  if (noteExists(relPath)) {
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
  return { violations, warnings };
}

// Check 5: Raw markdown links [text](path.md) in docs/canonical/*.md
const RAW_LINK_RE = /\[([^\]]+)\]\(([^)]+\.md)\)/g;

function runCheck5(): CheckOutcome {
  const violations: Violation[] = [];
  for (const path of checkFiles("5")) {
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
  return { violations, warnings: [] };
}

// Check 6: Broken wikilinks in docs/canonical/*.md (non-recursive)
function runCheck6(): CheckOutcome {
  const violations: Violation[] = [];
  if (!vault) return { violations, warnings: [] };
  const broken = vault.graph.brokenLinks();
  for (const edge of broken) {
    if (!isDirectCanonical(edge.from)) continue;
    if (!scopeMatches(edge.from)) continue;

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
  return { violations, warnings: [] };
}

// Check 7: Cross-reference tag consistency in docs/canonical/*.md (warning)
const check7Deps = new Map<string, Array<[string, string]>>();

function runCheck7(): CheckOutcome {
  const warnings: Violation[] = [];
  if (!vault) return { violations: [], warnings };
  for (const path of checkFiles("7")) {
    const outboundEdges = vault.graph.outbound(path);
    check7Deps.set(path, outboundEdges.map((edge) => [edge.to, fileStateHash(edge.to)] as [string, string]));

    const fileTags = collectTags(path);
    if (fileTags.length === 0) continue;

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
  return { violations: [], warnings };
}

// Check 8: Canvas file paths — check every file-type node exists on disk
function runCheck8(): CheckOutcome {
  const violations: Violation[] = [];
  for (const canvasPath of scopedCanvasPaths) {
    const absCanvasPath = resolve(REPO_ROOT, canvasPath);
    let data: { nodes?: { type?: string; file?: string }[] };
    try {
      data = JSON.parse(readFileSync(absCanvasPath, "utf-8")) as typeof data;
    } catch {
      violations.push({
        file: canvasPath, line: 1, check: "8",
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
          file: canvasPath, line: 1, check: "8",
          message: `broken path: ${node.file}`,
        });
      }
    }
  }
  return { violations, warnings: [] };
}

// Check 9: Frontmatter in ALL curriculum/ .md files (type: + tags: required)
function runCheck9(): CheckOutcome {
  const violations: Violation[] = [];
  for (const path of checkFiles("9")) {
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
  return { violations, warnings: [] };
}

// Check 10: Tag taxonomy — unrecognized tags (warning)
function runCheck10(): CheckOutcome {
  const warnings: Violation[] = [];
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

  // Collect tags from all docs/canonical/ and docs/analysis/ (global inputs,
  // not scope-filtered: the allowed set is defined by the whole vault)
  const canonicalTags = new Set<string>();
  for (const path of allMdPaths) {
    if (!path.startsWith("docs/canonical/")) continue;
    for (const t of collectTags(path)) canonicalTags.add(t);
  }

  const analysisTags = new Set<string>();
  for (const path of allMdPaths) {
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
  for (const path of checkFiles("10")) {
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
  return { violations: [], warnings };
}

// Check 11: relates-to presence in docs/canonical/, docs/analysis/, curriculum/
function runCheck11(): CheckOutcome {
  const violations: Violation[] = [];
  for (const path of checkFiles("11")) {
    const fm = getFrontmatter(path);
    if (!("relates-to" in fm)) {
      violations.push({
        file: path, line: 1, check: "11",
        message: "missing 'relates-to:' in frontmatter",
      });
    }
  }
  return { violations, warnings: [] };
}

// Check 12: aliases presence and non-empty in monitored directories
function runCheck12(): CheckOutcome {
  const violations: Violation[] = [];
  for (const path of checkFiles("12")) {
    const fm = getFrontmatter(path);
    const aliases = fm.aliases;
    if (!("aliases" in fm)) {
      violations.push({
        file: path, line: 1, check: "12",
        message: "missing 'aliases:' in frontmatter",
      });
    } else if (Array.isArray(aliases) && aliases.length === 0) {
      violations.push({
        file: path, line: 1, check: "12",
        message: "'aliases:' is empty (must have at least one value)",
      });
    }
  }
  return { violations, warnings: [] };
}

const CHECK_RUNNERS: Record<string, () => CheckOutcome> = {
  "1": runCheck1,
  "2": runCheck2,
  "3": runCheck3,
  "4": runCheck4,
  "5": runCheck5,
  "6": runCheck6,
  "7": runCheck7,
  "8": runCheck8,
  "9": runCheck9,
  "10": runCheck10,
  "11": runCheck11,
  "12": runCheck12,
};

// ── Run: replay from cache or compute ──────────────────────────────────────

const replayed = tryReplay();
let outcomes: Record<string, CheckOutcome>;
let cacheHit = false;

if (replayed) {
  outcomes = {};
  for (const checkId of selectedChecks) {
    const items = replayed[checkId] ?? [];
    outcomes[checkId] = {
      violations: items.filter((item) => item.severity === "error"),
      warnings: items.filter((item) => item.severity === "warning"),
    };
  }
  cacheHit = true;
} else {
  outcomes = {};
  for (const checkId of selectedChecks) {
    outcomes[checkId] = CHECK_RUNNERS[checkId]();
  }
  if (!opts.noCache) {
    saveCache(storeResults(outcomes));
  }
}

const violations: Violation[] = selectedChecks.flatMap((id) => outcomes[id].violations);
const warnings: Violation[] = selectedChecks.flatMap((id) => outcomes[id].warnings);

const touchedFiles = new Set<string>();
for (const checkId of selectedChecks) {
  for (const file of checkFiles(checkId)) touchedFiles.add(file);
}

// ── Output ─────────────────────────────────────────────────────────────────

const durationMs = Date.now() - startedAtMs;

if (opts.json) {
  const items = [
    ...violations.map((v) => ({ ...v, severity: "error", checkName: CHECK_NAMES[v.check] })),
    ...warnings.map((w) => ({ ...w, severity: "warning", checkName: CHECK_NAMES[w.check] })),
  ];
  const report = {
    summary: {
      errors: violations.length,
      warnings: warnings.length,
      exitCode: violations.length > 0 ? 1 : 0,
      durationMs,
      checksRun: selectedChecks.map((id) => CHECK_NAMES[id]),
    },
    cache: {
      enabled: !opts.noCache,
      hit: cacheHit,
      notesValidated: touchedFiles.size,
    },
    checks: selectedChecks.map((id) => ({
      id,
      name: CHECK_NAMES[id],
      errors: outcomes[id].violations.length,
      warnings: outcomes[id].warnings.length,
    })),
    items,
  };
  console.log(JSON.stringify(report, null, 2));
} else {
  // Human-readable, grouped by check
  for (const checkId of selectedChecks) {
    const errs = outcomes[checkId].violations;
    const wrns = outcomes[checkId].warnings;

    const label = CHECK_LABELS[checkId] ?? `Check ${checkId}`;
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

  if (!opts.noCache) {
    if (cacheHit) {
      console.log(`[cache] hit — ${touchedFiles.size}/${touchedFiles.size} note(s) unchanged, results replayed from .validator-cache/`);
    } else {
      console.log(`[cache] miss — ${touchedFiles.size} note(s) validated`);
    }
  }
}

process.exitCode = violations.length > 0 ? 1 : 0;
