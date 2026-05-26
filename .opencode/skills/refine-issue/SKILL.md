---
name: refine-issue
description: Break down GitHub issues into executable sub-issues with dependencies. Deep codebase exploration, single-file-focused tasks, dependency graphs, and verification gate. Use when the user mentions "refine", "break down", "decompose", or "plan" for an issue. Also triggers on: analyzing issue scope, creating implementation sub-tasks, or planning multi-step work from an existing issue.
---

# Refine Issue

## Objective

Transform a GitHub issue into a set of focused, executable sub-issues through deep codebase exploration. Each sub-issue targets a single file or tightly-coupled file pair. Sub-issues are created with blocking relationships to enable parallel work where dependencies allow.

## Context

This skill bridges high-level issues and actionable implementation work. It:

1. **Deeply researches** the codebase to understand existing patterns, dependencies, and affected areas
2. **Decomposes** work into single-file-focused sub-issues
3. **Identifies dependencies** between tasks to establish blocking relationships
4. **Creates sub-issues** as tracked work items with proper blocking order

Sub-issues are designed for autonomous execution — each should be completable without needing to reference other sub-issues.

## Workflow

### Step 1: Fetch Issue

```bash
gh issue view <ISSUE_NUMBER> --json title,body,labels,state,assignees
```

Extract:
- Title and description
- Acceptance criteria
- Labels and priority
- Existing relationships

### Step 2: Deep Exploration

Use the Explore agent or direct codebase search to understand:
- All files that will need modification
- Existing patterns in similar areas
- Dependencies between affected files
- Shared utilities, types, or services involved
- Test files that will need updates

### Step 3: Decompose into Sub-Issues

Each sub-issue should focus on ONE file (or tightly-coupled pair like component + test):

```markdown
## Sub-issue: [N] — [Brief title]

**Target file(s):** `path/to/file.js`
**Change type:** Create | Modify | Delete

### Action
[2-4 sentences of specific implementation guidance]

### Verify
```bash
npm test -- tests/path/to/test.js
```

### Acceptance Criteria
- [ ] Measurable outcome 1
- [ ] Measurable outcome 2

**Blocked by:** [Sub-issue numbers, or "None"]
**Enables:** [Sub-issue numbers this unblocks]
```

### Step 4: Determine Dependencies

Order by functional requirements:
1. **Foundation first:** Types, interfaces, schemas before implementations
2. **Dependencies flow down:** If A imports from B, B must be done first
3. **Tests with implementation:** Pair test files with their source files
4. **Verification last:** Always a final "Verification Gate" sub-issue

### Step 5: Include Verification Gate

**ALWAYS include a final Verification Gate sub-issue:**
- Title: `Verification Gate`
- Blocked by ALL implementation sub-issues
- Validates all acceptance criteria are met before parent can be completed

### Step 6: Present Breakdown

```markdown
# Implementation Breakdown: #N — Issue Title

**Total sub-issues:** X
**Parallelizable groups:** Y
**Critical path:** [sequential list]

## Dependency Graph
```
[1] Types/Interfaces
 └─► [2] Implementation
      ├─► [3] Component A
      └─► [4] Component B

[5] Verification Gate ← blocked by ALL
```

## Sub-issues
[List each sub-issue with full details]
```

### Step 7: Gather Feedback

Ask: "How would you like to proceed?"

Options:
1. **Create all sub-issues** — Breakdown looks correct
2. **Adjust scope** — Split or combine some tasks
3. **Change ordering** — Adjust dependencies
4. **Add context** — More information to include

### Step 8: Create Sub-Issues

After approval, create using `gh issue create`:

```bash
gh issue create \
  --title "[#PARENT] Sub-issue title" \
  --body "Full description with acceptance criteria" \
  --label "sub-task" \
  --assignee "@me"
```

Post a dependency graph comment on the parent issue.

## Sizing Guidelines

A well-sized sub-issue:
- Targets 1 file (or source + test pair)
- Has 2-4 acceptance criteria
- Can be described in 2-3 sentences
- Takes roughly 50-200 lines of changes

**Split if:** File needs multiple unrelated changes, description exceeds 5 sentences
**Combine if:** Two files are always modified together, changes are trivially small

## Anti-Patterns

- Don't create vague sub-issues ("Update components for feature X")
- Don't skip the research phase
- Don't over-split (separate task per function)
- Don't under-split ("Implement entire feature" as one task)
- Don't create circular dependencies

## Success Criteria

- [ ] All affected files identified through exploration
- [ ] Each sub-issue targets exactly one file (or source + test pair)
- [ ] Every sub-issue has clear, verifiable acceptance criteria
- [ ] Blocking relationships are logically sound
- [ ] No circular dependencies
- [ ] Verification Gate sub-issue created as final task
- [ ] User approved breakdown before creation

Source: Adapted from skillmd.ai refine-issue skill
