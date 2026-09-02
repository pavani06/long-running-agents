---
title: "Exercício 19: Content-Addressed Prompt Graph — Saber Exatamente o Que Entrou no Contexto"
type: exercise
level: 3
aliases: ["content-addressed prompt graph", "grafo de prompt endereçado por conteúdo", "prompt como grafo de hashes", "exact input reconstruction", "diff de prompt por componente", "compaction como manipulação de grafo"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "context-engineering", "evals", "production", "arquitetura", "harness-engineering", "verification"]
relates-to: ["[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|Padrões Agent Frameworks Considered Harmful]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-classification|Classificação Agent Frameworks Considered Harmful]]", "[[docs/canonical/prompt-as-code-causal-change-management|Prompt as Code Causal Change Management]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/graph-addressed-context-placement|Graph-Addressed Context Placement]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-17-self-iterating-agent-loop|Exercício 17: Self-Iterating Agent Loop]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-18-typed-event-boundaries|Exercício 18: Typed Tool and Event Boundaries]]"]
duration: "90-120 min"
last_updated: 2026-09-02
---

# 🔑 Exercício 19: Content-Addressed Prompt Graph — Saber Exatamente o Que Entrou no Contexto
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `04-server-side-compaction.md` (Nível 3) + `docs/canonical/prompt-as-code-causal-change-management.md` + `docs/canonical/stable-harness-prompt.md`
**Objetivo:** Representar o prompt como grafo de hashes de componentes ANTES da renderização em texto, com armazenamento endereçado por conteúdo (estilo git/Nix), resposta rastreável ao prompt exato, diff por componente entre runs e compaction como manipulação de grafo — o substrato mecânico que o replay do repo sempre assumiu e nunca aterrou

---

## 📖 Prólogo: A Regressão Que Ninguém Conseguiu Atribuir

### Terça vs. quarta-feira. Mesmo agente, output pior.

```
PM:          "o recommender piorou de terça pra quarta. As recomendações
              estão genéricas. O que mudou?"

ENG:         "nada! O código tá igual. Bom... a Ana editou a descrição
              da tool search_catalog pra ficar mais clara, o time
              adicionou uma skill nova de 'plano de assinatura', e o
              template da user message mudou pro formato curto.
              Mas nada que..."

PM:          "três mudanças. E qual delas quebrou?"

ENG:         "é... não sei dizer. O log da sessão guarda o prompt
              RENDERIZADO — o textão. O diff do textão mostra 47 linhas
              mudadas, mas não diz se foi a skill, a tool ou a user
              message. E tem um agravante: a sessão de quarta passou por
              compaction no meio, que corta e reescreve trechos como
              string. O prompt que eu vejo no log não é o prompt que
              entrou no modelo — é uma colagem depois de duas
              transformações."

PM:          "então 'saber o que efetivamente entrou no contexto' é
              impossível hoje?"

ENG:         "no momento, sim. E a troca de modelo barato que a gente
              quer fazer mês que vem? Sem saber o input exato, a gente
              não consegue nem comparar maçã com maçã — cada run é uma
              colagem diferente."
```

**O custo do prompt como textão indiferenciável:**

```
╔══════════════════════════════════════════════════════════════════╗
║      O QUE ENTROU NO CONTEXTO? — A PERGUNTA SEM RESPOSTA           ║
║                                                                  ║
║  O que o repo já tem          O que ninguém tem                  ║
║  ─────────────────────────    ──────────────────────────────────  ║
║  prompts versionados em git   hash do CONTEÚDO de cada componente ║
║  (prompt-as-code, commits     (estilo git/Nix — patterns.md:44)   ║
║  causais)                     prompt como GRAFO DE HASHES antes   ║
║  rollback por git-revert      da renderização em texto            ║
║  "qual texto no deploy X"     resposta → prompt EXATO → contexto  ║
║  ids de catálogo p/ contexto  diff POR COMPONENTE entre runs      ║
║  omitido                      compaction como manipulação de      ║
║  replay de conversas          grafo (não de strings)              ║
║                                                                  ║
║  classification.md:44: "None of this is content addressing" —     ║
║  o repo replaya conversas, não o prompt exato reconstruído de     ║
║  hashes; a troca de modelo e a regressão de prompt ficam sem      ║
║  ground mecânico                                                 ║
║                                                                  ║
║  Aviso do próprio autor: "deep rabbit hole" (patterns.md:57) —    ║
║  nasceu de falha de produção, não de plano                       ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é falta de versionamento.** O repo trata prompt como código com
commits causais e rollback auditável (`docs/canonical/prompt-as-code-causal-change-management.md:80-85`).
O problema é a **granularidade**: o git versiona ARQUIVOS por ponto no tempo; o padrão
versiona cada COMPONENTE do prompt por hash do conteúdo, e representa a sessão como
grafo desses hashes **antes** de virar texto (`...patterns.md:47`). É isso que responde
"o que entrou no contexto" sem reconstruir colagens: a sessão de chat não representa o
prompt real — compaction, quirks de provider e thinking traces ocultos entram no meio
(`...patterns.md:42`).

**Sua missão:** implementar o `ContentStore` (put/get endereçado por hash, com dedup
grátis), o `PromptGraph` (lista ordenada de componentes com hash estável e renderização
tardia), o `ResponseRecord` (resposta rastreável ao prompt exato), o `diff_prompts()`
(qual componente mudou entre runs), a `compact()` como operação de grafo, e o `replay()`
(o mesmo grafo de hashes alimentando outro modelo — input idêntico, maçã com maçã).

---

## 🧠 O Contexto

### O Modelo Mental: Hash Antes do Texto, Texto Depois

O padrão é o "deep rabbit hole" assumido do fonte: investimento grande que nasceu de
uma falha de produção (`...patterns.md:57-58`). Quatro propriedades o definem:

1. **O componente é a unidade, o hash é o endereço.** O prompt se decompõe em
   system prompt, descrição de cada skill, descrição de cada tool, user message
   (`...patterns.md:43`). Cada componente ganha `hash(kind, content)`; o mesmo
   conteúdo produz o MESMO hash em qualquer sessão, em qualquer dia — dedup e
   reconstrução vêm de graça (é o modelo git/Nix aplicado a prompt):

```
   SESSÃO (o que o modelo viu)
     │  não é um textão: é um grafo de hashes ANTES de renderizar
     ▼
   ┌─────────────────────────────────────────────────────┐
   │ PromptGraph                                          │
   │                                                     │
   │  (system,   a1b2c3)──┐                              │
   │  (skill,    9f8e7d)──┤─┬──▶ root: 77aa41            │
   │  (skill,    0c1d2e)──┤ │      (hash da lista)       │
   │  (tool,     4b5a69)──┤ │                            │
   │  (user,     e3f4a5)──┘ │                            │
   └───────────────────────┼─────────────────────────────┘
                           ▼
              ┌──────────────────────────┐
              │ ResponseRecord           │
              │ prompt_root: 77aa41      │──▶ o output traca de volta
              │ response_hash: b9c8d7    │    ao input EXATO
              │ model: "koda-mini-v1"    │
              └──────────────────────────┘

   diff(quarta, terça): tool 4b5a69 → 55aa01 MUDOU;
                        skill 0c1d2e é NOVA; user e3f4a5 MUDOU;
                        system a1b2c3 intacta.
   Quatro linhas substituem o diff de 47 linhas do textão.
```

2. **A resposta mora no mesmo esquema.** Model responses endereçadas como o prompt
   (`...patterns.md:45`): o par (input, output) fica consultável por hash —
   "por que o agente retornou isso" vira uma query, não uma arqueologia
   (`...patterns.md:55`).

3. **Compaction é manipulação de grafo.** Em vez de reescrever o textão com strings,
   a compaction remove/sumariza NÓS do grafo (`...patterns.md:50`): o grafo compactado
   é um novo grafo reconstruível, e o que foi cortado continua endereçado no store —
   nada desaparece.

4. **O replay volta a ser maçã com maçã.** O replay de conversas que o repo ensina
   (`docs/canonical/production-grounded-eval-sampling.md:28`) assume inputs
   comparáveis; o grafo de hashes entrega o literal: o MESMO conjunto de hashes
   alimentando outro modelo é input identico por construção (`...patterns.md:49`).

Os vizinhos do repo, e por que não bastam: o `prompt-as-code` versiona arquivos por
commit, não conteúdo por hash (`...md:28`); o `stable-harness-prompt` exige versões de
prompt/rubric/catalog no replay (`...md:52`) — versão de ARQUIVO, não reconstrução
exata; o `addressable-memory-catalog` dá id estável ao contexto OMITIDO
(`...md:28-43`) — endereça o que ficou de fora, não o que entrou; o
`graph-addressed-context-placement` chaveia conhecimento a nós de grafo de software
(`...md:42-48`) — grafo de outro domínio. O NOT_FOUND é explícito: "no hash function
over prompt components, no storage keyed by content hash" (`...classification.md:54`).

### O Que Você Vai Construir

1. `PromptComponent` — a unidade: kind (system/skill/tool/user) + content + hash
   estável de 12 hex chars
2. `ContentStore` — put/get endereçado por hash; put duplicado não duplica (dedup);
   get inexistente explode (`UnknownHashError`)
3. `PromptGraph` — lista ordenada de componentes com `root_hash` (hash da lista),
   `render()` tardia (o texto só existe quando alguém pede), e reconstrução a partir
   da lista de hashes
4. `ResponseRecord` — resposta endereçada no mesmo esquema, amarrada ao
   `prompt_root` e ao `model_id`
5. `diff_prompts()` — por componente: ADDED / REMOVED / CHANGED / UNCHANGED, com kind
   de cada entrada — o diff que atribui a regressão
6. `compact()` — operação de grafo: remove kinds sumarizáveis e produz novo grafo;
   o store continua capaz de reconstruir os dois
7. `replay()` — o mesmo `prompt_root` com outro `model_id`: input idêntico por
   construção

---

## 📋 Cenário

O recommender do KODA. Duas sessões: terça e quarta. A de quarta tem a descrição da
tool `search_catalog` reescrita, a skill `subscription-plan` adicionada, a user message
no formato curto — e a system prompt intacta. A resposta de terça está no log; a de
quarta está pior. A pergunta do PM ("qual das três mudanças quebrou?") só tem resposta
com diff por componente. Depois: a sessão de quarta cresceu e passou de 6 para 4
componentes via compaction (a skill antiga `audio-ack` foi sumarizada fora) — o grafo
compactado precisa continuar reconstruível. Por fim: o mesmo `prompt_root` de terça
alimentando o modelo barato `koda-mini-v1` — replay de input idêntico.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Hash estável e dedup:** `hash_component()` retorna 12 hex chars derivados
   de (kind, content); o mesmo conteúdo no mesmo kind produz o mesmo hash sempre; o
   `ContentStore.put()` de conteúdo repetido não cresce o store.
2. **RF2 — Grafo antes do texto:** `PromptGraph` só carrega componentes com hash; o
   texto renderizado é derivado on-demand em `render()`; `root_hash` identifica a
   lista inteira — dois grafos com os mesmos componentes na mesma ordem têm o mesmo
   `root_hash`.
3. **RF3 — Resposta rastreável:** cada `ResponseRecord` carrega `prompt_root`,
   `response_hash` (hash do conteúdo da resposta, kind "response") e `model_id`;
   dado o record, o prompt exato se reconstrói do store sem sobras.
4. **RF4 — Diff por componente:** `diff_prompts()` retorna entradas ADDED / REMOVED /
   CHANGED / UNCHANGED com kind e hashes; para as sessões do cenário, ele nomeia
   exatamente: tool CHANGED, skill ADDED, user CHANGED, system UNCHANGED — nada de
   diff de textão.
5. **RF5 — Compaction como grafo:** `compact()` recebe um grafo e os kinds a
   sumarizar, remove esses nós e devolve um NOVO `PromptGraph` (imutabilidade); o
   grafo original continua reconstruível no store — nada é perdido.
6. **RF6 — Replay de input idêntico:** `replay()` reconstrói o prompt do
   `prompt_root` e gera um novo `ResponseRecord` com OUTRO `model_id` e o MESMO
   `prompt_root` — a comparação entre modelos é maçã com maçã por construção.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas** (`hashlib` para sha256), type hints
   obrigatórios
2. **RT2 — `dataclasses` congelados** para componente, grafo e record; store é a
   única estrutura mutável
3. **RT3 — Renderização tardia:** nenhuma operação (put, diff, compact, replay)
   depende do texto renderizado — só de hashes; o texto é projeção
4. **RT4 — Hash determinístico e colado no kind:** kind entra no hash (mesmo texto
   como system e como user são componentes DIFERENTES)

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                  CONTENT-ADDRESSED PROMPT GRAPH                        │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ COMPONENTS + STORE (RF1)                                       │    │
│  │ PromptComponent(kind, content) ──hash──▶ "a1b2c3d4e5f6"         │    │
│  │ ContentStore.put()/get() — dedup grátis, endereço = conteúdo    │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ PROMPT GRAPH (RF2) — hashes ANTES do texto                      │    │
│  │ [(system,a1b2),(skill,9f8e),(tool,4b5a),(user,e3f4)]            │    │
│  │ root_hash = hash da lista │ render() tardia (projeção)          │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ RESPONSE RECORD (RF3) — o output mora no mesmo esquema          │    │
│  │ (prompt_root, response_hash, model_id) — a resposta traca de    │    │
│  │ volta ao input EXATO                                            │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ OPERAÇÕES SOBRE O GRAFO (RF4-RF6)                               │    │
│  │ diff_prompts:  ADDED/REMOVED/CHANGED/UNCHANGED por componente   │    │
│  │ compact:       remove kinds → NOVO grafo (o velho persiste)     │    │
│  │ replay:        mesmo prompt_root, outro model_id — maçã/maçã    │    │
│  └────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar por que o diff do textão não atribui (15 min)

Com as duas sessões renderizadas do fixture: rode um diff mental (ou no papel) dos
textos e explique por que ele não responde "qual componente mudou". Depois: qual
informação o hash por componente carrega que a linha do textão não carrega? Responda
como comentário.

### Parte 2 — Store, grafo e rastreio (40 min)

Implemente `hash_component()`, `ContentStore` (RF1), `PromptGraph` com render tardia
e `root_hash` (RF2) e `ResponseRecord` (RF3).

### Parte 3 — Diff, compaction e replay (45 min)

Implemente `diff_prompts()` (RF4), `compact()` (RF5) e `replay()` (RF6). Verifique: o
diff nomeia as três mudanças do cenário e poupa a system; a compaction preserva os
dois grafos; o replay mantém o `prompt_root` trocando o modelo.

---

## 💻 Starter Code

```python
"""
Exercício 19 — Content-Addressed Prompt Graph
Nível 3 — Arquitetura Avançada

O prompt como grafo de hashes de componentes ANTES da renderização.
Hash estável + store endereçado por conteúdo: resposta rastreável ao
input exato, diff por componente, compaction como grafo, replay de
input idêntico entre modelos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib


# ============================================================================
# DATA MODELS
# ============================================================================

class ComponentKind(Enum):
    SYSTEM = "system"
    SKILL = "skill"
    TOOL = "tool"
    USER = "user"
    RESPONSE = "response"     # a resposta mora no mesmo esquema (RF3)


def hash_component(kind: ComponentKind, content: str) -> str:
    """
    12 hex chars de sha256 sobre (kind + separador + conteúdo).
    O kind entra no hash (RT4): mesmo texto, kinds diferentes →
    componentes diferentes.
    """
    # TODO: implemente
    raise NotImplementedError


@dataclass(frozen=True)
class PromptComponent:
    kind: ComponentKind
    content: str
    hash: str                 # computado na construção via __post_init__? Não:
                              # dataclass congelado — receba o hash pronto ou
                              # use uma factory (ver make_component abaixo)

    def render(self) -> str:
        """Uma linha por componente: '[kind] conteúdo'."""
        # TODO: implemente
        raise NotImplementedError


def make_component(kind: ComponentKind, content: str) -> PromptComponent:
    """Factory que computa o hash — o único lugar onde hash nasce."""
    # TODO: implemente
    raise NotImplementedError


class UnknownHashError(Exception):
    pass


@dataclass
class ContentStore:
    """put/get endereçado por conteúdo; dedup grátis (RF1)."""
    _blobs: dict[str, PromptComponent] = field(default_factory=dict)

    def put(self, component: PromptComponent) -> str:
        """Guarda e retorna o hash; repetido não cresce o store."""
        # TODO: implemente
        raise NotImplementedError

    def get(self, component_hash: str) -> PromptComponent:
        """Hash desconhecido explode (UnknownHashError)."""
        # TODO: implemente
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._blobs)


@dataclass(frozen=True)
class PromptGraph:
    """A sessão como grafo de hashes — o texto é projeção tardia (RF2)."""
    hashes: tuple[str, ...]              # endereços no store, ordenados

    @property
    def root_hash(self) -> str:
        """Hash da LISTA de hashes: mesma ordem + mesmos componentes →
        mesmo root. Dois grafos iguais são indistinguíveis (por design)."""
        # TODO: implemente (dica: junte os hashes com '\n' e hash de novo)
        raise NotImplementedError

    def render(self, store: ContentStore) -> str:
        """Projeção tardia: só aqui o texto existe (RT3)."""
        # TODO: implemente
        raise NotImplementedError


def build_graph(
    store: ContentStore, components: list[PromptComponent]
) -> PromptGraph:
    """Constrói o grafo e garante que cada componente está no store."""
    # TODO: implemente
    raise NotImplementedError


@dataclass(frozen=True)
class ResponseRecord:
    """A resposta no mesmo esquema de endereçamento (RF3)."""
    prompt_root: str
    response_hash: str          # hash do conteúdo da resposta (kind RESPONSE)
    model_id: str


# ============================================================================
# PARTE 3 — OPERAÇÕES SOBRE O GRAFO
# ============================================================================

class DiffStatus(Enum):
    ADDED = "added"
    REMOVED = "removed"
    CHANGED = "changed"
    UNCHANGED = "unchanged"


@dataclass(frozen=True)
class ComponentDiff:
    status: DiffStatus
    kind: ComponentKind
    before: str | None         # hash no grafo antigo (None se ADDED)
    after: str | None          # hash no grafo novo (None se REMOVED)


def diff_prompts(old: PromptGraph, new: PromptGraph,
                 store: ContentStore) -> list[ComponentDiff]:
    """
    Diff POR COMPONENTE (RF4): casa nós pela posição+kind e compara hash.
    Mesma posição, hashes diferentes → CHANGED; nó sem contraparte →
    ADDED/REMOVED; hash igual → UNCHANGED.
    """
    # TODO: implemente
    raise NotImplementedError


def compact(
    graph: PromptGraph,
    store: ContentStore,
    summarize_kinds: tuple[ComponentKind, ...],
) -> PromptGraph:
    """
    Compaction como manipulação de grafo (RF5): devolve um NOVO grafo
    sem os kinds sumarizados; o original segue reconstruível no store.
    Manipulação de grafo, não de strings (patterns.md:50).
    """
    # TODO: implemente
    raise NotImplementedError


def replay(
    prompt_root_graph: PromptGraph,
    store: ContentStore,
    model_id: str,
    response_text: str,
) -> ResponseRecord:
    """
    Replay de input idêntico (RF6): reconstrói o prompt do grafo (a
    renderização existe para o modelo consumir), endereça a resposta no
    mesmo esquema e devolve o record — MESMO prompt_root, OUTRO model_id.
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# FIXTURES — terça vs. quarta-feira no recommender
# ============================================================================

SYSTEM_TUE = "Você é o recomendador do KODA. Seja específico."
TOOL_TUE = "search_catalog: busca produtos por query textual."
TOOL_WED = ("search_catalog: busca produtos no catálogo ativo por query "
            "textual; use termos do vocabulário do cliente.")
SKILL_PLAN = "skill subscription-plan: responda dúvidas sobre planos."
SKILL_AUDIO = "skill audio-ack: confirme recepção de áudio antes de tudo."
USER_TUE = "Quero um fone bom pra reunião, até 300."
USER_WED = "fone reunião até 300"


def build_tuesday(store: ContentStore) -> PromptGraph:
    return build_graph(store, [
        make_component(ComponentKind.SYSTEM, SYSTEM_TUE),
        make_component(ComponentKind.SKILL, SKILL_AUDIO),
        make_component(ComponentKind.TOOL, TOOL_TUE),
        make_component(ComponentKind.USER, USER_TUE),
    ])


def build_wednesday(store: ContentStore) -> PromptGraph:
    return build_graph(store, [
        make_component(ComponentKind.SYSTEM, SYSTEM_TUE),   # intacta
        make_component(ComponentKind.SKILL, SKILL_PLAN),    # nova skill
        make_component(ComponentKind.TOOL, TOOL_WED),       # reescrita
        make_component(ComponentKind.USER, USER_WED),       # formato curto
    ])


# ============================================================================
# TESTS
# ============================================================================

def test_store_dedups_and_addresses():
    store = ContentStore()
    a = make_component(ComponentKind.SYSTEM, SYSTEM_TUE)
    b = make_component(ComponentKind.SYSTEM, SYSTEM_TUE)
    assert a.hash == b.hash, "mesmo kind+conteúdo → mesmo hash (RF1)"
    store.put(a)
    size_before = len(store)
    assert store.put(b) == a.hash
    assert len(store) == size_before, "put duplicado não cresce o store"
    assert store.get(a.hash).content == SYSTEM_TUE
    try:
        store.get("000000000000")
        raise AssertionError("hash desconhecido deve explodir (RF1)")
    except UnknownHashError:
        pass
    # RT4: mesmo texto em kind diferente → componente diferente
    c = make_component(ComponentKind.USER, SYSTEM_TUE)
    assert c.hash != a.hash
    print("TESTE 1 PASSOU")


def test_graph_hash_before_text():
    store = ContentStore()
    g1 = build_tuesday(store)
    g2 = build_tuesday(ContentStore())   # outro store, mesmos componentes
    assert g1.root_hash == g2.root_hash, "grafo é função dos hashes (RF2)"
    text = g1.render(store)
    assert "[system]" in text and SYSTEM_TUE in text
    assert "[user]" in text and USER_TUE in text
    print("TESTE 2 PASSOU")


def test_diff_attributes_the_regression():
    store = ContentStore()
    tue = build_tuesday(store)
    wed = build_wednesday(store)
    diffs = diff_prompts(tue, wed, store)
    by_kind = {d.kind: d for d in diffs}
    assert by_kind[ComponentKind.TOOL].status == DiffStatus.CHANGED
    assert by_kind[ComponentKind.USER].status == DiffStatus.CHANGED
    assert by_kind[ComponentKind.SYSTEM].status == DiffStatus.UNCHANGED
    # a skill de áudio saiu e a de plano entrou: uma por posição
    skill = by_kind[ComponentKind.SKILL]
    assert skill.status in (DiffStatus.CHANGED, DiffStatus.REMOVED)
    statuses = {d.status for d in diffs}
    assert DiffStatus.UNCHANGED in statuses, "o diff poupa o que não mudou"
    print("TESTE 3 PASSOU")


def test_compact_and_replay():
    store = ContentStore()
    tue = build_tuesday(store)

    compacted = compact(tue, store, summarize_kinds=(ComponentKind.SKILL,))
    assert ComponentKind.SKILL not in {
        store.get(h).kind for h in compacted.hashes
    }, "kind sumarizado sai do grafo (RF5)"
    assert len(compacted.hashes) == 3
    assert tue.render(store), "o grafo original segue reconstruível (RF5)"

    record_tue = replay(tue, store, "koda-prod-v2", "fone Jabra Evolve2 65")
    record_mini = replay(tue, store, "koda-mini-v1", "fone bluetooth genérico")
    assert record_tue.prompt_root == record_mini.prompt_root == tue.root_hash, (
        "replay mantém o prompt_root — input idêntico por construção (RF6)"
    )
    assert record_tue.model_id != record_mini.model_id
    assert record_tue.response_hash != record_mini.response_hash
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 19: CONTENT-ADDRESSED PROMPT GRAPH")
    print("=" * 60)
    # Descomente após implementar:
    # test_store_dedups_and_addresses()
    # test_graph_hash_before_text()
    # test_diff_attributes_the_regression()
    # test_compact_and_replay()
    print("\nTODO: implemente hashing, store, graph, records,")
    print("diff, compact e replay")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] Mesmo kind+conteúdo → mesmo hash sempre; put duplicado não cresce o store; hash desconhecido explode (RF1)
- [ ] O grafo carrega só hashes; `render()` produz o texto on-demand; grafos com os mesmos componentes na mesma ordem compartilham `root_hash` (RF2)
- [ ] `ResponseRecord` carrega `prompt_root` + `response_hash` + `model_id`; o prompt exato se reconstrói do store a partir do record (RF3)
- [ ] O diff nomeia TOOL CHANGED, USER CHANGED, SKILL tocada e SYSTEM UNCHANGED — atribuição por componente, sem diff de textão (RF4)
- [ ] `compact()` devolve grafo novo sem os kinds sumarizados e o original segue reconstruível (RF5)
- [ ] `replay()` com outro modelo mantém o `prompt_root` idêntico — comparação entre modelos maçã com maçã (RF6)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Hash + Store (Parte 2)** | 20% | Não implementados | Hash sem kind no digest | Hash (kind, conteúdo) + dedup + erro em desconhecido | Store como única estrutura mutável, tudo mais congelado |
| **Grafo + render tardia (Parte 2)** | 25% | Não implementados | Texto guardado no grafo | Só hashes no grafo, texto como projeção | root_hash como identidade da lista (iguais indistinguíveis) |
| **Diff (Parte 3)** | 25% | Não implementado | Diff de texto renderizado | Diff por componente com 4 status | Atribuição do cenário completa (3 mudanças + 1 poupada) |
| **Compaction + replay (Parte 3)** | 30% | Não implementados | Compaction reescreve string | Grafo novo + original preservado | Replay com prompt_root idêntico entre modelos — a troca de modelo vira comparação justa |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **O kind entra no hash.** Se `SYSTEM_TUE` como system e como user dessem o mesmo hash, o grafo mentiria sobre a estrutura do prompt. `sha256(kind.value + "\x00" + content)` — o separador evita ambiguidade de concatenação.
2. **Resista à tentação de guardar texto no grafo.** O `PromptGraph` que carrega `str` junto "só pra facilitar o render" volta a ser o textão com passos extras. O texto é projeção: existe no `render()` e em nenhum outro lugar (RT3) — é isso que faz diff, compact e replay operarem em identidade, não em string.
3. **`root_hash` é a identidade da sessão.** Ele é o que a resposta rastreia (RF3) e o que o replay segura (RF6). Se você hashar a lista em ordem diferente e obtiver roots diferentes para o "mesmo" prompt, ótimo: ordem de componente É parte do prompt — o modelo lê em ordem.

---

## ❓ Dúvidas Comuns

**P: O git do prompt-as-code já não versiona isso?**
R: Versiona ARQUIVOS em pontos no tempo (`docs/canonical/prompt-as-code-causal-change-management.md:28`). O content addressing versiona CONTEÚDO por componente, independente de arquivo e de commit: a mesma skill citada em 40 sessões tem o mesmo hash nas 40 — o git te diz o que o repo tinha no deploy X; o grafo te diz o que entrou no contexto da sessão Y (`...classification.md:44`).

**P: Por que isso é "deep rabbit hole"?**
R: Porque exige disciplina de addressing em TODA peça de prompt, sem exceções — uma user message que entra sem hash quebra a reconstrução da sessão inteira (`...patterns.md:59`). O próprio autor do fonte chama assim (`...patterns.md:57`); a classificação repete o custo e ainda assim dá valor High: é o substrato que o replay e a troca de modelo do repo sempre assumiram (`...classification.md:56`).

**P: Compaction aqui é a do Exercício de server-side compaction?**
R: É a mesma operação com substrato diferente. A compaction de `04-server-side-compaction.md` manipula texto/conversa; aqui manipula NÓS do grafo (`...patterns.md:50`): o ganho é que o grafo compactado e o original são ambos reconstruíveis — o corte vira um diff endereçável, não uma reescrita opaca.

**P: Diff por posição não é frágil?**
R: Para o escopo do exercício (componentes ordenados, tamanho estável por kind), posição+kind é suficiente e determinístico. Num sistema real, casaria por (kind, papel semântico) — mas o insight não muda: o diff opera sobre hashes curtos, não sobre o textão; a atribuição "qual componente quebrou o output" é uma tabela, não uma arqueologia.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 2 completo e sua classificação: `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:38-59` e `...classification.md:40-56` — o NOT_FOUND mais explícito do lote e o valor High apesar do "rabbit hole"
2. Conecte ao repo: releia `docs/canonical/stable-harness-prompt.md` e note o que ele EXIGE do replay (versões de prompt/rubric/catalog) vs. o que este exercício FORNECE (o prompt exato reconstruído); o `addressable-memory-catalog` endereça o que ficou DE FORA — este grafo endereça o que ENTROU
3. Escreva o ADO do KODA: qual seria o menor corte content-addressed de valor — tool descriptions (mudam por deploy) ou user messages (mudam por sessão)? Por quê?

---

*Exercício 19 | Nível 3 — Arquitetura Avançada | Content-Addressed Prompt Graph*

**Se você não pode reconstruir o input exato, não pode debugar, nem comparar modelos. Hashe antes de renderizar.**
