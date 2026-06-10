---
title: "Phase-Gated Token Health Monitor"
type: canonical
aliases: ["monitor de saude de tokens", "token health phases", "green yellow orange red"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]", "[[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]", "[[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
---

# Phase-Gated Token Health Monitor

**Type:** canonical
**Status:** active
**Source:** [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]] and [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]
**Classification:** Partial Coverage
**Precedence:** document-level 2, because active canonical docs outrank analyses in the repository precedence model [[docs/system-of-record|System of Record]]:14-21.

---

## Problem

Agentes long-running geralmente percebem pressao de tokens tarde demais: depois que a qualidade cai, o raciocinio enfraquece, as respostas encurtam ou o limite de contexto chega. A analise de token budgeting identifica esse problema diretamente no padrao extraido: agentes descobrem pressao de tokens apenas depois de degradacao ou limite de contexto [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:59-79.

A causa e que saude de contexto nao e apenas um numero estatico de tokens restantes. O modelo de budget divide a sessao em input, output, context window e burn rate [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:28-37. A fonte curricular tambem define burn rate como `(Input + Output) / Minutos de Conversa` e usa essa taxa para planejar compactacao e mudanca de estrategia [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:143-165. Portanto, uma sessao com muito contexto aparente ainda pode estar em risco se o consumo estiver acelerando [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:37.

## Solution

Defina um monitor de saude de tokens que rode em cada turno, iteracao de loop ou montagem de contexto. O monitor recebe percentual de budget restante, previsao de burn rate, sinal de aceleracao e a lista de acoes disponiveis; ele retorna uma fase `green`, `yellow`, `orange` ou `red`, uma acao deterministica e uma razao auditavel. O padrao extraido especifica esses inputs e outputs: percentual restante, burn-rate forecast, thresholds, contexto atual, acoes de compactacao ou handoff, fase de saude, acao recomendada e motivo de intervencao [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:63-71.

O objetivo nao e substituir o context builder. O objetivo e transformar token budgeting em um controle de runtime que informa quando o loop deve continuar, observar, resumir, comprimir, reduzir contexto ou iniciar nova sessao. A analise chama isso de loop threshold-driven em vez de resposta unica no fim da janela [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:39-49.

```text
+-------------------+      +-------------------+      +----------------------+
| Token budget      |      | Burn-rate         |      | Context/action       |
| ledger            |      | forecast          |      | inventory            |
| - remaining %     |      | - tokens/min      |      | - summarize          |
| - response buffer |      | - acceleration    |      | - compress           |
| - safety buffer   |      | - runway          |      | - handoff/new session|
+---------+---------+      +---------+---------+      +----------+-----------+
          |                          |                           |
          +--------------------------+---------------------------+
                                     |
                                     v
                    +--------------------------------+
                    | Phase-gated token monitor      |
                    | green/yellow/orange/red        |
                    +---------------+----------------+
                                    |
                                    v
                    +--------------------------------+
                    | Deterministic loop action      |
                    | continue/monitor/compact/handoff|
                    +--------------------------------+
```

## Phase Policy

Thresholds devem ser calibrados por modelo, produto e estrategia de contexto. Como default operacional, use os thresholds da fonte curricular como ponto de partida: mais de 60% restante e `GREEN`, mais de 40% e `YELLOW`, mais de 20% e `ORANGE`, e 20% ou menos como `RED` [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:577-603. Ajuste a fase para cima quando a aceleracao de burn rate indicar que o runway esta caindo mais rapido que o esperado, porque burn rate acelerado e listado como red flag que deve ativar compressao, remocao de historico antigo e preparacao de resumo [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-499.

| Phase | Condition | Deterministic action | Reason to log |
|---|---|---|---|
| `green` | Budget restante acima do threshold seguro e sem aceleracao relevante | `continue` | Budget e runway suficientes para o proximo passo |
| `yellow` | Budget declinando ou burn rate acima do baseline, mas runway ainda aceitavel | `monitor` | A sessao ainda pode continuar, mas o loop deve registrar tendencia |
| `orange` | Budget em faixa de risco ou aceleracao indica risco antes do proximo checkpoint | `summarize` ou `compress` | Ainda ha espaco para compactar com qualidade antes de pressao critica |
| `red` | Budget abaixo do limite critico, runway insuficiente ou comportamento degradado observado | `new_session`, `handoff` ou `force_terminate` | Continuar no contexto atual ameaca qualidade, continuidade ou confiabilidade |

O monitor deve reservar buffer de resposta e buffer de seguranca antes de calcular disponibilidade. A calculadora curricular reserva resposta e seguranca antes de calcular tokens disponiveis [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:445-459. A analise tambem registra que reservar output e obrigatorio porque o tamanho da resposta e desconhecido antes da geracao [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:121-125.

## Implementation Contract

O contrato minimo do monitor e:

| Field | Meaning |
|---|---|
| `remaining_budget_tokens` | Context window menos input acumulado, buffer de resposta e safety buffer |
| `remaining_budget_percent` | Percentual disponivel usado para comparar thresholds |
| `burn_rate_current` | Tokens por minuto, mensagem ou iteracao recente |
| `burn_rate_baseline` | Baseline calibrado para o workflow atual |
| `burn_rate_accelerating` | Boolean ou score que indica consumo subindo acima do esperado |
| `phase` | `green`, `yellow`, `orange` ou `red` |
| `action` | `continue`, `monitor`, `summarize`, `compress`, `new_session`, `handoff` ou `force_terminate` |
| `reason` | Frase curta com o threshold, runway ou sinal que disparou a fase |
| `context_action_target` | Bloco ou politica que a acao deve executar, como older history, summary buffer ou handoff payload |

A acao retornada deve ser executavel pelo loop, nao apenas registrada. [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] ja define pontos de intervencao para `break`, `summarize`, `LM-as-judge`, `human approval gate` e `force terminate` [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75. O monitor usa esses pontos como atuadores: `orange` aciona summarizacao ou compressao no context builder; `red` aciona handoff, nova sessao, gate humano ou terminacao forcada.

## Implementation in this repo

### What already exists

- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] ja separa `Prompt`, `Context Builder`, `Switch Statement` e `Loop`, e diz que o context builder monta historico, memoria, tool results e business state [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:31-63.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] ja da ao loop pontos de intervencao compativeis com as acoes do monitor: `break`, `summarize`, `LM-as-judge`, `human approval gate` e `force terminate` [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75.
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] ja define uma escada ordenada de classificacao, retry, fallback ou hold, escalacao humana, log de outcome e testes de rung [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:27-65.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] ja mapeia sinais de dor para o proximo investimento minimo de eval, incluindo falhas tardias de sessao ou contexto como gatilho para [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]] [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:40-51.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] ja define active context limitado por prompt estavel, head, tail, latest result e middle recuperavel [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:28-39.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] ja separa prompt estavel de payload reducivel e lista politicas de reducao por bloco [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:28-41.
- A fonte curricular ja apresenta fases verde, amarela, laranja e vermelha para uma conversa KODA, com acoes de monitorar, ativar summary buffer, resumir, compactar agressivamente ou mudar para nova conversa [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:523-566.

### What is missing

- Um contrato canonico que una percentual restante e burn-rate forecast em fases token-specific. A classificacao marcou `Phase-Gated Token Health Monitor` como Partial Coverage e registrou NOT_FOUND para fases de saude de tokens guiadas por percentual restante e aceleracao de burn rate [[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:34-42.
- Um forecast canonico de burn rate. A classificacao marcou `Burn-Rate Runtime Forecast` como Missing e registrou NOT_FOUND para velocidade de consumo, aceleracao e minutos ou mensagens restantes [[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:24-32.
- Um ledger canonico de budget por chamada. A classificacao marcou `Explicit Token Budget Ledger` como Partial Coverage e registrou ausencia de schema com response reserve, safety reserve, percentual restante e breakdown por chamada [[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:14-22.
- Uma decisao de atuacao que feche o loop: o padrao extraido avisa que o monitor so e util se o harness implementar a acao retornada [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:76-79.

## Operating Rules

1. Calcule saude antes de montar o prompt final para o modelo, porque o context builder precisa saber se deve reduzir, resumir ou externalizar blocos antes da chamada.
2. Subtraia buffer de resposta e safety buffer antes de classificar a fase, porque gastar toda a janela em input reduz a capacidade de gerar uma resposta util [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:121-125.
3. Promova a fase quando a aceleracao de burn rate encurtar o runway, mesmo se o percentual restante parecer confortavel. A analise registra que budget health e temporal, nao apenas espacial [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:37.
4. Em `orange`, compacte enquanto ainda ha contexto suficiente para resumir com qualidade. A analise lista intervencao tardia como falha e recomenda thresholds que intervenham enquanto ainda ha espaco para resumir com seguranca [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:219-223.
5. Em `red`, prefira handoff ou nova sessao quando a continuidade dentro do contexto atual ameacar qualidade. A analise trata transicao de sessao como fluxo intencional quando o budget esta baixo [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:127.

## Evaluation and Observability

O monitor deve emitir evidencia por decisao: fase anterior, fase nova, percentuais, burn rate, acao escolhida, blocos afetados e outcome. Essa evidencia alimenta evals de sessao longa, porque late-session ou context failures recorrentes devem expandir [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]] segundo o gate de progressao de evals [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:40-51.

Casos de eval devem cobrir pelo menos:

- Uma sessao `green` que continua sem resumo desnecessario.
- Uma sessao `yellow` que registra tendencia mas nao compacta.
- Uma sessao `orange` que aciona summary buffer ou compressao antes de comportamento degradado.
- Uma sessao `red` que produz handoff, nova sessao ou terminacao forcada com estado suficiente para continuidade.
- Um caso de burn-rate acelerado que promove fase mesmo com budget restante aparentemente alto.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Intervem antes de crash ou degradacao visivel, alinhado ao objetivo de agir antes da qualidade colapsar [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:121-127 | Thresholds precisam calibracao com traces reais e comportamento do modelo [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:76-79 |
| Converte token budgeting em loop de controle, nao truncation reativo [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:72-75 | Thresholds agressivos podem aumentar latencia ou churn de resumos [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:76-79 |
| Usa pontos de intervencao ja definidos no loop owned [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 | O harness precisa implementar cada acao retornada, ou o monitor vira telemetria passiva [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:76-79 |
| Ajuda a escolher entre resumo, compressao e nova sessao com base em runway, nao intuicao [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-519 | Forecasts podem errar quando usuarios ou tool payloads mudam abruptamente [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:54-57 |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], porque as fases precisam atuar nos pontos de `summarize`, `break`, gates humanos e terminacao forcada [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75.
- **Uses:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]], porque `orange` pode reduzir active context preservando prompt estavel, head, tail, latest result e middle recuperavel [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:28-39.
- **Constrained by:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]], porque compactacao por fase nao deve reduzir o prompt de harness que define contrato operacional [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:20-41.
- **Complements:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]], porque fases `orange` e `red` sao uma forma de degradacao operacional antes de falha dura [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:27-65.
- **Validated by:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]], porque falhas tardias ou de contexto recorrentes devem acionar a proxima capacidade minima de eval [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:40-51.

## References

- [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:28-37 - quatro componentes do budget e burn rate.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:39-49 - modelo de fases verde, amarela, laranja e vermelha.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]:111-117 - token health monitor como mecanismo operacional.
- [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:59-79 - padrao extraido do Phase-Gated Token Health Monitor.
- [[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:34-42 - classificacao Partial Coverage e lacuna NOT_FOUND.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-519 - red flags de burn rate, baixo budget e comportamento ansioso.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:523-566 - fases KODA e acoes associadas.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:577-603 - exemplo de implementacao com thresholds e actions.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 - intervencoes de loop usadas como atuadores.
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29-65 - ladder de degradacao adjacente.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:40-51 - gate de eval por sinais de dor.
