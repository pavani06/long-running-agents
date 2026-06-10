---
title: "Solução de Referência — Exercício 3: Plano de Evolução do Harness KODA"
type: curriculum-solution
nivel: 3
aliases: []
tags: [curriculo-conteudo, nivel-3, solucao]
last_updated: 2026-06-10
---
# 📝 Solução de Referência — Exercício 3: Plano de Evolução do Harness KODA
## Nível 3 — Arquitetura Avançada

**Importante:** Esta é UMA solução válida entre várias possíveis. Seu plano pode diferir em ordem de fases ou decisões de simplificação vs remoção, desde que justificado com métricas e changelog. Use esta solução para comparar e entender racionais alternativos.

---

## Parte 1: Análise de Impacto

### Tabela de Decisão Preenchida

| # | Componente | Capacidade do Changelog Que Impacta | Decisão |
|---|-----------|--------------------------------------|---------|
| 1 | Context Loader | Atenção >99% @ 300K; system prompt priorizado automaticamente | ➡️ SIMPLIFICA |
| 2 | Dedup Layer | Janela 500K (2.5x maior); menos pressão por tokens | ⬇️ REMOVE |
| 3 | Priority Extractor | System prompt priorizado automaticamente — tags desnecessárias | ⬇️ REMOVE |
| 4 | Budget Guard | Janela 500K — conversas típicas = 10% da janela | ⬇️ REMOVE |
| 5 | Planner Agent | Self-correction 3x + raciocínio nativo | ➡️ SIMPLIFICA |
| 6 | Generator Agent | Nenhuma — componente core | ⬆️ MANTÉM |
| 7 | Evaluator Agent | Self-correction 3x — mas sycophancy é estrutural | ⬆️ MANTÉM (INVARIANTE) |
| 8 | Format Validator | JSON mode nativo com schema validation (<0.01% erro) | ⬇️ REMOVE |
| 9 | Constraint Checker | Self-correction 3x + grounding +98% + instruction following 98.7% | ➡️ SIMPLIFICA (consolidar no Evaluator) |
| 10 | Fallback Handler | Latência -35%; taxa de falha <0.1% | ➡️ SIMPLIFICA |
| 11 | History Compactor | Janela 500K; atenção >99% @ 300K | ➡️ SIMPLIFICA |

---

## Parte 2: Plano de Evolução em 3 Fases

### FASE 1 — "Low-Hanging Fruit" (Risco Baixo)
**Duração:** 4 semanas

**Objetivo:** Remover componentes com ROI mais baixo e risco comprovadamente mínimo. Gerar confiança no time e dados para as fases seguintes.

**Componentes (3):**
1. **Budget Guard — REMOVE** — 0 acionamentos. Feature flag: `harness_remove_budget_guard`. Shadow test 7 dias. Canary 5%→25%→100%. Rollback < 1h.
2. **Dedup Layer — REMOVE** — ROI 0.4x. Feature flag: `harness_remove_dedup_layer`. Shadow test 7 dias validando que tokens/mês não aumentam > 5%.
3. **Fallback Handler — SIMPLIFICA** — Reduzir 3→2 estratégias (remover "alternativa", manter retry + humano). Feature flag: `harness_simplify_fallback`. Shadow test 7 dias.

**Impacto:**
- Componentes: 11 → 9 (-2 removidos, -1 simplificado)
- Latência: 1.8s → 1.5s (-300ms)
- Tokens/mês: 61.7M → 58.0M (-3.7M)
- Custo API: R$ 9.240 → R$ 8.720 (-R$ 520/mês)
- Manutenção: 18h → 15h (-3h/mês)

**Riscos:** Baixo. Budget Guard nunca disparou. Dedup Layer tem ROI 0.4x. Fallback mantém proteção essencial com 2 estratégias.

**Gate:** 14 dias sem incidentes + time aprova em architectural review.

---

### FASE 2 — "Simplificações Guiadas por Changelog" (Risco Médio)
**Duração:** 4 semanas

**Objetivo:** Remover componentes cuja premissa original é coberta pelo changelog, e iniciar simplificação do Context Loader.

**Componentes (3):**
1. **Format Validator — REMOVE** — JSON mode nativo cobre a premissa (<0.01% erro). Feature flag: `harness_remove_format_validator`. Shadow test 14 dias monitorando erros de parsing.
2. **Priority Extractor — REMOVE** — System prompt priorizado automaticamente. Feature flag: `harness_remove_priority_extractor`. Shadow test 7 dias validando que constraints são respeitadas sem tags.
3. **Context Loader — SIMPLIFICA (Ondas 1 e 2)** — Onda 1: remover injeção dupla (-500 tokens/turno). Onda 2: recarregar só no início da conversa (-400 tokens/turno). Feature flag: `harness_simplify_context_loader`.

**Impacto:**
- Componentes: 9 → 7 (-2 removidos, -1 simplificado)
- Latência: 1.5s → 1.1s (-400ms)
- Tokens/mês: 58.0M → 51.5M (-6.5M)
- Custo API: R$ 8.720 → R$ 7.730 (-R$ 990/mês)
- Manutenção: 15h → 12h (-3h/mês)

**Riscos:** Médio. JSON mode pode não funcionar perfeitamente no domínio KODA — shadow test de 14 dias é essencial. Priority Extractor: validar que constraints de saúde (alergias) continuam protegidas.

**Gate:** 14 dias sem incidentes + acurácia ≥ 97%.

---

### FASE 3 — "Consolidações Estruturais" (Risco Médio-Alto)
**Duração:** 4 semanas

**Objetivo:** Consolidar componentes redundantes, otimizar thresholds, e alcançar o target de 6 componentes essenciais.

**Componentes (3):**
1. **Constraint Checker — CONSOLIDA no Evaluator** — O Evaluator absorve 100% das verificações de constraints. Feature flag: `harness_consolidate_constraint_checker`. Shadow test 14 dias.
2. **Planner Agent — SIMPLIFICA (condicional)** — Planner só aciona em jornadas complexas. Estimativa: 35%→15% de acionamento. Feature flag: `harness_simplify_planner`.
3. **History Compactor — SIMPLIFICA (threshold)** — Threshold de 2h→4h. Estimativa: 12%→3% de acionamento. Feature flag: `harness_simplify_compactor`.

**Impacto:**
- Componentes: 7 → 6 (-1 consolidado, -2 simplificados)
- Latência: 1.1s → 0.9s (-200ms)
- Tokens/mês: 51.5M → 46.0M (-5.5M)
- Custo API: R$ 7.730 → R$ 6.900 (-R$ 830/mês)
- Manutenção: 12h → 8h (-4h/mês)

**Impacto Total (após 3 fases):**
- Componentes: 11 → 6 (-45%)
- Latência: 1.8s → 0.9s (-50%)
- Tokens/mês: 61.7M → 46.0M (-25%)
- Custo API: R$ 9.240 → R$ 6.900 (-R$ 2.340/mês, -25%)
- Manutenção: 18h → 8h (-56%)

**Riscos:** Médio-Alto. Consolidação Constraint Checker → Evaluator é a mudança mais arriscada (constraints de saúde). Shadow test de 14 dias com bateria de regressão específica para cenários de alergia.

**Gate:** 14 dias sem incidentes + métricas de baseline documentadas + post-mortem positivo.

---

## Parte 3: Critérios de Validação por Fase

**FASE 1:**
- [x] Shadow test Budget Guard: 7 dias, delta acurácia = 0.0%
- [x] Shadow test Dedup Layer: tokens/mês sem aumento > 5%
- [x] Shadow test Fallback: taxa de sucesso mantida com 2 estratégias
- [x] Canary deploy 5%→25%→100% sem incidentes
- [x] ADRs escritos para Budget Guard e Dedup Layer

**FASE 2:**
- [x] Shadow test Format Validator: 14 dias, taxa erro parsing < 0.05%
- [x] Shadow test Priority Extractor: acurácia em constraints mantida
- [x] Shadow test Context Loader (Ondas 1+2): delta acurácia < 0.5%
- [x] 14 dias observação sem regressão

**FASE 3:**
- [x] Shadow test consolidação Constraint Checker: acurácia mantida, latência Evaluator < +100ms
- [x] Shadow test Planner condicional: sem aumento de revisões por conversa
- [x] Shadow test Compactor threshold: sem perda de contexto 2h–4h
- [x] Métricas baseline pós-evolução documentadas

---

## Parte 4: Tabela Comparativa

### Comparação Agregada

| Métrica | Antes (Abr 2026) | Após Fase 3 (Target) | Redução |
|---------|--------------------|----------------------|---------|
| Componentes ativos | 11 | 6 | -45% |
| Latência média/turno | 1.8s | 0.9s | -50% |
| Tokens/mês (milhões) | 61.7M | 46.0M | -25% |
| Custo API mensal | R$ 9.240 | R$ 6.900 | -25% |
| Horas manutenção/mês | 18h | 8h | -56% |
| Arquivos de estado | 7 | 4 | -43% |
| Tempo onboarding | 3 semanas | 1.5 semanas | -50% |
| Acurácia | 97.1% | 97.0% | -0.1% (não significativo) |

### Comparação do Pipeline por Turno

| Pipeline | Antes (11 comp.) | Depois (6 comp.) | Ganho |
|----------|------------------|------------------|-------|
| Pré-processamento | 900ms (4 comp.) | 200ms (State Loader, 1ª msg) | -700ms |
| Core Agents | 2600ms (3 comp.) | 2100ms (Gen + Eval unificado, Planner cond.) | -500ms |
| Pós-processamento | 600ms (3 comp.) | 50ms (Fallback simpl., cond.) | -550ms |
| History & State | 300ms cond. + 7 files | 300ms cond. (3% casos) + 4 files | -3 files |
| **Total** | **~4000ms** | **~1500ms** | **-62%** |

### Estratégias de Coordenação

| Dimensão | Antes (11 comp.) | Depois (6 comp.) | Ganho |
|----------|------------------|------------------|-------|
| Coordenação | 7 arquivos JSON/turno | 4 arquivos JSON/turno | -43% I/O |
| Validação output | 3 stages sequenciais | 1 stage unificado | -2 stages |
| Gestão contexto | 4 componentes | 1 componente (Compactor) | -3 componentes |
| Planejamento | Sempre (35% conversas) | Condicional (15%) | -57% chamadas |
| Fallback | 3 estratégias | 2 estratégias | -1 code path |
| System prompts | ~2000 tokens | ~600 tokens | -70% |

---

## Parte 5: Invariantes e Análise de Riscos

### Tabela de Invariantes

| Invariante | Componente | Por Que É Permanente |
|------------|-----------|---------------------|
| Segurança do cliente | Evaluator Agent (verificação de alergias) | Alergias são proteção de vida — nenhum modelo elimina o risco |
| Compliance (LGPD) | State Persistence (rastreabilidade) | Exigência legal independente da qualidade do modelo |
| Decisões irreversíveis | Evaluator Agent (gate) | Cobrança e envio precisam de checkpoint de sistema |
| Fallback de disponibilidade | Fallback Handler (2 estratégias) | API pode ficar offline — proteção contra falha do SERVIÇO |
| Gatekeeper qualidade | Evaluator Agent | Sycophancy é estrutural em LLMs |
| Auditabilidade | State Persistence + Trace | Sem estado persistente, não há debug nem auditoria |

### Respostas

**1. Quais componentes você classificou como invariantes?**
Evaluator Agent, State Persistence, Fallback Handler (simplificado), Generator Agent. Estes 4 protegem contra riscos que transcendem a qualidade do modelo: viés estrutural, exigências legais, falhas de infraestrutura e a própria existência do sistema.

**2. Maior potencial de economia?**
Context Loader: 5.4M tokens/mês (R$ 810) + 450ms/turno. Simplificação em 3 ondas economiza ~80% disso. Planner Agent é o segundo: 8.2M tokens/mês (R$ 1.230). Torná-lo condicional economiza ~R$ 700/mês.

**3. Maior dano se removido incorretamente?**
Evaluator Agent. Sem ele: sycophancy → cliente recebe recomendação ruim → perda de confiança. Shadow test mostrou queda de 8% na acurácia. ROI 45x confirma.

**4. Ordem de reativação se downgrade?**
(1) Budget Guard — se janela < 100K. (2) Context Loader completo — se atenção degradar. (3) Format Validator — se JSON mode indisponível. (4) Priority Extractor — se instruction following < 95%.

**5. Plano de rollback se Fase 2 degradar acurácia?**
Minutos: desativar feature flags da Fase 2. Horas: analisar logs de shadow test para isolar causa. Dias: reativar seletivamente. Semanas: ajustar abordagem uma vez isolado o problema.

**6. Componente mantido mesmo com ROI baixo?**
Fallback Handler (ROI 1.7x após simplificação). Embora marginal, fallback é invariante de disponibilidade. API offline sem fallback = perda de vendas. Simplificação (3→2 estratégias) melhora ROI mantendo proteção essencial.

---

*Solução de Referência — Exercício 3 | Nível 3 — Arquitetura Avançada | Maio 2026*
