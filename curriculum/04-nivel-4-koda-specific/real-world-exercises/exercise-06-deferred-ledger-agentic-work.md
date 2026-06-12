---
title: "Exercicio 6: Construir o Deferred Ledger de Divida Agente do KODA"
type: curriculum-exercise
nivel: 4
aliases: ["deferred ledger", "divida agentica", "skill debt KODA", "dependence debt", "carry debt", "ledger de divida"]
tags: [curriculo-conteudo, nivel-4, exercicio, debt-classification, risk-management, token-economics, skill-debt, dependence-debt, carry-debt, governance, financial-modeling]
relates-to: ["[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger Skill]]", "[[curriculum/04-nivel-4-koda-specific/05-harness-improvements|Harness Improvements]]"]
last_updated: 2026-06-11
---
# 📒 Exercicio 6: Construir o Deferred Ledger de Divida Agentica do KODA
## Nivel 4 -- KODA-Especifico

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avancado)
**Pre-requisito:** Ter lido `05-harness-improvements.md`, `docs/canonical/deferred-ledger-agentic-work.md`, `docs/canonical/explicit-token-budget-ledger.md`
**Objetivo:** Auditar o estado atual do KODA e classificar a divida agentica acumulada em tres categorias (skill, dependence, carry), produzindo um ledger com estimativas de exposicao e decisoes de mitigacao.

---

## 📖 Prologo: O Dia em Que o Preco dos Tokens Mudou

**Quinta-feira, 14h30. Sala de guerra do KODA.**

O CFO entrou com um email impresso. "A Anthropic anunciou o pricing do Claude Opus 5. Nao e mais preview gratuito. O preco de producao e 6x o que gastamos hoje em credits."

Silencio na sala.

O KODA processava 4.200 conversas por mes. Cada uma consumia em media 180 mil tokens. Com o novo preco, o custo mensal de inferencia saltaria de USD 1.200 para USD 7.200. E isso era so o custo operacional direto.

"Mas tem mais," o CFO continuou. "O problema nao e o custo de rodar. E o custo do que ja rodamos. Quantas features o KODA tem que foram construidas porque 'era barato'? Quantas dependem de prompts que so funcionam no Opus? Quantas precisam de manutencao que ninguem contabilizou?"

Foi ai que voce percebeu: o time nunca teve um **Deferred Ledger** -- um registro das dividas invisiveis que se acumularam enquanto construir era barato. Nao e um orcamento de tokens. E uma classificacao de passivo estrutural.

O Deferred Ledger tem tres categorias:

1. **Skill Debt** -- O julgamento nao exercitado nao sobrevive. Um time que passou trimestres sem tomar decisoes dificeis de build-or-dont-build perde a capacidade de toma-las quando o preco muda.
2. **Dependence Debt** -- Workflows construidos na premissa de que geracao e barata deixam de funcionar quando a geracao deixa de ser.
3. **Carry Debt** -- Software que foi barato de criar se torna inventario que precisa ser mantido, securitizado, compreendido e eventualmente reprecificado.

Seu trabalho hoje e auditar o estado real do KODA e construir esse ledger.

---

## 🎯 O Que Voce Precisa Fazer

Voce vai auditar o KODA como ele existe hoje e classificar a divida agentica em tres categorias, com estimativas de exposicao e decisoes de mitigacao.

### Contexto: O Estado Atual do KODA

O KODA foi construido ao longo de 8 meses de desenvolvimento agentico. Aqui esta o inventario das decisoes de build tomadas nesse periodo:

**Mes 1-2: Fundacao**
- Pipeline basico de conversa WhatsApp (Claude 3.5 Sonnet)
- Classificador de intencao baseado em regex (82% precisao)
- Integracao com catalogo de produtos (JSON estatico)
- Primeira versao do processador de pagamento (mock)

**Mes 3-4: Crescimento**
- Upgrade para Claude Opus 3 (prompts reescritos para o novo modelo)
- Generator/Evaluator para recomendacao de produtos
- 7 novos agentes no pipeline de customer journey
- Sistema de fallback para recomendacoes (3 niveis)
- Integracao real de pagamento com gateway externo

**Mes 5-6: Features Sob Demanda**
- "Ofertas relampago" -- recomendacoes com desconto baseadas em horario
- "Perguntas frequentes inteligentes" -- FAQ gerada por LLM a cada conversa
- "Resumo da conversa" enviado ao cliente apos cada interacao
- "Classificador de urgencia" para priorizar clientes premium
- Dashboard interno de metricas do agente (construido em um fim de semana)

**Mes 7-8: Maturidade e Divida**
- 14 features no total em producao
- 4 pessoas no time (2 engineers, 1 PM, 1 designer)
- 3 membros do time nunca tomaram uma decisao de "nao construir"
- Token budget mensal: 30M tokens (USD 450 em credits)
- Nenhum artefato tem dono de manutencao documentado
- Nenhum artefato tem data de revisao ou sunset
- O upgrade para Claude 4 foi adiado duas vezes por medo de reescrever prompts

---

## 📝 Entregaveis

### 1. Classificacao de Skill Debt

Para cada item abaixo, classifique o nivel de skill debt (Baixo / Medio / Alto) e escreva 1-2 frases de justificativa:

| Item de Skill Debt | Nivel | Justificativa |
|---|---|---|
| Capacidade do time de dizer "nao" a builds | [Baixo/Medio/Alto] | [justificativa] |
| Conhecimento de quanto custa REALMENTE cada feature (alem dos tokens) | | |
| Habilidade de precificar trabalho em "semanas de engenharia" em vez de "horas de agente" | | |
| Familiaridade com os prompts que o KODA usa em producao | | |
| Capacidade de migrar entre modelos (Claude 3 → 4) sem reescrever tudo | | |
| Documentacao de decisoes de build (quem aprovou, por que, com qual criterio de sucesso) | | |

### 2. Classificacao de Dependence Debt

Audite as 14 features do KODA e classifique-as por nivel de dependencia de modelo/tool:

| Categoria | Features | Risco de Repricing |
|---|---|---|
| **Dependencia Critica** (quebra se modelo mudar) | [liste as features] | [estimativa de custo se o preco 6x] |
| **Dependencia Alta** (degrada significativamente) | [liste as features] | [estimativa] |
| **Dependencia Media** (contorna com fallback) | [liste as features] | [estimativa] |
| **Dependencia Baixa** (logica deterministic) | [liste as features] | [estimativa] |

Para cada feature em Dependencia Critica, responda:
- O que exatamente depende do modelo que pode mudar?
- Existe um fallback deterministico ou de modelo mais barato?
- Quanto custaria reescrever esta feature para um modelo diferente?

### 3. Classificacao de Carry Debt

Para CADA UMA das 14 features, preencha:

| # | Feature | Tem usuario? (evidencia) | Tem dono de manutencao? | Custo mensal estimado de manutencao | Data de revisao? | Decisao |
|---|---|---|---|---|---|---|
| 1 | [nome] | [sim/nao/incerto + evidencia] | [nome ou "nenhum"] | [USD estimado] | [data ou "nenhuma"] | [keep/retire/archive/promote] |

As decisoes seguem o vocabulario do [[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]]:
- **Keep** -- artefato justificado, com dono e data de revisao.
- **Retire** -- nao justifica o carry cost. Remover com rollback plan.
- **Archive** -- nao esta em uso ativo mas tem valor historico ou de referencia. Mover para `archive/` com README.
- **Promote** -- de experimento para artefato de primeira classe, com dono, testes e documentacao.

### 4. Calculo de Exposicao

Com base nas tres categorias de divida, calcule a exposicao do KODA a um cenario de repricing (tokens 6x mais caros):

```
Custo operacional atual (tokens): USD 450/mes
Custo operacional com repricing 6x: USD _____/mes

Custo de reescrever features com dependence debt: USD _____ (estimado em horas de engenharia)
Custo de manter carry debt por mais 12 meses: USD _____ (estimado)
Custo de skill debt (tempo ate time recuperar julgamento): _____ semanas

Exposicao total no cenario de repricing: USD _____ (12 meses)
```

### 5. Plano de Mitigacao (3-5 acoes)

Com base no ledger, liste 3-5 acoes concretas para reduzir a exposicao do KODA antes que o repricing aconteca. Para cada acao:

| Prioridade | Acao | Categoria de divida atacada | Custo estimado | Reducao de exposicao | Prazo |
|---|---|---|---|---|---|
| 1 | [acao] | [skill/dependence/carry] | [USD/horas] | [% ou USD] | [semanas] |

### 6. Reflexao Final (2-3 paragrafos)

Responda:
- Qual categoria de divida (skill, dependence, carry) e a mais perigosa para o KODA hoje e por que?
- Se o time tivesse usado o Manual Brake desde o Mes 1, quantas das 14 features teriam sido classificadas como "parar" ou "experimento"?
- O que muda na sua percepcao de "custo" depois de construir este ledger?

---

## 🎯 Rubrica de Avaliacao

| Criterio | Peso | Insuficiente | Satisfatorio | Excelente |
|---|---|---|---|---|
| **Completude do inventario** | 25% | Audita menos de 50% das features ou ignora categorias de divida | Audita todas as 14 features nas tres categorias | Identifica divida que nao estava no inventario inicial (divida oculta) |
| **Precisao da classificacao** | 25% | Confunde skill debt com dependence debt ou carry debt | Classifica corretamente usando as definicoes do pattern | Identifica dividas que cruzam categorias e propoe tratamento hibrido |
| **Qualidade das decisoes de carry** | 20% | Decisoes arbitrarias (tudo "keep" ou tudo "retire") | Decisoes justificadas com tradeoffs visiveis | Decisoes consideram interdependencias entre features |
| **Realismo do calculo de exposicao** | 15% | Numeros irreais ou sem justificativa | Estimativas razoaveis com premissas declaradas | Range de cenarios (otimista, pessimista, provavel) com sensibilidades |
| **Plano de mitigacao** | 15% | Acoes genericas sem prioridade ou custo | Acoes especificas com estimativas | Acoes sequenciadas com dependencias e gatilhos de reavaliacao |

---

## 🔧 Habilidades Praticadas

- **Risk accounting** -- Classificar passivos estruturais que nao aparecem no P&L.
- **Carry cost modeling** -- Precificar o custo de manutencao de artefatos ao longo do tempo.
- **Dependency mapping** -- Identificar o que quebra quando o modelo ou tool subjacente muda.
- **Sunset decision-making** -- Tomar decisoes de keep/retire/archive/promote com dono e data.
- **Financial thinking for engineers** -- Conectar decisoes de build com exposicao financeira.

---

## 📚 Material de Referencia

- [[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]] -- Canonical doc com as tres categorias de divida.
- [[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]] -- Gate de revisao periodica de artefatos.
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] -- Ledger operacional que alimenta o deferred ledger.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] -- Ciclo BUILD/STABILIZE/SIMPLIFY/REMOVE.
- [[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger Skill]] -- Skill que mantem o deferred ledger.
- `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns.md` -- Pattern 6 (Deferred Ledger for Agentic Work) e Pattern 10 (Carry Debt Sunset Gate).

---
**Criado para o curriculo Long-Running Agents | v1.0 | Junho 2026**
