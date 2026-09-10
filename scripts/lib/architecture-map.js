import { execFileSync } from "node:child_process";

export function git(repo, ...args) {
  return execFileSync("git", ["-C", repo, ...args], {
    encoding: "utf8", maxBuffer: 32 * 1024 * 1024, stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env, GIT_OPTIONAL_LOCKS: "0" },
  });
}

export function commit(repo, ref) {
  return git(repo, "rev-parse", "--verify", "--end-of-options", `${ref}^{commit}`).trim();
}

function requireValue(condition, message) {
  if (!condition) throw new Error(message);
}

function safePath(path) {
  return typeof path === "string" && path.length > 0 &&
    !path.startsWith("/") && !/[\\:]/u.test(path) &&
    ![...path].some(character => character.codePointAt(0) < 32) &&
    !path.split("/").some(part => part === ".." || part === ".");
}

const matches = (path, scope) => scope.endsWith("/") ? path.startsWith(scope) : path === scope;

export function validateMap(repo, map) {
  requireValue(map.version === 1, "Unsupported map version");
  requireValue(typeof map.title === "string" && map.title.length > 0, "Missing title");
  requireValue(typeof map.summary === "string", "Missing summary");
  requireValue(/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/u.test(map.repository), "Expected a GitHub repository URL");
  requireValue(/^[a-f0-9]{40}$/u.test(map.commit), "Map needs a full commit SHA");
  requireValue(commit(repo, map.commit) === map.commit, "Baseline commit unavailable");
  requireValue(Array.isArray(map.components) && map.components.length > 0 && map.components.length <= 9, "Use 1–9 components");
  requireValue(Array.isArray(map.relations) && map.relations.length <= 12, "Use at most 12 relations");
  requireValue(map.limitations === undefined || (Array.isArray(map.limitations) && map.limitations.every(item => typeof item === "string")), "Limitations must be text entries");
  const files = git(repo, "ls-tree", "-r", "--name-only", "-z", map.commit).split("\0").filter(Boolean);
  const ids = new Set();
  const cells = new Set();
  const contents = new Map();
  const evidence = item => {
    requireValue(Array.isArray(item.evidence) && item.evidence.length > 0, `Missing evidence: ${item.id}`);
    for (const entry of item.evidence) {
      requireValue(safePath(entry.path) && files.includes(entry.path), `Missing evidence file: ${entry.path}`);
      if (!contents.has(entry.path)) contents.set(entry.path, git(repo, "show", `${map.commit}:${entry.path}`).split("\n"));
      requireValue(Number.isInteger(entry.start) && Number.isInteger(entry.end) && entry.start >= 1 &&
        entry.end >= entry.start && entry.end <= contents.get(entry.path).length, `Invalid evidence lines: ${entry.path}`);
    }
  };
  for (const component of map.components) {
    requireValue(typeof component.id === "string" && /^[a-z][a-z0-9-]*$/u.test(component.id) && !ids.has(component.id), "Invalid or duplicate component ID");
    ids.add(component.id);
    requireValue(typeof component.name === "string" && component.name.length > 0 && component.name.length <= 28, `Use a short name: ${component.id}`);
    requireValue(typeof component.responsibility === "string" && component.responsibility.length > 0, `Missing responsibility: ${component.id}`);
    requireValue(Array.isArray(component.paths) && component.paths.length > 0 && component.paths.every(path =>
      safePath(path) && files.some(file => matches(file, path))), `Invalid scopes: ${component.id}`);
    requireValue(Number.isInteger(component.row) && component.row >= 0 && component.row < 3 &&
      Number.isInteger(component.column) && component.column >= 0 && component.column < 3, "Use a 3×3 layout");
    const cell = `${component.row}:${component.column}`;
    requireValue(!cells.has(cell), "Overlapping components");
    cells.add(cell);
    evidence(component);
  }
  requireValue(map.focus === undefined || map.components.some(component => component.id === map.focus), "Unknown focus component");
  const pairs = new Set();
  for (const relation of map.relations) {
    requireValue(typeof relation.id === "string" && !ids.has(relation.id) && /^[a-z][a-z0-9-]*$/u.test(relation.id), "Invalid or duplicate relation ID");
    ids.add(relation.id);
    const from = map.components.find(component => component.id === relation.from);
    const to = map.components.find(component => component.id === relation.to);
    requireValue(from && to, `Unknown relation endpoint: ${relation.id}`);
    const pair = [from.id, to.id].sort().join(":");
    requireValue(!pairs.has(pair), "Use one relation per pair in the overview");
    pairs.add(pair);
    requireValue(Math.abs(from.row - to.row) + Math.abs(from.column - to.column) === 1, "Overview connectors need adjacent cells; split complex maps into details");
    requireValue(typeof relation.label === "string" && relation.label.length > 0 && relation.label.length <= 14, "Use relation labels up to 14 characters");
    requireValue(typeof relation.description === "string" && relation.description.length > 0, "Missing relation description");
    evidence(relation);
  }
  return map;
}

export function checkMap(repo, map, ref = "HEAD") {
  validateMap(repo, map);
  const target = commit(repo, ref);
  // Renames deliberately become deletion + addition: neither old evidence nor new scope disappears.
  const fields = git(repo, "diff", "--no-ext-diff", "--no-renames", "--name-status", "-z", map.commit, target, "--").split("\0");
  const changes = [];
  for (let index = 0; index < fields.length - 1; index += 2) {
    const path = fields[index + 1];
    const components = map.components.filter(component => component.paths.some(scope => matches(path, scope)) ||
      component.evidence.some(entry => entry.path === path)).map(component => component.id);
    const relations = map.relations.filter(relation => relation.evidence.some(entry => entry.path === path) ||
      components.includes(relation.from) || components.includes(relation.to)).map(relation => relation.id);
    changes.push({ status: fields[index], path, components, relations, unmapped: components.length === 0 && relations.length === 0 });
  }
  return {
    version: 1, repository: map.repository, baseline: map.commit, target,
    status: changes.length ? "review-required" : "no-committed-changes",
    workingTreeDirty: git(repo, "status", "--porcelain", "-z", "--untracked-files=normal").length > 0,
    scope: "Committed trees only; local edits are excluded. Changed paths are review candidates, not architectural conclusions.",
    changes,
  };
}
