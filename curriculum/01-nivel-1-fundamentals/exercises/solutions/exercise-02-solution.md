# 🧩 Solucao do Exercicio 02: Structured Output com Pydantic
## Validacao de JSON Schema, Regras de Negocio, Fallback Seguro e Auditoria para Recomendacoes KODA

**Tempo Estimado de Leitura:** 120-150 minutos  
**Nivel:** 1 - Fundamentals  
**Dificuldade:** ⭐⭐⭐ (Intermediaria-Avancada)  
**Pre-requisito:** Ter lido `03-basic-harness-patterns.md` e completado o Exercicio 01  
**Status:** 🟢 SOLUCAO COMPLETA COM CODIGO FUNCIONAL  
**Data de Criacao:** Maio 2026

---

## 📖 Prologo: A Recomendacao Que Parecia Boa, Mas Quebrou a Confiança

Fernando recebeu a mensagem as 21:17 de uma quinta-feira.

Marina, uma cliente antiga da KODA, tinha acabado de encerrar uma conversa de quase duas horas no WhatsApp. Ela tinha explicado que treinava quatro vezes por semana, que queria ganhar massa com controle de peso, que preferia chocolate, que tinha orcamento de R$ 150 e que precisava evitar qualquer coisa com amendoim.

O agente respondeu em texto livre:

```text
Marina, acho que o melhor para voce e o Vegan Protein Vanilla 500g. Ele e bem avaliado e combina com seu objetivo.
```

A resposta parecia humana. Parecia razoavel. Parecia ate cuidadosa.

Mas ela tinha tres problemas graves.

1. O produto estava sem estoque.
2. A resposta nao mostrava o `product_id`, entao o backend nao conseguia validar catalogo.
3. O agente nao informou a confianca nem os riscos, entao o time nao tinha como auditar a decisao.

Marina perguntou: "Mas tem mesmo disponivel?".

O agente respondeu: "Sim, pode comprar tranquila".

A frase era curta, mas o dano era grande. KODA tinha prometido estoque sem consultar estoque. Fernando abriu o trace e viu o root cause: o modelo gerou texto livre, e texto livre nao tinha contrato.

Na reuniao da manha seguinte, Fernando resumiu para o time:

> "Enquanto o agente puder responder qualquer coisa em qualquer formato, a gente nao tem um sistema. A gente tem uma aposta. KODA precisa falar em estrutura antes de falar com o cliente."

Este exercicio nasce dessa decisao.

A solucao nao e pedir para o modelo "ser mais cuidadoso". A solucao e obrigar o output a passar por um funil:

```text
texto bruto → JSON valido → Pydantic schema → regras de negocio → fallback seguro → audit log
```

Quando o modelo acerta, KODA envia uma recomendacao rastreavel.

Quando o modelo erra, KODA nao improvisa. KODA retorna um fallback seguro e deixa rastro para auditoria.

Essa e a diferenca entre um chatbot simpatico e um agente confiavel.

---

## 🎯 O Que o Exercicio Pede

O Exercicio 02 do Nivel 1 pede que voce construa um validador de recomendacoes estruturadas para o KODA.

A entrega tem quatro blocos principais.

1. Definir modelos Pydantic para representar recomendacao e alternativas.
2. Validar que a resposta bruta do modelo e JSON valido e segue o schema.
3. Validar regras de negocio que nao cabem apenas no schema.
4. Retornar recomendacao aprovada ou fallback seguro, sempre com auditoria.

### Requisitos Funcionais

| Requisito | Entrega nesta solucao | Por que importa no KODA |
|---|---|---|
| Definir `ProductRecommendation` | Modelo completo com campos obrigatorios, defaults e validadores | Backend recebe contrato fixo, nao texto livre |
| Definir `ProductAlternative` | Alternativas com `product_id`, nome opcional e justificativa | KODA pode mostrar trade-offs sem perder rastreabilidade |
| Validar JSON | `validate_json_format()` parseia e rejeita schema invalido | Evita que texto livre chegue ao checkout |
| Validar constraints | `validate_business_constraints()` checa catalogo, estoque, preco e preferencias | Evita venda errada, produto esgotado e budget violado |
| Gerar fallback | `get_fallback_recommendation()` sempre retorna objeto seguro | KODA nunca fica sem resposta estruturada |
| Logar decisao | `log_decision()` cria evento JSON em memoria e imprime registro estruturado | Permite auditoria e trace reading |
| Ativar testes | Todos os testes do starter code rodam no `run_all_tests()` | Prova comportamento no caminho feliz e nos erros |
| Bonus | Retry, penalidades, relatorio e historico estao incluidos | Mostra caminho realista para producao |

### Conexao com Nivel 1

| Conceito do Nivel 1 | Como aparece neste exercicio | Exemplo KODA |
|---|---|---|
| Context Amnesia | Preferencias antigas viram campos estruturados e historico validavel | Marina prefere chocolate e rejeitou um SKU antes |
| Token Budgeting | O output curto em JSON reduz ambiguidade e custo de interpretacao | Evaluator nao precisa reler 2 horas de conversa para achar `price` |
| Basic Harness Patterns | A validacao em camadas e um harness simples e deterministico | JSON Parser → Pydantic → Business Constraints → Fallback |
| Self-Evaluation Collapse | O modelo nao aprova a propria recomendacao | O validador rejeita mesmo que o texto pareca convincente |
| Trace Reading | Cada decisao vira evento de auditoria | Fernando consegue explicar por que `SKU-12346` foi rejeitado |

### Criterio de Sucesso

A solucao esta correta quando:

1. O codigo extraido do bloco Python roda com `python3 exercise-02-solution.py`.
2. Todos os testes passam.
3. JSON invalido retorna fallback, nao excecao para o usuario final.
4. Produto sem estoque e preco acima do budget sao rejeitados.
5. Confidence 100 e rejeitada porque nenhum modelo deve declarar certeza absoluta.
6. O documento explica o motivo de cada decisao em linguagem aplicavel ao KODA.

---

## 🏗️ Arquitetura da Solucao

A arquitetura e uma pipeline de validacao em camadas. Cada camada tem uma responsabilidade pequena e verificavel.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    STRUCTURED OUTPUT VALIDATION PIPELINE                     │
│                                                                              │
│  WhatsApp/Cliente                                                            │
│       │                                                                      │
│       ▼                                                                      │
│  ┌────────────────┐                                                          │
│  │ Raw response   │  Texto bruto gerado pelo modelo                          │
│  │ from model     │  Pode conter JSON correto, JSON quebrado ou texto livre   │
│  └───────┬────────┘                                                          │
│          │                                                                   │
│          ▼                                                                   │
│  ┌────────────────┐      falha       ┌─────────────────────┐                 │
│  │ JSON Parser    │ ───────────────► │ Fallback Handler    │                 │
│  │ json.loads()   │                  │ SKU seguro          │                 │
│  └───────┬────────┘                  └──────────┬──────────┘                 │
│          │ sucesso                              │                            │
│          ▼                                      │                            │
│  ┌────────────────────┐   falha      ┌──────────▼──────────┐                 │
│  │ Pydantic Validator │ ───────────► │ Audit Logger        │                 │
│  │ schema + types     │              │ rejeicao registrada │                 │
│  └─────────┬──────────┘              └──────────┬──────────┘                 │
│            │ sucesso                            │                            │
│            ▼                                    │                            │
│  ┌──────────────────────────────┐  falha        │                            │
│  │ Business Constraint Checker  │ ──────────────┘                            │
│  │ catalogo, estoque, budget    │                                           │
│  └──────────────┬───────────────┘                                           │
│                 │ sucesso                                                   │
│                 ▼                                                           │
│  ┌──────────────────────────────┐                                           │
│  │ Recommendation Approved      │                                           │
│  │ objeto estruturado seguro    │                                           │
│  └──────────────┬───────────────┘                                           │
│                 │                                                           │
│                 ▼                                                           │
│  ┌──────────────────────────────┐                                           │
│  │ Audit Logger                 │                                           │
│  │ entrada JSON com confidence  │                                           │
│  └──────────────┬───────────────┘                                           │
│                 │                                                           │
│                 ▼                                                           │
│  ┌──────────────────────────────┐                                           │
│  │ KODA State DB                │                                           │
│  │ trace consultavel pelo time  │                                           │
│  └──────────────────────────────┘                                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Fluxo Expandido

```text
WhatsApp/Cliente
  │
  │  "Quero whey ate R$ 150, sem amendoim, sabor chocolate"
  ▼
KODA Generator
  │
  │  Resposta bruta do modelo:
  │  {"product_id":"SKU-12345", "price":89.90, ...}
  ▼
JSON Parser
  │
  ├─ se nao for JSON: cria fallback + loga invalid_json
  │
  ▼
Pydantic Validator
  │
  ├─ product_id comeca com SKU?
  ├─ price > 0?
  ├─ reason tem conteudo suficiente?
  ├─ confidence esta entre 0 e 99?
  ├─ campos extras foram rejeitados?
  │
  ├─ se schema falhar: cria fallback + loga schema_validation_failed
  │
  ▼
Business Constraint Checker
  │
  ├─ SKU existe no catalogo?
  ├─ produto esta em estoque?
  ├─ preco bate com catalogo?
  ├─ preco cabe no budget?
  ├─ produto conflita com alergias?
  ├─ recomendacao contradiz historico?
  │
  ├─ se constraint falhar: confidence=0 + risk_flags + log de rejeicao
  │
  ▼
Fallback Handler
  │
  ├─ usado quando JSON ou schema falham completamente
  ├─ usa SKU-DEFAULT quando disponivel
  ├─ sempre retorna ProductRecommendation valida
  │
  ▼
Audit Logger
  │
  ├─ timestamp
  ├─ conversation_id
  ├─ client_id
  ├─ recommendation completa
  ├─ issues encontradas
  ├─ approved true/false
  │
  ▼
KODA State DB
  │
  └─ Fernando consegue reconstruir a decisao dias depois
```

### Por que Validacao em Camadas?

O schema Pydantic responde: "o formato esta correto?".

As regras de negocio respondem: "essa recomendacao pode ser enviada para esta cliente agora?".

Essas perguntas sao diferentes.

Um JSON pode estar perfeitamente valido e ainda assim recomendar produto sem estoque. Um produto pode existir no catalogo e ainda assim violar budget. Uma resposta pode ter confidence 92 e ainda contradizer uma preferencia que Marina informou no comeco da conversa.

Por isso a pipeline separa formato, contrato e negocio.

---

## 🧾 Formatos Estruturados

Structured output nao significa apenas JSON. JSON e a escolha desta solucao porque integra bem com backend, Pydantic e logs, mas o time KODA precisa entender o trade-off com outros formatos.

| Formato | Pros | Contras | Quando Usar | Aplicabilidade KODA |
|---|---|---|---|---|
| JSON | Nativo em APIs, facil de validar, compatibilidade excelente com Pydantic | Sensivel a virgulas e aspas, pouco amigavel para humanos em blocos longos | Contratos entre modelo, backend e evaluator | Principal formato para recomendacoes, carrinho, perfil e audit log |
| XML | Bom para documentos hierarquicos, tags explicitas, pode conter texto longo | Verboso, mais tokens, parsing menos comum em stacks modernas | Outputs com secoes textuais longas e estrutura aninhada | Util para prompts internos, menos ideal para checkout |
| Texto livre | Natural, facil para cliente, flexivel | Quase impossivel validar programaticamente, fraco para auditoria | Mensagem final ao cliente apos aprovacao | Nunca deve ser o contrato interno de recomendacao |
| YAML | Legivel para humanos, bom para configuracao | Indentacao fragil, parsers variam, risco de tipos ambiguos | Configuracoes de harness e exemplos de treinamento | Bom para docs e rubricas, nao para output operacional do modelo |

### Decisao da Solucao

Usamos JSON porque o KODA precisa de tres propriedades ao mesmo tempo:

1. Validacao deterministica.
2. Integracao direta com backend.
3. Audit trail simples de armazenar e comparar.

A mensagem final para Marina pode continuar humana. O contrato interno nao.

---

## 💻 Implementacao Completa

O bloco abaixo e autocontido. Se voce copiar para `exercise-02-solution.py` e executar com `python3 exercise-02-solution.py`, os testes rodam.

A solucao usa Pydantic quando ele esta instalado. Como ambientes educacionais as vezes nao tem a dependencia pronta, o arquivo tambem inclui um fallback minimo que permite executar os testes locais e entender o comportamento. Em producao, instale Pydantic e o caminho principal sera usado.

```python
from __future__ import annotations

import copy
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

try:
    from pydantic import BaseModel, Field, ValidationError, validator
    PYDANTIC_AVAILABLE = True
except ModuleNotFoundError:
    PYDANTIC_AVAILABLE = False

    class ValidationError(ValueError):
        ...

    class _Missing:
        ...

    MISSING = _Missing()

    class FieldInfo:
        def __init__(
            self,
            default: Any = MISSING,
            default_factory: Optional[Any] = None,
            gt: Optional[float] = None,
            ge: Optional[float] = None,
            le: Optional[float] = None,
            min_length: Optional[int] = None,
            description: str = "",
        ) -> None:
            self.default = default
            self.default_factory = default_factory
            self.gt = gt
            self.ge = ge
            self.le = le
            self.min_length = min_length
            self.description = description

    def Field(
        default: Any = MISSING,
        *,
        default_factory: Optional[Any] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        description: str = "",
    ) -> FieldInfo:
        if default is ...:
            default = MISSING
        return FieldInfo(default, default_factory, gt, ge, le, min_length, description)

    def validator(*field_names: str):
        def decorate(fn):
            fn._validator_fields = field_names
            return fn
        return decorate

    def _origin(tp: Any) -> Any:
        return getattr(tp, "__origin__", None)

    def _args(tp: Any) -> Tuple[Any, ...]:
        return getattr(tp, "__args__", ())

    def _coerce(value: Any, annotation: Any, field_name: str) -> Any:
        origin = _origin(annotation)
        args = _args(annotation)
        if origin is list or origin is List:
            if not isinstance(value, list):
                raise ValidationError(f"{field_name} deve ser uma lista")
            inner = args[0] if args else Any
            return [_coerce(item, inner, field_name) for item in value]
        if origin is dict or origin is Dict:
            if not isinstance(value, dict):
                raise ValidationError(f"{field_name} deve ser um objeto")
            return value
        if origin is Optional or (origin is getattr(__import__('typing'), 'Union') and type(None) in args):
            if value is None:
                return None
            non_none = [arg for arg in args if arg is not type(None)][0]
            return _coerce(value, non_none, field_name)
        if isinstance(annotation, str):
            return value
        if annotation is Any:
            return value
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            if isinstance(value, annotation):
                return value
            if isinstance(value, dict):
                return annotation(**value)
            raise ValidationError(f"{field_name} deve ser objeto {annotation.__name__}")
        if annotation is str:
            if not isinstance(value, str):
                raise ValidationError(f"{field_name} deve ser string")
            return value
        if annotation is int:
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValidationError(f"{field_name} deve ser inteiro")
            return value
        if annotation is float:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValidationError(f"{field_name} deve ser numero")
            return float(value)
        if annotation is bool:
            if not isinstance(value, bool):
                raise ValidationError(f"{field_name} deve ser booleano")
            return value
        return value

    class BaseModel:
        def __init__(self, **data: Any) -> None:
            annotations = getattr(self.__class__, "__annotations__", {})
            allow_extra = getattr(getattr(self.__class__, "Config", object), "extra", "ignore") != "forbid"
            extra = set(data) - set(annotations)
            if extra and not allow_extra:
                raise ValidationError(f"Campos extras nao permitidos: {sorted(extra)}")
            values: Dict[str, Any] = {}
            for field_name, annotation in annotations.items():
                field_def = getattr(self.__class__, field_name, MISSING)
                constraints = field_def if isinstance(field_def, FieldInfo) else None
                if field_name in data:
                    value = data[field_name]
                elif constraints and constraints.default_factory is not None:
                    value = constraints.default_factory()
                elif constraints and constraints.default is not MISSING:
                    value = copy.deepcopy(constraints.default)
                elif field_def is not MISSING and not callable(field_def) and not isinstance(field_def, FieldInfo):
                    value = copy.deepcopy(field_def)
                else:
                    raise ValidationError(f"Campo obrigatorio ausente: {field_name}")
                value = _coerce(value, annotation, field_name)
                if constraints:
                    if constraints.gt is not None and not value > constraints.gt:
                        raise ValidationError(f"{field_name} deve ser > {constraints.gt}")
                    if constraints.ge is not None and not value >= constraints.ge:
                        raise ValidationError(f"{field_name} deve ser >= {constraints.ge}")
                    if constraints.le is not None and not value <= constraints.le:
                        raise ValidationError(f"{field_name} deve ser <= {constraints.le}")
                    if constraints.min_length is not None and len(value) < constraints.min_length:
                        raise ValidationError(f"{field_name} deve ter pelo menos {constraints.min_length} caracteres")
                values[field_name] = value
            for attr_name in dir(self.__class__):
                fn = getattr(self.__class__, attr_name)
                fields = getattr(fn, "_validator_fields", ())
                for field_name in fields:
                    if field_name in values:
                        values[field_name] = fn(self.__class__, values[field_name])
            for field_name, value in values.items():
                setattr(self, field_name, value)

        def dict(self) -> Dict[str, Any]:
            result: Dict[str, Any] = {}
            for field_name in getattr(self.__class__, "__annotations__", {}):
                value = getattr(self, field_name)
                if isinstance(value, BaseModel):
                    result[field_name] = value.dict()
                elif isinstance(value, list):
                    result[field_name] = [item.dict() if isinstance(item, BaseModel) else item for item in value]
                else:
                    result[field_name] = value
            return result

        def model_dump(self) -> Dict[str, Any]:
            return self.dict()

        def copy(self, update: Optional[Dict[str, Any]] = None):
            data = self.dict()
            if update:
                data.update(update)
            return self.__class__(**data)


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class ProductAlternative(BaseModel):
    """Alternativa de produto enviada pelo modelo."""

    product_id: str
    product_name: Optional[str] = None
    reason: str

    @validator('product_id')
    def product_id_format(cls, value: str) -> str:
        if not value.startswith('SKU-'):
            raise ValueError("Product ID deve comecar com 'SKU-'")
        return value

    @validator('reason')
    def reason_has_content(cls, value: str) -> str:
        if len(value.strip()) < 8:
            raise ValueError("Reason da alternativa precisa explicar o trade-off")
        return value.strip()

    class Config:
        extra = "forbid"


class ProductRecommendation(BaseModel):
    """
    Schema estruturado para recomendacao de produto.

    Este objeto e o contrato entre o output bruto do modelo e o backend do KODA.
    """

    product_id: str = Field(..., description="ID unico do produto (SKU-XXXXX)")
    product_name: str = Field(..., description="Nome do produto")
    price: float = Field(..., gt=0, description="Preco em reais")
    reason: str = Field(..., min_length=10, description="Justificativa da recomendacao")
    confidence: int = Field(..., ge=0, le=100, description="Confianca 0-100")
    alternatives: List[ProductAlternative] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
    contradicts_previous_preferences: bool = Field(default=False)
    timestamp: Optional[str] = None
    source: str = Field(default="claude", description="Origem da recomendacao")

    @validator('confidence')
    def confidence_realistic(cls, value: int) -> int:
        if value == 100:
            raise ValueError("Confidence nunca deve ser 100%, use no maximo 99%")
        return value

    @validator('product_id')
    def product_id_format(cls, value: str) -> str:
        if not value.startswith('SKU-'):
            raise ValueError(f"Product ID deve comecar com 'SKU-', recebido: {value}")
        if value != 'SKU-DEFAULT' and not re.fullmatch(r"SKU-[0-9]{5}", value):
            raise ValueError("Product ID deve usar formato SKU-12345 ou SKU-DEFAULT")
        return value

    @validator('product_name')
    def product_name_meaningful(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("Product name muito curto")
        if cleaned.lower() in {"produto", "unknown", "n/a"}:
            raise ValueError("Product name generico demais")
        return cleaned

    @validator('reason')
    def reason_mentions_recommendation_logic(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned.split()) < 2:
            raise ValueError("Reason precisa ter explicacao legivel")
        return cleaned

    @validator('source')
    def source_is_known(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned not in {"claude", "fallback", "validator", "human_review"}:
            raise ValueError("Source precisa ser claude, fallback, validator ou human_review")
        return cleaned

    class Config:
        extra = "forbid"


def recommendation_to_dict(recommendation: ProductRecommendation) -> Dict[str, Any]:
    if hasattr(recommendation, "model_dump"):
        return recommendation.model_dump()
    return recommendation.dict()


def clone_recommendation(
    recommendation: ProductRecommendation,
    updates: Optional[Dict[str, Any]] = None,
) -> ProductRecommendation:
    payload = recommendation_to_dict(recommendation)
    if updates:
        payload.update(updates)
    return ProductRecommendation(**payload)


# ============================================================================
# VALIDADOR
# ============================================================================

class RecommendationValidator:
    """
    Valida recomendacoes contra schema, catalogo, restricoes de cliente e historico.
    """

    def __init__(
        self,
        available_products: List[Dict[str, Any]],
        client_constraints: Dict[str, Any],
        max_price: float = 10000.0,
    ) -> None:
        self.available_products = list(available_products)
        self.client_constraints = dict(client_constraints)
        self.max_price = float(max_price)
        self.product_index: Dict[str, Dict[str, Any]] = {
            product["id"]: product for product in self.available_products if "id" in product
        }
        self.audit_log: List[Dict[str, Any]] = []
        self.last_errors: List[str] = []
        self.client_id = self.client_constraints.get("client_id", "client_unknown")
        self.conversation_id = self.client_constraints.get("conversation_id", "conversation_unknown")

    def validate_json_format(self, response_text: str) -> Optional[ProductRecommendation]:
        self.last_errors = []
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as exc:
            self.last_errors.append(f"invalid_json:{exc.msg}")
            return None
        if not isinstance(data, dict):
            self.last_errors.append("json_root_not_object")
            return None
        try:
            recommendation = ProductRecommendation(**data)
        except (ValidationError, ValueError, TypeError) as exc:
            self.last_errors.append(f"schema_validation_failed:{exc}")
            return None
        if recommendation.timestamp is None:
            recommendation.timestamp = datetime.now(timezone.utc).isoformat()
        return recommendation

    def validate_business_constraints(
        self,
        recommendation: ProductRecommendation,
    ) -> Tuple[bool, List[str]]:
        violations: List[str] = []
        product = self.product_index.get(recommendation.product_id)
        if product is None:
            violations.append("product_not_in_catalog")
        else:
            if not product.get("in_stock", False):
                violations.append("product_out_of_stock")
            catalog_price = float(product.get("price", 0))
            if abs(catalog_price - recommendation.price) > 0.01:
                violations.append("price_mismatch_with_catalog")
            catalog_name = str(product.get("name", "")).strip().lower()
            if catalog_name and catalog_name != recommendation.product_name.strip().lower():
                violations.append("product_name_mismatch_with_catalog")
            blocked_allergens = set(self.client_constraints.get("allergies", []))
            product_allergens = set(product.get("allergens", []))
            if blocked_allergens.intersection(product_allergens):
                violations.append("allergy_conflict")
            blocked_restrictions = set(self.client_constraints.get("restrictions", []))
            product_restrictions = set(product.get("contains", []))
            if blocked_restrictions.intersection(product_restrictions):
                violations.append("dietary_restriction_conflict")
        budget_max = self.client_constraints.get("budget_max")
        if budget_max is not None and recommendation.price > float(budget_max):
            violations.append("exceeds_budget")
        if recommendation.price > self.max_price:
            violations.append("exceeds_system_max_price")
        if recommendation.contradicts_previous_preferences:
            violations.append("contradicts_previous_preferences")
        for alternative in recommendation.alternatives:
            if alternative.product_id not in self.product_index:
                violations.append(f"alternative_not_in_catalog:{alternative.product_id}")
            elif not self.product_index[alternative.product_id].get("in_stock", False):
                violations.append(f"alternative_out_of_stock:{alternative.product_id}")
        return len(violations) == 0, violations

    def validate_complete(
        self,
        response_text: str,
        previous_preferences: Optional[Dict[str, Any]] = None,
    ) -> Tuple[ProductRecommendation, List[str]]:
        issues: List[str] = []
        recommendation = self.validate_json_format(response_text)
        if recommendation is None:
            issues.extend(self.last_errors or ["invalid_json_or_schema"])
            fallback = self.get_fallback_recommendation()
            self.log_decision(fallback, self.client_id, issues, approved=False)
            return fallback, issues
        if previous_preferences:
            history_ok = self.validate_against_history(recommendation, [previous_preferences])
            if not history_ok:
                issues.append("history_contradiction")
        valid_business, business_violations = self.validate_business_constraints(recommendation)
        issues.extend(business_violations)
        if issues:
            recommendation = clone_recommendation(
                recommendation,
                {
                    "confidence": 0,
                    "risk_flags": sorted(set(recommendation.risk_flags + issues)),
                },
            )
            approved = False
        else:
            recommendation = self.apply_risk_penalties(recommendation)
            approved = recommendation.confidence > 0
        self.log_decision(recommendation, self.client_id, issues, approved=approved)
        return recommendation, issues

    def get_fallback_recommendation(self) -> ProductRecommendation:
        product = self.product_index.get("SKU-DEFAULT")
        if product is None:
            in_stock_products = [p for p in self.available_products if p.get("in_stock", False)]
            product = in_stock_products[0] if in_stock_products else {
                "id": "SKU-DEFAULT",
                "name": "Our Top Recommendation (System Default)",
                "price": 0.01,
            }
        return ProductRecommendation(
            product_id=str(product.get("id", "SKU-DEFAULT")),
            product_name=str(product.get("name", "Our Top Recommendation (System Default)")),
            price=float(product.get("price", 0.01)),
            reason="Fallback seguro usado porque a recomendacao original nao passou na validacao",
            confidence=0,
            alternatives=[],
            risk_flags=["fallback_response"],
            contradicts_previous_preferences=False,
            timestamp=datetime.now(timezone.utc).isoformat(),
            source="fallback",
        )

    def log_decision(
        self,
        recommendation: ProductRecommendation,
        client_id: str,
        issues: List[str],
        approved: bool,
    ) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "conversation_id": self.conversation_id,
            "client_id": client_id,
            "recommendation": recommendation_to_dict(recommendation),
            "issues": list(issues),
            "approved": bool(approved),
            "confidence": recommendation.confidence,
        }
        self.audit_log.append(entry)
        print(json.dumps(entry, ensure_ascii=False, sort_keys=True))

    def validate_with_retry(
        self,
        model_response: str,
        max_retries: int = 3,
    ) -> ProductRecommendation:
        attempts = [model_response]
        extracted = self._extract_first_json_object(model_response)
        if extracted and extracted != model_response:
            attempts.append(extracted)
        repaired = self._repair_common_json_errors(extracted or model_response)
        if repaired not in attempts:
            attempts.append(repaired)
        while len(attempts) < max_retries:
            attempts.append(attempts[-1])
        all_issues: List[str] = []
        for attempt in attempts[:max_retries]:
            recommendation, issues = self.validate_complete(attempt)
            all_issues.extend(issues)
            if not issues:
                return recommendation
        fallback = self.get_fallback_recommendation()
        self.log_decision(fallback, self.client_id, all_issues or ["retry_exhausted"], approved=False)
        return fallback

    def apply_risk_penalties(self, recommendation: ProductRecommendation) -> ProductRecommendation:
        penalties = {
            "premium_price_for_budget": 15,
            "high_price_alert": 20,
            "low_catalog_match": 25,
            "new_customer_uncertainty": 10,
            "weak_reasoning": 10,
        }
        total_penalty = sum(penalties.get(flag, 5) for flag in recommendation.risk_flags)
        adjusted = max(0, recommendation.confidence - total_penalty)
        return clone_recommendation(recommendation, {"confidence": adjusted})

    def generate_audit_report(self, conversation_id: str) -> str:
        entries = [entry for entry in self.audit_log if entry["conversation_id"] == conversation_id]
        if not entries:
            entries = list(self.audit_log)
        approved = sum(1 for entry in entries if entry["approved"])
        rejected = len(entries) - approved
        fallback_count = sum(
            1 for entry in entries
            if entry["recommendation"].get("source") == "fallback"
        )
        lines = [
            f"# Relatorio de Auditoria KODA - {conversation_id}",
            "",
            f"Total de decisoes: {len(entries)}",
            f"Aprovadas: {approved}",
            f"Rejeitadas: {rejected}",
            f"Fallbacks: {fallback_count}",
            "",
            "## Eventos",
        ]
        for index, entry in enumerate(entries, start=1):
            rec = entry["recommendation"]
            lines.extend([
                f"{index}. Produto: {rec['product_id']} - {rec['product_name']}",
                f"   Status: {'aprovada' if entry['approved'] else 'rejeitada'}",
                f"   Confidence: {entry['confidence']}",
                f"   Issues: {', '.join(entry['issues']) if entry['issues'] else 'nenhuma'}",
            ])
        return "\n".join(lines)

    def validate_against_history(
        self,
        recommendation: ProductRecommendation,
        client_history: List[Dict[str, Any]],
    ) -> bool:
        if recommendation.contradicts_previous_preferences:
            return False
        product = self.product_index.get(recommendation.product_id, {})
        for event in client_history:
            rejected_ids = set(event.get("rejected_product_ids", []))
            if recommendation.product_id in rejected_ids:
                return False
            avoided_categories = set(event.get("avoid_categories", []))
            if product.get("category") in avoided_categories:
                return False
            allergies = set(event.get("allergies", []))
            allergens = set(product.get("allergens", []))
            if allergies.intersection(allergens):
                return False
            required_flavor = event.get("preferred_flavor") or event.get("flavor")
            if required_flavor:
                text = f"{recommendation.product_name} {recommendation.reason}".lower()
                if required_flavor.lower() not in text and event.get("strict_flavor", False):
                    return False
        return True

    @staticmethod
    def _extract_first_json_object(text: str) -> Optional[str]:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        return text[start:end + 1]

    @staticmethod
    def _repair_common_json_errors(text: str) -> str:
        repaired = text.strip()
        repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
        if "'" in repaired and '"' not in repaired:
            repaired = repaired.replace("'", '"')
        return repaired


# ============================================================================
# TESTES
# ============================================================================

def create_test_data() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    available_products = [
        {
            "id": "SKU-12345",
            "name": "Whey Protein Chocolate 1kg",
            "price": 89.90,
            "in_stock": True,
            "category": "supplements",
            "allergens": [],
            "contains": [],
        },
        {
            "id": "SKU-12346",
            "name": "Vegan Protein Vanilla 500g",
            "price": 120.00,
            "in_stock": False,
            "category": "supplements",
            "allergens": [],
            "contains": [],
        },
        {
            "id": "SKU-DEFAULT",
            "name": "Our Top Recommendation (System Default)",
            "price": 99.90,
            "in_stock": True,
            "category": "supplements",
            "allergens": [],
            "contains": [],
        },
    ]
    client_constraints = {
        "client_id": "client_marina_001",
        "conversation_id": "wa_marina_structured_output",
        "budget_min": 50.0,
        "budget_max": 150.0,
        "restrictions": ["gluten"],
        "allergies": ["peanuts"],
    }
    return available_products, client_constraints


def test_valid_recommendation() -> None:
    print("\nTeste 1: recomendacao valida")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    valid_json = json.dumps({
        "product_id": "SKU-12345",
        "product_name": "Whey Protein Chocolate 1kg",
        "price": 89.90,
        "reason": "Matches chocolate preference, in stock, within budget",
        "confidence": 92,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False,
    })
    recommendation, issues = validator_instance.validate_complete(valid_json)
    assert recommendation.product_id == "SKU-12345"
    assert len(issues) == 0
    assert recommendation.confidence == 92
    print("Teste 1 passou")


def test_invalid_json() -> None:
    print("\nTeste 2: JSON invalido")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    invalid_json = "isso nao e JSON valido {]"
    recommendation, issues = validator_instance.validate_complete(invalid_json)
    assert recommendation.product_id == "SKU-DEFAULT"
    assert recommendation.confidence == 0
    assert len(issues) > 0
    print("Teste 2 passou")


def test_out_of_stock() -> None:
    print("\nTeste 3: produto sem estoque")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    json_out_of_stock = json.dumps({
        "product_id": "SKU-12346",
        "product_name": "Vegan Protein Vanilla 500g",
        "price": 120.00,
        "reason": "Vegan option with adequate protein profile",
        "confidence": 85,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False,
    })
    recommendation, issues = validator_instance.validate_complete(json_out_of_stock)
    assert "product_out_of_stock" in str(issues)
    assert recommendation.confidence < 85
    print("Teste 3 passou")


def test_exceeds_budget() -> None:
    print("\nTeste 4: preco acima do budget")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    json_exceeds = json.dumps({
        "product_id": "SKU-99999",
        "product_name": "Premium Supplement",
        "price": 200.00,
        "reason": "Premium option for advanced training routine",
        "confidence": 80,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False,
    })
    recommendation, issues = validator_instance.validate_complete(json_exceeds)
    assert "exceeds_budget" in str(issues) or "budget" in str(issues).lower()
    assert recommendation.confidence == 0
    print("Teste 4 passou")


def test_invalid_schema_field() -> None:
    print("\nTeste 5: schema invalido")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    json_invalid_schema = json.dumps({
        "product_id": "SKU-12345",
        "product_name": "Whey Protein",
        "price": 89.90,
        "confidence": 92,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False,
    })
    recommendation, issues = validator_instance.validate_complete(json_invalid_schema)
    assert recommendation.product_id == "SKU-DEFAULT" or recommendation.confidence == 0
    assert len(issues) > 0
    print("Teste 5 passou")


def test_confidence_validation() -> None:
    print("\nTeste 6: confidence 100 rejeitada")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    json_100_confidence = json.dumps({
        "product_id": "SKU-12345",
        "product_name": "Whey Protein Chocolate 1kg",
        "price": 89.90,
        "reason": "Good product for the stated customer goal",
        "confidence": 100,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False,
    })
    recommendation, issues = validator_instance.validate_complete(json_100_confidence)
    assert recommendation.confidence < 100
    assert len(issues) > 0
    print("Teste 6 passou")


def test_bonus_retry_and_audit_report() -> None:
    print("\nTeste 7: bonus retry e relatorio")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    wrapped_json = "Resposta do modelo:\n" + json.dumps({
        "product_id": "SKU-12345",
        "product_name": "Whey Protein Chocolate 1kg",
        "price": 89.90,
        "reason": "Chocolate product in stock and inside customer budget",
        "confidence": 91,
        "alternatives": [],
        "risk_flags": ["new_customer_uncertainty"],
        "contradicts_previous_preferences": False,
    })
    recommendation = validator_instance.validate_with_retry(wrapped_json)
    assert recommendation.product_id == "SKU-12345"
    assert recommendation.confidence == 81
    report = validator_instance.generate_audit_report("wa_marina_structured_output")
    assert "Total de decisoes" in report
    assert "SKU-12345" in report
    print("Teste 7 passou")


def test_bonus_history_validation() -> None:
    print("\nTeste 8: bonus historico")
    products, constraints = create_test_data()
    validator_instance = RecommendationValidator(products, constraints)
    recommendation = ProductRecommendation(
        product_id="SKU-12345",
        product_name="Whey Protein Chocolate 1kg",
        price=89.90,
        reason="Chocolate option that matches the customer flavor preference",
        confidence=90,
        alternatives=[],
        risk_flags=[],
        contradicts_previous_preferences=False,
    )
    assert validator_instance.validate_against_history(recommendation, [{"preferred_flavor": "chocolate", "strict_flavor": True}])
    assert not validator_instance.validate_against_history(recommendation, [{"rejected_product_ids": ["SKU-12345"]}])
    print("Teste 8 passou")


def run_all_tests() -> None:
    print("=" * 72)
    print("EXERCICIO 02: STRUCTURED OUTPUT COM PYDANTIC")
    print(f"Pydantic disponivel: {PYDANTIC_AVAILABLE}")
    print("=" * 72)
    test_valid_recommendation()
    test_invalid_json()
    test_out_of_stock()
    test_exceeds_budget()
    test_invalid_schema_field()
    test_confidence_validation()
    test_bonus_retry_and_audit_report()
    test_bonus_history_validation()
    print("\nTodos os testes passaram")


if __name__ == "__main__":
    run_all_tests()
```

### Decisoes de Design no Codigo

1. **`extra = "forbid"` nos modelos:** qualquer campo que o modelo inventar e rejeitado. Isso protege o backend contra drift silencioso.
2. **`confidence == 100` e invalido:** em recomendacao de saude, suplemento e ecommerce, certeza absoluta e um cheiro ruim. O maximo realista e 99.
3. **`product_id` segue formato `SKU-12345`:** integracao com catalogo precisa de chave estavel. Nome de produto sozinho nao e suficiente.
4. **Business constraints ficam fora do Pydantic:** estoque, budget e catalogo mudam por cliente e por momento. Schema valida formato; negocio valida contexto.
5. **Fallback retorna objeto valido:** o restante do sistema nao precisa lidar com `None`. O contrato e sempre `ProductRecommendation`.
6. **Audit log e estruturado:** toda decisao tem timestamp, cliente, recomendacao, issues, status e confidence.
7. **Bonus integrado sem dependencias externas:** retry, penalidade, relatorio e historico funcionam com dados locais.

---

## 🧪 Como Ler os Testes

Os testes nao existem apenas para deixar o terminal verde. Eles documentam o contrato operacional do KODA.

| Teste | Cenario | Propriedade garantida |
|---|---|---|
| `test_valid_recommendation` | JSON correto, SKU em estoque, preco no budget | Caminho feliz preserva confidence |
| `test_invalid_json` | Texto livre ou JSON quebrado | Sistema retorna fallback e registra issue |
| `test_out_of_stock` | SKU existe, mas esta sem estoque | Recomendacao e rejeitada e confidence vai a zero |
| `test_exceeds_budget` | Produto acima do budget | Budget do cliente vence a criatividade do modelo |
| `test_invalid_schema_field` | Campo obrigatorio ausente | Pydantic bloqueia contrato incompleto |
| `test_confidence_validation` | Modelo declara 100% | Certeza absoluta e rejeitada |
| `test_bonus_retry_and_audit_report` | Resposta com texto ao redor do JSON | Retry extrai JSON e gera relatorio |
| `test_bonus_history_validation` | Cliente ja rejeitou SKU antes | Historico bloqueia contradicao |

### Saida Esperada

```text
========================================================================
EXERCICIO 02: STRUCTURED OUTPUT COM PYDANTIC
Pydantic disponivel: True ou False
========================================================================
Teste 1 passou
Teste 2 passou
Teste 3 passou
Teste 4 passou
Teste 5 passou
Teste 6 passou
Teste 7 passou
Teste 8 passou
Todos os testes passaram
```

---

## 🧬 Aplicacao no KODA

Structured output no KODA aparece em todos os pontos em que uma resposta do modelo precisa virar acao operacional.

### Caso 1: Recomendacao de Produto

Antes:

```text
Marina, recomendo o Whey Protein Chocolate porque combina com seu treino e esta num preco bom.
```

Depois:

```json
{
  "product_id": "SKU-12345",
  "product_name": "Whey Protein Chocolate 1kg",
  "price": 89.9,
  "reason": "Matches chocolate preference, in stock, within budget",
  "confidence": 92,
  "alternatives": [],
  "risk_flags": [],
  "contradicts_previous_preferences": false
}
```

Impacto:

- Backend valida `SKU-12345`.
- Estoque e conferido antes da mensagem final.
- Budget de Marina e respeitado.
- Fernando consegue auditar por que a recomendacao passou.

### Caso 2: Validacao de Pedido

Antes:

```text
Seu pedido esta pronto: whey, creatina e BCAA. Total deve ficar uns R$ 220.
```

Problema: "uns R$ 220" nao e total de checkout.

Depois:

```json
{
  "cart_id": "cart_wa_marina_001",
  "items": [
    {"sku": "SKU-12345", "qty": 1, "unit_price": 89.90},
    {"sku": "SKU-33333", "qty": 1, "unit_price": 79.90}
  ],
  "subtotal": 169.80,
  "shipping": 12.90,
  "total": 182.70,
  "requires_human_review": false
}
```

Impacto:

- Carrinho pode ser recalculado.
- Frete e separado de subtotal.
- Divergencia de preco vira erro antes do pagamento.

### Caso 3: Extracao de Perfil do Cliente

Antes:

```text
A Marina gosta de chocolate, treina bastante e parece nao gostar de lactose.
```

Depois:

```json
{
  "customer_id": "cust_marina_001",
  "preferred_flavors": ["chocolate"],
  "training_goal": "ganho_de_massa",
  "dietary_restrictions": ["lactose"],
  "budget_max": 150.0,
  "confidence": 88
}
```

Impacto:

- Restricao alimentar sai do historico textual e vira estado persistido.
- Proximas recomendacoes nao dependem da memoria do modelo.
- Nivel 1 resolve Context Amnesia com estrutura.

### Caso 4: Mensagem Final ao Cliente

Structured output nao significa que Marina recebe JSON.

O fluxo correto e:

```text
1. Modelo gera JSON estruturado.
2. Validator aprova.
3. Formatter transforma em mensagem humana.
4. WhatsApp recebe texto curto e claro.
```

Mensagem final:

```text
Marina, eu iria no Whey Protein Chocolate 1kg. Ele esta dentro do seu orcamento, esta em estoque e combina com sua preferencia por chocolate. Posso confirmar o carrinho?
```

A humanidade fica na borda. A estrutura fica no miolo.

---

## 📊 Antes e Depois no Trace

### Trace Sem Structured Output

```text
21:17:04 model_output="Recomendo o Vegan Protein Vanilla..."
21:17:05 backend_parse=skipped
21:17:05 stock_check=skipped
21:17:06 message_sent=true
21:19:41 customer_complaint="Nao tem estoque?"
21:20:12 root_cause="free_text_not_validated"
```

### Trace Com Structured Output

```text
21:17:04 raw_response={...}
21:17:04 json_parser=passed
21:17:04 pydantic_schema=passed
21:17:04 product_id=SKU-12346
21:17:04 business_constraints=failed
21:17:04 issues=["product_out_of_stock"]
21:17:04 confidence=0
21:17:04 approved=false
21:17:04 fallback=SKU-DEFAULT
21:17:05 message_sent="Quero confirmar uma opcao segura antes de fechar."
```

O segundo trace e mais longo, mas e muito mais facil de debugar.

---

## 🧠 O Que Voce Aprendeu

| Area | Voce agora consegue | Evidencia na solucao |
|---|---|---|
| Pydantic | Definir modelos com campos obrigatorios, defaults e validadores | `ProductRecommendation` e `ProductAlternative` |
| JSON parsing | Separar erro de JSON de erro de schema | `validate_json_format()` |
| Regras de negocio | Validar catalogo, estoque, budget e historico | `validate_business_constraints()` |
| Fallback seguro | Retornar recomendacao estruturada mesmo em falha | `get_fallback_recommendation()` |
| Auditoria | Registrar cada decisao em JSON | `log_decision()` |
| Confidence | Preservar confidence quando aprovado e zerar quando rejeitado | `validate_complete()` |
| Retry | Extrair JSON de resposta imperfeita | `validate_with_retry()` |
| Penalidade | Reduzir confidence por risk flags | `apply_risk_penalties()` |
| Relatorio | Resumir decisoes aprovadas e rejeitadas | `generate_audit_report()` |
| Historico | Bloquear contradicao com preferencias antigas | `validate_against_history()` |

### Checklist de Dominio

- [x] Sei explicar por que texto livre e perigoso para recomendacoes.
- [x] Sei desenhar a pipeline JSON Parser → Pydantic → Constraints → Fallback → Audit.
- [x] Sei diferenciar validacao de formato e validacao de negocio.
- [x] Sei por que confidence 100 e rejeitada.
- [x] Sei como structured output reduz Context Amnesia.
- [x] Sei como structured output ajuda Token Budgeting.
- [x] Sei como structured output vira Basic Harness Pattern.
- [x] Sei como usar audit logs para explicar uma rejeicao.
- [x] Sei adaptar a solucao para outros objetos do KODA, como carrinho e perfil.

---

## 🔗 Conexao com Proximos Niveis

No Nivel 1, voce aprendeu a proteger uma recomendacao com estrutura e validacao local.

No Nivel 2, voce vai separar ainda mais responsabilidades:

| Nivel | O que muda | Como esta solucao prepara o caminho |
|---|---|---|
| Nivel 2 - Generator/Evaluator | Um componente gera e outro avalia | `RecommendationValidator` ja atua como avaliador deterministico |
| Nivel 2 - Sprint Contracts | Cada etapa tem contrato explicito | `ProductRecommendation` e um contrato de sprint pequeno |
| Nivel 2 - Rubric Design | Avaliacao fica declarativa | `validate_business_constraints()` pode virar rubrica configuravel |
| Nivel 2 - Trace Reading | Logs viram ferramenta de debug | `audit_log` ja mostra decisions e issues |
| Nivel 3 - State Persistence | Decisoes sobrevivem a crash | `log_decision()` pode gravar em SQLite ou arquivo JSONL |
| Nivel 3 - Multi-Agent | Planner, Generator e Evaluator se comunicam por artefatos | O JSON validado vira artefato entre agentes |

A ideia central continua a mesma: agentes longos nao ficam confiaveis por vontade. Eles ficam confiaveis por arquitetura.

---

## 📚 Apêndice A: Catalogo Mental de Falhas KODA

Este apendice transforma a solucao em repertorio. Cada caso abaixo e um mini-trace que um engenheiro pode usar para reconhecer erros em producao.

### Caso 001: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 90, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 002: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 100, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 003: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 110, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 004: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 120, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 005: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 130, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 006: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 140, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=76`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 007: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 150, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=77`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 008: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 160, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=78`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 009: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 80, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=79`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 010: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 90, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=80`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 011: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 100, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=81`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 012: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 110, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=82`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 013: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 120, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=83`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 014: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 130, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=84`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 015: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 140, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=85`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 016: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 150, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=86`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 017: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 160, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=87`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 018: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 80, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=88`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 019: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 90, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=89`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 020: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 100, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=90`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 021: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 110, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=91`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 022: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 120, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=92`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 023: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 130, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=93`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 024: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 140, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=94`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 025: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 150, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=70`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 026: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 160, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 027: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 80, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 028: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 90, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 029: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 100, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 030: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 110, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 031: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 120, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=76`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 032: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 130, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=77`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 033: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 140, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=78`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 034: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 150, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=79`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 035: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 160, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=80`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 036: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 80, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=81`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 037: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 90, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=82`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 038: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 100, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=83`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 039: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 110, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=84`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 040: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 120, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=85`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 041: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 130, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=86`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 042: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 140, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=87`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 043: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 150, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=88`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 044: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 160, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=89`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 045: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 80, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=90`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 046: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 90, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=91`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 047: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 100, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=92`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 048: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 110, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=93`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 049: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 120, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=94`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 050: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 130, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=70`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 051: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 140, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 052: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 150, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 053: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 160, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 054: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 80, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 055: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 90, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 056: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 100, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=76`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 057: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 110, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=77`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 058: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 120, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=78`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 059: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 130, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=79`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 060: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 140, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=80`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 061: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 150, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=81`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 062: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 160, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=82`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 063: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 80, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=83`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 064: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 90, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=84`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 065: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 100, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=85`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 066: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 110, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=86`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 067: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 120, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=87`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 068: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 130, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=88`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 069: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 140, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=89`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 070: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 150, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=90`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 071: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 160, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=91`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 072: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 80, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=92`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 073: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 90, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=93`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 074: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 100, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=94`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 075: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 110, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=70`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 076: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 120, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 077: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 130, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 078: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 140, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 079: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 150, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 080: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 160, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 081: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 80, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=76`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 082: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 90, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=77`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 083: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 100, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=78`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 084: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 110, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=79`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 085: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 120, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=80`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 086: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 130, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=81`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 087: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 140, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=82`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 088: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 150, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=83`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 089: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 160, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=84`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 090: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 80, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=85`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 091: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 90, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=86`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 092: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 100, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=87`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 093: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 110, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=88`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 094: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 120, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=89`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 095: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 130, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=90`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 096: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 140, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=91`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 097: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 150, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=92`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 098: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 160, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=93`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 099: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 80, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=94`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 100: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 90, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=70`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 101: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 100, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 102: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 110, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 103: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 120, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 104: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 130, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 105: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 140, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 106: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 150, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=76`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 107: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 160, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=77`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 108: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 80, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=78`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 109: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 90, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=79`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 110: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 100, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=80`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 111: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 110, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=81`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 112: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 120, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=82`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 113: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 130, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=83`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 114: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 140, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=84`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 115: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 150, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=85`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 116: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 160, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=86`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 117: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 80, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=87`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 118: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 90, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=88`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 119: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 100, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=89`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 120: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 110, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=90`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 121: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 120, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=91`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 122: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 130, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=92`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 123: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 140, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=93`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 124: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 150, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=94`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 125: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 160, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=70`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 126: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 80, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 127: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 90, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 128: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 100, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 129: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 110, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 130: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 120, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 131: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 130, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=76`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 132: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 140, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=77`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 133: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 150, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=78`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 134: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 160, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=79`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 135: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 80, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=80`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 136: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 90, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=81`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 137: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 100, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=82`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 138: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 110, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=83`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 139: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 120, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=84`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 140: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 130, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=85`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 141: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 140, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=86`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 142: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 150, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=87`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 143: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 160, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=88`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 144: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 80, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=89`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 145: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 90, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=90`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 146: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 100, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=91`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 147: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 110, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=92`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 148: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 120, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=93`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 149: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 130, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=94`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 150: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 140, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=70`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 151: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 150, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 152: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 160, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 153: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 80, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 154: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 90, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 155: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 100, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 156: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 110, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=76`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 157: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 120, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=77`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 158: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 130, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=78`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 159: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 140, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=79`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 160: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 150, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=80`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 161: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 160, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=81`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 162: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 80, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=82`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 163: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 90, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=83`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 164: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 100, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=84`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 165: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 110, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=85`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 166: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 120, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=86`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 167: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 130, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=87`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 168: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 140, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=88`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 169: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 150, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=89`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 170: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 160, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=90`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 171: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 80, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=91`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 172: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 90, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=92`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 173: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 100, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=93`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 174: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 110, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=94`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 175: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 120, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=70`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_not_in_catalog` porque o SKU nao existe no catalogo atual.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 176: Whey Protein Chocolate 1kg para cliente com objetivo de ganho de massa
- Entrada do cliente: "Quero algo de chocolate, ate R$ 130, para ganho de massa."
- Output estruturado esperado: `product_id=SKU-12345`, `confidence=71`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `product_out_of_stock` porque o produto existe mas nao pode ser vendido agora.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 177: Vegan Protein Vanilla 500g para cliente com objetivo de dieta vegana
- Entrada do cliente: "Quero algo de baunilha, ate R$ 140, para dieta vegana."
- Output estruturado esperado: `product_id=SKU-12346`, `confidence=72`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `exceeds_budget` porque o preco ultrapassa o limite informado pelo cliente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 178: Creatina Monohidratada 300g para cliente com objetivo de forca
- Entrada do cliente: "Quero algo de neutro, ate R$ 150, para forca."
- Output estruturado esperado: `product_id=SKU-33333`, `confidence=73`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `price_mismatch_with_catalog` porque o modelo citou preco diferente do backend.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 179: BCAA Morango 240g para cliente com objetivo de recuperacao
- Entrada do cliente: "Quero algo de morango, ate R$ 160, para recuperacao."
- Output estruturado esperado: `product_id=SKU-44444`, `confidence=74`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `history_contradiction` porque o cliente rejeitou esse caminho anteriormente.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

### Caso 180: Pre-Treino Cafeina 300g para cliente com objetivo de energia
- Entrada do cliente: "Quero algo de citrico, ate R$ 80, para energia."
- Output estruturado esperado: `product_id=SKU-55555`, `confidence=75`, `risk_flags=[]` quando todas as regras passam.
- Falha simulada: `allergy_conflict` porque o produto conflita com alergia registrada.
- Resposta correta do harness: rejeitar a recomendacao operacional, zerar confidence e registrar issue no audit log.
- Licao KODA: o cliente nao deve descobrir o erro; o sistema deve bloquear antes da mensagem final.
- Conexao Nivel 1: structured output transforma memoria fragil em estado verificavel.

---

## 📚 Apêndice B: Perguntas de Revisao para o Time

1. Onde o schema termina e a regra de negocio comeca?
2. Qual campo do `ProductRecommendation` voce usaria para rastrear risco comercial?
3. Por que `SKU-DEFAULT` deve existir no catalogo de teste?
4. Por que o fallback tem confidence 0 e nao 50?
5. Quando uma alternativa deve ser rejeitada mesmo que a recomendacao principal seja valida?
6. Como voce adaptaria `validate_against_history()` para uma conversa de 3 dias?
7. O que muda se KODA vender produtos com restricao medica mais sensivel?
8. Quais campos precisariam ir para SQLite em Nivel 3?
9. Como o Evaluator do Nivel 2 poderia consumir este mesmo JSON?
10. Qual alerta de observabilidade voce criaria para `product_out_of_stock`?

---

## 📋 Metadata

| Campo | Valor |
|---|---|
| **Arquivo** | `curriculum/01-nivel-1-fundamentals/exercises/solutions/exercise-02-solution.md` |
| **Exercicio** | 02 - Structured Output com Pydantic |
| **Nivel** | 1 - Fundamentals |
| **Tempo Estimado** | 120-150 minutos |
| **Status** | Solucao completa |
| **Conceitos** | JSON Schema, Pydantic, Business Constraints, Fallback, Audit Log |
| **Aplicacao KODA** | Recomendacoes de suplementos via WhatsApp |
| **Atualizado** | Maio 2026 |

---

## 💭 Reflexao Final

Marina nao quer saber se o output interno do KODA e JSON, XML ou objeto Python.

Ela quer saber se o agente lembra do que ela disse, respeita seu orcamento, nao inventa estoque e nao recomenda algo que possa fazer mal.

Structured output e a ponte entre essas duas realidades.

Para o cliente, KODA continua parecendo humano.

Para o sistema, KODA passa a ser verificavel.

Essa e a fundacao de todo o resto do curriculo: antes de agentes planejarem por horas, coordenarem varios workers ou persistirem estado em bancos sofisticados, eles precisam produzir respostas que outros componentes conseguem validar.

Sem contrato, nao ha confianca.

Com contrato, cada resposta vira uma decisao auditavel.

E uma decisao auditavel e o primeiro passo para um agente que merece operar no mundo real.

---

*Solucao completa do Exercicio 02 - Nivel 1 - Structured Output com Pydantic*  
*KODA Long-Running Agents Curriculum | FutanBear Technical Program | Maio 2026*
