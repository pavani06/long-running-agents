---
title: "Preenchimento de Aliases nos Documentos — Plano de Execução"
type: plan
date: 2026-06-10
tags: ["governanca", "curriculo-conteudo"]
aliases:
  - preenchimento de aliases
  - fill aliases
  - metadata aliases
relates-to: ["[[docs/system-of-record|System of Record]]", "[[AGENTS|AGENTS.md]]"]
---

# Preenchimento de Aliases nos Documentos — Plano de Execução

**Objetivo:** Preencher o campo `aliases` (hoje vazio como `[]`) em 106 arquivos markdown de `docs/analysis/` e `curriculum/`, usando os 23 canônicos de `docs/canonical/` e o `system-of-record.md` como benchmark de qualidade.
**Fase:** Implementação
**Dependências:** Nenhuma — trabalho autônomo de metadata
**Duração estimada:** 3-4 sessões

---

## Diagnóstico de partida

| Localização | Arquivos | Com `aliases: []` | Com aliases preenchidos | Sem campo |
|---|---|---|---|---|
| `docs/canonical/` | 23 | 0 | 23 | 0 |
| `docs/analysis/` (subpastas) | 22 | 15 | 0 | 7 |
| `docs/analysis/mhc-backend/` | 7 | 7 | 0 | 0 |
| `curriculum/` (lições, exercícios, etc.) | 87 | 84 | 0 | 3 |
| `docs/system-of-record.md` | 1 | 0 | 1 | 0 |
| **Total** | **149** | **106** | **24** | **10** |

---

## Convenção de aliases por tipo de documento

Baseada nos 23 canônicos preenchidos como referência. Cada alias deve ter 2-5 itens cobrindo: sinônimo, acrônimo (se houver), termo em PT-BR (se o título for EN), forma curta de busca.

### Análises (`docs/analysis/`)

| Arquivo | Estratégia de aliases |
|---|---|
| `analysis.md` | Título em PT-BR, palavras-chave do domínio, acrônimo da fonte |
| `classification.md` | Termos alternativos para "classificação": mapeamento, gap analysis, cobertura |
| `integration-roadmap.md` | Sinônimos: plano de integração, next steps, implementation path |
| `mental-model.md` | Sinônimos: modelo conceitual, framework mental, orientação |
| `patterns.md` | Sinônimos: catálogo de padrões, pattern library |

### Diagnósticos MHC (`docs/analysis/mhc-backend/`)

| Arquivo | Estratégia |
|---|---|
| `*-harness-diagnostic.md` | Diagnóstico em PT-BR, KODA harness, arquitetura KODA |
| `*-nivel-2-diagnostic.md` | Diagnóstico N2, maturidade padrões, nível 2 |
| `*-nivel-3-comparacao.md` | Comparação N3, KODA vs padrões, benchmark N3 |
| `*-pedido-bling-agente.md` | Falha webhook, notificação pedido, ERP Bling |
| `*-janela-deslizante-contexto.md` | Sliding window, resumo contexto, truncation |
| `*-output-validation-*.md` | Validação de saída, structured output, state persistence |

### Currículo — Lições (`curriculum/0*-*/`)

Cada lição recebe 2-3 aliases: título PT-BR (se original EN), conceito-chave curto, termo de busca comum.

### Currículo — Exercícios e Soluções (`curriculum/0*-*/exercises/`)

Idem lição + indicador de tipo (`exercício X`, `solução X`).

### Currículo — Índices e meta-documentos (`curriculum/` raiz)

Aliases em PT-BR para termos de navegação: `FAQ` → `"perguntas frequentes"`, `GLOSSARY` → `"glossário"`, `INDEX` → `"índice"`.

---

## Tarefas

### Tarefa 1: Leitura dos documentos de referência

**Artefatos:**
- Entrada: `docs/system-of-record.md`, `AGENTS.md` (Rule 16), 3 exemplos de canônicos com aliases
- Saída: entendimento consolidado das convenções

- [ ] **Passo 1: Reler system-of-record para domínios e taxonomia**
  Comando: `read docs/system-of-record.md`
  Esperado: confirmar os 4 domínios (agentes-orquestracao, curriculo-conteudo, stack-tooling, governanca) e os tópicos documentados

- [ ] **Passo 2: Revisar 3 canônicos como benchmark**
  Comando: `read docs/canonical/error-context-hygiene.md`, `read docs/canonical/closed-loop-agent-operating-system.md`, `read docs/canonical/split-brain-planning-review.md`
  Esperado: entender padrão de 2-5 aliases por documento (sinônimo + acrônimo + PT-BR)

- [ ] **Passo 3: Verificação**
  Critério: conseguir enunciar a regra de ouro para aliases em uma frase

---

### Tarefa 2: Lote 1 — `docs/analysis/` (4 subpastas, 22 arquivos)

**Artefatos:**
- Entrada: `docs/analysis/2026-06-09-12-factor-agents/`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/`, `docs/analysis/2026-06-10-eval-maturity-phases/`, `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/`
- Saída: todos os `analysis.md`, `classification.md`, `integration-roadmap.md`, `mental-model.md`, `patterns.md` com aliases preenchidos

- [ ] **Passo 2.1: 12-factor-agents (5 arquivos)**
  Comando: ler cada arquivo (`analysis.md`, `classification.md`, `integration-roadmap.md`, `mental-model.md`, `patterns.md`), identificar conceito central, preencher 2-3 aliases
  Esperado: 5 arquivos com `aliases:` não-vazio

- [ ] **Passo 2.2: how-we-solved-context-management (5 arquivos)**
  Comando: mesmo processo do passo 2.1
  Esperado: 5 arquivos com aliases preenchidos

- [ ] **Passo 2.3: eval-maturity-phases (5 arquivos)**
  Comando: mesmo processo
  Esperado: 5 arquivos com aliases preenchidos

- [ ] **Passo 2.4: stanford-cs153 (5 arquivos)**
  Comando: mesmo processo (nota: `classification.md` e `patterns.md` estão sem campo `aliases` — adicionar o campo)
  Esperado: 5 arquivos com aliases preenchidos (incluindo criação do campo nos 2 que não o têm)

- [ ] **Passo 2.5: Verificação do lote**
  Comando: `grep -r "^aliases:" docs/analysis/2026-06-*/ | grep "\[\]" | wc -l`
  Esperado: 0 (nenhum alias vazio restante nas 4 subpastas)

---

### Tarefa 3: Lote 2 — `docs/analysis/mhc-backend/` (7 arquivos)

**Artefatos:**
- Entrada: `docs/analysis/mhc-backend/`
- Saída: 7 arquivos com aliases preenchidos

- [ ] **Passo 3.1: Preencher aliases nos 7 diagnósticos MHC**
  Comando: para cada arquivo, ler o conteúdo e preencher 2-3 aliases incluindo termo PT-BR equivalente
  Arquivos:
  - `2026-05-26-harness-diagnostic.md` → "diagnóstico harness", "KODA arquitetura", "harness KODA"
  - `2026-05-26-nivel-2-diagnostic.md` → "diagnóstico nível 2", "maturidade padrões", "N2 diagnostic"
  - `2026-05-26-nivel-3-comparacao.md` → "comparação N3", "KODA benchmark", "nível 3"
  - `2026-05-26-pedido-bling-agente.md` → "falha webhook", "notificação Bling", "pedido pago"
  - `2026-05-28-janela-deslizante-contexto.md` → "sliding window", "resumo contexto", "truncation"
  - `2026-05-28-output-validation-state-persistence.md` → "validação saída", "state persistence", "output validation"
  - `2026-05-28-output-validation-structured-generation.md` → "validação estruturada", "Zod", "structured generation"
  Esperado: 7 arquivos com aliases preenchidos

- [ ] **Passo 3.2: Verificação do lote**
  Comando: `grep "^aliases:" docs/analysis/mhc-backend/*.md | grep "\[\]"`
  Esperado: nenhuma correspondência

---

### Tarefa 4: Lote 3 — `curriculum/` níveis 01-04, lições (20 arquivos)

**Artefatos:**
- Entrada: `curriculum/01-nivel-1-fundamentals/`, `curriculum/02-nivel-2-practical-patterns/`, `curriculum/03-nivel-3-advanced-architecture/`, `curriculum/04-nivel-4-koda-specific/` — apenas os arquivos de lição (não exercises/, solutions/, case-studies/, koda-applications/)
- Saída: 20 arquivos de lição com aliases preenchidos

- [ ] **Passo 4.1: Nível 1 (3 lições)**
  Comando: ler cada lição, extrair conceito-chave, gerar aliases
  Esperado: 3 arquivos com aliases

- [ ] **Passo 4.2: Nível 2 (4 lições)**
  Comando: mesmo processo
  Esperado: 4 arquivos com aliases

- [ ] **Passo 4.3: Nível 3 (5 lições)**
  Comando: mesmo processo
  Esperado: 5 arquivos com aliases

- [ ] **Passo 4.4: Nível 4 (5 lições)**
  Comando: mesmo processo
  Esperado: 5 arquivos com aliases

- [ ] **Passo 4.5: koda-applications (3 arquivos)**
  Comando: `nivel-1-koda.md`, `nivel-2-koda.md`, `nivel-3-koda.md`
  Esperado: 3 arquivos com aliases

- [ ] **Passo 4.6: Verificação do lote**
  Comando: `grep "^aliases:" curriculum/0[1-4]-*/0*.md | grep "\[\]"`
  Esperado: nenhuma correspondência

---

### Tarefa 5: Lote 4 — `curriculum/` níveis 01-04, exercícios e soluções (20 arquivos)

**Artefatos:**
- Entrada: `curriculum/0*-*/exercises/` e `curriculum/0*-*/exercises/solutions/`
- Saída: ~20 arquivos com aliases

- [ ] **Passo 5.1: Exercícios (12 arquivos)**
  Comando: para cada `exercise-*.md`, ler o enunciado e preencher aliases com o tópico do exercício
  Esperado: 12 exercícios com aliases

- [ ] **Passo 5.2: Soluções (8 arquivos)**
  Comando: para cada `*-solution.md`, espelhar aliases do exercício correspondente + "solução"
  Esperado: 8 soluções com aliases

- [ ] **Passo 5.3: Verificação do lote**
  Comando: `grep "^aliases:" curriculum/0[1-4]-*/exercises/**/*.md | grep "\[\]"`
  Esperado: nenhuma correspondência

---

### Tarefa 6: Lote 5 — `curriculum/` níveis 05-10 (30 arquivos)

**Artefatos:**
- Entrada: `curriculum/05-core-concepts/`, `curriculum/06-knowledge-graphs/`, `curriculum/07-implementation-guides/`, `curriculum/08-tools-templates/`, `curriculum/09-case-studies/`, `curriculum/10-references/`
- Saída: 30 arquivos com aliases

- [ ] **Passo 6.1: 05-core-concepts (8 arquivos)**
  Comando: cada arquivo cobre um conceito — alias é o conceito em PT-BR + forma curta
  Esperado: 8 arquivos com aliases

- [ ] **Passo 6.2: 06-knowledge-graphs (12 arquivos)**
  Comando: 4 principais + 8 detailed-graphs. Aliases incluem "gráfico de conhecimento", termo PT-BR, domínio
  Esperado: 12 arquivos com aliases

- [ ] **Passo 6.3: 07-implementation-guides (6 arquivos)**
  Comando: aliases incluem "guia de implementação", termo PT-BR
  Esperado: 6 arquivos com aliases

- [ ] **Passo 6.4: 08-tools-templates (6 arquivos)**
  Comando: aliases incluem "template", "modelo", termo PT-BR
  Esperado: 6 arquivos com aliases

- [ ] **Passo 6.5: 09-case-studies (6 arquivos)**
  Comando: incluir o caso em PT-BR + domínio de negócio
  Esperado: 6 arquivos com aliases (nota: `00-all-case-studies.md` pode não ter campo — verificar)

- [ ] **Passo 6.6: 10-references (3 arquivos)**
  Comando: aliases incluem termo PT-BR + acrônimos se aplicável
  Esperado: 3 arquivos com aliases

- [ ] **Passo 6.7: Verificação do lote**
  Comando: `grep "^aliases:" curriculum/0[5-9]-*/**/*.md curriculum/10-*/**/*.md | grep "\[\]"`
  Esperado: nenhuma correspondência

---

### Tarefa 7: Lote 6 — `curriculum/` raiz e `docs/plans/` (7 arquivos)

**Artefatos:**
- Entrada: `curriculum/` arquivos de índice e meta (INDEX, README, GLOSSARY, etc.) + `docs/plans/` (2 arquivos sem campo)
- Saída: 7 arquivos com aliases

- [ ] **Passo 7.1: Índices e meta-documentos (5 arquivos)**
  Comando: INDEX.md, README.md, QUICK_START.md, GLOSSARY.md, FAQ.md — aliases PT-BR
  Esperado: 5 arquivos com aliases

- [ ] **Passo 7.2: Planos e entrega (4 arquivos)**
  Comando: DELIVERY-COMPLETE.md, EXECUTION_PLAN.md, MASTER_PLAN.md + `docs/plans/2026-05-26-curriculum-completion-strategy.md` e `docs/plans/2026-06-10-obsidian-reading-improvements.md` (estes 2 sem campo `aliases` — adicionar)
  Esperado: 5 arquivos com aliases

- [ ] **Passo 7.3: docs/articles/ (3 arquivos sem campo)**
  Comando: `docs/articles/` contém 3 arquivos sem campo `aliases`. Adicionar campo com aliases PT-BR.
  Esperado: 3 arquivos com aliases

- [ ] **Passo 7.4: docs/analysis/ (patterns.md sem campo)**
  Comando: os 4 `patterns.md` que não têm campo `aliases` (12-factor-agents, how-we-solved, eval-maturity-phases, stanford-cs153) — adicionar campo. O classification.md do stanford-cs153 também.
  Esperado: 5 arquivos com campo adicionado e preenchido

- [ ] **Passo 7.5: Verificação do lote**
  Comando: `grep "^aliases:" curriculum/{INDEX,README,QUICK_START,GLOSSARY,FAQ,DELIVERY-COMPLETE,EXECUTION_PLAN,MASTER_PLAN}.md docs/plans/*.md docs/articles/*.md | grep "\[\]"`
  Esperado: nenhuma correspondência

---

### Tarefa 8: Validação final

**Artefatos:**
- Entrada: todo o repositório
- Saída: relatório de validação limpo

- [ ] **Passo 8.1: Rodar script de validação Obsidian**
  Comando: `bash scripts/check-obsidian-conventions.sh`
  Esperado: exit 0, sem erros de alias (o script verifica frontmatter e wikilinks; aliases vazios são tecnicamente válidos, mas o objetivo é zero `[]`)

- [ ] **Passo 8.2: Verificação quantitativa**
  Comando: `grep -r "^aliases:" docs/ curriculum/ | grep "\[\]" | wc -l`
  Esperado: 0

- [ ] **Passo 8.3: Verificação qualitativa por amostragem**
  Comando: `grep "^aliases:" docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis.md docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md curriculum/GLOSSARY.md`
  Esperado: cada linha mostra 2-5 aliases significativos (não genéricos como "doc" ou "file")

- [ ] **Passo 8.4: Verificação dos 10 arquivos que não tinham campo**
  Comando: listar os 10 arquivos originalmente sem campo e confirmar que agora o têm preenchido
  Esperado: 10 arquivos com campo `aliases:` não-vazio

- [ ] **Passo 8.5: Contagem final**
  Comando:
  ```
  echo "Total de aliases preenchidos:"
  grep -rh "^aliases:" docs/ curriculum/ | grep -v "\[\]" | grep -o '"[^"]*"' | wc -l
  echo "Arquivos cobertos:"
  grep -rl "^aliases:" docs/ curriculum/ | wc -l
  ```
  Esperado: ~300-400 aliases no total, 149 arquivos cobertos

---

## Resumo de batches

| Tarefa | Arquivos | Localização |
|---|---|---|
| T1 | 0 (leitura) | — |
| T2 | 22 | `docs/analysis/` (4 subpastas recentes) |
| T3 | 7 | `docs/analysis/mhc-backend/` |
| T4 | 20 | `curriculum/01-04`, lições + koda-apps |
| T5 | 20 | `curriculum/01-04`, exercícios + soluções |
| T6 | 30 | `curriculum/05-10` |
| T7 | 17 | `curriculum/` raiz, `docs/plans/`, `docs/articles/`, `patterns.md` restantes |
| T8 | 149 | Validação global |

---

## Regras de ouro para aliases

1. **2 a 5 aliases por documento.** Menos que 2 é sub-aproveitado; mais que 5 dilui.
2. **Um em PT-BR** se o título for em inglês (ex: "error context hygiene" → "higiene de erro").
3. **Forma curta de busca** — como alguém digitaria no Quick Switcher? ("pause resume", não "serializable pause resume state").
4. **Acrônimo** se o conceito tiver um estabelecido no repo (ex: "SOR", "12FA", "N+1").
5. **Nada genérico.** "documento", "analysis", "file" não são aliases.
6. **Sem duplicação do título.** Se o título já é "Error Context Hygiene", o alias não deve ser idêntico.
