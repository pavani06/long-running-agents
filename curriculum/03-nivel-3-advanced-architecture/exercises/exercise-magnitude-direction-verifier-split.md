---
title: "Exercicio: Implementar um Magnitude-Direction Verifier Split para Correcao Ponderada"
type: curriculum-exercise
nivel: 3
aliases: ["magnitude direction verifier split", "magnitude direction correction", "RLSD pattern", "weighted correction plan", "confidence weighted update", "trust but verify agent"]
tags: [curriculo-conteudo, nivel-3, agentes-orquestracao, evals, error-handling]
relates-to: ["[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]", "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|Policy Distillation Classification]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
last_updated: 2026-06-16
---
# Exercicio: Implementar um Magnitude-Direction Verifier Split para Correcao Ponderada
## Nivel 3 - Arquitetura Avancada

## Objetivo

Implementar um corretor que separa magnitude interna do agente e direcao de verificador externo para produzir um plano de correcao ponderada.

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avancado)
**Pre-requisito:** Ter lido `[[docs/canonical/generator-evaluator|Generator-Evaluator]]`, `[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]` e `[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]`
**Objetivo:** Implementar um corretor que separa o sinal de confianca interna do agente (magnitude) da verificacao externa (direcao), combinando ambos em um plano de correcao ponderada com regras de escalacao e trilha de auditoria.

---

## Prologo: O Agente Que Confiou Demais na Propria Confianca

### Quinta-feira, 15h30. Sala de revisao de qualidade.

```
TECH LEAD: "O agente de revisao de codigo esta otimo. A gente
           configurou ele pra sugerir correcoes nos PRs e ele
           sugere com 92% de confianca. E so aceitar."
```

O time tinha implementado um agente de code review que usava self-distillation: o modelo analisava o diff, comparava com seus proprios exemplos de "codigo bom", e sugeria correcoes com um score de confianca interno. Quanto maior a confianca, mais o time confiava na sugestao.

Durante 3 semanas, o agente acumulou 847 sugestoes aceitas. A taxa de aceitacao era 89%. O diretor estava satisfeito.

Ate que um bug em producao forcou uma auditoria das sugestoes aceitas. O resultado:

```
═══════════════════════════════════════════════════════════════
        AUDITORIA RETROATIVA — 847 SUGESTOES ACEITAS
═══════════════════════════════════════════════════════════════

SUGESTOES ANALISADAS:       847
SUGESTOES CORRETAS:         612  (72%)
SUGESTOES INCORRETAS:       203  (24%)
SUGESTOES AMBIGUAS:          32  (4%)

DETALHE DAS INCORRETAS:
  Alta confianca (>0.85), incorreta:   78  (38% das incorretas)
  Media confianca (0.5-0.85), incorreta: 89  (44%)
  Baixa confianca (<0.5), incorreta:   36  (18%)

PADRAO CRITICO:
  Das 78 sugestoes de ALTA CONFIANCA que estavam INCORRETAS:
  - 41 introduziram null pointer risks
  - 23 removeram error handling necessario
  - 14 quebraram contratos de API

  O agente CONFIOU que a mudanca era correta. Mas CONFIANCA
  nao e CORRECAO. Alta magnitude sem verificacao de direcao
  = dano amplificado pela confianca.
═══════════════════════════════════════════════════════════════
```

```
ARQUITETA (post-mortem): "O problema e estrutural. O agente usava
                          a propria confianca como sinal de correcao.
                          Isso e 'information leakage': o modelo aprende
                          a imitar o formato das correcoes sem verificar
                          se a direcao esta certa.

                          O que faltava: separar MAGNITUDE (o quanto o
                          agente acha que a mudanca importa) de DIRECAO
                          (um verificador externo diz se a mudanca esta
                          correta ou nao). E combinar os dois com pesos:
                          so gaste esforco de correcao onde a magnitude
                          e alta E a direcao esta confirmada."
```

**O que teria evitado tudo:**

> Magnitude-Direction Verifier Split: extrair a confianca interna do agente como sinal de magnitude (onde a correcao importa), verificar a direcao com um verificador externo (a correcao esta certa?), e produzir um plano de correcao ponderada. Alta magnitude + direcao incerta = escalacao para revisao humana. Alta magnitude + direcao confirmada = correcao prioritaria.

**Sua missao:** Construir um `MagnitudeDirectionCorrector` que implementa exatamente essa separacao.

---

## Cenario: Correcao Ponderada no Agente de Code Review

### Contexto

Voce e o engenheiro de qualidade do time de plataforma. O agente de code review atual produz sugestoes de correcao com um score de confianca interno (`magnitude`), mas nao verifica se a direcao da correcao esta certa. Voce vai adicionar um segundo estagio: um `ExternalVerifier` que avalia cada sugestao contra um conjunto de regras deterministicas e rubricas, produzindo um sinal de `direction` (+1 para correto, -1 para incorreto, 0 para incerto).

O corretor final combina magnitude e direcao em um `WeightedCorrectionPlan`:

| Cenario | Magnitude | Direction | Acao |
|---|---|---|---|
| Confiante e correto | Alta | +1 | Aplicar correcao com peso maximo |
| Confiante e incorreto | Alta | -1 | Rejeitar correcao + registrar falso-positivo de alta confianca |
| Inseguro e correto | Baixa | +1 | Aplicar correcao com peso baixo (sugestao, nao bloqueante) |
| Inseguro e incorreto | Baixa | -1 | Descartar silenciosamente |
| Confiante e incerto | Alta | 0 | Escalar para revisao humana |
| Inseguro e incerto | Baixa | 0 | Deferir (voltar a verificar depois) |

### Sinais de Magnitude

O corretor extrai magnitude de fontes internas do agente:

| Fonte | Descricao | Range |
|---|---|---|
| `self_distillation_delta` | Diferenca entre output do agente com e sem exemplos de referencia | [0, 1] |
| `log_ratio` | Log-razao entre probabilidade do token sugerido e a media dos alternativos | [0, +inf) |
| `attention_hotspot` | Concentracao de atencao no span de codigo modificado | [0, 1] |
| `disagreement_intensity` | Grau de discordancia entre multiplas amostras do mesmo agente | [0, 1] |

### Sinais de Direcao

O verificador externo avalia a sugestao contra criterios independentes:

| Fonte | Descricao | Output |
|---|---|---|
| `deterministic_tests` | Testes unitarios/integracao executados sobre o codigo modificado | +1 (pass), -1 (fail), 0 (no coverage) |
| `lint_rules` | Regras de lint especificas do projeto | +1 (clean), -1 (violation), 0 (not applicable) |
| `constraint_check` | Verificacao contra constraints de dominio (ex: "toda query tem indice") | +1 (satisfies), -1 (violates), 0 (not checkable) |
| `human_review_sample` | Amostra de revisao humana para calibracao periodica | +1 (approved), -1 (rejected), 0 (pending) |

### Dados de Entrada

Voce recebe um batch de 20 sugestoes do agente de code review. Cada sugestao contem:

```json
{
  "suggestion_id": "SUG-0042",
  "file": "src/payment/gateway.py",
  "line_range": [142, 158],
  "original_code": "result = db.execute(query)",
  "suggested_code": "result = db.execute(query, timeout=30)",
  "magnitude_signals": {
    "self_distillation_delta": 0.87,
    "log_ratio": 2.3,
    "attention_hotspot": 0.91,
    "disagreement_intensity": 0.12
  },
  "verifier_results": {
    "deterministic_tests": 1,
    "lint_rules": 1,
    "constraint_check": 1,
    "human_review_sample": 0
  }
}
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Magnitude composta:** O corretor combina os sinais de magnitude em um unico score normalizado em [0, 1] usando media ponderada com pesos configuraveis.
2. **RF2 - Direcao composta:** O corretor combina os sinais de direcao em um veredito tri-state: `CORRECT` (+1), `INCORRECT` (-1), ou `UNCERTAIN` (0). A direcao e `UNCERTAIN` se os verificadores discordam ou se nao ha verificadores aplicaveis.
3. **RF3 - Matriz de decisao:** O corretor aplica a matriz magnitude × direcao para classificar cada sugestao em uma acao: `APPLY_HIGH`, `APPLY_LOW`, `REJECT`, `DISCARD`, `ESCALATE`, `DEFER`.
4. **RF4 - Ponderacao por confianca:** Correcoes `APPLY_HIGH` recebem peso de correcao = magnitude (max 1.0). Correcoes `APPLY_LOW` recebem peso = magnitude * 0.3. Correcoes rejeitadas tem peso zero.
5. **RF5 - Escalacao com threshold:** Sugestoes com magnitude >= 0.70 e direcao `UNCERTAIN` sao escaladas para revisao humana. Sugestoes escaladas incluem o pacote completo de evidencias.
6. **RF6 - Trilha de auditoria:** Cada decisao registra separadamente: (a) evidencias de magnitude, (b) evidencias de direcao, (c) justificativa da decisao. As evidencias de confianca e correcao nunca sao misturadas no mesmo campo.

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses.
2. **RT2 - Normalizacao de magnitude:** `log_ratio` e normalizado para [0, 1] usando `min(1.0, log_ratio / LOG_RATIO_CAP)` onde `LOG_RATIO_CAP = 5.0`.
3. **RT3 - Verificador deterministico:** Dado o mesmo input, o `ExternalVerifier` produz o mesmo veredito de direcao.
4. **RT4 - Separacao de evidencias:** O `AuditRecord` tem campos distintos para `magnitude_evidence` e `direction_evidence` — nunca um campo unico de "confidence".

---

## Sua Tarefa

Voce vai implementar o MagnitudeDirectionCorrector em 3 partes.

---

### Parte 1: Diagnosticar o Information Leakage (15 min)

Analise as 20 sugestoes do batch abaixo. Identifique:

1. Sugestoes onde alta magnitude escondeu direcao incorreta (falsos positivos de alta confianca).
2. Sugestoes onde baixa magnitude subestimou uma correcao correta (correcoes uteis ignoradas).
3. Sugestoes que deveriam ter sido escaladas por terem alta magnitude e direcao incerta.

```python
# Batch de 20 sugestoes do agente de code review
# Formato: (id, magnitude_composta, direction_verdict, ground_truth)
# direction_verdict: +1=CORRECT, -1=INCORRECT, 0=UNCERTAIN
# ground_truth: o que um humano determinou depois (True=correcao era boa)

BATCH_SUGGESTIONS = [
    ("SUG-01", 0.92, +1, True),   # alta magnitude, direcao correta, realmente bom
    ("SUG-02", 0.88, -1, False),  # alta magnitude, direcao incorreta — FALSO POSITIVO CRITICO
    ("SUG-03", 0.35, +1, True),   # baixa magnitude, direcao correta — subestimado
    ("SUG-04", 0.15, -1, False),  # baixa magnitude, incorreto — descartavel
    ("SUG-05", 0.91,  0, True),   # alta magnitude, direcao INCERTA, realmente bom — ESCALAR
    ("SUG-06", 0.85,  0, False),  # alta magnitude, direcao INCERTA, realmente ruim — ESCALAR
    ("SUG-07", 0.42, +1, True),   # baixa magnitude, correto — peso baixo
    ("SUG-08", 0.78, -1, False),  # alta magnitude, incorreto — FALSO POSITIVO
    ("SUG-09", 0.95, +1, True),   # caso ideal
    ("SUG-10", 0.55,  0, True),   # media magnitude, incerto — DEFER
    ("SUG-11", 0.72, -1, False),  # alta magnitude, incorreto
    ("SUG-12", 0.08, +1, True),   # muito baixa magnitude, correto — quase irrelevante
    ("SUG-13", 0.89, +1, True),   # otimo
    ("SUG-14", 0.63, -1, False),  # media magnitude, incorreto
    ("SUG-15", 0.93,  0, True),   # alta magnitude, incerto, realmente bom — ESCALAR
    ("SUG-16", 0.47, +1, True),   # media-baixa, correto
    ("SUG-17", 0.81, -1, False),  # alta magnitude, incorreto — FALSO POSITIVO
    ("SUG-18", 0.37,  0, False),  # baixa magnitude, incerto, ruim — DEFER (deixa pra depois)
    ("SUG-19", 0.96, +1, True),   # quase perfeito
    ("SUG-20", 0.76,  0, False),  # alta magnitude, incerto, ruim — ESCALAR
]

# TAREFA: Responda no seu codigo como comentario:
#
# 1. Quais sugestoes sao FALSOS POSITIVOS DE ALTA CONFIANCA
#    (magnitude >= 0.70, direction = -1)?
#    Liste os IDs. Quantas sao?
#
# 2. Quais sugestoes deveriam ser ESCALADAS para revisao humana
#    (magnitude >= 0.70, direction = 0)?
#    Liste os IDs. Quantas sao?
#
# 3. Se o sistema atual (sem verifier) tivesse aceitado todas as
#    sugestoes com magnitude >= 0.70, qual seria a taxa de erro?
#    (Dica: conte quantas tem magnitude >= 0.70 e ground_truth = False)
#
# 4. Se o Magnitude-Direction Verifier Split tivesse sido aplicado:
#    a. Quantas sugestoes seriam APPLY_HIGH? (alta magnitude + CORRECT)
#    b. Quantas seriam REJECT? (alta magnitude + INCORRECT)
#    c. Quantas seriam ESCALATE? (alta magnitude + UNCERTAIN)
#    d. Qual seria a nova taxa de erro nas sugestoes aplicadas?
```

---

### Parte 2: Implementar o MagnitudeDirectionCorrector (55 min)

Implemente o corretor. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class DirectionVerdict(Enum):
    CORRECT = "correct"        # +1: verificadores concordam que a correcao e boa
    INCORRECT = "incorrect"   # -1: verificadores concordam que a correcao e ruim
    UNCERTAIN = "uncertain"    #  0: verificadores discordam ou nao ha cobertura


class CorrectionAction(Enum):
    APPLY_HIGH = "apply_high"        # alta magnitude + direcao correta
    APPLY_LOW = "apply_low"          # baixa magnitude + direcao correta
    REJECT = "reject"                # alta magnitude + direcao incorreta
    DISCARD = "discard"              # baixa magnitude + direcao incorreta
    ESCALATE = "escalate"            # alta magnitude + direcao incerta → humano
    DEFER = "defer"                  # baixa magnitude + direcao incerta → verificar depois


@dataclass
class MagnitudeSignals:
    """Sinais internos de magnitude do agente."""
    self_distillation_delta: float   # [0, 1]
    log_ratio: float                 # [0, +inf)
    attention_hotspot: float         # [0, 1]
    disagreement_intensity: float    # [0, 1]


@dataclass
class VerifierSignals:
    """Sinais externos de direcao do verificador."""
    deterministic_tests: int    # +1 pass, -1 fail, 0 no coverage
    lint_rules: int             # +1 clean, -1 violation, 0 N/A
    constraint_check: int       # +1 satisfies, -1 violates, 0 not checkable
    human_review_sample: int    # +1 approved, -1 rejected, 0 pending


@dataclass
class Suggestion:
    """Uma sugestao de correcao do agente de code review."""
    suggestion_id: str
    file: str
    line_range: tuple[int, int]
    original_code: str
    suggested_code: str
    magnitude_signals: MagnitudeSignals
    verifier_results: VerifierSignals


@dataclass
class AuditRecord:
    """Trilha de auditoria separando evidencias de magnitude e direcao."""
    suggestion_id: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Evidencias de magnitude (confianca interna) — SEPARADAS das de direcao
    magnitude_composite: float = 0.0
    magnitude_breakdown: dict[str, float] = field(default_factory=dict)

    # Evidencias de direcao (verificacao externa) — SEPARADAS das de magnitude
    direction_verdict: DirectionVerdict = DirectionVerdict.UNCERTAIN
    direction_breakdown: dict[str, int] = field(default_factory=dict)

    # Decisao
    action: CorrectionAction = CorrectionAction.DEFER
    correction_weight: float = 0.0
    rationale: str = ""

    def evidence_package(self) -> str:
        """Pacote completo de evidencias para revisao humana (escalacao)."""
        lines = [
            f"SUGGESTION: {self.suggestion_id}",
            f"ACTION: {self.action.value}",
            f"",
            f"MAGNITUDE (internal confidence): {self.magnitude_composite:.3f}",
        ]
        for signal, value in self.magnitude_breakdown.items():
            lines.append(f"  {signal}: {value:.3f}")
        lines.append(f"")
        lines.append(f"DIRECTION (external verification): {self.direction_verdict.value}")
        for signal, value in self.direction_breakdown.items():
            lines.append(f"  {signal}: {value}")
        lines.append(f"")
        lines.append(f"CORRECTION WEIGHT: {self.correction_weight:.3f}")
        lines.append(f"RATIONALE: {self.rationale}")
        return "\n".join(lines)


# ============================================================
# MAGNITUDE COMPOSITION
# ============================================================

# Pesos default para cada sinal de magnitude
DEFAULT_MAGNITUDE_WEIGHTS = {
    "self_distillation_delta": 0.35,
    "log_ratio": 0.30,
    "attention_hotspot": 0.20,
    "disagreement_intensity": 0.15,
}

# Cap para normalizacao do log_ratio
LOG_RATIO_CAP = 5.0

# Threshold de alta magnitude
HIGH_MAGNITUDE_THRESHOLD = 0.70


def normalize_log_ratio(log_ratio: float) -> float:
    """
    Normaliza log_ratio (ilimitado) para [0, 1].

    Formula: min(1.0, log_ratio / LOG_RATIO_CAP)
    """
    # SEU CODIGO AQUI
    pass


def compute_magnitude(signals: MagnitudeSignals, weights: dict[str, float] = None) -> float:
    """
    Calcula a magnitude composta como media ponderada dos sinais normalizados.

    Args:
        signals: Sinais brutos de magnitude.
        weights: Pesos por sinal. Usa DEFAULT_MAGNITUDE_WEIGHTS se None.

    Returns:
        Score de magnitude em [0, 1].
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Usar DEFAULT_MAGNITUDE_WEIGHTS se weights for None
    # 2. normalizar cada sinal:
    #    - self_distillation_delta, attention_hotspot, disagreement_intensity:
    #      ja estao em [0, 1] — usar direto
    #    - log_ratio: normalizar com normalize_log_ratio()
    # 3. Calcular media ponderada:
    #    magnitude = sum(normalized_value * weight for each signal)
    # 4. Garantir que o resultado esta em [0, 1]
    pass


# ============================================================
# DIRECTION COMPOSITION
# ============================================================

# Pesos default para cada sinal de direcao
DEFAULT_DIRECTION_WEIGHTS = {
    "deterministic_tests": 0.40,
    "lint_rules": 0.20,
    "constraint_check": 0.25,
    "human_review_sample": 0.15,
}

# Threshold para considerar direcao confirmada
DIRECTION_CONSENSUS_THRESHOLD = 0.60


def compute_direction(signals: VerifierSignals, weights: dict[str, float] = None) -> DirectionVerdict:
    """
    Combina os sinais de direcao em um veredito tri-state.

    Regras:
    1. Se nenhum verificador tem sinal (todos 0): UNCERTAIN
    2. Calcular score ponderado dos sinais nao-zero:
       score = sum(signal * weight) / sum(weight for non-zero signals)
    3. Se |score| >= DIRECTION_CONSENSUS_THRESHOLD:
       - score > 0 → CORRECT
       - score < 0 → INCORRECT
    4. Senao: UNCERTAIN (verificadores discordam ou sinal fraco)

    Args:
        signals: Sinais brutos de direcao.
        weights: Pesos por verificador.

    Returns:
        DirectionVerdict (CORRECT, INCORRECT, ou UNCERTAIN).
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Filtrar sinais nao-zero
    # 2. Se nenhum sinal nao-zero: return UNCERTAIN
    # 3. Calcular weighted_score = sum(s * w for s, w in non_zero)
    # 4. Calcular total_weight = sum(w for _, w in non_zero)
    # 5. normalized = weighted_score / total_weight  (entre -1 e +1)
    # 6. Se normalized >= DIRECTION_CONSENSUS_THRESHOLD: CORRECT
    # 7. Se normalized <= -DIRECTION_CONSENSUS_THRESHOLD: INCORRECT
    # 8. Senao: UNCERTAIN
    pass


# ============================================================
# MAGNITUDE-DIRECTION CORRECTOR — nucleo do exercicio
# ============================================================

def decide_action(magnitude: float, direction: DirectionVerdict) -> CorrectionAction:
    """
    Aplica a matriz magnitude × direcao para decidir a acao.

    Matriz de decisao:
    | Magnitude \ Direction | CORRECT      | INCORRECT    | UNCERTAIN    |
    |------------------------|--------------|--------------|--------------|
    | Alta (>= 0.70)         | APPLY_HIGH   | REJECT       | ESCALATE     |
    | Baixa (< 0.70)         | APPLY_LOW    | DISCARD      | DEFER        |

    Args:
        magnitude: Score composto de magnitude em [0, 1].
        direction: Veredito de direcao do verificador.

    Returns:
        CorrectionAction correspondente.
    """
    # SEU CODIGO AQUI
    pass


def compute_correction_weight(magnitude: float, action: CorrectionAction) -> float:
    """
    Calcula o peso de correcao baseado na magnitude e na acao decidida.

    Regras:
    - APPLY_HIGH: weight = magnitude (peso maximo, confia na magnitude)
    - APPLY_LOW:  weight = magnitude * 0.3 (peso reduzido, sugestao leve)
    - REJECT:     weight = 0.0 (rejeitado — nao aplicar)
    - DISCARD:    weight = 0.0 (descartado — nao aplicar)
    - ESCALATE:   weight = 0.0 (pausado ate revisao humana)
    - DEFER:      weight = 0.0 (pausado ate proxima verificacao)

    Args:
        magnitude: Score composto de magnitude.
        action: Acao decidida.

    Returns:
        Peso de correcao em [0, 1].
    """
    # SEU CODIGO AQUI
    pass


def process_suggestion(
    suggestion: Suggestion,
    magnitude_weights: dict[str, float] = None,
    direction_weights: dict[str, float] = None,
) -> AuditRecord:
    """
    Processa uma unica sugestao atraves do pipeline magnitude-direction.

    Fluxo:
    1. Extrair magnitude composta dos sinais internos
    2. Extrair direcao composta dos sinais do verificador
    3. Decidir acao pela matriz magnitude × direcao
    4. Calcular peso de correcao
    5. Construir AuditRecord com evidencias separadas

    Args:
        suggestion: Sugestao do agente.
        magnitude_weights: Pesos para sinais de magnitude.
        direction_weights: Pesos para sinais de direcao.

    Returns:
        AuditRecord completo com evidencias e decisao.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. magnitude = compute_magnitude(suggestion.magnitude_signals, magnitude_weights)
    # 2. direction = compute_direction(suggestion.verifier_results, direction_weights)
    # 3. action = decide_action(magnitude, direction)
    # 4. weight = compute_correction_weight(magnitude, action)
    # 5. Construir magnitude_breakdown com os sinais normalizados
    # 6. Construir direction_breakdown com os sinais brutos
    # 7. Gerar rationale explicando a decisao
    # 8. Retornar AuditRecord
    pass


def process_batch(
    suggestions: list[Suggestion],
    magnitude_weights: dict[str, float] = None,
    direction_weights: dict[str, float] = None,
) -> list[AuditRecord]:
    """
    Processa um batch de sugestoes e retorna registros de auditoria.

    Args:
        suggestions: Lista de sugestoes.
        magnitude_weights: Pesos para sinais de magnitude.
        direction_weights: Pesos para sinais de direcao.

    Returns:
        Lista de AuditRecord, um por sugestao.
    """
    # SEU CODIGO AQUI
    pass


def batch_summary(records: list[AuditRecord]) -> dict:
    """
    Produz um resumo agregado do batch.

    Returns:
        Dicionario com contagens por acao, taxa de escalacao, etc.
    """
    # SEU CODIGO AQUI
    #
    # Retornar:
    # {
    #     "total": len(records),
    #     "apply_high": count,
    #     "apply_low": count,
    #     "reject": count,
    #     "discard": count,
    #     "escalate": count,
    #     "defer": count,
    #     "escalation_rate": escalate_count / total,
    #     "avg_correction_weight": mean(r.correction_weight for r in records),
    # }
    pass


# ============================================================
# TESTES RAPIDOS: MagnitudeDirectionCorrector
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO MAGNITUDE-DIRECTION VERIFIER SPLIT")
    print("=" * 60)

    # Teste 1: normalize_log_ratio
    print("\nTeste 1: normalize_log_ratio")
    assert abs(normalize_log_ratio(2.5) - 0.5) < 0.01, f"log_ratio=2.5 → 0.5, got {normalize_log_ratio(2.5)}"
    assert normalize_log_ratio(10.0) == 1.0, "log_ratio acima do cap → 1.0"
    assert normalize_log_ratio(0.0) == 0.0, "log_ratio=0 → 0.0"
    print("  normalize_log_ratio: OK")

    # Teste 2: compute_magnitude — caso tipico
    signals = MagnitudeSignals(
        self_distillation_delta=0.87,
        log_ratio=2.3,
        attention_hotspot=0.91,
        disagreement_intensity=0.12,
    )
    mag = compute_magnitude(signals)
    print(f"\nTeste 2: compute_magnitude com sinais fortes")
    print(f"  Magnitude composta: {mag:.3f}")
    assert 0.60 <= mag <= 0.95, f"Magnitude esperada entre 0.6 e 0.95, obtida {mag:.3f}"
    print("  Magnitude dentro do range esperado: OK")

    # Teste 3: compute_magnitude — sinais fracos
    weak_signals = MagnitudeSignals(0.15, 0.2, 0.10, 0.05)
    weak_mag = compute_magnitude(weak_signals)
    print(f"\nTeste 3: compute_magnitude com sinais fracos")
    print(f"  Magnitude composta: {weak_mag:.3f}")
    assert weak_mag < 0.30, f"Magnitude deveria ser baixa, obtida {weak_mag:.3f}"
    print("  Magnitude baixa detectada: OK")

    # Teste 4: compute_direction — consenso CORRECT
    verifier = VerifierSignals(
        deterministic_tests=1,
        lint_rules=1,
        constraint_check=1,
        human_review_sample=0,
    )
    direction = compute_direction(verifier)
    print(f"\nTeste 4: compute_direction com consenso positivo")
    print(f"  Direcao: {direction.value}")
    assert direction == DirectionVerdict.CORRECT, f"Esperado CORRECT, obtido {direction.value}"
    print("  CORRECT detectado: OK")

    # Teste 5: compute_direction — consenso INCORRECT
    bad_verifier = VerifierSignals(-1, -1, 1, 0)
    bad_direction = compute_direction(bad_verifier)
    print(f"\nTeste 5: compute_direction com maioria negativa")
    print(f"  Direcao: {bad_direction.value}")
    assert bad_direction == DirectionVerdict.INCORRECT, f"Esperado INCORRECT, obtido {bad_direction.value}"
    print("  INCORRECT detectado: OK")

    # Teste 6: compute_direction — UNCERTAIN (sem verificadores)
    no_verifier = VerifierSignals(0, 0, 0, 0)
    no_dir = compute_direction(no_verifier)
    print(f"\nTeste 6: compute_direction sem verificadores")
    print(f"  Direcao: {no_dir.value}")
    assert no_dir == DirectionVerdict.UNCERTAIN, f"Esperado UNCERTAIN, obtido {no_dir.value}"
    print("  UNCERTAIN detectado (sem verificadores): OK")

    # Teste 7: decide_action — matriz completa
    print(f"\nTeste 7: decide_action — matriz magnitude × direcao")
    assert decide_action(0.85, DirectionVerdict.CORRECT) == CorrectionAction.APPLY_HIGH
    assert decide_action(0.30, DirectionVerdict.CORRECT) == CorrectionAction.APPLY_LOW
    assert decide_action(0.92, DirectionVerdict.INCORRECT) == CorrectionAction.REJECT
    assert decide_action(0.15, DirectionVerdict.INCORRECT) == CorrectionAction.DISCARD
    assert decide_action(0.88, DirectionVerdict.UNCERTAIN) == CorrectionAction.ESCALATE
    assert decide_action(0.45, DirectionVerdict.UNCERTAIN) == CorrectionAction.DEFER
    print("  Todos os 6 casos da matriz: OK")

    # Teste 8: compute_correction_weight
    print(f"\nTeste 8: compute_correction_weight")
    assert abs(compute_correction_weight(0.90, CorrectionAction.APPLY_HIGH) - 0.90) < 0.01
    assert abs(compute_correction_weight(0.60, CorrectionAction.APPLY_LOW) - 0.18) < 0.01
    assert compute_correction_weight(0.85, CorrectionAction.REJECT) == 0.0
    assert compute_correction_weight(0.75, CorrectionAction.ESCALATE) == 0.0
    print("  Pesos corretos para todas as acoes: OK")

    # Teste 9: process_suggestion — integracao completa
    print(f"\nTeste 9: process_suggestion — integracao")
    sug = Suggestion(
        suggestion_id="SUG-TEST",
        file="src/test.py",
        line_range=(10, 20),
        original_code="x = 1",
        suggested_code="x = 2",
        magnitude_signals=MagnitudeSignals(0.90, 3.5, 0.88, 0.10),
        verifier_results=VerifierSignals(1, 1, 1, 0),
    )
    record = process_suggestion(sug)
    print(f"  Action: {record.action.value}")
    print(f"  Magnitude: {record.magnitude_composite:.3f}")
    print(f"  Direction: {record.direction_verdict.value}")
    print(f"  Weight: {record.correction_weight:.3f}")
    assert record.action == CorrectionAction.APPLY_HIGH, f"Esperado APPLY_HIGH, obtido {record.action.value}"
    assert record.correction_weight > 0.70, "Peso deveria ser alto para APPLY_HIGH"
    # Verificar separacao de evidencias
    assert "self_distillation_delta" in record.magnitude_breakdown
    assert "deterministic_tests" in record.direction_breakdown
    assert len(record.rationale) > 0, "Rationale nao pode ser vazio"
    print("  Integracao completa + evidencias separadas: OK")

    # Teste 10: process_suggestion — ESCALATE
    print(f"\nTeste 10: process_suggestion — escalacao")
    escalate_sug = Suggestion(
        suggestion_id="SUG-ESC",
        file="src/db.py",
        line_range=(50, 65),
        original_code="query = f'SELECT * FROM {table}'",
        suggested_code="query = 'SELECT * FROM users'",
        magnitude_signals=MagnitudeSignals(0.85, 4.0, 0.92, 0.15),
        verifier_results=VerifierSignals(0, 0, 0, 0),  # sem verificadores
    )
    esc_record = process_suggestion(escalate_sug)
    print(f"  Action: {esc_record.action.value}")
    print(f"  Direction: {esc_record.direction_verdict.value}")
    assert esc_record.action == CorrectionAction.ESCALATE, f"Esperado ESCALATE, obtido {esc_record.action.value}"
    evidence = esc_record.evidence_package()
    assert "MAGNITUDE" in evidence
    assert "DIRECTION" in evidence
    assert "ESCALATE" in evidence
    print("  Escalacao com evidence package: OK")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO MAGNITUDE-DIRECTION CORRECTOR PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Executar o Batch e Comparar com o Sistema Sem Verifier (25 min)

```python
# ============================================================
# SIMULACAO: Batch de 20 sugestoes — com e sem verifier
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: BATCH DE 20 SUGESTOES")
    print("=" * 60)

    # Construir sugestoes a partir do BATCH_SUGGESTIONS
    suggestions = []
    for sug_id, magnitude, direction_val, ground_truth in BATCH_SUGGESTIONS:
        # Converter direction_val para VerifierSignals
        if direction_val == 1:
            v = VerifierSignals(1, 1, 1, 0)
        elif direction_val == -1:
            v = VerifierSignals(-1, -1, -1, 0)
        else:
            v = VerifierSignals(0, 0, 0, 0)

        suggestions.append(Suggestion(
            suggestion_id=sug_id,
            file=f"src/{sug_id.lower()}.py",
            line_range=(10, 20),
            original_code="old",
            suggested_code="new",
            magnitude_signals=MagnitudeSignals(magnitude, magnitude * 3, magnitude, 0.10),
            verifier_results=v,
        ))

    # Processar com Magnitude-Direction Verifier Split
    records = process_batch(suggestions)
    summary = batch_summary(records)

    print(f"\nRESUMO DO BATCH (Magnitude-Direction Verifier Split):")
    print(f"  Total: {summary['total']}")
    print(f"  APPLY_HIGH:  {summary['apply_high']}")
    print(f"  APPLY_LOW:   {summary['apply_low']}")
    print(f"  REJECT:      {summary['reject']}")
    print(f"  DISCARD:     {summary['discard']}")
    print(f"  ESCALATE:    {summary['escalate']}")
    print(f"  DEFER:       {summary['defer']}")
    print(f"  Escalation rate: {summary['escalation_rate']:.1%}")
    print(f"  Avg correction weight: {summary['avg_correction_weight']:.3f}")

    # Comparar com o sistema sem verifier
    print(f"\nCOMPARACAO: Com verifier vs. Sem verifier")
    print(f"  Sem verifier: aceita todas com magnitude >= 0.70")
    high_mag_total = sum(1 for _, m, _, _ in BATCH_SUGGESTIONS if m >= 0.70)
    high_mag_wrong = sum(1 for _, m, d, gt in BATCH_SUGGESTIONS if m >= 0.70 and not gt)
    high_mag_uncertain = sum(1 for _, m, d, _ in BATCH_SUGGESTIONS if m >= 0.70 and d == 0)
    print(f"    Aceitas: {high_mag_total}")
    print(f"    Incorretas (falsos positivos): {high_mag_wrong}")
    print(f"    Incertas (aceitas sem verificacao): {high_mag_uncertain}")
    if high_mag_total > 0:
        print(f"    Taxa de erro: {high_mag_wrong / high_mag_total:.1%}")

    print(f"\n  Com verifier (Magnitude-Direction Split):")
    applied = summary['apply_high'] + summary['apply_low']
    rejected = summary['reject'] + summary['discard']
    escalated = summary['escalate']
    print(f"    Aplicadas (HIGH+LOW): {applied}")
    print(f"    Rejeitadas/Descartadas: {rejected}")
    print(f"    Escaladas para humano: {escalated}")
    print(f"    Diferidas: {summary['defer']}")

    # Listar sugestoes escaladas
    print(f"\nSUGESTOES ESCALADAS PARA REVISAO HUMANA:")
    for r in records:
        if r.action == CorrectionAction.ESCALATE:
            print(f"  {r.suggestion_id}: magnitude={r.magnitude_composite:.2f}, "
                  f"direction={r.direction_verdict.value}")

    # Listar rejeicoes de alta confianca
    print(f"\nREJEICOES DE ALTA CONFIANCA (falsos positivos interceptados):")
    for r in records:
        if r.action == CorrectionAction.REJECT:
            print(f"  {r.suggestion_id}: magnitude={r.magnitude_composite:.2f} "
                  f"— seria aceito sem verifier, rejeitado com verifier")

    print(f"\nCONCLUSÃO:")
    print(f"  O Magnitude-Direction Verifier Split interceptou sugestoes")
    print(f"  de alta confianca que estavam incorretas e as rejeitou.")
    print(f"  Sugestoes de alta confianca com direcao incerta foram")
    print(f"  escaladas para revisao humana em vez de aplicadas as cegas.")
    print(f"  A confianca interna do agente (magnitude) e a verificacao")
    print(f"  externa (direcao) permanecem em trilhas de auditoria separadas.")
```

---

## Entregaveis

- Implementacao de `MagnitudeDirectionCorrector` com extracao de magnitude e direcao.
- Matriz de decisao para reforcar, corrigir, escalar, deferir ou ignorar.
- Audit trail separando evidencia de confianca e evidencia de correcao.

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce identificou corretamente os falsos positivos de alta confianca (magnitude >= 0.70, direction = -1)
- [ ] Voce identificou as sugestoes que deveriam ser escaladas (magnitude >= 0.70, direction = 0)
- [ ] Voce calculou a taxa de erro do sistema sem verifier e comparou com o sistema com verifier

### Criterio 2: Magnitude composta

- [ ] `normalize_log_ratio()` normaliza corretamente para [0, 1]
- [ ] `compute_magnitude()` retorna media ponderada correta dos sinais normalizados
- [ ] Sinais fortes (delta=0.9, log_ratio=5.0, attention=0.9) produzem magnitude > 0.70
- [ ] Sinais fracos (delta=0.1, log_ratio=0.2, attention=0.1) produzem magnitude < 0.30

### Criterio 3: Direcao composta

- [ ] `compute_direction()` retorna CORRECT quando todos os verificadores sao +1
- [ ] `compute_direction()` retorna INCORRECT quando a maioria e -1
- [ ] `compute_direction()` retorna UNCERTAIN quando nao ha verificadores ou ha discordancia
- [ ] O threshold de consenso (0.60) e respeitado

### Criterio 4: Matriz de decisao

- [ ] `decide_action()` cobre todos os 6 casos da matriz magnitude × direcao
- [ ] Alta magnitude + INCORRECT → REJECT (nao APPLY_HIGH)
- [ ] Alta magnitude + UNCERTAIN → ESCALATE (nao APPLY_HIGH)

### Criterio 5: Trilha de auditoria

- [ ] `AuditRecord` separa `magnitude_breakdown` de `direction_breakdown`
- [ ] `evidence_package()` formata evidencias para revisao humana
- [ ] `rationale` explica a decisao em linguagem natural

### Criterio 6: Testes

- [ ] Testes 1-3: magnitude (normalizacao, fortes, fracos)
- [ ] Testes 4-6: direcao (CORRECT, INCORRECT, UNCERTAIN)
- [ ] Testes 7-8: matriz de decisao e pesos de correcao
- [ ] Testes 9-10: integracao completa e escalacao

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou falsos positivos nem escalacoes | Identificou parcialmente (~50%) | Diagnostico completo com contagem e taxa de erro | Diagnostico + analise de sensibilidade dos thresholds |
| **Magnitude + Direcao (Parte 2)** | 40% | Funcoes core nao implementadas | Implementa mas erra em normalizacao ou threshold | Corretor funcional com todos os sinais e thresholds | Corretor completo + pesos configuraraveis + rationale contextual |
| **Simulacao (Parte 3)** | 30% | Nao executou o batch | Batch parcial sem contraste | Batch completo com comparacao verifier vs sem verifier | Batch + analise de falsos positivos interceptados + sugestoes de calibracao |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 5 criterios passam | Todos os 6 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para a Magnitude

1. **Magnitude nao e "qualidade" — e "intensidade de conviccao".** Um agente pode ter alta magnitude sobre uma correcao errada. Magnitude mede o quanto o agente ACHA que a mudanca importa, nao se a mudanca esta certa. E por isso que a direcao e necessaria.

2. **O log_ratio e o sinal mais informativo — e o mais perigoso.** Um log_ratio alto significa que o agente tinha uma preferencia muito forte por uma alternativa especifica. Isso e util para priorizar correcoes, mas sem verificacao de direcao, correcoes de alta magnitude viram erros de alta magnitude.

3. **Pesos de magnitude devem refletir a confiabilidade relativa de cada sinal.** `self_distillation_delta` (0.35) tem peso maior que `disagreement_intensity` (0.15) porque a comparacao com exemplos de referencia e mais informativa que a variancia entre amostras. Mas esses pesos sao pontos de partida — recalibre com dados reais do seu agente.

### Para a Direcao

1. **Direcao e uma questao de CONSENSO, nao de maioria simples.** Se `deterministic_tests` diz +1 mas `lint_rules` e `constraint_check` dizem -1, a direcao e UNCERTAIN — nao CORRECT. O threshold de consenso (0.60) existe para evitar que um unico verificador fraco decida a direcao.

2. **Verificador sem sinal nao e verificador.** Se `human_review_sample` = 0 (pending), ele nao entra no calculo de direcao. Nao presuma direcao a partir de silencio.

3. **A direcao pode ser INCORRECT mesmo com alguns verificadores positivos.** Se `deterministic_tests` = +1 mas `constraint_check` = -1 e `lint_rules` = -1, a direcao composta pode ser INCORRECT. O peso dos verificadores reflete sua confiabilidade relativa.

### Para a Matriz de Decisao

1. **REJECT e a decisao mais importante.** Interceptar uma sugestao de alta magnitude que esta incorreta e exatamente o que o sistema sem verifier nao faz. Cada REJECT e um falso positivo evitado.

2. **ESCALATE nao e falha — e higiene.** Alta magnitude + direcao incerta e o cenario mais perigoso: o agente esta convicto, mas nao ha como verificar. Escalar para um humano e a unica decisao responsavel. O custo de uma escalacao e uma revisao humana; o custo de aplicar uma correcao errada de alta confianca e um incidente em producao.

3. **DEFER e diferente de DISCARD.** DEFER significa "voltar a verificar depois" — a direcao pode se tornar clara com mais dados. DISCARD significa "essa sugestao e ruido" — baixa magnitude + direcao incorreta = nao vale o esforco de revisitar.

### Para a Trilha de Auditoria

1. **Nunca misture magnitude e direcao no mesmo campo.** Se um registro diz `confidence: 0.85`, nao fica claro se isso e confianca interna (magnitude) ou confianca na verificacao (direcao). Campos separados (`magnitude_composite`, `direction_verdict`) garantem rastreabilidade.

2. **O `rationale` deve ser acionavel.** Nao escreva "decisao baseada na matriz". Escreva "Alta magnitude (0.88) combinada com direcao INCORRECT (testes falharam, lint violado) → REJECT. Esta sugestao introduziria um null pointer risk que os testes detectaram."

---

## Duvidas Comuns

**P: Isso nao e so um Generator-Evaluator com pesos?**
R: E uma extensao do Generator-Evaluator. O Generator-Evaluator tradicional produz um veredito binario (bom/ruim). O Magnitude-Direction Split adiciona duas coisas: (1) a magnitude como sinal continuo de "o quanto isso importa", e (2) a separacao explicita entre confianca interna e verificacao externa na trilha de auditoria. O Generator-Evaluator diz "aceitar" ou "rejeitar". O Magnitude-Direction Split diz "aplicar com peso 0.9", "aplicar com peso 0.2", "rejeitar e registrar falso positivo", ou "escalar para humano".

**P: De onde vem os sinais de magnitude em um sistema real?**
R: Depende da implementacao. `self_distillation_delta` pode vir da comparacao entre o output do agente com e sem exemplos de referencia. `log_ratio` pode vir das log-probabilidades do modelo. `attention_hotspot` pode vir dos pesos de atencao do transformer. `disagreement_intensity` pode vir da variancia entre multiplas amostras do mesmo prompt. Em sistemas que nao expoem log-probabilidades, a magnitude pode ser inferida de heuristicas como "numero de alternativas consideradas" ou "intensidade da linguagem na justificativa".

**P: Como calibrar os thresholds de magnitude e direcao?**
R: Comece com os defaults (HIGH_MAGNITUDE_THRESHOLD = 0.70, DIRECTION_CONSENSUS_THRESHOLD = 0.60). Rode em shadow mode por N sessoes. Compare decisoes do corretor com ground truth humano. Ajuste thresholds para minimizar falsos positivos (REJECT quando ground truth e True) e falsos negativos (APPLY_HIGH quando ground truth e False). A calibracao e continua — reconfigure conforme o agente e os verificadores evoluem.

**P: O que acontece quando magnitude e direcao discordam sistematicamente?**
R: Isso e um sinal de que o agente esta sobre-confiante em cenarios onde os verificadores detectam problemas. E um problema de calibracao do agente, nao do corretor. O corretor esta funcionando corretamente ao rejeitar essas sugestoes. Mas a longo prazo, voce deve investigar por que o agente tem alta magnitude em correcoes incorretas — isso sugere vies no self-distillation ou exemplos de referencia contaminados.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/generator-evaluator|Generator-Evaluator]]` e compare: o Generator-Evaluator tradicional vs. o Magnitude-Direction Split.
2. Leia `[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]` — observe como a separacao builder/validator se relaciona com a separacao magnitude/direcao.
3. (Opcional) Estenda o corretor com `VerifierReliabilityTracking`: monitore a taxa de acordo de cada verificador com ground truth humano e ajuste os pesos de direcao dinamicamente.

---

*Exercicio Magnitude-Direction Verifier Split | Nivel 3 - Arquitetura Avancada*

**Confianca sem verificacao nao e qualidade — e information leakage.**
