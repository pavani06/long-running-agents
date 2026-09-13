---
url: "https://github.com/coldteadotai/pr-lens"
key: "bfc01f4b86fd"
status: "ok"
final_url: "https://github.com/coldteadotai/pr-lens"
method: "trafilatura"
content_hash: "6b6da2706801d0aacfd71767a6a74473ef2e0e80"
text_len: 10211
fetched: "2026-09-13"
---

Understand a pull request before you read a line of it.
  PR Lens draws every pull request as animated architecture and data-flow diagrams,
  posted as a comment inside the pull request itself
  Free for open source   ·   Or let your coding agent draw it: npx skills add coldteadotai/pr-lens
  
| What the pull request touches, drawn against the system around it: the components involved, and the calls that run between them. Colour carries the delta: green new, amber changed, red gone |  | 
| The ordered pipeline of the change as an animated sequence: one dot crosses one arrow at a time, in the order the steps happen. |  | 
| The comment nests <details> sections, each carrying its own diagram scoped to one part of the change: the whole blast radius on top, then the new path, then what was retired. |  | 
| Every comment links to the interactive canvas: the same diagrams at full size, with pan, zoom and a light or dark theme, so a large change is read at the size it needs rather than the width of a comment. |  | 
| A walkthrough tours the change one step at a time. It dims everything else, lights the cards and routes for that step, and says in a line what happened there. Press play on the canvas, or W. |  | 
| The same visual grammar answers for every size of change: lanes, node cards, delta colours, and routes you can trace with your eye alone. For what its worth, you should not be opening a PR this large |  | 
| With the Github app, every diagram ships as a pair, and GitHub shows the one that matches the reader's theme. Or you can render any theme locally via your coding agent |  | 
The pull requests behind Hooks, Node fetch and Ingress, run back through PR Lens. Same renderer and same contract as the diagrams above.
react/react#13968 · 36 files · +5,868/−130 · 5 lanes. Hooks arrive behind a feature flag.
nodejs/node#41749 · 16 files · +8,076/−3 · 5 lanes. fetch, Request, Response and Headers land in core.
kubernetes/kubernetes#14175 · 8 files · +766/−0 · 4 lanes. The first Ingress resource type, for L7 load balancing.
Seven more · Vue, Rust, Tokio, Neovim, Django, webpack, vLLM
vuejs/core#2532 · 11 files · +1,081/−670 · 3 lanes. <script setup> and the original ref sugar.
rust-lang/rust#31954 · 26 files · +369/−16 · 4 lanes. The postfix ? operator, chainable shorthand for try!.
tokio-rs/tokio#1657 · 100 files · +7,408/−6,795 · 3 lanes. The work-stealing pool rebuilt to cut scheduler overhead.
neovim/neovim#11336 · 15 files · +5,556/−1 · 3 lanes. The LSP client moves into Neovim itself.
django/django#11209 · 38 files · +931/−42 · 5 lanes. An ASGI handler and a coroutine-safe request context.
webpack/webpack#10440 · 13 files · +567/−5 · 5 lanes. ContainerPlugin, and module federation with it.
vllm-project/vllm#1348 · 6 files · +764/−139 · 3 lanes. PagedAttention V2 and its sequence-level parallelism.
Open the Hall of Fame → Every diagram there is live.
Use .github/pr-lens.yml to customize PR Lens. See the configuration reference for settings, defaults, and examples.
For CLI rendering, put map corrections in .github/pr-lens.yml rather than editing generated SVGs:
schemaVersion: 0.1.0
map:
  rename:
    - match: services/legacy-mailer.ts
      to: Postmark sender
  exclude:
    - "**/*.test.ts"
It is an overlay, so it keeps holding as the code moves and the model renames things between runs. Renames, exclusions, lane pins and groupings, all in packages/cli.
The App is the whole setup for most people. The modes below cover what it does not: your own CI, your own model, or a diagram before the pull request exists.
Via your coding agent
Your agent is usually already the model. Rather than spending a provider key to describe a diff it already understands, it writes the graph document itself and lets the validator hold it to the contract.
  
npx skills add coldteadotai/pr-lens
Then say, literally:
Diagram the change you just made with PR Lens and attach it to the pull request.
The agent reads the diff, writes the document, runs npx @coldtea/pr-lens-cli validate until the contract is satisfied, renders, and puts the diagram in the pull request description with gh pr create --attach, so it lands with the change instead of behind it. If a diagram names things wrongly, the same skill teaches it to fix .github/pr-lens.yml instead of editing generated output. Details in packages/agent-skill.
Prefer to have the agent do the whole setup? Paste this:
Set up PR Lens (prlens.dev) for me: it draws each pull request as animated architecture and data-flow diagrams, inside the pull request itself.
1. Install the agent skill: `npx skills add coldteadotai/pr-lens`.
2. Walk me through installing the GitHub App at https://github.com/apps/coldtea-pr-lens on every repository where I review pull requests. It posts one sticky comment per pull request and updates it on every push, with no model key of mine involved.
3. If I'd rather run it from CI with a model key of mine, offer the Action instead: `.github/workflows/pr-lens.yml` using `coldteadotai/pr-lens/packages/action@v0`, with the key as a repository secret. It takes Gemini by default, OpenAI, or any endpoint speaking `/chat/completions`.
4. Then prove it: diagram the most recent change in this repository and show me the rendered SVGs.
As a workflow: the GitHub Action · your CI · your key · one static comment
The same comment from your own CI, drawn with your own model key. Add that key as a repository secret — GEMINI_API_KEY below, because provider defaults to Gemini — then commit this as .github/workflows/pr-lens.yml:
name: PR Lens
on:
  pull_request:
permissions:
  contents: write # to publish the rendered SVGs
  pull-requests: write # to post the comment
concurrency: # one run per pull request; a push supersedes the last
  group: pr-lens-${{ github.event.pull_request.number }}
  cancel-in-progress: true
jobs:
  lens:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # the diff is between two commits, so both must be here
      - uses: coldteadotai/pr-lens/packages/action@v0
        with:
          api-key: ${{ secrets.GEMINI_API_KEY }}
Nothing here is tied to one model. provider takes gemini (the default), openai, or openai-compatible with a base-url and model, so the same workflow runs against OpenRouter, DeepSeek or a server of your own. The key reaches the CLI through the environment, never a command line, and the diff goes to the provider you name and nowhere else. The comment here is deliberately static — an Action cannot hold state between runs, so the checkboxes live in the App. Providers, lenses, branding and the rest of the inputs are in packages/action.
From the CLI · every step on your machine, one at a time
Everything the other modes do, one step at a time, on your machine. Only analyze talks to a model, and its key is read from the environment, never from a flag:
export GEMINI_API_KEY=…    # the default provider; OPENAI_API_KEY with --provider openai
# Diff in, graph document out — measured against the merge base, not the branch tip.
npx @coldtea/pr-lens-cli analyze --base origin/main
# The document as light and dark SVGs, plus the manifest a comment is built from.
npx @coldtea/pr-lens-cli render .pr-lens/graph.json
# The pull request comment as markdown, on stdout. Posting is your business.
npx @coldtea/pr-lens-cli comment --graph .pr-lens/drawn.graph.json --manifest .pr-lens/manifest.json \
  --asset-base-url https://raw.githubusercontent.com/owner/repo/pr-lens/42
# Any PR Lens document, checked against the contract — every problem, not just the first.
npx @coldtea/pr-lens-cli validate .pr-lens/graph.json .github/pr-lens.yml
# After the merge: the pull-request document as a stored map of the system, worth committing.
npx @coldtea/pr-lens-cli export .pr-lens/graph.json -o .github/pr-lens.map.json
Everything lands in .pr-lens/, which the CLI adds to your .gitignore the first time it writes there. Treat it as scratch: the files are rebuilt from the diff on demand, and the only one worth committing is the map export writes. --out puts them somewhere else if you would rather.
Ollama, DeepSeek, OpenRouter and anything else speaking /chat/completions are reached with --provider openai-compatible --base-url <url>. The full command reference, the correction file, and the failure codes a script can branch on are in packages/cli.
In your terminal · the diagram before the pull request exists
Nothing about the diagrams needs a pull request. Render locally and look at the change before anyone else does:
npx @coldtea/pr-lens-cli analyze --base origin/main
npx @coldtea/pr-lens-cli render .pr-lens/graph.json
open .pr-lens/*-dark-*.svg    # macOS; the SVGs are self-contained, any browser reads them
This is also the shape of reviewing an agent's work: while you read the diff, the agent that wrote it renders it. With the skill installed, "render this change with PR Lens and open the SVGs" gets you the diagram beside the diff, the same picture its pull request will carry, minutes earlier.
| Package | What it is | 
|---|---|
| packages/schema | @coldtea/pr-lens-schema : the contract every other component speaks | 
| packages/renderer | @coldtea/pr-lens-renderer : deterministic JSON graph → the animated, theme-paired SVGs on this page | 
| packages/cli | @coldtea/pr-lens-cli : read a diff with your own model key, render it, compose the comment | 
| packages/action | the GitHub Action: analyze, publish, post one static comment | 
| packages/agent-skill | @coldtea/pr-lens-agent-skill : teaches a coding agent to draw the change it just made | 
pnpm install
pnpm verify      # build, typecheck, test
Node 20.11+ and pnpm 10.
Open an issue first and wait for one of us to approve it before you (or agents) write any code. A pull request with no approved issue behind it will be closed. Once your issue is approved, link it from the pull request.
Commit under your own name only. No Co-Authored-By line for a model, no "Generated with" footer, no session link — use an agent if you like (and we do too), but the commits are yours, full responsibility. Most tools add these unless you turn them off.
Reducing the cognitive load of reviewing PRs
MIT © Coldtea
