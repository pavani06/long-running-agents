---
title: "Exercício 8: Defensive Patch Ledger — o Prompt Como Inventário Depreciável, Não Como Cemitério de Remendos"
type: exercise
level: "N2"
aliases: ["defensive patch ledger", "ledger de patches defensivos", "auditoria de patches na migração de modelo", "rationale at write time", "divida de patches de prompt", "patch debt"]
tags: ["curriculo-conteudo", "nivel-2", "agentes-orquestracao", "harness-engineering", "evals", "governanca", "production"]
relates-to: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|Padrões The Prompting Playbook]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|Classificação The Prompting Playbook]]", "[[docs/canonical/prompt-as-code-causal-change-management|Prompt as Code Causal Change Management]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-07-eval-coverage-matrix|Exercício 7: Eval Coverage Matrix]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-09-two-sided-trade-off-instruction|Exercício 9: Two-Sided Trade-off Instruction]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-22-capability-escalation-ladder|Exercício 22: Capability Escalation Ladder]]"]
duration: "60-90 min"
last_updated: 2026-09-02
---

# 🩹 Exercício 8: Defensive Patch Ledger — o Prompt Como Inventário Depreciável, Não Como Cemitério de Remendos
## Nível 2 — Padrões Práticos

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** (Intermediário)
**Pré-requisito:** Ter lido `03-rubric-design.md` (Nível 2) + `docs/canonical/prompt-as-code-causal-change-management.md` + `docs/canonical/invariant-compensation-split.md`
**Objetivo:** Tratar cada patch defensivo do prompt como um ativo registrado — com trigger, diagnóstico e intenção gravados NO MOMENTO DA ESCRITA — para que a migração de modelo dispare uma AUDITORIA de patches (não só um re-run de evals), classificando cada remendo entre compensação depreciável e invariante que sobrevive

---

## 📖 Prólogo: A Migração Que Passou nos Evals e Estragou o Agente

### Segunda-feira, 10h04. O agente de atendimento do KODA termina a migração para o modelo novo.

```
ENG_LEAD:   "migração verde. Eval suite: 148/150. Os 2 casos
             que regrediram eram variance conhecida — revalidados,
             passaram. Ship."

SUPPORT:    "desde ontem o agente está... estranho. Ele recusa
             dar detalhes de plano que o cliente TEM DIREITO a
             ver. E as respostas chegam com 1,5s a mais. NPS
             caindo nos tickets de reembolso."

PROMPT_OWN: "deixa eu ver o prompt... tem aqui:
             'NUNCA cite condições de plano em texto' — isso
             foi um remendo de 2025-03, quando o modelo antigo
             alucinava condições. E esse Context Loader que
             pré-formata o catálogo antes de cada resposta? Um
             remendo de 2025-06 porque o modelo antigo não
             achava nada no catálogo bruto."

ENG_LEAD:   "e por que ainda estão ligados?"

PROMPT_OWN: "porque ninguém sabe o que cada linha conserta.
             O git blame dessas linhas diz 'fix prompt' —
             commit do estagiário de 2025 que já saiu. O
             modelo novo segue instruções melhor que o antigo:
             ele obedece a proibição COMPLETA em vez de só
             não alucinar. Estamos pagando pelos erros de um
             modelo que já não existe."

ENG_LEAD:   "então a migração passou nos evals porque os evals
             testam o que o agente FAZ — não testam o que o
             prompt CARREGA. A gente re-rodou os evals e
             esqueceu de auditar o inventário."
```

**O custo do ledger inexistente:**

```
╔══════════════════════════════════════════════════════════════════╗
║   MIGRAÇÃO VERDE, PROMPT OBESO — O INVENTÁRIO QUE NINGUÉM TEM      ║
║                                                                  ║
║  Patches defensivos vivos no prompt de atendimento:               ║
║   ✓ ban de detalhes de plano (era: alucinação de condições)       ║
║   ✓ Context Loader de catálogo (era: modelo não achava nada)      ║
║   ✓ reformatação agressiva de resposta (era: verbosidade gen-1)   ║
║   ✓ ... mais 3 que ninguém sabe justificar                        ║
║                                                                  ║
║  Custo visível:                       Custo invisível:            ║
║   +1200 tokens/turno (loader)          comportamento errado por    ║
║   +450ms de latência (loader)          OVER-compliança de bans     ║
║   respostas evasivas (ban)             que o modelo novo cumpre    ║
║                                        na íntegra                 ║
║                                                                  ║
║  "Por que isso existe?" respondida por: git blame → "fix prompt"  ║
║                                                                  ║
║  A regra que faltou: o rationale se registra NA ESCRITA,          ║
║  ou nunca mais (patterns.md:88)                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é patchar.** Patch defensivo é resposta correta a uma falha
real — o prompt-as-code do repo já exige as três perguntas causais em todo
commit (trigger, diagnóstico, intenção — `docs/canonical/prompt-as-code-causal-change-management.md:32-59`).
O problema é que **a metade de decaimento não existe no repo**: compensações
escritas para o modelo antigo viram custo morto quando o modelo melhora
(`docs/canonical/invariant-compensation-split.md:23` — o Context Loader que
continuava custando 450ms e 1200 tokens depois de desnecessário), e nenhuma doc
casa o ledger de rationale com a migração de modelo como **trigger de
auditoria** (`...classification.md:85`, NOT_FOUND: nenhum doc liga patch
ledger a migração). O resultado do prólogo é o padrão exato do fonte: modelos
novos, mais instruction-following, **overfitam** os patches escritos para as
falhas de modelos velhos (`...patterns.md:76`).

**Sua missão:** implementar o `PatchLedger` — cada `PatchEntry` gravado com
trigger, diagnóstico, intenção, era de modelo e custo por turno, recusando
patch sem rationale (`MissingRationaleError`); a classificação
`COMPENSATION` vs `INVARIANT` com o decision test do invariant-compensation
split; e o `audit_on_migration()` — a auditoria que a migração dispara,
cruzando cada patch com a falha que o justificou re-testada no modelo novo,
produzindo vereditos `KEEP` / `RETIRE` / `TRIAL` e o custo recuperado em
tokens e latência.

---

## 🧠 O Contexto

### O Modelo Mental: Rationale na Escrita, Auditoria na Migração, Depreciação na Classificação

O padrão acopla dois canonicals maduros do repo num só procedimento
(`...classification.md:87` — Integration value High):

```
   FALHA OBSERVADA (modelo gen-1)
        │
        ▼
   ┌─────────────────────────────────────────────────────┐
   │  ESCRITA DO PATCH (com discipline do prompt-as-code)│
   │  PatchEntry:                                       │
   │    trigger    = qual incidente/eval regression      │
   │    diagnosis  = qual falha do modelo causou        │
   │    intent     = qual falha este patch endereça     │
   │    model_era  = gen-1                              │
   │    cost       = tokens/latency por turno           │
   │  sem rationale → MissingRationaleError             │
   └───────────────────────┬─────────────────────────────┘
                           │
        MIGRAÇÃO DE MODELO (gen-1 → gen-3)
                           │
                           ▼
   ┌─────────────────────────────────────────────────────┐
   │  AUDITORIA DE PATCHES (não só eval re-run)          │
   │  para cada patch: a falha-trigger ainda reproduz    │
   │  no modelo novo?                                    │
   │                                                     │
   │   reproduz → INVARIANT   → KEEP                     │
   │   não reproduz + compensação → RETIRE (deprecia)   │
   │   incerto → TRIAL (aposenta sob watch de eval)      │
   └─────────────────────────────────────────────────────┘
```

Três propriedades definem o padrão:

1. **O rationale é da escrita ou nunca.** "Discipline cost: the rationale must
   be recorded at write time or never" (`...patterns.md:88`). Reconstituir o
   porquê de um patch seis meses depois é arqueologia — o prólogo mostra o
   resultado: `git blame` diz "fix prompt" e ninguém decide nada. O ledger
   transforma patch debt de **passivo invisível em inventário depreciável**
   (`...patterns.md:84`).

2. **Migração dispara auditoria, não só eval.** O eval-gate canônico decide
   Switch/Hold/Hybrid comparando pass/fail (`docs/canonical/model-switching-architecture-enterprise-eval-gate.md:61-71`)
   — ele testa o que o agente FAZ. A auditoria de patches testa o que o prompt
   CARREGA: quais remendos da era anterior o modelo novo vai overfitar. É o
   acoplamento que falta ao repo (`...classification.md:77`).

3. **O ledger não decide sozinho.** "Does not by itself decide which patches
   are obsolete; audit judgment is still required" (`...patterns.md:89`). O
   decision test vem do invariant-compensation split: "if the failure still
   exists with a better model, it is an invariant candidate"
   (`docs/canonical/invariant-compensation-split.md:67`). Compensação decai
   entre gerações; invariante de domínio sobrevive.

### O Que Você Vai Construir

1. `PatchEntry` — o registro imutável: id, instrução, era de modelo,
   trigger/diagnosis/intent (as três perguntas causais do prompt-as-code),
   classificação `COMPENSATION`/`INVARIANT`, custo por turno
2. `PatchLedger` — o inventário: grava com rationale obrigatório
   (`MissingRationaleError`), responde consultas por era e por classificação
3. `MigrationAudit` / `PatchVerdict` — o procedimento da migração: para cada
   patch, cruzamento com a falha-trigger re-testada no modelo novo, veredito
   `KEEP` / `RETIRE` / `TRIAL`, custo recuperado somado
4. `run_migration_audit()` — o pipeline do prólogo: o prompt com 6 patches de
   3 eras auditado na migração gen-1→gen-3, com os números do Context Loader
   recuperados

---

## 📋 Cenário

O agente de atendimento do KODA, antes da migração para o modelo gen-3. O
prompt de sistema carrega 6 patches defensivos acumulados nas eras gen-1 e
gen-2:

| # | Patch | Era | Trigger original | Custo/turno |
|---|---|---|---|---|
| 1 | ban de citar condições de plano | gen-1 | alucinação de condições inexistentes | 0 tok / 0 ms |
| 2 | Context Loader de catálogo | gen-1 | modelo não localizava itens no catálogo bruto | 1200 tok / 450 ms |
| 3 | reformatação agressiva de resposta | gen-1 | verbosidade extrema do gen-1 | 80 tok / 10 ms |
| 4 | checagem duplicada de PII | gen-2 | falso negativo de PII do gen-2 | 150 tok / 30 ms |
| 5 | aviso de urgência em 2 idiomas | gen-2 | gen-2 ignorava marcadores de urgência | 40 tok / 0 ms |
| 6 | proibição de parafrasear tabela de preços | gen-1 | gen-1 inventava preços ao parafrasear | 0 tok / 0 ms |

Re-teste das falhas-trigger no modelo gen-3 (resultado da auditoria): alucinação
de condições **não reproduz** (gen-3 cita com fidelidade quando permitido);
catálogo bruto **não reproduz** (gen-3 localiza sem pré-formatação); verbosidade
**não reproduz**; falso negativo de PII **ainda reproduz** (falha de domínio,
não de modelo); urgência ignorada **não reproduz**; invenção de preço ao
parafrasear **ainda reproduz** (limite real do modelo com tabelas densas).

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Rationale na escrita:** `PatchLedger.record()` recusa patch sem as
   três respostas causais não vazias (trigger, diagnosis, intent) com
   `MissingRationaleError` nomeando o campo faltante; patch gravado é
   imutável e consultável por id, era e classificação.
2. **RF2 — Classificação explícita:** cada `PatchEntry` carrega
   `kind: COMPENSATION | INVARIANT`; a validação `classify()` aplica o decision
   test canônico — falha que persiste com modelo melhor é candidato a
   invariante, falha de era anterior que sumiu marca compensação
   (`docs/canonical/invariant-compensation-split.md:67`).
3. **RF3 — Custo como atributo de primeira classe:** cada patch carrega
   `token_cost` e `latency_cost_ms` por turno; o ledger expõe
   `carried_cost()` — o preço total que o prompt paga por turno para carregar
   o inventário.
4. **RF4 — Migração dispara auditoria:** `audit_on_migration()` percorre TODO
   patch vivo com o re-teste da falha-trigger no modelo novo e emite um
   `PatchVerdict` por patch — `KEEP` (falha persiste ou invariante de domínio),
   `RETIRE` (compensação cuja falha não reproduz), `TRIAL` (compensação com
   re-teste inconclusivo).
5. **RF5 — Recuperação contabilizada:** a auditoria soma o custo recuperado
   dos vereditos `RETIRE` (tokens e latência por turno) e reporta o inventário
   restante; nenhum veredito altera o `PatchEntry` original — o ledger é
   append-only como o audit trail canônico
   (`docs/canonical/prompt-as-code-causal-change-management.md:98-105`).
6. **RF6 — O pipeline do prólogo:** `run_migration_audit()` reproduz o cenário
   dos 6 patches: 3 `RETIRE` (recuperando 1280 tokens e 460 ms/turno — o
   Context Loader mais os outros dois), 2 `KEEP` (PII e tabela de preços — as
   falhas que persistem), 1 `TRIAL` (urgência bilíngue, re-teste inconclusivo).

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**, patches congelados (imutáveis); simulação
   determinística (sem aleatoriedade, sem I/O)
3. **RT3 — Funções puras de auditoria:** `(ledger, retest) → verdicts`; a
   auditoria nunca muta o ledger
4. **RT4 — Veredito rastreável:** cada `PatchVerdict` carrega o id do patch, a
   decisão, a falha-trigger re-testada e a justificativa citável em uma linha

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                      DEFENSIVE PATCH LEDGER                             │
│                                                                        │
│  ESCRITA (RF1)                        CONSULTA (RF3)                    │
│  PatchEntry(                          ledger.carried_cost()             │
│    id, instruction, model_era,        → 1670 tok / 490 ms por turno     │
│    trigger, diagnosis, intent,                                          │
│    kind, token_cost, latency_ms)      por era / por kind                │
│        │                                       ▲                        │
│        ▼ sem rationale →              ┌────────┴─────────┐              │
│        MissingRationaleError          │  PATCH LEDGER    │              │
│                                        └────────▲─────────┘              │
│  MIGRAÇÃO gen-1/gen-2 → gen-3 (RF4)             │                        │
│  re-teste da falha-trigger por patch            │                        │
│        │                                        │                        │
│        ▼                                        │                        │
│  ┌───────────────────────────────────────────────────────────┐          │
│  │ MigrationAudit — um PatchVerdict por patch                 │          │
│  │                                                            │          │
│  │  REPRODUCES + domain invariant  → KEEP    (PII, preços)    │          │
│  │  gone + COMPENSATION             → RETIRE  (ban, loader,   │          │
│  │                                    reformatação)           │          │
│  │  inconclusive + COMPENSATION      → TRIAL   (urgência)     │          │
│  │                                                            │          │
│     │  recovered: 1280 tok + 460 ms/turno (RF5, RF6)             │          │
│  └───────────────────────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar a migração verde (15 min)

Com o prólogo: por que o eval-gate canônico (Switch/Hold/Hybrid sobre
pass/fail) não podia pegar este incidente? Qual patch o modelo gen-3
"overfitou" e por que instruction-following MELHOR piora o sintoma? Por que
`git blame` é insuficiente como ledger? Responda como comentário, citando o
canonical e a linha do fonte.

### Parte 2 — Ledger com rationale obrigatório (35 min)

Implemente `PatchEntry`, `PatchLedger` com `MissingRationaleError` (RF1),
a classificação com o decision test (RF2) e o custo carregado (RF3).

### Parte 3 — A auditoria da migração (30 min)

Implemente `MigrationAudit.audit_on_migration()` com os três vereditos e o
custo recuperado (RF4-RF5), e `run_migration_audit()` reproduzindo o cenário
dos 6 patches (RF6): 3 RETIRE, 2 KEEP, 1 TRIAL, 1280 tokens e 460 ms
recuperados por turno.

---

## 💻 Starter Code

```python
"""
Exercício 8 — Defensive Patch Ledger
Nível 2 — Padrões Práticos

Cada patch defensivo é um ativo registrado: rationale na escrita,
classificação compensação/invariante, e uma auditoria que a migração
de modelo dispara — não só um re-run de evals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS — o patch como ativo registrado
# ============================================================================

class ModelEra(Enum):
    GEN_1 = "gen-1"   # o modelo que motivou a maioria dos patches
    GEN_2 = "gen-2"
    GEN_3 = "gen-3"   # o modelo novo da migração


class PatchKind(Enum):
    """O decision test do invariant-compensation-split (:67):
    falha que persiste com modelo melhor → INVARIANT;
    falha de era anterior que sumiu → a compensação decai."""
    COMPENSATION = "compensation"  # remendo para fraqueza DE MODELO
    INVARIANT = "invariant"        # proteção para risco DE DOMÍNIO


@dataclass(frozen=True)
class PatchEntry:
    """
    O registro imutável (RF1): as três perguntas causais do
    prompt-as-code-causal-change-management.md:32-59 — por que mudou,
    qual falha causou, qual falha endereça — gravadas NA ESCRITA.
    """
    patch_id: str
    instruction: str          # o texto que vive no prompt
    model_era: ModelEra       # era do modelo que motivou o patch
    trigger: str              # incidente/eval regression observado
    diagnosis: str            # qual falha (do modelo) causou o trigger
    intent: str               # qual falha este patch endereça
    kind: PatchKind
    token_cost: int = 0       # custo por turno por CARREGAR o patch
    latency_cost_ms: int = 0


class MissingRationaleError(Exception):
    """Patch sem rationale não entra no ledger (patterns.md:88)."""


@dataclass
class PatchLedger:
    """O inventário depreciável (RF1, RF3) — append-only."""
    _entries: dict[str, PatchEntry] = field(default_factory=dict)

    def record(self, patch: PatchEntry) -> None:
        """
        Recusa rationale vazio/ausente (trigger, diagnosis, intent) com
        MissingRationaleError nomeando o campo faltante; recusa id
        duplicado. Patch gravado nunca é alterado.
        """
        # TODO: implemente
        raise NotImplementedError

    def entry(self, patch_id: str) -> PatchEntry:
        # TODO: implemente
        raise NotImplementedError

    def by_era(self, era: ModelEra) -> list[PatchEntry]:
        # TODO: implemente
        raise NotImplementedError

    def carried_cost(self) -> tuple[int, int]:
        """(tokens, latency_ms) por turno para carregar TODO o inventário."""
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# A AUDITORIA QUE A MIGRAÇÃO DISPARA
# ============================================================================

class RetestOutcome(Enum):
    """Resultado de re-testar a FALHA-TRIGGER no modelo novo."""
    REPRODUCES = "reproduces"          # a falha ainda existe em gen-3
    GONE = "gone"                      # o modelo novo não tem a falha
    INCONCLUSIVE = "inconclusive"      # sinal misto → precisa de trial


class Verdict(Enum):
    KEEP = "keep"        # falha persiste (ou invariante de domínio)
    RETIRE = "retire"    # compensação depreciada — custo recuperado
    TRIAL = "trial"      # aposentar sob watch de eval (rollback pronto)


@dataclass(frozen=True)
class PatchVerdict:
    """Veredito rastreável (RT4): decisão + falha + justificativa citável."""
    patch_id: str
    verdict: Verdict
    trigger_retested: str     # qual falha foi re-testada
    rationale: str            # uma linha citável


@dataclass
class MigrationAudit:
    """O procedimento da migração (RF4, RF5) — nunca muta o ledger."""
    ledger: PatchLedger
    retest_results: dict[str, RetestOutcome]  # patch_id → re-teste da falha

    def audit_on_migration(self, new_era: ModelEra) -> list[PatchVerdict]:
        """
        Um veredito por patch VIVO (patches da era nova não se auditam
        contra si mesmos):
          - INVARIANT                        → KEEP (domínio não decai)
          - COMPENSATION + REPRODUCES        → KEEP (o remendo ainda segura)
          - COMPENSATION + GONE              → RETIRE (deprecated)
          - COMPENSATION + INCONCLUSIVE      → TRIAL (aposentar com watch)
        """
        # TODO: implemente
        raise NotImplementedError

    def recovered_cost(self, verdicts: list[PatchVerdict]) -> tuple[int, int]:
        """(tokens, latency_ms) por turno recuperados pelos RETIRE (RF5)."""
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# FIXTURES — o prompt de atendimento do KODA antes da migração
# ============================================================================

def build_koda_ledger() -> PatchLedger:
    """6 patches de 3 eras — o inventário do prólogo."""
    ledger = PatchLedger()
    ledger.record(PatchEntry(
        "P1", "NUNCA cite condições de plano em texto", ModelEra.GEN_1,
        trigger="incidente 2025-03: cliente cobrado por condição inexistente",
        diagnosis="gen-1 alucinava condições de plano não contratadas",
        intent="suprimir a fonte de alucinação até o cliente confirmar no painel",
        kind=PatchKind.COMPENSATION,
    ))
    ledger.record(PatchEntry(
        "P2", "Context Loader: pré-formatar catálogo antes de cada resposta",
        ModelEra.GEN_1,
        trigger="eval regression: taxa de item errado 34% em busca de catálogo",
        diagnosis="gen-1 não localizava itens no catálogo bruto (contexto denso)",
        intent="reduzir o problema de localização a um formato pré-digerido",
        kind=PatchKind.COMPENSATION,
        token_cost=1200, latency_cost_ms=450,
    ))
    ledger.record(PatchEntry(
        "P3", "reformatação agressiva: resposta em <= 3 parágrafos", ModelEra.GEN_1,
        trigger="NPS: 'respostas intermináveis' dominava reclamações",
        diagnosis="verbosidade extrema característica do gen-1",
        intent="conter o comprimento da resposta por instrução",
        kind=PatchKind.COMPENSATION,
        token_cost=80, latency_cost_ms=10,
    ))
    ledger.record(PatchEntry(
        "P4", "checagem duplicada de PII antes de qualquer citação", ModelEra.GEN_2,
        trigger="incidente 2026-01: CPF exposto em resposta",
        diagnosis="gen-2 com falso negativo em PII ofuscado; o padrão se repete entre modelos — risco de domínio, não de era",
        intent="barra determinística na fronteira, independente do modelo",
        kind=PatchKind.INVARIANT,
        token_cost=150, latency_cost_ms=30,
    ))
    ledger.record(PatchEntry(
        "P5", "aviso de urgência repetido em pt-BR e en-US", ModelEra.GEN_2,
        trigger="eval: 2/10 casos urgentes tratados como rotineiros",
        diagnosis="gen-2 ignorava marcadores de urgência no meio do turno",
        intent="elevar o salience do marcador duplicando o sinal",
        kind=PatchKind.COMPENSATION,
        token_cost=40, latency_cost_ms=0,
    ))
    ledger.record(PatchEntry(
        "P6", "proibição de parafrasear tabela de preços", ModelEra.GEN_1,
        trigger="incidente 2025-05: preço errado citado em proposta",
        diagnosis="gen-1 inventava valores ao condensar tabelas densas; o limite persiste — modelos atuais ainda erram tabelas densas",
        intent="forçar citação literal ou link em vez de paráfrase",
        kind=PatchKind.INVARIANT,
    ))
    return ledger


def gen3_retest_results() -> dict[str, RetestOutcome]:
    """Re-teste da falha-trigger de cada patch no modelo gen-3 (cenário)."""
    return {
        "P1": RetestOutcome.GONE,          # gen-3 cita com fidelidade
        "P2": RetestOutcome.GONE,          # gen-3 localiza no catálogo bruto
        "P3": RetestOutcome.GONE,          # gen-3 é conciso por padrão
        "P4": RetestOutcome.REPRODUCES,    # PII segue sendo risco de domínio
        "P5": RetestOutcome.INCONCLUSIVE,  # 1/10 urgente escapou no re-teste
        "P6": RetestOutcome.REPRODUCES,    # tabelas densas seguem invenção
    }


# ============================================================================
# PARTE 3 — O PIPELINE DO PRÓLOGO
# ============================================================================

@dataclass
class AuditReport:
    verdicts: list[PatchVerdict] = field(default_factory=list)
    kept: int = 0
    retired: int = 0
    trial: int = 0
    recovered_tokens: int = 0
    recovered_latency_ms: int = 0
    remaining_token_cost: int = 0   # custo do inventário que ficou


def run_migration_audit() -> AuditReport:
    """
    O pipeline completo (RF6): ledger do prólogo + re-testes do gen-3 →
    3 RETIRE (P1, P2, P3), 2 KEEP (P4, P6), 1 TRIAL (P5),
    1280 tokens e 460 ms/turno recuperados, inventário restante 190 tokens.
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# TESTS
# ============================================================================

def test_rationale_enforced_at_write_time():
    ledger = PatchLedger()
    bad = PatchEntry(
        "PX", "instrução qualquer", ModelEra.GEN_1,
        trigger="", diagnosis="d", intent="i",
        kind=PatchKind.COMPENSATION,
    )
    try:
        ledger.record(bad)
        raise AssertionError("sem trigger o ledger deve recusar (RF1)")
    except MissingRationaleError as exc:
        assert "trigger" in str(exc), "a exceção nomeia o campo faltante"
    print("TESTE 1 PASSOU")


def test_carried_cost():
    ledger = build_koda_ledger()
    tokens, ms = ledger.carried_cost()
    assert tokens == 1200 + 80 + 150 + 40, "custo de tokens do inventário (RF3)"
    assert ms == 450 + 10 + 30, "custo de latência do inventário (RF3)"
    print("TESTE 2 PASSOU")


def test_migration_audit_verdicts():
    audit = MigrationAudit(build_koda_ledger(), gen3_retest_results())
    verdicts = audit.audit_on_migration(ModelEra.GEN_3)
    by_id = {v.patch_id: v.verdict for v in verdicts}

    assert by_id["P1"] == Verdict.RETIRE, "falha gone + compensação → RETIRE"
    assert by_id["P2"] == Verdict.RETIRE, "o Context Loader decai (RF4)"
    assert by_id["P3"] == Verdict.RETIRE
    assert by_id["P4"] == Verdict.KEEP, "invariante de domínio → KEEP"
    assert by_id["P5"] == Verdict.TRIAL, "inconclusivo + compensação → TRIAL"
    assert by_id["P6"] == Verdict.KEEP, "falha persiste → KEEP"
    assert all(v.rationale for v in verdicts), "justificativa citável (RT4)"
    # o ledger não foi mutado pela auditoria (RF5)
    assert len(audit.ledger.by_era(ModelEra.GEN_1)) == 4
    print("TESTE 3 PASSOU")


def test_pipeline_reproduces_the_prologue():
    report = run_migration_audit()
    assert report.retired == 3 and report.kept == 2 and report.trial == 1
    assert report.recovered_tokens == 1200 + 80, "tokens recuperados (RF6)"
    assert report.recovered_latency_ms == 450 + 10, "latência recuperada (RF6)"
    assert report.remaining_token_cost == 150 + 40, "sobram P4 (invariante) e P5 (trial)"
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 8: DEFENSIVE PATCH LEDGER")
    print("=" * 60)
    # Descomente após implementar:
    # test_rationale_enforced_at_write_time()
    # test_carried_cost()
    # test_migration_audit_verdicts()
    # test_pipeline_reproduces_the_prologue()
    print("\nTODO: implemente PatchLedger.record/carried_cost,")
    print("MigrationAudit.audit_on_migration/recovered_cost e")
    print("run_migration_audit")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `record()` recusa rationale ausente com `MissingRationaleError` nomeando o campo; patch gravado é imutável (RF1)
- [ ] `carried_cost()` soma 1470 tokens e 490 ms do inventário do fixture (RF3)
- [ ] `audit_on_migration()` produz KEEP/RETIRE/TRIAL conforme (kind × re-teste), com justificativa citável por veredito (RF4, RT4)
- [ ] A auditoria não muta o ledger: os 6 patches seguem lá após o veredito (RF5)
- [ ] `run_migration_audit()` fecha os números do prólogo: 3 RETIRE, 2 KEEP, 1 TRIAL, 1280 tokens e 460 ms recuperados, 190 tokens restantes (RF6)
- [ ] Patches `INVARIANT` nunca recebem RETIRE no seu pipeline — nem com re-teste `GONE` mal atribuído

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Ledger + rationale (Parte 2)** | 25% | Não implementado | Grava sem validar rationale | Três perguntas causais obrigatórias com exceção nomeando o campo | Append-only explícito + consulta por era/kind como fonte do inventário |
| **Classificação (Parte 2)** | 20% | Sem kind | kind decorativo | Decision test compensação/invariante aplicado | Cita o teste canônico (:67) no código ou docstring |
| **Auditoria de migração (Parte 3)** | 35% | Não implementada | Veredito binário keep/retire | Os três vereditos com a matriz kind × re-teste | Justificativa por veredito citável + ledger não mutado como invariante |
| **Pipeline do prólogo (Parte 3)** | 20% | Não roda | Vereditos sem números | Números do fixture fecham (custo recuperado/restante) | Relatório final lê como resposta direta ao incidente do prólogo |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **A matriz do veredito é pequena — escreva ela primeiro.** Duas dimensões só: `kind` (COMPENSATION/INVARIANT) × re-teste (REPRODUCES/GONE/INCONCLUSIVE). INVARIANT → KEEP sempre (domínio não decai com modelo); COMPENSATION × GONE → RETIRE; COMPENSATION × INCONCLUSIVE → TRIAL. Se o seu código tem mais branches que essa matriz, releia o decision test.
2. **`str.strip()` é seu amigo no RF1.** Rationale de string vazia OU de espaços é a mesma ausência. O custo de aceitar rationale fantasma é o prólogo inteiro: um ledger que grava lixo recai em arqueologia de git blame.
3. **RETIRE é um veredito, não uma ação.** O exercício termina no veredito e no custo recuperado — o patch físico sai do prompt num commit de rollback auditável (`docs/canonical/prompt-as-code-causal-change-management.md:80-85`), fora do escopo aqui. "Does not by itself decide which patches are obsolete" — o julgamento continua humano (`...patterns.md:89`).

---

## ❓ Dúvidas Comuns

**P: Isso não é só o prompt-as-code causal change management de novo?**
R: É a metade que falta. O prompt-as-code grava o WHY de cada mudança (`docs/canonical/prompt-as-code-causal-change-management.md:32-59`) — o ledger da racional existe. O que não existe é o frame de decaimento: patches como inventário de uma ERA de modelo, auditoria disparada pela migração, e o cruzamento com o invariant-compensation split para classificar o que decai do que sobrevive (`...classification.md:77,87`).

**P: Por que TRIAL em vez de RETIRE direto no inconclusivo?**
R: Porque o ledger não decide sozinho (`...patterns.md:89`). O re-teste inconclusivo pode ser variance — o fonte do padrão 1 registra que variância natural entre runs imita regressão. TRIAL aposenta o patch com o eval de olho e o rollback pronto; RETIRE definitivo exige o sinal limpo.

**P: O eval-gate da migração não cobre isso?**
R: Não — e essa é a tese do exercício. O gate canônico compara pass/fail do CANDIDATO vs ATUAL e decide Switch/Hold/Hybrid (`docs/canonical/model-switching-architecture-enterprise-eval-gate.md:61-71`). Ele testa o que o agente faz; a auditoria testa o que o prompt carrega. O incidente do prólogo passou pelo gate verde — "model migration triggers a patch audit, not just an eval re-run" (`...patterns.md:85`).

**P: Patch com custo zero (P1, P6) — por que está no ledger?**
R: Porque o custo do patch não é só token. P1 custava zero tokens e era o MAIOR prejuízo do prólogo: over-compliança comportamental (respostas evasivas). O ledger registra o custo mensurável por turno; o custo comportamental aparece no veredito e no trigger.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 4 completo e sua classificação: `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:73-90` e `...classification.md:73-87` — Partial Coverage High: as duas metades existiam em canonicals separados; o acoplamento é o exercício
2. Siga a série: este exercício dá o inventário de patches → [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-09-two-sided-trade-off-instruction|Exercício 9]] neutraliza o patch ban que sobreviveu à auditoria com instrução balanceada → [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-22-capability-escalation-ladder|Exercício 22]] ordena os degraus quando o problema não é patch, é capacidade
3. Aplique ao repo real: o system prompt de 1800+ linhas citado pelo prompt-as-code (`docs/canonical/prompt-as-code-causal-change-management.md:116`) — quantos patches dele teriam rationale reconstituível hoje?

---

*Exercício 8 | Nível 2 — Padrões Práticos | Defensive Patch Ledger*

**O rationale se registra na escrita ou nunca — e a migração audita o inventário, não só o eval.**
