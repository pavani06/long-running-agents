---
url: "https://newsletter.pragmaticengineer.com/p/openai-software-factory"
key: "557dcb769a02"
status: "ok"
final_url: "https://newsletter.pragmaticengineer.com/p/openai-software-factory"
method: "trafilatura"
content_hash: "47f7e759b397ca57def2a1117777bd539e3eb6ed"
text_len: 20719
fetched: "2026-09-16"
---

It’s rare to work with an unlimited token budget, but at OpenAI, that’s what all engineers, researchers, finance colleagues, and marketing folks do. Recently, I visited one of the world’s leading frontier labs to find out how OpenAI operates today – and for a glimpse at where software engineering might be headed as a profession.
Plenty has changed since I visited OpenAI’s headquarters last year. Within a year, Codex has gone from a “nice-to-have” tool to being the backbone of pretty much everything at the company.
To learn more, I talked with seven engineering leaders and engineers there: Venkat Venkataramani (VP of Engineering, Applied Infra), Sulman Choudhry (Head of Engineering, ChatGPT), Andrew Ambrosino (Lead, Desktop), Joe Gershenson (Lead, Core Agent team), Akshay Nathan (Engineering Lead, Productivity), Ahmed Ibrahim (Engineer, Codex) and Steve Coffey (Engineer, Responses API). Thanks to all for taking part!
Today, we cover:
- Codex takes over at OpenAI. In a matter of months, nearly all OpenAI’s non-engineers moved over to Codex and ChatGPT Work without a mandate from above for it.
- Death of the IDE & pull requests. IDE usage has been down since January when Codex usage started to surge. PRs and code reviews need to be rethought.
- OpenAI’s agentic software factory. OpenAI has built a “software factory” with several automated, agentic feedback loops: for example, Perf Factory monitors production and kicks off Codex agents to automatically fix performance issues.
- How engineering tooling & practices are changing. Hand-built internal tools are slowly being replaced by Codex, which is increasingly preferred for debugging over specialized tools. Harness efficiency is critical in software factories.
- Engineering for a billion users: how OpenAI scales up its infra. They buy first and take it in-house later. Also, geographic infra distribution, capacity planning tactics and challenges.
- Making OpenAI’s API more reliable and performant. CPUs are becoming a bottleneck, doing slower deployments on purpose, and solving load challenges.
- How the software engineering job is changing. Engineering specializations are disappearing, judgment and agency are more important, and it only takes one or two engineers for previously “impossible” rewrites and migrations to succeed.
Before we start, a scheduling update: I’m in New York for the week, attending the LDX3 conference and visiting a few startups and tech companies in the city, so there will be no edition of The Pulse on Thursday. Normal service resumes next week!
The bottom of this article could be cut off in some email clients. Read the full article uninterrupted, online.
1. Codex takes over at OpenAI
The takeaway from my visit to the company’s headquarters which really sticks out is that Codex – and lately Codex and ChatGPT Work – have taken over everything there, starting in around January. Desktop lead, Andrew Ambrosino, told me:
“The big theme of the past months has been that everything is now a coding agent. Whether the visible code is your output or not, agents write your artifacts.
Think of it like this: your entire life is via software. You have these powerful tools (agents) in your computer, and the ability to loop and reason and write code is the ability to do everything.”
The token usage chart below shows this sudden adoption surge:
In a four-month period, non-engineering orgs like finance, recruitment, and legal went from ~0% usage of Codex to 90% usage. Now, almost all OpenAI employees use Codex and ChatGPT Work weekly. So, what happened?
OpenAI released the Codex app for Mac in February and for Windows in March, and ChatGPT Work (powered by the Codex harness) in July. Following that, non-engineers there moved all their workflows over to Codex and then to Work. Caveat: OpenAI’s internal version of Codex is a lot more advanced than its external counterpart because it’s plugged into pretty much every OpenAI system – similar to how Ramp’s Inspect AI agent has been wired up.
The fascinating part of this is that OpenAI got close to 40% adoption across non-engineering teams at a time when the Codex app was hostile to non-engineering users (hard to use). Between February and April, the Codex app still showed the code on-screen, but even so, non-technical colleagues outside of engineering still used it because it could do complex work like researching and creating a presentation, document, spreadsheet, or tasks that produce rich output. Today, those folks are very heavy users of it.
Being able to work for longer on more complex things drove adoption. OpenAI added the /goal setting to Codex, where you can set up a goal for the agent and it keeps working until it is complete. Between April and May, usage surged from 60% to 90%. Andrew believes improvement in the harness’s handling of long-running tasks was one cause of this:
“The number one thing that is changing is that people are starting to use threads for much longer, and this longer usage has been a breakthrough. It’s surprising to see the sheer length of time that people spend on a thread – even days! They often set a goal and then have the model crank.
Codex being good at longer-running tasks seems to cause people to do fewer things in parallel. This is because a long-running agent often spins off other agents to do other things, reducing the surface area that you, as a human, have to manage.”
“Awareness overhang” is another cause of the rapid adoption, the Codex team believes. As Akshay Nathan, Engineering Lead, Productivity team, told me:
“For a long time, we had a ‘capability overhang’: the models were capable but the products didn’t fully bring that out. Now, we’re seeing an awareness gap. Some people have figured out they can use Codex to monitor Slack, update Airtable, or create onboarding materials. But many others still use it for one task and then discover more uses from teammates via word-of-mouth.
But there’s still so much more, under the surface, that you can do with Codex.”
Role-specific and team-specific plugins are created and distributed. Another thing that sped up adoption is that each group started to distribute useful role-specific workflows as plugins. Andrew explained why it’s important to not just offer a generic coding agent:
“If you build a product that can do anything, teams need a way to make it their own. You can’t just give everyone an empty box. Skills and plugins let teams adapt the agent to their work. Sometimes, we also need a new app capability, like a browser that the agent can use alongside those skills. But the same building blocks already cover a lot of different roles.”
Subject matter experts are embedded in ChatGPT Work engineering teams. The models have become “smarter” than developers in some domains, so devs cannot channel “taste” into the harness in those areas. So, people who are domain experts are onboarded onto engineering teams. This is one outcome of ChatGPT Work being used by so many non-engineering domains: experts embedded with engineering advise developers on things like what a good slide deck, spreadsheet, or business report looks like.
Of course, domain experts being in engineering teams is a decades-old best practice for building quality products. It seems like this gets rediscovered in different contexts every few years!
OpenAI is fully dependent on Codex and Work. This is so much the case that in the event of even a minor outage, internal messages from colleagues alert the Codex and Work teams at the same time as – or before – automated alerts.
Basically, work happens through Codex and Work, and pretty much nothing else. From the outside, this dependence on a single shared harness is particularly eye-catching; two years ago, there were no AI agents, only advanced AI autocomplete!
2. Death of the IDE & pull requests
Late last year, the Codex team was torn about whether to release the Codex desktop app. Andrew recalls the hesitation:
“In December 2025, we weren’t entirely sure if we would release the Codex app. We had the Codex CLI as a terminal, and there are large, feature-rich IDEs out there. So, would there be space for a dev tool that is between a terminal and an IDE? In my head, there was this future where it would not work out, and be the kind of ‘misfit’ like the iPad was.
A lot of people buy iPads and then never use them: they either use their smaller, more portable smartphone (which could be the equivalent of the CLI in this metaphor), or their feature-rich laptop (the equivalent of the IDE).
Also, don’t forget that in November, Antigravity came out as a VS Code fork. This added to the feeling that perhaps we should have also forked VS Code for the Codex app. But still, we dismissed the temptation and went with our gut feeling that as AI agents get better, IDEs will matter less.”
Indeed, since January, IDE usage has gone down and OpenAI’s bet looks like a good one. However, the Codex app is becoming a little more akin to an IDE: for example, the ability to edit files inside the app was shipped in June.
CI/CD systems are seeing massive load increases. One sign of productivity gains from Codex is the amount of additional code flowing through OpenAI’s dev infra systems. More code being created and pushed leads to new scaling challenges which the team is currently heads-down on solving. Venkat Venkataramani, VP of Engineering, Applied Infra, said:
“The number of pull requests (PRs) per engineer is growing like a hockey stick (at a very high, accelerating rate). Every part of the build-test-deploy pipeline is seeing dramatically more load.
We’re talking about roughly a 10x increase in load on some systems. At most companies, that kind of growth might happen over two or three years. At OpenAI, we see it in about six months.
That level of acceleration exposes bottlenecks everywhere: version control has to handle far more code being written and pushed, CI/CD systems have to scale with it, and production release processes have to absorb a much higher rate of change.
Every month, we wake up to a new set of infrastructure scaling challenges to solve. Just when we think we’ve created enough capacity for the next phase of growth, the model unlocks another wave of capabilities, which creates a new set of bottlenecks somewhere else in the system.”
In this context, PRs and code reviews are being rethought. They have “core primitives” in software engineering, but this level of development acceleration is an opportunity to reimagine them. Again, from Venkat:
“The question we ought to ask ourselves in the middle of all this development acceleration is how do we reimagine many things we took for granted. For example, how do we reimagine the CI (continuous integration) and CD (continuous deployment) process? What does observability mean in this world, and how should people interact with pull requests?
If you ask me, the way we do code review today makes less and less sense, and the same is true for pull requests.
We’re now seeing agentic code reviews that look at code changes through a series of different lenses. In the past, it would have been impractical for a cloud infrastructure engineer and a security engineer to review every single code change. With agents, that becomes possible.
We can rethink how code is deployed with agents, too. We are building an agent that “handholds” a change all the way to production — whether it’s a code change or a change behind a feature flag. It observes the relevant monitoring graphs, but can also build its own dashboard to monitor important signals. More of our code changes are going to production with this kind of agent monitoring.”
An increasingly painful bottleneck is in deploying native mobile apps. When there are ten times more pull requests, it’s challenging to deploy on the backend or the web and more infrastructure is needed to do so. Then, after you rework a CI/CD system and make sure there’s enough capacity to run them, you’ll be deploying that many more PRs to production.
This arises in the shipping of updates to native iOS and Android apps because every app update needs to go through Apple’s and Google’s manual approval processes which take hours or days to complete.
Talking with Sulman Choudhry, Head of Engineering, ChatGPT, he explained how the app review bottleneck is affecting iteration speed. Sulman used to work at Facebook and remembers how the social media company sped up shipping mobile releases:
“Back in the 2010s, Facebook had a pretty important breakthrough in how to ship native mobile code faster. App Store releases went from monthly to bi-weekly to weekly. At the same time, experimentation and feature flags let teams ship code before it was ready to launch, then turn features on remotely when they were.
That model brought a lot more velocity to mobile.
In the age of Codex, I think we’re hitting the next version of this problem. Code generation is getting dramatically faster, but getting that code into users’ hands on native mobile is not. For Codex in particular, where usage is heavily mobile-first, that gap is already becoming painful for us and users.
I expect the pressure here to increase quickly. If software can be written in minutes, waiting days or weeks to get it onto a phone starts to look increasingly absurd.
We should be aiming for a world where shipping code on native mobile is as fast as shipping on the web. Getting there will probably require some creative rethinking of what we ship, when we ship it, and what can be activated remotely. Today, we’re nowhere close.”
There’s some irony in how shipping a native iOS or Android app has the exact same challenges today as in 2008, when the App Store was launched. In 18 years, not much has changed! Apple still does not officially allow apps to bypass the App Store review process to ship meaningful experience changes.
3. OpenAI’s agentic software factory
The idea of a “software factory” is similar to a physical factory where robots and humans produce autos together. In the software context, it is AI agents and humans producing software. Some manufacturing sites are fully automated “dark factories” where illumination isn’t needed because there are no humans. Could the same fully automated process emerge in software engineering? At OpenAI today, there’s a “software factory” running and it’s all built around Codex.
Here’s how the “traditional” software development pipeline used to look, compared to what OpenAI’s agentic infra pipeline looks like today, as described by VP of Engineering, Applied Infra, Venkat Venkataramani:
The pipeline:
1. A human builder defines the desired outcome. A software engineer or product manager specifies the problem and desired outcome. Judgment, prioritization, and taste are becoming more important for this phase. Interestingly, Venkat told me that engineers at OpenAI are becoming more like product managers than traditional systems engineers.
2. Codex gathers context. OpenAI has moved all its documentation inside of the source code, which makes it easier for agents to understand more of the code. Codex also has access to:
- Git repositories and GitHub
- Slack and Notion
- Internal data sources: Databricks, Datadog, internal logs, etc
- Internal Codex skills – some of which are maintained by OpenAI’s Codex implementation itself!
Codex is so “plugged” into OpenAI that new engineers are directed to ask Codex any questions they have during onboarding because it has a surprising amount of context.
3. Codex implements code changes. This part is trivial enough: Codex gets to work and makes a series of code changes until it reaches its goal, and then verifies that the software works as it should.
4. Build & test, then CI. The agent builds the code, runs the tests, fixes the code when it breaks the test, and then creates a pull request. This pull request triggers the continuous integration (CI) server to run and execute a more thorough suite of linters and tests. The agent babysits the PR until it’s “green”, fixing any CI failures and automatically updating the PR.
New: a “perf harness”: the agent also uses a perf harness to send problematic PRs to the Synthetics A/B framework for evaluating performance implications. As mentioned above, the load upon CI systems has increased greatly in the past six months.
5. Agentic code review. Instead of using one generic AI code reviewer, OpenAI spins off multiple agents, each with a “domain specialist” configuration. Venkat told me they see this as equivalent to having a human domain expert from each relevant infrastructure team review every change.
Note from Gergely: I was skeptical about the claim that an agent that’s told to be a cloud infra specialist would produce a different review from a generic agent. However, all Codex agents have full access to OpenAI’s code and docs, so this “cloud infra expert” agent likely has gathered a lot of context about cloud infra setup and best practices, meaning it should provide highly targeted feedback. The important thing is how these “domain specialist” agents are set up, the context they have access to, and how they focus only on their own domain to make best use of their limited context window.
Code changes are classified by risk. High-risk changes can be sent through stricter processes; for example, they might invoke more AI code reviews, or mandate that a human reviews it after the AI agents finish. Low-risk changes follow an easier path; areas of the codebase can opt in to an agent that will auto-approve low risk PRs, removing human acceptance as a bottleneck and improving velocity.
A neat thing about risk assessment is that OpenAI can automate when additional compliance input is needed: either automated (via another agent) or human review. With the quantity of PRs being produced, it simply wouldn’t be possible for humans to review all code without assistance.
Just like with CI, the coding agent babysits the comments and updates the PR to fix issues surfaced.
6. Agentic deploy. After a human approves a change to go to production, it is assigned its own agent with an instruction that could be summarized as:
“Handhold this change until it is safely and fully rolled out into production.”
Agents handhold both the code changes and the changes behind feature flags. For example, in the case of a change behind the feature flag, the agent will:
- Read the codebase and figure out where the feature flag lives
- Understand what the change does
- Decide which signals indicate success and failure
- Builds its own monitoring dashboard to use – this is a pretty impressive improvement and something that’s new to me
- Watches relevant production signals and its dashboard(s)
OpenAI’s long term goal is to have something like a “per-change autonomous SRE” (site reliability engineer) in the form of an agent that can deploy pretty much autonomously.
7. Observe production. Tools which track the production system:
- Dashboards generated by the agent during previous steps
- OpenAI’s internal observability stack, including a bunch of custom tools that generate logs, metrics, trace & wide event data
One big change at OpenAI since my previous visit, pre-Codex, is that back then, engineers created dashboards to monitor services whereas now, agents do this at the granularity of per-change deployment.
8. Production monitoring feeds back into development. OpenAI’s “Perf Factory” uses agents to sift through alerts and dashboards, de-duplicate signals, identify real latency regressions, root-cause them and propose fixes. This helps catch performance issues introduced by ongoing code changes, extending the workflow beyond deployment into continuous improvement.
9. Respond to outages. Sevbot is OpenAI’s internal incident response agent; unsurprisingly, it’s also built on top of Codex. When an incident is detected, the bot “wakes up.” Here’s what it does:
- Collects context about the incident
- Determines possible mitigations (but never executes any)
- Answers devs’ questions (it’s part of the Slack channel)
- An engineer can tell it to apply a specific mitigation
OpenAI’s goal is to get to the point where Sevbot can take autonomous action when mitigating some outages. The dream is that no humans be woken up outside of their working hours during an outage because Sevbot can handle “routine” outages autonomously, with humans reviewing its actions when they return to work. But as of now, oncall duty is not a thing of the past at the company.
4. How engineering tooling & practices are changing
Unsurprisingly, Codex is changing how easy it is to build internal tools and having an impact on standard engineering practices like debugging. Here’s what I gathered from talking with folks at OpenAI.
