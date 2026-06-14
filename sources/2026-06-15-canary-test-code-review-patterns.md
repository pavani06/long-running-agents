# Code Review Patterns for AI-Assisted Development

A talk on practical patterns for integrating AI into code review workflows.

## Pattern 1: The Pre-Commit Gate

Before pushing any code, run the AI reviewer as a local pre-commit hook. This catches
obvious issues (unused imports, missing type annotations, security anti-patterns) before
they reach CI. The key insight: AI reviewers are fast but shallow — use them as a first
pass, not the only pass.

Configure your pre-commit to call the AI with a prompt that includes the diff and asks
for three specific things: potential bugs, style violations against your project's
conventions, and security concerns. This triage approach means the human reviewer
focuses on architecture and design decisions, not linting.

Common failure mode: developers start ignoring the AI output because it's too noisy.
Fix this by tuning the prompt to match your team's actual conventions, not generic
best practices. The AI should enforce YOUR rules, not industry defaults.

## Pattern 2: Review Contract as Checklist

Every PR should include a review-contract.yaml file that lists exactly what the
reviewer should check. This turns the review from "look at this code" into "verify
these 5 specific properties hold."

The contract includes: security surface changes, data model migrations, API
compatibility, error handling coverage, and test coverage for new paths. Each item
has a pass/fail/not-applicable status.

This pattern eliminates the "I didn't know I was supposed to check that" problem.
It also makes AI reviewers more effective because they can process each contract
item independently, returning structured results instead of freeform commentary.

## Pattern 3: Shadow Review Pipeline

Run the AI reviewer in parallel with human review for two weeks without blocking
merges. Track agreement rates: where did the AI catch something the human missed?
Where did the AI flag false positives? After the shadow period, use the data to
decide which AI checks are reliable enough to block merges.

The shadow pipeline runs on every PR but only logs results to a dashboard. This
de-risks adoption because no one's workflow changes until there's data proving the
AI adds value. Teams typically find that AI catches 30-40% of issues humans miss,
while generating false positives on 15-20% of flags.

## Pattern 4: Contextual Severity Calibration

Not all code paths have the same risk profile. A change to the payment module
deserves stricter review than a change to the help page copy. The AI reviewer
should calibrate its severity levels based on which module changed.

Implement this by maintaining a risk-profile.yaml in each module directory that
declares the module's risk level (critical, high, medium, low) and the specific
checks that apply. The AI reviewer reads this profile before analyzing the diff
and adjusts its output accordingly. A low-risk module might get only style checks,
while a critical module gets full security, performance, and data integrity checks.
