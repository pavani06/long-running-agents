---
url: "https://code.claude.com/docs/en/plugin-evals"
key: "87bac08c42f2"
status: "ok"
final_url: "https://code.claude.com/docs/en/plugin-evals"
method: "trafilatura"
content_hash: "38201a257a70a23ffc11f979870a45e20d8148cc"
text_len: 32929
fetched: "2026-09-13"
---

claude plugin eval runs your plugin against a suite of test cases and scores the results. Each case is a realistic prompt plus one or more graders. A grader is a pass/fail check on what Claude produced, such as a regex over the reply, whether a particular tool was called, or a rubric that a second model judges the reply against.
You don’t have to write the suite manually. claude plugin eval init asks you about your plugin, proposes the cases and graders, tries them, and writes the files. You can also ask Claude to do the same from a session you already have open.
Use evals to measure how reliably your plugin steers Claude to the right outcome, to catch regressions when you change the plugin or a new model ships, and to see what the plugin contributes compared with no plugin at all.
This page is for plugin and skill authors who have a working plugin and want to test its behavior, and for teams that gate plugin changes in CI. Its case format is separate from the evals/evals.json file the skill-creator plugin uses. To create a plugin, see Create plugins; to check a plugin’s files for syntax and schema errors rather than its behavior, use claude plugin validate.
Every eval run and every judge grader is a real model call on your account, counted against your plan’s usage or your API bill, so check the requirements first. Then create your first eval suite, or go to Run evals in CI if you already have one.
Requirements
To run plugin evals you need:
- Claude Code v2.1.269 or later. Run claude --version to check andclaude update to upgrade.
- A plugin directory with a plugin.json or.claude-plugin/plugin.json manifest, or a skills-directory plugin.
- The same authentication and model provider your normal Claude Code sessions use. Eval runs, judge-scored graders, and claude plugin eval init call the model with your credentials, so they count against your plan’s usage limits or your API bill. When the command reports a cost, the figure is a list-price estimate of those calls.
How an eval run works
An eval suite lives in a directory calledevals/ inside your plugin, laid out as Write and refine cases shows. Each case is its own subdirectory with a prompt and one or more graders. The prompt is something a person using your plugin might type, such as a request one of its skills should handle.
What happens in a run
For each run of a case, Claude Code starts a fresh, isolated non-interactive session with only your plugin loaded, sends the prompt, and lets Claude work until it finishes or hits the case’s turn or time limit. Each grader then checks the final reply, the transcript, or a file Claude created, and passes or fails.
How a case is scored
One run of a non-deterministic agent tells you little, so each case runs three times by default. A run’s score is the fraction of its graders that passed, weighted if you set weights, and the case’s score is the mean across its runs. A case passes when its score meets the--threshold, 1.0 by default. In model calls, a suite makes roughly cases × runs agent runs with the plugin and as many again for the no-plugin baseline, plus three short judge calls per llm or baseline grader per run.
The no-plugin baseline
A high score on its own doesn’t tell you the plugin helped, because Claude might do as well without it. To separate the two, each case’s runs are repeated with no plugin loaded by default, and you get two scores,WITH and W/OUT. Their difference, Δ, is what the plugin contributed. If a case scores 1.0 both with and without the plugin, the plugin isn’t what made it pass. The two sets of runs are called the with-arm and the without-arm; Compare against a no-plugin baseline covers how graders are scored across them and how to turn the baseline off.
Create your first eval suite
This walkthrough writes one case for your own plugin, runs it, and reads the result. Before you start, make sure you have:
- Claude Code v2.1.269 or later and the other requirements
- A terminal open at your plugin’s root directory, the one containing plugin.json or.claude-plugin/plugin.json
- One skill in the plugin you want to test, and a request a user would type that should trigger it
1
Create the cases
From the plugin root, run:If Claude Code doesn’t already trust this directory it first asks 
Trust this plugin directory?; answer y. An interactive Claude Code session then opens. Claude reads your plugin and asks you what a good result looks like, proposes prompts that should and shouldn’t trigger the plugin, designs graders for each, pilots them once to check they behave, and writes one case directory per prompt under evals/, each named after its prompt. When Claude tells you the suite is ready, exit that session with /exit or Ctrl+D to return to your shell.If you already have a Claude Code session open at the plugin root, you can instead ask Claude there to run claude plugin eval init. Claude runs the command and then asks you the same questions in that conversation.If you’d rather write a case yourself to see exactly what the files contain, follow Write a case manually and come back here to run it.
2
Run the suite
Back at your shell in the plugin root, run every case under You already trusted this directory during step 1, so the run starts immediately. If you wrote the case manually instead, the run first asks 
evals/:Trust this plugin directory? [y/N]; answer y. What a run can access explains what you’re agreeing to.Each case runs three times with your plugin and three times without it, so one case is six runs. A progress line prints as each run finishes, with that run’s score and each grader’s verdict.
3
Read the summary
When the suite finishes you see a summary table, followed by where the report went:
WITH is the case’s score with your plugin loaded, W/OUT is the score without it, and a positive Δ means the plugin raised the score. COST is a list-price estimate of the model calls, and NOTES shows the highest-weight failing grader’s explanation, or the run’s error, from the with-arm.
4
Open the report and iterate
Open the Replace 
Published: URL, or the Report: path when no Published: line appears, to see each grader’s verdict and explanation for every run, and for llm graders the judge’s votes and the excerpt it judged. The Published: line appears only when your account can publish reports.The most common first finding is a Δ near zero with the case’s tool_used: Skill grader failing, which means Claude isn’t choosing your skill on natural phrasing. Adjust the skill’s description, run claude plugin eval . again, and compare.To iterate on one case cheaply, run a single arm once. A single run is noisy, so confirm any change at the default three runs before you trust it. With one arm the table shows SCORE and PASS% columns instead of WITH, W/OUT, and Δ:<case-name> with one of the directory names under evals/.
Write and refine cases
The casesclaude plugin eval init writes are plain files you can open, change, and add to. A case is a directory under the plugin’s eval directory that contains a prompt.md, a case.yaml, or both. To group cases, nest them under a directory that isn’t itself a case; anything inside a case directory, such as graders/ and fixture files, belongs to that case.
This is the layout claude plugin eval init writes and the one to use for new suites. The eval suite reference has the complete tree, including mocks and results:
Write a case manually
Having Claude write the cases withclaude plugin eval init is the recommended path. To write one yourself instead, start from a blank template. The following command writes a case named first-case with a placeholder prompt.md and one placeholder grader, and runs nothing:
prompt.md you write the message Claude receives in each run, and set the run’s limits and the tools the case may use in its frontmatter. Open evals/first-case/prompt.md and replace the placeholder body with a request one of your skills should handle, phrased the way a user would type it rather than naming the skill. This example is for a skill that drafts commit messages; use your own request:
graders/ is one check applied after the run. Open evals/first-case/graders/criteria.md and replace the placeholder with a rubric for the judge model, written as concrete PASS and FAIL conditions:
evals/first-case/graders/skill-fired.md, replacing your-skill-name with the name from your skill’s SKILL.md:
plugin-name:skill-name form. Grader types lists the other checks available, such as matching a regex or confirming a file was created.
With both files saved, run the case the way the quickstart does, with claude plugin eval . from the plugin root.
Set run limits and tools in prompt.md
Set a case’smax_turns, timeout_seconds, model, tags, and the allowed_tools it may use in prompt.md frontmatter; the prompt.md frontmatter reference lists every field and its default. Claude receives the body exactly as you wrote it. @path mentions in it aren’t expanded into file attachments, so if Claude needs to read a file, grant a tool for it in allowed_tools.
Choose and weight graders
A grader’s frontmatter sets itstype, and optionally a weight that makes it count for more of the run’s score and an arm that controls how it’s scored against the baseline. Of the six types, regex, tool_used, tool_order, and file_exists are computed from the transcript and files and cost nothing, while llm and baseline call a judge model and add to the run’s cost.
There are no custom-code graders. Grader types lists each type’s options and pass condition, and what a grader can look at lists the values target and focus accept.
The judge for llm and baseline graders is a small fast model by default. Pass --judge-model sonnet or a full model ID to use a stronger one for nuanced rubrics.
Choose graders that give a stable signal
Anllm grader asks a model for a verdict, so its answer can differ between runs, and it differs more the longer the text it has to read. These habits keep a suite’s scores steady enough to trust:
- For long output such as a generated file, grade it with a regex grader over the file’s contents, which checks the whole file the same way every time. Keepllm graders for short outputs, with rubrics written as concrete PASS and FAIL conditions.
- Give each case one grader on the result, such as the final message or a produced file, and one on how Claude got there, such as tool_used ortool_order . Together they tell you both whether the answer was right and whether your plugin produced it.
- If a case’s tool_used: Skill grader passes butΔ is negative, suspect the judge before the plugin. A small judge model can mark a correct answer wrong because it’s formatted differently from what the rubric describes. Re-run with--judge-model sonnet , and tighten the rubric so formatting doesn’t decide the verdict.
- To check that a build or test passed inside the run, have the prompt ask Claude to run it and write the outcome to a file, grade that file, and assert the command ran with a tool_used grader whoseinput_match names the command.
Score against the no-plugin baseline
When a plugin is under test, each case runs in two arms by default. The with-arm is its runs with the plugin loaded, and the without-arm is the same number of runs with no plugin at all. The summary and report show both scores andΔ, the with-arm score minus the without-arm score. Pass --ablation none to run only the with-arm, which halves the cost when you don’t need the comparison, such as while iterating on graders.
In a two-arm run, some graders are reported with scored: false. A check like “the skill was invoked” can never pass without the plugin, so counting it would push the without-arm toward zero and inflate Δ. To keep the two arms comparable, Claude Code excludes such graders from the score in both arms and reports them in the with-arm as pass/fail indicators only. That includes:
- Every tool_used grader whosetool isSkill
- Any grader you mark arm: with-only
arm: both on a grader to score it in both arms regardless, which is what you want for a “must not invoke the skill” check with min: 0 and max: 0. Under --ablation none nothing is excluded, so the same suite can produce a different absolute score in the two modes.
Use a different eval directory
Ifevals/ is already taken by another tool, keep the suite in a different directory. You can record that directory in the plugin’s plugin.json so every run and every collaborator uses it, or pass it on the command line for a single run:
- In plugin.json : add"experimental": { "evals": "quality/evals" } .
- On the command line: pass --eval-dir quality/evals to bothclaude plugin eval andclaude plugin eval init .
qa or quality/evals. An absolute path or one containing .. isn’t accepted: as a flag value it’s an error, while an unusable manifest value prints a Warning: line and the run uses evals/ instead. Cases, results, and init output all move to that directory.
Set up fixtures and mocks
A case can need more than a prompt: files or a git repository in the workspace, an earlier conversation to continue, or answers from the MCP servers your plugin talks to. Each of those is set up beside the case so runs stay repeatable.
Seed the workspace or conversation
Each run starts in an empty workspace. When a case needs more than the prompt, add acase.yaml beside prompt.md with a context block.
To create fixture files or a git repository first, write a Bash script in the case directory and name it in context.scaffold_script. The script runs as you, outside the agent’s sandbox, and only when you pass --scaffold, so pass that flag only for suites you or your organization wrote. To continue an earlier conversation, save the transcript as a .jsonl file and name it in context.history_file, and the case’s prompt becomes the next user turn. To let Claude read fixture directories in the case during the run, list them in context.add_dirs.
A case.yaml also needs schema_version: "1.1" and name; the case.yaml fields reference has the full list.
This case.yaml seeds a workspace from a script and lets Claude read fixtures from a resources/ directory:
Mock MCP servers
You can evaluate a plugin whose skills call MCP tools without the real service behind them. Put one Markdown file per tool underevals/mocks/<server>/<tool>.md for the whole suite, or under a case’s own mocks/ directory for one case, where <server> is the server’s name in your plugin’s MCP configuration.
A run never starts your plugin’s real MCP servers unless you ask. Claude Code registers a stand-in under each server’s own name. Tools with a mock file answer from it and are allowed without an --allow-tools grant, and a tool with no mock file isn’t available to Claude. A server with no mocks at all appears in the case’s mocked: progress line as plugin_<plugin>_<server>[not started: no mock].
The file’s body is what the tool returns to Claude. This mock stands in for a create_issue tool on a server named tracker, checks the input Claude sends, and echoes the title back. Save it as evals/mocks/tracker/create_issue.md:
{{input.<field>}}, and the contents of a fixture file beside the mock with {{file:fixtures/{input.<field>}.json}}. The expect: block guards the input. If a call violates it, the run aborts with score 0 and records why, so a case can assert what your plugin asked the server to do. Set error: true to return the body as a tool error instead, or type: agent to have a small model answer as the server from instructions in the body. The mock file reference lists every key and the _server.md and _tools.json files.
To grade the calls themselves, point a grader at target: mock_calls.
To run against the plugin’s real MCP servers instead, pass one of these flags. Either way those processes run as you, outside the run’s sandbox, and their tools need an --allow-tools grant:
- --allow-real-servers : start the real process for each server you haven’t mocked, and keep answering mocked tools from their files
- --mocks off : ignoremocks/ entirely and start every server the plugin declares
Replay agent mock answers
Atype: agent mock answers with a call to the --judge-model, so its output varies between runs and changes if you change the judge. When a run completes without an error or abort, Claude Code saves each answer an agent mock gave under the results directory in mock-recordings/.
Open ADOPT.txt there to see each recording and the .replay/<server>/ directory to copy it into, beside the mock that produced it. After you copy a recording there, later runs answer the identical call from it with no model call. Commit mocks/.replay/ with the rest of mocks/ so CI runs are repeatable.
Run evals
Once a suite exists,claude plugin eval runs it. You choose which plugin and cases run with the target argument, grant any tools the cases need beyond the read-only set with --allow-tools, and control run count, models, cost, and output with the other options.
Choose what to evaluate
Most of the time you runclaude plugin eval . from the plugin root, which runs every case in the suite with the plugin you’re standing in loaded. To run a single case file, or to evaluate a plugin you installed rather than one you’re developing, pass a different target:
Add 
--case <glob> to filter by case name and --tag <tag> to keep cases with any of the given tags. Put the target before --tag, --allow-tools, and --json. The first two take a list and --json takes an optional path, so each of them reads a target that follows as its own value.
Grant tools
Runs never stop to ask for permission. Built-in tools that need a grant you didn’t give, such asBash, Write, Edit, WebFetch, and WebSearch, are removed from the session, so Claude can’t call them at all. The allowlist is the read-only tools the case lists in allowed_tools, from Read, Glob, Grep, NotebookRead, Skill, Agent, TodoWrite, and the task tools TaskCreate, TaskGet, TaskList, TaskUpdate, TaskStop, and TaskOutput, plus whatever you grant with --allow-tools, which applies to every case in the run. To let cases use Bash, Write, Edit, WebFetch, or WebSearch, grant them yourself:
not granted. Tools on a mocked MCP server need no grant. Tools on a real plugin MCP server need both the server started, with --allow-real-servers or --mocks off, and a grant by name, such as --allow-tools "mcp__plugin_my-plugin_github__*"; a plugin’s MCP tools are named mcp__plugin_<plugin>_<server>__<tool>.
When you grant Bash in any form, every command runs under Claude Code’s OS-level sandbox. Writes are confined to the run’s workspace, your home directory and Claude Code configuration are unreadable, and network access is limited to domains you grant with --allow-tools "WebFetch(domain:example.com)". If you grant Bash or PowerShell on a machine with no sandbox backend, Claude Code refuses each run rather than running it unconfined, and the case shows a run error and usually scores 0. Native Windows has no backend, so run shell-granting suites under WSL2; on Linux, install bubblewrap and socat first. See the sandboxing prerequisites.
Command options
This table covers the options for run count, models, scoring, cost, tool grants, mocks, and output. Runclaude plugin eval --help for the complete list, which also includes --case, --tag, --eval-dir, --no-scaffold, --report, and --verbose.
Run evals in CI
In your CI job, run the suite with--json to write the result for archiving, and fail the build on the exit code. Pass --trust-plugin so the job never waits at the first-run trust prompt, pin both models so scores are comparable over time, keep the report local, and set a cost ceiling as an upper limit:
Problems writing or publishing the HTML report never change the exit code. To see why a case scored low, run it locally without 
--json so the per-run progress and grader lines print.
A CI runner needs a Claude Code install and credentials in the environment such as ANTHROPIC_API_KEY. Without --trust-plugin, a job whose checkout directory Claude Code doesn’t already trust is refused with exit 1 when it has no terminal, or waits at the prompt when the runner allocates one. claude plugin eval init needs a terminal to ask you its questions; in CI, run claude plugin eval init --bare <name> to get the blank template.
To keep costs predictable, give quick every-change suites only graders that don’t call a judge, use --ablation none where you don’t need Δ, and leave partial: true documents and runs with skippedPaidGraders out of any trend you chart.
Read the results
Every run with at least one case writes aresults/<timestamp>/ directory inside the eval directory, containing aggregate-result.json and report.html. For a path target that’s under the plugin; for a plugin you named, it’s under your current directory, as the target table shows. The summary table, the JSON, and the report all render the same result data.
HTML report
report.html is a single self-contained file that makes no external requests, so you can attach it to a CI job or open it from disk. This example is the top of a report for a three-case suite run with --threshold 0.8; the cost shown is a list-price estimate and varies with the model and the number of cases:
Read it from the top down:
- The verdict line and tiles answer whether the plugin helped across the whole suite. Suite score is the mean of the per-case with-plugin scores, Ablation Δ is how far that sits above or below the baseline score, and Cases counts how many met the threshold. Perfect runs is the share of with-plugin runs where every grader passed.
- Each case card shows the case’s own Δ and with-plugin score, with a tick on the bar at the threshold. A case whoseΔ is negative gets a red left edge, so regressions stand out when you scroll.
- Inside a case, the with-plugin runs come first and the baseline runs after. Each run lists its graders with a pass or fail chip. A failed grader is already expanded with its explanation, and an llm grader also shows the judge’s votes and the evidence it was shown, which is where you find out why a run scored low. Graders that don’t count toward the score, such astool_used: Skill , carry aplugin-fired indicator badge.
- Prompt and Graders, below the runs, show the case’s prompt and each grader’s rubric or pattern, so someone reading the report without the suite can see what was asked and what counted as good.
Published: <url>. Pass --no-publish to keep it local. If no Published: line appears, such as with API-key authentication, the local file is the report.
A run that a Claude Code session started, such as when you ask Claude to run the suite for you, also stays local, and its Report: line says kept local. Add --publish-report to that command to publish it.
JSON result
aggregate-result.json, and --json output, is a versioned document with schemaVersion: 1 for CI scripts to parse. Field names are camelCase and new fields are added without renaming existing ones, so write your script to ignore fields it doesn’t recognize.
These are the fields a gating script usually reads. The document also carries the suite configuration, every grader definition, and per-run grader results with explanations and evidence:
What a run can access
claude plugin eval loads the target plugin’s skills and hooks and runs its eval suite on your machine, as you. Pointing it at a plugin is the same trust decision as claude --plugin-dir, so only evaluate plugins you trust. The isolation described in this section limits what the agent under test can reach; it isn’t a boundary against the plugin’s own code, and a suite that passes says nothing about whether the plugin is safe.
Trust the plugin directory
The first time you runclaude plugin eval against a directory, Claude Code asks Trust this plugin directory? before it loads anything from it, unless you already accepted the trust prompt there in an interactive claude session. Inside a git repository, answering yes trusts the whole repository, for interactive sessions too. When stdin or stdout isn’t a terminal, or under --json, the run can’t ask and is refused with exit 1; pass --trust-plugin to assert the trust yourself, only for a plugin you’d run on your own machine. A target you name rather than give as a path, meaning an installed plugin or a skills-directory plugin, skips the prompt.
Some parts of the plugin and suite run only when you pass their flag for that run: a case’s scaffold_script with --scaffold, tools beyond the read-only set with --allow-tools, and the plugin’s real MCP servers with --allow-real-servers or --mocks off. A case’s allowed_tools and a skill’s own allowed-tools frontmatter can’t widen any of them. When the plugin ships hooks you didn’t write, or you start its real MCP servers, treat its scores as advisory unless you ran it in an isolated environment such as a container or CI runner, since hooks and servers run outside the agent’s sandbox and could touch the files the graders read.
How runs are isolated
Each run gets a throwaway home directory, working directory, and Claude Code configuration, and the agent under test runs there as aclaude -p child process with only your plugin loaded. Keep these consequences in mind when you write cases:
- Nothing personal or project-level loads. Your user settings, hooks, CLAUDE.md files, MCP servers, other installed plugins, memory, and skills are absent, and no project-scoped.claude/ or.mcp.json above the sandbox is read. Most of your shell environment is withheld too; only an allowlist andEVAL_* variables reach the run. If the plugin needs setup, ship it in the plugin, create it in ascaffold_script , or passEVAL_* variables.
- Managed policy can still restrict a run. Restrictions in managed settings an administrator deployed to the machine apply inside a run, so results on a managed machine can differ from an unmanaged one by that policy.
- The Artifact tool is off. A skill that publishes an artifact can be graded only on what it produces before that step.
- The case definitions are hidden from the agent. A run can’t read the eval directory, so Claude can’t see the case’s prompt, its graders, or sibling cases.
- No network sandbox outside shell commands. Shell commands you grant run under the sandbox’s network rules. A WebFetch(domain:…) grant reaches that domain directly, and the plugin’s own hooks and any real MCP servers you start can reach any host.
Eval suite reference
Everything an eval suite can contain lives under the plugin’s eval directory,evals/ unless you configured another. This tree shows every file claude plugin eval reads or writes there; only prompt.md or case.yaml is required for a case to exist:
prompt.md frontmatter
prompt.md frontmatter accepts these fields. An unknown key is an error:
case.yaml fields
case.yaml describes the same case in YAML and adds the fields that point at other files. It requires schema_version: "1.1" and name. The prompt.md fields description, tags, plugins, runs, and expected_outcome go at the top level; model, max_turns, timeout_seconds, allowed_tools, append_system_prompt, and env go under execution:. When both files exist, prompt.md frontmatter overrides the matching case.yaml fields, the prompt.md body is the prompt, and graders/*.md are added after any graders listed in case.yaml.
These fields exist only in case.yaml:
Grader frontmatter
Every grader file undergraders/ takes these keys in frontmatter, plus the options for its type. The grader’s name is the filename without .md:
What a grader can look at
regex graders take a target and llm graders take a focus. Both accept the same values:
Grader types
Each grader type below lists its options and when it passes:
Mock files
A<tool>.md file under mocks/<server>/ answers one tool. Its body is the tool result, with {{input.<field>}} and {{file:fixtures/<name>}} substitutions. Its frontmatter accepts these keys:
Two optional files sit beside the tool files in a server’s directory:
- _server.md : a singletype: agent mock that answers several tools, listed in itstools: frontmatter key. A<tool>.md for the same tool takes precedence. Put anexpect: guard on the individual<tool>.md , not here
- _tools.json : a savedtools/list response from the real server, so mocked tools carry their real descriptions and input schemas instead of a permissive placeholder
mocks/ directory uses the same layout and overrides the suite’s mocks file by file.
Troubleshooting
These are the problems authors hit most often, keyed on what you see.
”plugin eval is currently in early access”
Your build predates general availability of the command. Runclaude update, then run the command again in a fresh session.
”plugin eval is currently unavailable”
Anthropic has switched the command off server-side. Nothing on your machine turns it back on; runclaude update and try again in a fresh session later.
”is not a trusted plugin directory, and this run cannot stop to ask you about it”
This is the first run against a directory Claude Code doesn’t trust yet, and it can’t ask you because stdin or stdout isn’t a terminal or you passed--json. Run claude plugin eval <dir> once in a terminal and answer the prompt, or pass --trust-plugin if you trust the plugin’s code and suite. See What a run can access.
”No eval cases found”
No<case>/prompt.md or <case>/case.yaml exists beneath the eval directory in effect, or your --case and --tag filters matched no case. Run from the plugin root, or run claude plugin eval init to create a suite.
The baseline arm shows no plugin, or delta is zero
If the summary has noW/OUT column, or the case fails with “ablation requested but no plugin resolved”, no plugin was found for the case. Add plugins: ["../.."] to the case, giving the path from the case directory to the plugin directory.
If the plugin did load and Δ is still near zero with your tool_used: Skill grader failing, that’s usually a real finding, meaning the skill’s description doesn’t trigger on the prompt’s phrasing. Adjust the description and re-run the same suite.
Everything scores zero although the right files were produced
Your graders targetfiles, the list of created paths, when you meant the file’s contents. Use { source: file, path: <path> } as the target or focus. Separately, file_exists counts only files created during the run, so a file the scaffold created or that Claude only edited is invisible to it; grade its contents, or use tool_used on Edit.
A regex over the trace doesn’t match text I can see
The defaulttarget is last_message, not the trace. When you do target trace, it’s JSON per line, so quotes appear as \". Regexes use JavaScript syntax, so put i in flags rather than writing (?i).
Tools are denied, MCP tools are missing, or Bash won’t run
Anything beyond the read-only set needs your grant, such as--allow-tools Bash Write. Your personal MCP servers never load in a run. The plugin’s own servers don’t start unless you opt in, and their tools then also need an --allow-tools "mcp__plugin_<plugin>_<server>__*" grant; a mocked tool needs neither.
The run exits 1 but the results look fine
The default--threshold is 1.0, so the command exits 1 when any case scores below perfect. Set a threshold that matches your bar. Exit 1 also covers a case file that failed to load, which is reported on stderr above the table.
”—json output path must end in .json”
You put the target after--json, so it was read as the output path. Put the target first, as in claude plugin eval . --json, or give --json an explicit .json path.
A grader shows passed: false under a run that scored 1.0
That grader is excluded from the score by design in a two-arm run, and itsscored field is false. See Compare against a no-plugin baseline.
Runs fail with a usage-limit or rate-limit error partway through
If your account reaches its plan’s usage limit or an API rate limit while a suite is running, each later run ends with that error, is graded on what it produced, and usually scores 0. The suite still finishes and isn’t markedpartial, so the result can look like a regression. Check the NOTES column or cases[].arms.with[].error in the JSON for the limit message before trusting the scores, then re-run after the limit resets, with --runs 1 or a --case filter if you need to stay under it.
Runs time out or hit the turn cap
The defaults are 10 turns and 300 seconds. Raisemax_turns and timeout_seconds in the case for tasks that need more, and use --max-cost-usd as the cost ceiling rather than tight per-run limits.
See also
- Create plugins: build the plugin you’re testing, and load it with --plugin-dir during development
- Plugins reference: the plugin eval andplugin eval init command entries and the manifest’sexperimental.evals key
- Skills: how a skill’s description decides when Claude invokes it, which is what a case that checks whether the skill triggers is measuring
- Sandboxing: the OS-level sandbox that applies when you grant Bash to a run
- Create and distribute a plugin marketplace: publish the plugin once its suite passes
