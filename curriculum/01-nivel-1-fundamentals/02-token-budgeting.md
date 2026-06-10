---
title: "Token Budgeting: O Orçamento Invisível dos Agentes"
type: curriculum-lesson
nivel: 1
aliases: []
tags: [curriculo-conteudo, nivel-1, fundamentos, orcamento-de-tokens, gestao-de-contexto, burn-rate, janela-movel, buffer-de-resposta, buffer-de-resumo, compressao-de-contexto, agrupamento-semantico, estrategia-hibrida, monitoramento-proativo]
last_updated: 2026-06-10
---
# 💰 Token Budgeting: O Orçamento Invisível dos Agentes
## Como Gerenciar Tokens como um CFO Gerencia Dinheiro

**Tempo Estimado:** 45 minutos  
**Nível:** 1 - Conceitos Fundamentais  
**Pré-requisito:** Ter lido `01-why-agents-lose-plot.md`  
**Status:** 🟢 ESSENCIAL - A chave para agentes de longa duração  

---

## 📖 Prólogo: O Orçamento Invisível

Fernando é um empreendedor experiente. Quando lançou a KODA, ele não pensava apenas em funcionalidades bonitas. Ele pensava como um CFO:

> *"Se cada conversa com um cliente custa tokens, e tokens têm um limite, então temos um orçamento. Como qualquer negócio, precisamos entender esse orçamento, priorizá-lo e não desperdaçá-lo."*

Este é o pensamento que diferencia agentes que **podem rodar por horas** de agentes que **desabam após 30 minutos**.

**A pergunta central é:** Você sabe quanto "dinheiro" seus agentes estão gastando a cada resposta?

Se a resposta é não, este módulo vai mudar sua forma de pensar sobre long-running agents.

---

## 🎯 O Que É Token Budgeting?

### Definição Simples
**Token budgeting** é a prática de planejar, alocar e controlar o uso de tokens ao longo de uma conversa ou sessão de um agente.

Assim como:
- Um governo tem um orçamento anual (exemplo: $1 trilhão)
- Uma família tem um orçamento mensal (exemplo: R$ 5.000)
- Uma startup tem um orçamento de runway (exemplo: 18 meses de cash)

Um agente tem um **orçamento de tokens** por conversa:
- **Total disponível:** Seu context window
- **Já gasto:** Tudo que foi processado até agora
- **Disponível para o futuro:** Espaço para novas mensagens + respostas

### A Equação Fundamental

```
ESPAÇO DISPONÍVEL = TOTAL DO CONTEXTO - HISTÓRICO JÁ PROCESSADO - BUFFER DE RESPOSTA
```

Exemplo com Claude Sonnet 4.6:
```
200,000 (total)
-  80,000 (histórico já processado em 1 hora de conversa)
-  15,000 (buffer para gerar resposta de qualidade)
─────────────────
= 105,000 tokens restantes para continuar
```

---

## 📊 Os 4 Componentes do Orçamento

Quando você pensa em token budgeting, há 4 componentes que precisam trabalhar juntos:

### 1️⃣ Input Tokens (O Que Entra)
**O que são:** Tokens que o modelo processa como entrada.

**Composition em uma conversa típica:**
```
Input Tokens = Histórico + Instrução do Sistema + Instrução do Prompt
```

**Exemplo KODA:**
```
Histórico:    45,000 tokens (toda conversa anterior)
System:        2,000 tokens ("Você é KODA, um assistente...")
Prompt:        1,500 tokens (responda pergunta sobre whey protein)
─────────────────────────
Total Input:  48,500 tokens
```

**Impacto em Long-Running:**
- Cada nova mensagem do cliente = ~100-300 tokens
- Histórico cresce a cada troca
- Por isso conversas de 2 horas alcançam 60-80K tokens

---

### 2️⃣ Output Tokens (O Que Sai)
**O que são:** Tokens gerados pelo modelo como resposta.

**Características:**
- Não sabemos exatamente quanto será gerado até ser gerado
- Precisamos reservar espaço em advance (buffer)
- Uma resposta "boa" geralmente precisa de 200-1000 tokens

**Exemplo KODA:**
```
Pergunta: "Qual whey protein vocês recomendam para ganho muscular?"

Resposta típica: ~400-600 tokens
(
  Olá! Para ganho muscular, recomendo...
  [análise de 3 opções]
  [preços e promoções]
  [detalhes de frete]
)
```

**Impacto em Long-Running:**
- Se cada resposta = 500 tokens
- E temos 30 trocas na conversa
- Consumimos 15K tokens só em respostas

---

### 3️⃣ Context Window (O Limite)
**O que é:** A quantidade máxima de tokens que o modelo pode processar.

**Modelos atuais (Maio 2026):**
```
┌──────────────────────────────────┬──────────────┐
│ Modelo                           │ Context      │
├──────────────────────────────────┼──────────────┤
│ Claude Opus 4.6                  │ 1,000,000    │
│ Claude Sonnet 4.6                │ 200,000      │
│ Claude Haiku 4.5                 │ 100,000      │
└──────────────────────────────────┴──────────────┘
```

**Para conversação em KODA:**
- Usamos tipicamente **Sonnet 4.6** (200K tokens)
- Em tempo real (baixa latência) importante
- Equilíbrio entre custo e capacidade

---

### 4️⃣ Burn Rate (Taxa de Consumo)
**O que é:** Quanto rápido você consome tokens.

**Fórmula:**
```
Burn Rate = (Input + Output) / Minutos de Conversa
```

**Exemplo real de KODA:**
```
Conversa de 60 minutos:
- Input total:  80,000 tokens (histórico + prompts)
- Output total: 10,000 tokens (respostas geradas)
- Tempo:        60 minutos

Burn Rate = (80,000 + 10,000) / 60 = 1,500 tokens/min
```

**Por que é importante?**
- Saber quantos minutos você pode continuar
- Planejar quando fazer "compactação"
- Entender quando mudar de estratégia

---

## 🚨 O Problema do Over-Budgeting

Muitos developers cometem o mesmo erro: alocar tokens demais sem planejamento.

### Anti-pattern Clássico: O "Histórico Completo"

```python
# ❌ RUIM - Passa histórico completo SEMPRE
system_prompt = "Você é KODA..."
full_history = get_all_messages_ever()  # 80K tokens!
current_message = user_input

response = claude.invoke(
    system=system_prompt,
    messages=full_history + [current_message]
)
```

**Consequências:**
1. Primeiros 5 minutos: Excelente (contexto fresco)
2. 30 minutos depois: Começam bugs
3. 60 minutos depois: CRASH (contexto explodiu)

### O Padrão Correto: O "Histórico Seletivo"

```python
# ✅ BOM - Usa histórico inteligentemente
system_prompt = "Você é KODA..."

# Pega últimas N mensagens (últimas 2 horas)
recent_history = get_recent_messages(minutes=120)

# Adiciona context crítico do cliente
critical_context = {
    "alergias": client.allergies,
    "orçamento": client.budget,
    "histórico_compras": client.purchase_history
}

messages = [
    {"role": "system", "content": critical_context},
    ...recent_history,
    {"role": "user", "content": current_message}
]

response = claude.invoke(
    system=system_prompt,
    messages=messages
)
```

---

## 💡 5 Estratégias de Token Budgeting

### Estratégia 1: The Windowed History (Janela Móvel)
**Ideia:** Manter apenas últimas N mensagens em contexto.

```
Tempo 0:        Contexto = [ ]
Tempo 10 min:   Contexto = [msg1, msg2, msg3]
Tempo 20 min:   Contexto = [msg2, msg3, msg4]  ← msg1 removida
Tempo 30 min:   Contexto = [msg3, msg4, msg5]  ← msg2 removida
```

**Implementação:**
```python
def get_windowed_history(conversation, window_messages=20):
    """Pega apenas as últimas N mensagens"""
    return conversation[-window_messages:]
```

**Trade-offs:**
- ✅ Controle perfeito de tokens
- ✅ Previsível e simples
- ❌ Perde contexto muito antigo
- ❌ Pode não funcionar para dependências antigas

**Melhor para:** Conversas muito longas (3+ horas)

---

### Estratégia 2: The Summary Buffer (Buffer de Resumo)
**Ideia:** Manter história completa resumida em parágrafo.

```
Histórico Completo (80K tokens):
[toda conversa de 2 horas]
    ↓ (resumir periodicamente)
Resumo (2K tokens):
"Cliente é alérgico a glúten, orçamento de R$200,
 preferência por marcas premium, entregaria em SP"
```

**Implementação:**
```python
def create_summary_buffer(conversation, summary_interval=50):
    """A cada 50 mensagens, resumir tudo"""
    if len(conversation) % summary_interval == 0:
        summary = claude.invoke(
            "Resuma TODA esta conversa em 3 parágrafos, "
            "focando em informações críticas para o cliente.",
            conversation
        )
        return summary
    return None
```

**Trade-offs:**
- ✅ Mantém informações importante
- ✅ Reduz tokens dramaticamente
- ✅ Flexível - pode fazer múltiplas vezes
- ❌ Resumo pode perder nuances
- ❌ Requer API call extra

**Melhor para:** Conversas de 1-3 horas com muitos detalhes

---

### Estratégia 3: The Compression Algorithm (Compressão)
**Ideia:** Remover tokens "supérfluos" mantendo semântica.

```
Original (5K tokens):
"Olá, tudo bem? Eu gostaria de saber, se possível,
 qual marca de whey protein vocês têm disponível 
 atualmente em estoque aqui em São Paulo, considerando
 produtos com boa relação de custo benefício."

Comprimido (1K tokens):
"Qual whey protein em SP, boa relação custo/benefício?"
```

**Implementação:**
```python
def compress_message(text, target_tokens=500):
    """Remove redundâncias mantendo semântica"""
    compressed = claude.invoke(
        "Comprima este texto mantendo TODA informação crítica. "
        f"Máximo {target_tokens} tokens.",
        text
    )
    return compressed
```

**Trade-offs:**
- ✅ Preserva informação
- ✅ Redução significativa
- ❌ Pode soar robótico/artificial
- ❌ Requer ajuste fino

**Melhor para:** Conversas onde tom não é crítico

---

### Estratégia 4: The Semantic Bucketing (Agrupamento Semântico)
**Ideia:** Agrupar informações relacionadas e resumir grupos.

```
Mensagens sobre Preço:
  msg: "Qual o preço?"
  msg: "E com desconto?"
  msg: "Tá caro demais"
  msg: "E se eu comprar mais quantidade?"
    ↓ (resumir grupo)
  RESUMO: "Cliente quer entender preços, 
           quer saber sobre descontos de volume"

Mensagens sobre Alergias:
  msg: "Sou alérgico a glúten"
  msg: "E corn syrup? Tem?"
  msg: "Minha filha é lactose"
    ↓ (resumir grupo)
  RESUMO: "Cliente + filha têm restrições: 
           glúten, corn syrup, lactose"
```

**Implementação:**
```python
def bucket_messages_by_topic(conversation):
    """Agrupa mensagens por tema"""
    topics = {
        "preço": [],
        "alergias": [],
        "entrega": [],
        "recomendação": []
    }
    
    for msg in conversation:
        topic = detect_topic(msg)
        topics[topic].append(msg)
    
    # Resumir cada grupo
    return {k: summarize_group(v) for k, v in topics.items()}
```

**Trade-offs:**
- ✅ Muito eficiente
- ✅ Mantém estrutura lógica
- ✅ Fácil de implementar
- ❌ Requer bom classifier de tópicos
- ❌ Conversas multi-tópico complexas

**Melhor para:** Conversas estruturadas (shopping)

---

### Estratégia 5: The Hybrid Approach (Híbrida)
**Ideia:** Combinar múltiplas estratégias.

```
Camada 1 (Janela): últimas 20 mensagens (janela móvel)
Camada 2 (Buffer): resumo de tudo mais antigo
Camada 3 (Context): informações críticas fixas
```

**Implementação (pseudo-código):**
```python
def build_hybrid_context(conversation, client_profile):
    context = []
    
    # Camada 3: Crítico
    context.append({
        "role": "system",
        "content": f"""
        Cliente: {client_profile.name}
        Alergias: {client_profile.allergies}
        Orçamento: {client_profile.budget}
        Histórico: {client_profile.purchases}
        """
    })
    
    # Camada 2: Buffer
    if len(conversation) > 30:
        old_messages = conversation[:-20]
        summary = summarize(old_messages)
        context.append({
            "role": "system",
            "content": f"Histórico anterior: {summary}"
        })
    
    # Camada 1: Janela
    recent = conversation[-20:]
    for msg in recent:
        context.append(msg)
    
    return context
```

**Trade-offs:**
- ✅ Máxima flexibilidade
- ✅ Funciona para qualquer caso
- ✅ Pode ajustar estratégia em tempo real
- ❌ Complexidade aumenta
- ❌ Requer monitoramento

**Melhor para:** Aplicações críticas (KODA em produção)

---

## 🔢 Calculadora de Token Budgeting

### Como Calcular seus Tokens

```
┌─────────────────────────────────────────────┐
│ CÁLCULO DE VIABILIDADE DE CONVERSA          │
└─────────────────────────────────────────────┘

Passo 1: Qual é seu context window?
  Resposta: 200,000 tokens (Sonnet 4.6)

Passo 2: Quanto já foi consumido?
  System prompt:         2,000
  Histórico processado: 45,000
  Total consumido:      47,000

Passo 3: Reserve buffer de resposta
  Resposta típica:       1,000
  Buffer de segurança:   2,000
  Total reservado:       3,000

Passo 4: Calcule o disponível
  200,000 - 47,000 - 3,000 = 150,000 tokens disponíveis

Passo 5: Quantas mensagens você tem espaço?
  Mensagem típica: 300 tokens
  150,000 / 300 = 500 mensagens ainda possíveis
  
Passo 6: Quantos minutos isso é?
  Assume 5-10 mensagens/minuto (conversa normal)
  500 / 7 = ~71 minutos possíveis
```

### Dashboard Simplificado

```
╔═══════════════════════════════════════════════╗
║ TOKEN BUDGET MONITOR - KODA SESSION          ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Total Context:        200,000 tokens        ║
║  Already Used:          47,000 tokens (23%) ║
║  Reserved:               3,000 tokens         ║
║  Available:            150,000 tokens (75%) ║
║                                               ║
║  Burn Rate:            1,500 tokens/min      ║
║  Time Remaining:        ~100 min             ║
║  Status:               ✅ HEALTHY            ║
║                                               ║
║  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ║
║  23% consumed | 75% available                ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

## 🔴 Sinais de Alerta (Quando Intervir)

### Red Flag 1: Burn Rate Acelerando
```
Minuto 10:  500 tokens/min
Minuto 20:  750 tokens/min  ← Acelerou 50%!
Minuto 30: 1200 tokens/min  ← Acelerou 60% novamente!
```

**O que fazer:**
1. Ativar compressão imediatamente
2. Remover histórico antigo
3. Preparar resumo de contexto

### Red Flag 2: Menos de 20% Disponível
```
Available: 40,000 tokens / 200,000 total (20%)
```

**O que fazer:**
1. Preparar para transição (se conversa será longa)
2. Avisar ao cliente que nova conversa será melhor
3. Salvar estado para contexto futuro

### Red Flag 3: Comportamento "Ansioso"
Quando agente começa a:
- ✖ Dar respostas muito curtas
- ✖ Fazer suposições rápidas
- ✖ Ser menos empático
- ✖ Perder raciocínio lógico

**Causa:** Próximo ao limite, modelo se torna ansiedad

**Solução:** Compactação imediata ou nova sessão

---

## 🎯 Aplicação em KODA

### Cenário Real: Cliente Shopping por 2 Horas

#### Minuto 0-30: FASE VERDE
```
Histórico:     5,000 tokens (poucas mensagens)
Disponível:  195,000 tokens (97.5%)
Status:      ✅ EXCELENTE
Ação:        Nenhuma - deixar rodar normalmente
```

#### Minuto 30-60: FASE AMARELA
```
Histórico:    40,000 tokens (30 min de conversa)
Disponível:  160,000 tokens (80%)
Burn Rate:   1,200 tokens/min
Status:      ⚠️  ATENÇÃO
Ação:        Monitorar. Se continuar neste ritmo,
             durará mais 130 minutos - OK ainda
```

#### Minuto 60-90: FASE LARANJA
```
Histórico:    80,000 tokens (conversa intensa)
Disponível:  120,000 tokens (60%)
Burn Rate:   1,500 tokens/min
Status:      🟠 CUIDADO
Ação:        Ativar Summary Buffer
             Resumir tudo e manter apenas últimas 10 msg
```

#### Minuto 90+: FASE VERMELHA
```
Histórico:   110,000 tokens (conversa muito longa)
Disponível:   90,000 tokens (45%)
Burn Rate:   1,800 tokens/min
Status:      🔴 CRÍTICO
Ação:        OPÇÃO A: Mudar para nova conversa
             OPÇÃO B: Compactação agressiva
             Avisar cliente: "Vou preparar seu pedido,
                              uma nova especialista pode
                              ajudá-lo no checkout"
```

### Implementação Prática em KODA

```python
class KODATokenManager:
    def __init__(self):
        self.total_tokens = 200_000
        self.safety_buffer = 5_000
        self.phase = "GREEN"
    
    def check_token_health(self, conversation):
        """Monitora saúde de tokens"""
        used = self.estimate_tokens(conversation)
        available = self.total_tokens - used - self.safety_buffer
        percentage = (available / self.total_tokens) * 100
        
        if percentage > 60:
            self.phase = "GREEN"
            return {"action": "continue", "health": "✅ Healthy"}
        elif percentage > 40:
            self.phase = "YELLOW"
            return {"action": "monitor", "health": "⚠️  Watch"}
        elif percentage > 20:
            self.phase = "ORANGE"
            return {
                "action": "compress",
                "health": "🟠 Intervene",
                "compress_older_than": "30 min"
            }
        else:
            self.phase = "RED"
            return {
                "action": "new_session",
                "health": "🔴 Critical",
                "message": "Inicie nova conversa com especialista"
            }
    
    def estimate_tokens(self, conversation):
        """Estimativa rápida de tokens"""
        # ~4 caracteres = 1 token (heurística simples)
        total_chars = sum(len(msg.get("content", "")) 
                         for msg in conversation)
        return total_chars // 4
```

---

## ✅ Checklist: Você Domina Token Budgeting?

- [ ] **Sei o tamanho do context window** de cada modelo que uso
- [ ] **Consigo estimar tokens** de uma mensagem (regra de 4 chars/token)
- [ ] **Entendo burn rate** e consegui calcular para meu caso
- [ ] **Conheço as 5 estratégias** de token budgeting
- [ ] **Sou capaz de implementar** pelo menos 2 delas
- [ ] **Posso reconhecer red flags** quando estão acontecendo
- [ ] **Tenho plano** para quando buffer fica baixo
- [ ] **Mapeei token budgeting** para KODA especificamente

---

## 🔄 Próximos Passos

### Para Hoje
1. ✅ Abra a calculadora de tokens acima
2. ✅ Estime quantos tokens sua conversa típica usa
3. ✅ Calcule quantos minutos você pode continuar

### Para Esta Semana
1. ✅ Escolha **1 estratégia** para implementar (comece com Windowed History)
2. ✅ Implemente monitoramento básico (print de status)
3. ✅ Teste em conversa real de 30+ minutos

### Para Próximo Módulo
Leia `03-basic-harness-patterns.md` - que mostra **como estruturar** seu agente para usar token budgeting efetivamente.

---

## 💬 Conexão com Problemas Anteriores

Lembra do `01-why-agents-lose-plot.md`? Ele descrevia **3 problemas**:

1. **Context Amnesia** ← Token budgeting ajuda aqui
   - Ao gerenciar tokens, você decide *o que* lembrar
   - Não é amnésia - é seleção consciente

2. **Decision Degradation** ← Token budgeting previne aqui
   - Não deixar buffer cair evita comportamento ansioso
   - Decisões melhores quando há espaço de respiração

3. **Communication Breakdown** ← Token budgeting suporta aqui
   - Com espaço, agente pode comunicar melhor
   - Sem aperto de tokens, pode ser transparente

**A diferença:** Problema 1 é o *sintoma*. Token budgeting é o *diagnóstico e tratamento*.

---

## 📚 Recursos Adicionais

**Glossário:** Veja `GLOSSARY.md` para:
- Context Window
- Burn Rate
- Context Rot
- Token estimation

**Implementação:** Veja `03-basic-harness-patterns.md` para:
- Como estruturar código para token budgeting
- Integração com seu harness
- Exemplos de produção

**Casos Práticos:** Veja caso de estudo:
- KODA Order Processing (como KODA gerencia tokens em checkout)

---

## 🎓 Resumo em 1 Minuto

**Token budgeting é:**
- Gerenciar tokens como um CFO gerencia dinheiro
- Saber quanto você tem, quanto está usando, quanto falta
- Planejar estrategicamente para não "quebrar"

**5 estratégias:**
1. **Windowed History** - Manter só últimas N mensagens
2. **Summary Buffer** - Resumir periodicamente
3. **Compression** - Remover redundâncias
4. **Semantic Bucketing** - Agrupar por tópico
5. **Hybrid** - Combinar tudo

**Para KODA:**
- Conversas shopping pode chegar a 1-2 horas
- Precisa de monitoramento proativo
- Planejar transição para nova especialista em vez de crash

**Próximo:** Padrões de harness que implementam essas estratégias 👇

---

## 📝 Notas Finais

> *"Um agente sem token budgeting é como um negócio sem fluxo de caixa - que parece estar bem até desabar subitamente."*

Token budgeting não é sexy. Não é algo que clientes veem. Mas é a diferença entre:
- ✅ KODA que funciona por 2 horas contínuas
- ❌ KODA que falha misteriosamente após 30 minutos

Fernando aprendeu isso na prática com seus projetos anteriores. Por isso que KODA foi construído com token budgeting desde o design - não como "fix" depois.

**Você está um passo à frente agora que sabe.** 🚀

---

**Pronto para o próximo? → `03-basic-harness-patterns.md`** 

Naquele módulo, vamos ver *como* implementar tudo que aprendeu aqui.

---

*Módulo 2 - Nível 1 Fundamentals | FutanBear Long-Running Agents Program | v1.0*
