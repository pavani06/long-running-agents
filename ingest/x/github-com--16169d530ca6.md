---
url: "https://github.com/ayghri/i-have-adhd"
key: "16169d530ca6"
status: "ok"
final_url: "https://github.com/ayghri/i-have-adhd"
method: "trafilatura"
content_hash: "03fa5f0a10c6cf5631dff709858b656f2d866a93"
text_len: 1449
fetched: "2026-09-13"
---

ADHD-friendly outputs. No ADHD diagnosis needed!
🇬🇧 · 🇨🇳 · 🇧🇷 · 🇯🇵 · 🇻🇳 · 🇰🇷 · 🇹🇭
Copy/paste into your CLI prompt:
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
Or 🔗 check the installation instructions.
A skill for your coding assistant that stops it from burying the answer. Action first. Steps numbered. No "Hope this helps!"
|   |  src/auth.tsverifyToken (lines 42–58) with the snippet belownpm test -- auth.spec.ts | 
10 rules. Full text in SKILL.md.
- Lead with the next action.
- Number multi-step tasks.
- End with one concrete next step.
- Suppress tangents.
- Restate state every turn.
- Specific time estimates (minutes, not "a bit").
- Make wins visible.
- Matter-of-fact errors.
- Cap lists to 5 items.
- No preamble. No recap. No closers.
Fork, edit skills/i-have-adhd/SKILL.md, then swap your copy in:
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
Restart Claude Code, then re-invoke /i-have-adhd.
Loosely based on The Adult ADHD Tool Kit by J. Russell Ramsay and Anthony L. Rostain. Adapted for how an LLM should respond, not how a human should organize their day.
MIT.
Star ⭐ if it saved you one scroll past one "Great question!"
