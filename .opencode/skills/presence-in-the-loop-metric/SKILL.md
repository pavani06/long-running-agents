---
name: presence-in-the-loop-metric
description: "Mede a presenca humana durante a execucao agentica como metrica de governanca, nao apenas a aprovacao simbolica no gate final. Gera timeline de envolvimento, alertas de ausencia prolongada (stale-presence), e pontos de intervencao obrigatoria antes que o loop continue. Previne o cenario onde o humano so aparece no final para abencoar um diff grande demais para realmente ler. Usar ao monitorar sessoes agenticas longas, ao projetar loops de controle com gates humanos, ou quando diffs grandes estao sendo mergeados sem envolvimento proporcional do outcome-owner. Dispara com: 'presenca no loop', 'presence in the loop', 'presence metric', 'metrica de presenca', 'owner presence', 'stale owner', 'owner ausente', 'dono ausente', 'human involvement', 'timeline de presenca', 'intervention points', 'approval at the gate', 'review confidence', 'diff sem dono', 'agente escreveu sozinho', 'dez mil linhas', 'ninguem leu o diff'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: governance
  priority: medium
  source: "IDSD — Intent-Driven Software Development (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu transformo "presenca humana" de um conceito vago em uma metrica operacional. Meu trabalho nao e monitorar pessoas -- e garantir que a ausencia do outcome-owner durante a execucao agentica seja visivel e acionavel antes que um diff grande demais para revisar chegue ao gate final.

Eu produzo quatro artefatos:

1. **Timeline de presenca** — registro de quando o owner esteve envolvido (checkpoints, comentarios, decisoes, perguntas respondidas) durante a execucao
2. **Alertas de ausencia** — warnings quando o owner esta ausente por tempo ou complexidade acima de thresholds configurados (stale-presence)
3. **Pontos de intervencao obrigatoria** — momentos no loop agentico onde o owner DEVE se manifestar antes que o loop continue (required intervention points)
4. **Sinal de confianca para o gate final** — score composto que informa ao revisor final se o owner esteve presente durante a construcao ou se o diff foi produzido sem envolvimento proporcional

A metrica central e simples: **presenca no loop, nao aprovacao no gate**. O humano e parte do time enquanto o trabalho acontece, nao o revisor que chega no fim para abencoar um diff que ja nao da tempo de entender.

## When to Use Me

Carregue esta skill quando:

- Sessoes agenticas longas estao produzindo diffs grandes e voce quer saber se o outcome-owner esteve envolvido durante a construcao
- Voce esta projetando ou auditando um loop de controle agentico com gates humanos (ex: [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]])
- Um diff de 500+ linhas chegou para revisao e ninguem consegue apontar quem acompanhou a construcao passo a passo
- O [[docs/canonical/manual-brake-question-gate|Manual Brake]] identificou que ha um owner, mas voce quer verificar se esse owner permaneceu presente apos o gate inicial
- Voce suspeita de "approval rubber-stamping" -- revisores aprovando codigo que nao tiveram tempo de entender porque o diff ja esta grande demais
- Uma falha em producao ocorreu e a pergunta e: "quem estava acompanhando isso enquanto era construido?"
- Voce quer estabelecer thresholds de presenca por nivel de risco (ex: diffs acima de 200 linhas exigem pelo menos 3 checkpoints do owner)

Nao use quando:

- A tarefa e puramente mecanica e AFK-ready (classificada pelo [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]) -- nestes casos, ausencia do owner e esperada e correta
- O time e de uma pessoa (founder = owner = builder = reviewer) -- a metrica existe para times onde owner e builder sao pessoas diferentes
- Voce quer transformar isso em surveillance de produtividade -- esta skill mede envolvimento com o outcome, nao horas trabalhadas ou tempo de tela
- O loop agentico e totalmente autonomo por design e o contrato de execucao nao preve intervencao humana (ex: batch processing, scheduled jobs)

## The Anti-Pattern

```
ANTI-PATTERN: Aprovacao no gate substitui presenca no loop.

Cenario:
  1. O outcome-owner escreve um intent: "adiciona dashboard de analytics
     com metricas de retencao e churn".
  2. O intent passa pelo Manual Brake. Alguem diz "sim, construa".
  3. O agente trabalha por 4 horas. Produz 1,200 linhas em 8 arquivos.
     Ninguem acompanha. Ninguem pergunta. Ninguem intervem.
  4. O agente abre um PR. O diff e grande, mas o codigo compila, os testes
     passam, o lint esta verde.
  5. O revisor olha o PR. 1,200 linhas. Ele le os primeiros 3 arquivos,
     faz comentarios cosmeticos, aprova. Nao ha tempo para ler tudo.
  6. Merge. Deploy. Duas semanas depois: o dashboard calcula churn
     errado porque o agente interpretou "cliente inativo" como 7 dias,
     mas o negocio define como 30 dias. O owner nunca foi consultado
     sobre essa definicao durante a construcao.

Consequencia:
  - O diff foi grande demais para revisar; a aprovacao foi simbolica
  - O agente tomou decisoes de dominio (definicao de churn) que o
    outcome-owner deveria ter tomado
  - A falha so foi descoberta em producao, duas semanas depois
  - Ninguem sabe quem deveria ter respondido a pergunta sobre a
    definicao de inatividade -- o owner estava ausente do loop
```

O ponto de falha nao e a qualidade do codigo ou dos testes -- ambos passaram. A falha e de governanca: o humano que define o que "certo" significa nao estava presente enquanto o agente decidia o que "certo" significava.

## The Pattern

```
PATTERN: Timeline de presenca como metrica operacional de governanca.

Fluxo:

  Execucao agentica inicia
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. CONTRATO DE PRESENCA                                  │
  │                                                         │
  │ Antes da execucao, define-se:                            │
  │ - Nivel de risco da tarefa (baixo / medio / alto)       │
  │ - Threshold de presenca minima (quantos checkpoints?)    │
  │ - Intervalo maximo sem intervencao (stale-presence)      │
  │ - Pontos de intervencao obrigatoria (quais decisoes      │
  │   o agente NAO pode tomar sozinho?)                      │
  │ - Owner nomeado e canal de contato                       │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. TIMELINE DE PRESENCA                                  │
  │                                                         │
  │ Durante a execucao, registra-se cada evento de presenca: │
  │                                                         │
  │  Tipo de evento                    Exemplo               │
  │  ─────────────────────────────────────────────────────  │
  │  Checkpoint decision     Owner respondeu pergunta de    │
  │                          design ou escopo               │
  │  Constraint clarification Owner esclareceu constraint    │
  │                          ambigua                        │
  │  Failure review          Owner revisou falha e decidiu   │
  │                          retry vs. escalate             │
  │  Direction change        Owner alterou o rumo da        │
  │                          implementacao                  │
  │  Interim review          Owner revisou artefato parcial  │
  │                          e deu feedback                 │
  │  Approval to proceed     Owner autorizou continuacao     │
  │                          apos checkpoint                │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. DETECCAO DE AUSENCIA (STALE-PRESENCE)                 │
  │                                                         │
  │ Monitora:                                               │
  │ - Tempo desde o ultimo evento de presenca               │
  │ - Linhas geradas desde o ultimo checkpoint              │
  │ - Decisoes de dominio tomadas pelo agente sem consulta  │
  │                                                         │
  │ Alerta quando:                                          │
  │ - Tempo sem presenca > threshold (ex: 2h para alto      │
  │   risco, 8h para medio)                                 │
  │ - Linhas geradas sem checkpoint > threshold (ex: 200    │
  │   linhas para alto risco)                               │
  │ - Agente tomou N decisoes de dominio sem consulta       │
  │   (ex: > 3 para alto risco)                             │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. PONTOS DE INTERVENCAO OBRIGATORIA                     │
  │                                                         │
  │ O loop agentico PARA e requer presenca antes de:         │
  │                                                         │
  │ - Cruzar um boundary de modulo ou sistema               │
  │ - Introduzir uma nova abstracao ou dependencia           │
  │ - Alterar comportamento existente (breaking change)      │
  │ - Atingir o threshold de linhas-sem-checkpoint           │
  │ - Encontrar uma constraint ambigua que o owner nao       │
  │   esclareceu                                            │
  │ - Completar uma fase (planejar → executar → verificar)   │
  │   e transitar para a proxima                             │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 5. SINAL DE CONFIANCA PARA O GATE FINAL                  │
  │                                                         │
  │ Calculado a partir da timeline de presenca:              │
  │                                                         │
  │  Componente                    Peso                      │
  │  ─────────────────────────────────────────────────────  │
  │  Checkpoints atendidos /       Determina score base     │
  │    checkpoints requeridos                               │
  │  Decisoes de dominio com       Penaliza ausencia em     │
  │    owner vs. sem owner          decisoes criticas        │
  │  Linhas geradas com vs.        Penaliza diffs grandes   │
  │    sem supervisao               nao supervisionados      │
  │  Tempo total com owner          Bonus por presenca       │
  │    presente vs. ausente          consistente             │
  │                                                         │
  │ Score baixo → gate final deve ser mais rigoroso.         │
  │ Score alto → evidencia de que o owner possui o outcome.  │
  └─────────────────────────────────────────────────────────┘
```

### Risk-Tiered Presence Thresholds

A presenca exigida escala com o risco da tarefa:

| Nivel de Risco | Exemplos | Checkpoints Minimos | Intervalo Max sem Presenca | Linhas Max sem Checkpoint |
|---|---|---|---|---|
| Baixo | Bump de dependencia, correcao de lint, refactor local | 0-1 (apenas aprovacao final) | Ilimitado | Ilimitado |
| Medio | Feature interna, melhoria de tooling, script de automacao | 2+ (inicio e meio) | 8h | 400 linhas |
| Alto | Feature de usuario, mudanca de API, alteracao de comportamento | 3+ (inicio + 2 intermediarios) | 2h | 200 linhas |
| Critico | Mudanca de arquitetura, cross-system, regulacao, dados de cliente | 5+ (checkpoint por fase ou componente) | 1h | 100 linhas |

### O Que Nao e Presenca

Nem toda interacao conta como presenca significativa:

| E presenca | Nao e presenca |
|---|---|
| Responder pergunta de design ou dominio | Dar "like" ou "ack" em uma mensagem |
| Revisar artefato parcial com feedback concreto | Dizer "parece bom" sem ler |
| Esclarecer constraint ambigua | Estar online mas nao interagir com o trabalho |
| Decidir retry vs. escalate apos falha | Receber notificacao e ignorar |
| Alterar direcao da implementacao | Aprovar PR sem ler o diff |

Presenca e envolvimento ativo com o outcome, nao disponibilidade passiva.

## Implementation Rules

1. **Presenca nao e vigilancia.** Esta skill mede envolvimento do owner com o outcome que ele encomendou. Nao mede horas de trabalho, velocidade de resposta, ou tempo de tela. O proposito e garantir que o owner esta presente para possuir as decisoes que o agente nao pode tomar, nao para monitorar se o owner esta "trabalhando o suficiente".

2. **Thresholds sao calibraveis por time e dominio.** Os valores sugeridos na tabela de risk-tiering sao pontos de partida. Times diferentes, dominios diferentes, e fases diferentes do projeto exigem calibracao. Um time em fase de exploracao tolera mais ausencia que um time em fase de manutencao de sistema critico.

3. **Stale-presence gera pergunta, nao bloqueio.** Um alerta de ausencia nao deve parar o agente automaticamente. Deve gerar uma pergunta: "Owner ausente ha X horas, com Y linhas geradas. Continuar, pausar, ou escalar?" A decisao e de quem recebe o alerta.

4. **Intervention points sao contratos, nao surpresas.** Os pontos de intervencao obrigatoria devem ser conhecidos antes da execucao comecar. O owner sabe que sera chamado quando o agente cruzar um boundary de modulo ou completar uma fase. Isso transforma a presenca de reativa ("me chamaram!") para proativa ("sei que serei chamado quando X acontecer").

5. **O sinal de confianca informa, nao decide.** O score de presenca e uma entrada para o gate final, nao o gate em si. Um score baixo significa "revise com mais cuidado", nao "rejeite automaticamente". Um score alto significa "o owner esteve presente", nao "aprove sem ler".

6. **Registre a ausencia como dado de governanca.** Ausencias repetidas do mesmo owner, ou em tarefas do mesmo tipo, sao sinais de que o contrato de presenca precisa ser renegociado. O padrao de ausencia e tao informativo quanto o padrao de presenca.

## Integration with Existing Repo Infrastructure

A metrica de presenca se integra ao ciclo de vida agentico do repositorio como camada de governanca transversal:

| Componente Existente | Como a Presence-in-the-Loop Metric complementa |
|---|---|
| [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] | O Manual Brake pergunta "quem e o dono de dizer nao?" no inicio. A Presence Metric responde: "esse dono permaneceu presente depois que disse sim?" O brake garante que ha um owner; a metrica garante que o owner nao abandonou o loop. |
| [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]] | O value gate decide BUILD/EXPERIMENT/DEFER/STOP antes da execucao. A Presence Metric adiciona checkpoints de presenca DURANTE a execucao. Se o value gate disse BUILD e o owner desapareceu, a metrica sinaliza que o contrato de valor nao esta sendo honrado. |
| [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] | O AFK Gate classifica tarefas como AFK-ready ou human-in-loop. Tarefas human-in-loop sao exatamente aquelas que exigem presenca. A Presence Metric operacionaliza a dimensao "human-in-loop": o que "human-in-loop" significa em termos de checkpoints, intervalos e thresholds. |
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me captura intents, constraints e decisoes antes da execucao. A Presence Metric garante que as decisoes capturadas nao sao as ultimas -- durante a execucao, novas perguntas surgem e o owner precisa estar presente para responde-las. |
| [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]] | O Owner-of-No define quem pode recusar trabalho. A Presence Metric mede se esse owner esta presente para exercer sua autoridade durante a execucao. Um Owner-of-No ausente e um owner que existe no papel mas nao no loop. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Evaluator detecta falhas contra constraints. Quando uma falha ocorre, a Presence Metric registra se o owner foi consultado sobre o que fazer (retry, escalate, change direction). Falhas resolvidas sem o owner sao decisoes de dominio tomadas pelo agente. |
| [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] | As transicoes entre fases (plan → execute → verify) sao pontos naturais de intervencao obrigatoria. A Presence Metric insere checkpoints nestas transicoes: o owner aprova o plano antes da execucao, revisa o progresso durante a execucao, e valida o resultado na verificacao. |
| [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] | O OS de loop fechado conecta state intake, execution routing e feedback writeback. A Presence Metric adiciona uma camada de governanca a esse loop: o estado do owner (presente, ausente, stale) e parte do state intake; a necessidade de checkpoints afeta o execution routing; e a timeline de presenca alimenta o feedback writeback. |
| [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] | O split-brain review separa revisao de engenharia e destino. A Presence Metric informa ambas: o revisor de engenharia sabe se o codigo foi produzido com ou sem supervisao; o revisor de destino sabe se o outcome-owner validou o rumo durante a construcao. |
| [[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]] | O Deferred Ledger rastreia carry debt de artefatos sem owner. A Presence Metric identifica artefatos construidos com owner ausente -- candidatos naturais a carry debt review. |

## Quality Gates

Antes de declarar a metrica de presenca como operacional para um ciclo de execucao, verifique:

- [ ] O contrato de presenca foi definido antes da execucao: nivel de risco, checkpoints minimos, intervalo maximo sem intervencao, e pontos de intervencao obrigatoria
- [ ] O owner foi nomeado e o canal de contato esta estabelecido
- [ ] A timeline de presenca esta sendo registrada durante a execucao (nao reconstruida a posteriori)
- [ ] Alertas de stale-presence estao configurados com thresholds proporcionais ao risco
- [ ] Pontos de intervencao obrigatoria estao instrumentados no loop agentico (o agente PARA e REQUER presenca nesses pontos)
- [ ] O sinal de confianca para o gate final e calculado a partir de dados reais de presenca, nao de estimativas
- [ ] Ausencias detectadas geram perguntas, nao bloqueios automaticos -- o alerta pergunta "continuar, pausar, ou escalar?"
- [ ] O revisor final recebe o score de presenca como input para calibrar a profundidade da revisao
- [ ] Apos o ciclo: a timeline de presenca e revisada para calibrar thresholds e identificar padroes de ausencia sistemica
- [ ] Nao ha confusao entre "presenca" (envolvimento com o outcome) e "disponibilidade" (estar online) -- os registros refletem interacoes substantivas com o trabalho

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:53-55 — Drift como ausencia humana, nao falha da spec
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:96-100 — Presence-in-the-loop como metrica central
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:118 — "Uma spec boa nao se sustenta sozinha; sustenta porque alguem fica no loop"
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:132-134 — Presenca como parte do time, nao revisor do gate
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]:161-188 — Pattern 6: Presence-in-the-Loop Operating Metric
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]:163-192 — Classification as Missing (Medium integration value)
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] — gate de valor pre-execucao (owner nomeado, mas sem garantia de presenca continua)
- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]] — papel organizacional cuja presenca esta metrica mede
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] — classificacao de tarefas (human-in-loop = requer presenca)
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]] — loop com gates de valor (checkpoints de presenca durante o loop)
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] — sistema operacional do loop (ponto de insercao dos checkpoints de presenca)
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] — separacao em fases (transicoes = pontos de intervencao obrigatoria)

---

*Created: 2026-06-12 | Source: IDSD Method — Pattern 6 (Missing, Medium value)*
