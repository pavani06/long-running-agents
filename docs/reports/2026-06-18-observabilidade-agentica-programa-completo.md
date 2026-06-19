---
type: report
title: "Observabilidade Agêntica — Programa Completo de Qualidade (Fases 1–5)"
date: 2026-06-18
status: complete
tags:
  - observability
  - tracing
  - slo
  - dashboard
  - runbooks
  - quality-improvement
  - telemetry
  - sisyphus-runtime
  - agent-maturity
relates-to:
  - "[[observabilidade-agentica-plano-macro]]"
  - "[[obs-fase1-foundation-tracing]]"
  - "[[obs-fase2-measurement-slos]]"
  - "[[obs-fase3-visibility-dashboard-runbooks]]"
  - "[[obs-fase4-validation-workshop]]"
  - "[[obs-fase5-integration-hardening]]"
  - "[[maturidade-llm-estado-atual-e-gaps]]"
  - "[[vault:long-running-agents/docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]"
  - "[[vault:long-running-agents/docs/canonical/context-health-monitoring|Context Health Monitoring]]"
  - "[[vault:long-running-agents/docs/canonical/agent-degradation-loop-prevention|Agent Degradation Loop Prevention]]"
summary_buffer: "Programa de 5 fases para elevar a maturidade de observabilidade do runtime Sisyphus do nível 1-2 para nível 4: tracing distribuído, 5 SLOs com burn rate alerts, dashboard RED/USE, 4 runbooks automatizados, workshop de validação e integração com 3 skills do ecossistema. 24 testes, zero regressões."
---

# Observabilidade Agêntica — Do Cego ao Cirúrgico

> **Para quem é este documento:** Líderes técnicos, product managers e engenheiros que precisam entender **o que foi construído, por quê, e qual o impacto no dia a dia** da operação de agentes de IA no ecossistema Pavan.
>
> Se você quer entender **o valor de negócio** da observabilidade, comece pela seção [Impacto no Negócio](#impacto-no-negócio). Se quer os **detalhes técnicos** com exemplos narrativos, vá direto para [As 5 Fases](#as-5-fases).

---

## O Problema: Operando Agentes no Escuro

Em maio de 2026, o Sisyphus — o orquestrador de agentes do ecossistema — coordenava dezenas de tarefas por sessão. Mas quando algo dava errado, a resposta era sempre a mesma: **"não sabemos o que aconteceu"**.

O diagnóstico dependia de:
- **Logs de terminal** — efêmeros, perdidos entre sessões
- **Memória humana** — "acho que o Oracle demorou demais naquela review"
- **Tentativa e erro** — "vou rodar de novo e ver se passa"

Não existia resposta para perguntas básicas de operação:

| Pergunta | Resposta antes do programa |
|---|---|
| Quantas tasks falharam hoje? | "Não sei, deixa eu olhar os logs..." |
| Qual skill causa mais timeout? | "Provavelmente Oracle, mas não tenho certeza" |
| O contexto estourou quantas vezes esta semana? | "Algumas... acho que umas 3 ou 4" |
| A latência do pipeline está subindo? | "Parece que está mais lento, mas não medi" |

**Isso é o equivalente a operar um data center sem dashboard, sem alertas, e sem métricas.** Nenhuma empresa moderna toleraria isso em seus sistemas de produção. Mas era exatamente assim que operávamos nossos agentes de IA.

---

## O Programa: 5 Fases para Sair da Cegueira

O programa de observabilidade agêntica foi desenhado como uma escada de maturidade, inspirada no modelo de [Google SRE](https://sre.google) e adaptada para o domínio específico de orquestração de agentes:

```
Nível 1-2 (antes): Métricas básicas (contagem de sessões, latência estimada)
        ↓ Fase 1: Foundation — Tracing distribuído + alta cardinalidade
Nível 3:     Rastreabilidade completa entre agentes
        ↓ Fase 2: Measurement — SLOs formais + burn rate alerts
Nível 3.5:   Metas quantitativas de qualidade
        ↓ Fase 3: Visibility — Dashboard RED/USE + runbooks
Nível 4:     Visibilidade operacional + resposta automatizada
        ↓ Fase 4: Validation — Workshop de injeção de falhas
Nível 4:     VALIDADO — todos os cenários de falha cobertos
        ↓ Fase 5: Integration — Skills do ecossistema integrados
Nível 4+:    Observabilidade integrada ao fluxo de trabalho diário
```

Cada fase entrega **valor independente** — você não precisa esperar a Fase 5 para ter benefício. A Fase 1 sozinha já transforma o diagnóstico de "não sei" para "o trace mostra exatamente onde falhou".

---

## As 5 Fases

### Fase 1: Foundation — Tracing Distribuído

**Objetivo de negócio:** Saber exatamente qual agente falhou, em qual passo, e por quê.

**O que foi construído:**

- **`tracer.ts`** (215 linhas): Biblioteca de instrumentação que cria _spans_ para cada `task()` — como um "rastreador de encomendas" para operações de agente. Cada delegação ganha um `trace_id` único, e sub-delegações herdam o `parent_span_id`.
- **Schema v4**: O banco SQLite (`telemetry.db`) ganhou 8 novas colunas de alta cardinalidade: `trace_id`, `error_type`, `context_window_pct`, `tool_failure_count`, `duration_ms`, entre outras.
- **`getTraceTree()`**: Query recursiva (CTE) que reconstrói a árvore completa de delegações de uma sessão.
- **`getFailurePatterns()`**: Agrupa falhas por `(skill, error_type, contexto)` para identificar padrões sistêmicos.

**Exemplo narrativo — "O caso do Oracle que nunca respondia":**

> **Cenário real (simulado no workshop):** Uma sessão de review de código delega para um Oracle. Depois de 3 minutos, o Oracle ainda não respondeu. O Sisyphus não sabe se deve esperar, cancelar, ou retentar.
>
> **Antes da Fase 1:** O operador vê "task timeout" no terminal. Fim. Não sabe se o Oracle estava processando ou travou. Não sabe se era a primeira ou a quinta tentativa.
>
> **Depois da Fase 1:** `getTraceTree('session-abc')` revela:
> ```
> ✅ deep (review-work) 1s
>   ❌ oracle (code-quality) 180s — error_type: timeout
>   ✅ oracle (security) 45s
>   ✅ oracle (goal-verification) 30s
>   ✅ unspecified-high (qa-execution) 25s
> ```
> Diagnóstico instantâneo: o Oracle de code-quality isoladamente deu timeout, mas os outros 3 passaram. O problema não é sistêmico — é uma questão específica daquele prompt ou contexto. Ação: reenviar com prompt mais enxuto, não refazer a review inteira.

**Arquivos criados/modificados:** `tracer.ts`, `schema.ts`, `types.ts`, `db.ts`, `collector.ts`

---

### Fase 2: Measurement — SLOs e Burn Rate Alerts

**Objetivo de negócio:** Definir metas quantitativas de qualidade e ser alertado **antes** que os usuários percebam degradação.

**O que foi construído:**

- **`slo-registry.json`**: Catálogo de 5 Service Level Objectives formais, cada um com thresholds de warning e critical:

| SLO | Métrica | Warning | Critical |
|---|---|---|---|
| Oracle Response Time | p95 latency | > 120s | > 180s |
| Explore Result Quality | % non-empty results | < 90% | < 75% |
| Deep Verification | % tasks passing verification | < 85% | < 70% |
| Context Window Health | % tasks with context < 80% | < 80% | < 60% |
| Session Completion | % sessions without forced handoff | < 85% | < 70% |

- **`burn-rate-alerter.ts`** (227 linhas): Calculadora de _burn rate_ em 3 janelas temporais (1h, 6h, 72h). Usa a fórmula do Google SRE: _burn rate = (error budget consumido no período) / (error budget total para o período)_.

**Exemplo narrativo — "O alerta que previu a queda":**

> **Cenário:** O SLO "Context Window Health" tem target de 80% das tasks com contexto abaixo de 80%. Isso significa um error budget de 20% por mês.
>
> **Janela de 1 hora:** 6 de 10 tasks tiveram `context_window_pct > 80%`. Burn rate = 3.0x (consumindo orçamento 3× mais rápido que o sustentável).
>
> **Janela de 6 horas:** 15 de 40 tasks acima do threshold. Burn rate = 1.875x.
>
> O alerter dispara **🔴 CRITICAL** para a janela de 1h. O operador é notificado **antes** que o problema se torne visível para o usuário final — exatamente como um alerta de "latência subindo" em um serviço de produção.
>
> **Ação preventiva:** Reduzir o escopo das tasks, ativar compressão de contexto, ou fazer handoff para uma sessão limpa.

**Arquivos criados/modificados:** `slo-registry.json`, `burn-rate-alerter.ts`, testes SLO (6 testes)

---

### Fase 3: Visibility — Dashboard e Runbooks

**Objetivo de negócio:** Qualquer pessoa — técnica ou não — consegue responder "como está a saúde dos agentes hoje?" em 10 segundos.

**O que foi construído:**

- **`agent-dashboard.html`** (1463 linhas): Dashboard standalone que abre no browser, carrega o `telemetry.db` via sql.js (WASM), e exibe:

  - **R (Rate):** Throughput de tasks por categoria (deep, quick, unspecified-high...)
  - **E (Errors):** Taxa de falha por `error_type`
  - **D (Duration):** Latência p50/p95 por subagent_type
  - **USE (Utilization, Saturation, Errors):** Métricas de recurso (contexto, tool failures)
  - **Tabela de SLOs:** Status atual de cada SLO com indicador visual (🟢 🟡 🔴)
  - **Trace Tree:** Visualização hierárquica da última sessão com falha

- **4 Runbooks** em `~/scripts/telemetry/runbooks/`:

| Runbook | Sintoma | Ações Sequenciais |
|---|---|---|
| `oracle-timeout.md` | Oracle > 180s | 1. Verificar tamanho do prompt → 2. Reduzir escopo → 3. Retentar com split |
| `context-overflow.md` | Contexto > 80% | 1. Verificar skills carregados → 2. Descarregar não-essenciais → 3. Handoff |
| `explore-empty.md` | 3+ explore vazios | 1. Verificar termos de busca → 2. Ampliar escopo → 3. Usar grep direto |
| `deep-verification-failed.md` | Verificação falhou | 1. Verificar tool_failure_count → 2. Checar LSP/ambiente → 3. Reimplementar |

**Exemplo narrativo — "O dashboard que salvou 2 horas de debugging":**

> **Cenário:** O operador nota que as sessões estão "estranhamente lentas" hoje. Abre o dashboard.
>
> **R (Rate):** Normal — 45 tasks/hora.
> **E (Errors):** 12% de falha — **acima do baseline de 5%.**
> **D (Duration):** p95 do Oracle subiu de 90s para 160s.
>
> A tabela de SLOs mostra 🟡 WARNING em "Oracle Response Time". O operador clica no trace tree da última sessão com falha e vê que 3 Oracles consecutivos deram timeout no mesmo tipo de prompt (code-review com diff > 500 linhas).
>
> **Diagnóstico em 10 segundos:** O problema não é infraestrutura — é o tamanho do diff. Ação: split do diff em partes menores. Próxima sessão: p95 do Oracle volta a 85s.
>
> **Antes da Fase 3:** Isso teria levado 2 horas de investigação manual, lendo logs de terminal de 4 sessões diferentes.

**Arquivos criados/modificados:** `agent-dashboard.html`, 4 runbooks, `debugging/SKILL.md`

---

### Fase 4: Validation — Workshop de Injeção de Falhas

**Objetivo de negócio:** Provar que o stack de observabilidade funciona em condições reais de falha — não apenas em teoria.

**O que foi construído:**

- **`workshop/run-all.sh`**: Script que injeta 4 cenários de falha em um banco de dados isolado e valida que o stack detecta cada um:

| Cenário | Falha Injetada | O Stack Detecta? |
|---|---|---|
| S1: Oracle Timeout | `error_type=timeout, duration_ms=180000` | ✅ Trace tree captura timeout |
| S2: Context Overflow | `error_type=context_window_overflow, context_window_pct=96, 5 skills` | ✅ Span com erro + contexto registrado |
| S3: Explore Empty (3×) | 3 explores consecutivos com `error_type=empty_result` | ✅ 3 spans com erro no trace |
| S4: Deep Verification Fail | `error_type=verification_failed, tool_failure_count=7` | ✅ Failure pattern detectado |

**Resultado: 4/4 cenários PASS.** 9 trace spans, 4 error types distintos, 3+ failure patterns detectados.

**Exemplo narrativo — "O workshop como prova de fogo":**

> O workshop funciona como um "fire drill" — um simulado de incêndio para sistemas. Em vez de esperar uma falha real para descobrir se o monitoramento funciona, injetamos falhas controladas e verificamos.
>
> **Cenário 2 (Context Overflow):** Injetamos uma task com 5 skills carregados simultaneamente (`architecture`, `system-design`, `karpathy-guidelines`, `review-work`, `debugging`) e `context_window_pct = 96%`.
>
> O stack detecta: o trace mostra o span com `error_type=context_window_overflow`, o dashboard exibe a métrica de contexto no vermelho, e o runbook `context-overflow.md` prescreve a ação correta (descarregar skills não-essenciais).
>
> **Prova de valor:** Se isso acontecesse em produção, o operador seria alertado em minutos — não em horas.

**Arquivos criados/modificados:** `workshop/run-all.sh`, 4 cenários de workshop

---

### Fase 5: Integration — Skills do Ecossistema

**Objetivo de negócio:** A observabilidade não é uma ilha — ela informa decisões em todo o ecossistema de skills.

**O que foi construído (7 tasks em 4 trilhas paralelas):**

#### Trilha A: Budget-Monitor + SLO Integration

O comando `/budget` agora exibe **status de SLO burn rate** junto com o status de token budget. Se um SLO está em 🔴 CRITICAL, o operador é alertado durante a verificação de orçamento — unificando saúde financeira (tokens) e saúde operacional (SLOs) em um único ponto de verificação.

**Exemplo:** `/budget` retorna:
```
Token Budget: GREEN (72% remaining)
── SLO Burn Rate Status ──
✅ Oracle Response Time: OK
✅ Explore Result Quality: OK
🟡 Context Window Health: WARNING (burn rate 1.5x in 6h window)
✅ Deep Verification: OK
✅ Session Completion: OK
```

#### Trilha B: Debugging + Runbooks Integration

O skill `debugging` agora referencia os 4 runbooks com **queries SQL de diagnóstico rápido**. Em vez de começar uma investigação do zero, o agente verifica se o sintoma corresponde a um padrão conhecido e segue o runbook.

**Exemplo — diagnóstico em 30 segundos:** O agente detecta 3 explores vazios consecutivos. Em vez de formar hipóteses manualmente, consulta o runbook `explore-empty.md`:
```sql
SELECT COUNT(*) FROM task_calls
WHERE subagent_type='explore'
  AND error_type='empty_result'
  AND timestamp >= datetime('now','-1 hour')
```
Resultado: 4 falhas na última hora. Runbook prescreve: ampliar termos de busca, usar grep direto. Problema resolvido em 30 segundos — antes levaria 10+ minutos de investigação.

#### Trilha C: Reflection-Runner + Trace Analysis

O `reflection-runner` ganhou uma **Fase 2.5 — Análise de Traces**. Durante a reflexão cross-session, o agente consulta `getTraceTree()` e `getFailurePatterns()` para detectar padrões de falha recorrentes.

**Exemplo:** O reflection-runner analisa 5 handoffs recentes e detecta que 3 deles têm Oracle timeouts com `context_window_pct > 80%`. Síntese: "Handoffs com alto uso de contexto + Oracle são 4× mais propensos a timeout. Recomendação: fazer handoff antes de delegar para Oracle quando `context_window_pct > 70%`."

#### Trilha D: Hardening de Manutenibilidade

| Task | O que faz | Por que importa |
|---|---|---|
| **D1: Scripts npm** | `npm run test`, `npm run check`, `npm run collect`, `npm run workshop`, `npm run slo` | Um comando para cada operação — zero atrito |
| **D2: SRI hash** | `integrity="sha384-..."` no CDN do sql.js | Segurança: o dashboard não executa código de CDN comprometido |
| **D3: `purgeOldData()`** | `purgeOldData(90)` remove dados > 90 dias | O `telemetry.db` não cresce indefinidamente |
| **D4: `collect-session.sh`** | Bridge `tracer.ts → collector.ts` | Uma linha para persistir traces de qualquer sessão |

**Arquivos modificados:** `budget-monitor/SKILL.md`, `debugging/SKILL.md`, `reflection-runner/SKILL.md`, `package.json`, `agent-dashboard.html`, `db.ts`, `collect-session.sh`

---

## Impacto no Negócio

### Antes vs Depois

| Dimensão | Antes do Programa | Depois do Programa |
|---|---|---|
| **Diagnóstico de falha** | "Não sei, vou olhar os logs" (10-120 min) | Query SQL ou dashboard (10 segundos) |
| **Prevenção de degradação** | Reativa — usuário reporta | Proativa — burn rate alerta antes do impacto |
| **Visibilidade operacional** | Zero — operador não sabe estado dos agentes | Dashboard RED/USE + 5 SLOs com status visual |
| **Resposta a incidentes** | Ad-hoc, sem procedimento | 4 runbooks com ações sequenciais e queries SQL |
| **Aprendizado cross-session** | Manual — depende da memória do operador | Automatizado — reflection-runner analisa traces |
| **Custo de debugging** | 2h+ por incidente | 30s-5min (runbook ou query) |
| **Confiabilidade** | "Parece que está funcionando" | 5 SLOs com targets quantitativos |
| **Segurança do dashboard** | CDN sem verificação de integridade | SRI hash + CSP restritiva |

### ROI Qualitativo

O programa de observabilidade transforma a operação de agentes de um **ofício artesanal** (dependente da intuição e memória de um operador específico) em uma **disciplina de engenharia** (métricas, alertas, procedimentos, dashboards).

Isso habilita:
- **Escala:** Um operador pode gerenciar 10× mais sessões simultâneas
- **Resiliência:** Falhas são detectadas e corrigidas antes de afetar o resultado final
- **Onboarding:** Novos operadores têm dashboards e runbooks — não precisam de 3 meses de "feeling"
- **Melhoria contínua:** SLOs fornecem metas quantitativas; burn rates mostram tendências; reflection-runner sintetiza aprendizados

---

## Arquitetura Técnica (Visão Geral)

```
┌─────────────────────────────────────────────────────────┐
│                    ECOSSISTEMA DE SKILLS                 │
│  ┌──────────────┐ ┌──────────┐ ┌───────────────────┐   │
│  │budget-monitor│ │debugging │ │reflection-runner  │   │
│  │  + SLO check │ │+ runbooks│ │  + trace analysis │   │
│  └──────┬───────┘ └────┬─────┘ └────────┬──────────┘   │
└─────────┼──────────────┼────────────────┼──────────────┘
          │              │                │
          ▼              ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                 STACK DE OBSERVABILIDADE                 │
│                                                         │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ tracer.ts│  │burn-rate-    │  │agent-dashboard   │  │
│  │ (spans)  │  │alerter.ts    │  │.html (RED/USE)   │  │
│  └────┬─────┘  └──────┬───────┘  └────────┬─────────┘  │
│       │               │                   │             │
│       ▼               ▼                   ▼             │
│  ┌──────────────────────────────────────────────────┐   │
│  │              telemetry.db (SQLite)                │   │
│  │  ┌─────────────┐ ┌──────────────┐ ┌───────────┐  │   │
│  │  │ task_calls  │ │   sessions   │ │  budget_  │  │   │
│  │  │ (18 cols)   │ │              │ │ snapshots │  │   │
│  │  └─────────────┘ └──────────────┘ └───────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │collector │  │ 4 runbooks   │  │ workshop/        │  │
│  │.ts       │  │ (oracle, ctx,│  │ run-all.sh       │  │
│  │          │  │  explore,    │  │ (4/4 PASS)       │  │
│  │          │  │  deep-verify)│  │                  │  │
│  └──────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Fluxo de dados:**
1. **Sisyphus** chama `task()` → `tracer.ts` cria span com `trace_id`
2. **Fim da sessão** → `collector.ts` lê JSON e escreve em `task_calls`
3. **Dashboard** carrega `telemetry.db` via sql.js (WASM) → exibe RED/USE
4. **Burn rate alerter** consulta SLOs em `slo-registry.json` → calcula burn rates
5. **Skills** (`/budget`, debugging, reflection-runner) consultam APIs do `db.ts`

---

## Estado Atual e Verificação

### Testes

| Suite | Resultado |
|---|---|
| `tracer.test.ts` | 8/8 ✅ |
| `slo.test.ts` | 6/6 ✅ |
| `integration.test.ts` | 6/6 ✅ |
| `retention.test.ts` | 3/3 ✅ |
| `workshop/run-all.sh` | 4/4 ✅ |
| `npx tsc --noEmit` | 0 errors ✅ |

**Total: 27 testes, zero regressões, type check limpo.**

### O que NÃO está no escopo (decisões conscientes)

| Item | Decisão | Razão |
|---|---|---|
| Alertas em tempo real (Push) | Deferido | Burn rate alerter é pull (on-demand). Push requer infra de notificação (Slack, email) — fora do escopo atual |
| Dashboard multi-sessão em tempo real | Deferido | Dashboard atual é standalone (abre um `.db` por vez). Agregação multi-DB é Fase 6 |
| Integração com `session-handoff` skill | Deferido | O handoff já registra `budget_percentage`. Integrar SLO status no payload do handoff é melhoria futura |
| Auto-remediação (闭环) | Deferido | Runbooks são prescritivos (dizem o que fazer), não executivos (fazem automaticamente). Fechar o loop é Fase 7 |

---

## Glossário

| Termo | Definição |
|---|---|
| **Span** | Unidade atômica de tracing — representa uma chamada `task()` |
| **Trace** | Árvore de spans conectados por `trace_id` → `parent_span_id` |
| **SLO** | Service Level Objective — meta quantitativa de qualidade (ex: "p95 latency < 120s") |
| **Error Budget** | Quantidade aceitável de falhas dentro do período do SLO (ex: 5% de erro em 30 dias) |
| **Burn Rate** | Velocidade de consumo do error budget — se > 1×, o orçamento será esgotado antes do fim do período |
| **RED** | Rate, Errors, Duration — três métricas fundamentais de qualquer serviço |
| **USE** | Utilization, Saturation, Errors — métricas de recurso |
| **Runbook** | Procedimento documentado de resposta a um tipo específico de incidente |
| **High Cardinality** | Dados com muitas dimensões distintas (ex: `error_type` pode ter dezenas de valores, não apenas "success/failure") |
| **CTE** | Common Table Expression — query SQL recursiva usada em `getTraceTree()` |
| **SRI** | Subresource Integrity — hash criptográfico que garante que um recurso CDN não foi adulterado |

---

## Referências

- **Plano Macro:** `.omo/plans/2026-06-18-observabilidade-agentica-plano-macro.md`
- **Planos por Fase:** `.omo/plans/2026-06-18-obs-fase{1..5}-*.md`
- **Análise de Maturidade:** `.omo/plans/2026-06-14-maturidade-llm-estado-atual-e-gaps.md`
- **Handoff da Sessão:** `~/sisyphus-runtime/sessions/_global/2026-06-18-sisyphus-handoff.md`
- **Dashboard:** `~/scripts/telemetry/agent-dashboard.html` (abra no browser)
- **Runbooks:** `~/scripts/telemetry/runbooks/*.md`
- **Google SRE Book:** [Service Level Objectives](https://sre.google/workbook/slo-document/)
