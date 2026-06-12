---
name: manual-brake-question-gate
description: "Aplica o Manual Brake — tres perguntas diagnosticas de valor antes de autorizar construcao por agente. Restaura artificialmente o gate economico que tokens gratuitos removeram. Usar antes de qualquer execucao agentica nao-trivial, na fase de alinhamento, ou quando uma tarefa chega sem dono claro. Dispara com: 'freio manual', 'brake question', 'vale a pena construir', 'quem precisa disso', 'pergunta de valor', 'value gate', 'manual brake', 'antes de construir', 'devo construir', 'quem diz nao', 'custo de engenharia', 'brake gate', 'freio de valor'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: decision
  priority: high
  source: "The Trap Spec-Driven Development Is Setting (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu sou o freio manual que substitui os dois freios que desapareceram: o custo economico (tokens quase gratuitos) e a disciplina metodologica (Spec-Driven Development colapsado). Antes que qualquer agente comece a construir, eu aplico tres perguntas diagnosticas:

1. **Quem precisa disso e o que quebra se nunca existir?** — classifica o trabalho como experimento ou build comprometido.
2. **Ainda construiriamos se custasse uma semana de engenharia em vez de uma tarde de tokens?** — restaura artificialmente o gate economico que o preco real removeu.
3. **Quem e o dono de dizer nao a isso?** — nomeia a pessoa cujo trabalho e a recusa fundamentada e o fornecimento de intents alternativos.

O output e uma decisao registrada: **experimento, build comprometido, adiar, ou parar**, com dono nomeado e racional documentado.

## When to Use Me

Carregue esta skill quando:

- Uma tarefa ou feature chega para execucao agentica sem uma decisao de valor previa
- O ciclo de alinhamento (Grill-Me) esta para iniciar e as perguntas de valor precisam ser feitas
- Alguem pede "constroi X" e nao esta claro quem precisa de X nem o que quebra sem X
- Voce suspeita de feature inflation — builds que acontecem so porque sao baratas
- Um agente reporta que "terminou" mas ninguem consegue apontar o retorno concreto
- A tarefa chegou sem um named owner que possa recusa-la
- O custo real da construcao (tempo de engenharia, manutencao futura, carry debt) nao foi considerado

Nao use quando:

- A tarefa ja passou por um value gate documentado com as tres perguntas respondidas
- E um hotfix ou incidente com severidade SEV1/SEV2 onde a pergunta de valor ja foi respondida pela urgencia operacional
- A tarefa e puramente mecanica (ex: atualizar dependencia, corrigir lint) e o custo de fazer a pergunta excede o custo de construir

## The Anti-Pattern

```
ANTI-PATTERN: Construir porque tokens sao baratos e ninguem perguntou se vale a pena.

Cenario:
  1. Um stakeholder ou agente gera uma tarefa: "adiciona dashboard de analytics"
  2. O agente recebe a tarefa, planeja, implementa, testa, mergeia
  3. Ninguem perguntou: quem vai usar esse dashboard? O que quebra sem ele?
     Ainda fariamos se custasse uma semana de engenharia? Quem e o dono de dizer nao?
  4. Seis meses depois: o dashboard existe, ninguem usa, mas alguem precisa mante-lo,
     testa-lo, migra-lo. O build foi barato; o carry debt e permanente.

Consequencia:
  - Feature inflation: mais coisas existem do que precisam existir
  - Carry debt acumula silenciosamente (ver [[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger for Agentic Work]])
  - O time perde a capacidade de distinguir build-que-importa de build-porque-pode
  - Decisoes sem dono se auto-aprovam um mes de cada vez
```

## The Pattern

```
PATTERN: Tres perguntas diagnosticas antes de qualquer build nao-trivial.

Fluxo:

  Tarefa chega
      │
      ▼
  ┌─────────────────────────────────────────────────────┐
  │ PERGUNTA 1: Quem precisa disso e o que quebra       │
  │ se nunca existir?                                    │
  │                                                     │
  │ Se "ninguem" → classificar como EXPERIMENTO.        │
  │ Se "alguem, e isso quebra" → passar para pergunta 2. │
  └─────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────┐
  │ PERGUNTA 2: Ainda construiriamos se custasse        │
  │ uma semana de engenharia em vez de uma tarde        │
  │ de tokens?                                          │
  │                                                     │
  │ Se "nao" → classificar como ADIAR ou PARAR.         │
  │ Se "sim" → passar para pergunta 3.                  │
  └─────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────┐
  │ PERGUNTA 3: Quem e o dono de dizer nao a isso?      │
  │                                                     │
  │ Nomear a pessoa. Se nao existe → PARAR ate existir. │
  │ O dono do "nao" tambem fornece intents alternativos. │
  └─────────────────────────────────────────────────────┘
      │
      ▼
  Decisao registrada: [EXPERIMENTO | BUILD | ADIAR | PARAR]
  com dono nomeado e racional documentado.
```

### Classification Matrix

| Respostas | Classificacao | Acao |
|---|---|---|
| P1: ninguem / P2: nao / P3: sem dono | PARAR | Nao construir. Registrar racional. |
| P1: ninguem / P2: sim ou nao | EXPERIMENTO | Construir com scope minimo, stop criteria explicito, e dono do stop. |
| P1: alguem / P2: nao | ADIAR | Nao construir agora. Revisitar quando custo relativo mudar ou urgencia aumentar. |
| P1: alguem / P2: sim / P3: dono nomeado | BUILD | Construir com scope constraints, dono, e criterios de verificacao. |

### Implementation Rules

1. **Nao pule pergunta 2.** A pergunta do custo-proxy e o coracao do freio. Tokens sao baratos agora, mas o custo real inclui manutencao, carry debt, dependencia e atrofia de julgamento. Tratar "uma semana de engenharia" como o custo total de longo prazo, nao como o custo imediato de tokens.

2. **Nomeie o dono do nao explicitamente.** "O time" nao e um dono. "O PO" so e um dono se o PO aceitou esse papel. Uma decisao sem dono se auto-aprova.

3. **Registre a decisao.** Toda aplicacao do Manual Brake produz um registro com: data, tarefa, respostas as tres perguntas, classificacao final, dono nomeado, e racional. Isso fecha o loop de accountability e alimenta o [[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger]].

4. **Experimentos tem stop criteria.** Se a classificacao for EXPERIMENTO, o escopo deve incluir: o que constitui evidencia de retorno, quando o experimento termina (data ou condicao), e quem decide continuar ou parar.

5. **O freio escala com o risco.** Para tarefas triviais (hotfix, bump de dependencia, correcao de lint), as tres perguntas podem ser respondidas em 30 segundos. Para features, produtos, ou mudancas de arquitetura, as perguntas exigem discussao real.

## Integration with Existing Repo Infrastructure

O Manual Brake se encaixa entre o alinhamento e a execucao no pipeline agentico do repositorio:

| Componente Existente | Como o Manual Brake complementa |
|---|---|
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me faz perguntas de alinhamento (escopo, arquitetura, constraints). O Manual Brake adiciona as tres perguntas de valor que o Grill-Me nao cobre: quem precisa, custo-proxy, e dono da recusa. Aplicar o Manual Brake imediatamente apos ou durante a fase final do Grill-Me. |
| [[.opencode/skills/issue-start/SKILL|issue-start skill]] | O execution brief do issue-start tem objective, success criteria, scope, out-of-scope. O Manual Brake adiciona a dimensao ausente: a decisao de valor (experimento/build/adiar/parar) e o dono do "nao". Integrar a classificacao do Manual Brake no execution brief como campo "Value Decision". |
| [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] | O AFK Routing Gate classifica tarefas por ambiguity, architecture, feedback-loop readiness e product judgment. O Manual Brake adiciona a dimensao de valor: uma tarefa pode ser AFK-ready tecnicamente mas ainda precisar de value gate antes da execucao. |
| [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] | O OS de loop fechado conecta state intake, priority synthesis, execution routing e feedback writeback. O Manual Brake insere um value-gating checkpoint entre priority synthesis e execution routing. |
| [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] | O GC Day revisa slop e misbehavior semanalmente. Pode incluir uma revisao das decisoes de Manual Brake da semana: builds que passaram pelo gate — o retorno se materializou? |

## Quality Gates

Antes de declarar uma decisao de build como validada, verifique:

- [ ] As tres perguntas foram respondidas e registradas (nao apenas "sim" sem elaboracao)
- [ ] A resposta a P1 identifica uma pessoa ou grupo concreto (nao "os usuarios" generico)
- [ ] A resposta a P2 considera custo total de longo prazo (manutencao, carry debt, dependencia), nao apenas tokens
- [ ] A resposta a P3 nomeia uma pessoa especifica (nao "o time", nao "o PO" sem confirmacao)
- [ ] A classificacao final (EXPERIMENTO | BUILD | ADIAR | PARAR) e consistente com as respostas
- [ ] Se EXPERIMENTO: stop criteria, data/condicao de termino, e dono do stop estao definidos
- [ ] Se BUILD: scope constraints e criterios de verificacao de retorno estao documentados
- [ ] Se PARAR ou ADIAR: racional registrado para auditoria futura
- [ ] O registro da decisao esta acessivel para o [[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger]] e para ciclos de revisao

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/analysis|The Trap SDD Analysis]]:62-70 — as tres perguntas diagnosticas e o modelo Two-Brake Failure
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/patterns|SDD Trap Patterns]]:43-68 — Pattern 2: Manual Brake Question Gate
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/classification|SDD Classification]]:56-77 — classificacao como Missing (High value)
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] — entrevista de alinhamento pre-execucao (complementar, diferente conjunto de perguntas)
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] — gate de classificacao de tarefas (complementar, foco em readiness, nao em valor)
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] — sistema operacional de loop fechado (ponto de insercao do value gate)

---

*Created: 2026-06-11 | Source: The Trap Spec-Driven Development Is Setting — Pattern 2 (Missing, High value)*
