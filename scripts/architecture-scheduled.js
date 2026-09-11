import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync, openSync, closeSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";
import { checkMap, git, commit } from "./lib/architecture-map.js";
import { renderMap } from "./lib/architecture-html.js";
import { mapFile, htmlFile, reviewFile, sourceChanges, validateReview, reviewPrompt, readReviewOutput } from "./lib/architecture-review.js";

const { values } = parseArgs({ options: {
  state: { type: "string", default: join(homedir(), ".local/state/architecture-monitor") },
  repo: { type: "string", default: "pavani06/long-running-agents" },
  model: { type: "string", default: "zai-coding-plan/glm-5.3-flash" },
  "review-log": { type: "string" },
} });
if (!/^[\w.-]+\/[\w.-]+$/u.test(values.repo)) throw new Error("Expected owner/repository");
process.umask(0o077);
const state = resolve(values.state);
const checkout = join(state, "checkout");
const installation = dirname(dirname(fileURLToPath(import.meta.url)));
const runDirectory = join(state, "runs", new Date().toISOString().replaceAll(":", "-"));
mkdirSync(runDirectory, { recursive: true });
let stage = "preflight";
const status = { startedAt: new Date().toISOString(), repository: values.repo, model: values.model, reasoningEffort: "low", runDirectory };
const save = extra => {
  Object.assign(status, extra, { finishedAt: new Date().toISOString() });
  const json = JSON.stringify(status, null, 2) + "\n";
  writeFileSync(join(runDirectory, "status.json"), json);
  writeFileSync(join(state, "latest.json"), json);
  process.stdout.write(json);
};
const gh = (...args) => execFileSync(process.env.ARCHITECTURE_GH || "gh", [...args, "--repo", values.repo], {
  encoding: "utf8", timeout: 120_000, stdio: ["ignore", "pipe", "pipe"],
});
const jsonFile = path => JSON.parse(readFileSync(path, "utf8"));

function run() {
  stage = "pending-pr";
  const pending = JSON.parse(gh("pr", "list", "--state", "open", "--limit", "100", "--json", "url,headRefName"))
    .find(pr => pr.headRefName.startsWith("automation/architecture-map-"));
  if (pending) { save({ status: "awaiting-merge", pr: pending.url, modelCalled: false }); return; }

  stage = "fetch";
  if (!existsSync(checkout)) {
    execFileSync("git", ["clone", `https://github.com/${values.repo}.git`, checkout], {
      timeout: 120_000, stdio: ["ignore", "pipe", "pipe"],
    });
  }
  // Only this owned checkout is touched. Failed runs are preserved for inspection.
  if (git(checkout, "status", "--porcelain", "--untracked-files=all").trim()) {
    throw new Error("Owned checkout has pending edits from an earlier run; inspect before retrying");
  }
  git(checkout, "fetch", "origin", "main");
  const target = commit(checkout, "origin/main");
  status.target = target;
  // Switching the dedicated checkout never changes the operator's working tree.
  git(checkout, "switch", "--detach", target);
  const map = jsonFile(join(checkout, mapFile));
  const report = checkMap(checkout, map, target);
  status.baseline = report.baseline;
  writeFileSync(join(runDirectory, "input.json"), JSON.stringify(report, null, 2) + "\n");
  if (!sourceChanges(report).length) {
    save({ status: "unchanged", modelCalled: false, ignoredDerivedChanges: report.changes.length }); return;
  }
  const branch = `automation/architecture-map-${target.slice(0, 12)}`;
  status.branch = branch;
  // Idempotent recovery if a prior push succeeded but PR creation failed.
  const remoteBranch = git(checkout, "ls-remote", "--heads", "origin", branch).trim();
  if (remoteBranch) throw new Error(`Review branch already exists: ${branch}; inspect its PR before retrying`);
  git(checkout, "switch", "-c", `${branch}-${Date.now()}`);

  stage = "opencode-review";
  status.modelCalled = !values["review-log"];
  const agentSource = readFileSync(join(installation, ".opencode/agents/repository-architecture-monitor.md"), "utf8")
    .replace(/^---\n[\s\S]*?\n---\n/u, "");
  const ledgerPath = reviewFile(target);
  const config = {
    share: "disabled",
    mcp: { zread: { enabled: false }, promptschat: { enabled: false }, context7: { enabled: false } },
    agent: { "repository-architecture-monitor": {
      mode: "primary", steps: 40, reasoningEffort: "low", prompt: agentSource,
      permission: {
        "*": "deny", read: "allow", glob: "allow", grep: "allow",
        edit: "deny", bash: "deny",
      },
    } },
  };
  const diff = git(checkout, "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--unified=4",
    report.baseline, target, "--", ...sourceChanges(report).map(change => change.path));
  if (Buffer.byteLength(diff) > 200_000) throw new Error("Source diff exceeds the 200 KB review budget; split the review manually");
  const prompt = reviewPrompt(report, diff);
  writeFileSync(join(runDirectory, "prompt.txt"), prompt);
  const reviewLog = join(runDirectory, "opencode.jsonl");
  if (values["review-log"]) {
    status.replayedLog = resolve(values["review-log"]);
    writeFileSync(reviewLog, readFileSync(status.replayedLog));
  } else {
    const log = openSync(reviewLog, "wx", 0o600);
    try {
      execFileSync(process.env.ARCHITECTURE_OPENCODE || "opencode", ["--pure", "run", "--model", values.model,
        "--dir", checkout, "--agent", "repository-architecture-monitor", "--format", "json", "--title", `Architecture ${target.slice(0, 12)}`, prompt], {
        cwd: checkout, timeout: 900_000, killSignal: "SIGKILL", stdio: ["ignore", log, log],
        env: { ...process.env, OPENCODE_CONFIG_CONTENT: JSON.stringify(config),
          OPENCODE_DISABLE_AUTOUPDATE: "true", OPENCODE_DISABLE_CLAUDE_CODE: "true" },
      });
    } finally { closeSync(log); }
  }

  stage = "validate";
  const changed = [...new Set([
    ...git(checkout, "diff", "--no-renames", "--name-only", "-z", "HEAD", "--").split("\0"),
    ...git(checkout, "ls-files", "--others", "--exclude-standard", "-z").split("\0"),
  ].filter(Boolean))];
  if (commit(checkout, "HEAD") !== target) throw new Error("Agent changed HEAD");
  if (changed.length) throw new Error("Read-only agent modified the checkout");
  const { map: revised, review: ledger, normalizedCommits } = readReviewOutput(readFileSync(reviewLog, "utf8"), report);
  validateReview(checkout, report, revised, ledger, changed);
  status.normalizedEvidenceCommits = normalizedCommits;
  if (normalizedCommits) ledger.normalization = { symbolicEvidenceCommitsExpanded: normalizedCommits };
  writeFileSync(join(checkout, mapFile), JSON.stringify(revised, null, 2) + "\n");
  mkdirSync(dirname(join(checkout, ledgerPath)), { recursive: true });
  writeFileSync(join(checkout, ledgerPath), JSON.stringify(ledger, null, 2) + "\n");
  writeFileSync(join(checkout, htmlFile), renderMap(revised));
  const tests = execFileSync(process.execPath, ["--test", "tests/unit/architecture-monitor.test.js", "tests/unit/architecture-review.test.js"], {
    cwd: installation, timeout: 120_000, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"],
  });
  writeFileSync(join(runDirectory, "tests.txt"), tests);
  git(checkout, "diff", "--check");

  stage = "publish";
  git(checkout, "-c", "user.name=Architecture Monitor", "-c", "user.email=architecture-monitor@users.noreply.github.com",
    "add", "--", mapFile, htmlFile, ledgerPath);
  git(checkout, "-c", "user.name=Architecture Monitor", "-c", "user.email=architecture-monitor@users.noreply.github.com",
    "-c", "commit.gpgsign=false", "commit", "-m", `docs(architecture): review repository at ${target.slice(0, 12)}`);
  git(checkout, "push", "origin", `HEAD:refs/heads/${branch}`);
  const body = `Atualiza o mapa de arquitetura após revisar as mudanças de ${report.baseline} até ${target}.\n\n` +
    `Foram revisados ${ledger.dispositions.length} caminhos. O JSON, o HTML e o registro por arquivo estão neste PR.\n\n` +
    `Validação: evidências por commit e linha, cobertura completa da fila, escopo de escrita e testes automatizados passaram.\n\n` +
    `Revisão semântica: OpenCode, modelo ${values.model}. Merge continua manual.\n`;
  const bodyPath = join(runDirectory, "pr-body.md");
  writeFileSync(bodyPath, body);
  const pr = gh("pr", "create", "--base", "main", "--head", branch,
    "--title", `docs(architecture): mapa revisado até ${target.slice(0, 12)}`, "--body-file", bodyPath).trim();
  save({ status: "pr-opened", pr, reviewedPaths: ledger.dispositions.length });
}

try { run(); }
catch (error) {
  // Child-process errors may contain provider output. Keep them out of the journal.
  const reason = error instanceof Error && !Object.hasOwn(error, "cmd") && !Object.hasOwn(error, "stderr")
    ? String(error) : `Command failed during ${stage}; inspect the private run directory`;
  save({ status: "failed", stage, reason });
  process.exitCode = 1;
}
