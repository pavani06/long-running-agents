import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, rmSync, mkdirSync, renameSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { git, commit, checkMap } from "../../scripts/lib/architecture-map.js";
import { sourceChanges, validateReview, reviewPrompt, readReviewOutput, mapFile, htmlFile, reviewFile } from "../../scripts/lib/architecture-review.js";

function fixture(t) {
  const repo = mkdtempSync(join(tmpdir(), "scheduled-architecture-test-"));
  t.after(() => rmSync(repo, { recursive: true, force: true }));
  git(repo, "init", "-q");
  git(repo, "config", "user.name", "Test");
  git(repo, "config", "user.email", "test@example.invalid");
  git(repo, "config", "commit.gpgsign", "false");
  writeFileSync(join(repo, "source.txt"), "component v1\n");
  git(repo, "add", "."); git(repo, "commit", "-qm", "baseline");
  const map = { version: 1, repository: "https://github.com/example/repo", commit: commit(repo, "HEAD"),
    title: "Test", summary: "A component", components: [{ id: "core", name: "Core", row: 0, column: 0,
      responsibility: "A component", paths: ["source.txt"], evidence: [{ path: "source.txt", start: 1, end: 1 }] }], relations: [] };
  writeFileSync(join(repo, "source.txt"), "component v2\n");
  git(repo, "add", "."); git(repo, "commit", "-qm", "update");
  const report = checkMap(repo, map);
  const revised = { ...map, commit: report.target };
  const ledger = { baseline: report.baseline, target: report.target, mapChanges: [], unresolved: [],
    dispositions: [{ path: "source.txt", classification: "no-architecture-change", reason: "Same component",
      evidence: [{ path: "source.txt", commit: report.target, start: 1, end: 1 }] }] };
  return { repo, report, revised, ledger };
}

test("generated map merges do not trigger another model call; human docs still do", () => {
  const report = { changes: [mapFile, htmlFile, reviewFile("a".repeat(40))].map(path => ({ path })) };
  assert.deepEqual(sourceChanges(report), []);
  report.changes.push({ path: "docs/architecture/README.md" });
  assert.equal(sourceChanges(report).length, 1);
});

test("complete evidenced review is accepted and prompt fixes target and output scope", t => {
  const { repo, report, revised, ledger } = fixture(t);
  assert.doesNotThrow(() => validateReview(repo, report, revised, ledger, [mapFile, reviewFile(report.target)]));
  const prompt = reviewPrompt(report);
  assert.ok(prompt.includes(report.target));
  assert.ok(prompt.includes("source.txt"));
  assert.ok(prompt.includes("Não faça commit"));
});

test("missing, duplicate and uncertain dispositions cannot publish", t => {
  const { repo, report, revised, ledger } = fixture(t);
  assert.throws(() => validateReview(repo, report, revised, { ...ledger, dispositions: [] }, []), /coverage/u);
  assert.throws(() => validateReview(repo, report, revised, { ...ledger, dispositions: [...ledger.dispositions, ...ledger.dispositions] }, []), /coverage/u);
  ledger.dispositions[0].classification = "uncertain";
  assert.throws(() => validateReview(repo, report, revised, ledger, []), /Uncertain/u);
});

test("scope escapes, stale baseline and fabricated evidence are rejected", t => {
  const { repo, report, revised, ledger } = fixture(t);
  assert.throws(() => validateReview(repo, report, revised, ledger, ["package.json"]), /outside/u);
  assert.throws(() => validateReview(repo, report, { ...revised, repository: "https://github.com/other/repo" }, ledger, []), /identity/u);
  assert.throws(() => validateReview(repo, report, { ...revised, commit: report.baseline }, ledger, []), /advance/u);
  assert.throws(() => validateReview(repo, report, revised, { ...ledger, baseline: report.target }, []), /mismatch/u);
  assert.throws(() => validateReview(repo, report, revised, { ...ledger, unresolved: ["unknown"] }, []), /Unresolved/u);
  ledger.dispositions[0].evidence[0].end = 999;
  assert.throws(() => validateReview(repo, report, revised, ledger, []), /evidence lines/u);
});

const completedOutput = text => [
  { type: "text", part: { text: "Intermediate analysis is not an artifact" } },
  { type: "text", part: { text } },
  { type: "step_finish", part: { reason: "stop" } },
].map(event => JSON.stringify(event)).join("\n");

test("controller parses only the final complete envelope and validates it", t => {
  const { repo, report, revised, ledger } = fixture(t);
  const result = readReviewOutput(completedOutput(JSON.stringify({ map: revised, review: ledger })), report);
  validateReview(repo, report, result.map, result.review, []);
  assert.equal(result.normalizedCommits, 0);
});

test("saved two-artifact response expands only exact commit aliases, with validation intact", t => {
  const { repo, report, revised, ledger } = fixture(t);
  ledger.dispositions[0].evidence[0].commit = "target";
  const text = `Map:\n\`\`\`json\n${JSON.stringify(revised)}\n\`\`\`\nReview:\n\`\`\`json\n${JSON.stringify(ledger)}\n\`\`\``;
  const result = readReviewOutput(completedOutput(text), report);
  assert.equal(result.normalizedCommits, 1);
  assert.equal(result.review.dispositions[0].evidence[0].commit, report.target);
  validateReview(repo, report, result.map, result.review, []);
  assert.throws(() => readReviewOutput(completedOutput(text), { ...report, target: report.baseline }), /mismatch/u);
});

test("provider errors, incomplete streams and ambiguous artifacts cannot be replayed", t => {
  const { report, revised, ledger } = fixture(t);
  const good = completedOutput(JSON.stringify({ map: revised, review: ledger }));
  assert.throws(() => readReviewOutput(good.split("\n").slice(0, -1).join("\n"), report), /incomplete/u);
  assert.throws(() => readReviewOutput(good + '\n{"type":"error"}', report), /reported an error/u);
  assert.throws(() => readReviewOutput(completedOutput("Just an assurance, no artifacts"), report), /Expected/u);
});

function runController(t, state, pending) {
  const ghPath = join(state, "fake-gh");
  writeFileSync(ghPath, `#!${process.execPath}\nprocess.stdout.write(${JSON.stringify(JSON.stringify(pending))});\n`, { mode: 0o700 });
  t.after(() => rmSync(state, { recursive: true, force: true }));
  return JSON.parse(execFileSync(process.execPath, [resolve("scripts/architecture-scheduled.js"),
    "--state", state, "--repo", "example/repo"], { encoding: "utf8",
    env: { ...process.env, ARCHITECTURE_GH: ghPath, ARCHITECTURE_OPENCODE: "/must-not-call-a-model" },
  }));
}

test("controller skips Git and model when an automation PR is pending", t => {
  const state = mkdtempSync(join(tmpdir(), "architecture-controller-"));
  const result = runController(t, state, [{ headRefName: "automation/architecture-map-abc", url: "https://github.com/example/repo/pull/1" }]);
  assert.equal(result.status, "awaiting-merge");
  assert.equal(result.modelCalled, false);
});

test("controller fetches a local main and skips model after a generated-map-only commit", t => {
  const { repo, revised } = fixture(t);
  const state = mkdtempSync(join(tmpdir(), "architecture-controller-"));
  const checkout = join(state, "checkout");
  renameSync(repo, checkout);
  mkdirSync(join(checkout, "docs/architecture"), { recursive: true });
  writeFileSync(join(checkout, mapFile), JSON.stringify(revised));
  git(checkout, "add", "."); git(checkout, "commit", "-qm", "generated map update");
  git(checkout, "branch", "-M", "main");
  git(checkout, "remote", "add", "origin", ".");
  const result = runController(t, state, []);
  assert.equal(result.status, "unchanged");
  assert.equal(result.modelCalled, false);
  assert.equal(result.ignoredDerivedChanges, 1);
});
