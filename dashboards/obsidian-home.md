---
title: "Obsidian Home"
type: index
aliases: ["home", "inicio", "moc"]
tags: ["index", "curriculo-conteudo", "analise"]
last_updated: "2026-06-10"
---

# Obsidian Home

Main dynamic MOC for the vault.

## Canonical Patterns

```dataview
TABLE file.link AS Pattern, aliases, tags, last_updated
FROM "docs/canonical"
SORT last_updated DESC
```

## Recent Analyses

```dataview
TABLE file.link AS Analysis, date, domain, tags
FROM "docs/analysis"
SORT date DESC
LIMIT 10
```

## Curriculum Overview

### Nivel 1

```dataview
TABLE file.link AS Lesson, aliases, tags
FROM "curriculum/01-nivel-1-fundamentals"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

### Nivel 2

```dataview
TABLE file.link AS Lesson, aliases, tags
FROM "curriculum/02-nivel-2-practical-patterns"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

### Nivel 3

```dataview
TABLE file.link AS Lesson, aliases, tags
FROM "curriculum/03-nivel-3-advanced-architecture"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

### Nivel 4

```dataview
TABLE file.link AS Lesson, aliases, tags
FROM "curriculum/04-nivel-4-koda-specific"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

## Quick Links

- [[index|Root Index]]
- [[curriculum/INDEX|Curriculum Index]]
- [[docs/system-of-record|System of Record]]

## Recently Updated

```dataview
LIST FROM "docs/canonical" OR "docs/analysis" OR "curriculum"
WHERE last_updated
SORT last_updated DESC
LIMIT 10
```
