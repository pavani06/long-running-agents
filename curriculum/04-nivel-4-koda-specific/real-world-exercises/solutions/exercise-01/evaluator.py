"""
Evaluator para a feature koda.product_recommendation.

Responsabilidades:
- Aplicar rubric de 5 dimensoes com pesos e minimos
- Detectar blockers de seguranca antes de calcular scores
- Emitir verdict com justificativa e feedback acionavel
- NUNCA aprovar output que viola constraints
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Verdict(str, Enum):
    APROVAR = "APROVAR"
    APROVAR_COM_RESSALVAS = "APROVAR_COM_RESSALVAS"
    REJEITAR = "REJEITAR"
    REJEITAR_IMEDIATAMENTE = "REJEITAR_IMEDIATAMENTE"


class FeatureStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ABSTAINED = "ABSTAINED"


@dataclass
class DimensionScore:
    dimension: str
    score: float
    justification: str
    evidence_used: List[str]


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


@dataclass
class CustomerProfile:
    customer_id: str
    restrictions: list
    goal: str
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
    suitable_for: list
    in_stock: bool
    stock_quantity: int
    description: str
    contraindications: list = field(default_factory=list)


@dataclass
class EvaluatorInput:
    feature_run_id: str
    generator_output: GeneratorOutput
    customer_profile: CustomerProfile
    catalog_snapshot: List[CatalogProduct]
    contract_version: str


@dataclass
class EvaluatorOutput:
    feature_run_id: str
    rubric_id: str
    verdict: Verdict
    overall_score: float
    confidence_score: float
    dimension_scores: List[DimensionScore]
    blockers: List[str]
    feedback_to_generator: List[str]
    approved_state_updates: dict


class ProductRecommendationEvaluator:
    """Evaluator com rubric de 5 dimensoes para product recommendation."""

    RUBRIC_ID = "koda.product_recommendation.v1"
    APPROVAL_THRESHOLD = 0.82
    MIN_CONFIDENCE = 0.70
    MIN_RESERVATIONS_OVERALL = 0.74
    MIN_RESERVATIONS_CONFIDENCE = 0.65

    DIMENSIONS = {
        "safety": {"weight": 0.30, "minimum": 0.80},
        "goal_fit": {"weight": 0.25, "minimum": 0.70},
        "budget_fit": {"weight": 0.15, "minimum": 0.60},
        "timing": {"weight": 0.15, "minimum": 0.60},
        "clarity": {"weight": 0.15, "minimum": 0.70},
    }

    def evaluate(self, input_data: EvaluatorInput) -> EvaluatorOutput:
        output = input_data.generator_output

        if output.status == FeatureStatus.ABSTAINED:
            return EvaluatorOutput(
                feature_run_id=input_data.feature_run_id,
                rubric_id=self.RUBRIC_ID,
                verdict=Verdict.APROVAR_COM_RESSALVAS,
                overall_score=0.0,
                confidence_score=1.0,
                dimension_scores=[],
                blockers=[],
                feedback_to_generator=[],
                approved_state_updates={},
            )

        blockers = self._detect_blockers(input_data)
        if blockers:
            return self._build_rejection(input_data, blockers, immediate=True)

        dimension_scores = self._score_all_dimensions(input_data)

        overall_score = self._calculate_overall(dimension_scores)

        for ds in dimension_scores:
            dim_config = self.DIMENSIONS.get(ds.dimension, {})
            minimum = dim_config.get("minimum", 0)
            if ds.score < minimum and ds.dimension == "safety":
                return self._build_rejection(
                    input_data,
                    [f"Safety abaixo do minimo ({ds.score:.2f} < {minimum}): {ds.justification}"],
                    immediate=True,
                )

        for ds in dimension_scores:
            dim_config = self.DIMENSIONS.get(ds.dimension, {})
            minimum = dim_config.get("minimum", 0)
            if ds.score < minimum:
                feedback = [f"{ds.dimension}: {ds.score:.2f} abaixo do minimo {minimum}. {ds.justification}"]
                return EvaluatorOutput(
                    feature_run_id=input_data.feature_run_id,
                    rubric_id=self.RUBRIC_ID,
                    verdict=Verdict.REJEITAR,
                    overall_score=round(overall_score, 4),
                    confidence_score=0.0,
                    dimension_scores=dimension_scores,
                    blockers=[],
                    feedback_to_generator=feedback,
                    approved_state_updates={},
                )

        confidence = self._calculate_confidence(dimension_scores, input_data)

        verdict = self._decide_verdict(overall_score, confidence)

        feedback = self._generate_feedback(verdict, dimension_scores)

        approved_updates = (
            output.state_updates
            if verdict in (Verdict.APROVAR, Verdict.APROVAR_COM_RESSALVAS)
            else {}
        )

        return EvaluatorOutput(
            feature_run_id=input_data.feature_run_id,
            rubric_id=self.RUBRIC_ID,
            verdict=verdict,
            overall_score=round(overall_score, 4),
            confidence_score=round(confidence, 4),
            dimension_scores=dimension_scores,
            blockers=[],
            feedback_to_generator=feedback,
            approved_state_updates=approved_updates,
        )

    # ═══════════════════════════════════════════════════════════
    # BLOCKER DETECTION
    # ═══════════════════════════════════════════════════════════

    def _detect_blockers(self, input_data: EvaluatorInput) -> List[str]:
        blockers = []
        output = input_data.generator_output
        customer = input_data.customer_profile

        catalog_map = {p.sku: p for p in input_data.catalog_snapshot}

        for product in output.recommended_products:
            cat_product = catalog_map.get(product.sku)

            # Blocker 1: Produto nao esta no catalogo
            if cat_product is None:
                blockers.append(
                    f"BLOCKER: SKU {product.sku} nao encontrado no catalog_snapshot. "
                    f"Produto pode ter sido inventado."
                )
                continue

            # Blocker 2: Restricao de lactose
            if "sem_lactose" in customer.restrictions and not cat_product.lactose_free:
                blockers.append(
                    f"BLOCKER: {product.sku} ({product.name}) tem lactose_free=False, "
                    f"mas cliente tem restriction=sem_lactose."
                )

            # Blocker 3: Restricao de gluten
            if "sem_gluten" in customer.restrictions and not cat_product.gluten_free:
                blockers.append(
                    f"BLOCKER: {product.sku} ({product.name}) tem gluten_free=False, "
                    f"mas cliente tem restriction=sem_gluten."
                )

            # Blocker 4: Contraindicacoes vs gastrite
            if "gastrite" in customer.restrictions:
                contraindications_lower = [c.lower() for c in cat_product.contraindications]
                for bad_term in ["estimulante", "cafeina", "acido"]:
                    if any(bad_term in c for c in contraindications_lower):
                        blockers.append(
                            f"BLOCKER: {product.sku} ({product.name}) contem {bad_term} "
                            f"nas contraindicacoes, mas cliente tem gastrite."
                        )
                        break

            # Blocker 5: Preco inventado
            if abs(product.price - cat_product.price) > 0.01:
                blockers.append(
                    f"BLOCKER: Preco divergente para {product.sku}. "
                    f"Output: R$ {product.price:.2f}, Catalog: R$ {cat_product.price:.2f}."
                )

            # Blocker 6: Fora de estoque
            if not cat_product.in_stock or cat_product.stock_quantity == 0:
                blockers.append(
                    f"BLOCKER: {product.sku} ({product.name}) esta fora de estoque "
                    f"(in_stock={cat_product.in_stock}, quantity={cat_product.stock_quantity})."
                )

            # Blocker 7: Promessa de resultado garantido
            guaranteed_phrases = [
                "resultado garantido", "garantimos resultado",
                "resultado em 7 dias", "emagrece rapido",
                "resultado certo", "garantia de ganho",
            ]
            draft_lower = output.customer_message_draft.lower()
            for phrase in guaranteed_phrases:
                if phrase in draft_lower:
                    blockers.append(
                        f"BLOCKER: Mensagem contem promessa de resultado "
                        f"garantido: '{phrase}'."
                    )
                    break

            # Blocker 8: Restricao vegana vs produto animal
            if "vegano" in customer.restrictions or "vegana" in customer.restrictions:
                animal_indicators = ["whey", "leite", "lactose", "caseina", "albumina"]
                product_name_lower = product.name.lower()
                if any(indicator in product_name_lower for indicator in animal_indicators):
                    blockers.append(
                        f"BLOCKER: {product.sku} ({product.name}) parece ser de origem "
                        f"animal, mas cliente tem restriction=vegano."
                    )

        return blockers

    # ═══════════════════════════════════════════════════════════
    # DIMENSION SCORING
    # ═══════════════════════════════════════════════════════════

    def _score_all_dimensions(self, input_data: EvaluatorInput) -> List[DimensionScore]:
        return [
            self._score_safety(input_data),
            self._score_goal_fit(input_data),
            self._score_budget_fit(input_data),
            self._score_timing(input_data),
            self._score_clarity(input_data),
        ]

    def _score_safety(self, input_data: EvaluatorInput) -> DimensionScore:
        output = input_data.generator_output
        customer = input_data.customer_profile
        catalog_map = {p.sku: p for p in input_data.catalog_snapshot}

        if not output.recommended_products:
            return DimensionScore("safety", 1.0, "Nenhum produto para avaliar.", [])

        scores = []
        evidence = []
        for product in output.recommended_products:
            cat = catalog_map.get(product.sku)
            if cat is None:
                scores.append(0.0)
                evidence.append(f"{product.sku}: ausente do catalogo")
                continue

            product_score = 1.0
            checks = []

            for restriction in customer.restrictions:
                r = restriction.lower()
                if "lactose" in r:
                    if cat.lactose_free:
                        checks.append("OK")
                    else:
                        checks.append("FALHA")
                        product_score = 0.0
                if "gluten" in r:
                    if cat.gluten_free:
                        checks.append("OK")
                    else:
                        checks.append("FALHA")
                        product_score = 0.0
                if "gastrite" in r:
                    contra_lower = [c.lower() for c in cat.contraindications]
                    if any(
                        bad in c for bad in ["estimulante", "cafeina", "acido"]
                        for c in contra_lower
                    ):
                        checks.append("FALHA")
                        product_score = 0.0
                    else:
                        checks.append("OK")

            scores.append(product_score)
            evidence.append(
                f"{product.sku}: restriction_checks={checks}, score={product_score}"
            )

        if any(s == 0.0 for s in scores):
            avg = 0.0
            justification = "Um ou mais produtos violam restricao de saude. "
        else:
            avg = sum(scores) / len(scores)
            justification = "Todos os produtos respeitam as restricoes de saude documentadas."

        if avg == 1.0:
            score = 1.0
        elif avg >= 0.8:
            score = 0.8
        elif avg >= 0.5:
            score = 0.6
        else:
            score = 0.2

        return DimensionScore("safety", score, justification, evidence)

    def _score_goal_fit(self, input_data: EvaluatorInput) -> DimensionScore:
        output = input_data.generator_output
        goal = input_data.customer_profile.goal
        if hasattr(goal, 'value'):
            goal = goal.value
        catalog_map = {p.sku: p for p in input_data.catalog_snapshot}

        if not output.recommended_products:
            return DimensionScore("goal_fit", 0.0, "Nenhum produto recomendado.", [])

        scores = []
        evidence = []
        for product in output.recommended_products:
            cat = catalog_map.get(product.sku)
            if cat is None:
                scores.append(0.0)
                continue

            suitable = [s.lower() for s in cat.suitable_for]
            if goal in suitable:
                scores.append(1.0)
                evidence.append(f"{product.sku}: suitable_for contem {goal}")
            else:
                scores.append(0.3)
                evidence.append(f"{product.sku}: suitable_for={suitable}, nao contem {goal}")

        avg = sum(scores) / len(scores)
        if avg >= 0.9:
            score = 1.0
        elif avg >= 0.7:
            score = 0.8
        elif avg >= 0.4:
            score = 0.6
        else:
            score = 0.3

        justification = (
            f"{sum(1 for s in scores if s >= 0.9)} de {len(scores)} "
            f"produtos sao otimos para o goal '{goal}'."
        )
        return DimensionScore("goal_fit", score, justification, evidence)

    def _score_budget_fit(self, input_data: EvaluatorInput) -> DimensionScore:
        output = input_data.generator_output
        budget_min, budget_max = input_data.customer_profile.budget_range

        if not output.recommended_products:
            return DimensionScore("budget_fit", 1.0, "Nenhum produto para avaliar.", [])

        if budget_min == 0 and budget_max == 0:
            return DimensionScore(
                "budget_fit", 0.7,
                "Budget nao definido pelo cliente; ajustando score para neutro.",
                [],
            )

        scores = []
        evidence = []
        for product in output.recommended_products:
            if product.price <= budget_max:
                comfort = (budget_max - product.price) / budget_max if budget_max > 0 else 1.0
                if comfort >= 0.3:
                    scores.append(1.0)
                    evidence.append(f"{product.sku}: R$ {product.price:.2f} confortavel dentro do budget R$ {budget_max:.2f}")
                elif comfort >= 0.05:
                    scores.append(0.8)
                    evidence.append(f"{product.sku}: R$ {product.price:.2f} proximo do limite R$ {budget_max:.2f}")
                else:
                    scores.append(0.6)
                    evidence.append(f"{product.sku}: R$ {product.price:.2f} no limite exato do budget")
            else:
                scores.append(0.2)
                evidence.append(f"{product.sku}: R$ {product.price:.2f} ACIMA do budget R$ {budget_max:.2f}")

        avg = sum(scores) / len(scores)
        justification = f"Media de budget fit: {avg:.2f}. "
        if all(s >= 0.8 for s in scores):
            justification += "Todos confortaveis no orcamento."
        elif all(s >= 0.6 for s in scores):
            justification += "Maioria dentro do orcamento com margem apertada."
        else:
            justification += "Alguns produtos acima do orcamento."

        return DimensionScore("budget_fit", avg, justification, evidence)

    def _score_timing(self, input_data: EvaluatorInput) -> DimensionScore:
        journey = input_data.customer_profile
        sentiment = getattr(journey, 'sentiment', 'neutro')
        if hasattr(journey, 'journey_state'):
            stage = getattr(journey, 'journey_state', 'descoberta')
        else:
            stage = "descoberta"

        if sentiment == "frustrado":
            return DimensionScore("timing", 0.0, "Cliente frustrado: recomendar agora e pressao.", [])
        if sentiment == "negativo":
            return DimensionScore("timing", 0.3, "Cliente com sentimento negativo. Timing ruim.", [])

        timing_map = {
            "descoberta": (1.0, "Cliente em descoberta: momento ideal para recomendar."),
            "comparacao": (0.8, "Cliente comparando: timing bom para refinar opcoes."),
            "decisao": (0.6, "Cliente decidindo: timing aceitavel, mas evitar overload."),
            "checkout": (0.0, "Cliente em checkout: nao e momento de recomendar."),
            "suporte": (0.0, "Cliente em suporte: nao e momento de recomendar."),
        }
        score, justification = timing_map.get(stage, (0.6, "Estagio desconhecido, score neutro."))
        return DimensionScore("timing", score, justification, [f"journey_stage={stage}"])

    def _score_clarity(self, input_data: EvaluatorInput) -> DimensionScore:
        message = input_data.generator_output.customer_message_draft
        products = input_data.generator_output.recommended_products

        if not message:
            return DimensionScore("clarity", 0.0, "Mensagem vazia.", [])

        evidence = []
        score = 1.0
        issues = []

        lines = message.split("\n")
        if len(lines) > 8:
            score -= 0.2
            issues.append(f"Mensagem tem {len(lines)} linhas (max 8)")

        aggressive_words = ["compre agora", "imperdivel", "oportunidade unica",
                           "nao perca", "ultima chance", "estoque acabando"]
        message_lower = message.lower()
        for word in aggressive_words:
            if word in message_lower:
                score -= 0.3
                issues.append(f"Tom agressivo detectado: '{word}'")
                break

        has_price = any(f"R$ {p.price:.2f}" in message or f"R${p.price:.2f}" in message for p in products)
        if not has_price and products:
            score -= 0.1
            issues.append("Preco nao mencionado na mensagem")

        has_cta = any(
            phrase in message_lower
            for phrase in ["quer", "prefere", "o que acha", "comparar", "detalhes", "fechar"]
        )
        if not has_cta:
            score -= 0.1
            issues.append("Call-to-action ausente")

        score = max(0.0, min(1.0, score))

        if not issues:
            justification = "Mensagem clara, tom consultivo, call-to-action presente."
        else:
            justification = "; ".join(issues)

        evidence.append(f"linhas={len(lines)}, tom_agressivo={'nao' if score > 0.7 else 'sim'}")
        return DimensionScore("clarity", round(score, 2), justification, evidence)

    # ═══════════════════════════════════════════════════════════
    # SCORE AGGREGATION
    # ═══════════════════════════════════════════════════════════

    def _calculate_overall(self, dimension_scores: List[DimensionScore]) -> float:
        total = 0.0
        for ds in dimension_scores:
            weight = self.DIMENSIONS.get(ds.dimension, {}).get("weight", 0.0)
            total += ds.score * weight
        return total

    def _calculate_confidence(
        self,
        dimension_scores: List[DimensionScore],
        input_data: EvaluatorInput,
    ) -> float:
        factors = []

        has_catalog = len(input_data.catalog_snapshot) > 0
        factors.append(0.3 if has_catalog else 0.0)

        has_restrictions = len(input_data.customer_profile.restrictions) > 0
        factors.append(0.2 if has_restrictions else 0.1)

        evidence_count = sum(len(ds.evidence_used) for ds in dimension_scores)
        factors.append(min(0.3, evidence_count * 0.05))

        score_variance = 0.0
        if len(dimension_scores) >= 2:
            scores = [ds.score for ds in dimension_scores]
            mean = sum(scores) / len(scores)
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            score_variance = variance
        consistency = 0.2 if score_variance < 0.1 else 0.1 if score_variance < 0.3 else 0.0
        factors.append(consistency)

        return sum(factors)

    def _decide_verdict(self, overall_score: float, confidence_score: float) -> Verdict:
        if overall_score >= self.APPROVAL_THRESHOLD and confidence_score >= self.MIN_CONFIDENCE:
            return Verdict.APROVAR
        elif overall_score >= self.MIN_RESERVATIONS_OVERALL and confidence_score >= self.MIN_RESERVATIONS_CONFIDENCE:
            return Verdict.APROVAR_COM_RESSALVAS
        else:
            return Verdict.REJEITAR

    def _generate_feedback(
        self,
        verdict: Verdict,
        dimension_scores: List[DimensionScore],
    ) -> List[str]:
        feedback = []

        if verdict == Verdict.APROVAR:
            return feedback

        for ds in dimension_scores:
            dim_config = self.DIMENSIONS.get(ds.dimension, {})
            minimum = dim_config.get("minimum", 0)
            if ds.score < minimum:
                feedback.append(
                    f"Dimensao '{ds.dimension}': score={ds.score:.2f} "
                    f"(minimo={minimum}). {ds.justification}"
                )
            elif ds.score < 0.65:
                feedback.append(
                    f"Dimensao '{ds.dimension}': score={ds.score:.2f} pode ser melhorado. "
                    f"{ds.justification}"
                )

        if not feedback and verdict == Verdict.APROVAR_COM_RESSALVAS:
            feedback.append("Aprovado com ressalvas. Revisar clareza da mensagem e call-to-action.")

        return feedback

    def _build_rejection(
        self,
        input_data: EvaluatorInput,
        blockers: List[str],
        immediate: bool = False,
    ) -> EvaluatorOutput:
        verdict = Verdict.REJEITAR_IMEDIATAMENTE if immediate else Verdict.REJEITAR
        return EvaluatorOutput(
            feature_run_id=input_data.feature_run_id,
            rubric_id=self.RUBRIC_ID,
            verdict=verdict,
            overall_score=0.0,
            confidence_score=1.0 if immediate else 0.8,
            dimension_scores=[],
            blockers=blockers,
            feedback_to_generator=[b.replace("BLOCKER: ", "") for b in blockers],
            approved_state_updates={},
        )
