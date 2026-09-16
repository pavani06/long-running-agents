---
url: "https://github.com/mattpocock/skills/pull/1083"
key: "d726b6e64d38"
status: "ok"
final_url: "https://github.com/mattpocock/skills/pull/1083"
method: "trafilatura"
content_hash: "2f60c4c779174f91e9f5e2143021aaad737a5d29"
text_len: 2866
fetched: "2026-09-16"
---

retro: push mechanical coding-standards findings toward deterministic checks - #1083
Merged
Merged
Conversation
… checks
retro currently treats every reviewer-agent gap the same way: write a new
CODING_STANDARDS.md line. That's fine for judgement calls, but for fixed
syntactic patterns it just asks the reviewer agent to re-derive the same
call on every future diff, forever, instead of paying once for a check.
Adds two things to the Automated checks / Coding standards categories:
- Automated checks now treats an un-linted repo (no pre-commit hook, no CI
  job running lint/typecheck/test) as a finding in its own right, not just
  a consequence of a specific mistake.
- Coding standards now classifies a violation as mechanical (deterministic
  check) vs. judgement call (CODING_STANDARDS.md) before writing a finding,
  and defaults to building the check.
Kept language-agnostic (no ESLint/ts-specific naming) since retro runs
across repos in different languages. No em-dashes, per this repo's prose
rule in CLAUDE.md.
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
| 🦋 Changeset detected Latest commit: 6942bff The changes in this PR will be included in the next version bump. This PR includes changesets to release 1 package Not sure what this means? Click here to learn what changesets are. Click here if you're a maintainer who wants to add another changeset to this PR | 
| Name | Type | 
|---|---|
| mattpocock-skills | Patch | 
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
  This was referenced Sep 15, 2026 
      
  This was referenced Sep 16, 2026 
      
  
    
      This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
      Learn more about bidirectional Unicode characters
    
  
  
    
  
    Sign up for free
    to join this conversation on GitHub.
    Already have an account?
    Sign in to comment
  
Add this suggestion to a batch that can be applied as a single commit.This suggestion is invalid because no changes were made to the code.Suggestions cannot be applied while the pull request is closed.Suggestions cannot be applied while viewing a subset of changes.Only one suggestion per line can be applied in a batch.Add this suggestion to a batch that can be applied as a single commit.Applying suggestions on deleted lines is not supported.You must change the existing code in this line in order to create a valid suggestion.Outdated suggestions cannot be applied.This suggestion has been applied or marked resolved.Suggestions cannot be applied from pending reviews.Suggestions cannot be applied on multi-line comments.Suggestions cannot be applied while the pull request is queued to merge.Suggestion cannot be applied right now. Please check back later.
