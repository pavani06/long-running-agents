---
title: "Exercício 4: Refatorar o Harness como Compilador Fuzzy"
type: curriculum-exercise
nivel: 3
aliases: ["llm as fuzzy compiler", "compilador fuzzy", "codigo descartavel", "harness optimization passes", "modelo como backend", "durable harness assets"]
tags: [curriculo-conteudo, nivel-3, exercicio, harness-evolution, model-upgrade, compiler-passes, harness-assets, disposable-code, invariant-compensation, python, dataclass, architecture-review]
relates-to: ["[[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"]
last_updated: 2026-06-11
---

# 🧬 Exercício 4: Refatorar o Harness como Compilador Fuzzy
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 75-105 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter completado `05-harness-evolution.md` + Exercício 3 (Plano de Evolução do Harness)
**Objetivo:** Internalizar o modelo mental "LLM = compilador fuzzy, harness = passes de otimização, código = artefato de build descartável" e implementar um sistema que sobrevive a trocas de modelo sem perder qualidade

---

## 📖 Prólogo: A Migração Que Deletou Seis Meses de Trabalho

**Terça-feira, 9h15. Sala de reunião do time de plataforma.**

A migração era para ser simples. Trocar o Claude 3.5 pelo Claude 4. O changelog prometia: "melhor em tudo". Contexto maior, reasoning mais preciso, menos alucinações. A diretoria estimou duas semanas de adaptação.

O que aconteceu em vez disso:

```
═══════════════════════════════════════════════════════════════
        RELATÓRIO DE MIGRAÇÃO — CLAUDE 3.5 → CLAUDE 4
                 Semanas 1-6 (ATRASO: 4 semanas)
═══════════════════════════════════════════════════════════════

SEMANA 1: "Só ajustar os prompts"
  └─ Modelo novo ignorava system prompt. Outputs mal formatados.
  └─ 47 testes quebrando. Time reescreve 12 prompts.

SEMANA 2: "Precisa refinar os exemplos few-shot"
  └─ Modelo interpretava exemplos de forma diferente.
  └─ 31 testes quebrando. Time reescreve 89 exemplos.

SEMANA 3: "As constraints não estão sendo respeitadas"
  └─ Budget Checker falhava em 23% dos casos.
  └─ Time ajusta thresholds e reescreve constraint logic.

SEMANA 4: "Descobrimos que o modelo novo NÃO PRECISA de..."
  └─ Dedup Layer: completamente desnecessária (janela 500K).
  └─ Format Validator: JSON mode nativo cobre 100% dos casos.
  └─ Priority Extractor: modelo prioriza system prompt automaticamente.
  └─ Três componentes que custaram 8 semanas de desenvolvimento
     são agora código morto. Mas ninguém sabia DISSO quando foram
     escritos — eram essenciais para o modelo antigo.

SEMANA 5: "Vamos reescrever o Generator do zero"
  └─ O modelo novo gera código diferente. Os padrões antigos não
     aproveitam as capacidades novas. O time reescreve 3.400 linhas
     que funcionavam perfeitamente na semana 0.

SEMANA 6: "E os reviewers?"
  └─ Reviewer Agent treinado nos padrões do modelo antigo.
  └─ Começa a rejeitar código CORRETO do modelo novo.
  └─ Time precisa reescrever as rubricas de review também.

RESULTADO APÓS 6 SEMANAS:
  Código reescrito:       6.200 linhas (41% do codebase)
  Testes quebrados:       143 (corrigidos ou deletados)
  Componentes obsoletos:  3 (removidos)
  Prompts reescritos:     27
  Atraso:                 4 semanas
  LIÇÕES APRENDIDAS:      Nenhuma formalizada
═══════════════════════════════════════════════════════════════
```

Na sexta-feira da semana 6, durante a retrospectiva, a arquiteta do time — Mariana — projetou um slide que mudou a conversa:

```
O QUE A GENTE PRESERVOU (ERRADO):
  ✅ 6.200 linhas de código gerado
  ✅ 27 prompts específicos do modelo antigo
  ✅ 89 exemplos few-shot do modelo antigo
  ✅ 3 componentes que só existiam por limitação do modelo antigo

O QUE A GENTE DEVERIA TER PRESERVADO (CERTO):
  ❌ O conhecimento de que "clientes alérgicos NUNCA recebem lactose"
  ❌ A regra de que "orçamento é constraint, não sugestão"
  ❌ O padrão de que "toda recomendação tem evidência de produto"
  ❌ A estrutura de que "avaliação é separada de geração"
```

```
Mariana: "A gente passou seis semanas reescrevendo código. Mas o
         código NÃO ERA o ativo. O ativo eram as constraints, as
         regras de domínio, os invariantes. O código era só o output
         de um compilador que a gente trocou."

Dev Senior: "Mas como a gente preserva as constraints sem preservar
             o código?"

Mariana: "Pensa no LLM como um compilador. Você não preserva o
         binário quando troca de compilador — você preserva o
         source. Nosso 'source' são as constraints de domínio,
         as regras de negócio, as rubricas de qualidade. O código
         gerado é o 'binário' — descartável e regenerável."

Dev Junior: "Então quando o modelo melhora, a gente... recompila?"

Mariana: "Exatamente. Você mantém o mesmo source — as mesmas
         constraints de 'cliente alérgico nunca recebe produto
         com alérgeno'. E deixa o novo compilador gerar código
         novo que satisfaz essas constraints. Se o compilador
         melhorou, o código gerado melhora também. Zero rewrites."
```

Ela abriu um arquivo e mostrou:

```
ANTES (preservando código):
  ├── src/generated/koda_agent_v35.py     ← reescrito na migração
  ├── src/generated/koda_agent_v4.py      ← versão nova
  └── src/generated/... (8 versões acumuladas)

DEPOIS (preservando constraints):
  ├── harness/constraints/
  │   ├── domain_invariants.json    ← "alergias são bloqueantes"
  │   ├── budget_rules.json         ← "preço <= orçamento declarado"
  │   └── quality_rubrics.json      ← "explicação fundamentada"
  ├── harness/passes/
  │   ├── lint_pass.py              ← verifica padrões de código
  │   ├── type_check_pass.py        ← verifica tipos
  │   └── reviewer_pass.py          ← verifica contra rubrics
  └── output/                        ← REGENERADO a cada modelo novo
      └── koda_agent.py              ← descartável
```

```
Mariana: "O harness é um compilador. Os passes são otimizações.
         Trocar o modelo é trocar o backend. O source — as
         constraints — sobrevive a qualquer backend."
```

**Agora é a sua vez.**

Você é o arquiteto que vai implementar esse harness-compilador. Você tem as constraints de domínio do KODA, os passes de otimização, e dois backends diferentes. Sua missão: construir um sistema onde trocar o modelo não destrói seis meses de trabalho — apenas regenera o artefato final.

---

## 🎯 O Contexto

### O Modelo Mental: LLM como Compilador Fuzzy

Este exercício ensina um modelo mental, não uma técnica de implementação. O modelo mental é:

| Conceito Tradicional | Equivalente no Harness |
|---|---|
| **Source code** | Constraints de domínio, regras de negócio, rubricas de qualidade |
| **Compiler** | O harness (prompts + lint rules + validators + reviewers) |
| **Optimization passes** | Cada validação que o harness aplica (lint, type check, review, constraint check) |
| **Backend** | O modelo de LLM específico (Claude 3.5, Claude 4, GPT-5) |
| **Binary / build artifact** | O código gerado pelo agente |
| **Recompilar** | Trocar o modelo e regenerar o artefato a partir das mesmas constraints |

A implicação mais profunda: **o ativo durável não é o código gerado, mas as constraints que o produziram.** Quando você troca de modelo, você não reescreve código — você recompila o mesmo source com um backend melhor.

### Por Que Este Modelo Mental Importa

Sem este modelo mental, times cometem três erros fundamentais:

1. **Preservam o artefato errado.** Versionam código gerado como se fosse source, gastam tempo mantendo código que poderia ser regenerado em minutos com um modelo melhor.

2. **Acoplam constraints ao modelo.** Escrevem prompts e regras que assumem capacidades específicas de um modelo ("use tags [HIGH_PRIORITY] porque o modelo não prioriza system prompt"). Quando o modelo melhora, essas adaptações viram ruído.

3. **Não separam invariantes de compensações.** Misturam regras de domínio ("alergias são bloqueantes") com workarounds de modelo ("recarregue perfil do cliente a cada 3 turns para evitar perda de atenção"). Quando o modelo melhora, não sabem o que remover.

### O Que Você Vai Construir

Você vai implementar um **HarnessCompiler** — um sistema que:

1. Recebe constraints de domínio como source (invariantes)
2. Aplica passes de otimização (lint, type check, constraint validation)
3. Usa um backend de LLM (simulado) para gerar código
4. Permite trocar o backend sem alterar o source
5. Demonstra que o mesmo source gera outputs consistentes com backends diferentes

O domínio de exemplo é o KODA: um agente de recomendação de suplementos com constraints de alergia, orçamento e qualidade de explicação.

---

## 📋 Requisitos

### Funcionais

- [ ] Sistema recebe constraints de domínio e gera uma função de recomendação
- [ ] Constraints de domínio (invariantes) são armazenadas separadamente dos passes de otimização (compensações)
- [ ] O harness aplica passes em sequência: lint → constraint check → review
- [ ] Cada pass pode aprovar ou rejeitar o código gerado
- [ ] Se rejeitado, o código é regenerado (até 2 tentativas)
- [ ] Trocar o backend (modelo simulado) não requer alterar as constraints
- [ ] O mesmo conjunto de constraints gera outputs consistentes com backends diferentes
- [ ] As constraints sobrevivem à troca de backend intactas

### Técnicos

- [ ] Python 3.9+ com type hints
- [ ] Usar `dataclasses` para os modelos de dados
- [ ] Separar claramente: `DomainInvariant` (source) vs `ModelCompensation` (passes dependentes de backend)
- [ ] Implementar ao menos 3 passes de otimização
- [ ] Implementar ao menos 2 backends simulados com comportamentos diferentes
- [ ] Persistir as constraints em JSON (simulando o sistema de arquivos)

### Validação

- [ ] Cenario 1: backend "antigo" (com falhas) gera código que passa nos passes após correções
- [ ] Cenario 2: mesmo source, backend "novo" (melhor) gera código melhor com menos correções
- [ ] Cenario 3: constraints de domínio (alergia, orçamento) são preservadas entre backends
- [ ] Cenario 4: trocar backend e regenerar produz output funcionalmente equivalente
- [ ] Cenario 5: remover um pass específico do modelo antigo (compensação) não quebra o sistema

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│                    HARNESS COMPILER                               │
│                                                                   │
│  SOURCE (Durável — sobrevive a qualquer backend)                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ domain_constraints.json                                  │     │
│  │ {                                                        │     │
│  │   "invariants": [                                        │     │
│  │     "alergias_sao_bloqueantes",                          │     │
│  │     "orcamento_eh_restricao",                            │     │
│  │     "explicacao_fundamentada_em_produto"                 │     │
│  │   ],                                                     │     │
│  │   "domain_rules": {                                      │     │
│  │     "max_products_per_recommendation": 3,                │     │
│  │     "require_evidence_for_claim": true                    │     │
│  │   }                                                      │     │
│  │ }                                                        │     │
│  └─────────────────────────────────────────────────────────┘     │
│                            │                                      │
│                            ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │               BACKEND (Intercambiável)                    │     │
│  │                                                           │     │
│  │  ┌──────────────────┐    ┌──────────────────┐            │     │
│  │  │  LegacyBackend   │    │  ModernBackend   │            │     │
│  │  │  (Claude 3.5)    │    │  (Claude 4)      │            │     │
│  │  │  - ignora budget  │    │  - respeita tudo  │            │     │
│  │  │  - esquece alerg. │    │  - código limpo   │            │     │
│  │  │  - JSON quebrado  │    │  - JSON nativo    │            │     │
│  │  └──────────────────┘    └──────────────────┘            │     │
│  └─────────────────────────────────────────────────────────┘     │
│                            │                                      │
│                            ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │          OPTIMIZATION PASSES (Compensações)               │     │
│  │                                                           │     │
│  │  ┌──────────┐   ┌───────────────┐   ┌──────────────┐    │     │
│  │  │ LintPass │──▶│ ConstraintPass│──▶│ ReviewerPass │    │     │
│  │  │          │   │               │   │              │    │     │
│  │  │ verifica │   │ verifica      │   │ verifica     │    │     │
│  │  │ padrões  │   │ alergias,     │   │ rubricas de  │    │     │
│  │  │ de código│   │ orçamento,    │   │ qualidade    │    │     │
│  │  │          │   │ evidências    │   │              │    │     │
│  │  └──────────┘   └───────────────┘   └──────────────┘    │     │
│  │       │                │                   │              │     │
│  │       ▼                ▼                   ▼              │     │
│  │  ┌──────────────────────────────────────────────────┐    │     │
│  │  │              FEEDBACK LOOP                        │    │     │
│  │  │  Se qualquer pass falhar → regenerar (max 2x)    │    │     │
│  │  │  Se 2 tentativas falham → reportar falha         │    │     │
│  │  └──────────────────────────────────────────────────┘    │     │
│  └─────────────────────────────────────────────────────────┘     │
│                            │                                      │
│                            ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  BUILD ARTIFACT (Descartável — regenerado a cada build)  │     │
│  │  output/koda_agent.py                                    │     │
│  │  "Código gerado que satisfaz todas as constraints"       │     │
│  └─────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

### Separação Invariante vs Compensação

Este é o conceito central do exercício. Cada componente do harness deve ser classificado:

| Tipo | Definição | Exemplo no KODA | Sobrevive a upgrade? |
|---|---|---|---|
| **Domain Invariant** | Regra que independe do modelo. Vem do domínio do negócio. | "Cliente alérgico nunca recebe produto com alérgeno" | SIM — é verdade com qualquer modelo |
| **Model Compensation** | Regra que existe por limitação do modelo atual. | "Recarregue perfil do cliente a cada turno porque o modelo perde atenção após 40 min" | NÃO — modelo novo pode não precisar |

O harness deve tratar esses dois tipos de forma diferente: invariants são permanentes, compensations são candidatas a remoção quando o backend melhora.

### Data Flow Entre Componentes

| Etapa | Input | Output | Dono | Persistido? |
|---|---|---|---|---|
| Carregar source | `domain_constraints.json` | `CompilationUnit` | HarnessCompiler | Source: SIM |
| Gerar código | `CompilationUnit` + backend | `GeneratedArtifact` | Backend | Artifact: NÃO |
| Lint pass | `GeneratedArtifact` | `PassResult` | LintPass | NÃO |
| Constraint pass | `GeneratedArtifact` + invariants | `PassResult` | ConstraintPass | NÃO |
| Reviewer pass | `GeneratedArtifact` + rubrics | `PassResult` | ReviewerPass | NÃO |
| Loop | `PassResult` (rejected) | novo `GeneratedArtifact` | Backend | NÃO |
| Entrega | `GeneratedArtifact` (aprovado) | `output/koda_agent.py` | HarnessCompiler | Descartável |

---

## 🚀 Starter Code

```python
"""
Exercício 4 — Refatorar o Harness como Compilador Fuzzy
Nível 3 — Arquitetura Avançada

Implemente um HarnessCompiler que trata o LLM como backend intercambiável
e preserva constraints de domínio como o ativo durável.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Protocol


# ============================================================================
# DATA MODELS
# ============================================================================

class PassStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class DomainInvariant:
    """
    Restrição de domínio que transcende qualquer modelo específico.

    Invariants vêm do negócio, não da tecnologia. Exemplos:
    - "alergias são bloqueantes"
    - "orçamento é restrição, não sugestão"
    - "toda recomendação precisa de evidência de produto"

    Estes NUNCA são removidos quando o modelo melhora.
    """
    invariant_id: str
    description: str
    check_rule: str  # descrição de como verificar se o output respeita


@dataclass
class ModelCompensation:
    """
    Regra que existe por limitação de um modelo específico.

    Compensations são workarounds. Exemplos:
    - "recarregue perfil a cada turno" (modelo antigo perdia atenção)
    - "use tags [HIGH_PRIORITY]" (modelo antigo não priorizava system prompt)
    - "valide JSON pós-output" (modelo antigo não tinha JSON mode)

    Estas SÃO candidatas a remoção quando o modelo melhora.
    """
    compensation_id: str
    description: str
    target_model: str  # qual backend essa compensação foi criada para
    reason: str        # por que existe (qual limitação do modelo)


@dataclass
class CompilationUnit:
    """
    Unidade de compilação: o "source" do harness.

    Contém apenas o que sobrevive a trocas de backend:
    invariants de domínio + regras + rubricas de qualidade.
    """
    schema_version: str = "1.0"
    unit_id: str = ""
    invariants: list[DomainInvariant] = field(default_factory=list)
    domain_rules: dict[str, Any] = field(default_factory=dict)
    quality_rubrics: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class GeneratedArtifact:
    """
    Artefato gerado pelo backend: código + metadados.

    Este é o "binário" — descartável e regenerável.
    Deve ser tratado como output de build, não como source.
    """
    artifact_id: str = ""
    source_unit_id: str = ""       # qual CompilationUnit gerou isto
    backend_name: str = ""         # qual backend foi usado
    code: str = ""                 # o código gerado
    generation_attempt: int = 0    # qual tentativa (0 = primeira)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PassResult:
    """Resultado de um passe de otimização."""
    pass_name: str
    status: PassStatus
    failures: list[str] = field(default_factory=list)
    evidence: str = ""


@dataclass
class CompilationReport:
    """Relatório completo de uma compilação."""
    compilation_id: str = ""
    source_unit_id: str = ""
    backend_name: str = ""
    total_attempts: int = 0
    pass_results: list[PassResult] = field(default_factory=list)
    final_status: PassStatus = PassStatus.FAILED
    final_artifact: GeneratedArtifact | None = None
    compiled_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# BACKEND PROTOCOL (interface que todo backend deve implementar)
# ============================================================================

class Backend(Protocol):
    """
    Protocolo que todo backend de LLM deve implementar.

    Cada backend representa um modelo diferente (Claude 3.5, Claude 4, GPT-5).
    O harness NÃO deve conhecer detalhes específicos de cada backend.
    """

    @property
    def name(self) -> str:
        """Nome identificador do backend (ex: 'claude-3.5', 'claude-4')."""
        ...

    @property
    def capabilities(self) -> dict[str, bool]:
        """
        Capacidades documentadas do modelo.

        Exemplo:
        {
            "json_mode_native": False,     # modelo antigo não tem
            "attention_gt_99_pct": False,  # modelo antigo perde atenção
            "respects_system_prompt": False,
            "self_correction": False,
        }
        """
        ...

    def generate(self, unit: CompilationUnit, feedback: str | None = None) -> GeneratedArtifact:
        """
        Gera código a partir da CompilationUnit.

        Args:
            unit: A unidade de compilação (constraints + rubrics).
            feedback: Se presente, é feedback de um passe que rejeitou
                      a tentativa anterior. O backend deve corrigir.

        Returns:
            GeneratedArtifact com código gerado.
        """
        ...


# ============================================================================
# BACKEND IMPLEMENTATIONS (simulados)
# ============================================================================

class LegacyBackend:
    """
    Simula Claude 3.5 — um modelo mais antigo com limitações conhecidas.

    Comportamentos simulados:
    - Ignora orçamento ~30% das vezes (viés de recência)
    - Esquece alergias em conversas longas (atenção < 99%)
    - Produz JSON malformado ocasionalmente
    - Não faz self-correction
    """

    @property
    def name(self) -> str:
        return "claude-3.5-legacy"

    @property
    def capabilities(self) -> dict[str, bool]:
        return {
            "json_mode_native": False,
            "attention_gt_99_pct": False,
            "respects_system_prompt": False,
            "self_correction": False,
        }

    def generate(self, unit: CompilationUnit, feedback: str | None = None) -> GeneratedArtifact:
        """
        Gera código com as limitações do modelo antigo.

        Simula uma chamada de API que retorna código que pode ter problemas:
        - Se for primeira tentativa, introduz falhas aleatórias
        - Se receber feedback, corrige as falhas apontadas
        """
        # TODO: Implementar geração simulada do backend legado
        #
        # Comportamento esperado:
        # 1. Gerar código base que implementa uma função recommend()
        # 2. Se for primeira tentativa (feedback is None):
        #    - ~30% de chance de ignorar budget
        #    - ~30% de chance de ignorar alergia
        #    - ~20% de chance de produzir código com erro de sintaxe
        # 3. Se receber feedback:
        #    - Corrigir especificamente o que o feedback aponta
        #    - Outros problemas podem persistir
        # 4. O código gerado deve ser Python executável
        pass


class ModernBackend:
    """
    Simula Claude 4 — um modelo moderno com capacidades superiores.

    Comportamentos simulados:
    - Respeita todas as constraints na primeira tentativa
    - JSON mode nativo (código sempre bem formado)
    - Atenção > 99% em contextos longos
    - Self-correction ativo
    """

    @property
    def name(self) -> str:
        return "claude-4-modern"

    @property
    def capabilities(self) -> dict[str, bool]:
        return {
            "json_mode_native": True,
            "attention_gt_99_pct": True,
            "respects_system_prompt": True,
            "self_correction": True,
        }

    def generate(self, unit: CompilationUnit, feedback: str | None = None) -> GeneratedArtifact:
        """
        Gera código com as capacidades do modelo moderno.

        Simula uma chamada de API que retorna código de alta qualidade:
        - Primeira tentativa: código limpo, constraints respeitadas
        - Se receber feedback (raro): corrige na primeira tentativa
        """
        # TODO: Implementar geração simulada do backend moderno
        #
        # Comportamento esperado:
        # 1. Gerar código base que implementa uma função recommend()
        # 2. Respeitar TODAS as constraints na primeira tentativa
        # 3. Código bem formado, sem erros de sintaxe
        # 4. Explicações inline como comentários
        # 5. Se receber feedback (deve ser raro):
        #    - Corrigir na primeira tentativa
        pass


# ============================================================================
# OPTIMIZATION PASSES
# ============================================================================

class LintPass:
    """
    Pass 1: Verificação de qualidade de código.

    Verifica padrões estruturais:
    - Código é sintaticamente válido?
    - Funções têm docstring?
    - Type hints estão presentes?
    - Nomes seguem snake_case?

    Este é o pass mais barato — execute primeiro.
    """

    def run(self, artifact: GeneratedArtifact) -> PassResult:
        """
        Executa verificação de lint no artefato gerado.

        Args:
            artifact: Código gerado pelo backend.

        Returns:
            PassResult com status e lista de falhas.
        """
        # TODO: Implementar LintPass
        #
        # Verificações:
        # 1. O código compila? (tentar compilar com compile())
        # 2. A função recommend() existe?
        # 3. A função recommend() tem docstring?
        # 4. A função recommend() tem type hints?
        # 5. Nomes de variáveis seguem snake_case? (verificação simples)
        pass


class ConstraintPass:
    """
    Pass 2: Verificação de constraints de domínio.

    Este pass NÃO depende de qual backend gerou o código.
    Ele verifica invariants de domínio que são verdade independente do modelo.

    Verifica:
    - Alergias: se cliente tem restrição, nenhum produto recomendado contém alérgeno
    - Orçamento: preço de todos os produtos <= orçamento do cliente
    - Evidência: toda recomendação referencia um produto real do catálogo
    """

    def run(self, artifact: GeneratedArtifact, invariants: list[DomainInvariant]) -> PassResult:
        """
        Verifica se o artefato respeita as constraints de domínio.

        Args:
            artifact: Código gerado pelo backend.
            invariants: Lista de invariants de domínio a verificar.

        Returns:
            PassResult com status e lista de falhas.
        """
        # TODO: Implementar ConstraintPass
        #
        # Algoritmo sugerido:
        # 1. Para cada invariant em invariants:
        #    a. Extrair a lógica de verificação do invariant.check_rule
        #    b. Simular a execução do código gerado com dados de teste
        #    c. Verificar se o output respeita a constraint
        #    d. Registrar PassResult
        #
        # Dados de teste fixos para simulação:
        # - Cliente: budget=80, alergia="lactose"
        # - Catálogo: usar PRODUCT_CATALOG (definido abaixo)
        #
        # 2. Se TODOS os invariants passaram: status = PASSED
        # 3. Se ALGUM falhou: status = FAILED, listar quais
        pass


class ReviewerPass:
    """
    Pass 3: Verificação contra rubricas de qualidade.

    Verifica aspectos subjetivos mas mensuráveis:
    - A explicação é fundamentada? (menciona características do produto)
    - O tom é adequado? (não pressiona compra)
    - A recomendação é clara? (cliente entende por que recebeu essa opção)
    """

    def run(self, artifact: GeneratedArtifact, rubrics: list[str]) -> PassResult:
        """
        Verifica se o artefato atende às rubricas de qualidade.

        Args:
            artifact: Código gerado pelo backend.
            rubrics: Lista de critérios de qualidade.

        Returns:
            PassResult com status e lista de falhas.
        """
        # TODO: Implementar ReviewerPass
        #
        # Verificações:
        # 1. "explicação fundamentada": o código gerado contém comentários
        #    ou strings que explicam o raciocínio?
        # 2. "tom adequado": procurar por palavras de pressão
        #    ("aproveite", "só hoje", "não perca", "últimas unidades")
        # 3. "recomendação clara": o output é conciso (< 500 caracteres)?
        # 4. "não recomenda fora de estoque": verificar contra catálogo
        pass


# ============================================================================
# PRODUCT CATALOG (dados de domínio simulados)
# ============================================================================

PRODUCT_CATALOG: list[dict[str, Any]] = [
    {
        "sku": "CREA-MONO-300", "name": "Creatina Monohidratada 300g",
        "category": "creatina", "price_brl": 69.90,
        "lactose_free": True, "gluten_free": True, "in_stock": True,
    },
    {
        "sku": "CREA-MICRO-250", "name": "Creatina Micronizada 250g",
        "category": "creatina", "price_brl": 74.90,
        "lactose_free": True, "gluten_free": True, "in_stock": True,
    },
    {
        "sku": "WHEY-CONC-1000", "name": "Whey Concentrado Chocolate 1kg",
        "category": "whey", "price_brl": 89.90,
        "lactose_free": False, "gluten_free": True, "in_stock": True,
    },
    {
        "sku": "WHEY-ISO-900", "name": "Whey Isolado Chocolate 900g",
        "category": "whey", "price_brl": 139.90,
        "lactose_free": True, "gluten_free": True, "in_stock": True,
    },
    {
        "sku": "WHEY-VEG-750", "name": "Proteína Vegetal Baunilha 750g",
        "category": "whey", "price_brl": 99.90,
        "lactose_free": True, "gluten_free": True, "in_stock": True,
    },
]


# ============================================================================
# DOMAIN CONSTRAINTS (o "source" durável)
# ============================================================================

def build_koda_compilation_unit() -> CompilationUnit:
    """
    Constrói a CompilationUnit do KODA com invariants de domínio.

    Este é o "source" que sobrevive a qualquer troca de backend.
    As constraints aqui definidas NÃO dependem de qual modelo está
    gerando o código — são verdades do domínio de recomendação.
    """
    return CompilationUnit(
        unit_id="koda-recommendation-v1",
        invariants=[
            DomainInvariant(
                invariant_id="allergy_blocking",
                description="Produtos com alérgenos do cliente são bloqueados",
                check_rule="nenhum produto recomendado contém alérgeno do cliente",
            ),
            DomainInvariant(
                invariant_id="budget_constraint",
                description="Preço de todos os produtos recomendados <= orçamento do cliente",
                check_rule="price_brl <= customer_budget para todos os produtos",
            ),
            DomainInvariant(
                invariant_id="in_stock_only",
                description="Apenas produtos em estoque podem ser recomendados",
                check_rule="in_stock == True para todos os produtos",
            ),
            DomainInvariant(
                invariant_id="evidence_based",
                description="Toda recomendação referencia um produto real do catálogo",
                check_rule="sku do produto existe em PRODUCT_CATALOG",
            ),
        ],
        domain_rules={
            "max_products": 3,
            "min_products": 1,
            "customer_budget": 80.0,
            "customer_allergies": ["lactose"],
            "sort_by": "rating_desc",
        },
        quality_rubrics=[
            "explicação fundamentada em características do produto",
            "tom consultivo, não agressivo",
            "recomendação clara e concisa",
            "menciona preço explicitamente",
        ],
    )


# ============================================================================
# HARNESS COMPILER
# ============================================================================

class HarnessCompiler:
    """
    O compilador fuzzy: coordena backend + passes de otimização.

    Responsabilidades:
    1. Carregar a CompilationUnit (source)
    2. Selecionar o backend (modelo)
    3. Executar passes de otimização em sequência
    4. Coordenar o loop de feedback (regenerar se rejeitado)
    5. Produzir CompilationReport

    Invariante arquitetural:
    - O HarnessCompiler NUNCA modifica a CompilationUnit
    - O HarnessCompiler NUNCA depende de qual backend está ativo
    - Os passes podem ser adicionados/removidos sem alterar o source
    """

    def __init__(self, backend: Backend):
        """
        Args:
            backend: O backend de LLM a ser usado nesta compilação.
        """
        # TODO: Implementar inicialização
        # 1. Armazenar backend
        # 2. Inicializar lista de passes (LintPass, ConstraintPass, ReviewerPass)
        pass

    def compile(
        self,
        unit: CompilationUnit,
        max_attempts: int = 2,
    ) -> CompilationReport:
        """
        Executa o pipeline completo de compilação.

        Fluxo:
        1. Backend gera código
        2. Executa passes em sequência
        3. Se todos passam: sucesso
        4. Se algum falha: feedback → regenera (até max_attempts)
        5. Se esgotar tentativas: reporta falha

        Args:
            unit: CompilationUnit com constraints e rubricas.
            max_attempts: Número máximo de tentativas de geração.

        Returns:
            CompilationReport com resultado completo.
        """
        # TODO: Implementar o pipeline de compilação
        #
        # Algoritmo sugerido:
        # 1. Criar CompilationReport
        # 2. Tentar gerar código:
        #    for attempt in range(max_attempts + 1):
        #        a. Chamar backend.generate(unit, feedback)
        #        b. Executar LintPass.run(artifact)
        #        c. Se passou: executar ConstraintPass.run(artifact, unit.invariants)
        #        d. Se passou: executar ReviewerPass.run(artifact, unit.quality_rubrics)
        #        e. Se TODOS passaram: sucesso, retornar
        #        f. Se algum falhou: preparar feedback com as falhas
        #        g. Se última tentativa: reportar falha
        #
        # 3. Preencher CompilationReport com todos os resultados
        # 4. Retornar report
        pass

    def get_passes_for_backend(self) -> list[str]:
        """
        Retorna quais passes são relevantes para o backend atual.

        Backends modernos podem não precisar de certos passes.
        Exemplo: se o backend tem json_mode_native, o LintPass
        (que verifica sintaxe) pode ser simplificado.

        Returns:
            Lista de nomes de passes ativos para este backend.
        """
        # TODO: Implementar seleção dinâmica de passes
        #
        # Algoritmo sugerido:
        # 1. Verificar backend.capabilities
        # 2. Se json_mode_native: LintPass pode ser mais leve
        # 3. Se self_correction: menos tentativas necessárias
        # 4. Se respects_system_prompt: ConstraintPass pode ser simplificado
        # 5. Retornar lista de passes ativos
        pass


# ============================================================================
# TESTS / EXEMPLOS DE USO
# ============================================================================

def test_legacy_backend_needs_corrections():
    """Cenário 1: backend antigo gera código com falhas, passes corrigem."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: Backend Legado Precisa de Correções")
    print("=" * 60)

    unit = build_koda_compilation_unit()
    backend = LegacyBackend()
    compiler = HarnessCompiler(backend)

    report = compiler.compile(unit, max_attempts=2)

    print(f"\n📊 Backend: {report.backend_name}")
    print(f"   Tentativas: {report.total_attempts}")
    print(f"   Status final: {report.final_status.value}")

    # Com backend legado, pode precisar de mais de 1 tentativa
    # Mas deve eventualmente passar (ou falhar graciosamente)
    assert report.total_attempts >= 1, "Deve tentar pelo menos 1 vez"

    if report.final_status == PassStatus.PASSED:
        assert report.final_artifact is not None
        assert len(report.final_artifact.code) > 0, "Código não pode ser vazio"
        print("   ✅ Código aprovado após passes")
        for pr in report.pass_results:
            print(f"      - {pr.pass_name}: {pr.status.value}")
    else:
        # Se falhou mesmo após 2 tentativas, o feedback deve ser informativo
        print("   ⚠️ Falha após 2 tentativas (esperado com backend legado)")
        for pr in report.pass_results:
            if pr.status == PassStatus.FAILED:
                print(f"      - {pr.pass_name}: FAILED — {pr.failures}")

    print("✅ Teste 1 concluído!")


def test_same_source_different_backends():
    """Cenário 2: mesmo source, backends diferentes, outputs funcionalmente equivalentes."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: Mesmo Source, Backends Diferentes")
    print("=" * 60)

    unit = build_koda_compilation_unit()

    # Compilar com backend legado
    legacy = LegacyBackend()
    compiler_legacy = HarnessCompiler(legacy)
    report_legacy = compiler_legacy.compile(unit, max_attempts=2)

    # Compilar com backend moderno
    modern = ModernBackend()
    compiler_modern = HarnessCompiler(modern)
    report_modern = compiler_modern.compile(unit, max_attempts=2)

    print(f"\n📊 Comparação:")
    print(f"   Legacy: {report_legacy.total_attempts} tentativas, status={report_legacy.final_status.value}")
    print(f"   Modern: {report_modern.total_attempts} tentativas, status={report_modern.final_status.value}")

    # O source (unit) é o mesmo para ambos
    # A diferença está apenas no backend e no número de tentativas
    assert report_legacy.source_unit_id == report_modern.source_unit_id, (
        "Ambos devem usar o mesmo source"
    )

    # Backend moderno deve precisar de menos tentativas
    assert report_modern.total_attempts <= report_legacy.total_attempts, (
        "Backend moderno deve precisar de menos ou igual número de tentativas"
    )

    print("✅ Teste 2 concluído!")


def test_invariants_survive_backend_swap():
    """Cenário 3: invariants de domínio sobrevivem à troca de backend."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: Invariants Sobrevivem à Troca de Backend")
    print("=" * 60)

    unit = build_koda_compilation_unit()

    # Verificar que os invariants existem antes de compilar
    invariant_ids_before = {inv.invariant_id for inv in unit.invariants}
    assert "allergy_blocking" in invariant_ids_before
    assert "budget_constraint" in invariant_ids_before
    assert "in_stock_only" in invariant_ids_before
    assert "evidence_based" in invariant_ids_before

    # Compilar com backend legado
    legacy = LegacyBackend()
    compiler_legacy = HarnessCompiler(legacy)
    report_legacy = compiler_legacy.compile(unit, max_attempts=2)

    # Compilar com backend moderno — MESMA unit
    modern = ModernBackend()
    compiler_modern = HarnessCompiler(modern)
    report_modern = compiler_modern.compile(unit, max_attempts=2)

    # Os invariants NÃO MUDARAM entre as compilações
    invariant_ids_after = {inv.invariant_id for inv in unit.invariants}
    assert invariant_ids_before == invariant_ids_after, (
        "Invariants não devem mudar entre compilações!"
    )

    print(f"   Invariants antes: {sorted(invariant_ids_before)}")
    print(f"   Invariants depois: {sorted(invariant_ids_after)}")
    print("   ✅ Invariants preservados entre backends")

    print("✅ Teste 3 concluído!")


def test_constraint_pass_detects_allergy_violation():
    """Cenário 4: ConstraintPass detecta violação de alergia."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: ConstraintPass Detecta Violação de Alergia")
    print("=" * 60)

    unit = build_koda_compilation_unit()

    # Criar um artefato que VIOLA a constraint de alergia
    bad_artifact = GeneratedArtifact(
        artifact_id="test-bad-001",
        source_unit_id=unit.unit_id,
        backend_name="test-backend",
        code="""
def recommend(customer_budget, customer_allergies):
    '''Recomenda whey protein.'''
    return [{"sku": "WHEY-CONC-1000", "name": "Whey Concentrado", "price_brl": 89.90}]
""",
    )

    constraint_pass = ConstraintPass()
    result = constraint_pass.run(bad_artifact, unit.invariants)

    print(f"\n📊 ConstraintPass: {result.status.value}")
    if result.status == PassStatus.FAILED:
        print(f"   Falhas: {result.failures}")
        # Deve detectar que WHEY-CONC-1000 tem lactose
        assert any("lactose" in f.lower() or "alerg" in f.lower() for f in result.failures), (
            "Deve detectar violação de alergia"
        )
    print(f"   Evidência: {result.evidence}")

    print("✅ Teste 4 concluído!")


def test_constraint_pass_detects_budget_violation():
    """Cenário 5: ConstraintPass detecta violação de orçamento."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: ConstraintPass Detecta Violação de Orçamento")
    print("=" * 60)

    unit = build_koda_compilation_unit()

    # Criar artefato que viola orçamento (R$139.90 > R$80.00)
    bad_artifact = GeneratedArtifact(
        artifact_id="test-bad-002",
        source_unit_id=unit.unit_id,
        backend_name="test-backend",
        code="""
def recommend(customer_budget, customer_allergies):
    '''Recomenda whey protein.'''
    return [{"sku": "WHEY-ISO-900", "name": "Whey Isolado", "price_brl": 139.90}]
""",
    )

    constraint_pass = ConstraintPass()
    result = constraint_pass.run(bad_artifact, unit.invariants)

    print(f"\n📊 ConstraintPass: {result.status.value}")
    if result.status == PassStatus.FAILED:
        print(f"   Falhas: {result.failures}")
        assert any("orçamento" in f.lower() or "budget" in f.lower() or "139.90" in f or "80" in f for f in result.failures), (
            "Deve detectar violação de orçamento"
        )

    print("✅ Teste 5 concluído!")


def test_backend_swap_preserves_functional_equivalence():
    """Cenário 6: Trocar backend preserva equivalência funcional."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 6: Equivalência Funcional Entre Backends")
    print("=" * 60)

    unit = build_koda_compilation_unit()

    # Compilar com ambos os backends
    legacy = LegacyBackend()
    modern = ModernBackend()
    compiler_legacy = HarnessCompiler(legacy)
    compiler_modern = HarnessCompiler(modern)

    report_legacy = compiler_legacy.compile(unit, max_attempts=2)
    report_modern = compiler_modern.compile(unit, max_attempts=2)

    # Ambos os reports devem referenciar o mesmo source
    assert report_legacy.source_unit_id == report_modern.source_unit_id == unit.unit_id, (
        "Ambos devem referenciar o mesmo source"
    )

    # Se ambos passaram, verificar que produziram artefatos
    if report_legacy.final_status == PassStatus.PASSED:
        assert report_legacy.final_artifact is not None
        assert "recommend" in report_legacy.final_artifact.code.lower(), (
            "Código deve conter função recommend()"
        )

    if report_modern.final_status == PassStatus.PASSED:
        assert report_modern.final_artifact is not None
        assert "recommend" in report_modern.final_artifact.code.lower(), (
            "Código deve conter função recommend()"
        )

    print(f"\n   Legacy backend: {report_legacy.backend_name}")
    print(f"   Modern backend: {report_modern.backend_name}")
    print(f"   Source unit: {unit.unit_id}")
    print("   ✅ Source preservado, backends intercambiáveis")

    print("✅ Teste 6 concluído!")


def test_invariant_vs_compensation_separation():
    """Cenário 7: Invariants e Compensations são tratados diferentemente."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 7: Separação Invariant vs Compensation")
    print("=" * 60)

    # Criar compensations específicas do modelo legado
    compensations = [
        ModelCompensation(
            compensation_id="reload_profile_every_turn",
            description="Recarregar perfil do cliente a cada turno",
            target_model="claude-3.5-legacy",
            reason="Modelo antigo perde atenção após 40 minutos de conversa",
        ),
        ModelCompensation(
            compensation_id="explicit_priority_tags",
            description="Usar tags [HIGH_PRIORITY] para constraints críticas",
            target_model="claude-3.5-legacy",
            reason="Modelo antigo não prioriza system prompt automaticamente",
        ),
        ModelCompensation(
            compensation_id="post_output_json_validation",
            description="Validar JSON do output após geração",
            target_model="claude-3.5-legacy",
            reason="Modelo antigo não tem JSON mode nativo",
        ),
    ]

    # Estas compensations são ESPECÍFICAS do modelo legado
    for comp in compensations:
        assert comp.target_model == "claude-3.5-legacy", (
            f"{comp.compensation_id} deve ser específica do modelo legado"
        )

    # Com modelo moderno, estas compensations são candidatas a remoção
    modern_capabilities = ModernBackend().capabilities
    removable = []
    for comp in compensations:
        if comp.compensation_id == "post_output_json_validation" and modern_capabilities.get("json_mode_native"):
            removable.append(comp.compensation_id)
        if comp.compensation_id == "explicit_priority_tags" and modern_capabilities.get("respects_system_prompt"):
            removable.append(comp.compensation_id)
        if comp.compensation_id == "reload_profile_every_turn" and modern_capabilities.get("attention_gt_99_pct"):
            removable.append(comp.compensation_id)

    print(f"\n   Compensations do modelo legado: {len(compensations)}")
    print(f"   Removíveis com modelo moderno: {len(removable)}")
    for r in removable:
        print(f"      - {r}")

    assert len(removable) >= 2, (
        "Pelo menos 2 compensations devem ser removíveis com modelo moderno"
    )

    # Invariants NUNCA são removíveis
    unit = build_koda_compilation_unit()
    assert len(unit.invariants) == 4, "Os 4 invariants devem permanecer"
    print(f"   Invariants de domínio: {len(unit.invariants)} (permanentes)")

    print("✅ Teste 7 concluído!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 4: REFATORAR O HARNESS COMO COMPILADOR FUZZY")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_legacy_backend_needs_corrections()
    # test_same_source_different_backends()
    # test_invariants_survive_backend_swap()
    # test_constraint_pass_detects_allergy_violation()
    # test_constraint_pass_detects_budget_violation()
    # test_backend_swap_preserves_functional_equivalence()
    # test_invariant_vs_compensation_separation()

    print("\n📝 TODO: Implemente as classes acima!")
    print("   1. LegacyBackend.generate()")
    print("   2. ModernBackend.generate()")
    print("   3. LintPass.run()")
    print("   4. ConstraintPass.run()")
    print("   5. ReviewerPass.run()")
    print("   6. HarnessCompiler.compile()")
    print("   7. HarnessCompiler.get_passes_for_backend()")
    print("   Após implementar, descomente os testes em main()")
```

---

## 🏗️ Como Começar

### Passo 1: Entender a Separação Invariant vs Compensation (10 min)

Antes de escrever código, leia os data models com atenção:

- `DomainInvariant`: regras que vêm do negócio. "Alergias são bloqueantes" é verdade com qualquer modelo.
- `ModelCompensation`: regras que existem por limitação de um modelo específico. "Recarregar perfil a cada turno" só existe porque o modelo antigo perdia atenção.

A diferença é a chave do exercício. Quando você troca de backend, invariants permanecem, compensations podem ser removidas.

### Passo 2: Implementar os Backends (20 min)

Comece pelo `LegacyBackend.generate()`. Este é o backend "ruim":

```python
def generate(self, unit, feedback=None):
    attempt = 0  # você vai precisar rastrear tentativas
    
    if feedback is None:
        # Primeira tentativa: introduzir falhas
        code = self._generate_with_flaws(unit)
    else:
        # Feedback: corrigir especificamente o que foi apontado
        code = self._fix_specific_issues(unit, feedback)
    
    return GeneratedArtifact(
        artifact_id=f"legacy-{uuid4().hex[:8]}",
        source_unit_id=unit.unit_id,
        backend_name=self.name,
        code=code,
        generation_attempt=attempt,
    )
```

Dica: faça o código gerado ser uma string Python simples com uma função `recommend()`. Isso facilita os passes verificarem.

Depois implemente `ModernBackend.generate()`. Este backend gera código limpo na primeira tentativa:

```python
def generate(self, unit, feedback=None):
    # Sempre gera código que respeita constraints
    # Filtra produtos por budget E alergia E estoque
    # Retorna função recommend() bem formatada
    ...
```

### Passo 3: Implementar os Passes (25 min)

**LintPass:** Verificações estruturais básicas. Use `compile()` para checar sintaxe:

```python
def run(self, artifact):
    failures = []
    try:
        compile(artifact.code, "<generated>", "exec")
    except SyntaxError as e:
        failures.append(f"Erro de sintaxe: {e}")
    
    # Verificar se recommend() existe
    if "def recommend" not in artifact.code:
        failures.append("Função recommend() não encontrada")
    
    status = PassStatus.PASSED if not failures else PassStatus.FAILED
    return PassResult(pass_name="LintPass", status=status, failures=failures)
```

**ConstraintPass:** O mais importante. Execute a função gerada com dados de teste e verifique o output:

```python
def run(self, artifact, invariants):
    # 1. Executar o código gerado
    # 2. Chamar recommend(customer_budget=80, customer_allergies=["lactose"])
    # 3. Verificar cada produto retornado contra as constraints:
    #    - lactose_free == True
    #    - price_brl <= 80
    #    - in_stock == True
    #    - sku existe no catálogo
    ...
```

**ReviewerPass:** Verificações de qualidade:

```python
def run(self, artifact, rubrics):
    failures = []
    code_lower = artifact.code.lower()
    
    # Verificar palavras de pressão
    pressure_words = ["aproveite", "só hoje", "não perca", "últimas unidades"]
    for word in pressure_words:
        if word in code_lower:
            failures.append(f"Linguagem de pressão detectada: '{word}'")
    
    # Verificar se tem explicação (comentários ou docstring)
    if '"""' not in artifact.code and "'''" not in artifact.code:
        failures.append("Sem docstring ou explicação")
    
    ...
```

### Passo 4: Implementar o HarnessCompiler (20 min)

Esta é a orquestração central:

```python
def compile(self, unit, max_attempts=2):
    report = CompilationReport(
        compilation_id=f"comp-{uuid4().hex[:8]}",
        source_unit_id=unit.unit_id,
        backend_name=self.backend.name,
    )
    
    feedback = None
    for attempt in range(max_attempts + 1):
        # Gerar código
        artifact = self.backend.generate(unit, feedback)
        report.total_attempts = attempt + 1
        
        # Executar passes
        all_passed = True
        for p in self.passes:
            if isinstance(p, ConstraintPass):
                result = p.run(artifact, unit.invariants)
            elif isinstance(p, ReviewerPass):
                result = p.run(artifact, unit.quality_rubrics)
            else:
                result = p.run(artifact)
            
            report.pass_results.append(result)
            if result.status == PassStatus.FAILED:
                all_passed = False
        
        if all_passed:
            report.final_status = PassStatus.PASSED
            report.final_artifact = artifact
            return report
        
        # Preparar feedback para próxima tentativa
        failures = [r.failures for r in report.pass_results if r.status == PassStatus.FAILED]
        feedback = " | ".join(str(f) for f in failures)
    
    # Esgotou tentativas
    report.final_status = PassStatus.FAILED
    return report
```

### Passo 5: Testar (10 min)

Descomente os testes em `main()` e execute. Todos os 7 testes devem passar.

---

## 🎯 Desafios Extra (Opcional)

### Desafio 1: CompilationUnit versionada com schema evolution

```python
def migrate_compilation_unit(old_unit: dict, from_version: str, to_version: str) -> CompilationUnit:
    """
    Quando o schema de constraints evolui, compilações antigas
    precisam ser migradas. Implemente versionamento de schema.
    """
    pass
```

### Desafio 2: Cache de artefatos por hash da CompilationUnit

```python
class ArtifactCache:
    """
    Se a CompilationUnit não mudou e o backend é o mesmo,
    reusar o artefato gerado anteriormente em vez de recompilar.
    """
    def get(self, unit_hash: str, backend: str) -> GeneratedArtifact | None: ...
    def put(self, unit_hash: str, backend: str, artifact: GeneratedArtifact) -> None: ...
```

### Desafio 3: Passes condicionais por backend

```python
def build_pass_pipeline(backend: Backend) -> list:
    """
    Backends com json_mode_native não precisam de LintPass completo.
    Backends com self_correction podem usar menos tentativas.
    Construa um pipeline de passes condicional às capacidades do backend.
    """
    pass
```

### Desafio 4: Compilação paralela com múltiplos backends

```python
def compile_with_all_backends(unit: CompilationUnit, backends: list[Backend]) -> dict[str, CompilationReport]:
    """
    Executa a mesma CompilationUnit em todos os backends em paralelo.
    Compara outputs e seleciona o melhor (menos tentativas, melhor qualidade).
    Útil para avaliar qual backend produz melhores resultados.
    """
    pass
```

---

## 📊 Checklist de Implementação

- [ ] `LegacyBackend.generate()` — gera código com falhas simuladas
- [ ] `ModernBackend.generate()` — gera código limpo
- [ ] `LintPass.run()` — verifica sintaxe, docstring, type hints
- [ ] `ConstraintPass.run()` — verifica alergias, orçamento, estoque, evidência
- [ ] `ReviewerPass.run()` — verifica tom, clareza, fundamentação
- [ ] `HarnessCompiler.__init__()` — inicializa com backend e passes
- [ ] `HarnessCompiler.compile()` — pipeline completo com loop de feedback
- [ ] `HarnessCompiler.get_passes_for_backend()` — passes condicionais
- [ ] Teste 1 (backend legado) passa ✅
- [ ] Teste 2 (backends diferentes) passa ✅
- [ ] Teste 3 (invariants sobrevivem) passa ✅
- [ ] Teste 4 (detecta alergia) passa ✅
- [ ] Teste 5 (detecta orçamento) passa ✅
- [ ] Teste 6 (equivalência funcional) passa ✅
- [ ] Teste 7 (invariant vs compensation) passa ✅

---

## 💡 Dicas de Implementação

**Dica 1:** O código gerado pelos backends não precisa ser código "real" que executaria em produção. Basta ser uma string Python que os passes conseguem inspecionar. Exemplo:

```python
code = '''
def recommend(customer_budget, customer_allergies):
    """Recomenda creatina dentro do orçamento."""
    products = [
        {"sku": "CREA-MONO-300", "name": "Creatina Monohidratada 300g", "price_brl": 69.90},
    ]
    return products
'''
```

**Dica 2:** Para o `ConstraintPass`, use `exec()` para executar o código gerado em um namespace isolado e depois chamar `recommend()`:

```python
namespace = {}
exec(artifact.code, namespace)
result = namespace["recommend"](customer_budget=80, customer_allergies=["lactose"])
```

**Dica 3:** O segredo do exercício não é a complexidade do código — é a separação conceitual. Passe mais tempo pensando em "isso é invariant ou compensation?" do que otimizando os passes.

**Dica 4:** Para o feedback loop, seja específico. Em vez de feedback genérico "código ruim", passe exatamente qual constraint falhou: "budget_constraint: produto WHEY-ISO-900 com preço R$139.90 excede orçamento de R$80.00".

---

## ✅ Validação Final

Sua implementação está correta se:

1. ✅ Todos os 7 testes passam
2. ✅ Trocar de `LegacyBackend` para `ModernBackend` não requer alterar `CompilationUnit`
3. ✅ `DomainInvariant` e `ModelCompensation` são classes separadas com responsabilidades diferentes
4. ✅ O `HarnessCompiler` não tem conhecimento específico de qual backend está usando (além do protocolo)
5. ✅ O loop de feedback passa informações específicas (não genéricas) para o backend
6. ✅ Código gerado é tratado como descartável (regenerado, não versionado)

---

## 🎓 O Que Você Aprendeu

Após completar este exercício, você internalizou:

- ✅ O modelo mental "LLM = compilador fuzzy, harness = passes de otimização"
- ✅ A diferença fundamental entre invariants de domínio e compensações de modelo
- ✅ Por que o código gerado é o ativo errado para versionar
- ✅ Como construir um harness que sobrevive a upgrades de modelo
- ✅ Como separar o que é permanente (regras de negócio) do que é contingente (workarounds de modelo)
- ✅ O padrão de "compilação" com passes em sequência e loop de feedback

**Próximo:** Exercício 5 — Documentação Baseada em Personas

---

*Exercício 4 de Nível 3 | Curso Long-Running Agents | Programa Técnico FutanBear*
