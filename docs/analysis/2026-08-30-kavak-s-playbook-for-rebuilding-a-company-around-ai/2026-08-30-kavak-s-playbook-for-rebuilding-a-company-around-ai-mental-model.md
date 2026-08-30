---
title: "Mental Model: Kavak's Playbook for Rebuilding a Company Around AI (Repository Rebuild)"
type: analysis
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "governanca"]
date: 2026-08-30
aliases: ["kavak mental model", "repo mental model rebuild", "long-running-agents mental model 2026-08-30"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|Agent Rules]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/GLOSSARY|Glossary]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/decisions/2026-06-24-skill-canons-bridge-implementation|Skill-Canons Bridge ADR]]"]
sources: ["[[AGENTS|AGENTS]]", "[[README|README]]", "[[docs/system-of-record|System of Record]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/GLOSSARY|Glossary]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/decisions/2026-06-24-skill-canons-bridge-implementation|ADR Skill-Canons Bridge]]"]
---

# Mental Model: long-running-agents (Full Rebuild, 2026-08-30)

**Date:** 2026-08-30
**Repo:** `long-running-agents` at `/mnt/c/Users/pavan/long-running-agents` (branch `main`)
**Scope:** Repository only. The external source document (Kavak/a16z transcript) was NOT analyzed in this pass.

All `file:line` citations below use paths anchored at the repository root `/mnt/c/Users/pavan/long-running-agents/`.

---

## 1. Project Goals

1. **Knowledge base + curriculum for reliable long-running agents.** Base de conhecimento e programa curricular para sistemas de IA que operam de forma confiável por horas ou dias sem perder contexto, planejamento ou julgamento de qualidade (`/mnt/c/Users/pavan/long-running-agents/README.md:12`).
2. **Teach and operationalize harness engineering.** A tese central: a degradação de agentes longos não é limitação de modelo, é lacuna de engenharia; a disciplina é construir a infraestrutura de suporte (harness) ao redor do modelo (`/mnt/c/Users/pavan/long-running-agents/README.md:16`, `/mnt/c/Users/pavan/long-running-agents/README.md:18`).
3. **Attack three structural failures.** Perda de contexto, planejamento frágil e autoavaliação cega (`/mnt/c/Users/pavan/long-running-agents/README.md:24`-`28`); harnesses são definidos como as estruturas que gerenciam contexto, decompõem trabalho e separam geração de avaliação (`/mnt/c/Users/pavan/long-running-agents/README.md:30`).
4. **Deliver a 12-week curriculum as the main product.** 4 níveis, 8 conceitos core, 35+ diagramas, ancorado no caso real KODA, agente de venda de suplementos via WhatsApp (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:13`, `/mnt/c/Users/pavan/long-running-agents/README.md:20`, `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:71`).
5. **Run an automated external-knowledge pipeline.** O harness em `harness/` orquestra o pipeline `analyze-and-improve` (7 fases com evaluators e gates): alimenta uma fonte externa (talk, paper, transcript) e obtém padrões extraídos, classificados contra o repositório e integrados como canonical docs, skills ou exercícios (`/mnt/c/Users/pavan/long-running-agents/README.md:102`, `/mnt/c/Users/pavan/long-running-agents/README.md:136`).
6. **Serve as a reusable agent-system template.** `.opencode/` é um sistema completo de agentes (Handoff Protocol + skills) adaptável como template para outros projetos agentic (`/mnt/c/Users/pavan/long-running-agents/README.md:140`).
7. **Govern documentation by precedence.** ADRs > canonical > evidence > analysis > archive > READMEs, resolvido pelo system of record (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:14`-`21`, `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:80`-`91`).
8. **Agent operational discipline.** Regras obrigatórias para agentes de IA no repo: uma tarefa por sessão, não assumir, mudança mínima, verificação definida antes de implementar, issues/branches traceáveis, gates reais de validação (`/mnt/c/Users/pavan/long-running-agents/AGENTS.md:14`-`16`, `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:26`-`32`, `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:42`-`48`, `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:69`-`78`).

**Audience:** pessoas de negócio com skill em construção de agentes e sistemas agenticos, de iniciantes a operadores de produção (`/mnt/c/Users/pavan/long-running-agents/README.md:34`).

---

## 2. Architecture

### 2.1 Core abstractions

| Abstraction | Role | Evidence |
|---|---|---|
| **System of Record** | Mapa das fontes canônicas; resolve conflitos por precedência e define os domínios do projeto | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:12`, `:14`-`21`, `:23` |
| **Canonical pattern library** | Camada autoritativa de padrões agentic ativos; ~116 padrões em `docs/canonical/` (129 entradas no diretório), cada um com problema/mecanismo/trade-offs | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:166`-`170`; directory listing 2026-08-30 |
| **Curriculum** | Produto principal: programa de 12 semanas, 4 níveis, master docs (MASTER_PLAN, QUICK_START, GLOSSARY, EXECUTION_PLAN, INDEX, FAQ) e diretórios 01-10 | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:71`-`93` |
| **.opencode agent system (HoP)** | Sistema de agentes no modelo HoP (Handoff Protocol): escopo fechado, dono e gates de validação por agente | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:27`; `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:9` |
| **HoP agents (3)** | `hop-orchestrator-rezek` (orquestrador primário, governança e coordenação), `koda-hop-init-basic` (inicial guiada do KODA), `hop-live-whatsapp-tester` (teste live WhatsApp) | `/mnt/c/Users/pavan/long-running-agents/README.md:103`; `/mnt/c/Users/pavan/long-running-agents/.opencode/agents/hop-orchestrator-rezek.md:21`-`29` |
| **Skills layer** | 31 diretórios de skills em `.opencode/skills/` (README declara "28 skills" — drift de contagem): issue lifecycle, orquestração, docs, planos, error hygiene, shadow review, token budget, constraint gates, intent decomposition, analyze-and-improve, etc. | `/mnt/c/Users/pavan/long-running-agents/README.md:104`; `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:33`-`65`; directory listing 2026-08-30 |
| **Analysis pipeline (analyze-and-improve)** | Pipeline conhecimento → mental model → extração → padrões → classificação → integração; 8 módulos stdlib com cache, retry, model tiering, schemas, chunking, trajectory, eval, refinement | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:46`; `/mnt/c/Users/pavan/long-running-agents/README.md:102` |
| **Harness runtime** | `harness/` com `GUIDE-analyze-and-improve.md`, `harness-analysis.sh`, templates e resultados de teste | `/mnt/c/Users/pavan/long-running-agents/harness/` (directory listing 2026-08-30) |
| **KODA case domain** | Domínio aplicado: product discovery, order processing, fulfillment, journeys, rubrics; conversas de 2+ horas via WhatsApp | `/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:34`; `/mnt/c/Users/pavan/long-running-agents/README.md:20` |
| **Stack e tooling** | Node >= 20.18.0 ESM, ESLint 10 + 2 regras customizadas, OpenCode, Obsidian (wikilinks/dataview), CLI `obsidian-eval`, portais HTML estáticos com Mermaid | `/mnt/c/Users/pavan/long-running-agents/README.md:153`-`161`; `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:115`-`127` |
| **Runtime state** | `.runtime/` e `artifacts/` guardam estado de execução; modificação casual proibida (Rule 15) | `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:11`, `:132`-`134` |
| **Governança GitHub** | PR template com checklist de crossroad files, CODEOWNERS, issue templates, dependabot, script de criação de issues do currículo | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:129`-`139` |

### 2.2 Relationships

- **AGENTS.md ↔ System of Record:** AGENTS.md governa comportamento de agentes e gates (`/mnt/c/Users/pavan/long-running-agents/AGENTS.md:3`, `:69`-`78`); o system of record governa autoridade documental (Rule 8 remete a ele: `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:80`-`91`).
- **Curriculum → Canonical docs:** o currículo aponta consultas de evals e padrões para `docs/canonical/` (ex.: pain-signal-eval-progression-gate, eval-tier-stratification) (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:347`-`356`).
- **Pipeline → canonical/skills/exercícios:** `analyze-and-improve` transforma fontes externas em canonical docs, skills ou exercícios (`/mnt/c/Users/pavan/long-running-agents/README.md:136`); sessões de análise produzem pacotes `analysis/patterns/classification/mental-model/roadmap` (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:321`-`399`).
- **Canonical docs ↔ Skills:** o ADR aceito Skill-Canons Bridge conecta skills do ecossistema aos padrões canônicos do vault via bridge Level 3 (inline injection, promotion rule D8, snapshot baseline, budget gate 4 fases, cópia local DRY) (`/mnt/c/Users/pavan/long-running-agents/docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:27`-`43`).
- **Generator/Evaluator ↔ cluster de evals:** o canonical Generator-Evaluator relaciona-se com multi-model-evaluation-council, eval-tier-stratification, pr-gated-eval-enforcement, production-grounded-eval-sampling, constraint-anchored-evaluation (`/mnt/c/Users/pavan/long-running-agents/docs/canonical/generator-evaluator.md:7`).
- **Trace instrumentation ↔ telemetria:** o canonical trace-instrumentation liga-se ao stack de telemetria do runtime Sisyphus e à CLI obsidian-eval (epistemic graph) (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:124`-`127`).
- **Currículo → KODA:** conceitos genéricos de confiabilidade culminam na arquitetura KODA, journeys, feature patterns, rubrics e melhorias (Nível 4) (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:246`-`257`).
- **Glossário → canonical docs:** cada termo avançado do glossário referencia seu canonical doc (ex.: Agent Degradation Loop Prevention → canonical correspondente) (`/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:37`, `:102`, `:118`).

---

## 3. Patterns

Padrões existentes, com maturidade declarada. "SOR" = linha da tabela de padrões canônicos ativos em `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:172`-`300`.

**Clusters de padrões canônicos (ativos):**

| Cluster | Padrões representativos | Maturidade |
|---|---|---|
| Control loop e dispatch | Owned Agent Control Loop (SOR `:176`), Deterministic Tool Dispatch (SOR `:175`), Application-Owned Agent Control Plane (SOR `:179`), Value-Gated Agent Control Loop (SOR `:232`) | Active canonical |
| Erros e degradação | Error Context Hygiene (SOR `:174`), Tested Degradation Ladder (SOR `:182`), Agent Degradation Loop Prevention (SOR `:273`) | Active canonical |
| Estado e persistência | Serializable Pause/Resume State (SOR `:177`), Versioned Durable Agent State (SOR `:181`), External State Persistence (SOR `:213`), File-System Materialization (SOR `:299`) | Active canonical |
| Contexto e memória | Head-Tail Context Truncation (SOR `:184`), Hybrid Context Stack (SOR `:191`), Addressable Memory Catalog (SOR `:193`), Tiered Context Storage (SOR `:266`), Relational Context Graph (SOR `:271`), Deliberate Forgetting (SOR `:269`), Smallest Sufficient Context (SOR `:270`) | Active canonical |
| Token economics | Explicit Token Budget Ledger (SOR `:185`), Burn-Rate Runtime Forecast (SOR `:186`), Phase-Gated Token Health Monitor (SOR `:187`), Budget-Aware Session Handoff (SOR `:192`), Token Economics Gap Filling (SOR `:242`) | Active canonical |
| Evals | Eval Tier Stratification (SOR `:200`), Pain-Signal Eval Progression Gate (SOR `:197`), Production-Grounded Eval Sampling (SOR `:199`), Production Failure Regression Flywheel (SOR `:203`), 3-Layer Evaluation Architecture (SOR `:285`), Living Eval Dataset (SOR `:287`), Behavioral Eval Path Analysis (SOR `:201`) | Active canonical |
| Planejamento e intenção | Plan-Execute-Verify (SOR `:214`), Generator/Evaluator (SOR `:215`), Intent Five-Part Primitive (SOR `:234`), Goal-Atomicity Split (SOR `:252`), Two-Implementations Goal Test (SOR `:251`), Constraint Budget Gate (SOR `:253`), Constraint-Failure Decision Rule (SOR `:254`) | Active canonical |
| Revisão e segurança | Shadow Review Pipeline (SOR `:244`), Contextual Severity Calibration (SOR `:245`), Review Contract Checklist (SOR `:246`), Pre-Commit AI Review Gate (SOR `:247`), Manual Brake Question Gate (SOR `:228`), Devil's Advocate (skill, `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:63`) | Active canonical / skill |
| Harness lifecycle | Measured Harness Evolution Lifecycle BUILD → STABILIZE → SIMPLIFY → REMOVE (SOR `:150`, `:183`), Garbage Collection Day Meta-Loop (SOR `:226`), Failure Pattern Classification Loop (SOR `:227`) | Active canonical |
| ADR formalizado | Skill-Canons Bridge Ondas 0-2: 5 decisões cross-cutting (grounding inline, promotion D8, baseline snapshot, budget gate 4 fases, DRY cópia local) | Accepted ADR (`/mnt/c/Users/pavan/long-running-agents/docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:35`-`43`) |

**Padrões de exemplo com granularidade inspecta:**

- **Generator-Evaluator** — dois agentes (Generator criativo/voltado ao usuário; Evaluator imparcial/voltado a constraints) com loop approve/reject; classificação declarada "Partial Coverage — 12+ eval infrastructure docs exist, no unified Generator-Evaluator architecture doc" (`/mnt/c/Users/pavan/long-running-agents/docs/canonical/generator-evaluator.md:11`-`31`, classificação em `:16`). Quantificação do problema: self-evaluation detecta ~3% dos erros reais vs ~14% de avaliador externo (`/mnt/c/Users/pavan/long-running-agents/docs/canonical/generator-evaluator.md:27`).
- **Issue lifecycle (skills):** issue-start (claim → worktree → execution brief), issue-review (validação → draft PR → second-agent review), issue-finish (merge → cleanup), issue-workflow (ciclo completo) (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:36`-`39`).
- **Karpathy guidelines (skill):** Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution — referenciadas como detalhe operacional das Rules 1-4 do AGENTS.md (`/mnt/c/Users/pavan/long-running-agents/AGENTS.md:24`, `:32`, `:40`, `:48`; `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:44`).
- **Obsidian document conventions (Rule 16):** frontmatter obrigatório por tipo de documento, wikilinks para toda referência interna, tags derivadas dos domínios do SOR, slug naming, validação por `scripts/validate-obsidian.ts` (`/mnt/c/Users/pavan/long-running-agents/AGENTS.md:136`-`257`).
- **Commit/PR style:** `type(scope): short description`, `[FUP-N]` para follow-ups, PRs com checklist de crossroad files (`/mnt/c/Users/pavan/long-running-agents/AGENTS.md:59`-`67`; `/mnt/c/Users/pavan/long-running-agents/README.md:174`).

---

## 4. Abstractions — key terminology

Termos com definição e fonte (glossário, canonical docs, README/AGENTS).

| Term | Definition | Source |
|---|---|---|
| **Agent** | Entidade autônoma de IA (geralmente LLM) que toma ações, usa ferramentas e executa tarefas em sequência | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:17`-`24` |
| **Agent Loop** | Ciclo repetitivo input → pensa → ação → resultado → repete | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:41`-`47` |
| **Harness / Harness Engineering** | Infraestrutura de suporte que envolve o modelo e garante confiabilidade em execuções longas; engenharia de software aplicada ao runtime do agente | `/mnt/c/Users/pavan/long-running-agents/README.md:18` |
| **KODA** | Agente de venda de suplementos via WhatsApp que precisa manter qualidade em conversas de 2+ horas; caso âncora do repositório | `/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:34`; `/mnt/c/Users/pavan/long-running-agents/README.md:20` |
| **HoP (House of Pace) / Handoff Protocol** | Modelo do sistema de agentes: cada agente tem escopo fechado, dono e gates de validação | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:27`; `/mnt/c/Users/pavan/long-running-agents/.opencode/agents/hop-orchestrator-rezek.md:21` |
| **Amnesia (Context Amnesia)** | Agente "esquece" contexto anterior por exceder a janela; solução: state persistence + memory management | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:50`-`58` |
| **Compaction** | Resumir/comprimir contexto antigo para abrir espaço mantendo informações-chave (server-side quando feito pelo servidor/modelo) | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:81`-`87` |
| **Generator/Evaluator** | Separação em dois agentes: Generator (criativo, janela de conversa) e Evaluator (imparcial, constraints/rubrics/estado persistido) com veredicto approve/reject | `/mnt/c/Users/pavan/long-running-agents/docs/canonical/generator-evaluator.md:29`-`31` |
| **Compartmented Evaluation Architecture** | Builder e Validator recebem superfícies de informação seladas para impedir reward-hacking (otimizar para checks visíveis em vez de outcomes) | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:90`-`102` |
| **Constraint Budget Gate** | Limite de 5-7 constraints direcionais, incondicionais e em linguagem de negócio por tarefa; excedentes são reclassificados como contexto ou failure conditions | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:106`-`118` |
| **Agent Degradation Loop Prevention** | Framework diagnóstico dos 4 elos do loop de degradação: atenção desigual, erros que se compõem, fragmentação de estado externo, feedback inerte de memória | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:28`-`37` |
| **Closed-Loop Company** | Agentes leem estado real da empresa (código, issues, artefatos) e devolvem trabalho/decisões fechando o ciclo observação → execução | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:74`-`78` |
| **ADR (Architecture Decision Record)** | Documento que registra decisão de arquitetura, contexto e consequências; topo da precedência documental | `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md:61`-`68`; `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:16` |
| **System of Record** | Fonte da verdade: precedência, domínios do projeto, padrões ativos e status de ADRs | `/mnt/c/Users/pavan/long-running-agents/README.md:127`; `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:12` |
| **analyze-and-improve** | Pipeline/harness que converte fontes externas em padrões classificados e integrados ao repositório | `/mnt/c/Users/pavan/long-running-agents/README.md:136`; `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:46` |
| **12-Factor Agents** | Talk de origem (Dex Horthy, AI Engineer 2025) de vários padrões canônicos (error-context-hygiene = Padrão 6, deterministic-tool-dispatch = Padrão 2, etc.) | `/mnt/c/Users/pavan/long-running-agents/README.md:67`; `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:174`-`177` |
| **Skill-Canons Bridge** | Framework de 3 níveis de bridging que conecta skills do ecossistema aos padrões canônicos do vault | `/mnt/c/Users/pavan/long-running-agents/docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:27`-`31` |

**Domínios do projeto (taxonomia de tags):** Agentes e orquestração; Currículo e conteúdo; Portal web; Stack e tooling; Governança de repositório; Testes e QA (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:23`-`151`; tags derivadas em `/mnt/c/Users/pavan/long-running-agents/AGENTS.md:171`-`200`).

---

## 5. Curriculum Structure

- **Programa:** 12 semanas, 4 níveis, 8 conceitos core, 35+ diagramas Mermaid; 30-50 horas por pessoa (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:13`, `:296`).
- **Master docs:** MASTER_PLAN (índice geral), QUICK_START (45 min), GLOSSARY, EXECUTION_PLAN (cronograma), INDEX, FAQ (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:76`-`80`).

**Níveis (progressão):**

| Nível | Diretório | Pergunta / Foco | Carga |
|---|---|---|---|
| 1 — Fundamentos | `curriculum/01-nivel-1-fundamentals/` | Por que agentes falham? Context windows, token budgeting, harness básico | 3-4h (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:202`-`210`) |
| 2 — Padrões Práticos | `curriculum/02-nivel-2-practical-patterns/` | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading | 6-8h (`:216`-`227`) |
| 3 — Arquitetura Avançada | `curriculum/03-nivel-3-advanced-architecture/` (+ `03-nivel-3-operacional/`, `03-nivel-arquiteto/`, `04-nivel-3-engenharia-avancada/`) | Multi-agent, state persistence, file-based coordination, server-side compaction, harness evolution | 8-10h (`:231`-`242`) |
| 4 — Aplicação KODA | `curriculum/04-nivel-4-koda-specific/` | Arquitetura KODA, customer journeys, feature patterns, rubrics, implementação | Contínuo (`:246`-`257`) |

**8 conceitos core** (`curriculum/05-core-concepts/`), cada um com explicação profunda, 3 knowledge graphs, aplicação KODA e checklist (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:261`-`280`): Context Management; Planning vs. Execution; Generator/Evaluator; Sprint Contracts; State Persistence; Harness Evolution; Multi-Agent Coordination; Evaluation Rubrics.

**Diretórios complementares:** `06-knowledge-graphs/` (35+ diagramas), `07-implementation-guides/`, `08-tools-templates/` (sprint contract, rubrica, ADR, progress tracker), `09-case-studies/` (5 casos: retro-game-maker, browser-daw, 3× KODA), `10-references/` (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:88`-`93`).

**Exercícios:** por nível, com solutions (ex.: N2 inclui exercise-04-error-context-hygiene, two-implementations-goal-test, goal-atomicity-split; N3 inclui constraint gates, autonomy-curriculum-sampling, magnitude-direction-verifier-split; N4 inclui manual-brake-question-gate, deferred-ledger-agentic-work) (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:84`-`143`).

**Cronograma:** Semanas 1-2 fundação (N1) → 3-4 padrões (N2) → 5-6 arquitetura (N3 subconjunto) → 7-12 aplicação (N4) (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:286`-`294`).

**Métricas de sucesso:** marcos por 2/4/6/12 semanas (100% entende os 3 problemas; rubrics para 2+ features; 60-80% em N3; 50%+ em N4 mentoreando novos membros) (`/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:453`-`474`).

**Material-fonte:** `rawfiles/` (material usado para gerar o currículo) e `prompts/` (prompts de geração) (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:93`-`94`).

---

## 6. Existing Gaps (documented)

| # | Gap | Where documented |
|---|---|---|
| 1 | `docs/canonical/agent-lifecycle.md` (ciclo claim → worktree → implement → review → merge → cleanup) pendente | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:67` |
| 2 | `docs/canonical/curriculum-model.md` (taxonomia de níveis, tipos de artefato, critérios de qualidade) pendente | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:96` |
| 3 | `docs/canonical/portal-architecture.md` pendente, a criar quando a SPA proposta for implementada | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:109` |
| 4 | `docs/canonical/crossroad-change-policy.md` e arquivos `src/lib/*` (safe-console, logger) referenciados pelo PR template mas inexistentes | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:141` |
| 5 | Tabela de canonical docs pendentes: agent-lifecycle, curriculum-model, portal-architecture, crossroad-change-policy; obsidian-document-conventions só se a convenção crescer além da Rule 16 | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:301`-`307` |
| 6 | ADRs candidatos ainda não formalizados: stack do portal, modelo de content chunking, persistência de estado entre agentes, versionamento do currículo | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:160`-`164` |
| 7 | Ações pendentes do ADR Skill-Canons Bridge: atualizar system-design para budget gate 4 fases; extrair shared module quando >5 skills com bridge; capturar runs manuais de baseline | `/mnt/c/Users/pavan/long-running-agents/docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:91`-`93` |
| 8 | FAQ do currículo "em construção" | `/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:69`, `:487` |
| 9 | Os 8 conceitos core com status ⏳ (pendente) na tabela de status | `/mnt/c/Users/pavan/long-running-agents/curriculum/README.md:269`-`278` |
| 10 | Generator-Evaluator classificado "Partial Coverage": 12+ docs de infra de eval existem, mas não há doc unificado da arquitetura Generator-Evaluator | `/mnt/c/Users/pavan/long-running-agents/docs/canonical/generator-evaluator.md:16` |
| 11 | Contagem de skills divergente: README declara "28 skills" (`:104`); o diretório `.opencode/skills/` tem 31 entradas (listing 2026-08-30) | `/mnt/c/Users/pavan/long-running-agents/README.md:104` vs `.opencode/skills/` listing |
| 12 | Nomenclatura de níveis inconsistentes no currículo: coexistem `03-nivel-3-advanced-architecture`, `03-nivel-3-operacional`, `03-nivel-arquiteto`, `04-nivel-3-engenharia-avancada`, `04-nivel-4-koda-specific` | `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:83`-`87`; curriculum directory listing 2026-08-30 |

---

## Notes for downstream phases

- A precedência documental (ADRs > canonical > evidence > analysis > READMEs) define onde qualquer conteúdo novo derivado da fonte externa deve pousar: análise vive em `docs/analysis/<date>-<slug>/`, padrões aceitos sobem para `docs/canonical/`, e integração segue o contrato da skill `analyze-and-improve` (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:394`-`399`).
- Formato legacy vs atual: sessões pós-2026-06-14 usam `<date>-<source-slug>-artifacts.{md,yaml}` em vez de `integration-roadmap.md` (`/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md:394`-`399`).
- Qualquer novo doc em `docs/analysis/` deve ter frontmatter completo (title, type: analysis, tags de domínio, date, aliases, relates-to) e wikilinks — hard error no CI (`/mnt/c/Users/pavan/long-running-agents/AGENTS.md:143`-`145`, `:242`-`257`).
