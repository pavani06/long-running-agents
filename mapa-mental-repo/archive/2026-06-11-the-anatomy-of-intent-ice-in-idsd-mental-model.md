---
title: "Mental Model: The Anatomy of Intent - ICE in IDSD"
type: analysis
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "context-engineering", "evals", "governanca", "spec-driven-development", "decision-discipline"]
date: 2026-06-11
aliases: ["anatomy intent ice mental model", "repo mental model intent ice", "intent ice idsd mental model", "modelo mental intent ice"]
last_updated: 2026-06-14
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|AGENTS.md]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[curriculum/INDEX|Curriculum Index]]", "[[curriculum/GLOSSARY|Glossary]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[.opencode/skills/analyze-and-improve/SKILL.md|Analyze and Improve Skill]]"]
sources: ["[[AGENTS|AGENTS.md]]", "[[README|README.md]]", "[[docs/system-of-record|System of Record]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[curriculum/INDEX|Curriculum Index]]", "[[curriculum/GLOSSARY|Glossary]]"]
---
# Mental Model: long-running-agents

**Date:** 2026-06-11  
**Repo:** `long-running-agents`  
**Type:** `mental-model`  
**Scope:** leitura somente do repositório alvo antes de analisar a fonte externa `the-anatomy-of-intent-ice-in-idsd`.

## 1. Project Goals

`long-running-agents` é simultaneamente uma base de conhecimento, um currículo e uma camada operacional para construir agentes que trabalham por horas ou dias sem perder contexto, planejamento ou julgamento de qualidade. A tese central do repo é que agentes long-running falham por perda de contexto, planejamento frágil e autoavaliação cega; a resposta é ensinar e operacionalizar harnesses que gerenciam contexto, decompõem trabalho e separam geração de avaliação ([[README|README.md]]:3-13).

- Construir e gerir workflows de agentes long-running usando `.opencode/` como sistema de agentes, Node >= 20.18.0/ESM como stack, `.runtime/` e `artifacts/` como runtime state, e `docs/decisions/` como local de decisões aceitas ([[AGENTS|AGENTS.md]]:7-12; [[README|README.md]]:107-113).
- Ensinar builders de negócio e operadores de sistemas agentic, de iniciantes a pessoas que já operam agentes em produção e querem elevar confiabilidade ([[README|README.md]]:15-17).
- Manter um currículo completo de 12 semanas, 4 níveis, 8 conceitos core e 35+ diagramas para formar especialistas em long-running agents aplicados ao KODA ([[curriculum/README|curriculum/README.md]]:11-13; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:18-27).
- Aplicar padrões ao KODA, agente de venda de suplementos via WhatsApp que precisa manter qualidade em conversas de 2+ horas ([[curriculum/README|curriculum/README.md]]:33-34; [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:352-363).
- Governar documentação por precedência explícita: ADRs aceitos, canonical docs ativos, evidências, análises, arquivos históricos, depois READMEs e resumos operacionais ([[docs/system-of-record|docs/system-of-record.md]]:14-21; [[AGENTS|AGENTS.md]]:64-75).
- Transformar conhecimento externo em melhorias concretas por meio do pipeline `analyze-and-improve`: mental model do repo, extração, padrões, classificação, geração de melhorias, integração e integração curricular ([[.opencode/skills/analyze-and-improve/SKILL.md|.opencode/skills/analyze-and-improve/SKILL.md]]:47-57; [[.opencode/skills/analyze-and-improve/SKILL.md|.opencode/skills/analyze-and-improve/SKILL.md]]:171-249).
- Preservar um sistema de trabalho agentic com claim de issue, worktree isolado, execution brief, validação, draft PR, second-agent review, aprovação explícita e cleanup ([[.opencode/skills/issue-start/SKILL.md|issue-start]]:12-15; [[.opencode/skills/issue-review/SKILL.md|issue-review]]:12-15; [[.opencode/skills/issue-finish/SKILL.md|issue-finish]]:12-15).

## 2. Architecture

### Core Abstractions

| Abstraction | Role in the repo | Evidence |
|---|---|---|
| System of Record | Fonte de verdade para precedência, domínios, inventário de fontes e lacunas pendentes. | [[docs/system-of-record|docs/system-of-record.md]]:12-23 |
| Documentation Precedence | Regra de conflito: ADR aceito > canonical ativo > evidência > análise > arquivo > README/resumo operacional. | [[docs/system-of-record|docs/system-of-record.md]]:14-21; [[AGENTS|AGENTS.md]]:64-75 |
| Operational Contract | `AGENTS.md` define uma tarefa por sessão, mudança mínima, tocar só o necessário, gates reais, segurança e convenções Obsidian. | [[AGENTS|AGENTS.md]]:14-32; [[AGENTS|AGENTS.md]]:53-85; [[AGENTS|AGENTS.md]]:120-238 |
| Canonical Pattern Catalog | Camada autoritativa de padrões agentic, contexto, evals, governança, intenção/ICE e review. | [[docs/system-of-record|docs/system-of-record.md]]:135-211 |
| Curriculum | Produto principal: programa de 12 semanas, 4 níveis, 8 conceitos core, exercícios, soluções, KODA, knowledge graphs, guias, templates e case studies. | [[docs/system-of-record|docs/system-of-record.md]]:57-82; [[curriculum/README|curriculum/README.md]]:11-13; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:178-267 |
| Agent System / HoP | `.opencode/` contém agentes e skills para orquestração, issue lifecycle, revisão, documentação e gates de governança. | [[docs/system-of-record|docs/system-of-record.md]]:25-55; [[README|README.md]]:62-66 |
| Issue Lifecycle | Fluxo claim -> worktree -> brief -> implement -> validate -> draft PR -> review -> explicit merge -> cleanup. | [[.opencode/skills/issue-start/SKILL.md|issue-start]]:78-149; [[.opencode/skills/issue-review/SKILL.md|issue-review]]:44-226; [[.opencode/skills/issue-finish/SKILL.md|issue-finish]]:50-170 |
| Application-Owned Control Plane | Contrato que une prompt versionado, context builder, action schema, dispatch determinístico, loop policy, estado persistente e gates de intervenção. | [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:27-75 |
| Context and Memory Stack | Stack de prompt estável, durable state, head/tail anchors, summaries, omitted-memory catalog, token ledger e handoff consciente de budget. | [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:28-42; [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:71-82 |
| Evaluation and Review Stack | Generator/Evaluator, eval tiers fast/medium/deep, PR gates, production regressions, shadow review e severidade contextual. | [[docs/canonical/generator-evaluator|Generator-Evaluator]]:29-85; [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:20-50; [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]:13-28 |
| Intent and ICE Layer | Intenção, contexto e expectativas são crafts separados com donos explícitos; intent pode virar primitivo de cinco partes antes da execução. | [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:29-77; [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:29-52 |
| KODA Case Domain | Domínio aplicado que prova os conceitos: vendas WhatsApp, descoberta de produtos, pedidos, fulfillment, jornadas, rubricas e melhorias de harness. | [[curriculum/README|curriculum/README.md]]:33-34; [[curriculum/README|curriculum/README.md]]:232-243; [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:352-363 |
| Stack and Validation Tooling | Projeto Node ESM com comandos reais `lint`, `test:unit` e `test:integration`; validação de docs usa convenções Obsidian. | [[package.json|package.json]]:1-13; [[AGENTS|AGENTS.md]]:53-62; [[scripts/check-obsidian-conventions.sh|scripts/check-obsidian-conventions.sh]]:18-66 |

### Relationships

| From | To | Relationship | Evidence |
|---|---|---|---|
| `docs/system-of-record.md` | Todas as superfícies documentais | Decide autoridade antes de README, analysis ou skill operacional resolver divergência. | [[docs/system-of-record|docs/system-of-record.md]]:14-21 |
| `AGENTS.md` | Todo trabalho agentic | Define disciplina de escopo, mudança mínima, segurança, validação e convenções de documentação. | [[AGENTS|AGENTS.md]]:14-32; [[AGENTS|AGENTS.md]]:53-85; [[AGENTS|AGENTS.md]]:120-238 |
| Canonical docs | Curriculum | Canonicals nomeiam padrões; o currículo transforma esses padrões em progressão, exercícios, KODA applications, graphs e templates. | [[docs/system-of-record|docs/system-of-record.md]]:135-211; [[curriculum/INDEX|curriculum/INDEX.md]]:82-180 |
| Curriculum | KODA | Níveis 1-3 ensinam conceitos genéricos; Nível 4 aplica ao KODA em arquitetura, journeys, feature patterns, rubrics e exercises. | [[curriculum/README|curriculum/README.md]]:186-243; [[curriculum/INDEX|curriculum/INDEX.md]]:56-65 |
| `.opencode` skills | Repository execution | Skills operacionalizam setup, review, merge, cleanup, análise, documentação e gates de valor/risco. | [[.opencode/skills/issue-start/SKILL.md|issue-start]]:12-15; [[.opencode/skills/orchestrator/SKILL.md|orchestrator]]:12-17; [[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve]]:47-57 |
| Application-Owned Control Plane | Owned Agent Control Loop | O control plane amplia os quatro componentes do owned loop e adiciona estado persistente, action schema e gates. | [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:29-75; [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:29-75 |
| Context Stack | Long-session reliability | Stable prompt, durable facts, head/tail anchors, summaries e memory catalog preservam continuidade sob pressão de tokens. | [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:34-42; [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:121-136 |
| Evaluation Stack | Merge and production quality | Generator/Evaluator separa criação de julgamento; eval tiers e PR gates definem profundidade proporcional a risco, custo e trigger. | [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-85; [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-72 |
| Intent/ICE Layer | Harness execution | O humano mantém Intent e Expectations; o harness possui Context e Loop; lacunas viram perguntas em vez de decisões inferidas pelo agente. | [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:31-63; [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:43-52 |
| Recent analyses | Canonical and skills | `analyze-and-improve` converte análises em canonical docs, skills e exercícios, mantendo rastreabilidade para classificação e integração. | [[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve]]:130-148; [[docs/system-of-record|docs/system-of-record.md]]:222-299 |

## 3. Patterns

| Pattern | Where Defined | Maturity |
|---|---|---|
| Application-Owned Agent Control Plane | [[docs/canonical/application-owned-agent-control-plane|docs/canonical/application-owned-agent-control-plane.md]]:11-16 | Active canonical; Partial Coverage. Unifica prompt, context builder, action schema, dispatch, loop policy, state e intervention gates. |
| Owned Agent Control Loop | [[docs/canonical/owned-agent-control-loop|docs/canonical/owned-agent-control-loop.md]]:10-16 | Active canonical; Partial Coverage. A decomposição em Prompt, Context Builder, Switch Statement e Loop é a moldura do harness owned. |
| Deterministic Tool Dispatch | [[docs/canonical/deterministic-tool-dispatch|docs/canonical/deterministic-tool-dispatch.md]]:10-16 | Active canonical; Partial Coverage. Reenquadra ferramentas como JSON + código determinístico, testável sem LLM. |
| Structured Generation and Constraint Validation Circuit | [[docs/canonical/structured-generation-constraint-validation-circuit|docs/canonical/structured-generation-constraint-validation-circuit.md]]:11-16 | Active canonical; Partial Coverage. Formaliza geração estruturada, validação de constraints, repair/rejection e audit. |
| Versioned Durable Agent State | [[docs/canonical/versioned-durable-agent-state|docs/canonical/versioned-durable-agent-state.md]]:11-16 | Active canonical; Partial Coverage. Estado durável versionado, migração, writeback, reload e audit trail. |
| External State Persistence | [[docs/canonical/external-state-persistence|docs/canonical/external-state-persistence.md]]:11-16 | Active canonical; Partial Coverage. Persistir fatos críticos fora da janela e recarregá-los por turno. |
| Hybrid Context Stack | [[docs/canonical/hybrid-context-stack|docs/canonical/hybrid-context-stack.md]]:10-16 | Active canonical; Partial Coverage. Policy de context builder por camadas com ordem, budget e decision trace. |
| Head-Tail Context Truncation | [[docs/canonical/head-tail-context-truncation|docs/canonical/head-tail-context-truncation.md]]:10-15 | Active canonical; Partial Coverage. Preserva head/tail e move middle para memória recuperável. |
| Addressable Memory Catalog | [[docs/canonical/addressable-memory-catalog|docs/canonical/addressable-memory-catalog.md]]:10-15 | Active canonical; Partial Coverage. Catálogo de memória omitida com `id`, `kind`, `location`, `preview`, `scope` e `fetch`. |
| Explicit Token Budget Ledger | [[docs/canonical/explicit-token-budget-ledger|docs/canonical/explicit-token-budget-ledger.md]]:10-15 | Active canonical; Partial Coverage. Ledger por chamada com custo fixo, custo reduzível, reserva, safety buffer e saldo. |
| Budget-Aware Session Handoff | [[docs/canonical/budget-aware-session-handoff|docs/canonical/budget-aware-session-handoff.md]]:11-16 | Active canonical; Partial Coverage. Handoff de sessão guiado por budget e continuidade. |
| Eval Tier Stratification | [[docs/canonical/eval-tier-stratification|docs/canonical/eval-tier-stratification.md]]:10-16 | Active canonical; Partial Coverage. Tiers fast/medium/deep com runtime, custo, flakiness, trigger, threshold e owner. |
| Generator-Evaluator | [[docs/canonical/generator-evaluator|docs/canonical/generator-evaluator.md]]:11-17 | Active canonical; Partial Coverage. Separa Generator criativo de Evaluator cético e orientado por constraints. |
| Constraint-Anchored Evaluation | [[docs/canonical/constraint-anchored-evaluation|docs/canonical/constraint-anchored-evaluation.md]]:11-16 | Active canonical; Partial Coverage. Avaliação objetiva ancorada em constraints explícitas e persistidas. |
| PR-Gated Eval Enforcement | [[docs/canonical/pr-gated-eval-enforcement|docs/canonical/pr-gated-eval-enforcement.md]]:10-15 | Active canonical; Partial Coverage. Evidência de eval entra como gate de PR para mudanças sensíveis. |
| Production Failure Regression Flywheel | [[docs/canonical/production-failure-regression-flywheel|docs/canonical/production-failure-regression-flywheel.md]]:10-15 | Active canonical; Partial Coverage. Falhas de produção viram casos de regressão, triagem e suite evolution. |
| Shadow Review Pipeline | [[docs/canonical/shadow-review-pipeline|docs/canonical/shadow-review-pipeline.md]]:11-17 | Active canonical; Missing na classificação original. Define AI review não-bloqueante, métricas de concordância e graduação para gate. |
| Review Contract Checklist | [[docs/canonical/review-contract-checklist|docs/canonical/review-contract-checklist.md]]:11-16 | Active canonical; Partial Coverage. Checklist estruturado de review para achados comparáveis. |
| Contextual Severity Calibration | [[docs/canonical/contextual-severity-calibration|docs/canonical/contextual-severity-calibration.md]]:11-16 | Active canonical; Missing na classificação original. Calibra profundidade e severidade por perfil de risco do módulo. |
| Manual Brake Question Gate | [[docs/canonical/manual-brake-question-gate|docs/canonical/manual-brake-question-gate.md]]:11-16 | Active canonical; Missing, High integration value. Três perguntas de valor antes de autorizar build agentic. |
| Owner-of-No Role Design | [[docs/canonical/owner-of-no-role-design|docs/canonical/owner-of-no-role-design.md]]:11-16 | Active canonical; Missing, Medium integration value. Papel explícito para recusar trabalho de baixo valor e oferecer intents alternativos. |
| Deferred Ledger for Agentic Work | [[docs/canonical/deferred-ledger-agentic-work|docs/canonical/deferred-ledger-agentic-work.md]]:11-16 | Active canonical; Missing, High integration value. Classifica skill debt, dependence debt e carry debt. |
| LLM as Fuzzy Compiler | [[docs/canonical/llm-as-fuzzy-compiler|docs/canonical/llm-as-fuzzy-compiler.md]]:11-16 | Active canonical; Missing. Trata LLM como compiler backend, harness como optimization passes e código como build artifact. |
| Persona-Based Documentation | [[docs/canonical/persona-based-documentation|docs/canonical/persona-based-documentation.md]]:11-16 | Active canonical; Missing. NFRs por persona e reviewers por dimensão de qualidade. |
| Intent as Five-Part Primitive | [[docs/canonical/intent-five-part-primitive|docs/canonical/intent-five-part-primitive.md]]:11-17 | Active canonical; Missing, Medium integration value. Intent vira cinco campos obrigatórios antes da execução. |
| ICE Craft Separation | [[docs/canonical/ice-craft-separation|docs/canonical/ice-craft-separation.md]]:11-17 | Active canonical; Partial Coverage, High integration value. Separa Intent, Context e Expectations com donos explícitos. |
| Human-Owned Expectations Boundary | [[docs/canonical/human-owned-expectations-boundary|docs/canonical/human-owned-expectations-boundary.md]]:11-16 | Active canonical; Partial Coverage, High integration value. Done/failure pertence ao outcome owner. |
| Presence-in-the-Loop Metric | [[docs/canonical/presence-in-the-loop-metric|docs/canonical/presence-in-the-loop-metric.md]]:11-16 | Active canonical; Missing, Medium integration value. Mede presença humana durante execução, não só aprovação final. |
| Token Economics of Gap-Filling | [[docs/canonical/token-economics-gap-filling|docs/canonical/token-economics-gap-filling.md]]:11-16 | Active canonical; Partial Coverage, High integration value. Atribui custo de tokens a gaps de Intent, Context e Expectations. |
| Symphony Trap Awareness | [[docs/canonical/symphony-trap-awareness|docs/canonical/symphony-trap-awareness.md]]:11-16 | Active canonical; Partial Coverage, Medium integration value. Alerta contra over-specification e perda de adaptabilidade. |
| Skill-Resolver-Skillify Capability Pipeline | [[docs/canonical/skill-resolver-skillify-capability-pipeline|docs/canonical/skill-resolver-skillify-capability-pipeline.md]]:10-15 | Active canonical; Partial Coverage, High integration value. Transforma workflow em skill roteável, testada e resolvível. |
| Resolver-Based Context Progressive Disclosure | [[docs/canonical/resolver-based-context-progressive-disclosure|docs/canonical/resolver-based-context-progressive-disclosure.md]]:10-15 | Active canonical; Partial Coverage, High integration value. Capacidade e contexto são carregados por resolver, não em prompt monolítico. |
| HoP Issue Lifecycle Skills | [[.opencode/skills/issue-start/SKILL.md|issue-start]]:12-15; [[.opencode/skills/issue-review/SKILL.md|issue-review]]:12-15; [[.opencode/skills/issue-finish/SKILL.md|issue-finish]]:12-15 | Active operational skills; canonical `agent-lifecycle.md` ainda pendente no SOR. |
| Analyze-and-Improve Pipeline | [[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve]]:47-57 | Active analysis skill. Repo mental model é Phase 0 antes de qualquer fonte externa. |
| Error Context Hygiene Skill | [[.opencode/skills/error-context-hygiene/SKILL.md|error-context-hygiene]]:13-30 | Active implementation skill. Resume erros, limpa após sucesso, não faz blind append e controla tamanho de contexto. |
| Manual Brake Skill | [[.opencode/skills/manual-brake-question-gate/SKILL.md|manual-brake-question-gate]]:13-21 | Active decision skill. Produz decisão experimento/build/adiar/parar. |
| Shadow Review Skill | [[.opencode/skills/shadow-review-pipeline/SKILL.md|shadow-review-pipeline]]:13-28 | Active governance skill. Coleta métricas TP/FP/missed-by-human/missed-by-AI antes de tornar AI review bloqueante. |

## 4. Abstractions

| Term | Definition | Source |
|---|---|---|
| Agent | Entidade autônoma de IA, geralmente LLM-based, que toma ações, usa ferramentas e executa tarefas em sequência. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:17-24 |
| Agent Loop | Ciclo repetitivo input -> pensa -> ação -> resultado -> repete. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:28-35 |
| Context Window | Número total de tokens que um modelo processa por vez; memória imediata do agente. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:97-107 |
| Context Amnesia | Esquecimento de contexto anterior quando a janela útil é excedida. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:37-45 |
| Context Rot | Perda gradual de coerência ao longo da janela de contexto. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:88-94 |
| Context Anxiety | Comportamento apressado perto do limite de contexto. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:77-85 |
| Context Progressive Disclosure | Instruções e capacidades ficam em skills carregadas por trigger, não em prompt monolítico. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:110-113 |
| Harness | Infraestrutura e padrões que envolvem agentes para torná-los confiáveis por períodos longos. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:265-278 |
| Harness Evolution | Simplificar ou remover componentes de harness conforme modelos melhoram. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:282-295 |
| Generator | Agente responsável por construir ou criar output. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:215-225 |
| Evaluator | Agente separado que avalia criticamente o trabalho de um Generator contra rubricas. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:131-143 |
| Generator/Evaluator Pattern | Duas entidades separadas colaboram: uma gera, outra avalia. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:228-248; [[docs/canonical/generator-evaluator|Generator-Evaluator]]:29-85 |
| Sprint Contract | Acordo prévio sobre o que pronto significa antes da execução. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:117-126 |
| Evaluation Rubric | Critérios mensuráveis para avaliar qualidade subjetiva. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:147-163 |
| Trace | Log detalhado de inputs, reasoning, ações e outputs do agente; ferramenta principal de debugging de behavior. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:653-668 |
| Memory / State | Informação retida entre operações, incluindo short-term, long-term e file-based. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:380-390 |
| Multi-Agent System | Sistema com múltiplos agentes independentes coordenados, com Planner, Generator e Evaluator como padrão comum. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:407-419 |
| Planner | Agente especializado em quebrar problema em etapas. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:425-439 |
| KODA | Agente conversacional de venda de suplementos via WhatsApp e case study do programa. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:352-363 |
| ICE Craft Separation | Decomposição do trabalho agentic em Intent, Context e Expectations com donos explícitos. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:314-327; [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:31-58 |
| Intent as Five-Part Primitive | Intent estruturado em description, constraints, failure scenarios, success scenarios e connections. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:331-346; [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-48 |
| Human-Owned Expectations Boundary | Done/failure é artefato separado, escrito pelo outcome owner e consumido pelo harness. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:298-309 |
| Token Budget | Gestão consciente de tokens disponíveis, consumidos e reservados. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:622-632; [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:13-15 |
| Token Economics of Gap-Filling | Modelo que atribui custo de tokens a gaps nos campos de Intent, Context e Expectations. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:636-649 |
| Fuzzy Compiler | Modelo mental onde LLM é compiler backend, harness é optimization pass e código gerado é artefato. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:182-197; [[.opencode/skills/llm-as-fuzzy-compiler/SKILL.md|llm-as-fuzzy-compiler]]:13-21 |
| Persona-Based Documentation | NFRs por persona especialista, carregados por agentes/reviewers conforme a tarefa. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:452-466; [[.opencode/skills/persona-based-documentation/SKILL.md|persona-based-documentation]]:13-21 |
| Presence-in-the-Loop Metric | Métrica de governança para medir envolvimento humano durante execução agentic. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:470-484 |
| Verification Loop | Ciclo Generator -> Test/Evaluator -> Feedback. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:674-687 |
| ADR | Registro de decisão arquitetural significativa, contexto e consequências. | [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]]:48-55 |
| System of Record | Índice de autoridade e mapa de domínios do repo. | [[docs/system-of-record|docs/system-of-record.md]]:12-23 |

## 5. Curriculum Structure

O currículo é organizado por perfil, tipo de conteúdo, pergunta, tempo disponível, nível e conceito. `curriculum/INDEX.md` funciona como navegação executiva; `curriculum/MASTER_PLAN.md` detalha objetivos, estrutura, roadmap de 12 semanas, critérios de conclusão, conceitos, guides, templates e case studies ([[curriculum/INDEX|curriculum/INDEX.md]]:15-82; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:18-31).

### Levels

| Level | Focus | Progression and outputs | Evidence |
|---|---|---|---|
| Nível 1 - Fundamentos | Por que agentes falham: contexto, token budget e harness básico. | 3-4h no overview; 2 exercícios; KODA application; critérios de entender os 3 motivos de falha, context windows e token budgeting. | [[curriculum/README|curriculum/README.md]]:188-198; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:180-197 |
| Nível 2 - Padrões Práticos | Generator/Evaluator, Sprint Contracts, Rubric Design e Trace Reading. | 6-8h; 5 exercícios incluindo Error Context Hygiene e Intent Five-Part Primitive; output inclui generator/evaluator e rubrics KODA. | [[curriculum/README|curriculum/README.md]]:202-213; [[curriculum/INDEX|curriculum/INDEX.md]]:105-111; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:201-220 |
| Nível 3 - Arquitetura Avançada | Multi-agent systems, state persistence, file-based coordination, server-side compaction e harness evolution. | 8-10h; 9 exercícios incluindo fuzzy compiler, persona docs, presence metric, owner-of-no, shadow review e severity calibration. | [[curriculum/README|curriculum/README.md]]:217-228; [[curriculum/INDEX|curriculum/INDEX.md]]:112-122; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:224-243 |
| Nível 4 - KODA-specific | Arquitetura KODA, customer journeys, feature patterns, KODA rubrics, harness improvements e real-world exercises. | Contínuo; semanas 7-12; foco em diagnóstico de traces, melhorias com dados, feature implementation e decisões arquiteturais. | [[curriculum/README|curriculum/README.md]]:232-243; [[curriculum/INDEX|curriculum/INDEX.md]]:123-128; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:247-267 |

### Concepts

| Concept | Role in progression | Evidence |
|---|---|---|
| Context Management | Conceito base para long-session reliability. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:345-362 |
| Planning vs. Execution | Separa decomposição e execução para evitar agente tentando tudo de uma vez. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:345-362 |
| Generator/Evaluator | Separa criação e julgamento. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/INDEX|curriculum/INDEX.md]]:192-195 |
| Sprint Contracts | Define o que pronto significa antes da execução. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/INDEX|curriculum/INDEX.md]]:196-207 |
| State Persistence | Mantém fatos críticos fora do contexto imediato. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/INDEX|curriculum/INDEX.md]]:245-248 |
| Harness Evolution | Remove scaffolding quando modelos melhoram e mede ciclo de vida do harness. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/INDEX|curriculum/INDEX.md]]:249-251 |
| Multi-Agent Coordination | Coordena Planner, Generator, Evaluator e agentes especializados. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/INDEX|curriculum/INDEX.md]]:236-239 |
| Evaluation Rubrics | Transforma qualidade subjetiva em critérios mensuráveis. | [[curriculum/README|curriculum/README.md]]:247-264; [[curriculum/INDEX|curriculum/INDEX.md]]:213-230 |

### Supporting Surfaces

- Exercises cobrem Nível 1, Nível 2, Nível 3, Nível 3 operacional e Nível 4 real-world; soluções vivem em `exercises/solutions/` por nível ([[curriculum/INDEX|curriculum/INDEX.md]]:99-129).
- Knowledge graphs incluem ecosystem completo, KODA feature dependencies, learning progression, problem-solution mapping e detailed graphs por conceito ([[curriculum/INDEX|curriculum/INDEX.md]]:145-153; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:366-375).
- Templates incluem sprint contract, evaluation rubric, knowledge graph, ADR, progress tracker e learning rubric ([[curriculum/INDEX|curriculum/INDEX.md]]:157-166; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:392-414).
- Implementation guides cobrem setup, progressão de equipe, harness design checklist, rubrics, trace analysis e harness evolution playbook ([[curriculum/INDEX|curriculum/INDEX.md]]:170-179; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:379-389).
- Case studies incluem Retro Game Maker, Browser DAW e três fluxos KODA: discovery, order processing e fulfillment ([[curriculum/INDEX|curriculum/INDEX.md]]:133-141; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:418-436).
- O cronograma de 12 semanas passa por Fundação, Padrões, Arquitetura e Aplicação KODA ([[curriculum/README|curriculum/README.md]]:270-284; [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]]:270-327).

## 6. Existing Gaps

| Gap | Where Documented |
|---|---|
| Nenhum ADR formal foi registrado; `docs/decisions/` contém apenas `.gitkeep` nesta leitura. | [[docs/system-of-record|docs/system-of-record.md]]:125-134; direct directory read of `docs/decisions/` |
| ADRs candidatos ainda pendentes: stack do portal, content chunking, persistência de estado entre agentes e versionamento do currículo. | [[docs/system-of-record|docs/system-of-record.md]]:127-134 |
| `docs/canonical/agent-lifecycle.md` está pendente para o ciclo claim -> worktree -> implement -> review -> merge -> cleanup. | [[docs/system-of-record|docs/system-of-record.md]]:55; [[docs/system-of-record|docs/system-of-record.md]]:212-219 |
| `docs/canonical/curriculum-model.md` está pendente para taxonomia de níveis, tipos de artefato e critérios de qualidade. | [[docs/system-of-record|docs/system-of-record.md]]:82; [[docs/system-of-record|docs/system-of-record.md]]:212-219 |
| `docs/canonical/portal-architecture.md` está pendente enquanto a SPA proposta não for implementada. | [[docs/system-of-record|docs/system-of-record.md]]:84-95; [[docs/system-of-record|docs/system-of-record.md]]:212-219 |
| `docs/canonical/crossroad-change-policy.md` está pendente como política de arquivos de alto blast radius. | [[docs/system-of-record|docs/system-of-record.md]]:123; [[docs/system-of-record|docs/system-of-record.md]]:212-219 |
| O PR template referencia crossroad files (`src/lib/safe-console.js`, `src/lib/logger.js`) e `docs/guides/crossroad-change-policy.md`, mas o SOR observa que eles ainda não existem. | [[docs/system-of-record|docs/system-of-record.md]]:117-123 |
| `docs/canonical/obsidian-document-conventions.md` aparece como documento esperado apenas se a convenção crescer além da Rule 16; hoje Rule 16 em `AGENTS.md` cobre a convenção. | [[docs/system-of-record|docs/system-of-record.md]]:180; [[docs/system-of-record|docs/system-of-record.md]]:220; [[AGENTS|AGENTS.md]]:120-238 |
| Agentes KODA referenciam docs em `docs/canonical/operations/`, `docs/canonical/product/` e `docs/canonical/architecture/`, mas as leituras recentes registram esses paths como NOT_FOUND. | [[.opencode/agents/koda-hop-init-basic.md|koda-hop-init-basic]]:28-35; [[.opencode/agents/hop-live-whatsapp-tester.md|hop-live-whatsapp-tester]]:22-31; [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD mental model]]:217 |
| Alguns gates citados por `issue-review` são exemplos mais amplos que não existem no `package.json` atual; os scripts reais são `lint`, `lint:fix`, `test:unit` e `test:integration`. | [[.opencode/skills/issue-review/SKILL.md|issue-review]]:50-71; [[package.json|package.json]]:8-13; [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD mental model]]:218 |
| O SOR atualiza canônicos ativos, mas `README.md` ainda fala em 16 padrões canônicos; pela precedência, o SOR vence. | [[README|README.md]]:53-56; [[README|README.md]]:90-105; [[docs/system-of-record|docs/system-of-record.md]]:135-211 |
| `curriculum/FAQ.md` ainda aparece como em construção em índices, embora análises recentes apontem conteúdo existente. | [[curriculum/README|curriculum/README.md]]:64-70; [[curriculum/INDEX|curriculum/INDEX.md]]:368-377; [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD mental model]]:220 |
| Gaps recentes de review ainda não têm artefatos operacionais completos fora dos canonicals/skills: `review-contract.yaml`, `risk-profile.yaml`, agreement dashboard e pre-commit AI review format aparecem como NOT_FOUND nas análises de canary. | [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary classification]]:50-62; [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary classification]]:88-90; [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary classification]]:146-150 |
| Gaps de ICE/token economics ainda permanecem em skills/exercises/lessons: skill e exercício de `Token Economics of Gap-Filling`, lesson dedicada a ICE Craft Separation e integração curricular adicional. | [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-integration-roadmap|IDSD integration roadmap]]:166-196 |

## Synthesis

O modelo mental útil é: `long-running-agents` tem quatro camadas acopladas. `docs/system-of-record.md` decide autoridade; `docs/canonical/` nomeia padrões e maturidade; `curriculum/` transforma padrões em trilha didática aplicada ao KODA; `.opencode/` transforma trabalho agentic em lifecycle governado por issue, handoff, review, gates e cleanup.

Para a próxima fase, a fonte externa deve ser comparada contra essas camadas, não contra uma memória genérica do repo. Em particular, qualquer ideia sobre intenção, ICE ou IDSD precisa respeitar o estado atual: o repo já tem `Intent as Five-Part Primitive`, `ICE Craft Separation`, `Human-Owned Expectations Boundary`, `Presence-in-the-Loop Metric`, `Token Economics of Gap-Filling`, skills correspondentes para intenção/valor/review, e gaps documentados para integração curricular e artefatos operacionais.
