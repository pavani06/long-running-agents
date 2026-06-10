---
title: "Analysis Hub"
type: index
aliases: ["analises", "analise dashboard"]
tags: ["index", "analise", "evals"]
last_updated: "2026-06-10"
---

# Analysis Hub

## All Analyses by Date

```dataview
TABLE file.link AS Analysis, date, domain, tags
FROM "docs/analysis"
SORT date DESC
```

## By Domain

### Context Management

```dataview
TABLE file.link AS Analysis, date, domain, tags
FROM "docs/analysis"
WHERE contains(tags, "context-management")
SORT date DESC
```

### Evals

```dataview
TABLE file.link AS Analysis, date, domain, tags
FROM "docs/analysis"
WHERE contains(tags, "evals")
SORT date DESC
```

### Harness

```dataview
TABLE file.link AS Analysis, date, domain, tags
FROM "docs/analysis"
WHERE contains(tags, "harness")
SORT date DESC
```

### 12-Factor Agents

```dataview
TABLE file.link AS Analysis, date, domain, tags
FROM "docs/analysis"
WHERE contains(tags, "12-factor-agents")
SORT date DESC
```

### Production

```dataview
TABLE file.link AS Analysis, date, domain, tags
FROM "docs/analysis"
WHERE contains(tags, "production")
SORT date DESC
```

## Analysis Calendar

```dataview
CALENDAR date
FROM "docs/analysis"
```
