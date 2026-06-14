---
title: "Exercicio: Aplicar o Constraint Budget Gate com Limite de 5-7 Restricoes"
type: curriculum-exercise
nivel: 3
aliases: ["constraint budget gate", "limite constraints", "5-7 constraint rule", "constraint budget heuristic", "constraint list gate", "implementation constraint reclassification"]
tags: [curriculo-conteudo, nivel-3, exercicio, agentes-orquestracao, spec-driven-development, constraint-engineering, decision-discipline, harness-engineering, python, dataclass]
relates-to: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]"]
last_updated: 2026-06-14
---
# Exercicio: Aplicar o Constraint Budget Gate com Limite de 5-7 Restricoes
## Nivel 3 - Arquitetura Avancada

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** (Avancado)
**Pre-requisito:** Ter completado Exercicio 5 (Intent Five-Part Primitive) + Exercicio Two-Implementations Goal Test
**Objetivo:** Diagnosticar constraint lists que cresceram ate virar especificacoes de implementacao e implementar um ConstraintBudgetGate que impoe o limite de 5-7 restricoes direcionais em linguagem de negocio

---

## Prologo: As 23 Restricoes Que Mataram a Criatividade do Agente

### Segunda-feira, 10h00. A Sprint de Recomendacao Inteligente.

```
PM: "Precisamos que o agente de recomendacao do KODA seja melhor.
     Vou listar todas as restricoes que o time levantou."

[30 minutos depois, um documento de 4 paginas...]
```

O time de produto passou 3 workshops levantando restricoes para o novo agente de recomendacao. O resultado foi uma lista de 23 restricoes. Ninguem questionou o tamanho da lista -- "quanto mais restricoes, mais seguro", pensaram.

O agente recebeu o intent com 23 constraints. Este foi o resultado:

```
╔══════════════════════════════════════════════════════════════════╗
║         AS 23 RESTRICOES E SEU EFEITO NO AGENTE                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  RESTRICOES GENUINAS (devem ficar):                              ║
║   1. Nenhum produto com alergeno do cliente nos resultados       ║
║   2. Preco dos produtos <= orcamento declarado                   ║
║   3. Explicacao da recomendacao referencia atributos do produto  ║
║   4. Maximo 3 produtos por recomendacao                          ║
║   5. Produtos fora de estoque sao excluidos                      ║
║                                                                  ║
║  IMPLEMENTACAO DISFARCADA DE RESTRICAO (devem ir para contexto): ║
║   6. Usar Redis para cache de perfil do cliente                  ║
║   7. Usar PostgreSQL com indice GIN para busca textual           ║
║   8. Implementar com Python 3.11 + FastAPI                       ║
║   9. Usar React 18 no frontend de recomendacao                   ║
║  10. Deploy via Docker + Kubernetes                              ║
║  11. Logs estruturados em formato JSON                           ║
║  12. Usar JWT para autenticacao entre servicos                   ║
║  13. Implementar Circuit Breaker para API de catalogo            ║
║                                                                  ║
║  CHECKS DISFARCADOS DE RESTRICAO (devem ir para failure cond.):  ║
║  14. Tempo de resposta < 500ms                                   ║
║  15. Throughput >= 100 req/s                                     ║
║  16. Disponibilidade 99.9%                                       ║
║  17. Taxa de erro < 0.1%                                         ║
║  18. Cobertura de testes >= 80%                                  ║
║                                                                  ║
║  AMBIGUIDADES (precisam de clarificacao):                        ║
║  19. "Deve ser escalavel" (sem metrica)                          ║
║  20. "Interface intuitiva" (subjetivo)                           ║
║  21. "Codigo limpo e bem documentado" (vago)                     ║
║  22. "Performance aceitavel" (sem definicao)                     ║
║  23. "Seguranca robusta" (sem especificacao)                     ║
║                                                                  ║
║  RESULTADO:                                                      ║
║  - Agente recebeu 23 restricoes                                  ║
║  - 13 delas eram decisoes de implementacao (mataram 90% da      ║
║    liberdade de design do agente)                                ║
║  - 5 delas eram checks de validacao (deveriam ser failure        ║
║    conditions, nao constraints)                                  ║
║  - 5 delas eram ambiguas (zero valor de orientacao)              ║
║  - O agente efetivamente recebeu uma especificacao de 23 itens   ║
║    em vez de 5 restricoes direcionais                            ║
║  - A recomendacao gerada era tecnicamente correta mas            ║
║    generica -- o agente nao teve espaco para surpreender         ║
╚══════════════════════════════════════════════════════════════════╝
```

**A regra que teria evitado tudo:**

> O intent tem um orcamento de 5 a 7 constraints. Apenas restricoes direcionais, incondicionais, em linguagem de negocio. Toda decisao de implementacao vai para Context. Todo check que so pode ser verificado apos o output existir vai para Failure Conditions (Expectations). Toda restricao ambigua sem quantificador e rejeitada.

**Sua missao:** Construir um `ConstraintBudgetGate` que recebe uma lista de constraints candidatas, as classifica em 3 categorias, aplica o limite de 5-7, e gera um `BudgetReport` com as constraints aprovadas, reclassificadas, e rejeitadas.

---

## O Cenario: Pipeline de Constraints sem Orcamento

### Contexto

Voce recebeu o codigo de um `ConstraintCollector` que coleta restricoes de stakeholders e as anexa ao intent sem filtro. O collector atual e um bucket -- tudo que chega, entra. O resultado sao intents com 15-25 "constraints" que na verdade sao uma mistura de restricoes genuinas, decisoes de implementacao, checks de validacao, e ruido.

Voce vai adicionar um `ConstraintBudgetGate` que:

1. Recebe uma lista de constraints candidatas
2. Classifica cada uma em: `BUSINESS_CONSTRAINT` (direcional, incondicional, linguagem de negocio), `IMPLEMENTATION_CHOICE` (nomeia ferramenta, padrao, ou tecnologia), `POST_HOC_CHECK` (so pode ser verificado depois do output existir), ou `AMBIGUOUS` (vago, sem quantificador)
3. Mantem apenas `BUSINESS_CONSTRAINT` -- maximo 7, ideal 5
4. Redireciona `IMPLEMENTATION_CHOICE` para Context
5. Redireciona `POST_HOC_CHECK` para Failure Conditions (Expectations)
6. Rejeita `AMBIGUOUS` com perguntas de clarificacao
7. Se mais de 7 `BUSINESS_CONSTRAINT` passarem, prioriza e corta para 7

### Dados de Entrada

O gate recebe listas como esta (versao resumida das 23):

```json
{
  "intent_id": "INT-2026-155",
  "domain": "product_recommendation",
  "candidate_constraints": [
    "Nenhum produto com alergeno do cliente nos resultados",
    "Preco dos produtos <= orcamento declarado",
    "Usar Redis para cache de perfil do cliente",
    "Tempo de resposta < 500ms",
    "Deve ser escalavel",
    "Implementar com Python 3.11 + FastAPI",
    "Explicacao referencia atributos do produto",
    "Cobertura de testes >= 80%",
    "Usar PostgreSQL com indice GIN para busca",
    "Maximo 3 produtos por recomendacao",
    "Produtos fora de estoque sao excluidos",
    "Performance aceitavel",
    "Usar JWT para autenticacao entre servicos"
  ]
}
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Classificacao em 4 categorias:** Cada constraint candidata e classificada como `BUSINESS_CONSTRAINT`, `IMPLEMENTATION_CHOICE`, `POST_HOC_CHECK`, ou `AMBIGUOUS`
2. **RF2 - Limite de 5-7:** O gate impoe um maximo de 7 `BUSINESS_CONSTRAINT`. Se houver mais de 7 aprovadas, as excedentes sao priorizadas e cortadas -- o gate explica por que cada corte foi feito
3. **RF3 - Redirecionamento para Context:** `IMPLEMENTATION_CHOICE` sao movidas para um campo `context_additions` no relatorio, com justificativa: "Esta e uma decisao de implementacao, nao uma restricao direcional. Ela pertence ao Context, nao ao Intent."
4. **RF4 - Redirecionamento para Failure Conditions:** `POST_HOC_CHECK` sao movidas para `failure_conditions` no relatorio, com justificativa: "Esta e uma verificacao que so pode ser feita apos o output existir. Ela pertence as Failure Conditions, nao as Constraints."
5. **RF5 - Rejeicao de ambiguidades:** `AMBIGUOUS` sao rejeitadas com perguntas de clarificacao especificas. Ex: "Deve ser escalavel" → "Qual a metrica de escalabilidade? (ex: suporta 10x o volume atual sem degradacao > 20%)"
6. **RF6 - Relatorio de orcamento:** O `BudgetReport` lista constraints APROVADAS (com posicao e prioridade), RECLASSIFICADAS (com destino e justificativa), e REJEITADAS (com pergunta de clarificacao)

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Gate deterministico:** `evaluate_constraints(candidates) -> BudgetReport` e deterministico
3. **RT3 - Heuristicas lexicas:** A classificacao usa palavras-chave de ferramentas, metricas, e ambiguidades -- nao requer LLM
4. **RT4 - Ordem de prioridade:** As constraints aprovadas sao ordenadas por: (1) seguranca/legal, (2) dominio/core, (3) qualidade/experiencia. O corte remove as de menor prioridade primeiro

---

## Sua Tarefa

Voce vai implementar o ConstraintBudgetGate em 3 partes.

---

### Parte 1: Diagnosticar a Lista de 23 Constraints (15 min)

Analise as constraints do prologo. Classifique manualmente cada uma das 23 em uma das 4 categorias.

```python
# As 23 constraints do prologo — classifique cada uma
CONSTRAINTS_23 = [
    "Nenhum produto com alergeno do cliente nos resultados",           # 1
    "Preco dos produtos <= orcamento declarado",                       # 2
    "Explicacao da recomendacao referencia atributos do produto",      # 3
    "Maximo 3 produtos por recomendacao",                              # 4
    "Produtos fora de estoque sao excluidos",                          # 5
    "Usar Redis para cache de perfil do cliente",                      # 6
    "Usar PostgreSQL com indice GIN para busca textual",               # 7
    "Implementar com Python 3.11 + FastAPI",                           # 8
    "Usar React 18 no frontend de recomendacao",                       # 9
    "Deploy via Docker + Kubernetes",                                  # 10
    "Logs estruturados em formato JSON",                               # 11
    "Usar JWT para autenticacao entre servicos",                       # 12
    "Implementar Circuit Breaker para API de catalogo",                # 13
    "Tempo de resposta < 500ms",                                       # 14
    "Throughput >= 100 req/s",                                         # 15
    "Disponibilidade 99.9%",                                           # 16
    "Taxa de erro < 0.1%",                                             # 17
    "Cobertura de testes >= 80%",                                      # 18
    "Deve ser escalavel",                                              # 19
    "Interface intuitiva",                                             # 20
    "Codigo limpo e bem documentado",                                  # 21
    "Performance aceitavel",                                           # 22
    "Seguranca robusta",                                               # 23
]

# TAREFA: Responda no seu codigo como comentario:
#
# 1. Classifique as 23 constraints em 4 categorias:
#    - BUSINESS_CONSTRAINT: __ itens (quais?)
#    - IMPLEMENTATION_CHOICE: __ itens (quais?)
#    - POST_HOC_CHECK: __ itens (quais?)
#    - AMBIGUOUS: __ itens (quais?)
#
# 2. Das BUSINESS_CONSTRAINT, se houver mais de 7, quais voce cortaria
#    e por que? (Use a prioridade: seguranca > dominio > qualidade)
#
# 3. Para as IMPLEMENTATION_CHOICE, para qual destino cada uma deveria
#    ir? (Context? Ou alguma e legitima como constraint externa?)
#
# 4. Para as POST_HOC_CHECK, reescreva cada uma como Failure Condition.
#    Ex: "Tempo de resposta < 500ms" → "Tempo de resposta p95 > 500ms:
#    recomendacao rejeitada, agente deve regenerar com estrategia
#    alternativa"
#
# 5. Para as AMBIGUOUS, escreva a pergunta de clarificacao para cada uma.
```

**Resposta esperada (em comentario):**

```python
# CLASSIFICACAO:
# BUSINESS_CONSTRAINT (5): 1, 2, 3, 4, 5
# IMPLEMENTATION_CHOICE (8): 6, 7, 8, 9, 10, 11, 12, 13
# POST_HOC_CHECK (5): 14, 15, 16, 17, 18
# AMBIGUOUS (5): 19, 20, 21, 22, 23
#
# As 5 BUSINESS_CONSTRAINT estao dentro do orcamento de 5-7. Nenhum corte necessario.
#
# IMPLEMENTATION_CHOICE → Context:
#   "Usar Redis para cache" → Context (stack decision, nao constraint de negocio)
#   "Usar PostgreSQL com indice GIN" → Context
#   ...etc. NENHUMA implementacao e constraint de negocio.
#
# POST_HOC_CHECK → Failure Conditions:
#   "Tempo de resposta < 500ms" → "latency p95 > 500ms: rejeitar e regenerar"
#   ...
#
# AMBIGUOUS → Perguntas:
#   "Deve ser escalavel" → "Qual metrica de escalabilidade?"
#   ...
```

---

### Parte 2: Implementar o ConstraintBudgetGate (45 min)

Implemente o gate. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class ConstraintCategory(Enum):
    """Classificacao de uma constraint candidata."""
    BUSINESS_CONSTRAINT = "business_constraint"
    IMPLEMENTATION_CHOICE = "implementation_choice"
    POST_HOC_CHECK = "post_hoc_check"
    AMBIGUOUS = "ambiguous"


class ConstraintPriority(Enum):
    """Prioridade para ordenacao e corte de constraints."""
    SECURITY_LEGAL = 1    # "alergenos sao bloqueantes", "LGPD compliance"
    DOMAIN_CORE = 2       # "orcamento e restricao", "apenas produtos em estoque"
    QUALITY_UX = 3        # "explicacao referencia produto", "max 3 recomendacoes"


@dataclass
class ClassifiedConstraint:
    """Uma constraint candidata apos classificacao."""
    original: str
    category: ConstraintCategory
    rationale: str = ""
    priority: ConstraintPriority = ConstraintPriority.QUALITY_UX
    clarification_question: str = ""  # preenchido se AMBIGUOUS
    suggested_destination: str = ""   # "context" ou "failure_conditions"


@dataclass
class BudgetReport:
    """Relatorio do Constraint Budget Gate."""
    intent_id: str
    total_candidates: int = 0
    approved: list[ClassifiedConstraint] = field(default_factory=list)
    reclassified: list[ClassifiedConstraint] = field(default_factory=list)
    rejected: list[ClassifiedConstraint] = field(default_factory=list)
    cut: list[ClassifiedConstraint] = field(default_factory=list)
    context_additions: list[str] = field(default_factory=list)
    failure_conditions: list[str] = field(default_factory=list)
    budget_remaining: int = 0
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def within_budget(self) -> bool:
        return len(self.approved) <= 7


# ============================================================
# CONSTRAINT HEURISTICS — palavras que indicam cada categoria
# ============================================================

# Palavras de ferramentas/tecnologias → IMPLEMENTATION_CHOICE
TOOL_KEYWORDS: list[str] = [
    "redis", "postgresql", "postgres", "mongo", "elasticsearch",
    "pinecone", "kafka", "rabbitmq", "docker", "kubernetes",
    "fastapi", "flask", "django", "react", "vue", "angular",
    "jwt", "oauth", "graphql", "grpc", "websocket",
    "celery", "nginx", "haproxy", "s3", "lambda",
    "circuit breaker", "python 3", "python3",
]

# Metricas e thresholds → POST_HOC_CHECK
METRIC_KEYWORDS: list[str] = [
    "< ", "> ", "<=", ">=", "ms", "req/s", "%",
    "latencia", "throughput", "disponibilidade", "uptime",
    "taxa de erro", "cobertura", "p95", "p99",
    "no maximo", "no minimo", "pelo menos",
]

# Palavras ambiguas sem quantificador → AMBIGUOUS
AMBIGUOUS_KEYWORDS: list[str] = [
    "escalavel", "intuitivo", "intuitiva", "limpo", "robusto",
    "robusta", "aceitavel", "bom", "boa", "eficiente",
    "moderno", "moderna", "melhor", "rapido", "rapida",
    "seguro", "segura",
]

# Palavras de negocio → BUSINESS_CONSTRAINT
BUSINESS_KEYWORDS: list[str] = [
    "cliente", "produto", "orcamento", "alergeno", "restricao",
    "alimentar", "estoque", "preco", "pedido", "entrega",
    "recomendacao", "atributo", "explicacao", "catalogo",
]


# ============================================================
# CONSTRAINT BUDGET GATE — nucleo do exercicio
# ============================================================

def classify_constraint(constraint: str) -> ClassifiedConstraint:
    """
    Classifica uma constraint candidata em uma das 4 categorias.

    Heuristicas (em ordem de precedencia):
    1. Se contem palavras ambiguas sem quantificador: AMBIGUOUS
    2. Se contem metricas/thresholds mensuraveis: POST_HOC_CHECK
    3. Se contem nomes de ferramentas/tecnologias: IMPLEMENTATION_CHOICE
    4. Senao, se descreve uma restricao de negocio direcional: BUSINESS_CONSTRAINT

    Args:
        constraint: O texto da constraint candidata.

    Returns:
        ClassifiedConstraint com categoria e justificativa.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. lower = constraint.lower()
    # 2. Verificar AMBIGUOUS primeiro:
    #    a. Se contem palavra ambigua E nao contem metrica/numero:
    #       → AMBIGUOUS
    #    b. Ex: "deve ser escalavel" (ambiguo sem "suporta X req/s")
    #    c. Ex: "Tempo de resposta < 500ms" (NAO ambiguo — tem metrica)
    # 3. Verificar POST_HOC_CHECK:
    #    a. Se contem operador de comparacao (<, >, <=, >=) OU
    #       contem unidade de medida (ms, req/s, %):
    #       → POST_HOC_CHECK
    #    b. Ex: "Tempo de resposta < 500ms", "Cobertura >= 80%"
    # 4. Verificar IMPLEMENTATION_CHOICE:
    #    a. Se contem nome de ferramenta/tecnologia:
    #       → IMPLEMENTATION_CHOICE
    #    b. Ex: "Usar Redis", "Implementar com FastAPI"
    # 5. Senao: BUSINESS_CONSTRAINT
    # 6. Preencher rationale explicando a decisao
    pass


def assign_priority(constraint: ClassifiedConstraint) -> ConstraintPriority:
    """
    Atribui prioridade a uma BUSINESS_CONSTRAINT para ordenacao de corte.

    SEQUENCIA: SECURITY_LEGAL > DOMAIN_CORE > QUALITY_UX

    Heuristicas:
    - SECURITY_LEGAL: menciona "alergeno", "bloqueante", "proibido",
      "legal", "LGPD", "compliance", "nunca", "zero"
    - DOMAIN_CORE: menciona "orcamento", "preco", "estoque",
      "catalogo", "pedido"
    - QUALITY_UX: menciona "explicacao", "maximo", "atributos",
      "cliente ve", "experiencia"

    Args:
        constraint: A constraint classificada como BUSINESS_CONSTRAINT.

    Returns:
        ConstraintPriority atribuida.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. lower = constraint.original.lower()
    # 2. Se contem palavras de seguranca/legal: SECURITY_LEGAL
    # 3. Senao, se contem palavras de dominio core: DOMAIN_CORE
    # 4. Senao: QUALITY_UX
    pass


def generate_clarification_question(constraint: str) -> str:
    """
    Gera uma pergunta de clarificacao especifica para uma constraint ambigua.

    Args:
        constraint: O texto da constraint ambigua.

    Returns:
        Uma pergunta direcionada (nao generica).
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido (template por palavra-chave):
    # 1. Se contem "escalavel":
    #    → "Qual a metrica de escalabilidade? (ex: suporta 10x volume atual
    #       com degradacao maxima de 20% na latencia p95)"
    # 2. Se contem "intuitivo" ou "intuitiva":
    #    → "Qual o criterio de intuitividade? (ex: usuario completa tarefa
    #       principal em < 30s sem ajuda na primeira sessao)"
    # 3. Se contem "limpo" ou "documentado":
    #    → "Qual o criterio objetivo? (ex: zero funcoes > 50 linhas,
    #       docstring em 100% das funcoes publicas)"
    # 4. Se contem "performance" ou "rapido" ou "eficiente":
    #    → "Qual a metrica de performance? (ex: p95 < 200ms, p99 < 500ms)"
    # 5. Se contem "seguro" ou "seguranca":
    #    → "Qual o criterio de seguranca? (ex: OWASP Top 10 zerado,
    #       zero secrets em codigo, autenticacao em todas as rotas)"
    # 6. Fallback: "Qual o criterio objetivo e mensuravel para [constraint]?"
    pass


def suggest_destination(constraint: ClassifiedConstraint) -> str:
    """
    Para IMPLEMENTATION_CHOICE e POST_HOC_CHECK, sugere o destino correto.

    Args:
        constraint: A constraint classificada.

    Returns:
        "context" para IMPLEMENTATION_CHOICE, "failure_conditions" para POST_HOC_CHECK.
    """
    # SEU CODIGO AQUI
    if constraint.category == ConstraintCategory.IMPLEMENTATION_CHOICE:
        return "context"
    elif constraint.category == ConstraintCategory.POST_HOC_CHECK:
        return "failure_conditions"
    return ""


def apply_budget(
    approved: list[ClassifiedConstraint],
    max_constraints: int = 7,
) -> list[ClassifiedConstraint]:
    """
    Aplica o limite de constraints: mantem no maximo max_constraints,
    ordenadas por prioridade. As excedentes sao cortadas.

    Args:
        approved: Lista de BUSINESS_CONSTRAINT aprovadas.
        max_constraints: Limite maximo (default 7).

    Returns:
        Lista ordenada com no maximo max_constraints itens.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Ordenar approved por priority (SECURITY_LEGAL primeiro)
    # 2. Se len(approved) <= max_constraints: retornar todas
    # 3. Se len(approved) > max_constraints:
    #    a. Manter as primeiras max_constraints
    #    b. As restantes vao para a lista de "cut"
    #    c. Retornar apenas as mantidas
    # 4. Em caso de empate na mesma prioridade, manter ordem original
    pass


def evaluate_constraints(
    intent_id: str,
    candidate_constraints: list[str],
    max_budget: int = 7,
) -> BudgetReport:
    """
    Avalia uma lista de constraints candidatas contra o Constraint Budget Gate.

    Fluxo completo:
    1. Classificar cada constraint
    2. Separar BUSINESS_CONSTRAINT das demais
    3. Atribuir prioridades as BUSINESS_CONSTRAINT
    4. Aplicar orcamento (max_budget)
    5. Gerar clarification questions para AMBIGUOUS
    6. Gerar destinations para IMPLEMENTATION_CHOICE e POST_HOC_CHECK
    7. Produzir BudgetReport

    Args:
        intent_id: ID do intent.
        candidate_constraints: Lista de constraints candidatas.
        max_budget: Limite maximo de constraints aprovadas.

    Returns:
        BudgetReport completo.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. classified = [classify_constraint(c) for c in candidate_constraints]
    # 2. approved_raw = [c for c in classified if c.category == BUSINESS_CONSTRAINT]
    # 3. Para cada aprovada: assign_priority(a)
    # 4. approved, cut = separar por orcamento
    # 5. reclassified = [c for c in classified if c.category in (IMPLEMENTATION_CHOICE, POST_HOC_CHECK)]
    # 6. rejected = [c for c in classified if c.category == AMBIGUOUS]
    #    a. Para cada rejected: generate_clarification_question
    # 7. Para cada reclassified: suggest_destination
    # 8. Preencher BudgetReport
    # 9. Retornar
    pass


# ============================================================
# TESTES RAPIDOS: ConstraintBudgetGate
# ============================================================

if __name__ == "__main__":
    # Teste 1: Classificar constraint de negocio
    c = classify_constraint("Nenhum produto com alergeno do cliente nos resultados")
    assert c.category == ConstraintCategory.BUSINESS_CONSTRAINT, (
        f"Esperado BUSINESS_CONSTRAINT, obtido {c.category.value}"
    )
    print("Teste 1 passou: constraint de negocio detectada")

    # Teste 2: Classificar implementacao disfarcada
    c = classify_constraint("Usar Redis para cache de perfil do cliente")
    assert c.category == ConstraintCategory.IMPLEMENTATION_CHOICE, (
        f"Esperado IMPLEMENTATION_CHOICE, obtido {c.category.value}"
    )
    print("Teste 2 passou: implementacao disfarcada detectada")

    # Teste 3: Classificar check pos-hoc
    c = classify_constraint("Tempo de resposta < 500ms")
    assert c.category == ConstraintCategory.POST_HOC_CHECK, (
        f"Esperado POST_HOC_CHECK, obtido {c.category.value}"
    )
    print("Teste 3 passou: check pos-hoc detectado")

    # Teste 4: Classificar ambiguidade
    c = classify_constraint("Deve ser escalavel")
    assert c.category == ConstraintCategory.AMBIGUOUS, (
        f"Esperado AMBIGUOUS, obtido {c.category.value}"
    )
    assert c.clarification_question != "", "Deve gerar pergunta de clarificacao"
    print(f"Teste 4 passou: ambiguidade detectada")
    print(f"  Pergunta: {c.clarification_question}")

    # Teste 5: Orcamento aplicado — 10 aprovadas → 7 mantidas, 3 cortadas
    ten_business = [
        "Nenhum produto com alergeno do cliente",
        "Preco <= orcamento declarado",
        "Explicacao referencia atributos do produto",
        "Maximo 3 produtos por recomendacao",
        "Produtos fora de estoque excluidos",
        "Cliente pode refinar busca por categoria",
        "Recomendacao inclui comparativo de preco",
        "Produtos ordenados por relevancia",
        "Pelo menos 1 produto da categoria preferida do cliente",
        "Resultados Exibidos em menos de 2 segundos",
    ]
    report = evaluate_constraints("INT-001", ten_business, max_budget=7)
    assert len(report.approved) == 7, f"Esperado 7 aprovadas, obtido {len(report.approved)}"
    assert len(report.cut) == 3, f"Esperado 3 cortadas, obtido {len(report.cut)}"
    assert report.within_budget, "Deve estar dentro do orcamento"
    print(f"\nTeste 5 passou: orcamento aplicado")
    print(f"  Aprovadas: {len(report.approved)}")
    print(f"  Cortadas: {len(report.cut)}")

    # Teste 6: Relatorio completo com as 23 constraints
    all_23 = [
        "Nenhum produto com alergeno do cliente nos resultados",
        "Preco dos produtos <= orcamento declarado",
        "Explicacao da recomendacao referencia atributos do produto",
        "Maximo 3 produtos por recomendacao",
        "Produtos fora de estoque sao excluidos",
        "Usar Redis para cache de perfil do cliente",
        "Usar PostgreSQL com indice GIN para busca textual",
        "Implementar com Python 3.11 + FastAPI",
        "Usar React 18 no frontend de recomendacao",
        "Deploy via Docker + Kubernetes",
        "Logs estruturados em formato JSON",
        "Usar JWT para autenticacao entre servicos",
        "Implementar Circuit Breaker para API de catalogo",
        "Tempo de resposta < 500ms",
        "Throughput >= 100 req/s",
        "Disponibilidade 99.9%",
        "Taxa de erro < 0.1%",
        "Cobertura de testes >= 80%",
        "Deve ser escalavel",
        "Interface intuitiva",
        "Codigo limpo e bem documentado",
        "Performance aceitavel",
        "Seguranca robusta",
    ]
    report = evaluate_constraints("INT-155", all_23)
    print(f"\nTeste 6 passou: relatorio completo das 23 constraints")
    print(f"  Total: {report.total_candidates}")
    print(f"  Aprovadas (BUSINESS_CONSTRAINT): {len(report.approved)}")
    print(f"  Reclassificadas: {len(report.reclassified)}")
    print(f"    → Context: {len([c for c in report.reclassified if c.suggested_destination == 'context'])}")
    print(f"    → Failure Conditions: {len([c for c in report.reclassified if c.suggested_destination == 'failure_conditions'])}")
    print(f"  Rejeitadas (AMBIGUOUS): {len(report.rejected)}")
    print(f"  Cortadas (excedente): {len(report.cut)}")
    print(f"  Orcamento restante: {report.budget_remaining}")

    print("\nTodos os testes do ConstraintBudgetGate passaram!")
```

---

### Parte 3: Pipeline de Intent com Constraint Budget Gate (25 min)

Agora implemente o pipeline que integra o `ConstraintBudgetGate` ao fluxo de criacao de intents:

```python
# ============================================================
# INTENT BUILDER COM CONSTRAINT BUDGET GATE
# ============================================================

@dataclass
class GatedIntent:
    """Intent apos passar pelo ConstraintBudgetGate."""
    intent_id: str
    original_constraints: list[str]
    budget_report: BudgetReport
    final_constraints: list[str] = field(default_factory=list)
    context_additions: list[str] = field(default_factory=list)
    failure_conditions: list[str] = field(default_factory=list)
    pending_clarifications: list[str] = field(default_factory=list)


def build_gated_intent(
    intent_id: str,
    candidate_constraints: list[str],
    max_budget: int = 7,
) -> GatedIntent:
    """
    Constroi um intent passando as constraints pelo Budget Gate.

    Fluxo:
    1. evaluate_constraints() → BudgetReport
    2. Extrair final_constraints das aprovadas
    3. Extrair context_additions das reclassificadas (IMPLEMENTATION_CHOICE)
    4. Extrair failure_conditions das reclassificadas (POST_HOC_CHECK)
    5. Extrair pending_clarifications das rejeitadas (AMBIGUOUS)
    6. Retornar GatedIntent

    Args:
        intent_id: ID do intent.
        candidate_constraints: Lista bruta de constraints.
        max_budget: Limite maximo.

    Returns:
        GatedIntent com constraints filtradas e reclassificadas.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. report = evaluate_constraints(intent_id, candidate_constraints, max_budget)
    # 2. final_constraints = [c.original for c in report.approved]
    # 3. context_additions = [c.original for c in report.reclassified
    #    if c.suggested_destination == "context"]
    # 4. failure_conditions = [c.original for c in report.reclassified
    #    if c.suggested_destination == "failure_conditions"]
    # 5. pending_clarifications = [c.clarification_question for c in report.rejected]
    # 6. Retornar GatedIntent
    pass


# ============================================================
# TESTE COMPLETO DO PIPELINE
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTE DO PIPELINE DE INTENT COM BUDGET GATE")
    print("=" * 60)

    # Cenario realista: intent de recomendacao com constraints misturadas
    gated = build_gated_intent(
        intent_id="INT-2026-155",
        candidate_constraints=[
            # 5 boas constraints de negocio
            "Nenhum produto com alergeno do cliente nos resultados",
            "Preco dos produtos <= orcamento declarado",
            "Explicacao da recomendacao referencia atributos do produto",
            "Maximo 3 produtos por recomendacao",
            "Produtos fora de estoque sao excluidos",
            # 5 implementacoes disfarcadas
            "Usar Redis para cache de perfil do cliente",
            "Implementar com Python 3.11 + FastAPI",
            "Usar JWT para autenticacao entre servicos",
            "Deploy via Docker + Kubernetes",
            "Logs estruturados em formato JSON",
            # 3 checks pos-hoc
            "Tempo de resposta < 500ms",
            "Cobertura de testes >= 80%",
            "Disponibilidade 99.9%",
            # 3 ambiguidades
            "Deve ser escalavel",
            "Interface intuitiva",
            "Performance aceitavel",
        ],
    )

    print(f"\nIntent ID: {gated.intent_id}")
    print(f"Constraints originais: {len(gated.original_constraints)}")
    print(f"Constraints finais (apos gate): {len(gated.final_constraints)}")
    for i, c in enumerate(gated.final_constraints):
        print(f"  [{i+1}] {c}")

    print(f"\nRedirecionadas para Context: {len(gated.context_additions)}")
    for c in gated.context_additions:
        print(f"  → {c}")

    print(f"\nRedirecionadas para Failure Conditions: {len(gated.failure_conditions)}")
    for c in gated.failure_conditions:
        print(f"  → {c}")

    print(f"\nClarificacoes pendentes: {len(gated.pending_clarifications)}")
    for q in gated.pending_clarifications:
        print(f"  ? {q}")

    # Verificacoes
    assert len(gated.final_constraints) == 5, (
        f"Deve ter 5 constraints finais, obtido {len(gated.final_constraints)}"
    )
    assert len(gated.context_additions) == 5, (
        f"Deve ter 5 redirecionamentos para Context"
    )
    assert len(gated.failure_conditions) == 3, (
        f"Deve ter 3 redirecionamentos para Failure Conditions"
    )
    assert len(gated.pending_clarifications) == 3, (
        f"Deve ter 3 clarificacoes pendentes"
    )
    assert gated.budget_report.within_budget, "Deve estar dentro do orcamento"

    print(f"\nOrcamento utilizado: {len(gated.final_constraints)}/7")
    print("GatedIntent construido com sucesso!")

    print("\n" + "=" * 60)
    print("PIPELINE DE INTENT COM BUDGET GATE COMPLETO")
    print("=" * 60)
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce classificou as 23 constraints em 4 categorias com contagem correta (5 + 8 + 5 + 5)
- [ ] Voce gerou perguntas de clarificacao para as 5 ambiguidades
- [ ] Voce sugeriu o destino correto (Context / Failure Conditions) para as reclassificadas

### Criterio 2: Classificador funcional

- [ ] `classify_constraint()` classifica corretamente constraints de negocio, implementacao, check, e ambiguidade
- [ ] `assign_priority()` prioriza SECURITY_LEGAL > DOMAIN_CORE > QUALITY_UX
- [ ] `generate_clarification_question()` gera perguntas especificas (nao genericas)
- [ ] `suggest_destination()` retorna "context" para implementacao e "failure_conditions" para checks

### Criterio 3: Orcamento

- [ ] `apply_budget()` mantem no maximo `max_constraints` itens
- [ ] Itens cortados sao os de menor prioridade
- [ ] Se <= max_constraints, nenhum corte ocorre

### Criterio 4: Relatorio

- [ ] `evaluate_constraints()` produz BudgetReport com approved, reclassified, rejected, cut
- [ ] `context_additions` contem constraints de implementacao redirecionadas
- [ ] `failure_conditions` contem checks redirecionados
- [ ] `budget_remaining` reflete corretamente o orcamento

### Criterio 5: Testes

- [ ] Teste 1: constraint de negocio detectada
- [ ] Teste 2: implementacao disfarcada detectada
- [ ] Teste 3: check pos-hoc detectado
- [ ] Teste 4: ambiguidade detectada com pergunta gerada
- [ ] Teste 5: orcamento aplicado (10 → 7 aprovadas, 3 cortadas)
- [ ] Teste 6: relatorio completo das 23 constraints

---

## Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao classificou ou errou > 50% | Classificou parcialmente (~70%) | Classificou corretamente (~90%) | Classificacao exata + perguntas e destinos para todas |
| **Classificador (Parte 2)** | 35% | Heuristicas ausentes | Classifica 2 de 4 categorias | Classifica todas as 4 categorias | Classificador completo com prioridades, perguntas, e destinos |
| **Orcamento e Relatorio (Parte 3)** | 35% | Nao implementado | Orcamento sem corte por prioridade | Orcamento com prioridade + relatorio | Pipeline completo: gate → relatorio → gated intent com 4 destinos |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 5 criterios passam | Todos os 6 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para a Classificacao

1. **A ordem de verificacao importa.** AMBIGUOUS deve ser verificado primeiro -- se uma constraint e ambigua, nao importa se tambem contem nome de ferramenta. Ex: "Usar um banco escalavel" → AMBIGUOUS (escalavel sem metrica), nao IMPLEMENTATION_CHOICE.

2. **Metricas com numeros sao POST_HOC_CHECK.** "< 500ms", ">= 80%", "99.9%", "100 req/s" -- a presenca de um numero com unidade de medida e o sinal mais forte de que e uma verificacao, nao uma constraint direcional.

3. **"Usar [ferramenta]" e IMPLEMENTATION_CHOICE.** Mesmo que a frase nao tenha um verbo de implementacao explicito, nomear uma ferramenta a torna uma escolha de implementacao.

### Para o Orcamento

1. **Seguranca nunca e cortada.** Se uma constraint de seguranca (alergeno bloqueante, nunca expor dado do cliente) ocupar a posicao 8, ela substitui uma constraint de qualidade na posicao 7. A prioridade SECURITY_LEGAL e inegociavel.

2. **O numero magico e 5-7.** Abaixo de 5: o agente tem informacao insuficiente. Acima de 7: a lista vira especificacao. O gate nao e binario ("passou/falhou") -- e um orcamento. Ele diz "voce tem 7 slots, escolha os mais importantes".

3. **Corte nao e descarte.** As constraints cortadas aparecem no relatorio como `cut` com justificativa. O outcome owner pode revisar e trocar uma constraint aprovada por uma cortada -- mas o total permanece <= 7.

### Para o Destino

1. **Context e persistido, nao descartado.** Quando uma constraint "Usar Redis" e movida para Context, ela nao desaparece. Ela vai para o contexto que o harness monta para o agente. O agente ainda SABE que Redis esta disponivel -- mas nao e OBRIGADO a usa-lo.

2. **Failure Conditions sao verificadas pelo Evaluator.** "Tempo de resposta < 500ms" nao e algo que o agente "respeita" -- e algo que o Evaluator MEDE depois que o agente produziu o output. Essa distincao e o coracao do Generator-Evaluator.

---

## Duvidas Comuns

**P: 5-7 constraints nao e muito pouco? E se o dominio realmente precisar de mais?**
R: O limite de 5-7 e uma heuristica, nao uma lei. Dominios regulados (saude, financeiro) podem precisar de 10-12. Mas se voce PRECISA de mais de 7, cada constraint adicional deve ser justificada. O gate aceita um parametro `max_budget` configuravel. O ponto nao e o numero exato -- e a disciplina de perguntar "esta constraint e realmente direcional ou e uma decisao de implementacao disfarcada?"

**P: O que acontece se uma constraint de implementacao for uma decisao arquitetural irrevogavel?**
R: Ela vai para Context com a anotacao "architectural decision -- nao remover". O gate classifica, nao deleta. A decisao de "usar PostgreSQL" como banco principal e uma decisao arquitetural que pertence ao Context -- o agente precisa saber disso, mas como FATO, nao como RESTRICAO.

**P: Como isso se relaciona com a Constraint-Failure Decision Rule?**
R: O Budget Gate classifica constraints em 4 categorias. A Decision Rule foca especificamente na fronteira entre BUSINESS_CONSTRAINT e POST_HOC_CHECK, aplicando a pergunta "saber isso mudaria como o builder escreve o codigo?" Sao gates complementares: o Budget Gate da o limite numerico, a Decision Rule da o criterio de classificacao.

**P: E se todas as 5-7 constraints forem de seguranca e nenhuma de qualidade?**
R: Isso e um sinal de que o time esta pensando apenas em evitar desastres, nao em entregar valor. O gate nao resolve isso -- mas o relatorio mostra a distribuicao de prioridades, e um reviewer humano pode notar a ausencia de constraints de qualidade.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns.md` para entender o contexto completo do padrao
2. Compare com `docs/canonical/constraint-anchored-evaluation.md` -- observe como as constraints que passam pelo Budget Gate alimentam o verificador de constraints
3. (Opcional) Integre o ConstraintBudgetGate ao Intent Five-Part Primitive: o campo `constraints` do intent so aceita BUSINESS_CONSTRAINT que passaram pelo gate

---

*Exercicio Constraint Budget Gate | Nivel 3 - Arquitetura Avancada*

**Cinco a sete. Direcionais. Linguagem de negocio. Nada alem disso.**
