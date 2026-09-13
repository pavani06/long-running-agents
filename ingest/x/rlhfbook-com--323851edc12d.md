---
url: "https://rlhfbook.com/"
key: "323851edc12d"
status: "ok"
final_url: "https://rlhfbook.com/"
method: "trafilatura"
content_hash: "34caaab519998d778ed415f44acf3fd68289e57f"
text_len: 5993
fetched: "2026-09-13"
---

A short introduction to RLHF and post-training focused on language models.
Reinforcement learning from human feedback (RLHF) has become a crucial tool to build the latest machine learning systems at scale. The field grew around the core methods of RLHF into today’s broader suite of post-training techniques. In this book, we give a comprehensive introduction to the core methods for post-training models for people with some level of quantitative background, organized around the canonical RLHF recipe. The book starts with what RLHF does and why it was created, with seminal technical milestones in its young history and a primer on reinforcement learning context needed to understand the book. The core of the book details every optimization stage in using RLHF, from starting with instruction tuning to training a reward model and finally all of rejection sampling, reinforcement learning, on-policy distillation, and direct alignment algorithms. The book also discusses broader topics, such as the origins of RLHF – both in recent literature and in a convergence of disparate fields of science in economics, philosophy, and optimal control. The book concludes with advanced topics – understudied or emerging research questions in synthetic data, tool-use, character training, and evaluation – and open questions for the field. The book is released with a variety of companion resources, including a codebase, a library to compare model completions from within post-training stages, and an educational course, to be a one-stop shop for learning all foundational concepts for post-training language models.
The book will be re-printed roughly 2 and 6 months after the initial print in July 2026. This section tracks the differences between the web version and the physical book, and will be updated to note which improvements or fixes make it into which print version.
Content additions and fixes:
- Expanded the canonical training recipes with MOPD and agentic post-training examples, plus new pipeline figures (Chapter 3) — #529.
- Added a short subsection on agentic evaluation (Chapter 16) — #492.
- Clarified the history of outcome reward models, fixed some loose language, and reorganized the reward modeling chapter (Chapter 5) — #516.
- Cleaned up RL notation, especially the trajectory sampling distribution and time indexing (Chapter 6) — #466.
- Expanded the on-policy distillation section, particularly more on self-distillation and OPSD (Chapter 12) — #439.
Organizational improvements:
- Renamed Chapter 12 to "Synthetic Data & Distillation" — #469.
- Reordered the regularization chapter for better flow (Chapter 15) — #486.
Typos and minor fixes:
Book overview & course introduction
A codebase for the algorithms in this book
Compare model completions at post-training stages
Discuss the book on Discord
Unofficial translations maintained by readers, independent of the official print editions
I would like to thank the following people who helped me directly with this project: Costa Huang, Ross Taylor, Hamish Ivison, John Schulman, Valentina Pyatkin, Daniel Han, Shane Gu, Joanne Jang, LJ Miranda, Sharan Maiya, Andrew Carr, Cameron R. Wolfe, and others in my RL sphere (and of course Claude).
Additionally, thank you to the contributors on GitHub who helped improve this project.
Last built: 11 September 2026
August 2026: Finished accompanying course, Amazon sales begin.
July 2026: The print, ePub, and liveBook editions were published by Manning.
April 2026: Final editorial polish for print — ported Manning edition improvements, clarity pass on equations and terminology, typo/grammar fixes across all chapters, product chapter expansions. The book is heading to print, so expect fewer content changes going forward.
March 2026: Launch course page with lecture videos; PDF syntax highlighting; product chapter expansions (Ch. 17).
February 2026: v2 content: direct alignment chapter, new diagrams, RL cheatsheet, appendices, search bar, Kindle support, editor fixes.
January 2026: Major chapter reorganization to match Manning book structure; code examples library; old URLs redirect to new locations.
December 2025: Working on v2 of the book based on editors' feedback. Check back for updates!
November 2025: Manning preorder available.
July 2025: Add tool use chapter (see PR)
June 2025: v1.1. Lots of RLVR/reasoning improvements (see PR)
April 2025: Finish v0; overoptimization, open questions, etc.; evaluation section; RLHF x Product research, improving website, reasoning section.
March 2025: Improving policy gradient section; finish DPO, major cleaning; start DPO chapter, improve intro.
February 2025: Improve SEO, add IFT chapter; RM additions, preference data, policy gradient finalization; PPO and GAE; added changelog, revamped introduction.
January 2025: Policy gradients (REINFORCE, PPO, GRPO); overoptimization content; discussion content merged from the blog; navigation and code-listing improvements.
December 2024: Preferences chapter; continued cleaning and additions.
October 2024: Regularization, preferences, and reward modeling chapters; figures and formatting.
August 2024: First chapters drafted (rejection sampling, bibliography); automated site builds set up.
May 2024: rlhfbook.com domain purchased; project started.
If you found this useful for your research, please cite it!
For the web and arXiv version:
@misc{lambert2025reinforcementlearninghumanfeedback,
  title = {Reinforcement Learning from Human Feedback},
  author = {Nathan Lambert},
  year = {2025},
  eprint = {2504.12501},
  archivePrefix = {arXiv},
  primaryClass = {cs.LG},
  url = {https://arxiv.org/abs/2504.12501}
}
    For the Manning edition:
@book{lambert2026reinforcement,
  author = {Nathan Lambert},
  title = {Reinforcement Learning from Human Feedback: Alignment and post-training of {LLMs}},
  year = {2026},
  publisher = {Manning Publications},
  isbn = {9781633434301},
  url = {https://www.manning.com/books/reinforcement-learning-from-human-feedback}
}
