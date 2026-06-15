---
name: karpathy-guidelines
description: "Diretrizes comportamentais derivadas das observacoes de Andrej Karpathy sobre onde LLMs falham ao codificar. Quatro principios: pense antes de codificar, simplicidade radical, edicao cirurgica, metas verificaveis. Carregar em toda task de implementacao nao-trivial para reduzir overengineering, edicoes ortogonais, suposicoes silenciosas e loops sem criterio de parada. Dispara com: 'karpathy', 'guidelines', 'behavioral guidelines', 'coding discipline', 'pense antes', 'simplicidade', 'edicao cirurgica', 'metas verificaveis', 'goal-driven', 'surgical changes', 'think before coding'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: implementation
  priority: high
  source: "Andrej Karpathy's LLM coding observations (X, Jan 2026); forrestchang/andrej-karpathy-skills"
---

## What I Do

Eu injeto disciplina comportamental em agentes de codigo, atacando os quatro modos de falha que Andrej Karpathy documentou e que sao particularmente destrutivos em execucoes long-running:

| Modo de falha | Por que importa em long-running agents | Principio que corrige |
|---|---|---|
| Suposicoes silenciosas | Cada premissa errada polui a janela de contexto e vira divida acumulada | **Think Before Coding** |
| Overengineering | Abstracoes prematuras consomem tokens e complexidade que o harness nao precisava | **Simplicity First** |
| Edicoes ortogonais | Mudancas nao relacionadas quebram wikilinks, invalidam docs, criam regressoes | **Surgical Changes** |
| Sem criterio de parada | O agente loopa indefinidamente porque "faz funcionar" nao e verificavel | **Goal-Driven Execution** |

## When to Use Me

Carregue esta skill em toda task de implementacao nao-trivial. Especialmente quando:

- A tarefa envolve multiplos arquivos ou modulos (risco de edicoes ortogonais)
- O pedido e vago ou aberto (risco de suposicoes silenciosas)
- O agente tende a supercomplicar solucoes simples (risco de overengineering)
- Voce quer que o agente verifique o proprio trabalho antes de declarar pronto
- Esta trabalhando em docs/canonical/ ou curriculum/ (onde edicoes cirurgicas sao criticas para nao quebrar wikilinks e frontmatter)

Nao carregue quando:

- A tarefa e puramente mecanica (typo, lint fix, atualizacao de dependencia)
- O custo cognitivo dos principios excede o custo da tarefa (one-liners, search/replace triviais)

---

## 1. Think Before Coding — Pense Antes de Codificar

**Nao assuma. Nao esconda confusao. Apresente tradeoffs.**

No contexto de long-running agents, este principio e critico porque cada premissa errada consome tokens da janela de contexto e vira divida acumulada em sprints futuros do harness.

Antes de implementar:

- Liste as premissas que voce esta fazendo. Se houver incerteza, **pergunte** em vez de escolher silenciosamente.
- Se existem multiplas interpretacoes do pedido, apresente as alternativas — nao decida sozinho.
- Se existe um caminho mais simples que o solicitado, diga. Questione quando necessario.
- Se algo esta confuso, pare e nomeie o que nao esta claro. Peca esclarecimento.

**Exemplo no dominio do projeto:**

```
Pedido: "Adiciona um mecanismo de retry no harness"

Antes de implementar, preciso esclarecer:

1. Escopo: retry por tool call individual ou retry do sprint contract inteiro?
2. Backoff: exponencial com jitter ou fixo? Qual teto de tentativas?
3. State: o harness persiste estado entre retries? Se sim, como limpar contexto
   de tentativas falhas (Error Context Hygiene)?
4. Boundary: retry automatico ou com aprovacao humana (Manual Brake)?

Abordagem mais simples: retry por tool call com backoff exponencial,
max 3 tentativas, sumarizando erros conforme error-context-hygiene.
```

O custo de uma pergunta e uma mensagem; o custo de uma premissa errada e codigo descartado + contexto poluido + divida no harness.

---

## 2. Simplicity First — Simplicidade Radical

**O minimo que resolve. Nada especulativo.**

Em long-running agents, complexidade desnecessaria tem custo composto: consome tokens da janela de contexto, dificulta debugging de sprints longos, e torna o harness mais fragil a mudancas.

- Nada alem do que foi pedido. Zero features especulativas.
- Nenhuma abstracao (classes, interfaces, padroes) para codigo usado uma unica vez.
- Nenhuma "flexibilidade" ou "configurabilidade" que nao foi solicitada.
- Se voce escreveu 200 linhas e o problema se resolve em 50, reescreva.
- A pergunta-ancora: **"Um engenheiro senior diria que isso esta supercomplicado?"** Se sim, simplifique.

**Exemplo no dominio do projeto:**

```typescript
// OVERENGINEERED: Factory + Strategy + Config para um unico retry
class RetryStrategyFactory {
  static create(type: RetryType, config: RetryConfig): RetryStrategy { ... }
}
interface RetryStrategy { execute(fn: () => Promise<T>): Promise<T>; }
class ExponentialBackoffStrategy implements RetryStrategy { ... }
class FixedDelayStrategy implements RetryStrategy { ... }
class RetryConfig { maxAttempts: number; baseDelay: number; ... }

// SIMPLE: Uma funcao. O dia que precisar de 3 estrategias, refatora.
async function withRetry<T>(fn: () => Promise<T>, maxAttempts = 3): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try { return await fn(); }
    catch (e) {
      if (attempt === maxAttempts) throw e;
      await sleep(Math.pow(2, attempt) * 100);
    }
  }
}
```

---

## 3. Surgical Changes — Edicao Cirurgica

**Mexa so no que precisa. Limpe so a sua propria bagunca.**

No long-running-agents, edicoes ortogonais sao particularmente perigosas porque o repositorio tem alta densidade de cross-references (wikilinks, `relates-to`, system-of-record). Uma "melhoria" inofensiva pode quebrar dezenas de referencias.

Ao editar codigo ou documentacao existente:

- Nao "melhore" codigo adjacente, comentarios, nomes de variavel ou formatacao que nao fazem parte da tarefa.
- Nao refatore coisas que nao estao quebradas.
- Respeite o estilo existente do arquivo (aspas, indentacao, padrao de nomes, formato de frontmatter), mesmo que voce faria diferente.
- Se notar codigo morto, wikilinks quebrados ou problemas nao relacionados, **mencione** no comentario final — nao delete nem corrija.
- Remova apenas imports/variaveis/funcoes/wikilinks que **suas mudancas** tornaram orfas.

**O teste:** Cada linha alterada deve ser rastreavel diretamente ao pedido do usuario.

**Exemplo no dominio do projeto:**

```
Pedido: "Corrige o wikilink quebrado em error-context-hygiene.md"

CORRETO (cirurgico):
- Altera APENAS o [[wikilink]] quebrado → aponta para o path correto
- NAO atualiza tags do frontmatter
- NAO adiciona relates-to que faltava
- NAO corrige typos em paragrafos adjacentes
- Se notar que o system-of-record.md tambem tem link quebrado, menciona no comentario final

INCORRETO (ortogonal):
- Conserta o wikilink E atualiza tags E adiciona relates-to E corrige typos E
  reorganiza a ordem dos topicos no system-of-record
```

---

## 4. Goal-Driven Execution — Metas Verificaveis

**Defina o criterio de sucesso antes de comecar. Loope ate verificar.**

Este e o principio mais importante para long-running agents: sem criterios verificaveis, o agente loopa indefinidamente porque "faz funcionar" nao e uma condicao de parada. O harness precisa de gates explicitos.

Transforme tarefas vagas em metas com criterio de verificacao:

| Em vez de... | Transforme em... |
|---|---|
| "Adiciona validacao no harness" | "Escreva teste para input invalido → implemente a validacao → verifique que o teste passa" |
| "Corrige o bug de contexto" | "Escreva teste que reproduz o estouro de contexto → confirme que falha → corrija → confirme que passa" |
| "Refatora o orquestrador" | "Garanta que `npm run test:unit` e `npm run lint` passam antes e depois da refatoracao" |
| "Melhora a documentacao" | "Rode `npx tsx scripts/validate-obsidian.ts` → corrija todos os erros → confirme zero erros" |

Para tarefas multi-etapa, declare o plano com verificacao por etapa:

```
1. Escrever teste que reproduz o bug → verify: test fail
2. Implementar correcao minima → verify: test pass + npm run lint pass
3. Verificar ausencia de regressao → verify: npm run test:unit pass
4. Verificar convencoes de doc → verify: npx tsx scripts/validate-obsidian.ts pass
```

**Criterios fortes permitem loop autonomo ate passar. Criterios fracos ("faz funcionar") exigem esclarecimento constante e sao a causa raiz de sprints que nao convergem.**

---

## Anti-Patterns no Contexto de Long-Running Agents

| Principio | Anti-Pattern | Custo em long-running |
|---|---|---|
| Think Before Coding | Assume que o harness persiste estado de um jeito especifico sem verificar | Contexto poluido, sprint descartado |
| Simplicity First | Cria abstraction layer para um unico tipo de retry | Tokens gastos, harness mais dificil de debugar |
| Surgical Changes | "Melhora" wikilinks adjacentes enquanto corrige um bug | system-of-record dessincronizado, CI quebrado |
| Goal-Driven | "Vou melhorar o harness" sem criterio de parada | Loop infinito, janela de contexto estoura |

---

## Verificacao de Que Esta Funcionando

Estes guidelines estao ativos se voce observar:

- **Menos mudancas desnecessarias nos diffs** — apenas o pedido aparece, sem "melhorias" colaterais
- **Menos reescritas por overengineering** — codigo simples na primeira tentativa
- **Perguntas de esclarecimento antes da implementacao** — nao depois de cometer erros
- **PRs limpos e minimos** — sem refactors nao solicitados, sem style drift
- **Sprints do harness que convergem** — porque cada etapa tem um gate de verificacao explicito
