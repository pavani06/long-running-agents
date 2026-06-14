---
title: "Exercício 8: Implementar Contextual Severity Calibration por Módulo"
type: curriculum-exercise
nivel: 3
aliases: ["contextual severity calibration", "calibração de severidade", "risk profile por módulo", "severidade contextual", "review depth ajustado por risco"]
tags: [curriculo-conteudo, nivel-3, exercicio, agentic-coding, evals, governanca, risk-calibration, severity-calibration, module-risk-profile, check-selection, blast-radius, false-positive-feedback, python, dataclass, yaml-risk-profile]
relates-to: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[curriculum/03-nivel-3-operational/exercises/exercise-shadow-review-pipeline|Shadow Review Pipeline Exercise]]"]
duration: "90-120 min"
last_updated: 2026-06-14
---
# ⚖️ Exercício 8: Implementar Contextual Severity Calibration por Módulo
## Nível 3 — Operacional

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter completado o Exercício 7 (Shadow Review Pipeline) e lido `eval-tier-stratification.md`, `constraint-anchored-evaluation.md`
**Objetivo:** Implementar um sistema de calibração de severidade que ajusta a profundidade e intensidade do AI code review com base no perfil de risco do módulo alterado, eliminando o modelo one-size-fits-all que sobre-revisa código de baixo risco e sub-revisa caminhos críticos

---

## 📖 Prólogo: O Help Page Que Custou Uma Hora

**Quinta-feira, 15h20. Sprint review.**

O time de checkout estava frustrado. Nas últimas três semanas, todo PR que tocava no módulo de pagamento vinha com 40+ findings do AI reviewer. O time passava mais tempo respondendo a falsos positivos do que revisando código de verdade.

```
Dev Checkout: "Olha isso. PR de 12 linhas. Mudei uma mensagem de erro 
              no gateway de pagamento. O bot gerou 47 findings."

Tech Lead: "47? Deixa eu ver... 'Consider using a connection pool' — 
          isso é um comment genérico. 'Avoid nested callbacks' — 
          o código não tem nested callbacks. Isso é ruído puro."

Dev Checkout: "E enquanto isso, o PR da Ana no módulo de pricing, que 
              mexe em cálculo de juros compostos, recebeu... 3 findings."

Tech Lead: "Três?! O pricing module é onde um erro de centavos vira 
          um rombo de milhões em 48 horas. Como que o bot foi tão 
          superficial lá e tão agressivo aqui?"
```

O problema tinha um nome: **one-size-fits-all review depth**. O AI reviewer tratava todo arquivo como igual. Um `README.md` e um `src/payment/settlement.py` recebiam exatamente os mesmos checks, com a mesma severidade.

A arquiteta do time, a Priya, abriu o editor e mostrou algo que ninguém tinha visto antes:

```
═══════════════════════════════════════════════════════════════
    IMPACTO DO REVIEW UNIFORME — ÚLTIMOS 90 DIAS (2.400 PRs)
═══════════════════════════════════════════════════════════════

MÓDULO                   PRs   FINDINGS  FPs    TEMPO GASTO
────────────────────────────────────────────────────────────
src/payment/settlement    180    8.400    1.200  340 horas
src/pricing/engine         95    1.900      180   76 horas
src/auth/login            210    9.800    3.400  290 horas
src/help/pages            340    5.100    2.100  140 horas  ← 41% FP!
README.md                  80    1.200      950   32 horas   ← 79% FP!!
CHANGELOG.md               45      680      620   18 horas   ← 91% FP!!!

GASTO TOTAL COM FALSOS POSITIVOS: 896 horas em 90 dias
CHECK CATEGORIES APLICADOS: 14 (todos os módulos recebem todos)
═══════════════════════════════════════════════════════════════
```

O time ficou em silêncio. 896 horas. Quase 10 horas por dia. Gasto com ruído.

```
Priya: "O problema não é o bot. O problema é que a gente não diz 
       para ele QUAIS módulos importam e QUANTO eles importam."

Dev Checkout: "Mas como a gente define isso?"

Priya: "Risk profile por módulo. Três níveis: critical, high, medium, 
       low. Para cada nível, um conjunto diferente de checks. Para 
       cada check, uma severidade calibrada."

Tech Lead: "Então no payment module a gente aplica TUDO. No README, 
           aplica... nada?"

Priya: "Quase. No README, aplica só markdown-lint e link-checker. 
       Não faz sentido rodar sql-injection num README. E a severidade 
       dos findings é ajustada: um null-safety no módulo de pricing 
       é CRITICAL. Um null-safety no módulo de help pages é LOW."

Dev Checkout: "E a severidade dentro do mesmo módulo? Se eu mexo no 
              arquivo de cálculo de juros vs. no arquivo de formatação 
              de output?"

Priya: "Aí entra a segunda camada: blast radius do arquivo específico. 
       Dentro do módulo de pricing, `interest_calculator.py` é risk=critical. 
       `price_formatter.py` é risk=low. O sistema combina: 
       risco do módulo × risco do arquivo = check set final."
```

Em três semanas, o time implementou o sistema. Os resultados:

```
═══════════════════════════════════════════════════════════════
   APÓS CALIBRAÇÃO — MESMO PERÍODO DE 90 DIAS (2.400 PRs)
═══════════════════════════════════════════════════════════════

MÓDULO                   PRs   FINDINGS  FPs    TEMPO GASTO
────────────────────────────────────────────────────────────
src/payment/settlement    180    9.200      210   370 horas
src/pricing/engine         95    4.100       45   164 horas  (+checks!)
src/auth/login            210    6.300      480   200 horas
src/help/pages            340      890       95    44 horas  (-83% ruido!)
README.md                  80      120       15     5 horas  (-97% ruido!!)

GASTO TOTAL COM FALSOS POSITIVOS: 168 horas (↓ 81%)
TEMPO DE REVIEW TOTAL: ↓ 42%
BUGS EM PRODUÇÃO ENCONTRADOS: ↑ 23% (mais checks nos lugares certos)
═══════════════════════════════════════════════════════════════
```

**A diferença não foi um modelo melhor. Foi dizer ao modelo onde olhar com mais cuidado e onde olhar com menos.**

Neste exercício, você vai construir esse sistema de calibração.

---

## 🎯 Objetivo

Você vai implementar um **Contextual Severity Calibration Engine** que:

1. Lê um arquivo `risk-profile.yaml` que define o perfil de risco de cada módulo e arquivo do repositório
2. Determina quais check categories aplicar com base no risk level do módulo alterado
3. Ajusta a severidade dos findings com base no risk level (ex: `null-safety` em `critical` → `severity=CRITICAL`, em `low` → `severity=LOW`)
4. Combina risco do módulo com risco do arquivo para determinar o check set final
5. Implementa um feedback loop que ajusta perfis de risco baseado em métricas históricas de falsos positivos
6. Simula a aplicação em um PR multi-arquivo e produz o check set calibrado

**Resultado Final:** Você entenderá como transformar "todos os módulos recebem todos os checks" em "cada módulo recebe exatamente os checks proporcionais ao seu risco operacional", eliminando o ruído que consome 81% do tempo de revisão.

---

## 📋 Cenário

### O Repositório MercuryPay

O MercuryPay tem 6 módulos principais, cada um com um perfil de risco diferente:

| Módulo | Risk Level | Blast Radius | O Que Acontece Se Falhar |
|---|---|---|---|
| `src/payment/settlement` | `critical` | Financeiro + Regulatório | Liquidações incorretas, multas do BC |
| `src/pricing/engine` | `critical` | Financeiro | Cálculo errado de juros = prejuízo acumulativo |
| `src/auth/login` | `high` | Segurança + Dados | Acesso não autorizado, vazamento de PII |
| `src/api/handlers` | `high` | Disponibilidade | API fora do ar, todas as integrações param |
| `src/notifications` | `medium` | Experiência | Clientes não recebem confirmações |
| `src/help/pages` | `low` | Imagem | Typo em página de ajuda |
| `README.md`, `CHANGELOG.md` | `low` | Nenhum | Documentação desatualizada |

### Os Check Categories Disponíveis

O AI reviewer tem 8 categorias de check. Nem todas fazem sentido para todos os módulos:

| Check Category | O Que Verifica | Custo (tokens) | Adequado Para |
|---|---|---|---|
| `security-surface` | Vulnerabilidades de segurança | Alto | critical, high |
| `sql-injection` | Strings interpoladas em queries | Alto | critical, high, medium |
| `null-safety` | Acessos sem null-check | Medio | critical, high, medium |
| `error-handling` | Exceções não tratadas | Medio | critical, high, medium, low |
| `data-integrity` | Consistência de dados transacionais | Alto | critical, high |
| `performance` | Loops ineficientes, queries N+1 | Medio | critical, high, medium |
| `naming-convention` | Nomes fora do padrão | Baixo | Todos |
| `style-formatting` | Espaçamento, indentação | Baixo | Todos |

### O Problema

Atualmente, todos os 8 checks são aplicados a todos os módulos. Isso significa que `README.md` recebe `security-surface` e `sql-injection` — checks que nunca encontrarão nada relevante lá, mas que consomem tokens, geram falsos positivos, e irritam os desenvolvedores.

### Sua Missão

Construir o engine de calibração. Definir `risk-profile.yaml`. Para cada PR, determinar quais checks aplicar com qual severidade, baseado nos arquivos alterados.

### Dados de Entrada

**Arquivo `risk-profile.yaml`:**

```yaml
schema_version: "1.0"
repository: "mercurypay"
last_updated: "2026-06-14"

# Global defaults
default_risk_level: "medium"

# Risk levels define check sets and severity calibration
risk_levels:
  critical:
    checks: [security-surface, sql-injection, null-safety, error-handling, data-integrity, performance, naming-convention, style-formatting]
    severity_multiplier: 1.5     # Findings tem severidade aumentada
    min_severity: "medium"       # Achados abaixo de medium sao suprimidos
  high:
    checks: [security-surface, sql-injection, null-safety, error-handling, data-integrity, naming-convention, style-formatting]
    severity_multiplier: 1.0
    min_severity: "low"
  medium:
    checks: [sql-injection, null-safety, error-handling, performance, naming-convention, style-formatting]
    severity_multiplier: 1.0
    min_severity: "low"
  low:
    checks: [error-handling, naming-convention, style-formatting]
    severity_multiplier: 0.5     # Findings tem severidade reduzida
    min_severity: "medium"       # So reporta findings medium+

# Module-level risk assignments
modules:
  - path: "src/payment/"
    risk_level: "critical"
    notes: "Financial settlement — errors cause regulatory fines"
  - path: "src/pricing/"
    risk_level: "critical"
    notes: "Interest calculation errors compound over time"
  - path: "src/auth/"
    risk_level: "high"
    notes: "Authentication — security boundary"
  - path: "src/api/"
    risk_level: "high"
    notes: "Public API surface — availability critical"
  - path: "src/notifications/"
    risk_level: "medium"
    notes: "Customer communications — non-critical"
  - path: "src/help/"
    risk_level: "low"
    notes: "Help pages — documentation only"

# File-level overrides (within modules)
file_overrides:
  - path: "src/pricing/interest_calculator.py"
    risk_level: "critical"
    notes: "Core compounding logic — highest blast radius"
  - path: "src/pricing/price_formatter.py"
    risk_level: "low"
    notes: "Output formatting only — no business logic"
  - path: "src/api/health_check.py"
    risk_level: "low"
    notes: "Health check endpoint — no data access"
  - path: "src/auth/login.py"
    risk_level: "critical"
    notes: "Login entry point — highest security sensitivity"

# Document files
document_patterns:
  - pattern: "README.md"
    risk_level: "low"
  - pattern: "CHANGELOG.md"
    risk_level: "low"
  - pattern: "*.md"
    risk_level: "low"

# Historical FP rates per module per check (do shadow pipeline)
# Usado para auto-ajustar: checks com FP > threshold perdem severidade
false_positive_thresholds:
  max_fp_rate: 0.30       # Se FP rate > 30% para um check neste modulo, reduz severidade
  recalibration_period_days: 90
```

---

## 📋 Requisitos

### Funcionais

- [ ] Engine lê `risk-profile.yaml` e constrói o mapa de risco em memória
- [ ] Para um PR com arquivos alterados, determina o risk level de cada arquivo (modulo + overrides)
- [ ] Para cada arquivo, seleciona o check set apropriado baseado no risk level
- [ ] Checks sao deduplicados: se 2 arquivos no mesmo PR pedem o mesmo check, ele e executado uma vez
- [ ] Para cada check aplicado, a severidade dos findings e calibrada pelo `severity_multiplier`
- [ ] Findings abaixo de `min_severity` sao filtrados (suprimidos)
- [ ] Engine calcula o custo total de tokens estimado para o PR baseado nos checks selecionados
- [ ] Suporte a feedback loop: atualiza `risk-profile.yaml` com base em FP rates historicos
- [ ] Output: `calibration_decision.json` com check set, severidade calibrada, e custo estimado

### Técnicos

- [ ] Python 3.9+ (type hints nativos)
- [ ] Usar apenas biblioteca padrao (`json`, `pathlib`, `datetime`, `dataclasses`, `typing`, `enum`, `yaml` — se yaml nao disponivel, usar JSON equivalente)
- [ ] NÃO usar frameworks externos para logica de negocio
- [ ] Dataclasses para modelos de dados
- [ ] Funcoes puras para resolucao de risco e selecao de checks
- [ ] Type hints em todas as funcoes publicas
- [ ] Docstrings no formato Google-style

### Validação

- [ ] Cenário 1 (critical module): arquivo em `src/payment/` → todos os 8 checks, severity 1.5x
- [ ] Cenário 2 (low module): arquivo em `src/help/` → 3 checks, severity 0.5x
- [ ] Cenário 3 (file override): `src/pricing/interest_calculator.py` → critical, mesmo modulo tendo mix de arquivos
- [ ] Cenário 4 (multi-file PR): PR com 3 arquivos em modulos diferentes → checks union, mas calibrados por arquivo
- [ ] Cenário 5 (dedup): 2 arquivos no mesmo modulo → cada check executado uma vez
- [ ] Cenário 6 (min_severity filter): modulo low so reporta findings medium+
- [ ] Cenário 7 (FP feedback): modulo com FP rate 45% em naming-convention → naming-convention removido do check set

---

## 🚀 Starter Code

```python
"""
Exercicio 8 — Contextual Severity Calibration por Modulo
Nivel 3 — Operacional

Implemente um engine que ajusta a profundidade e severidade do AI code
review baseado no perfil de risco do modulo alterado.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# DATA MODELS
# ============================================================================

class RiskLevel(Enum):
    """Niveis de risco do modulo/arquivo."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Severity(Enum):
    """Niveis de severidade de um finding."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CheckCategory(Enum):
    """Categorias de check disponiveis no AI reviewer."""
    SECURITY_SURFACE = "security-surface"
    SQL_INJECTION = "sql-injection"
    NULL_SAFETY = "null-safety"
    ERROR_HANDLING = "error-handling"
    DATA_INTEGRITY = "data-integrity"
    PERFORMANCE = "performance"
    NAMING_CONVENTION = "naming-convention"
    STYLE_FORMATTING = "style-formatting"


@dataclass
class RiskLevelConfig:
    """Configuracao de checks e severidade para um nivel de risco."""
    checks: list[str] = field(default_factory=list)
    severity_multiplier: float = 1.0
    min_severity: str = "low"

    def get_min_severity_enum(self) -> Severity:
        """Converte min_severity string para enum Severity."""
        severity_order = {
            "low": 0, "medium": 1, "high": 2, "critical": 3
        }
        return Severity(self.min_severity)


@dataclass
class ModuleRiskEntry:
    """Entrada de risco para um modulo (prefixo de path)."""
    path: str
    risk_level: str
    notes: str = ""


@dataclass
class FileOverride:
    """Override de risco para um arquivo especifico."""
    path: str
    risk_level: str
    notes: str = ""


@dataclass
class DocumentPattern:
    """Pattern para arquivos de documentacao."""
    pattern: str
    risk_level: str


@dataclass
class RiskProfile:
    """Perfil de risco completo do repositorio."""
    schema_version: str = "1.0"
    repository: str = ""
    last_updated: str = ""
    default_risk_level: str = "medium"
    risk_levels: dict[str, dict[str, Any]] = field(default_factory=dict)
    modules: list[dict[str, str]] = field(default_factory=list)
    file_overrides: list[dict[str, str]] = field(default_factory=list)
    document_patterns: list[dict[str, str]] = field(default_factory=list)
    false_positive_thresholds: dict[str, Any] = field(default_factory=dict)


@dataclass
class CalibratedCheck:
    """Um check calibrado para um arquivo especifico."""
    check: str
    risk_level: str          # Risk level do arquivo que gerou este check
    severity_multiplier: float
    min_severity: str        # Severidade minima para reportar


@dataclass
class CalibrationDecision:
    """Decisao de calibracao para um PR completo."""
    pr_id: str = ""
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    files_analyzed: list[dict[str, Any]] = field(default_factory=list)
    checks_to_apply: list[dict[str, Any]] = field(default_factory=list)
    checks_deduplicated: int = 0
    estimated_token_cost: int = 0
    risk_summary: dict[str, int] = field(default_factory=lambda: {
        "critical_files": 0,
        "high_files": 0,
        "medium_files": 0,
        "low_files": 0,
    })


# ============================================================================
# RISK PROFILE (hardcoded para o exercicio — em producao, viria de YAML)
# ============================================================================

def load_risk_profile() -> RiskProfile:
    """
    Carrega o perfil de risco do repositorio MercuryPay.

    Em producao, este metodo leria um arquivo risk-profile.yaml.
    Para o exercicio, os dados estao hardcoded para eliminar
    dependencia de parser YAML.

    Returns:
        RiskProfile completo com modulos, overrides e configs.
    """
    return RiskProfile(
        schema_version="1.0",
        repository="mercurypay",
        last_updated="2026-06-14",
        default_risk_level="medium",
        risk_levels={
            "critical": {
                "checks": ["security-surface", "sql-injection", "null-safety",
                          "error-handling", "data-integrity", "performance",
                          "naming-convention", "style-formatting"],
                "severity_multiplier": 1.5,
                "min_severity": "medium",
            },
            "high": {
                "checks": ["security-surface", "sql-injection", "null-safety",
                          "error-handling", "data-integrity",
                          "naming-convention", "style-formatting"],
                "severity_multiplier": 1.0,
                "min_severity": "low",
            },
            "medium": {
                "checks": ["sql-injection", "null-safety", "error-handling",
                          "performance", "naming-convention", "style-formatting"],
                "severity_multiplier": 1.0,
                "min_severity": "low",
            },
            "low": {
                "checks": ["error-handling", "naming-convention", "style-formatting"],
                "severity_multiplier": 0.5,
                "min_severity": "medium",
            },
        },
        modules=[
            {"path": "src/payment/", "risk_level": "critical",
             "notes": "Financial settlement — errors cause regulatory fines"},
            {"path": "src/pricing/", "risk_level": "critical",
             "notes": "Interest calculation errors compound over time"},
            {"path": "src/auth/", "risk_level": "high",
             "notes": "Authentication — security boundary"},
            {"path": "src/api/", "risk_level": "high",
             "notes": "Public API surface — availability critical"},
            {"path": "src/notifications/", "risk_level": "medium",
             "notes": "Customer communications — non-critical"},
            {"path": "src/help/", "risk_level": "low",
             "notes": "Help pages — documentation only"},
        ],
        file_overrides=[
            {"path": "src/pricing/interest_calculator.py", "risk_level": "critical",
             "notes": "Core compounding logic — highest blast radius"},
            {"path": "src/pricing/price_formatter.py", "risk_level": "low",
             "notes": "Output formatting — no business logic"},
            {"path": "src/api/health_check.py", "risk_level": "low",
             "notes": "Health check endpoint — no data access"},
            {"path": "src/auth/login.py", "risk_level": "critical",
             "notes": "Login entry point — highest security sensitivity"},
        ],
        document_patterns=[
            {"pattern": "README.md", "risk_level": "low"},
            {"pattern": "CHANGELOG.md", "risk_level": "low"},
            {"pattern": "*.md", "risk_level": "low"},
        ],
        false_positive_thresholds={
            "max_fp_rate": 0.30,
            "recalibration_period_days": 90,
        },
    )


# ============================================================================
# COST MODEL
# ============================================================================

# Tokens estimados por check category (valores simulados)
CHECK_TOKEN_COST: dict[str, int] = {
    "security-surface": 800,
    "sql-injection": 600,
    "null-safety": 400,
    "error-handling": 350,
    "data-integrity": 700,
    "performance": 500,
    "naming-convention": 200,
    "style-formatting": 150,
}


# ============================================================================
# CORE: RISK RESOLUTION
# ============================================================================

def resolve_file_risk(
    file_path: str,
    profile: RiskProfile,
) -> tuple[str, str]:
    """
    Determina o risk level de um arquivo consultando o perfil de risco.

    Ordem de precedencia:
    1. File-level override (match exato no path)
    2. Document pattern (ex: *.md → low)
    3. Module match (prefixo de path mais longo)
    4. Default risk level do perfil

    Args:
        file_path: Caminho do arquivo alterado (ex: "src/payment/gateway.py").
        profile: RiskProfile do repositorio.

    Returns:
        Tupla com (risk_level, source) onde source indica qual regra foi aplicada.
        Ex: ("critical", "module:src/payment/"), ("low", "override:src/pricing/price_formatter.py")
    """
    # TODO: Implementar resolucao de risco
    #
    # Algoritmo sugerido:
    # 1. Verificar file_overrides por match exato no path
    #    - Se encontrado, retornar (risk_level, "override:{path}")
    #
    # 2. Verificar document_patterns:
    #    - Para cada pattern, verificar se file_path corresponde
    #    - Patterns podem ser exatos ("README.md") ou glob ("*.md")
    #    - Se encontrado, retornar (risk_level, "pattern:{pattern}")
    #
    # 3. Verificar modules (prefixo de path):
    #    - Ordenar modules por len(path) decrescente para priorizar
    #      match mais especifico (ex: "src/payment/gateway/" > "src/")
    #    - Se file_path comeca com module.path, retornar (risk_level, "module:{path}")
    #
    # 4. Fallback: retornar (profile.default_risk_level, "default")
    pass


def get_check_set(
    risk_level: str,
    profile: RiskProfile,
) -> RiskLevelConfig:
    """
    Retorna a configuracao de checks para um determinado risk level.

    Args:
        risk_level: String do risk level ("critical", "high", "medium", "low").
        profile: RiskProfile com definicoes de risk_levels.

    Returns:
        RiskLevelConfig com checks, severity_multiplier, e min_severity.
    """
    # TODO: Implementar obtencao de check set
    #
    # Algoritmo sugerido:
    # 1. Obter config do profile.risk_levels[risk_level]
    # 2. Construir e retornar RiskLevelConfig com os campos
    # 3. Se risk_level nao encontrado, usar "medium" como fallback
    pass


# ============================================================================
# CORE: SEVERITY CALIBRATION
# ============================================================================

def calibrate_severity(
    base_severity: str,
    multiplier: float,
) -> str:
    """
    Ajusta a severidade de um finding pelo multiplier do risk level.

    Mapeamento de severidades para indice numerico:
      low=0, medium=1, high=2, critical=3

    O multiplier e aplicado ao indice e o resultado e clampado em [0, 3].

    Exemplos:
      base="medium"(1) × 1.5 = 1.5 → round para 2 → "high"
      base="high"(2) × 1.5 = 3.0 → "critical"
      base="medium"(1) × 0.5 = 0.5 → round para 1 → "medium" (sem mudanca)
      base="low"(0) × 1.5 = 0.0 → "low" (nao sobe)

    Args:
        base_severity: Severidade original do finding.
        multiplier: Multiplier do risk level (0.5, 1.0, 1.5).

    Returns:
        Severidade calibrada como string.
    """
    # TODO: Implementar calibracao de severidade
    #
    # Algoritmo sugerido:
    # 1. Mapear base_severity para indice numerico (0-3)
    # 2. Calcular calibrated_index = round(base_index * multiplier)
    # 3. Clampar em [0, 3]
    # 4. Mapear de volta para string de severidade
    pass


def should_report_finding(
    finding_severity: str,
    min_severity: str,
) -> bool:
    """
    Decide se um finding deve ser reportado baseado na severidade minima.

    Args:
        finding_severity: Severidade calibrada do finding.
        min_severity: Severidade minima configurada para o risk level.

    Returns:
        True se o finding deve ser reportado.
    """
    # TODO: Implementar filtro de severidade minima
    #
    # Algoritmo sugerido:
    # 1. Mapear ambas severidades para indice numerico (0-3)
    # 2. Retornar finding_index >= min_index
    pass


# ============================================================================
# CORE: CALIBRATION ENGINE
# ============================================================================

def calibrate_pr(
    pr_id: str,
    files_changed: list[str],
    profile: RiskProfile,
    historical_fp_rates: Optional[dict[str, dict[str, float]]] = None,
) -> CalibrationDecision:
    """
    Engine principal: determina checks e severidades para um PR.

    Fluxo:
    1. Para cada arquivo alterado, resolve o risk level
    2. Determina o check set para cada risk level encontrado
    3. Deduplica checks (mesmo check em 2 arquivos → executado 1 vez)
    4. Para cada check, registra severity_multiplier e min_severity
    5. Se historical_fp_rates fornecido, remove checks com FP rate > threshold
    6. Calcula custo estimado de tokens

    Args:
        pr_id: ID do PR.
        files_changed: Lista de paths dos arquivos alterados.
        profile: RiskProfile do repositorio.
        historical_fp_rates: Metricas historicas de FP por modulo e check (opcional).
            Formato: {"src/payment/": {"naming-convention": 0.45, ...}, ...}

    Returns:
        CalibrationDecision com check set calibrado.
    """
    # TODO: Implementar o engine de calibracao
    #
    # Algoritmo sugerido:
    # 1. Criar CalibrationDecision com pr_id
    #
    # 2. Para cada file_path em files_changed:
    #    a. risk_level, source = resolve_file_risk(file_path, profile)
    #    b. Adicionar em decision.files_analyzed:
    #       {"file": file_path, "risk_level": risk_level, "source": source}
    #    c. Incrementar decision.risk_summary[f"{risk_level}_files"]
    #
    # 3. Coletar checks de cada arquivo:
    #    a. Para cada file_path, obter RiskLevelConfig via get_check_set()
    #    b. Para cada check na config, criar entrada com:
    #       - check, risk_level, severity_multiplier, min_severity
    #    c. Acumular em um dict indexado por check
    #
    # 4. Deduplicar:
    #    a. Para checks que aparecem de multiplos arquivos:
    #       - Usar o MAIOR severity_multiplier e a MAIOR min_severity
    #         (principio conservador: se um arquivo critical pede o check,
    #          aplica-se com severidade de critical)
    #    b. Contar checks antes e depois da dedup
    #
    # 5. Se historical_fp_rates fornecido:
    #    a. Para cada modulo dos arquivos alterados, consultar FP rates
    #    b. Se FP rate de um check > profile.false_positive_thresholds["max_fp_rate"],
    #       remover o check do set
    #    c. Registrar checks removidos por FP feedback
    #
    # 6. Calcular estimated_token_cost:
    #    a. Somar CHECK_TOKEN_COST[check] para cada check em checks_to_apply
    #
    # 7. Preencher decision.checks_to_apply com lista de dicts
    # 8. Preencher decision.checks_deduplicated
    # 9. Retornar decision
    pass


# ============================================================================
# SIMULATED PRs
# ============================================================================

def get_sample_prs() -> list[dict[str, Any]]:
    """Retorna PRs simulados para teste."""
    return [
        {
            "pr_id": "PR-CRITICAL-001",
            "description": "PR no modulo de pagamento — maximo escrutinio",
            "files_changed": [
                "src/payment/gateway.py",
                "src/payment/settlement.py",
            ],
            "expected_checks": 8,   # Todos os 8 checks
            "expected_multiplier": 1.5,
        },
        {
            "pr_id": "PR-LOW-002",
            "description": "PR no modulo de help pages — minimo escrutinio",
            "files_changed": [
                "src/help/faq.py",
                "README.md",
            ],
            "expected_checks": 3,   # error-handling, naming-convention, style-formatting
            "expected_multiplier": 0.5,
        },
        {
            "pr_id": "PR-MIXED-003",
            "description": "PR multi-modulo com arquivos de riscos diferentes",
            "files_changed": [
                "src/pricing/interest_calculator.py",  # critical (override)
                "src/pricing/price_formatter.py",       # low (override)
                "src/api/health_check.py",              # low (override)
            ],
            "expected_checks": 8,   # Union de todos os checks (critical domina)
        },
        {
            "pr_id": "PR-OVERRIDE-004",
            "description": "File override: login.py e critical, nao high",
            "files_changed": [
                "src/auth/login.py",      # critical (override)
                "src/auth/session.py",    # high (module default)
            ],
            "expected_checks": 8,   # critical domina sobre high
        },
    ]


# ============================================================================
# TESTS
# ============================================================================

def test_cenario_1_critical_module():
    """Cenario 1: modulo critical → todos os checks, severity 1.5x."""
    print("\n" + "=" * 60)
    print("TESTE 1: Modulo Critical — Maximo Escrutinio")
    print("=" * 60)

    profile = load_risk_profile()
    decision = calibrate_pr(
        "PR-TEST-1",
        ["src/payment/gateway.py"],
        profile,
    )

    # Deve ter 1 arquivo analisado como critical
    assert decision.risk_summary["critical_files"] == 1
    assert decision.risk_summary["high_files"] == 0
    assert decision.risk_summary["low_files"] == 0

    # Deve ter 8 checks (todos)
    check_names = [c["check"] for c in decision.checks_to_apply]
    assert len(check_names) == 8, f"Esperado 8 checks, obtido {len(check_names)}"

    # Todos os checks devem ter multiplier 1.5 e min_severity medium
    for c in decision.checks_to_apply:
        assert c["severity_multiplier"] == 1.5, (
            f"Check {c['check']}: esperado multiplier 1.5, obtido {c['severity_multiplier']}"
        )
        assert c["min_severity"] == "medium", (
            f"Check {c['check']}: esperado min_severity medium, obtido {c['min_severity']}"
        )

    # Deve ter custo de tokens > 0
    assert decision.estimated_token_cost > 0

    print(f"  Arquivos critical: {decision.risk_summary['critical_files']}")
    print(f"  Checks aplicados: {len(check_names)}")
    print(f"  Custo estimado tokens: {decision.estimated_token_cost}")
    print("  Teste 1 passou!")


def test_cenario_2_low_module():
    """Cenario 2: modulo low → 3 checks, severity 0.5x."""
    print("\n" + "=" * 60)
    print("TESTE 2: Modulo Low — Minimo Escrutinio")
    print("=" * 60)

    profile = load_risk_profile()
    decision = calibrate_pr(
        "PR-TEST-2",
        ["src/help/faq.py"],
        profile,
    )

    assert decision.risk_summary["low_files"] == 1

    check_names = [c["check"] for c in decision.checks_to_apply]
    assert len(check_names) == 3, f"Esperado 3 checks, obtido {len(check_names)}"

    # Verificar que os checks corretos estao presentes
    assert "error-handling" in check_names
    assert "naming-convention" in check_names
    assert "style-formatting" in check_names

    # Verificar que security-surface e sql-injection NAO estao
    assert "security-surface" not in check_names
    assert "sql-injection" not in check_names

    # Todos devem ter multiplier 0.5 e min_severity medium
    for c in decision.checks_to_apply:
        assert c["severity_multiplier"] == 0.5
        assert c["min_severity"] == "medium"

    print(f"  Arquivos low: {decision.risk_summary['low_files']}")
    print(f"  Checks aplicados: {check_names}")
    print(f"  Custo estimado tokens: {decision.estimated_token_cost}")
    print("  Teste 2 passou!")


def test_cenario_3_file_override():
    """Cenario 3: file override → interest_calculator.py e critical."""
    print("\n" + "=" * 60)
    print("TESTE 3: File Override — interest_calculator.py")
    print("=" * 60)

    profile = load_risk_profile()

    # Resolver risco do arquivo com override
    risk, source = resolve_file_risk("src/pricing/interest_calculator.py", profile)
    assert risk == "critical", f"Esperado critical, obtido {risk}"
    assert "override" in source, f"Esperado source 'override', obtido {source}"

    # Resolver risco do price_formatter (override para low)
    risk2, source2 = resolve_file_risk("src/pricing/price_formatter.py", profile)
    assert risk2 == "low", f"Esperado low, obtido {risk2}"

    # Resolver risco do health_check (override para low)
    risk3, source3 = resolve_file_risk("src/api/health_check.py", profile)
    assert risk3 == "low", f"Esperado low, obtido {risk3}"

    # Resolver risco do login.py (override para critical)
    risk4, source4 = resolve_file_risk("src/auth/login.py", profile)
    assert risk4 == "critical", f"Esperado critical, obtido {risk4}"

    print(f"  interest_calculator.py: {risk} ({source})")
    print(f"  price_formatter.py: {risk2} ({source2})")
    print(f"  health_check.py: {risk3} ({source3})")
    print(f"  login.py: {risk4} ({source4})")
    print("  Teste 3 passou!")


def test_cenario_4_multi_file_pr():
    """Cenario 4: PR multi-arquivo com mix de riscos."""
    print("\n" + "=" * 60)
    print("TESTE 4: PR Multi-Arquivo — Mix de Riscos")
    print("=" * 60)

    profile = load_risk_profile()
    decision = calibrate_pr(
        "PR-TEST-4",
        [
            "src/pricing/interest_calculator.py",  # critical
            "src/pricing/price_formatter.py",       # low
        ],
        profile,
    )

    # Deve ter 1 critical e 1 low
    assert decision.risk_summary["critical_files"] == 1
    assert decision.risk_summary["low_files"] == 1

    # Checks devem ser a uniao (critical domina → todos os 8)
    check_names = [c["check"] for c in decision.checks_to_apply]
    assert len(check_names) == 8, (
        f"Union de checks deve ser 8 (critical domina), obtido {len(check_names)}"
    )

    # Mas o arquivo low nao deve forcar min_severity medium nos checks
    # que ele nao pediu — isso e tratado na dedup (maior severidade ganha)

    print(f"  Arquivos: 1 critical + 1 low")
    print(f"  Checks aplicados: {len(check_names)}")
    print(f"  Custo estimado tokens: {decision.estimated_token_cost}")
    print("  Teste 4 passou!")


def test_cenario_5_deduplication():
    """Cenario 5: 2 arquivos no mesmo modulo → checks deduplicados."""
    print("\n" + "=" * 60)
    print("TESTE 5: Deduplicacao de Checks")
    print("=" * 60)

    profile = load_risk_profile()
    decision = calibrate_pr(
        "PR-TEST-5",
        [
            "src/payment/gateway.py",
            "src/payment/settlement.py",
        ],
        profile,
    )

    # Ambos sao critical → 8 checks esperados, nao 16
    check_names = [c["check"] for c in decision.checks_to_apply]
    assert len(check_names) == 8, (
        f"Esperado 8 checks deduplicados, obtido {len(check_names)}"
    )

    # Verificar que nao ha duplicatas
    assert len(check_names) == len(set(check_names)), (
        "Checks nao devem ter duplicatas"
    )

    # checks_deduplicated deve registrar quantos foram removidos
    assert decision.checks_deduplicated > 0, (
        "Deve registrar checks deduplicados"
    )

    print(f"  Arquivos: 2 (ambos critical)")
    print(f"  Checks apos dedup: {len(check_names)}")
    print(f"  Checks deduplicados: {decision.checks_deduplicated}")
    print("  Teste 5 passou!")


def test_cenario_6_min_severity_filter():
    """Cenario 6: modulo low → so reporta findings medium+."""
    print("\n" + "=" * 60)
    print("TESTE 6: Filtro de Severidade Minima")
    print("=" * 60)

    # Severity calibration: low × 1.5 = ainda low se base for low
    calibrated = calibrate_severity("low", 1.5)
    assert calibrated == "low", (
        f"low × 1.5 deve continuar low, obtido {calibrated}"
    )

    # Severity calibration: medium × 1.5 → high
    calibrated2 = calibrate_severity("medium", 1.5)
    assert calibrated2 == "high", f"medium × 1.5 deve ser high, obtido {calibrated2}"

    # Severity calibration: high × 1.5 → critical
    calibrated3 = calibrate_severity("high", 1.5)
    assert calibrated3 == "critical", f"high × 1.5 deve ser critical, obtido {calibrated3}"

    # Severity calibration: medium × 0.5 → low
    calibrated4 = calibrate_severity("medium", 0.5)
    assert calibrated4 == "low", f"medium × 0.5 deve ser low, obtido {calibrated4}"

    # Min severity filter: modulo low (min_severity=medium)
    # Um finding de severity "low" NAO deve ser reportado
    assert should_report_finding("low", "medium") == False
    assert should_report_finding("medium", "medium") == True
    assert should_report_finding("high", "medium") == True

    print(f"  low × 1.5 → {calibrated}")
    print(f"  medium × 1.5 → {calibrated2}")
    print(f"  high × 1.5 → {calibrated3}")
    print(f"  medium × 0.5 → {calibrated4}")
    print(f"  should_report(low, medium) → False")
    print(f"  should_report(medium, medium) → True")
    print("  Teste 6 passou!")


def test_cenario_7_fp_feedback_loop():
    """Cenario 7: FP feedback remove checks com alta taxa de falsos positivos."""
    print("\n" + "=" * 60)
    print("TESTE 7: Feedback Loop — Remocao por FP Rate")
    print("=" * 60)

    profile = load_risk_profile()

    # Simular FP rates do shadow pipeline: naming-convention no modulo
    # de payment tem 45% de FP rate (acima do threshold de 30%)
    fp_rates = {
        "src/payment/": {
            "naming-convention": 0.45,  # 45% FP → deve ser removido
            "style-formatting": 0.25,   # 25% FP → abaixo do threshold, mantido
        },
        "src/pricing/": {
            "performance": 0.55,  # 55% FP → deve ser removido
        },
    }

    decision = calibrate_pr(
        "PR-TEST-7",
        ["src/payment/gateway.py"],
        profile,
        historical_fp_rates=fp_rates,
    )

    check_names = [c["check"] for c in decision.checks_to_apply]

    # naming-convention deve ter sido removido (FP 45% > 30%)
    assert "naming-convention" not in check_names, (
        "naming-convention com 45% FP deve ser removido"
    )

    # style-formatting deve permanecer (FP 25% <= 30%)
    assert "style-formatting" in check_names, (
        "style-formatting com 25% FP deve permanecer"
    )

    # security-surface, sql-injection, etc. devem permanecer (sem FP data)
    assert "security-surface" in check_names
    assert "sql-injection" in check_names

    print(f"  Checks aplicados: {check_names}")
    print(f"  Checks removidos por FP: naming-convention (45% FP)")
    print(f"  Checks mantidos com FP baixo: style-formatting (25% FP)")
    print("  Teste 7 passou!")


def test_severity_calibration_edge_cases():
    """Testes de borda para calibrate_severity."""
    print("\n" + "=" * 60)
    print("TESTE EXTRA: Edge Cases de Severidade")
    print("=" * 60)

    # critical × 1.5 → critical (ja no maximo)
    assert calibrate_severity("critical", 1.5) == "critical"

    # low × 0.5 → low (ja no minimo)
    assert calibrate_severity("low", 0.5) == "low"

    # critical × 0.5 → medium (reducao)
    result = calibrate_severity("critical", 0.5)
    assert result in ("medium", "high"), f"critical × 0.5 deve ser medium ou high, obtido {result}"

    print("  Edge cases passaram!")
    print(f"  critical × 1.5 → critical (clampado)")
    print(f"  low × 0.5 → low (clampado)")
    print(f"  critical × 0.5 → {result} (reduzido)")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCICIO 8: CONTEXTUAL SEVERITY CALIBRATION")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_cenario_1_critical_module()
    # test_cenario_2_low_module()
    # test_cenario_3_file_override()
    # test_cenario_4_multi_file_pr()
    # test_cenario_5_deduplication()
    # test_cenario_6_min_severity_filter()
    # test_cenario_7_fp_feedback_loop()
    # test_severity_calibration_edge_cases()

    print("\nTODO: Implemente as funcoes acima!")
    print("   1. resolve_file_risk() — resolucao de risco com precedencia")
    print("   2. get_check_set() — obtencao de checks por risk level")
    print("   3. calibrate_severity() — ajuste de severidade por multiplier")
    print("   4. should_report_finding() — filtro de severidade minima")
    print("   5. calibrate_pr() — engine principal de calibracao")
    print("   Apos implementar, descomente os testes em main()")
```

---

## 🏗️ Como Comecar

### Passo 1: Implementar Resolucao de Risco (20 min)

`resolve_file_risk` e a funcao mais importante — toda decisao de calibracao depende dela. A ordem de precedencia e:

1. **File override** (match exato): `src/auth/login.py` → risk `critical`
2. **Document pattern** (match por glob): `README.md` → risk `low`
3. **Module match** (prefixo de path, mais longo primeiro): `src/payment/gateway.py` → risk `critical`
4. **Default**: risk `medium`

Dica: para module match, ordene os modulos por `len(path)` decrescente. Assim `src/payment/gateway/` tem precedencia sobre `src/`.

### Passo 2: Implementar Calibracao de Severidade (15 min)

`calibrate_severity` usa um modelo simples de indice × multiplier:

```
severity_index = {"low": 0, "medium": 1, "high": 2, "critical": 3}
calibrated = round(index * multiplier)
clamped = max(0, min(3, calibrated))
```

Isso significa que:
- `low(0) × 1.5 = 0` → `low` (nao sobe sozinho)
- `medium(1) × 1.5 = 1.5 → 2` → `high`
- `high(2) × 1.5 = 3` → `critical`

### Passo 3: Implementar Filtro de Severidade Minima (10 min)

`should_report_finding` compara a severidade calibrada com a `min_severity` do risk level. Para modulos `low`, `min_severity = "medium"`, entao findings `low` sao suprimidos. Isso reduz ruido em modulos de baixo risco.

### Passo 4: Implementar o Engine de Calibracao (30 min)

`calibrate_pr` e o orquestrador que junta tudo:

1. Para cada arquivo, resolve o risco
2. Coleta os checks de cada risk level
3. Deduplica: mesma check category em 2 arquivos → 1 execucao
4. Na dedup, usa o **maior** severity_multiplier e a **maior** min_severity (principio conservador: se um arquivo critical e um low compartilham um check, aplica-se com severidade de critical)
5. Se houver dados historicos de FP, remove checks com FP rate acima do threshold
6. Calcula custo de tokens

### Passo 5: Implementar o Feedback Loop (15 min)

O feedback loop usa metricas do Shadow Review Pipeline (Exercicio 7) para auto-ajustar o perfil de risco:

- Se um check tem FP rate > 30% em um modulo especifico, ele e removido do check set para aquele modulo
- Isso fecha o ciclo: shadow pipeline → FP data → severity calibration → menos ruido → mais confianca

---

## ✅ Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

```python
# 1. Resolucao de risco com precedencia correta
risk, source = resolve_file_risk("src/auth/login.py", profile)
assert risk == "critical"  # override vence module
assert "override" in source

risk, source = resolve_file_risk("src/auth/session.py", profile)
assert risk == "high"  # module default

risk, source = resolve_file_risk("README.md", profile)
assert risk == "low"   # document pattern

# 2. Check set correto por risk level
config = get_check_set("critical", profile)
assert len(config.checks) == 8
assert config.severity_multiplier == 1.5

config = get_check_set("low", profile)
assert len(config.checks) == 3
assert config.severity_multiplier == 0.5

# 3. Calibracao de severidade
assert calibrate_severity("medium", 1.5) == "high"
assert calibrate_severity("high", 1.5) == "critical"
assert calibrate_severity("medium", 0.5) == "low"

# 4. Filtro de severidade minima
assert should_report_finding("low", "medium") == False
assert should_report_finding("medium", "medium") == True

# 5. PR multi-arquivo com dedup
decision = calibrate_pr("PR-X", ["src/payment/a.py", "src/payment/b.py"], profile)
assert len(decision.checks_to_apply) == 8  # dedup: nao 16

# 6. PR mixed risk → union de checks
decision = calibrate_pr("PR-Y", 
    ["src/pricing/interest_calculator.py", "src/help/faq.py"], profile)
# critical domina → 8 checks, nao 3
assert len(decision.checks_to_apply) == 8

# 7. FP feedback remove checks
decision = calibrate_pr("PR-Z", ["src/payment/gateway.py"], profile,
    historical_fp_rates={"src/payment/": {"naming-convention": 0.45}})
assert "naming-convention" not in [c["check"] for c in decision.checks_to_apply]
```

---

## 📊 Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Risk Resolution (Passo 1)** | 20% | Nao resolve ou sempre default | Module match apenas | + File overrides | + Document patterns, longest-prefix |
| **Severity Calibration (Passo 2)** | 15% | Nao implementado | Multiplica sem clamp | + Clamp e round | + Edge cases (critical×1.5, low×0.5) |
| **Min Severity Filter (Passo 3)** | 10% | Nao implementado | Filtro basico | + Mapeamento correto de severidades | + Integrado ao engine |
| **Calibration Engine (Passo 4)** | 30% | Nao orquestra | Checks por arquivo, sem dedup | + Dedup, maior severidade ganha | + Custo de tokens, multi-arquivo |
| **FP Feedback (Passo 5)** | 15% | Nao implementado | Remove checks com FP fixo | + Threshold configuravel | + Por modulo, nao global |
| **Testes** | 10% | Nenhum cenario passa | 2-3 cenarios passam | 5-6 cenarios passam | Todos os 7+ cenarios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## 🎯 Desafios Extra

### Desafio 1: Risk Profile Auto-Generator

Implemente um script que analisa o historico de git do repositorio e gera um `risk-profile.yaml` inicial baseado em:
- Frequencia de bugs por arquivo (via `git log --grep="fix"`)
- Blast radius (quantos arquivos importam este modulo)
- Churn rate (quantas vezes o arquivo foi alterado nos ultimos 6 meses)

### Desafio 2: Severity Decay com Confianca

Implemente um mecanismo de "severity decay": se um check tem precision > 95% por mais de 60 dias, sua severidade e reduzida (confia-se mais no check, menos necessidade de alarme alto). O inverso tambem: se precision cai, severidade sobe.

### Desafio 3: Integracao com Shadow Review Pipeline

Conecte os dois exercicios: o output do Exercicio 7 (FP rates por modulo e check) alimenta automaticamente o engine de calibracao do Exercicio 8. O pipeline completo: shadow period → FP data → calibration → check selection → novo shadow period → recalibracao.

---

## 🎓 O Que Voce Aprendeu

Apos completar este exercicio, voce entende:

- Por que one-size-fits-all review depth causa 81% de ruido em modulos de baixo risco enquanto sub-revisa caminhos criticos
- Como definir risk profiles por modulo e arquivo que refletem o blast radius e custo de falha reais
- Como calibrar a severidade dos findings com base no contexto do modulo (critical → severidade aumentada, low → severidade reduzida)
- Como selecionar check sets proporcionais ao risco (README.md nao precisa de sql-injection)
- Como usar dados historicos de falsos positivos para auto-ajustar o perfil de risco (feedback loop)
- Como a calibracao contextual reduz o tempo de review em 42% enquanto aumenta a deteccao de bugs em 23%

**Prerequisite chain:** Exercicio 7 (Shadow Review Pipeline) → Exercicio 8 (Contextual Severity Calibration). O shadow pipeline gera os dados de FP que alimentam a calibracao.

---

*Exercicio 8 | Nivel 3 — Operacional | Contextual Severity Calibration*
