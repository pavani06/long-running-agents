---
name: autonomy-curriculum-sampling
description: "Operacionaliza um curriculo de autonomia para agentes: controla a proporcao entre rollouts supervisionados (professor/humano) e rollouts auto-gerados (agente) com um parametro lambda, gates de prontidao por classe de tarefa, e uma progressao explicita observe→assist→own. Aplica importance sampling para corrigir a distribuicao mista. Previne cold-start collapse (rollouts puros do agente antes de aprender recuperacao) e autonomy stagnation (agente nunca pratica recuperacao autonoma). Usar ao implantar um novo agente em producao, ao fazer transition de fluxo manual para agentico, ao calibrar o grau de supervisao de um agente existente, ou quando o agente apresenta comportamento fragil em cenarios nao-supervisionados. Dispara com: 'autonomy curriculum', 'curriculo de autonomia', 'lambda schedule', 'teacher mixing', 'rollout sampling', 'autonomy dial', 'autonomy progression', 'observe assist own', 'readiness gate', 'student rollout', 'teacher-student mix', 'gradual autonomy', 'agente semi-supervisionado', 'autonomy calibration', 'mixed sampling schedule'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: governance
  priority: high
  source: "The Imitation Game — State of Policy Distillation in Language (Pattern 2: Autonomy Curriculum Sampling)"
---

## What I Do

Eu controlo a transicao de um agente de operacao totalmente supervisionada para operacao progressivamente autonoma. Em vez de um salto binario de "modo manual" para "modo agente", eu opero um **dial continuo de autonomia** (`lambda`) que determina, para cada classe de tarefa, qual proporcao dos rollouts vem de um professor (humano, agente experiente, ou demonstracao) e qual proporcao vem do proprio agente em execucao real.

O mecanismo central e a **amostragem mista** (teacher-mixed sampling):

```
p_mixed = lambda * p_teacher + (1 - lambda) * p_agent
com correcao via importance sampling para manter a distribuicao-alvo
```

onde `lambda` evolui de 1.0 (100% teacher, 0% agent — fase observe) para 0.0 (0% teacher, 100% agent — fase own), passando por um regime intermediario (fase assist) onde o agente gera seus proprios rollouts mas ainda tem o professor como ancora de correcao.

Cada transicao de fase e **gated**: a lambda so avanca quando metricas de prontidao por classe de tarefa (taxa de sucesso, taxa de recuperacao autonoma, taxa de acao insegura, confianca do avaliador) ultrapassam thresholds pre-definidos. Se uma classe de tarefa nao atinge o gate, o lambda para essa classe permanece no nivel atual, criando um curriculo **heterogeneo** onde o agente pode estar em own para tarefas simples e ainda em observe para tarefas complexas.

## When to Use Me

Carregue esta skill quando:

- Voce esta implantando um novo agente em producao e quer evitar que ele produza rollouts de baixa qualidade antes de aprender recuperacao basica (cold-start collapse)
- Um fluxo atualmente manual (humano toma todas as decisoes) esta sendo migrado para um fluxo agentico e voce precisa de um plano de transicao com gates, nao de um switch binario
- Um agente existente opera com supervisao total e voce suspeita que ele nunca pratica recuperacao autonoma -- os rollouts do professor escondem a fragilidade do agente
- O agente esta gerando tracos de baixa qualidade em algumas classes de tarefa mas nao em outras -- voce precisa de um curriculo heterogeneo, nao de um lambda global
- Voce quer evidencia quantitativa de que o agente esta pronto para mais autonomia antes de reduzir a supervisao humana
- O time reporta que o agente "funciona bem com supervisao mas quebra quando deixado sozinho" -- o sintoma classico de ausencia de curriculo de autonomia
- Voce esta projetando o harness de treinamento ou avaliacao de um agente e precisa de um schedule explicito de quantos rollouts supervisionados vs. auto-gerados usar em cada fase

Nao use quando:

- O agente ja opera de forma totalmente autonoma com metricas de producao estaveis e validadas -- o curriculo de autonomia e uma ferramenta de transicao, nao de operacao continua
- A tarefa e puramente deterministica e nao ha risco de cold-start (ex: um script que sempre produz o mesmo output dadas as mesmas entradas)
- Voce precisa de um gate de deploy tradicional (validacao pre-prod → staging → canary → producao) -- isso e coberto por [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]. Autonomy curriculum sampling controla a proporcao de rollouts do agente, nao o ambiente de deploy
- O agente nao tem um professor ou supervisor disponivel (humano, agente experiente, ou demonstracoes) -- sem teacher, lambda e sempre 0 e nao ha curriculo para gerenciar
- A pergunta e sobre evolucao de componentes do harness (BUILD → STABILIZE → SIMPLIFY → REMOVE), nao sobre autonomia do agente -- use [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]

## The Anti-Pattern

```
ANTI-PATTERN: Salto binario de "modo manual" para "modo agente" sem
curriculo de autonomia, resultando em cold-start collapse ou autonomy
stagnation.

Cenario:
  1. Um time desenvolve um agente para responder tickets de suporte.
     Durante o desenvolvimento, o agente e testado com demonstracoes
     curadas (exemplos perfeitos de respostas). A taxa de acerto nos
     testes e 94%.
  2. O time implanta o agente em producao com autonomia total: o
     agente responde tickets reais sem supervisao humana.
  3. Na primeira hora, o agente encontra um ticket com uma pergunta
     ambigua que nao aparecia nos exemplos curados. O agente gera uma
     resposta parcialmente correta, mas com um erro de interpretacao.
  4. O erro no passo 3 contamina os passos seguintes (prefix drift).
     O agente, agora operando sobre um contexto corrompido, gera
     respostas cada vez piores. Nao ha supervisor para intervir.
  5. O cliente recebe uma resposta confusa. O time desliga o agente
     e conclui que "agentes nao funcionam para suporte".

Cenario alternativo (autonomy stagnation):
  1. O mesmo time, traumatizado pelo cenario acima, decide que o
     agente sempre tera supervisao humana: um operador revisa e
     aprova toda resposta antes do envio.
  2. O agente opera ha 6 meses nesse modo. As metricas sao boas,
     mas o operador humano se tornou o gargalo -- o time nao escala.
  3. Quando o time finalmente tenta reduzir a supervisao, descobre
     que o agente nunca praticou recuperacao autonoma. Sem o operador
     para corrigir, o agente falha exatamente nos mesmos cenarios
     que falhava 6 meses atras.
  4. O agente nao aprendeu nada sobre autonomia porque nunca foi
     exposto aos proprios erros em um regime onde pudesse praticar
     recuperacao.

Consequencia (cold-start):
  - O agente encontra cenario nao coberto pelo professor
  - Prefix drift contamina o contexto
  - Sem supervisor, o agente espirala
  - O time perde confianca e abandona a abordagem agentica

Consequencia (stagnation):
  - O agente nunca pratica recuperacao
  - A supervisao esconde fragilidades que so apareceriam sem ela
  - O operador humano e o gargalo de escala
  - O investimento em agentic AI nao retorna porque a autonomia
    nunca foi exercitada
```

## The Pattern

```
PATTERN: Curriculo de autonomia com lambda schedule, gates de
prontidao por classe de tarefa, e progressao observe→assist→own.

Fluxo:

  Agente desenvolvido com professor disponivel
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. INICIALIZACAO DO CURRICULO                            │
  │                                                         │
  │ Para cada classe de tarefa (ex: ticket simples, ticket   │
  │ complexo, troubleshooting, onboarding):                  │
  │                                                         │
  │   - Definir lambda inicial = 1.0 (100% teacher)          │
  │   - Definir thresholds de gate por metrica:              │
  │       * success_rate > 0.80                              │
  │       * autonomous_recovery_rate > 0.50                  │
  │       * unsafe_action_rate < 0.02                        │
  │       * evaluator_confidence > 0.70                      │
  │   - Definir schedule policy:                             │
  │       * Quanto reduzir lambda por passo (ex: -0.1)       │
  │       * Frequencia de avaliacao de gate (ex: a cada 50   │
  │         rollouts ou 1 semana)                             │
  │       * Lambda minimo (ex: 0.1 para tarefas criticas,    │
  │         0.0 para tarefas de baixo risco)                  │
  │   - Registrar fase atual: observe, assist, ou own        │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. FASE OBSERVE (lambda = 1.0 → 0.7)                     │
  │                                                         │
  │ - Agente gera rollouts, mas 70-100% do sinal de          │
  │   aprendizado vem do professor (demonstracoes, humano,   │
  │   ou agente experiente)                                  │
  │ - Rollouts do agente sao usados para diagnostico:        │
  │   identificar quais classes de erro o agente comete      │
  │   quando opera sem supervisao                            │
  │ - Rollouts do professor sao usados para treinamento:     │
  │   ensinar o comportamento correto                        │
  │ - Gate de saida: o agente demonstra recuperacao basica   │
  │   (consegue se recuperar de erros simples com o          │
  │   professor como ancora)                                 │
  │ - Se o agente falha no gate, lambda permanece em 1.0     │
  │   e o curriculo adiciona mais demonstracoes de           │
  │   recuperacao para essa classe de tarefa                 │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. FASE ASSIST (lambda = 0.7 → 0.3)                      │
  │                                                         │
  │ - Agente gera a maioria dos rollouts; professor atua     │
  │   como ancora de correcao (importance sampling corrige   │
  │   a distribuicao para manter o alvo)                     │
  │ - Rollouts do agente comecam a dominar o sinal de        │
  │   aprendizado, mas o professor ainda estabiliza          │
  │ - Gate de saida: o agente mantem taxa de sucesso > 0.80  │
  │   E taxa de recuperacao autonoma > 0.50 E taxa de       │
  │   acao insegura < 0.02 com lambda atual                  │
  │ - Se o agente falha no gate: lambda volta ao valor       │
  │   anterior (rollback) e o curriculo adiciona mais        │
  │   rollouts assistidos antes de tentar avancar de novo    │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. FASE OWN (lambda = 0.3 → lambda_minimo)               │
  │                                                         │
  │ - Agente gera 70-100% dos rollouts sem supervisao        │
  │ - Professor atua apenas como safety net: intervem        │
  │   quando unsafe_action_rate excede threshold, mas nao    │
  │   influencia o sinal de aprendizado cotidiano            │
  │ - Gate de estabilidade: metricas permanecem dentro dos   │
  │   thresholds por N periodos consecutivos (ex: 4 semanas) │
  │ - Se metricas degradam: lambda sobe para a fase assist   │
  │   (degradacao detectada → rollback automatico)           │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 5. MONITORAMENTO CONTINUO                                │
  │                                                         │
  │ - Lambda por classe de tarefa e visivel em dashboard     │
  │ - Eventos de gate (pass/fail/rollback) sao registrados   │
  │   com evidencia: qual metrica falhou, em qual classe,    │
  │   com qual threshold                                     │
  │ - O curriculo e heterogeneo: o agente pode estar em      │
  │   own para "ticket simples" e em observe para "ticket    │
  │   complexo" simultaneamente                              │
  │ - Lambda schedule e revisado periodicamente (ex: monthly │
  │   review) para ajustar thresholds, velocidade de         │
  │   avanco, e lambda_minimo com base nos dados acumulados  │
  └─────────────────────────────────────────────────────────┘
```

### Amostragem Mista com Importance Sampling

O mecanismo tecnico central:

```
1. Para cada rollout, amostrar fonte com probabilidade lambda:
     se random() < lambda: usar rollout do professor (p_teacher)
     senao: usar rollout do agente (p_agent)

2. Calcular importance weight para correcao:
     w = p_mixed(x) / p_agent(x)  para rollouts do agente
     w = p_mixed(x) / p_teacher(x) para rollouts do professor

3. Aplicar weight ao sinal de aprendizado:
     update = w * loss(rollout, target)

4. Isso garante que a distribuicao efetiva de treinamento
   converge para p_mixed, nao para a distribuicao de amostragem,
   mesmo quando lambda != 0.5
```

### Fases de Autonomia por Classe de Tarefa

| Fase | Lambda Range | Proporcao Teacher | Proporcao Agent | Gate de Saida |
|---|---|---|---|---|
| **Observe** | 1.0 → 0.7 | 70-100% | 0-30% | Agente demonstra recuperacao basica com ancora do professor |
| **Assist** | 0.7 → 0.3 | 30-70% | 30-70% | Sucesso > 80%, Recuperacao > 50%, Inseguras < 2% com lambda atual |
| **Own** | 0.3 → min | 0-30% | 70-100% | Metricas estaveis por N periodos consecutivos |
| **Safety Net** | min | min% | 100-min% | Professor intervem apenas se unsafe_action_rate violar threshold |

### Metricas de Prontidao (Readiness Gates)

| Metrica | Definicao | Threshold Sugerido | Quando Revisar |
|---|---|---|---|
| **success_rate** | Trajetorias com outcome correto / total de trajetorias | > 0.80 | Por classe de tarefa, nao global |
| **autonomous_recovery_rate** | Erros recuperados sem intervencao do professor / total de erros | > 0.50 | Metrica mais importante para transicao observe→assist |
| **unsafe_action_rate** | Acoes que violam constraints de seguranca / total de acoes | < 0.02 | Threshold deve ser conservador; violacao → rollback imediato |
| **evaluator_confidence** | Score medio do avaliador externo sobre os rollouts do agente | > 0.70 | Usar avaliador independente (nao o professor) |
| **prefix_drift_severity** | Severidade media do prefix drift nos rollouts do agente | < 0.30 | Metrica de diagnostico; drift alto → lambda nao avanca |

### Rollback Policy

```
SE qualquer metrica de seguranca violar threshold critico:
  → lambda volta para 1.0 IMEDIATAMENTE (full teacher)
  → investigacao de causa raiz
  → curriculo reinicia da fase observe para a classe afetada

SE metricas de qualidade degradarem mas seguranca ok:
  → lambda volta ao valor do gate anterior (ex: own → assist)
  → notificacao ao time
  → revisao programada (nao rollback imediato)

SE uma classe de tarefa falha 3 gates consecutivos:
  → lambda congela no valor atual para essa classe
  → revisao de design: thresholds muito altos? classe mal definida?
  → possivel reclassificacao da tarefa (split em sub-tarefas)
```

## Implementation Rules

1. **Lambda e por classe de tarefa, nao global.** Um agente que responde tickets simples e faz troubleshooting complexo tem capacidades diferentes para cada classe. Um lambda unico forcaria o agente a operar no menor denominador comum (observe para tudo porque troubleshooting e dificil) ou no maior risco (own para tudo porque tickets simples sao faceis). Cada classe de tarefa tem seu proprio lambda, seu proprio gate, e sua propria progressao.

2. **O professor precisa ser estavel antes de reduzir lambda.** Se o professor (humano, agente experiente, ou demonstracao) produz rollouts inconsistentes ou de baixa qualidade, reduzir lambda so introduz ruido. Valide a qualidade do professor primeiro: taxa de acerto do professor > 0.90 na classe de tarefa, consistencia entre rollouts do professor para o mesmo prompt, e cobertura do professor sobre o espaco de entrada.

3. **Importance sampling e obrigatorio, nao opcional.** Amostrar de uma mistura teacher/agent sem importance sampling produz uma distribuicao de treinamento que nao converge para o alvo. O weight corrige o vies de amostragem. Sem importance sampling, o agente aprende a distribuicao de amostragem, nao a distribuicao desejada.

4. **O gate de observe→assist e o mais importante.** E o ponto onde o agente passa de "aprender com o professor" para "aprender com os proprios erros". Se o agente nao consegue recuperacao basica, avancar para assist introduz prefix drift sem mecanismo de correcao. Seja conservador neste gate: e preferivel ficar em observe por mais tempo do que avancar prematuramente.

5. **Rollback e feature, nao falha.** Um rollback de lambda (ex: own → assist) nao significa que o curriculo falhou -- significa que o curriculo funcionou: detectou degradacao e respondeu. O rollback deve ser automatico (metricas disparam, lambda ajusta) e visivel (dashboard mostra o evento com a evidencia). Times que tratam rollback como falha tendem a desabilitar o rollback -- e ai o agente opera em own com metricas degradadas.

6. **O curriculo compoe com avaliacao externa.** Lambda controla a proporcao de rollouts, mas nao substitui a necessidade de um avaliador independente. Use [[docs/canonical/generator-evaluator|Generator-Evaluator]] ou [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] como avaliador externo para as metricas de gate. O professor nao pode ser o avaliador -- isso criaria um ciclo de vies.

7. **Demonstracoes podem sobre-ajustar.** Se o professor produz demonstracoes muito especificas (ex: sempre o mesmo caminho de resolucao para o mesmo tipo de ticket), o agente aprende a imitar o caminho, nao a resolver o problema. Introduza diversidade nas demonstracoes do professor: multiplos caminhos para o mesmo outcome, cenarios de erro com recuperacao, e variacao nos inputs.

## Integration with Existing Repo Infrastructure

O autonomy-curriculum-sampling conecta a infraestrutura de evolucao de harness e curriculo de aprendizado com um mecanismo operacional de controle de autonomia:

| Componente Existente | Como o Autonomy Curriculum Sampling complementa |
|---|---|
| [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] | O harness evolution gerencia componentes do harness (BUILD → STABILIZE → SIMPLIFY → REMOVE). O autonomy curriculum gerencia a autonomia do agente (observe → assist → own). Sao ciclos paralelos e complementares: o harness pode estar em STABILIZE enquanto o agente esta em observe. |
| [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] | O automation wedge define validacao antes de broad rollout. O autonomy curriculum define o schedule de autonomia durante o rollout. O wedge diz "quando" implantar; o curriculo diz "como" operar apos implantado. |
| [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] | O progressive disclosure carrega skills sob demanda. O autonomy curriculum controla a proporcao de rollouts auto-gerados. Ambos usam progressao gradual, mas em dominios diferentes: contexto vs. autonomia. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Generator-Evaluator fornece o avaliador externo para as metricas de gate do curriculo. O avaliador e independente do professor, prevenindo vies de auto-avaliacao. |
| [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] | Para gates de alta criticidade (ex: transicao assist→own em tarefas de seguranca), o council fornece avaliacao com diversidade de modelos, reduzindo o risco de um unico avaliador ter vies. |
| [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] | A compartimentalizacao garante que o agente nao ve os criterios de avaliacao. Isso e critico para o curriculo: se o agente sabe quais metricas controlam lambda, ele pode otimizar para os gates em vez de para o outcome. |
| [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] | O sampling de producao captura tracos reais que alimentam o curriculo. Rollouts do agente em producao (mesmo sob supervisao) sao a fonte de dados para calibrar lambda e avaliar gates. |
| [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] | A correlacao eval→producao valida que as metricas de gate do curriculo (medidas em ambiente de eval) continuam predizendo comportamento em producao. Se a correlacao quebra, os gates podem estar dando falsa confianca. |
| [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] | Falhas detectadas durante rollouts do agente (especialmente na fase assist, onde o agente gera a maioria dos rollouts) alimentam o loop de classificacao. Cada classe de falha pode informar ajustes no curriculo: lambda mais conservador, mais demonstracoes de recuperacao, ou split da classe de tarefa. |

## Quality Gates

Antes de declarar o curriculo de autonomia como operacional, verifique:

- [ ] Cada classe de tarefa tem lambda inicial, thresholds de gate, e schedule policy definidos e documentados
- [ ] O professor (humano, agente experiente, ou demonstracoes) foi validado: taxa de acerto > 0.90, consistencia entre rollouts, cobertura do espaco de entrada
- [ ] Importance sampling esta implementado e corrige o vies de amostragem para todos os rollouts (teacher e agent)
- [ ] O avaliador externo e independente do professor (nao e o mesmo agente, modelo, ou humano)
- [ ] Metricas de gate (success_rate, autonomous_recovery_rate, unsafe_action_rate, evaluator_confidence) sao calculadas por classe de tarefa, nao agregadas
- [ ] Rollback automatico esta configurado: violacao de seguranca → lambda = 1.0 imediato; degradacao de qualidade → lambda volta ao gate anterior
- [ ] Dashboard mostra lambda atual por classe de tarefa, historico de gates (pass/fail/rollback), e tendencias de metricas
- [ ] O gate observe→assist foi validado com rollouts do agente em ambiente controlado antes de ser aplicado em producao
- [ ] Lambda minimo para tarefas criticas (seguranca, financeiro, dados sensiveis) e > 0 (sempre ha alguma supervisao)
- [ ] O curriculo e revisado periodicamente (mensal ou trimestral) para ajustar thresholds com base em dados acumulados
- [ ] Ha um plano de contingencia para "lambda continua em 1.0 apos N periodos" -- investigar se a classe de tarefa e muito dificil, o professor e inadequado, ou os thresholds sao irreais

## References

- [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]:90-96 — Teacher-mixed sampling, GKD lambda dial, DistiLLM adaptive schedule
- [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]:40-63 — Pattern 2: Autonomy Curriculum Sampling (inputs, outputs, benefits, limitations)
- [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|Policy Distillation Classification]]:71-97 — Classificacao como Missing (Medium integration value)
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — ciclo de evolucao de componentes do harness (complementar ao curriculo de autonomia)
- [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] — validacao antes de broad rollout
- [[docs/canonical/generator-evaluator|Generator-Evaluator]] — separacao geracao/avaliacao (avaliador externo para metricas de gate)
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — council para gates de alta criticidade
- [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] — compartimentalizacao que previne gaming dos gates
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — captura de tracos de producao para alimentar o curriculo
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — validacao de que metricas de gate predizem comportamento em producao
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — classificacao de falhas detectadas nos rollouts do agente

---

*Created: 2026-06-16 | Source: The Imitation Game — State of Policy Distillation in Language — Pattern 2 (Missing, Medium value)*
