---
url: "https://github.com/anthropics/claude-code/tree/main/mods/agents-md"
key: "87de4bcdb293"
status: "ok"
final_url: "https://github.com/anthropics/claude-code/tree/main/mods/agents-md"
method: "trafilatura"
content_hash: "9dd58432bf3444d939e72432b5a636c93b0bab64"
text_len: 11488
fetched: "2026-09-19"
---

AGENTS.md read the way Claude Code reads CLAUDE.md, as a plugin, under
one option, instructionFiles:
- claude-md : onlyCLAUDE.md is loaded, by the engine, as today. The plugin
adds nothing.
- claude-md-or-agents-md (the default): a project with no instruction files
of its own gets itsAGENTS.md files instead, loaded exactly where and howCLAUDE.md would be. "Of its own" is read off what the engine loaded for
the context: aCLAUDE.md ,.claude/CLAUDE.md orCLAUDE.local.md in any
directory from the root down to the working directory leaves the whole
project to the engine, and the plugin stays out (the organization's managed
file, the person's~/.claude/CLAUDE.md , a.claude/rules file and an
added directory'sCLAUDE.md do not count, as the nested walk does not see
them either). With none, everyAGENTS.md and.claude/AGENTS.md on that
path joins the instruction files the engine renders, and aRead under a
subdirectory attaches that directory'sAGENTS.md unless aCLAUDE.md there claims it.
- claude-md-and-agents-md : everyAGENTS.md is loaded besideCLAUDE.md ,
up and down the tree; a fileCLAUDE.md already@ -imports, or is a link
to, is not loaded a second time (compared by path, then by content).
- managed-only : the project's checked-in and private instruction files and
the person's own are dropped from the context; the organization's managedCLAUDE.md and the engine's memory stay. The engine's nestedCLAUDE.md attachments onRead are not an event yet and still arrive. (The engine'sclaudeMdExcludes setting also exists, for user, project and local files,
and applies to theAGENTS.md files this plugin reads too.)
How the files reach the model is the engine's doing, not the plugin's:
prompt.context hands a hook the instruction files behind claudeMd
({ path, kind, content, parent? }, kinds managed, user, project,
local, memory, in load order) and a hook answers the list changed. The
engine then renders claudeMd from the answered files with its own preamble
and framing, announces them by name, and keeps only the managed ones for an
agent that omits project instructions (Explore, Plan, a custom agent with
omitClaudeMd). So an AGENTS.md this plugin adds as a project file is, to
everything downstream, a project instruction file: same place in the context,
same framing, same omission rules, same announcement. An organization's
prepended plugin on prompt.context sits above this one and has the last
word on the files.
hooks/register.ts is the module; everything under hooks/ is its parts,
importing claude-code and one another alone. tests/ runs under
claude plugin test <this folder>.
As a built-in its option is the /config row "Project instructions", a
picker over the four values, each described there. By hand it is
{
  "pluginConfigs": {
    "agents-md@builtin": {
      "options": { "instructionFiles": "claude-md-and-agents-md" }
    }
  }
}
in user settings (~/.claude/settings.json), --settings, or managed
settings; a project's .claude/settings.json is not read for plugin
options. Changing it reloads the module, and the next context the engine
builds (the next turn after the reload, a new conversation, /clear, a
compaction) carries the new mode's files. A hand-typed value outside the
four is told once in the transcript and reads as the default. /plugin
lists the plugin among the built-ins, where a person can turn it off; with
it off the engine reads CLAUDE.md alone. No hooks setting or CLI mode turns
it off (disableAllHooks, allowManagedHooksOnly and --bare govern
settings hooks and installed plugins, not built-ins); where the engine loads
no instruction files (--bare without --add-dir, --safe-mode,
CLAUDE_CODE_DISABLE_CLAUDE_MDS) its walk finds none and it adds none,
CLAUDE.md and AGENTS.md alike.
The option was first keyed projectInstructions, with the values claude,
agents-fallback, both and none. A value still stored under that key is
honoured for now while instructionFiles reads as its default: none as
managed-only, claude as claude-md, agents-fallback as
claude-md-or-agents-md, both as claude-md-and-agents-md, any other
value as claude-md (which adds nothing, never as the default, which loads
AGENTS.md); the first session.start of a load says in the transcript how
it was read. Once instructionFiles is set to anything but its default, the
old key is not read and the transcript says to remove it.
Run from this folder instead (claude --plugin-dir mods/agents-md), the
same entry is keyed "agents-md".
| event | what the hook does | 
|---|---|
| session.start | in every mode: passes the start straight through and floats the usage row for the configured mode, never awaited; the first start of a load logs how a stored projectInstructions value is read. The session's start never waits on this plugin | 
| prompt.context | under claude-md-or-agents-md andclaude-md-and-agents-md : walks$.fs.ancestors for theAGENTS.md files above the working directory and answers them asproject instruction files, each@ import its own entry after its file, each placed where a project file of its directory stands (root first, before the first deeper project file, else after the last project file, before memory); files the engine already holds by path or by content are left out; underclaude-md-or-agents-md it answers nothing when the project has aCLAUDE.md of its own (among the handed files, else found by a$.fs.ancestors walk, so aCLAUDE.md the engine loaded and then withheld still counts), and logs which files it loaded once, and again after a move to another project root; handed unknown files (a hook above rewrote theclaudeMd text) it adds nothing; the first context of a load sends the load row (counts) and the feature mark; undermanaged-only (matcher: aproject ,local oruser file present): answers the list without those kinds | 
| agent.spawn onfork: true | under claude-md-or-agents-md andclaude-md-and-agents-md : a fork the Agent tool starts shares its parent's prompt prefix, so the parent loop's delivered nested files are copied to the fork's loop and not attached to it again (a/fork or/subtask fork does not raiseagent.spawn yet and starts from an empty set, as every fork did before; a fork started in the same tool batch as aRead inherits that Read's file although its prefix holds a placeholder for it) | 
| tool.call onRead | under claude-md-or-agents-md andclaude-md-and-agents-md , for a file under the session's project root ($.session.root() , read live, so/cd , a host's directory change and worktree moves are followed and a moved root starts the delivered sets and the fallback decision over; a file elsewhere gets nothing, as the engine attaches no nestedCLAUDE.md there; and nothing anywhere in a run where the engine attaches nothing to a turn,--bare with itsCLAUDE_CODE_SIMPLE orCLAUDE_CODE_DISABLE_ATTACHMENTS , read on every Read through$.env.get as the engine reads them on every turn): walks only the directories strictly between the root and the read file ($.fs.ancestors withbelow: root , as the engine walks only those for a nestedCLAUDE.md , never up to the filesystem root again) and attaches theirAGENTS.md files not yet given to that agent loop, not already among the context's instruction files (by path or, for a project file, by text) and not claimed by aCLAUDE.md of the same directory (or imported by one), ascontext after the tool result, framedContents of <path>: byte for byte as the engine frames a nestedCLAUDE.md , whatever its size; each file once per loop and conversation (the context's recomputation after a compaction or/clear starts the count over), the context's files never; a Read that attached files sends the nested row. A~ or~/ path is read under the home directory as the Read tool reads it | 
fs.ancestors (with each found file's parts: the file and its imports
apart; with below on a Read; it finds nothing on a thin client, whose
workspace files are remote, as the engine's own walk does), session.root,
session.cwd, env.get (HOME and USERPROFILE, once per load, the
profile first on a Windows spelling of the working directory, so a ~/ path
the model hands a Read resolves where the Read tool reads it; CLAUDE_CODE_SIMPLE
and CLAUDE_CODE_DISABLE_ATTACHMENTS on every Read), ui.log,
telemetry.log and telemetry.mark.
$.telemetry is the telemetry plugin's noun; where that
plugin is not seated the calls find no noun and are dropped without a trace,
and nothing else changes.
Counts and closed choices only; no path and no file text. Each row goes
through $.telemetry.log, so it exists only where the telemetry plugin
does:
| event | when | properties | 
|---|---|---|
| agents_md_mode | once per fresh load, at session.start | mode (claude-md \|claude-md-or-agents-md \|claude-md-and-agents-md \|managed-only ),is_interactive | 
| agents_md_load | the first context of a load, under claude-md-or-agents-md andclaude-md-and-agents-md | mode ,file_count (AGENTS.md files handed to the engine),import_count (their@ imports),total_content_length ,yielded (claude-md-or-agents-md stood down for aCLAUDE.md of the project's own),walk_failed ; with it one$.telemetry.mark for featureagents_md :ok , orsad with reasonwalk_failed | 
| agents_md_nested | a Read that attached nested files | mode ,file_count | 
All of these apply only to the modes that load AGENTS.md,
claude-md-or-agents-md (the default) and claude-md-and-agents-md. Each
names a loader fact a plugin cannot reach through the events it has today.
- Nested files attach on a text Read only. The engine also attaches a
directory'sCLAUDE.md for a file@ -mentioned in the prompt, for the
IDE's opened file or selection, and for theRead tool's notebook, image
and PDF results.
- A nested file the plugin attaches is not registered in the loop's
read-file state, so after a compaction the engine does not restore it
among the recently read files (the plugin attaches it again at the next
Read under that directory instead), and a change to it mid-session is
not re-announced.
- /cd carries the new tree'sCLAUDE.md in its own notice; the plugin's
files for the new tree arrive in the same next request through the
engine's instructions announcement instead.
- Paths compare by spelling; the engine resolves a symlinked alias of the working directory before deciding a file is inside it.
- --add-dir directories contribute noAGENTS.md , where the engine can
load theirCLAUDE.md .
- /memory and the# shortcut do not knowAGENTS.md files, and the
engine's own initial-load row does not count them (this plugin'sagents_md_load row does).
- An @ import outside the working directory inside anAGENTS.md is
honoured only once the approval the engine asks for aCLAUDE.md 's
external imports has been given (without it the import is left out, as aCLAUDE.md 's is); the approval dialog itself is raised forCLAUDE.md imports alone.
- A subagent that is not a fork gets a nested AGENTS.md at its own firstRead under that directory even when its parent's loop was already given
it; the engine does not hand such a subagent the nestedCLAUDE.md again.
A fork matches the engine on both sides.
claude plugin test mods/agents-md
tests/register.test.ts covers the default mode: a project with AGENTS.md
alone gets it as a project instruction file and one transcript line naming
it, a project with a CLAUDE.md of its own is left to the engine without a
walk, a failed walk leaves the context as handed, and the start hands
$.telemetry the mode row alone where a test seats a provider for that
noun, and goes on untouched where none is seated.
