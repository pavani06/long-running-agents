---
url: "https://academy.dair.ai/papers/collections/harness-engineering"
key: "4b87f810cdf0"
status: "ok"
final_url: "https://academy.dair.ai/papers/collections/harness-engineering"
method: "trafilatura"
content_hash: "cc4d9dd92d1e7bdfb902d4e14653ce2265c27a48"
text_len: 10196
fetched: "2026-09-13"
---

Harness Engineering
A harness is everything between the model weights and the world: the loop, the context it assembles, the tools and skills it can reach for, the sub-agents it can spawn, and lately the code of the harness itself. This list follows that idea from a bare while-not-EOS loop in 2019 to harnesses that rewrite themselves in 2026. Read in order, it explains why the same weight file can score 30% or 95% on the same benchmark depending only on what surrounds it.
1. The V0 harness
Before anything deserved the name, a harness was a sampling loop and a prompt. These three papers are the whole of it: the bare loop, then the two things you can do without ever leaving the context window, which are to put examples in it and to let the model spend more tokens thinking inside it.
- 01Language Models are Unsupervised Multitask Learners Alec Radford et al. · 2019The V0 harness, and the baseline every later entry is measured against. There is no tool calling here, no skills, no memory: a while-not-EOS loop, top-p sampling, and an environment that scores whatever comes after the delimiter. The talk opens the history here precisely because so little is present, which makes the next six years legible as one move repeated, giving the loop something new it is allowed to do.
- 02Language Models are Few-Shot Learners Tom B. Brown et al. · 2020The first thing anyone ever put in a harness. Nothing about the loop changes here: you simply paste solved examples above the question and accuracy moves. That makes the context window the first place a system designer can spend effort, and every technique further down this list is a descendant of that realisation.
- 03Chain-of-Thought Prompting Elicits Reasoning in Large Language Models Jason Wei et al. · 2022Smear the computation over more tokens instead of demanding the answer in one. This is the first output-space intervention in the lineage, and the reason every harness since budgets tokens rather than calls.
2. Static harnesses: growing the action space
The next six years are one move repeated: give the loop something new it is allowed to do. Search the web, call a tool, act and observe, critique itself, run code, spawn a peer, write a skill, edit its own memory, recurse. The harness gets more functional; the harness code stays fixed.
- 04WebGPT: Browser-assisted question-answering with human feedback Reiichiro Nakano et al. · 2021The first time the loop reached outside itself. WebGPT gives a model a browser and human feedback on how it used one, which turns retrieval from a preprocessing step into an action the model chooses to take.
- 05Toolformer: Language Models Can Teach Themselves to Use Tools Timo Schick et al. · 2023Where tool calling comes from. Instead of computing five minus three in the weights, the model emits a call and the harness runs it. Declare the tools in the system prompt and the action space is suddenly whatever you are willing to execute.
- 06ReAct: Synergizing Reasoning and Acting in Language Models Shunyu Yao et al. · 2022Interleave a thought and an action instead of choosing between them. ReAct is the shape almost every agent loop still has, and the talk's point is that models now do this natively, so a modern harness should stop imposing it.
- 07Self-Refine: Iterative Refinement with Self-Feedback Aman Madaan et al. · 2023The cheapest feedback loop there is: the same model grades its own draft and rewrites it, with no extra training and no environment. This is the internal evaluator in the slide's diagram, the branch that never leaves the harness.
- 08Reflexion: Language Agents with Verbal Reinforcement Learning Noah Shinn et al. · 2023Take the real reward signal from the environment and write it back into the context as words. Reflexion is where a failed episode stops being wasted, which is the seed of everything in the self-improving half of this list.
- 09InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback John Yang et al. · 2023Once the action is code, the tool list stops being finite. InterCode makes the interactive coding loop a standard environment with execution feedback, which is the direct ancestor of the persistent REPL that Prime Agent builds its whole design on.
- 10Multi-Agent Collaboration: Harnessing the Power of Intelligent LLM Agents Yashar Talebirad, Amirhossein Nadiri · 2023Spawning another agent becomes just another tool call. The framing here, agents with roles that persist and can be addressed, is what makes sub-agents an addressable resource rather than a one-shot fan-out.
- 11Voyager: An Open-Ended Embodied Agent with Large Language Models Guanzhi Wang et al. · 2023Where skills come from. Voyager chains tools into a routine, verifies it worked in Minecraft, and writes it back to a library the agent searches later. Read the skill library section and you are reading the design of the SKILLS.md sitting in your repo today.
- 12MemGPT: Towards LLMs as Operating Systems Charles Packer et al. · 2023Before this, context could only be appended to. MemGPT gives the model create, read, update, and delete over a carved-out region of its own context, which is the move that turns a transcript into managed state.
- 13Recursive Language Models Alex L. Zhang, Tim Kraska, Omar Khattab · 2025The recursion that closes out the static era. An LLM call inside a REPL can issue further LLM calls over slices of a document too big to read, so context stops being a wall and becomes a resource you program against. Prime Agent is built directly on this abstraction.
3. Let the harness learn
Then the fixed part stops being fixed. First the prompt becomes something you optimize, then the scaffolding, then the harness code itself, and finally the whole thing adapts online while it runs.
- 14DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines Omar Khattab et al. · 2023The first entry where the harness stops being hand-written. You cannot backpropagate through a prompt, so DSPy searches over prompts against a small train set instead, and the system prompt becomes an optimised artifact rather than an author's guess.
- 15GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning Lakshya A Agrawal et al. · 2025The optimiser the OpenJarvis talk reaches for. GEPA reads its own failed traces in natural language and mutates the prompt from what it saw, beating reinforcement learning at a fraction of the rollouts. Reflexion's idea, with a proper search loop around it.
- 16Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents Jenny Zhang et al. · 2025Now the harness code itself is the thing being edited. Agents sample from an archive of their own ancestors, rewrite their own scaffolding, get scored on coding benchmarks, and go back into the archive. Empirical validation replaces the original Gödel machine's proof requirement.
- 17Meta-Harness: End-to-End Optimization of Model Harnesses Yoonho Lee et al. · 2026The meta harness: a harness whose job is producing harnesses. A coding agent is handed the full search history, source, traces, and scores, and rewrites the retrieval, memory, and prompt-assembly code around a fixed model. State of the art on Terminal-Bench 2 without touching the weights.
- 18Continual Harness: Online Adaptation for Self-Improving Foundation Agents Seth Karten et al. · 2026The last step before online learning. Continual Harness keeps history, memory, skills, prompts, and sub-agent specs across trajectories and mutates them while the agent runs, then goes further and updates the weights DAgger-style from what just happened. The presenter calls test-time training the direction that matters most.
4. Harnesses shipped in 2026
Two systems presented at the paper club, built on everything above. Both are open source, and both are arguments about where the harness boundary should sit.
- 19Prime Agent Seth Karten et al. · 2026The first of the night's three talks, and the clearest statement of the thesis. A persistent IPython REPL, recursive sub-agents that stay addressable after they finish, and continual refinement of prompts and skills. On identical weights it takes ARC-AGI-3 from 30% to 95.5%, which is the number the whole evening is arguing about.
- 20OpenJarvis: Personal AI, On Personal Devices Jon Saad-Falcon et al. · 2026The same argument pointed at your laptop. Decompose the personal AI stack into five primitives, then let a frontier cloud model search over that spec while everything runs locally at inference. Roughly 800x lower marginal cost, with the harness rather than the model closing the gap.
5. How you know any of this worked
The measurement paper behind the trend line everyone cites. Harness progress only counts if the horizon a system can work over is actually getting longer.
- 21Measuring AI Ability to Complete Long Software Tasks Thomas Kwa et al. · 2025The trend line the talk opens on. Measuring capability as the length of task a system completes, rather than a single-turn score, is what makes harness progress visible at all: the static-harness era and the self-improving era are two slopes on this chart.
Keep learning
New harness research and practical labs. Occasional email.
Beyond the papers
Everything else the night pointed at: the code you can actually run and the benchmark the harness gap shows up on.
- Prime Agent (GitHub) ↗The harness behind the 95.5% ARC-AGI-3 result, with the verifiers package used to reproduce the evals.
- OpenJarvis (GitHub) ↗The on-device personal AI stack, including the five-primitive spec that the cloud model optimizes.
- QM, YC's multiplayer agent harness (GitHub) ↗The third talk of the night. No paper: YC's internal work harness, open sourced under MIT, with the brain pulled out of the sandbox and into Postgres.
- ARC-AGI-3 ↗The benchmark used throughout the night to show a harness gap on identical weights, from 30% baseline to 95.5%.
- Darwin Gödel Machine (GitHub) ↗Reference implementation of the self-modifying agent archive.
- Meta-Harness (GitHub) ↗Reference code for the harness that searches over harnesses.
- DSPy ↗The framework the prompt-optimization half of this list is built on, and where GEPA ships.
