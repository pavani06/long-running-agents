---
name: perceived-eval
description: "Instrumenta a qualidade percebida do agente em producao tratando o comportamento de correcao do usuario como dado de avaliacao. Capta correcoes, pushback e redirecionamentos do usuario, metricas comportamentais de saida do chat/stuck/rage quit, e NPS periodico — sem rodar surveys continuos. Alimenta sessoes de sinal negativo no loop producao-para-offline (regression flywheel). Usar ao instrumentar conversas de producao para detectar frustracao implicita, ao conectar CSAT/NPS a o pipeline de evals, ou quando dashboards verdes coexistem com usuarios corrigindo o agente toda sessao. Dispara com: 'perceived eval', 'qualidade percebida', 'perceived quality', 'user correction', 'correcao do usuario', 'usuario corrige', 'cliente corrige', 'pushback', 'redirecionamento', 'redirection', 'rage quit', 'chat exit', 'saida do chat', 'stuck session', 'sessao travada', 'NPS', 'CSAT', 'satisfacao', 'survey fatigue', 'sinal online', 'online signal', 'online evaluator', 'implicit feedback', 'feedback implicito', 'user behavior telemetry', 'producao para offline', 'production to offline'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: implementation
  priority: high
  version: 1.0.0
  source: "Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline) — pattern 8, classified Missing/High"
---

## What I Do

Eu converto o comportamento do usuario durante a conversa com o agente em dado de avaliacao continuo. Meu contrato e responder a pergunta "o usuario esta percebendo qualidade?" sem rodar surveys constantes — a correcao do usuario E a avaliacao.

Eu produzo quatro artefatos:

1. **Eventos de correction/pushback/redirection** — deteccao de momentos em que o usuario corrige a saida do agente ("nao, eu disse X"), empurra de volta uma afirmacao/comportamento, ou tenta guiar o agente para outro caminho
2. **Metricas comportamentais objetivas** — saida do chat para outras areas do produto, stuck (inatividade/prompts repetidos), rage quit (abandono abrupto apos sinais de frustracao)
3. **Medida explicita periodica** — NPS/satisfacao amostrada, combinada aos sinais implicitos continuos
4. **Sessoes de sinal negativo encaminhadas ao loop producao-para-offline** — sessoes flaggadas viram intake do regression flywheel, nao apenas linha de dashboard

A tese central: o comportamento de correcao do usuario e o unico sinal de qualidade percebida que se coleta sozinho, em toda sessao, sem survey fatigue. Sinal implicito (comportamento) e continuo e objetivo; sinal explicito (NPS) e periodico e subjetivo; o padrao usa os dois, com resolucao por sessao — nunca por decisao individual do agente.

## When to Use Me

Carregue esta skill quando:

- O agente roda em producao com usuarios reais e voce quer medir qualidade percebida sem instrumentar surveys continuos
- Dashboards de CSAT/proxy existem mas sao so outcome de release (`docs/canonical/eval-to-production-correlation-tracking.md:35`) e ninguem sabe quais sessoes geraram a nota baixa
- Evals verdes coexistem com usuarios corrigindo o agente em toda sessao — o "scoring gap" que o flywheel classifica como "Eval said pass but user judged fail" (`docs/canonical/production-failure-regression-flywheel.md:50`)
- Voce esta projetando telemetry de produto conversacional e quer distinguir saida-do-chat-benigna (tarefa concluida) de saida-do-chat-de-frustracao
- O loop producao-para-offline precisa de fontes de sinal alem de tickets de suporte e online evaluators — correcoes de usuario sao o combustivel de maior volume
- Voce esta montando o quadrante online/nao-deterministico da matriz de cobertura de evals

Nao use quando:

- O agente nao tem usuarios interativos em producao (batch/scheduled jobs sem conversa) — nao ha comportamento de usuario a captar
- O objetivo e monitorar anomalias do sistema (latencia, erros, custo) — isso e [[docs/canonical/always-on-monitoring-human-triage|Always-On Monitoring with Human Triage]], que observa o sistema; perceived-eval observa a percepcao do usuario final
- O objetivo e calibrar intervencao de operadores humanos no loop — isso e [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]], que mede operadores, nao usuarios
- O volume e tao baixo que revisao humana de cada trace e viavel — sinal comportamental aggregate precisa de volume para significar algo
- Voce quer punir decisoes individuais do agente com o sinal — a resolucao e por sessao; uso disciplinar do sinal e anti-padrao

## The Anti-Pattern

```
ANTI-PATTERN: Survey periodico como unica medida de qualidade percebida.

Cenario:
  1. O time lanca o agente. A cada trimestre, roda um survey de NPS.
  2. Entre surveys, zero visibilidade de percepcao do usuario.
  3. Usuarios corrigem o agente em 40% das sessoes ("nao, quero em
     formato de tabela", "isso nao e o que eu pedi"). Ninguem registra.
  4. Um usuario da rage quit apos 3 correcoes seguidas. O evento
     aparece como "sessao encerrada" — sem causa, sem classificacao.
  5. O survey trimestral chega: NPS 42. O time pergunta "o que
     aconteceu em marco?" — impossivel responder; o dado morreu.
  6. A suite de eval continua verde: os goldens cobrem o formato
     que o time acha que o usuario quer, nao o que ele pede.

Consequencia:
  - Sinal de qualidade percebida existe em amostra de 100%, mas
    e coletado em amostra de ~1%, com lag de semanas
  - Correcoes de usuario — o caso de eval mais barato e abundante —
    evaporam; viram nada, nao viram regressao
  - "Scoring gap" (eval pass + usuario insatisfeito) nunca e
    detectado; evals e percepcao seguem mundos separados
```

Variacao igualmente comum: logar eventos comportamentais (exit, stuck) apenas como metricas de dashboard de release, sem join com a transcrita da sessao e sem encaminhar ao pipeline de evals — telemetry que nao alimenta learning loop e apenas ar decorativo.

## The Pattern

```
PATTERN: O comportamento de correcao do usuario e avaliacao continua.

Fluxo:

  Producao: conversa usuario <-> agente
      |
      v
  +-----------------------------------------------------------+
  | 1. DETECTOR DE CORRECAO/PUSHBACK/REDIRECTION              |
  |                                                           |
  | Sobre cada turno do usuario (heuristica deterministica    |
  | + classificador LLM sobre a transcrita):                  |
  |                                                           |
  |  Tipo de evento              Exemplo                      |
  |  -------------------------  ---------------------------   |
  |  Correction      "nao, eu disse a versao 2, nao a 1"      |
  |  Pushback        "isso esta errado / eu discordo"         |
  |  Redirection     "esquece, faz de outro jeito"            |
  |  Repeat-repair   mesmo pedido refeito apos saida errada   |
  +-----------------------------------------------------------+
      |
      v
  +-----------------------------------------------------------+
  | 2. TELEMETRIA COMPORTAMENTAL OBJETIVA                     |
  |                                                           |
  |  Sinal                      Leitura                       |
  |  -------------------------  -----------------------------  |
  |  Chat exit c/ tarefa       Possivel frustracao — join     |
  |    incompleta               com outcome da sessao         |
  |  Exit para outra area       Fuga do agente                |
  |    do produto                (ou exploracao benigna)      |
  |  Stuck (inatividade /       Usuario confuso ou travado    |
  |    prompts identicos         repetidos)                   |
  |  Rage quit (abandono        Frustracao terminal           |
  |    abrupto pos-correcoes)                                 |
  +-----------------------------------------------------------+
      |
      v
  +-----------------------------------------------------------+
  | 3. SINAL EXPLICITO PERIODICO                              |
  |                                                           |
  | NPS/satisfacao amostrado por episodio, nao survey massivo |
  | continuo — calibra a leitura dos sinais implicitos        |
  | (qual taxa de exit e "ruído benigno"? o NPS diz).         |
  +-----------------------------------------------------------+
      |
      v
  +-----------------------------------------------------------+
  | 4. ENCAMINHAMENTO AO LOOP PRODUCAO-PARA-OFFLINE           |
  |                                                           |
  | Sessao com sinal negativo (correcao + exit/stuck/raq)     |
  |   -> intake do regression flywheel                        |
  |   -> captura com privacy filters (sampling canonico)      |
  |   -> label: classe de falha ("scoring gap" etc.)          |
  |   -> caso de regressao no tier correto                    |
  |   -> metrica de production outcome no correlation         |
  |      tracking (evals tem que prever este sinal)           |
  +-----------------------------------------------------------+
```

### O que conta como sinal

| Sinal | Tipo | Forca | Observacao |
|---|---|---|---|
| Correction explicita do usuario | Implicito | Alta | O usuario esta escrevendo a golden answer ao vivo |
| Pushback sobre afirmacao do agente | Implicito | Alta | Indica factual/tono reprovado |
| Redirection ("faz de outro jeito") | Implicito | Media | Sozinho e ambiguo; em cluster e padrao |
| Repeat-repair (pedido refeito) | Implicito | Alta | A saida anterior falhou silenciosamente |
| Exit com tarefa incompleta | Comportamental | Media | Join obrigatorio com outcome da sessao |
| Exit apos correcao/insucesso | Comportamental | Alta | Sequencia correction->exit e o rage quit path |
| Stuck / prompts repetidos | Comportamental | Media | Causa benigna possivel (usuario AFK) |
| NPS baixo no episodio | Explicito | Alta | Amostrado, nao continuo |

## Implementation Rules

1. **Deteccao em dois estagios.** Estando 1: heuristicas deterministicas sobre o turno (repeticao de instrucao anterior, negacao seguida de reformulacao, marcadores lexicos de discordancia) — alto recall, precisao baixa. Estagio 2: classificador LLM sobre a janela da transcrita confirma e tipifica o evento. O precedente de escala do repo e a classificacao LLM de logs de producao em taxonomia (`docs/canonical/llm-classified-log-taxonomy.md:48,53`) — mesma arquitetura, nova dimensao (percepcao, nao topico).

2. **Comportamental precisa de join com outcome.** Exit/stick tem causas benignas (tarefa concluida, usuario explorando — limitacao declarada do padrao). Nunca reporte exit rate cru como sinal de qualidade: join com status da tarefa, presenca de correcao previa na mesma sessao, e tempo desde a ultima resposta do agente. Sinal negativo = combinacao (correction + exit incompleto), nao evento isolado.

3. **Resolucao por sessao, nao por decisao.** O sinal delimita a sessao onde a qualidade percebida falhou; nao identifica o turno exato culpado. A triagem humana (ou LLM) do caso extrai o turno no intake do flywheel — nao presuma atribuicao automatica.

4. **NPS e periodico e amostrado, nunca continuo.** O beneficio central do padrao e eliminar survey fatigue: o sinal implicito cobre 100% das sessoes; o explicito calibra a leitura (diz qual fracao dos exits e benigna) em amostra. Survey continuo recria o anti-padrao.

5. **Encaminhamento ao flywheel segue o contrato existente.** Sessao de sinal negativo entra no intake do [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (`:32-40`): captura de interacao/trace/versoes, privacy filters e retention antes de preservar fixture ([[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] `:35-36`), label de classe de falha — o default natural e "Scoring gap" (eval passou, usuario reprovou, `:50`) — dedup, tier, backfill.

6. **Perceived-eval e production outcome no correlation tracking.** As metricas derivadas (taxa de correcao por sessao, rage quit rate, NPS episodico) entram na tabela de production outcomes que os evals devem prever (`docs/canonical/eval-to-production-correlation-tracking.md:35-36`). Se a suite fica verde enquanto a taxa de correcao sobe, a correlacao decaiu — recalibracao dispara (`:38-39`).

7. **Instrumente antes de precisar.** A deteccao confiavel de correcoes exige iteracao sobre os proprios detectores (falsos positivos de pushback, etc.). Trate os detectores como monitores refinaveis, no espirito do [[docs/canonical/always-on-monitoring-human-triage|Always-On Monitoring]] (`:40-44`): flag dispensada por falso positivo ajusta o detector.

## Integration with Existing Repo Infrastructure

| Componente existente | Como o Perceived-Eval se integra |
|---|---|
| [[docs/canonical/perceived-eval\|Perceived-Eval]] (doc canonico) | Fonte canonica do padrao — esta skill e a superficie de implementacao; detalhes de problema/solucao/tradeoffs vivem no canonico |
| [[docs/canonical/production-failure-regression-flywheel\|Production Failure Regression Flywheel]] | Destino dos sinais negativos: sessao flaggada = intake; classe "Scoring gap" (`:50`) e a label natural de correcao de usuario com eval verde |
| [[docs/canonical/production-grounded-eval-sampling\|Production-Grounded Eval Sampling]] | Contrato de captura: privacy filters, retention, coverage metadata e labeling para o fixture derivado da sessao (`:35-41`) |
| [[docs/canonical/eval-to-production-correlation-tracking\|Eval-to-Production Correlation Tracking]] | Upgrade do slot "CSAT proxy" (`:35`): de proxy de survey para sinal comportamental continuo + NPS amostrado; vira outcome que evals devem prever |
| [[docs/canonical/always-on-monitoring-human-triage\|Always-On Monitoring with Human Triage]] | Complemento por eixo: monitors observam qualidade do sistema; perceived-eval observa a percepcao do usuario final. Sessoes flaggadas podem entrar na mesma fila de triagem humana |
| [[docs/canonical/presence-in-the-loop-metric\|Presence-in-the-Loop Metric]] | Distincao de sujeito: presence mede operadores internos no loop de execucao; perceived-eval mede usuarios finais na conversa — mesmo mecanismo de timeline, sujeitos diferentes |
| [[docs/canonical/llm-classified-log-taxonomy\|LLM-Classified Log Taxonomy]] | Precedente arquitetural do estagio 2 do detector: classificacao LLM de producao em volume sobre taxonomia (`:48,53`) |
| `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1596` | O dashboard baseline/candidate ja exibe CSAT proxy; perceived-eval fornece a origem granular (quais sessoes, qual sinal) por tras do numero |

## Quality Gates

Antes de declarar o perceived-eval operacional, verifique:

- [ ] Eventos de correction/pushback/redirection sao detectados nas conversas de producao (heuristica + classificador), nao apenas imaginados no design
- [ ] Telemetria comportamental (exit, stuck, rage quit) tem join com outcome da sessao — nenhum exit rate cru reportado como qualidade
- [ ] NPS/satisfacao e amostrado por episodio; nenhum survey continuo injetado em toda sessao
- [ ] Sessoes de sinal negativo chegam ao intake do regression flywheel com privacy filters e retention aplicados antes da preservacao do fixture
- [ ] Cada caso encaminhado recebe label de classe de falha ("Scoring gap" quando eval passou e usuario reprovou)
- [ ] As metricas derivadas (correction rate, rage quit rate, NPS episodico) constam na tabela de production outcomes do correlation tracking
- [ ] Falsos positivos dispensados em triagem alimentam refinamento dos detectores
- [ ] A resolucao do sinal esta documentada como por-sessao — nenhuma decisao individual do agente e auto-punida com este dado
- [ ] Causas benignas de exit/stuck (tarefa concluida, exploracao) sao tratadas no join, nao ignoradas

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md:132-144` — classificacao Missing/High; NOT_FOUND de mecanica de perceived-eval no repo
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:163-183` — definicao extraida do padrao (inputs/outputs/benefits/limitations)
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.yaml:216-244` — componentes e flow canonicos
- [[docs/canonical/perceived-eval|Perceived-Eval]] — doc canonico (criado em paralelo a esta skill)
- `docs/canonical/eval-to-production-correlation-tracking.md:35-39` — CSAT como outcome proxy; decay/recalibracao
- `docs/canonical/production-failure-regression-flywheel.md:28-41,50` — flywheel e taxonomia de falhas ("Scoring gap")
- `docs/canonical/production-grounded-eval-sampling.md:32-41` — captura, privacy, retention, labeling, refresh
- `docs/canonical/always-on-monitoring-human-triage.md` — monitoramento de sistema com triagem humana (adjacente, eixo diferente)
- `docs/canonical/presence-in-the-loop-metric.md` — metrica de operadores (adjacente, sujeito diferente)
- `docs/canonical/llm-classified-log-taxonomy.md:48,53` — precedente de classificacao LLM de producao em escala
- `docs/system-of-record.md:238,300` — entradas SOR dos adjacentes citados pela classificacao

---

*Created: 2026-08-31 | Source: Clay Eval Stack pattern classification — Pattern 8 (Missing, High value)*
