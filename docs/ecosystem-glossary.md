---
id: docs.ecosystem-glossary
title: "Glossário do Ecossistema"
type: reference
tags:
  - documentation
  - glossary
  - ecosystem
status: stable
date: 2026-06-21
relates-to:
  - "[[curriculum/GLOSSARY|Glossário do Currículo]]"
  - "[[docs/system-of-record|System of Record]]"
  - "[[../../agent-analysis/docs/glossary|Glossário Agent-Analysis]]"
---

# Glossário do Ecossistema Pavan

Este glossário define **30 termos cross-cutting** do ecossistema.
Para termos específicos do currículo de agentes (Agent, Amnesia, Harness, etc.),
veja o [[curriculum/GLOSSARY|Glossário do Currículo]] (1002 linhas).
Para termos do domínio KODA/MHC, veja o
[[../../agent-analysis/docs/glossary|Glossário Agent-Analysis]].

Os termos estão organizados em 4 níveis: **Runtime** (infraestrutura),
**Pipeline** (fluxo de conhecimento), **Agente** (conceitos), **Qualidade** (verificação).

---

## Nível Runtime

### Vault

Repositório de conhecimento em Markdown gerenciado pelo `obsidian-eval`.
Cada vault declara seus `exports` e `imports` no `MANIFEST.md`.

**No código:** `obsidian-eval/src/types.ts` — interface `Vault`; `listVaults()`, `registerVault()`, `isVault()`

**Vaults ativos:**
| Nome | Path | Propósito |
|------|------|-----------|
| `long-running-agents` | `./long-running-agents` | 95 docs canônicos, currículo N1-N4, ADRs |
| `mhc-knowledge-base` | `./mhc-knowledge-base` | Domínio KODA, intents, templates |
| `raw-knowledge` | `./raw-knowledge` | Fontes ingeridas (papers, talks, transcripts) |
| `sisyphus-runtime` | `~/sisyphus-runtime` | Vault privado: handoffs, fatos duráveis, estado |

**Exemplo:**
```bash
obsidian-eval list-vaults
obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'durable-fact')"
```

**Ver também:** [[#MANIFEST.md]], [[#Cross-vault Wikilink]]

---

### MANIFEST.md

Declaração de dependências cross-vault. Cada vault tem um `MANIFEST.md` na raiz
que lista quais arquivos exporta e de quais vaults importa.

**No código:** `obsidian-eval/src/manifest.ts` — `parseManifest()`, `validateManifests()`;
`obsidian-eval/src/types.ts` — interface `VaultManifest`

**Exemplo:**
```markdown
# ~/sisyphus-runtime/MANIFEST.md
exports:
  facts:
    - "facts/_global/principles.md"
    - "facts/_global/constraints.md"
imports:
  long-running-agents:
    - "docs/canonical/"
```

**Comandos:**
```bash
obsidian-eval <vault> manifest          # exibir manifesto
obsidian-eval <vault> manifest-check     # validar imports/exports
obsidian-eval <vault> manifest-graph     # grafo de dependências
```

**Ver também:** [[#Vault]], [[#Cross-vault Wikilink]]

---

### Cross-vault Wikilink

Wikilink que referencia um documento em outro vault usando o prefixo `vault:`.

**Sintaxe:** `[[vault:<nome-do-vault>/<path>]]`

**No código:** `obsidian-eval/src/index.ts` — `resolveVaultRoot()`, `isExternalWikilink()`, `resolveWikilinkPath()`, `extractWikilinkTargets()`

**Exemplos:**
```markdown
[[vault:long-running-agents/docs/canonical/error-context-hygiene]]
[[vault:sisyphus-runtime/facts/_global/ground-truth]]
```

**Resolução:** O `obsidian-eval` resolve `vault:<nome>` para o path absoluto do vault
via `resolveVaultRoot()`. Sem dependência do app Obsidian.

**Ver também:** [[#MANIFEST.md]], [[#Vault]]

---

### Telemetry DB

Banco SQLite (`~/sisyphus-runtime/telemetry.db`) que armazena métricas de sessão:
tokens consumidos, traces de `task()`, SLOs, e burn rates.

**No código:** `~/scripts/telemetry/collector.ts` — coleta pós-sessão;
`~/scripts/telemetry/daily-summary.ts` — sumário diário;
`~/scripts/telemetry/budget-slo-check.sh` — verificação de SLOs

**Tabelas principais:** `sessions`, `task_calls`, `trace_spans`

**Exemplo:**
```bash
npx tsx ~/scripts/telemetry/daily-summary.ts
~/scripts/telemetry/budget-slo-check.sh --json
```

**Ver também:** [[#Trace Span]], [[#Scheduler]]

---

### Trace Span

Registro instrumentado de uma chamada `task()`. Cada span captura:
categoria, subagent_type, skills carregados, duração, tokens, success/failure, error_type.

**No código:** `~/scripts/telemetry/trace-cli.ts` — `start`, `end`, `dump`, `clear`;
`~/scripts/telemetry/task-wrapper.sh` — wrapper obrigatório para toda delegação `task()`

**Exemplo:**
```bash
SPAN_ID=$(bash ~/scripts/telemetry/task-wrapper.sh --start-only \
  --category "deep" --subagent-type "" --skills "canonical-context,debugging" \
  --description "Fix query engine bug")
# ... executa task() ...
bash ~/scripts/telemetry/task-wrapper.sh --end-last \
  --success true --duration-ms 45200 --tokens 3200 --model "deepseek-v4-pro"
```

**Ver também:** [[#Telemetry DB]], [[#Scheduler]]

---

### Scheduler

Estimador de tokens que fragmenta tarefas para caber no budget da sessão.

**No código:** `obsidian-eval/src/scheduler.ts` — `estimateTaskTokens()`, `fragmentTask()`,
`heuristicCountTokens()`, `createSchedulerEstimate()`

**Exemplo:**
```typescript
const estimate = createSchedulerEstimate(task, { budgetRemaining: 15000 });
// → { fragments: [...], tokenCosts: [...], safeToProceed: true }
```

**Ver também:** [[#Token Budget]], [[#Trace Span]]

---

### Execution Graph

DAG de tarefas que modela a orquestração de sessões.
Cada nó (`TaskNode`) tem status, pais, filhos, estimativa de tokens, e contexto de retomada.

**No código:** `obsidian-eval/src/execution-graph.ts` — `createGraph()`, `addNode()`,
`getCurrentNode()`, `completeNode()`, `getNextNodes()`, `getBlockedNodes()`,
`estimateGraphCost()`, `getGraphStatus()`, `getResumeContext()`, `getAllNodes()`

**Usado por:** `canonical-context` skill (modo `KNOWLEDGE_RUNTIME`), `session-handoff` skill

**Ver também:** [[#Handoff]], [[#Session]]

---

## Nível Pipeline

### Knowledge Pipeline

Fluxo completo de transformação de handoffs em conhecimento durável:
handoff → compressWorkingMemory (A1) → relevanceScore (B1) → promotePatterns (B2)
→ buildProvenance (C4) → checkDrift (C5) → appendFact com valid_from/valid_to (C2)
→ cross-vault manifest export (C3) → simulation verification (C6) → execution graph injection (D1).

**Walkthrough completo:** `obsidian-eval/docs/walkthroughs/pipeline-completo.md`
**Artigo:** `obsidian-eval/articles/memory-os-article/index.md`

**Ver também:** [[#Memory Layers]], [[#Relevance Score]], [[#Reflection Loop]], [[#Ground Truth]]

---

### Handoff

Snapshot do estado de uma sessão OpenCode, persistido como nota no vault de runtime
(`type: session-handoff`). Permite que a próxima sessão retome o contexto.

**Campos principais:**
| Campo | Descrição |
|-------|-----------|
| `continuity_message` | Resumo do que estava sendo feito |
| `open_decisions` | Decisões pendentes que a próxima sessão precisa tomar |
| `memory_handles` | Referências a arquivos para injeção de contexto |
| `execution_graph` | ID do grafo de execução |
| `current_node` | Nó atual no grafo de execução |
| `trigger` | `manual` (intenção explícita) ou `red-phase` (interrompido por budget) |
| `budget_percentage` | Percentual de budget restante no momento do handoff |

**Skill:** `session-handoff` (`/handoff`)

**Exemplo:**
```bash
obsidian-eval ~/sisyphus-runtime query \
  "filter(n => n.frontmatter.type === 'session-handoff' && n.frontmatter.status === 'active')"
```

**Ver também:** [[#Session]], [[#Execution Graph]], [[#Durable Fact]]

---

### Session

Unidade de interação contínua entre humano e agente no OpenCode.
Cada sessão tem um `session_id` (`ses_...`), message count, date range, e agents usados.

**Estadualidade:** Handoffs conectam sessões. O `canonical-context` skill carrega
o handoff da sessão anterior no início da nova sessão.

**Ver também:** [[#Handoff]], [[#Token Budget]]

---

### Durable Fact

Conhecimento persistido como nota no vault de runtime com `type: durable-fact`.
Pode ser um `constraint`, `preference`, `baseline`, `diagnostic`, ou `principle`.

**Schema:** `obsidian-eval/src/types.ts` — interface `DurableFactFields`:
`valid_from`, `valid_to`, `confidence`, `provenance`, `summary_buffer`

**Comando:**
```bash
obsidian-eval ~/sisyphus-runtime append-fact \
  --kind principle \
  --title "Sempre usar obsidian-eval para navegar vaults" \
  --confidence high \
  --valid-from "2026-06-01"
```

**Ver também:** [[#Provenance Chain]], [[#Ground Truth]], [[#Temporal Versioning]]

---

### Memory Layers

Pipeline de 3 camadas que transforma handoffs brutos em conhecimento:
1. **Working Memory** — `compressWorkingMemory()` agrupa handoffs similares
2. **Session Memory** — contexto da sessão atual
3. **Long-term Memory** — fatos duráveis promovidos

**No código:** `obsidian-eval/src/memory-layers.ts` — `compressWorkingMemory()`,
`promotePatterns()`, `deprecateStaleFacts()`

**Ver também:** [[#Knowledge Pipeline]], [[#Promotion Candidate]]

---

### Relevance Score

Pontuação de 0 a 1 que determina quão relevante um `KnowledgeItem` é para o contexto
atual da tarefa. Usa 5 dimensões: recência, importância, frequência, similaridade, confiança.

**No código:** `obsidian-eval/src/relevance.ts` — `relevanceScore(item, taskContext)`

**Exemplo:**
```typescript
const score = relevanceScore(knowledgeItem, {
  objective: "corrigir query engine",
  repo: "obsidian-eval",
  tags: ["query", "validation"]
});
// → 0.87 (recência < 7d + tags sobrepostas + confiança alta)
```

**Usado por:** `canonical-context` skill (Passo 3: seleção top-N por budget)

**Ver também:** [[#Knowledge Pipeline]], [[#Canonical Doc]]

---

### Promotion Candidate

Padrão detectado em ≥3 handoffs similares, candidato a virar princípio.
Gerado por `promotePatterns()` com Porter stemmer + Jaccard fuzzy clustering.

**No código:** `obsidian-eval/src/types.ts` — interface `PromotionCandidate`;
`obsidian-eval/src/memory-layers.ts` — `promotePatterns()`

**Exemplo:**
```typescript
const candidates = promotePatterns(recentHandoffs, {
  minFrequency: 3,
  similarityThreshold: 0.6
});
// → [{ summary: "...", evidence: [...], confidence: "high", provenance: {...} }]
```

**Ver também:** [[#Memory Layers]], [[#Provenance Chain]], [[#Reflection Loop]]

---

### Reflection Loop

Pipeline cross-session de 4 fases que detecta padrões, sintetiza princípios,
e os aplica como fatos duráveis: Gather → Analyze → Synthesize → Apply.

**Skill:** `reflection-runner` (`/reflection-runner`)
**Automação:** systemd timer (`reflection-runner.timer`), diariamente às 09:00 BRT

**Fases:**
1. **Gather** — coleta handoffs não refletidos do vault de runtime
2. **Analyze** — `promotePatterns()` detecta padrões recorrentes
3. **Synthesize** — Oracle sintetiza princípios candidatos com evidências
4. **Apply** — verifica drift (C5) → promove princípios aprovados

**Ver também:** [[#Knowledge Pipeline]], [[#Ground Truth]], [[#Provenance Chain]]

---

### Temporal Versioning

Sistema de validade temporal para fatos duráveis. Todo fato tem `valid_from`
(opcional) e `valid_to` (opcional). Fatos expirados são penalizados no `relevanceScore()`.

**No código:** `obsidian-eval/src/types.ts:93-100` — `DurableFactFields`;
`obsidian-eval/src/memory-layers.ts:330-334` — `deprecateStaleFacts()`

**Regras de penalização:**
- `valid_to < now` → fator 0.1 (expirado, quase irrelevante)
- `valid_from > now` → fator 0.5 (ainda não ativo)
- Sem `valid_to` → sem penalização (fato permanente)

**CLI:**
```bash
obsidian-eval ~/sisyphus-runtime append-fact \
  --valid-from "2026-06-01" --valid-to "2026-12-31" ...
```

**Ver também:** [[#Durable Fact]], [[#Relevance Score]]

---

## Nível Agente

### Canonical Doc

Documento de referência autoritativo no vault `long-running-agents` com
`type: canonical`. Define um padrão reutilizável de design de agente.

**Localização:** `long-running-agents/docs/canonical/` (95 documentos)
**Catálogo:** `long-running-agents/docs/system-of-record.md`

**Exemplo:** `docs/canonical/error-context-hygiene.md` — padrão para sumarizar
erros em vez de despejar stack traces no contexto.

**Ver também:** [[#System of Record]], [[#Skill]]

---

### Skill

Conjunto de instruções e workflows para um domínio específico, carregado
pelo orquestrador via `skill(name="...")`. Invocável também como comando (`/skill`).

**Localização:** `~/.config/opencode/skills/` (25 skills)
**Testes:** 237 testes, 26/26 suites passam

**Skills do pipeline:**
| Skill | Função |
|-------|--------|
| `canonical-context` | Injeção de contexto cross-session |
| `session-handoff` | Persistência de estado entre sessões |
| `reflection-runner` | Pipeline de aprendizado cross-session |
| `budget-monitor` | Monitoramento de token budget |

**Ver também:** [[#Harness]], [[#Canonical Doc]]

---

### Harness

Infraestrutura de controle que envolve o agente: testes, reviews, convenções,
skills, e documentação. O harness é o que transforma código gerado por LLM
em software de produção.

**Convenções de teste:** `long-running-agents/docs/canonical/skill-testing-conventions.md`
**Skill:** `harness-analyze-and-improve`

**Ver também:** [[#Skill]], [[#Token Budget]]

---

### Token Budget

Orçamento de tokens disponível por sessão. Classificado em 4 fases:

| Fase | Percentual | Ação |
|------|-----------|------|
| Green | > 50% | Operação normal |
| Yellow | 30-50% | Contexto reduzido |
| Orange | 20-30% | Handoff recomendado |
| Red | ≤ 20% | Handoff automático obrigatório |

**Skill:** `budget-monitor` (`/budget`)
**Tokenizer:** `~/scripts/token-counter/count-session.sh` (usa `@goliapkg/tiktoken-wasm`, encoding `deepseek_v3`)

**Ver também:** [[#Session]], [[#Handoff]]

---

### Context Window

Limite de tokens que o modelo pode processar em uma única sessão.
Gerenciado pelo `budget-monitor` skill com handoff automático em red phase.

**Ver também:** [[#Token Budget]], [[#Session]]

---

### Orchestrator

Agente principal (Sisyphus) que decompõe tarefas e delega para sub-agentes
especializados via `task()`. Não implementa diretamente — coordena.

**Sub-agentes:** `explore`, `librarian`, `oracle`, `deep`, `ultrabrain`, `quick`, etc.
**Padrão canônico:** `long-running-agents/docs/canonical/closed-loop-agent-operating-system.md`

**Ver também:** [[#Sub-agent]], [[#Execution Graph]]

---

### Sub-agent

Agente especializado invocado pelo orquestrador para uma tarefa específica.
Cada sub-agente tem um tipo (`explore`, `oracle`, `deep`, etc.) e pode carregar skills.

**Instrumentação:** toda chamada `task()` deve ser instrumentada com `task-wrapper.sh`
(Trace Instrumentation Gate).

**Ver também:** [[#Orchestrator]], [[#Trace Span]]

---

### Epistemic Graph

Grafo de entidades e relacionamentos extraído automaticamente do vault de runtime.
Permite queries como `affectedBy`, `mostModifiedFiles`, `staleFacts`.

**No código:** `obsidian-eval/src/epistemic-graph.ts` — `EpistemicGraph`, `EpistemicNode`,
`EpistemicEdge`; CLI: `obsidian-eval epistemic build|stats|query`

**Métricas atuais (2026-06-19):** 174 nós, 191 edges

**Exemplo:**
```bash
obsidian-eval ~/sisyphus-runtime epistemic build
obsidian-eval ~/sisyphus-runtime epistemic stats --json
obsidian-eval ~/sisyphus-runtime epistemic query budget-monitor
```

**Ver também:** [[#Vault]], [[#Durable Fact]]

---

## Nível Qualidade

### Ground Truth

Assertions imutáveis definidas por humanos que bloqueiam a contaminação do pipeline
de conhecimento. Armazenadas em `facts/_global/ground-truth.md`.

**No código:** `obsidian-eval/src/ground-truth.ts` — `loadGroundTruths()`, `checkDrift()`

**Ground truths atuais (5):**
1. Nunca usar `grep`, `sed`, `awk` para leitura via bash
2. Nunca suprimir erros de tipo com `as any`, `@ts-ignore`
3. Nunca apagar ou enfraquecer testes para "passar"
4. Sempre carregar `canonical-context` antes de decisões de arquitetura
5. Sempre usar `obsidian-eval` para navegar vaults

**Ver também:** [[#Drift Detection]], [[#Knowledge Pipeline]]

---

### Drift Detection

Verificação de que um princípio candidato não contradiz nenhuma ground truth.
Usa correspondência lexical (negação + Jaccard similarity > 0.3).

**No código:** `obsidian-eval/src/ground-truth.ts:25-89` — `checkDrift(candidate, groundTruths)`

**Retorno:** `DriftAlert | null`
- `null` = sem contradição, promoção permitida
- `DriftAlert` = contradição detectada, promoção bloqueada

**Limitação conhecida:** apenas lexical (não semântico). Upgrade para embeddings planejado.

**Ver também:** [[#Ground Truth]], [[#Knowledge Pipeline]]

---

### Provenance Chain

Trilha de auditoria que registra a origem de cada fato durável promovido.

**No código:** `obsidian-eval/src/types.ts:102-116` — interface `Provenance`

**Campos:**
| Campo | Descrição |
|-------|-----------|
| `derived_from` | Handoff IDs que geraram este princípio |
| `reasoning_summary` | Resumo do raciocínio de promoção |
| `premises` | Premissas assumidas |
| `promoted_at` | ISO timestamp da promoção |
| `promoted_by` | Skill ou agente que promoveu |

**Ver também:** [[#Promotion Candidate]], [[#Reflection Loop]]

---

### Simulation

Geração de handoffs sintéticos para testar propriedades emergentes do pipeline.
Usa PRNG determinístico (mulberry32) para reprodutibilidade.

**No código:** `obsidian-eval/src/simulate.ts` — `generateHandoff()`, `runSimulation()`

**5 asserts de comportamento emergente:**
1. Memória converge (não cresce indefinidamente)
2. Sem falsos positivos (threshold ≥ 3 handoffs)
3. Drift bloqueia contaminação
4. Depreciação limpa fatos expirados
5. Proveniência capturada em toda promoção

**Exemplo:**
```bash
cd obsidian-eval && npx vitest run test/simulate.test.ts
```

**Ver também:** [[#Knowledge Pipeline]], [[#Drift Detection]]

---

### System of Record

Documento que define a precedência e as fontes canônicas de um vault.
É o árbitro para resolver conflitos de documentação.

**Principal:** `long-running-agents/docs/system-of-record.md` (371 linhas)
Define 6 níveis de precedência: ADRs > canonical > evidence > analysis > archive > READMEs

**Ver também:** [[#Canonical Doc]], [[#Vault]]

---

### MOC (Map of Content)

Arquivo com prefixo `_moc-` que agrega wikilinks para um cluster temático.
Não contém conteúdo original — apenas links organizados por categoria.

**Convenção:** `_moc-<tema>.md` na raiz do diretório de docs do vault

**Exemplo:** `long-running-agents/docs/_moc-ecosystem.md`

**Ver também:** [[#System of Record]], [[#Vault]]

---

## Referência Rápida

| Quero entender... | Vá para... |
|-------------------|-----------|
| O que é um vault? | [[#Vault]] |
| Como funciona o pipeline? | [[#Knowledge Pipeline]] |
| O que é um handoff? | [[#Handoff]] |
| Como fatos são promovidos? | [[#Promotion Candidate]] → [[#Reflection Loop]] |
| Como evitar contaminação? | [[#Ground Truth]] → [[#Drift Detection]] |
| Como verificar o pipeline? | [[#Simulation]] |
| O que significam os níveis C2-C6? | [[#Temporal Versioning]] (C2), [[#MANIFEST.md]] (C3), [[#Provenance Chain]] (C4), [[#Ground Truth]] (C5), [[#Simulation]] (C6) |
| Termos de agente (Agent, Harness...)? | [[curriculum/GLOSSARY|Glossário do Currículo]] |
| Termos do KODA? | [[../../agent-analysis/docs/glossary|Glossário Agent-Analysis]] |
