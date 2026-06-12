---
name: owner-of-no-role
description: "Define o papel de Owner-of-No — a pessoa cujo trabalho explicito e recusar trabalho de baixo valor e fornecer intents alternativos. Transforma 'dizer nao' de ato acidental de coragem em papel organizacional desenhado, com criterios de recusa, caminho de escalacao e accountability documentada. Usar ao estruturar times agenticos, designar governanca de build/dont-build, ou quando decisoes de construcao estao se auto-aprovando por falta de dono. Dispara com: 'owner of no', 'dono do nao', 'quem diz nao', 'refusal role', 'papel de recusa', 'recusar trabalho', 'dizer nao', 'value gate owner', 'dono da decisao', 'quem recusa', 'governanca de build', 'no-owner', 'recusa fundamentada'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: governance
  priority: medium
  source: "The Trap Spec-Driven Development Is Setting (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu defino e operacionalizo o papel de Owner-of-No — a pessoa cujo trabalho nao e construir, mas garantir que so se construa o que merece ser construido. O Owner-of-No tem tres responsabilidades:

1. **Recusa fundamentada**: dizer "nao" a builds que nao passam no [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake]], com racional documentado e alternativas concretas.
2. **Fornecimento de intents**: quando diz "nao", o Owner-of-No nao apenas bloqueia — ele fornece intents alternativos: o que DEVERIA ser construido em vez disso.
3. **Accountability documentada**: cada decisao de recusa ou aprovacao e registrada com dono, data, racional e criterios de reavaliacao.

O Owner-of-No nao e um gatekeeper burocratico. E o papel que transforma "dizer nao" de um ato acidental de coragem individual em uma funcao organizacional desenhada, com autoridade, criterios e responsabilidade.

## When to Use Me

Carregue esta skill quando:

- Times agenticos estao produzindo builds sem que ninguem pergunte "alguem precisa disso?"
- Decisoes de construcao estao se auto-aprovando ("ninguem aprovou isso. Ele se aprova sozinho, um mes de cada vez.")
- Voce esta desenhando a estrutura de governanca de um time que usa agentic coding
- O [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake]] identificou que nao ha dono do "nao" (Pergunta 3 sem resposta)
- Um ciclo de revisao (GC Day, Harness Evolution Lifecycle) identificou carry debt de builds sem owner
- Voce quer evitar que "dizer nao" dependa de coragem individual em vez de design organizacional

Nao use quando:

- O time ja tem um processo formal de aprovacao com autoridade de recusa documentada e funcional
- A escala e muito pequena (ex: time de 2 pessoas onde o founder e naturalmente o owner-of-no)
- Voce quer criar um gatekeeper burocratico que atrasa tudo — o Owner-of-No acelera o trabalho certo, nao atrasa todo trabalho

## The Anti-Pattern

```
ANTI-PATTERN: Builds que se auto-aprovam porque ninguem e dono do "nao".

Cenario:
  1. Um time de builders recebe uma ideia: "vamos adicionar integracao com X"
  2. Ninguem e formalmente responsavel por perguntar "alguem precisa de integracao com X?"
  3. O builder implementa. O revisor revisa o codigo (qualidade, nao valor).
     O merge acontece. A feature existe.
  4. Meses depois: a feature nao e usada, mas precisa de manutencao, migracao, testes.
     Ninguem sabe quem aprovou. Ninguem nunca aprova. Ela se aprovou sozinha.
  5. Quando alguem pergunta "por que isso existe?", a resposta e "o agente construiu".
     Ninguem consegue apontar o retorno.

Consequencia:
  - Carry debt acumula sem accountability (ver [[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger]])
  - "Dizer nao" vira ato de coragem individual, nao funcao do sistema
  - Features existem porque foram faceis de construir, nao porque alguem precisava delas
  - O time perde a capacidade de distinguir o essencial do acidental
```

## The Pattern

```
PATTERN: Um papel organizacional explicito cujo trabalho e a recusa fundamentada.

Modelo do Owner-of-No:

  ┌─────────────────────────────────────────────────────────┐
  │                    OWNER-OF-NO                           │
  │                                                         │
  │ RESPONSABILIDADES:                                      │
  │ 1. Recusar builds de baixo valor com racional documentado│
  │ 2. Fornecer intents alternativos ("em vez disso, X")     │
  │ 3. Nomear donos para builds aprovados                    │
  │ 4. Manter o ledger de decisoes build/dont-build          │
  │ 5. Escalar quando a decisao excede sua autoridade        │
  │                                                         │
  │ AUTORIDADE:                                             │
  │ - Pode recusar builds abaixo de um threshold definido    │
  │ - Pode exigir que builds passem pelo Manual Brake        │
  │ - Pode convocar revisao de builds existentes (carry debt)│
  │ - NAO pode aprovar builds unilateralmente                │
  │   (aprovacao requer o Manual Brake completo)             │
  │                                                         │
  │ CRITERIOS DE RECUSA:                                     │
  │ - Build nao tem usuario concreto identificado            │
  │ - Build nao sobrevive a pergunta do custo-proxy          │
  │ - Build cria carry debt sem plano de manutencao           │
  │ - Build duplica funcionalidade existente sem justificar   │
  │                                                         │
  │ CAMINHO DE ESCALACAO:                                    │
  │ - Se o builder discorda da recusa → arquitetura da decisao│
  │   (documentar ambos os lados, escalar para lideranca)     │
  │ - Se o build excede autoridade do Owner-of-No → escalar   │
  │   para o nivel com autoridade sobre o dominio             │
  │ - Se o Owner-of-No esta sobrecarregado → distribuir       │
  │   ownership por dominio (cada dominio tem seu owner)      │
  └─────────────────────────────────────────────────────────┘
```

### Implementation Rules

1. **O Owner-of-No nao e um bloqueador — e um acelerador do trabalho certo.** A meta nao e dizer "nao" para tudo, e garantir que cada "sim" tem valor documentado, dono nomeado e criterios de verificacao. Um Owner-of-No eficaz aumenta a velocidade do trabalho que importa ao eliminar o trabalho que nao importa.

2. **Autoridade sem accountability e pior que ausencia de autoridade.** O Owner-of-No deve ter: criterios de decisao publicos, registro documentado de cada decisao, e um caminho de escalacao para quando builder e owner discordam. Sem isso, o papel vira gatekeeper arbitrario.

3. **"Nao" sempre vem com alternativa.** Recusar sem oferecer alternativa e bloqueio. O Owner-of-No deve fornecer: "em vez de construir X, considere Y" ou "X e valido, mas precisa de Z antes". A recusa e construtiva, nao destrutiva.

4. **O papel escala por dominio.** Um unico Owner-of-No para todo o time vira gargalo. Distribua ownership por dominio: o Owner-of-No de pagamentos recusa builds de pagamento; o Owner-of-No de onboarding recusa builds de onboarding. Cada dominio tem seu especialista que entende o contexto.

5. **O Owner-of-No opera com o Manual Brake.** A primeira pergunta do Manual Brake ("quem precisa disso?") e o criterio central. A terceira ("quem e o dono de dizer nao?") e respondida pelo proprio Owner-of-No. O papel existe para que a Pergunta 3 nunca fique sem resposta.

6. **Revisao periodica das decisoes.** Trimestralmente, revisar: quais builds foram recusadas? Os intents alternativos geraram valor? Alguma recusa deveria ser revertida (novas informacoes)? Isso fecha o loop de aprendizado e previne vies de recusa excessiva.

## Integration with Existing Repo Infrastructure

O Owner-of-No complementa a infraestrutura de governanca do repositorio com um papel organizacional explicito:

| Componente Existente | Como o Owner-of-No complementa |
|---|---|
| [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake Question Gate]] | A Pergunta 3 do Manual Brake ("quem e o dono de dizer nao?") e respondida pelo Owner-of-No. O Owner-of-No e a institucionalizacao dessa pergunta: um papel cuja existencia garante que a pergunta sempre tem resposta. |
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me entrevista o requisitante sobre escopo, arquitetura e constraints. O Owner-of-No participa da entrevista como a voz da recusa fundamentada: "entendi o que voce quer construir. Por que isso, e nao X?" |
| [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] | O split-brain review avalia planos com rubricas de engenharia e destino. O Owner-of-No adiciona a terceira rubrica: valor. "O plano e tecnicamente solido, mas alguem precisa disso?" |
| [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] | O AFK Gate classifica tarefas como AFK-ready ou human-in-loop. O Owner-of-No define o criterio de valor para essa classificacao: uma tarefa so e AFK-ready se passou pelo value gate (Manual Brake + Owner-of-No). |
| [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] | O GC Day revisa slop semanalmente. O Owner-of-No participa do GC Day revisando builds da semana: algum build passou sem value gate? Alguma recusa foi bypassada? |
| [[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger for Agentic Work]] | O Deferred Ledger classifica carry debt de artefatos sem owner. O Owner-of-No e o responsavel por auditar esse inventario e decidir: keep, retire, archive, ou promote. |
| [[.opencode/skills/orchestrator/SKILL|orchestrator skill]] | O orchestrator sugere proximas tarefas e gerencia agentes paralelos. O Owner-of-No define a politica de priorizacao: tarefas que passaram pelo value gate tem prioridade sobre tarefas que ainda nao passaram. |

### Distribuicao por Dominio (Template)

```
Dominios e seus Owners-of-No:

| Dominio | Owner-of-No | Criterios especificos de recusa |
|---|---|---|
| Agentes e orquestracao | [nome] | Build deve ter agent lifecycle documentado |
| Curriculo e conteudo | [nome] | Build deve mapear para um nivel e conceito core |
| Portal web | [nome] | Build deve respeitar DESIGN.md e vanilla JS |
| Stack e tooling | [nome] | Build deve ser compativel com Node >= 20.18 e ESM |
| Governanca | [nome] | Build deve seguir precedence order do system-of-record |
```

Este template deve ser adaptado a estrutura real do time. O importante e que cada dominio com atividade agentica tenha um Owner-of-No nomeado.

## Quality Gates

Antes de declarar a estrutura de Owner-of-No como operacional, verifique:

- [ ] Cada dominio com builds agenticos tem um Owner-of-No nomeado e documentado
- [ ] Os criterios de recusa estao publicos e acessiveis para builders e stakeholders
- [ ] O caminho de escalacao esta definido (o que acontece quando builder discorda da recusa)
- [ ] Toda recusa e registrada com: data, build proposto, razao da recusa, intents alternativos oferecidos, e criterios de reavaliacao
- [ ] Toda aprovacao e registrada com: data, build aprovado, respostas as tres perguntas do Manual Brake, e dono nomeado
- [ ] O Owner-of-No participa do [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake]] como respondedor da Pergunta 3
- [ ] O Owner-of-No tem slot reservado no [[docs/canonical/garbage-collection-day-meta-loop|GC Day]] para revisar decisoes da semana
- [ ] Trimestralmente: revisao das decisoes de recusa e aprovacao para calibrar criterios
- [ ] Nao ha builds ativos sem owner documentado (auditoria de carry debt)

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/analysis|The Trap SDD Analysis]]:90-94 — Ownership-of-No como design de papel organizacional
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/patterns|SDD Trap Patterns]]:124-148 — Pattern 5: Owner-of-No Role
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting.md/classification|SDD Classification]]:124-147 — classificacao como Missing (Medium value)
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] — entrevista de alinhamento (Owner-of-No participa como voz da recusa)
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] — revisao de planos (Owner-of-No adiciona rubrica de valor)
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] — gate de classificacao (Owner-of-No define criterio de valor)
- [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] — cadencia semanal de revisao
- [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake Question Gate]] — as tres perguntas que o Owner-of-No aplica
- [[.opencode/skills/deferred-ledger-agentic-work/SKILL|Deferred Ledger for Agentic Work]] — classificacao de carry debt de builds sem owner

---

*Created: 2026-06-11 | Source: The Trap Spec-Driven Development Is Setting — Pattern 5 (Missing, Medium value)*
