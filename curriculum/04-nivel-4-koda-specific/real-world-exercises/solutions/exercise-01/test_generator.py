import unittest
from generator import (
    ProductRecommendationGenerator,
    GeneratorInput,
    GeneratorOutput,
    CustomerProfile,
    CatalogProduct,
    JourneyState,
    OfferRecord,
    Goal,
    JourneyStage,
    FeatureStatus,
    RecommendedProduct,
)


class TestProductRecommendationGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ProductRecommendationGenerator()
        self.compatible_products = [
            CatalogProduct(
                sku="WHEY-ISO-001", name="Whey Isolado Neutro 900g",
                price=129.90, protein_per_dose=23.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular", "recuperacao"],
                in_stock=True, stock_quantity=45,
                description="Proteina isolada de alta pureza, zero lactose.",
                contraindications=[],
            ),
            CatalogProduct(
                sku="VEG-PRO-003", name="Proteina Vegetal Ervilha 800g",
                price=119.90, protein_per_dose=20.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular", "emagrecimento", "energia"],
                in_stock=True, stock_quantity=32,
                description="Proteina 100% vegetal, hipoalergenica.",
                contraindications=[],
            ),
            CatalogProduct(
                sku="WHEY-CONC-002", name="Whey Concentrado Premium 1kg",
                price=89.90, protein_per_dose=21.0,
                lactose_free=False, gluten_free=True,
                suitable_for=["ganho_muscular", "emagrecimento"],
                in_stock=True, stock_quantity=120,
                description="Whey concentrado tradicional, contem tracos de lactose.",
                contraindications=["contem lactose"],
            ),
        ]
        self.sample_customer = CustomerProfile(
            customer_id="cust_rafael_001",
            restrictions=["sem_lactose", "gastrite"],
            goal=Goal.GANHO_MUSCULAR,
            budget_range=(0, 140),
            price_sensitivity="medium",
        )
        self.sample_journey = JourneyState(
            current_stage=JourneyStage.DESCOBERTA,
            last_customer_intent="quero recomendacao de whey",
            sentiment="positivo",
        )

    def _make_input(self, **overrides):
        kwargs = dict(
            conversation_id="conv_test_001",
            customer_profile=self.sample_customer,
            catalog_products=self.compatible_products,
            journey_state=self.sample_journey,
            offer_history=[],
            token_budget_remaining=4000,
        )
        kwargs.update(overrides)
        return GeneratorInput(**kwargs)

    def test_filters_lactose_when_client_restricted(self):
        input_data = self._make_input()
        output = self.generator.generate(input_data)
        skus = [p.sku for p in output.recommended_products]
        self.assertNotIn("WHEY-CONC-002", skus)

    def test_filters_out_of_budget_products(self):
        expensive = CatalogProduct(
            sku="EXP-001", name="Produto Caro", price=199.00,
            protein_per_dose=30.0, lactose_free=True, gluten_free=True,
            suitable_for=["ganho_muscular"], in_stock=True,
            stock_quantity=10, description="Caro.", contraindications=[],
        )
        all_products = self.compatible_products + [expensive]
        input_data = self._make_input(catalog_products=all_products)
        output = self.generator.generate(input_data)
        skus = [p.sku for p in output.recommended_products]
        self.assertNotIn("EXP-001", skus)

    def test_filters_previously_rejected_offers(self):
        input_data = self._make_input(
            offer_history=[
                OfferRecord(sku="WHEY-ISO-001", status="recusado",
                           timestamp="2026-05-28T10:00:00Z", reason_rejected="cliente nao gostou"),
            ]
        )
        output = self.generator.generate(input_data)
        skus = [p.sku for p in output.recommended_products]
        self.assertNotIn("WHEY-ISO-001", skus)

    def test_abstains_when_catalog_empty(self):
        input_data = self._make_input(catalog_products=[])
        output = self.generator.generate(input_data)
        self.assertEqual(output.status, FeatureStatus.ABSTAINED)

    def test_abstains_when_token_budget_low(self):
        input_data = self._make_input(token_budget_remaining=100)
        output = self.generator.generate(input_data)
        self.assertEqual(output.status, FeatureStatus.ABSTAINED)

    def test_max_three_recommendations(self):
        many_products = []
        for i in range(10):
            many_products.append(CatalogProduct(
                sku=f"PROD-{i:03d}", name=f"Produto {i}",
                price=100.0 + i * 5, protein_per_dose=20.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular"], in_stock=True,
                stock_quantity=50, description="...", contraindications=[],
            ))
        input_data = self._make_input(
            customer_profile=CustomerProfile(
                customer_id="cust_test", restrictions=[], goal=Goal.GANHO_MUSCULAR,
                budget_range=(0, 9999), price_sensitivity="low",
            ),
            catalog_products=many_products,
        )
        output = self.generator.generate(input_data)
        self.assertLessEqual(len(output.recommended_products), 3)

    def test_output_has_feature_run_id(self):
        input_data = self._make_input()
        output = self.generator.generate(input_data)
        self.assertTrue(output.feature_run_id)
        self.assertIn("conv_test_001", output.feature_run_id)

    def test_message_within_whatsapp_limit(self):
        input_data = self._make_input()
        output = self.generator.generate(input_data)
        if output.status == FeatureStatus.PROPOSED:
            lines = output.customer_message_draft.split("\n")
            self.assertLessEqual(len(lines), 8)

    def test_evidence_cites_source(self):
        input_data = self._make_input()
        output = self.generator.generate(input_data)
        if output.status == FeatureStatus.PROPOSED:
            for ev in output.evidence:
                self.assertTrue(
                    "catalog_snapshot" in ev or "lactose_free" in ev or
                    "excluido" in ev or "in_stock" in ev or "preco" in ev.lower(),
                    f"Evidence nao cita fonte: {ev}"
                )

    def test_risk_flags_when_restrictions_present(self):
        input_data = self._make_input()
        output = self.generator.generate(input_data)
        if output.status == FeatureStatus.PROPOSED:
            self.assertIn("restriction_sensitive", output.risk_flags)

    def test_abstains_on_checkout_stage(self):
        input_data = self._make_input(
            journey_state=JourneyState(
                current_stage=JourneyStage.CHECKOUT,
                last_customer_intent="finalizar compra",
                sentiment="positivo",
            )
        )
        output = self.generator.generate(input_data)
        self.assertEqual(output.status, FeatureStatus.ABSTAINED)

    def test_abstains_on_frustrated_sentiment(self):
        input_data = self._make_input(
            journey_state=JourneyState(
                current_stage=JourneyStage.DESCOBERTA,
                last_customer_intent="recomendar",
                sentiment="frustrado",
            )
        )
        output = self.generator.generate(input_data)
        self.assertEqual(output.status, FeatureStatus.ABSTAINED)

    def test_filters_by_multiple_restrictions(self):
        multi_restriction_customer = CustomerProfile(
            customer_id="cust_marina", restrictions=["sem_lactose", "sem_gluten"],
            goal=Goal.GANHO_MUSCULAR, budget_range=(0, 200), price_sensitivity="medium",
        )
        gluten_product = CatalogProduct(
            sku="GLUTEN-001", name="Produto com Gluten", price=99.00,
            protein_per_dose=18.0, lactose_free=True, gluten_free=False,
            suitable_for=["ganho_muscular"], in_stock=True,
            stock_quantity=20, description="...", contraindications=[],
        )
        all_products = self.compatible_products + [gluten_product]
        input_data = self._make_input(
            customer_profile=multi_restriction_customer,
            catalog_products=all_products,
        )
        output = self.generator.generate(input_data)
        skus = [p.sku for p in output.recommended_products]
        self.assertNotIn("GLUTEN-001", skus)
        self.assertNotIn("WHEY-CONC-002", skus)

    def test_ranks_by_score_descending(self):
        input_data = self._make_input()
        output = self.generator.generate(input_data)
        if output.status == FeatureStatus.PROPOSED and len(output.recommended_products) >= 2:
            scores = [p.score for p in output.recommended_products]
            self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
