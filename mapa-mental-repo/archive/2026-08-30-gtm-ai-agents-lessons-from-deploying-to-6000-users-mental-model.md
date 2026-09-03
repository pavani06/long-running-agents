---
title: "Mental Model: GTM AI Agents — Lessons from Deploying to 6000 Users (Repository Rebuild)"
type: analysis
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "governanca"]
date: 2026-08-30
aliases: ["gtm ai agents mental model", "repo mental model rebuild 2026-08-30", "long-running-agents mental model gtm-6000-users"]
relates-to:
  - "[[docs/system-of-record|System of Record]]"
  - "[[README|Repository README]]"
  - "[[AGENTS|Agent Rules]]"
  - "[[curriculum/README|Curriculum README]]"
  - "[[curriculum/GLOSSARY|Glossary]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/decisions/2026-06-24-skill-canons-bridge-implementation|Skill-Canons Bridge ADR]]"
sources:
  - "[[AGENTS|AGENTS]]"
  - "[[README|README]]"
  - "[[docs/system-of-record|System of Record]]"
  - "[[curriculum/README|Curriculum README]]"
  - "[[curriculum/GLOSSARY|Glossary]]"
  - "[[docs/decisions/2026-06-24-skill-canons-bridge-implementation|ADR Skill-Canons Bridge]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
---

# Mental Model: long-running-agents (Full Rebuild, 2026-08-30)

**Data:** 2026-08-30
**Repo:** `long-running-agents` em `/home/pavanpavan/long-running-agents` (branch `main`)
**Escopo:** Somente o repositório. O documento-fonte externo (GTM AI Agents / deploying to 6000 users) NÃO foi analisado neste passo.

Citações `file:line` usam paths relativos à raiz do repositório. Este modelo é um rebuild completo — nenhum modelo anterior foi usado como base. O estado atual inclui os artefatos absorvidos pelos commits `2e38fea` (pacote kavak-playbook: 13 canonical docs + 9 enriquecimentos de currículo + skill mega-expert-consolidation + exercise-07) e `dfb67d8` (qi-loop iter 1: skill sidekick-pattern-physical-boundaries, exercise-08, classification batches 1-2, mental model kavak em `mapa-mental-repo/`), verificados via `git show --stat` em 2026-08-30.

---

## 1. Project Goals

1. **Base de conhecimento + currículo para agentes long-running confiáveis.** Sistemas de IA que operam de forma confiável por horas ou dias sem perder contexto, capacidade de planejamento ou julgamento de qualidade (`README.md:12`).
2. **Ensinar e operacionalizar harness engineering.** Tese central: a degradação de agentes longos não é limitação de modelo, é lacuna de engenharia; a disciplina é construir a infraestrutura de suporte (harness) ao redor do modelo — engenharia de software aplicada ao runtime do agente (`README.md:16`-`18`).
3. **Atacar três falhas estruturais.** Perda de contexto, planejamento frágil e autoavaliação cega (`README.md:24`-`28`); harnesses gerenciam contexto, decompõem trabalho e separam geração de avaliação (`README.md:30`).
4. **Entregar o currículo de 12 semanas como produto principal.** 4 níveis, 8 conceitos core, 35+ diagramas Mermaid, ancorado no caso real KODA — agente de venda de suplementos via WhatsApp com conversas de 2+ horas (`curriculum/README.md:13`, `README.md:20`, `docs/system-of-record.md:71`-`72`).
5. **Rodar o pipeline automatizado de análise de conhecimento externo.** O harness em `harness/` orquestra o pipeline `analyze-and-improve` (7 fases com evaluators e gates): alimenta uma fonte externa (talk, paper, transcript) e obtém padrões extraídos, classificados contra o repositório e integrados como canonical docs, skills ou exercícios (`README.md:102`, `README.md:136`; `docs/system-of-record.md:46`).
6. **Servir de template de sistema de agentes reutilizável.** `.opencode/` é um sistema completo (Handoff Protocol + skills + agentes) adaptável a outros projetos agenticos (`README.md:140`).
7. **Governar documentação por precedência.** ADRs > canonical > evidence > analysis > archive > READMEs, resolvido pelo system of record (`docs/system-of-record.md:14`-`21`; `AGENTS.md:80`-`91`).
8. **Disciplina operacional de agentes.** Regras obrigatórias para agentes de IA no repo: uma tarefa por sessão (Rule 0), não assumir, mudança mínima, verificação definida antes de implementar, issues/branches traceáveis, gates reais de validação (`AGENTS.md:14`-`16`, `:26`-`32`, `:42`-`48`, `:50`-`57`, `:69`-`78`).

**Audiência:** pessoas de negócio com skill em construção de agentes e sistemas agenticos, de iniciantes a operadores de produção (`README.md:34`).

---

## 2. Architecture

### 2.1 Abstrações core

| Abstração | Papel | Evidência |
|---|---|---|
| **System of Record** | Mapa das fontes canônicas; resolve conflitos por precedência e define os 6 domínios do projeto | `docs/system-of-record.md:12`, `:14`-`21`, `:23` |
| **Biblioteca de padrões canônicos** | Camada autoritativa de padrões agentic ativos; **142 arquivos** em `docs/canonical/` (listagem 2026-08-30), cada um com problema/mecanismo/trade-offs; inclui o cluster Kavak absorvido em 2026-08-30 | `docs/system-of-record.md:167`-`169`; directory listing 2026-08-30 |
| **Currículo** | Produto principal: 12 semanas, 4 níveis, 8 conceitos core, master docs (MASTER_PLAN, QUICK_START, GLOSSARY, EXECUTION_PLAN, INDEX, FAQ) e diretórios 01-10 | `docs/system-of-record.md:71`-`97` |
| **Sistema de agentes `.opencode/` (HoP)** | Modelo HoP (House of Pace) / Handoff Protocol: cada agente com escopo fechado, dono e gates de validação | `docs/system-of-record.md:27`; `AGENTS.md:9` |
| **Agentes HoP (3)** | `hop-orchestrator-rezek` (orquestrador primário: negócio→produto→técnica→GTM com governança e red-team antes de GTM), `koda-hop-init-basic` (inicialização guiada de testes KODA, coleta de telefone + menu de 3 caminhos), `hop-live-whatsapp-tester` (testes live do KODA com cenários, OTP/token, captura de resposta real e promoção para regressão) | `README.md:103`; `.opencode/agents/hop-orchestrator-rezek.md:21`-`39`; `.opencode/agents/koda-hop-init-basic.md:16`-`26`; `.opencode/agents/hop-live-whatsapp-tester.md:20`, `:35`-`59` |
| **Camada de skills** | **33 diretórios** em `.opencode/skills/` (listagem 2026-08-30): issue lifecycle, orquestração, docs, planos, error hygiene, shadow review, token budget, constraint gates, intent decomposition, analyze-and-improve, mega-expert-consolidation, sidekick-pattern-physical-boundaries, etc. | `docs/system-of-record.md:33`-`65`; directory listing 2026-08-30 |
| **Pipeline de análise (analyze-and-improve)** | Pipeline conhecimento → mental model → extração → padrões → classificação → integração; 8 módulos stdlib com cache, retry, model tiering, schemas, chunking, trajectory, eval, refinement | `docs/system-of-record.md:46`; `README.md:102` |
| **Runtime do harness** | `harness/` com `GUIDE-analyze-and-improve.md`, `harness-analysis.sh`, `templates/`, `test-results.json` | `harness/` (directory listing 2026-08-30) |
| **Domínio aplicado KODA** | Product discovery, order processing, fulfillment, journeys, rubrics; conversas de 2+ horas via WhatsApp | `curriculum/README.md:34`; `README.md:20` |
| **Stack e tooling** | Node >= 20.18.0 ESM, ESLint 10 + 2 regras customizadas (`no-catch-message`, `no-raw-console-in-scripts`), OpenCode, Obsidian (wikilinks/dataview), CLI `obsidian-eval`, portais HTML estáticos com Mermaid | `README.md:153`-`161`; `docs/system-of-record.md:113`-`128` |
| **Estado de runtime** | `.runtime/` e `artifacts/` guardam estado de execução; modificação casual proibida (Rule 15) | `AGENTS.md:11`, `:132`-`134` |
| **Governança GitHub** | PR template com checklist de crossroad files, CODEOWNERS, issue templates, dependabot, script de criação de issues do currículo | `docs/system-of-record.md:130`-`142` |
| **Mapas mentais de fontes** | `mapa-mental-repo/` guarda os mental models dos pipelines (5 ativos em 2026-08-30: idsd, quarto, simpler-than-you-think, production-playbook, kavak) | `mapa-mental-repo/` (directory listing 2026-08-30) |

### 2.2 Relacionamentos

- **AGENTS.md ↔ System of Record:** AGENTS.md governa comportamento de agentes e gates de validação (`AGENTS.md:3`, `:69`-`78`); o SOR governa autoridade documental (Rule 8 remete a ele: `AGENTS.md:80`-`91`).
- **Currículo → Canonical docs:** o currículo aponta consultas de evals e padrões para `docs/canonical/` (ex.: pain-signal-eval-progression-gate, eval-tier-stratification) (`curriculum/README.md:351`-`358`).
- **Pipeline → canonical/skills/exercícios:** `analyze-and-improve` transforma fontes externas em canonical docs, skills ou exercícios (`README.md:136`); cada sessão produz um pacote em `docs/analysis/<date>-<slug>/` com analysis/patterns/classification/mental-model/artifacts (`docs/system-of-record.md:408`-`415` para o pacote kavak).
- **Canonical docs ↔ Skills:** o ADR aceito Skill-Canons Bridge conecta skills do ecossistema aos padrões canônicos do vault via bridge Level 3 — 5 decisões: grounding inline (Opção B), promotion rule D8, baseline por snapshot, budget gate 4 fases, DRY por cópia local (`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:35`-`43`).
- **Canonical docs ↔ pacotes de análise:** cada canonical derivado de fonte externa referencia o pacote de origem em `sources:`/`relates-to` do frontmatter (ex.: `evals-as-brakes.md` referencia o pacote kavak, `docs/canonical/evals-as-brakes.md:20`-`23`).
- **Generator/Evaluator ↔ cluster de evals:** o canonical Generator-Evaluator relaciona-se com multi-model-evaluation-council, eval-tier-stratification, pr-gated-eval-enforcement, production-grounded-eval-sampling, constraint-anchored-evaluation (listados juntos na tabela do SOR: `docs/system-of-record.md:210`-`216`).
- **Trace instrumentation ↔ telemetria:** o canonical trace-instrumentation liga-se ao stack de telemetria do runtime Sisyphus e à CLI obsidian-eval (epistemic graph) (`docs/system-of-record.md:125`-`128`).
- **Currículo → KODA:** conceitos genéricos de confiabilidade culminam na arquitetura KODA, journeys, feature patterns, rubrics e melhorias (Nível 4) (`curriculum/README.md:246`-`259`).
- **Glossário → canonical docs:** termos avançados do glossário referenciam seus canonical docs via wikilink (ex.: Agent Degradation Loop Prevention → `docs/canonical/agent-degradation-loop-prevention`) (`curriculum/GLOSSARY.md:37`, `:102`, `:118`, `:134`).
- **Handoff entre agentes:** `koda-hop-init-basic` entrega telefone confirmado + opção 2 para `hop-live-whatsapp-tester`, que opera em modo chat direto sem re-pedir o número (`.opencode/agents/koda-hop-init-basic.md:50`; `.opencode/agents/hop-live-whatsapp-tester.md:56`-`57`).

---

## 3. Patterns

"SOR" = linha da tabela de padrões canônicos ativos em `docs/system-of-record.md:172`-`313`. Maturidade = status declarado no canonical (frontmatter `Status: Active`, precedência Level 2).

**Clusters de padrões canônicos (ativos):**

| Cluster | Padrões representativos | Maturidade |
|---|---|---|
| Control loop e dispatch | Owned Agent Control Loop (SOR `:176`), Deterministic Tool Dispatch (SOR `:175`), Application-Owned Agent Control Plane (SOR `:179`), Value-Gated Agent Control Loop (SOR `:233`) | Active canonical |
| Erros e degradação | Error Context Hygiene (SOR `:174`), Tested Degradation Ladder (SOR `:183`), Agent Degradation Loop Prevention (SOR `:274`) | Active canonical |
| Estado e persistência | Serializable Pause/Resume State (SOR `:177`), Versioned Durable Agent State (SOR `:181`), External State Persistence (SOR `:214`), File-System Materialization (SOR `:300`) | Active canonical |
| Contexto e memória | Head-Tail Context Truncation (SOR `:184`), Hybrid Context Stack (SOR `:192`), Addressable Memory Catalog (SOR `:194`), Tiered Context Storage (SOR `:267`), Relational Context Graph (SOR `:272`), Deliberate Forgetting (SOR `:270`), Smallest Sufficient Context (SOR `:271`) | Active canonical |
| Token economics | Explicit Token Budget Ledger (SOR `:185`), Burn-Rate Runtime Forecast (SOR `:186`), Phase-Gated Token Health Monitor (SOR `:187`), Budget-Aware Session Handoff (SOR `:193`), Token Economics Gap Filling (SOR `:243`) | Active canonical |
| Evals | Eval Tier Stratification (SOR `:201`), Pain-Signal Eval Progression Gate (SOR `:198`), Production-Grounded Eval Sampling (SOR `:200`), Production Failure Regression Flywheel (SOR `:204`), 3-Layer Evaluations Architecture (SOR `:286`), Living Eval Dataset (SOR `:288`), Behavioral Eval Path Analysis (SOR `:202`), Eval Dashboard Primary Detection Surface (SOR `:280`) | Active canonical |
| Planejamento e intenção | Plan-Execute-Verify (SOR `:215`), Generator/Evaluator (SOR `:216`), Intent Five-Part Primitive (SOR `:235`), Goal-Atomicity Split (SOR `:253`), Two-Implementations Goal Test (SOR `:252`), Constraint Budget Gate (SOR `:254`), Constraint-Failure Decision Rule (SOR `:255`) | Active canonical |
| Revisão e segurança | Shadow Review Pipeline (SOR `:245`), Contextual Severity Calibration (SOR `:246`), Review Contract Checklist (SOR `:247`), Pre-Commit AI Review Gate (SOR `:248`), Manual Brake Question Gate (SOR `:229`), Accidental Brake Replacement (SOR `:232`) | Active canonical |
| Harness lifecycle | Measured Harness Evolution Lifecycle BUILD → STABILIZE → SIMPLIFY → REMOVE (SOR `:151`, `:184`), Garbage Collection Day Meta-Loop (SOR `:227`), Failure Pattern Classification Loop (SOR `:228`) | Active canonical |
| **Cluster Kavak (absorvido 2026-08-30)** | Model-Agnostic Agent-VM Harness (SOR `:301`), Alarm-Clock Agent Lifecycle (SOR `:302`), Evals-as-Brakes (SOR `:303`), Carve-Out Pilot Hard Target (SOR `:304`), Mega-Expert Consolidation (SOR `:305`), Sidekick Pattern Physical Boundaries (SOR `:306`), Agent-Per-Customer Outcome Ownership (SOR `:307`), Goal-Driven Agents over Workflows (SOR `:308`), Shared-Fleet Learning (SOR `:309`), Closed-Loop Help API (SOR `:310`), Eval Investment Parity (SOR `:311`), Outcome-Level Eval Hierarchy (SOR `:312`), Production Contact Training Loop (SOR `:313`) | Active canonical (source: a16z Kavak, `docs/canonical/evals-as-brakes.md:17`) |
| Sierra (enterprise) | Multi-Provider Model Routing, Confidence-Gated Continual Learning, Regulated Data Boundary, Auth-Coupled Memory, Task-Routed Model Tiering, Temporal Context Injection, Three-Tier Memory Persistence, Always-On Monitoring Human Triage, Model-Switch-Driven Eval Hardening (SOR `:291`-`299`) | Active canonical |

**Padrões operacionais (fora do canonical):**

- **Issue lifecycle (skills):** issue-start (claim → worktree → execution brief), issue-review (validação → draft PR → second-agent review), issue-finish (merge → cleanup), issue-workflow (ciclo completo), refine-issue (decomposição em sub-issues) (`docs/system-of-record.md:36`-`40`).
- **Karpathy guidelines (skill):** Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution — detalhe operacional das Rules 1-4 do AGENTS.md (`AGENTS.md:24`, `:32`, `:40`, `:48`; `docs/system-of-record.md:44`).
- **Obsidian document conventions (Rule 16):** frontmatter obrigatório por tipo de documento, wikilinks `[[path|Display]]` para toda referência interna, tags derivadas dos domínios do SOR, slug naming, `relates-to` obrigatório, validação por `scripts/validate-obsidian.ts` (`AGENTS.md:136`-`257`).
- **Commit/PR style:** `type(scope): short description`, `[FUP-N]` para follow-ups, PRs com checklist de crossroad files (`AGENTS.md:59`-`67`; `README.md:174`). Exemplo observado: `analysis(kavak-playbook): pipeline completo — 13 canonical docs + ...` (commit `2e38fea`).
- **Pipeline analyze-and-improve (7 fases):** Phase 0 mental model → Phase 1 extração (map-reduce) → Phase 2 patterns → Phase 3 classification → Phase 4 canonical/skills/exercises → Phase 5 SOR/índices → Phase 6 enriquecimento de currículo; cache de Phases 1+2; pacote com analysis/patterns/classification/mental-model/artifacts (commit `2e38fea`; formato atual em `docs/system-of-record.md:417`-`422`).
- **ADR formalizado:** Skill-Canons Bridge Ondas 0-2 — 5 decisões cross-cutting documentadas com opções, trade-offs e condições de revisita (`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:35`-`43`, `:78`-`82`).

---

## 4. Abstractions — terminologia chave

| Termo | Definição | Fonte |
|---|---|---|
| **Agent (Agente)** | Entidade autônoma de IA (geralmente LLM) que toma ações, usa ferramentas e executa tarefas em sequência | `curriculum/GLOSSARY.md:17`-`24` |
| **Agent Loop** | Ciclo repetitivo input → pensa → ação → resultado → repete | `curriculum/GLOSSARY.md:41`-`47` |
| **Harness / Harness Engineering** | Infraestrutura de suporte que envolve o modelo e garante confiabilidade em execuções longas; engenharia de software aplicada ao runtime do agente | `README.md:18` |
| **KODA** | Agente de venda de suplementos via WhatsApp; caso âncora do repositório, conversas de 2+ horas | `curriculum/README.md:34`; `README.md:20` |
| **HoP (House of Pace) / Handoff Protocol** | Modelo do sistema de agentes: cada agente tem escopo fechado, dono e gates de validação; handoff carrega estado confirmado (ex.: telefone) | `docs/system-of-record.md:27`; `.opencode/agents/hop-orchestrator-rezek.md:21` |
| **Amnesia (Context Amnesia)** | Agente "esquece" contexto anterior por exceder a janela; solução: state persistence + memory management | `curriculum/GLOSSARY.md:50`-`58` |
| **Compaction** | Resumir/comprimir contexto antigo para abrir espaço mantendo informações-chave (server-side quando feito pelo servidor/modelo) | `curriculum/GLOSSARY.md:81`-`87` |
| **Context Anxiety / Context Rot** | Comportamento ansioso/pressa perto do limite de janela; degradação gradual de coerência conforme a janela avança | `curriculum/GLOSSARY.md:138`-`150` |
| **Generator/Evaluator** | Dois agentes: Generator (criativo, janela de conversa) e Evaluator (imparcial, constraints/rubrics/estado persistido) com veredicto approve/reject | `docs/system-of-record.md:216`; `README.md:82` |
| **Compartmented Evaluation Architecture** | Builder e Validator recebem superfícies de informação seladas para impedir reward-hacking (otimizar para checks visíveis em vez de outcomes) | `curriculum/GLOSSARY.md:90`-`102` |
| **Constraint Budget Gate** | Limite de 5-7 constraints direcionais, incondicionais e em linguagem de negócio por tarefa; excedentes viram contexto ou failure conditions | `curriculum/GLOSSARY.md:106`-`118` |
| **Constraint-Failure Decision Rule** | Pergunta-âncora "saber isso mudaria como o Builder escreve código?" — classifica cada item como constraint (guia geração) ou failure condition (guia validação) | `curriculum/GLOSSARY.md:122`-`134` |
| **Agent Degradation Loop Prevention** | Framework diagnóstico dos 4 elos do loop de degradação: atenção desigual, erros que se compõem, fragmentação de estado externo, feedback inerte de memória | `curriculum/GLOSSARY.md:28`-`37` |
| **Closed-Loop Company** | Agentes leem estado real da empresa (código, issues, artefatos) e devolvem trabalho/decisões fechando o ciclo observação → execução | `curriculum/GLOSSARY.md:74`-`78` |
| **Evals-as-Brakes** | Velocidade de shipping permitida como função da qualidade/cobertura de evals; resposta ao risco de IA é construir evals, não ir mais devagar (Kavak) | `docs/system-of-record.md:303`; `docs/canonical/evals-as-brakes.md:17` |
| **Mega-Expert Consolidation** | Um agente por especialidade benchmarkado contra o melhor humano individual, fundidos em um único agente voltado ao cliente, sem handoffs nem deflection bot (Kavak) | `docs/system-of-record.md:305` |
| **ADR (Architecture Decision Record)** | Documento que registra decisão de arquitetura, contexto e consequências; topo da precedência documental | `curriculum/GLOSSARY.md:61`-`68`; `docs/system-of-record.md:16` |
| **System of Record** | Fonte da verdade: precedência, domínios do projeto, padrões ativos e status de ADRs | `README.md:127`; `docs/system-of-record.md:12` |
| **analyze-and-improve** | Pipeline/harness que converte fontes externas em padrões extraídos, classificados e integrados ao repositório | `README.md:136`; `docs/system-of-record.md:46` |
| **12-Factor Agents** | Talk de origem (Dex Horthy, AI Engineer 2025) de vários padrões canônicos (error-context-hygiene = Padrão 6, deterministic-tool-dispatch = Padrão 2, etc.) | `README.md:67`; `docs/system-of-record.md:174`-`177` |
| **Skill-Canons Bridge** | Framework de 3 níveis de bridging que conecta skills do ecossistema aos padrões canônicos do vault | `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:27`-`31` |

**Domínios do projeto (taxonomia de tags):** Agentes e orquestração; Currículo e conteúdo; Portal web; Stack e tooling; Governança de repositório; Testes e QA (`docs/system-of-record.md:23`-`151`; tags derivadas em `AGENTS.md:171`-`200`).

---

## 5. Curriculum Structure

- **Programa:** 12 semanas, 4 níveis, 8 conceitos core, 35+ diagramas Mermaid; 30-50 horas por pessoa (`curriculum/README.md:13`, `:296`-`298`).
- **Master docs:** MASTER_PLAN (índice geral), QUICK_START (45 min), GLOSSARY (~69 termos), EXECUTION_PLAN (cronograma de 12 semanas), INDEX, FAQ (`docs/system-of-record.md:76`-`81`; contagem de termos por `grep '^### ' curriculum/GLOSSARY.md` = 69, 2026-08-30).

**Níveis (progressão):**

| Nível | Diretório | Pergunta / Foco | Carga |
|---|---|---|---|
| 1 — Fundamentos | `curriculum/01-nivel-1-fundamentals/` | Por que agentes falham? Context windows, token budgeting, harness básico (3 lições + exercises + koda-applications) | 3-4h (`curriculum/README.md:204`-`212`) |
| 2 — Padrões Práticos | `curriculum/02-nivel-2-practical-patterns/` | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading (4 lições) | 6-8h (`:218`-`229`) |
| 3 — Arquitetura Avançada | `curriculum/03-nivel-3-advanced-architecture/` + dirs auxiliares `03-nivel-3-operacional/`, `03-nivel-arquiteto/`, `04-nivel-3-engenharia-avancada/` | Multi-agent, state persistence, file-based coordination, server-side compaction, harness evolution (5 lições) | 8-10h (`:233`-`244`) |
| 4 — Aplicação KODA | `curriculum/04-nivel-4-koda-specific/` | Arquitetura KODA, customer journeys, feature patterns, rubrics, harness improvements, real-world-exercises, case studies | Contínuo (`:248`-`259`) |

**8 conceitos core** (`curriculum/05-core-concepts/`), cada um com explicação profunda, 3 knowledge graphs, aplicação KODA e checklist (`curriculum/README.md:263`-`282`): Context Management; Planning vs. Execution; Generator/Evaluator; Sprint Contracts; State Persistence; Harness Evolution; Multi-Agent Coordination; Evaluation Rubrics.

**Diretórios complementares:** `06-knowledge-graphs/` (35+ diagramas), `07-implementation-guides/`, `08-tools-templates/` (sprint contract, rubrica, ADR, progress tracker), `09-case-studies/` (5 casos: retro-game-maker, browser-daw, 3× KODA), `10-references/` (`docs/system-of-record.md:89`-`93`).

**Exercícios:** por nível, com solutions. N2 inclui error-context-hygiene, two-implementations-goal-test, goal-atomicity-split; N3 inclui constraint gates, autonomy-curriculum-sampling, magnitude-direction-verifier-split, llm-as-fuzzy-compiler, persona-based-documentation, **exercise-07-mega-expert-consolidation** e **exercise-08-sidekick-pattern** (adicionados pelo pacote kavak, commits `2e38fea`/`dfb67d8`); core-concepts inclui tiered-context-storage, neutral-selection-layer, selection-budgeted-retrieval; N4 inclui manual-brake-question-gate, deferred-ledger-agentic-work (`curriculum/README.md:84`-`143`; `git show --stat 2e38fea dfb67d8`).

**Cronograma:** Semanas 1-2 fundação (N1) → 3-4 padrões (N2) → 5-6 arquitetura (N3 subconjunto) → 7-12 aplicação (N4) (`curriculum/README.md:286`-`296`).

**Métricas de sucesso:** marcos por 2/4/6/12 semanas (100% entende os 3 problemas; rubrics para 2+ features; 60-80% em N3; 50%+ em N4 mentoreando novos membros) (`curriculum/README.md:455`-`476`).

**Material-fonte:** `rawfiles/` (material usado para gerar o currículo) e `prompts/` (prompts de geração) (`docs/system-of-record.md:94`-`95`). Curso adicional top-level `curso-reimplementar-runtime/` (PR #144, commit `f2c5017`) fora da numeração 01-10.

---

## 6. Existing Gaps

### 6.1 Pendências documentadas

| # | Gap | Onde documentado |
|---|---|---|
| 1 | `docs/canonical/agent-lifecycle.md` (ciclo claim → worktree → implement → review → merge → cleanup) pendente | `docs/system-of-record.md:68` |
| 2 | `docs/canonical/curriculum-model.md` (taxonomia de níveis, tipos de artefato, critérios de qualidade) pendente | `docs/system-of-record.md:97` |
| 3 | `docs/canonical/portal-architecture.md` pendente, a criar quando a SPA proposta for implementada | `docs/system-of-record.md:110` |
| 4 | `docs/canonical/crossroad-change-policy.md` e arquivos `src/lib/*` (safe-console, logger) referenciados pelo PR template mas inexistentes | `docs/system-of-record.md:142` |
| 5 | Tabela de canonical docs pendentes: agent-lifecycle, curriculum-model, portal-architecture, crossroad-change-policy; obsidian-document-conventions só se a convenção crescer além da Rule 16 | `docs/system-of-record.md:315`-`321` |
| 6 | ADRs candidatos não formalizados: stack do portal, content chunking, persistência de estado entre agentes, versionamento do currículo | `docs/system-of-record.md:161`-`165` |
| 7 | Ações pendentes do ADR Skill-Canons Bridge: atualizar system-design para budget gate 4 fases; extrair shared module quando >5 skills com bridge; capturar runs manuais de baseline | `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:91`-`93` |
| 8 | FAQ do currículo "em construção" | `curriculum/README.md:69`, `:489` |
| 9 | Os 8 conceitos core com status ⏳ (pendente) na tabela de status | `curriculum/README.md:271`-`280` |

### 6.2 Drifts observados (listagem 2026-08-30)

| # | Drift | Evidência |
|---|---|---|
| 10 | Contagem de canonical docs divergente: SOR declara "~116 padrões" e README "85+"; o diretório tem **142 arquivos** (impacto do pacote kavak +13 e de promoções de runtime) | `docs/system-of-record.md:169` vs `README.md:67` vs `ls docs/canonical/ \| wc -l` = 142 |
| 11 | Contagem de skills divergente: README declara "28 skills"; o diretório `.opencode/skills/` tem **33 entradas** (incluindo mega-expert-consolidation e sidekick-pattern-physical-boundaries do pacote kavak) | `README.md:104` vs directory listing 2026-08-30 |
| 12 | Skill `devils-advocate` referenciada no SOR (linha da tabela de skills, "Wave 1 anti-sycophancy") mas **não existe** em `.opencode/skills/` | `docs/system-of-record.md:63` vs directory listing (grep retornou vazio) |
| 13 | Nomenclatura de níveis inconsistente: coexistem `03-nivel-3-advanced-architecture`, `03-nivel-3-operacional`, `03-nivel-arquiteto`, `04-nivel-3-engenharia-avancada`, `04-nivel-4-koda-specific` | `docs/system-of-record.md:82`-`88`; curriculum directory listing 2026-08-30 |
| 14 | Curso top-level `curso-reimplementar-runtime/` (merged via PR #144) não mapeado nas tabelas de domínio do SOR | top-level listing 2026-08-30 vs `docs/system-of-record.md:23`-`151` |
| 15 | Canonical docs `operator-channel-authority.md` e `structural-guarantee-over-compliance.md` presentes no diretório mas ausentes da tabela de padrões ativos do SOR | directory listing vs `docs/system-of-record.md:172`-`313` |

---

## Notas para fases downstream

- A precedência documental (ADRs > canonical > evidence > analysis > READMEs) define onde o conteúdo derivado da fonte externa deve pousar: análise vive em `docs/analysis/<date>-<slug>/`, padrões aceitos sobem para `docs/canonical/`, integração segue o contrato da skill `analyze-and-improve` (`docs/system-of-record.md:417`-`422`).
- Formato atual de pacotes (pós-2026-06-14): `<date>-<source-slug>-artifacts.{md,yaml}` como manifest de artefatos; o pacote kavak é o precedente mais recente, incluindo classification em 2 batches (`docs/system-of-record.md:408`-`422`).
- Todo novo doc em `docs/analysis/` precisa de frontmatter completo (title, type: analysis, tags de domínio, date, aliases, relates-to) e wikilinks — hard error no CI via `npx tsx scripts/validate-obsidian.ts` (`AGENTS.md:143`-`157`, `:242`-`257`).
- O mental model da fonte anterior (kavak) foi salvo em `mapa-mental-repo/` (passo 0c do qi-loop, commit `dfb67d8`) — este documento cumpre o mesmo papel para a nova fonte.
