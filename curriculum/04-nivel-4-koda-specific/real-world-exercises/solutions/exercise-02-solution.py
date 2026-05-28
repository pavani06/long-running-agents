"""
Solucao do Exercicio 2 — Pipeline Completo de Customer Journey com Agentes Coordenados
Nivel 4 — KODA-Especifico

Esta e a solucao de referencia. Execute com:
    python exercise-02-solution.py

Todos os 8 cenarios de teste devem passar com OK.
"""

import json
import random
import re
import tempfile
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# ENUMS
# ============================================================================

class JourneyStage(str, Enum):
    ENTRY = "ENTRY"
    AWARENESS = "AWARENESS"
    CONSIDERATION = "CONSIDERATION"
    DECISION = "DECISION"
    RETENTION = "RETENTION"


class Intent(str, Enum):
    PRODUCT_DISCOVERY = "PRODUCT_DISCOVERY"
    ORDER_STATUS = "ORDER_STATUS"
    SUPPORT = "SUPPORT"
    RICOMPRA = "RICOMPRA"
    RECLAMACAO = "RECLAMACAO"
    UNKNOWN = "UNKNOWN"


class EvalStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Product:
    sku: str
    name: str
    category: str
    price_brl: float
    servings: int
    lactose_free: bool
    gluten_free: bool
    vegan: bool
    in_stock: bool
    rating: float
    description: str = ""


@dataclass
class CustomerProfile:
    schema_version: str = "2.0"
    conversation_id: str = ""
    customer_id: str = ""
    name: str = ""
    whatsapp_number: str = ""
    budget_brl: Optional[float] = None
    dietary_restrictions: list[str] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)
    training_goal: Optional[str] = None
    training_frequency: Optional[str] = None
    preferred_flavor: Optional[str] = None
    preferred_format: Optional[str] = None
    purchase_history: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class JourneyState:
    schema_version: str = "2.0"
    conversation_id: str = ""
    customer_id: str = ""
    current_stage: JourneyStage = JourneyStage.ENTRY
    current_sub_state: str = ""
    stage_history: list[dict[str, Any]] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Generation:
    schema_version: str = "2.0"
    conversation_id: str = ""
    candidate_response: str = ""
    products_mentioned: list[str] = field(default_factory=list)
    tone: str = "whatsapp_natural"
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RubricResult:
    criterion: str
    passed: bool
    evidence: str


@dataclass
class Evaluation:
    schema_version: str = "2.0"
    conversation_id: str = ""
    status: str = ""
    rubric_results: list[RubricResult] = field(default_factory=list)
    feedback: str = ""
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Order:
    schema_version: str = "2.0"
    conversation_id: str = ""
    order_id: str = ""
    items: list[dict[str, Any]] = field(default_factory=list)
    total_brl: float = 0.0
    discount_applied: float = 0.0
    shipping_address: dict[str, str] = field(default_factory=dict)
    payment_method: str = ""
    payment_status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Fulfillment:
    schema_version: str = "2.0"
    conversation_id: str = ""
    order_id: str = ""
    tracking_code: str = ""
    carrier: str = ""
    estimated_delivery: str = ""
    status: str = "processing"
    delivered_at: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Retention:
    schema_version: str = "2.0"
    conversation_id: str = ""
    customer_id: str = ""
    follow_up_scheduled_at: str = ""
    follow_up_type: str = ""
    re_engagement_offers: list[dict[str, Any]] = field(default_factory=list)
    last_contact_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ConversationTurn:
    conversation_id: str
    turn_id: str
    customer_message: str
    received_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# PRODUCT CATALOG
# ============================================================================

FUTANBEAR_CATALOG: list[Product] = [
    Product(sku="WHEY-CONC-900", name="Whey Protein Concentrado 900g", category="whey_protein",
            price_brl=99.90, servings=30, lactose_free=False, gluten_free=True, vegan=False,
            in_stock=True, rating=4.5, description="Proteina de alta qualidade para ganho de massa muscular."),
    Product(sku="WHEY-ISO-900", name="Whey Protein Isolado 900g", category="whey_protein",
            price_brl=159.90, servings=30, lactose_free=True, gluten_free=True, vegan=False,
            in_stock=True, rating=4.8, description="Whey isolado com baixissimo teor de lactose."),
    Product(sku="WHEY-VEG-800", name="Proteina Vegetal Blend 800g", category="whey_protein",
            price_brl=129.90, servings=25, lactose_free=True, gluten_free=True, vegan=True,
            in_stock=True, rating=4.3, description="Blend de ervilha, arroz e quinoa."),
    Product(sku="CREA-MONO-300", name="Creatina Monohidratada 300g", category="creatina",
            price_brl=69.90, servings=60, lactose_free=True, gluten_free=True, vegan=True,
            in_stock=True, rating=4.9, description="Creatina pura monohidratada."),
    Product(sku="CREA-MICRO-250", name="Creatina Micronizada 250g", category="creatina",
            price_brl=74.90, servings=50, lactose_free=True, gluten_free=True, vegan=True,
            in_stock=True, rating=4.7, description="Particulas menores para melhor absorcao."),
    Product(sku="PRE-BASIC-300", name="Pre-Treino Basico 300g", category="pre_workout",
            price_brl=89.90, servings=30, lactose_free=True, gluten_free=True, vegan=False,
            in_stock=True, rating=4.4, description="Energia e foco para seu treino."),
    Product(sku="PRE-VEG-270", name="Pre-Treino Vegano 270g", category="pre_workout",
            price_brl=109.90, servings=30, lactose_free=True, gluten_free=True, vegan=True,
            in_stock=True, rating=4.6, description="Energia 100% vegetal."),
    Product(sku="SONO-MEL-120", name="Melatonina 120 Capsulas", category="sono",
            price_brl=49.90, servings=120, lactose_free=True, gluten_free=True, vegan=False,
            in_stock=True, rating=4.5, description="Ajuda a regular o ciclo do sono."),
    Product(sku="SONO-MAG-90", name="Magnesio Quelato 90 Capsulas", category="sono",
            price_brl=59.90, servings=90, lactose_free=True, gluten_free=True, vegan=True,
            in_stock=True, rating=4.7, description="Relaxa o sistema nervoso."),
    Product(sku="SONO-HERB-90", name="Blend Herbal Noturno 90 Capsulas", category="sono",
            price_brl=72.00, servings=90, lactose_free=True, gluten_free=True, vegan=True,
            in_stock=True, rating=4.4, description="Camomila, valeriana e passiflora."),
    Product(sku="REC-BCAA-400", name="BCAA 400g", category="post_workout",
            price_brl=79.90, servings=40, lactose_free=True, gluten_free=True, vegan=False,
            in_stock=True, rating=4.3, description="Aminoacidos de cadeia ramificada."),
    Product(sku="REC-GLUT-300", name="L-Glutamina 300g", category="post_workout",
            price_brl=69.90, servings=60, lactose_free=True, gluten_free=True, vegan=False,
            in_stock=True, rating=4.5, description="Acelera a recuperacao muscular."),
    Product(sku="REC-ZMA-120", name="ZMA 120 Capsulas", category="post_workout",
            price_brl=89.90, servings=120, lactose_free=True, gluten_free=True, vegan=True,
            in_stock=True, rating=4.6, description="Zinco, Magnesio e Vitamina B6."),
    Product(sku="WHEY-HYDRO-800", name="Whey Protein Hidrolisado 800g", category="whey_protein",
            price_brl=199.90, servings=25, lactose_free=True, gluten_free=True, vegan=False,
            in_stock=False, rating=4.9, description="Absorcao ultra-rapida."),
    Product(sku="PRE-ELITE-500", name="Pre-Treino Elite 500g", category="pre_workout",
            price_brl=249.90, servings=50, lactose_free=True, gluten_free=True, vegan=False,
            in_stock=True, rating=4.8, description="Formula premium com 12 ativos."),
]


# ============================================================================
# PERSISTENCE HELPERS
# ============================================================================

def write_json(data: Any, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(data, '__dataclass_fields__'):
        data = asdict(data)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', dir=filepath.parent,
                                      delete=False, encoding='utf-8') as tf:
        json.dump(data, tf, indent=2, ensure_ascii=False, default=str)
    Path(tf.name).replace(filepath)


def read_json(filepath: Path) -> dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def ensure_state_dir(conversation_id: str, base_dir: str = "state") -> Path:
    dir_path = Path(base_dir) / conversation_id
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def update_journey_state(
    state: JourneyState,
    new_stage: JourneyStage,
    trigger: str,
    guard_evaluation: str = "ALL_PASS",
    conversation_id: str = "",
) -> JourneyState:
    old_stage = state.current_stage
    state.stage_history.append({
        "from": old_stage.value,
        "to": new_stage.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trigger": trigger,
        "guard_evaluation": guard_evaluation,
    })
    state.current_stage = new_stage
    state.updated_at = datetime.now(timezone.utc).isoformat()
    if conversation_id:
        state.conversation_id = conversation_id
    return state


# ============================================================================
# AGENTS
# ============================================================================

def _infer_category(message: str) -> str:
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["whey", "proteina", "protein"]):
        return "whey_protein"
    if "creatina" in msg_lower:
        return "creatina"
    if any(w in msg_lower for w in ["pre-treino", "pre treino", "preworkout"]):
        return "pre_workout"
    if any(w in msg_lower for w in ["dormir", "sono", "melatonina"]):
        return "sono"
    if any(w in msg_lower for w in ["recuperacao", "pos-treino", "pos treino", "recuperar"]):
        return "post_workout"
    return ""


def discovery_agent(
    customer_message: str,
    existing_profile: Optional[CustomerProfile] = None,
    conversation_id: str = "",
) -> tuple[Intent, CustomerProfile]:
    profile = existing_profile or CustomerProfile(conversation_id=conversation_id)
    profile.updated_at = datetime.now(timezone.utc).isoformat()

    msg_lower = customer_message.lower()

    # Intent classification
    if any(w in msg_lower for w in ["comprar de novo", "mesmo de antes", "recorrente", "de novo"]):
        intent = Intent.RICOMPRA
    elif any(w in msg_lower for w in ["onde esta meu pedido", "tracking", "entrega", "rastreio"]):
        intent = Intent.ORDER_STATUS
    elif any(w in msg_lower for w in ["problema", "errado", "defeito", "reclamar"]):
        intent = Intent.RECLAMACAO
    elif any(w in msg_lower for w in ["duvida", "como usar", "ajuda", "funciona"]):
        intent = Intent.SUPPORT
    elif any(w in msg_lower for w in ["quero comprar", "preciso de", "recomenda", "quero", "preciso", "procuro", "tem"]):
        intent = Intent.PRODUCT_DISCOVERY
    else:
        intent = Intent.UNKNOWN

    # Extract budget
    budget_match = re.findall(r'R\$\s*(\d+[\.,]?\d*)', customer_message, re.IGNORECASE)
    if budget_match:
        try:
            profile.budget_brl = float(budget_match[0].replace(',', '.'))
        except ValueError:
            pass

    # Extract name
    name_match = re.search(r'(?:me chamo|sou\s+(?:a\s+)?o\s+)?(\b[A-ZÀ-Ú][a-zà-ú]{2,}\b)(?:\s|$|\.|,)', customer_message)
    if name_match and not any(w in name_match.group(1).lower() for w in ["quero", "preciso", "tenho", "oi", "ola"]):
        profile.name = name_match.group(1)

    # Extract dietary restrictions
    if any(w in msg_lower for w in ["intolerante a lactose", "sem lactose", "lactose"]):
        if "lactose_free" not in profile.dietary_restrictions:
            profile.dietary_restrictions.append("lactose_free")
    if any(w in msg_lower for w in ["sem gluten", "celiaco", "gluten"]):
        if "gluten_free" not in profile.dietary_restrictions:
            profile.dietary_restrictions.append("gluten_free")
    if any(w in msg_lower for w in ["vegetariano", "vegano", "vegetal"]):
        if "vegano" not in profile.dietary_restrictions:
            profile.dietary_restrictions.append("vegano")

    # Extract allergies
    for allergy_word in ["amendoim", "soja", "camarao", "frutos do mar"]:
        if allergy_word in msg_lower:
            profile.allergies.append(allergy_word)

    # Extract training info
    freq_match = re.search(r'treino\s+(\d+)\s*(?:x|vezes)', msg_lower)
    if freq_match:
        profile.training_frequency = f"{freq_match.group(1)}x por semana"

    return intent, profile


def catalog_agent(
    intent: Intent,
    profile: CustomerProfile,
    catalog: list[Product],
    customer_message: str = "",
    max_results: int = 5,
) -> list[Product]:
    results = list(catalog)

    # Filter by category from message
    if intent == Intent.PRODUCT_DISCOVERY:
        category = _infer_category(customer_message)
        if category:
            results = [p for p in results if p.category == category]

    # Apply dietary restriction filters
    if "lactose_free" in profile.dietary_restrictions:
        results = [p for p in results if p.lactose_free]
    if "gluten_free" in profile.dietary_restrictions:
        results = [p for p in results if p.gluten_free]
    if "vegano" in profile.dietary_restrictions:
        results = [p for p in results if p.vegan]

    # Budget filter
    if profile.budget_brl is not None:
        results = [p for p in results if p.price_brl <= profile.budget_brl]

    # Stock filter
    results = [p for p in results if p.in_stock]

    # Sort by rating descending
    results.sort(key=lambda p: p.rating, reverse=True)

    return results[:max_results]


def generator_agent(
    profile: CustomerProfile,
    products: list[Product],
    conversation_id: str = "",
    feedback: str = "",
) -> Generation:
    # If feedback provided (retry), re-filter based on feedback
    filtered_products = list(products)
    if feedback:
        fb_lower = feedback.lower()
        if "orcamento" in fb_lower and profile.budget_brl is not None:
            filtered_products = [p for p in filtered_products if p.price_brl <= profile.budget_brl]
        if "lactose" in fb_lower:
            filtered_products = [p for p in filtered_products if p.lactose_free]
        if "gluten" in fb_lower:
            filtered_products = [p for p in filtered_products if p.gluten_free]
        if "vegano" in fb_lower:
            filtered_products = [p for p in filtered_products if p.vegan]

    name = profile.name or "cliente"

    if not filtered_products:
        budget_str = f" de R$ {profile.budget_brl:.0f}" if profile.budget_brl else ""
        return Generation(
            conversation_id=conversation_id,
            candidate_response=f"Oi {name}! Infelizmente nao encontrei opcoes no momento dentro do seu orcamento{budget_str}. Quer dar uma olhada em valores um pouco acima? Ou prefere que eu sugira algo em outra categoria?",
            products_mentioned=[],
        )

    lines = [f"Oi {name}! 🌟 {'Reavaliei e encontrei ' if feedback else 'Encontrei '}{len(filtered_products)} opcoes que se encaixam no que voce procura:\n"]
    emoji_map = {"whey_protein": "🥛", "creatina": "💪", "pre_workout": "⚡", "sono": "🌙", "post_workout": "🔄"}

    for p in filtered_products:
        emoji = emoji_map.get(p.category, "🏷️")
        lines.append(f"{emoji} {p.name}")
        lines.append(f"✅ {p.description}")
        lines.append(f"💰 R$ {p.price_brl:.2f}".replace('.', ','))
        lines.append(f"⭐ {p.rating}/5\n")

    lines.append("Qual desses combina mais com sua rotina? Posso te explicar melhor qualquer um! 😊")
    response = "\n".join(lines)

    return Generation(
        conversation_id=conversation_id,
        candidate_response=response,
        products_mentioned=[p.sku for p in filtered_products],
    )


def evaluator_agent(
    generation: Generation,
    profile: CustomerProfile,
    products: list[Product],
    conversation_id: str = "",
) -> Evaluation:
    results: list[RubricResult] = []
    product_map = {p.sku: p for p in products}
    mentioned = [product_map[sku] for sku in generation.products_mentioned if sku in product_map]

    # Rubric 1: Budget
    if profile.budget_brl is not None and mentioned:
        over_budget = [p for p in mentioned if p.price_brl > profile.budget_brl]
        results.append(RubricResult(
            criterion="RESTRICAO_ORCAMENTO",
            passed=len(over_budget) == 0,
            evidence=f"Produtos acima do orcamento: {[p.sku for p in over_budget]}" if over_budget else "Todos dentro do orcamento."
        ))
    else:
        results.append(RubricResult(criterion="RESTRICAO_ORCAMENTO", passed=True, evidence="Nao aplicavel."))

    # Rubric 2: Lactose
    if "lactose_free" in profile.dietary_restrictions and mentioned:
        with_lactose = [p for p in mentioned if not p.lactose_free]
        results.append(RubricResult(
            criterion="RESTRICAO_LACTOSE",
            passed=len(with_lactose) == 0,
            evidence=f"Produtos com lactose: {[p.sku for p in with_lactose]}" if with_lactose else "Todos lactose_free."
        ))
    else:
        results.append(RubricResult(criterion="RESTRICAO_LACTOSE", passed=True, evidence="Nao aplicavel."))

    # Rubric 3: Gluten
    if "gluten_free" in profile.dietary_restrictions and mentioned:
        with_gluten = [p for p in mentioned if not p.gluten_free]
        results.append(RubricResult(
            criterion="RESTRICAO_GLUTEN",
            passed=len(with_gluten) == 0,
            evidence=f"Produtos com gluten: {[p.sku for p in with_gluten]}" if with_gluten else "Todos gluten_free."
        ))
    else:
        results.append(RubricResult(criterion="RESTRICAO_GLUTEN", passed=True, evidence="Nao aplicavel."))

    # Rubric 4: Vegano
    if "vegano" in profile.dietary_restrictions and mentioned:
        non_vegan = [p for p in mentioned if not p.vegan]
        results.append(RubricResult(
            criterion="RESTRICAO_VEGANO",
            passed=len(non_vegan) == 0,
            evidence=f"Produtos nao veganos: {[p.sku for p in non_vegan]}" if non_vegan else "Todos veganos."
        ))
    else:
        results.append(RubricResult(criterion="RESTRICAO_VEGANO", passed=True, evidence="Nao aplicavel."))

    # Rubric 5: Response not empty
    results.append(RubricResult(
        criterion="RESPOSTA_NAO_VAZIA",
        passed=len(generation.candidate_response) > 10,
        evidence=f"Tamanho da resposta: {len(generation.candidate_response)} caracteres."
    ))

    # Rubric 6: WhatsApp tone
    results.append(RubricResult(
        criterion="TOM_WHATSAPP",
        passed=len(generation.candidate_response) <= 800,
        evidence=f"Tamanho: {len(generation.candidate_response)} (limite: 800)."
    ))

    # Rubric 7: In stock
    if mentioned:
        out_of_stock = [p for p in mentioned if not p.in_stock]
        results.append(RubricResult(
            criterion="PRODUTOS_EM_ESTOQUE",
            passed=len(out_of_stock) == 0,
            evidence=f"Fora de estoque: {[p.sku for p in out_of_stock]}" if out_of_stock else "Todos em estoque."
        ))
    else:
        results.append(RubricResult(criterion="PRODUTOS_EM_ESTOQUE", passed=True, evidence="Nenhum produto mencionado."))

    # Rubric 8: Personalization
    results.append(RubricResult(
        criterion="PERSONALIZACAO",
        passed=profile.name in generation.candidate_response if profile.name else True,
        evidence=f"Nome '{profile.name}' {'encontrado' if profile.name and profile.name in generation.candidate_response else 'ausente'} na resposta."
    ))

    all_pass = all(r.passed for r in results)
    feedback_msgs = [r.criterion for r in results if not r.passed]

    return Evaluation(
        conversation_id=conversation_id,
        status=EvalStatus.APPROVED.value if all_pass else EvalStatus.REJECTED.value,
        rubric_results=results,
        feedback="; ".join(f"{c} falhou" for c in feedback_msgs) if feedback_msgs else "",
    )


def order_agent(
    profile: CustomerProfile,
    selected_product_sku: str,
    shipping_address: dict[str, str],
    payment_method: str,
    catalog: list[Product],
    conversation_id: str = "",
) -> Order:
    product = next((p for p in catalog if p.sku == selected_product_sku), None)

    if product is None:
        return Order(conversation_id=conversation_id, order_id="", payment_status="rejected")
    if not product.in_stock:
        return Order(conversation_id=conversation_id, order_id="", payment_status="rejected")

    zip_code = shipping_address.get("zip", "")
    if len(zip_code) != 8 or not zip_code.isdigit():
        return Order(conversation_id=conversation_id, order_id="", payment_status="rejected")

    total = product.price_brl
    discount = 0.0

    if payment_method == "pix":
        pix_discount = round(total * 0.05, 2)
        if pix_discount > discount:
            discount = pix_discount

    if len(profile.purchase_history) >= 2:
        loyalty_discount = round(total * 0.10, 2)
        if loyalty_discount > discount:
            discount = loyalty_discount

    total -= discount

    order_id = f"KDA-{conversation_id[-6:]}" if conversation_id else f"KDA-{random.randint(100000, 999999)}"

    return Order(
        conversation_id=conversation_id,
        order_id=order_id,
        items=[{"sku": product.sku, "name": product.name, "qty": 1, "unit_price_brl": product.price_brl}],
        total_brl=round(total, 2),
        discount_applied=discount,
        shipping_address=shipping_address,
        payment_method=payment_method,
        payment_status="confirmed",
    )


def fulfillment_agent(order: Order, conversation_id: str = "") -> Fulfillment:
    if order.payment_status != "confirmed":
        return Fulfillment(conversation_id=conversation_id, order_id=order.order_id, status="rejected")

    state = order.shipping_address.get("state", "").upper()
    if "SP" in state:
        carrier = "Loggi"
        days = 1
    elif state in ("RJ", "MG"):
        carrier = "Total Express"
        days = 3
    else:
        carrier = "Correios"
        days = 7

    eta = datetime.now(timezone.utc) + timedelta(days=days)
    tracking = f"KDA-{random.randint(100000, 999999)}"

    return Fulfillment(
        conversation_id=conversation_id,
        order_id=order.order_id,
        tracking_code=tracking,
        carrier=carrier,
        estimated_delivery=eta.strftime("%Y-%m-%d"),
        status="processing",
    )


def retention_agent(profile: CustomerProfile, order: Order, conversation_id: str = "") -> Retention:
    # Determine product servings to calculate follow-up timing
    total_servings = sum(item.get("qty", 1) * FUTANBEAR_CATALOG_DICT.get(item["sku"], Product(sku="", name="", category="", price_brl=0, servings=30, lactose_free=True, gluten_free=True, vegan=True, in_stock=True, rating=0)).servings for item in order.items) if order.items else 30
    follow_up_days = int(total_servings * 0.8)
    follow_up_date = datetime.now(timezone.utc) + timedelta(days=follow_up_days)

    # Re-engagement offers
    offers: list[dict[str, Any]] = []
    if len(profile.purchase_history) == 0:
        offers.append({"type": "discount", "value": "10%", "condition": "segunda_compra"})
    elif len(profile.purchase_history) >= 1:
        offers.append({"type": "discount", "value": "15%", "condition": "cliente_fiel"})
        offers.append({"type": "free_shipping", "value": "frete_gratis", "condition": "cliente_fiel"})
    if order.total_brl > 200:
        offers.append({"type": "combo", "value": "produto_complementar", "condition": "ticket_alto"})

    return Retention(
        conversation_id=conversation_id,
        customer_id=profile.customer_id,
        follow_up_scheduled_at=follow_up_date.isoformat(),
        follow_up_type="ESTOQUE_ACABANDO",
        re_engagement_offers=offers,
    )


# Pre-build catalog dict for retention_agent
FUTANBEAR_CATALOG_DICT = {p.sku: p for p in FUTANBEAR_CATALOG}


# ============================================================================
# GUARD CONDITIONS & TRANSITIONS
# ============================================================================

def evaluate_guard_conditions(state: JourneyState, profile: CustomerProfile) -> list[dict[str, Any]]:
    transitions: list[dict[str, Any]] = []
    stage = state.current_stage

    if stage == JourneyStage.ENTRY:
        transitions.append({"from": "ENTRY", "to": "AWARENESS", "status": "ALL_PASS", "reason": "primeira mensagem"})

    elif stage == JourneyStage.AWARENESS:
        context = state.context
        has_name = bool(profile.name)
        intent_ok = context.get("intent_classified", False)
        context_ok = context.get("minimal_context_collected", False)

        if has_name and intent_ok and context_ok:
            transitions.append({"from": "AWARENESS", "to": "CONSIDERATION", "status": "ALL_PASS"})
        else:
            transitions.append({"from": "AWARENESS", "to": "AWARENESS", "status": "ALL_PASS", "reason": "coletando_contexto"})

    elif stage == JourneyStage.CONSIDERATION:
        context = state.context
        if context.get("product_selected") and context.get("product_validated"):
            transitions.append({"from": "CONSIDERATION", "to": "DECISION", "status": "ALL_PASS"})
        elif context.get("customer_cancelled"):
            transitions.append({"from": "CONSIDERATION", "to": "CONSIDERATION", "status": "ALL_PASS", "reason": "cancelado"})
        else:
            transitions.append({"from": "CONSIDERATION", "to": "CONSIDERATION", "status": "ALL_PASS", "reason": "explorando"})

    elif stage == JourneyStage.DECISION:
        context = state.context
        if context.get("payment_confirmed") and context.get("order_created"):
            transitions.append({"from": "DECISION", "to": "RETENTION", "status": "ALL_PASS"})
        elif context.get("customer_cancelled"):
            transitions.append({"from": "DECISION", "to": "CONSIDERATION", "status": "ALL_PASS"})
        else:
            transitions.append({"from": "DECISION", "to": "DECISION", "status": "ALL_PASS", "reason": "processando"})

    elif stage == JourneyStage.RETENTION:
        if state.context.get("customer_wants_rebuy"):
            transitions.append({"from": "RETENTION", "to": "CONSIDERATION", "status": "ALL_PASS"})
        else:
            transitions.append({"from": "RETENTION", "to": "RETENTION", "status": "ALL_PASS", "reason": "aguardando"})

    return transitions


def select_transition(possible_transitions: list[dict[str, Any]], customer_message: str = "") -> dict[str, Any]:
    msg_lower = customer_message.lower()
    # Priority 1: Human handoff
    if any(w in msg_lower for w in ["falar com atendente", "pessoa real", "humano"]):
        for t in possible_transitions:
            if t.get("to") == "RETENTION":
                return t

    # Priority 2: Advance transitions (forward progress)
    for t in possible_transitions:
        if t["to"] not in (t.get("from", ""), "ENTRY"):
            return t

    # Priority 3: Loop (stay)
    return possible_transitions[0] if possible_transitions else {"from": "UNKNOWN", "to": "UNKNOWN", "status": "FAIL"}


# ============================================================================
# ORCHESTRATOR
# ============================================================================

FALLBACK_RESPONSE = "Preciso confirmar um detalhe antes de continuar. So um momento! 😊"
MAX_RETRIES = 2


def run_customer_journey_turn(
    customer_message: str,
    conversation_id: str,
    catalog: list[Product],
    base_state_dir: str = "state",
) -> dict[str, Any]:
    state_dir = ensure_state_dir(conversation_id, base_state_dir)

    # Load or create state
    state_path = state_dir / "state.json"
    profile_path = state_dir / "profile.json"

    if state_path.exists():
        state_data = read_json(state_path)
        state = JourneyState(**{k: v for k, v in state_data.items() if k in JourneyState.__dataclass_fields__})
        state.current_stage = JourneyStage(state_data["current_stage"])
    else:
        state = JourneyState(conversation_id=conversation_id)

    if profile_path.exists():
        profile_data = read_json(profile_path)
        profile = CustomerProfile(**{k: v for k, v in profile_data.items() if k in CustomerProfile.__dataclass_fields__})
    else:
        profile = CustomerProfile(conversation_id=conversation_id)

    # Run Discovery
    intent, profile = discovery_agent(customer_message, profile, conversation_id)
    state.context["intent_classified"] = True
    if profile.name:
        state.context["minimal_context_collected"] = True

    write_json(profile, profile_path)

    # Evaluate guards
    transitions = evaluate_guard_conditions(state, profile)
    selected = select_transition(transitions, customer_message)
    new_stage = JourneyStage(selected["to"])

    if new_stage != state.current_stage:
        state = update_journey_state(state, new_stage, selected.get("reason", "transition"))

    evaluation: Optional[Evaluation] = None
    order: Optional[Order] = None
    response = ""

    if state.current_stage == JourneyStage.AWARENESS:
        if not profile.name:
            response = "Oi! Antes de te mostrar os produtos, me conta: qual seu nome? E voce tem alguma restricao alimentar? (intolerancia a lactose, vegetariano, etc.) 😊"
        else:
            response = f"Obrigado, {profile.name}! So mais uma coisa: voce tem alguma restricao alimentar ou alergia que eu deva saber?"

    elif state.current_stage == JourneyStage.CONSIDERATION:
        products = catalog_agent(intent, profile, catalog, customer_message)

        for retry_count in range(MAX_RETRIES + 1):
            gen = generator_agent(profile, products, conversation_id,
                                  feedback=evaluation.feedback if evaluation else "")
            write_json(gen, state_dir / "generation.json")

            ev = evaluator_agent(gen, profile, products, conversation_id)
            write_json(ev, state_dir / "evaluation.json")
            evaluation = ev

            if ev.status == EvalStatus.APPROVED.value:
                response = gen.candidate_response
                break
        else:
            response = FALLBACK_RESPONSE

    elif state.current_stage == JourneyStage.DECISION:
        # Simulate order from context
        selected_sku = state.context.get("selected_sku", "")
        address = state.context.get("shipping_address", {"zip": "00000000"})
        payment = state.context.get("payment_method", "pix")

        order = order_agent(profile, selected_sku, address, payment, catalog, conversation_id)
        if order.payment_status == "confirmed":
            state.context["order_created"] = True
            state.context["payment_confirmed"] = True
            write_json(order, state_dir / "order.json")

            fulf = fulfillment_agent(order, conversation_id)
            write_json(fulf, state_dir / "fulfillment.json")

            ret = retention_agent(profile, order, conversation_id)
            write_json(ret, state_dir / "retention.json")

            response = f"Pedido confirmado, {profile.name}! 🎉\n📦 Pedido: {order.order_id}\n💰 Total: R$ {order.total_brl:.2f}\n🚚 Entrega: {fulf.estimated_delivery}\n\nTe aviso quando sair pra entrega! 😊"
            state = update_journey_state(state, JourneyStage.RETENTION, "pedido_confirmado")
        else:
            response = "Hmm, encontrei um problema com seu pedido. Pode verificar o CEP? Preciso de 8 digitos (ex: 01310100)."

    elif state.current_stage == JourneyStage.RETENTION:
        response = f"Ola {profile.name}! Como esta sendo a experiencia com o produto? 🌟"

    if not response:
        response = FALLBACK_RESPONSE

    write_json(state, state_path)

    return {
        "response": response,
        "state": state,
        "evaluation": evaluation,
        "order": order,
        "stage": state.current_stage,
    }


# ============================================================================
# TEST SCENARIOS
# ============================================================================

def _make_conv_id(label: str) -> str:
    return f"test_{label}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"


def test_scenario_1_happy_path() -> bool:
    conv = _make_conv_id("happy")
    r1 = run_customer_journey_turn("Oi, quero comprar whey protein. Meu orcamento e R$ 180.", conv, FUTANBEAR_CATALOG)
    assert r1["stage"] == JourneyStage.AWARENESS

    # Provide name
    r2 = run_customer_journey_turn("Me chamo Carlos.", conv, FUTANBEAR_CATALOG)
    assert r2["stage"] == JourneyStage.CONSIDERATION
    assert r2["evaluation"].status == "approved"

    # Verify budget respected
    profile_data = read_json(Path("state") / conv / "profile.json")
    assert profile_data["budget_brl"] == 180.0

    return True


def test_scenario_2_lactose_restriction() -> bool:
    conv = _make_conv_id("lactose")
    r1 = run_customer_journey_turn("Preciso de whey, mas sou intolerante a lactose. Ate R$ 200.", conv, FUTANBEAR_CATALOG)
    r2 = run_customer_journey_turn("Ana.", conv, FUTANBEAR_CATALOG)

    profile_data = read_json(Path("state") / conv / "profile.json")
    assert "lactose_free" in profile_data["dietary_restrictions"]

    assert r2["evaluation"].status == "approved"
    for rr in r2["evaluation"].rubric_results:
        if rr.criterion == "RESTRICAO_LACTOSE":
            assert rr.passed

    return True


def test_scenario_3_budget_violation() -> bool:
    conv = _make_conv_id("budget")
    r1 = run_customer_journey_turn("Quero o melhor pre-treino. Orcamento R$ 50.", conv, FUTANBEAR_CATALOG)
    r2 = run_customer_journey_turn("Pedro.", conv, FUTANBEAR_CATALOG)
    assert r2["evaluation"].status == "approved"
    return True


def test_scenario_4_vegan_customer() -> bool:
    conv = _make_conv_id("vegan")
    r1 = run_customer_journey_turn("Sou vegano. Tem proteina pra mim?", conv, FUTANBEAR_CATALOG)
    r2 = run_customer_journey_turn("Luiza.", conv, FUTANBEAR_CATALOG)

    profile_data = read_json(Path("state") / conv / "profile.json")
    assert "vegano" in profile_data["dietary_restrictions"]

    for rr in r2["evaluation"].rubric_results:
        if rr.criterion == "RESTRICAO_VEGANO":
            assert rr.passed

    return True


def test_scenario_5_evaluator_rejection_and_retry() -> bool:
    # This test verifies fallback behavior with impossible constraints
    conv = _make_conv_id("retry")
    r1 = run_customer_journey_turn("Quero whey. Orcamento R$ 1.", conv, FUTANBEAR_CATALOG)
    r2 = run_customer_journey_turn("Joao. Sou intolerante a lactose.", conv, FUTANBEAR_CATALOG)

    # With budget R$1 and lactose restriction, no products match
    # System should return honest response, not crash
    assert len(r2["response"]) > 10
    return True


def test_scenario_6_full_order_pipeline() -> bool:
    conv = _make_conv_id("order")
    run_customer_journey_turn("Oi, quero algo pra me recuperar depois do treino. R$ 200.", conv, FUTANBEAR_CATALOG)
    run_customer_journey_turn("Patricia. Sou intolerante a lactose.", conv, FUTANBEAR_CATALOG)

    # Simulate selecting a product by setting context directly
    state_dir = Path("state") / conv
    state_data = read_json(state_dir / "state.json")
    state_data["context"]["selected_sku"] = "REC-ZMA-120"
    state_data["context"]["shipping_address"] = {"street": "Rua Augusta", "number": "1500",
                                                    "city": "Sao Paulo", "state": "SP", "zip": "01310100"}
    state_data["context"]["payment_method"] = "pix"
    state_data["context"]["product_selected"] = True
    state_data["context"]["product_validated"] = True
    write_json(state_data, state_dir / "state.json")

    r = run_customer_journey_turn("Pode fechar o pedido. PIX.", conv, FUTANBEAR_CATALOG)
    assert r["order"] is not None
    assert r["order"].payment_status == "confirmed"
    assert r["order"].total_brl > 0

    assert (state_dir / "order.json").exists()
    assert (state_dir / "fulfillment.json").exists()
    assert (state_dir / "retention.json").exists()

    fulf_data = read_json(state_dir / "fulfillment.json")
    assert fulf_data["tracking_code"].startswith("KDA-")

    ret_data = read_json(state_dir / "retention.json")
    assert ret_data["follow_up_scheduled_at"] != ""

    return True


def test_scenario_7_order_with_invalid_zip() -> bool:
    conv = _make_conv_id("invalidzip")

    # Setup state manually for DECISION stage
    state_dir = Path("state") / conv
    state_dir.mkdir(parents=True, exist_ok=True)
    profile = CustomerProfile(conversation_id=conv, name="Teste", customer_id="x",
                               dietary_restrictions=["lactose_free"])
    write_json(profile, state_dir / "profile.json")

    state = JourneyState(conversation_id=conv, current_stage=JourneyStage.CONSIDERATION,
                         context={"intent_classified": True, "minimal_context_collected": True,
                                  "product_selected": True, "product_validated": True,
                                  "selected_sku": "REC-ZMA-120",
                                  "shipping_address": {"zip": "123"},
                                  "payment_method": "pix"})
    write_json(state, state_dir / "state.json")

    r = run_customer_journey_turn("finalizar", conv, FUTANBEAR_CATALOG)
    assert "CEP" in r["response"] or "zip" in r["response"].lower()
    return True


def test_scenario_8_out_of_stock_product() -> bool:
    conv = _make_conv_id("outofstock")

    state_dir = Path("state") / conv
    state_dir.mkdir(parents=True, exist_ok=True)
    profile = CustomerProfile(conversation_id=conv, name="Maria", customer_id="x")
    write_json(profile, state_dir / "profile.json")

    state = JourneyState(conversation_id=conv, current_stage=JourneyStage.CONSIDERATION,
                         context={"intent_classified": True, "minimal_context_collected": True,
                                  "product_selected": True, "product_validated": True,
                                  "selected_sku": "WHEY-HYDRO-800",
                                  "shipping_address": {"zip": "01310100"},
                                  "payment_method": "pix"})
    write_json(state, state_dir / "state.json")

    r = run_customer_journey_turn("quero comprar", conv, FUTANBEAR_CATALOG)
    assert r["order"] is not None
    assert r["order"].payment_status == "rejected"
    return True


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    tests = [
        ("Cenario 1: Caminho Feliz", test_scenario_1_happy_path),
        ("Cenario 2: Restricao Lactose", test_scenario_2_lactose_restriction),
        ("Cenario 3: Orcamento Impossivel", test_scenario_3_budget_violation),
        ("Cenario 4: Cliente Vegano", test_scenario_4_vegan_customer),
        ("Cenario 5: Rejeicao + Retry + Fallback", test_scenario_5_evaluator_rejection_and_retry),
        ("Cenario 6: Pipeline de Pedido Completo", test_scenario_6_full_order_pipeline),
        ("Cenario 7: CEP Invalido", test_scenario_7_order_with_invalid_zip),
        ("Cenario 8: Fora de Estoque", test_scenario_8_out_of_stock_product),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            result = test_fn()
            if result:
                print(f"  OK  {name}")
                passed += 1
            else:
                print(f" FAIL {name} — retornou False")
                failed += 1
        except Exception as e:
            print(f" FAIL {name} — {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Resultado: {passed}/{len(tests)} passaram, {failed} falharam")
    print(f"{'='*60}")

    if failed > 0:
        exit(1)
