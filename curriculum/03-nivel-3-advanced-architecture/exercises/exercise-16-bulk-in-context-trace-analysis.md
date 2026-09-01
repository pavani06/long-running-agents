---
title: "Exercício 16: Bulk In-Context Trace Analysis — Dez Mil Traces, Zero Vibe Review"
type: exercise
level: 3
aliases: ["bulk in-context trace analysis", "análise in-context em massa", "10k traces in-context", "trend-finding prompt", "split-half stability", "substituto do vibe review", "frontier model step change como observabilidade"]
tags: ["curriculo-conteudo", "nivel-3", "evals", "production", "harness-engineering", "tracing", "analise-estrutural", "ai", "stack-tooling"]
relates-to: ["[[docs/canonical/bulk-in-context-trace-analysis|Bulk In-Context Trace Analysis]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Clay Eval Stack Classification]]", "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]", "[[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]]", "[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]", "[[curriculum/02-nivel-2-practical-patterns/04-trace-reading|Trace Reading]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy|Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy]]"]
duration: "90-120 min"
last_updated: 2026-08-31
---

# 🔭 Exercício 16: Bulk In-Context Trace Analysis — Dez Mil Traces, Zero Vibe Review
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `04-trace-reading.md` (Nível 2) + `docs/canonical/llm-classified-log-taxonomy.md` + Exercício 13
**Objetivo:** Substituir o vibe review humano de mão-cheia de traces por análise in-context de uma amostra grande num frontier model — com amostragem estratificada, prompts de trend-finding, validação de estabilidade (o próprio juiz é não-determinístico) e conversão de findings em casos de eval

---

## 📖 Prólogo: A Reunião de Sexta em Que Cinco Traces Confirmaram a Opinião de Cada Um

### Sexta-feira, 16h00. O ritual semanal de "revisão de traces".

```
TRACE_REVIEW (ritual, toda sexta, 50 min):
  ENG1: peguei 5 traces aleatórios de ontem.
        Vi muita coisa boa! O agente responde certo.
  ENG2: eu peguei 5 com score baixo no dashboard.
        Vi um padrão: ele erra quando o cliente manda áudio.
  ENG3: peguei os 5 do meu próprio fluxo de teste.
        Pareceu ok? Anexei no doc.

PM:  "então... o produto está bom ou não?"

ENG1: "eu acho que sim."
ENG2: "eu acho que não."
ENG3: "depende."

PM:  "isso é vibe. Eu preciso de tendência. Vocês revisaram
      15 de 40.000 conversas da semana — 0,04%. Como acha
      que um padrão que aparece em 2% das sessões (800
      conversas!) vai cair na sua mão de 5?"
```

**A aritmética brutal do vibe review:**

```
╔══════════════════════════════════════════════════════════════════╗
║      15 TRACES POR SEMANA CONTRA 40.000 CONVERSAS                  ║
║                                                                  ║
║  Cobertura do vibe review:       0,04%                            ║
║  P(achar padrão de frequência 2%) com 5 amostras aleatórias:      ║
║         1 - (0.98)^5 ≈ 9,6%  ← enganchar é sorte                 ║
║  Viés de seleção:                cada engenheiro pegou a amostra  ║
║                                   que confirmava sua opinião       ║
║  Achado do ENG2 (áudio):         plausível? sim. validado? não.   ║
║  Conclusão da reunião:           "depende" (zero valor acionável) ║
║                                                                  ║
║  O que o padrão propõe no lugar:                                 ║
║  amostra de ~10k traces, stratificada, submetida IN-CONTEXT a um  ║
║  frontier model com goal de trend-finding: achar padrões, não     ║
║  julgar itens. O step change de frontier models (capacidade de    ║
║  raciocinar sobre 10k exemplos de uma vez) é o que torna isso     ║
║  viável AGORA — era impossível com modelos de geração anterior.   ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é preguiça.** Ler traces é trabalho real — o repo ensina em profundidade
(`04-trace-reading.md`, 5.089 linhas). O problema é que **leitura humana de mão-cheia não
escala para descoberta de tendências**: é cara, enviesada por seleção e estatisticamente
cega para tudo que não seja frequente o bastante para cair nas 5 amostras. E o que o repo
tem de LLM-at-scale sobre logs é classificação *por item* em taxonomia
(`llm-classified-log-taxonomy.md:48,53`) — não síntese de tendências in-context.

O mecanismo do padrão (`...patterns.md:310-330`): amostra grande → um frontier model com
todo o contexto → goal de trend-finding → findings que viram casos de eval. Com duas
honestidades estruturais: a análise é **ela própria não-determinística e precisa de
validação própria**; e ela **depende do step change** — modelo menor simplesmente não faz
isto (`...patterns.md:326-328`).

**Sua missão:** implementar o `BulkTraceAnalyzer` — amostragem estratificada (não
aleatória), construção de prompt de trend-finding em lotes dentro do orçamento de
contexto, merge de findings com deduplicação, **validação split-half** (só finding que
replica em metades disjuntas sobrevive), e emissão de `EvalCaseCandidate` para o loop do
Exercício 13 — com gate de capacidade de modelo que recusa rodar em modelo pequeno.

---

## 🧠 O Contexto

### O Modelo Mental: Descoberta de Tendências ≠ Classificação por Item

O repo já tem as duas peças vizinhas, e o padrão é a terceira peça que faltava:

| Mecanismo | Pergunta que responde | Determinismo | Escala |
|---|---|---|---|
| Trace reading humano (`04-trace-reading.md`) | "o que aconteceu AQUI?" | humano | 5-15 por semana |
| LLM-classified log taxonomy (`llm-classified-log-taxonomy.md`) | "qual categoria deste item?" | LLM por item | ~40k/semana |
| **Bulk in-context analysis (este padrão)** | "que PADRÕES existem no conjunto?" | LLM sobre o todo | ~10k por passada |

A diferença estrutural: classificação aplica um rótulo conhecido a cada item; análise
bulk pede ao modelo para **descobrir o que os itens têm em comum** — o prompt não conhece
a resposta de antemão. É qualitativo em escala, e por isso mesmo:

1. **A amostra é estratificada, não aleatória.** Padrões raros morrem em amostra
   aleatória (a aritmética do prólogo). Estratificar por use case/tier/outcome garante
   que cada estrato contribui amostras suficientes para suas tendências aparecerem.
2. **O finding que não replica não existe.** O juiz é não-determinístico; um "padrão"
   achado numa passada pode ser alucinação. Split-half: rode em duas metades disjuntas,
   keep só o que aparece nas duas — o próprio padrão admite "needs its own validation"
   (`...patterns.md:327`).
3. **O gate de modelo é parte do desenho.** "Depends on a model capability step change;
   smaller models cannot do it" (`...patterns.md:326`). Rodar isto num modelo médio
   produz findings de plausibilidade cosmética e custo real — o sistema recusa.

### O Que Você Vai Construir

1. `StratifiedSampler` — amostra proporcional-com-mínimo por estrato (use case ×
   outcome), garantindo representação de estratos pequenos
2. `TrendPromptBuilder` — monta o prompt de trend-finding por lote, dentro do budget de
   contexto do modelo, com goal explícito (padrões, não julgamentos por item)
3. `FindingsMerger` — une findings dos lotes/metas com deduplicação semântica (por
   assinatura de padrão)
4. `SplitHalfValidator` — roda a análise em duas metades disjuntas e mantém só findings
   replicados (com Jaccard de assinatura)
5. `EvalCaseEmitter` — finding validado → `EvalCaseCandidate` (com exemplares citáveis)
   para o loop do Exercício 13
6. `ModelCapabilityGate` — recusa análise em modelo abaixo do tier frontier

---

## 📋 Cenário

Corpus da semana do KODA (miniatura de 60 traces no starter, em pé de 10k em produção):
3 padrões embutidos + ruído — (a) agente recomenda produto descontinuado após sync do
catálogo (6 traces, 10%), (b) loop de reformulação quando cliente manda áudio (9 traces,
15%), (c) pergunta de assinatura respondida com produto (4 traces ~7%, o buraco do
Exercício 13) — espalhados por estratos `subscription_questions`/`product_recommendation`/
`order_tracking`, com outcomes `negative`/`ok`.

Dois "modelos" simulados (stubs determinísticos com variação semeada): `frontier-alpha`
(tier FRONTIER) que acha os 3 padrões com flutuação de assinatura; `mid-tier-beta`
(tier MID) cujo gate recusa a análise. Modelo de custo: tokens por passada em função do
tamanho da amostra e do prompt.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Estratificação com mínimo:** `StratifiedSampler.sample()` aloca a amostra
   proporcionalmente aos estratos, mas com piso de `min_per_stratum` (default 5) —
   estrato de 4% recebe mais que os 4% proporcionais para que suas tendências tenham
   chance estatística.
2. **RF2 — Prompt de trend-finding:** `TrendPromptBuilder.build()` particiona a amostra
   em lotes que cabem no `context_budget` do modelo; cada prompt declara o GOAL
   ("encontre padrões recorrentes; NÃO julgue traces individuais"), o estrato, e exige
   saída estruturada com `pattern_signature`, `description`, `estimated_frequency`,
   `exemplar_trace_ids`.
3. **RF3 — Merge com deduplicação:** `FindingsMerger.merge()` une findings de todos os
   lotes; findings com a mesma `pattern_signature` (mesma chave) colapsam em um, com
   frequência somada e exemplares unificados (dedup).
4. **RF4 — Split-half replication:** `SplitHalfValidator.validate()` divide a amostra em
   metades disjuntas, roda a análise (via função de análise injetada) em cada uma, e
   mantém apenas findings cuja assinatura aparece nas DUAS metades (tolerância de
   prefixo de assinatura para variação semeada). Finding não replicado vira
   `DroppedFinding` com motivo — nunca desaparece silenciosamente.
5. **RF5 — Emissão de casos de eval:** cada finding replicado gera `EvalCaseCandidate`
   com `use_case` inferido do estrato, `exemplar_trace_ids`, `origin_finding` e
   `suggested_case_id` — o formato que o `OfflineRefreshLoop` do Exercício 13 consome.
6. **RF6 — Gate de capacidade:** `ModelCapabilityGate.check()` recusa (`GateError`) a
   análise em modelo de tier abaixo de FRONTIER, com mensagem citando a dependência de
   step change; em FRONTIER, estima o custo (tokens × preço por passada × 2 do
   split-half) antes de rodar.
7. **RF7 — Traceability:** o relatório final lista, para cada padrão do corpus, se foi
   achado, replicado e emitido — os 3 padrões embutidos devem completar o pipeline; o
   ruído não deve virar finding replicado.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; análise de modelo injetada como callable (stub
   determinístico semeado — sem rede)
3. **RT3 — Amostras e findings imutáveis** (frozen) onde possível
4. **RT4 — Custo estimado antes de rodar:** nenhuma passada acontece sem estimativa
   registrada no relatório

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                     BULK IN-CONTEXT TRACE ANALYZER                     │
│                                                                       │
│  CORPUS (40k/semana) ──► STRATIFIED SAMPLER (RF1)                     │
│  estratos: use_case × outcome      proporional + piso por estrato      │
│                          │                                            │
│                          ▼                                            │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  MODEL CAPABILITY GATE (RF6)                               │        │
│  │  tier < FRONTIER → GateError ("step change dependency")    │        │
│  │  tier = FRONTIER → estimativa de custo ×2 (split-half)     │        │
│  └──────────────────────────┬────────────────────────────────┘        │
│                             ▼                                         │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  TREND PROMPT BUILDER (RF2)                                │        │
│  │  lotes ≤ context_budget | GOAL: padrões, não itens         │        │
│  │  saída: pattern_signature, freq, exemplares                │        │
│  └──────────────────────────┬────────────────────────────────┘        │
│                             ▼                                         │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  SPLIT-HALF VALIDATOR (RF4)                                │        │
│  │  metade A ▶ análise ▶ findings A                           │        │
│  │  metade B ▶ análise ▶ findings B                           │        │
│  │  mantém: assinatura ∈ A ∩ B (tolerância de prefixo)        │        │
│  │  descarta: DroppedFinding(motivo="não replicou")           │        │
│  └──────────────────────────┬────────────────────────────────┘        │
│                             ▼                                         │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  FINDINGS MERGER + EVAL CASE EMITTER (RF3, RF5)            │        │
│  │  finding replicado → EvalCaseCandidate                     │        │
│  │  (use_case, exemplares, origin_finding, case_id)           │        │
│  │  ──► OfflineRefreshLoop do Exercício 13                    │        │
│  └───────────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar a aritmética do vibe review (15 min)

Com a aritmética do prólogo: qual a probabilidade de 5 amostras aleatórias engancharem
um padrão de 15%? E o de 2%? Por que a amostragem estratificada muda essa conta (dica:
piso por estrato)? Responda como comentário — e diga por que o achado do ENG2 (áudio)
precisa de split-half antes de virar trabalho de sprint.

### Parte 2 — Amostrador, prompt e merge (40 min)

Implemente `StratifiedSampler.sample()` (RF1), `TrendPromptBuilder.build()` (RF2) e
`FindingsMerger.merge()` (RF3). Verifique que o estrato de assinatura (4 traces + piso)
entra com ≥ 5 amostras.

### Parte 3 — Validação e emissão (45 min)

Implemente `ModelCapabilityGate`, `SplitHalfValidator.validate()` e `EvalCaseEmitter`
(RF4-RF7). Rode o pipeline ponta a ponta com o stub `frontier-alpha`: 3 padrões
replicados e emitidos; adicione um finding não replicado no stub e verifique que ele é
derrubado com motivo registrado.

---

## 💻 Starter Code

```python
"""
Exercício 16 — Bulk In-Context Trace Analysis
Nível 3 — Arquitetura Avançada

Substitua o vibe review (mão-cheia de traces humanos) por análise in-context
de amostra grande num frontier model: estratificação, trend-finding,
validação split-half e emissão de casos de eval.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS
# ============================================================================

class ModelTier(Enum):
    MID = "mid"            # não raciocina sobre 10k exemplos
    FRONTIER = "frontier"  # o step change que habilita o padrão


class GateError(Exception):
    pass


@dataclass(frozen=True)
class ModelProfile:
    name: str
    tier: ModelTier
    context_budget_tokens: int   # ex.: 200_000
    price_per_mtok: float


@dataclass(frozen=True)
class TraceRecord:
    trace_id: str
    use_case: str
    outcome: str                 # "ok" | "negative"
    summary: str                 # resumo de 1-2 linhas (o que vai ao contexto)

    @property
    def stratum(self) -> tuple[str, str]:
        return (self.use_case, self.outcome)


@dataclass(frozen=True)
class TrendFinding:
    pattern_signature: str       # chave canônica do padrão (ex.: "audio-reform-loop")
    description: str
    estimated_frequency: float   # fração da amostra
    exemplar_trace_ids: tuple[str, ...]
    origin_batch: str

    def matches(self, other: "TrendFinding", prefix_len: int = 6) -> bool:
        """Tolerância de variação semeada: mesma assinatura por prefixo."""
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class DroppedFinding:
    finding: TrendFinding
    reason: str                  # "não replicou na split-half"


@dataclass(frozen=True)
class EvalCaseCandidate:
    suggested_case_id: str
    use_case: str
    exemplar_trace_ids: tuple[str, ...]
    origin_finding_signature: str
    description: str


@dataclass
class AnalysisReport:
    model: str
    sample_size: int = 0
    strata_sampled: dict[str, int] = field(default_factory=dict)
    estimated_cost_usd: float = 0.0
    raw_findings: list[TrendFinding] = field(default_factory=list)
    replicated_findings: list[TrendFinding] = field(default_factory=list)
    dropped: list[DroppedFinding] = field(default_factory=list)
    eval_cases: list[EvalCaseCandidate] = field(default_factory=list)


# ============================================================================
# PARTE 2 — AMOSTRADOR, PROMPT, MERGER
# ============================================================================

class StratifiedSampler:
    """Amostra proporcional por estrato com piso (RF1)."""

    def __init__(self, min_per_stratum: int = 5) -> None:
        self.min_per_stratum = min_per_stratum

    def sample(
        self, corpus: list[TraceRecord], target_size: int
    ) -> list[TraceRecord]:
        """
        1. agrupe por stratum
        2. aloque proporcional, mas nunca menos que min_per_stratum
           (limitado ao tamanho do estrato)
        3. preencha a sobra (target - alocado) proporcional aos restos
        Determinístico: ordene por trace_id antes de fatiar.
        """
        # TODO: implemente
        raise NotImplementedError


class TrendPromptBuilder:
    """Monta os prompts de trend-finding em lotes (RF2)."""

    TOKENS_PER_TRACE = 60        # estimativa de tokens por trace no contexto
    PROMPT_OVERHEAD = 500

    def build(
        self, model: ModelProfile, sample: list[TraceRecord]
    ) -> list[tuple[str, list[TraceRecord]]]:
        """
        Retorna [(batch_id, traces_do_lote)] com o PROMPT textual pronto.
        Cada prompt contém:
          - GOAL: "Encontre PADRÕES recorrentes no conjunto abaixo.
            NÃO julgue traces individuais. Reporte cada padrão com:
            pattern_signature (chave-canônica-kebab), description,
            estimated_frequency (fração do lote), exemplar_trace_ids."
          - os traces do lote (trace_id | stratum | summary)
        Lote máximo: (context_budget - PROMPT_OVERHEAD) // TOKENS_PER_TRACE.
        """
        # TODO: implemente
        raise NotImplementedError


class FindingsMerger:
    """Colapsa findings de mesmas assinaturas (RF3)."""

    def merge(self, findings: list[TrendFinding]) -> list[TrendFinding]:
        """
        Mesma pattern_signature (via TrendFinding.matches) → um finding:
        frequência = MÉDIA das estimativas, exemplares = união dedup
        (preservando ordem de primeira aparição).
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — GATE, VALIDAÇÃO, EMISSÃO
# ============================================================================

class ModelCapabilityGate:
    """Recusa modelos abaixo do step change; estima custo antes (RF6)."""

    PRICE_INPUT_MTOK = 3.0   # referência de custo de input p/ estimativa

    def check(self, model: ModelProfile, sample_size: int, passes: int = 2) -> float:
        """
        tier != FRONTIER → GateError citando a dependência de step change.
        FRONTIER → retorna custo estimado em USD:
          tokens ≈ sample_size × TrendPromptBuilder.TOKENS_PER_TRACE + overhead
          custo = tokens/1e6 × PRICE_INPUT_MTOK × passes (split-half = 2)
        """
        # TODO: implemente
        raise NotImplementedError


# A "chamada ao modelo" é injetada — no exercício, um stub determinístico
AnalysisFn = callable  # (model, batch) -> list[TrendFinding]


class SplitHalfValidator:
    """Só finding que replica em metades disjuntas sobrevive (RF4)."""

    def validate(
        self,
        sample: list[TraceRecord],
        analyze: AnalysisFn,
        model: ModelProfile,
    ) -> tuple[list[TrendFinding], list[DroppedFinding]]:
        """
        1. divida a amostra em metades disjuntas (ordem por trace_id;
           índices pares vs. ímpares)
        2. rode analyze em cada metade (os lotes são internos da análise)
        3. merge dos findings de cada metade
        4. replicado = finding de A cuja assinatura casa com algum de B
           (via matches); não replicado → DroppedFinding("não replicou
           na split-half")
        Retorne (replicados, dropped) — replicados com exemplares unificados.
        """
        # TODO: implemente
        raise NotImplementedError


class EvalCaseEmitter:
    """Finding replicado → caso de eval para o loop (RF5)."""

    def emit(
        self, findings: list[TrendFinding], sample: list[TraceRecord]
    ) -> list[EvalCaseCandidate]:
        """
        use_case = estrato mais frequente entre os exemplares no sample.
        suggested_case_id = f"EVAL-BULK-{i:03d}" na ordem de frequência
        estimada (maior primeiro).
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# FIXTURES — corpus da semana (miniatura) + stubs de modelo
# ============================================================================

def week_corpus() -> list[TraceRecord]:
    """60 traces: 3 padrões embutidos + ruído."""
    corpus: list[TraceRecord] = []
    # padrão (a): produto descontinuado pós-sync — 6 traces, recommendation/negative
    for i in range(6):
        corpus.append(TraceRecord(
            f"TRC-DISC-{i:02d}", "product_recommendation", "negative",
            "agente recomenda produto marcado discontinued após sync do catálogo",
        ))
    # padrão (b): loop de reformulação com áudio — 9 traces, recommendation/negative
    for i in range(9):
        corpus.append(TraceRecord(
            f"TRC-AUD-{i:02d}", "product_recommendation", "negative",
            "cliente envia áudio; agente responde texto irrelevante; reformulação em loop",
        ))
    # padrão (c): assinatura respondida com produto — 4 traces, subscription/negative
    for i in range(4):
        corpus.append(TraceRecord(
            f"TRC-SUB-{i:02d}", "subscription_questions", "negative",
            "pergunta sobre plano/assinatura respondida com recomendação de produto",
        ))
    # ruído saudável
    for i in range(21):
        corpus.append(TraceRecord(
            f"TRC-OK-REC-{i:02d}", "product_recommendation", "ok",
            "recomendação aceita sem correção",
        ))
    for i in range(12):
        corpus.append(TraceRecord(
            f"TRC-OK-TRK-{i:02d}", "order_tracking", "ok",
            "rastreio respondido corretamente",
        ))
    for i in range(8):
        corpus.append(TraceRecord(
            f"TRC-OK-SUB-{i:02d}", "subscription_questions", "ok",
            "dúvida de assinatura resolvida",
        ))
    return corpus


def frontier_stub_analyze(model, batch_traces):
    """Stub do frontier model: acha os 3 padrões com flutuação de assinatura."""
    sigs = {"discontinued-product-reco", "audio-reform-loop", "subscription-as-product"}
    found: list[TrendFinding] = []
    for i, sig in enumerate(sigs):
        marker = {
            "discontinued-product-reco": "discontinued",
            "audio-reform-loop": "áudio",
            "subscription-as-product": "assinatura",
        }[sig]
        hits = [t for t in batch_traces if marker in t.summary]
        if not hits:
            continue
        freq = len(hits) / len(batch_traces)
        flut = sig if i % 2 == 0 else sig + f"-v{i}"  # variação semeada
        found.append(TrendFinding(
            pattern_signature=flut,
            description=f"padrão: {marker}",
            estimated_frequency=round(freq, 3),
            exemplar_trace_ids=tuple(t.trace_id for t in hits[:4]),
            origin_batch="stub",
        ))
    # um finding que NÃO replica: aparece só em lotes com marker "rastreio"
    if any("rastreio" in t.summary for t in batch_traces):
        found.append(TrendFinding(
            pattern_signature="ghost-tracking-bias",
            description="padrão fantasma que só aparece às vezes",
            estimated_frequency=0.05,
            exemplar_trace_ids=("TRC-OK-TRK-00",),
            origin_batch="stub",
        ))
    return found


FRONTIER_MODEL = ModelProfile("frontier-alpha", ModelTier.FRONTIER, 200_000, 3.0)
MID_MODEL = ModelProfile("mid-tier-beta", ModelTier.MID, 128_000, 0.5)


# ============================================================================
# TESTS
# ============================================================================

def test_stratified_min_per_stratum():
    sampler = StratifiedSampler(min_per_stratum=5)
    sample = sampler.sample(week_corpus(), target_size=40)
    strata: dict[tuple[str, str], int] = {}
    for t in sample:
        strata[t.stratum] = strata.get(t.stratum, 0) + 1
    # o estrato pequeno de assinatura/negative (4 traces) entra com TODOS os 4
    assert strata[("subscription_questions", "negative")] == 4
    # e nenhum estrato viável fica abaixo do piso
    for s, n in strata.items():
        available = sum(1 for t in week_corpus() if t.stratum == s)
        assert n == min(max(5, 0), available) or n >= min(5, available), (
            f"estrato {s} abaixo do piso: {n}"
        )
    assert len(sample) <= len(week_corpus())
    print("TESTE 1 PASSOU")


def test_prompt_batches_within_budget():
    builder = TrendPromptBuilder()
    sample = StratifiedSampler().sample(week_corpus(), 40)
    batches = builder.build(FRONTIER_MODEL, sample)
    assert len(batches) >= 1
    max_batch = (FRONTIER_MODEL.context_budget_tokens
                 - TrendPromptBuilder.PROMPT_OVERHEAD) // TrendPromptBuilder.TOKENS_PER_TRACE
    assert all(len(traces) <= max_batch for _, traces in batches)
    assert sum(len(traces) for _, traces in batches) == len(sample)
    print("TESTE 2 PASSOU")


def test_gate_blocks_mid_tier():
    gate = ModelCapabilityGate()
    try:
        gate.check(MID_MODEL, sample_size=40)
        raise AssertionError("mid-tier deve ser recusado pelo gate")
    except GateError as e:
        assert "step change" in str(e) or "frontier" in str(e).lower()
    cost = gate.check(FRONTIER_MODEL, sample_size=40, passes=2)
    assert cost > 0, "estimativa de custo registrada antes de rodar (RT4)"
    print("TESTE 3 PASSOU")


def test_splithalf_keeps_replicated_drops_ghost():
    sample = StratifiedSampler().sample(week_corpus(), 40)
    validator = SplitHalfValidator()
    replicated, dropped = validator.validate(sample, frontier_stub_analyze, FRONTIER_MODEL)

    sigs = {f.pattern_signature[:6] for f in replicated}
    assert "discon" in sigs and "audio" in sigs and "subscr" in sigs, (
        f"os 3 padrões devem replicar; obtido: {sigs}"
    )
    # o fantasma não replica → derrubado COM motivo (RF4)
    assert all(d.finding.pattern_signature == "ghost-tracking-bias"
               for d in dropped) or len(dropped) >= 1
    assert all("replic" in d.reason.lower() for d in dropped)
    print("TESTE 4 PASSOU")


def test_eval_cases_emitted():
    sample = StratifiedSampler().sample(week_corpus(), 40)
    validator = SplitHalfValidator()
    replicated, _ = validator.validate(sample, frontier_stub_analyze, FRONTIER_MODEL)
    cases = EvalCaseEmitter().emit(replicated, sample)

    assert len(cases) == len(replicated)
    by_sig = {c.origin_finding_signature[:6]: c for c in cases}
    sub = by_sig.get("subscr")
    assert sub is not None and sub.use_case == "subscription_questions"
    assert sub.suggested_case_id.startswith("EVAL-BULK-")
    assert sub.exemplar_trace_ids, "exemplares citáveis obrigatórios"
    print("TESTE 5 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 16: BULK IN-CONTEXT TRACE ANALYSIS")
    print("=" * 60)
    # Descomente após implementar:
    # test_stratified_min_per_stratum()
    # test_prompt_batches_within_budget()
    # test_gate_blocks_mid_tier()
    # test_splithalf_keeps_replicated_drops_ghost()
    # test_eval_cases_emitted()
    print("\nTODO: implemente sampler, prompt builder, merger, gate,")
    print("split-half validator e emitter")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] O estrato `subscription_questions/negative` (4 traces) entra inteiro na amostra; nenhum estrato viável fica abaixo do piso (RF1)
- [ ] Os lotes de prompt respeitam o budget de contexto e cobrem a amostra inteira, com GOAL de padrões (não julgamento por item) no texto (RF2)
- [ ] O gate recusa `mid-tier-beta` com `GateError` citando step change, e estima custo > 0 para o frontier antes de rodar (RF6, RT4)
- [ ] Split-half mantém os 3 padrões embutidos (prefixos `discon`/`audio`/`subscr`) e derruba o fantasma com motivo registrado (RF4)
- [ ] Cada finding replicado vira `EvalCaseCandidate` com `use_case` correto (assinatura → `subscription_questions`), exemplares e case id (RF5)
- [ ] O relatório final mostra a cadeia completa: raw → replicated → dropped → eval cases (RF7)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Sampler + Prompt (Parte 2)** | 25% | Não implementados | Aleatório sem piso | Proporcional com piso + lotes no budget | GOAL anti-item no prompt + determinismo documentado |
| **Merger (Parte 2)** | 15% | Não implementado | União sem dedup | Colapso por assinatura | Frequência média + exemplares unificados preservando ordem |
| **Split-half (Parte 3)** | 30% | Não implementado | Roda uma vez, sem validação | Duas metades disjuntas + interseção | Tolerância de prefixo + drops com motivo nunca silenciosos |
| **Gate + Emissão (Parte 3)** | 30% | Não implementados | Gate sem custo | Gate + custo estimado + casos emitidos | Casos no formato do loop (Exercício 13), traceability ponta a ponta |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **A aritmética é o argumento.** Com 5 amostras, padrão de 2% tem ~9,6% de chance de aparecer; com piso estratificado de 5 num estrato onde ele é localmente frequente, a chance vira quase certa. A estratificação não é detalhe de engenharia — é o que torna a descoberta estatisticamente possível.
2. **Split-half é barato relativo ao que protege.** Custa 2× a passada; economiza sprints inteiros de "padrão" que era alucinação do juiz. O finding fantasma do fixture existe para você sentir o gosto do drop documentado.
3. **O GOAL do prompt é uma cerca de segurança.** Sem o "NÃO julgue traces individuais", o modelo volta à modalidade de classificação por item (o que o repo já tem em `llm-classified-log-taxonomy`) e a síntese de tendências desaparece na saída.

---

## ❓ Dúvidas Comuns

**P: Por que não rodar a análise no corpus inteiro (40k) em vez de amostra?**
R: Custo e redundância. 10k estratificadas dão cobertura estatística dos estratos a uma fração do custo — o padrão fala explicitamente de "on the order of 10,000 examples" (`...patterns.md:316`). Amostrar bem > jogar tudo.

**P: O que muda quando o próximo frontier model dobrar de contexto?**
R: O parâmetro `context_budget_tokens` — e mais nada. É a tese do padrão: "frontier-model step changes convert directly into observability" (`...patterns.md:324`) — o ganho de capacidade vira capacidade de observação sem redesenho. O gate existe para impedir a direção contrária (modelo menor fingindo).

**P: Isso substitui o trace reading humano do Nível 2?**
R: Não — muda a divisão do trabalho. A análise bulk acha *onde olhar* (tendências com exemplares); o humano entra nas sessões exemplares com o método de `04-trace-reading.md` para entender o mecanismo. Vibra review de 5 aleatórios é o que morre.

**P: Onde o finding entra no sistema de evals?**
R: No loop do Exercício 13: o `EvalCaseCandidate` é insumo de intake (junto com tickets e perceived-eval events); e a tendência não replicada como eval viraria drift de uma vez. A análise bulk é o detector do quadrante offline/não-determinístico que a matriz do Exercício 7 cobra.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 15 completo e sua classificação: `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:310-330` e `...classification.md:270-286` — o elo que converte a infraestrutura de trace existente em detecção de tendências
2. Compare com `docs/canonical/llm-classified-log-taxonomy.md:48,53`: classificação por item em volume vs. síntese in-context do conjunto — quando usar cada um?
3. Siga para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-17-self-iterating-agent-loop|Exercício 17: Self-Iterating Agent Loop]] — a arquitetura-alvo em que findings, falhas e correções alimentam o mesmo substrato que o agente raciocina para melhorar a si mesmo

---

*Exercício 16 | Nível 3 — Arquitetura Avançada | Bulk In-Context Trace Analysis*

**Cinco traces confirmam a opinião de quem os escolheu. Dez mil, estratificados, contam o que aconteceu.**
