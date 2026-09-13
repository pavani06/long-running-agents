---
url: "https://hackernoon.com/what-happens-to-your-engineering-platform-when-ai-raises-the-baseline"
key: "2d2f41f5915e"
status: "ok"
final_url: "https://hackernoon.com/what-happens-to-your-engineering-platform-when-ai-raises-the-baseline"
method: "trafilatura"
content_hash: "2e9b89aff2a1be345138a62d7c9d8e5a18b23100"
text_len: 17814
fetched: "2026-09-13"
---

AI is changing what engineers can produce. The harder job is redesigning the system around them.
In January 2023, we ran GPT-3.5 through the same Go and SQL interview blocks we were using to hire senior engineers. We did not create a separate benchmark for the model or simplify the questions. By our internal rubric, it crossed the senior hiring threshold on both blocks.
That did not mean GPT-3.5 could do the job of a senior engineer. We did not test it on system design, navigating a large codebase, working through an ambiguous production problem, or taking responsibility for a decision. Still, the result exposed something uncomfortable: part of what we treated as senior-level signal was pattern recognition that a general-purpose model could already reproduce.
At the time, I dismissed the result as a workaround. It felt a little like using Google Translate instead of learning a language: useful, but not a real capability.
I was wrong about what the workaround meant.
Today, effective use of an LLM is part of the engineering baseline. The skill is not getting the model to produce an answer. The skill is defining the problem well, recognizing when the answer is weak, and remaining responsible for what happens when the result reaches production.
That is the important shift. AI does not only make engineers faster. It moves the boundary between execution and judgment.
I lead Tech Platform at inDrive, a global ride-hailing and services company operating in more than 40 countries. Our group is responsible for developer tooling, shared infrastructure, CI/CD, and engineering practices across product teams.
We do not build the product. We build the environment in which the product gets built.
By platform, I mean more than infrastructure and deployment pipelines. It includes the tools, standards, context, and feedback loops that shape how engineering work is done. As AI changes what individual engineers can produce, that environment has to change with them.
Speed matters, but speed is not the goal. The goal is to ship more of the right product without lowering the bar on quality, security, or accountability.
Here is how we are approaching that work.
When a Senior Signal Is No Longer Enough
The GPT-3.5 experiment did not show that an LLM was equivalent to a senior engineer. It showed that some of the signals in our interview process were no longer sufficient.
The model performed well when the problem was already structured and the expected output was clear. It struggled when it had to define the problem before solving it, work through incomplete context, or make an original judgment across several conflicting constraints.
That distinction changed how we think about technical interviews.
Our Go interviews now run in CoderPad with the built-in AI chat available to both the candidate and the interviewer. AI use is not an edge case that we tolerate. It is an explicit condition of the interview.
We evaluate how candidates turn incomplete requirements into a precise task. We watch whether they challenge the model’s output, how they reason about trade-offs, and whether they can explain the code that was generated. We also verify that they retain enough independent knowledge to judge the model rather than simply follow it.
The problems are framed as realistic engineering scenarios: optimizing a student dashboard service, implementing the core of a web crawler, or designing a component under concrete performance and reliability constraints.
Each interview has two scored phases: design and requirements gathering, followed by live coding.
During the design phase, we do not score whether the candidate used AI. We score how they used it.
Strong candidates narrow the problem before asking for a solution. They identify missing constraints, question assumptions, and support their choices with rough calculations around throughput, latency, storage, and failure modes.
Weak candidates accept the first answer at face value. They cannot explain why a particular approach was chosen, or they describe an architectural decision as “obvious” without being able to defend it.
Architectural fundamentals are still evaluated directly. The purpose is not to test memorization. We need to know whether the candidate understands the system well enough to recognize when the model is leading them in the wrong direction.
The same principle applies during live coding. Candidates may use AI for any part of the solution, but they remain responsible for the code. The interviewer can select an arbitrary section and ask:
Could this be implemented differently, and why would you choose one approach over another?
The candidate answers without AI.
Every session also includes five to ten minutes of unassisted coding. The candidate writes a moderately complex function using concepts such as timeouts, retries, cancellation, or context handling.
If they cannot work with the fundamentals independently, that phase fails regardless of how polished the AI-assisted solution looks.
For senior and staff-level roles, we add another dimension. We look at whether candidates can turn ambiguous intent into a testable specification, redesign an existing process around AI-assisted execution, define evaluation and failure criteria, and build permissions and accountability into the system from the beginning.
This change does not end when someone is hired.
Routine implementation work has historically helped junior engineers develop judgment. They learned by writing ordinary code, seeing it fail, debugging it, and gradually building a mental library of failure modes.
If agents absorb more of that routine work, we cannot assume that the same judgment will develop automatically. Unassisted exercises, supervised exception handling, rotations, and structured review have to become deliberate parts of the engineering operating model.
AI changes what an engineer can produce. Our interviews and development systems must measure whether the engineer can still understand, challenge, and own the result.
Trust Is Earned One Workflow at a Time
New AI tools appear faster than a normal enterprise adoption cycle can comfortably process them. Evaluation, controlled pilots, and gradual rollout are still necessary, but the technology may change materially before a traditional review process is finished.
The answer is not to skip evaluation. It is to evaluate under real operating conditions without handing over authority too early.
Most AI workflows today are still assisted: an agent does the work, and the person validates the result. When we find a process that could plausibly become more autonomous, we run the AI-assisted version alongside the existing manual path.
The agent handles what it can. The old process covers the gaps and retains final authority.
One example is crash analysis in one of our larger product verticals.
The mobile stability team used to work through top crashes manually. An engineer would read the stack trace, identify the responsible module, find the owner, create a ticket, wait for a fix, and then verify the result in a later release.
Working with the product and stability teams, we built dedicated AI skills for iOS and Android. By a skill, we mean a reusable, parameterized workflow designed for a specific class of work, rather than a general chat prompt.
The workflow can now read crash reports and stack traces, identify the likely responsible module, suggest an owner, prepare a draft pull request, and connect the proposed fix to release validation.
The team still decides whether the diagnosis is correct, whether the change should be accepted, and whether the workflow has earned more authority.
While the AI component is being tuned, the manual process continues to run in parallel. That gives us evidence from real production conditions without making the business process depend on unproven autonomy.
Average accuracy is not enough. The cases that determine whether a workflow is trustworthy are often the unusual ones: a misleading ownership signal, an unfamiliar stack trace, or a fix that works locally but fails during rollout.
We call the principle behind this Tail Reliability. Autonomy increases only after a workflow has demonstrated stable performance across the long tail of edge cases that can hurt us, not merely on the average case.
The reliability bar is different for every workflow. An agent drafting documentation should not be evaluated like an agent initiating a rollback. The potential damage, reversibility, observability, and available human intervention all matter.
We also do not treat autonomy as a permanent achievement. A workflow may move from assisted to supervised operation after it passes evaluation. But a new model, prompt, tool integration, or vendor version does not automatically inherit the previous level of trust. If the workflow regresses against its evaluation suite, its autonomy is reduced until reliability is demonstrated again.
Make Good AI Use Repeatable
Giving every engineer access to an AI tool is not an AI transformation. Access matters, but the larger question is whether good use can spread beyond the people who discovered it first.
We approach enablement through tooling, education, and local role models.
At the company level, we have opened agentic AI tools to all engineers. We want engineers to have access to capable and efficient models. But access to a model is not where an engineering organization creates lasting advantage. The advantage comes from the framework around the model and the domain context connected to it.
We maintain a common repository of reusable AI skills. Teams contribute workflows for code review, test generation, incident analysis, crash investigation, and other recurring engineering tasks. What one team figures out becomes infrastructure for everyone else.
The second part is education.
inDrive has a structured AI education program for engineers. It includes a foundational course, an advanced cohort, and specialized tracks for QA, mobile, and backend development.
The foundational course is part of engineering onboarding. Every new engineer starts with the same basic context: how the tools work, where they tend to fail, how we expect them to be used, and where human judgment remains mandatory.
The goal is not to teach people how to generate more code. It is to develop specification literacy, systems thinking, evidence-based decision-making, and calibrated trust.
Engineers need to know what can be delegated, what must be checked, and when the model is operating outside the context it needs to make a useful recommendation.
The third part is role modeling.
Inside teams, that role is filled by people we call AI champions. They do more than use the tools frequently. They receive early access, break workflows, investigate failures, debug integrations, and explain what they learn to their teammates.
Documentation can explain what a tool is supposed to do. A trusted colleague can show the team how it fails, how to recover, and when not to trust it. That embedded experience is difficult to replace with internal newsletters or one-time training sessions.
Tech Platform and the champion network provide the shared capabilities and trusted context. Product teams apply those capabilities to their own domain problems and remain accountable for the outcome.
This does not turn specialists into generic generalists. We still need deep expertise. But engineers increasingly need enough breadth to understand how a decision moves from an initial request, through an agent and a set of tools, into a production outcome.
Build a Platform Agents Can Actually Use
Consider a developer investigating a failed production rollout.
The information they need may be spread across Grafana, Kubernetes, GitHub, the deployment platform, internal documentation, and the ticketing system. The difficult part is often not running a single query. It is assembling enough context to understand what happened.
An agent can help with that work, but only when it can discover the right tools, receive the right context, and act within clearly defined permissions.
API-first design made systems programmable. Agentic systems add another requirement: the interface must also be discoverable and usable by an agent without bypassing the controls of the underlying system.
We describe this direction as MCP-first.
The Model Context Protocol does not replace APIs. It provides a standardized way for AI applications to discover and invoke tools backed by those APIs. MCP is the connection mechanism. Governance, context, permissions, and accountability still have to be built around it.
In our target architecture, we call this surrounding layer the Knowledge Spine.
It has three main parts.
The Protected Knowledge Zone contains stable, curated context that agents must not redefine: architecture principles, security requirements, product contracts, verified runbooks, and strategic guardrails.
Agents may read this information, but they cannot modify it directly.
The Live Knowledge Zone contains operational context: metrics, deployment state, incident timelines, and knowledge created as people and agents execute work. Updates are controlled, attributable, and auditable.
The Orchestrator sits above both zones. It handles identity, routing, access control, tool selection, context injection, and the audit trail for each interaction.
This separation is deliberate. An agent should not be able to rewrite the rules governing its own behavior while it is executing a task.
Our internal Dev Platform, the CI/CD and deployment system used across product teams, has its own MCP server. Through it, an authorized agent can search for services, inspect deployment state, investigate rollout failures, retrieve pipeline context, and initiate a rollback within governed permissions.
Our internal Zero-Code Platform follows a similar pattern. Its MCP layer proxies the existing GraphQL API and authentication flow, allowing product managers to manage widget configuration through an agent without working directly in the administration interface.
The goal is not to replace every UI and CLI with a chat window. The goal is to reduce the cost of assembling context across fragmented systems while preserving the permissions, controls, and auditability of those systems.
An agent can collect evidence and build an operational picture. The underlying platforms still decide what data is available, which actions are permitted, and who is responsible for the result. MCP is how tools connect to the agent. The Knowledge Spine determines what the agent knows, what it may do, and who remains accountable.
Treat AI Capacity Like Infrastructure
Once agents can act across internal systems, AI stops looking like a collection of individual subscriptions. It starts looking like a familiar category: shared infrastructure.
It has to be provisioned, observed, metered, secured, evaluated, and supported.
The cloud analogy is useful here, but it is often reduced to cost.
For a stable and predictable workload, dedicated infrastructure may be cheaper than cloud infrastructure. The same can be true for AI-assisted work. AI is not automatically the cheapest way to perform every task, and token cost should not be confused with the full cost of an engineering outcome.
The more interesting property is elasticity.
A team may need additional capacity for a migration, release-hardening effort, incident backlog, documentation push, or short product experiment. AI capacity can absorb part of that temporary peak without forcing the organization to treat a short-term spike as permanent demand.
Tech Platform’s role begins to resemble the role infrastructure teams played during the original cloud migration. We provide a reliable, observable, governed, and metered layer of AI capacity that product teams can apply to their problems without rebuilding the same foundation independently.
The capacity created by agents does not simply disappear from the organization.
It moves into work that was previously too expensive to prioritize. It also creates new permanent work: evaluation, skill development, knowledge curation, security, observability, and exception handling.
And it should move engineers toward the parts of the job where their judgment matters most.
That is what “augment, not replace” means operationally. The team’s impact grows, but quality is not traded for automation. People remain capable of judging the work, owning the result, and taking over when the workflow reaches an exception it cannot safely handle.
The Baseline Will Keep Moving
The GPT-3.5 interview experiment we ran in January 2023 was small and informal. But it made a larger change visible earlier than we expected.
If a general-purpose language model can reproduce what your hiring process treats as a senior-level signal, that signal is no longer sufficient on its own. The same logic applies to the engineering platform.
When AI changes what individuals can do, the organization has to redesign the environment around their work: the interviews, training, workflows, tools, context, evaluation, permissions, and guardrails. The hard part is not adopting a model. It is moving quickly without outsourcing judgment.
Trust has to be earned by each workflow. Access has to be governed. Context has to be maintained. Engineers have to understand the systems they operate, challenge the output they receive, and remain accountable for what reaches production.
AI transformation is not a project with a completion date. It is a continuous redefinition of the engineering baseline.
The job of an engineering platform is not to help teams catch up after that baseline moves. It is to make the new baseline safe, usable, and repeatable.
The models may be external. The engineering system around them is not.
