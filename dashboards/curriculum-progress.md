---
title: "Curriculum Progress"
type: index
aliases: ["progresso", "curriculo dashboard"]
tags: ["index", "curriculo-conteudo"]
last_updated: "2026-06-10"
---

# Curriculum Progress

## By Level

### Nivel 1

```dataview
TABLE file.link AS Lesson, aliases, tags, last_updated
FROM "curriculum/01-nivel-1-fundamentals"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

### Nivel 2

```dataview
TABLE file.link AS Lesson, aliases, tags, last_updated
FROM "curriculum/02-nivel-2-practical-patterns"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

### Nivel 3

```dataview
TABLE file.link AS Lesson, aliases, tags, last_updated
FROM "curriculum/03-nivel-3-advanced-architecture"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

### Nivel 4

```dataview
TABLE file.link AS Lesson, aliases, tags, last_updated
FROM "curriculum/04-nivel-4-koda-specific"
WHERE type = "curriculum-lesson"
SORT file.name ASC
```

## Exercises

```dataview
LIST FROM "curriculum"
WHERE type = "curriculum-exercise"
SORT nivel ASC, file.name ASC
```

## Solutions

```dataview
LIST FROM "curriculum"
WHERE type = "curriculum-solution"
SORT nivel ASC, file.name ASC
```

## Implementation Guides

```dataview
TABLE file.link AS Guide, aliases, tags, last_updated
FROM "curriculum/07-implementation-guides"
WHERE type = "curriculum-guide"
SORT file.name ASC
```

## Case Studies

```dataview
TABLE file.link AS CaseStudy, aliases, tags, last_updated
FROM "curriculum/09-case-studies"
WHERE type = "curriculum-case-study"
SORT file.name ASC
```
