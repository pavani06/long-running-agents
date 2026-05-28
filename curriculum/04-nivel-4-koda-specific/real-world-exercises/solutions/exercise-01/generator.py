"""
Generator para a feature koda.product_recommendation.

Responsabilidades:
- Filtrar produtos por restricoes, objetivo e orcamento
- Ranquear candidatos por fit com o cliente
- Gerar draft de mensagem WhatsApp
- Expor incertezas nos risk_flags
- NUNCA auto-aprovar ou enviar ao cliente
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum


class FeatureStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ABSTAINED = "ABSTAINED"


class Goal(str, Enum):
    GANHO_MUSCULAR = "ganho_muscular"
    EMAGRECIMENTO = "emagrecimento"
    ENERGIA = "energia"
    RECUPERACAO = "recuperacao"


class JourneyStage(str, Enum):
    DESCOBERTA = "descoberta"
    COMPARACAO = "comparacao"
    DECISAO = "decisao"
    CHECKOUT = "checkout"
    SUPORTE = "suporte"


@dataclass
class CustomerProfile:
    customer_id: str
    restrictions: List[str]
    goal: Goal
    budget_range: tuple
    price_sensitivity: str
    last_objection: Optional[str] = None


@dataclass
class CatalogProduct:
    sku: str
    name: str
    price: float
    protein_per_dose: float
    lactose_free: bool
    gluten_free: bool
    suitable_for: List[str]
    in_stock: bool
    stock_quantity: int
    description: str
    contraindications: List[str] = field(default_factory=list)


@dataclass
class OfferRecord:
    sku: str
    status: str
    timestamp: str
    reason_rejected: Optional[str] = None


@dataclass
class JourneyState:
    current_stage: JourneyStage
    last_customer_intent: str
    sentiment: str
    turns_since_last_purchase: int = 0


@dataclass
class GeneratorInput:
    conversation_id: str
    customer_profile: CustomerProfile
    catalog_products: List[CatalogProduct]
    journey_state: JourneyState
    offer_history: List[OfferRecord]
    token_budget_remaining: int


@dataclass
class RecommendedProduct:
    sku: str
    name: str
    price: float
    why_this_customer: str
    restriction_checks: List[str]
    score: float


@dataclass
class GeneratorOutput:
    feature_run_id: str
    status: FeatureStatus
    recommended_products: List[RecommendedProduct]
    customer_message_draft: str
    evidence: List[str]
    risk_flags: List[str]
    state_updates: dict
    abstain_reason: Optional[str] = None


class ProductRecommendationGenerator:
    """
    Generator para a feature koda.product_recommendation.

    Implementa filtragem em pipeline: restricoes -> goal -> budget ->
    offers -> stock -> ranking. Cada etapa remove candidatos invalidos.
    """

    MAX_RECOMMENDATIONS = 3
    MAX_WHATSAPP_LINES = 8
    MIN_TOKEN_BUDGET = 500

    def __init__(self):
        self._run_counter = 0

    # ═══════════════════════════════════════════════════════════
    # METODOS PUBLICOS
    # ═══════════════════════════════════════════════════════════

    def generate(self, input_data: GeneratorInput) -> GeneratorOutput:
        """Orquestra o pipeline completo de recomendacao."""
        self._run_counter += 1
        feature_run_id = self._make_run_id(input_data.conversation_id)

        # Verifica condicoes de abstencao primeiro
        abstain_reason = self._check_abstain_conditions(input_data)
        if abstain_reason:
            return GeneratorOutput(
                feature_run_id=feature_run_id,
                status=FeatureStatus.ABSTAINED,
                recommended_products=[],
                customer_message_draft="",
                evidence=[],
                risk_flags=[],
                state_updates={},
                abstain_reason=abstain_reason,
            )

        # Pipeline de filtragem em cadeia
        candidates = input_data.catalog_products
        candidates = self._filter_by_restrictions(input_data, candidates)
        candidates = self._filter_by_goal(input_data, candidates)
        candidates = self._filter_by_budget(input_data, candidates)
        candidates = self._filter_previous_offers(input_data, candidates)
        candidates = self._filter_by_stock(candidates)

        # Se apos filtros nao sobrou nenhum candidato, abster
        if not candidates:
            return GeneratorOutput(
                feature_run_id=feature_run_id,
                status=FeatureStatus.ABSTAINED,
                recommended_products=[],
                customer_message_draft="",
                evidence=["Nenhum produto passou em todos os filtros: restricoes, goal, budget, stock."],
                risk_flags=["limited_options"],
                state_updates={},
                abstain_reason="Nenhum produto compativel encontrado apos aplicar todos os filtros.",
            )

        # Ranking e selecao dos melhores
        ranked = self._rank_candidates(input_data, candidates)
        top_picks = ranked[:self.MAX_RECOMMENDATIONS]

        evidence = self._collect_evidence(input_data, top_picks)
        risk_flags = self._detect_risks(input_data, top_picks)
        message = self._compose_message(input_data, top_picks, risk_flags)
        state_updates = self._prepare_state_updates(top_picks)

        return GeneratorOutput(
            feature_run_id=feature_run_id,
            status=FeatureStatus.PROPOSED,
            recommended_products=top_picks,
            customer_message_draft=message,
            evidence=evidence,
            risk_flags=risk_flags,
            state_updates=state_updates,
        )

    # ═══════════════════════════════════════════════════════════
    # METODOS PRIVADOS
    # ═══════════════════════════════════════════════════════════

    def _make_run_id(self, conversation_id: str) -> str:
        """Gera ID unico correlacionando esta execucao com a conversa."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        short_uuid = uuid.uuid4().hex[:8]
        return f"feat_koda_pr_{conversation_id}_{ts}_{short_uuid}"

    def _check_abstain_conditions(self, input_data: GeneratorInput) -> Optional[str]:
        """Verifica se a feature deve se abster e retorna o motivo."""
        if not input_data.catalog_products:
            return "Catalogo vazio: nenhum produto disponivel para recomendacao."

        if not input_data.customer_profile:
            return "Perfil do cliente ausente: impossivel recomendar sem dados do cliente."

        if not input_data.customer_profile.goal:
            return "Objetivo do cliente nao definido: necessario para filtrar produtos relevantes."

        if input_data.journey_state.current_stage in (JourneyStage.CHECKOUT, JourneyStage.SUPORTE):
            return (
                f"Timing inadequado: cliente esta em "
                f"{input_data.journey_state.current_stage.value}. "
                f"Recomendacao de produto nao e apropriada neste momento."
            )

        if input_data.token_budget_remaining < self.MIN_TOKEN_BUDGET:
            return (
                f"Token budget insuficiente: {input_data.token_budget_remaining} tokens "
                f"restantes, minimo necessario: {self.MIN_TOKEN_BUDGET}."
            )

        if input_data.journey_state.sentiment == "frustrado":
            return "Cliente demonstrou frustracao recente. Recomendar agora seria pressao."

        return None

    def _filter_by_restrictions(
        self,
        input_data: GeneratorInput,
        candidates: List[CatalogProduct],
    ) -> List[CatalogProduct]:
        """Remove produtos que violam restricoes do cliente."""
        restrictions = input_data.customer_profile.restrictions
        if not restrictions:
            return candidates

        result = []
        for product in candidates:
            passes = True
            for restriction in restrictions:
                r = restriction.lower()

                if "lactose" in r:
                    if not product.lactose_free:
                        passes = False
                        break

                if "gluten" in r or "gluten" in r:
                    if not product.gluten_free:
                        passes = False
                        break

                if "gastrite" in r or "estomago" in r:
                    contraindications_lower = [c.lower() for c in product.contraindications]
                    if any(
                        bad in c
                        for bad in ["estimulante", "acido", "cafeina", "picante"]
                        for c in contraindications_lower
                    ):
                        passes = False
                        break

                if "vegano" in r or "vegana" in r:
                    if "vegano" not in [s.lower() for s in product.suitable_for] and \
                       "vegetal" not in product.name.lower():
                        passes = False
                        break

            if passes:
                result.append(product)

        return result

    def _filter_by_goal(
        self,
        input_data: GeneratorInput,
        candidates: List[CatalogProduct],
    ) -> List[CatalogProduct]:
        """Mantem apenas produtos adequados ao objetivo do cliente."""
        goal_value = input_data.customer_profile.goal.value if isinstance(
            input_data.customer_profile.goal, Goal
        ) else input_data.customer_profile.goal

        return [
            p for p in candidates
            if goal_value in [s.lower() for s in p.suitable_for]
        ]

    def _filter_by_budget(
        self,
        input_data: GeneratorInput,
        candidates: List[CatalogProduct],
    ) -> List[CatalogProduct]:
        """Filtra produtos por orcamento."""
        budget_min, budget_max = input_data.customer_profile.budget_range

        if budget_min == 0 and budget_max == 0:
            return candidates

        return [
            p for p in candidates
            if p.price <= budget_max
        ]

    def _filter_previous_offers(
        self,
        input_data: GeneratorInput,
        candidates: List[CatalogProduct],
    ) -> List[CatalogProduct]:
        """Remove produtos ja recusados nesta conversa."""
        rejected_skus = {
            offer.sku for offer in input_data.offer_history
            if offer.status == "recusado"
        }
        if not rejected_skus:
            return candidates

        return [p for p in candidates if p.sku not in rejected_skus]

    def _filter_by_stock(
        self,
        candidates: List[CatalogProduct],
    ) -> List[CatalogProduct]:
        """Remove produtos fora de estoque."""
        return [p for p in candidates if p.in_stock and p.stock_quantity > 0]

    def _rank_candidates(
        self,
        input_data: GeneratorInput,
        candidates: List[CatalogProduct],
    ) -> List[RecommendedProduct]:
        """Ranqueia candidatos por fit com o cliente."""
        restrictions = input_data.customer_profile.restrictions
        budget_min, budget_max = input_data.customer_profile.budget_range
        goal_value = input_data.customer_profile.goal.value if isinstance(
            input_data.customer_profile.goal, Goal
        ) else input_data.customer_profile.goal

        ranked = []
        for product in candidates:
            restriction_checks = self._build_restriction_checks(product, restrictions)

            # Calcula score multi-fator
            goal_score = 1.0 if goal_value in [s.lower() for s in product.suitable_for] else 0.5
            budget_mid = (budget_min + budget_max) / 2 if budget_max > 0 else float("inf")
            budget_score = (
                1.0 if product.price <= budget_mid * 0.85
                else 0.8 if product.price <= budget_max
                else 0.4
            )
            stock_score = min(1.0, product.stock_quantity / 20.0)
            restriction_score = 1.0  # Todos passaram nos filtros

            score = (goal_score * 0.4 + budget_score * 0.25 + stock_score * 0.15 + restriction_score * 0.2)

            why = self._build_why_this_customer(product, restrictions, goal_value, budget_max)

            ranked.append(RecommendedProduct(
                sku=product.sku,
                name=product.name,
                price=product.price,
                why_this_customer=why,
                restriction_checks=restriction_checks,
                score=round(score, 4),
            ))

        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked

    def _build_restriction_checks(
        self,
        product: CatalogProduct,
        restrictions: List[str],
    ) -> List[str]:
        """Constroi lista de verificacoes de restricao para um produto."""
        checks = []
        for restriction in restrictions:
            r = restriction.lower()
            if "lactose" in r:
                status = "OK" if product.lactose_free else "FALHA"
                checks.append(f"sem_lactose: {status} (lactose_free={product.lactose_free})")
            if "gluten" in r:
                status = "OK" if product.gluten_free else "FALHA"
                checks.append(f"sem_gluten: {status} (gluten_free={product.gluten_free})")
            if "gastrite" in r or "estomago" in r:
                has_contra = any(
                    bad in c.lower()
                    for bad in ["estimulante", "acido", "cafeina"]
                    for c in product.contraindications
                )
                status = "FALHA" if has_contra else "OK"
                checks.append(f"gastrite: {status} (contraindicacoes={product.contraindications})")
        return checks

    def _build_why_this_customer(
        self,
        product: CatalogProduct,
        restrictions: List[str],
        goal: str,
        budget_max: float,
    ) -> str:
        """Constroi explicacao personalizada do motivo da recomendacao."""
        parts = []

        # Restricoes respeitadas
        if restrictions:
            parts.append(f"Compativel com: {', '.join(restrictions)}")

        # Objetivo
        goal_labels = {
            "ganho_muscular": "ganho muscular",
            "emagrecimento": "emagrecimento",
            "energia": "energia",
            "recuperacao": "recuperacao",
        }
        parts.append(f"Adequado para {goal_labels.get(goal, goal)}")

        # Orcamento
        if budget_max > 0:
            if product.price <= budget_max * 0.8:
                parts.append(f"Confortavel dentro do orcamento")
            else:
                parts.append(f"Dentro do orcamento de R$ {budget_max:.0f}")

        # Caracteristicas especiais
        if product.lactose_free:
            parts.append("Zero lactose")
        if product.gluten_free:
            parts.append("Sem glúten")
        if product.protein_per_dose >= 20:
            parts.append(f"{product.protein_per_dose:.0f}g proteina/dose")

        return ". ".join(parts) + "."

    def _collect_evidence(
        self,
        input_data: GeneratorInput,
        products: List[RecommendedProduct],
    ) -> List[str]:
        """Coleta evidencias que justificam cada recomendacao."""
        evidence = []

        catalog_map = {p.sku: p for p in input_data.catalog_products}

        for rp in products:
            cat_product = catalog_map.get(rp.sku)
            if cat_product:
                evidence.append(
                    f"{rp.sku}: lactose_free={cat_product.lactose_free}, "
                    f"gluten_free={cat_product.gluten_free} "
                    f"confirmado no catalog_snapshot."
                )
                evidence.append(
                    f"{rp.sku}: in_stock=True, stock_quantity={cat_product.stock_quantity} "
                    f"confirmado no catalog_snapshot."
                )
                evidence.append(
                    f"{rp.sku}: preco=R$ {cat_product.price:.2f} "
                    f"confirmado no catalog_snapshot."
                )

        # Registra produtos excluidos por restricao
        restrictions = input_data.customer_profile.restrictions
        for product in input_data.catalog_products:
            if product.sku not in {rp.sku for rp in products}:
                reasons = []
                if "sem_lactose" in restrictions and not product.lactose_free:
                    reasons.append(f"lactose_free=False viola restriction=sem_lactose")
                if "sem_gluten" in restrictions and not product.gluten_free:
                    reasons.append(f"gluten_free=False viola restriction=sem_gluten")
                if reasons:
                    evidence.append(f"{product.sku} excluido: {'; '.join(reasons)}")

        return evidence

    def _detect_risks(
        self,
        input_data: GeneratorInput,
        products: List[RecommendedProduct],
    ) -> List[str]:
        """Detecta riscos que o Evaluator deve considerar."""
        risks = []

        if input_data.customer_profile.restrictions:
            risks.append("restriction_sensitive")

        if input_data.customer_profile.price_sensitivity in ("medium", "high"):
            risks.append("price_sensitive")

        if any(p.stock_quantity < 10 for p in input_data.catalog_products if p.sku in {rp.sku for rp in products}):
            risks.append("stock_low")

        if input_data.customer_profile.budget_range == (0, 0):
            risks.append("budget_uncertainty")

        if input_data.journey_state.turns_since_last_purchase == 0:
            risks.append("first_time_buyer")

        if input_data.journey_state.sentiment in ("negativo", "frustrado"):
            risks.append("sentiment_fragile")

        if len(products) < 2:
            risks.append("limited_options")

        return risks

    def _compose_message(
        self,
        input_data: GeneratorInput,
        products: List[RecommendedProduct],
        risk_flags: List[str],
    ) -> str:
        """Compoe a mensagem WhatsApp para o cliente."""
        customer_name = input_data.customer_profile.customer_id.replace("cust_", "").split("_")[0].title()
        restrictions = input_data.customer_profile.restrictions

        lines = []

        # Saudacao com mencao de restricoes
        if restrictions:
            rest_text = " e ".join(restrictions)
            lines.append(f"{customer_name}, considerando {rest_text}, filtrei opcoes seguras para voce:\n")
        else:
            lines.append(f"{customer_name}, aqui vao as melhores opcoes para voce:\n")

        # Produtos (max 3, cada um ocupa ~2 linhas)
        for i, product in enumerate(products):
            emoji = ["🥛", "🌱", "💪"][i] if i < 3 else "➡️"
            lines.append(f"{emoji} {product.name} — R$ {product.price:.2f}")
            # Features com emoji check
            features = []
            if "Zero lactose" in product.why_this_customer:
                features.append("✓ Zero lactose")
            if product.name and "Isolado" in product.name:
                features.append(f"✓ Alta pureza")
            features.append(f"✓ Cabe no seu orcamento")
            lines.append("   " + "  ".join(features[:2]))
            lines.append("")

        # Call-to-action suave
        if "price_sensitive" in risk_flags:
            lines.append("Qual delas se encaixa melhor para voce?")
        elif len(products) == 1:
            lines.append("Essa e a melhor opcao para o seu perfil. Quer fechar?")
        else:
            lines.append("Quer que eu compare com mais detalhes ou prefere alguma?")

        message = "\n".join(lines)
        # Garantir max 8 linhas
        message_lines = message.split("\n")
        if len(message_lines) > self.MAX_WHATSAPP_LINES:
            message_lines = message_lines[:self.MAX_WHATSAPP_LINES - 1]
            message_lines.append("...")
            message = "\n".join(message_lines)

        return message

    def _prepare_state_updates(self, products: List[RecommendedProduct]) -> dict:
        """Prepara state_updates para persistir apos aprovacao."""
        return {
            "recommended_skus": [p.sku for p in products],
            "recommended_at": datetime.now(timezone.utc).isoformat(),
            "count": len(products),
        }
