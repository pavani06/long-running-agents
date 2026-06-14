---
name: contextual-severity-calibration
description: "Calibra a profundidade e severidade da revisao agentica com base no perfil de risco do modulo alterado. Usa risk-profile.yaml para declarar nivel de risco por modulo (critical, high, medium, low) e conjunto de checks aplicaveis (style, correctness, security, performance, data integrity). Ajusta a profundidade da revisao proporcionalmente ao blast radius e custo de falha da mudanca, em vez de aplicar severidade uniforme a todos os modulos. Usar ao configurar revisao agentica para um codebase multi-modulo, ao calibrar thresholds de revisao por contexto, ou quando falsos positivos em modulos de baixo risco estao gerando fadiga de revisao. Dispara com: 'risk profile', 'severity calibration', 'module risk', 'perfil de risco', 'calibracao de severidade', 'risk-profile.yaml', 'blast radius', 'risk-adjusted review', 'revisao por risco', 'contextual severity', 'module risk metadata', 'check selection by risk', 'critical module review', 'low risk module', 'review depth calibration'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: governance
  priority: high
  source: "Canary Test Code Review (extracted via analyze-and-improve pipeline, 2026-06-15)"
---

## What I Do

Eu substituo a revisao agentica de severidade uniforme — onde uma mudanca na pagina de ajuda recebe o mesmo escrutinio que uma mudanca no modulo de pagamento — por uma revisao calibrada por perfil de risco do modulo. Meu trabalho e garantir que o esforco de revisao seja proporcional ao custo operacional da falha.

Eu opero em tres camadas:

1. **Declaracao de risco por modulo** — um arquivo `risk-profile.yaml` (ou mecanismo equivalente) onde cada modulo do codebase declara seu nivel de risco (`critical`, `high`, `medium`, `low`) e o conjunto de checks aplicaveis (estilo, correcao, seguranca, performance, integridade de dados).

2. **Selecao de checks proporcional ao risco** — quando uma mudanca chega para revisao, o conjunto de checks aplicados e determinado pelo perfil de risco dos modulos alterados, nao por uma lista universal. Um modulo `critical` ativa todos os checks; um modulo `low` ativa apenas checks essenciais.

3. **Severidade calibrada por contexto** — o mesmo finding (ex: "funcao sem tratamento de erro") recebe severidade diferente dependendo de onde ocorre. No modulo de pagamento, e `critical`. Na pagina de ajuda, e `low`. A severidade reflete o blast radius, nao uma escala absoluta.

O output e uma revisao onde modulos de alto risco recebem escrutinio maximo, modulos de baixo risco nao geram fadiga de revisao com falsos positivos, e a severidade dos findings comunica o risco real ao desenvolvedor.

## When to Use Me

Carregue esta skill quando:

- O codebase tem modulos com perfis de risco claramente diferentes (ex: `payment/` vs. `admin/` vs. `help/`) e a revisao agentica trata todos como iguais
- Desenvolvedores reportam fadiga de revisao porque o AI reviewer sinaliza problemas "critical" em modulos onde uma falha teria baixo impacto
- Voce esta configurando um AI reviewer pela primeira vez em um codebase multi-modulo e quer evitar o anti-padrao de severidade uniforme
- Uma mudanca em um modulo critico passou com revisao superficial porque o threshold de revisao era calibrado para o caso medio
- Voce quer que o [[.opencode/skills/shadow-review-pipeline/SKILL|Shadow Review Pipeline]] produza metricas de concordancia segmentadas por nivel de risco
- O time esta crescendo e novos desenvolvedores nao sabem quais modulos exigem revisao mais cuidadosa — o perfil de risco documentado serve como conhecimento institucional
- Voce precisa justificar diferentes SLAs de revisao para diferentes partes do sistema (ex: revisao de `payment/` em < 1h, `help/` em < 24h)

Nao use quando:

- O codebase e pequeno ou homogeneo (um unico modulo, ou modulos com perfis de risco indistinguiveis) — a sobrecarga de manter `risk-profile.yaml` excede o beneficio
- O AI reviewer ainda esta em shadow period inicial e as metricas de concordancia por modulo ainda nao existem — a calibracao sem dados e arbitraria
- A pergunta e puramente sobre cobertura de testes por modulo (use [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] para selecao de suites)
- Voce quer substituir julgamento humano de severidade por regras deterministicas — a calibracao contextual informa o revisor, mas nao elimina a necessidade de julgamento em casos ambiguos

## The Anti-Pattern

```
ANTI-PATTERN: Severidade uniforme — todos os modulos recebem a mesma
profundidade de revisao e a mesma escala de severidade.

Cenario:
  1. O time configura um AI reviewer com checks de seguranca, correcao,
     estilo, performance e integridade de dados.
  2. O AI reviewer aplica TODOS os checks em TODAS as mudancas,
     independentemente do modulo.
  3. Uma mudanca na pagina de ajuda (modulo de baixo risco, zero acesso
     a dados sensiveis) recebe o mesmo escrutinio de seguranca que uma
     mudanca no modulo de pagamento.
  4. O AI reviewer reporta 8 findings na pagina de ajuda: 5 de estilo,
     2 de "possivel vulnerabilidade" (falsos positivos em codigo que
     nunca toca dados sensiveis), 1 de performance (irrelevante para
     uma pagina estatica).
  5. Desenvolvedores gastam 45 minutos revisando e descartando falsos
     positivos em codigo de baixo risco.
  6. Enquanto isso, uma mudanca no modulo de pagamento recebe os
     mesmos checks e passa — mas o AI reviewer, calibrado para nao
     ser "chato demais", nao escala a profundidade para o contexto
     de alto risco.

Consequencia:
  - Fadiga de revisao em modulos de baixo risco (ruido)
  - Falsa confianca em modulos de alto risco (checks insuficientes)
  - Desenvolvedores aprendem a ignorar o AI reviewer em todos os
    modulos, inclusive nos criticos
  - O tempo de revisao e gasto desproporcionalmente em modulos
    onde falhas tem baixo custo operacional
```

O ponto de falha nao e a qualidade dos checks individuais — e a aplicacao uniforme deles a contextos de risco radicalmente diferentes. Um check de seguranca que faz sentido em `payment/` pode ser ruido em `help/`. A severidade `critical` em `help/` nao significa a mesma coisa que `critical` em `payment/`.

## The Pattern

```
PATTERN: Perfil de risco por modulo determina profundidade e severidade da revisao.

Fluxo:

  Codebase com modulos de risco heterogeneo
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. DECLARACAO DE RISCO POR MODULO                        │
  │                                                         │
  │ risk-profile.yaml (ou mecanismo equivalente):            │
  │                                                         │
  │ modules:                                                │
  │   payment:                                              │
  │     risk_level: critical                                │
  │     checks: [security, correctness, data_integrity,      │
  │              performance, style]                         │
  │     blast_radius: "customer financial data, PCI scope"  │
  │     owner: platform-team                                │
  │                                                         │
  │   auth:                                                 │
  │     risk_level: critical                                │
  │     checks: [security, correctness]                      │
  │     blast_radius: "user identity, session management"   │
  │     owner: platform-team                                │
  │                                                         │
  │   api:                                                  │
  │     risk_level: high                                    │
  │     checks: [security, correctness, performance]         │
  │     blast_radius: "public API surface, rate limiting"   │
  │     owner: backend-team                                 │
  │                                                         │
  │   admin:                                                │
  │     risk_level: medium                                  │
  │     checks: [correctness, style]                         │
  │     blast_radius: "internal tools, no customer data"    │
  │     owner: platform-team                                │
  │                                                         │
  │   help:                                                 │
  │     risk_level: low                                     │
  │     checks: [style]                                     │
  │     blast_radius: "static content, zero data access"    │
  │     owner: content-team                                 │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. SELECAO DE CHECKS POR MUDANCA                         │
  │                                                         │
  │ Quando uma mudanca chega, o AI reviewer:                 │
  │                                                         │
  │ a) Identifica os modulos alterados (via file paths)      │
  │ b) Consulta o risk-profile.yaml para cada modulo         │
  │ c) Seleciona a UNIAO dos checks de todos os modulos      │
  │    alterados (se mudanca toca payment/ E help/, aplica   │
  │    todos os checks de payment/ — o modulo mais critico   │
  │    dita a profundidade)                                  │
  │ d) Aplica apenas os checks selecionados a cada arquivo    │
  │                                                         │
  │ Regra: o risco da mudanca = max(risco dos modulos        │
  │ alterados). Uma mudanca que toca payment/ e help/ e      │
  │ tratada como critical, nao como media.                   │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. SEVERIDADE CALIBRADA POR CONTEXTO                     │
  │                                                         │
  │ O mesmo finding recebe severidade diferente conforme     │
  │ o modulo onde ocorre:                                    │
  │                                                         │
  │  Finding: "Funcao sem tratamento de erro"                │
  │  ─────────────────────────────────────────────────────  │
  │  Em payment/auth.rs      → severity: critical            │
  │    (falha = transacao perdida, dinheiro parado)          │
  │                                                         │
  │  Em api/handler.ts       → severity: high                │
  │    (falha = 500 para cliente, mas retry e possivel)      │
  │                                                         │
  │  Em admin/dashboard.tsx  → severity: medium              │
  │    (falha = dashboard quebrado, interno, sem impacto     │
  │     no cliente)                                          │
  │                                                         │
  │  Em help/faq.html        → severity: low                 │
  │    (falha = pagina estatica quebrada, baixo impacto)     │
  │                                                         │
  │ A severidade reflete "o que quebra se isso falhar?",     │
  │ nao uma escala absoluta de qualidade de codigo.          │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. FEEDBACK LOOP DE CALIBRACAO                           │
  │                                                         │
  │ Periodicamente (ex: trimestral ou apos shadow period):   │
  │                                                         │
  │ a) Revisar false-positive rates por modulo               │
  │    - Se FP rate em modulos low > threshold: reduzir      │
  │      checks nesses modulos                               │
  │    - Se FP rate em modulos critical > threshold:         │
  │      revisar prompt, nao reduzir checks                  │
  │                                                         │
  │ b) Revisar missed-by-AI rates por modulo                 │
  │    - Se AI perde coisas em modulos critical: expandir    │
  │      checks ou adicionar revisao humana obrigatoria      │
  │                                                         │
  │ c) Reclassificar modulos quando:                         │
  │    - Um modulo ganha acesso a dados sensiveis            │
  │    - Um modulo se torna customer-facing                  │
  │    - Um modulo e deprecated ou arquivado                 │
  │    - A arquitetura muda e o blast radius se altera        │
  └─────────────────────────────────────────────────────────┘
```

### Risk Level Taxonomy

| Nivel | Criterio | Checks Minimos | Exemplos |
|---|---|---|---|
| **Critical** | Acesso a dados financeiros, PII, autenticacao, ou sessao. Falha = perda financeira, breach de seguranca, ou outage de sistema core. | Security, Correctness, Data Integrity, Performance | `payment/`, `auth/`, `billing/` |
| **High** | API publica, surface de integracao, ou componente compartilhado por multiples servicos. Falha = outage de feature ou degradacao visivel ao cliente. | Security, Correctness, Performance | `api/`, `webhooks/`, `shared-lib/` |
| **Medium** | Ferramenta interna, admin dashboard, ou script de automacao. Falha = inconveniencia interna, sem impacto direto no cliente. | Correctness, Style | `admin/`, `scripts/`, `internal-tools/` |
| **Low** | Conteudo estatico, documentacao, paginas de ajuda. Falha = incoveniencia menor, recuperacao trivial. | Style | `help/`, `docs/`, `landing/` |

### Check Set Definitions

| Check | O que cobre | Custo (latencia) | Aplicavel a |
|---|---|---|---|
| `security` | Vulnerabilidades, exposicao de dados, auth bypass, injection | Alto | Critical, High |
| `correctness` | Logica de negocio, edge cases, null handling, race conditions | Alto | Critical, High, Medium |
| `data_integrity` | Consistencia de dados, constraints de schema, transacoes | Alto | Critical |
| `performance` | N+1 queries, memory leaks, blocking I/O, algoritmo ineficiente | Medio | Critical, High |
| `style` | Convencoes de projeto, nomenclatura, estrutura de arquivos | Baixo | Todos (default) |

## Implementation Rules

1. **O perfil de risco e mantido por quem conhece o sistema, nao pelo AI reviewer.** O `risk-profile.yaml` deve ser criado e mantido pelos owners de cada modulo. O AI reviewer consome o perfil; nao o define. Um owner ausente ou desatualizado e pior que perfil nenhum.

2. **A regra do maximo prevalece.** Se uma mudanca toca modulos com diferentes niveis de risco, o nivel mais alto dita a profundidade da revisao. Uma mudanca que altera `payment/` (critical) e `help/` (low) recebe todos os checks de `critical`. Isso evita que mudancas cross-module escapem com revisao insuficiente.

3. **Reduzir checks em modulos de baixo risco nao e negligencia — e alocacao de atencao.** O tempo de revisao e finito. Gastá-lo em falsos positivos em `help/` significa menos tempo para revisar `payment/` com a profundidade necessaria. A calibracao existe para concentrar esforco onde o custo da falha e maior.

4. **A severidade calibrada e um rotulo, nao um bloqueio.** Um finding `low` em `help/` nao significa "ignorar" — significa "isto nao e urgente, resolva quando conveniente". Um finding `critical` em `payment/` significa "isto bloqueia o merge ate ser resolvido ou waivado com justificativa".

5. **O perfil de risco envelhece.** Modulos mudam de proposito, ganham acesso a dados sensiveis, ou sao descontinuados. O `risk-profile.yaml` deve ser revisado em cadencia regular (trimestral, ou a cada mudanca de arquitetura significativa). Um perfil desatualizado e pior que perfil nenhum porque gera falsa confianca.

6. **Dados do Shadow Review Pipeline alimentam a calibracao.** As metricas de concordancia por modulo produzidas pelo [[.opencode/skills/shadow-review-pipeline/SKILL|Shadow Review Pipeline]] (TP, FP, Missed-by-AI, Missed-by-Human) sao a entrada empirica para ajustar perfis de risco. Se um modulo `medium` consistentemente tem mais Missed-by-AI que modulos `critical`, seu perfil de risco pode estar subestimado.

7. **Nao existe "risco zero".** Mesmo modulos `low` podem conter bugs. A calibracao nao elimina a revisao nesses modulos — reduz a profundidade e ajusta a severidade para refletir o impacto real. O desenvolvedor ainda ve os findings; so nao e forcado a trata-los como emergencia.

## Integration with Existing Repo Infrastructure

A Contextual Severity Calibration se integra a infraestrutura de evals e governanca como camada de precisao que evita o tratamento uniforme de modulos com perfis de risco radicalmente diferentes:

| Componente Existente | Como a Contextual Severity Calibration complementa |
|---|---|
| [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] | A estratificacao seleciona tiers por tipo de mudanca (prompt, model, tool, loop). A Severity Calibration adiciona uma segunda dimensao: dentro do mesmo tier, a profundidade varia por modulo. Um eval `fast` em `payment/` pode ser mais profundo que um eval `fast` em `help/`. |
| [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] | O PR-gated enforcement define thresholds de merge. A Severity Calibration ajusta esses thresholds por modulo: um finding `medium` em `payment/` pode bloquear merge, enquanto o mesmo finding em `help/` e informativo. |
| [[.opencode/skills/shadow-review-pipeline/SKILL|Shadow Review Pipeline]] | O shadow period produz metricas de concordancia (TP, FP, Missed) por modulo. A Severity Calibration consome esses dados para ajustar perfis de risco e selecao de checks. Modulos com alta taxa de FP podem ter checks reduzidos; modulos com alta taxa de Missed-by-AI podem ter checks expandidos. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A avaliacao ancorada em constraints verifica constraints explicitas. A Severity Calibration determina QUAIS constraints se aplicam a cada modulo — constraints de seguranca so se aplicam a modulos com `security` no check set. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Evaluator aplica rubricas de qualidade. A Severity Calibration fornece ao Evaluator o perfil de risco do modulo alterado, permitindo que a rubrica seja ajustada por contexto em vez de ser uniforme. |
| [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]] | Arquitetura como affordance enfatiza deep modules com interfaces simples e reduced coupling para reduzir blast radius. A Severity Calibration operacionaliza o conceito de blast radius: modulos com interfaces bem definidas e baixo acoplamento tendem a ter blast radius menor e, portanto, menor risco. |
| [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] | O AFK gate classifica tarefas como AFK-ready ou human-in-loop. A Severity Calibration adiciona uma dimensao: mudancas em modulos `critical` podem exigir human-in-loop mesmo que a tarefa seja tecnicamente AFK-ready. |
| [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] | A escada de degradacao classifica falhas por tipo (retryable, unsafe, hold). A Severity Calibration adiciona contexto de modulo: uma falha `unsafe` em `help/` pode ser tratada como `retryable`, enquanto a mesma falha em `payment/` permanece `unsafe` com escalacao imediata. |
| [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] | O loop de classificacao de falhas captura padroes de misbehavior. A Severity Calibration segmenta esses padroes por modulo, permitindo identificar se certos tipos de falha sao endemicos a modulos especificos. |

## Quality Gates

Antes de declarar a calibracao de severidade como operacional, verifique:

- [ ] `risk-profile.yaml` (ou mecanismo equivalente) existe e cobre todos os modulos do codebase com nivel de risco e check set declarados
- [ ] Cada modulo tem um owner nomeado responsavel por manter seu perfil de risco
- [ ] Os niveis de risco seguem a taxonomia (critical, high, medium, low) com criterios consistentes
- [ ] Checks selecionados para cada modulo sao proporcionais ao blast radius e custo de falha declarados
- [ ] A regra do maximo esta implementada: mudancas cross-module recebem a profundidade do modulo mais critico
- [ ] A severidade dos findings e calibrada por modulo: o mesmo finding tem severidade diferente em contextos diferentes
- [ ] O AI reviewer consulta o risk-profile.yaml ANTES de selecionar checks (nao aplica checks e depois verifica risco)
- [ ] Dados do [[.opencode/skills/shadow-review-pipeline/SKILL|Shadow Review Pipeline]] estao segmentados por modulo e disponiveis para calibrar perfis
- [ ] Ha uma cadencia definida para revisao e atualizacao dos perfis de risco (ex: trimestral, ou apos mudancas de arquitetura)
- [ ] Modulos `critical` tem revisao humana obrigatoria alem da revisao AI (a calibracao aumenta, nao substitui, o escrutinio humano em modulos criticos)
- [ ] Desenvolvedores sabem consultar o perfil de risco para entender a severidade dos findings que recebem
- [ ] O custo de revisao (tempo, tokens) e proporcional ao risco: mais recursos gastos em `critical`, menos em `low`

## References

- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]] — analise fonte dos padroes de code review agentic
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]] — Pattern 4: Contextual Severity Calibration (inputs, outputs, benefits, limitations)
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]] — classificacao como Missing (High integration value) com evidencias de ausencia no repositorio
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — estratificacao fast/medium/deep (severity calibration como segunda dimensao)
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — enforcement de evals em PRs (thresholds calibrados por modulo)
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — avaliacao ancorada em constraints (check selection determina quais constraints)
- [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]] — arquitetura como affordance (blast radius como criterio de risco)
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] — gate de roteamento (severity calibration adiciona dimensao de risco)
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] — escada de degradacao (severidade calibrada por contexto de modulo)
- [[docs/canonical/generator-evaluator|Generator-Evaluator]] — arquitetura Generator-Evaluator (rubrica ajustada por perfil de risco)
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — loop de classificacao de falhas (segmentacao por modulo)
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] — gate de valor (perfis de risco informam a pergunta "o que quebra se isso falhar?")
- [[.opencode/skills/shadow-review-pipeline/SKILL|Shadow Review Pipeline]] — pipeline de shadow review (produz dados de concordancia por modulo que alimentam a calibracao)

---

*Created: 2026-06-14 | Source: Canary Test Code Review — Pattern 4 (Missing, High value)*
