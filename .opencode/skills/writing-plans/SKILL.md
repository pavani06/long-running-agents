---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code. Writes comprehensive implementation plans with exact file paths, code, tests, and bite-sized tasks. Triggers on "create a plan", "implementation plan", "write a plan", "task breakdown", or when given specs/requirements for a multi-step change.
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Scope Check

If the spec covers multiple independent subsystems, suggest breaking into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for.

- Design units with clear boundaries and well-defined interfaces.
- Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together.
- In existing codebases, follow established patterns.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

## Plan Document Header

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.js`
- Modify: `exact/path/to/existing.js:123-145`
- Test: `tests/exact/path/to/test.js`

- [ ] **Step 1: Write the failing test**
```js
test('specific behavior', () => {
    const result = functionUnderTest(input);
    expect(result).toBe(expected);
});
```

- [ ] **Step 2: Run test to verify it fails**
Run: `npm test -- tests/path/test.js`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**
```js
export function functionUnderTest(input) {
    return expected;
}
```

- [ ] **Step 4: Run test to verify it passes**
Run: `npm test -- tests/path/test.js`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add tests/path/test.js src/path/file.js
git commit -m "feat: add specific feature"
```
```

## No Placeholders

Every step must contain actual content. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code)
- Steps that describe what to do without showing how

## Remember
- Exact file paths always
- Complete code in every step
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Self-Review

After writing the complete plan:

1. **Spec coverage:** Can you point to a task for each requirement? List any gaps.
2. **Placeholder scan:** Search for red flags from the "No Placeholders" section.
3. **Type consistency:** Do types, signatures, and names match across tasks?

Fix issues inline. If you find a spec requirement with no task, add the task.

## Execution Handoff

After saving the plan:

**"Plan complete and saved to `docs/plans/<filename>.md`.**

To execute, open a new session or continue in this one. Each task in the plan is self-contained and can be implemented independently. Tasks are ordered by dependency — work sequentially or delegate parallel tasks."

Source: Adapted from obra/superpowers writing-plans skill
