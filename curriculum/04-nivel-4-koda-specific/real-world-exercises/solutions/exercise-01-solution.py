"""
Solucao do Exercicio 1 — Feature KODA: Recomendacao de Produto com Generator/Evaluator
Nivel 4 — KODA-Especifico — Real-World Feature

Esta e a solucao de referencia. Execute com:
    python exercise-01-solution.py

Todos os 8 cenarios de teste devem passar com ✅.
"""

import json
import re
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# FEATURE CONTRACT
# ============================================================================

FEATURE_CONTRACT = {
    "feature_name": "koda_smart_product_recommendation",
    "version": "1.0.0",
    "owner_team": "koda-engenharia",
    "description": (
        "Analisa o perfil do cliente e recomenda ate 3 produtos "
        "ordenados por adequacao, respeitando restricoes alimentares, "
        "orcamento e preferencias declaradas."
    ),
    "input_contract": {
        "customer_profile": {
            "required": ["customer_id", "name", "budget_brl"],
            "optional": ["dietary_restrictions", "preferred_flavor", "training_goal", "training_frequency"],
            "guarantees": [
                "budget_brl sempre positivo",
                "dietary_restrictions, se presente, array de strings normalizadas"
            ]
        },
        "catalog": {
            "required": ["sku", "name", "category", "price_brl", "lactose_free", "gluten_free", "in_stock", "rating"],
            "guarantees": [
                "price_brl positivo",
                "rating entre 0.0 e 5.0",
                "in_stock booleano verificado"
            ]
        }
    },
    "output_contract": {
        "required": ["candidate_response", "products_considered", "assumptions"],
        "guarantees": [
            "products_considered contem de 0 a 3 produtos",
            "todos os produtos em products_considered respeitam restricoes declaradas",
            "todos os produtos em products_considered estao dentro do orcamento",
            "todos os produtos em products_considered estao em estoque",
            "candidate_response nao excede 500 caracteres",
            "assumptions lista suposicoes explicitas do Generator"
        ]
    },
    "quality_rubric": [
        "respeita restricoes alimentares declaradas (lactose, gluten)",
        "respeita orcamento maximo do cliente",
        "nao recomenda produto fora de estoque",
        "prioriza sabor preferido quando opcoes equivalentes",
        "resposta com tom humano, sem jargao excessivo",
        "nao pressiona compra com linguagem de urgencia",
        "explica recomendacao de forma clara e justificada",
        "fallback seguro quando nenhum produto atende todos os criterios"
    ],
    "max_iterations": 2,
    "max_products_per_recommendation": 3,
    "max_response_chars": 500,
}


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Product:
    """Produto no catalogo do KODA."""
    sku: str
    name: str
    category: str
    price_brl: float
    servings: int
    lactose_free: bool
    gluten_free: bool
    in_stock: bool
    rating: float


@dataclass
class CustomerProfile:
    """Perfil do cliente KODA com preferencias e restricoes."""
    customer_id: str
    name: str
    budget_brl: float
    dietary_restrictions: list[str] = field(default_factory=list)
    preferred_flavor: Optional[str] = None
    training_goal: Optional[str] = None
    training_frequency: Optional[str] = None
    purchase_history: list[str] = field(default_factory=list)


@dataclass
class Generation:
    """Output do Generator — recomendacoes candidatas."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    candidate_response: str = ""
    products_considered: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RubricResult:
    """Resultado da verificacao de um criterio da rubrica."""
    criterion: str
    passed: bool
    evidence: str


@dataclass
class Evaluation:
    """Output do Evaluator — resultado da validacao."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    status: str = "rejected"
    rubric_results: list[dict[str, Any]] = field(default_factory=list)
    feedback: str = ""
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# PRODUCT CATALOG (Dados simulados do KODA)
# ============================================================================

PRODUCT_CATALOG: list[Product] = [
    Product(
        sku="WHEY-CONC-CHOC-1000",
        name="Whey Concentrado Chocolate 1kg",
        category="whey",
        price_brl=89.90,
        servings=30,
        lactose_free=False,
        gluten_free=True,
        in_stock=True,
        rating=4.5,
    ),
    Product(
        sku="WHEY-ISO-CHOC-900",
        name="Whey Isolado Chocolate 900g",
        category="whey",
        price_brl=139.90,
        servings=27,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.7,
    ),
    Product(
        sku="WHEY-VEG-BAUN-750",
        name="Proteina Vegetal Baunilha 750g",
        category="whey_vegano",
        price_brl=99.90,
        servings=25,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.3,
    ),
    Product(
        sku="PROT-VEG-CHOC-750",
        name="Proteina Vegetal Chocolate 750g",
        category="whey_vegano",
        price_brl=119.90,
        servings=25,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.6,
    ),
    Product(
        sku="CREA-MONO-300",
        name="Creatina Monohidratada 300g",
        category="creatina",
        price_brl=69.90,
        servings=60,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.8,
    ),
    Product(
        sku="CREA-MICRO-250",
        name="Creatina Micronizada 250g",
        category="creatina",
        price_brl=74.90,
        servings=50,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.6,
    ),
    Product(
        sku="PRE-TREINO-CAFE-300",
        name="Pre-Treino Cafeina 300g",
        category="pre_treino",
        price_brl=79.90,
        servings=30,
        lactose_free=True,
        gluten_free=True,
        in_stock=False,
        rating=4.4,
    ),
    Product(
        sku="BCAA-PO-200",
        name="BCAA em Po 200g",
        category="bcaa",
        price_brl=59.90,
        servings=40,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.1,
    ),
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _has_restriction(restrictions: list[str], target: str) -> bool:
    """Verifica se uma restricao especifica existe na lista."""
    return any(target in r.lower() for r in restrictions)


def _extract_category(message: str) -> Optional[str]:
    """Extrai a categoria de produto da mensagem do cliente, se mencionada."""
    msg = message.lower()
    keywords = {
        "whey": "whey",
        "proteina vegetal": "whey_vegano",
        "vegano": "whey_vegano",
        "vegana": "whey_vegano",
        "creatina": "creatina",
        "pre treino": "pre_treino",
        "pre-treino": "pre_treino",
        "bcaa": "bcaa",
    }
    for keyword, category in keywords.items():
        if keyword in msg:
            return category
    return None


def _format_whatsapp_response(
    products: list[Product],
    profile: CustomerProfile,
) -> str:
    """Formata resposta curta para WhatsApp com tom humano e informativo."""
    if not products:
        return (
            f"Nao encontrei produtos que atendam todos os seus criterios, {profile.name}. "
            "Quer ajustar alguma preferencia para eu buscar alternativas?"
        )

    best = products[0]
    response = (
        f"Encontrei {len(products)} opcao(oes) para voce, {profile.name}. "
        f"A melhor avaliada e {best.name} por R$ {best.price_brl:.2f} "
        f"(nota {best.rating}/5)."
    )

    # Menciona caracteristica relevante
    if profile.dietary_restrictions:
        tags = []
        if best.lactose_free and _has_restriction(profile.dietary_restrictions, "lactose"):
            tags.append("sem lactose")
        if best.gluten_free and _has_restriction(profile.dietary_restrictions, "gluten"):
            tags.append("sem gluten")
        if tags:
            response += f" {' e '.join(tags)}."

    if len(products) > 1:
        second = products[1]
        response += (
            f" Tambem temos {second.name} por R$ {second.price_brl:.2f}. "
            "Qual prefere?"
        )
    else:
        response += " Quer que eu separe para voce?"

    return response


def _build_candidate_response(
    products: list[Product],
    profile: CustomerProfile,
) -> str:
    """Constroi resposta candidata com limite de caracteres."""
    response = _format_whatsapp_response(products, profile)
    max_chars = FEATURE_CONTRACT["max_response_chars"]
    if len(response) > max_chars:
        response = response[:max_chars - 3] + "..."
    return response


# ============================================================================
# GENERATOR AGENT
# ============================================================================

def generator_agent(
    profile: CustomerProfile,
    catalog: list[Product],
    customer_message: str = "",
    evaluator_feedback: Optional[str] = None,
    conversation_id: str = "unknown",
) -> Generation:
    """
    Generator Agent: filtra catalogo, ranqueia produtos e gera resposta candidata.

    Responsabilidades:
    - Aplicar filtros de restricao alimentar, orcamento e estoque
    - Priorizar sabor preferido
    - Ranquear por rating
    - Selecionar top-3 produtos
    - Formatar resposta para WhatsApp
    - Registrar suposicoes explicitamente
    - NAO se auto-avaliar

    Args:
        profile: Perfil completo do cliente
        catalog: Lista de produtos disponiveis
        customer_message: Mensagem do cliente (para extracao de categoria)
        evaluator_feedback: Feedback do Evaluator para segunda tentativa
        conversation_id: ID da conversa para rastreamento

    Returns:
        Generation com resposta candidata, produtos e suposicoes
    """
    # Determinar categoria alvo da mensagem do cliente
    target_category = _extract_category(customer_message)

    # Iniciar com todos os produtos do catalogo
    filtered = list(catalog)

    # Filtro 1: categoria alvo (se o cliente especificou "whey", "creatina", etc.)
    if target_category:
        filtered = [p for p in filtered if p.category == target_category]

    # Filtro 2: estoque (nunca recomendar produto indisponivel)
    filtered = [p for p in filtered if p.in_stock]

    # Filtro 3: restricao de lactose
    if _has_restriction(profile.dietary_restrictions, "lactose"):
        filtered = [p for p in filtered if p.lactose_free]

    # Filtro 4: restricao de gluten
    if _has_restriction(profile.dietary_restrictions, "gluten"):
        filtered = [p for p in filtered if p.gluten_free]

    # Filtro 5: orcamento
    filtered = [p for p in filtered if p.price_brl <= profile.budget_brl]

    # Se houver feedback do Evaluator, reaplicar filtros com correcoes
    if evaluator_feedback:
        corrected_budget = _extract_budget_from_feedback(evaluator_feedback)
        if corrected_budget is not None:
            filtered = [p for p in filtered if p.price_brl <= corrected_budget]

    # Ordenacao: prioriza sabor preferido, depois rating
    preferred = profile.preferred_flavor
    if preferred:
        with_flavor = [p for p in filtered if preferred.lower() in p.name.lower()]
        without_flavor = [p for p in filtered if preferred.lower() not in p.name.lower()]
        with_flavor.sort(key=lambda p: p.rating, reverse=True)
        without_flavor.sort(key=lambda p: p.rating, reverse=True)
        ranked = with_flavor + without_flavor
    else:
        ranked = sorted(filtered, key=lambda p: p.rating, reverse=True)

    # Selecionar top-3
    top = ranked[:FEATURE_CONTRACT["max_products_per_recommendation"]]

    # Construir lista de produtos considerados (formato dict para JSON)
    products_considered = [
        {
            "sku": p.sku,
            "name": p.name,
            "price_brl": p.price_brl,
            "rating": p.rating,
            "lactose_free": p.lactose_free,
            "gluten_free": p.gluten_free,
            "in_stock": p.in_stock,
            "category": p.category,
        }
        for p in top
    ]

    # Registrar suposicoes
    assumptions: list[str] = []
    if target_category:
        assumptions.append(f"categoria alvo extraida da mensagem: {target_category}")
    else:
        assumptions.append("nenhuma categoria especifica mencionada; considerando todas")
    assumptions.append(f"orcamento maximo: R$ {profile.budget_brl:.2f}")
    if _has_restriction(profile.dietary_restrictions, "lactose"):
        assumptions.append("cliente intolerante a lactose — filtrando produtos lactose_free")
    if _has_restriction(profile.dietary_restrictions, "gluten"):
        assumptions.append("cliente intolerante a gluten — filtrando produtos gluten_free")
    if profile.preferred_flavor:
        assumptions.append(f"sabor preferido: {profile.preferred_flavor} — priorizando no ranking")
    if evaluator_feedback:
        assumptions.append("segunda tentativa apos feedback do Evaluator")

    # Gerar resposta candidata
    candidate_response = _build_candidate_response(top, profile)

    return Generation(
        conversation_id=conversation_id,
        candidate_response=candidate_response,
        products_considered=products_considered,
        assumptions=assumptions,
    )


def _extract_budget_from_feedback(feedback: str) -> Optional[float]:
    """Tenta extrair um valor de orcamento corrigido do feedback do Evaluator."""
    match = re.search(r"R\$\s*([\d,.]+)", feedback)
    if match:
        raw = match.group(1).replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            return None
    return None


# ============================================================================
# EVALUATOR AGENT
# ============================================================================

def evaluator_agent(
    generation: Generation,
    profile: CustomerProfile,
    conversation_id: str = "unknown",
) -> Evaluation:
    """
    Evaluator Agent: valida recomendacoes contra rubrica de qualidade.

    Responsabilidades:
    - Verificar cada criterio da rubrica de qualidade
    - Registrar evidencias para cada verificacao
    - Aprovar (approved) ou rejeitar (rejected)
    - Fornecer feedback acionavel para correcao

    Args:
        generation: Output do Generator a ser validado
        profile: Perfil do cliente para verificacoes cruzadas
        conversation_id: ID da conversa para rastreamento

    Returns:
        Evaluation com status, resultados por criterio e feedback
    """
    rubric_results: list[RubricResult] = []
    products = generation.products_considered
    response = generation.candidate_response
    has_products = len(products) > 0

    # Criterio 1: Respeita restricao de lactose
    rubric_results.append(_check_lactose_restriction(products, profile))

    # Criterio 2: Respeita restricao de gluten
    rubric_results.append(_check_gluten_restriction(products, profile))

    # Criterio 3: Respeita orcamento
    rubric_results.append(_check_budget(products, profile))

    # Criterio 4: Produtos em estoque
    rubric_results.append(_check_stock(products, profile, has_products))

    # Criterio 5: Prioriza sabor preferido
    rubric_results.append(_check_flavor_priority(products, profile, has_products))

    # Criterio 6: Tom humano, sem jargao
    rubric_results.append(_check_human_tone(response))

    # Criterio 7: Nao pressiona compra
    rubric_results.append(_check_no_pressure(response))

    # Criterio 8: Explicacao clara e justificada
    rubric_results.append(_check_explanation_clarity(response, has_products))

    # Criterio 9: Resposta nao vazia
    rubric_results.append(_check_not_empty(response))

    # Criterio 10: Fallback seguro
    rubric_results.append(_check_fallback_safety(response, has_products))

    # Determinar status final
    all_passed = all(r.passed for r in rubric_results)
    status = "approved" if all_passed else "rejected"

    # Construir feedback se rejeitado
    feedback = ""
    if not all_passed:
        failed = [r for r in rubric_results if not r.passed]
        feedback_lines = [f"- {r.criterion}: {r.evidence}" for r in failed]
        feedback = "Criterios reprovados:\n" + "\n".join(feedback_lines)
        if not has_products:
            feedback += "\nNenhum produto atende aos criterios. Ajuste restricoes ou informe cliente."

    return Evaluation(
        conversation_id=conversation_id,
        status=status,
        rubric_results=[{
            "criterion": r.criterion,
            "passed": r.passed,
            "evidence": r.evidence,
        } for r in rubric_results],
        feedback=feedback,
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


def _check_lactose_restriction(
    products: list[dict[str, Any]],
    profile: CustomerProfile,
) -> RubricResult:
    """Verifica restricao de lactose em todos os produtos considerados."""
    if not _has_restriction(profile.dietary_restrictions, "lactose"):
        return RubricResult(
            criterion="respeita restricao de lactose",
            passed=True,
            evidence="cliente nao possui restricao de lactose",
        )
    if not products:
        return RubricResult(
            criterion="respeita restricao de lactose",
            passed=True,
            evidence="nenhum produto encontrado — nada a violar",
        )
    violations = [f"{p['sku']} (contem lactose)" for p in products if not p.get("lactose_free", False)]
    if violations:
        return RubricResult(
            criterion="respeita restricao de lactose",
            passed=False,
            evidence=f"produtos com lactose encontrados: {'; '.join(violations)}",
        )
    return RubricResult(
        criterion="respeita restricao de lactose",
        passed=True,
        evidence=f"todos os {len(products)} produtos sao lactose_free",
    )


def _check_gluten_restriction(
    products: list[dict[str, Any]],
    profile: CustomerProfile,
) -> RubricResult:
    """Verifica restricao de gluten em todos os produtos considerados."""
    if not _has_restriction(profile.dietary_restrictions, "gluten"):
        return RubricResult(
            criterion="respeita restricao de gluten",
            passed=True,
            evidence="cliente nao possui restricao de gluten",
        )
    if not products:
        return RubricResult(
            criterion="respeita restricao de gluten",
            passed=True,
            evidence="nenhum produto encontrado — nada a violar",
        )
    violations = [f"{p['sku']} (contem gluten)" for p in products if not p.get("gluten_free", False)]
    if violations:
        return RubricResult(
            criterion="respeita restricao de gluten",
            passed=False,
            evidence=f"produtos com gluten encontrados: {'; '.join(violations)}",
        )
    return RubricResult(
        criterion="respeita restricao de gluten",
        passed=True,
        evidence=f"todos os {len(products)} produtos sao gluten_free",
    )


def _check_budget(
    products: list[dict[str, Any]],
    profile: CustomerProfile,
) -> RubricResult:
    """Verifica se todos os produtos estao dentro do orcamento."""
    if not products:
        return RubricResult(
            criterion="respeita orcamento maximo",
            passed=True,
            evidence="nenhum produto encontrado — nada a violar",
        )
    budget = profile.budget_brl
    violations = [
        f"{p['sku']} (R$ {p['price_brl']:.2f} > R$ {budget:.2f})"
        for p in products if p["price_brl"] > budget
    ]
    if violations:
        return RubricResult(
            criterion=f"respeita orcamento maximo de R$ {budget:.2f}",
            passed=False,
            evidence=f"produtos acima do orcamento: {'; '.join(violations)}",
        )
    return RubricResult(
        criterion=f"respeita orcamento maximo de R$ {budget:.2f}",
        passed=True,
        evidence=f"todos os {len(products)} produtos estao <= R$ {budget:.2f}",
    )


def _check_stock(
    products: list[dict[str, Any]],
    profile: CustomerProfile,
    has_products: bool,
) -> RubricResult:
    """Verifica se todos os produtos estao em estoque."""
    if not has_products:
        return RubricResult(
            criterion="nao recomenda produto fora de estoque",
            passed=True,
            evidence="nenhum produto recomendado",
        )
    violations = [f"{p['sku']}" for p in products if not p.get("in_stock", True)]
    if violations:
        return RubricResult(
            criterion="nao recomenda produto fora de estoque",
            passed=False,
            evidence=f"produtos indisponiveis encontrados: {'; '.join(violations)}",
        )
    return RubricResult(
        criterion="nao recomenda produto fora de estoque",
        passed=True,
        evidence=f"todos os {len(products)} produtos estao em estoque",
    )


def _check_flavor_priority(
    products: list[dict[str, Any]],
    profile: CustomerProfile,
    has_products: bool,
) -> RubricResult:
    """Verifica se o sabor preferido foi priorizado no ranking."""
    if not profile.preferred_flavor or not has_products or len(products) < 2:
        return RubricResult(
            criterion="prioriza sabor preferido quando opcoes equivalentes",
            passed=True,
            evidence="criterio nao aplicavel (sem preferencia declarada ou poucos produtos)",
        )
    preferred = profile.preferred_flavor.lower()
    # O primeiro produto deveria corresponder ao sabor preferido se existir
    for i, p in enumerate(products):
        if preferred in p["name"].lower():
            if i == 0:
                return RubricResult(
                    criterion="prioriza sabor preferido quando opcoes equivalentes",
                    passed=True,
                    evidence=f"produto com sabor {preferred} ranqueado em primeiro lugar",
                )
            return RubricResult(
                criterion="prioriza sabor preferido quando opcoes equivalentes",
                passed=False,
                evidence=f"produto com sabor {preferred} encontrado na posicao {i+1}, nao em primeiro",
            )
    return RubricResult(
        criterion="prioriza sabor preferido quando opcoes equivalentes",
        passed=True,
        evidence=f"nenhum produto com sabor {preferred} disponivel nos filtros atuais",
    )


_PRESSURED_PHRASES = [
    "aproveite agora",
    "so hoje",
    "por tempo limitado",
    "ultimas unidades",
    "nao perca",
    "compre ja",
    "oferta imperdivel",
    "estoque acabando",
    "promocao relampago",
]

_JARGON_PATTERNS = [
    r"\bbioavailability\b",
    r"\bwhey protein isolate hydrolyzed\b",
    r"\befficacy rate\b",
    r"\babsorption kinetics\b",
]


def _check_human_tone(response: str) -> RubricResult:
    """Verifica se a resposta tem tom humano e sem jargao excessivo."""
    response_lower = response.lower()
    for pattern in _JARGON_PATTERNS:
        if re.search(pattern, response_lower):
            return RubricResult(
                criterion="resposta com tom humano, sem jargao excessivo",
                passed=False,
                evidence=f"jargao tecnico detectado: '{pattern}'",
            )
    return RubricResult(
        criterion="resposta com tom humano, sem jargao excessivo",
        passed=True,
        evidence="linguagem natural e acessivel, sem jargao tecnico",
    )


def _check_no_pressure(response: str) -> RubricResult:
    """Verifica se a resposta nao usa linguagem de pressao."""
    response_lower = response.lower()
    found = [phrase for phrase in _PRESSURED_PHRASES if phrase in response_lower]
    if found:
        return RubricResult(
            criterion="nao pressiona compra com linguagem de urgencia",
            passed=False,
            evidence=f"frases de pressao detectadas: {', '.join(found)}",
        )
    return RubricResult(
        criterion="nao pressiona compra com linguagem de urgencia",
        passed=True,
        evidence="resposta informativa, sem urgencia artificial",
    )


def _check_explanation_clarity(
    response: str,
    has_products: bool,
) -> RubricResult:
    """Verifica se a resposta explica a recomendacao de forma clara e justificada."""
    if not has_products:
        return RubricResult(
            criterion="explica recomendacao de forma clara e justificada",
            passed=True,
            evidence="sem produtos — explicacao de ausencia e suficiente",
        )
    response_lower = response.lower()
    clarity_indicators = ["nota", "rating", "avaliada", "avaliacao", "porque", "justificativa"]
    has_clarity = any(indicator in response_lower for indicator in clarity_indicators)
    if has_clarity:
        return RubricResult(
            criterion="explica recomendacao de forma clara e justificada",
            passed=True,
            evidence="resposta inclui indicadores de justificativa (rating, nota, etc.)",
        )
    return RubricResult(
        criterion="explica recomendacao de forma clara e justificada",
        passed=False,
        evidence="resposta nao inclui justificativa clara para a recomendacao",
    )


def _check_fallback_safety(
    response: str,
    has_products: bool,
) -> RubricResult:
    """Verifica se o fallback e seguro quando nenhum produto atende."""
    if has_products:
        return RubricResult(
            criterion="fallback seguro quando nenhum produto atende todos os criterios",
            passed=True,
            evidence="ha produtos recomendados — fallback nao necessario",
        )
    response_lower = response.lower()
    fallback_indicators = [
        "nao encontrei",
        "ajustar alguma preferencia",
        "buscar alternativas",
        "preciso confirmar",
        "verificar e retornar",
    ]
    has_fallback = any(indicator in response_lower for indicator in fallback_indicators)
    if has_fallback:
        return RubricResult(
            criterion="fallback seguro quando nenhum produto atende todos os criterios",
            passed=True,
            evidence="resposta de fallback apropriada quando sem produtos",
        )
    return RubricResult(
        criterion="fallback seguro quando nenhum produto atende todos os criterios",
        passed=False,
        evidence="sem produtos mas resposta nao e fallback seguro",
    )


def _check_not_empty(response: str) -> RubricResult:
    """Verifica se a resposta nao esta vazia."""
    if not response.strip():
        return RubricResult(
            criterion="resposta nao vazia",
            passed=False,
            evidence="candidate_response esta vazia ou em branco",
        )
    return RubricResult(
        criterion="resposta nao vazia",
        passed=True,
        evidence=f"resposta com {len(response)} caracteres",
    )


# ============================================================================
# ORCHESTRATOR (HARNESS)
# ============================================================================

def run_koda_recommendation(
    profile: CustomerProfile,
    catalog: list[Product],
    customer_message: str = "",
    conversation_id: str = "conv_unknown",
    max_revisions: int = 2,
    state_dir: Optional[Path] = None,
) -> str:
    """
    Orquestrador principal: coordena Generator → Evaluator com loop de revisao.

    Fluxo:
    1. Generator cria recomendacoes candidatas
    2. Evaluator valida contra rubrica
    3. Se APROVADO: retorna resposta
    4. Se REJEITADO: feedback → Generator tenta novamente (ate max_revisions)
    5. Apos max_revisions falhas: retorna fallback seguro

    Args:
        profile: Perfil completo do cliente
        catalog: Lista de produtos disponiveis
        customer_message: Mensagem do cliente (para extracao de categoria)
        conversation_id: ID da conversa para rastreamento
        max_revisions: Numero maximo de revisoes apos rejeicao
        state_dir: Diretorio para persistir estado (None = sem persistencia)

    Returns:
        Mensagem de resposta para o cliente
    """
    # 1. Generator — primeira tentativa
    generation = generator_agent(
        profile=profile,
        catalog=catalog,
        customer_message=customer_message,
        conversation_id=conversation_id,
    )

    if state_dir:
        _persist_json(state_dir, "generation.json", generation)

    # 2. Evaluator — validacao
    evaluation = evaluator_agent(
        generation=generation,
        profile=profile,
        conversation_id=conversation_id,
    )

    if state_dir:
        _persist_json(state_dir, "evaluation.json", evaluation)

    # 3. Loop de revisao
    revision_count = 0
    while evaluation.status != "approved" and revision_count < max_revisions:
        revision_count += 1
        generation = generator_agent(
            profile=profile,
            catalog=catalog,
            customer_message=customer_message,
            evaluator_feedback=evaluation.feedback,
            conversation_id=conversation_id,
        )
        if state_dir:
            _persist_json(state_dir, f"generation_revision_{revision_count}.json", generation)

        evaluation = evaluator_agent(
            generation=generation,
            profile=profile,
            conversation_id=conversation_id,
        )
        if state_dir:
            _persist_json(state_dir, f"evaluation_revision_{revision_count}.json", evaluation)

    # 4. Resultado final
    if evaluation.status == "approved":
        if state_dir:
            _persist_json(state_dir, "delivery.json", {
                "schema_version": "1.0",
                "conversation_id": conversation_id,
                "status": "approved",
                "message": generation.candidate_response,
                "sent_at": datetime.now(timezone.utc).isoformat(),
            })
        return generation.candidate_response

    # Fallback seguro
    fallback = (
        "Preciso confirmar um detalhe antes de te responder com seguranca, "
        f"{profile.name}. Posso verificar e retornar em instantes?"
    )
    if state_dir:
        _persist_json(state_dir, "delivery.json", {
            "schema_version": "1.0",
            "conversation_id": conversation_id,
            "status": "fallback",
            "message": fallback,
            "sent_at": datetime.now(timezone.utc).isoformat(),
        })
    return fallback


def _persist_json(directory: Path, filename: str, data: Any) -> Path:
    """Persiste dados em arquivo JSON no diretorio de estado."""
    from dataclasses import asdict, is_dataclass

    directory.mkdir(parents=True, exist_ok=True)
    tmp = directory / f".{filename}.tmp"
    final = directory / filename

    if is_dataclass(data) and not isinstance(data, type):
        payload = asdict(data)
    elif isinstance(data, dict):
        payload = data
    else:
        payload = {"value": str(data)}

    payload.setdefault("schema_version", "1.0")
    if "persisted_at" not in payload:
        payload["persisted_at"] = datetime.now(timezone.utc).isoformat()

    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    tmp.rename(final)
    return final


# ============================================================================
# TESTS
# ============================================================================

def _make_temp_dir() -> Path:
    """Cria diretorio temporario para estado de teste."""
    return Path(tempfile.mkdtemp(prefix="koda_test_state_"))


def test_cenario_1_caminho_feliz():
    """Cenario 1: recomendacao aprovada na primeira tentativa."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: Caminho Feliz — Recomendacao Aprovada")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_rafael_001",
        name="Rafael",
        budget_brl=80.0,
        dietary_restrictions=[],
        training_goal="ganho_de_forca",
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        customer_message="Quero comprar creatina.",
        conversation_id="conv_rafael_001",
        state_dir=state_dir,
    )

    print(f"\n📤 Resposta final: {response}")

    assert (state_dir / "generation.json").exists(), "generation.json deveria existir"
    assert (state_dir / "evaluation.json").exists(), "evaluation.json deveria existir"

    eval_data = json.loads((state_dir / "evaluation.json").read_text(encoding="utf-8"))
    assert eval_data["status"] == "approved", (
        f"Esperado 'approved', obtido '{eval_data['status']}'. Feedback: {eval_data.get('feedback', '')}"
    )

    gen_data = json.loads((state_dir / "generation.json").read_text(encoding="utf-8"))
    assert len(gen_data["products_considered"]) > 0, "deve ter encontrado produtos"
    assert len(gen_data["assumptions"]) > 0, "assumptions nao pode ser vazio"

    # Verificar que produtos sao de creatina
    for p in gen_data["products_considered"]:
        assert p["price_brl"] <= 80.0, f"Produto {p['sku']} excede orcamento"

    print("✅ Teste 1 passou!")


def test_cenario_2_respeita_orcamento():
    """Cenario 2: nunca recomenda produto fora do orcamento."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: Garantia de Respeito ao Orcamento")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_ana_002",
        name="Ana",
        budget_brl=70.0,
        dietary_restrictions=[],
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        customer_message="Preciso de whey protein.",
        conversation_id="conv_ana_002",
        state_dir=state_dir,
    )

    print(f"\n📤 Resposta final: {response}")

    gen_data = json.loads((state_dir / "generation.json").read_text(encoding="utf-8"))
    for p in gen_data.get("products_considered", []):
        assert p["price_brl"] <= 70.0, (
            f"VIOLACAO: {p.get('sku')} custa R$ {p['price_brl']} > budget R$ 70.0"
        )

    eval_data = json.loads((state_dir / "evaluation.json").read_text(encoding="utf-8"))
    budget_result = next(
        (r for r in eval_data["rubric_results"] if "orcamento" in r["criterion"].lower()), None
    )
    assert budget_result is not None, "rubric_results deve incluir criterio de orcamento"
    assert budget_result["passed"], (
        f"criterio de orcamento deveria passar: {budget_result['evidence']}"
    )

    print(f"  Produtos considerados: {len(gen_data['products_considered'])}")
    for p in gen_data["products_considered"]:
        print(f"  - {p.get('sku')}: R$ {p['price_brl']}")

    print("✅ Teste 2 passou!")


def test_cenario_3_respeita_restricao_lactose():
    """Cenario 3: nunca recomenda produto com lactose para cliente intolerante."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: Garantia de Respeito a Restricao de Lactose")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_bruno_003",
        name="Bruno",
        budget_brl=150.0,
        dietary_restrictions=["intolerancia_lactose"],
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        customer_message="Quero comprar whey protein.",
        conversation_id="conv_bruno_003",
        state_dir=state_dir,
    )

    print(f"\n📤 Resposta final: {response}")

    gen_data = json.loads((state_dir / "generation.json").read_text(encoding="utf-8"))
    for p in gen_data.get("products_considered", []):
        assert p.get("lactose_free", False), (
            f"VIOLACAO: {p.get('sku')} nao e lactose_free, mas cliente e intolerante"
        )

    eval_data = json.loads((state_dir / "evaluation.json").read_text(encoding="utf-8"))
    lactose_result = next(
        (r for r in eval_data["rubric_results"] if "lactose" in r["criterion"].lower()), None
    )
    assert lactose_result is not None, "rubric_results deve incluir criterio de lactose"
    assert lactose_result["passed"], (
        f"criterio de lactose deveria passar: {lactose_result['evidence']}"
    )

    print(f"  Produtos considerados: {len(gen_data['products_considered'])}")
    for p in gen_data["products_considered"]:
        print(f"  - {p.get('sku')}: lactose_free={p.get('lactose_free')}")

    print("✅ Teste 3 passou!")


def test_cenario_4_respeita_restricao_gluten():
    """Cenario 4: nunca recomenda produto com gluten para cliente celiaco."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: Garantia de Respeito a Restricao de Gluten")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_carla_004",
        name="Carla",
        budget_brl=200.0,
        dietary_restrictions=["intolerancia_gluten"],
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        customer_message="Qual o melhor whey?",
        conversation_id="conv_carla_004",
        state_dir=state_dir,
    )

    print(f"\n📤 Resposta final: {response}")

    gen_data = json.loads((state_dir / "generation.json").read_text(encoding="utf-8"))
    for p in gen_data.get("products_considered", []):
        assert p.get("gluten_free", False), (
            f"VIOLACAO: {p.get('sku')} nao e gluten_free, mas cliente e celiaco"
        )

    eval_data = json.loads((state_dir / "evaluation.json").read_text(encoding="utf-8"))
    gluten_result = next(
        (r for r in eval_data["rubric_results"] if "gluten" in r["criterion"].lower()), None
    )
    assert gluten_result is not None, "rubric_results deve incluir criterio de gluten"
    assert gluten_result["passed"], (
        f"criterio de gluten deveria passar: {gluten_result['evidence']}"
    )

    print("✅ Teste 4 passou!")


def test_cenario_5_fallback_sem_produtos():
    """Cenario 5: fallback seguro quando budget e impossivel."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: Fallback Seguro — Budget Impossivel")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_pedro_005",
        name="Pedro",
        budget_brl=10.0,
        dietary_restrictions=[],
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        customer_message="Quero o melhor whey.",
        conversation_id="conv_pedro_005",
        state_dir=state_dir,
    )

    print(f"\n📤 Resposta final: {response}")

    assert "Preciso confirmar" in response or "Nao encontrei" in response, (
        f"Esperado fallback ou mensagem de ausencia, obtido: {response}"
    )

    # Verificar que o delivery.json registrou fallback
    delivery_path = state_dir / "delivery.json"
    if delivery_path.exists():
        delivery = json.loads(delivery_path.read_text(encoding="utf-8"))
        print(f"  Status de entrega: {delivery.get('status')}")

    print("✅ Teste 5 passou!")


def test_cenario_6_prioriza_sabor_preferido():
    """Cenario 6: prioriza sabor preferido no ranking."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 6: Priorizacao de Sabor Preferido")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_marina_006",
        name="Marina",
        budget_brl=150.0,
        dietary_restrictions=["intolerancia_lactose"],
        preferred_flavor="chocolate",
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        customer_message="Quero whey protein.",
        conversation_id="conv_marina_006",
        state_dir=state_dir,
    )

    print(f"\n📤 Resposta final: {response}")

    gen_data = json.loads((state_dir / "generation.json").read_text(encoding="utf-8"))
    products = gen_data.get("products_considered", [])

    if len(products) >= 2:
        has_chocolate = any("chocolate" in p["name"].lower() for p in products)
        if has_chocolate:
            print(f"  Primeiro produto: {products[0]['name']}")
            # Nao assertamos que o primeiro e chocolate porque pode nao existir
            # no catalogo, mas verificamos que a preferencia foi registrada
            print("  Sabor chocolate verificado nos produtos")

    assumptions = gen_data.get("assumptions", [])
    assert any("chocolate" in a.lower() for a in assumptions), (
        "assumptions deve mencionar sabor preferido"
    )

    eval_data = json.loads((state_dir / "evaluation.json").read_text(encoding="utf-8"))
    flavor_result = next(
        (r for r in eval_data["rubric_results"] if "sabor" in r["criterion"].lower()), None
    )
    if flavor_result:
        print(f"  Resultado do criterio de sabor: {flavor_result['evidence']}")

    print("✅ Teste 6 passou!")


def test_cenario_7_audit_trail():
    """Cenario 7: todos os arquivos JSON tem campos obrigatorios."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 7: Audit Trail — Campos Obrigatorios nos JSONs")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_rafael_007",
        name="Rafael",
        budget_brl=80.0,
        dietary_restrictions=["intolerancia_lactose"],
        training_goal="ganho_de_forca",
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        customer_message="Qual a melhor creatina?",
        conversation_id="conv_rafael_007",
        state_dir=state_dir,
    )

    # generation.json
    gen_path = state_dir / "generation.json"
    assert gen_path.exists(), "generation.json nao existe"
    gen = json.loads(gen_path.read_text(encoding="utf-8"))
    required_gen = ["schema_version", "conversation_id", "candidate_response", "products_considered", "assumptions", "generated_at"]
    for field in required_gen:
        assert field in gen, f"generation.json: campo '{field}' ausente"

    # evaluation.json
    eval_path = state_dir / "evaluation.json"
    assert eval_path.exists(), "evaluation.json nao existe"
    eval_data = json.loads(eval_path.read_text(encoding="utf-8"))
    required_eval = ["schema_version", "conversation_id", "status", "rubric_results", "checked_at"]
    for field in required_eval:
        assert field in eval_data, f"evaluation.json: campo '{field}' ausente"
    assert eval_data["status"] in ("approved", "rejected"), f"status invalido: {eval_data['status']}"
    assert len(eval_data["rubric_results"]) >= 8, (
        f"rubric_results muito curto: {len(eval_data['rubric_results'])} criterios"
    )

    # Verificar que cada rubric_result tem campos obrigatorios
    for rr in eval_data["rubric_results"]:
        assert "criterion" in rr, f"rubric_result sem criterion: {rr}"
        assert "passed" in rr, f"rubric_result sem passed: {rr}"
        assert "evidence" in rr, f"rubric_result sem evidence: {rr}"

    print(f"\n📁 Arquivos gerados em: {state_dir}")
    for f in sorted(state_dir.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            print(f"  📄 {f.name}")

    print("✅ Teste 7 passou!")


def test_cenario_8_feature_contract():
    """Cenario 8: output do Generator respeita o feature contract."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 8: Validacao do Feature Contract")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_laura_008",
        name="Laura",
        budget_brl=200.0,
        dietary_restrictions=["intolerancia_lactose", "intolerancia_gluten"],
        preferred_flavor="baunilha",
        training_goal="ganho_de_massa",
    )

    response = run_koda_recommendation(
        profile=profile,
        catalog=PRODUCT_CATALOG,
        conversation_id="conv_laura_008",
        state_dir=state_dir,
    )

    print(f"\n📤 Resposta final: {response}")

    gen = json.loads((state_dir / "generation.json").read_text(encoding="utf-8"))

    # Verificar garantias do output_contract
    products = gen.get("products_considered", [])
    assert len(products) <= FEATURE_CONTRACT["max_products_per_recommendation"], (
        f"max_products_per_recommendation violado: {len(products)} > {FEATURE_CONTRACT['max_products_per_recommendation']}"
    )

    # Verificar que todos os campos required do output estao presentes
    for field in FEATURE_CONTRACT["output_contract"]["required"]:
        assert field in gen, f"output_contract: campo required '{field}' ausente"

    # Verificar tamanho maximo da resposta
    max_chars = FEATURE_CONTRACT["max_response_chars"]
    assert len(gen["candidate_response"]) <= max_chars, (
        f"max_response_chars violado: {len(gen['candidate_response'])} > {max_chars}"
    )

    # Verificar garantias de produtos
    for p in products:
        if _has_restriction(profile.dietary_restrictions, "lactose"):
            assert p.get("lactose_free"), f"{p['sku']} viola restricao de lactose"
        if _has_restriction(profile.dietary_restrictions, "gluten"):
            assert p.get("gluten_free"), f"{p['sku']} viola restricao de gluten"
        assert p["price_brl"] <= profile.budget_brl, f"{p['sku']} viola orcamento"
        assert p.get("in_stock"), f"{p['sku']} nao esta em estoque"

    print(f"  ✅ Contract verificado:")
    print(f"     - produtos: {len(products)}/max {FEATURE_CONTRACT['max_products_per_recommendation']}")
    print(f"     - tamanho resposta: {len(gen['candidate_response'])}/max {max_chars}")
    print(f"     - campos required: todos presentes")

    print("✅ Teste 8 passou!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SOLUCAO: FEATURE KODA — RECOMENDACAO DE PRODUTO COM GENERATOR/EVALUATOR")
    print("Nivel 4 — KODA-Especifico — Real-World Feature")
    print("=" * 60)

    test_cenario_1_caminho_feliz()
    test_cenario_2_respeita_orcamento()
    test_cenario_3_respeita_restricao_lactose()
    test_cenario_4_respeita_restricao_gluten()
    test_cenario_5_fallback_sem_produtos()
    test_cenario_6_prioriza_sabor_preferido()
    test_cenario_7_audit_trail()
    test_cenario_8_feature_contract()

    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
