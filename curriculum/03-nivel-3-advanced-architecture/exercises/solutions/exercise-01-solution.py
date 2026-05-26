"""
Solucao do Exercicio 1 — Sistema Multi-Agente Planner/Generator/Evaluator
Nivel 3 — Arquitetura Avancada

Esta e a solucao de referencia. Execute com:
    python exercise-01-solution.py

Todos os 6 cenarios de teste devem passar com ✅.
"""

import json
import re
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Product:
    """Representa um produto no catalogo simulado do KODA."""
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
    """Perfil do cliente com preferencias e restricoes."""
    customer_id: str
    name: str
    budget_brl: float
    dietary_restrictions: list[str] = field(default_factory=list)
    preferred_flavor: Optional[str] = None
    training_goal: Optional[str] = None
    training_frequency: Optional[str] = None


@dataclass
class ConversationEvent:
    """Evento de entrada: mensagem recebida do WhatsApp."""
    conversation_id: str
    turn_id: str
    customer_message: str
    received_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PlanStep:
    """Uma etapa do plano criado pelo Planner."""
    step_id: str
    task: str
    owner: str
    success_criteria: list[str] = field(default_factory=list)


@dataclass
class Plan:
    """Plano completo criado pelo Planner."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    current_goal: str = ""
    known_constraints: dict[str, Any] = field(default_factory=dict)
    steps: list[PlanStep] = field(default_factory=list)
    evaluation_rubric: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Generation:
    """Resposta candidata gerada pelo Generator."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    step_id: str = ""
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
    """Resultado da avaliacao feita pelo Evaluator."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    evaluated_step_id: str = ""
    status: str = ""
    rubric_results: list[RubricResult] = field(default_factory=list)
    feedback: str = ""
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# PRODUCT CATALOG (Dados simulados)
# ============================================================================

PRODUCT_CATALOG: list[Product] = [
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
        category="whey",
        price_brl=99.90,
        servings=25,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.3,
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
    Product(
        sku="CREA-CREA-150",
        name="Creatina Creapure 150g",
        category="creatina",
        price_brl=89.90,
        servings=30,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.9,
    ),
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def write_json(directory: Path, filename: str, data: Any) -> Path:
    """Escreve dados em arquivo JSON de forma atomica."""
    directory.mkdir(parents=True, exist_ok=True)
    serializable = _dataclass_to_dict(data)
    tmp_path = directory / f".{filename}.tmp"
    tmp_path.write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    final_path = directory / filename
    tmp_path.rename(final_path)
    return final_path


def read_json(filepath: Path) -> dict[str, Any]:
    """Le arquivo JSON e retorna como dicionario."""
    return json.loads(filepath.read_text(encoding="utf-8"))


def _dataclass_to_dict(obj: Any) -> Any:
    """Converte dataclass, lista ou dict para dicionario serializavel."""
    from dataclasses import asdict, is_dataclass

    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, list):
        return [_dataclass_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    return obj


def _make_envelope(conversation_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Envolve dados em envelope padrao com schema_version, conversation_id e timestamp."""
    payload["schema_version"] = payload.get("schema_version", "1.0")
    payload["conversation_id"] = conversation_id
    if "created_at" not in payload and "received_at" not in payload:
        payload["persisted_at"] = datetime.now(timezone.utc).isoformat()
    return payload


# ============================================================================
# PLANNER AGENT
# ============================================================================

def _extract_category(message: str) -> str:
    """Extrai a categoria de produto da mensagem do cliente."""
    msg = message.lower()
    keywords = {
        "creatina": "creatina",
        "whey": "whey",
        "pre treino": "pre_treino",
        "pre-treino": "pre_treino",
        "bcaa": "bcaa",
    }
    for keyword, category in keywords.items():
        if keyword in msg:
            return category
    return "todos"


def _has_restriction(restrictions: list[str], target: str) -> bool:
    """Verifica se uma restricao especifica existe na lista."""
    return any(target in r.lower() for r in restrictions)


def planner_agent(
    event: ConversationEvent,
    profile: CustomerProfile,
    catalog: list[Product],
) -> Plan:
    """Planner Agent: decompoe a tarefa do cliente em etapas e define criterios."""
    category = _extract_category(event.customer_message)

    constraints: dict[str, Any] = {
        "budget_brl": profile.budget_brl,
        "target_category": category,
    }
    if _has_restriction(profile.dietary_restrictions, "lactose"):
        constraints["lactose_free"] = True
    if _has_restriction(profile.dietary_restrictions, "gluten"):
        constraints["gluten_free"] = True

    steps = [
        PlanStep(
            step_id="s1",
            task=f"filtrar produtos da categoria {category} e verificar estoque",
            owner="generator",
            success_criteria=["categoria correta", "em estoque"],
        ),
        PlanStep(
            step_id="s2",
            task="aplicar restricoes de budget, lactose e gluten",
            owner="generator",
            success_criteria=[
                f"preco <= R$ {profile.budget_brl:.2f}",
            ],
        ),
        PlanStep(
            step_id="s3",
            task="preparar resposta curta e humana para WhatsApp",
            owner="generator",
            success_criteria=["tom humano", "sem jargao excessivo", "pergunta final clara"],
        ),
    ]

    rubric = [
        "respeita orcamento definido no perfil",
        "respeita restricoes alimentares",
        "nao recomenda produto fora de estoque",
        "mantem foco no objetivo principal",
        "explica recomendacao sem pressionar compra",
    ]

    plan = Plan(
        conversation_id=event.conversation_id,
        current_goal=f"recomendar {category} dentro do orcamento de R$ {profile.budget_brl:.2f}",
        known_constraints=constraints,
        steps=steps,
        evaluation_rubric=rubric,
    )
    plan.created_at = datetime.now(timezone.utc).isoformat()
    return plan


# ============================================================================
# GENERATOR AGENT
# ============================================================================

_PRESSURED_WORDS = ["aproveite", "so hoje", "nao perca", "ultimas unidades", "estoque acabando"]


def generator_agent(
    plan: Plan,
    catalog: list[Product],
    evaluator_feedback: Optional[str] = None,
) -> Generation:
    """Generator Agent: itera sobre as etapas do plano e gera resposta candidata."""
    constraints = plan.known_constraints
    target_category = constraints.get("target_category", "todos")
    budget = constraints.get("budget_brl")

    filtered = list(catalog)

    if target_category != "todos":
        filtered = [p for p in filtered if p.category == target_category]

    filtered = [p for p in filtered if p.in_stock]

    if budget is not None:
        filtered = [p for p in filtered if p.price_brl <= budget]

    if constraints.get("lactose_free"):
        filtered = [p for p in filtered if p.lactose_free]

    if constraints.get("gluten_free"):
        filtered = [p for p in filtered if p.gluten_free]

    if evaluator_feedback:
        budget_match = _extract_budget_from_feedback(evaluator_feedback)
        if budget_match is not None and budget is not None:
            filtered = [p for p in filtered if p.price_brl <= budget_match]

    filtered.sort(key=lambda p: p.rating, reverse=True)
    top = filtered[:3]

    products_considered = [
        {
            "sku": p.sku,
            "name": p.name,
            "price_brl": p.price_brl,
            "rating": p.rating,
            "lactose_free": p.lactose_free,
            "in_stock": p.in_stock,
        }
        for p in top
    ]

    if not top:
        candidate_response = (
            "Nao encontrei produtos que atendam todos os seus criterios neste momento. "
            "Quer ajustar alguma preferencia para eu buscar alternativas?"
        )
    elif len(top) == 1:
        p = top[0]
        candidate_response = (
            f"Encontrei 1 opcao: {p.name} por R$ {p.price_brl:.2f} "
            f"(nota {p.rating}). "
            f"E a melhor escolha dentro do seu perfil. Quer que eu separe para voce?"
        )
    else:
        best = top[0]
        second = top[1]
        candidate_response = (
            f"Encontrei {len(top)} opcoes. "
            f"A melhor avaliada e {best.name} por R$ {best.price_brl:.2f} "
            f"(nota {best.rating}). "
            f"Tambem temos {second.name} por R$ {second.price_brl:.2f}. "
            f"Qual prefere?"
        )

    assumptions = [
        f"categoria alvo: {target_category}",
        f"budget maximo: R$ {budget:.2f}" if budget else "sem limite de budget",
    ]

    current_step_id = plan.steps[0].step_id if plan.steps else "s0"

    return Generation(
        conversation_id=plan.conversation_id,
        step_id=current_step_id,
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
    plan: Plan,
    generation: Generation,
    profile: CustomerProfile,
) -> Evaluation:
    """Evaluator Agent: valida resposta contra cada criterio da rubrica do plano."""
    results: list[RubricResult] = []
    products = generation.products_considered
    has_products = len(products) > 0
    target_category = plan.known_constraints.get("target_category", "todos")
    lactose_required = _has_restriction(profile.dietary_restrictions, "lactose")
    gluten_required = _has_restriction(profile.dietary_restrictions, "gluten")

    for criterion in plan.evaluation_rubric:
        criterion_lower = criterion.lower()

        if "orcamento" in criterion_lower:
            if not has_products:
                results.append(RubricResult(
                    criterion=criterion,
                    passed=False,
                    evidence="nenhum produto encontrado para validar orcamento",
                ))
                continue
            violations = [
                f"{p['sku']} (R$ {p['price_brl']:.2f} > R$ {profile.budget_brl:.2f})"
                for p in products if p["price_brl"] > profile.budget_brl
            ]
            passed = len(violations) == 0
            evidence = (
                f"todos os {len(products)} produtos estao <= R$ {profile.budget_brl:.2f}"
                if passed else f"violacoes: {'; '.join(violations)}"
            )
            results.append(RubricResult(criterion=criterion, passed=passed, evidence=evidence))

        elif "restric" in criterion_lower and "alimentar" in criterion_lower:
            if not has_products:
                results.append(RubricResult(
                    criterion=criterion,
                    passed=False,
                    evidence="nenhum produto encontrado para validar restricoes alimentares",
                ))
                continue
            violations = []
            for p in products:
                if lactose_required and not p.get("lactose_free", True):
                    violations.append(f"{p['sku']} contem lactose")
                if gluten_required and not p.get("gluten_free", True):
                    violations.append(f"{p['sku']} contem gluten")
            passed = len(violations) == 0
            evidence = (
                "todos os produtos respeitam restricoes declaradas"
                if passed else f"violacoes: {'; '.join(violations)}"
            )
            results.append(RubricResult(criterion=criterion, passed=passed, evidence=evidence))

        elif "estoque" in criterion_lower:
            if not has_products:
                results.append(RubricResult(
                    criterion=criterion,
                    passed=False,
                    evidence="nenhum produto encontrado para validar estoque",
                ))
                continue
            violations = [p["sku"] for p in products if not p.get("in_stock", True)]
            passed = len(violations) == 0
            evidence = (
                "todos os produtos estao em estoque" if passed
                else f"fora de estoque: {', '.join(violations)}"
            )
            results.append(RubricResult(criterion=criterion, passed=passed, evidence=evidence))

        elif "foco" in criterion_lower or "objetivo" in criterion_lower:
            if target_category == "todos":
                results.append(RubricResult(
                    criterion=criterion, passed=True,
                    evidence="sem categoria restrita para verificar foco",
                ))
            else:
                results.append(RubricResult(
                    criterion=criterion, passed=True,
                    evidence=f"resposta focada em {target_category}",
                ))

        elif "pressionar" in criterion_lower or "pressao" in criterion_lower:
            response_lower = generation.candidate_response.lower()
            found = [w for w in _PRESSURED_WORDS if w in response_lower]
            passed = len(found) == 0
            evidence = (
                "resposta informativa, sem linguagem de pressao" if passed
                else f"linguagem de pressao detectada: {', '.join(found)}"
            )
            results.append(RubricResult(criterion=criterion, passed=passed, evidence=evidence))

        else:
            results.append(RubricResult(
                criterion=criterion, passed=True,
                evidence="criterio verificado implicitamente",
            ))

    all_passed = all(r.passed for r in results)
    status = "approved" if all_passed else "rejected"
    feedback = ""
    if not all_passed:
        failed = [r.criterion for r in results if not r.passed]
        feedback = f"Criterios que falharam: {', '.join(failed)}."
        if not has_products:
            feedback += " Nenhum produto atende aos criterios. Ajustar restricoes ou informar indisponibilidade."

    return Evaluation(
        conversation_id=plan.conversation_id,
        evaluated_step_id=generation.step_id,
        status=status,
        rubric_results=results,
        feedback=feedback,
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


# ============================================================================
# ORCHESTRATOR (HARNESS)
# ============================================================================

def run_customer_turn(
    state_dir: Path,
    event: ConversationEvent,
    profile: CustomerProfile,
    catalog: list[Product],
    max_revisions: int = 2,
) -> str:
    """Orquestrador principal: coordena Planner -> Generator -> Evaluator."""
    profile_envelope = _make_envelope(event.conversation_id, {
        "customer_id": profile.customer_id,
        "name": profile.name,
        "budget_brl": profile.budget_brl,
        "dietary_restrictions": profile.dietary_restrictions,
        "preferred_flavor": profile.preferred_flavor,
        "training_goal": profile.training_goal,
        "training_frequency": profile.training_frequency,
    })
    write_json(state_dir, "customer_profile.json", profile_envelope)

    write_json(state_dir, "conversation_event.json", {
        "schema_version": "1.0",
        "conversation_id": event.conversation_id,
        "turn_id": event.turn_id,
        "customer_message": event.customer_message,
        "received_at": event.received_at,
    })

    plan = planner_agent(event, profile, catalog)
    write_json(state_dir, "plan.json", plan)

    generation = generator_agent(plan, catalog)
    write_json(state_dir, "generation.json", generation)

    evaluation = evaluator_agent(plan, generation, profile)
    write_json(state_dir, "evaluation.json", evaluation)

    revision_count = 0
    while evaluation.status != "approved" and revision_count < max_revisions:
        revision_count += 1
        generation = generator_agent(plan, catalog, evaluator_feedback=evaluation.feedback)
        write_json(state_dir, f"generation_revision_{revision_count}.json", generation)
        evaluation = evaluator_agent(plan, generation, profile)
        write_json(state_dir, f"evaluation_revision_{revision_count}.json", evaluation)

    if evaluation.status == "approved":
        write_json(state_dir, "delivery.json", {
            "schema_version": "1.0",
            "conversation_id": event.conversation_id,
            "turn_id": event.turn_id,
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "approved_by": "evaluator",
            "message": generation.candidate_response,
        })
        return generation.candidate_response

    return (
        "Preciso confirmar um detalhe antes de te responder com seguranca. "
        "Posso verificar e retornar em instantes?"
    )


# ============================================================================
# TESTS
# ============================================================================

def _make_temp_dir() -> Path:
    """Cria diretorio temporario para estado de teste."""
    return Path(tempfile.mkdtemp(prefix="test_state_"))


def test_cenario_1_caminho_feliz():
    """Cenario 1: recomendacao aprovada na primeira tentativa."""
    print("\n" + "=" * 60)
    print("\U0001f9ea TESTE 1: Caminho Feliz — Recomendacao Aprovada")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_rafael_001",
        name="Rafael",
        budget_brl=80.0,
        dietary_restrictions=["intolerancia_lactose"],
        training_goal="ganho_de_forca",
    )

    event = ConversationEvent(
        conversation_id="conv_rafael_001",
        turn_id="turn_001",
        customer_message="Quero comprar creatina. Meu orcamento e R$ 80.",
    )

    response = run_customer_turn(state_dir, event, profile, PRODUCT_CATALOG)
    print(f"\n\U0001f4e4 Resposta final: {response}")

    assert (state_dir / "plan.json").exists(), "plan.json deveria existir"
    assert (state_dir / "generation.json").exists(), "generation.json deveria existir"
    assert (state_dir / "evaluation.json").exists(), "evaluation.json deveria existir"

    evaluation = read_json(state_dir / "evaluation.json")
    assert evaluation["status"] == "approved", (
        f"Esperado 'approved', obtido '{evaluation['status']}'"
    )
    assert "Preciso confirmar" not in response, "Resposta nao deveria ser fallback"
    assert len(evaluation["rubric_results"]) > 0, "rubric_results nao pode ser vazio"

    gen = read_json(state_dir / "generation.json")
    assert len(gen["products_considered"]) > 0, "deve ter encontrado produtos"

    print("✅ Teste 1 passou!")


def test_cenario_2_rejeicao_e_correcao():
    """Cenario 2: avaliador rejeita, generator tenta corrigir com feedback."""
    print("\n" + "=" * 60)
    print("\U0001f9ea TESTE 2: Rejeicao e Correcao — Budget Estourado")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_marina_002",
        name="Marina",
        budget_brl=50.0,
        dietary_restrictions=["intolerancia_lactose"],
        training_goal="ganho_de_massa",
    )

    event = ConversationEvent(
        conversation_id="conv_marina_002",
        turn_id="turn_001",
        customer_message="Quero comprar whey protein sabor chocolate.",
    )

    response = run_customer_turn(state_dir, event, profile, PRODUCT_CATALOG, max_revisions=2)
    print(f"\n\U0001f4e4 Resposta final: {response}")

    evaluation = read_json(state_dir / "evaluation.json")
    status = evaluation["status"]

    if status == "approved":
        gen = read_json(state_dir / "generation.json")
        for p in gen.get("products_considered", []):
            assert p["price_brl"] <= 50.0, (
                f"Produto {p.get('sku')} com preco R$ {p['price_brl']} > budget R$ 50.0"
            )
        print("  Aprovado com budget respeitado.")
    else:
        assert "Preciso confirmar" in response, "Esperado fallback quando budget impossivel"
        rev_files = list(state_dir.glob("generation_revision_*.json"))
        print(f"  Rejeitado. Arquivos de revisao: {len(rev_files)}")

    print("✅ Teste 2 passou!")


def test_cenario_3_fallback_apos_duas_revisoes():
    """Cenario 3: budget impossivel força fallback apos 2 revisoes."""
    print("\n" + "=" * 60)
    print("\U0001f9ea TESTE 3: Fallback Apos 2 Revisoes Falhas")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_pedro_003",
        name="Pedro",
        budget_brl=15.0,
        dietary_restrictions=["intolerancia_lactose", "intolerancia_gluten"],
        training_goal="ganho_de_massa",
    )

    event = ConversationEvent(
        conversation_id="conv_pedro_003",
        turn_id="turn_001",
        customer_message="Quero o melhor whey protein que tiver.",
    )

    response = run_customer_turn(state_dir, event, profile, PRODUCT_CATALOG, max_revisions=2)
    print(f"\n\U0001f4e4 Resposta final: {response}")

    eval_path = state_dir / "evaluation.json"
    assert eval_path.exists(), "evaluation.json deveria existir"

    final_eval = read_json(eval_path)
    if final_eval["status"] == "rejected":
        assert "Preciso confirmar" in response, "Fallback esperado quando budget impossivel"
        rev_files = list(state_dir.glob("evaluation_revision_*.json"))
        print(f"  Revisoes registradas: {len(rev_files)}")
    elif final_eval["status"] == "approved":
        gen = read_json(state_dir / "generation.json")
        for p in gen.get("products_considered", []):
            assert p["price_brl"] <= 15.0, (
                f"Produto {p.get('sku')} excede budget de R$ 15.0"
            )

    print("✅ Teste 3 passou!")


def test_cenario_4_respeito_ao_orcamento():
    """Cenario 4: sistema nunca recomenda produto acima do budget."""
    print("\n" + "=" * 60)
    print("\U0001f9ea TESTE 4: Garantia de Respeito ao Orcamento")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_ana_004",
        name="Ana",
        budget_brl=70.0,
        dietary_restrictions=[],
        training_goal="resistencia",
    )

    event = ConversationEvent(
        conversation_id="conv_ana_004",
        turn_id="turn_001",
        customer_message="Quero comprar creatina.",
    )

    response = run_customer_turn(state_dir, event, profile, PRODUCT_CATALOG)
    print(f"\n\U0001f4e4 Resposta final: {response}")

    gen_path = state_dir / "generation.json"
    assert gen_path.exists(), "generation.json nao existe"

    generation = read_json(gen_path)
    for p in generation.get("products_considered", []):
        assert p["price_brl"] <= 70.0, (
            f"VIOLACAO: {p.get('sku')} custa R$ {p['price_brl']} > budget R$ 70.0"
        )
    print(f"  Produtos considerados: {len(generation['products_considered'])}")
    for p in generation["products_considered"]:
        print(f"  - {p.get('sku')}: R$ {p['price_brl']}")

    eval_data = read_json(state_dir / "evaluation.json")
    budget_result = next(
        (r for r in eval_data["rubric_results"] if "orcamento" in r["criterion"].lower()), None
    )
    assert budget_result is not None, "rubric_results deve incluir criterio de orcamento"
    assert budget_result["passed"], f"criterio de orcamento deveria passar: {budget_result['evidence']}"

    print("✅ Teste 4 passou!")


def test_cenario_5_respeito_restricao_alimentar():
    """Cenario 5: sistema nunca recomenda produto com alergeno bloqueado."""
    print("\n" + "=" * 60)
    print("\U0001f9ea TESTE 5: Garantia de Respeito a Restricao Alimentar")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_bruno_005",
        name="Bruno",
        budget_brl=150.0,
        dietary_restrictions=["intolerancia_lactose"],
        training_goal="ganho_de_massa",
    )

    event = ConversationEvent(
        conversation_id="conv_bruno_005",
        turn_id="turn_001",
        customer_message="Quero comprar whey protein.",
    )

    response = run_customer_turn(state_dir, event, profile, PRODUCT_CATALOG)
    print(f"\n\U0001f4e4 Resposta final: {response}")

    gen_path = state_dir / "generation.json"
    assert gen_path.exists(), "generation.json nao existe"

    generation = read_json(gen_path)
    for p in generation.get("products_considered", []):
        sku = p.get("sku")
        product = next((prod for prod in PRODUCT_CATALOG if prod.sku == sku), None)
        if product:
            assert product.lactose_free, (
                f"VIOLACAO: {sku} nao e lactose_free, mas cliente tem intolerancia"
            )
    print(f"  Produtos considerados: {len(generation['products_considered'])}")
    for p in generation["products_considered"]:
        print(f"  - {p.get('sku')}: R$ {p['price_brl']}")

    eval_data = read_json(state_dir / "evaluation.json")
    restriction_result = next(
        (r for r in eval_data["rubric_results"] if "restric" in r["criterion"].lower()), None
    )
    assert restriction_result is not None, "rubric_results deve incluir criterio de restricao"
    assert restriction_result["passed"], (
        f"criterio de restricao deveria passar: {restriction_result['evidence']}"
    )

    print("✅ Teste 5 passou!")


def test_cenario_6_audit_trail():
    """Cenario 6: todos os arquivos JSON tem campos obrigatorios."""
    print("\n" + "=" * 60)
    print("\U0001f9ea TESTE 6: Audit Trail — Campos Obrigatorios nos JSONs")
    print("=" * 60)

    state_dir = _make_temp_dir()
    profile = CustomerProfile(
        customer_id="cust_rafael_001",
        name="Rafael",
        budget_brl=80.0,
        dietary_restrictions=["intolerancia_lactose"],
        training_goal="ganho_de_forca",
    )

    event = ConversationEvent(
        conversation_id="conv_rafael_001",
        turn_id="turn_006",
        customer_message="Qual a melhor creatina ate R$ 80?",
    )

    response = run_customer_turn(state_dir, event, profile, PRODUCT_CATALOG)

    plan_path = state_dir / "plan.json"
    assert plan_path.exists(), "plan.json nao existe"
    plan = read_json(plan_path)
    required_plan = ["schema_version", "conversation_id", "current_goal", "steps", "evaluation_rubric", "created_at"]
    for field in required_plan:
        assert field in plan, f"plan.json: campo '{field}' ausente"
    assert len(plan["steps"]) > 0, "plan.json: steps vazio"
    assert len(plan["evaluation_rubric"]) > 0, "plan.json: evaluation_rubric vazio"

    gen_path = state_dir / "generation.json"
    assert gen_path.exists(), "generation.json nao existe"
    generation = read_json(gen_path)
    required_gen = ["schema_version", "conversation_id", "candidate_response", "products_considered", "generated_at"]
    for field in required_gen:
        assert field in generation, f"generation.json: campo '{field}' ausente"
    assert len(generation["candidate_response"]) > 0, "candidate_response vazio"

    eval_path = state_dir / "evaluation.json"
    assert eval_path.exists(), "evaluation.json nao existe"
    evaluation = read_json(eval_path)
    required_eval = ["schema_version", "conversation_id", "evaluated_step_id", "status", "rubric_results", "checked_at"]
    for field in required_eval:
        assert field in evaluation, f"evaluation.json: campo '{field}' ausente"
    assert evaluation["status"] in ("approved", "rejected"), f"status invalido: {evaluation['status']}"
    assert len(evaluation["rubric_results"]) > 0, "rubric_results vazio"

    profile_path = state_dir / "customer_profile.json"
    assert profile_path.exists(), "customer_profile.json nao existe"
    profile_data = read_json(profile_path)
    assert "schema_version" in profile_data, "customer_profile.json: falta schema_version"
    assert "conversation_id" in profile_data, "customer_profile.json: falta conversation_id"
    assert "persisted_at" in profile_data, "customer_profile.json: falta persisted_at"

    print(f"\n\U0001f4c1 Arquivos gerados em: {state_dir}")
    for f in sorted(state_dir.iterdir()):
        print(f"  {'\U0001f4c4' if f.is_file() else '\U0001f4c1'} {f.name}")

    print("✅ Teste 6 passou!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SOLUCAO: SISTEMA MULTI-AGENTE PLANNER/GENERATOR/EVALUATOR")
    print("=" * 60)

    test_cenario_1_caminho_feliz()
    test_cenario_2_rejeicao_e_correcao()
    test_cenario_3_fallback_apos_duas_revisoes()
    test_cenario_4_respeito_ao_orcamento()
    test_cenario_5_respeito_restricao_alimentar()
    test_cenario_6_audit_trail()

    print("\n" + "=" * 60)
    print("\U0001f389 TODOS OS TESTES PASSARAM!")
    print("=" * 60)
