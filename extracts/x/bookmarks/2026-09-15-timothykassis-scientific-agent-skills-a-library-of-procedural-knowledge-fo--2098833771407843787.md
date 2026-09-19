---
title: "Biblioteca de habilidades procedurais para agentes científicos"
type: "extract"
source: "x"
status_id: "2098833771407843787"
handle: "TimothyKassis"
url: "https://x.com/TimothyKassis/status/2098833771407843787"
created_at: "2026-09-12T17:59:00.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-15-timothykassis-scientific-agent-skills-a-library-of-procedural-knowledge-fo--2098833771407843787.json]]"
tags: ["agents", "agent-context", "context-engineering", "context-management", "token-budgeting", "knowledge-management", "documentation-as-code", "repo-as-context"]
topic: "Biblioteca de habilidades procedurais para agentes científicos"
summary: "Paper de Timothy Kassis apresenta Scientific Agent Skills, biblioteca aberta com 163 procedimentos em 16 áreas (genômica, quimioinformática, imaging médico, desenho de estudos) empacotados como arquivos de instrução versionados e carregados por agentes sob demanda, com medição de custo em tokens. Vale salvar como referência concreta de como codificar conhecimento procedural de domínio de forma econômica em contexto."
key_points: ["Um agente LLM retorna código funcional, mas análise defensável depende de escolhas procedurais: qual teste o campo aceita, qual namespace de identificadores é autoritativo, quais ressalvas devem acompanhar o resultado — conhecimento que não está no modelo", "Cada skill é um diretório com arquivo de instrução versionado e legível por humanos, mais material de referência e scripts executáveis; carregado apenas quando a tarefa exige (lazy loading de contexto)", "Métricas de custo: as descrições always-resident dos 163 skills custam 7,1% de uma janela de 200k tokens; o workflow documentado mediano cabe em 23,9% dela", "Limitações honestas: sem avaliação task-level nem taxa de seleção do host; 29 de 46 workflows transbordariam a janela se todos os arquivos de referência fossem carregados — evidência de que hierarquia de carga é essencial", "Licença aberta; relevante como padrão de arquitetura para bibliotecas de skills/contexto em agentes de domínio"]
entities: ["Timothy Kassis", "Scientific Agent Skills", "arXiv"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://arxiv.org/abs/2609.00065"]
media: []
theme: "Tooling para agentes de código"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-google-if-you-maintain-a-skill-library-for--2093324233158045788|Evolução de skills em agentes]]", "[[extracts/x/bookmarks/2026-09-14-cyrilxbt-every-department-installable-developers-superpowers-https-t--2098652326248493447|Superpowers: metodologia para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-knowledge-work-is-so-much-harder-to-automate-with-agents-tha--2096906181121818702|agents em código vs conhecimento]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-baai-if-you-are-building-research-agents-t--2095539831141220620|Skills para research agents]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-just-saw-a-comment-saying-that-i-ve-never-made-a-proper-over--2088290952704151671|Visão geral das 25 skills de agentes]]", "[[extracts/x/bookmarks/2026-09-15-snwiki238337-openai-skillskill-githubskill-agent-skills-eval-skillopenai--2099052462653002157|Metodologia de avaliação de skills (OpenAI)]]"]
---

# Biblioteca de habilidades procedurais para agentes científicos

**@TimothyKassis** · [2098833771407843787](https://x.com/TimothyKassis/status/2098833771407843787) · `resource`

## Resumo
Paper de Timothy Kassis apresenta Scientific Agent Skills, biblioteca aberta com 163 procedimentos em 16 áreas (genômica, quimioinformática, imaging médico, desenho de estudos) empacotados como arquivos de instrução versionados e carregados por agentes sob demanda, com medição de custo em tokens. Vale salvar como referência concreta de como codificar conhecimento procedural de domínio de forma econômica em contexto.

## Pontos-chave
- Um agente LLM retorna código funcional, mas análise defensável depende de escolhas procedurais: qual teste o campo aceita, qual namespace de identificadores é autoritativo, quais ressalvas devem acompanhar o resultado — conhecimento que não está no modelo
- Cada skill é um diretório com arquivo de instrução versionado e legível por humanos, mais material de referência e scripts executáveis; carregado apenas quando a tarefa exige (lazy loading de contexto)
- Métricas de custo: as descrições always-resident dos 163 skills custam 7,1% de uma janela de 200k tokens; o workflow documentado mediano cabe em 23,9% dela
- Limitações honestas: sem avaliação task-level nem taxa de seleção do host; 29 de 46 workflows transbordariam a janela se todos os arquivos de referência fossem carregados — evidência de que hierarquia de carga é essencial
- Licença aberta; relevante como padrão de arquitetura para bibliotecas de skills/contexto em agentes de domínio

## Links
- https://arxiv.org/abs/2609.00065

## Entidades
Timothy Kassis, Scientific Agent Skills, arXiv

> **Revisit:** `high` · **fonte:** `article`
