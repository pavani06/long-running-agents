---
title: "Padrões Básicos de Harness: A Estrutura que Sustenta Agentes"
type: source
date: 2026-05-26
tags:
  - curriculo-conteudo
  - agentes-orquestracao
  - harness-engineering
aliases:
  - basic harness patterns
  - padroes de harness
  - estrutura de agentes
relates-to:
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution]]"
  - "[[curriculum/05-core-concepts/06-harness-evolution|Harness Evolution]]"
---

# 🏗️ Padrões Básicos de Harness: A Estrutura que Sustenta Agentes
## Como Construir um "Sistema Imunológico" para Agentes de Longa Duração

**Tempo Estimado:** 45 minutos  
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

KODA começou simples - apenas um chatbot respondendo perguntas. Mas para se tornar um **sistema confiável que processa milhares de pedidos por dia**, precisava de um harness sofisticado.

Este módulo vai revelar os padrões mais simples (e mais poderosos) que você pode usar começando hoje.

---

## 🎯 O Que É um Harness?

### Definição Simples

Um **harness** é um conjunto de padrões, estruturas e validações que cercam o núcleo do agente (o LLM) para melhorar sua confiabilidade.

**Analogia:** 
- O **núcleo** = o modelo Claude (poderoso mas não determinístico)
- O **harness** = os guardrails que transformam um modelo em um **produto confiável**

```
┌─────────────────────────────────────────────────┐
│           MUNDO REAL (Cliente/Sistema)          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  INPUT VALIDATION (Verificar dados de entrada)  │
├─────────────────────────────────────────────────┤
│  CONTEXT MANAGEMENT (Gerenciar histórico)       │
├─────────────────────────────────────────────────┤
│  [MODELO CLAUDE - O NÚCLEO]                     │
├─────────────────────────────────────────────────┤
│  OUTPUT VALIDATION (Verificar resposta)         │
├─────────────────────────────────────────────────┤
│  PERSISTENCE LAYER (Guardar estado)             │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│     RESULTADO DETERMINÍSTICO (Produto Seguro)   │
└─────────────────────────────────────────────────┘
```

### Componentes Essenciais de um Harness

Um harness bem-desenhado tem **3 camadas obrigatórias:**

#### 1️⃣ **Input Layer** - O Que Entra
O agente recebe dados. Antes que qualquer token seja processado:
- Validar que os dados são bem-formados
- Extrair contexto relevante
- Preparar o histórico de forma otimizada
- Aplicar restrições de negócio (ex: não processar se cliente está bloqueado)

**Impacto:** Evita que o modelo processe "lixo" que o confunde

#### 2️⃣ **Core Layer** - O Processamento
Este é onde o Claude roda. Mas não roda sozinho:
- System prompt bem-definido
- Histórico contexto curado
- Chain-of-thought ou reasoning estruturado
- Tokens orçados inteligentemente

**Impacto:** Melhor qualidade de output, menos alucinações

#### 3️⃣ **Output Layer** - O Que Sai
A resposta do modelo é checada antes de chegar ao cliente:
- Validar que a resposta segue o formato esperado
- Verificar se faz sentido semanticamente
- Aplicar guardrails de segurança
- Persistir o estado para a próxima interação

**Impacto:** Evita respostas perigosas, contraditórias ou insensatas

---

## 🔌 Os 5 Padrões Básicos de Harness

Você não precisa inventar tudo do zero. Existem 5 padrões que resolvem **90% dos problemas** em agentes de longa duração. Todos ao seu alcance hoje.

### Padrão 1: **History Windowing** 🪟
#### O Problema
Contexto cresce infinitamente. Token budgeting fica insustentável.

#### A Solução
Em vez de manter **toda** a conversa, mantenha apenas:
- Os últimos **K mensagens** (janela deslizante)
- Um **resumo comprimido** do histórico antigo
- **Metadados críticos** (decisões já tomadas, commitments feitos)

#### Exemplo com KODA

```
Conversa com cliente durante 4 horas = 2000+ mensagens potenciais

❌ INEFICIENTE (Manter tudo):
Histórico completo = 120K tokens
Buffer de resposta = 20K tokens
Novo input = 2K tokens
TOTAL = 142K tokens de 200K disponíveis (71% gastos)

✅ EFICIENTE (History Windowing):
Últimas 20 mensagens = 15K tokens
Resumo do histórico antigo = 5K tokens
Metadados críticos = 2K tokens
Buffer de resposta = 20K tokens
Novo input = 2K tokens
TOTAL = 44K tokens de 200K disponíveis (22% gastos)
```

**Como Implementar:**
1. Manter janela deslizante de últimas 15-20 mensagens
2. Gerar resumo estruturado a cada 30 minutos
3. Incluir no resumo: decisões principais, preferências, commitments
4. Descartar histórico antigo (mas guardar em arquivo para auditoria)

**Impacto em KODA:**
- Cliente pode ter conversas de 4+ horas sem degradação
- Menos custo por token
- Melhor performance (respostas mais rápidas)

---

### Padrão 2: **Output Validation (Structured Generation)** ✅
#### O Problema
Modelo gera texto livre. Às vezes, não faz sentido. Às vezes, é contraditório com decisões anteriores.

#### A Solução
Força o modelo a responder em **formato estruturado** (JSON, XML, etc):
- Campo: "recommendation" (qual produto recomendar)
- Campo: "reasoning" (por que este produto)
- Campo: "alternatives" (alternativas consideradas)
- Campo: "confidence" (0-100%, o modelo valida sua própria confiança)

#### Exemplo com KODA

```
❌ SEM ESTRUTURA (Perigoso):
[Modelo responde em texto livre]
"Acho que você ia gostar de whey protein da marca X..."
[Pode fazer uma recomendação que contradiz preferências do cliente]

✅ COM ESTRUTURA (Seguro):
{
  "recommendation": {
    "product_id": "SKU-12345",
    "product_name": "Whey Protein Chocolate 1kg",
    "reason": "matches_dietary_restriction=true, price_range=true, in_stock=true"
  },
  "alternatives": [
    {"product_id": "SKU-12346", "reason": "higher_protein_per_serving"}
  ],
  "confidence": 92,
  "contradicts_previous_preferences": false
}
```

**Como Implementar:**
1. Definir schema JSON do que espera como resposta
2. Incluir no prompt: "Responda APENAS em JSON válido"
3. Validar resposta após geração
4. Se não é JSON válido, re-tentar com novo prompt mais específico

**Impacto em KODA:**
- Respostas previsíveis e parseáveis
- Fácil validar se recomendação faz sentido
- Integração com sistemas backend sem erro

---

### Padrão 3: **State Persistence (Memory Entre Turnos)** 💾
#### O Problema
Conversas são sequenciais. Mas contexto é ameaçado de desaparecer.

#### A Solução
Estruturar e persistir o **estado do conhecimento** entre mensagens:
- Preferências confirmadas do cliente
- Decisões já tomadas
- Restrições (alergias, budget, etc)
- Compromissos feitos ("vamos enviar em 4 horas")

Guardar isso em arquivo ou banco de dados de forma **estruturada**.

#### Exemplo com KODA

```yaml
# conversation_state.json
{
  "conversation_id": "conv_12345",
  "client_id": "client_67890",
  
  "confirmed_preferences": {
    "dietary_restrictions": ["gluten_free"],
    "flavor_preference": "chocolate",
    "budget_range": "R$50-R$150"
  },
  
  "decisions_made": [
    {
      "decision": "recommend_product_SKU123",
      "timestamp": "2026-05-25T14:30:00Z",
      "reasoning": "matches all preferences"
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

**Como Implementar:**
1. Após cada mensagem do modelo, extrair e atualizar estado
2. Guardar em arquivo/banco de dados
3. Próxima vez que retomar conversa, carregar esse estado
4. Incluir no prompt novo: "Estado atual do cliente é X"

**Impacto em KODA:**
- Conversa pode ser pausada e retomada sem perder contexto
- Cliente sai e volta no dia seguinte: KODA ainda lembra tudo
- Decisões críticas são auditáveis

---

### Padrão 4: **Fallback & Retry Logic** 🔄
#### O Problema
Às vezes o modelo erra. Às vezes fica confuso. Às vezes o output não é válido.

#### A Solução
Ao invés de falhar, tentar novamente com **estratégia diferente**:
1. **Retry simples:** Se output não é JSON válido, re-tentar mesmo prompt
2. **Retry com ajuste:** Se continuou inválido, re-tentar com prompt mais restritivo
3. **Escalation:** Se ainda falhou, passar para lógica manual ou sugerir ao usuário

#### Exemplo com KODA

```python
def get_product_recommendation(client_state, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = call_claude(prompt, client_state)
            result = parse_json(response)
            
            # Validar estrutura
            if not has_required_fields(result):
                raise ValueError("Missing fields")
            
            # Validar lógica
            if contradicts(result, client_state.preferences):
                raise ValueError("Contradicts preferences")
            
            return result
        
        except Exception as e:
            if attempt < max_retries - 1:
                # Retry com prompt mais específico
                prompt = refine_prompt(prompt, error=str(e))
            else:
                # Escalation: retornar resultado padrão seguro
                return get_default_recommendation(client_state)
```

**Como Implementar:**
1. Envolver chamadas do modelo em try/catch
2. Definir critérios de sucesso (JSON válido? Faz sentido?)
3. Retry até 3 vezes com prompts progressivamente mais específicos
4. Se falhar sempre, usar fallback seguro (recomendação padrão, pedir input manual)

**Impacto em KODA:**
- Robustez: erros ocasionais não quebram o fluxo
- Experiência melhor: cliente raramente vê erro
- Dados para melhoria: você vê quando o modelo falha

---

### Padrão 5: **Guardrails & Constraint Enforcement** 🛑
#### O Problema
Modelo pode fazer coisas erradas:
- Recomendar produto fora de estoque
- Oferecer desconto que não existe
- Fazer promessa que KODA não pode cumprir

#### A Solução
Antes que o modelo gere resposta, **definir constraints** claros:
- Quais produtos pode recomendar? (apenas SKUs em estoque)
- Qual desconto máximo? (máximo 20% ou R$50)
- Qual prazo pode prometer? (mínimo 4 horas, máximo 48 horas)

#### Exemplo com KODA

```python
# Definir constraints antes de chamar o modelo
constraints = {
    "available_skus": get_products_in_stock(),  # Apenas estes 15 produtos
    "max_discount": 0.20,  # Máximo 20% de desconto
    "delivery_time_range": (4, 48),  # 4-48 horas apenas
    "max_price_budget": client_state.budget * 1.1,  # Até 10% acima do budget
}

prompt = f"""
You are KODA. Follow these constraints:
- ONLY recommend products from: {constraints['available_skus']}
- Maximum discount: {constraints['max_discount']*100}%
- Promise delivery time between {constraints['delivery_time_range'][0]} and {constraints['delivery_time_range'][1]} hours
- Never recommend products over: R${constraints['max_price_budget']}

Client preferences: {client_state.preferences}

What is your recommendation?
"""

response = call_claude(prompt)

# Validar que resposta respeita constraints
assert response.product_id in constraints['available_skus']
assert response.discount <= constraints['max_discount']
assert constraints['delivery_time_range'][0] <= response.delivery_time <= constraints['delivery_time_range'][1]
```

**Como Implementar:**
1. Listar todos os constraints do sistema
2. Passar explicitamente no system prompt ou context
3. Após geração, validar que resposta respeita constraints
4. Se viola constraint, re-tentar com prompt mais restritivo

**Impacto em KODA:**
- Impossível fazer promessas ilegais (desconto impossível, frete errado)
- Compliance automático com políticas
- Menos fraude, menos chargebacks

---

## 🌉 Introdução ao Conceito: Generator vs. Evaluator

Antes de fechar este módulo, preciso apresentar a **ideia que vai revolucionar** como você constrói agentes no próximo nível.

Todos os 5 padrões acima fazem **basicamente a mesma coisa**: colocam guardrails ao redor do modelo. Mas há uma forma mais sofisticada de pensar sobre isso.

### A Estrutura Generator/Evaluator

Em vez de um único modelo fazendo tudo, divida em **dois papéis**:

```
INPUT
  │
  ▼
┌─────────────────────────┐
│  GENERATOR              │
│  (Gera opções/ideias)   │
└────────────┬────────────┘
             │
             ▼
         [Opções A, B, C]
             │
             ▼
┌─────────────────────────┐
│  EVALUATOR              │
│  (Valida opções)        │
└────────────┬────────────┘
             │
             ▼
OUTPUT (A opção mais segura)
```

### Por Que Funciona?

O modelo é excelente em **gerar ideias** (Generator), mas não é confiável em **avaliar suas próprias ideias** (Evaluator).

É como pedir ao mesmo pintor para pintar um quadro **e** avaliar se ficou bom. Melhor ter dois: um que pinta criativamente, outro que avalia com crítica.

#### Exemplo com KODA

```python
# GENERATOR: Gerar 3 recomendações diferentes
generator_prompt = """
Generate 3 different product recommendations for this customer.
For each, explain the reasoning.

Customer preferences: {client_preferences}

Response format:
[
  {"product_id": "...", "reasoning": "..."},
  {"product_id": "...", "reasoning": "..."},
  {"product_id": "...", "reasoning": "..."}
]
"""

candidates = call_claude(generator_prompt)
# Result: 3 opções diferentes

# EVALUATOR: Qual é melhor?
evaluator_prompt = f"""
You are a critical evaluator. Given these 3 product recommendations:
{candidates}

For each, score 0-100 based on:
- Does it match customer preferences?
- Is it in stock?
- Is it within budget?
- Is it the best value?

Return the ID of the best option and why.
"""

best_recommendation = call_claude(evaluator_prompt)
# Result: produto_id_A é melhor porque X, Y, Z
```

**Vantagem:** Você vai de 1 chance para acertar, para 3 chances. E depois avalia melhor.

**Você vai aprender isso em profundidade no Nível 2.** Por enquanto, saiba que é assim que os agentes mais confiáveis funcionam.

---

## 📋 Checklist: Qual Padrão Para Qual Situação?

| Problema | Padrão | Quando Usar |
|----------|--------|----------|
| Contexto cresce muito | History Windowing | Conversas > 1 hora |
| Output é imprevisível | Structured Generation | Qualquer integração com sistema |
| Perdi informações críticas | State Persistence | Qualquer conversa multi-turno |
| Modelo às vezes erra | Fallback & Retry | Sempre, em produção |
| Modelo promete coisas ilegais | Guardrails & Constraints | Sempre, quando há limites |

---

## 🎯 Aplicação em KODA: O Harness Real

KODA não usa apenas 1 padrão. Usa **todos os 5, combinados**:

```
Cliente entra no WhatsApp
│
├─ INPUT VALIDATION: Cliente está bloqueado? Pode fazer pedido?
│
├─ HISTORY WINDOWING: Carregar últimas 20 msgs + resumo do histórico
│
├─ STATE PERSISTENCE: Carregar preferências confirmadas (alergias, etc)
│
├─ CORE (CLAUDE): "Recomende 3 produtos"
│  ↓
│  └─ GENERATOR/EVALUATOR: Gera 3, avalia qual é melhor
│
├─ OUTPUT VALIDATION: A recomendação é JSON válido?
│
├─ GUARDRAILS: Produto está em estoque? Preço está no budget?
│
├─ FALLBACK: Se falhou, tenta novamente ou usa recomendação padrão
│
└─ PERSISTENCE: Salvar estado (qual produto foi recomendado)
```

Cada passo é independente, testável e confiável.

Resultado? Um agente que pode rodar **4 horas contínuas** sem degradação.

---

## 📚 Resumo: Os 5 Padrões em 60 Segundos

| Padrão | Faz O Quê | Por Que Importa |
|--------|-----------|-----------------|
| **History Windowing** | Mantém apenas histórico relevante | Token budgeting sustentável |
| **Structured Generation** | Força resposta em JSON/XML | Output previsível e parseável |
| **State Persistence** | Salva decisões críticas em arquivo | Contexto nunca é perdido |
| **Fallback & Retry** | Re-tenta se falhar | Robustez automática |
| **Guardrails** | Define constraints no prompt | Impossível violar regras |

---

## 🚀 Próximos Passos

Você aprendeu os **fundamentos** (Níveis 1 completo agora!). 

No Nível 2, você vai aprender:
1. **Padrão Generator/Evaluator** em profundidade (como usar para aumentar confiabilidade 10x)
2. **Sprint Contracts** (como definir expectativas para seus agentes)
3. **Rubric Design** (como avaliar a qualidade de forma sistemática)
4. **Trace Reading** (como debugar seu agente quando algo dá errado)

Mas primeiro, teste os padrões deste módulo. Implemente um deles em seu código. Veja a diferença.

---

## 💡 Reflexão: A Diferença Entre Prototipo e Produto

Muitas pessoas acham que a diferença entre um **protótipo de agente** e um **agente em produção** é a qualidade do modelo.

Errado.

A diferença é o **harness**.

Um protótipo é:
```
Input → [Claude] → Output
```

Um produto é:
```
Input → [Validação] → [Histórico] → [Estado] → [Claude] → [Validação] 
  → [Constraints] → [Fallback] → [Persistência] → Output
```

Fernando entendeu isso quando lançou KODA. Não era sobre ter o melhor modelo. Era sobre **construir a estrutura correta ao redor dele**.

É por isso que KODA funciona enquanto agentes similares (feitos por outras pessoas) desabam.

Harnesses ganham produtos.

---

## 📝 Exercícios Recomendados

Próximo: Complete `exercices/exercise-01_-_01-nivel-1-fundamentals.md` e `exercise-02_-_01-nivel-1-fundamentals.md` para consolidar estes conceitos.

---

**Parabéns!** Você completou o **Nível 1: Conceitos Fundamentais**.

Você agora entende:
- ✅ Por que agentes perdem o foco
- ✅ Como gerenciar tokens como orçamento
- ✅ Quais padrões de harness usar

**Próximo:** Nível 2 - Padrões Práticos (comece em `01-generator-evaluator-pattern.md`)

---

*Módulo 3 de Nível 1 | Curso Long-Running Agents | FutanBear Technical Program*
