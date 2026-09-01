#!/usr/bin/env -S npx tsx
/**
 * frontmatter.ts — Safe frontmatter YAML transformer (CLI).
 *
 * CLI surface of scripts/lib/frontmatter.ts (issue #205, epic #197).
 * Dry-run by default: nothing is written unless --apply is passed.
 * The delta manifest (per-file before/after of touched fields) is always
 * emitted BEFORE any write, to stdout or to --manifest <file>.
 *
 * Usage:
 *   npx tsx scripts/frontmatter.ts <file...> [options]
 *
 * Options:
 *   --set <field=value>     set field to value (creates the field when absent)
 *   --append <field=value>  append value to an existing list field
 *                           (idempotent; MISSING_FIELD/FIELD_NOT_A_LIST otherwise)
 *   --remove <field>        remove field (MISSING_FIELD when absent)
 *   --assert <field=v1,v2>  resulting value must be in the allowed set
 *                           (for lists: every element; checked AFTER ops)
 *   --apply                 write changes (default: dry-run, writes nothing)
 *   --manifest <file>       write the delta manifest to this file (default: stdout)
 *   -h, --help              show this help
 *
 * Exit codes: 0 on success (including no-op dry-runs), 1 on any named error
 * ([INVALID_SPEC], [MISSING_FIELD], [ASSERTION_FAILED], ...) — in which case
 * nothing was written.
 */

import { runTransform, FrontmatterError, type FieldOp, type FieldAssertion } from "./lib/frontmatter.ts";

// ── Argument parsing ───────────────────────────────────────────────────────

interface CliArgs {
  files: string[];
  ops: FieldOp[];
  asserts: FieldAssertion[];
  apply: boolean;
  manifestPath?: string;
}

function invalid(message: string): never {
  throw new FrontmatterError("INVALID_SPEC", message);
}

function splitFieldRaw(raw: string, flag: string): { field: string; rest: string } {
  const eq = raw.indexOf("=");
  if (eq <= 0) invalid(`${flag} expects <field=value>, got '${raw}'`);
  return { field: raw.slice(0, eq), rest: raw.slice(eq + 1) };
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = { files: [], ops: [], asserts: [], apply: false };
  const takeValue = (flag: string, index: number): [string, number] => {
    if (index + 1 >= argv.length) invalid(`${flag} expects a value`);
    return [argv[index + 1], index + 1];
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case "-h":
      case "--help": {
        process.stdout.write(USAGE);
        process.exit(0);
        break;
      }
      case "--apply": {
        args.apply = true;
        break;
      }
      case "--manifest": {
        const [value, next] = takeValue(arg, i);
        args.manifestPath = value;
        i = next;
        break;
      }
      case "--set": {
        const [raw, next] = takeValue(arg, i);
        i = next;
        const { field, rest: value } = splitFieldRaw(raw, arg);
        args.ops.push({ op: "set", field, value });
        break;
      }
      case "--append": {
        const [raw, next] = takeValue(arg, i);
        i = next;
        const { field, rest: value } = splitFieldRaw(raw, arg);
        args.ops.push({ op: "append", field, value });
        break;
      }
      case "--remove": {
        const [raw, next] = takeValue(arg, i);
        i = next;
        if (raw.length === 0 || raw.startsWith("--")) invalid(`--remove expects a field name, got '${raw}'`);
        args.ops.push({ op: "remove", field: raw });
        break;
      }
      case "--assert": {
        const [raw, next] = takeValue(arg, i);
        i = next;
        const { field, rest } = splitFieldRaw(raw, arg);
        const allowed = rest.split(",");
        if (allowed.some((value) => value.length === 0)) {
          invalid(`${arg} expects <field=v1,v2> with non-empty values, got '${raw}'`);
        }
        args.asserts.push({ field, allowed });
        break;
      }
      default: {
        if (arg.startsWith("--")) invalid(`unknown option: ${arg}`);
        args.files.push(arg);
      }
    }
  }

  if (args.files.length === 0) invalid("at least one file is required");
  if (args.ops.length === 0 && args.asserts.length === 0) {
    invalid("at least one of --set, --append, --remove or --assert is required");
  }
  return args;
}

// ── Entry point ────────────────────────────────────────────────────────────

const USAGE = `Usage: npx tsx scripts/frontmatter.ts <file...> [options]

Options:
  --set <field=value>     set field to value (creates the field when absent)
  --append <field=value>  append value to an existing list field (idempotent)
  --remove <field>        remove field (error when absent)
  --assert <field=v1,v2>  resulting value must be in the allowed set
  --apply                 write changes (default: dry-run, writes nothing)
  --manifest <file>       write the delta manifest to this file (default: stdout)
  -h, --help              show this help

Safety: delta manifest is emitted before any write; writes are atomic
(temp + rename); missing fields are named errors, never inferred.
`;

try {
  const args = parseArgs(process.argv.slice(2));
  const result = runTransform(args.files, {
    ops: args.ops,
    asserts: args.asserts,
    apply: args.apply,
    manifestPath: args.manifestPath,
  });
  const { totals } = result.manifest;
  const summary = args.apply
    ? `apply: ${totals.changed}/${totals.files} file(s) changed, ${result.written} written\n`
    : `dry-run: ${totals.changed}/${totals.files} file(s) would change; nothing written (pass --apply to write)\n`;
  process.stderr.write(summary);
} catch (error) {
  if (error instanceof FrontmatterError) {
    const where = [error.file, error.field].filter((part) => part !== undefined).join(":");
    process.stderr.write(`[${error.code}]${where.length > 0 ? ` ${where}:` : ""} ${error.message}\n`);
  } else {
    process.stderr.write(`unexpected error: ${error instanceof Error ? (error.stack ?? error.message) : String(error)}\n`);
  }
  process.exitCode = 1;
}
