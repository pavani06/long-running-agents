---
name: shadow-review-pipeline
description: "Executa um revisor AI em modo shadow nao-bloqueante ao lado de revisores humanos, coleta metricas de concordancia (true positive, false positive, missed-by-human, missed-by-AI), e usa dados do periodo de shadow para graduar checks especificos de AI a status bloqueante. Des-risca a adocao de revisao agentica porque o workflow humano nao muda durante a medicao. Usar ao introduzir revisao AI em um fluxo de PR existente, ao decidir quais checks de AI podem bloquear merge, ou quando precisar de evidencia de confiabilidade antes de mudar gates de revisao. Dispara com: 'shadow review', 'AI review shadow', 'shadow pipeline', 'review agreement metrics', 'AI reviewer trust', 'graduar AI reviewer', 'non-blocking AI review', 'shadow period', 'agreement rate', 'review shadow mode', 'AI review graduation', 'pipeline de shadow', 'confianca em AI review', 'reviewer agreement'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: governance
  priority: high
  source: "Canary Test Code Review (extracted via analyze-and-improve pipeline, 2026-06-15)"
---

## What I Do

Eu executo um revisor AI em modo shadow — o revisor AI analisa cada PR ou mudanca proposta, produz findings estruturados, mas nenhum finding bloqueia o merge. Ao mesmo tempo, revisores humanos produzem seus outcomes normalmente. Eu comparo os dois conjuntos de findings e classifico cada resultado em uma de quatro categorias de concordancia:

1. **True Positive (TP)**: AI e humano concordam que e um problema real.
2. **False Positive (FP)**: AI reportou, mas humano determinou que nao e um problema (ou nao e acionavel).
3. **Missed by Human**: AI encontrou algo que o humano nao viu — e, apos revisao, confirmou-se que e um problema real.
4. **Missed by AI**: O humano encontrou algo que o AI nao viu.

Durante o shadow period configurado, eu acumulo essas metricas por categoria de check (seguranca, correcao, estilo, performance, etc.) e por modulo ou arquivo. Ao final do periodo, os dados respondem a tres perguntas:

- Quais checks de AI adicionam valor real (alta taxa de TP, baixa taxa de FP)?
- Quais checks criam ruido (alta taxa de FP, baixo valor incremental)?
- Em quais modulos o AI reviewer e mais e menos confiavel?

Com esses dados, a decisao de quais checks de AI podem se tornar bloqueantes deixa de ser opiniao e passa a ser evidencia observada no workflow real do time.

## When to Use Me

Carregue esta skill quando:

- Voce esta introduzindo um revisor AI em um fluxo de PR existente e quer medir confiabilidade antes de torná-lo bloqueante
- Um time ou stakeholder pergunta "o AI reviewer e bom o suficiente para confiar como gate?"
- Voce precisa decidir quais categorias de check de AI (seguranca, correcao, estilo) podem bloquear merge e quais devem permanecer como sugestao
- O volume de revisao e suficiente para produzir dados de concordancia estatisticamente uteis (dezenas de PRs, nao unidades)
- Os findings do AI reviewer sao estruturados o suficiente para serem comparados com outcomes humanos (idealmente via [[docs/canonical/constraint-anchored-evaluation|constraint-anchored evaluation]])
- Voce quer evidencia de que o AI reviewer nao esta introduzindo falsa confianca ("o AI aprovou, entao deve estar certo")
- O time reporta fadiga de revisao com falsos positivos do AI e voce precisa de dados para calibrar

Nao use quando:

- O AI reviewer ja opera como gate bloqueante com historico de confiabilidade validado — o shadow period ja passou
- O volume de PRs e muito baixo para produzir metricas de concordancia significativas (menos de ~20 PRs no periodo)
- Os findings do AI sao puramente freeform e nao podem ser comparados sistematicamente com outcomes humanos — resolva isso primeiro com um contrato de revisao estruturado
- Voce precisa de protecao bloqueante imediata (o shadow period, por definicao, nao bloqueia nada) — combine com [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] para checks ja validados
- A pergunta e exclusivamente sobre custo ou latencia do AI reviewer (use [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] para dimensionamento operacional)

## The Anti-Pattern

```
ANTI-PATTERN: Ligar o AI reviewer como gate bloqueante sem shadow period,
confiando que "parece bom" e substituindo a calibracao por intuicao.

Cenario:
  1. O time implanta um AI reviewer que bloqueia merge em todas as categorias:
     seguranca, correcao, estilo, performance.
  2. Nas primeiras duas semanas, o AI reviewer gera 15 falsos positivos.
     Desenvolvedores comecam a desabilitar o gate localmente ou a
     marcar "skip" sem ler.
  3. Na terceira semana, um true positive de seguranca e ignorado porque
     "o AI sempre reclama de coisa que nao importa".
  4. O bug de seguranca vai para producao. O AI reviewer estava certo,
     mas ninguem confiava mais nele.

Consequencia:
  - O AI reviewer perdeu credibilidade antes de ter chance de prova-la
  - Falsos positivos queimaram a confianca que true positives posteriores
    precisavam
  - O time aprendeu a ignorar o AI, nao a usa-lo
  - Nao ha dados para saber se o problema e o AI reviewer, o prompt,
    as categorias, ou a cultura de revisao do time
```

O ponto de falha nao e a qualidade do AI reviewer — ele encontrou o bug de seguranca. A falha e de processo: o AI reviewer foi promovido a gate antes que houvesse evidencia de que o time confiava nele e de que a taxa de falsos positivos era aceitavel para o contexto.

## The Pattern

```
PATTERN: Shadow period com metricas de concordancia antes da graduacao a gate.

Fluxo:

  AI reviewer configurado
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. SHADOW MODE ATIVADO                                   │
  │                                                         │
  │ - AI reviewer analisa cada PR/mudanca                    │
  │ - Findings sao registrados em log sink ou dashboard      │
  │ - NENHUM finding bloqueia merge                          │
  │ - Revisores humanos operam normalmente                   │
  │ - Duracao do shadow period e declarada (ex: 4 semanas    │
  │   ou N PRs, o que vier primeiro)                         │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. CLASSIFICACAO DE CONCORDANCIA                         │
  │                                                         │
  │ Para cada PR, compara-se AI findings vs. human outcomes: │
  │                                                         │
  │  Categoria            Definicao                          │
  │  ─────────────────────────────────────────────────────  │
  │  True Positive (TP)   AI e humano concordam: e um        │
  │                       problema real                      │
  │  False Positive (FP)  AI reportou, humano determinou     │
  │                       que nao e problema                 │
  │  Missed by Human      AI encontrou, humano nao viu,      │
  │                       confirmou-se ser problema real     │
  │  Missed by AI         Humano encontrou, AI nao viu       │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. ACUMULACAO DE METRICAS                                │
  │                                                         │
  │ Metricas sao segmentadas por:                            │
  │ - Categoria de check (seguranca, correcao, estilo,       │
  │   performance, data integrity)                           │
  │ - Modulo ou arquivo (ex: payment/, auth/, admin/)        │
  │ - Severidade do finding (critical, high, medium, low)    │
  │                                                         │
  │ Metricas calculadas:                                     │
  │ - Precision = TP / (TP + FP)                             │
  │ - Recall = TP / (TP + Missed-by-AI)                      │
  │ - Value-add = Missed-by-Human / Total AI findings        │
  │ - Noise ratio = FP / Total AI findings                   │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. DECISAO DE GRADUACAO                                  │
  │                                                         │
  │ Ao final do shadow period, cada categoria de check       │
  │ recebe uma decisao baseada em thresholds:                │
  │                                                         │
  │  Metrica               Graduar se...                     │
  │  ─────────────────────────────────────────────────────  │
  │  Precision             > 70% (menos de 30% FP)           │
  │  Recall                > 60% (nao deixa passar muito)   │
  │  Value-add             > 10% (encontra coisas que        │
  │                         humanos estao perdendo)           │
  │  Noise ratio           < 20% (nao polui o fluxo)        │
  │                                                         │
  │ Categorias que passam → gate bloqueante.                 │
  │ Categorias que falham → permanecem shadow ou vao para    │
  │                         recalibracao de prompt.          │
  │ Categorias com alta FP sistematica → revisar prompt,     │
  │                         escopo, ou descontinuar.          │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 5. FEEDBACK LOOP                                         │
  │                                                         │
  │ - False positives sao usados para refinar o prompt       │
  │   do AI reviewer                                         │
  │ - Missed-by-AI findings sao usados para expandir o       │
  │   escopo de checks                                       │
  │ - Dados de concordancia por modulo alimentam o            │
  │   [[.opencode/skills/contextual-severity-calibration/SKILL|Contextual Severity Calibration]] │
  │ - Metricas historicas permitem detectar degradacao       │
  │   do AI reviewer apos mudancas de modelo ou prompt        │
  └─────────────────────────────────────────────────────────┘
```

### Shadow Period Configuration

| Parametro | Recomendacao | Justificativa |
|---|---|---|
| Duracao minima | 4 semanas ou 30 PRs | Volume suficiente para significancia estatistica basica |
| Categorias iniciais | Seguranca, correcao, convencoes de projeto | Comecar com checagens de alto valor e baixa ambiguidade |
| Log sink | Dashboard ou canal dedicado (ex: Slack #ai-review-shadow) | Visibilidade sem interromper o fluxo |
| Revisao de concordancia | Semanal (atribuicao humana de TP/FP/Missed) | Evitar acumulo de backlog de classificacao |
| Threshold de graduacao | Configuravel por time e dominio | Times diferentes toleram diferentes taxas de FP |

### O Que NAO e Shadow Review

| E shadow review | Nao e shadow review |
|---|---|
| AI reviewer roda em paralelo, sem bloquear merge | AI reviewer bloqueia merge desde o dia 1 |
| Concordancia e medida contra outcomes humanos reais | Concordancia e assumida porque "o AI parece certo" |
| Graduacao e baseada em dados do periodo | Graduacao e baseada em intuição ou benchmark sintetico |
| False positives sao tratados como sinal para calibrar | False positives sao tratados como "o time que ignore" |
| Categorias diferentes tem metricas independentes | Todas as categorias sao tratadas como um bloco uniforme |

## Implementation Rules

1. **O shadow period nao bloqueia nada, por definicao.** Se houver necessidade de protecao bloqueante imediata, use checks deterministicos (lint, type-check, testes) ou gates de PR ja validados. O shadow period e exclusivamente para construcao de confianca baseada em evidencia.

2. **A classificacao de concordancia requer julgamento humano.** Nao automatize a classificacao de TP/FP/Missed — e exatamente o julgamento humano que voce esta medindo contra. Um humano (idealmente o revisor do PR) deve classificar cada finding do AI apos a revisao.

3. **Segmente metricas por categoria, nao agregue tudo.** Um AI reviewer pode ter 90% de precisao em seguranca e 30% em estilo. Agregar tudo em uma metrica unica esconde que estilo esta gerando ruido enquanto seguranca esta funcionando. Cada categoria sobe ou desce independentemente.

4. **False positives sao sinal de calibracao, nao de falha.** Um FP nao significa "o AI e ruim" — significa que o prompt, o escopo, ou os thresholds precisam de ajuste. Trate FPs como entrada para o loop de melhoria do reviewer, nao como evidencia para descartá-lo.

5. **O shadow period tem fim declarado.** "Shadow para sempre" nao e shadow — e um reviewer perpétuo que ninguem le porque nao bloqueia nada. Defina uma data ou condicao de termino no inicio. Ao final, tome decisoes concretas: graduar, recalibrar, ou descontinuar.

6. **Missed-by-Human e a metrica de valor mais importante.** Encontrar coisas que o humano tambem encontra (TP) e bom, mas o valor incremental do AI reviewer esta no que ele encontra e o humano nao viu (Missed-by-Human). Se essa metrica e zero apos o shadow period, o AI reviewer nao esta adicionando valor — esta apenas duplicando esforco.

7. **O dashboard do shadow period e publico para o time.** A confianca no AI reviewer se constroi com transparencia. Se o time nao ve as metricas, assume o pior (ou o melhor — ambos sao perigosos).

## Integration with Existing Repo Infrastructure

O Shadow Review Pipeline se integra a infraestrutura de evals e governanca do repositorio como camada de construcao de confianca antes que gates automaticos entrem em operacao:

| Componente Existente | Como o Shadow Review Pipeline complementa |
|---|---|
| [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] | A estratificacao define tiers fast/medium/deep com triggers e thresholds. O Shadow Review Pipeline adiciona uma fase anterior a qualquer tier: o periodo de shadow onde as metricas de concordancia determinam se um check de AI merece entrar em um tier. |
| [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] | O correlation tracking mede se scores de eval continuam prevendo outcomes de producao. O Shadow Review Pipeline produz a linha de base inicial de concordancia que o correlation tracking vai monitorar ao longo do tempo. |
| [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] | O PR-gated enforcement define como evals bloqueiam merge. O Shadow Review Pipeline responde a pergunta anterior: "este eval merece ser PR-gated?" com dados, nao com opiniao. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A avaliacao ancorada em constraints produz findings estruturados e comparaveis. Isso e pre-requisito para o Shadow Review Pipeline: sem findings estruturados, a comparacao AI vs. humano e ambigua e as metricas de concordancia perdem significado. |
| [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] | O ciclo BUILD → STABILIZE → SIMPLIFY → REMOVE do harness. O shadow period corresponde a fase STABILIZE para AI reviewers: coleta de dados, calibracao, e decisao de promocao ou remocao. |
| [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] | O loop de classificacao de falhas categoriza slop e misbehavior. False positives do AI reviewer sao uma categoria de slop que este loop pode capturar e encaminhar para recalibracao. |
| [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] | O gate de progressao por sinais de dor. Se o shadow period revela alta taxa de FP em uma categoria, isso e um pain signal que dispara revisao do prompt ou escopo daquela categoria. |
| [[.opencode/skills/contextual-severity-calibration/SKILL|Contextual Severity Calibration]] | O shadow period produz dados de concordancia por modulo. Esses dados alimentam a calibracao de severidade contextual: modulos onde o AI reviewer tem baixa precisao podem exigir thresholds mais conservadores ou revisao humana obrigatoria. |

## Quality Gates

Antes de declarar o shadow period como concluido e tomar decisoes de graduacao, verifique:

- [ ] O shadow period foi declarado com duracao minima e condicao de termino antes de comecar
- [ ] Todo finding do AI reviewer foi registrado em log sink ou dashboard acessivel ao time
- [ ] Para cada finding do AI, um humano classificou a concordancia (TP, FP, Missed-by-Human, Missed-by-AI)
- [ ] As metricas estao segmentadas por categoria de check (nao agregadas em um score unico)
- [ ] Precision, Recall, Value-add e Noise ratio foram calculadas por categoria
- [ ] Thresholds de graduacao foram definidos antes do periodo (nao ajustados post-hoc para favorecer o resultado desejado)
- [ ] Categorias que passaram nos thresholds tem decisao explicita de graduacao para gate bloqueante
- [ ] Categorias que falharam tem plano de recalibracao (ajuste de prompt, escopo, ou thresholds)
- [ ] Missed-by-Human findings foram revisados para identificar lacunas no processo de revisao humana
- [ ] O time foi comunicado sobre as decisoes de graduacao e a logica por tras delas
- [ ] Dados de concordancia por modulo foram encaminhados para [[.opencode/skills/contextual-severity-calibration/SKILL|Contextual Severity Calibration]]
- [ ] O dashboard do shadow period permanece acessivel como baseline historica para correlation tracking futuro

## References

- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]] — analise fonte dos padroes de code review agentic
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]] — Pattern 1: Shadow Review Pipeline (inputs, outputs, benefits, limitations)
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]] — classificacao como Missing com evidencias de ausencia no repositorio
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — estratificacao fast/medium/deep (shadow period e pre-tier)
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — correlation tracking (shadow data como baseline)
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — enforcement de evals em PRs (destino da graduacao)
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — findings estruturados (pre-requisito para comparacao AI vs. humano)
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — ciclo BUILD → STABILIZE → SIMPLIFY → REMOVE (shadow = STABILIZE)
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — loop de classificacao de falhas (captura de FP para recalibracao)
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — gate de progressao por sinais de dor (FP como pain signal)
- [[.opencode/skills/contextual-severity-calibration/SKILL|Contextual Severity Calibration]] — calibracao de severidade contextual (consome dados de concordancia por modulo)

---

*Created: 2026-06-14 | Source: Canary Test Code Review — Pattern 1 (Missing, Medium value)*
