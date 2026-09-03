---
name: capability-escalation-ladder
description: "Procedimento de decisao ordenado para tarefas que o agente falha: explorar quatro rungs de escalonamento de capability na ordem de custo de teste crescente — (1) modelo maior, (2) reasoning budget (adaptive thinking / mais tokens de raciocinio), (3) instrucao melhorada, (4) decomposicao arquitetural (generator/evaluator/repairer) — medindo eval pass/fail, violation counts, tokens e latencia em CADA rung, e escolhendo entre as rotas que passam pelo vencedor ECONOMICO, nao pela primeira que passou. Previne pular direto para modelo maior (passa no eval mas triplica custo/latencia) e sequencias ad hoc de alavancas guiadas por preferencia. O rung de decomposicao tipicamente vence na economia — o argumento medido do harness-over-model. Usar quando um agente falha tarefas dificeis no eval, quando o time discute 'trocar de modelo vs melhorar o prompt vs decompor', ou quando uma rota passou no eval mas o custo/latencia ficou inaceitavel. Dispara com: 'capability escalation ladder', 'escalation ladder', 'bigger model', 'larger model', 'model upsizing', 'reasoning budget', 'adaptive thinking', 'thinking budget', 'decomposition vs bigger model', 'economic winner', 'cost per passing route', 'failed task lever', 'qual alavanca puxar', 'escalonar capability', 'rung', 'decomposicao arquitetural', 'harness over model medido', 'violation counts por rung', 'instrucao vs arquitetura'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: troubleshooting
  priority: high
  source: "The Prompting Playbook — Pattern 6: Capability Escalation Ladder"
---

## What I Do

Eu substituo o chute por um procedimento. Quando um agente falha uma tarefa dificil, existem quatro alavancas: modelo maior, mais raciocinio, instrucao melhor, decomposicao arquitetural. Times sem procedimento puxam a alavanca da semana (tipicamente o modelo maior, porque e a mais facil de configurar) e nunca descobrem que outra rota passaria nos mesmos casos por uma fracao do custo.

Eu oriento a exploracao por custo de TESTE crescente:

| Rung | Alavanca | O que muda | Custo de testar | Custo de operar |
|---|---|---|---|---|
| 1 | Capability (modelo maior) | Troca do modelo por um mais capaz | Minimo (config + re-run do eval) | Alto (tokens/preco por token) |
| 2 | Reasoning budget (adaptive thinking) | Mais tokens/tempo de raciocinio no MESMO modelo | Minimo (config + re-run) | Medio-alto (tokens) |
| 3 | Instrucao | Prompt melhor: estrutura, exemplos, self-check | Baixo (edicao de prompt) | Nenhum adicional |
| 4 | Arquitetura (decomposicao) | Quebrar a mega-tarefa em passos simples (ex.: generator/evaluator/repairer) | Alto (engenharia, 3 prompts em vez de 1) | Tipicamente o MENOR por caso |

Em cada rung eu exijo o mesmo registro: eval pass/fail, violation counts, tokens por caso, latencia. Rungs que nao passam avancam o ladder; entre as rotas QUE PASSAM, a decisao final e economica — e no caso-fonte, o ultimo rung (decomposicao) passou tudo no menor custo. O ladder so e executavel com eval suite existindo ANTES (veja a regra 1): sem eval, comparar rungs e vibes.

Dois sinais direccionais guiam o percurso: violation counts (uma rota pode reduzir violacoes sem ainda passar — sinal de melhoria de capability) e a classe da falha (truncamento com raciocinio enriquecido e budget failure, nao quality failure — nao confundir com capability gap).

## When to Use Me

Carregue esta skill quando:

- Um agente falha consistentemente uma classe de tarefa dificil no eval (extracao complexa, raciocinio multi-passo, formato exigente) e o time precisa decidir qual alavanca puxar
- A discussao da equipe e "trocar de modelo vs melhorar o prompt vs decompor o problema" sem dados de custo por rota
- Uma rota ja passou no eval mas o custo ou a latencia ficou inaceitavel (triplicou tokens) — pass/fail sozinho nao decide
- Voce quer o argumento MEDIDO do harness-over-model: a decomposicao que passa nos mesmos casos por menor custo
- Violation counts estao estagnados ou caindo devagar e voce precisa decidir se continua investindo no rung atual ou avanca
- Um self-check ou instrucao melhorou parcialmente (ex.: 0/5 para 2/5) e a pergunta e se o proximo passo e mais prompt ou arquitetura

Nao use quando:

- Nao existe eval suite para a tarefa. O ladder compara rungs contra uma medida; sem eval, cada rung e uma opiniao. Construa o eval primeiro ([[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]], [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]])
- A falha e runtime, nao de capability: crash, timeout de infraestrutura, API fora do ar. Isso pertence ao [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] (retry, fallback, escalada humana) — um ladder diferente que nao compartilha rungs com este
- A tarefa JA PASSA e a questao e custo de roteamento entre subtarefas que funcionam — isso e [[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]] (tiering roteia o que funciona; ladder escala o que falha)
- A decisao e entre dois modelos candidatos para o portfolio geral, nao para uma tarefa que falha — isso e o gate do [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] (o rung 1 do ladder reusa a disciplina do gate, mas o escopo e uma tarefa)

## The Anti-Pattern

```
ANTI-PATTERN: Pular direto para o modelo maior (ou para a alavanca
favorita da semana) sem explorar os rungs mais baratos nem medir
custo/latencia por rota.

Cenario:
  1. Um agente de extracao falha 5/5 casos dificis: raciocinia
     sobre o problema mas submete trabalho nao verificado, viola
     formato, nao termina dentro do output limit.
  2. O time discute dez minutos. Alguem diz "o modelo e fraco".
     O modelo maior esta a um flag de config de distancia.
  3. Rung 1 sozinho: trocam para o modelo maior. Passa 5/5 no
     eval. Ship.
  4. Tres meses depois, o financeiro reclama: tokens por caso
     triplicaram, latencia p50 dobrou, e o volume cresceu. A rota
     que passa e tambem a mais cara possivel — e ninguem sabe se
     havia alternativa, porque nenhuma foi medida.
  5. Paralelo nunca executado: decompor em tres prompts simples
     (generator, evaluator, repairer) teria passado os mesmos 5/5
     com MENOS tokens e MENOR latencia que a linha de base — o
     resultado do caso-fonte. A rota mais cara passou primeiro
     porque era a mais facil de TESTAR, e ninguem olhou alem dela.

Variante igualmente comum (sequencia ad hoc):
  1. Sem procedimento, a ordem das alavancas segue a preferencia
     de quem esta na sala: um mes de prompt-tuning, depois
     "nao deu", depois o modelo maior "so para testar", depois o
     output limit duplicado ("passou no eval" — e destruiu a
     economia de tokens sem ninguem registrar).
  2. Nenhum rung teve violation counts ou custo medidos; duas
     iteracoes se perdem; a decisao final nao e reproduzivel.

Consequencia:
  - Ship de rotas que passam evals mas falham economics
  - O vencedor economico (tipicamente decomposicao) nunca e
    descoberto porque nunca e testado
  - Decisoes nao reproduziveis: ninguem sabe por que a rota atual
    e a atual
  - O argumento harness-over-model do repositorio fica retorica —
    sem medicao, "decomposicao ganha" e fe, nao fato
```

## The Pattern

```
PATTERN: Exploracao ordenada de quatro rungs por custo de teste
crescente, com registro padrao por rung (eval, violation counts,
tokens, latencia) e decisao final economica entre as rotas que
passam.

Fluxo:

  Tarefa falhando + eval suite + violation counts conhecidos
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ REGISTRO PADRAO (por rung, obrigatoria)                  │
  │                                                         │
  │   rung | mudanca feita | pass/fail | violation count     │
  │        | tokens/caso   | latencia p50 | custo eng.       │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ RUNG 1: CAPABILITY (modelo maior)                        │
  │                                                         │
  │ Trocar o modelo (ou subir de tier no mesmo provider) e   │
  │ re-rodar o eval. Minimo esforco de teste.                │
  │                                                         │
  │ Sinais: pass direto? violation counts caem sem passar    │
  │ (capability melhorando)? Custo por caso a partir daqui   │
  │ e o teto a bater.                                       │
  │ Disciplina do rung: comparacao por caso do               │
  │ [[docs/canonical/model-switching-architecture-           │
  │ enterprise-eval-gate|Eval Gate]] (regressoes por         │
  │ categoria, nao so media).                                │
  └─────────────────────────────────────────────────────────┘
       │  se passou → registrar custo e CONTINUAR o ladder
       │  (passar nao encerra: a rota passa, a economia ainda
       │   nao foi comparada)
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ RUNG 2: REASONING BUDGET (adaptive thinking)             │
  │                                                         │
  │ MESMO modelo, mais tokens/tempo de raciocinio. Tambem    │
  │ config + re-run.                                         │
  │                                                         │
  │ CUIDADO diagnostico: truncamento com raciocinio          │
  │ enriquecido e BUDGET FAILURE (output limit), nao quality │
  │ failure. Resolver truncamento inflando max tokens passa  │
  │ o eval e destrui a economia — registre tokens/latencia   │
  │ antes de aceitar.                                       │
  └─────────────────────────────────────────────────────────┘
       │  se passou → registrar e continuar
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ RUNG 3: INSTRUCAO                                        │
  │                                                         │
  │ Prompt melhorado: estrutura seccionada, exemplos,        │
  │ self-check antes de submeter. Custo de teste baixo       │
  │ (edicao), custo operacional zero.                        │
  │                                                         │
  │ Expectativa calibrada: lift parcial e comum (no          │
  │ caso-fonte, 0/5 → 2/5). Lift parcial NAO e fracasso —    │
  │ e sinal direcional; registre e avance se nao passar.     │
  │ Mudanca registrada como mudanca causal ([[docs/canonical/│
  │ prompt-as-code-causal-change-management|Prompt-as-Code]]).│
  └─────────────────────────────────────────────────────────┘
       │  se passou → registrar e continuar
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ RUNG 4: ARQUITETURA (decomposicao)                       │
  │                                                         │
  │ Quebrar a mega-tarefa em passos simples com prompts      │
  │ independentes: generator (rascunho) → evaluator (verifi-│
  │ ca cada regra com evidencia) → repairer (correcoes       │
  │ direcionadas pelas violacoes) — [[docs/canonical/        │
  │ generator-evaluator|Generator-Evaluator]]. Custo de      │
  │ engenharia alto (3 prompts, loop), custo por caso        │
  │ tipicamente o menor.                                     │
  │                                                         │
  │ No caso-fonte: este rung passou TODOS os casos com menos │
  │ tokens e menor latencia que os rungs 1-2.                │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ DECISAO FINAL: VENCEDOR ECONOMICO ENTRE AS ROTAS QUE     │
  │ PASSAM                                                   │
  │                                                         │
  │   rotas_que_passaram = [r1?, r2?, r3?, r4?]              │
  │   para cada uma: tokens/caso, latencia p50, custo de     │
  │   manutanca (prompts/loops a manter), risco (acoplamento │
  │   a um modelo caro vs harness portavel)                  │
  │                                                         │
  │ Escolha: a rota que passa com a melhor economia —        │
  │ tipicamente a decomposicao. NUNCA a primeira que passou, │
  │ so por ter passado primeiro.                             │
  │                                                         │
  │ A tarefa que falhou vira caso permanente do eval        │
  │ ([[docs/canonical/living-eval-dataset|Living Eval        │
  │ Dataset]]): o proximo ladder comeca com ela ja travada. │
  └─────────────────────────────────────────────────────────┘
```

### Exemplo de Registro Preenchido (caso-fonte, forma ilustrativa)

| Rung | Mudanca | Pass/fail | Violations | Tokens/caso | Latencia p50 | Eng. |
|---|---|---|---|---|---|---|
| Base | — | 0/5 | alto | 1.0x | 1.0x | — |
| 1. Modelo maior | troca de modelo | 5/5 | 0 | 3.1x | 2.4x | config |
| 2. Reasoning budget | +thinking tokens | 5/5 (truncou 1) | 1 | 2.8x | 2.1x | config |
| 3. Instrucao | self-check + estrutura | 2/5 | medio | 1.2x | 1.1x | 1 dia |
| 4. Decomposicao | gen/eval/repair | 5/5 | 0 | 0.9x | 0.8x | 1 semana |
| **Decisao** | **rung 4** — passa tudo, menor custo/latencia que a base; rungs 1-2 passam falando economics | | | | | |

## Implementation Rules

1. **Sem eval, o ladder nao roda.** O pre-requisito absoluto e o eval suite com violation counts ANTES do primeiro rung ("Meaningless without eval infrastructure to compare rungs" — patterns doc, limitacoes). Sem ele, cada rung e uma opiniao carinnosa. Primeiro consulta: existe suite? Se nao, construa (3-layer eval, golden questions) e so entao escale.

2. **A ordem e por custo de TESTE crescente, nao por custo de operacao.** O modelo maior vem primeiro porque e o mais barato de TENTAR (flag de config), nao porque e a melhor decisao. Custo de operacao entra so no final, na comparacao economica — e e onde o modelo maior quase sempre perde.

3. **Passar o eval nao encerra o ladder.** O ladder continua ate o rung 4 mesmo com rungs anteriores passando, porque pass/fail nao decide: "Early rungs can pass evals at unacceptable cost; pass/fail alone does not decide" (patterns doc). Encerrar no primeiro pass e o anti-pattern com cerebro.

4. **Violation counts sao o sinal direcional entre rungs.** Uma rota que reduz violations sem passar esta melhorando capability — registre e use para decidir se vale mais um incremento no rung atual ou avancar. Pass/fail binario esconde esse gradiente.

5. **Truncamento com raciocinio enriquecido e budget failure, nao quality failure.** No rung 2/3, raciocinio maior colide com output limit fixo. Diagnosticar como capability gap leva a inflar max tokens — rota que passa o eval e destrroi a economia de tokens/latencia. Verifique a classe da falha antes de escolher o proximo incremento.

6. **Rung 4 e o default provavel, confirmado por medicao.** A decomposicao ganhou no caso-fonte e e o argumento central do repositorio (harness-over-model). Mas o default e hipotese a confirmar pelo registro preenchido, nao fe: ha tarefas em que o rung 1-2 com custo toleravel e a decisao certa (engenharia zero, maintenabilidade zero).

7. **Cada rung e uma mudanca causal registrada.** Rungs 3 e 4 editam prompts/harness: trigger, diagnostico, intencao via [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]. O registro do ladder dobra como patch ledger para a proxima migracao de modelo — as compensacoes criadas no rung vencedor sao candidatas a obsolescencia quando o modelo melhorar ([[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]).

8. **Custo de manutencao entra na comparacao economica.** Tres prompts e um loop (rung 4) sao mais manutencao que um flag (rung 1). A decisao economica compara o custo total — tokens, latencia, engenharia de manutencao, risco de acoplamento a um modelo especifico — nao so o custo por chamada.

## Integration with Existing Repo Infrastructure

O capability escalation ladder unifica os canonicals de tiering, prompt e decomposicao do repositorio sob um protocolo de decisao unico — a medida que faltava para o thesis harness-over-model:

| Componente Existente | Como o Capability Escalation Ladder complementa |
|---|---|
| [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] | O eval gate define a disciplina de comparacao por caso entre modelos candidatos (:43-59, Switch/Hold/Hybrid :61-71). O rung 1 do ladder REUSA essa disciplina, com escopo reduzido: uma tarefa que falha, nao o portfolio. O ladder adiciona o que falta ao gate: a ordenacao contra os outros tres rungs e a decisao economica final. |
| [[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]] | O tiering roteia subtarefas QUE FUNCIONAM para o tier certo por custo/latencia (:32). O ladder e o complemento para tarefas que FALHAM: primeiro escala ate passar (rungs), depois o tiering otimiza a rota vencedora em producao. Sequencia: ladder decide o how, tiering refina o how much. |
| [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] | Distincao obrigatoria: aquele ladder ordena FALHA RUNTIME (classify, retry, safe fallback, escalada humana, :29); este ordena INVESTIMENTO DE CAPABILITY para uma tarefa que falha no eval. Nao compartilham rungs; confundir os dois manda crash de infra para prompt-tuning e tarefa incapaz para retry. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O rung 4 INSTANCIA este canonical: generator produz rascunho, evaluator verifica cada regra com evidencia (:31), e o repairer fecha o loop com correcoes direcionadas. O ladder fornece o quando: decomposicao so entra depois que os rungs 1-3 foram medidos. |
| [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] | Variante de decomposicao para o rung 4 quando a falha e de coordinacao multi-passo (Verify valida steps contra success gates, :68-72) em vez de qualidade de artefato unico. |
| [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] | E a infraestrutura pre-requisito (regra 1): Layer 1 deterministica (:30-43) e Layer 2 semantica (:45-59) produzem o pass/fail e os violation counts que cada rung registra. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A matriz de verificacao por constraint (:31-33) e a fonte dos violation counts por regra — o sinal direcional que diferencia melhoria de capability de estagnacao entre rungs. |
| [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] | O rung 4 e harness evolution medido: BUILD porque o modelo atual tem a fraqueza, medir o payoff, re-avaliar quando o modelo melhorar. O ladder adiciona a comparacao explicita contra as rotas de modelo que o lifecycle nao cobre. |
| [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] | O rastro do ladder vira insumo do split pos-migracao: cada compensacao criada no rung vencedor (Context Loader, verifier extra) tem custo medido (:23) e e candidata a remocao quando um modelo melhor elimina a fraqueza que a justificou. |
| [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]] | Rungs 3 e 4 sao mudancas de prompt/harness com as tres perguntas causais obrigatorias (:32-59). O registro do ladder e o ledger que a proxima migracao audita. |
| [[docs/canonical/living-eval-dataset|Living Eval Dataset]] | A tarefa que falhou e fez o ladder rodar vira caso permanente do dataset (:28) — o custo de um ciclo de escalonamento se paga travando a regressao para sempre. |
| [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] | O rung 3 edita os blocos do harness prompt (role, policy, formato, :22); o rung 4 redistribui responsabilidades entre os prompts decompostos mantendo o contrato estavel do harness. |

## Quality Gates

Antes de declarar o ciclo de escalonamento concluido, verifique:

- [ ] O eval suite existia ANTES do primeiro rung (com baseline de pass/fail e violation counts registrado)
- [ ] Os quatro rungs foram testados NA ORDEM (capability → budget → instrucao → arquitetura), ou o desvio de ordem tem justificativa registrada
- [ ] Cada rung tem o registro padrao completo: mudanca, pass/fail, violation counts, tokens/caso, latencia, custo de engenharia
- [ ] Nenhuma rota foi declarada vencedora por passar primeiro — a decisao final compara TODAS as rotas que passaram em custo, latencia e manutencao
- [ ] Truncamento com raciocinio enriquecido foi classificado como budget failure antes de qualquer decisao de inflar output limit (e o custo da inflamcao foi registrado)
- [ ] Lift parcial de instrucao (ex.: 0/5 → 2/5) foi registrado como sinal direcional, nao descartado como fracasso
- [ ] As mudancas de prompt/harness dos rungs executados foram registradas como mudancas causais (trigger/diagnostico/intencao) com rollback
- [ ] As compensacoes criadas no rung vencedor ficaram marcadas para re-auditoria na proxima migracao de modelo (invariant-compensation split)
- [ ] A tarefa que falhou entrou no eval suite como caso permanente de regressao
- [ ] A decisao final e reproduzivel por quem nao estava na sala: o registro sozinho conta por que a rota escolhida e a escolhida

## References

- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:112-130 — Pattern 6: Capability Escalation Ladder (inputs, outputs, benefits, limitations)
- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:106-116 — Classificacao como Missing (High integration value): rungs existem separados, a ordenacao e a comparacao economica nao
- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:231-249 — Pattern 12 (Self-Check Reasoning Instruction): o rung 3 como lever parcial e o truncamento como budget failure
- [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]:43-59, :61-71 — disciplina de comparacao por caso e decisao estruturada que o rung 1 reusa
- [[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]]:32 — tiering por subtarefa para tarefas que funcionam (complemento pos-ladder)
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29 — o ladder de falha RUNTIME, distinto deste
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31, :116 — rung 4 como instancia do padrao generate/evaluate/reject
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:68-72 — variante de decomposicao com Verify contra success gates
- [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]:30-43, :45-59 — infraestrutura de eval pre-requisito
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:31-33 — matriz de verificacao como fonte dos violation counts
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:44 — BUILD defensivo e re-avaliacao medida do harness
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:23 — custo medido de compensacoes obsoletas pos-melhoria de modelo
- [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]:32-59 — registro causal dos rungs 3-4
- [[docs/canonical/living-eval-dataset|Living Eval Dataset]]:28 — a tarefa falha vira caso permanente
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:22 — blocos que o rung 3 edita

---

*Created: 2026-09-02 | Source: The Prompting Playbook — Pattern 6 (Missing, High value)*
