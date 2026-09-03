---
title: "Two-Layer Output Contract"
type: canonical
status: accepted
date: 2026-09-02
tags: ["harness-engineering", "agentes-orquestracao", "agent-loop", "error-handling", "evals"]
aliases: ["two layer output contract", "contrato de saída em duas camadas", "prompt layer harness layer format", "format contract enforcement"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]", "[[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Two-Layer Output Contract

**Type:** Canonical Pattern
**Status:** accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 8)
**Classification:** Partial Coverage / Medium ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:148, :259)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Confiar apenas no texto do prompt para consistência de formato produz drift: o modelo adere ao formato na maioria das vezes e escapa nas demais, e consumidores de máquina de saída estruturada não toleram escape nenhum ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:156). Instrução de formato é compliance — depende de o modelo lembrar e escolher seguir; a garantia precisa morar na estrutura ("the rule lives in the gate, not the memory", [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]:69-71).

## Solução

Definir o formato **uma vez** e enforce nas **duas camadas** — a mesma definição aparece no prompt e no harness, como um só contrato:

1. **Prompt layer (definição):** o formato declarado em texto estruturado — por exemplo, XML tags envolvendo a resposta ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:158).
2. **Harness layer (enforcement):** mecanismos programáticos que tornam o escape impossível de servir — stop sequence que detecta a closing tag e encerra a geração na fronteira do contrato; structured outputs (JSON schema nativo) para estruturas aninhadas ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:159, :162).

**Right-sizing do contrato pela classe de saída** ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:160, :165):

| Tipo de saída | Contrato | Enforcement |
|---|---|---|
| Conversacional (sem consumidor de máquina) | Leve | Formato no prompt; sem maquinaria pesada |
| Estruturada (consumidor de máquina) | Pesado | Stop sequence/structured outputs + validação de schema na fronteira |

```text
Format definition (XML tags / JSON schema)
        |
   +----+----+
   v         v
Prompt     Harness
layer      layer
(define)   (enforce: stop sequence na closing tag,
            structured outputs para JSON aninhado)
   |         |
   +----+----+
        v
 Generation para na fronteira do contrato;
 schema constrange a estrutura antes do consumo
```

Enforcement de harness garante consistência em grau maior que instrução textual e sobrevive a migration de modelo melhor que "format pleading" no prompt ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:164, :166).

## Implementação neste repositório

### O que já existe

A camada heavy (harness-side) está coberta em profundidade canônica e ensinada desde o Nível 1:

- [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]:42 — structured outputs como contrato de saída, com o kernel validando o evento no publish e no consume; `:44` — "A fronteira rejeita, não corrige".
- [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]:29 — um circuito de ação-segura com output schema, generation prompt, validador pós-geração, política de repair/rejection e audit log.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:24 — "The model emits JSON (a structured output)"; `:107` — "Built on: Pattern 1 (Structured Output Contract)".
- `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md:37-39` — o repo trata structured output como pressuposto foundational; o exercício de N1 o ensina como um dos 5 padrões básicos de harness ([[curriculum/01-nivel-1-fundamentals/exercises/exercise-02-structured-output|Exercício N1: Structured Output]]).
- [[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution]]:947 — "Structured Output nativo | Format Validator, Output Parser, Schema Enforcer" como componentes de harness.
- O princípio geral está codificado em [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]:46-47 — mover a garantia de compliance para estrutura.

### O que falta

(Classificação:150, :162 — NOT_FOUND com locais pesquisados.)

1. **O pareamento explícito das duas camadas** — o mesmo formato definido no prompt (XML tags) e enforced no harness (stop sequence detectando a closing tag; structured outputs para JSON aninhado) como um único contrato. O repo tem as camadas separadas (prompt ensina formato; harness valida schema) sem a convenção de que são o mesmo contrato espelhado.
2. **A regra de right-sizing** — saída conversacional carrega contrato leve; saída estruturada com consumidor de máquina carrega enforcement pesado. Ausente de `docs/canonical/`, `docs/decisions/`, `curriculum/`.
3. **Stop sequence como fronteira de formato** — os `stop_sequences` do currículo são delimitadores de conteúdo para controle de custo/bloat ("Controla custo e evita responses bloated", [[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|Generator-Evaluator Pattern]]:737-748), não enforcement de closing tag.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Consistência de formato garantida programaticamente, não por texto de prompt | Stop sequence exige conhecer o token terminal do formato |
| Right-sizing: contrato leve onde não há consumidor de máquina, pesado onde há | Structured outputs acoplam schema à superfície de API; mudança de schema vira mudança de API |
| Sobrevive a migration de modelo melhor que format pleading no prompt | Overkill para saídas sem consumidor de máquina downstream |

## Relação com outros padrões

- **Pareia com:** [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]] — este padrão define o contrato nas duas camadas; aquele valida o evento na fronteira (publish/consume).
- **Executa via:** [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]] — o validador pós-geração é a máquina de enforcement da camada harness.
- **Substrato de:** [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] — o dispatch determinístico lê o JSON que este contrato garante (`:107`).
- **Instancia:** [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]] — formato é o caso canônico de mover a regra do prompt para o gate (`:69-71`).
- **Ensina junto de:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] — a avaliação determinística de formato (hard) precede o judge semântico.

## Referências

- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:153-170 — definição do padrão 8 (inputs, outputs, benefícios, limitações).
- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:146-164 — Partial Coverage/Medium com evidência file:line e NOT_FOUND.
- [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]:42, :44 — structured outputs como contrato de saída; fronteira rejeita, não corrige.
- [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]:29 — circuito com output schema, validador e repair/rejection.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:24, :107 — structured output como entrada do dispatch.
- [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]:46-47, :69-71 — garantia na estrutura, não na memória.
- [[curriculum/01-nivel-1-fundamentals/exercises/exercise-02-structured-output|Exercício N1: Structured Output]] — structured output como padrão básico de harness.
- [[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|Generator-Evaluator Pattern]]:737-748 — `stop_sequences` no generator config (controle de custo, não fronteira de contrato).
- [[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution]]:947 — Format Validator, Output Parser, Schema Enforcer.

---

*Criado: 2026-09-02 | De: The Prompting Playbook classification | Precedência: canonical*
