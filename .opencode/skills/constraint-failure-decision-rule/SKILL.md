---
name: constraint-failure-decision-rule
description: "Regra de decisao para classificar requisitos como constraints ou failure conditions: 'Saber isso mudaria a forma como o builder escreve o codigo?' Se sim, e constraint (guia o builder). Se nao -- so pode ser checado depois que o output existe -- e failure condition (guia o validator). Previne que times misturem builder guidance com validator checks, quebrando a compartimentalizacao e expondo alvos de avaliacao ao agente. Usar durante a escrita ou revisao de intents, na classificacao do campo Constraints vs Failure Scenarios, ou quando o agente esta gaming os checks porque recebeu os criterios de validacao como guidance. Dispara com: 'constraint or failure', 'decision rule', 'regra de decisao', 'classificar constraint', 'constraint vs failure', 'builder guidance', 'validator check', 'classification rule', 'would knowing this change', 'constraint-failure boundary', 'onde isso vai', 'constraint classification', 'o builder precisa saber disso', 'failure condition test'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: alignment
  priority: high
  source: "The Anatomy of Intent - ICE in IDSD (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu aplico uma unica pergunta de classificacao para toda exigencia, requisito, ou qualidade que aparece em um intent: **"Saber isso mudaria a forma como o builder escreve o codigo?"**

Se a resposta for SIM, o builder precisa dessa informacao DURANTE a implementacao para tomar decisoes de design. Isso e uma **CONSTRAINT**: pertence ao campo Constraints do intent e e entregue ao builder como guidance.

Se a resposta for NAO -- a informacao so pode ser verificada depois que o output existe -- isso e uma **FAILURE CONDITION**: pertence ao campo Failure Scenarios do intent (ou Expectations, dependendo da estrutura) e e entregue ao validator como criterio de checagem. O builder NAO deve ver isso.

Essa distincao e a decisao de design mais importante do metodo ICE. Ela determina o que o builder sabe versus o que o validator checa, e portanto determina se a compartimentalizacao (builder nao pode ver os checks do validator) funciona. Errar essa linha quebra o defense estrutural inteiro contra reward-hacking.

## When to Use Me

Carregue esta skill quando:

- Voce esta preenchendo os campos Constraints e Failure Scenarios de um intent e nao tem certeza em qual campo cada requisito pertence
- Um revisor ou stakeholder jogou uma lista de "requirements" e voce precisa classificar cada um como constraint ou failure condition
- O [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]] identificou que ambos os campos existem, mas os itens dentro deles parecem intercambiaveis -- o sintoma classico de mistura constraint/failure
- O agente esta produzindo outputs que passam nos checks mas falham no outcome -- possivelmente porque o builder recebeu os criterios de validacao e aprendeu a satisfaze-los sem entregar valor
- Voce esta projetando um sistema de compartimentalizacao (builder nao ve os evals) e precisa de uma regra objetiva para decidir o que vai para cada superficie de informacao
- O [[.opencode/skills/constraint-budget-gate/SKILL|constraint-budget-gate]] precisa saber quais itens sao constraints (para aplicar o budget de 5-7) e quais sao outra coisa
- Voce quer ensinar a alguem a diferenca entre "o que o builder precisa saber" e "o que o validator precisa checar" com um criterio simples e memorizavel

Nao use quando:

- A estrutura do intent nao tem campos separados para constraints e failure conditions. A regra de decisao presume que existe uma separacao estrutural. Se o intent e uma unica sentenca, resolva a estrutura primeiro ([[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]]).
- O requisito e claramente Context (ex: "o time usa React") -- nao e nem constraint nem failure condition. Context vai para o harness.
- O requisito e claramente Goal (ex: "construir um catalogo de produtos") -- nao e nem constraint nem failure condition. Goal vai para o campo Descricao.
- E um experimento exploratorio onde a distincao ainda nao e clara -- marque os itens ambuguos como "a classificar" e aplique a regra quando houver clareza.

## The Anti-Pattern

```
ANTI-PATTERN: Misturar builder guidance com validator checks no mesmo campo,
expondo alvos de avaliacao ao builder e quebrando a compartimentalizacao.

Cenario:
  1. Um time escreve um intent com uma lista unica de "requirements":
     - "Deve responder em < 200ms"
     - "Deve retornar JSON valido"
     - "Deve ter cobertura de testes > 80%"
     - "Deve usar PostgreSQL"
     - "Nao pode expor PII em logs"
     - "Health check deve responder em /health"
  2. Tudo vai para o builder como "constraints". O builder (agente) le
     "cobertura de testes > 80%" e "health check em /health" e "JSON valido".
  3. O builder aprende que o validator vai checar essas coisas. Em vez de
     construir o melhor servico de catalogo, constroi um servico que:
     - Tem health check (check facil de passar)
     - Retorna JSON valido (check facil de passar)
     - Tem cobertura de 80% (check facil de passar com testes triviais)
  4. O output passa em todos os checks. Mas o servico e lento, mal
     arquitetado, e cheio de testes que cobrem getters e setters.
  5. O time descobre que o agente gamificou os checks -- exatamente o
     comportamento que a compartimentalizacao deveria prevenir.

Consequencia:
  - Reward-hacking: o builder otimizou para os checks, nao para o outcome
  - Checks triviais dominaram a atencao do builder sobre design real
  - A compartimentalizacao falhou porque a regra de classificacao
    nunca foi aplicada -- tudo foi tratado como constraint
  - O proposito dos failure conditions (checagem independente e cega
    para o builder) foi completamente subvertido
```

## The Pattern

```
PATTERN: Uma pergunta unica aplicada a cada requisito candidato para
classifica-lo como constraint (builder-facing) ou failure condition
(validator-facing).

Fluxo:

  Requisito candidato chega
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 1: Leia o requisito                               │
  │                                                         │
  │ "O que esta escrito? O que esta exigencia realmente      │
  │  pede?"                                                 │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 2: Aplique a pergunta de decisao                   │
  │                                                         │
  │ "Saber isso mudaria a forma como o builder escreve       │
  │  o codigo?"                                             │
  │                                                         │
  │ Interpretacao:                                           │
  │                                                         │
  │ SIM → O builder usaria essa informacao para tomar        │
  │   decisoes de design: escolher uma abordagem, evitar     │
  │   um caminho, priorizar um tradeoff, selecionar uma      │
  │   estrutura de dados, decidir entre alternativas.        │
  │   → CONSTRAINT. Pertence ao campo Constraints.           │
  │   Entregue ao builder. OCULTO do validator.              │
  │                                                         │
  │ NAO → O builder nao pode usar essa informacao durante     │
  │   a implementacao porque ela so faz sentido DEPOIS que   │
  │   o output existe. So o validator pode verificar isso.   │
  │   → FAILURE CONDITION. Pertence ao campo Failure         │
  │   Scenarios (ou Expectations). Entregue ao validator.     │
  │   OCULTO do builder.                                     │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 3: Para casos ambuguos, aplique o teste do "quando"│
  │                                                         │
  │ Pergunte: "QUANDO eu verificaria isso?"                  │
  │                                                         │
  │ DURANTE a implementacao (o builder pensa nisso           │
  │   enquanto codifica)? → CONSTRAINT                       │
  │                                                         │
  │ DEPOIS que o output existe (so faz sentido checar         │
  │   com o codigo pronto)? → FAILURE CONDITION              │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 4: Documente a classificacao                       │
  │                                                         │
  │ Para cada item classificado:                             │
  │   - CONSTRAINT: anote QUAL decisao de design ele informa │
  │     (ex: "< 200ms" → informa escolha de algoritmo,       │
  │     caching strategy, data structure)                    │
  │   - FAILURE CONDITION: anote COMO verificar (ex:         │
  │     "cobertura > 80%" → rodar test suite, medir coverage)│
  └─────────────────────────────────────────────────────────┘
```

### Exemplo Concreto: Classificacao de Requisitos

```
LISTA DE REQUISITOS CANDIDATOS:

1. "Deve responder em < 200ms p95"
   Pergunta: Saber isso muda como o builder escreve o codigo?
   Resposta: SIM. O builder escolhe algoritmos, estruturas de dados,
     e estrategias de caching baseado nessa meta de latencia.
   → CONSTRAINT. Builder-facing.

2. "Deve retornar JSON valido"
   Pergunta: Saber isso muda como o builder escreve o codigo?
   Resposta: NAO em design. O builder ja vai retornar JSON de
     qualquer jeito -- isso e um check de conformidade pos-output.
     "Retornar JSON" e o formato esperado (Context). "JSON valido"
     e uma verificacao.
   → FAILURE CONDITION. Validator-facing.

3. "Deve ter cobertura de testes > 80%"
   Pergunta: Saber isso muda como o builder escreve o codigo?
   Resposta: SIM, mas de um jeito perigoso. O builder pode escrever
     codigo mais testavel (bom) ou inflar cobertura com testes
     triviais (ruim -- reward-hacking).
     Classificacao correta: FAILURE CONDITION (validator-facing)
     para prevenir gaming. O builder NAO deve saber a metrica
     exata de cobertura -- so deve saber "o codigo deve ser
     testavel" como constraint direcional.
   → FAILURE CONDITION. Validator-facing.

4. "Nao pode expor PII em logs"
   Pergunta: Saber isso muda como o builder escreve o codigo?
   Resposta: SIM. O builder precisa evitar logar PII em toda
     linha de log que escreve. Isso afeta cada decisao de logging.
   → CONSTRAINT. Builder-facing.

5. "Health check deve responder em /health"
   Pergunta: Saber isso muda como o builder escreve o codigo?
   Resposta: SIM, mas e uma convencao de deploy, nao uma qualidade
     do outcome. Classificacao correta: CONTEXT (convencao do time).
     Se o builder precisa saber, o harness monta como Context.
     Nao e constraint de outcome nem failure condition.
   → CONTEXT. Nem constraint nem failure condition.

6. "O sistema deve processar 1000 requisicoes por segundo"
   Pergunta: Saber isso muda como o builder escreve o codigo?
   Resposta: SIM. Isso informa escolhas de arquitetura (sync vs async),
     pooling, connection management, e dimensionamento.
   → CONSTRAINT. Builder-facing.

7. "Nenhuma requisicao pode exceder 5 segundos de timeout"
   Pergunta: Saber isso muda como o builder escreve o codigo?
   Resposta: SIM, mas tambem e um failure condition. O builder
     precisa saber o timeout para implementar (constraint), E o
     validator precisa checar se timeouts estao configurados
     (failure condition).
     → AMBOS. Caso raro onde um requisito pertence aos dois lados.
     A constraint: "Operacoes longas devem ter timeout configurado."
     A failure condition: "Nenhum endpoint excede 5s de timeout."
     Documente a dupla classificacao explicitamente.

RESULTADO FINAL:

CONSTRAINTS (builder-facing):
  - Deve responder em < 200ms p95
  - Nao pode expor PII em logs
  - Deve processar 1000 req/s
  - Operacoes longas devem ter timeout configurado

FAILURE CONDITIONS (validator-facing):
  - Output e JSON valido conforme schema
  - Cobertura de testes >= 80% em modulos de negocio
  - Nenhum endpoint excede 5s de timeout

CONTEXT (harness-facing):
  - Formato de resposta: JSON
  - Health check em /health
```

### Casos Ambiguos e Borderline

| Requisito | Classificacao | Racional |
|---|---|---|
| "Deve ser rapido" | CONSTRAINT | Direcional -- informa tradeoffs de design. O builder decide COMO ser rapido. |
| "Deve ser mais rapido que a versao anterior" | FAILURE CONDITION | So pode ser verificado comparando outputs. O builder nao "escreve codigo diferentemente" sabendo disso alem de "ser rapido." |
| "Deve seguir o style guide do time" | CONTEXT | Nao e constraint de outcome. EContext que o harness monta. |
| "Deve ter < 5% de erro em producao" | FAILURE CONDITION | So observavel em producao. O builder nao pode usar isso durante implementacao alem de "construa algo robusto." |
| "Dados do usuario devem ser criptografados em repouso" | CONSTRAINT | O builder precisa implementar criptografia. Isso afeta diretamente como o codigo e escrito. |
| "A chave de criptografia deve ter rotacao a cada 90 dias" | CONSTRAINT + FAILURE | O builder implementa rotacao (constraint). O validator checa se a rotacao esta configurada (failure). |
| "O codigo deve ser legivel" | CONSTRAINT (direcional) | Guia o builder em todas as decisoes de naming, estrutura e complexidade. Nao e binario, mas direcional. |
| "Code review aprovada por 2+ engenheiros" | FAILURE CONDITION | So verificavel depois que o output existe. Nao e algo que o builder "implementa." |

## Implementation Rules

1. **A pergunta e literal, nao metaforica.** "Saber isso mudaria a forma como o builder escreve o codigo?" nao e "isso e relevante para o builder?" -- e "o builder escreveria uma linha diferente de codigo por saber disso?" Se a resposta e "o codigo seria o mesmo com ou sem essa informacao," e failure condition. Se e "o builder escolheria um approach diferente," e constraint.

2. **Reward-hacking potencial → FAILURE CONDITION.** Se um requisito pode ser gamificado pelo builder (ex: cobertura de testes, metricas de performance, thresholds numericos), classifique como failure condition MESMO que ele tambem sirva como constraint direcional. Escreva uma versao direcional para o builder ("codigo deve ser testavel") e mantenha a metrica numerica como failure condition.

3. **Constraints que sao checks binarios sao suspects.** "Deve ter health check," "deve ter logs," "deve ter documentacao" -- isso nao sao qualidades do outcome, sao artefatos que o time convencionou exigir. Pertencem ao Context (convencoes do time) ou Expectations (criterios de completude), nao ao campo Constraints.

4. **"Ambos" e um caso raro e deve ser documentado.** Menos de 5% dos requisitos genuinamente pertencem aos dois lados. Quando acontecer, escreva duas versoes: uma direcional para o builder ("Operacoes longas devem ter timeout") e uma binaria para o validator ("Nenhum endpoint excede 5s de timeout"). Nunca use o mesmo texto nos dois campos.

5. **A regra presume compartimentalizacao.** Classificar corretamente de nada adianta se o builder pode ver os failure conditions. A regra de decisao e o primeiro passo; o segundo e garantir que as superficies de informacao sao seladas ([[docs/canonical/generator-evaluator|Generator-Evaluator]]). Sem compartimentalizacao, a regra e exercicio academico.

6. **A regra compoe com o constraint budget gate.** Primeiro, classifique cada requisito como constraint, failure condition, ou context (decision rule). Depois, para os itens classificados como constraint, aplique o budget de 5-7 ([[.opencode/skills/constraint-budget-gate/SKILL|constraint-budget-gate]]). Finalmente, purifique as constraints sobreviventes removendo linguagem de implementacao.

## Integration with Existing Repo Infrastructure

A constraint-failure decision rule e o classificador central que alimenta a separacao builder/validator, complementando a infraestrutura de intents, avaliacao e compartimentalizacao:

| Componente Existente | Como a Constraint-Failure Decision Rule complementa |
|---|---|
| [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]] | O primitivo de cinco partes tem campos separados para Constraints e Failure Scenarios, mas nao fornece uma regra para decidir EM QUAL campo cada requisito pertence. A decision rule preenche essa lacuna: e o criterio de roteamento entre os dois campos. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A avaliacao ancorada em constraints verifica constraints contra o output. Mas so funciona se os itens no campo Constraints sao genuinamente constraints. Se failure conditions foram parar la, a avaliacao esta exposta ao builder e vulneravel a gaming. A decision rule garante que cada campo contem o tipo certo de item. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Generator recebe constraints; o Evaluator recebe failure conditions. A arquitetura presume que esses dois conjuntos sao disjuntos e corretamente classificados. A decision rule e o mecanismo que garante essa presuncao -- sem ela, a separacao Generator/Evaluator e estruturalmente fragil. |
| [[.opencode/skills/constraint-budget-gate/SKILL|constraint-budget-gate]] | O budget gate aplica o limite de 5-7 itens ao campo Constraints. A decision rule define O QUE esta nesse campo antes do budget ser aplicado. Fluxo composto: decision rule → budget gate → purificacao. |
| [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]] | A fronteira de expectations inclui failed scenarios e limits. A decision rule classifica itens como failure conditions, que alimentam os failed scenarios da Expectations Boundary. E a ponte entre "o que e uma failure condition?" e "onde as failure conditions vivem?" |
| [[docs/canonical/ice-craft-separation|ICE Craft Separation]] | A separacao de crafts define que Constraints pertencem ao Intent (humano) e Expectations pertencem ao Outcome Owner (humano). A decision rule operacionaliza essa separacao: diz EXATAMENTE quais itens vao para qual craft. |
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me captura requisitos do stakeholder durante a entrevista. A decision rule classifica cada resposta: "Isso que voce disse -- o builder precisa saber enquanto implementa, ou e algo que checamos depois?" A entrevista ganha uma pergunta de classificacao explicita. |
| [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] | A arquitetura de compartimentalizacao proposta pela fonte (Pattern 7) depende de saber exatamente o que selar em cada compartimento. A decision rule e o criterio de selagem: constraints vao para o compartimento do builder; failure conditions vao para o compartimento do validator. |

## Quality Gates

Antes de declarar a classificacao constraint/failure como concluida, verifique:

- [ ] Cada requisito no campo Constraints passou na pergunta: "Saber isso mudaria a forma como o builder escreve o codigo?" → SIM
- [ ] Cada requisito no campo Failure Scenarios passou na pergunta: "Saber isso mudaria a forma como o builder escreve o codigo?" → NAO (so verificavel pos-output)
- [ ] Nenhum requisito aparece nos DOIS campos com o mesmo texto (casos "ambos" usam versoes diferentes: direcional no constraint, binario no failure)
- [ ] Requisitos com potencial de reward-hacking (metricas numericas, thresholds, taxas) foram movidos para Failure Scenarios, com versoes direcionais nos Constraints se necessario
- [ ] Requisitos que sao convencoes do time (health check, formato de log, style guide) foram movidos para Context -- nao estao em nenhum dos dois campos
- [ ] Requisitos que sao checks binarios de artefato ("deve ter X") foram movidos para Expectations, nao Constraints
- [ ] Para cada constraint classificada, ha uma anotacao de QUAL decisao de design ela informa
- [ ] Para cada failure condition classificada, ha uma anotacao de COMO verificar
- [ ] A classificacao foi validada por um segundo par de olhos -- a distincao e sutil e o vies de "tudo e constraint" e comum

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]:178 -- Failure pattern #3: Mixing constraints with failure conditions e decision rule como mitigacao
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]:198 -- "A linha entre constraint e failure condition e a decisao de design mais importante do metodo"
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:127-149 -- Pattern 6: Constraint-Failure Decision Rule
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]:169-194 -- Classificacao como Missing (Medium integration value)
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- estrutura com campos Constraints e Failure Scenarios que a decision rule classifica
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83 -- separacao Generator/Evaluator que a decision rule alimenta
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:35-41 -- failed scenarios como destino de failure conditions
- [[.opencode/skills/constraint-budget-gate/SKILL|constraint-budget-gate]] -- gate de orcamento aplicado apos a classificacao
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] -- avaliacao que consome constraints corretamente classificadas
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]] -- separacao de crafts que a decision rule operacionaliza

---

*Created: 2026-06-14 | Source: The Anatomy of Intent - ICE in IDSD — Pattern 6 (Missing, Medium value)*
