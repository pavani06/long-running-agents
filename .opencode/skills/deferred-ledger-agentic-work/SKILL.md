---
name: deferred-ledger-agentic-work
description: "Mantem o Deferred Ledger — classificacao de divida agentica em tres categorias (skill, dependence, carry) que acumulam silenciosamente enquanto tokens sao baratos. Consome dados do token budget ledger, burn rate, health monitor e harness evolution lifecycle para produzir uma visao de exposicao ao risco. Usar em revisoes trimestrais, GC Day, ou quando houver suspeita de que builds baratos estao acumulando passivos invisiveis. Dispara com: 'deferred ledger', 'divida agentica', 'skill debt', 'dependence debt', 'carry debt', 'risco de repricing', 'token exposure', 'ledger de divida', 'risco acumulado', 'quanto custa manter', 'deferred risk', 'exposicao de tokens', 'what breaks when tokens cost real money'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: governance
  priority: high
  source: "The Trap Spec-Driven Development Is Setting (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu mantenho o Deferred Ledger — o framework de risco que classifica a divida invisivel que se acumula enquanto a construcao agentica e barata. Diferente do token budget ledger (que mede custo operacional), eu classifico o passivo estrutural em tres categorias:

1. **Skill Debt**: o julgamento nao exercitado nao sobrevive. Um time que passou meses sem tomar decisoes dificeis de build-or-dont-build perde a capacidade de toma-las quando subitamente importa. A divida nao e o que foi construido — e o que atrofiou enquanto construia.
2. **Dependence Debt**: workflows construidos na premissa de que geracao e gratuita deixam de funcionar quando a geracao deixa de ser. Nao e um outage catastrofico (visivel); e degradacao silenciosa onde times shippam contra uma ferramenta quebrada sem saber.
3. **Carry Debt**: software que foi barato de criar se torna inventario que precisa ser mantido, securitizado, compreendido e eventualmente reprecificado. O custo de construcao foi uma tarde de tokens; o custo de manutencao e permanente.

O output e uma visao de exposicao: o que quebra quando tokens custam o que realmente custam, quais decisoes de build criaram passivos estruturais, e quais mitigações (parar, simplificar, aposentar, avaliar, exercitar julgamento) reduzem o risco antes que o repricing chegue.

## When to Use Me

Carregue esta skill quando:

- Houver suspeita de que builds baratos estao acumulando divida invisivel (feature inflation, artefatos sem dono)
- O time passou um ciclo longo (trimestre ou mais) sem uma decisao dificil de build-or-dont-build
- Um fornecedor de AI coding tool anunciou mudanca de precificacao ou metricas de consumo
- O custo real dos tokens esta sendo subsidiado (venture funding, credits, trial) e o preco real e desconhecido
- Voce precisa justificar investimento em harness/governanca contra o risco do Deferred Ledger
- O [[docs/canonical/garbage-collection-day-meta-loop|GC Day]] identificou acumulo de artefatos sem owner claro
- Uma revisao trimestral do [[docs/canonical/measured-harness-evolution-lifecycle|Harness Evolution Lifecycle]] esta para acontecer

Nao use quando:

- O time acabou de comecar com agentic coding e ainda nao tem historico suficiente para classificar divida
- A pergunta e puramente sobre custo operacional corrente (use [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] e [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]])
- Voce precisa de uma metrica financeira exata (o Deferred Ledger e um framework de risco, nao de contabilidade)

## The Anti-Pattern

```
ANTI-PATTERN: Medir apenas custo operacional enquanto a divida estrutural acumula.

Cenario:
  1. O time monitora token budget, burn rate e health phases religiosamente.
  2. Os numeros estao verdes: consumo dentro do orcamento, runway confortavel.
  3. Mas o time nao percebe que:
     - Skill Debt: ninguem tomou uma decisao dificil de "nao construir" em 6 meses.
       Quando o CFO perguntar "corta 40% do budget agentico", ninguem sabe priorizar.
     - Dependence Debt: 70% dos workflows dependem de geraçao gratuita.
       Quando o provider reprecificar, os workflows quebram silenciosamente.
     - Carry Debt: o agente criou 47 artefatos. 12 sao usados. 35 existem.
       Alguem vai precisar mante-los, migra-los, securitiza-los.
  4. O time descobre a divida no pior momento: quando o repricing chega e
     a habilidade de decidir o que cortar ja atrofiou.

Consequencia:
  - O dashboard operacional mostra verde; o risco estrutural mostra vermelho
  - A organizacao se transformou em algo que depende de precos insustentaveis
  - O ponto de inflexao nao e quando a conta chega — e quando ja e tarde demais para voltar
```

## The Pattern

```
PATTERN: Classificar a divida agentica em tres categorias e produzir uma visao
de exposicao com decisoes de mitigacao.

Estrutura do Deferred Ledger:

  ┌────────────────────────────────────────────────────────┐
  │                   DEFERRED LEDGER                       │
  │                                                        │
  │ SKILL DEBT                                              │
  │ ├─ Decisoes build/dont-build tomadas no periodo         │
  │ ├─ Proporcao de "nao" vs. "sim"                        │
  │ ├─ Ultimo "nao" registrado (data, contexto, dono)       │
  │ └─ Risco: atrofia de julgamento sob pressao             │
  │                                                        │
  │ DEPENDENCE DEBT                                         │
  │ ├─ Workflows que dependem de geraçao gratuita           │
  │ ├─ Superficie de ferramenta: agent loop, context, tools │
  │ ├─ Cenario de repricing: o que quebra se custo 2x? 10x?│
  │ └─ Risco: falha silenciosa, degradacao nao detectada    │
  │                                                        │
  │ CARRY DEBT                                              │
  │ ├─ Inventario de artefatos criados por agente           │
  │ ├─ Artefatos com owner vs. sem owner                    │
  │ ├─ Artefatos usados vs. nao usados                      │
  │ └─ Risco: manutencao perpetua sem retorno               │
  │                                                        │
  │ EXPOSURE VIEW: o que quebra quando tokens custam real $ │
  │ MITIGATION: parar | simplificar | aposentar | avaliar   │
  └────────────────────────────────────────────────────────┘
```

### Classification Rules

#### Skill Debt

| Indicador | Sinal de Alerta | Acao |
|---|---|---|
| Proporcao de "nao" no periodo | < 10% dos builds tiveram um "nao" registrado | Forcar exercicio de julgamento: revisar backlog e classificar cada item como build/dont-build |
| Ultimo "nao" registrado | > 90 dias sem uma recusa documentada | Aplicar [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake]] no proximo ciclo de decisao |
| Decisoes sem dono | Builds aprovados sem named owner do "sim" | Nomear owner para cada build ativo; builds sem owner entram em quarantine |

#### Dependence Debt

| Indicador | Sinal de Alerta | Acao |
|---|---|---|
| Workflows com provider lock-in | > 50% dos workflows usam features especificas de um provider | Documentar superficies de substituicao; testar com provider alternativo |
| Degradacao silenciosa | Sem evals de qualidade de output nos ultimos 30 dias | Ativar [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] e [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] |
| Cenario de repricing | Nenhum cenario modelado (2x, 5x, 10x custo) | Modelar cenarios: o que quebra em cada nivel de repricing? |

#### Carry Debt

| Indicador | Sinal de Alerta | Acao |
|---|---|---|
| Artefatos sem owner | > 20% dos artefatos nao tem maintainer nomeado | Aplicar [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]: classificar cada artefato como keep/retire/archive/promote |
| Artefatos nao usados | Artefatos criados ha > 90 dias sem evidencia de uso | Marcar para arquivamento ou remocao |
| Artefatos sem value hypothesis | Criados sem responder "quem precisa disso?" | Retroativamente aplicar [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake]]; se sem valor, aposentar |

### Implementation Rules

1. **O Deferred Ledger e um framework de risco, nao de contabilidade.** As categorias sao qualitativas. Nao tente atribuir valores monetarios exatos ao skill debt ou dependence debt. O objetivo e visibilidade e decisoes de mitigacao, nao precisao contabil.

2. **Atualize no ritmo das revisoes de governanca.** O ledger deve ser revisado em cada [[docs/canonical/garbage-collection-day-meta-loop|GC Day]] (semanal, lightweight) e em profundidade a cada ciclo do [[docs/canonical/measured-harness-evolution-lifecycle|Harness Evolution Lifecycle]] (trimestral).

3. **Conecte com o token budget ledger.** O [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] mede o custo operacional corrente; o Deferred Ledger mede o passivo estrutural. Ambos se complementam: custo corrente OK + passivo estrutural alto = risco invisivel.

4. **Toda entrada do ledger gera uma acao.** Nao e um relatorio para ler e arquivar. Cada classificacao de risco (skill alto, dependence medio, carry critico) deve produzir uma decisao: parar, simplificar, aposentar, avaliar mais, ou exercitar julgamento.

5. **Modele cenarios de repricing.** Nao espere o provider anunciar. Modele: se o custo de tokens dobrar, quais workflows quebram? Se quintuplicar? Se o provider descontinuar o modelo atual? Isso transforma dependence debt de conceito abstrato em plano de contingencia.

## Integration with Existing Repo Infrastructure

O Deferred Ledger adiciona uma camada de risco estrategico sobre a camada de custo operacional que o repositorio ja possui:

| Componente Existente | Como o Deferred Ledger complementa |
|---|---|
| [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] | O token ledger mede custo por chamada (fixo, reduzivel, reserva, saldo). O Deferred Ledger classifica o passivo que esse custo corrente esconde: skill debt, dependence debt, carry debt. Ambos devem ser revisados juntos. |
| [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]] | O burn rate preve autonomia restante da sessao. O Deferred Ledger preve autonomia organizacional: por quanto tempo a empresa consegue operar se o custo subir 5x? |
| [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]] | O health monitor converte orcamento em fases green/yellow/orange/red. O Deferred Ledger adiciona uma dimensao ortogonal: o health monitor pode estar verde (custo corrente OK) enquanto o Deferred Ledger mostra vermelho (passivo estrutural acumulado). |
| [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] | O lifecycle governa componentes do harness com BUILD/STABILIZE/SIMPLIFY/REMOVE. O Deferred Ledger estende esse modelo para artefatos criados por agentes: aplicar keep/retire/archive/promote ao inventario de carry debt. |
| [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] | O GC Day revisa slop e constroi guardrails semanalmente. O Deferred Ledger adiciona uma secao de revisao de divida estrutural ao GC Day: skill debt (decisoes da semana), carry debt (artefatos acumulados), dependence debt (mudancas de provider). |
| [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] | O correlation tracking detecta quando evals param de prever outcomes de producao — o sinal de dependence debt se materializando. Alimente o Deferred Ledger com os dados de correlacao. |
| [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake Question Gate]] | O Manual Brake previne carry debt e skill debt na origem (antes do build). O Deferred Ledger audita a divida que ja foi acumulada. Use o Manual Brake para prevenir, o Deferred Ledger para detectar e mitigar. |

## Quality Gates

Antes de declarar uma revisao do Deferred Ledger como completa, verifique:

- [ ] As tres categorias (skill, dependence, carry) foram avaliadas no periodo corrente
- [ ] Skill Debt: a proporcao de decisoes "nao" vs. "sim" foi calculada e esta documentada
- [ ] Skill Debt: se > 90 dias sem um "nao" registrado, um exercicio de julgamento foi agendado
- [ ] Dependence Debt: a superficie de dependencia de provider foi mapeada (quais workflows usam qual provider)
- [ ] Dependence Debt: pelo menos um cenario de repricing (2x, 5x) foi modelado com plano de contingencia
- [ ] Carry Debt: o inventario de artefatos criados por agente foi atualizado (owner, uso, value hypothesis)
- [ ] Carry Debt: artefatos sem owner e sem uso ha > 90 dias tem decisao de aposentadoria ou arquivamento
- [ ] Cada categoria com risco alto ou critico gerou pelo menos uma acao de mitigacao concreta
- [ ] O ledger foi conectado aos dados do token budget ledger e do eval-to-production correlation tracking
- [ ] A revisao esta documentada e acessivel para o proximo ciclo (trimestral ou GC Day)

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/analysis|The Trap SDD Analysis]]:31-39 — Deferred Ledger framework com as tres categorias
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/patterns|SDD Trap Patterns]]:150-177 — Pattern 6: Deferred Ledger for Agentic Work
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/classification|SDD Classification]]:150-171 — classificacao como Missing (High value)
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] — medicao de custo operacional (camada abaixo do Deferred Ledger)
- [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]] — projecao de consumo (alimenta cenarios de repricing)
- [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]] — fases operacionais (complementar, dimensao ortogonal)
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — lifecycle de componentes (modelo para keep/retire/archive/promote de carry debt)
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — deteccao de dependence debt se materializando
- [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] — cadencia de revisao semanal

---

*Created: 2026-06-11 | Source: The Trap Spec-Driven Development Is Setting — Pattern 6 (Missing, High value)*
