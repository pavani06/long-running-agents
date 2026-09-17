---
url: "https://executor.sh"
key: "80612c2a5639"
status: "ok"
final_url: "https://executor.sh/"
method: "trafilatura"
content_hash: "94ace1f4836449a32c36b4528ff119d5af90ae7a"
text_len: 2851
fetched: "2026-09-17"
---

Executor is an MCP gateway.
- 01Connect everything to Executor.
- 02Give your agent the Executor tool.
- 03That's it. Get started.
One MCP. All your accounts.
Sign in, point your agent at one URL, done. Free for up to three people and 100,000 executions a month.
What we think
Every agent wants its own copy of every integration. You set up GitHub in Claude Code, then again in Cursor, then again in Codex. Same OAuth, same API key pasted in five places, and none of them agree on what a tool is allowed to do.
Your tools should belong to you, not to whichever agent you opened today. Executor turns everything into one shape: a name, an input, an output. An MCP server, an OpenAPI spec, and a GraphQL API all look the same to the agent, so you connect once and every agent gets it.
And the safe way has to be the easy way, or nobody does it. Executor knows a GET from a DELETE, asks before the scary ones, and runs everything in a sandbox where the model never sees a raw token.
Thousands of tools, one in the prompt
The model only ever sees one tool. Executor looks up what it needs when the code asks for it, so you can connect fifty services and the prompt stays the same size. Toggle a few below and watch the numbers.
Safe by default
- Policies come from the source.
- GET versus DELETE for OpenAPI, destructiveHint for MCP, mutations for GraphQL. Agents run the safe calls on their own and ask before the rest. You can override any tool.
- Secrets never reach the model.
- Calls run in an isolated JavaScript sandbox. Credentials are attached host-side at call time and never enter the sandbox, the agent, or the model's context.
- Set up once, whole team has it.
- Admins add workspace connections everyone shares. Individuals add their own. New teammates get the catalog on day one, with the same policies, and you can block a tool for the whole workspace in one click.
- Open source, so you can check.
- Cloud stores credentials in WorkOS Vault. Local and self-hosted keep them on your machine, or in 1Password. The whole thing is on GitHub if you would rather read the code than take our word for it.Source â
Run it where you want
Same tools, same policies, four ways to run them.
npm i -g executor
Not an agent? Cloud also has an HTTP API with user and workspace keys, so a script or a service can call the same tools with the same policies.
What people say
Mostly that they stopped copying API keys into five different agents.
Pricing
Cloud is free for up to three people. Team is $15 per member per month. Running it yourself is free.
Writing
About
Executor is backed by Y Combinator. It started because I wanted my own agents to reach my accounts in a way that was not scary. Most setups make you choose between locked down and useless, or wide open and risky. I wanted a third option.
Rhys SullivanFounder. Say hi on X, @RhysSullivan â
