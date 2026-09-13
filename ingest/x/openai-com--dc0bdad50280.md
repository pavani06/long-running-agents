---
url: "https://openai.com/index/introducing-the-agents-api/"
key: "dc0bdad50280"
status: "ok"
final_url: "https://openai.com/index/introducing-the-agents-api/"
method: "trafilatura"
content_hash: "bb084eb123c156da44de3207ce1c886f2a2971f4"
text_len: 5135
fetched: "2026-09-13"
---

As we’ve scaled Codex and ChatGPT for Work to millions of people around the world, we’ve learned what it takes to make long-running agents work well in practice. Useful agents need a powerful harness that manages context, uses tools efficiently, and coordinates subagents. They also need infrastructure that keeps them running reliably for days, with environments where they can work with files, run code, and save intermediate results.
Today, we’re introducing the Agents API(opens in a new window) in public beta, bringing that same harness and infrastructure that powers Codex to developers through a simple, flexible API.
With the Agents API, you can create a production-ready agent in a single API call by specifying the task, model, tools, and environment:
OpenAI hosts and maintains the harness. You choose the agent’s compute environment: in an OpenAI-managed sandbox, on your own infrastructure, or with one of our sandbox partners. The Agents API gives you a strong foundation for building agents on top of our optimized agent harness and infrastructure, so you can focus on the tools, knowledge, and workflows that make your agent unique.
Different workloads need different compute, storage, and deployment options. The Agents API lets you choose a sandbox that fits your application.
We’re partnering with ecosystem providers(opens in a new window), including Blaxel, Cloudflare, Daytona, DigitalOcean, E2B, Modal, Oracle, Runloop, and Vercel, to provide first-class integrations for a range of needs:
- Fully managed environments or deployments within your VPC
- Specific file and secret storage mechanisms
- Different CPU, GPU, and memory configurations, with performance, cold-start, and cost profiles to match your company’s workflow.
For developers who want to get started quickly and scale efficiently, we’re also introducing the OpenAI hosted sandbox(opens in a new window). This leverages the same sandboxing infrastructure that powers Codex and ChatGPT.
OpenAI provisions and manages the sandbox, giving your agent a secure and performant environment to run code, work with files, and produce artifacts. These sandboxes can be flexibly configured with your files, packages, skills and plugins to give the agent what it needs to complete the task.
Taking advantage of new model capabilities often means reworking your harness, taking valuable time away from improving your application. The Agents API provides versioned access to these capabilities with each model launch. We maintain and continuously improve the harness alongside our models, helping your agents get better performance from every upgrade. For example, recent improvements to the harness include:
To support models working for hours, we’ve built context management that helps agents carry relevant information across longer sessions. The Agents API automatically compacts(opens in a new window) earlier context as a session approaches its context limit, preserving information the agent needs to continue. Developers can build workflows that span multiple context windows without implementing their own compaction logic.
The Agents API helps agents find the right tools and use them efficiently. Tool search(opens in a new window) loads relevant tool definitions as needed, helping reduce token usage and cost while preserving the model’s cache. Once tools are available, programmatic tool calling(opens in a new window) lets agents run calls in parallel, chain related operations, and filter or combine results in code so they can work through large volumes of data while bringing only the relevant results back into context. The Agents API supports MCP, custom functions, and built-in tools like web search.
With multi-agent support(opens in a new window), the Agents API can break complex tasks into independent pieces and delegate them to subagents that work in parallel. Each subagent maintains its own context, helping it stay focused on its assignment, while the main agent coordinates their work and brings the results together. This can speed up research, analysis, and coding tasks that benefit from parallel work, without requiring you to build your own orchestration.
The Agents API is powered by the open-source Codex harness, giving developers visibility into the core logic that coordinates model calls, tools, and context. With the Agents API, OpenAI operates and maintains that harness while developers can inspect and learn from its public codebase(opens in a new window).
Agents API is available in public beta today to all developers. There are no additional fees for using the Agents API – you simply pay for the tokens and tools your agents use, as outlined on our pricing page(opens in a new window).
Explore the Agents API overview(opens in a new window) to learn more, or follow the quickstart(opens in a new window) to get started and bring the harness behind Codex into your own agents.
During the public beta, we’ll iterate quickly based on your feedback as we work toward general availability. Let us know what’s working, where you’re running into friction, and what you need to build and run your agents in production.
