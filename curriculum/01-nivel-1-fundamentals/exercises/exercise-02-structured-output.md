---
title: "Exercício 2: Implementar Structured Output (JSON Schema Validation)"
type: curriculum-exercise
nivel: 1
aliases: ["saída estruturada", "structured output", "validação JSON", "exercício schema"]
tags: [curriculo-conteudo, nivel-1, exercicio, structured-output, json-schema, schema-validation, fallback-pattern, audit-logging, business-constraints, product-recommendation, pydantic, python]
relates-to: ["[[curriculum/01-nivel-1-fundamentals/03-basic-harness-patterns|Basic Harness Patterns]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"]
last_updated: 2026-06-10
---
# ✅ Exercício 2: Implementar Structured Output (JSON Schema Validation)

**Nível:** 1 - Fundamentals  
**Tempo Estimado:** 60-90 minutos  
**Dificuldade:** ⭐⭐⭐ (Intermediária-Avançada)  
**Pré-requisito:** Ter lido `03-basic-harness-patterns.md` + completado Exercise 1  
**Status:** Hands-On Prático com Validação Real  

---

## 🎯 Objetivo

Você vai implementar um **validador de recomendações estruturadas** que:
1. Define um schema JSON estruturado com Pydantic
2. Valida que respostas do modelo seguem o schema
3. Aplica regras de negócio (constraints)
4. Retorna recomendações seguras ou fallback

**Resultado Final:** Você entenderá como KODA garante que recomendações são seguras antes de enviar ao cliente.

---

## 📖 O Problema Real

Seu agente gera recomendações em texto livre:

```
"Recomendo o Whey Protein Chocolate de 2kg, custa R$89 e tem 25g de proteína por scoop."
```

**Problemas:**
- ❌ Não consegue validar programaticamente
- ❌ Pode recomendar produto out-of-stock
- ❌ Pode exceder budget do cliente
- ❌ Integração com backend é frágil
- ❌ Difícil logar decisão para auditoria

**Solução:**
```json
{
  "product_id": "SKU-12345",
  "product_name": "Whey Protein Chocolate 1kg",
  "price": 89.90,
  "reason": "matches chocolate preference, vegan option, within budget",
  "alternatives": [
    {"product_id": "SKU-12346", "reason": "higher protein per serving"}
  ],
  "confidence": 92,
  "risk_flags": ["premium_price_for_budget"],
  "contradicts_previous_preferences": false
}
```

Agora você consegue validar cada campo!

---

## 📋 Requisitos

### Funcional
- [ ] Definir Pydantic model para `ProductRecommendation`
- [ ] Implementar classe `RecommendationValidator`
- [ ] Validar formato JSON (com retry se falhar)
- [ ] Validar constraints de negócio
- [ ] Gerar fallback seguro se tudo falhar
- [ ] Logar todas as decisões para auditoria

### Técnico
- [ ] Usar Pydantic (instale com `pip install pydantic`)
- [ ] Type hints completos
- [ ] Tratamento de erros robusto
- [ ] Logging estruturado
- [ ] Suportar Python 3.8+

### Validação
- [ ] Schema JSON válido conforme modelo
- [ ] Rejeitar recomendações que violam constraints
- [ ] Preservar confiança (0-100) realista
- [ ] Rastreabilidade completa de por quê foi rejeitado

---

## 🚀 Starter Code

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from enum import Enum
import json
from datetime import datetime

# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class ProductAlternative(BaseModel):
    """Alternativa de produto"""
    product_id: str
    product_name: Optional[str] = None
    reason: str
    
    class Config:
        extra = "forbid"  # Rejeita campos extras


class ProductRecommendation(BaseModel):
    """
    Schema estruturado para recomendação de produto.
    
    Todos os campos devem estar presentes e válidos.
    """
    
    # Identificação
    product_id: str = Field(..., description="ID único do produto (SKU-XXXXX)")
    product_name: str = Field(..., description="Nome do produto")
    
    # Recomendação
    price: float = Field(..., gt=0, description="Preço em reais (deve ser > 0)")
    reason: str = Field(..., min_length=10, description="Por que recomenda (mín 10 chars)")
    
    # Confiança
    confidence: int = Field(..., ge=0, le=100, description="Confiança 0-100%")
    
    # Opções
    alternatives: List[ProductAlternative] = Field(
        default_factory=list,
        description="Alternativas (pode estar vazio)"
    )
    
    # Alertas
    risk_flags: List[str] = Field(
        default_factory=list,
        description="Lista de riscos (compatibilidade, preço alto, etc)"
    )
    
    # Validação
    contradicts_previous_preferences: bool = Field(
        default=False,
        description="Se contradiz preferências anteriores do cliente"
    )
    
    # Metadata
    timestamp: Optional[str] = None
    source: str = Field(default="claude", description="Qual modelo gerou")
    
    @validator('confidence')
    def confidence_realistic(cls, v):
        """Valida que confiança não é 100% (sempre há incerteza)"""
        if v == 100:
            raise ValueError("Confidence nunca deve ser 100%, mínimo é 99%")
        return v
    
    @validator('product_id')
    def product_id_format(cls, v):
        """Valida formato de SKU"""
        if not v.startswith('SKU-'):
            raise ValueError(f"Product ID deve começar com 'SKU-', got: {v}")
        return v
    
    # TODO: Adicione mais validadores se necessário!
    
    class Config:
        extra = "forbid"  # Rejeita campos extras


# ============================================================================
# VALIDADOR
# ============================================================================

class RecommendationValidator:
    """
    Valida recomendações contra schema + regras de negócio.
    """
    
    def __init__(
        self,
        available_products: List[Dict],
        client_constraints: Dict,
        max_price: float = 10000.0
    ):
        """
        Args:
            available_products: Lista de produtos disponíveis em estoque
            client_constraints: Constraints do cliente (budget, restrições)
            max_price: Preço máximo permitido no sistema (sanidade check)
        """
        # TODO: Implementar inicialização
        # Dica: Armazene os dados e crie índices para lookup rápido
        pass
    
    def validate_json_format(self, response_text: str) -> Optional[ProductRecommendation]:
        """
        Valida que response é JSON válido conforme schema Pydantic.
        
        Args:
            response_text: Texto que deveria ser JSON válido
        
        Returns:
            ProductRecommendation se válido, None se inválido
        
        Comportamento esperado:
        1. Tentar parsear como JSON
        2. Tentar criar ProductRecommendation com dados
        3. Se falhar, registrar erro e retornar None
        4. Se sucesso, retornar objeto
        
        Exemplo:
            response = validator.validate_json_format('{"product_id": "SKU-123", ...}')
            if response:
                print(f"✅ JSON válido: {response.product_name}")
            else:
                print("❌ JSON inválido")
        """
        # TODO: Implementar
        pass
    
    def validate_business_constraints(
        self, 
        recommendation: ProductRecommendation
    ) -> tuple[bool, List[str]]:
        """
        Valida que recomendação respeita constraints de negócio.
        
        Args:
            recommendation: Recomendação já validada no schema
        
        Returns:
            (is_valid: bool, violations: List[str])
            
        Comportamento esperado:
        1. Verificar se produto existe em available_products
        2. Verificar se produto está em estoque
        3. Verificar se preço está dentro do budget do cliente
        4. Verificar se product_id é válido/existe
        5. Se houver violação, adicionar à violations list
        6. Retornar (True, []) se tudo ok, (False, [violações]) caso contrário
        
        Violações esperadas:
        - "product_not_in_catalog"
        - "product_out_of_stock"
        - "exceeds_budget"
        - "exceeds_system_max_price"
        - "price_mismatch_with_catalog"
        
        Exemplo:
            is_valid, violations = validator.validate_business_constraints(rec)
            if not is_valid:
                print(f"❌ Violações: {violations}")
                rec.confidence = 0  # Zerar confiança
        """
        # TODO: Implementar
        pass
    
    def validate_complete(
        self,
        response_text: str,
        previous_preferences: Optional[Dict] = None
    ) -> tuple[ProductRecommendation, List[str]]:
        """
        Validação COMPLETA: formato JSON + business constraints.
        
        Args:
            response_text: Resposta bruta do modelo
            previous_preferences: Preferências anteriores do cliente
        
        Returns:
            (recommendation, issues)
            - recommendation: Objeto validado (ou fallback se falhou)
            - issues: Lista de problemas encontrados (pode estar vazia)
        
        Comportamento esperado:
        1. Validar JSON format
        2. Se falhou JSON, registrar e retornar fallback
        3. Se passed JSON, validar constraints
        4. Se falhou constraints, adicionar issues + zerar confidence
        5. Sempre retornar ALGO (recomendação real ou fallback)
        6. Logar tudo para auditoria
        
        Exemplo:
            rec, issues = validator.validate_complete(
                response_text='{"product_id": "SKU-123", ...}',
                previous_preferences={"flavor": "chocolate"}
            )
            
            if issues:
                print(f"⚠️ Issues: {issues}")
                print(f"Confidence reduzida para: {rec.confidence}")
            else:
                print(f"✅ Recomendação aprovada: {rec.product_name}")
        """
        # TODO: Implementar
        pass
    
    def get_fallback_recommendation(self) -> ProductRecommendation:
        """
        Retorna recomendação segura de fallback.
        
        Usado quando modelo falha completamente.
        Deve ser um produto que SEMPRE está disponível.
        
        Returns:
            ProductRecommendation com confidence=0
        
        Exemplo:
            fallback = validator.get_fallback_recommendation()
            # Resultado:
            # {
            #   "product_id": "SKU-DEFAULT",
            #   "product_name": "Our Top Recommendation (System Default)",
            #   "reason": "Model unable to generate recommendation",
            #   "confidence": 0,
            #   ...
            # }
        """
        # TODO: Implementar
        pass
    
    def log_decision(
        self,
        recommendation: ProductRecommendation,
        client_id: str,
        issues: List[str],
        approved: bool
    ) -> None:
        """
        Loga decisão para auditoria.
        
        Args:
            recommendation: Recomendação gerada
            client_id: ID do cliente
            issues: Problemas encontrados
            approved: Se foi aprovada ou não
        
        Comportamento esperado:
        - Criar um log estruturado JSON
        - Incluir timestamp, client_id, todos os detalhes
        - Guardar em arquivo ou registrar via logging
        
        Exemplo output:
            {
                "timestamp": "2026-05-25T14:30:00Z",
                "client_id": "client_123",
                "recommendation": {"product_id": "SKU-123", ...},
                "issues": [],
                "approved": true,
                "confidence": 92
            }
        """
        # TODO: Implementar
        pass


# ============================================================================
# TESTES
# ============================================================================

def create_test_data():
    """Cria dados de teste"""
    available_products = [
        {
            "id": "SKU-12345",
            "name": "Whey Protein Chocolate 1kg",
            "price": 89.90,
            "in_stock": True,
            "category": "supplements"
        },
        {
            "id": "SKU-12346",
            "name": "Vegan Protein Vanilla 500g",
            "price": 120.00,
            "in_stock": False,  # Out of stock
            "category": "supplements"
        },
        {
            "id": "SKU-DEFAULT",
            "name": "Our Top Recommendation (System Default)",
            "price": 99.90,
            "in_stock": True,
            "category": "supplements"
        }
    ]
    
    client_constraints = {
        "budget_min": 50.0,
        "budget_max": 150.0,
        "restrictions": ["gluten"],
        "allergies": ["peanuts"]
    }
    
    return available_products, client_constraints


def test_valid_recommendation():
    """Test 1: Recomendação válida passa em tudo"""
    print("\n🧪 Test 1: Recomendação Válida")
    
    products, constraints = create_test_data()
    validator = RecommendationValidator(products, constraints)
    
    valid_json = json.dumps({
        "product_id": "SKU-12345",
        "product_name": "Whey Protein Chocolate 1kg",
        "price": 89.90,
        "reason": "Matches chocolate preference, in stock, within budget",
        "confidence": 92,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False
    })
    
    rec, issues = validator.validate_complete(valid_json)
    
    assert rec.product_id == "SKU-12345", "Product ID deve corresponder"
    assert len(issues) == 0, "Não deve ter issues"
    assert rec.confidence == 92, "Confiança deve ser preservada"
    
    print("✅ Test 1 passou!")


def test_invalid_json():
    """Test 2: JSON inválido retorna fallback"""
    print("\n🧪 Test 2: JSON Inválido")
    
    products, constraints = create_test_data()
    validator = RecommendationValidator(products, constraints)
    
    invalid_json = "isso não é JSON válido {]"
    
    rec, issues = validator.validate_complete(invalid_json)
    
    # Deve retornar fallback
    assert rec.product_id == "SKU-DEFAULT", "Deve usar fallback"
    assert rec.confidence == 0, "Fallback tem confidence 0"
    assert len(issues) > 0, "Deve ter issues registrados"
    
    print("✅ Test 2 passou!")


def test_out_of_stock():
    """Test 3: Produto out-of-stock é rejeitado"""
    print("\n🧪 Test 3: Produto Out-of-Stock")
    
    products, constraints = create_test_data()
    validator = RecommendationValidator(products, constraints)
    
    json_out_of_stock = json.dumps({
        "product_id": "SKU-12346",  # Out of stock!
        "product_name": "Vegan Protein Vanilla 500g",
        "price": 120.00,
        "reason": "Vegan option",
        "confidence": 85,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False
    })
    
    rec, issues = validator.validate_complete(json_out_of_stock)
    
    assert "out_of_stock" in str(issues), "Deve detectar out-of-stock"
    assert rec.confidence < 85, "Confiança deve ser reduzida"
    
    print("✅ Test 3 passou!")


def test_exceeds_budget():
    """Test 4: Preço acima do budget é detectado"""
    print("\n🧪 Test 4: Exceeds Budget")
    
    products, constraints = create_test_data()
    validator = RecommendationValidator(products, constraints)
    
    # Cliente tem budget máximo de 150, mas recomendação é 200
    json_exceeds = json.dumps({
        "product_id": "SKU-99999",
        "product_name": "Premium Supplement",
        "price": 200.00,  # Acima do budget!
        "reason": "Premium option",
        "confidence": 80,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False
    })
    
    rec, issues = validator.validate_complete(json_exceeds)
    
    assert "exceeds_budget" in str(issues) or "budget" in str(issues).lower(), \
        "Deve detectar ultrapassagem de budget"
    
    print("✅ Test 4 passou!")


def test_invalid_schema_field():
    """Test 5: Campo inválido no schema"""
    print("\n🧪 Test 5: Schema Inválido (campo faltando)")
    
    products, constraints = create_test_data()
    validator = RecommendationValidator(products, constraints)
    
    # Falta o campo 'reason'
    json_invalid_schema = json.dumps({
        "product_id": "SKU-12345",
        "product_name": "Whey Protein",
        "price": 89.90,
        # FALTA 'reason'!
        "confidence": 92,
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False
    })
    
    rec, issues = validator.validate_complete(json_invalid_schema)
    
    # Deve usar fallback
    assert rec.product_id == "SKU-DEFAULT" or rec.confidence == 0, \
        "Deve rejeitar schema inválido"
    
    print("✅ Test 5 passou!")


def test_confidence_validation():
    """Test 6: Confiança 100% é rejeitada"""
    print("\n🧪 Test 6: Confidence 100% Validation")
    
    products, constraints = create_test_data()
    validator = RecommendationValidator(products, constraints)
    
    # Tenta usar confidence=100
    json_100_confidence = json.dumps({
        "product_id": "SKU-12345",
        "product_name": "Whey Protein",
        "price": 89.90,
        "reason": "Good product",
        "confidence": 100,  # Inválido!
        "alternatives": [],
        "risk_flags": [],
        "contradicts_previous_preferences": False
    })
    
    rec, issues = validator.validate_complete(json_100_confidence)
    
    assert rec.confidence < 100, "Confidence deve ser < 100"
    
    print("✅ Test 6 passou!")


def run_all_tests():
    """Executa todos os testes"""
    print("="*60)
    print("EXERCÍCIO 2: IMPLEMENTAR STRUCTURED OUTPUT")
    print("="*60)
    
    # Descomente quando implementado:
    # test_valid_recommendation()
    # test_invalid_json()
    # test_out_of_stock()
    # test_exceeds_budget()
    # test_invalid_schema_field()
    # test_confidence_validation()
    
    print("\n📝 TODO: Implemente a classe RecommendationValidator acima!")
    print("   Após implementar, descomente os tests em run_all_tests()")


if __name__ == "__main__":
    run_all_tests()
```

---

## 🏗️ Como Começar

### Passo 1: Instalar Pydantic
```bash
pip install pydantic
```

### Passo 2: Entender os Modelos
- `ProductAlternative`: Alternativa de produto (simples)
- `ProductRecommendation`: Recomendação completa (com validadores)

### Passo 3: Implementar `__init__` da classe
```python
def __init__(self, available_products, client_constraints, max_price=10000.0):
    self.available_products = available_products
    self.client_constraints = client_constraints
    self.max_price = max_price
    
    # Dica: Crie um índice para lookup rápido
    self.product_index = {p['id']: p for p in available_products}
```

### Passo 4: Implementar `validate_json_format`
```python
def validate_json_format(self, response_text):
    try:
        data = json.loads(response_text)
        return ProductRecommendation(**data)
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}")
        return None
    except Exception as e:
        print(f"❌ Schema inválido: {e}")
        return None
```

### Passo 5: Implementar `validate_business_constraints`
- Verificar se produto existe
- Verificar se está em estoque
- Verificar se preço está no budget
- Retornar (True, []) ou (False, [violations])

### Passo 6: Implementar `validate_complete`
- Chamar validate_json_format
- Se falhar, retornar fallback
- Se passar, chamar validate_business_constraints
- Se falhar constraints, zerar confidence
- Logar tudo

### Passo 7: Testar
- Descomente os testes
- Execute `python seu_arquivo.py`
- Todos devem passar ✅

---

## 🎯 Desafios Extra (Opcional)

### Desafio 1: Retry com Claude
```python
def validate_with_retry(
    self, 
    model_response: str, 
    max_retries: int = 3
) -> ProductRecommendation:
    """
    Se JSON falhar, tente novamente com prompt mais específico.
    """
    pass
```

### Desafio 2: Penalidade Dinâmica
```python
def apply_risk_penalties(self, recommendation: ProductRecommendation):
    """
    Reduza confidence baseado em risk_flags.
    Exemplo: Se tem "high_price_alert", reduz 20% de confidence
    """
    pass
```

### Desafio 3: Auditoria Completa
```python
def generate_audit_report(self, conversation_id: str) -> str:
    """
    Gera relatório completo de todas as recomendações
    nesta conversa: aceitas, rejeitadas, fallbacks.
    """
    pass
```

### Desafio 4: Integração com Estado
```python
def validate_against_history(
    self,
    recommendation: ProductRecommendation,
    client_history: List[Dict]
) -> bool:
    """
    Valida que recomendação não contradiz histórico do cliente.
    """
    pass
```

---

## 📊 Checklist de Implementação

- [ ] Models Pydantic definidos (`ProductAlternative`, `ProductRecommendation`)
- [ ] Validadores Pydantic implementados (@validator)
- [ ] Classe `RecommendationValidator` criada
- [ ] Método `__init__` implementado
- [ ] Método `validate_json_format` implementado
- [ ] Método `validate_business_constraints` implementado
- [ ] Método `validate_complete` implementado
- [ ] Método `get_fallback_recommendation` implementado
- [ ] Método `log_decision` implementado
- [ ] Test 1 (válido) passa ✅
- [ ] Test 2 (JSON inválido) passa ✅
- [ ] Test 3 (out-of-stock) passa ✅
- [ ] Test 4 (exceeds budget) passa ✅
- [ ] Test 5 (schema inválido) passa ✅
- [ ] Test 6 (confidence 100%) passa ✅

---

## 💡 Dicas de Implementação

**Dica 1:** Pydantic faz validação automática. Use-o!
```python
# Isso valida sozinho:
rec = ProductRecommendation(product_id="SKU-123", ...)
# Se product_id não começar com "SKU-", raise erro
```

**Dica 2:** Use try/except para capturar erros Pydantic
```python
try:
    rec = ProductRecommendation(**data)
except ValueError as e:
    print(f"Erro validação: {e}")
```

**Dica 3:** Confidence deve ser reduzida progressivamente
```python
# Se tem 1 issue: reduz 10%
# Se tem 2 issues: reduz 25%
# Se tem 3+: vai a 0
```

**Dica 4:** Sempre retorne ALGO
```python
if validation_failed:
    return self.get_fallback_recommendation(), issues
```

**Dica 5:** Log estruturado é crítico
```python
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "product_id": rec.product_id,
    "confidence": rec.confidence,
    "issues": issues,
    "approved": len(issues) == 0
}
```

---

## ✅ Validação Final

Sua implementação está correta se:

1. ✅ Todos os 6 testes passam
2. ✅ JSON inválido retorna fallback (não crash)
3. ✅ Constraints de negócio são enforçados
4. ✅ Confidence é ajustado baseado em issues
5. ✅ Logging é estruturado e completo
6. ✅ Código tem type hints e docstrings

---

## 🎓 O Que Você Aprendeu

Após completar este exercício, você entende:

- ✅ Como usar Pydantic para validação de schema
- ✅ Como implementar validadores customizados
- ✅ Trade-off entre validação no schema vs no código
- ✅ Como aplicar regras de negócio (constraints)
- ✅ Como fazer audit logging para conformidade
- ✅ Padrão: Validação em camadas (schema → constraints → logic)

**Próximo:** Nível 2 - Padrões Práticos Avançados

---

*Exercício 2 de Nível 1 | Curso Long-Running Agents | FutanBear Technical Program*
