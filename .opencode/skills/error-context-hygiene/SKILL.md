---
name: error-context-hygiene
description: "Apply Error Context Hygiene rules when implementing agent error handling. Summarize errors instead of dumping stack traces; clear pending errors after successful recovery; never blind-append errors to context. Use when implementing tool error handling, retry loops, agent fallback logic, or context window management. Triggers: 'error context', 'error hygiene', 'context pollution', 'retry loop feedback', 'tool error handling', 'agent error recovery'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: implementation
  priority: high
  source: "12-Factor Agents (Dex Horthy, AI Engineer 2025)"
---

## What I Do

I ensure agent error handling doesn't pollute the context window. I enforce four rules:

1. **Summarize, don't dump** — Convert raw errors into one-line structured summaries
2. **Clear on success** — Remove all error context after a valid tool call succeeds
3. **Never blind-append** — Every error entering context must be deliberately formatted and size-controlled
4. **Keep only what's needed** — The model needs actionable hints, not forensic records

## When to Use Me

Load this skill when:

- Implementing tool error handling in any agent (LangChain, LangGraph, or custom harness)
- Adding retry logic to agent tool calls
- Diagnosing agent spiral-out or context pollution from accumulated errors
- Reviewing agent code for context management quality
- Designing a new agent harness or control loop

## The Anti-Pattern

```typescript
// ANTI-PATTERN: Blind append — will pollute context
try {
  const result = await tool.invoke(args);
  messages.push(new ToolMessage({ content: JSON.stringify(result) }));
} catch (error) {
  messages.push(new ToolMessage({
    content: `Error: ${error.message}\n${error.stack}`  // ← 40-line stack trace
  }));
}
```

This causes:
- Tokens wasted on stack traces the model can't use
- Model learning that "errors are normal" → spiral-out
- Stale errors lingering after recovery

## The Pattern

```typescript
// Error Context Hygiene
try {
  const result = await tool.invoke(args);
  messages.push(new ToolMessage({ content: JSON.stringify(result) }));
  // RULE 2: Clear pending errors on success
  clearPendingErrors(messages);
} catch (error) {
  // RULE 1: Summarize, don't dump
  const summary = summarizeError({
    tool: tool.name,
    errorType: classifyError(error),
    hint: deriveHint(error),
  });
  // Format: "[error] <tool>: <type>. <hint>"
  messages.push(new ToolMessage({ content: `[error] ${summary}` }));
}
```

## Error Summarizer Rules

### classifyError()

| Error Pattern | Classification |
|---|---|
| Connection refused, timeout, ECONNREFUSED | `connectivity` |
| 400, validation error, schema mismatch | `bad_request` |
| 401, 403, unauthorized | `auth` |
| 404, not found | `not_found` |
| 429, rate limit | `rate_limit` |
| 500, internal server error | `upstream` |
| Unknown | `unknown` |

### deriveHint()

Generate one actionable sentence:

| Error Type | Hint Template |
|---|---|
| `connectivity` | "Retrying with same parameters." |
| `bad_request` | "Check parameter format." |
| `auth` | "Escalate to human — credentials needed." |
| `not_found` | "Try broader search or different category." |
| `rate_limit` | "Wait %d seconds and retry." |
| `upstream` | "Fallback to alternative data source." |
| `unknown` | "Log for investigation; continue with available data." |

### Format

Always: `[error] <tool_name>: <error_type>. <hint>`

Maximum one line. No stack traces. No API response bodies. No HTTP headers.

## Recovery Rules

### After retry succeeds

When a tool call fails, then a subsequent call (same tool or different) succeeds:

```typescript
function clearPendingErrors(messages: BaseMessage[]): void {
  // Remove all [error] ToolMessages from the array
  const cleaned = messages.filter(m => {
    if (m instanceof ToolMessage) {
      return !String(m.content).startsWith('[error]');
    }
    return true;
  });
  // Replace array in place
  messages.length = 0;
  messages.push(...cleaned);
}
```

### After recovery, inject acknowledgment

After clearing errors, inject a brief acknowledgment so the model knows recovery happened:

```
[recovered] Previous tool errors resolved. Proceeding with task.
```

This is optional but helps the model transition from error-handling to task-execution mode.

## Retry Loop Integration

```typescript
async function executeWithHygiene(
  tool: DynamicStructuredTool,
  args: Record<string, unknown>,
  maxRetries: number = 3
): Promise<ToolResult> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const result = await tool.invoke(args);
      return { success: true, result };
    } catch (error) {
      if (attempt === maxRetries - 1) {
        // Final attempt failed — return summarized error
        return {
          success: false,
          errorSummary: summarizeError({
            tool: tool.name,
            errorType: classifyError(error),
            hint: "Max retries exceeded. Escalate or use fallback.",
          }),
        };
      }
      // Will retry — context hygiene handled by caller
      continue;
    }
  }
}
```

## Integration with Existing Repo Infrastructure

The mhc-backend already has 10 fallback mechanisms. Add error context hygiene on top:

| Existing | Add Context Hygiene |
|---|---|
| `try/catch` in `OrchestratorAgent` → generic fallback message | Before fallback: summarize error, inject hint into messages[] |
| `MemoryExtractionService` → `.catch()` silent swallow | Emit `[error] memory_extraction: non-blocking failure. Agent proceeds without memory.` |
| `ConversationStateBuilder` → fallback: "agent will run without context" | Format consistently: `[error] state_build: <specific query failed>. Agent proceeds with partial context.` |

## Quality Gates

Before declaring error handling complete, verify:

- [ ] No raw `error.stack` enters any `ToolMessage` or prompt
- [ ] All error messages are ≤ 1 line
- [ ] All error messages use the `[error]` prefix format
- [ ] Pending errors are cleared after a successful tool call
- [ ] The retry loop injects hints, not just "trying again"
- [ ] Silent catches (`.catch() {}`) emit at minimum a one-line classification

## References

- `docs/canonical/error-context-hygiene.md` — canonical pattern description
- `docs/analysis/2026-06-09-pattern-classification.md` — classification as Missing
- `docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md:320` — "sem retry loop com feedback"
- `docs/analysis/mhc-backend/2026-05-26-nivel-2-diagnostic.md` — multi-point gap analysis

---

*Created: 2026-06-09 | Source: 12-Factor Agents pattern classification*
