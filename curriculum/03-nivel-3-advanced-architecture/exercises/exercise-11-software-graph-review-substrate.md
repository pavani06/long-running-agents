---
title: "Exercício 11: Software Graph Review Substrate — Revisar o Grafo de Contratos, Não o Diff"
type: exercise
level: 3
aliases: ["software graph review substrate", "software graph review", "grafo de software como substrato de review", "contratos como arestas", "cross-PR collision detection", "colisão cross-PR", "PR bubble", "review unit shift diff para grafo"]
tags: ["curriculo-conteudo", "agentes-orquestracao", "code-review", "context-engineering", "knowledge-management", "production", "spec-driven-development", "stack-tooling"]
relates-to: ["[[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]]", "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]", "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Source Classification]]", "[[docs/canonical/relational-context-graph|Relational Context Graph]]", "[[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]]", "[[curriculum/03-nivel-3-operational/exercises/exercise-shadow-review-pipeline|Exercício 7: Shadow Review Pipeline]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-semantic-rule-gated-auto-approve-block|Exercício 12: Semantic-Rule-Gated Auto Approve/Block]]"]
duration: "90-120 min"
---

# 🕸️ Exercício 11: Software Graph Review Substrate — Revisar o Grafo de Contratos, Não o Diff
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter lido `docs/canonical/relational-context-graph.md` + Exercício 7 (`exercise-shadow-review-pipeline.md`, Nível 3 — Operacional)
**Objetivo:** Construir o substrato de review que trata o software revisado como um grafo tipado — serviços como nós, contratos entre serviços como arestas carregando o histórico de discussões de fixes de root-cause (Parte 1), PRs in-flight sobrepostos ao grafo como bolhas com detecção de colisão de contrato cross-PR antes do merge (Parte 2), e a unidade de review deslocada do diff do PR para o grafo: consumidores afetados, histórico de incidentes surfacado na aresta e pontos cegos que o diff não enxerga (Parte 3)

---

## 📖 Prólogo: O P0 Que Dois Diffs Limpos Fizeram Juntos

**MeridianPay, fintech de pagamentos. Sexta-feira, 17h58. Dois PRs mergeados com CI verde, dois diffs revisados por seniors. Segunda-feira, 02h47, pager geral.**

```
╔══════════════════════════════════════════════════════════════════╗
║           POSTMORTE INC-2026-207 — P0 DE PAGAMENTOS              ║
║           41 minutos · 100% dos pagamentos rejeitados            ║
║                                                                  ║
║  PR-101 (checkout)        PR-102 (fraud-scorer)                  ║
║  renomeia amount_minor    aperta validação de amount_minor        ║
║  → amount_cents           int → decimal                           ║
║  diff: 2 arquivos         diff: 1 arquivo                         ║
║  CI: verde ✓              CI: verde ✓                             ║
║  review senior: "LGTM"    review senior: "LGTM"                   ║
║                                                                  ║
║  Nenhum diff contém o outro lado do contrato.                    ║
║  Cada time stubou o contrato do seu jeito nos testes.            ║
║  Juntos, os dois PRs mutaram O MESMO CAMPO da MESMA aresta       ║
║  — e nenhuma revisão de diff do mundo ia ver isso.               ║
╚══════════════════════════════════════════════════════════════════╝
```

A reunião de postmortem, terça-feira:

```
DIRETORA DE ENG:  "Como isso passou por DOIS reviews seniors?"

SRE:              "Passou porque cada diff estava 'correto' de fato.
                   O problema mora ENTRE os PRs: os dois tocam o
                   campo amount_minor do contrato checkout→fraud-
                   scorer. O review olha o diff; o contrato não
                   vive em nenhum diff — vive na aresta."

PLATAFORMA:       "E tem um agravante. Isso já tinha acontecido.
                   INC-2025-118, novembro passado: checkout renomeou
                   campo do contrato sem atualizar o consumidor,
                   fraud-scorer rejeitou tudo por meia hora."

DIRETORA:         "Por que ninguém lembrou disso no review?"

PLATAFORMA:       "Porque esse conhecimento vive num thread de Slack
                   de um RCA de novembro. O tribal knowledge de
                   arquitetura — quais são os P-zeros, qual par de
                   serviços já quebrou, qual contrato é frágil —
                   não existe em lugar nenhum que o review consulte.

                   A proposta: parar de revisar diffs e começar a
                   revisar o GRAFO.

                   ┌──────────────────────────────────────────┐
                   │  NÓ     = repo/serviço                   │
                   │  ARESTA = contrato entre dois serviços   │
                   │           + histórico de discussões dos  │
                   │           fixes de RCA daquela aresta    │
                   │  PR     = bolha sobreposta ao grafo      │
                   └──────────────────────────────────────────┘

                   Areview de um PR passa a responder três perguntas
                   que o diff não responde: QUEM consome o que eu
                   mudei? O que já quebrou nessa aresta antes? E:
                   mais algum PR in-flight está mutando o mesmo
                   contrato — esses dois PRs vão colidir?"

DIRETORA:         "Colisão cross-PR... antes do merge."

PLATAFORMA:       "Antes do merge. O review vira leitura de grafo."
```

**O pipeline que você vai implementar teria pego os dois PRs na sexta-feira:** o grafo sabe que `amount_minor` vive na aresta `checkout→fraud-scorer`, a aresta carrega o INC-2025-118 como histórico, e o overlay de PRs in-flight detecta que PR-101 e PR-102 mutam o mesmo campo da mesma aresta — colisão sinalizada antes de qualquer merge.

Este padrão não existe implementado em nenhum lugar do repositório: a classificação o marcou como `Partial Coverage` com valor de integração `High` (`docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:46-61`) — os grafos canônicos do repo endereçam memória e contexto, nunca o artefato revisado. Você está construindo a primeira implementação.

---

## 🧠 O Contexto

### O Modelo Mental: o Objeto do Review Muda de Diff para Grafo

O padrão vem da talk "The Last Human Code Review" (Itamar Friedman, Qodo): o conhecimento tribal profundo "sits in understanding the system architecture. What are the P zeros, the bugs that actually made an outage... when a microservice one changed its contract and broke a microservice 2. That... does not exist in most code review" (`docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:66-70`).

O mecanismo em três camadas:

| Camada | O que adiciona | O que resolve |
|---|---|---|
| **Nós e arestas** | Serviços como nós; arestas carregam o contrato entre dois componentes **e links para o histórico de discussões de fixes anteriores** | Conhecimento de arquitetura (P-zeros, pares frágeis) surfaca no ponto da mudança, não em Slack |
| **PRs como bolhas** | PRs in-flight sobrepostos ao grafo | "Even if three different PRs are on the fly which contract they might break" — visão combinada |
| **Detecção de colisão** | Dois PRs mutando o mesmo ponto do mesmo contrato | "Whether two PRs are going to crash very soon" — colisão prevista antes do merge |

A mudança estrutural é a unidade: "software development, at least code governance, is going to change from reviewing your pull request to actually reviewing your entire software development from a graph abstraction" (`...analysis.md:70`).

### Fronteiras do padrão (o que NÃO é este grafo)

1. **Nós de software ≠ nós de contexto.** O [[docs/canonical/relational-context-graph|Relational Context Graph]] define nós como unidades de contexto (resultados de tool, decisões, snapshots) com quatro classes de aresta tipada — o objeto é a *memória do agente*. Aqui os nós são *repos/serviços* e as arestas são *contratos entre software*: a mesma gramática de grafo apontada para um objeto novo. A classificação é explícita: o repo tem vocabulário de grafo em profundidade canônica, "but for context units, not for software artifacts under review" (`...classification.md:50`).

2. **Histórico na aresta ≠ histórico em documento.** Um postmortem num wiki é acessível por busca; histórico ancorado NA aresta é acessível por travessia — ele aparece quando você toca a aresta, sem ninguém lembrar que ele existe. É a diferença entre conhecimento arquivado e conhecimento surfacado.

3. **Colisão cross-PR ≠ conflito de merge.** Conflito de git acontece quando dois PRs tocam as MESMAS LINHAS do MESMO repo. Colisão de contrato acontece quando dois PRs em repos DIFERENTES mutam o mesmo campo da mesma aresta — o git nunca vê, porque a aresta não vive em repo nenhum.

4. **Substrato ≠ gate.** Este exercício produz o substrato (grafo + overlay + colisão + unidade de review). O approve/block automático por regras semânticas é outro padrão — e o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-semantic-rule-gated-auto-approve-block|Exercício 12]] consome exatamente este grafo como pré-requisito. O shadow review do Exercício 7 é o subcaso single-PR: sem grafo, o teto do pipeline é concordância por check dentro de um diff.

5. **Grafo de software ≠ teste estrutural de dependência.** O GC Day prescreve teste estrutural que asserta arestas de dependência entre pacotes (`docs/canonical/garbage-collection-day-meta-loop.md:64`) — determinístico, intra-repo, sem histórico nem PRs in-flight. Aqui o grafo é cross-repo, carrega metadados conversacionais e é consultado por review, não só por CI.

### O Que Você Vai Construir

1. **`SoftwareGraph`** (Parte 1 — Substrato): serviços como nós, `ContractEdge` com campos do contrato + `RCAHistoryEntry` ancorado na aresta; travessias `edges_touching` / `consumers_of` / `history_for`
2. **`detect_collisions`** (Parte 2 — Diagnóstico): agrupamento das mudanças dos PRs in-flight por `(edge_id, field_name)`; colisão quando dois PRs diferentes mutam o mesmo campo; conflito de renome quando dois renomes divergem
3. **`review_unit_for`** (Parte 3 — Pipeline): o relatório de review de um PR como objeto de grafo — arestas afetadas, contrapartes afetadas, histórico de RCA surfacado, colisões com os outros PRs abertos, mudanças quebradoras e os pontos cegos do diff

O domínio é o MeridianPay do prólogo: 5 serviços, 4 contratos, 3 PRs in-flight — incluindo o par PR-101/PR-102 que causou o P0.

---

## 📋 Cenário

### O Grafo do MeridianPay

| Serviço (nó) | Tier | Papel |
|---|---|---|
| `checkout` | P0 | Orquestra o pagamento; provider do `PaymentRequest` |
| `ledger` | P0 | Contabiliza; consumer do `PaymentRequest`, provider do `PaymentSettled` |
| `fraud-scorer` | P1 | Pontua fraude; consumer do `PaymentRequest` |
| `notifications` | P2 | Notifica settlement; consumer do `PaymentSettled` |
| `authz` | P1 | Autoriza; provider do `AuthzDecision` para `checkout` |

| Aresta | Provider → Consumer | Contrato | Campos | Histórico de RCA na aresta |
|---|---|---|---|---|
| `E-CHK-FRAUD` | checkout → fraud-scorer | PaymentRequest v2 | `amount_minor` (int, req), `currency` (str, req), `payment_method` (str, opt) | **INC-2025-118** — rename sem consumer update, 41min de rejeição |
| `E-CHK-LED` | checkout → ledger | PaymentRequest v2 | `amount_minor` (int, req), `currency` (str, req) | — |
| `E-LED-NOTIF` | ledger → notifications | PaymentSettled v1 | `settlement_id` (str, req), `amount_minor` (int, req) | INC-2026-014 — evento sem campo, drop silencioso |
| `E-AUTH-CHK` | authz → checkout | AuthzDecision v1 | `decision` (str, req) | — |

### Os PRs In-Flight (bolhas sobre o grafo)

| PR | Serviço | Muda | Aresta(s) | Natureza |
|---|---|---|---|---|
| PR-101 | checkout | `amount_minor` → renome para `amount_cents` | E-CHK-FRAUD, E-CHK-LED | **quebra consumidores** |
| PR-102 | fraud-scorer | `amount_minor` tipo `int` → `decimal` | E-CHK-FRAUD | **quebra parse**, **colide com PR-101** |
| PR-103 | ledger | adiciona `correlation_id` opcional | E-LED-NOTIF | compatível |

O diff do PR-101 contém apenas `services/checkout/api.py` e `services/checkout/contracts.py` — nenhum arquivo de `fraud-scorer` ou `ledger`. É isso que o review por diff não vê e o review por grafo traz para a mesa.

---

## ✅ Requisitos

### Funcionais

- [ ] `ContractEdge` carrega campos do contrato (`ContractField`: name/type/required) **e** `rca_history` com `RCAHistoryEntry` (incident_id, root_cause, discussion_url, broken_pair)
- [ ] `ContractChange.is_breaking` é `True` para `ADD_REQUIRED_FIELD`, `RENAME_FIELD`, `REMOVE_FIELD`, `TYPE_CHANGE`; `False` para `ADD_OPTIONAL_FIELD`
- [ ] `SoftwareGraph.edges_touching(service_id)` retorna arestas onde o serviço é provider **ou** consumer; `consumers_of(edge_id)` e `history_for(edge_id)` consultam a aresta
- [ ] `detect_collisions(open_prs)` agrupa mudanças por `(edge_id, field_name)` e emite: `CROSS_PR_FIELD_COLLISION` quando dois PRs distintos mutam o mesmo campo da mesma aresta; `CROSS_PR_RENAME_CONFLICT` quando dois renomes do mesmo campo divergem no `new_name`
- [ ] `review_unit_for(pr, graph, other_open_prs)` produz `PRReviewReport` com: `affected_edges`, `affected_counterparts` (serviços do outro lado das arestas tocadas, excluindo o autor), `surfaced_history` (RCA das arestas tocadas), `collisions` (achados que envolvem o PR), `breaking_fields`, `blind_spots` (contrapartes afetadas que não aparecem em `pr.files`), `has_blocking`
- [ ] `has_blocking` é `True` quando há colisão envolvendo o PR **ou** mudança quebradora em aresta com contraparte; `False` para mudança compatível sem colisão (PR-103)
- [ ] `blind_spots` plaqueia a tese da mudança de unidade: contrapartes que o diff do PR não contém

### Técnicos

- [ ] Python 3.9+ com type hints (`from __future__ import annotations`)
- [ ] Apenas biblioteca padrão; `dataclasses` para todos os modelos, `Enum` para `ChangeKind` e `CollisionCode`
- [ ] `detect_collisions` e `review_unit_for` são determinísticos, sem estado e sem I/O
- [ ] `BREAKING_KINDS` como constante nomeada; nenhum "magic string" para kind de mudança
- [ ] Dados de teste 100% determinísticos (grafo e PRs declarados literalmente nos builders)

### Validação

- [ ] Cenário 1: `edges_touching("checkout")` = 3 arestas (2 como provider, 1 como consumer); `history_for("E-CHK-FRAUD")` traz INC-2025-118
- [ ] Cenário 2: `ADD_OPTIONAL_FIELD` não é quebradora; `RENAME_FIELD` é
- [ ] Cenário 3: PR-101 + PR-102 → `CROSS_PR_FIELD_COLLISION` em `E-CHK-FRAUD`/`amount_minor` com `pr_ids` = os dois; PR-103 não colide com ninguém
- [ ] Cenário 4: dois renomes divergentes do mesmo campo → `CROSS_PR_RENAME_CONFLICT`
- [ ] Cenário 5: review do PR-101 → contrapartes `["fraud-scorer", "ledger"]`, histórico INC-2025-118 surfacado, `has_blocking True`; review do PR-103 → `has_blocking False`
- [ ] Cenário 6: `blind_spots` do PR-101 = `["fraud-scorer", "ledger"]` — os serviços que o diff não contém

---

## 🏗️ Arquitetura do Sistema

```
┌──────────────────────────────────────────────────────────────────┐
│            SOFTWARE GRAPH REVIEW SUBSTRATE                        │
│                                                                   │
│  PARTE 1 — SUBSTRATO (nós, arestas com histórico)                 │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │   authz ──E-AUTH-CHK──► checkout ──E-CHK-FRAUD──► fraud-│     │
│  │                            │              ‖          scorer │     │
│  │                            │E-CHK-LED     ‖ mutação dupla    │     │
│  │                            ▼              ‖                  │     │
│  │                         ledger ─E-LED-NOTIF─► notifications │     │
│  │                                                           │     │
│  │   aresta = contrato (campos) + RCAHistoryEntry[]          │     │
│  │   E-CHK-FRAUD carrega INC-2025-118 (o P0 anterior)       │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 2 — OVERLAY DE PRs + DETECÇÃO DE COLISÃO                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  PR-101 (bolha em checkout):  RENAME amount_minor       │     │
│  │      → amount_cents  em E-CHK-FRAUD e E-CHK-LED         │     │
│  │  PR-102 (bolha em fraud-scorer): TYPE_CHANGE            │     │
│  │      amount_minor int→decimal em E-CHK-FRAUD            │     │
│  │  PR-103 (bolha em ledger): ADD_OPTIONAL (compatível)    │     │
│  │                                                           │     │
│  │  agrupa por (edge_id, field_name):                       │     │
│  │    (E-CHK-FRAUD, amount_minor) ← PR-101 E PR-102         │     │
│  │    → CROSS_PR_FIELD_COLLISION  🟥 antes do merge         │     │
│  │    renomes divergentes → CROSS_PR_RENAME_CONFLICT 🟥     │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 3 — UNIDADE DE REVIEW = GRAFO (não o diff)                 │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  review_unit_for(PR-101, grafo, [PR-102]):               │     │
│  │    affected_edges:      E-CHK-FRAUD, E-CHK-LED           │     │
│  │    affected_counterparts:[fraud-scorer, ledger]          │     │
│  │    surfaced_history:    INC-2025-118 (na aresta!)        │     │
│  │    collisions:          cross-PR com PR-102              │     │
│  │    breaking_fields:     [amount_minor]                    │     │
│  │    blind_spots:         [fraud-scorer, ledger]           │     │
│  │    has_blocking:        True                              │     │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Modelar o substrato (`SoftwareGraph`, `ContractEdge`, `RCAHistoryEntry`)
O grafo precisa carregar as duas semânticas ao mesmo tempo: a estrutura (quem conversa com quem, sob qual contrato, com quais campos) e a memória (o que já quebrou nessa aresta, com link para a discussão do fix). O histórico ancorado na aresta é o que transforma conhecimento tribal arquivado em conhecimento surfacado por travessia — `history_for` é a consulta que o review de diff não consegue fazer.

### Parte 2 — Sobrepor os PRs e detectar colisões (`detect_collisions`)
O agrupamento é a chave: uma mudança isolada é um diff; duas mudanças no mesmo `(edge_id, field_name)` vindas de PRs distintos são uma colisão. Distinga os dois códigos — colisão genérica de campo versus conflito de renome divergente — e carregue os `pr_ids` e um rationale legível no achado: é ele que entra na mesa de review.

### Parte 3 — Deslocar a unidade de review (`review_unit_for`)
O relatório de review de um PR passa a ser um objeto de grafo: arestas tocadas, contrapartes do outro lado, histórico de RCA daquelas arestas, colisões com os outros PRs abertos e os pontos cegos — as contrapartes que o diff não contém. O `has_blocking` fecha o diagnóstico: colisão ou mudança quebradora com contraparte na jogada bloqueia; mudança compatível sem colisão passa.

---

## 💻 Starter Code

```python
"""
Exercício 11 — Software Graph Review Substrate
Nível 3 — Arquitetura Avançada

Pipeline: substrato (serviços como nós, contratos como arestas com
histórico de RCA) → overlay de PRs in-flight com detecção de colisão
cross-PR → unidade de review deslocada do diff para o grafo.

Fonte do padrão: docs/analysis/2026-08-31-the-last-human-code-review-
building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-
building-trust-in-ai-generated-co-patterns.md:44-63 (padrão 2, Software
Graph Review Substrate).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# TIPOS DE MUDANÇA E COMPATIBILIDADE DE CONTRATO
# ============================================================================

class ChangeKind(Enum):
    ADD_OPTIONAL_FIELD = "add_optional_field"   # compatível com consumidores
    ADD_REQUIRED_FIELD = "add_required_field"   # quebra consumidores atuais
    RENAME_FIELD = "rename_field"               # quebra quem lê o nome antigo
    REMOVE_FIELD = "remove_field"               # quebra quem consome o campo
    TYPE_CHANGE = "type_change"                 # quebra quem faz parse do tipo


BREAKING_KINDS = {
    ChangeKind.ADD_REQUIRED_FIELD,
    ChangeKind.RENAME_FIELD,
    ChangeKind.REMOVE_FIELD,
    ChangeKind.TYPE_CHANGE,
}


class CollisionCode(Enum):
    # dois PRs distintos mutando o mesmo campo da mesma aresta
    CROSS_PR_FIELD_COLLISION = "cross_pr_field_collision"
    # dois renomes do mesmo campo divergindo no novo nome
    CROSS_PR_RENAME_CONFLICT = "cross_pr_rename_conflict"


# ============================================================================
# PARTE 1 — SUBSTRATO: NÓS, ARESTAS E HISTÓRICO ANCORADO
# ============================================================================

@dataclass
class ContractField:
    """Um campo do contrato entre dois serviços."""
    name: str
    type: str
    required: bool = True


@dataclass
class RCAHistoryEntry:
    """
    Histórico de discussão de um fix de root-cause, ancorado NA aresta.

    É o metadado que transforma conhecimento tribal (thread de Slack de
    um incidente antigo) em conhecimento surfacado por travessia: aparece
    quando alguém toca a aresta, sem ninguém lembrar que ele existe.
    """
    incident_id: str
    root_cause: str
    discussion_url: str
    broken_pair: tuple[str, str]      # (provider, consumer) quebrado na época


@dataclass
class ContractEdge:
    """Aresta: o contrato entre dois serviços + o histórico acumulado."""
    edge_id: str
    provider: str
    consumer: str
    contract_name: str
    fields: list[ContractField] = field(default_factory=list)
    rca_history: list[RCAHistoryEntry] = field(default_factory=list)

    def has_field(self, field_name: str) -> bool:
        """TODO (Parte 1): existe um campo com este nome no contrato?"""
        # TODO: Implementar
        pass


@dataclass
class ServiceNode:
    """Nó: um repo/serviço do sistema."""
    service_id: str
    name: str
    tier: str = "P2"                  # P0 (crítico), P1, P2


@dataclass
class SoftwareGraph:
    """O substrato de review: serviços + contratos + histórico."""
    services: dict[str, ServiceNode] = field(default_factory=dict)
    edges: dict[str, ContractEdge] = field(default_factory=dict)

    def edges_touching(self, service_id: str) -> list[ContractEdge]:
        """
        TODO (Parte 1): arestas onde o serviço é provider OU consumer.

        Returns:
            Lista de ContractEdge (ordem estável: ordem de inserção).
        """
        # TODO: Implementar
        pass

    def consumers_of(self, edge_id: str) -> list[str]:
        """
        TODO (Parte 1): consumidores da aresta (aqui, 1 por aresta).

        Raises:
            KeyError: se edge_id não existir no grafo.
        """
        # TODO: Implementar
        pass

    def history_for(self, edge_id: str) -> list[RCAHistoryEntry]:
        """
        TODO (Parte 1): histórico de RCA ancorado na aresta.

        A consulta que o review de diff não consegue fazer: o que já
        quebrou neste contrato, com link para a discussão do fix.
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 2 — OVERLAY: PRS COMO BOLHAS E DETECÇÃO DE COLISÃO
# ============================================================================

@dataclass
class ContractChange:
    """Uma mutação que um PR aplica a um campo de um contrato."""
    edge_id: str
    field_name: str
    change_kind: ChangeKind
    new_name: str | None = None       # para RENAME_FIELD
    new_type: str | None = None       # para TYPE_CHANGE

    @property
    def is_breaking(self) -> bool:
        """TODO (Parte 1): change_kind está em BREAKING_KINDS?"""
        # TODO: Implementar
        pass


@dataclass
class PRBubble:
    """Um PR in-flight sobreposto ao grafo como bolha."""
    pr_id: str
    service_id: str                   # serviço autor do PR
    title: str
    changes: list[ContractChange] = field(default_factory=list)
    files: list[str] = field(default_factory=list)   # o que o diff enxerga


@dataclass
class CollisionFinding:
    """Achado de colisão cross-PR sobre uma aresta do grafo."""
    code: CollisionCode
    edge_id: str
    field_name: str
    pr_ids: tuple[str, ...]
    rationale: str


def detect_collisions(open_prs: list[PRBubble]) -> list[CollisionFinding]:
    """
    TODO (Parte 2): detectar colisões entre PRs in-flight.

    Algoritmo:
      1. Coletar (edge_id, field_name, pr_id, change) de TODOS os PRs.
      2. Agrupar por (edge_id, field_name).
      3. Grupo com mudanças de 2+ PRs distintos:
         a. ambos RENAME_FIELD com new_name diferentes
            → CROSS_PR_RENAME_CONFLICT
         b. caso contrário → CROSS_PR_FIELD_COLLISION
      4. rationale legível: o que cada PR tenta fazer com o campo.
      5. Mudanças de um PR só (como PR-103) não geram achado aqui —
         risco single-PR é papel do review_unit_for (Parte 3).

    Args:
        open_prs: PRs in-flight sobrepostos ao grafo.

    Returns:
        Lista de CollisionFinding (estável: ordenada por edge_id,
        field_name, pr_ids).
    """
    # TODO: Implementar
    pass


# ============================================================================
# PARTE 3 — UNIDADE DE REVIEW: O GRAFO, NÃO O DIFF
# ============================================================================

@dataclass
class PRReviewReport:
    """O review de um PR como objeto de grafo."""
    pr_id: str
    affected_edges: list[str] = field(default_factory=list)
    affected_counterparts: list[str] = field(default_factory=list)
    surfaced_history: list[RCAHistoryEntry] = field(default_factory=list)
    collisions: list[CollisionFinding] = field(default_factory=list)
    breaking_fields: list[str] = field(default_factory=list)
    blind_spots: list[str] = field(default_factory=list)
    has_blocking: bool = False
    rationale: str = ""


def review_unit_for(
    pr: PRBubble,
    graph: SoftwareGraph,
    other_open_prs: list[PRBubble],
) -> PRReviewReport:
    """
    TODO (Parte 3): o relatório de review do PR sob a ótica do grafo.

    Algoritmo:
      1. affected_edges: edge_ids únicos de pr.changes.
      2. affected_counterparts: para cada aresta afetada, o serviço do
         outro lado (consumer se pr é provider; provider se consumer),
         excluindo o próprio pr.service_id, sem duplicatas, ordenado.
      3. surfaced_history: RCA entries das arestas afetadas (ordem
         estável por aresta).
      4. collisions: detect_collisions([pr] + other_open_prs) filtrado
         para achados cujos pr_ids incluem pr.pr_id.
      5. breaking_fields: field_names (sem duplicata, ordenado) das
         mudanças do PR quebradoras em aresta com contraparte.
      6. blind_spots: contrapartes afetadas que NÃO aparecem em nenhum
         arquivo de pr.files (substring no path).
      7. has_blocking: collisions não-vazio OU breaking_fields não-vazio.
      8. rationale legível: resumo do porquê do bloqueio (ou da liberação).

    Args:
        pr: O PR sob review (a bolha central).
        graph: O substrato com contratos e histórico.
        other_open_prs: As demais bolhas in-flight (para colisão).

    Returns:
        PRReviewReport — a unidade de review deslocada do diff para o
        grafo: contrapartes, histórico, colisões e pontos cegos.
    """
    # TODO: Implementar
    pass


# ============================================================================
# DADOS DE TESTE — MERIDIANPAY (o grafo do postmortem INC-2026-207)
# ============================================================================

def build_payment_graph() -> SoftwareGraph:
    """Grafo do MeridianPay: 5 serviços, 4 contratos, 2 incidentes na aresta."""
    graph = SoftwareGraph(
        services={
            "checkout": ServiceNode("checkout", "Checkout Service", "P0"),
            "ledger": ServiceNode("ledger", "Ledger Service", "P0"),
            "fraud-scorer": ServiceNode("fraud-scorer", "Fraud Scorer", "P1"),
            "notifications": ServiceNode("notifications", "Notifications", "P2"),
            "authz": ServiceNode("authz", "Authorization", "P1"),
        },
        edges={
            "E-CHK-FRAUD": ContractEdge(
                edge_id="E-CHK-FRAUD",
                provider="checkout",
                consumer="fraud-scorer",
                contract_name="PaymentRequest v2",
                fields=[
                    ContractField("amount_minor", "int", required=True),
                    ContractField("currency", "str", required=True),
                    ContractField("payment_method", "str", required=False),
                ],
                rca_history=[
                    RCAHistoryEntry(
                        incident_id="INC-2025-118",
                        root_cause=(
                            "checkout renomeou campo do contrato sem "
                            "atualizar consumidor; fraud-scorer rejeitou "
                            "100% dos pagamentos por 41min (P0)"
                        ),
                        discussion_url="https://slack.archives/ch/payments/inc-2025-118",
                        broken_pair=("checkout", "fraud-scorer"),
                    ),
                ],
            ),
            "E-CHK-LED": ContractEdge(
                edge_id="E-CHK-LED",
                provider="checkout",
                consumer="ledger",
                contract_name="PaymentRequest v2",
                fields=[
                    ContractField("amount_minor", "int", required=True),
                    ContractField("currency", "str", required=True),
                ],
            ),
            "E-LED-NOTIF": ContractEdge(
                edge_id="E-LED-NOTIF",
                provider="ledger",
                consumer="notifications",
                contract_name="PaymentSettled v1",
                fields=[
                    ContractField("settlement_id", "str", required=True),
                    ContractField("amount_minor", "int", required=True),
                ],
                rca_history=[
                    RCAHistoryEntry(
                        incident_id="INC-2026-014",
                        root_cause=(
                            "ledger emitiu PaymentSettled sem amount_minor; "
                            "notifications dropou o evento silenciosamente"
                        ),
                        discussion_url="https://slack.archives/ch/payments/inc-2026-014",
                        broken_pair=("ledger", "notifications"),
                    ),
                ],
            ),
            "E-AUTH-CHK": ContractEdge(
                edge_id="E-AUTH-CHK",
                provider="authz",
                consumer="checkout",
                contract_name="AuthzDecision v1",
                fields=[
                    ContractField("decision", "str", required=True),
                ],
            ),
        },
    )
    return graph


def build_open_prs() -> list[PRBubble]:
    """Os 3 PRs in-flight da sexta-feira do postmortem."""
    pr_101 = PRBubble(
        pr_id="PR-101",
        service_id="checkout",
        title="Rename amount_minor -> amount_cents across PaymentRequest",
        changes=[
            ContractChange(
                edge_id="E-CHK-FRAUD",
                field_name="amount_minor",
                change_kind=ChangeKind.RENAME_FIELD,
                new_name="amount_cents",
            ),
            ContractChange(
                edge_id="E-CHK-LED",
                field_name="amount_minor",
                change_kind=ChangeKind.RENAME_FIELD,
                new_name="amount_cents",
            ),
        ],
        files=["services/checkout/api.py", "services/checkout/contracts.py"],
    )
    pr_102 = PRBubble(
        pr_id="PR-102",
        service_id="fraud-scorer",
        title="Tighten amount validation to decimal",
        changes=[
            ContractChange(
                edge_id="E-CHK-FRAUD",
                field_name="amount_minor",
                change_kind=ChangeKind.TYPE_CHANGE,
                new_type="decimal",
            ),
        ],
        files=["services/fraud-scorer/validation.py"],
    )
    pr_103 = PRBubble(
        pr_id="PR-103",
        service_id="ledger",
        title="Add optional correlation_id to PaymentSettled",
        changes=[
            ContractChange(
                edge_id="E-LED-NOTIF",
                field_name="correlation_id",
                change_kind=ChangeKind.ADD_OPTIONAL_FIELD,
            ),
        ],
        files=["services/ledger/events.py"],
    )
    return [pr_101, pr_102, pr_103]


def build_rename_war_prs() -> list[PRBubble]:
    """Dois times renomeando o mesmo campo para nomes diferentes."""
    pr_a = PRBubble(
        pr_id="PR-201",
        service_id="checkout",
        title="Rename amount_minor -> amount_cents",
        changes=[
            ContractChange(
                edge_id="E-CHK-LED",
                field_name="amount_minor",
                change_kind=ChangeKind.RENAME_FIELD,
                new_name="amount_cents",
            ),
        ],
        files=["services/checkout/contracts.py"],
    )
    pr_b = PRBubble(
        pr_id="PR-202",
        service_id="ledger",
        title="Rename amount_minor -> value_minor",
        changes=[
            ContractChange(
                edge_id="E-CHK-LED",
                field_name="amount_minor",
                change_kind=ChangeKind.RENAME_FIELD,
                new_name="value_minor",
            ),
        ],
        files=["services/ledger/importer.py"],
    )
    return [pr_a, pr_b]


# ============================================================================
# TESTES
# ============================================================================

def test_1_grafo_e_historico_na_aresta():
    """Cenário 1: o grafo conhece os vizinhos e o histórico de cada aresta."""
    print("\n" + "=" * 60)
    print("TESTE 1: Grafo — vizinhos e histórico ancorado")
    print("=" * 60)

    graph = build_payment_graph()
    touching = {e.edge_id for e in graph.edges_touching("checkout")}

    assert touching == {"E-CHK-FRAUD", "E-CHK-LED", "E-AUTH-CHK"}, (
        f"checkout toca 3 arestas (2 provider + 1 consumer), obtido {touching}"
    )
    assert graph.consumers_of("E-CHK-FRAUD") == ["fraud-scorer"]

    history = graph.history_for("E-CHK-FRAUD")
    assert len(history) == 1 and history[0].incident_id == "INC-2025-118", (
        "o P0 anterior vive ancorado na aresta E-CHK-FRAUD"
    )
    print(f"  checkout toca: {sorted(touching)}")
    print(f"  E-CHK-FRAUD carrega: {history[0].incident_id}")
    print("  TESTE 1 PASSOU")


def test_2_compatibilidade_de_mudanca():
    """Cenário 2: classificação de mudança quebradora por ChangeKind."""
    print("\n" + "=" * 60)
    print("TESTE 2: Compatibilidade — optional passa, rename quebra")
    print("=" * 60)

    add_optional = ContractChange(
        edge_id="E-LED-NOTIF",
        field_name="correlation_id",
        change_kind=ChangeKind.ADD_OPTIONAL_FIELD,
    )
    rename = ContractChange(
        edge_id="E-CHK-FRAUD",
        field_name="amount_minor",
        change_kind=ChangeKind.RENAME_FIELD,
        new_name="amount_cents",
    )

    assert add_optional.is_breaking is False
    assert rename.is_breaking is True
    print("  ADD_OPTIONAL_FIELD: compatível")
    print("  RENAME_FIELD: quebrador")
    print("  TESTE 2 PASSOU")


def test_3_colisao_cross_pr():
    """Cenário 3: PR-101 e PR-102 mutam o mesmo campo da mesma aresta."""
    print("\n" + "=" * 60)
    print("TESTE 3: Colisão Cross-PR — a sexta-feira do postmortem")
    print("=" * 60)

    pr_101, pr_102, pr_103 = build_open_prs()
    collisions = detect_collisions([pr_101, pr_102, pr_103])

    assert len(collisions) == 1, f"esperada 1 colisão, obtidas {len(collisions)}"
    hit = collisions[0]
    assert hit.code == CollisionCode.CROSS_PR_FIELD_COLLISION
    assert hit.edge_id == "E-CHK-FRAUD"
    assert hit.field_name == "amount_minor"
    assert set(hit.pr_ids) == {"PR-101", "PR-102"}
    assert "PR-103" not in hit.pr_ids, "PR-103 (campo novo, opcional) não colide"

    print(f"  {hit.code.value} em {hit.edge_id}/{hit.field_name}")
    print(f"  PRs: {sorted(hit.pr_ids)}")
    print(f"  rationale: {hit.rationale}")
    print("  TESTE 3 PASSOU")


def test_4_conflito_de_renome():
    """Cenário 4: dois renomes divergentes do mesmo campo."""
    print("\n" + "=" * 60)
    print("TESTE 4: Conflito de Renome — nomes divergentes")
    print("=" * 60)

    pr_a, pr_b = build_rename_war_prs()
    collisions = detect_collisions([pr_a, pr_b])

    assert len(collisions) == 1
    hit = collisions[0]
    assert hit.code == CollisionCode.CROSS_PR_RENAME_CONFLICT
    assert hit.edge_id == "E-CHK-LED"
    assert set(hit.pr_ids) == {"PR-201", "PR-202"}

    print(f"  {hit.code.value}: amount_cents vs value_minor")
    print("  TESTE 4 PASSOU")


def test_5_unidade_de_review():
    """Cenário 5: o review do PR-101 vê contrapartes, histórico e colisão."""
    print("\n" + "=" * 60)
    print("TESTE 5: Unidade de Review — grafo em vez de diff")
    print("=" * 60)

    graph = build_payment_graph()
    pr_101, pr_102, pr_103 = build_open_prs()

    report = review_unit_for(pr_101, graph, [pr_102, pr_103])
    assert sorted(report.affected_counterparts) == ["fraud-scorer", "ledger"], (
        "o rename do checkout afeta os DOIS consumidores do contrato"
    )
    assert any(
        h.incident_id == "INC-2025-118" for h in report.surfaced_history
    ), "o P0 anterior surfaca no review da aresta tocada"
    assert len(report.collisions) == 1, "a colisão com PR-102 entra no report"
    assert report.breaking_fields == ["amount_minor"]
    assert report.has_blocking is True

    report_103 = review_unit_for(pr_103, graph, [pr_101, pr_102])
    assert report_103.has_blocking is False, "campo opcional novo não bloqueia"
    assert report_103.breaking_fields == []

    print(f"  PR-101 → contrapartes: {sorted(report.affected_counterparts)}")
    print(f"  PR-101 → colisões: {[c.code.value for c in report.collisions]}")
    print(f"  PR-101 → has_blocking: {report.has_blocking}")
    print(f"  PR-103 → has_blocking: {report_103.has_blocking}")
    print("  TESTE 5 PASSOU")


def test_6_pontos_cegos_do_diff():
    """Cenário 6: contrapartes afetadas que o diff do PR não contém."""
    print("\n" + "=" * 60)
    print("TESTE 6: Pontos Cegos — o que o diff não enxerga")
    print("=" * 60)

    graph = build_payment_graph()
    pr_101, pr_102, pr_103 = build_open_prs()

    report = review_unit_for(pr_101, graph, [pr_102, pr_103])

    assert report.blind_spots == ["fraud-scorer", "ledger"], (
        "serviços afetados ausentes do diff = pontos cegos do review por diff"
    )
    assert pr_101.files == [
        "services/checkout/api.py", "services/checkout/contracts.py",
    ]
    print(f"  diff do PR-101: {pr_101.files}")
    print(f"  pontos cegos:   {report.blind_spots}")
    print("  TESTE 6 PASSOU")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 11: SOFTWARE GRAPH REVIEW SUBSTRATE")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_1_grafo_e_historico_na_aresta()
    # test_2_compatibilidade_de_mudanca()
    # test_3_colisao_cross_pr()
    # test_4_conflito_de_renome()
    # test_5_unidade_de_review()
    # test_6_pontos_cegos_do_diff()

    print("\nTODO: Implemente as partes acima!")
    print("   1. ContractEdge/SoftwareGraph — substrato com histórico na aresta")
    print("   2. detect_collisions() — agrupamento por (edge, field) entre PRs")
    print("   3. review_unit_for() — a unidade de review como objeto de grafo")
    print("   Após implementar, descomente os testes em main()")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

```python
# 1. O grafo carrega o conhecimento tribal na aresta
graph = build_payment_graph()
assert {e.edge_id for e in graph.edges_touching("checkout")} == {
    "E-CHK-FRAUD", "E-CHK-LED", "E-AUTH-CHK"
}
assert graph.history_for("E-CHK-FRAUD")[0].incident_id == "INC-2025-118"

# 2. Compatibilidade é classificada pelo tipo de mudança
assert ContractChange("E-X", "f", ChangeKind.ADD_OPTIONAL_FIELD).is_breaking is False
assert ContractChange("E-X", "f", ChangeKind.RENAME_FIELD, new_name="g").is_breaking is True

# 3. Colisão cross-PR: dois PRs, mesma aresta, mesmo campo — antes do merge
pr_101, pr_102, pr_103 = build_open_prs()
collisions = detect_collisions([pr_101, pr_102, pr_103])
assert any(
    c.code == CollisionCode.CROSS_PR_FIELD_COLLISION
    and set(c.pr_ids) == {"PR-101", "PR-102"}
    and c.field_name == "amount_minor"
    for c in collisions
)

# 4. Conflito de renome divergente é um achado distinto
pr_a, pr_b = build_rename_war_prs()
assert any(
    c.code == CollisionCode.CROSS_PR_RENAME_CONFLICT
    for c in detect_collisions([pr_a, pr_b])
)

# 5. A unidade de review é o grafo, não o diff
report = review_unit_for(pr_101, build_payment_graph(), [pr_102, pr_103])
assert sorted(report.affected_counterparts) == ["fraud-scorer", "ledger"]
assert report.has_blocking is True
assert any(h.incident_id == "INC-2025-118" for h in report.surfaced_history)

# 6. Pontos cegos: contrapartes que o diff não contém
assert report.blind_spots == ["fraud-scorer", "ledger"]

# 7. Mudança compatível sem colisão não bloqueia
report_103 = review_unit_for(pr_103, build_payment_graph(), [pr_101, pr_102])
assert report_103.has_blocking is False
```

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Substrato (Parte 1)** | 25% | Grafo sem histórico na aresta | Nós/arestas corretos, histórico opcional ignorado | Travessias (`edges_touching`, `history_for`) corretas | Histórico como cidadão de primeira classe: RCA ancorado e surfacado por travessia |
| **Colisão (Parte 2)** | 25% | Sem agrupamento por campo | Detecta colisão genérica | Distingue `FIELD_COLLISION` de `RENAME_CONFLICT` | Achados com `pr_ids` e rationale que entra na mesa de review |
| **Unidade de review (Parte 3)** | 30% | Review continua centrado no diff | Contrapartes calculadas | + Histórico surfacado, colisões e `breaking_fields` no report | + `blind_spots` plagueando a tese: o que o diff estruturalmente não vê |
| **Interpretação arquitetural** | 20% | Trata o grafo como diagrama estático | Entende nós/arestas como modelo | Articula a mudança de unidade (diff → grafo) | Conecta ao contexto do repo: grafos de contexto vs grafo do artefato revisado; colisão ≠ conflito de merge |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

### Para o substrato

1. **O histórico é dado da aresta, não apêndice.** Se `RCAHistoryEntry` estiver num dict separado "para consulta", você reconstruiu o wiki — o conhecimento existe mas não é surfacado pela travessia. Ele vive dentro do `ContractEdge`.
2. **`edges_touching` olha os dois lados.** `checkout` é provider de duas arestas e consumer de uma (`E-AUTH-CHK`). Esquecer o lado consumer quebra o Cenário 1 silenciosamente.

### Para a colisão

1. **Agrupe por `(edge_id, field_name)`, não por aresta só.** Duas mudanças em campos diferentes da mesma aresta são coordenáveis; duas mudanças no mesmo campo de PRs distintos são a colisão que derrubou o MeridianPay.
2. **A ordem dos checks importa.** Teste `RENAME_CONFLICT` antes do genérico: dois renomes divergentes satisfazem as duas condições, mas o achado específico informa mais a decisão.
3. **PR-103 é o controle negativo.** Campo novo opcional, aresta com contraparte, zero colisões — se ele gera achado, seu agrupamento está granular demais.

### Para a unidade de review

1. **Contraparte é o outro lado da aresta.** Quando o PR é do provider (`pr_101` em `checkout`), contraparte é o consumer; quando é do consumer (`pr_102` em `fraud-scorer`), é o provider. Exclua sempre o próprio autor do PR.
2. **`blind_spots` é subtração, não consulta.** Contrapartes afetadas MENOS as que aparecem nos `files` do diff. Para o PR-103 a contraparte `notifications` também é ponto cego — o review por grafo informa, o `has_blocking` é que decide.
3. **O `has_blocking` é a síntese.** Colisão OU mudança quebradora com contraparte. Não confunda com "mudança quebradora em aresta sem contraparte nenhuma" — aí não há quem quebrar.

---

## ❓ Dúvidas Comuns

**P: Por que o histórico de incidente vive na aresta e não no nó do serviço?**
R: Porque o conhecimento tribal do postmortem é sobre o *par*: "checkout mudou contrato e quebrou fraud-scorer" (`...analysis.md:68`). Ancorar no serviço perde a direção; ancorar no repositório espalha o mesmo conhecimento pelos dois lados. A aresta é o endereço exato onde a próxima mudança vai precisar dele — é a disciplina de placement que a análise do padrão 3 chama de "context located at the graph node/edge where it applies" (`...patterns.md:71-74`).

**P: Isso não é o Relational Context Graph do repositório?**
R: Não — e a diferença é o objeto. O [[docs/canonical/relational-context-graph|Relational Context Graph]] tipa arestas entre *unidades de contexto* (tool results, decisões, snapshots) para recuperar memória de agente. Aqui as arestas são *contratos entre software* com histórico de discussões humanas. A classificação deste padrão é explícita: o repo tem o vocabulário, "but for context units, not for software artifacts under review" (`...classification.md:50`). Mesma gramática, objeto novo — por isso a integração é `High`.

**P: Conflito de merge do git não pegaria o PR-201 vs PR-202?**
R: Não — eles estão em *repos diferentes* (`services/checkout/contracts.py` vs `services/ledger/importer.py`). O git só detecta conflito nas mesmas linhas do mesmo repo. A colisão de contrato é invisível para qualquer ferramenta cuja unidade seja o diff: é exatamente o argumento para deslocar a unidade de review para o grafo (`...analysis.md:70`).

**P: De onde viriam, em produção, os `ContractChange` de cada PR?**
R: Da extração de contrato: comparação do contrato serializado (OpenAPI/protobuf/AVRO) antes e depois do PR, ou parsing do diff contra um registry de schemas. O exercício entrega os changes prontos porque o foco é o substrato — a extração é a limitação declarada da fonte ("requires contract extraction and discussion-history linking per edge", `...patterns.md:62`).

**P: Por que `has_blocking` não considera o tier do serviço (P0/P1/P2)?**
R: Para manter o exercício no mecanismo estrutural. Tier entra como dado do nó — uma extensão natural é ponderar severidade por tier e por histórico da aresta (uma aresta com dois P0s e um incidente anterior pesa mais), que é o caminho para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-semantic-rule-gated-auto-approve-block|Exercício 12]]: as regras semânticas de approve/block consomem exatamente estes achados como insumo.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 2 completo e sua classificação em `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:44-63` e `...classification.md:46-61` — e o canônico [[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]]
2. Compare com [[docs/canonical/relational-context-graph|Relational Context Graph]]: as quatro classes de aresta tipada (Dependency, Provenance, Supersession, Causation) aplicadas a *contratos de software* — qual seria a tipagem equivalente para arestas de contrato?
3. Siga para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-semantic-rule-gated-auto-approve-block|Exercício 12: Semantic-Rule-Gated Auto Approve/Block]] — o motor de decisão por regras que consome este grafo: os `CollisionFinding` e `PRReviewReport` daqui são o insumo que as regras semânticas de lá avaliam

---

*Exercício 11 | Nível 3 — Arquitetura Avançada | Software Graph Review Substrate*

**O contrato não vive em nenhum diff — vive na aresta. Revise a aresta.**
