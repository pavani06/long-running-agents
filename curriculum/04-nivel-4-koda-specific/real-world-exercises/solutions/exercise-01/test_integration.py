import unittest
from generator import (
    ProductRecommendationGenerator,
    GeneratorInput,
    CustomerProfile,
    CatalogProduct,
    JourneyState,
    Goal,
    JourneyStage,
    FeatureStatus,
)
from evaluator import (
    ProductRecommendationEvaluator,
    EvaluatorInput,
    Verdict,
)


class TestProductRecommendationPipeline(unittest.TestCase):

    def setUp(self):
        self.generator = ProductRecommendationGenerator()
        self.evaluator = ProductRecommendationEvaluator()

        self.rafael_profile = CustomerProfile(
            customer_id="cust_rafael_001",
            restrictions=["sem_lactose", "gastrite"],
            goal=Goal.GANHO_MUSCULAR,
            budget_range=(0, 140),
            price_sensitivity="medium",
        )

        self.rafael_journey = JourneyState(
            current_stage=JourneyStage.DESCOBERTA,
            last_customer_intent="quero whey para ganhar massa",
            sentiment="positivo",
        )

        self.catalog = [
            CatalogProduct(
                sku="WHEY-ISO-001", name="Whey Isolado Neutro 900g",
                price=129.90, protein_per_dose=23.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular", "recuperacao"],
                in_stock=True, stock_quantity=45,
                description="Proteina isolada, zero lactose, digestao suave.",
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
            CatalogProduct(
                sku="VEG-PRO-003", name="Proteina Vegetal Ervilha 800g",
                price=119.90, protein_per_dose=20.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular", "emagrecimento", "energia"],
                in_stock=True, stock_quantity=32,
                description="Proteina 100% vegetal, hipoalergenica, digestao leve.",
                contraindications=[],
            ),
        ]

    def test_full_pipeline_safe_recommendation(self):
        gen_input = GeneratorInput(
            conversation_id="conv_rafael_2026_05_28_001",
            customer_profile=self.rafael_profile,
            catalog_products=self.catalog,
            journey_state=self.rafael_journey,
            offer_history=[],
            token_budget_remaining=4000,
        )

        gen_output = self.generator.generate(gen_input)

        self.assertEqual(gen_output.status, FeatureStatus.PROPOSED)

        skus = [p.sku for p in gen_output.recommended_products]
        self.assertNotIn("WHEY-CONC-002", skus,
                        "Produto com lactose nao deveria ser recomendado")
        self.assertIn("WHEY-ISO-001", skus,
                     "Whey Isolado deveria estar nas recomendacoes")

        eval_input = EvaluatorInput(
            feature_run_id=gen_output.feature_run_id,
            generator_output=gen_output,
            customer_profile=self.rafael_profile,
            catalog_snapshot=self.catalog,
            contract_version="1.0.0",
        )

        eval_output = self.evaluator.evaluate(eval_input)

        self.assertEqual(eval_output.verdict, Verdict.APROVAR)
        self.assertGreaterEqual(eval_output.overall_score, 0.82)
        self.assertGreaterEqual(eval_output.confidence_score, 0.70)

        self.assertTrue(len(eval_output.approved_state_updates) > 0,
                       "State updates devem ser persistidos quando aprovado")

        self.assertEqual(eval_output.feature_run_id, gen_output.feature_run_id,
                        "feature_run_id deve ser consistente")

    def test_pipeline_blocks_unsafe_recommendation(self):
        unsafe_catalog = [
            CatalogProduct(
                sku="WHEY-CONC-002", name="Whey Concentrado Premium 1kg",
                price=89.90, protein_per_dose=21.0,
                lactose_free=False, gluten_free=True,
                suitable_for=["ganho_muscular"],
                in_stock=True, stock_quantity=120,
                description="Contem lactose.",
                contraindications=["contem lactose"],
            ),
        ]

        gen_input = GeneratorInput(
            conversation_id="conv_test_unsafe",
            customer_profile=self.rafael_profile,
            catalog_products=unsafe_catalog,
            journey_state=self.rafael_journey,
            offer_history=[],
            token_budget_remaining=4000,
        )

        gen_output = self.generator.generate(gen_input)

        if gen_output.status == FeatureStatus.PROPOSED:
            eval_input = EvaluatorInput(
                feature_run_id=gen_output.feature_run_id,
                generator_output=gen_output,
                customer_profile=self.rafael_profile,
                catalog_snapshot=unsafe_catalog,
                contract_version="1.0.0",
            )
            eval_output = self.evaluator.evaluate(eval_input)

            self.assertIn(
                eval_output.verdict,
                [Verdict.REJEITAR, Verdict.REJEITAR_IMEDIATAMENTE],
                f"Recomendacao insegura deve ser rejeitada. Verdict: {eval_output.verdict}"
            )
            self.assertEqual(eval_output.approved_state_updates, {},
                           "Nenhum state update deve ser aprovado para rejeicao")
        else:
            self.assertEqual(gen_output.status, FeatureStatus.ABSTAINED,
                           "Generator pode se abster se so tem produtos inseguros")

    def test_offer_history_prevents_repeat(self):
        gen_input_1 = GeneratorInput(
            conversation_id="conv_test_repeat",
            customer_profile=CustomerProfile(
                customer_id="cust_lucas", restrictions=[],
                goal=Goal.GANHO_MUSCULAR, budget_range=(0, 200),
                price_sensitivity="low",
            ),
            catalog_products=self.catalog,
            journey_state=self.rafael_journey,
            offer_history=[],
            token_budget_remaining=4000,
        )

        output_1 = self.generator.generate(gen_input_1)
        skus_1 = [p.sku for p in output_1.recommended_products]
        self.assertTrue(len(skus_1) > 0)

        eval_1 = self.evaluator.evaluate(EvaluatorInput(
            feature_run_id=output_1.feature_run_id,
            generator_output=output_1,
            customer_profile=gen_input_1.customer_profile,
            catalog_snapshot=self.catalog,
            contract_version="1.0.0",
        ))

        rejected_sku = "WHEY-ISO-001"
        gen_input_2 = GeneratorInput(
            conversation_id="conv_test_repeat",
            customer_profile=gen_input_1.customer_profile,
            catalog_products=self.catalog,
            journey_state=self.rafael_journey,
            offer_history=[
                type('OfferRecord', (), {
                    'sku': rejected_sku,
                    'status': 'recusado',
                    'timestamp': '2026-05-28T10:00:00Z',
                    'reason_rejected': 'cliente nao quis',
                })(),
            ],
            token_budget_remaining=4000,
        )

        output_2 = self.generator.generate(gen_input_2)
        skus_2 = [p.sku for p in output_2.recommended_products]

        if output_2.status == FeatureStatus.PROPOSED:
            self.assertNotIn(rejected_sku, skus_2,
                           f"Produto recusado {rejected_sku} nao deve ser reoferecido")


if __name__ == "__main__":
    unittest.main()
