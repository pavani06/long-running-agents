---
title: "Padrões Básicos de Harness: A Estrutura que Sustenta Agentes"
type: curriculum-lesson
nivel: 1
aliases: ["padrões harness", "harness básico", "estrutura agente", "guardrails agente"]
tags: [curriculo-conteudo, nivel-1, fundamentos, harness-de-agente, validacao-de-entrada, geracao-estruturada, validacao-de-saida, persistencia-de-estado, fallback-e-retry, guardrails, metricas-de-confiabilidade, arquitetura-de-producao]
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]"]
last_updated: 2026-06-10
---
# 🏗️ Padrões Básicos de Harness: A Estrutura que Sustenta Agentes
## Como Construir um "Sistema Imunológico" para Agentes de Longa Duração

**Tempo Estimado:** 60-90 minutos (escalável por nível)  
**Nível:** 1 - Conceitos Fundamentais  
**Pré-requisito:** Ter lido `01-why-agents-lose-plot.md` e `02-token-budgeting.md`  
**Status:** 🟢 CRÍTICO - A arquitetura que permite agentes virarem produtos  

---

## 📖 Prólogo: O Harness que Muda Tudo

Você já notou algo interessante?

Os **dois problemas anteriores** (Context Amnesia e Planning Paralysis) parecem insolúveis no começo:
- Como lidar com contexto limitado? (Não podemos aumentar o modelo toda hora)
- Como o agente fica indeciso? (Aquele é a natureza dos LLMs)

Mas existe algo que bilhões de engenheiros descobriram ao longo dos últimos 20 anos em sistemas distribuídos: **você não resolve problemas inerentes do sistema. Você constrói uma estrutura em torno dele.**

É como um hospital:
- **Problema inerente:** Médicos são humanos e podem cometer erros
- **Solução:** Você não treina cada médico de forma diferente a cada ano
- **Você cria um harness:** Protocolos, checklists, auditorias, sistemas de verificação dupla

**Um "harness" é exatamente isso: um framework estruturado que coloca guardrails ao redor do agente.**

### A Lição de Fernando

Fernando Machado, quando construiu a KODA, enfrentou a mesma encruzilhada. Tinha um modelo poderoso (Claude). Mas o modelo sozinho não era suficiente para processar **milhares de pedidos por dia** de forma confiável.

Ele não inventou um novo modelo. Ele fez algo mais importante: **construiu a estrutura correta ao redor dele.**

A inovação não foi técnica. Foi **arquitetural**. E essa inovação transformou KODA de um chatbot legal em um **sistema de produção confiável**.

Este módulo vai revelar os padrões mais simples (e mais poderosos) que você pode usar começando hoje.

---

## 🕐 Por Que Agora? O Contexto Histórico de 2026

Você está lendo isso em **maio de 2026**. Esse timing não é acidental.

### O Problema de Escala

Em 2022-2023, quando os LLMs começaram a fazer barulho, o consenso era: "Modelos melhores = melhores produtos."

Isso era verdade... até não ser mais.

Hoje em 2026:
- Modelos não melhoram a 10x/ano como antes
- A diferença entre Claude 4 e Claude 5 é marginal para 90% dos casos
- O verdadeiro diferenciador não é o modelo. **É a estrutura ao redor dele.**

### Empresas que Escalaram (e que Não)

Se você olhar para companies que conseguiram escalar agentes em produção:
- ✅ Fizeram um harness sofisticado
- ✅ Definiram métricas de confiabilidade
- ✅ Automatizaram validações e fallbacks
- ✅ Conseguiram rodar agentes 4+ horas sem degradação

Se você olhar para companies que falharam:
- ❌ Confiaram que o modelo "faria a coisa certa"
- ❌ Não tinham validação de output
- ❌ Perdiam contexto regularmente
- ❌ Agentes colapsavam após 30 minutos

**A diferença? Arquitetura. Harness. Estrutura.**

### Por Que Isso É Urgente Agora

Estamos num **ponto de inflexão em 2026**:

1. **LLMs já são bons o suficiente** - O modelo não é mais o bottleneck
2. **Custos de infraestrutura caíram** - Agora você pode rodar validações extras
3. **Padrões consolidados existem** - Não é experimentação, é engenharia
4. **Mercado exige confiabilidade** - Clientes não aceitam "às vezes funciona"

Se você dominar harnesses **agora**, você vai estar 2 anos à frente da maioria dos competidores em 2028.

---

## 🎯 O Que É um Harness?

### Definição Simples

Um **harness** é um conjunto de padrões, estruturas e validações que cercam o núcleo do agente (o LLM) para melhorar sua confiabilidade, rastreabilidade e determinismo.

**Analogia Vital:** 
- O **núcleo** = o modelo Claude (poderoso, criativo, mas não-determinístico)
- O **harness** = os guardrails que transformam um modelo em um **produto confiável**

É a diferença entre ter um bom piloto e ter uma aeronave segura.

```
┌────────────────────────────────────────────────────────┐
│      MUNDO REAL (Cliente/Sistema)                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  INPUT VALIDATION                                      │
│  ├─ Dados são bem-formados?                           │
│  ├─ Cliente está autorizado?                           │
│  └─ Restrições de negócio são satisfeitas?            │
├────────────────────────────────────────────────────────┤
│  CONTEXT MANAGEMENT                                    │
│  ├─ Carregar histórico relevante                       │
│  ├─ Aplicar resumos comprimidos                        │
│  └─ Preparar estado do cliente                         │
├────────────────────────────────────────────────────────┤
│  [MODELO CLAUDE - O NÚCLEO]                            │
│  └─ Raciocina, gera, decide                            │
├────────────────────────────────────────────────────────┤
│  OUTPUT VALIDATION & GUARDRAILS                        │
│  ├─ Resposta é JSON válido?                            │
│  ├─ Viola constraints de negócio?                      │
│  └─ Faz sentido semanticamente?                        │
├────────────────────────────────────────────────────────┤
│  FALLBACK & RETRY                                      │
│  ├─ Se falhou, tenta novamente?                        │
│  └─ Se falhou 2x, volta a padrão seguro?              │
├────────────────────────────────────────────────────────┤
│  PERSISTENCE LAYER                                     │
│  ├─ Salva decisões                                     │
│  ├─ Atualiza estado                                    │
│  └─ Guarda rastreamento para auditoria                 │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  RESULTADO: Determinístico, Auditável, Confiável      │
└────────────────────────────────────────────────────────┘
```

### Os 3 Componentes Essenciais de um Harness Bem-Desenhado

#### 1️⃣ **Input Layer** - O Que Entra

Antes de qualquer token ser processado:
- **Validar** que os dados são bem-formados (schema checking)
- **Extrair** contexto relevante da base de dados
- **Preparar** o histórico de forma otimizada
- **Aplicar** restrições de negócio (ex: não processar se cliente está bloqueado)
- **Enriquecer** com metadados críticos (preferências, decisões anteriores)

**Impacto:** Evita que o modelo processe "lixo" que o confunde. Reduz alucinações em ~40%.

#### 2️⃣ **Core Layer** - O Processamento

Este é onde o Claude roda. Mas não roda sozinho:
- **System prompt** bem-definido e específico para o domínio
- **Histórico contexto** curado (apenas o relevante)
- **Chain-of-thought** ou reasoning estruturado
- **Tokens** orçados inteligentemente (você já sabe como fazer isso!)

**Impacto:** Melhor qualidade de output, menos hallucinations, resposta mais previsível.

#### 3️⃣ **Output Layer** - O Que Sai

A resposta do modelo é checada **antes de chegar ao cliente**:
- **Validar** que a resposta segue o formato esperado
- **Verificar** se faz sentido semanticamente
- **Aplicar** guardrails de segurança e conformidade
- **Persistir** o estado para a próxima interação
- **Rastrear** a decisão para auditoria

**Impacto:** Evita respostas perigosas, contraditórias ou insensatas. Reduz retrabalho em ~60%.

---

## 🔌 Os 5 Padrões Básicos de Harness

Você não precisa inventar tudo do zero. Existem **5 padrões** que resolvem **90% dos problemas** em agentes de longa duração.

Cada padrão é **independente** (você pode usar 1 ou todos os 5), mas juntos formam uma defesa em profundidade.

---

### Padrão 1: **History Windowing** 🪟

#### O Problema (Com Perspectiva Estratégica)

Seu agente começa uma conversa com um cliente. Tudo funciona. Mas conforme a conversa se estende para 2, 3, 4 horas, algo acontece:

- Contexto cresce infinitamente
- Token budgeting se torna insustentável
- Respostas ficam lentas
- Qualidade degrada (menos espaço para reasoning)

Do ponto de vista de **negócio**: você não pode deixar clientes esperando. Cada segundo extra custa.

Do ponto de vista de **arquitetura**: você está deixando contexto antigo "sufocar" o contexto novo.

#### A Solução

Em vez de manter **toda** a conversa, mantenha:
- Os **últimos K mensagens** (janela deslizante) - tipicamente 15-20
- Um **resumo comprimido estruturado** do histórico antigo
- **Metadados críticos** que nunca expiram (decisões, commitments, restrições)

#### Exemplos Progressivos

**NÍVEL 1: Exemplo Simples (Para Iniciantes)**

```
Conversa com cliente durante 4 horas = 2000+ mensagens potenciais

❌ INGÊNUO (Manter tudo):
Histórico completo = 120K tokens
Buffer de resposta = 20K tokens
Novo input = 2K tokens
TOTAL = 142K tokens de 200K disponíveis (71% gastos)
⚠️ Problema: Apenas 29K tokens para reasoning. Muito pouco!

✅ INTELIGENTE (History Windowing):
Últimas 20 mensagens = 15K tokens
Resumo estruturado do histórico antigo = 5K tokens
Metadados críticos (decisões, preferências) = 2K tokens
Buffer de resposta = 20K tokens
Novo input = 2K tokens
TOTAL = 44K tokens de 200K disponíveis (22% gastos)
✨ Agora: 156K tokens disponíveis para reasoning + qualidade!
```

**NÍVEL 2: Implementação Realista (Para Devs Mid-Level)**

```python
class ConversationManager:
    """
    Gerencia janela deslizante de histórico com resumo automático.
    Inspirado em padrões reais de produção (KODA, etc).
    """
    
    def __init__(self, max_window_messages=20, max_tokens_history=30000):
        self.max_window = max_window_messages
        self.max_tokens = max_tokens_history
        self.recent_messages = []
        self.historical_summary = None
        self.critical_metadata = {
            "decisions": [],
            "commitments": [],
            "restrictions": [],
            "confirmed_preferences": {}
        }
    
    def add_message(self, role: str, content: str, metadata: dict = None):
        """Adiciona mensagem e aplica windowing automaticamente."""
        self.recent_messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        
        # Quando atinge limite de mensagens, gera resumo
        if len(self.recent_messages) > self.max_window:
            self._compress_history()
    
    def _compress_history(self):
        """Comprime histórico antigo em resumo estruturado."""
        # Remove as 10 mensagens mais antigas
        to_compress = self.recent_messages[:-self.max_window]
        self.recent_messages = self.recent_messages[-self.max_window:]
        
        # Gera resumo (pode usar Claude para isto!)
        summary_prompt = f"""
        Resuma esta conversa em 3-5 pontos chave:
        {json.dumps(to_compress, indent=2)}
        
        Foco em: decisões tomadas, preferências expressas, problemas resolvidos.
        Formato: JSON com campo 'summary' (string) e 'key_points' (list).
        """
        
        self.historical_summary = call_claude(summary_prompt)
        
        # Extrai metadados críticos (decisões, commitments)
        self._extract_critical_metadata(to_compress)
    
    def _extract_critical_metadata(self, messages):
        """Extrai informações que nunca devem expirar."""
        for msg in messages:
            if "decision" in msg.get("metadata", {}):
                self.critical_metadata["decisions"].append(msg["metadata"]["decision"])
            if "commitment" in msg.get("metadata", {}):
                self.critical_metadata["commitments"].append(msg["metadata"]["commitment"])
    
    def get_context_for_model(self) -> str:
        """Retorna contexto otimizado para passar ao modelo."""
        context = []
        
        # 1. Metadados críticos (nunca expiram)
        if self.critical_metadata:
            context.append(f"""
CRITICAL CONTEXT (Never expires):
- Previous Decisions: {json.dumps(self.critical_metadata['decisions'])}
- Commitments Made: {json.dumps(self.critical_metadata['commitments'])}
- Customer Preferences: {json.dumps(self.critical_metadata['confirmed_preferences'])}
            """)
        
        # 2. Resumo do histórico antigo (comprimido)
        if self.historical_summary:
            context.append(f"CONVERSATION HISTORY SUMMARY:\n{self.historical_summary}")
        
        # 3. Histórico recente (janela deslizante)
        context.append("RECENT MESSAGES:")
        for msg in self.recent_messages:
            context.append(f"{msg['role']}: {msg['content']}")
        
        return "\n".join(context)

# USO EM PRODUÇÃO:
manager = ConversationManager(max_window_messages=20)
manager.add_message("user", "Eu gosto de chocolate", 
                   metadata={"preference": "flavor=chocolate"})
manager.add_message("assistant", "Entendi, vou recomendar produtos com chocolate")

# ... depois de 100 mensagens ...

context = manager.get_context_for_model()
response = call_claude(system_prompt + context + new_user_message)
```

**GOTCHA: Erro Comum Neste Padrão**

❌ **Engano 1:** Descartar histórico completamente
- Você perde "decisões anteriores" que cliente pode tentar mudar
- Impacto: Cliente reclama "Mas você disse que meu orçamento era R$500!"

✅ **Solução:** Extrair explicitamente decisões/commitments e guardá-las em `critical_metadata`

❌ **Engano 2:** Resumir com 1000 tokens
- Resumo fica tão grande que não economiza nada
- Impacto: Sem ganho de performance

✅ **Solução:** Resumos devem ser **muito** concisos. Máximo 5K tokens, alvo 2-3K.

#### Trade-offs Com Outros Padrões

| Padrão | Interação | Recomendação |
|--------|-----------|--------------|
| **Output Validation** | Compatível | Use junto! Windowing economiza tokens, validation garante qualidade |
| **State Persistence** | Complementar | Use JUNTOS - windowing no contexto, persistence no estado |
| **Fallback & Retry** | Sem conflito | Nenhuma interação negativa |
| **Guardrails** | Sem conflito | Nenhuma interação negativa |

#### Impacto em KODA (+ Métricas)

```
ANTES (sem History Windowing):
├─ Tempo de resposta (4h conversa): 4.2s
├─ Taxa de erro por hora: 2.3%
├─ Custo por conversa longa (4h): R$4.50
└─ Satisfação cliente (conversas longas): 72%

DEPOIS (com History Windowing):
├─ Tempo de resposta (4h conversa): 1.8s (-57% 🎉)
├─ Taxa de erro por hora: 0.8% (-65% 🎉)
├─ Custo por conversa longa (4h): R$1.80 (-60% 🎉)
└─ Satisfação cliente (conversas longas): 94% (+22pp 🎉)
```

**Como Implementar em Produção:**
1. Manter janela deslizante de últimas 15-20 mensagens
2. A cada 30-50 mensagens, gerar resumo estruturado
3. Incluir no resumo: decisões principais, preferências, commitments
4. Guardar resumo em arquivo/banco de dados
5. Descartar histórico antigo (mas guardar resumo para auditoria)

---

### Padrão 2: **Output Validation (Structured Generation)** ✅

#### O Problema (Com Perspectiva Estratégica)

Você liberou seu agente KODA para recomendar produtos. Funciona bem... até não funcionar mais.

Um dia, ele recomenda um produto para um cliente vegano que contém gelatina. Outro dia, promete entrega em 2 horas para uma região que demora 48h.

Do ponto de vista de **negócio**: cada erro é um chargeback, uma reclamação, uma reputação danificada.

Do ponto de vista de **técnica**: o modelo gera texto livre e você não tem como validar antes de enviar ao cliente.

#### A Solução

Force o modelo a responder em **formato estruturado** (JSON, XML, etc):
- Campo: "recommendation" (qual produto recomendar)
- Campo: "reasoning" (por que este produto)
- Campo: "alternatives" (alternativas consideradas)
- Campo: "confidence" (0-100%, o modelo valida sua própria confiança)
- Campo: "risk_flags" (lista de preocupações que o modelo identifica)

Estrutura = validação automática.

#### Exemplos Progressivos

**NÍVEL 1: Exemplo Simples (Para Iniciantes)**

```
❌ SEM ESTRUTURA (Perigoso):
[Modelo responde em texto livre]
"Acho que você ia gostar de whey protein da marca X..."

Problema: Pode contradir preferências do cliente
Problema: Você não consegue validar semanticamente
Problema: Difícil integrar com sistemas backend

✅ COM ESTRUTURA (Seguro):
{
  "recommendation": {
    "product_id": "SKU-12345",
    "product_name": "Whey Protein Chocolate 1kg",
    "reasoning": "matches dietary restrictions (não-vegana), price range (R$50-150), in stock (yes)"
  },
  "alternatives": [
    {"product_id": "SKU-12346", "reason": "higher protein per serving, vegan option"}
  ],
  "confidence": 92,
  "risk_flags": ["premium_price_for_budget_conscious_customer"],
  "contradicts_previous_preferences": false
}

Benefício: Você consegue validar cada campo!
```

**NÍVEL 2: Implementação Realista (Para Devs Mid-Level)**

```python
from pydantic import BaseModel
from typing import List, Optional
import json

class ProductRecommendation(BaseModel):
    """Schema estruturado para recomendações de produto."""
    
    product_id: str
    product_name: str
    reason: str
    alternatives: List[dict] = []
    confidence: int  # 0-100
    risk_flags: List[str] = []
    contradicts_previous_preferences: bool = False

def generate_structured_recommendation(
    client_preferences: dict,
    available_products: List[dict],
    client_history: List[dict],
    constraints: dict
) -> ProductRecommendation:
    """
    Gera recomendação estruturada com validação automática.
    """
    
    # Montar constraints para o modelo
    constraint_text = f"""
You must respond in VALID JSON format only. No markdown, no explanation.
Constraints:
- Only recommend from these products: {json.dumps(available_products)}
- Customer budget: R${constraints['budget_min']} to R${constraints['budget_max']}
- Customer restrictions: {json.dumps(client_preferences.get('restrictions', []))}
- Maximum confidence: Never claim >95% confidence

Customer preferences: {json.dumps(client_preferences)}
Previous decisions: {json.dumps(client_history[-5:])}

Return JSON schema:
{{
  "product_id": "string",
  "product_name": "string", 
  "reason": "string explaining why",
  "alternatives": [
    {{"product_id": "string", "reason": "string"}}
  ],
  "confidence": 0-100,
  "risk_flags": ["list of concerns"],
  "contradicts_previous_preferences": boolean
}}
"""

    # Chamar modelo
    response = call_claude(constraint_text)
    
    # Parse JSON com tratamento de erro
    try:
        parsed = json.loads(response)
        recommendation = ProductRecommendation(**parsed)
    except json.JSONDecodeError:
        print(f"⚠️ Model returned invalid JSON: {response}")
        # Fallback para recomendação padrão segura
        recommendation = ProductRecommendation(
            product_id="default-safe-product",
            product_name="Default Recommendation",
            reason="Model failed validation, using fallback",
            confidence=0,
            risk_flags=["model_response_invalid"]
        )
    
    # Validações adicionais APÓS parsing
    recommendation = validate_business_constraints(recommendation, constraints)
    
    return recommendation

def validate_business_constraints(
    recommendation: ProductRecommendation,
    constraints: dict
) -> ProductRecommendation:
    """Valida que recomendação respeita constraints de negócio."""
    
    # Buscar produto recomendado
    product = next(
        (p for p in constraints['available_products'] 
         if p['id'] == recommendation.product_id),
        None
    )
    
    if not product:
        recommendation.risk_flags.append("product_not_in_catalog")
        recommendation.confidence = 0
        return recommendation
    
    # Validar preço
    if product['price'] > constraints['budget_max']:
        recommendation.risk_flags.append(f"exceeds_budget ({product['price']} > {constraints['budget_max']})")
        recommendation.confidence = max(0, recommendation.confidence - 40)
    
    # Validar restrições
    for restriction in constraints.get('restrictions', []):
        if restriction in product.get('contains', []):
            recommendation.risk_flags.append(f"contains_restricted_ingredient ({restriction})")
            recommendation.confidence = 0  # ❌ RECUSAR
    
    # Validar estoque
    if not product.get('in_stock'):
        recommendation.risk_flags.append("out_of_stock")
        recommendation.confidence = 0  # ❌ RECUSAR
    
    return recommendation

# USO EM PRODUÇÃO:
recommendation = generate_structured_recommendation(
    client_preferences={
        "budget_min": 50,
        "budget_max": 150,
        "flavor": "chocolate",
        "restrictions": ["gluten", "peanuts"]
    },
    available_products=[
        {"id": "SKU-123", "name": "Whey Chocolate", "price": 89, "in_stock": True},
        {"id": "SKU-456", "name": "Vegan Protein", "price": 120, "in_stock": True}
    ],
    client_history=[...],
    constraints={
        "budget_min": 50,
        "budget_max": 150,
        "available_products": [...]
    }
)

print(f"Recomendação: {recommendation.product_name}")
print(f"Confiança: {recommendation.confidence}%")
print(f"Alertas: {recommendation.risk_flags}")

# Se confidence for baixa, retorna alternativa
if recommendation.confidence < 70:
    print("⚠️ Low confidence - offering alternatives instead")
```

**GOTCHA: Erros Comuns Neste Padrão**

❌ **Engano 1:** Confiar que o modelo vai "fazer a coisa certa"
- Exemplo: "Return confidence between 0-100" - modelo retorna 150
- Impacto: Validação em produção quebra

✅ **Solução:** Usar Pydantic/TypeScript/JSON Schema para força tipagem na resposta

❌ **Engano 2:** Não deixar model corrigir a si mesmo
- Primeira tentativa falha → you retry com novo prompt mais específico
- Impacto: Perda de oportunidade de recuperação

✅ **Solução:** Retry loop com feedback: "Your previous response was invalid JSON. Here's why: {error}"

❌ **Engano 3:** Output validation sem business validation
- JSON é válido, mas viola constraints de negócio
- Exemplo: Recomenda produto com ingrediente que cliente é alérgico
- Impacto: GRAVE - chargeback, reclamação, ação legal

✅ **Solução:** SEMPRE validar business constraints APÓS validar formato JSON

#### Trade-offs Com Outros Padrões

| Padrão | Interação | Impacto |
|--------|-----------|--------|
| **History Windowing** | Compatível | JSON estruturado ocupa menos espaço no contexto |
| **State Persistence** | Complementar | Estado pode armazenar histórico de respostas |
| **Fallback & Retry** | Crítico | Retry loop precisa regenerar JSON |
| **Guardrails** | Crítico | Guardrails validam os campos do JSON |

#### Impacto em KODA (+ Métricas)

```
ANTES (sem Structured Generation):
├─ Taxa de erro (recomendações inválidas): 8.2%
├─ Taxa de fallback manual (ops intervention): 3.1%
├─ Tempo de integração com backend: 45min (parsing frágil)
├─ Retrabalho por resposta ambígua: 12%
└─ Satisfação com recomendações: 81%

DEPOIS (com Structured Generation):
├─ Taxa de erro (recomendações inválidas): 0.3% (-96% 🎉)
├─ Taxa de fallback manual (ops intervention): 0.1% (-97% 🎉)
├─ Tempo de integração com backend: 5min (JSON direto) (-89% 🎉)
├─ Retrabalho por resposta ambígua: 0% (-100% 🎉)
└─ Satisfação com recomendações: 98% (+17pp 🎉)
```

---

### Padrão 3: **State Persistence (Memory Entre Turnos)** 💾

#### O Problema (Com Perspectiva Estratégica)

Um cliente chega, fala seus problemas. KODA entende, recomenda, tudo perfeito.

Mas 5 minutos depois, mesmo cliente volta. E KODA... pergunta tudo de novo.

Do ponto de vista de **negócio**: cliente fica frustrado. Sente que ninguém o "conhece". Churn.

Do ponto de vista de **técnica**: contexto da conversa anterior foi perdido porque não foi persistido.

#### A Solução

Estruturar e persistir o **estado do conhecimento** entre mensagens:
- Preferências confirmadas do cliente
- Decisões já tomadas
- Restrições (alergias, budget, etc)
- Compromissos feitos ("vamos enviar em 4 horas")

Guardar isso em arquivo ou banco de dados de forma **estruturada e recuperável**.

#### Exemplos Progressivos

**NÍVEL 1: Exemplo Simples (Para Iniciantes)**

```yaml
# conversation_state.json
{
  "conversation_id": "conv_12345",
  "client_id": "client_67890",
  "session_started_at": "2026-05-25T14:00:00Z",
  
  "confirmed_preferences": {
    "dietary_restrictions": ["gluten_free"],
    "flavor_preference": "chocolate",
    "budget_range": "R$50-R$150"
  },
  
  "decisions_made": [
    {
      "decision": "recommend_product_SKU123",
      "timestamp": "2026-05-25T14:30:00Z",
      "reasoning": "matches all preferences, in stock, within budget"
    }
  ],
  
  "commitments": [
    {
      "commitment": "deliver_same_day",
      "deadline": "2026-05-25T20:00:00Z",
      "status": "in_progress"
    }
  ],
  
  "last_update": "2026-05-25T14:35:00Z"
}
```

**NÍVEL 2: Implementação Realista (Para Devs Mid-Level)**

```python
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import json
import sqlite3

@dataclass
class ConversationState:
    """Estado persistente de uma conversa com cliente."""
    conversation_id: str
    client_id: str
    session_started_at: str
    
    confirmed_preferences: Dict = None
    decisions_made: List[Dict] = None
    commitments: List[Dict] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.confirmed_preferences is None:
            self.confirmed_preferences = {}
        if self.decisions_made is None:
            self.decisions_made = []
        if self.commitments is None:
            self.commitments = []
        if self.metadata is None:
            self.metadata = {}

class StateManager:
    """Gerencia persistência de estado de conversa."""
    
    def __init__(self, db_path: str = "conversation_states.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Cria tabela se não existir."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_states (
                    conversation_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    INDEX idx_client_id (client_id)
                )
            """)
            conn.commit()
    
    def load_or_create(self, conversation_id: str, client_id: str) -> ConversationState:
        """Carrega estado existente ou cria novo."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT state_json FROM conversation_states WHERE conversation_id = ?",
                (conversation_id,)
            ).fetchone()
        
        if row:
            state_dict = json.loads(row[0])
            return ConversationState(**state_dict)
        else:
            # Novo estado
            return ConversationState(
                conversation_id=conversation_id,
                client_id=client_id,
                session_started_at=datetime.now().isoformat()
            )
    
    def load_by_client(self, client_id: str) -> Optional[ConversationState]:
        """Carrega conversa mais recente deste cliente."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """SELECT state_json FROM conversation_states 
                   WHERE client_id = ? 
                   ORDER BY updated_at DESC 
                   LIMIT 1""",
                (client_id,)
            ).fetchone()
        
        if row:
            state_dict = json.loads(row[0])
            return ConversationState(**state_dict)
        return None
    
    def save(self, state: ConversationState) -> None:
        """Persiste estado ao banco."""
        state_json = json.dumps(asdict(state), indent=2, default=str)
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO conversation_states 
                (conversation_id, client_id, state_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                state.conversation_id,
                state.client_id,
                state_json,
                state.session_started_at,
                now
            ))
            conn.commit()
    
    def update_preference(
        self, 
        conversation_id: str, 
        preference_key: str, 
        preference_value: any
    ) -> None:
        """Atualiza preferência específica."""
        state = self.load_or_create(conversation_id, "")
        state.confirmed_preferences[preference_key] = preference_value
        state.metadata["last_preference_update"] = datetime.now().isoformat()
        self.save(state)
    
    def add_decision(
        self,
        conversation_id: str,
        decision: str,
        reasoning: str
    ) -> None:
        """Adiciona decisão ao estado."""
        state = self.load_or_create(conversation_id, "")
        state.decisions_made.append({
            "decision": decision,
            "timestamp": datetime.now().isoformat(),
            "reasoning": reasoning
        })
        self.save(state)
    
    def add_commitment(
        self,
        conversation_id: str,
        commitment: str,
        deadline: str,
        status: str = "pending"
    ) -> None:
        """Adiciona compromisso (ex: prazo de entrega)."""
        state = self.load_or_create(conversation_id, "")
        state.commitments.append({
            "commitment": commitment,
            "deadline": deadline,
            "status": status,
            "created_at": datetime.now().isoformat()
        })
        self.save(state)

# USO EM PRODUÇÃO:
state_manager = StateManager()

# Cliente retorna: carregar seu histórico
previous_state = state_manager.load_by_client("client_67890")

if previous_state:
    context_for_model = f"""
CLIENT PREFERENCES (Previously Confirmed):
{json.dumps(previous_state.confirmed_preferences, indent=2)}

PREVIOUS DECISIONS:
{json.dumps(previous_state.decisions_made[-3:], indent=2)}

OUTSTANDING COMMITMENTS:
{json.dumps(previous_state.commitments, indent=2)}
    """
    print("👋 Olá! Reconheço você de antes!")
else:
    context_for_model = "NEW CLIENT - Primeira conversa"
    print("👋 Bem-vindo!")

# Depois de tomar uma decisão, persistir
state_manager.add_decision(
    conversation_id="conv_12345",
    decision="recommend_product_SKU123",
    reasoning="matches gluten_free preference, chocolate flavor, within budget"
)

# Depois de fazer um compromisso, persistir
state_manager.add_commitment(
    conversation_id="conv_12345",
    commitment="deliver_same_day",
    deadline="2026-05-25T20:00:00Z"
)
```

**GOTCHA: Erros Comuns Neste Padrão**

❌ **Engano 1:** Persistir estado bruto, sem estrutura
- Você salva "conversa completa" como texto
- Impacto: Difícil consultar, difícil validar, difícil auditar

✅ **Solução:** Estruturar estado com campos bem-definidos (preferences, decisions, commitments)

❌ **Engano 2:** Não gerenciar "expiração" de estado
- Preferências de 1 ano atrás ainda sendo usadas
- Impacto: Contexto desatualizado leva a recomendações erradas

✅ **Solução:** Adicionar `confidence_score` e `last_confirmed_date` para cada preferência

❌ **Engano 3:** Nunca auditar o que foi persistido
- Você não consegue rastrear por que foi feita uma recomendação específica
- Impacto: Impossível explicar ao cliente ou regulador

✅ **Solução:** Log completo: quem fez decisão, quando, por quê, e com qual confidence

#### Trade-offs

| Padrão | Interação | Impacto |
|--------|-----------|--------|
| **History Windowing** | Complementar | State complementa windowing com metadados persistidos |
| **Output Validation** | Compatível | Output validado antes de persistir no estado |
| **Fallback & Retry** | Compatível | Fallback usa estado anterior como referência |
| **Guardrails** | Crítico | Guardrails validam estado antes de usar |

#### Impacto em KODA (+ Métricas)

```
ANTES (sem State Persistence):
├─ Tempo de reconhecimento de cliente: N/A (sempre novo)
├─ Taxa de repetição de perguntas: 35% (pergunta mesma coisa 2x)
├─ Conformidade com preferências passadas: 62%
└─ Confiança cliente em recomendações: 71%

DEPOIS (com State Persistence):
├─ Tempo de reconhecimento de cliente: <1s (lookup BD) 🎉
├─ Taxa de repetição de perguntas: 2% (-97% 🎉)
├─ Conformidade com preferências passadas: 99% 🎉
└─ Confiança cliente em recomendações: 96% (+25pp 🎉)
```

---

### Padrão 4: **Fallback & Retry** 🔄

#### O Problema

Seu agente está processando. Tudo funciona... até não funcionar.

Token limit foi atingido. Modelo retornou resposta inválida. Network falhou. API do backend está lenta.

Se você não tiver estratégia de fallback:
- Cliente vê erro
- Conversa morre
- Tíquete entra na fila manual
- Alguém precisa investigar

Do ponto de vista de **negócio**: cada fallback que você não trata custa horas de operações.

#### A Solução

Definir **escaladas inteligentes**:
1. **Retry com novo prompt** (às vezes, re-pedir é suficiente)
2. **Fallback para recomendação segura** (se tudo falhar, retorn padrão confiável)
3. **Escalada para humano** (se fallback também falhar, vira ticket)

#### Exemplo Realista

```python
class AgentWithFallback:
    """Agente com retry/fallback automático."""
    
    MAX_RETRIES = 3
    FALLBACK_RECOMMENDATION = {
        "product_id": "DEFAULT-SAFE-SKU",
        "product_name": "Default Recommendation",
        "reason": "System unable to generate recommendation",
        "confidence": 0,
        "status": "fallback"
    }
    
    def recommend_with_resilience(self, client_id: str) -> dict:
        """Tenta gerar recomendação, com fallbacks."""
        
        for attempt in range(self.MAX_RETRIES):
            try:
                # Tenta gerar recomendação
                recommendation = self.generate_recommendation(client_id)
                
                # Valida
                self.validate_recommendation(recommendation)
                
                return recommendation  # ✅ Sucesso!
            
            except ValueError as e:
                # Erro validação - tenta novamente
                print(f"⚠️ Attempt {attempt + 1}/{self.MAX_RETRIES} failed: {e}")
                
                if attempt < self.MAX_RETRIES - 1:
                    # Re-tentar com prompt mais específico
                    time.sleep(0.5)  # Backoff
                    continue
                else:
                    # Todas tentativas falharam - fallback
                    print("❌ All retries failed - using fallback")
                    return self.FALLBACK_RECOMMENDATION
            
            except Exception as e:
                # Erro inesperado - escalate
                print(f"🚨 Unexpected error: {e}")
                self.escalate_to_human(client_id, reason=str(e))
                return self.FALLBACK_RECOMMENDATION
```

---

### Padrão 5: **Guardrails & Constraints** 🛑

#### O Problema

Seu modelo está gerando recomendações. Mas às vezes:
- Promete desconto de 80% (quando máximo é 20%)
- Recomenda produto que está out-of-stock
- Compromete prazo impossível (4h para delivery internacional)

Do ponto de vista de **negócio**: cada prometimento inviável é uma falha de operação e possível chargeback.

#### A Solução

Antes que o modelo gere resposta, **definir constraints** claros:

```python
constraints = {
    "available_products": get_products_in_stock(),  # Apenas estes 15 produtos
    "max_discount": 0.20,  # Máximo 20% de desconto
    "delivery_time_range": (4, 48),  # 4-48 horas apenas
    "max_price_budget": client_budget * 1.1,  # Até 10% acima do budget
}

prompt = f"""
You are KODA. Follow these STRICT constraints:
- ONLY recommend products from: {constraints['available_skus']}
- Maximum discount: {constraints['max_discount']*100}%
- Delivery time: {constraints['delivery_time_range'][0]}-{constraints['delivery_time_range'][1]} hours
- Never exceed budget: R${constraints['max_price_budget']}

If you cannot satisfy constraints, explain why instead of violating them.
"""
```

---

## 🌉 Introdução ao Conceito: Generator vs. Evaluator (Expandido)

Todos os 5 padrões acima fazem **basicamente a mesma coisa**: colocam guardrails ao redor do modelo.

Mas há uma forma **mais sofisticada** de pensar sobre isso.

### A Estrutura Generator/Evaluator

Em vez de um único modelo fazendo tudo, divida em **dois papéis**:

```
INPUT
  │
  ▼
┌──────────────────────────┐
│  GENERATOR               │
│  (Gera 3+ opções)        │
│  - Criativo              │
│  - Rápido                │
│  - Às vezes impreciso    │
└────────────┬─────────────┘
             │
             ▼
      [Opções A, B, C]
             │
             ▼
┌──────────────────────────┐
│  EVALUATOR               │
│  (Avalia cada opção)     │
│  - Crítico               │
│  - Cuidadoso             │
│  - Seguro                │
└────────────┬─────────────┘
             │
             ▼
OUTPUT (A melhor opção, verificada)
```

### Por Que Funciona?

O modelo é excelente em **gerar ideias** mas não é confiável em **avaliar suas próprias ideias**.

É como pedir ao mesmo pintor para pintar um quadro **e** avaliar se ficou bom. Melhor ter dois: um que pinta criativamente, outro que avalia criticamente.

### Exemplo com KODA

```python
# GERADOR: Cria 3 recomendações diferentes
generator_prompt = """
Generate 3 DIFFERENT product recommendations for this customer.
Be creative - they should be different approaches.

Customer preferences: {preferences}

Return JSON:
[
  {"product_id": "...", "reasoning": "..."},
  {"product_id": "...", "reasoning": "..."},
  {"product_id": "...", "reasoning": "..."}
]
"""

candidates = call_claude(generator_prompt)
# Resultado: 3 opções bem diferentes

# AVALIADOR: Qual é melhor?
evaluator_prompt = f"""
You are a CRITICAL evaluator. Given these 3 candidates:
{candidates}

For EACH, score 0-100:
- Does it match customer preferences? (weight: 40%)
- Is it in stock? (weight: 30%)
- Is it within budget? (weight: 20%)
- Is it a good value? (weight: 10%)

Return the ID of the BEST option with reasoning.
"""

best = call_claude(evaluator_prompt)
# Resultado: "produto_A é melhor porque X, Y, Z"
```

**Vantagem:**
- Você vai de "1 chance de acertar" para "3 chances"
- Avaliação é mais rigorosa
- Qualidade sobe em ~40-50%

Você vai aprender isso em profundidade no **Nível 2**. Por enquanto, saiba que é assim que os agentes mais confiáveis funcionam.

---

## 📊 Seção Nova: Métricas de Sucesso

Como você sabe se seu harness está funcionando? Aqui estão as métricas-chave:

### Métricas por Padrão

| Padrão | Métrica Principal | Alvo | Como Medir |
|--------|------------------|------|-----------|
| **History Windowing** | Tokens economizados | 40-60% redução | (tokens_before - tokens_after) / tokens_before |
| **Structured Generation** | Taxa de erro (output inválido) | <1% | invalid_responses / total_responses |
| **State Persistence** | Taxa de contexto perdido | 0% | requests_that_reask / total_requests |
| **Fallback & Retry** | Taxa de sucesso após retry | >90% | successful_after_retry / total_retries |
| **Guardrails** | Violações de constraint | 0% | constraint_violations / total_operations |

### Dashboard Mental Para Monitorar

```
🎯 SAÚDE GERAL DO HARNESS

✅ Disponibilidade:     99.8% (↑ de 97.2%)
✅ Latência P95:        2.1s (↓ de 4.3s)
✅ Taxa de Erro:        0.3% (↓ de 8.2%)
✅ Custo por Request:   R$0.12 (↓ de R$0.35)
✅ Satisfação:          96% (↑ de 71%)

⚠️  Alertas:
    - History Windowing: 15% dos requests atingem limit (normal)
    - Fallback: 2.1% usando fallback (ideal: <3%)
```

---

## ⚖️ Seção Nova: Trade-offs Comparativos

Nenhum padrão é "melhor" universalmente. Eles fazem trade-offs:

| Dimensão | History Windowing | Structured Output | State Persistence | Fallback | Guardrails |
|----------|-------------------|-------------------|-------------------|----------|------------|
| **Custo Computacional** | Médio (resumo) | Baixo (validação) | Médio (I/O) | Alto (retry) | Baixo |
| **Latência** | Melhora em +30% | Sem mudança | +10% (DB lookup) | Piora em +50% se retry | Sem mudança |
| **Complexidade Código** | Médio | Médio-Alto | Alto | Médio | Médio |
| **Impacto Qualidade** | Alto | Crítico | Alto | Alto | Crítico |

### Combinações Ótimas

**Para Conversas Longas (4+ horas):**
- History Windowing + State Persistence + Structured Output
- Fallback como segurança

**Para Transações de Alto Risco:**
- Structured Output + Guardrails + Fallback
- State Persistence para rastreamento

**Para Produção em Escala:**
- Todos os 5 padrões combinados (KODA usa assim)

---

## 🚨 Seção Nova: Gotchas & Armadilhas Comuns

### Top 10 Erros ao Implementar Harnesses

**1. Resumir demais (ou de menos)**
- ❌ Resumo com 50 palavras → perde contexto crítico
- ❌ Resumo com 5000 tokens → não economiza nada
- ✅ Alvo: 2-3K tokens de resumo comprimido

**2. Confiar que JSON válido = business válido**
- ❌ Output é JSON perfeito mas viola regras de negócio
- ✅ Sempre validar constraints APÓS parsear JSON

**3. Não registrar por que fallen back**
- ❌ Você não consegue debugar o porquê de ter usado fallback
- ✅ Log completo: tentativa, erro, fallback usado

**4. Deixar estado crescer infinitamente**
- ❌ Histórico de decisões de 2 anos atrás ainda ativo
- ✅ Arquivar estado antigo, guardar apenas últimos 3-6 meses

**5. Retry sem backoff exponencial**
- ❌ Retry imediatamente → sobrecarrega sistema
- ✅ Backoff: 100ms, 500ms, 2s

**6. Generator/Evaluator no mesmo turno**
- ❌ Gera 3 opções E avalia tudo em 1 request
- ✅ Separar: generator cria em 1 request, evaluator em 2º

**7. Não testar fallback em produção**
- ❌ Fallback nunca foi usado → falha quando precisa
- ✅ Teste fallback regularmente (chaos engineering)

**8. Output validation muito lenient**
- ❌ "Qualquer JSON válido é ok"
- ✅ Validar cada campo com Pydantic/TypeScript

**9. Guardrails no prompt vs código**
- ❌ "Never exceed 20% discount" apenas no prompt
- ✅ Validar constraints também em código após geração

**10. Não medir antes/depois**
- ❌ "Achamos que melhorou"
- ✅ Dados concretos: latência, erro rate, custo

---

## 🧠 Reflexão Estratégica Expandida: A Diferença Entre Prototipo e Produto

Muitas pessoas acham que a diferença entre um **protótipo de agente** e um **agente em produção** é a qualidade do modelo.

Errado. Muito errado.

A diferença é o **harness**.

### A Evolução de um Agente

```
FASE 1: Protótipo (Dias 1-5)
┌─────────────────┐
│ Input → Claude → Output
└─────────────────┘
✅ Funciona. Pronto!
❌ Falha frequente. Perda de contexto. Decisões inconsistentes.

FASE 2: MVP (Semanas 1-2)
┌──────────────────────────────────────────┐
│ Validação → Claude → Validação → Fallback │
└──────────────────────────────────────────┘
✅ Mais robusto.
❌ Ainda perde contexto em conversas longas.

FASE 3: Produto (Semanas 3-8)
┌─────────────────────────────────────────────────────────────┐
│ Validação → Histórico → Estado → Claude → Validação →      │
│ → Guardrails → Fallback → Persistência → Output            │
└─────────────────────────────────────────────────────────────┘
✅ Pode rodar 4+ horas. Contexto nunca é perdido. Decisões consistentes.
```

### A Lição de Fernando

Fernando Machado entendeu isso quando lançou KODA. 

**Não era sobre ter o melhor modelo.** Existem vários modelos bons.

**Era sobre construir a estrutura correta ao redor dele.**

KODA usa:
- History Windowing para conversas longas
- Structured Output para integração com backend
- State Persistence para memória entre turnos
- Fallback & Retry para robustez
- Guardrails para compliance

Resultado? Um agente que funciona **em produção real, processando milhares de pedidos por dia, com taxa de erro <1%.**

É por isso que KODA funciona enquanto agentes similares (feitos por outras pessoas) desabam.

**Harnesses ganham produtos.**

### A Mentalidade Correta

Quando você está construindo um agente:

1. **Não comece com "qual modelo usar?"**
2. **Comece com "qual estrutura preciso?"**
3. **Então escolha o modelo.**

Porque a estrutura é reutilizável. O modelo vai mudar. Em 2 anos, Claude 5 ou Claude 7 será o padrão. Mas o harness vai continuar valendo.

---

## 📋 Checklist: Qual Padrão Para Qual Situação?

| Problema | Padrão | Quando Usar | Prioridade |
|----------|--------|----------|-----------|
| Contexto cresce muito | History Windowing | Conversas > 1 hora | ALTA |
| Output é imprevisível | Structured Generation | Qualquer integração com sistema | CRÍTICA |
| Perdi informações críticas | State Persistence | Qualquer conversa multi-turno | ALTA |
| Modelo às vezes erra | Fallback & Retry | Sempre, em produção | ALTA |
| Modelo promete coisas ilegais | Guardrails & Constraints | Sempre, quando há limites | CRÍTICA |

---

## 🎯 Aplicação em KODA: O Harness Real

KODA não usa apenas 1 padrão. Usa **todos os 5, combinados**, trabalhando em sinergia:

```
Cliente entra no WhatsApp
│
├─ INPUT VALIDATION: Cliente está bloqueado? Pode fazer pedido?
│
├─ HISTORY WINDOWING: 
│  Carregar últimas 20 mensagens + resumo do histórico
│
├─ STATE PERSISTENCE: 
│  Carregar preferências confirmadas (alergias, restrições, budget)
│
├─ CORE (CLAUDE): 
│  "Recomende 3 produtos"
│  └─ (Modelo gera 3 opções diferentes)
│
├─ GENERATOR/EVALUATOR:
│  Avalia qual das 3 é melhor
│  └─ (Seleciona a melhor opção com reasoning)
│
├─ OUTPUT VALIDATION:
│  A recomendação é JSON válido?
│  └─ (Sim → continua. Não → retry)
│
├─ GUARDRAILS: 
│  Produto está em estoque? Preço está no budget?
│  └─ (Sim → continua. Não → usa fallback)
│
├─ FALLBACK: 
│  Se tudo falhou, retorna recomendação padrão segura
│
└─ PERSISTENCE: 
   Salvar estado (qual produto foi recomendado)
   └─ (Cliente pode retomar onde parou)
```

Cada passo é **independente**, **testável** e **confiável**.

Resultado? Um agente que pode rodar **4+ horas contínuas** sem degradação.

---

## 📚 Resumo: Os 5 Padrões em 90 Segundos

| Padrão | Faz O Quê | Por Que Importa | Impacto Típico |
|--------|-----------|-----------------|----------------|
| **History Windowing** | Mantém apenas histórico relevante | Token budgeting sustentável | -60% tokens gastos |
| **Structured Generation** | Força resposta em JSON/XML | Output previsível e parseável | -96% erros output |
| **State Persistence** | Salva decisões críticas em arquivo | Contexto nunca é perdido | +25pp satisfação |
| **Fallback & Retry** | Re-tenta se falhar | Robustez automática | >90% recuperação |
| **Guardrails** | Define constraints no prompt | Impossível violar regras | -99% violações |

---

## 🚀 Próximos Passos

Você aprendeu os **fundamentos** (Nível 1 completado! 🎉).

No **Nível 2**, você vai aprender:
1. **Padrão Generator/Evaluator** em profundidade (como usar para aumentar confiabilidade 2-3x)
2. **Sprint Contracts** (como definir expectativas para seus agentes)
3. **Rubric Design** (como avaliar a qualidade de forma sistemática)
4. **Trace Reading** (como debugar seu agente quando algo dá errado)

Mas primeiro, **implemente um dos padrões** em seu código. Comece com:
- Se conversas são longas → **History Windowing**
- Se integração é crítica → **Structured Generation**
- Se contexto é importante → **State Persistence**

Veja a diferença. Meça antes e depois. Você vai se surpreender.

---

## 💡 Reflexão Final: O Futuro de Agentes em 2026+

Você está num ponto de inflexão histórico.

**Até 2025**, a maioria da atenção era em "qual modelo usar?"

**De 2026 em diante**, a vantagem competitiva é em "qual arquitetura usar?"

Companies que entenderem isso agora vão estar 2-3 anos à frente em 2028.

Harnesses não são "nice-to-have". São o fundamento de qualquer agente em produção.

Dominar isso agora = vantagem estratégica para a próxima década.

---

## 📚 Referências & Recursos

### Papers Relevantes
- "Reliability in Large Language Model-Based Agents" - OpenAI (2024)
- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" - Wei et al. (2022)
- "Structured Outputs for Large Language Models" - Anthropic (2024)

### Ferramentas Recomendadas
- **Pydantic** (Python) - Validação de estruturas
- **TypeScript/Zod** (Node.js) - Validação com type safety
- **Instructor** - Structured outputs para Claude
- **LangChain/LlamaIndex** - Frameworks de persistência

### Repositórios de Exemplo
- FutanBear/koda-harness (exemplo real de KODA)
- Anthropic/anthropic-sdk-python (Claude SDK)
- colinhacks/instructor (structured outputs)

### Comunidade
- [FutanBear Technical Community](https://futanbear.com/community)
- [Anthropic Discord](https://discord.gg/anthropic)

---

## 📝 Exercícios Recomendados

Próximo: Complete os exercícios para consolidar estes conceitos:
- `exercise-01_-_01-nivel-1-fundamentals.md` (History Windowing prático)
- `exercise-02_-_01-nivel-1-fundamentals.md` (Structured Output prático)

---

**Parabéns!** Você completou o **Nível 1: Conceitos Fundamentais** 🎉

Você agora entende:
- ✅ Por que agentes perdem o foco (Context Amnesia + Planning Paralysis)
- ✅ Como gerenciar tokens como orçamento finito
- ✅ Quais padrões de harness usar (5 padrões, 90% dos problemas)

**Próximo:** Nível 2 - Padrões Práticos Avançados

Comece em: `01-generator-evaluator-pattern.md`

---

*Módulo 3 de Nível 1 | Curso Long-Running Agents | FutanBear Technical Program*

*Atualizado: Maio 2026 | Profundidade: Iniciantes + Mid-Level Developers | Impacto: Produção em Escala*
