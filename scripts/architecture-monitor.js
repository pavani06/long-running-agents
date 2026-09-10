import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { parseArgs } from "node:util";
import { checkMap, validateMap } from "./lib/architecture-map.js";
import { renderMap } from "./lib/architecture-html.js";

const { positionals, values } = parseArgs({ allowPositionals: true, options: {
  repo: { type: "string", default: "." },
  map: { type: "string", default: "docs/architecture/repository-map.json" },
  ref: { type: "string", default: "HEAD" },
  output: { type: "string" },
} });
const [command] = positionals;
if (positionals.length !== 1 || !["check", "validate", "render"].includes(command)) {
  throw new Error("Usage: node scripts/architecture-monitor.js check|validate|render [--repo DIR] [--map FILE] [--ref COMMIT] [--output FILE]");
}
const repo = resolve(values.repo);
const mapPath = resolve(repo, values.map);
const map = JSON.parse(readFileSync(mapPath, "utf8"));
validateMap(repo, map);
let result;
if (command === "render") result = renderMap(map);
else if (command === "check") result = JSON.stringify(checkMap(repo, map, values.ref), null, 2) + "\n";
else result = JSON.stringify({ status: "valid", commit: map.commit }) + "\n";
if (values.output) {
  const output = resolve(repo, values.output);
  if (output === mapPath) throw new Error("Output must not overwrite the source map");
  writeFileSync(output, result, { flag: "wx" });
} else process.stdout.write(result);
