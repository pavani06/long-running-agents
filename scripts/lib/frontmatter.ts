/**
 * scripts/lib/frontmatter.ts — Safe frontmatter YAML transformation library.
 *
 * Single entry point for transforming YAML frontmatter in Obsidian-style
 * markdown files. Built after two write-first incidents (issue #205, epic
 * #197): a tag applier that flattened valid tags across 115 files and a
 * flow-style-only regex parser that crashed on block-style mid-apply.
 *
 * Safety contract:
 *   - Parses flow-style AND block-style YAML, multi-line block scalars,
 *     comments, anchors. Untouched nodes keep their source style.
 *   - Dry-run by default: `runTransform` writes nothing unless `apply: true`.
 *   - Delta manifest (per-file before/after of touched fields) is emitted
 *     BEFORE any file write.
 *   - Atomic writes: temp file in the same directory + rename. A crash
 *     mid-apply never leaves a truncated or corrupted target file.
 *   - Zero fallback: a missing field is a named error (MISSING_FIELD),
 *     never silent inference.
 *   - Optional invariant: the resulting value of a field must belong to an
 *     allowed set, otherwise ASSERTION_FAILED and nothing is written.
 *
 * Phase order inside `runTransform` (fail-fast, all-or-nothing per batch):
 *   1. read + transform + assert every file (any error aborts with zero writes)
 *   2. emit manifest (stdout, or a file via `manifestPath`)
 *   3. only then write changed files, atomically
 */

import { parseDocument, isScalar, isSeq, isMap, type Document } from "yaml";
import { readFileSync, writeFileSync, renameSync, rmSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { randomUUID } from "node:crypto";

// ── Named errors ───────────────────────────────────────────────────────────

export type FrontmatterErrorCode =
  | "INVALID_SPEC"
  | "FRONTMATTER_READ_ERROR"
  | "FRONTMATTER_NOT_FOUND"
  | "FRONTMATTER_PARSE_ERROR"
  | "MISSING_FIELD"
  | "FIELD_NOT_A_LIST"
  | "ASSERTION_FAILED"
  | "WRITE_ERROR";

export class FrontmatterError extends Error {
  readonly code: FrontmatterErrorCode;
  readonly file?: string;
  readonly field?: string;

  constructor(
    code: FrontmatterErrorCode,
    message: string,
    details: { file?: string; field?: string; cause?: unknown } = {},
  ) {
    super(message, { cause: details.cause });
    this.name = "FrontmatterError";
    this.code = code;
    this.file = details.file;
    this.field = details.field;
  }
}

// ── Types ──────────────────────────────────────────────────────────────────

export type FieldOp =
  | { op: "set"; field: string; value: string }
  | { op: "append"; field: string; value: string }
  | { op: "remove"; field: string };

export interface FieldAssertion {
  field: string;
  /** Allowed values for the resulting field value (string-compared). */
  allowed: string[];
}

export interface FieldDelta {
  field: string;
  op: "set" | "append" | "remove";
  before: unknown;
  after: unknown;
}

export interface FileManifest {
  file: string;
  changed: boolean;
  changes: FieldDelta[];
}

export interface Manifest {
  mode: "dry-run" | "apply";
  files: FileManifest[];
  totals: { files: number; changed: number };
}

export interface TransformOptions {
  /** Transformations applied, in order, to every file. */
  ops: FieldOp[];
  /** Invariants checked against the RESULTING values, after all ops. */
  asserts?: FieldAssertion[];
  /** Dry-run unless explicitly true. */
  apply?: boolean;
  /** Write the manifest to this file instead of stdout. */
  manifestPath?: string;
}

export interface TransformResult {
  manifest: Manifest;
  /** Number of files actually written (always 0 in dry-run). */
  written: number;
}

// ── Frontmatter splitting ──────────────────────────────────────────────────

const OPEN_DELIMITER = /^---\r?\n/;
const CLOSE_DELIMITER = /^---[ \t]*\r?(\n|$)/;

interface SplitResult {
  yamlText: string;
  closeLine: string;
  body: string;
}

/**
 * Split a raw file into frontmatter YAML text, the exact bytes of the
 * closing delimiter line, and the verbatim body. Throws FRONTMATTER_NOT_FOUND
 * when the file has no (or unclosed) frontmatter block.
 */
export function splitFrontmatter(raw: string, file: string): SplitResult {
  if (!OPEN_DELIMITER.test(raw)) {
    throw new FrontmatterError("FRONTMATTER_NOT_FOUND", `no frontmatter block at start of file`, { file });
  }
  const lines = raw.slice(raw.indexOf("\n") + 1).split(/(?<=\n)/);
  const closeIdx = lines.findIndex((line) => CLOSE_DELIMITER.test(line));
  if (closeIdx === -1) {
    throw new FrontmatterError("FRONTMATTER_NOT_FOUND", `frontmatter block is never closed`, { file });
  }
  return {
    yamlText: lines.slice(0, closeIdx).join(""),
    closeLine: lines[closeIdx],
    body: lines.slice(closeIdx + 1).join(""),
  };
}

// ── FrontmatterFile ────────────────────────────────────────────────────────

export class FrontmatterFile {
  readonly path: string;
  private readonly doc: Document;
  private readonly closeLine: string;
  private readonly body: string;

  private constructor(path: string, doc: Document, closeLine: string, body: string) {
    this.path = path;
    this.doc = doc;
    this.closeLine = closeLine;
    this.body = body;
  }

  /** Reads and parses a file. Named errors: READ_*, NOT_FOUND, PARSE_ERROR. */
  static read(path: string): FrontmatterFile {
    let raw: string;
    try {
      raw = readFileSync(path, "utf8");
    } catch (cause) {
      throw new FrontmatterError("FRONTMATTER_READ_ERROR", `cannot read file: ${errorMessage(cause)}`, {
        file: path,
        cause,
      });
    }
    const { yamlText, closeLine, body } = splitFrontmatter(raw, path);
    if (/^\s*%/m.test(yamlText)) {
      throw new FrontmatterError("FRONTMATTER_PARSE_ERROR", `YAML directives are not supported`, { file: path });
    }
    const doc = parseDocument(yamlText);
    if (doc.errors.length > 0) {
      throw new FrontmatterError("FRONTMATTER_PARSE_ERROR", `invalid YAML: ${doc.errors[0].message}`, {
        file: path,
        cause: doc.errors[0],
      });
    }
    if (doc.contents !== null && !isMap(doc.contents)) {
      throw new FrontmatterError("FRONTMATTER_PARSE_ERROR", `frontmatter root is not a mapping`, { file: path });
    }
    return new FrontmatterFile(path, doc, closeLine, body);
  }

  /** Applies ops in order and returns the deltas of fields actually touched. */
  transform(ops: FieldOp[]): FieldDelta[] {
    const deltas: FieldDelta[] = [];
    for (const op of ops) {
      const before = this.valueOf(op.field);
      switch (op.op) {
        case "set": {
          this.doc.set(op.field, op.value);
          break;
        }
        case "append": {
          const node: unknown = this.doc.getIn([op.field], true);
          if (node === undefined) {
            throw new FrontmatterError(
              "MISSING_FIELD",
              `cannot append to '${op.field}': field is absent (zero fallback: no implicit list creation)`,
              { file: this.path, field: op.field },
            );
          }
          if (!isSeq(node)) {
            throw new FrontmatterError(
              "FIELD_NOT_A_LIST",
              `cannot append to '${op.field}': current value is not a list`,
              { file: this.path, field: op.field },
            );
          }
          const alreadyPresent = node.items.some(
            (item) => isScalar(item) && String(item.value) === op.value,
          );
          if (!alreadyPresent) {
            node.add(op.value);
          }
          break;
        }
        case "remove": {
          if (this.doc.getIn([op.field], true) === undefined) {
            throw new FrontmatterError(
              "MISSING_FIELD",
              `cannot remove '${op.field}': field is absent`,
              { file: this.path, field: op.field },
            );
          }
          this.doc.delete(op.field);
          break;
        }
      }
      const after = this.valueOf(op.field);
      if (!sameValue(before, after)) {
        deltas.push({ field: op.field, op: op.op, before, after });
      }
    }
    return deltas;
  }

  /**
   * Invariant on the resulting value: a scalar must be in `allowed`; every
   * element of a list must be in `allowed`. Missing field is a named error.
   */
  assert({ field, allowed }: FieldAssertion): void {
    const value = this.valueOf(field);
    if (this.doc.getIn([field], true) === undefined) {
      throw new FrontmatterError(
        "MISSING_FIELD",
        `cannot assert on '${field}': field is absent`,
        { file: this.path, field },
      );
    }
    const ok = Array.isArray(value)
      ? value.every((element) => allowed.includes(String(element)))
      : allowed.includes(String(value));
    if (!ok) {
      throw new FrontmatterError(
        "ASSERTION_FAILED",
        `resulting value of '${field}' (${JSON.stringify(value)}) is not in the allowed set [${allowed.join(", ")}]`,
        { file: this.path, field },
      );
    }
  }

  /** Full file content after transformations (delimiters + YAML + body). */
  content(): string {
    const serialized = this.doc.toString({ lineWidth: 0 });
    const head =
      serialized.length === 0
        ? "---\n"
        : `---\n${serialized.endsWith("\n") ? serialized : `${serialized}\n`}`;
    return head + this.closeLine + this.body;
  }

  private valueOf(field: string): unknown {
    const plain: unknown = this.doc.toJS();
    if (typeof plain !== "object" || plain === null) return undefined;
    return Reflect.get(plain, field);
  }
}

// ── Atomic write ───────────────────────────────────────────────────────────

/**
 * Writes content via temp file + rename, so the target is either fully old
 * or fully new — never truncated. The temp file lives in the target's
 * directory (same filesystem, rename stays atomic) and is cleaned up on error.
 */
export function atomicWrite(path: string, content: string): void {
  const tmpPath = join(
    dirname(path),
    `.${basename(path)}.frontmatter-${process.pid.toString(36)}-${randomUUID().slice(0, 8)}.tmp`,
  );
  try {
    writeFileSync(tmpPath, content, { flag: "wx" });
    renameSync(tmpPath, path);
  } catch (cause) {
    try {
      rmSync(tmpPath, { force: true });
    } catch {
      // Best-effort cleanup only: surface the original write failure below.
    }
    throw new FrontmatterError("WRITE_ERROR", `atomic write failed: ${errorMessage(cause)}`, {
      file: path,
      cause,
    });
  }
}

// ── Batch transform (the single safe entry point) ──────────────────────────

export function runTransform(paths: string[], options: TransformOptions): TransformResult {
  const mode = options.apply === true ? "apply" : "dry-run";

  // Phase 1 — read, transform and assert every file. Fail-fast: any named
  // error propagates before a single byte is written anywhere.
  const entries = paths.map((path) => {
    const file = FrontmatterFile.read(path);
    const changes = file.transform(options.ops);
    for (const assertion of options.asserts ?? []) {
      file.assert(assertion);
    }
    return { path, file, manifest: { file: path, changed: changes.length > 0, changes } };
  });

  const manifest: Manifest = {
    mode,
    files: entries.map((entry) => entry.manifest),
    totals: {
      files: entries.length,
      changed: entries.filter((entry) => entry.manifest.changed).length,
    },
  };

  // Phase 2 — emit the delta manifest BEFORE any write.
  const json = `${JSON.stringify(manifest, null, 2)}\n`;
  if (options.manifestPath) {
    atomicWrite(options.manifestPath, json);
  } else {
    process.stdout.write(json);
  }

  // Phase 3 — apply (only with explicit opt-in).
  let written = 0;
  if (mode === "apply") {
    for (const entry of entries) {
      if (entry.manifest.changed) {
        atomicWrite(entry.path, entry.file.content());
        written += 1;
      }
    }
  }

  return { manifest, written };
}

// ── Helpers ────────────────────────────────────────────────────────────────

function errorMessage(cause: unknown): string {
  return cause instanceof Error ? cause.message : String(cause);
}

function sameValue(a: unknown, b: unknown): boolean {
  return JSON.stringify(a) === JSON.stringify(b) && typeof a === typeof b;
}
