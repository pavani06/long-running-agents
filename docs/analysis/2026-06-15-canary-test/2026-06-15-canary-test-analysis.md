---
title: "Canary Test — Code Review Patterns for AI-Assisted Development"
type: analysis
tags: ["agentic-coding", "governanca", "decision-discipline", "harness-engineering", "evals", "spec-driven-development"]
date: 2026-06-15
aliases: ["canary test code review", "code review patterns analysis"]
relates-to:
  - "[[.opencode/skills/manual-brake-question-gate/SKILL|manual-brake-question-gate]]"
  - "[[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]]"
  - "[[docs/canonical/constraint-anchored-evaluation|constraint-anchored-evaluation]]"
  - "[[docs/canonical/multi-model-evaluation-council|multi-model-evaluation-council]]"
  - "[[docs/canonical/pr-gated-eval-enforcement|pr-gated-eval-enforcement]]"
sources:
  - "[[sources/2026-06-15-canary-test-code-review-patterns|2026-06-15-canary-test-code-review-patterns.md]]"
---

# Canary Test — Code Review Patterns for AI-Assisted Development

Extracao de conhecimento nao-obvio de patterns praticos para integrar AI reviewers em
workflows de code review.

---

## 1. Frameworks & Models

### AI Reviewer Capability Model — Fast but Shallow

O modelo conceitual subjacente posiciona AI reviewers como verificadores de primeira
passagem: rapidos na deteccao de problemas mecanicos (imports nao usados, type
annotations ausentes, anti-padroes de seguranca) mas incapazes de avaliacao profunda
de arquitetura ou design. A premissa e que AI reviewers sao complementares, nao
substitutos, da revisao humana.

> "AI reviewers are fast but shallow — use them as a first pass, not the only pass."

### Review Triage Model — Three-Question Prompt

O prompt do AI reviewer deve solicitar exatamente tres categorias de achados:
**potential bugs**, **style violations against the project's own conventions**, e
**security concerns**. Essa triagem em tres eixos garante que o humano foque em
arquitetura e decisoes de design, nao em linting.

> "The human reviewer focuses on architecture and design decisions, not linting."

### Risk Stratification Model — Module-Level Profiles

Cada modulo do codigo carrega um perfil de risco declarado em `risk-profile.yaml` no
diretorio do modulo. Os niveis sao: **critical**, **high**, **medium**, **low**. O
perfil declara o nivel de risco e a lista de verificacoes aplicaveis. O AI reviewer le
esse perfil antes de analisar o diff e ajusta a profundidade da analise de acordo.

> "A change to the payment module deserves stricter review than a change to the help
> page copy."

| Risk level | Checks applied |
|---|---|
| Low | Style checks only |
| Medium | Style + basic correctness |
| High | Style + correctness + security |
| Critical | Full security, performance, and data integrity checks |

### Review Contract Model — Structured Checklist

A revisao e transformada de "olhe esse codigo" para "verifique essas 5 propriedades
especificas". O contrato cobre cinco dimensoes: **security surface changes**, **data
model migrations**, **API compatibility**, **error handling coverage**, e **test
coverage for new paths**. Cada item tem status `pass`, `fail`, ou `not-applicable`.

> "This pattern eliminates the 'I didn't know I was supposed to check that' problem."

---

## 2. Patterns & Architectures

### Pattern 1: Pre-Commit Gate

**Mecanica**: Antes de push, o AI reviewer e executado como hook local de pre-commit.
Recebe o diff como input. O prompt e configurado com as tres questoes de triagem
(bugs, style contra convencoes do projeto, seguranca). As convencoes no prompt devem
refletir as regras reais do time, nao defaults genericos da industria.

**Fluxo**:
```
git diff → AI reviewer (prompt: bugs + project conventions + security) → gate: pass/block
```

**Propriedade estrutural**: O gate opera localmente, antes do CI. Isso reduz feedback
loop time e evita poluir o pipeline de CI com problemas triviais.

> "Configure your pre-commit to call the AI with a prompt that includes the diff and
> asks for three specific things."

### Pattern 2: Review Contract as Checklist

**Mecanica**: Todo PR inclui um arquivo `review-contract.yaml` que lista exatamente o
que o revisor deve verificar. O contrato torna a revisao verificavel item a item. AI
reviewers processam cada item do contrato independentemente, retornando resultados
estruturados em vez de comentarios livres.

**Estrutura do contrato**:
```yaml
items:
  - dimension: security_surface
    status: pass | fail | not-applicable
  - dimension: data_model_migrations
    status: pass | fail | not-applicable
  - dimension: api_compatibility
    status: pass | fail | not-applicable
  - dimension: error_handling_coverage
    status: pass | fail | not-applicable
  - dimension: test_coverage_new_paths
    status: pass | fail | not-applicable
```

**Propriedade estrutural**: A decomposicao em itens independentes permite que o AI
reviewer processe cada dimensao em isolamento, produzindo saida estruturada em vez de
comentario livre. Isso reduz ambiguidade e facilita a acao pelo desenvolvedor.

> "AI reviewers more effective because they can process each contract item
> independently, returning structured results instead of freeform commentary."

### Pattern 3: Shadow Review Pipeline

**Mecanica**: O AI reviewer e executado em paralelo com a revisao humana por duas
semanas sem bloquear merges. Os resultados sao apenas registrados em um dashboard. Ao
final do periodo, os dados de concordancia (onde o AI pegou algo que o humano perdeu,
onde gerou falsos positivos) sao usados para decidir quais verificacoes de AI sao
confiaveis o suficiente para bloquear merges.

**Metricas coletadas**:
- **True positives encontrados pelo AI e perdidos pelo humano**: 30-40% dos issues
- **False positives do AI**: 15-20% das flags levantadas
- **Agreement rate**: taxa de concordancia humano-AI por categoria de verificacao

**Fluxo**:
```
PR aberto → [humano revisa] + [AI revisa → dashboard] (2 semanas) → dados → decisao de gating
```

**Propriedade estrutural**: A adocao e de-risked porque o workflow de ninguem muda ate
que haja dados provando que o AI adiciona valor. O shadow period transforma a decisao
de adotar AI review de uma questao de opiniao para uma questao de dados.

> "De-risks adoption because no one's workflow changes until there's data proving the
> AI adds value."

### Pattern 4: Contextual Severity Calibration

**Mecanica**: Cada diretorio de modulo contem um `risk-profile.yaml` que declara o
nivel de risco do modulo e as verificacoes aplicaveis. O AI reviewer le esse perfil
antes de analisar o diff e ajusta a severidade e o conjunto de verificacoes de acordo.

**Estrutura do risk-profile.yaml por modulo**:
```yaml
risk_level: critical | high | medium | low
checks:
  - style
  - correctness
  - security
  - performance
  - data_integrity
```

**Propriedade estrutural**: A calibracao por contexto evita dois extremos: revisao
excessivamente pesada em modulos de baixo risco (fadiga do revisor, falsos positivos
em codigo trivial) e revisao insuficiente em modulos criticos (risco de falha
catastrofica). O custo de revisao e proporcional ao risco real da mudanca.

> "The AI reviewer should calibrate its severity levels based on which module changed."

---

## 3. Operational Lessons

### O que funcionou

1. **Prompt tuning contra convencoes reais do time**: Quando o prompt do AI reviewer e
   ajustado para refletir as convencoes especificas do projeto (nao defaults da
   industria), o output e significativamente menos ruidoso e mais acionavel. O AI deve
   aplicar as regras do time, nao melhores praticas genericas.

   > "The AI should enforce YOUR rules, not industry defaults."

2. **Shadow period como estrategia de adocao**: Executar o AI reviewer sem bloquear
   merges por duas semanas remove a resistencia a mudanca porque ninguem e forcado a
   alterar seu fluxo de trabalho. A transicao so ocorre apoiada em dados.

   > "No one's workflow changes until there's data proving the AI adds value."

3. **Contratos estruturados melhoram AI reviewers**: Transformar a revisao de
   "comente o que achar relevante" em "verifique esses 5 itens especificos" torna AI
   reviewers significativamente mais efetivos. O processamento independente de cada
   item produz resultados estruturados e ageis.

   > "Makes AI reviewers more effective because they can process each contract item
   > independently."

4. **Triagem em tres eixos**: Solicitar bugs + style violations + security concerns
   como categorias fixas de output produz resultados mais focados do que prompts
   abertos.

### Metricas empiricas reportadas

| Metrica | Valor |
|---|---|
| Issues capturados pelo AI que humanos perdem | 30-40% |
| False positives do AI | 15-20% das flags |
| Periodo de shadow recomendado | 2 semanas |

### O que falhou

1. **Output generico e ruidoso**: Quando o prompt do AI reviewer e configurado com
   regras genericas da industria, o output e tao ruidoso que desenvolvedores passam a
   ignora-lo completamente. O padrao de falha e: prompt generico → muito ruido →
   desenvolvedor para de ler → AI reviewer se torna inutil.

   > "Common failure mode: developers start ignoring the AI output because it's too
   > noisy."

---

## 4. Tradeoffs & Design Decisions

### Tradeoff: Velocidade vs. Profundidade na Revisao

**Decisao**: Usar AI reviewer como primeira passagem (rapida, superficial), mantendo o
humano como revisor de arquitetura e design.

**Racional**: AI reviewers sao intrinsecamente rapidos e superficiais. Tentar faze-los
substituir revisao profunda e ineficaz. A alternativa — AI como unico revisor — foi
explicitamente rejeitada. O custo de falsos negativos em decisoes de arquitetura e
alto demais para delegar a AI.

> "AI reviewers are fast but shallow — use them as a first pass, not the only pass."

### Tradeoff: Cobertura vs. Relacao Sinal-Ruido

**Decisao**: Afunilar o prompt do AI para as convencoes reais do time, sacrificando
cobertura de "melhores praticas" genericas em troca de maior taxa de acao sobre os
achados.

**Racional**: Um AI reviewer que reporta 100 issues dos quais 85 sao ignorados e pior
que um AI reviewer que reporta 30 issues dos quais 28 geram acao. A taxa de acao sobre
os findings e a metrica que importa, nao o volume bruto.

> "Fix this by tuning the prompt to match your team's actual conventions, not generic
> best practices."

### Tradeoff: Bloqueio Imediato vs. Adocao Gradual

**Decisao**: Shadow pipeline de 2 semanas com zero bloqueio, seguido de decisao
data-driven sobre quais verificacoes bloquear.

**Racional**: Bloquear merges com AI reviewer no dia 1 gera resistencia e
desconfianca. O shadow period constroi confianca com dados objetivos. O custo e 2
semanas sem protecao de AI review — aceitavel dado que a alternativa (rejeicao do
tool) tem custo maior.

### Tradeoff: Revisao Uniforme vs. Calibrada por Risco

**Decisao**: Modularizar a profundidade da revisao por nivel de risco do modulo,
usando `risk-profile.yaml`.

**Racional**: Revisao uniforme trata codigo de help page com a mesma severidade que
codigo de modulo de pagamento. Isso gera fadiga no time (excesso de verificacoes em
codigo de baixo risco) e risco (verificacoes insuficientes em codigo critico). A
calibracao por perfil de risco aloca esforco de revisao proporcionalmente ao impacto.

> "Not all code paths have the same risk profile. A change to the payment module
> deserves stricter review than a change to the help page copy."

### Tradeoff: Comentario Livre vs. Resultado Estruturado

**Decisao**: Exigir que AI reviewers processem itens de contrato individualmente,
retornando status `pass`/`fail`/`not-applicable` por dimensao.

**Racional**: Comentario livre e ambiguo e requer interpretacao humana adicional para
ser acionavel. Resultado estruturado por item de contrato e imediatamente acionavel e
verificavel.

---

## 5. Failure Patterns & Anti-patterns

### Failure Pattern 1: AI Output Ignored Due to Noise

**Causa**: Prompt do AI reviewer usa regras genericas da industria em vez das
convencoes reais do time.

**Mecanismo de falha**: O AI gera um volume alto de flags, a maioria irrelevante para
o contexto do projeto. O desenvolvedor aprende que a maioria das flags e falsa ou
irrelevante e para de ler o output completamente. O AI reviewer se torna ruido de
fundo.

**Prevencao**: Afinar o prompt para as convencoes especificas do projeto. O AI deve
enforce as regras do time, nao defaults da industria.

> "Common failure mode: developers start ignoring the AI output because it's too noisy.
> Fix this by tuning the prompt to match your team's actual conventions."

### Failure Pattern 2: AI as Sole Review Gate

**Causa**: Delegar toda a revisao ao AI, incluindo decisoes de arquitetura e design.

**Mecanismo de falha**: O AI reviewer e intrinsecamente superficial e nao consegue
avaliar tradeoffs arquiteturais, coesao de design, ou adequacao ao dominio. Issues
profundos passam despercebidos.

**Prevencao**: Posicionar o AI como primeira passagem (problemas mecanicos), mantendo
o humano responsavel por arquitetura e design.

> "Use them as a first pass, not the only pass."

### Failure Pattern 3: One-Size-Fits-All Review Depth

**Causa**: Aplicar o mesmo nivel de escrutinio a todos os modulos independentemente do
risco.

**Mecanismo de falha**: Modulos de baixo risco recebem revisao excessiva (fadiga,
desperdicio de tempo). Modulos criticos recebem revisao insuficiente (risco nao
mitigado). O time perde confianca no processo porque o esforco nao e proporcional ao
impacto.

**Prevencao**: Implementar `risk-profile.yaml` por modulo e calibrar a profundidade da
revisao.

### Failure Pattern 4: Freeform AI Commentary

**Causa**: Deixar o AI reviewer produzir comentarios livres sem estrutura ou contrato
prévio.

**Mecanismo de falha**: Comentarios livres sao ambiguos, dificeis de verificar, e
exigem que o humano releia o diff para entender o contexto. A latencia de acao
aumenta. Issues podem ser ignorados por falta de clareza.

**Prevencao**: Usar review contracts com itens estruturados e status
`pass`/`fail`/`not-applicable`.

> "Returning structured results instead of freeform commentary."

### Failure Pattern 5: Premature Gating Without Data

**Causa**: Bloquear merges com AI reviewer sem evidencia previa de que as verificacoes
sao confiaveis.

**Mecanismo de falha**: O time experimenta bloqueios por falsos positivos, perde
confianca no tool, e busca formas de bypass (commits diretos, desabilitar o hook). A
ferramenta e rejeitada antes de provar valor.

**Prevencao**: Shadow pipeline de 2 semanas com dados de concordancia antes de
qualquer bloqueio.

---

## 6. Synthesis

### Como as pecas se conectam

Os quatro padroes formam um pipeline de maturidade de AI review, da adocao inicial a
operacao calibrada:

1. **Shadow Review Pipeline** (Pattern 3) e o ponto de entrada. Ele introduz AI review
   sem risco: executa em paralelo, coleta dados, nao bloqueia nada. Resolve o problema
   de adocao.

2. **Review Contract as Checklist** (Pattern 2) fornece a estrutura que torna o AI
   reviewer eficaz. Sem contrato, o AI produz comentario livre ambiguo; com contrato,
   produz verificacoes estruturadas e acionaveis. Resolve o problema de qualidade do
   output.

3. **Pre-Commit Gate** (Pattern 1) e a camada tatica: move a verificacao para o
   momento mais cedo possivel (antes do push), reduzindo o ciclo de feedback. Opera
   com as tres questoes de triagem (bugs, style, security). Resolve o problema de
   latencia.

4. **Contextual Severity Calibration** (Pattern 4) e a camada de otimizacao: garante
   que o esforco de revisao seja proporcional ao risco real do codigo alterado.
   Resolve o problema de alocacao de esforco.

### Dependencias entre os padroes

- **Shadow pipeline depende de review contracts**: Sem contratos estruturados, os
  dados de concordancia do shadow period seriam ambiguos e nao-acionaveis. E preciso
  saber exatamente o que o AI verificou para comparar com o que o humano verificou.

- **Pre-commit gate depende de severity calibration**: Sem calibracao por risco, o
  pre-commit gate aplicaria o mesmo peso a todos os modulos, gerando fadiga e
  incentivando bypass.

- **Severity calibration e alimentada pelos dados do shadow pipeline**: As metricas de
  false positive rate por modulo, coletadas durante o shadow period, informam quais
  niveis de severidade sao confiaveis para cada tipo de modulo.

### Propriedade emergente: Data-Driven Review Governance

O sistema completo produz um ciclo de melhoria continua: shadow pipeline gera dados
sobre eficacia do AI → dados informam calibracao de severidade → severidade calibrada
reduz falsos positivos → menos falsos positivos aumenta confianca → maior confianca
permite expandir o escopo do que o AI revisa → novo escopo volta ao shadow pipeline
para validacao.

Este ciclo fecha o loop entre adocao, calibracao e expansao, transformando AI review
de uma ferramenta estatica em um sistema que melhora com o uso.
