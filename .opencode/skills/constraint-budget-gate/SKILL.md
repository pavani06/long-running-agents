---
name: constraint-budget-gate
description: "Gate rigido de orcamento de constraints: maximo 5 a 7 linhas. Revisa listas de constraints em busca de bloat, reclassifica escolhas de implementacao como Context, rejeita specs disfarcadas de constraints, e garante que cada constraint restante e direcional, incondicional e em linguagem de negocio. Previne que listas de constraints crescam ate virarem specs escondidas que removem toda liberdade de design do agente. Usar durante a escrita ou revisao de intents, como gate pre-execucao, ou quando o campo Constraints do intent parece uma lista de requisitos tecnicos em vez de qualidades do outcome. Dispara com: 'constraint budget', 'orcamento de constraints', 'limite de constraints', 'constraint limit', '5 a 7 constraints', 'constraint gate', 'constraint bloat', 'muitas constraints', 'constraint list too long', 'constraints viram spec', 'reduzir constraints', 'constraint budget gate', 'directional constraints', 'business language constraints'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: alignment
  priority: high
  source: "The Anatomy of Intent - ICE in IDSD (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu aplico um gate de orcamento sobre o campo Constraints do intent: **maximo 5 a 7 constraints direcionais, incondicionais, em linguagem de negocio.** Tudo que passa de 7, tudo que descreve COMO implementar, e tudo que poderia ser checado depois que o output existe -- eu reclassifico e movo para o destino correto, ou rejeito.

Meu trabalho nao e reduzir constraints arbitrariamente -- e garantir que as constraints que ficam sao genuinamente qualidades do outcome que o builder precisa saber durante a implementacao. Cada constraint alem de 7 e um grau de liberdade removido do agente. Cada constraint que diz "use PostgreSQL" em vez de "os dados devem sobreviver a reinicializacao do servico" e uma decisao de design que o humano tomou no lugar do agente.

Tres saidas possiveis para cada constraint candidata:

- **CONSTRAINT**: direcional, incondicional, em linguagem de negocio. Ex: "Deve responder em menos de 200ms no p95." Fica no campo Constraints.
- **CONTEXT**: padrao do time, convencao de stack, decisao de arquitetura que o builder precisa saber mas nao e uma restricao de outcome. Ex: "O time usa PostgreSQL." Move para o harness montar como Context.
- **REJEITADA**: spec disfarcada, check pos-output, ou instrucao de implementacao. Ex: "Use o padrao Repository." Isso nao e constraint de outcome -- e instrucao de coding que nao pertence ao intent.

## When to Use Me

Carregue esta skill quando:

- O campo Constraints de um intent tem mais de 7 itens -- o alarme de bloat disparou
- Voce suspeita que constraints estao se acumulando como "requirements" de spec em vez de qualidades do outcome
- O intent foi escrito por alguem com habito de spec-writing -- cada "constraint" parece uma decisao de implementacao
- O [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]] completou o gate de completude, mas o campo Constraints parece inflado -- completude nao garante qualidade
- A avaliacao ancorada em constraints ([[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]) esta lenta ou confusa porque ha constraints demais para verificar
- Voce esta treinando alguem a escrever constraints de qualidade e precisa de criterios objetivos de classificacao
- O [[.opencode/skills/constraint-failure-decision-rule/SKILL|constraint-failure-decision-rule]] identificou que um item e constraint, mas voce ainda suspeita que nao e uma boa constraint -- o budget gate faz a segunda passada de qualidade

Nao use quando:

- O dominio e regulado (saude, financas, seguranca) e constraints legais/regulatorias genuinas excedem 7 -- o budget e uma heuristica, nao uma lei. Documente o excesso e justifique.
- O intent e um experimento exploratorio com poucas constraints conhecidas -- o problema oposto (sub-constrained) e pior que bloat
- Voce nao tem um sistema de Context (harness, resolvers, skills) para onde mover as constraints reclassificadas -- mover para o vazio e perder informacao. Construa o sistema de Context primeiro, depois aplique o budget gate.

## The Anti-Pattern

```
ANTI-PATTERN: Constraint list bloat — 6 constraints viram 16, e cada linha
adicionada se justifica como "essencial", mas o conjunto para de ser qualidades
do outcome e vira spec disfarcada.

Cenario:
  1. Um intent comeca com 5 constraints legítimas sobre um servico de catalogo.
  2. Um revisor adiciona: "Use PostgreSQL", "Implemente com Repository Pattern",
     "Use gRPC para comunicacao interna", "Adicione circuit breaker",
     "Logs em formato JSON", "Metrique com Prometheus", "Deploy via Kubernetes",
     "Health check no endpoint /health", "Rate limiting por IP",
     "Cache com Redis", "Filas com RabbitMQ."
  3. O campo Constraints agora tem 16 linhas. O builder (agente) recebe isso.
     Nao ha decisao de design para tomar: stack, padroes, infra, e comunicacao
     estao todos decididos. O agente e um executor de spec.
  4. O time acredita que esta fazendo intent-driven porque "o Goal ainda esta la".
     Mas o Goal diz "Build a product catalog service" e as constraints dizem
     exatamente COMO -- o agente nao tem latitude nenhuma.
  5. Drift silencioso: a cada sprint, mais uma constraint "essencial" entra.
     Ninguem percebe que o metodo voltou a ser spec-driven.

Consequencia:
  - O agente perdeu toda liberdade de design -- constraints viraram spec
  - Constraints em linguagem de implementacao sao frageis: se o time trocar
    PostgreSQL por MongoDB, 16 constraints precisam ser reescritas, nao 5
  - A avaliacao ancorada em constraints tem que verificar 16 coisas --
    latencia sobe, falsos positivos aumentam
  - O proposito original das constraints (direcionar o builder sem ditar
    o metodo) foi completamente subvertido
```

## The Pattern

```
PATTERN: Gate de tres passos — classificar, budgetar, rejeitar.

Fluxo:

  Lista de constraints candidatas chega
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 1: CLASSIFICAR cada constraint candidata           │
  │                                                         │
  │ Para cada linha, responda TRES perguntas:                 │
  │                                                         │
  │ PERGUNTA A: Esta constraint descreve uma QUALIDADE DO    │
  │   OUTCOME ou uma DECISAO DE IMPLEMENTACAO?               │
  │                                                         │
  │   Qualidade: "Deve responder em < 200ms p95"             │
  │   Implementacao: "Use PostgreSQL"                         │
  │                                                         │
  │ PERGUNTA B: Esta constraint e DIRECIONAL ("o outcome     │
  │   deve ser X") ou e um CHECK BINARIO ("o output deve     │
  │   conter Y")?                                            │
  │                                                         │
  │   Direcional: "Deve ser rapido para o usuario final"      │
  │   Check: "Deve ter health check no /health"               │
  │                                                         │
  │ PERGUNTA C: Esta constraint e INCONDICIONAL ou depende   │
  │   de contexto que o builder precisaria adivinhar?         │
  │                                                         │
  │   Incondicional: "Nao pode expor PII em logs"             │
  │   Condicional: "Use Redis se o trafego for alto"          │
  │                                                         │
  │ CLASSIFICACAO:                                           │
  │   Qualidade + Direcional + Incondicional → CONSTRAINT    │
  │   Implementacao → CONTEXT (o builder precisa saber,      │
  │     mas nao e restricao de outcome)                      │
  │   Check binario → FAILURE CONDITION ou EXPECTATION       │
  │     (checavel depois que o output existe)                │
  │   Condicional → REJEITAR (constraints nao podem depender  │
  │     de condicoes que o builder teria que adivinhar)       │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 2: BUDGETAR — aplicar o limite de 5-7              │
  │                                                         │
  │ Das constraints classificadas como CONSTRAINT genuínas:   │
  │                                                         │
  │ Se ≤ 7: todas ficam. Continue.                            │
  │                                                         │
  │ Se > 7: priorize e corte. Criterios de priorizacao:       │
  │   1. Seguranca / compliance (sempre ficam)                │
  │   2. Propriedades do outcome que, se violadas, o output   │
  │      e inaceitavel (ex: "nao pode expor PII")             │
  │   3. Qualidades que afetam a experiencia do usuario final  │
  │      (ex: latencia, disponibilidade)                      │
  │   4. Qualidades tecnicas internas (ex: testabilidade) —    │
  │      estas sao as primeiras a serem movidas para Context   │
  │                                                         │
  │ Constraints cortadas do budget vao para:                  │
  │   - Context (se o builder precisa saber)                  │
  │   - Expectations (se e um criterio de sucesso)            │
  │   - Removidas (se e ruido)                                │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 3: REJEITAR — remover o que nao e constraint       │
  │                                                         │
  │ Items REJEITADOS recebem destino explicito:               │
  │                                                         │
  │   "Use PostgreSQL" → CONTEXT: "Stack padrao do time"      │
  │   "Implemente Repository Pattern" → REJEITADO: instrucao  │
  │     de coding que nao pertence ao intent                  │
  │   "Health check no /health" → EXPECTATION ou CONTEXT:     │
  │     "Convencao de deploy do time"                         │
  │   "Logs em JSON estruturado" → CONTEXT: "Padrao de        │
  │     observabilidade do time"                              │
  │                                                         │
  │ Cada item rejeitado deve ter um MOTIVO documentado e      │
  │ um DESTINO explicito. Nada e descartado sem destino.      │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 4: Validar as constraints sobreviventes             │
  │                                                         │
  │ Para cada constraint no budget final (≤7):                │
  │   - Esta em linguagem de negocio, nao de implementacao?   │
  │   - Um stakeholder nao-tecnico entende?                   │
  │   - Sobrevive a uma mudanca de stack?                     │
  │     ("< 200ms p95" sobrevive; "Use PostgreSQL" nao)       │
  │   - E verificavel por um evaluator?                       │
  │                                                         │
  │ Se uma constraint falha em qualquer criterio → reavalie   │
  │ a classificacao.                                         │
  └─────────────────────────────────────────────────────────┘
```

### Exemplo Concreto: Bloat → Budget

```
ORIGINAL (16 constraints, todas misturadas):
  1. Deve responder em < 200ms p95
  2. Use PostgreSQL para storage
  3. Implemente com Repository Pattern
  4. Use gRPC para comunicacao interna
  5. Deve estar disponível 99.9% do tempo
  6. Nao pode expor PII em logs
  7. Logs em formato JSON estruturado
  8. Adicione circuit breaker para dependencias externas
  9. Metrique com Prometheus
  10. Deploy via Kubernetes
  11. Health check no endpoint /health
  12. Rate limiting por IP
  13. Cache com Redis para queries frequentes
  14. Filas com RabbitMQ para processamento assincrono
  15. Testes unitarios com > 80% de cobertura
  16. Documentacao da API em OpenAPI 3.0

APOS O GATE:

CONSTRAINTS (6, dentro do budget):
  1. Deve responder em < 200ms p95              [qualidade]
  2. Deve estar disponivel 99.9% do tempo        [qualidade]
  3. Nao pode expor PII em logs                  [seguranca]
  4. Rate limiting por IP — max 100 req/s        [qualidade]
  5. Dados devem sobreviver a reinicializacao     [qualidade -
     do servico                                    reformulada de
                                                   "use PostgreSQL"]
  6. Comunicacao entre servicos deve ser confiavel [qualidade -
     e tipada                                      reformulada de
                                                   "use gRPC"]

CONTEXT (movido para o harness montar):
  - Stack de storage: PostgreSQL
  - Protocolo interno: gRPC
  - Orquestracao: Kubernetes
  - Observabilidade: Prometheus + JSON logs
  - Cache: Redis
  - Filas: RabbitMQ

EXPECTATIONS / FAILURE CONDITIONS (checaveis pos-output):
  - Health check responde em /health
  - Cobertura de testes > 80%
  - API documentada em OpenAPI 3.0
  - Circuit breaker funcional para dependencias externas

REJEITADO (nao pertence ao intent):
  - "Implemente com Repository Pattern" — instrucao de coding.
    Se for padrao do time, vai para Context como convencao
    de arquitetura, nao como constraint de outcome.
```

### O Criterio de Linguagem de Negocio

A pergunta-ancora: **"Um stakeholder nao-tecnico entende esta constraint?"**

| Constraint Original | Em Linguagem de Negocio? | Reformulacao |
|---|---|---|
| "Use PostgreSQL" | NAO — detalhe de infra | "Dados devem sobreviver a reinicializacao do servico e serem consultaveis por ID com latencia < 50ms" |
| "gRPC com Protobuf" | NAO — protocolo especifico | "Comunicacao entre servicos deve ser confiavel e tipada, sem perda de mensagens" |
| "Cache com Redis" | NAO — ferramenta especifica | "Consultas frequentes devem ser respondidas sem atingir o banco de dados principal" |
| "Deploy via Kubernetes" | NAO — plataforma | Nao e constraint de outcome. E Context (infraestrutura do time). |
| "Nao pode expor PII" | SIM — e claro para qualquer pessoa | Mantem. |
| "< 200ms p95" | SIM — performance e universal | Mantem. |

## Implementation Rules

1. **5-7 e uma heuristica, nao uma lei.** Dominios regulados podem precisar de mais constraints de compliance. Documente o excesso e justifique por que cada constraint extra e genuinamente uma restricao de outcome, nao uma decisao de implementacao. O budget existe para forcar a conversa, nao para substituir o julgamento.

2. **Constraints em linguagem de implementacao sao frageis.** "Use PostgreSQL" quebra se o time migrar para MongoDB. "Dados devem sobreviver a reinicializacao do servico" sobrevive a qualquer storage. Constraints devem ser estaveis sob mudancas de stack, arquitetura, e time.

3. **Toda constraint rejeitada tem destino.** Nada desaparece. Implementacao → Context (o harness monta). Checks pos-output → Expectations ou Failure Conditions. Instrucoes de coding → removidas do intent (pertencem ao guia de estilo ou convencoes do time, nao ao contrato do agente).

4. **O budget e aplicado ANTES do agente receber o intent.** Constraints que excedem o budget e nao foram reclassificadas viram specs escondidas. O gate e pre-flight, nao mid-execution -- nao se corta constraints enquanto o agente esta buildando.

5. **Constraints direcionais guiam; constraints binarias engessam.** "Deve ser rapido" da direcao e deixa o builder decidir como. "Deve responder em < 200ms" da um alvo mensuravel sem ditar metodo. "Deve usar cache Redis com TTL de 5 minutos" ditou tudo -- e uma spec, nao uma constraint.

6. **O budget gate compoe com o constraint-failure decision rule.** Primeiro, classifique cada requisito como constraint ou failure condition (constraint-failure decision rule). Depois, para os itens classificados como constraint, aplique o budget gate. A ordem importa: o decision rule define O QUE e constraint; o budget gate define QUAIS constraints ficam.

## Integration with Existing Repo Infrastructure

O constraint-budget-gate opera como gate de qualidade sobre o campo Constraints, complementando a infraestrutura de avaliacao e alinhamento:

| Componente Existente | Como o Constraint Budget Gate complementa |
|---|---|
| [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]] | O primitivo de cinco partes garante que o campo Constraints existe. O budget gate garante que o conteudo desse campo e enxuto, direcional, e em linguagem de negocio -- qualidade sobre quantidade. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A avaliacao ancorada em constraints verifica cada constraint contra o output. Com budget controlado (≤7), a verificacao e rapida, focada, e cada falha sinaliza um problema real. Com 16 constraints, a avaliacao e lenta, ruidosa, e falsos positivos minam a confianca. |
| [[.opencode/skills/constraint-failure-decision-rule/SKILL|constraint-failure-decision-rule]] | O decision rule classifica requisitos como constraint ou failure condition. O budget gate recebe os itens classificados como constraint e aplica o limite de 5-7. Fluxo composto: decision rule → budget gate → purificacao final. |
| [[docs/canonical/ice-craft-separation|ICE Craft Separation]] | A separacao de crafts atribui Context ao harness. O budget gate identifica constraints que sao na verdade Context (padroes do time, stack, infra) e as move para o harness montar -- preservando a separacao que a arquitetura define. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Generator recebe constraints como guia de design. Constraints infladas viram spec -- o Generator perde latitude. Constraints enxutas (≤7, direcionais) maximizam a capacidade de geracao enquanto previnem outputs inaceitaveis. |
| [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]] | O budget gate identifica constraints que sao na verdade Expectations (checaveis pos-output) e as move para o campo correto, mantendo a fronteira entre o que guia o builder (constraints) e o que valida o output (expectations). |
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me captura constraints durante a entrevista. O budget gate revisa as constraints capturadas: "Voce disse 12 coisas. 5 sao constraints de verdade. As outras 7 sao contexto ou expectations. Confirma?" |
| [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]] | O control plane monta o Context. Constraints movidas para Context pelo budget gate alimentam o assembly de contexto do control plane, garantindo que informacao de stack e time chega ao builder sem poluir o intent. |

## Quality Gates

Antes de declarar o campo Constraints como aprovado pelo budget gate, verifique:

- [ ] O numero de constraints no campo Constraints e ≤ 7 (ou o excesso esta documentado e justificado)
- [ ] Cada constraint descreve uma qualidade do outcome, nao uma decisao de implementacao
- [ ] Cada constraint esta em linguagem de negocio -- um stakeholder nao-tecnico entende o que ela significa
- [ ] Cada constraint e direcional ("o outcome deve ser X") ou tem um alvo mensuravel, nao e um check binario pos-output
- [ ] Cada constraint e incondicional -- nao depende de contexto que o builder teria que adivinhar
- [ ] Items de implementacao removidos do campo Constraints foram movidos para Context (com destino explicito)
- [ ] Items de verificacao removidos foram movidos para Expectations ou Failure Conditions
- [ ] Items rejeitados tem motivo documentado e destino explicito (nao desapareceram)
- [ ] Constraints sobreviventes sobrevivem a uma mudanca hipotetica de stack (PostgreSQL → MongoDB? gRPC → REST?)
- [ ] O gate foi aplicado ANTES que o agente recebesse o intent (pre-flight)

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]:176 -- Failure pattern #2: Constraint list bloat e limite de 5-7 como mitigacao
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]:187 -- Failure pattern #7: Drift silencioso do metodo via constraints
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:104-126 -- Pattern 5: Constraint Budget Gate
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]:141-166 -- Classificacao como Missing (Medium integration value)
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:89 -- Nota sobre constraint list growth como custo
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]] -- estrutura que contem o campo Constraints
- [[.opencode/skills/constraint-failure-decision-rule/SKILL|constraint-failure-decision-rule]] -- decision rule que classifica requisitos antes do budget gate
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]] -- separacao de crafts que define Context como propriedade do harness
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]] -- destino de constraints que sao na verdade expectations
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]] -- control plane que monta Context a partir de constraints reclassificadas

---

*Created: 2026-06-14 | Source: The Anatomy of Intent - ICE in IDSD — Pattern 5 (Missing, Medium value)*
