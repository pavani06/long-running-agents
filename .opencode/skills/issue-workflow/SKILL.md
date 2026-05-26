---
name: issue-workflow
description: Manage GitHub Issues through full lifecycle: create, track, and complete. Use when (1) creating issues from story breakdowns or planning discussions, (2) starting work on a feature branch, (3) tracking progress with commits and changes, (4) completing issues and updating parent epics. Triggers on: branch names like `issue/N-slug`, keywords like "create issue" or "close issue", reading breakdown files or plans, or discussing epics/stories/tasks.
---

# GitHub Issue Workflow

Manage GitHub Issues through the full lifecycle with automatic project integration and audit trail.

## MANDATORY BEHAVIORS

### On Session Start (ALWAYS)
1. Detect issue number from branch or ask user
2. Fetch issue details and display context
3. Add `in-progress` label
4. Post "Starting session" comment with work plan

### During Work (AFTER EACH SIGNIFICANT CHANGE)
1. Update acceptance criteria checkboxes when completed
2. Post progress comment for: bug fixes, decisions, blockers

### On Session End (ALWAYS)
1. Post handoff comment with completed/pending/next steps
2. Update any remaining checkboxes
3. If blocked, add `blocked` label and document why

### On Issue Completion (ALWAYS)
1. Verify all acceptance criteria are checked
2. Remove `in-progress` label
3. Post completion comment
4. Close issue (or let PR close it)

---

## Phase 1: Issue Creation

Trigger: keywords like "create issue", "create epic", "add issues", or reading breakdown/plan files.

### Epic Template

```bash
gh issue create \
  --title "Epic: <Title>" \
  --body "$(cat <<'EOF'
## Summary
<1-2 sentence description>

## Scope
- <Key deliverable 1>
- <Key deliverable 2>

## Success Criteria
- [ ] <Measurable outcome 1>
- [ ] <Measurable outcome 2>
EOF
)"
```

### Sub-Issue Template

```bash
gh issue create \
  --title "<Descriptive title>" \
  --body "$(cat <<'EOF'
## Description
<What this issue delivers>

## Acceptance Criteria
- [ ] <Criterion 1>
- [ ] <Criterion 2>
- [ ] <Criterion 3>

## Progress Log
_Updates will be posted here._
EOF
)"
```

If the issue is blocked by another, add to body:
```markdown
> **BLOCKED BY #N**: <reason>. Cannot proceed until <what needs to happen>.
```

---

## Phase 2: Working on Issues

### Issue Detection (REQUIRED FIRST STEP)

```bash
# From branch name: issue/N-slug → issue #N
BRANCH=$(git branch --show-current)
ISSUE_NUM=$(echo "$BRANCH" | grep -oE '^issue/([0-9]+)' | cut -d/ -f2)
```

### Session Start Checklist

```bash
# 1. Fetch and display context
gh issue view $ISSUE_NUM --json title,body,labels,state

# 2. Add in-progress label
gh issue edit $ISSUE_NUM --add-label "in-progress"

# 3. Post starting comment with work plan
gh issue comment $ISSUE_NUM --body "## Starting Session — $(date)

### Work Plan
- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Step 3: Final verification

### Context
- Branch: $(git branch --show-current)"
```

### Progress Logging

**For routine changes (file creation, minor edits):**
```bash
gh issue comment $ISSUE_NUM --body "Progress: created Component, updated types"
```

**For bug fixes, decisions, or blockers (DETAILED):**
```bash
gh issue comment $ISSUE_NUM --body "$(cat <<'EOF'
### Fixed: <title>
**Problem:** <what was wrong>
**Cause:** <root cause>
**Solution:** <how it was fixed>
**Files:** path/to/file.js
EOF
)"
```

### Update Checkboxes

```bash
# When criterion is complete, check it off in the issue body
gh issue edit $ISSUE_NUM --body "$(gh issue view $ISSUE_NUM --json body -q .body | sed 's/- \[ \] Criterion/- [x] Criterion/')"
gh issue comment $ISSUE_NUM --body "Completed: **Criterion name**"
```

### Session Handoff (REQUIRED)

```bash
gh issue comment $ISSUE_NUM --body "$(cat <<'EOF'
## Session Handoff — $(date)

### Completed This Session
- Item 1
- Item 2

### Acceptance Criteria Status
- [x] Criterion 1
- [ ] Criterion 2 (in progress)

### Important Context
- Technical notes, gotchas, decisions made

### Next Session
Resume with **specific task** — pick up from exact point
EOF
)"
```

---

## Phase 3: Completing Issues

### Pre-Completion Checklist

```bash
# Verify no unchecked criteria remain
UNCHECKED=$(gh issue view $ISSUE_NUM --json body -q .body | grep -c '\- \[ \]')
if [ "$UNCHECKED" -gt 0 ]; then
  echo "WARNING: $UNCHECKED unchecked items remain"
fi
```

### Completion Actions

```bash
# 1. Post completion comment with sign-off checklist
gh issue comment $ISSUE_NUM --body "## Completed — $(date)

### Summary
<1-2 sentence summary>

### Delivered
- <outcome 1>

### Sign-off
- [x] All acceptance criteria met
- [x] Code self-reviewed"

# 2. Remove work labels
gh issue edit $ISSUE_NUM --remove-label "in-progress"

# 3. Close issue
gh issue close $ISSUE_NUM
```

---

## Labels Reference

| Label | When to Add | When to Remove |
|-------|-------------|----------------|
| `in-progress` | Session start | Issue closed |
| `blocked` | When blocked | When unblocked |

## Anti-Patterns

- Start coding without posting session start comment
- Complete acceptance criteria without checking them off
- End session without handoff comment
- Close issue without completion comment
- Close issue with unchecked criteria (without explicit user approval)

## Quick Reference

```bash
# Session start
gh issue view N --json title,body,labels,state
gh issue edit N --add-label "in-progress"
gh issue comment N --body "..."

# Progress
gh issue comment N --body "Progress: ..."
gh issue edit N --body "$(gh issue view N --json body -q .body | sed 's/- \[ \] X/- [x] X/')"

# Session end
gh issue comment N --body "## Session Handoff..."

# Completion
gh issue edit N --remove-label "in-progress"
gh issue comment N --body "## Completed..."
gh issue close N
```

Source: Adapted from karanivincent/claude-code-tools issue-workflow skill
