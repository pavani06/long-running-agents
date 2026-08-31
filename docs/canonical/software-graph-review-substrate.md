---
title: "Software Graph Review Substrate"
type: canonical
tags: ["agentes-orquestracao", "code-review", "context-engineering", "governanca"]
Status: Active
Source: "AI Engineer talk — Itamar Friedman, Qodo (The Last Human Code Review: Building Trust in AI-Generated Code)"
Classification: "Partial Coverage (P1, High integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-31
aliases: ["software graph review", "graph review substrate", "software graph", "cross-PR contract collision", "review unit graph"]
relates-to:
  - "[[docs/canonical/graph-addressed-context-placement|Graph-Addressed Context Placement]]"
  - "[[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]]"
  - "[[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]]"
  - "[[docs/canonical/relational-context-graph|Relational Context Graph]]"
  - "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]"
  - "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]"
  - "[[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]]"
  - "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]"
sources:
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Classification]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis|Knowledge Extraction]]"
---

# Software Graph Review Substrate

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Itamar Friedman, Qodo ([The Last Human Code Review: Building Trust in AI-Generated Code](https://www.youtube.com/watch?v=s-aixZYJG4c))
**Classification:** Partial Coverage (P1, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

O conhecimento tribal profundo — "the P zeros, the bugs that actually made an outage... when a microservice one changed its contract and broke a microservice 2" — vive no entendimento da arquitetura do sistema e não aparece no diff de PR nenhum (`docs/analysis/...-analysis.md:68`). Review em nível de diff é estruturalmente cego a quebras de contrato entre serviços.

O agravante é concorrência: múltiplos PRs in-flight podem tocar o mesmo contrato entre serviços sem que nenhum diff individual revele a colisão — "even if three different PRs are on the fly which contract they might break" (`docs/analysis/...-analysis.md:70`). A falha só fica visível quando os PRs mergeiam e "crash very soon".

## Solução

Fazer do software revisado o próprio grafo: repositórios/serviços como nós, arestas carregando o contrato entre duas peças de software mais links para o histórico de discussões dos fixes anteriores (root cause analysis). PRs in-flight são sobrepostos como "bubbles" no grafo vivo, e a unidade de review muda de diff para abstração de grafo (`docs/analysis/...-analysis.md:69-70`).

| Componente | Função |
|---|---|
| Nós (repos/serviços) | Cada repositório ou microserviço é um nó endereçável do grafo |
| Aresta de contrato | A aresta entre dois nós carrega o contrato vigente entre as duas peças de software |
| Histórico de discussão | Links, por aresta, para as discussões de developers que fixaram incidentes anteriores (RCA) |
| Overlay de PRs in-flight | PRs abertos como "bubbles" sobre o grafo, com os contratos que cada um toca |
| Detecção de colisão cross-PR | Sinalizar quando dois PRs em voo alteram o mesmo contrato ("whether two PRs are going to crash very soon") |

Fluxo (`docs/analysis/...-patterns.md:48-55`): construir o grafo de repos e conexões → extrair o contrato de cada aresta e anexar o histórico de discussões dos fixes anteriores → sobrepor os PRs in-flight como bubbles → detectar colisões de contrato entre PRs concorrentes → revisar na abstração de grafo, não no diff individual.

O mesmo grafo serve três consumidores: review com conhecimento de arquitetura embutido, previsão de colisão cross-PR e a camada de decisão approve/block ([[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]]).

## Implementação neste repositório

### O que já existe

O repo tem vocabulário de grafo em profundidade canônica — mas para unidades de contexto, não para artefatos de software sob review (classification:50-61):

- **Reframe grafo-como-propriedade:** [[docs/canonical/relational-context-graph|Relational Context Graph]] — "The structural error: treating relevance as proximity in embedding space rather than as a graph property" (`docs/canonical/relational-context-graph.md:22`); nós são unidades de contexto ("tool results, decisions, state snapshots", `:28`) com quatro tipos formais de aresta (`:30-37`) e travessia que converte retrieval em selection (`:39`).
- **Grafo implementado:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — grafo de memória com status epistêmico citado como infraestrutura real do repo (`docs/canonical/relational-context-graph.md:62-63`); o runtime `obsidian-eval` expõe scan, query, graph e epistemic graph (`docs/system-of-record.md:127`).
- **Mecânica estrutural mais próxima:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] — linha da rubrica prescrevendo structural test que asserta arestas de dependência entre pacotes: "Structural test: assert package dependency edges" (`docs/canonical/garbage-collection-day-meta-loop.md:64`).
- **Filosofia vizinha:** [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]] — "A deep module with a simple public interface and behavior-level boundary tests is not only better human design; it is more navigable terrain for the next agent" (`docs/canonical/architecture-as-agent-affordance.md:30`).

### O que falta

(classification:59) — greps `microservice|cross-PR|in-flight|collision|software graph|service graph|repo graph` em `docs/canonical/` retornam apenas colisões de nome de arquivo de handoff (`docs/canonical/budget-aware-session-handoff.md:103`, `:117` — conceito diferente):

1. **O software revisado como grafo** — nenhum doc faz dos repos/serviços os nós e dos contratos entre serviços as arestas; os grafos do repo endereçam memória e contexto, nunca o artefato revisado.
2. **Contrato nas arestas + histórico de discussão** — extração de contrato por aresta e anexação do histórico de RCA dos fixes anteriores não existem em nenhuma superfície.
3. **Overlay de PRs in-flight e detecção de colisão cross-PR** — nenhum mecanismo projeta PRs abertos sobre estrutura de software nem detecta colisão de contrato entre PRs concorrentes.
4. **Mudança da unidade de review de diff para grafo** — ausente em `docs/canonical/`, `curriculum/`, `.opencode/skills/`.

Nota de honestidade: o próprio [[docs/canonical/relational-context-graph|Relational Context Graph]] declara seus componentes (Edge Classifier, Supersession Updater, Node Ingestor, Traversal Engine) não implementados (`docs/canonical/relational-context-graph.md:67-74`) — o substrato de grafo do repo é spec-level. Apontá-lo para artefatos de software seria uma segunda camada sobre uma primeira ainda não construída.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Superficia conhecimento de arquitetura (P-zero, quebras de contrato) dentro do review em vez de deixar em cabeças | Custo de build alto — "if you try to build yourself it's really hard to build" (claim de vendor com viés declarado, `docs/analysis/...-analysis.md:109`) |
| Detecta colisões entre PRs concorrentes no mesmo contrato antes do merge | Exige extração de contrato e ligação de histórico de discussão por aresta |
| O mesmo grafo alimenta review, previsão de colisão e auto approve/block | Muda o workflow de review de leitura de diff para leitura de grafo |
| Reaproveita o vocabulário de arestas tipadas que o repo já possui | Camada nova sobre um substrato de contexto cujos componentes estão declarados não implementados |

## Relação com outros padrões

- **Reaproveita o vocabulário de:** [[docs/canonical/relational-context-graph|Relational Context Graph]] — os quatro tipos de aresta e a travessia-como-seleção apontados a um objeto novo (artefatos de software em vez de unidades de contexto).
- **Ancora na infraestrutura de:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — o grafo já implementado no `obsidian-eval` é o substrato mais próximo existente no repo.
- **É pré-requisito de:** [[docs/canonical/graph-addressed-context-placement|Graph-Addressed Context Placement]] — placement de conhecimento codificado exige a estrutura de endereçamento que este padrão define.
- **Alimenta:** [[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]] — "now you're ready to start approving and blocking PRs automatically" quando o grafo está maduro (`docs/analysis/...-analysis.md:75`).
- **Carrega o conhecimento de:** [[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]] — contratos e históricos de discussão são conhecimento codificado que precisa da camada de contexto governada.
- **Mecânica mais próxima no repo:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] (`:64`) — assert de arestas de dependência como structural test.
- **Filosofia:** [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]] — estrutura como terreno para o próximo agente; aqui, estrutura como substrato de review.
- **É o supraconjunto de:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] — o pipeline de shadow é o subcaso single-PR desta arquitetura (`docs/analysis/...-analysis.md:130`).

## Referências

- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:44-63` — padrão extraído: problema, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:46-61` — classificação Partial Coverage (High) com evidência e NOT_FOUND dos greps de mecânica.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:66-70` — mecânica do grafo de software e mudança da unidade de review.
- `docs/canonical/relational-context-graph.md:22-39, :62-74` — vocabulário de arestas tipadas, âncora epistêmica e gap declarado dos componentes.
- `docs/canonical/garbage-collection-day-meta-loop.md:64` — structural test de arestas de dependência.
- `docs/canonical/architecture-as-agent-affordance.md:30` — estrutura como affordance para o próximo agente.
