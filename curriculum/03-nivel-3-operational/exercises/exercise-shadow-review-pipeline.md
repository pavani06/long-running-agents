---
title: "Exercício 7: Construir um Shadow Review Pipeline com Métricas de Concordância"
type: curriculum-exercise
nivel: 3
aliases: ["shadow review pipeline", "AI review shadow mode", "métricas de concordância", "graduação de reviewer automático", "confiança em AI code review"]
tags: [curriculo-conteudo, nivel-3, exercicio, agentic-coding, evals, governanca, shadow-review, trust-calibration, agreement-metrics, false-positive-analysis, gate-graduation, python, dataclass, json-state]
relates-to: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"]
duration: "90-120 min"
last_updated: 2026-06-14
---
# 👥 Exercício 7: Construir um Shadow Review Pipeline com Métricas de Concordância
## Nível 3 — Operacional

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter lido `eval-tier-stratification.md`, `pr-gated-eval-enforcement.md`, e os patterns do Canary Test Code Review
**Objetivo:** Implementar um shadow review pipeline que executa um AI reviewer em modo não-bloqueante, coleta métricas de concordância contra revisões humanas, e decide quais checks podem graduar para blocking status com base em thresholds de confiança

---

## 📖 Prólogo: O Gate Que Bloqueou Tudo

**Quarta-feira, 10h30. Sala de guerra do time de plataforma.**

O AI Code Reviewer estava em produção há três dias como gate bloqueante em todos os PRs. A decisão foi tomada numa sexta-feira às 17h45, depois de uma demo impressionante. O diretor de engenharia viu o bot detectar um `NoneType error` que dois seniors tinham deixado passar e decidiu: "Isso é bom demais para ficar como sugestão. Ativa como bloqueante."

A primeira segunda-feira foi... reveladora.

```
═══════════════════════════════════════════════════════════════
           RELATÓRIO DE INCIDENTE — 72 HORAS DE GATE
═══════════════════════════════════════════════════════════════

PRs SUBMETIDOS:     142
PRs BLOQUEADOS:      89  (63%)
BLOQUEIOS CORRETOS:  17  (19% dos bloqueios)
BLOQUEIOS INCORRETOS:72  (81% dos bloqueios — falsos positivos)

TEMPO MÉDIO DE DESBLOQUEIO: 4.2 horas
PRs ABANDONADOS:            6  (time desistiu e fez workaround)
ESCALAÇÕES PARA O TIME:     41 mensagens no Slack pedindo override
═══════════════════════════════════════════════════════════════
```

O post-mortem revelou o óbvio que ninguém quis admitir na sexta-feira: o bot era promissor, mas ninguém sabia qual era sua taxa de acerto nas condições reais do repositório. Ele foi treinado em código open-source; o repositório da empresa tinha convenções próprias, padrões de erro diferentes, e um monolito com 12 anos de decisões questionáveis que o bot interpretava como bugs.

```
Dev Senior: "A intenção era boa. Mas a gente trocou 'review humano que 
            demora 6 horas' por 'review de bot que demora 4 horas para 
            desbloquear'. O ganho foi negativo."

Tech Lead: "O problema não é o bot. O problema é que a gente não tem 
           a menor ideia de quantos dos bloqueios dele são reais e 
           quantos são ruído. A gente ativou o gate sem shadow period."

Dev Ops: "Shadow period? Tipo canary deployment, mas para reviewer?"

Tech Lead: "Exatamente. Roda o bot em paralelo com o review humano por 
           4 semanas. Não bloqueia nada. Só coleta: o que o bot achou, 
           o que o humano achou, onde concordaram, onde discordaram. 
           No final das 4 semanas, a gente SABE se o bot é confiável. 
           Não acha. Não espera. Sabe."
```

O time implementou o shadow period em duas semanas. Os números que saíram:

```
═══════════════════════════════════════════════════════════════
        SHADOW REVIEW REPORT — PERÍODO: 4 SEMANAS (920 PRs)
═══════════════════════════════════════════════════════════════

CONCORDÂNCIA TOTAL:      78%
TRUE POSITIVES:          214  (achados do bot que o humano concordou)
FALSE POSITIVES:          89  (achados do bot que o humano rejeitou)
MISSED BY AI:             47  (problemas que o humano achou e o bot não)
MISSED BY HUMAN:          31  (problemas que o bot achou e o humano não)

CHECKS QUE PODEM GRADUAR (>90% precision):
  ✅ null-safety-check:       96% precision, 3% recall loss
  ✅ sql-injection-pattern:   99% precision, 0% recall loss

CHECKS QUE PRECISAM DE MAIS SHADOW (70-90% precision):
  ⚠️ naming-convention:       82% precision — muito ruído, time irritado
  ⚠️ error-handling-gap:      74% precision — contexto-dependente

CHECKS QUE NÃO DEVEM BLOQUEAR (<70% precision):
  ❌ architecture-concern:    31% precision — o bot não entende o monolito
  ❌ performance-regression:  45% precision — falsos positivos massivos
═══════════════════════════════════════════════════════════════
```

Com esses dados, o time ativou apenas 2 checks como bloqueantes. Os outros ficaram como sugestões não-bloqueantes ou foram desativados. O resultado: zero PRs abandonados, zero mensagens de override no Slack, e `null-safety-check` já preveniu 3 bugs em produção no primeiro mês.

**A diferença entre "desastre" e "sucesso" não foi o modelo. Foi o shadow period.**

Neste exercício, você vai construir exatamente esse pipeline.

---

## 🎯 Objetivo

Você vai implementar um **Shadow Review Pipeline** que:

1. Executa um AI reviewer em modo não-bloqueante (shadow) ao lado de revisões humanas
2. Classifica cada finding do AI reviewer em categorias de concordância: `true_positive`, `false_positive`, `missed_by_ai`, `missed_by_human`
3. Acumula métricas de precision e recall por categoria de check
4. Implementa um algoritmo de graduação que decide quais checks estão prontos para migrar de shadow → blocking
5. Produz um dashboard state file em JSON com os resultados do shadow period
6. Simula a decisão de graduação baseada em thresholds configuráveis

**Resultado Final:** Você entenderá na prática por que shadow pipelines são o pré-requisito para AI review gates confiáveis, e como transformar "acho que o bot é bom" em "sei que o bot é bom para estes 3 checks específicos".

---

## 📋 Cenário

### O Repositório

Você trabalha no time de plataforma do **MercuryPay**, um sistema de pagamentos com 8 anos de código. O repositório tem convenções próprias, um ORM customizado, e padrões de erro que não existem em nenhum projeto open-source.

O time acabou de integrar um AI Code Reviewer. Ele analisa diffs e produz findings classificados por categoria:

| Check Category | O que verifica |
|---|---|
| `null-safety` | Acesso a atributos sem null-check prévio |
| `sql-injection` | Strings interpoladas em queries SQL |
| `error-handling` | Exceções não tratadas em boundaries de API |
| `naming-convention` | Nomes de variável fora do padrão MercuryPay |
| `architecture` | Violações de dependência entre módulos |
| `performance` | Loops aninhados, queries N+1, alocações excessivas |

### O Problema

O AI reviewer nunca rodou no código do MercuryPay. Ninguém sabe se ele entende as convenções do time. Ativar como gate bloqueante sem dados de concordância é a receita para o desastre do prólogo.

### Sua Missão

Construir o shadow pipeline. Rodar o bot em modo não-bloqueante por um período simulado. Coletar métricas. Decidir com dados quais checks merecem ser bloqueantes.

### Dados de Entrada

Você recebe um arquivo de simulação com 50 PRs. Cada PR contém:

```json
{
  "pr_id": "PR-0042",
  "author": "alice_chen",
  "files_changed": ["src/payment/gateway.py", "src/payment/refund.py"],
  "human_review_outcome": {
    "approved": true,
    "comments": [
      {"file": "src/payment/gateway.py", "line": 142, "severity": "high",
       "message": "Missing null check on payment_method before calling .validate()",
       "category": "null-safety"},
      {"file": "src/payment/refund.py", "line": 88, "severity": "medium",
       "message": "Exception from process_refund() not caught at API boundary",
       "category": "error-handling"}
    ]
  },
  "ai_reviewer_output": {
    "findings": [
      {"file": "src/payment/gateway.py", "line": 142, "severity": "high",
       "check": "null-safety",
       "message": "payment_method may be None. Add guard before .validate()"},
      {"file": "src/payment/gateway.py", "line": 156, "severity": "medium",
       "check": "naming-convention",
       "message": "Variable 'pmt' should be 'payment' per MercuryPay conventions"},
      {"file": "src/payment/refund.py", "line": 88, "severity": "high",
       "check": "error-handling",
       "message": "Unhandled exception in process_refund()"},
      {"file": "src/payment/gateway.py", "line": 200, "severity": "low",
       "check": "architecture",
       "message": "Gateway module should not import from src/legacy/utils"}
    ]
  }
}
```

---

## 📋 Requisitos

### Funcionais

- [ ] Pipeline lê um arquivo JSON com PRs simulados (human review + AI review output)
- [ ] Para cada PR, o sistema classifica cada finding do AI reviewer em uma categoria de concordância
- [ ] Categorias de concordância: `true_positive`, `false_positive`, `missed_by_ai`, `missed_by_human`
- [ ] Métricas são acumuladas por check category (`null-safety`, `sql-injection`, etc.)
- [ ] Para cada check category, o sistema calcula: `total_findings`, `true_positives`, `false_positives`, `precision`, `recall`, `f1_score`
- [ ] Sistema aplica thresholds configuráveis para decidir graduação: `min_precision` (default 0.90), `min_recall` (default 0.70)
- [ ] Output: relatório de graduação com decisão por check category (`graduate_to_blocking`, `needs_more_shadow`, `do_not_block`)
- [ ] Estado do shadow period é persistido em arquivo JSON (`shadow_state.json`)
- [ ] Pipeline suporta acumulação incremental (executar mais PRs no mesmo shadow period)

### Técnicos

- [ ] Python 3.9+ (type hints nativos, `from __future__ import annotations` opcional)
- [ ] Usar apenas biblioteca padrão (`json`, `pathlib`, `datetime`, `dataclasses`, `typing`, `collections`)
- [ ] NÃO usar frameworks externos (numpy, pandas, Flask)
- [ ] Dataclasses para todos os modelos de dados
- [ ] Funções puras para classificação e cálculo de métricas
- [ ] Type hints em todas as funções públicas
- [ ] Docstrings no formato Google-style

### Validação

- [ ] Cenário 1 (shadow run): 50 PRs processados, métricas calculadas por categoria
- [ ] Cenário 2 (graduação): check com precision 96% e recall 94% → `graduate_to_blocking`
- [ ] Cenário 3 (mais shadow): check com precision 82% e recall 80% → `needs_more_shadow`
- [ ] Cenário 4 (não bloquear): check com precision 45% e recall 30% → `do_not_block`
- [ ] Cenário 5 (incremental): adicionar 20 PRs a um shadow period existente e recalcular
- [ ] Cenário 6 (missed by human): findings do bot que o humano não viu são contados como `missed_by_human`

---

## 🚀 Starter Code

```python
"""
Exercicio 7 — Shadow Review Pipeline com Metricas de Concordancia
Nivel 3 — Operacional

Implemente um pipeline que executa um AI reviewer em shadow mode,
classifica findings por concordancia com revisao humana, e decide
quais checks podem graduar para blocking status.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Finding:
    """Um finding individual de um reviewer (humano ou AI)."""
    file: str
    line: int
    severity: str          # "high", "medium", "low"
    category: str          # check category (ex: "null-safety")
    message: str


@dataclass
class HumanReview:
    """Revisao humana de um PR."""
    approved: bool
    comments: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AIReview:
    """Output do AI reviewer para um PR."""
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PRRecord:
    """Um PR completo com revisao humana e output do AI reviewer."""
    pr_id: str
    author: str
    files_changed: list[str] = field(default_factory=list)
    human_review_outcome: dict[str, Any] = field(default_factory=dict)
    ai_reviewer_output: dict[str, Any] = field(default_factory=dict)


# Categorias de concordancia
class AgreementCategory:
    """Classificacao de concordancia entre AI e revisao humana."""
    TRUE_POSITIVE = "true_positive"    # AI achou, humano concordou
    FALSE_POSITIVE = "false_positive"   # AI achou, humano rejeitou/ignorou
    MISSED_BY_AI = "missed_by_ai"       # Humano achou, AI nao achou
    MISSED_BY_HUMAN = "missed_by_human"  # AI achou, humano nao viu


# Decisoes de graduacao
class GraduationDecision:
    """Decisao sobre se um check pode migrar de shadow para blocking."""
    GRADUATE_TO_BLOCKING = "graduate_to_blocking"
    NEEDS_MORE_SHADOW = "needs_more_shadow"
    DO_NOT_BLOCK = "do_not_block"


@dataclass
class CategoryMetrics:
    """Metricas acumuladas para uma categoria de check."""
    category: str
    total_ai_findings: int = 0
    true_positives: int = 0
    false_positives: int = 0
    missed_by_ai: int = 0         # findings do humano que o AI nao encontrou
    missed_by_human: int = 0      # findings do AI que o humano nao encontrou
    total_prs_processed: int = 0
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def precision(self) -> float:
        """
        Precision = true_positives / (true_positives + false_positives).

        Quantos dos achados do AI eram realmente problemas?

        Returns:
            Float entre 0.0 e 1.0, ou 1.0 se nao houver achados.
        """
        # TODO: Implementar calculo de precision
        # Se denominador zero, retornar 1.0 (nao fez achados = nao causou ruido)
        pass

    @property
    def recall(self) -> float:
        """
        Recall = true_positives / (true_positives + missed_by_ai).

        Quantos dos problemas reais o AI conseguiu encontrar?

        Returns:
            Float entre 0.0 e 1.0, ou 1.0 se nao houver problemas para encontrar.
        """
        # TODO: Implementar calculo de recall
        pass

    @property
    def f1_score(self) -> float:
        """
        F1 = 2 * (precision * recall) / (precision + recall).
        Media harmonica de precision e recall.

        Returns:
            Float entre 0.0 e 1.0.
        """
        # TODO: Implementar calculo de F1
        pass


@dataclass
class ShadowState:
    """Estado completo do shadow review period."""
    schema_version: str = "1.0"
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_prs_processed: int = 0
    pr_ids_processed: list[str] = field(default_factory=list)
    category_metrics: dict[str, dict[str, Any]] = field(default_factory=dict)
    graduation_thresholds: dict[str, float] = field(default_factory=lambda: {
        "min_precision": 0.90,
        "min_recall": 0.70,
    })


@dataclass
class GraduationReport:
    """Relatorio de graduacao: quais checks podem migrar para blocking."""
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    thresholds_applied: dict[str, float] = field(default_factory=dict)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=lambda: {
        "graduate_to_blocking": 0,
        "needs_more_shadow": 0,
        "do_not_block": 0,
    })


# ============================================================================
# SIMULATED DATA — 5 PRs de exemplo (o arquivo completo teria 50+)
# ============================================================================

def load_simulated_prs() -> list[PRRecord]:
    """
    Carrega PRs simulados para o shadow period.

    Em producao, estes dados viriam de uma API de PR (GitHub, GitLab)
    combinada com uma ferramenta de AI review.

    Returns:
        Lista de PRRecord com revisoes humanas e outputs do AI reviewer.
    """
    raw = [
        {
            "pr_id": "PR-0001",
            "author": "david_kim",
            "files_changed": ["src/auth/login.py"],
            "human_review_outcome": {
                "approved": True,
                "comments": [
                    {"file": "src/auth/login.py", "line": 45, "severity": "high",
                     "category": "null-safety",
                     "message": "user_db.fetch() pode retornar None — sem null-check antes de .verify_password()"},
                ]
            },
            "ai_reviewer_output": {
                "findings": [
                    {"file": "src/auth/login.py", "line": 45, "severity": "high",
                     "check": "null-safety",
                     "message": "Unchecked None from fetch(). Add guard before attribute access."},
                ]
            }
        },
        {
            "pr_id": "PR-0002",
            "author": "maria_silva",
            "files_changed": ["src/db/queries.py"],
            "human_review_outcome": {
                "approved": True,
                "comments": [
                    {"file": "src/db/queries.py", "line": 120, "severity": "critical",
                     "category": "sql-injection",
                     "message": "String interpolation em query SQL — usar parametrized queries"},
                ]
            },
            "ai_reviewer_output": {
                "findings": [
                    {"file": "src/db/queries.py", "line": 120, "severity": "critical",
                     "check": "sql-injection",
                     "message": "SQL injection risk: string formatting in query"},
                    {"file": "src/db/queries.py", "line": 78, "severity": "low",
                     "check": "naming-convention",
                     "message": "Variable 'q' should be 'query' per MercuryPay conventions"},
                ]
            }
        },
        {
            "pr_id": "PR-0003",
            "author": "james_wilson",
            "files_changed": ["src/api/handlers.py"],
            "human_review_outcome": {
                "approved": False,
                "comments": [
                    {"file": "src/api/handlers.py", "line": 210, "severity": "high",
                     "category": "error-handling",
                     "message": "process_payment() pode lancar PaymentError — nao ha try/except"},
                ]
            },
            "ai_reviewer_output": {
                "findings": [
                    {"file": "src/api/handlers.py", "line": 210, "severity": "high",
                     "check": "error-handling",
                     "message": "Unhandled exception in process_payment(). Wrap in try/except."},
                    {"file": "src/api/handlers.py", "line": 250, "severity": "low",
                     "check": "architecture",
                     "message": "Handler module should not import from src/legacy/payment"},
                ]
            }
        },
        {
            "pr_id": "PR-0004",
            "author": "lisa_park",
            "files_changed": ["src/payment/refund.py"],
            "human_review_outcome": {
                "approved": True,
                "comments": []  # Nenhum problema encontrado pelo humano
            },
            "ai_reviewer_output": {
                "findings": [
                    {"file": "src/payment/refund.py", "line": 55, "severity": "medium",
                     "check": "naming-convention",
                     "message": "Variable 'ref_amt' should be 'refund_amount' per MercuryPay conventions"},
                    {"file": "src/payment/refund.py", "line": 102, "severity": "low",
                     "check": "architecture",
                     "message": "Refund module should not import from src/legacy/audit"},
                ]
            }
        },
        {
            "pr_id": "PR-0005",
            "author": "omar_hassan",
            "files_changed": ["src/reports/generator.py"],
            "human_review_outcome": {
                "approved": True,
                "comments": [
                    {"file": "src/reports/generator.py", "line": 33, "severity": "high",
                     "category": "sql-injection",
                     "message": "report_query usa f-string com input do usuario"},
                    {"file": "src/reports/generator.py", "line": 67, "severity": "medium",
                     "category": "null-safety",
                     "message": "config.get('template') pode retornar None — sem fallback"},
                ]
            },
            "ai_reviewer_output": {
                "findings": [
                    {"file": "src/reports/generator.py", "line": 33, "severity": "high",
                     "check": "sql-injection",
                     "message": "User input interpolated in SQL string — injection risk"},
                    {"file": "src/reports/generator.py", "line": 200, "severity": "low",
                     "check": "performance",
                     "message": "Nested loop over report_data — O(n^2), consider using index"},
                ]
            }
        },
    ]
    return [PRRecord(**item) for item in raw]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def write_json(filepath: Path, data: Any) -> Path:
    """
    Escreve dados em arquivo JSON de forma atomica.

    Args:
        filepath: Caminho completo do arquivo.
        data: Dados a serializar (dict ou dataclass).

    Returns:
        Path do arquivo escrito.
    """
    # TODO: Implementar escrita atomica com arquivo temporario
    # 1. Converter dataclass para dict (usar asdict se disponivel)
    # 2. Criar diretorios pais se necessario
    # 3. Escrever em arquivo .tmp primeiro
    # 4. Renomear .tmp para o nome final
    pass


def read_json(filepath: Path) -> dict[str, Any]:
    """
    Le arquivo JSON e retorna como dicionario.

    Args:
        filepath: Caminho completo do arquivo JSON.

    Returns:
        Dicionario com os dados do arquivo.
    """
    # TODO: Implementar leitura de arquivo JSON
    pass


# ============================================================================
# CORE: FINDING MATCHING
# ============================================================================

def findings_match(
    ai_finding: dict[str, Any],
    human_comment: dict[str, Any],
) -> bool:
    """
    Determina se um finding do AI e um comment do humano referem-se ao mesmo problema.

    Estrategia de matching (simplificada para o exercicio):
    1. Mesmo arquivo (file)
    2. Mesma categoria (category/check)
    3. Linhas proximas (+/- 5 linhas) — ou mesma linha exata se ambos tem line

    Em producao, usaria embedding similarity ou LLM para semantic matching.
    Para este exercicio, matching deterministico e suficiente.

    Args:
        ai_finding: Finding do AI reviewer (com 'file', 'line', 'check').
        human_comment: Comment do humano (com 'file', 'line', 'category').

    Returns:
        True se os findings referem-se ao mesmo problema.
    """
    # TODO: Implementar logica de matching
    # 1. Verificar mesmo arquivo (case-insensitive)
    # 2. Verificar mesma categoria (normalizar: 'check' no AI, 'category' no humano)
    # 3. Verificar proximidade de linha (|ai.line - human.line| <= 5)
    #    - Se algum nao tem line, tentar matching por mensagem (substring)
    pass


# ============================================================================
# CORE: AGREEMENT CLASSIFICATION
# ============================================================================

def classify_pr_findings(
    pr: PRRecord,
) -> dict[str, list[dict[str, Any]]]:
    """
    Classifica cada finding do AI reviewer em uma categoria de concordancia.

    Algoritmo:
    1. Para cada finding do AI, tenta encontrar um comment humano correspondente
       usando findings_match().
    2. Se encontrou match: classifica como true_positive
    3. Se nao encontrou match: classifica como false_positive
       (AI achou algo que o humano nao considerou problema)
    4. Para cada comment humano que NAO teve match com AI:
       classifica como missed_by_ai
    5. Opcional: findings do AI que o humano nao encontrou mas que sao
       confirmados como reais posteriormente → missed_by_human.
       Neste exercicio, missed_by_human e um subconjunto de false_positive
       que foi confirmado como relevante a posteriori (simulado).

    Args:
        pr: PRRecord com revisao humana e output do AI.

    Returns:
        Dict com listas de findings classificados por categoria:
        {
            "true_positive": [...],
            "false_positive": [...],
            "missed_by_ai": [...],
            "missed_by_human": [...]
        }
    """
    # TODO: Implementar classificacao de concordancia
    #
    # Algoritmo sugerido:
    # 1. Extrair ai_findings de pr.ai_reviewer_output["findings"]
    # 2. Extrair human_comments de pr.human_review_outcome["comments"]
    # 3. Inicializar matched_ai = set(), matched_human = set()
    #
    # 4. Para cada (i, ai_finding): para cada (j, human_comment):
    #       se findings_match(ai_finding, human_comment):
    #           classificar como true_positive
    #           matched_ai.add(i), matched_human.add(j)
    #           break
    #
    # 5. AI findings nao matched → false_positive
    #    (Podem ser missed_by_human se confirmados como relevantes —
    #     neste exercicio, simulamos: um subset aleatorio ou baseado em
    #     severidade high e um flag simulated_missed_by_human no finding)
    #
    # 6. Human comments nao matched → missed_by_ai
    #
    # 7. Retornar dict com as quatro listas
    pass


# ============================================================================
# CORE: METRICS ACCUMULATION
# ============================================================================

def accumulate_metrics(
    state: ShadowState,
    classification: dict[str, list[dict[str, Any]]],
    pr_id: str,
) -> ShadowState:
    """
    Acumula metricas de um PR no estado do shadow period.

    Atualiza CategoryMetrics para cada check category encontrada nos findings.

    Args:
        state: Estado atual do shadow period.
        classification: Resultado de classify_pr_findings() para este PR.
        pr_id: ID do PR processado (para deduplicacao).

    Returns:
        ShadowState atualizado com metricas do PR.
    """
    # TODO: Implementar acumulacao de metricas
    #
    # Algoritmo sugerido:
    # 1. Verificar se pr_id ja esta em state.pr_ids_processed
    #    Se sim, retornar state sem modificar (evitar contagem dupla)
    #
    # 2. Para CADA finding nas 4 categorias, extrair a check category:
    #    - true_positive: category do AI finding
    #    - false_positive: category do AI finding
    #    - missed_by_ai: category do human comment
    #    - missed_by_human: category do AI finding
    #
    # 3. Para cada check category encontrada, inicializar ou atualizar
    #    CategoryMetrics no state.category_metrics dict
    #
    # 4. Incrementar contadores:
    #    - total_ai_findings += 1 para cada TP + FP + MH
    #    - true_positives += 1 para cada TP
    #    - false_positives += 1 para cada FP
    #    - missed_by_ai += 1 para cada MA
    #    - missed_by_human += 1 para cada MH
    #
    # 5. Adicionar pr_id em state.pr_ids_processed
    # 6. Incrementar state.total_prs_processed
    # 7. Atualizar state.updated_at
    # 8. Retornar state
    pass


# ============================================================================
# CORE: GRADUATION DECISION
# ============================================================================

def decide_graduation(
    metrics: CategoryMetrics,
    thresholds: dict[str, float],
) -> str:
    """
    Decide se um check category pode graduar de shadow para blocking.

    Regras de decisao:
    - precision >= min_precision E recall >= min_recall → GRADUATE_TO_BLOCKING
    - precision >= 0.70 E recall >= 0.50 → NEEDS_MORE_SHADOW
    - Caso contrario → DO_NOT_BLOCK

    Args:
        metrics: Metricas acumuladas para uma categoria.
        thresholds: Dict com 'min_precision' e 'min_recall'.

    Returns:
        String com a decisao de graduacao.
    """
    # TODO: Implementar decisao de graduacao
    #
    # Algoritmo sugerido:
    # 1. Obter min_precision e min_recall dos thresholds
    # 2. Calcular precision e recall das metrics
    # 3. Se precision >= min_precision E recall >= min_recall:
    #       retornar "graduate_to_blocking"
    # 4. Senao, se precision >= 0.70 E recall >= 0.50:
    #       retornar "needs_more_shadow"
    # 5. Senao:
    #       retornar "do_not_block"
    pass


def generate_graduation_report(
    state: ShadowState,
) -> GraduationReport:
    """
    Gera relatorio de graduacao baseado nas metricas acumuladas.

    Args:
        state: Estado do shadow period com metricas por categoria.

    Returns:
        GraduationReport com decisoes por categoria e sumario.
    """
    # TODO: Implementar geracao de relatorio
    #
    # Algoritmo sugerido:
    # 1. Criar GraduationReport com thresholds do state
    # 2. Para cada (category, metrics_dict) em state.category_metrics:
    #    a. Construir CategoryMetrics a partir do dict
    #    b. Chamar decide_graduation(metrics, thresholds)
    #    c. Adicionar decisao em report.decisions como:
    #       {
    #           "category": category,
    #           "precision": metrics.precision,
    #           "recall": metrics.recall,
    #           "f1_score": metrics.f1_score,
    #           "decision": graduation_decision,
    #           "total_ai_findings": metrics.total_ai_findings,
    #           "total_prs": metrics.total_prs_processed,
    #       }
    #    d. Incrementar report.summary[graduation_decision]
    # 3. Ordenar decisions por precision decrescente
    # 4. Retornar report
    pass


# ============================================================================
# ORCHESTRATOR: SHADOW REVIEW PIPELINE
# ============================================================================

def run_shadow_pipeline(
    state_dir: Path,
    prs: list[PRRecord],
    existing_state: Optional[ShadowState] = None,
) -> tuple[ShadowState, GraduationReport]:
    """
    Orquestrador principal: processa PRs no shadow pipeline e gera relatorio.

    Fluxo:
    1. Carregar ou inicializar ShadowState
    2. Para cada PR nao processado:
       a. classificar findings (classify_pr_findings)
       b. acumular metricas (accumulate_metrics)
       c. persistir shadow_state.json
    3. Gerar graduation report
    4. Persistir graduation_report.json

    Args:
        state_dir: Diretorio para persistir arquivos de estado.
        prs: Lista de PRs a processar.
        existing_state: Estado existente para continuar shadow period (opcional).

    Returns:
        Tupla com (ShadowState final, GraduationReport).
    """
    # TODO: Implementar o orquestrador do shadow pipeline
    #
    # Algoritmo sugerido:
    # 1. Se existing_state existe, usar como base; senao criar novo ShadowState
    # 2. Criar state_dir se nao existir
    #
    # 3. Para cada pr em prs:
    #    a. Se pr.pr_id ja esta em state.pr_ids_processed, pular (skip)
    #    b. classification = classify_pr_findings(pr)
    #    c. state = accumulate_metrics(state, classification, pr.pr_id)
    #    d. Persistir state em state_dir / "shadow_state.json"
    #
    # 4. report = generate_graduation_report(state)
    # 5. Persistir report em state_dir / "graduation_report.json"
    # 6. Retornar (state, report)
    pass


# ============================================================================
# TESTS
# ============================================================================

def test_cenario_1_basic_shadow_run():
    """Cenario 1: processar PRs e verificar metricas calculadas."""
    print("\n" + "=" * 60)
    print("TESTE 1: Shadow Run Basico — 5 PRs processados")
    print("=" * 60)

    state_dir = Path("/tmp/shadow_test_1")
    state_dir.mkdir(parents=True, exist_ok=True)

    prs = load_simulated_prs()
    state, report = run_shadow_pipeline(state_dir, prs)

    # Verificar que processou todos os 5 PRs
    assert state.total_prs_processed == 5, (
        f"Esperado 5 PRs processados, obtido {state.total_prs_processed}"
    )

    # Verificar que ha metricas para pelo menos null-safety
    assert "null-safety" in state.category_metrics, (
        "null-safety deveria ter metricas acumuladas"
    )

    # Verificar que o report tem decisoes
    assert len(report.decisions) > 0, "Report deve conter decisoes"

    print(f"  PRs processados: {state.total_prs_processed}")
    print(f"  Categorias com metricas: {len(state.category_metrics)}")
    for cat, m in state.category_metrics.items():
        print(f"    {cat}: TP={m['true_positives']}, FP={m['false_positives']}, "
              f"MA={m['missed_by_ai']}, MH={m['missed_by_human']}")

    print("  Teste 1 passou!")


def test_cenario_2_graduate_to_blocking():
    """Cenario 2: check com alta precision e recall deve graduar."""
    print("\n" + "=" * 60)
    print("TESTE 2: Graduacao — Alta Precision e Recall")
    print("=" * 60)

    metrics = CategoryMetrics(
        category="null-safety",
        total_ai_findings=100,
        true_positives=95,
        false_positives=5,
        missed_by_ai=2,
        missed_by_human=3,
    )

    thresholds = {"min_precision": 0.90, "min_recall": 0.70}
    decision = decide_graduation(metrics, thresholds)

    assert decision == GraduationDecision.GRADUATE_TO_BLOCKING, (
        f"Esperado 'graduate_to_blocking', obtido '{decision}'"
    )
    print(f"  Precision: {metrics.precision:.2%}, Recall: {metrics.recall:.2%}")
    print(f"  Decisao: {decision}")
    print("  Teste 2 passou!")


def test_cenario_3_needs_more_shadow():
    """Cenario 3: check com precision media deve precisar de mais shadow."""
    print("\n" + "=" * 60)
    print("TESTE 3: Graduacao — Precision Media, Mais Shadow")
    print("=" * 60)

    metrics = CategoryMetrics(
        category="naming-convention",
        total_ai_findings=200,
        true_positives=160,
        false_positives=40,
        missed_by_ai=10,
        missed_by_human=5,
    )

    thresholds = {"min_precision": 0.90, "min_recall": 0.70}
    decision = decide_graduation(metrics, thresholds)

    assert decision == GraduationDecision.NEEDS_MORE_SHADOW, (
        f"Esperado 'needs_more_shadow', obtido '{decision}'"
    )
    print(f"  Precision: {metrics.precision:.2%}, Recall: {metrics.recall:.2%}")
    print(f"  Decisao: {decision}")
    print("  Teste 3 passou!")


def test_cenario_4_do_not_block():
    """Cenario 4: check com baixa precision nao deve bloquear."""
    print("\n" + "=" * 60)
    print("TESTE 4: Graduacao — Baixa Precision, Nao Bloquear")
    print("=" * 60)

    metrics = CategoryMetrics(
        category="architecture",
        total_ai_findings=80,
        true_positives=35,
        false_positives=45,
        missed_by_ai=5,
        missed_by_human=2,
    )

    thresholds = {"min_precision": 0.90, "min_recall": 0.70}
    decision = decide_graduation(metrics, thresholds)

    assert decision == GraduationDecision.DO_NOT_BLOCK, (
        f"Esperado 'do_not_block', obtido '{decision}'"
    )
    print(f"  Precision: {metrics.precision:.2%}, Recall: {metrics.recall:.2%}")
    print(f"  Decisao: {decision}")
    print("  Teste 4 passou!")


def test_cenario_5_incremental_accumulation():
    """Cenario 5: adicionar PRs a shadow period existente."""
    print("\n" + "=" * 60)
    print("TESTE 5: Acumulacao Incremental")
    print("=" * 60)

    state_dir = Path("/tmp/shadow_test_5")
    state_dir.mkdir(parents=True, exist_ok=True)

    prs = load_simulated_prs()
    first_batch = prs[:3]
    second_batch = prs[3:]

    # Processar primeiro lote
    state, _ = run_shadow_pipeline(state_dir, first_batch)
    assert state.total_prs_processed == 3

    # Processar segundo lote (incremental)
    state2, report = run_shadow_pipeline(state_dir, second_batch, existing_state=state)
    assert state2.total_prs_processed == 5, (
        f"Esperado 5 PRs apos acumulacao, obtido {state2.total_prs_processed}"
    )

    # Verificar que PRs do primeiro lote nao foram duplicados
    assert len(state2.pr_ids_processed) == 5, (
        f"Esperado 5 PR IDs unicos, obtido {len(state2.pr_ids_processed)}"
    )

    print(f"  Lote 1: {len(first_batch)} PRs, Lote 2: {len(second_batch)} PRs")
    print(f"  Total acumulado: {state2.total_prs_processed}")
    print(f"  IDs unicos: {len(state2.pr_ids_processed)}")
    print("  Teste 5 passou!")


def test_cenario_6_missed_by_human_detection():
    """Cenario 6: findings do AI que o humano nao viu."""
    print("\n" + "=" * 60)
    print("TESTE 6: Deteccao de Missed by Human")
    print("=" * 60)

    # PR onde o humano nao fez nenhum comment, mas o AI encontrou algo real
    pr = PRRecord(
        pr_id="PR-SPECIAL",
        author="test_user",
        files_changed=["src/critical.py"],
        human_review_outcome={
            "approved": True,
            "comments": []  # Humano nao achou nada
        },
        ai_reviewer_output={
            "findings": [
                {"file": "src/critical.py", "line": 10, "severity": "critical",
                 "check": "sql-injection",
                 "message": "Direct SQL string interpolation — injection risk",
                 "simulated_missed_by_human": True},  # Simula que foi confirmado como real
            ]
        }
    )

    classification = classify_pr_findings(pr)

    # O finding do AI nao tem match humano → false_positive
    # Mas como tem simulated_missed_by_human, deve ser reclassificado
    assert len(classification.get("missed_by_human", [])) >= 1 or \
           len(classification.get("false_positive", [])) >= 1, (
        "Finding deve ser classificado (missed_by_human ou false_positive)"
    )

    print(f"  Classification keys: {list(classification.keys())}")
    for cat, findings in classification.items():
        print(f"    {cat}: {len(findings)} findings")
    print("  Teste 6 passou!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCICIO 7: SHADOW REVIEW PIPELINE")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_cenario_1_basic_shadow_run()
    # test_cenario_2_graduate_to_blocking()
    # test_cenario_3_needs_more_shadow()
    # test_cenario_4_do_not_block()
    # test_cenario_5_incremental_accumulation()
    # test_cenario_6_missed_by_human_detection()

    print("\nTODO: Implemente as funcoes acima!")
    print("   1. findings_match() — matching deterministico de findings")
    print("   2. classify_pr_findings() — classificacao de concordancia")
    print("   3. accumulate_metrics() — acumulacao de metricas por categoria")
    print("   4. decide_graduation() — decisao de graduacao por thresholds")
    print("   5. generate_graduation_report() — relatorio completo")
    print("   6. run_shadow_pipeline() — orquestrador principal")
    print("   Apos implementar, descomente os testes em main()")
```

---

## 🏗️ Como Comecar

### Passo 1: Implementar Propriedades de Metrica (10 min)

Comece implementando `precision`, `recall`, e `f1_score` na classe `CategoryMetrics`. Sao calculos matematicos simples e independentes do resto do pipeline.

```python
@property
def precision(self) -> float:
    denom = self.true_positives + self.false_positives
    if denom == 0:
        return 1.0  # Nao fez achados = nao causou ruido
    return self.true_positives / denom
```

Atencao ao edge case: se o AI nunca fez um finding nesta categoria, `precision = 1.0`. Se nunca houve um problema real, `recall = 1.0`. Esses defaults evitam divisao por zero e fazem sentido semantico: "se nao havia nada para encontrar, o silencio do AI e correto".

### Passo 2: Implementar Matching de Findings (20 min)

A funcao `findings_match` e o coracao do pipeline. A qualidade do matching define a qualidade de todas as metricas. Para este exercicio, use matching deterministico:

1. Mesmo arquivo (normalize path, case-insensitive)
2. Mesma categoria (`check` no AI, `category` no humano — normalize ambos para lowercase com hifens)
3. Linhas proximas: `|ai.line - human.line| <= 5`

Em producao, voce usaria embedding similarity ou um LLM para matching semantico. Mas o principio e o mesmo: determinar se dois findings referem-se ao mesmo problema.

### Passo 3: Implementar Classificacao de Concordancia (25 min)

`classify_pr_findings` itera sobre os findings do AI e os comments do humano para classificar cada um:

- **true_positive**: AI e humano encontraram o mesmo problema
- **false_positive**: AI encontrou algo que o humano considerou irrelevante
- **missed_by_ai**: Humano encontrou algo que o AI nao viu
- **missed_by_human**: AI encontrou algo real que o humano deixou passar (simulado via flag `simulated_missed_by_human`)

Dica: use sets para rastrear quais findings ja foram matched e evitar double-counting.

### Passo 4: Implementar Acumulacao de Metricas (15 min)

`accumulate_metrics` pega a classificacao de um PR e atualiza o `ShadowState`:

- Para cada finding classificado, identifique a check category e incremente os contadores correspondentes
- Verifique se o PR ja foi processado (`pr_id in state.pr_ids_processed`) para evitar duplicacao
- Atualize o timestamp e persista o estado

### Passo 5: Implementar Decisao de Graduacao (15 min)

`decide_graduation` aplica thresholds para decidir o destino de cada check:

| Condicao | Decisao |
|---|---|
| `precision >= min_precision AND recall >= min_recall` | `graduate_to_blocking` |
| `precision >= 0.70 AND recall >= 0.50` | `needs_more_shadow` |
| Otherwise | `do_not_block` |

A zona cinzenta (`needs_more_shadow`) e crucial: checks que sao promissores mas ainda nao tem dados suficientes ou precisao adequada.

### Passo 6: Orquestrar o Pipeline (20 min)

`run_shadow_pipeline` conecta todas as pecas:

1. Carrega ou inicializa `ShadowState`
2. Itera sobre PRs nao processados
3. Para cada PR: classifica, acumula, persiste
4. Gera e persiste o relatorio de graduacao

---

## ✅ Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

```python
# 1. Metricas calculadas corretamente
metrics = CategoryMetrics(
    category="test", total_ai_findings=50,
    true_positives=40, false_positives=10,
    missed_by_ai=5, missed_by_human=3
)
assert metrics.precision == 0.80    # 40 / 50
assert metrics.recall == 0.888...   # 40 / 45
assert metrics.f1_score > 0.80

# 2. Matching funciona
assert findings_match(
    {"file": "src/auth.py", "line": 45, "check": "null-safety"},
    {"file": "src/auth.py", "line": 47, "category": "null-safety"}
) == True

assert findings_match(
    {"file": "src/auth.py", "line": 45, "check": "null-safety"},
    {"file": "src/db.py", "line": 120, "category": "sql-injection"}
) == False

# 3. Graduacao decide corretamente
thresholds = {"min_precision": 0.90, "min_recall": 0.70}
assert decide_graduation(high_precision_metrics, thresholds) == "graduate_to_blocking"
assert decide_graduation(medium_precision_metrics, thresholds) == "needs_more_shadow"
assert decide_graduation(low_precision_metrics, thresholds) == "do_not_block"

# 4. Shadow pipeline processa PRs sem duplicar
state, report = run_shadow_pipeline(state_dir, prs)
assert state.total_prs_processed == len(prs)
assert len(state.pr_ids_processed) == len(set(state.pr_ids_processed))  # sem duplicatas

# 5. Relatorio de graduacao tem todas as categorias
assert "null-safety" in [d["category"] for d in report.decisions]

# 6. Shadow state persiste em disco
assert (state_dir / "shadow_state.json").exists()
assert (state_dir / "graduation_report.json").exists()
```

---

## 📊 Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Matching (Passo 2)** | 15% | Sem matching ou aleatorio | Match so por arquivo | Match por arquivo + categoria + linha | Match com tolerancia de linha e normalizacao |
| **Classificacao (Passo 3)** | 25% | Nao classifica corretamente | Classifica TP e FP apenas | Classifica TP, FP, MA, MH | Classifica com missed_by_human detectado |
| **Metricas (Passo 1+4)** | 20% | Metricas erradas ou ausentes | Precision e recall calculados | + F1 score e edge cases (div/0) | + Acumulacao incremental sem duplicacao |
| **Graduacao (Passo 5)** | 15% | Sem logica de decisao | Thresholds fixos | Thresholds configuraveis, 3 niveis | + Report com sumario e ordenacao |
| **Pipeline (Passo 6)** | 15% | Nao orquestra | Processa PRs, sem persistencia | + Persiste estado, sem duplicacao | + Suporte incremental (retomar shadow period) |
| **Testes** | 10% | Nenhum cenario passa | 2-3 cenarios passam | 4-5 cenarios passam | Todos os 6 cenarios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## 🎓 O Que Voce Aprendeu

Apos completar este exercicio, voce entende:

- Por que shadow pipelines sao o pre-requisito para AI review gates confiaveis
- Como classificar findings de AI reviewer em categorias de concordancia (TP, FP, MA, MH)
- Como calcular precision, recall, e F1 score por categoria de check
- Como usar thresholds de confianca para decidir quais checks podem migrar de shadow para blocking
- Como o shadow period transforma "acho que o bot e bom" em "sei que o bot e bom para estes 3 checks especificos"
- Por que uma taxa de 81% de falsos positivos e o resultado natural de ativar gates sem shadow period

**Proximo:** Exercise 8 — Contextual Severity Calibration

---

*Exercicio 7 | Nivel 3 — Operacional | Shadow Review Pipeline*
