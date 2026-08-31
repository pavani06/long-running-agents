---
title: "Graph-Addressed Context Placement"
type: canonical
tags: ["context-engineering", "knowledge-management", "code-review", "governanca"]
Status: Active
Source: "AI Engineer talk — Itamar Friedman, Qodo (The Last Human Code Review: Building Trust in AI-Generated Code)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-31
aliases: ["graph addressed context placement", "context placement", "placement discipline", "context at the node", "addressable context placement"]
relates-to:
  - "[[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]]"
  - "[[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]]"
  - "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]"
  - "[[docs/canonical/smallest-sufficient-context|Smallest Sufficient Context]]"
  - "[[docs/canonical/relational-context-graph|Relational Context Graph]]"
  - "[[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]]"
sources:
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Classification]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis|Knowledge Extraction]]"
---

# Graph-Addressed Context Placement

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Itamar Friedman, Qodo ([The Last Human Code Review: Building Trust in AI-Generated Code](https://www.youtube.com/watch?v=s-aixZYJG4c))
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Contexto codificado despejado em arquivos não é recuperável por agentes, porque nada diz ao agente **onde** aquele contexto se aplica: "It needs to be not just thrown into files. It Needs to sit and located in a place that agent understand where is that context fitting" (`docs/analysis/...-analysis.md:96`).

O conhecimento existe no sistema — a falha é de endereçamento, não de persistência. É o mesmo modo de falha que o repo documenta como decoupling entre metadata recuperável e conteúdo valioso: "the metadata that makes knowledge *retrievable*... is decoupled from the content that makes knowledge *valuable*" (`docs/canonical/cross-context-knowledge-siloing.md:53`).

## Solução

Disciplina de placement keyed à estrutura de software: todo ato de codificação posiciona o conhecimento (regra, standard, histórico de discussão/outage) **no nó ou aresta do grafo de software onde ele se aplica**. A recuperação passa a ser por travessia no ponto da mudança, não por scan de dumps (`docs/analysis/...-patterns.md:65-78`).

| Componente | Função |
|---|---|
| Estrutura de endereçamento | Os nós/arestas do grafo de software ([[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]]) como espaço de endereços |
| Placement disciplinado | Cada codificação obedece à regra: o endereço é determinado pelo elemento de software que o conhecimento governa |
| Recuperação por travessia | No ponto da mudança, o agente atravessa o grafo e recupera o contexto que se aplica àquele nó/aresta |
| Conhecimento acionável | O histórico acumulado vira asset consumível pela próxima revisão, não arquivo órfão |

Fluxo (`docs/analysis/...-patterns.md:70-74`): codificar conhecimento → determinar o elemento de software que ele governa → posicioná-lo nesse endereço do grafo → na mudança seguinte, recuperar por travessia o contexto que fitting a mudança atual.

## Implementação neste repositório

### O que já existe

A metade retrieval é canônica e bem-ancorada (classification:69-79):

- **Endereçamento estável:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — "Represent omitted context as an addressable catalog. Each omitted message, tool call, span... receives a stable identifier plus enough metadata for the agent to choose what to fetch" (`docs/canonical/addressable-memory-catalog.md:28`); campos de catálogo `location`, `preview`, `scope`, `tool`, `path` com allowlist (`:36-41`).
- **Minimalismo por travessia:** [[docs/canonical/smallest-sufficient-context|Smallest Sufficient Context]] — "determine the minimal token set the agent needs... retrieve only those tokens through relational graph traversal" (`docs/canonical/smallest-sufficient-context.md:28`).
- **Primitivo de travessia:** [[docs/canonical/relational-context-graph|Relational Context Graph]] — "traversing the graph by typed relationships converts retrieval (returning what is near) into selection (returning what is relevant)" (`docs/canonical/relational-context-graph.md:39`).
- **Modo de falha nomeado:** [[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]] (`:53`) — o exato failure mode "dumped into files is not agent-retrievable", em termos do repo.

### O que falta

(classification:79) — os greps de termos de software-graph (`microservice|cross-PR|software graph|...`) retornam zero matches relevantes; as superfícies de endereçamento existentes (paths de catálogo, triggers de skill, tags de frontmatter) localizam memória e instruções, nunca regras keyed a nós/arestas de código:

1. **Placement keyed à estrutura de software** — a disciplina de que o endereço de uma regra é determinado pelo elemento de software que ela governa não existe como princípio.
2. **Implementação do catálogo** — o próprio [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] declara: "The classification found no explicit pattern for an omitted-memory catalog with `id + location + preview` in the canonical docs, curriculum, evidence, decisions, or operational skills" (`docs/canonical/addressable-memory-catalog.md:61`).
3. **Travessia de fato** — [[docs/canonical/smallest-sufficient-context|Smallest Sufficient Context]] declara: "Retrieval is by handle or topic, not by dependency/provenance traversal" (`docs/canonical/smallest-sufficient-context.md:63`).

Nota de honestidade: este gap é mais fino do que a classificação sugere à primeira leitura. O schema de endereçamento do catálogo **está** especificado em nível de campos (`addressable-memory-catalog.md:36-41`) e o princípio de retrieval-por-travessia é canônico (`relational-context-graph.md:39`); o que genuinamente falta é (a) a implementação dessas specs e (b) o keying a endereços de estrutura de software — que por sua vez pressupõe o substrato do [[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]], ele próprio spec-level.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Elimina o failure mode "context dumped into files is not agent-retrievable" | Pressupõe uma estrutura de endereçamento (o grafo) antes do placement ser possível |
| Precisão de retrieval no ponto da mudança em vez de whole-dump loading | Todo ato de codificação precisa obedecer à disciplina de placement |
| Conhecimento acumulado vira asset acionável para a próxima revisão | Contexto misplaced fica silenciosamente órfão — nenhum caminho de retrieval o encontra |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]] — o padrão-fonte pressupõe a estrutura de endereçamento do padrão 2 como input (`docs/analysis/...-patterns.md:71`).
- **Aplica a:** [[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]] — o conhecimento codificado na camada dupla-interface é o objeto que recebe placement.
- **Estende:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] (endereçamento estável) e [[docs/canonical/smallest-sufficient-context|Smallest Sufficient Context]] (recuperação mínima por travessia) — o delta é a disciplina de placement para conhecimento codificado, não para memória omitida.
- **Mitiga:** [[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]] — placement com endereçamento é a contramedida ao decoupling metadata/conteúdo.
- **Ponte:** conecta o cluster de contexto do repo à superfície de review, via [[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]] — regras colocadas onde se aplicam são as que o gating consome (classification:81).

## Referências

- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:65-82` — padrão extraído: problema, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:65-81` — classificação Partial Coverage (Medium) com evidência e NOT_FOUND.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:96` — requisito de placement ("not just thrown into files").
- `docs/canonical/addressable-memory-catalog.md:28, :36-41, :61` — contrato de endereçamento e implementação declarada ausente.
- `docs/canonical/smallest-sufficient-context.md:28, :63` — recuperação mínima por travessia; retrieval por handle/topic declarado.
- `docs/canonical/relational-context-graph.md:39` — travessia converte retrieval em selection.
- `docs/canonical/cross-context-knowledge-siloing.md:53` — decoupling metadata/conteúdo.
