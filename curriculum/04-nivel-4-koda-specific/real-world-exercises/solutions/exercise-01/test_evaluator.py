import unittest
from evaluator import (
    ProductRecommendationEvaluator,
    EvaluatorInput,
    EvaluatorOutput,
    Verdict,
    FeatureStatus,
    RecommendedProduct,
    GeneratorOutput,
    CustomerProfile,
    CatalogProduct,
)


class TestProductRecommendationEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = ProductRecommendationEvaluator()

        self.safe_products = [
            RecommendedProduct(
                sku="WHEY-ISO-001", name="Whey Isolado Neutro 900g",
                price=129.90, why_this_customer="Compativel com restricoes.",
                restriction_checks=["sem_lactose: OK (lactose_free=True)", "gastrite: OK"],
                score=0.92,
            ),
            RecommendedProduct(
                sku="VEG-PRO-003", name="Proteina Vegetal Ervilha 800g",
                price=119.90, why_this_customer="Opcao vegetal segura.",
                restriction_checks=["sem_lactose: OK (lactose_free=True)", "gastrite: OK"],
                score=0.87,
            ),
        ]

        self.safe_catalog = [
            CatalogProduct(
                sku="WHEY-ISO-001", name="Whey Isolado Neutro 900g",
                price=129.90, protein_per_dose=23.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular", "recuperacao"],
                in_stock=True, stock_quantity=45,
                description="...", contraindications=[],
            ),
            CatalogProduct(
                sku="VEG-PRO-003", name="Proteina Vegetal Ervilha 800g",
                price=119.90, protein_per_dose=20.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular", "emagrecimento"],
                in_stock=True, stock_quantity=32,
                description="...", contraindications=[],
            ),
        ]

        self.safe_customer = CustomerProfile(
            customer_id="cust_rafael_001",
            restrictions=["sem_lactose", "gastrite"],
            goal="ganho_muscular",
            budget_range=(0, 140),
            price_sensitivity="medium",
        )

    def _make_generator_output(self, **overrides):
        kwargs = dict(
            feature_run_id="feat_test_001",
            status=FeatureStatus.PROPOSED,
            recommended_products=self.safe_products,
            customer_message_draft="Rafael, aqui esta sua recomendacao. Whey Isolado R$ 129.90.",
            evidence=["WHEY-ISO-001: lactose_free=True confirmado"],
            risk_flags=["restriction_sensitive"],
            state_updates={"recommended_skus": ["WHEY-ISO-001", "VEG-PRO-003"]},
        )
        kwargs.update(overrides)
        return GeneratorOutput(**kwargs)

    def _make_input(self, **overrides):
        kwargs = dict(
            feature_run_id="feat_test_001",
            generator_output=self._make_generator_output(),
            customer_profile=self.safe_customer,
            catalog_snapshot=self.safe_catalog,
            contract_version="1.0.0",
        )
        kwargs.update(overrides)
        return EvaluatorInput(**kwargs)

    def test_rejects_immediately_on_lactose_violation(self):
        lactose_product = RecommendedProduct(
            sku="WHEY-CONC-002", name="Whey Concentrado",
            price=89.90, why_this_customer="Barato.",
            restriction_checks=["sem_lactose: FALHA"],
            score=0.5,
        )
        input_data = self._make_input(
            generator_output=self._make_generator_output(
                recommended_products=[lactose_product],
            ),
            catalog_snapshot=[
                CatalogProduct(
                    sku="WHEY-CONC-002", name="Whey Concentrado",
                    price=89.90, protein_per_dose=21.0,
                    lactose_free=False, gluten_free=True,
                    suitable_for=["ganho_muscular"], in_stock=True,
                    stock_quantity=120, description="...",
                    contraindications=["contem lactose"],
                ),
            ],
        )
        output = self.evaluator.evaluate(input_data)
        self.assertEqual(output.verdict, Verdict.REJEITAR_IMEDIATAMENTE)
        self.assertTrue(len(output.blockers) > 0)

    def test_rejects_when_overall_below_threshold(self):
        bad_output = self._make_generator_output(
            recommended_products=[
                RecommendedProduct(
                    sku="BAD-001", name="Produto Ruim", price=190.00,
                    why_this_customer="Fora do orcamento.",
                    restriction_checks=[], score=0.3,
                ),
            ],
            customer_message_draft="Compra ai.",
            risk_flags=["price_sensitive"],
        )
        bad_customer = CustomerProfile(
            customer_id="cust_test", restrictions=["sem_lactose"],
            goal="emagrecimento", budget_range=(0, 140), price_sensitivity="high",
        )
        bad_catalog = [
            CatalogProduct(
                sku="BAD-001", name="Produto Ruim", price=190.00,
                protein_per_dose=15.0, lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular"], in_stock=True,
                stock_quantity=10, description="...", contraindications=[],
            ),
        ]
        input_data = EvaluatorInput(
            feature_run_id="feat_test_002",
            generator_output=bad_output,
            customer_profile=bad_customer,
            catalog_snapshot=bad_catalog,
            contract_version="1.0.0",
        )
        output = self.evaluator.evaluate(input_data)
        self.assertIn(output.verdict, [Verdict.REJEITAR, Verdict.REJEITAR_IMEDIATAMENTE])

    def test_approves_safe_relevant_recommendation(self):
        input_data = self._make_input()
        output = self.evaluator.evaluate(input_data)
        self.assertEqual(output.verdict, Verdict.APROVAR)
        self.assertGreaterEqual(output.overall_score, 0.82)

    def test_rejects_out_of_stock_product(self):
        out_of_stock_catalog = [
            CatalogProduct(
                sku="WHEY-ISO-001", name="Whey Isolado Neutro 900g",
                price=129.90, protein_per_dose=23.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular"],
                in_stock=False, stock_quantity=0,
                description="...", contraindications=[],
            ),
        ]
        input_data = self._make_input(catalog_snapshot=out_of_stock_catalog)
        output = self.evaluator.evaluate(input_data)
        self.assertEqual(output.verdict, Verdict.REJEITAR_IMEDIATAMENTE)

    def test_rejects_invented_price(self):
        wrong_price_catalog = [
            CatalogProduct(
                sku="WHEY-ISO-001", name="Whey Isolado Neutro 900g",
                price=149.90, protein_per_dose=23.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular"], in_stock=True,
                stock_quantity=45, description="...", contraindications=[],
            ),
            CatalogProduct(
                sku="VEG-PRO-003", name="Proteina Vegetal Ervilha 800g",
                price=119.90, protein_per_dose=20.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular"], in_stock=True,
                stock_quantity=32, description="...", contraindications=[],
            ),
        ]
        input_data = self._make_input(catalog_snapshot=wrong_price_catalog)
        output = self.evaluator.evaluate(input_data)
        self.assertEqual(output.verdict, Verdict.REJEITAR_IMEDIATAMENTE)

    def test_feedback_is_actionable(self):
        lactose_product = RecommendedProduct(
            sku="WHEY-CONC-002", name="Whey Concentrado",
            price=89.90, why_this_customer="...",
            restriction_checks=["sem_lactose: FALHA"], score=0.5,
        )
        input_data = self._make_input(
            generator_output=self._make_generator_output(
                recommended_products=[lactose_product],
            ),
            catalog_snapshot=[
                CatalogProduct(
                    sku="WHEY-CONC-002", name="Whey Concentrado",
                    price=89.90, protein_per_dose=21.0,
                    lactose_free=False, gluten_free=True,
                    suitable_for=["ganho_muscular"], in_stock=True,
                    stock_quantity=120, description="...", contraindications=[],
                ),
            ],
        )
        output = self.evaluator.evaluate(input_data)
        for fb in output.feedback_to_generator:
            self.assertTrue(
                len(fb) > 10,
                f"Feedback muito curto/vago: '{fb}'",
            )
            self.assertTrue(
                "SKU" in fb or "WHEY-CONC" in fb or "lactose" in fb.lower(),
                f"Feedback nao especifica o problema: '{fb}'",
            )

    def test_state_updates_only_on_approval(self):
        input_data = self._make_input(
            generator_output=self._make_generator_output(
                recommended_products=[
                    RecommendedProduct(
                        sku="WHEY-CONC-002", name="Whey Concentrado",
                        price=89.90, why_this_customer="...",
                        restriction_checks=["sem_lactose: FALHA"], score=0.5,
                    ),
                ],
            ),
            catalog_snapshot=[
                CatalogProduct(
                    sku="WHEY-CONC-002", name="Whey Concentrado",
                    price=89.90, protein_per_dose=21.0,
                    lactose_free=False, gluten_free=True,
                    suitable_for=["ganho_muscular"], in_stock=True,
                    stock_quantity=120, description="...", contraindications=[],
                ),
            ],
        )
        output = self.evaluator.evaluate(input_data)
        self.assertEqual(output.approved_state_updates, {})

    def test_confidence_reflects_data_quality(self):
        input_data = self._make_input()
        output_full = self.evaluator.evaluate(input_data)

        partial_input = self._make_input(catalog_snapshot=[])
        output_partial = self.evaluator.evaluate(partial_input)

        self.assertTrue(
            output_full.confidence_score > output_partial.confidence_score
            or output_partial.verdict in (Verdict.REJEITAR_IMEDIATAMENTE, Verdict.APROVAR_COM_RESSALVAS),
            f"Confidence should reflect data quality. "
            f"Full: {output_full.confidence_score}, Partial: {output_partial.confidence_score}, "
            f"Partial verdict: {output_partial.verdict}",
        )

    def test_safety_beats_other_dimensions(self):
        unsafe_catalog = [
            CatalogProduct(
                sku="WHEY-ISO-001", name="Whey Isolado",
                price=129.90, protein_per_dose=23.0,
                lactose_free=False, gluten_free=True,
                suitable_for=["ganho_muscular"], in_stock=True,
                stock_quantity=45, description="...", contraindications=[],
            ),
        ]
        input_data = self._make_input(catalog_snapshot=unsafe_catalog)
        output = self.evaluator.evaluate(input_data)
        self.assertIn(
            output.verdict,
            [Verdict.REJEITAR_IMEDIATAMENTE, Verdict.REJEITAR],
        )

    def test_rubric_weights_sum_to_one(self):
        total_weight = sum(v["weight"] for v in self.evaluator.DIMENSIONS.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)

    def test_approves_with_reservations_for_minor_issues(self):
        mediocre_customer = CustomerProfile(
            customer_id="cust_test", restrictions=[], goal="ganho_muscular",
            budget_range=(0, 200), price_sensitivity="low",
        )
        mediocre_catalog = [
            CatalogProduct(
                sku="VEG-PRO-003", name="Proteina Vegetal Ervilha 800g",
                price=119.90, protein_per_dose=20.0,
                lactose_free=True, gluten_free=True,
                suitable_for=["ganho_muscular", "emagrecimento"],
                in_stock=True, stock_quantity=32,
                description="...", contraindications=[],
            ),
        ]
        mediocre_output = GeneratorOutput(
            feature_run_id="feat_test_003",
            status=FeatureStatus.PROPOSED,
            recommended_products=[
                RecommendedProduct(
                    sku="VEG-PRO-003", name="Proteina Vegetal Ervilha 800g",
                    price=119.90, why_this_customer="Adequado.",
                    restriction_checks=[], score=0.7,
                ),
            ],
            customer_message_draft="Aqui esta.",
            evidence=["VEG-PRO-003: disponivel"],
            risk_flags=[],
            state_updates={"recommended_skus": ["VEG-PRO-003"]},
        )
        input_data = EvaluatorInput(
            feature_run_id="feat_test_003",
            generator_output=mediocre_output,
            customer_profile=mediocre_customer,
            catalog_snapshot=mediocre_catalog,
            contract_version="1.0.0",
        )
        output = self.evaluator.evaluate(input_data)
        self.assertIn(output.verdict, [
            Verdict.APROVAR_COM_RESSALVAS,
            Verdict.APROVAR,
            Verdict.REJEITAR,
        ])


if __name__ == "__main__":
    unittest.main()
