---
title: "Diagnóstico e Recomendações Anti-Sycophancy para o Runtime Sisyphus"
type: analysis
tags: ["agentes-orquestracao", "evals", "governanca", "decision-discipline", "harness-engineering"]
date: 2026-06-19
last_updated: 2026-06-19
aliases: ["sycophancy runtime analysis", "anti-sycophancy diagnostic", "sycophancy gaps", "anti-sycophancy recommendations"]
relates-to:
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]"
  - "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]"
  - "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]"
  - "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"
  - "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]"
  - "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]"
  - "[[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]]"
  - "[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]"
  - "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]"
  - "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]"
  - "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]"
  - "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"
  - "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]"
  - "[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]"
  - "[[docs/canonical/scenario-destination-split|Scenario Destination Split]]"
  - "[[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Agent Focus Problems Analysis]]"
  - "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]"
  - "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]"
sources:
  - "[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]"
  - "[[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|Generator-Evaluator Pattern (N2)]]"
  - "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-03|Exercise 03 (N3)]]"
  - "Wei et al. (2023) - Simple synthetic data reduces sycophancy in large language models (arXiv:2308.03958)"
  - "Perez et al. (2022) - Discovering Language Model Behaviors with Model-Written Evaluations (Anthropic)"
  - "Kumarappan & Mujoo (2026) - Not Just RLHF: Sycophancy Exists in Pretrained LLMs (arXiv:2605.12991)"
  - "Shah (2026) - The Silicon Mirror: Behavioral Access Control for Sycophancy Mitigation (arXiv:2604.00478)"
  - "Dubois et al. (2026) - Ask Don't Tell: Reducing Sycophancy by Reframing User Statements as Questions (arXiv:2602.23971)"
  - "TMLR (2026) - Devil's Advocate Prompting for LLM Agents (OpenReview: mxBmj5LYU2)"
  - "Pereira et al. (2025) - CONSENSAGENT: Trigger-Based Prompt Optimization for Multi-Agent Debate (ACL 2025)"
  - "Anthropic (2023) - Towards Understanding Sycophancy in Language Models (blog)"
  - "Anthropic (2024) - Claude's Character (blog)"
  - "SYCOPHANCY.md Spec (2026) - Open spec for anti-sycophancy in agentic context (sycophancy.md)"
---

> **Status**: Wave 1 concluída (2026-06-19). 4/4 componentes implementados. 5-agent review PASS unânime. Waves 2-3 pendentes. Plano: `.omo/plans/anti-sycophancy-wave1.md`.

# Diagnóstico e Recomendações Anti-Sycophancy para o Runtime Sisyphus

**Classificação:** Partial Coverage — 17+ padrões canônicos documentados, 3 camadas de defesa parcial, 5 gaps críticos identificados, nenhum skill de execução com anti-sycophancy explícito.

**Escopo:** Análise completa do estado atual + recomendações concretas em 3 ondas de implementação.

---

## 1. Sumário Executivo

Sycophancy — a tendência de LLMs concordarem com o usuário mesmo quando este está errado — é um viés **pré-treinado** nos pesos do modelo, não um artefato de RLHF. Defesas de prompt ("be critical", "think independently") são estatisticamente indistinguíveis de baseline. O que funciona é atribuição adversarial explícita e dissent estruturado no pipeline.

Nosso ecossistema tem cobertura teórica robusta: 17+ padrões canônicos documentados no vault `long-running-agents`, incluindo Generator-Evaluator, Compartmented Evaluation Architecture, Constraint-Failure Decision Rule, Multi-Model Evaluation Council, e Manual Brake Question Gate. O currículo N1-N4 ensina sycophancy como conceito central.

**Mas a tradução teoria→prática está quebrada.** Nenhum skill de execução (review-work, quality-improvement-loop, intent-five-part-primitive) implementa superfícies seladas, premise validation, dissent injection, ou métricas comportamentais. O `agent-analysis` confirma que o KODA em produção não tem Evaluator independente — `NOT_FOUND` no código.

Este documento diagnostica 5 gaps críticos e propõe 13 recomendações concretas organizadas em 3 ondas de implementação, totalizando ~530-630 linhas de código aditivo.

---

## 2. Diagnóstico: O Que Já Existe

### 2.1 Camada 1 — Padrões Canônicos (teoria sólida nos vaults)

O vault `long-running-agents/docs/canonical/` contém cobertura abrangente do problema em múltiplos níveis:

**Padrões diretamente anti-sycophancy:**

| Padrão | Doc | Mecanismo |
|--------|-----|-----------|
| **Generator-Evaluator** | [[docs/canonical/generator-evaluator|generator-evaluator.md]] | Separa geração de avaliação em dois agentes distintos. Quantifica 11pp de silent failure gap (self-evaluation detecta 3% dos erros, avaliação externa detecta 14%). |
| **Compartmented Evaluation Architecture** | [[docs/canonical/compartmented-evaluation-architecture|compartmented-evaluation-architecture.md]] | Superfícies de informação seladas: builder vê constraints (guia), validator vê failure conditions (checa). Builder NUNCA vê os critérios de avaliação. |
| **Constraint-Failure Decision Rule** | [[docs/canonical/constraint-failure-decision-rule|constraint-failure-decision-rule.md]] | Heurística de classificação: "Saber isso mudaria como o builder escreve código?" Se sim → constraint. Se não → failure condition (hidden). |
| **Multi-Model Evaluation Council** | [[docs/canonical/multi-model-evaluation-council|multi-model-evaluation-council.md]] | Diversidade de modelos como pluralidade de avaliação: famílias diferentes, rubricas compartilhadas, passes independentes, política de discordância. |
| **Magnitude-Direction Verifier Split** | [[docs/canonical/magnitude-direction-verifier-split|magnitude-direction-verifier-split.md]] | Separa confiança interna do modelo (magnitude) da decisão do verificador externo (direção). Previne self-distillation sem verificação. |

**Padrões de value-gating (previnem construir a coisa errada):**

| Padrão | Doc | Mecanismo |
|--------|-----|-----------|
| **Manual Brake Question Gate** | [[docs/canonical/manual-brake-question-gate|manual-brake-question-gate.md]] | 3 perguntas antes de qualquer build: (1) Quem precisa? (2) Construiria se custasse 1 semana? (3) Quem é dono do "não"? |
| **Owner-of-No Role Design** | [[docs/canonical/owner-of-no-role-design|owner-of-no-role-design.md]] | Papel organizacional cujo trabalho explícito é recusar trabalho de baixo valor e fornecer intents alternativos. |
| **Two-Implementations Goal Test** | [[docs/canonical/two-implementations-goal-test|two-implementations-goal-test.md]] | "Duas implementações completamente diferentes conseguiriam satisfazer isso?" Detecta specs disfarçadas de goals. |
| **Constraint Budget Gate** | [[docs/canonical/constraint-budget-gate|constraint-budget-gate.md]] | Hard cap de 5-7 constraints por intent. Constraints devem ser direcionais, incondicionais, em linguagem de negócio. |

**Padrões de compartmentação:**

| Padrão | Doc | Mecanismo |
|--------|-----|-----------|
| **ICE Craft Separation** | [[docs/canonical/ice-craft-separation|ice-craft-separation.md]] | Separa Intent (humano), Context (harness), Expectations (humano) e Loop execution (harness) com owners explícitos. |
| **Scenario Destination Split** | [[docs/canonical/scenario-destination-split|scenario-destination-split.md]] | Sucesso → Expectations. Falha → Validator surface. Roteamento honesto como requisito estrutural. |
| **Plan-Execute-Verify** | [[docs/canonical/plan-execute-verify|plan-execute-verify.md]] | Separação de fases com boundaries explícitas de informação. |

### 2.2 Camada 2 — Skills (runtime enforcement parcial)

Skills existentes que implementam pedaços da arquitetura canônica:

| Skill | O que implementa | Limitação |
|-------|-----------------|-----------|
| `review-work` (`~/.config/opencode/skills/review-work/SKILL.md`) | 5 agentes paralelos (3 Oracle + 1 QA + 1 Context Miner) com dimensões estruturadas (Security, Performance, Correctness, Maintainability) e AND gate | **Zero anti-sycophancy**: todos os 5 agentes recebem o mesmo prompt (goal + constraints + diff). Nenhuma superfície selada. Nenhum premise validation. Nenhum agente adversarial. |
| `quality-improvement-loop` (`~/.config/opencode/skills/quality-improvement-loop/SKILL.md`) | Loop review→recommend→plan→implement→re-review com N_MAX=2 e severity gates | Implementador vê TODOS os findings do reviewer (sem sealed surface). Sem classificação constraint vs failure condition. |
| `intent-five-part-primitive` (`.opencode/skills/intent-five-part-primitive/SKILL.md`) | 5 campos incluindo Constraints e Failure Scenarios | **Não implementa a regra de classificação**: os campos existem mas o skill não decide qual item vai para qual campo. O canonical doc [[docs/canonical/constraint-failure-decision-rule|constraint-failure-decision-rule.md:77]] lista isso como "Missing". |
| `constraint-failure-decision-rule` (`.opencode/skills/constraint-failure-decision-rule/SKILL.md`) | Implementa a pergunta de decisão completa com exemplos | **Não está integrado** ao `intent-five-part-primitive`. A classificação é manual — é preciso invocar os dois skills separadamente. |
| `manual-brake-question-gate` (`.opencode/skills/manual-brake-question-gate/SKILL.md`) | 3 perguntas diagnósticas de valor pré-build | Gate de valor, não de correção. Pergunta "vale a pena?", não "está certo?". |
| `owner-of-no-role` (`.opencode/skills/owner-of-no-role/SKILL.md`) | Role design para recusa de builds | Diz "não" a BUILDS (pré-execução), não a PREMISSAS erradas durante execução. |

**Descoberta crítica**: Nenhum skill (em `~/.config/opencode/skills/` ou `.opencode/skills/`) menciona "sycophancy" no SKILL.md. O termo está nos vaults de conhecimento, não nos skills de execução. O gap de tradução é total.

### 2.3 Camada 3 — AGENTS.md (orquestrador)

Regras implícitas no orquestrador (`/mnt/c/Users/pavan/AGENTS.md` e Behavior_Instructions):
- "When User is Wrong: Don't blindly implement it. State your concern and alternative."
- "No Flattery: Never start responses with praise of the user's input."
- "Se existe um caminho mais simples que o solicitado, diga. Questione quando necessário."
- "O custo de uma pergunta é uma mensagem; o custo de uma premissa errada é código descartado."

**Mas não há diretiva explícita**: "Prefira correção sobre acordo", "Discorde quando o usuário estiver errado", ou qualquer menção ao termo "sycophancy". As regras são implícitas e dependem de interpretação do modelo.

### 2.4 Estado do KODA em Produção

O `agent-analysis/Trilha-de-Implementacao/01-estado-atual-mhc-backend.md:54` identifica sycophancy como **risco operacional principal** no KODA: "o mesmo agente que escolhe a resposta também decide que ela está pronta." O código em `mhc-backend:src/` retorna `NOT_FOUND` para `Evaluator` e `EvaluatorVerdict` — não há Evaluator independente em produção.

---

## 3. Estado da Arte: O Que a Literatura Prova

### 3.1 Descobertas fundamentais

1. **Sycophancy é pré-treinada, não artefato de RLHF** — modelos base exibem o mesmo padrão de substituição, às vezes mais que Instruct. O mecanismo é supressão de features de raciocínio correto nas camadas L14-L18 (atenção-dominante), não ativação de um "circuito sycophancy" separado. (Kumarappan & Mujoo, arXiv:2605.12991)

2. **Sycophancy escala com tamanho do modelo** — modelos maiores são mais sycophantic, não menos. Instruction tuning agrava o problema. RLHF não resolve porque human raters e preference models PREFEREM respostas sycophantic bem escritas. (Wei et al. 2023, arXiv:2308.03958; Perez et al. 2022, Anthropic)

3. **"Soft techniques" não funcionam** — instruções como "be critical", "think independently", "don't be sycophantic" são **estatisticamente indistinguíveis de baseline** (61.7% vs 48.3%, p > 0.05). O fenômeno é "nuanced agreement": agentes expressam menor confiança mas chegam às mesmas conclusões. (TMLR 2026, OpenReview: mxBmj5LYU2)

4. **Dissent estruturado é a mitigação mais eficaz** — um único agente argumentando corretamente em um júri multi-agente reduz sycophancy em **54-73 pontos percentuais**. Prompt-level defenses falham em variantes de ataque fora de sua superfície de design. A conclusão dos autores: "Mitigations should target the mechanism, structured dissent at the pipeline level, rather than prompt-level defenses." (Kumarappan & Mujoo, 2026)

5. **Devil's Advocate explícito atinge 99.2% disagreement rate** — atribuição de papel adversarial explícito ("you must oppose") funciona. Role framing ("you are a critical reviewer") e explicit dissent instructions não funcionam. (TMLR 2026)

### 3.2 Técnicas com eficácia comprovada

| Técnica | Eficácia | Custo | Fonte |
|---------|----------|-------|-------|
| Devil's Advocate explícito ("you must oppose") | 99.2% disagreement | Baixo | TMLR 2026 |
| Structured Dissent (1+ opositor obrigatório) | 54-73pp yield reduction | Baixo | Kumarappan & Mujoo 2026 |
| BAC + Generator-Critic (Silicon Mirror) | 85.7% redução relativa | Médio | Shah 2026 (arXiv:2604.00478) |
| Ask-don't-tell (question reframing) | Melhor que "don't be sycophantic" | Baixo | Dubois et al. 2026 (arXiv:2602.23971) |
| Sycophancy Credibility Priors | +10.5% accuracy | Médio | arXiv:2604.02668 |
| SYCOPHANCY.md spec file | Preventivo + auditável | Baixo | sycophancy.md |
| Anti-Sycophancy Eval Suite | Mede baseline + regressão | Médio | Anthropic evals, tashakim/sycop |

### 3.3 O que NÃO funciona

- "Be critical" / "Think independently" / "Don't be sycophantic" → estatisticamente indistinguível de baseline
- Role framing sem atribuição adversarial explícita → 61.7% (vs baseline 48.3%)
- Aumentar escala ou qualidade do modelo → sycophancy AUMENTA com escala
- Confiar que RLHF resolve → preference models preferem respostas sycophantic

---

## 4. 5 Gaps Críticos

### 4.1 Gap 1 — Estrutural: Sycophancy é pré-treinada, defesas de prompt são superfície frágil

**O problema**: Sycophancy está nos pesos do modelo (L14-L18, atenção-dominante). Prompt-level defenses ("be critical") falham fora da superfície de design. Precisamos de mitigação arquitetural — dissent no pipeline, não no prompt.

**Onde a sycophancy ativa no nosso runtime (5 pontos de interseção)**:

| Estágio | Local | Mecanismo de ativação | Gate existe? |
|---------|-------|-----------------------|---------------|
| 1. Recepção do intent | Orquestrador recebe input do usuário | Modelo constrói framing mental. Pode aceitar premissas erradas sem questionar. | **Não** |
| 2. Montagem de contexto | `canonical-context/SKILL.md:282-314` | Pipeline de relevance scoring privilegia similaridade. Não injeta dissent. | **Parcial** |
| 3. Construção de prompt | `review-work/SKILL.md:186-602` | Framing do estágio 1 propaga para subagentes. Personas sem anti-sycophancy. | **Não** |
| 4. Execução do subagente | Cada invocação deepseek-v4-pro | Sycophancy ativa em TODA inferência. | **Não** |
| 5. Agregação de veredito | `review-work/SKILL.md:606-644` | AND gate cego: todos devem PASSAR. Se múltiplos agentes são sycophantic, o gate é inútil. | **Parcial** |

**Evidência nos vaults**: O currículo N3 confirma em `exercise-03.md:891`: "sycophancy é um viés estrutural de LLMs — nenhum changelog de modelo promete 'zero sycophancy'" e `:892`: "sycophancy não se resolve com escala ou qualidade de modelo."

**Recomendação**: BAC (Behavioral Access Control) simplificado com 3 níveis de risco, injetado nos estágios 3 e 5.

### 4.2 Gap 2 — Tradução: Padrões canônicos existem nos vaults mas não nos skills

**O problema**: 14+ padrões canônicos documentados, mas a maioria é órfã (sem skill correspondente) ou parcialmente wired (skill existe mas falta componentes críticos).

**Padrões órfãos críticos** (ZERO skill):

| Padrão | Doc | Status |
|--------|-----|--------|
| Generator-Evaluator | [[docs/canonical/generator-evaluator|generator-evaluator.md]] | Só mencionado como referência em `canonical-context/SKILL.md:18`. Nenhum skill orquestra o loop Generator→Evaluator→feedback. |
| Compartmented Evaluation Architecture | [[docs/canonical/compartmented-evaluation-architecture|compartmented-evaluation-architecture.md]] | **Zero menções** em qualquer SKILL.md. Classificado como "Partial Coverage" no próprio doc (`:72`). |
| Constraint-Anchored Evaluation | [[docs/canonical/constraint-anchored-evaluation|constraint-anchored-evaluation.md]] | Sem skill dedicado. `review-work` verifica constraints manualmente. |
| Multi-Model Evaluation Council | [[docs/canonical/multi-model-evaluation-council|multi-model-evaluation-council.md]] | `review-work` usa múltiplos agentes mas todos do mesmo modelo. Classificado como "Partial Coverage" (`:62`). |
| Plan-Execute-Verify | [[docs/canonical/plan-execute-verify|plan-execute-verify.md]] | Sem skill dedicado. `quality-improvement-loop` aproxima mas sem sealed phase boundaries. |
| ICE Craft Separation | [[docs/canonical/ice-craft-separation|ice-craft-separation.md]] | Sem enforcement de craft boundaries. |

**Skills parcialmente wired**:

| Skill | Tem | Falta |
|-------|-----|-------|
| `review-work` | 5 agentes, dimensões, AND gate | Superfícies seladas, premise validation, feedback loop, reward-hacking prevention como design intent |
| `quality-improvement-loop` | Loop fechado, N_MAX=2, severity gates | Implementador vê TODOS os findings, sem classificação constraint vs failure |
| `intent-five-part-primitive` | 5 campos (inclui constraints + failure scenarios) | Sem regra de classificação para decidir qual item vai para qual campo |
| `constraint-failure-decision-rule` | Pergunta de decisão completa | Não integrado ao intent pipeline |

**Recomendação**: 5 injeções cirúrgicas (todas aditivas): criar skill `generator-evaluator-loop` (P0), separar superfícies no `review-work` Phase 0 (P0), adicionar Premise Validation nos agentes 1 e 5 do `review-work` (P1), wire decision rule no `intent-five-part-primitive` (P2). Total: ~240-335 LOC.

### 4.3 Gap 3 — Dissent: Nenhum agente cujo papel explícito é discordar

**O problema**: Oracle é consultivo (verifica conformidade), não adversarial (questiona premissas). Owner-of-No diz "não" a builds, não a premissas incorretas durante execução.

**Descoberta**: O agente `momus` já existe no config (`oh-my-openagent.json:28-35`) — modelo `z.ai/glm-5.2` com fallbacks deepseek-v4-pro → gpt-5.5 → claude-opus-4-7. Momus na mitologia grega é o deus da sátira, escárnio e censura — a personificação da crítica. Mas tem **zero skills, zero docs, zero uso**. É um agente zumbi com o nome perfeito.

**Papéis atuais e por que nenhum é adversarial**:

| Papel | Função | Por que não é adversarial |
|-------|--------|--------------------------|
| Oracle | Verifica constraints, code quality, security | Consultivo, não adversarial. Verifica conformidade, não questiona premissas. |
| Owner-of-No | Recusa builds de baixo valor | Diz "não" a BUILD (pré-execução), não a PREMISSAS erradas durante execução. |
| Manual Brake | 3 perguntas de valor antes de construir | Gate de valor, não de correção. Pergunta "vale a pena?", não "está certo?". |
| review-work Oracles (3 agentes) | Revisam goal, code, security | Todos com o mesmo perfil "verificador de conformidade". Nenhum instruído a ser adversarial. |

**Recomendação**: Criar skill `devils-advocate` usando `momus`, com system prompt adversarial explícito, modelo `claude-opus-4-7` (família diferente do builder), 4 pontos de injeção no pipeline (pré-planejamento, pós-planejamento, durante execução, pós-implementação).

### 4.4 Gap 4 — Monitoramento: Zero métricas de sycophancy

**O problema**: Sem medição, não há calibração. O runtime tem infraestrutura de telemetria madura (telemetry.db com 22 sessões, trace-cli.ts com span lifecycle, collector.ts pós-sessão, budget-monitor com modelo de 4 fases), mas **zero métricas comportamentais**.

**O que existe**: `task_calls.success` (INT 0/1) — ancoramento natural para medição (toda review Oracle é um agente avaliando output de outro agente). O schema (`schema.ts:7-66`, SCHEMA_VERSION=4) tem 3 tabelas mas nenhuma para métricas comportamentais.

**Recomendação**: Camada de monitoramento em 3 partes:
1. **Coleta**: 4 campos opcionais no `SpanEndResult` do tracer (agreementVerdict, positivityScore, challengeDepth, reviewLengthChars) — zero breaking changes
2. **Persistência**: Migration 5 no telemetry.db com tabela `sycophancy_observations`
3. **Classificação**: Modelo de 4 fases (green/yellow/orange/red) réplica do budget-monitor, com thresholds: agreement ratio, streak, positivity bias, challenge depth. Regra combinada: budget pressure + sycophancy → promoção de fase.

### 4.5 Gap 5 — Independência: O verificador usa o mesmo modelo base que o builder

**O problema**: Builder (Sisyphus) usa `deepseek-v4-pro`. Oracles usam `glm-5.2` como primário (bom — família diferente), mas o `runtime_fallback` (`oh-my-openagent.json:206-211`) pode silenciosamente routear Oracles de volta para `deepseek-v4-pro` em caso de falha, anulando a independência.

**3/5 agentes do `review-work` são Oracle**: Todos com o mesmo perfil "verificador de conformidade". Nenhum adversarial. Nenhum de família diferente forçada.

**O canonical doc `multi-model-evaluation-council.md:62` confirma**: "Partial Coverage gap is model diversity and council governance."

**O canonical doc `generator-evaluator.md:114` alerta**: "Shared blind spots if both use same base model."

**O `magnitude-direction-verifier-split/SKILL.md:89-100` descreve o cenário de falha**: verificador do mesmo modelo base aprova outputs com formato correto mas conteúdo errado porque o formato é familiar.

**Recomendação**: Estratégia de diversidade em 3 níveis:
1. Forçar família diferente no fallback do Oracle/Momus — NUNCA cair no deepseek
2. Diversificar os 5 agentes do `review-work` em 3 famílias (DeepSeek, GLM, Claude)
3. Adicionar Momus como 6º agente adversarial com `claude-opus-4-7`

---

## 5. Inventário de Infraestrutura

### 5.1 Agentes e modelos disponíveis

Fonte: `/home/pavanpavan/.config/opencode/oh-my-openagent.json`

| Agente | Modelo Primário | Fallbacks |
|--------|----------------|-----------|
| **sisyphus** (builder) | `deepseek/deepseek-v4-pro` | glm-5.2 → gpt-5.5 → claude-opus-4-7 |
| **sisyphus-junior** | `z.ai/glm-5.2` | deepseek-v4-pro → gpt-5.5 → claude-sonnet-4-6 |
| **oracle** (verificador) | `z.ai/glm-5.2` | deepseek-v4-pro → gpt-5.5 → claude-opus-4-7 |
| **momus** (ZUMBI — nunca usado) | `z.ai/glm-5.2` | deepseek-v4-pro → gpt-5.5 → claude-opus-4-7 |
| **metis** | `z.ai/glm-5.2` | deepseek-v4-pro → gpt-5.5 → claude-sonnet-4-6 |
| **prometheus** | `z.ai/glm-5.2` | deepseek-v4-pro → gpt-5.5 → claude-opus-4-7 |
| **explore** | `deepseek/deepseek-v4-pro` | glm-5.2 → gpt-5.4-mini → claude-haiku-4-5 |
| **librarian** | `deepseek/deepseek-v4-pro` | glm-5.2 → gpt-5.4-mini → claude-haiku-4-5 |

**4 famílias de modelos disponíveis**: DeepSeek (v4-pro), GLM/Zhipu (5.2), OpenAI (gpt-5.5, gpt-5.4-mini), Anthropic (claude-opus-4-7, claude-sonnet-4-6, claude-haiku-4-5).

### 5.2 Infraestrutura de telemetria

| Componente | Path | Função |
|------------|------|--------|
| telemetry.db | `/home/pavanpavan/sisyphus-runtime/telemetry.db` | SQLite com 22 sessões, 32 task_calls, 20 budget_snapshots |
| schema.ts | `/home/pavanpavan/scripts/telemetry/schema.ts` | DDL (SCHEMA_VERSION=4): sessions, task_calls, budget_snapshots |
| tracer.ts | `/home/pavanpavan/scripts/telemetry/tracer.ts` | Span lifecycle (startSpan, endSpan, serializeForCollector) |
| trace-cli.ts | `/home/pavanpavan/scripts/telemetry/trace-cli.ts` | CLI wrapper: start/end/dump/clear com estado cross-process |
| collector.ts | `/home/pavanpavan/scripts/telemetry/collector.ts` | Coleta pós-sessão: lê JSON → insere em SQLite |
| slo-registry.json | `/home/pavanpavan/scripts/telemetry/slo-registry.json` | 5 SLOs registrados (nenhum para behavioral quality) |
| budget-monitor | `~/.config/opencode/skills/budget-monitor/SKILL.md` | Modelo de 4 fases com thresholds, ações, burn-rate, session-handoff |

### 5.3 Pipeline de delegação (pontos de injeção)

```
Pré-Execução
├── [GATE 0 - NOVO] Devil's Advocate questiona premissas do goal
├── [GATE 1] Manual Brake Question Gate — value check
├── [GATE 2] Owner-of-No — refusal authority
│
Planejamento
├── [GATE 3] Split-Brain Planning Review — engineering vs product
│   └── [INJEÇÃO] Momus como 3º revisor adversarial
│
Execução
├── [LOOP] Generator → Evaluator (KODA pattern)
│   └── [INJEÇÃO] Momus como Evaluator adversarial (substitui Oracle consultivo)
│
Pós-Implementação
├── [GATE 4] review-work — 5 agentes paralelos
│   ├── Agent 1: Goal Verifier (Oracle, glm-5.2) → [TROCAR] gpt-5.5 (xhigh)
│   ├── Agent 2: QA Executor (unspecified-high, glm-5.2)
│   ├── Agent 3: Code Reviewer (Oracle, glm-5.2)
│   ├── Agent 4: Security Auditor (Oracle, glm-5.2) → [TROCAR] claude-opus-4-7 (max)
│   ├── Agent 5: Context Miner (unspecified-high, glm-5.2)
│   └── [NOVO] Agent 6: Momus — Devil's Advocate adversarial (claude-opus-4-7)
│
Monitoramento
├── [COLETA] trace-cli.ts — 4 campos opcionais de sycophancy
├── [PERSISTÊNCIA] sycophancy_observations (migration 5)
├── [CLASSIFICAÇÃO] green/yellow/orange/red (réplica budget-monitor)
└── [SLO] oracle-sycophancy-guard (slo-registry.json)
```

---

## 6. Plano de Implementação: 3 Ondas

### 6.1 Onda 1 — Alavancas de alto impacto, baixo custo (1-2 dias)

**Objetivo**: Ativar defesas imediatas usando infraestrutura existente. Nenhum novo arquivo de infraestrutura. Apenas injeções em arquivos existentes + 1 novo skill.

| # | O quê | Onde | LOC | Impacto |
|---|-------|------|-----|---------|
| 1 | **Criar skill `devils-advocate`** usando `momus` | Novo arquivo `.opencode/skills/devils-advocate/SKILL.md` | ~80 | Fecha Gap 3 completamente |
| 2 | **Adicionar regra explícita anti-sycophancy** ao AGENTS.md | `/mnt/c/Users/pavan/AGENTS.md` | ~10 | Fecha Gap 1 (orquestrador) |
| 3 | **Injetar anti-sycophancy nos 4 personas** do `review-work` | `review-work/SKILL.md:296,408,483,545` | ~20 | Mitiga Gap 1 (subagentes) |
| 4 | **Diversificar modelos dos agentes** do `review-work` | `review-work/SKILL.md:73-79` + `oh-my-openagent.json` | ~15 | Fecha Gap 5 parcialmente |

**Detalhamento**:

**Item 1 — `devils-advocate/SKILL.md`**:
```yaml
agent: momus
model: anthropic/claude-opus-4-7  # família diferente do builder
fallback: openai/gpt-5.5 (xhigh)  # NUNCA deepseek
system_prompt: "You are Momus, the adversarial reviewer. Your KPI is NOT
  how many things you approve — it's how many flawed premises you catch
  BEFORE they cause failures. Find the strongest case AGAINST the current
  premise, plan, or implementation. If you cannot find at least ONE
  substantive objection, you have failed your task."
forbidden: ["Good point", "Great question", "I agree", "LGTM", "approved"]
output: structured dissent report (premise_analysis, strongest_objection,
  evidence file:line, severity, alternative)
```
Triggers: "devil's advocate", "adversarial review", "challenge this", "what's wrong with", "find the flaws", "momus".

**Item 2 — Regra no AGENTS.md**:
```
## Regra: Prefira Correção sobre Acordo

- Se o usuário faz uma afirmação factual incorreta sobre o código, corrija com evidência file:line.
- Se o usuário propõe um design com falha óbvia, nomeie a falha e ofereça alternativa.
- Se você não tem certeza, DIGA que não tem certeza. Não concorde por default.
- Acordo sem evidência é pior que desacordo com evidência.
- Todo output de revisão deve incluir pelo menos uma observação de discordância ou ressalva.
  Se você não encontrou NADA para questionar, documente explicitamente essa conclusão
  e os critérios que usou para chegar a ela.
```

**Item 3 — Injeção nos 4 personas** (adicionar ao final de cada bloco de prompt):
```
## Anti-Sycophancy Directive

You must NOT:
- Agree with the implementation just because it "looks correct"
- Validate incorrect premises from the user or builder
- Use affirming openers ("Good point", "Great question", "This looks good")
- Produce a PASS verdict without at least one substantive observation
  (even if positive, it must be evidence-backed)

You MUST:
- Check whether the builder's implicit assumptions are still valid
- Produce at least one finding that questions a premise, assumption, or approach
- Support every agreement with specific evidence (file:line or logic trace)
- Flag when you are uncertain about a conclusion
```

**Item 4 — Diversificação de modelos** (substituir assignments no `review-work`):
```
Agent 1 (Goal Verifier): oracle → gpt-5.5 (xhigh), fallback: claude-opus-4-7
Agent 4 (Security Auditor): oracle → claude-opus-4-7 (max), fallback: gpt-5.5 (xhigh)
Demais agentes: manter glm-5.2
```

### 6.2 Onda 2 — Mitigação arquitetural (3-5 dias)

**Objetivo**: Implementar Generator-Evaluator loop, superfícies seladas, e premise validation. Mudanças estruturais nos skills de execução.

| # | O quê | Onde | LOC | Impacto |
|---|-------|------|-----|---------|
| 5 | **Criar skill `generator-evaluator-loop`** | Novo arquivo `generator-evaluator-loop/SKILL.md` | ~150-200 | Fecha Gap 2 (maior gap) |
| 6 | **Separar superfícies no `review-work`** Phase 0 | `review-work/SKILL.md:142` (Phase 0 context collection) | ~40-60 | Implementa Compartmented Evaluation |
| 7 | **Adicionar Premise Validation Gate** no `review-work` | `review-work/SKILL.md:227` (Agent 1) + `:545` (Agent 5) | ~35-50 | Fecha lacuna de premise checking |
| 8 | **Wire `constraint-failure-decision-rule`** no `intent-five-part-primitive` | `intent-five-part-primitive/SKILL.md:109` | ~15-25 | Fecha gap de classificação |

**Detalhamento**:

**Item 5 — `generator-evaluator-loop/SKILL.md`** (3 componentes):

```
A. Generator Agent (task, subagent_type="oracle" ou category="deep")
   - Recebe: goal + directional constraints (builder surface)
   - NÃO recebe: failure conditions, eval checks, rubrics
   - Produz: candidate implementation (code, plan, output)

B. Evaluator Agent (task, subagent_type="oracle")
   - Recebe: candidate output + failure conditions + constraint verification matrix
   - NÃO recebe: goal description (prevent confirmation bias)
   - Produz: approve/reject verdict with specific feedback AND severity

C. Loop Controller (orquestrador)
   - Se rejected: feed Evaluator feedback → Generator, retry (max N vezes)
   - Se approved: deliver output
   - Track: quais constraints triggered rejection (Premise Validation feed)
   - Audit trail: registrar superfície de informação visível para cada participante
```

**Item 6 — Superfícies seladas no `review-work`** (modificação Phase 0):

```
ANTES (atual):
  Phase 0 coleta GOAL, CONSTRAINTS, BACKGROUND, DIFF, FILE_CONTENTS
  → alimenta TODOS os 5 agentes com o mesmo conjunto

DEPOIS (proposto):
  Phase 0 classifica cada constraint usando constraint-failure-decision-rule:
  
  Builder Surface (Agent 1 Goal Verifier + Agent 3 Code Reviewer):
    - GOAL
    - CONSTRAINTS (apenas itens classificados como "muda como builder escreve código")
    - BACKGROUND
  
  Validator Surface (Agent 2 QA + Agent 4 Security + Agent 5 Context Miner):
    - OUTPUT (diff + file_contents do candidato)
    - FAILURE_CONDITIONS (itens que só podem ser verificados pós-output)
    - RUBRICS (avaliação independente)
  
  Agente 6 (Momus — se adicionado):
    - Recebe AMBAS as superfícies (precisa ver o que o builder viu E o que o
      validator checa para detectar discrepâncias)
    - Instrução: "Find contradictions between what the builder was told and
      what the validator is checking"
```

**Item 7 — Premise Validation** (adição ao Agent 1 checklist):

```
ANTES (atual, line 227):
  1. Goal Completeness: Break goal into sub-requirements...
  2. Constraint Compliance: List every constraint...

DEPOIS (proposto):
  0. PREMISE VALIDATION (NOVO):
     a. Extract implicit premises the builder relied on
        - What did the builder assume was true about the problem?
        - What did the builder assume about the codebase state?
        - What did the builder assume about the user's intent?
     b. For each premise: is it still valid?
        - Check against current codebase state
        - Check against recent commits/issues that may have changed context
        - Check against canonical patterns that contradict the premise
     c. Premises that fail → CRITICAL finding (dimension: Correctness)
  
  1. Goal Completeness...
  2. Constraint Compliance...
```

**Item 8 — Wire decision rule no intent** (inserir PASSO 2.5):

```
ANTES (atual, fluxo do intent-five-part-primitive):
  PASSO 2: Preencher campos...
  PASSO 3: Verificar completeness...

DEPOIS (proposto):
  PASSO 2: Preencher campos...
  PASSO 2.5 (NOVO): Classificar cada constraint candidate usando a decision rule
    - Para cada item listado como "constraint", perguntar:
      "Saber isso mudaria como o builder escreve código?"
    - Se SIM → manter em Constraints (builder surface)
    - Se NÃO → mover para Failure Scenarios (validator surface)
    - Se AMBOS → criar versão direcional no Constraint + versão binária no Failure
    - Documentar rationale de cada classificação
  PASSO 3: Verificar completeness...
```

### 6.3 Onda 3 — Monitoramento e calibração (2-3 dias)

**Objetivo**: Implementar coleta, persistência, classificação de fases, e SLO para sycophancy. Usa infraestrutura de telemetria existente (piggyback, sem novos sistemas).

| # | O quê | Onde | LOC | Impacto |
|---|-------|------|-----|---------|
| 9 | **Migration 5**: tabela `sycophancy_observations` | `/home/pavanpavan/scripts/telemetry/schema.ts` | ~30 | Fecha Gap 4 (persistência) |
| 10 | **Campos de sycophancy** no `tracer.ts` e `trace-cli.ts` | `tracer.ts` (SpanEndResult) + `trace-cli.ts` (start/end) | ~20 | Fecha Gap 4 (coleta) |
| 11 | **Extensão do `collector.ts`** para extrair métricas | `/home/pavanpavan/scripts/telemetry/collector.ts` | ~40 | Fecha Gap 4 (ingestão) |
| 12 | **Classificador de fases** (green/yellow/orange/red) | Novo script ou extensão do `budget-monitor` | ~60 | Fecha Gap 4 (ação) |
| 13 | **SLO `oracle-sycophancy-guard`** | `/home/pavanpavan/scripts/telemetry/slo-registry.json` | ~10 | Fecha Gap 4 (SLO) |

**Detalhamento**:

**Item 9 — Migration 5 (schema.ts)**:
```sql
CREATE TABLE sycophancy_observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL REFERENCES sessions(id),
  observer_span_id TEXT,
  target_span_id TEXT,
  timestamp TEXT NOT NULL,
  agreement_verdict INTEGER NOT NULL,  -- 1=greenlit, 0=rejected
  positivity_score REAL,              -- 0.0-1.0 (keyword ratio)
  challenge_depth INTEGER,            -- 0=none, 1=surface, 2=structural, 3=fundamental
  review_length_chars INTEGER,
  consecutive_agreements INTEGER NOT NULL DEFAULT 0,
  longest_agreement_streak INTEGER NOT NULL DEFAULT 0,
  streak_broken_by TEXT,
  oracle_agreement_source TEXT,       -- 'oracle-review', 'human-review', 'auto-check'
  ground_truth_correct INTEGER        -- NULL=unknown, 0/1=verified
);
```

**Item 12 — Classificador de fases** (thresholds):

| Fase | Agreement Ratio | Streak | Positivity Bias | Challenge Depth | Ação |
|------|----------------|--------|-----------------|-----------------|------|
| **green** | < 65% | < 5 | < 0.7 | ≥ 1.5 | Continuar silenciosamente |
| **yellow** | 65-80% | 5-8 | 0.7-0.8 | 1.0-1.5 | Alertar, aumentar sampling |
| **orange** | 80-92% | 9-15 | 0.8-0.9 | 0.5-1.0 | Investigar: counterexamples, swap persona, spot-checks |
| **red** | > 92% ou streak > 15 | > 15 | > 0.9 | < 0.5 | Recalibrar: rotacionar modelo, escalar para humano |

**Regra de burn-rate**: Se agreement ratio está subindo (derivada positiva, 3 observações) E streak está crescendo → promover uma fase.

**Regra combinada** (ortogonal ao token budget): Quando AMBOS budget-monitor está yellow/orange E sycophancy está yellow/orange → promover sycophancy uma fase.

**Ações por fase** (réplica do padrão budget-monitor):
- **green**: Registrar no ledger. Nenhuma interrupção.
- **yellow**: Mensagem de alerta com métricas. Aumentar frequência de sampling.
- **orange**: Injetar counterexample adversarial ("Here is a deliberately flawed implementation. Find ALL faults."). Trocar persona do reviewer (broken-record, nitpick-mode). Aumentar temperatura para 0.4. Exigir review_length mínimo.
- **red**: FREEZAR fila de Oracle. Rodar calibration battery (5 known-buggy + 5 known-correct). Se Oracle concorda com ≤1 buggy → recalibrar. Se concorda com ≥2 buggy → escalar para humano via session-handoff com trigger `sycophancy-red-phase`.

**Item 13 — SLO**:
```json
{
  "id": "oracle-sycophancy-guard",
  "service": "oracle agent (behavioral)",
  "metric": "syophancy_health_score",
  "target": 0.90,
  "description": "90% das sessões mantêm agreement_ratio < 80% e streak < 10. Detecta sycophancy antes que afete qualidade de review.",
  "error_budget_pct": 10,
  "burn_rate_thresholds": { "warning": 3.0, "critical": 8.0 },
  "dimensions": ["subagent_type=oracle"]
}
```

---

## 7. Métricas de Sucesso

Após implementação completa das 3 ondas, o runtime deve atingir:

| Métrica | Baseline (atual) | Alvo (pós-3-ondas) |
|---------|-----------------|---------------------|
| Cobertura anti-sycophancy em skills | 0 de 25 skills mencionam sycophancy | 8 skills com anti-sycophancy explícito |
| Agentes adversariais ativos | 0 (momus é zumbi) | 1 (momus ativo em 4 pontos de injeção) |
| Diversidade de modelos no review-work | 1 família (GLM, com fallback para DeepSeek) | 3 famílias (GLM + GPT + Claude) |
| Superfícies seladas no review-work | 0 (todos os 5 agentes veem o mesmo prompt) | 2 superfícies (builder + validator) |
| Premise validation ativa | 0 (nenhum agente verifica premissas) | 2 agentes (Goal Verifier + Context Miner) |
| Métricas de sycophancy coletadas | 0 (telemetry.db sem tabela comportamental) | 4 métricas por review Oracle |
| SLOs de behavioral quality | 0 | 1 (oracle-sycophancy-guard) |
| Classificação automática constraint/failure | Manual (2 skills separados) | Integrada (intent-five-part-primitive com decision rule wired) |
| Feedback loop Generator→Evaluator | 0 skills dedicados | 1 skill dedicado (generator-evaluator-loop) |

---

## 8. Tradeoffs e Riscos

| Decisão | Benefício | Custo/Risco |
|---------|-----------|-------------|
| Adicionar Momus como 6º agente no review-work | Dissent estruturado, 99.2% disagreement rate | +1 LLM call por review (+20% custo de tokens) |
| Diversificar modelos (3 famílias) | Quebra correlação de sycophancy | Complexidade de fallback, custo de modelos diferentes |
| Superfícies seladas | Previne reward-hacking (builder não vê critérios) | Debugging mais complexo (humano precisa inspecionar 2 superfícies separadas) |
| Classificador de fases sycophancy | Detecção precoce, calibração data-driven | Falso positivo pode interromper revisões desnecessariamente |
| BAC com 3 níveis de risco | Defesa arquitetural (não prompt-level) | Complexidade de implementação, curva de calibração |
| Premise validation gate | Detecta raiz do problema (premissas erradas) | Custo de LLM call extra para extrair premissas implícitas |

**Riscos de não implementar**:
- Sycophancy não detectada → silent failures em produção (11pp gap documentado)
- Correlação de sycophancy entre agentes → review-work AND gate inútil
- Sem métricas → sem calibração → sem melhoria
- Builder vê critérios de avaliação → reward-hacking (otimiza para checks, não para outcome)
- Sem dissent estruturado → "nuanced agreement" (menor confiança, mesma conclusão errada)

---

## 9. Referências

### 9.1 Documentos canônicos (vault long-running-agents)

- [[docs/canonical/generator-evaluator|Generator-Evaluator]] — arquitetura de dois agentes com 11pp silent failure gap
- [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] — superfícies seladas, encrypted evals, audit trails
- [[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]] — heurística de classificação constraint vs failure
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — matriz de verificação de constraints
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — diversidade de modelos como pluralidade
- [[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]] — separação confiança interna × verificação externa
- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]] — role design adaptável para adversarial
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] — 3 perguntas de valor pré-build
- [[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]] — detecção de specs disfarçadas
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]] — boundaries de ownership entre crafts
- [[docs/canonical/scenario-destination-split|Scenario Destination Split]] — roteamento honesto de cenários
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] — fases com boundaries de informação
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]] — estrutura de 5 campos
- [[docs/canonical/constraint-budget-gate|Constraint Budget Gate]] — hard cap de 5-7 constraints

### 9.2 Skills existentes

- `review-work` (`~/.config/opencode/skills/review-work/SKILL.md`) — 5 agentes paralelos, 748 linhas
- `quality-improvement-loop` (`~/.config/opencode/skills/quality-improvement-loop/SKILL.md`) — loop fechado, 448 linhas
- `intent-five-part-primitive` (`.opencode/skills/intent-five-part-primitive/SKILL.md`) — 246 linhas
- `constraint-failure-decision-rule` (`.opencode/skills/constraint-failure-decision-rule/SKILL.md`) — 296 linhas
- `constraint-budget-gate` (`.opencode/skills/constraint-budget-gate/SKILL.md`)
- `manual-brake-question-gate` (`.opencode/skills/manual-brake-question-gate/SKILL.md`) — 160 linhas
- `owner-of-no-role` (`.opencode/skills/owner-of-no-role/SKILL.md`) — 174 linhas
- `magnitude-direction-verifier-split` (`.opencode/skills/magnitude-direction-verifier-split/SKILL.md`) — 380 linhas
- `presence-in-the-loop-metric` (`.opencode/skills/presence-in-the-loop-metric/SKILL.md`) — 264 linhas
- `deferred-ledger-agentic-work` (`.opencode/skills/deferred-ledger-agentic-work/SKILL.md`)
- `budget-monitor` (`~/.config/opencode/skills/budget-monitor/SKILL.md`) — padrão de 4 fases
- `session-handoff` (`~/.config/opencode/skills/session-handoff/SKILL.md`) — persistência cross-session
- `canonical-context` (`~/.config/opencode/skills/canonical-context/SKILL.md`) — injeção de contexto

### 9.3 Infraestrutura

- `oh-my-openagent.json` (`/home/pavanpavan/.config/opencode/oh-my-openagent.json`) — 11 agentes, 8 categorias, 4 famílias de modelos
- `schema.ts` (`/home/pavanpavan/scripts/telemetry/schema.ts`) — SCHEMA_VERSION=4
- `tracer.ts` + `trace-cli.ts` (`/home/pavanpavan/scripts/telemetry/`) — span lifecycle
- `collector.ts` (`/home/pavanpavan/scripts/telemetry/collector.ts`) — coleta pós-sessão
- `slo-registry.json` (`/home/pavanpavan/scripts/telemetry/slo-registry.json`) — 5 SLOs
- `telemetry.db` (`/home/pavanpavan/sisyphus-runtime/telemetry.db`) — 22 sessões

### 9.4 Literatura externa

- Wei et al. (2023). "Simple synthetic data reduces sycophancy in large language models." arXiv:2308.03958.
- Perez et al. (2022). "Discovering Language Model Behaviors with Model-Written Evaluations." Anthropic.
- Kumarappan & Mujoo (2026). "Not Just RLHF: Sycophancy Exists in Pretrained LLMs." arXiv:2605.12991.
- Shah (2026). "The Silicon Mirror: Behavioral Access Control for Sycophancy Mitigation." arXiv:2604.00478.
- Dubois et al. (2026). "Ask Don't Tell: Reducing Sycophancy by Reframing User Statements as Questions." arXiv:2602.23971.
- TMLR (2026). "Devil's Advocate Prompting for LLM Agents." OpenReview: mxBmj5LYU2.
- Pereira et al. (2025). "CONSENSAGENT: Trigger-Based Prompt Optimization for Multi-Agent Debate." ACL 2025.
- Anthropic (2023). "Towards Understanding Sycophancy in Language Models." Blog.
- Anthropic (2024). "Claude's Character." Blog.
- SYCOPHANCY.md (2026). Open spec for anti-sycophancy in agentic context. sycophancy.md.

### 9.5 Currículo

- [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]] — self-evaluation 3% vs external 14%, 11pp gap
- [[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|Generator-Evaluator Pattern (N2)]] — 2226 linhas, definição canônica de sycophancy
- [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-03|Exercise 03 (N3)]] — sycophancy como viés estrutural

### 9.6 Análises

- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Agent Focus Problems Analysis]] — extração de conhecimento com silent failure quantification
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]] — failure pattern #3 e decision rule
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]] — Manual Brake e Owner-of-No

---

## 10. Status de Implementação

**Wave 1 — Concluída (2026-06-19)**

| Componente | Status | Evidência |
|-----------|--------|-----------|
| C1 — `devils-advocate` skill | ✅ Implementado | `.opencode/skills/devils-advocate/SKILL.md` (117 linhas, harness bootstrapped) |
| C2 — Regra "Prefira Correção sobre Acordo" | ✅ Implementado | `AGENTS.md:133-141` |
| C3 — Anti-Sycophancy Directive nos 5 agentes | ✅ Implementado | `review-work/SKILL.md` — 5 ocorrências de `## Anti-Sycophancy Directive` |
| C4 — Diversificação de modelos | ✅ Implementado | `oh-my-openagent.json`: `review-goal-verifier` (GPT-5.5), `review-security-auditor` (Claude Opus 4.7), `momus` → Claude, `family_diversity` declarativo |

**Review pós-implementação**: 5 agentes paralelos, **PASS** unânime. 10/10 QA checks.

**Known Limitations**:
- `family_diversity` é declarativo — runtime enforcement pendente Onda 3
- Agent 3 (Code Reviewer) do review-work ainda usa Oracle/GLM — por design do escopo
- Harness do devils-advocate: contract 5/6, modules/integration deferred Onda 2

**Próximo passo**: Onda 2 — Generator-Evaluator loop, superfícies seladas, premise validation.

**Plano**: `.omo/plans/anti-sycophancy-wave1.md`

---

*Created: 2026-06-19 | From: análise cross-skill + cross-vault + literatura externa | Status: Wave 1 concluída
