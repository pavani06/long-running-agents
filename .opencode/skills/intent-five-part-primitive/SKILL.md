---
name: intent-five-part-primitive
description: "Formaliza o intent como primitivo de cinco partes — descricao, constraints, cenarios de falha, cenarios de sucesso e conexoes — antes que qualquer agente comece a implementar. Elimina a ambiguidade que forcaria o agente a preencher lacunas com suposicoes durante a execucao. Usar quando uma tarefa, feature ou outcome chega para execucao agentica sem os cinco campos preenchidos, durante a fase de alinhamento (Grill-Me), ou quando o agente esta queimando tokens em retries por falta de clareza. Dispara com: 'intent de cinco partes', 'five-part intent', 'intent completeness gate', 'intent primitivo', 'campos do intent', 'intent structure', 'intent gaps', 'descreva o intent', 'falta constraints', 'cenarios de falha', 'cenarios de sucesso', 'conexoes do intent', 'intent traceability', 'impacto downstream'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: alignment
  priority: high
  source: "IDSD — Intent-Driven Software Development (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu formalizo o intent como um primitivo de primeira classe com cinco campos obrigatorios. Meu trabalho nao e gerar codigo -- e garantir que, antes que qualquer agente comece a implementar, o intent esta completo o suficiente para que o agente nao precise adivinhar constraints, cenarios de falha, cenarios de sucesso ou conexoes com outros sistemas.

Os cinco campos sao:

1. **Descricao** — o que se quer atingir, em linguagem do outcome-owner
2. **Constraints** — limites que o trabalho deve respeitar (tecnicos, de negocio, de dominio)
3. **Cenarios de falha** — outputs que seriam inaceitaveis e como detecta-los
4. **Cenarios de sucesso** — o resultado desejado em termos observaveis e verificaveis
5. **Conexoes** — outros intents, sistemas, workflows ou decisoes afetados por uma mudanca aqui

Cada campo faltante e um buraco que o agente sera forcado a preencher durante a execucao. Meu output e um veredito: **passa** (todos os cinco campos com conteudo suficiente), **clarifica** (campos especificos precisam de mais detalhe), ou **incompleto** (devolver ao outcome-owner com perguntas concretas).

## When to Use Me

Carregue esta skill quando:

- Uma tarefa, feature ou outcome chega para execucao agentica com descricao vaga ("implementa X", "adiciona Y", "melhora Z")
- O ciclo de alinhamento (Grill-Me, Manual Brake) esta para iniciar e o intent precisa ser estruturado antes das perguntas de valor
- Um agente esta queimando tokens em retries, explorando opcoes, ou produzindo outputs que "parecem certos" mas sao rejeitados -- o sintoma classico de gaps no intent
- Voce suspeita que o agente esta decidindo coisas que deveriam ter sido decididas pelo outcome-owner
- Uma mudanca em um sistema esta sendo planejada e voce quer rastreabilidade de impacto (o que mais quebra se isso mudar?)
- O outcome-owner e um stakeholder nao-tecnico e o intent precisa ser traduzido para campos acionaveis sem jargao de implementacao
- Voce quer registrar o intent como artefato duraivel para auditoria futura (por que isso foi construido? O que definia sucesso?)

Nao use quando:

- A tarefa e puramente mecanica (ex: bump de dependencia, correcao de lint) onde os cinco campos sao triviais ou irrelevantes
- O intent ja foi capturado com estrutura equivalente (ex: [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] ja especifica comportamento observavel, constraints e cenario de falha)
- E um experimento exploratorio onde o proposito e exatamente descobrir constraints e cenarios -- neste caso, marque os campos desconhecidos como "a descobrir" em vez de bloquea-los
- A tarefa e um hotfix ou incidente SEV1/SEV2 onde a urgencia operacional substitui a formalizacao completa (mas registre o intent a posteriori para o postmortem)

## The Anti-Pattern

```
ANTI-PATTERN: Intent como frase unica — o agente preenche o resto.

Cenario:
  1. Um stakeholder escreve: "adiciona suporte a pagamentos via PIX"
  2. O agente recebe essa frase como input unico.
  3. O agente precisa decidir: quais bancos? Precisa de conciliacao? Qual timeout?
     O que acontece se o PSP estiver fora do ar? O que constitui "funcionou" —
     o pagamento foi criado, processado, ou confirmado? Isso afeta o modulo
     de notificacoes? E o refund?
  4. O agente decide tudo isso sozinho. Produz 800 linhas. O codigo compila.
     Os testes passam.
  5. Duas semanas depois: o PIX funciona para o banco A, mas quebra no banco B
     (constraint nao declarada). O refund nao notifica o cliente (conexao nao
     mapeada). "Sucesso" foi definido como "endpoint retorna 200", nao como
     "cliente recebeu o produto" (cenario de sucesso errado).

Consequencia:
  - Tokens queimados em implementar a coisa errada e depois consertar
  - Constraints omitidas viram bugs em producao
  - Conexoes nao mapeadas viram regressoes ("ninguem sabia que isso afetava aquilo")
  - O outcome-owner descobre na revisao que o agente entendeu "sucesso"
    de um jeito que nao corresponde ao que ele queria
```

O padrao de falha e sempre o mesmo: o intent entrou como frase unica ou paragrafo vago, e o agente usou tokens para preencher os quatro campos faltantes com suposicoes. Quanto maior o diff, maior a aposta de que as suposicoes estao erradas.

## The Pattern

```
PATTERN: Cinco campos obrigatorios preenchidos antes que o agente receba a tarefa.

Fluxo:

  Tarefa chega
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 1: O outcome-owner escreve a DESCRICAO             │
  │                                                         │
  │ "O que voce quer que aconteca quando isso estiver        │
  │  pronto?"                                               │
  │                                                         │
  │ Exemplo: "Um comprador pode buscar tenis vermelhos,      │
  │ filtrar por preco maximo de $90, ver apenas itens em     │
  │ estoque no seu tamanho, e completar a compra."           │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 2: O outcome-owner lista CONSTRAINTS               │
  │                                                         │
  │ "O que NAO pode acontecer? Quais limites o resultado     │
  │  DEVE respeitar?"                                       │
  │                                                         │
  │ Exemplo:                                                │
  │ - Tamanho do comprador (nao mostrar tenis fora do tamanho)│
  │ - Em estoque (nao mostrar itens esgotados)               │
  │ - Entregavel para o CEP do comprador                     │
  │ - Preco final (com frete e impostos) < $90               │
  │ - Deve ser vermelho (nao "similar ao vermelho")          │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 3: O outcome-owner define CENARIOS DE FALHA        │
  │                                                         │
  │ "Se o output for X, esta errado. Como eu sei?"           │
  │                                                         │
  │ Exemplo:                                                │
  │ - Retorna um tenis de $140 (viola constraint de preco)   │
  │ - Retorna um tenis fora de estoque                       │
  │ - Retorna um tenis nao-vermelho                          │
  │ - Retorna um tenis que nao entrega no CEP do comprador   │
  │ - Nenhum tenis encontrado e o agente nao reporta         │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 4: O outcome-owner define CENARIOS DE SUCESSO      │
  │                                                         │
  │ "O que eu vejo acontecer quando isso funcionar?"         │
  │                                                         │
  │ Exemplo:                                                │
  │ - Comprador ve uma lista de tenis vermelhos no tamanho   │
  │   dele, todos abaixo de $90 com frete                    │
  │ - Comprador adiciona um ao carrinho                      │
  │ - Comprador completa checkout                            │
  │ - Confirmacao de pedido e enviada                        │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 5: O outcome-owner mapeia CONEXOES                 │
  │                                                         │
  │ "O que mais quebra ou muda se isso for alterado?"        │
  │                                                         │
  │ Exemplo:                                                │
  │ - Modulo de precos (qualquer mudanca em preco afeta)     │
  │ - Modulo de inventario (estoque e compartilhado)         │
  │ - Modulo de checkout (fluxo de compra depende)           │
  │ - Notificacao de pedido (confirmacao dispara)            │
  │ - Relatorio de vendas (metrica de conversao afeta)       │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 6: O gate de completude avalia os cinco campos     │
  │                                                         │
  │ Para cada campo:                                        │
  │   - Vazio ou generico → devolver ao owner com pergunta   │
  │   - Suficiente → marcar como presente                    │
  │                                                         │
  │ Verdictos possiveis:                                     │
  │   PASSA → entregar ao agente com os cinco campos         │
  │   CLARIFICA → devolver campos especificos ao owner       │
  │   INCOMPLETO → nao entregar; owner precisa preencher     │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  Intent registrado como artefato duraivel, anexado a tarefa
  do agente, e referenciado por validacoes downstream.
```

### Completude Progressiva

Nem todo intent precisa dos cinco campos com 100% de profundidade antes de comecar. A completude escala com o risco:

| Risco da tarefa | Completude esperada |
|---|---|
| Exploratoria / experimento | Descricao + 1 constraint de seguranca. Demais campos: "a descobrir" |
| Feature interna | Descricao + constraints + cenario de sucesso. Conexoes e falhas podem ser parciais |
| Feature de usuario / produto | Todos os cinco campos preenchidos |
| Mudanca de arquitetura / cross-system | Todos os cinco campos com revisao cruzada dos donos das conexoes |
| Regulacao / compliance | Todos os cinco campos com auditoria documentada |

### Practical First Move (Uma Hora, Nao um Rollout)

O autor do IDSD recomenda: pegue um unico outcome real que voce vai shipar esta semana. Escreva as cinco partes so para ele. Entregue para alguem que nao estava na sua cabeca e pergunte onde o agente ainda teria que adivinhar. Cada lugar apontado e um buraco que voce estava prestes a deixar o agente preencher. Feche esses, nao o sistema inteiro. Custa uma hora, nao um rollout metodologico.

## Implementation Rules

1. **Nao pule constraints.** Constraints sao o campo que mais diretamente previne o agente de produzir outputs plausiveis mas errados. Uma constraint ausente e uma decisao delegada ao agente. Se voce nao sabe todas as constraints, liste as que conhece e marque o resto como "a descobrir" -- mas nao deixe o campo vazio.

2. **Cenarios de falha devem ser testaveis.** "Output ruim" nao e um cenario de falha. "Retorna tenis de $140 quando o teto e $90" e um cenario de falha. Cada cenario de falha deve ser verificavel por um evaluator ou teste automatizado.

3. **Cenarios de sucesso devem ser observaveis.** "O sistema funciona" nao e um cenario de sucesso. "O comprador ve tenis vermelhos no tamanho correto, abaixo de $90, e completa checkout" e um cenario de sucesso. Escreva em linguagem de outcome, nao de implementacao.

4. **Conexoes sao o campo de rastreabilidade.** Cada conexao listada e um lugar onde uma mudanca neste intent pode causar regressao. As conexoes alimentam revisoes de impacto, testes de regressao, e notificacao de stakeholders. Se voce listar zero conexoes para um intent que toca um sistema compartilhado, a lista esta errada.

5. **O gate de completude nao e bloqueio -- e protecao.** "INCOMPLETO" nao significa "nunca faca". Significa "os campos X, Y, Z precisam de resposta antes que o agente comece". O gate produz perguntas concretas, nao rejeicoes genericas.

6. **O intent evolui.** O intent registrado antes da execucao e uma hipotese. Se durante a execucao o agente ou o owner descobrem uma constraint nova, um cenario de falha nao antecipado, ou uma conexao omitida, o intent e atualizado. O artefato vive junto com o codigo.

## Integration with Existing Repo Infrastructure

O primitivo de cinco partes se encaixa entre a captura de necessidade e a execucao agentica, complementando a infraestrutura existente:

| Componente Existente | Como o Five-Part Intent complementa |
|---|---|
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me faz perguntas de alinhamento (escopo, arquitetura, constraints). O Five-Part Intent fornece a estrutura para as respostas: cada resposta do Grill-Me preenche um ou mais campos do intent. A entrevista descobre o que precisa ser decidido; o primitivo organiza as decisoes nos cinco campos. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A avaliacao ancorada em constraints recebe sua lista de constraints diretamente do campo Constraints do intent. O campo Cenarios de Falha alimenta os casos de teste do evaluator. O campo Cenarios de Sucesso define o criterio de aprovacao agregada. |
| [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]] | O handoff do conceito compartilhado transporta o output do alinhamento para artefatos downstream. O Five-Part Intent e o conteudo transportado: os cinco campos sao o payload do handoff. |
| [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] | Issues geradas como fatias verticais herdam os cinco campos do intent como especificacao de comportamento observavel. O campo Conexoes informa quais outras issues seriam afetadas. |
| [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] | O Manual Brake pergunta "quem precisa disso?" e "ainda construiriamos se custasse uma semana?". O Five-Part Intent responde a implicacao: se a resposta for "sim, construa", o intent precisa estar completo nos cinco campos para que o build nao descarrile. |
| [[.opencode/skills/issue-start/SKILL|issue-start skill]] | O execution brief do issue-start tem objective e success criteria. O Five-Part Intent expande o objective para descricao + constraints + conexoes, e os success criteria para cenarios de sucesso + cenarios de falha. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Generator recebe o intent como contrato de trabalho. O Evaluator usa constraints e cenarios de falha como rubrica de validacao. Sem os cinco campos, ambos operam no escuro. |
| [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]] | O value gate decide se o build vale a pena. O Five-Part Intent garante que, se a decisao for BUILD, o agente recebe um contrato completo -- o gate de valor e o gate de completude sao independentes e complementares. |

## Quality Gates

Antes de entregar um intent ao agente para execucao, verifique:

- [ ] O campo **Descricao** existe e descreve o resultado em linguagem do outcome-owner (nao em jargao de implementacao)
- [ ] O campo **Constraints** lista limites verificaveis -- cada constraint pode ser testada por um evaluator ou teste automatizado
- [ ] O campo **Cenarios de Falha** lista outputs inaceitaveis com criterios de deteccao -- "output ruim" nao conta; "retorna X quando deveria retornar Y" conta
- [ ] O campo **Cenarios de Sucesso** lista resultados observaveis -- o outcome-owner consegue apontar para cada cenario e dizer "se isso acontecer, funcionou"
- [ ] O campo **Conexoes** mapeia sistemas, modulos, ou intents afetados -- se a lista esta vazia para um intent que toca sistemas compartilhados, esta errada
- [ ] Nenhum campo esta vazio sem justificativa explicita (ex: "a descobrir durante experimento")
- [ ] Campos marcados como "a descobrir" tem um dono nomeado responsavel por descobri-los e um prazo
- [ ] O gate de completude produziu um veredito (PASSA / CLARIFICA / INCOMPLETO) com perguntas concretas para campos insuficientes
- [ ] O intent registrado e acessivel para o evaluator (Constraint-Anchored Evaluation), para o generator (Generator-Evaluator), e para auditoria futura

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:26 — Intent como primitivo de cinco partes
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:65-76 — Mecanica dos cinco campos com exemplo concreto
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:80-82 — Practical First Move (uma hora, nao um rollout)
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]:44-71 — Pattern 2: Five-Part Intent Completeness Gate
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]:55-81 — Classification as Missing (Medium integration value)
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] — entrevista de alinhamento (fonte das respostas que preenchem o intent)
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — consumidor do campo Constraints e Cenarios de Falha
- [[docs/canonical/generator-evaluator|Generator-Evaluator]] — consumidor do intent completo como contrato de trabalho
- [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]] — mecanismo de transporte do intent para artefatos downstream
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] — gate de valor que decide SE construir (complementar ao gate de completude que decide SE o intent esta pronto)

---

*Created: 2026-06-12 | Source: IDSD Method — Pattern 2 (Missing, Medium value)*
