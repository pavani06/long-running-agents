---
url: "https://github.com/obra/superpowers"
key: "2046f5e50faf"
status: "ok"
final_url: "https://github.com/obra/superpowers"
method: "trafilatura"
content_hash: "e43c4c6566a1ea18c7563e0a14d95523e39c11b2"
text_len: 9700
fetched: "2026-09-15"
---

Superpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them.
It starts from the moment you fire up your coding agent. As soon as it sees that you're building something, it doesn't just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do.
Once it's teased a spec out of the conversation, it shows it to you in chunks short enough to actually read and digest.
After you've signed off on the design, your agent puts together an implementation plan that's clear enough for an enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing to follow. It emphasizes true red/green TDD, YAGNI (You Aren't Gonna Need It), and DRY.
Next up, once you say "go", it launches a subagent-driven-development process, having agents work through each engineering task, inspecting and reviewing their work, and continuing forward. It's not uncommon for your agent to work autonomously for a couple hours at a time without deviating from the plan you put together.
There's a bunch more to it, but that's the core of the system. And because the skills trigger automatically, you don't need to do anything special. Your coding agent just has Superpowers.
If you're using Superpowers in enterprise and could benefit from commercial support, additional tooling, or managed spending, please don't hesitate to drop us a line at sales@primeradiant.com.
Installation differs by harness. If you use more than one, install Superpowers separately for each one.
Superpowers is available via the official Claude plugin marketplace
- 
Install the plugin from Anthropic's official marketplace: /plugin install superpowers@claude-plugins-official
The Superpowers marketplace provides Superpowers and some other related plugins for Claude Code.
- 
Register the marketplace: /plugin marketplace add obra/superpowers-marketplace
- 
Install the plugin from this marketplace: /plugin install superpowers@superpowers-marketplace
Install Superpowers as a plugin from this repository:
agy plugin install https://github.com/obra/superpowers
Antigravity runs the plugin's session-start hook, so Superpowers is active from the first message. Reinstall with the same command to update.
Superpowers is available via the official Codex plugin marketplace.
- In the Codex app, click on Plugins in the sidebar.
- You should see Superpowers in the Coding section.
- Click the + next to Superpowers and follow the prompts.
Superpowers is available via the official Codex plugin marketplace.
- 
Open the plugin search interface: /plugins
- 
Search for Superpowers: superpowers
- 
Select Install Plugin .
- 
In Cursor Agent chat, install from marketplace: /add-plugin superpowers
- 
Or search for "superpowers" in the plugin marketplace.
- 
Install the plugin from this repository: devin plugins install obra/superpowers
- 
Update to the latest version with: devin plugins update superpowers
- 
Register the marketplace: droid plugin marketplace add https://github.com/obra/superpowers
- 
Install the plugin: droid plugin install superpowers@superpowers
- 
Install the extension: gemini extensions install https://github.com/obra/superpowers
- 
Update later: gemini extensions update superpowers
- 
Register the marketplace: copilot plugin marketplace add obra/superpowers-marketplace
- 
Install the plugin: copilot plugin install superpowers@superpowers-marketplace
Superpowers is available via the official Grok plugin marketplace.
- 
Install the plugin from xAI's official marketplace: grok plugin install superpowers@xai-official --trust
- 
Or open the marketplace in the TUI, search for Superpowers, and install it: /marketplace
Superpowers is available in Kimi Code's plugin marketplace.
- 
Open Kimi Code's plugin manager: /plugins
- 
Go to Marketplace >Superpowers and install it.
- 
Or install directly from this repository: /plugins install https://github.com/obra/superpowers
- 
Detailed docs: docs/README.kimi.md
OpenCode uses its own plugin install; install Superpowers separately even if you already use it in another harness.
- 
Tell OpenCode: Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
- 
Detailed docs: docs/README.opencode.md
Install Superpowers as a Pi package from this repository:
pi install git:github.com/obra/superpowers
For local development, run Pi with this checkout loaded as a temporary package:
pi -e /path/to/superpowers
The Pi package loads the Superpowers skills and a small extension that injects the using-superpowers bootstrap at session startup and again after compaction. Pi has native skills, so no compatibility Skill tool is required. Subagent and task-list tools remain optional Pi companion packages.
Install Superpowers as a Hermes plugin from this repository:
hermes plugins install obra/superpowers --enable
Restart any active Hermes sessions after installing. Note: Hermes has no post-compaction hook, so a very long session that compacts over its first turn loses the bootstrap — start a fresh session if skills stop triggering.
- 
brainstorming - Activates before writing code. Refines rough ideas through questions, explores alternatives, presents design in sections for validation. Saves design document.
- 
using-git-worktrees - Activates after design approval. Creates isolated workspace on new branch, runs project setup, verifies clean test baseline.
- 
writing-plans - Activates with approved design. Breaks work into bite-sized tasks (2-5 minutes each). Every task has exact file paths, complete code, verification steps.
- 
subagent-driven-development or executing-plans - Activates with plan. Dispatches fresh subagent per task with two-stage review (spec compliance, then code quality), or executes in batches with human checkpoints.
- 
test-driven-development - Activates during implementation. Enforces RED-GREEN-REFACTOR: write failing test, watch it fail, write minimal code, watch it pass, commit. Deletes code written before tests.
- 
requesting-code-review - Activates between tasks. Reviews against plan, reports issues by severity. Critical issues block progress.
- 
finishing-a-development-branch - Activates when tasks complete. Verifies tests, presents options (merge/PR/keep/discard), cleans up worktree.
The agent checks for relevant skills before any task. Mandatory workflows, not suggestions.
Superpowers is built by Jesse Vincent and the rest of the folks at Prime Radiant.
- Discord: Join us for community support, questions, and sharing what you're building with Superpowers
- Issues: https://github.com/obra/superpowers/issues
- Release announcements: Sign up to get notified about new versions
Testing
- test-driven-development - RED-GREEN-REFACTOR cycle (includes testing anti-patterns reference)
Debugging
- systematic-debugging - 4-phase root cause process (includes root-cause-tracing, defense-in-depth, condition-based-waiting techniques)
- verification-before-completion - Ensure it's actually fixed
Collaboration
- brainstorming - Socratic design refinement
- writing-plans - Detailed implementation plans
- executing-plans - Batch execution with checkpoints
- dispatching-parallel-agents - Concurrent subagent workflows
- requesting-code-review - Pre-review checklist
- receiving-code-review - Responding to feedback
- using-git-worktrees - Parallel development branches
- finishing-a-development-branch - Merge/PR decision workflow
- subagent-driven-development - Fast iteration with two-stage review (spec compliance, then code quality)
Meta
- writing-skills - Create new skills following best practices (includes testing methodology)
- using-superpowers - Introduction to the skills system
- Test-Driven Development - Write tests first, always
- Systematic over ad-hoc - Process over guessing
- Complexity reduction - Simplicity as primary goal
- Evidence over claims - Verify before declaring success
Read the original release announcement.
The general contribution process for Superpowers is below. Keep in mind that we don't generally accept contributions of new skills and that any updates to skills must work across all of the coding agents we support.
- Fork the repository
- Switch to the 'dev' branch
- Create a branch for your work
- Follow the writing-skills skill for creating and testing new and modified skills
- Submit a PR, being sure to fill in the pull request template.
Skill-behavior tests use the drill eval harness from superpowers-evals, cloned into evals/ — see evals/README.md for setup. Plugin-infrastructure tests live at tests/ and run via the relevant run-*.sh or npm test.
See skills/writing-skills/SKILL.md for the complete guide.
Superpowers updates are somewhat coding-agent dependent, but are often automatic.
MIT License - see LICENSE file for details
Because skills and plugins don't provide any feedback to creators, we have no idea how many of you are using Superpowers. By default, the Prime Radiant logo on brainstorming's optional visual companion feature is loaded from our website. It includes the version of Superpowers in use. It does not include any details about your project, prompt, or coding agent. We don't see your clicks or anything about what you're building. This helps us have a rough idea of how many folks are using Superpowers and which version of Superpowers they're using. It's 100% optional. To disable this, set the environment variable SUPERPOWERS_DISABLE_TELEMETRY to any true value. Superpowers also honors Claude Code's DISABLE_TELEMETRY and CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC opt-outs.
