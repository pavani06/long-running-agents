import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync, renameSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { execFileSync } from "node:child_process";
import { checkMap, commit, git, validateMap } from "../../scripts/lib/architecture-map.js";
import { renderMap } from "../../scripts/lib/architecture-html.js";

function fixture(t) {
  const repo = mkdtempSync(join(tmpdir(), "architecture-monitor-"));
  t.after(() => rmSync(repo, { recursive: true, force: true }));
  git(repo, "init", "-q");
  git(repo, "config", "user.name", "Architecture test");
  git(repo, "config", "user.email", "test@example.invalid");
  git(repo, "config", "commit.gpgsign", "false");
  mkdirSync(join(repo, "core"));
  writeFileSync(join(repo, "core/main.txt"), "Core sends to store\n");
  writeFileSync(join(repo, "store.txt"), "Store receives\n");
  git(repo, "add", ".");
  git(repo, "commit", "-qm", "baseline");
  const entry = path => [{ path, start: 1, end: 1 }];
  const map = {
    version: 1, repository: "https://github.com/example/repo", commit: commit(repo, "HEAD"),
    title: "Test map", summary: "Core and store", focus: "core",
    components: [
      { id: "core", name: "Core", responsibility: "Send", paths: ["core/"], row: 0, column: 0, evidence: entry("core/main.txt") },
      { id: "store", name: "Store", responsibility: "Receive", paths: ["store.txt"], row: 0, column: 1, evidence: entry("store.txt") },
    ],
    relations: [{ id: "send", from: "core", to: "store", label: "sends", description: "Core sends to store", evidence: entry("core/main.txt") }],
  };
  return { repo, map };
}

test("unchanged committed tree is stable; local edits are disclosed but excluded", t => {
  const { repo, map } = fixture(t);
  assert.equal(checkMap(repo, map).status, "no-committed-changes");
  assert.equal(checkMap(repo, map).workingTreeDirty, false);
  writeFileSync(join(repo, "core/main.txt"), "uncommitted edit\n");
  const report = checkMap(repo, map);
  assert.equal(report.workingTreeDirty, true);
  assert.deepEqual(report.changes, []);
});

test("real commits expose affected components, relations, new files and unmapped paths", t => {
  const { repo, map } = fixture(t);
  const baseline = map.commit;
  writeFileSync(join(repo, "core/main.txt"), "Core no longer sends\n");
  writeFileSync(join(repo, "core/new file.txt"), "new worker\n");
  writeFileSync(join(repo, "unknown.txt"), "new subsystem\n");
  writeFileSync(join(repo, "store.txt.extra"), "not the store\n");
  git(repo, "add", ".");
  git(repo, "commit", "-qm", "new worker and changed relation");
  const report = checkMap(repo, map);
  assert.equal(report.status, "review-required");
  assert.equal(report.target, commit(repo, "HEAD"));
  assert.deepEqual(report.changes.find(change => change.path === "core/main.txt").relations, ["send"]);
  assert.deepEqual(report.changes.find(change => change.path === "core/new file.txt").components, ["core"]);
  assert.equal(report.changes.find(change => change.path === "unknown.txt").unmapped, true);
  assert.equal(report.changes.find(change => change.path === "store.txt.extra").unmapped, true);
  assert.equal(map.commit, baseline, "checking must never advance the baseline");
});

test("renaming and deleting evidence stays visible against the original commit", t => {
  const { repo, map } = fixture(t);
  renameSync(join(repo, "core/main.txt"), join(repo, "renamed.txt"));
  rmSync(join(repo, "store.txt"));
  git(repo, "add", "-A");
  git(repo, "commit", "-qm", "rename and delete");
  const changes = checkMap(repo, map).changes;
  assert.equal(changes.find(change => change.path === "core/main.txt").status, "D");
  assert.equal(changes.find(change => change.path === "store.txt").status, "D");
  assert.equal(changes.find(change => change.path === "renamed.txt").status, "A");
  assert.throws(() => validateMap(repo, { ...map, commit: commit(repo, "HEAD") }), /Invalid scopes|Missing evidence/u);
});

test("a reviewed relation removal can advance the baseline and regenerate the page", t => {
  const { repo, map } = fixture(t);
  writeFileSync(join(repo, "core/main.txt"), "Core operates independently\n");
  git(repo, "add", ".");
  git(repo, "commit", "-qm", "remove store integration");
  assert.equal(checkMap(repo, map).status, "review-required");
  // Represents the agent's explicit edit after reading the changed source;
  // the detector must not make this semantic decision itself.
  const revised = structuredClone(map);
  revised.relations = [];
  revised.components[0].responsibility = "Operates independently";
  revised.commit = commit(repo, "HEAD");
  validateMap(repo, revised);
  assert.equal(checkMap(repo, revised).status, "no-committed-changes");
  const html = renderMap(revised);
  assert.ok(!html.includes("Core sends to store"));
  assert.ok(html.includes("Operates independently"));
  assert.ok(html.includes(`/blob/${revised.commit}/core/main.txt`));
  assert.notEqual(revised.commit, map.commit);
});

test("rejects unverifiable evidence, invalid references and unsupported layouts", t => {
  const { repo, map } = fixture(t);
  const mutate = fn => { const copy = structuredClone(map); fn(copy); return copy; };
  assert.throws(() => validateMap(repo, mutate(m => { m.components[0].evidence[0].end = 100; })), /Invalid evidence lines/u);
  assert.throws(() => validateMap(repo, mutate(m => { m.components[0].evidence[0].path = "../secret"; })), /Missing evidence/u);
  assert.throws(() => validateMap(repo, mutate(m => { m.relations[0].to = "missing"; })), /Unknown relation endpoint/u);
  assert.throws(() => validateMap(repo, mutate(m => { m.components[1].row = 1; })), /adjacent cells/u);
  assert.throws(() => checkMap(repo, map, "--help"));
});

test("HTML escapes content, keeps pinned evidence links and exposes every relation", t => {
  const { repo, map } = fixture(t);
  map.title = '<script>alert("x")</script>';
  validateMap(repo, map);
  const html = renderMap(map);
  assert.ok(!html.includes("<script>"));
  assert.ok(html.includes("&lt;script&gt;"));
  assert.ok(html.includes(`/blob/${map.commit}/core/main.txt#L1-L1`));
  assert.ok(html.includes('aria-labelledby="map-title map-desc"'));
  assert.ok(html.includes("Core sends to store"));
  assert.equal(renderMap(map), html, "rendering is deterministic");
});

test("CLI works with another repository and refuses to overwrite the map or output", t => {
  const { repo, map } = fixture(t);
  const mapPath = join(repo, "map.json");
  writeFileSync(mapPath, JSON.stringify(map));
  const cli = resolve("scripts/architecture-monitor.js");
  const args = [cli, "check", "--repo", repo, "--map", "map.json"];
  const report = JSON.parse(execFileSync(process.execPath, args, { encoding: "utf8" }));
  assert.equal(report.baseline, map.commit);
  assert.throws(() => execFileSync(process.execPath, [...args, "--output", "map.json"], { stdio: "pipe" }));
  assert.deepEqual(JSON.parse(readFileSync(mapPath, "utf8")), map);
  execFileSync(process.execPath, [...args, "--output", "report.json"]);
  assert.throws(() => execFileSync(process.execPath, [...args, "--output", "report.json"], { stdio: "pipe" }));
});
