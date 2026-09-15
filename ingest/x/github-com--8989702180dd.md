---
url: "https://github.com/anthropics/claude-code/issues/91870#issuecomment-5666255143"
key: "8989702180dd"
status: "ok"
final_url: "https://github.com/anthropics/claude-code/issues/91870#issuecomment-5666255143"
method: "trafilatura"
content_hash: "36ddd9816d6d4383ebe4a0c5d5314062c4e4043b"
text_len: 5214
fetched: "2026-09-15"
---

- 
                Notifications
    You must be signed in to change notification settings
- Fork 23.2k
Mods - make Claude 10x more extensible #91870
Description
Community Update: Sep 9, 2026
AI;DR: We're shipping in N weeks.
Thank you all for the positive feedback, and especially for the insightful, high-signal feedback that has materially shaped our design.
We're now committed to shipping function hooks, on the scale of weeks in lieu of days or months. As well, from a product perspective, we are going to be calling this functionality "Claude Mods". The engineering term of art 'function hook' will still exist as the documented implementation primitive Mods are built on. A mod is just a plugin that uses function hooks, nothing is changing there. Hopefully the ontology is not too confusing.
We're still rapidly iterating on the interface, design, etc. but much of the semantics are now set in place, and we don't anticipate as many breaking changes as our first week. Therefore, we've made available our source listings for our first three built-in mods, perusable here. Our intent is to take further extant features as they exist in CC today and migrate them to mod form.
Finally, I'm sharing here a cheat sheet reference that enumerates some affordances on v267/v268 (today / tomorrow). As well, I may now publicly acknowledge that any folks who want to test and give feedback may use CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude.
We are still iterating and it is only more important for the community to engage and give critical feedback to ensure this ends up in the right shape. Thank you all.
Original Post: Sep 3, 2026
Hi folks! ✨
AI;DR: Function Hooks let you modify CC very deeply, while still being safe through side-effect tracking over a parameterized $ object, and while composing neatly using a registration-order-based 'next' continuation model a la Express, or Koa.
I was asked to get feedback from the community regarding an internal proposal we have.
Basically, it would be neat if you could hook into CC using TypeScript functions a la Express (or Koa!), and basically change whatever you want. So that's what we're proposing. In the workplace, admins will be able to change what they want too, including your ability to change things, to a very fine level of programmatic detail.
You should even be able to modify how components get rendered. We use React across the board, so why not utilize that fact?
There's a technical architecture doc, that goes through some of the design. As well, I made a few videos for internal folks so they could see how it might feel, which I'm sharing here too. I've tried to ensure that they're informative and engaging.
Algebraically, this is just an effect-parameterized endomorphic continuation model for plugins.
If you want this, please engage here - the response from the community likely dictates whether this ships or not. The $ sigil isn't negotiable though, I follow a more ancient god.
Basic Series
You can either click on the thumbnails or the inline video toggles below. Each Basic and Advanced video is 60 seconds; the full Case Study videos are around 2 minutes long and show more comprehensive uses of function hooks to form cohesive features.
| 1-a-hook-as-a-function.mp4 | 2-a-hook-that-says-no.mp4 | 3-plugins-can-draw-now.mp4 | 4-admin-control-as-a-hook.mp4 | 
⚠️ GitHub mutes videos by default, so be sure to turn sound on.
The four videos
⓵ A hook as a function
We introduce the ability for hooks to be TypeScript functions, with full type definitions and LSP support.
1-a-hook-as-a-function.mp4
⓶ A hook that says no
Function hooks may be used to restrict behavior, for safety and control, as you're used to.
2-a-hook-that-says-no.mp4
⓷ Plugins can draw now
You can hook onto components and modify their props or wrap their returned render nodes.
3-plugins-can-draw-now.mp4
⓸ Admin control as a hook
Admins can remove affordances from $ so that all plugins below cannot invoke that side-effect.
4-admin-control-as-a-hook.mp4
Advanced Series
| 5-order-is-nesting.mp4 | 6-press-a-plugins-button.mp4 | 7-every-event-at-once.mp4 | 
The three videos
⓹ Order is nesting
Plugins nest like middleware. The first one registered wraps the rest, so admins prepend for control and append for defaults.
5-order-is-nesting.mp4
⓺ Press a plugin's button
Hooks catch interactions too. One hook on ui.press sees the same button pressed in the terminal and in the desktop app.
6-press-a-plugins-button.mp4
⓻ Every event at once
A single hook on * sees every event, including every plugin's own calls on $, so an audit log is one function.
7-every-event-at-once.mp4
Case Studies
| 8-one-sentence-one-plugin.mp4 | 9-change-what-claude-code-shows.mp4 | 
The two videos
⓼ One sentence. One plugin
From one short ask, Claude writes, validates and loads a plugin that replaces secrets in tool output before the model reads them.
8-one-sentence-one-plugin.mp4
⓽ Change what Claude Code shows
A plugin hides sensitive values in Claude Code Desktop until you hover over them, so you can share your screen without showing your data.
9-change-what-claude-code-shows.mp4
AI usage disclosure
thumbnails are AI; demos and code are real, running on actual binaries
