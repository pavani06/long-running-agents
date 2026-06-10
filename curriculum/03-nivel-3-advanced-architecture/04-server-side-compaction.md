---
title: "Server-Side Compaction: A Arte de Manter Contexto Sem Perder a Essência"
type: curriculum-lesson
nivel: 3
aliases: []
tags: [curriculo-conteudo, nivel-3, arquitetura-avancada, compactacao-no-servidor, sumarizacao-extrativa, sumarizacao-abstrativa, chunking-semantico, priorizacao-de-contexto, janela-deslizante-adaptativa, retencao-de-contexto, budget-de-tokens, conversas-longas, validacao-de-contexto]
relates-to: ["[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]"]
last_updated: 2026-06-10
---
# 🗜️ Server-Side Compaction: A Arte de Manter Contexto Sem Perder a Essência
## Como Técnicas de Compactação no Servidor Transformam Agentes que Esquecem em Agentes que Lembram

**Tempo Estimado:** 120 minutos  
**Nível:** 3 - Arquitetura Avançada  
**Pré-requisito:** Ter completado Nível 1 (Context Management, Token Budgeting) e Nível 2 (State Persistence, File-Based Coordination)  
**Status:** 🟡 CRÍTICO - Habilita agentes a manterem coerência em sessões de 6+ horas  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Pesadelo das 4 Horas

**Segunda-feira, 09:00. KODA recebe uma mensagem no WhatsApp:**

```
Cliente: "Bom dia KODA! Preciso montar minha suplementação completa. 
         Treino há 3 anos, foco em hipertrofia, tenho 78kg, e sou 
         intolerante à lactose e glúten."
         
KODA: "Bom dia! Que incrível seu comprometimento. Vou te ajudar 
       a montar o stack perfeito. Vamos começar?"
```

O que parecia uma conversa simples rapidamente se transformou em algo épico:

- **09:15** - Cliente detalha rotina de treino, horários, intensidade
- **09:45** - Discutem 12 produtos diferentes, comparam preços, analisam reviews
- **10:30** - Cliente revela que já usou 5 marcas e quer saber diferenças
- **11:00** - Conversa sobre objetivos de curto, médio e longo prazo
- **11:45** - Negociam promoções, frete, formas de pagamento
- **12:15** - Cliente faz perguntas sobre interações entre suplementos
- **13:00** - **4 horas depois** - Cliente finalmente decide comprar

E é aqui que o problema acontece:

```
Cliente: "Então o whey vegano que você recomendou, aquele de baunilha, 
         tem garantia de qualidade? E aquele terceiro produto que você 
         mencionou lá no começo, o BCAA, vale a pena mesmo?"

KODA: [Pausa longa...]
      "Desculpe, pode repetir qual whey você está perguntando?
       E sobre o BCAA... qual era mesmo nossa recomendação?"
```

**4 horas de conversa. 240 minutos de contexto. Milhares de tokens. E KODA está perdido.**

O cliente desabafa:

```
"KODA, parece que você não estava prestando atenção... 
 Eu passei a manhã inteira falando com você."
```

O que aconteceu?

KODA não é mal-educado. KODA não é incompetente. KODA sofreu de algo que todo agente sofre quando sessões ultrapassam 2-3 horas: **degradação de contexto por sobrecarga de informação**. A janela de contexto - mesmo com 200K ou 1M tokens - eventualmente se torna um repositório de ruído onde informações críticas são diluídas entre centenas de trocas triviais.

Mas há uma solução. E ela é elegante.

---

### A Descoberta de Fernando

Fernando, o CTO da KODA, estava frustrado. Ele já tinha resolvido:

- ✅ **Context Amnesia** com State Persistence (Nível 1)
- ✅ **Planning Collapse** com Generator/Evaluator (Nível 2)  
- ✅ **Self-Evaluation** com Rubrics e Evaluators (Nível 2)
- ✅ **Coordenação** com File-Based Coordination (Nível 3)

Mas havia um limite prático que ninguém tinha previsto: **conversas de 4+ horas simplesmente tinham informação demais para caber em qualquer janela de contexto, não importa quão grande**.

Foi numa madrugada de debugging que Fernando teve o insight:

> *"Não podemos guardar tudo. Mas podemos guardar o que IMPORTA."*

Ele percebeu que nem todo token tem o mesmo valor:

```
Mensagem crítica:
"SOU ALÉRGICO A AMENDOIM - RISCO DE MORTE"
→ Valor: ALTÍSSIMO. Não pode ser perdida NUNCA.

Mensagem trivial:
"haha verdade, meu cachorro também late pra entregador"
→ Valor: BAIXO. Contexto social, mas não essencial.

Mensagem ambígua:
"acho que vou querer o de chocolate, mas não tenho certeza"
→ Valor: MÉDIO. Indica preferência, mas é maleável.
```

**Server-Side Compaction** nasceu dessa percepção. Não é sobre jogar informação fora. É sobre **priorizar, sumarizar e destilar o que realmente importa**, mantendo a essência da conversa enquanto libera espaço para o agente continuar sendo inteligente.

---

### Conexão com os Níveis Anteriores

Você aprendeu em Nível 1 que **Context Amnesia** é um dos 3 problemas fundamentais. Aprendeu soluções: persistir estado, comprimir histórico, usar harnesses.

Você aprendeu em Nível 2 que **State Persistence** guarda informações críticas em arquivos externos. Que **File-Based Coordination** permite que agentes compartilhem contexto via JSON. Que **Generator/Evaluator** cria checkpoints de qualidade.

Mas Nível 1 e 2 resolvem o problema **até certo ponto**. Quando conversas ultrapassam 3-4 horas, mesmo com state persistence e file coordination, você enfrenta um problema novo:

**A janela de contexto enche de "ruído contextual"** - informações que são relevantes no momento, mas que acumulam ao longo do tempo e competem com informações verdadeiramente críticas.

Server-Side Compaction é a **camada de Nível 3** que resolve este problema. É a diferença entre um agente que funciona por 2 horas e um agente que funciona por 8 horas.

---

### O Que Você Vai Aprender

Neste módulo, você vai:

✅ Entender **por que** a compactação no servidor é superior à compactação no cliente  
✅ Dominar **estratégias de sumarização** extrativa e abstrativa  
✅ Projetar sistemas de **chunking inteligente** que priorizam contexto por relevância  
✅ Implementar **sliding windows adaptativos** que se ajustam ao ritmo da conversa  
✅ Entender a variante head-tail com middle recuperável: preserve âncoras e externalize o meio com recuperação exata.
✅ Construir um **pipeline completo de compactação** para conversas de 6+ horas  
✅ Medir o impacto: **75% → 98% de retenção de contexto** com 60% menos tokens  
✅ Aplicar tudo ao **KODA** em um cenário real de conversa WhatsApp de 4 horas

E ao final, você terá nas mãos uma técnica que transforma agentes que "esquecem" em agentes que "lembram o que importa".

---

## 🎯 Parte 1: Por Que Compactar no Servidor vs. Cliente?

### O Dilema Arquitetural

Quando você percebe que o contexto está grande demais, a primeira pergunta é: **onde compactar?**

Há duas opções fundamentais:

```
OPÇÃO A: CLIENT-SIDE COMPACTION
┌──────────────────────────────────────┐
│  Dispositivo do Usuário (WhatsApp)   │
│  ┌────────────────────────────────┐  │
│  │  APP KODA (Cliente)            │  │
│  │  • Recebe todas as mensagens   │  │
│  │  • Decide o que enviar         │  │
│  │  • Compacta ANTES de mandar    │  │
│  │  • Envia resumo para servidor  │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
                │
                ▼ (resumo compactado)
┌──────────────────────────────────────┐
│  Servidor KODA                       │
│  • Recebe resumo pronto              │
│  • Processa com LLM                  │
│  • Sem controle sobre o que perdeu   │
└──────────────────────────────────────┘


OPÇÃO B: SERVER-SIDE COMPACTION
┌──────────────────────────────────────┐
│  Dispositivo do Usuário (WhatsApp)   │
│  • Envia TUDO (histórico completo)   │
│  • Zero processamento local          │
└──────────────────────────────────────┘
                │
                ▼ (histórico completo)
┌──────────────────────────────────────┐
│  Servidor KODA                       │
│  ┌────────────────────────────────┐  │
│  │  COMPACTION ENGINE             │  │
│  │  • Analisa histórico completo  │  │
│  │  • Prioriza por relevância     │  │
│  │  • Sumariza com LLM dedicado   │  │
│  │  • Injeta no contexto do KODA  │  │
│  └────────────────────────────────┘  │
│  • KODA recebe contexto otimizado    │
└──────────────────────────────────────┘
```

### Head-Tail com Middle Recuperável

Sliding window mantém as últimas K mensagens. Sumarização comprime tudo em uma representação menor. Head-tail é uma variante diferente: preserva três âncoras explícitas e externaliza o meio para recuperação exata.

As três âncoras são:
- **Head:** início da conversa, contexto original, objetivo, restrições e definições.
- **Tail:** últimas interações, estado atual, decisões recentes e pedido imediato.
- **System prompt:** instruções do harness, que NUNCA devem ser reduzidas pela compactação.

O middle não é descartado. Ele sai do contexto ativo e entra em um catálogo endereçável com IDs, preview e contrato de fetch. Assim, KODA mantém começo e fim visíveis, mas ainda consegue recuperar uma pergunta, decisão ou tool result do meio quando um follow-up depender desse conteúdo.

**Quando usar:**
- Conversas longas em que o início contém restrições ou objetivos duráveis.
- Sessões em que o fim carrega estado operacional sensível, como checkout ou pagamento.
- Traces, spans ou tool calls em que o meio precisa ficar auditável e recuperável.

**Quando NÃO usar:**
- Conteúdo omitido que não pode ser armazenado por política de privacidade.
- Conversas curtas em que tudo cabe no budget sem ruído relevante.
- Fluxos em que o middle não terá mecanismo confiável de fetch por ID.

### Por Que Server-Side é Superior

#### 1. **Controle de Qualidade**

No cliente, você está limitado ao poder de processamento de um celular. No servidor, você tem acesso a LLMs dedicados para sumarização, bancos de dados para referência cruzada, e pipelines de validação.

**Exemplo KODA:**
```
CLIENTE (Celular, WhatsApp):
"Preciso compactar 4h de conversa"
→ Memória: 200MB disponível no app
→ Processamento: 2 núcleos de CPU mobile
→ Resultado: Resumo genérico, perde detalhes

SERVIDOR (Cloud KODA):
"Preciso compactar 4h de conversa"
→ Usa Claude Haiku para sumarização (rápido, barato)
→ Cruza com customer_profile.json (dados persistentes)
→ Valida contra alergias, preferências registradas
→ Resultado: Resumo preciso, preserva críticos
```

#### 2. **Consistência de Estado**

No servidor, você tem acesso ao **estado completo do cliente** - não apenas o que foi dito na conversa atual, mas também:

- Histórico de compras (últimos 6 meses)
- Preferências salvas (alergias, sabores, orçamento)
- Estado do pedido atual (carrinho, etapa do checkout)
- Métricas de saúde do agente (token usage, latência)

O cliente WhatsApp **não tem acesso** a esse estado. Então qualquer compactação feita no cliente é cega ao contexto mais amplo.

**Cenário real:**
```
Cliente diz: "Aquele produto que você recomendou na semana passada era bom?"
Cliente-side compaction: "Cliente pergunta sobre produto recomendado"
Server-side compaction: "Cliente pergunta sobre Whey Vegano Baunilha SKU#W452 
                      recomendado em 19/05 - comprou 2 unidades, avaliou 4.8/5"
```

O servidor "sabe" qual produto era. O cliente não tem essa informação.

#### 3. **Atomicidade da Operação**

Server-side compaction acontece como uma **transação atômica**:

```
1. Recebe histórico completo
2. Analisa → Prioriza → Sumariza
3. Valida resultado (Evaluator)
4. Se aprovado → injeta no contexto
5. Se rejeitado → ajusta parâmetros, tenta novamente
```

No cliente, se a compactação falhar no meio, você perdeu a conversa. Não há "rollback". No servidor, você sempre tem o histórico completo como backup.

#### 4. **Evolução Independente**

Estratégias de compactação evoluem rapidamente:

- Mês 1: Sumarização extrativa simples
- Mês 3: Sumarização abstrativa com LLM
- Mês 6: Compactação hierárquica multi-nível
- Mês 12: Compactação com aprendizado por reforço (RLHF)

Se a compactação está no cliente, cada atualização requer **deploy de app** (App Store review, Google Play review, adoção do usuário). No servidor, você atualiza e **todos os clientes recebem instantaneamente**.

#### 5. **Segurança e Compliance**

No servidor, você pode:

- **Auditar** cada compactação: o que foi removido, por quê, quando
- **Replay** de conversas para debugging
- **Compliance** com LGPD: registro do que foi sumarizado vs removido
- **Detectar viés**: se o compactador está sistematicamente removendo certos tipos de informação

No cliente, você perde essa rastreabilidade.

---

### 📊 Tabela Comparativa: Client-Side vs. Server-Side Compaction

| Dimensão | Client-Side | Server-Side |
|----------|-------------|-------------|
| **Poder de processamento** | Limitado (CPU mobile) | Ilimitado (cloud scalable) |
| **Acesso a estado externo** | Nenhum (só conversa atual) | Completo (DB, perfil, histórico) |
| **Qualidade da sumarização** | Baixa (sem LLM dedicado) | Alta (LLM + validação) |
| **Latência adicional** | Baixa (local) | Média (network + processing) |
| **Auditabilidade** | Nenhuma | Completa (logs, traces, replay) |
| **Evolução de algoritmo** | Lenta (deploy de app) | Instantânea (server update) |
| **Custo operacional** | Zero (processa no device) | Baixo (Haiku sumarização ~$0.001) |
| **Recuperação de falha** | Impossível (dados perdidos) | Completa (histórico no servidor) |
| **Segurança de dados** | Dados sensíveis no device | Dados em ambiente controlado |
| **Consistência cross-session** | Ruim (não vê outras sessões) | Excelente (state persistence) |
| **Escalabilidade** | 1:1 (um device = um processador) | N:1 (múltiplos clientes, um pipeline) |

### Quando Client-Side AINDA é Útil

Server-side não é bala de prata. Client-side compaction tem seu lugar:

✅ **Modo offline**: Quando o dispositivo está sem internet, precisa de fallback  
✅ **Privacidade extrema**: Quando dados NUNCA podem sair do dispositivo  
✅ **Latência zero**: Para operações em tempo real (ex: digitação preditiva)  
✅ **Custo zero de servidor**: Para MVPs com orçamento mínimo  

Mas para KODA - que processa milhares de conversas simultâneas, precisa de 98% de precisão, e onde cada erro custa um cliente - **server-side é a única escolha viável**.

---

### O Pipeline de Compactação: Visão Macro

Antes de mergulharmos nas técnicas específicas, veja como o pipeline completo se parece:

```
CONVERSA DE 4 HORAS
(Histórico completo: ~180K tokens)
        │
        ▼
┌───────────────────────────────────────────────┐
│  FASE 1: CHUNKING                             │
│  Divide conversa em blocos de ~30 minutos     │
│  Cada bloco = unidade de sumarização          │
│  Output: 8 chunks de ~22K tokens cada          │
└───────────────────┬───────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│  FASE 2: PRIORIZAÇÃO                          │
│  Classifica cada mensagem:                    │
│  • 🔴 CRÍTICA (alergias, decisões, pedidos)    │
│  • 🟡 IMPORTANTE (preferências, contexto)      │
│  • 🟢 TRIVIAL (small talk, confirmações)       │
│  Output: chunks com scoring de prioridade     │
└───────────────────┬───────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│  FASE 3: SUMARIZAÇÃO                          │
│  Para cada chunk:                             │
│  • Extrativa: mantém mensagens 🔴 intactas    │
│  • Abstractiva: resume 🟡 em 2-3 frases       │
│  • Descarta 🟢 com baixo score                │
│  Output: 8 resumos de ~3K tokens cada         │
└───────────────────┬───────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│  FASE 4: MONTAGEM DO CONTEXTO                 │
│  Sliding window com:                          │
│  • Últimos 15 min: COMPLETO (fresco)          │
│  • 15-60 min: RESUMO DETALHADO                │
│  • 1-4 horas: RESUMO COMPACTO                 │
│  • State externo: SEMPRE injetado             │
│  Output: Contexto otimizado de ~35K tokens    │
└───────────────────┬───────────────────────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │  KODA (LLM)         │
          │  Processa com       │
          │  contexto otimizado │
          │  Qualidade: 98%     │
          └─────────────────────┘
```

Este pipeline transforma **180K tokens de ruído** em **35K tokens de sinal puro**. O segredo está em cada fase - e é isso que vamos dominar agora.

---

## 📊 Parte 2: Summarization Strategies - Extractive vs. Abstractive

### O Fundamento: Dois Paradigmas de Sumarização

Quando você precisa reduzir informação, existem duas abordagens fundamentais:

```
EXTRACTIVE SUMMARIZATION (Extrativa)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Princípio: "Selecionar as frases mais importantes"
Método: Rankear e escolher sentenças do texto original
Output: Cópia literal das sentenças originais

Vantagens:
✅ 100% factual - não inventa nada
✅ Rápido - sem LLM necessário
✅ Auditável - toda frase tem origem rastreável
✅ Determinístico - mesmo input = mesmo output

Desvantagens:
❌ Robótico - frases soltas, sem fluidez narrativa
❌ Redundante - pode copiar frases redundantes
❌ Sem inferência - não conecta informações implícitas
❌ Limite de compressão: ~50-60%



ABSTRACTIVE SUMMARIZATION (Abstractiva)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Princípio: "Gerar novo texto que capture a essência"
Método: LLM lê o texto e escreve um resumo original
Output: Texto novo, sintetizado, coerente

Vantagens:
✅ Natural - lê como texto humano
✅ Alta compressão - pode reduzir 80-90%
✅ Conecta ideias - faz inferências e conexões
✅ Adaptável - pode focar no que é relevante

Desvantagens:
❌ Pode alucinar - gerar informação que não existe
❌ Lento - requer chamada LLM
❌ Custo - tokens de input + output
❌ Não-determinístico - temperature afeta resultado
```

---

### Extractive Summarization em Detalhe

A sumarização extrativa é como um **highlight inteligente**: você não cria nada novo, apenas decide quais partes do texto original são importantes o suficiente para manter.

#### Algoritmo Básico: TF-IDF Scoring

```python
# Pseudocódigo: Sumarização Extrativa para Conversa KODA

def extractive_summarize(conversation: list[Message], keep_ratio: float = 0.3) -> list[Message]:
    """
    Seleciona as keep_ratio% mensagens mais importantes.
    """
    # Passo 1: Calcular importância de cada mensagem
    for msg in conversation:
        msg.score = 0
        
        # Score por keywords críticas (alergia, comprar, preço, etc)
        if contains_critical_keywords(msg):
            msg.score += 100  # Máxima prioridade
        
        # Score por entidades nomeadas (produtos, valores, datas)
        if contains_product_reference(msg):
            msg.score += 50
        
        # Score por decisão do cliente
        if contains_decision(msg):  # "quero", "comprar", "fechar"
            msg.score += 40
        
        # Score por pergunta (indica que cliente precisa de resposta)
        if msg.is_question:
            msg.score += 30
        
        # Score por sentimento forte (frustração, entusiasmo)
        if msg.sentiment_intensity > 0.7:
            msg.score += 20
        
        # Score por comprimento informativo
        if 50 < msg.token_count < 200:
            msg.score += 10  # Mensagens de tamanho médio tendem a ser informativas
    
    # Passo 2: Ordenar por score e selecionar top N%
    conversation.sort(key=lambda m: m.score, reverse=True)
    keep_count = int(len(conversation) * keep_ratio)
    
    # Passo 3: Reordenar por timestamp (manter ordem cronológica)
    selected = conversation[:keep_count]
    selected.sort(key=lambda m: m.timestamp)
    
    return selected
```

#### Exemplo Real: Conversa KODA de 2h

```
ENTRADA: 240 mensagens (2 horas de conversa)

APÓS SCORING AUTOMÁTICO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Score 100+: 8 mensagens (3.3%)
   "Sou alérgico a amendoim - risco de morte"
   "Vou comprar o Whey Vegano então"
   "Meu orçamento máximo é R$ 200"
   ...

🟡 Score 50-99: 34 mensagens (14.2%)
   "Qual desses tem melhor custo-benefício?"
   "O de chocolate é melhor que baunilha?"
   "Pode calcular o frete para SP?"
   ...

🟢 Score <50: 198 mensagens (82.5%)
   "haha verdade"
   "ok"
   "entendi"
   "👍"
   "deixa eu ver aqui"
   ...

SAÍDA (keep_ratio = 0.25 → 60 mensagens):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 8/8 mantidas (100% de preservação crítica)
🟡 34/34 mantidas (100% de preservação importante)
🟢 18/198 mantidas (9% - só as mais relevantes)

Total: 60 mensagens (240 → 60, compressão de 75%)
Tokens: ~45K → ~12K (compressão de 73%)
```

#### Limitações da Abordagem Extrativa Pura

```
PROBLEMA 1: FRAGMENTAÇÃO
━━━━━━━━━━━━━━━━━━━━━━━━
Original:
  Cliente: "Qual whey você recomenda?"
  KODA: "Temos 3 opções:"
  [LISTA DETALHADA DE 3 PRODUTOS COM PREÇOS]
  Cliente: "O segundo parece bom"
  KODA: "Ótima escolha! O Whey Vegano Baunilha..."

Extrativa (só frases com score alto):
  Cliente: "Qual whey você recomenda?"
  Cliente: "O segundo parece bom"
  KODA: "Ótima escolha! O Whey Vegano Baunilha..."

PROBLEMA: "O segundo" refere-se a quê? A lista foi removida!
Perdemos o REFERENTE. O texto fica incoerente.


PROBLEMA 2: REDUNDÂNCIA
━━━━━━━━━━━━━━━━━━━━━━━━
Original:
  [Minuto 20] Cliente: "Sou intolerante à lactose"
  [Minuto 55] Cliente: "Lembra que não posso lactose?"
  [Minuto 90] Cliente: "Sem lactose, ok?"

Extrativa:
  Mantém as 3 frases (todas têm score alto)
  → 3x a mesma informação, ocupando tokens

Ideal:
  "Cliente é intolerante à lactose (confirmado 3x durante a conversa)"
  → 1 frase, mesma informação, 70% menos tokens
```

---

### Abstractive Summarization em Detalhe

A sumarização abstrativa usa um LLM para **entender e reescrever** o conteúdo. Não é sobre copiar frases; é sobre **capturar a essência**.

#### O Prompt de Sumarização

```json
{
  "model": "claude-haiku-4-6",  // Rápido e barato para sumarização
  "system_prompt": "Você é um especialista em sumarização de conversas para agentes de IA. Seu trabalho é preservar informações CRÍTICAS e destilar o resto em resumos concisos.",
  
  "messages": [
    {
      "role": "user",
      "content": "Resuma esta conversa entre um cliente e o agente KODA. Regras:\n\n1. Informações CRÍTICAS (alergias, restrições médicas, decisões de compra) devem ser preservadas TEXTUALMENTE.\n\n2. Preferências e opiniões devem ser resumidas em 1-2 frases.\n\n3. Small talk e confirmações ('ok', 'entendi') devem ser OMITIDAS.\n\n4. Cada produto mencionado deve ter: nome, SKU (se presente), preço (se mencionado), e decisão do cliente sobre ele.\n\n5. O resumo deve permitir que outro agente entenda o estado atual da conversa e tome decisões.\n\nCONVERSA:\n[180 mensagens do chunk de 30 minutos]"
    }
  ]
}
```

#### Exemplo: Chunk de 30 Minutos Sumarizado

```
ENTRADA (30 min de conversa, ~22K tokens, 180 mensagens):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...180 mensagens sobre produtos, preços, preferências...

SAÍDA (Resumo Abstractivo, ~1.2K tokens):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Resumo do Bloco 10:00-10:30

### Informações Críticas (PRESERVADAS TEXTUALMENTE)
- "Sou ALÉRGICO A AMENDOIM. Sério, já tive reação forte." 
  ⚠️ Mencionado novamente às 10:12. Confirmado intolerância à lactose 
  também às 10:05.

### Decisões do Cliente
- Decidiu NÃO comprar Creatina Monohidratada (R$ 45) - achou cara
- Mostrou interesse no Whey Vegano Baunilha (R$ 89) - "esse parece ideal"
- Pediu para reservar BCAA (R$ 35) - "volto nisso depois"

### Preferências Expressas
- Prefere sabores de baunilha e chocolate (não gosta de morango)
- Prioriza custo-benefício sobre marca premium
- Quer produtos com certificação de qualidade (mencionou "quero garantia")

### Produtos Discutidos
1. Whey Vegano Baunilha (WHEY-VEG-001) R$89 - CLIENTE INTERESSADO
2. Creatina Monohidratada (CREA-001) R$45 - CLIENTE RECUSOU
3. BCAA Premium (BCAA-001) R$35 - CLIENTE QUER RESERVAR
4. Whey Isolado Chocolate (WHEY-ISO-002) R$120 - MENCIONADO, sem decisão
5. Multivitamínico Daily (VIT-001) R$55 - CLIENTE PEDIU MAIS INFORMAÇÕES

### Estado da Conversa
Cliente está na fase de comparação de produtos. Ainda não decidiu compra
final. Próximo passo provável: decidir entre Whey Vegano e outra opção.
Humor: positivo, engajado.
```

**Compressão:** 22K tokens → 1.2K tokens (94.5% de redução)  
**Qualidade:** Todas as informações críticas preservadas, decisões claras, contexto narrativo mantido

---

### Estratégia Híbrida: O Melhor dos Dois Mundos

Para KODA, a melhor estratégia **não é escolher uma ou outra**. É combiná-las:

```
ESTRATÉGIA HÍBRIDA KODA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 MENSAGENS CRÍTICAS (score 100+)
   → PRESERVAÇÃO TEXTUAL (extractive)
   → "Sou alérgico a amendoim" fica EXATAMENTE como foi dito
   → Zero risco de paráfrase alterar significado

🟡 MENSAGENS IMPORTANTES (score 50-99)
   → SUMARIZAÇÃO ABSTRATIVA (abstractive)
   → LLM reescreve de forma concisa e conectada
   → "Cliente discutiu 5 produtos, recusou 2, interessou-se em 3"

🟢 MENSAGENS TRIVIAIS (score <50)
   → DESCARTE CONTROLADO
   → "haha", "ok", "entendi", "👍" → removido
   → Mas mantemos contagem: "[12 mensagens de small talk removidas]"

⚪ CONTEXTO RECENTE (últimos 15 minutos)
   → PRESERVAÇÃO TOTAL
   → Últimas mensagens SEMPRE completas
   → Agente precisa de contexto fresco para responder naturalmente
```

---

### 📊 Tabela Comparativa: Estratégias de Sumarização

| Dimensão | Extrativa Pura | Abstractiva Pura | Híbrida (KODA) |
|----------|---------------|-------------------|----------------|
| **Compressão máxima** | 50-60% | 90-95% | 75-85% |
| **Risco de alucinação** | 0% (só copia) | 3-8% (pode inventar) | <1% (críticos preservados) |
| **Velocidade** | <100ms (regex + scoring) | 2-5s (LLM call) | 1-3s (híbrido) |
| **Custo por chunk** | $0 | ~$0.001 (Haiku) | ~$0.0005 |
| **Coerência narrativa** | Baixa (frases soltas) | Alta (texto fluido) | Alta (resumo + citações) |
| **Auditabilidade** | Perfeita (rastreável) | Média (resumo é novo) | Alta (críticos rastreáveis) |
| **Consistência cross-chunk** | Baixa (sem contexto entre chunks) | Alta (LLM mantém continuidade) | Alta (resumos cross-referenciados) |
| **Recuperação de referentes** | Ruim ("o segundo" perde a lista) | Boa (reescreve com referência) | Excelente (preserva ou reescreve) |
| **Adequado para** | Conversas curtas (<1h) | Conversas longas (>3h) | Qualquer duração |

---

## 🧩 Parte 3: Chunking e Priorização de Contexto

### O Problema do Chunking

Antes de sumarizar, você precisa decidir **como dividir** a conversa. Esta decisão é mais importante do que parece.

```
ABORDAGEM INGÊNUA: Chunks de tamanho fixo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"Vou pegar 50 mensagens por chunk"

Problema:
  Chunk 1: 50 mensagens de small talk inicial
  Chunk 2: 48 mensagens de small talk + 2 críticas no final
  
  → As 2 mensagens críticas ficam no final do chunk 2
  → Quando sumarizadas, podem ser diluídas entre o small talk
  → Informação vital pode ser perdida no resumo de bloco


ABORDAGEM INTELIGENTE: Chunking semântico
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"Vou dividir por tópicos e tempo"

  Chunk 1 (09:00-09:18): Apresentação e contexto inicial
  Chunk 2 (09:18-09:45): Discussão de produtos - Categoria Whey
  Chunk 3 (09:45-10:15): Discussão de produtos - Categoria BCAA/Creatina
  Chunk 4 (10:15-10:40): Comparação de preços e orçamento
  Chunk 5 (10:40-11:10): Perguntas sobre frete e entrega
  Chunk 6 (11:10-11:50): Negociação e promoções
  Chunk 7 (11:50-12:30): Decisão de compra e checkout
  Chunk 8 (12:30-13:00): Finalização e confirmação

Vantagens:
✅ Cada chunk tem coerência temática
✅ Sumarização de cada chunk faz sentido isoladamente
✅ Fácil de referenciar: "no chunk 5, cliente perguntou sobre frete"
✅ Respeita fronteiras naturais da conversa
```

### O Algoritmo de Chunking Semântico

```python
def semantic_chunking(messages: list[Message], 
                      max_chunk_tokens: int = 25000,
                      min_chunk_minutes: int = 15,
                      max_chunk_minutes: int = 45) -> list[Chunk]:
    """
    Divide conversa em chunks semanticamente coerentes.
    
    Estratégia: detecta mudanças de tópico e combina com janelas de tempo.
    """
    chunks = []
    current_chunk = Chunk()
    current_topic = None
    
    for msg in messages:
        # Detecta tópico da mensagem atual
        msg_topic = classify_topic(msg)
        
        # Verifica se deve iniciar novo chunk
        should_split = False
        
        # 1. Mudança de tópico significativa
        if current_topic and msg_topic != current_topic:
            if topic_distance(current_topic, msg_topic) > 0.7:
                should_split = True
        
        # 2. Limite de tempo do chunk atual
        if current_chunk.duration_minutes >= max_chunk_minutes:
            should_split = True
        
        # 3. Limite de tokens do chunk atual
        if current_chunk.token_count + msg.token_count > max_chunk_tokens:
            should_split = True
        
        if should_split and current_chunk.duration_minutes >= min_chunk_minutes:
            chunks.append(current_chunk)
            current_chunk = Chunk()
        
        current_chunk.add(msg)
        current_topic = msg_topic
    
    if current_chunk.messages:
        chunks.append(current_chunk)
    
    return chunks


def classify_topic(msg: Message) -> str:
    """Classifica o tópico de uma mensagem na conversa KODA."""
    
    # Mapeamento de keywords → tópico
    topic_keywords = {
        "apresentacao": ["olá", "bom dia", "boa tarde", "preciso de ajuda"],
        "alergias_restricoes": ["alérgico", "intolerante", "não posso", "restrição", 
                                 "lactose", "glúten", "amendoim"],
        "produto_whey": ["whey", "proteína", "isolado", "concentrado"],
        "produto_creatina": ["creatina", "monohidratada", "micronizada"],
        "produto_bcaa": ["bcaa", "aminoácido", "ramificado"],
        "produto_vitaminas": ["vitamina", "multivitamínico", "suplemento diário"],
        "preco_orcamento": ["preço", "custo", "orçamento", "caro", "barato", 
                            "promoção", "desconto"],
        "comparacao": ["comparar", "diferença", "qual melhor", "vs"],
        "frete_entrega": ["frete", "entrega", "prazo", "sedex", "pac"],
        "pagamento": ["pagar", "cartão", "pix", "boleto", "parcela"],
        "decisao_compra": ["vou levar", "comprar", "fechar", "quero esse", 
                           "pode enviar"],
        "pos_compra": ["chegou", "recebi", "obrigado", "avaliação", "review"],
        "small_talk": ["haha", "rsrs", "legal", "valeu", "👍", "ok", "entendi"],
    }
    
    for topic, keywords in topic_keywords.items():
        if any(kw in msg.text.lower() for kw in keywords):
            return topic
    
    return "geral"
```

### O Sistema de Priorização

Uma vez que os chunks estão definidos, cada mensagem dentro deles precisa ser priorizada. O sistema de scoring que vimos antes é a primeira camada. Mas há camadas mais sofisticadas:

#### Camada 1: Scoring por Palavras-Chave (imediato)

```
PRIORIDADE MÁXIMA (score += 100):
- Menções de alergia, condição médica, restrição alimentar
- Decisões de compra: "vou levar", "comprar", "fechar pedido"
- Informações de contato/entrega: endereço, telefone

PRIORIDADE ALTA (score += 50):
- Perguntas diretas ao KODA (terminam com "?")
- Referências a produtos com SKU ou preço
- Expressões de insatisfação ou urgência

PRIORIDADE MÉDIA (score += 25):
- Preferências declaradas ("prefiro chocolate", "não gosto de morango")
- Perguntas sobre funcionamento ("como funciona o frete?")
- Contexto sobre uso do produto

PRIORIDADE BAIXA (score += 10):
- Mensagens informativas sem decisão
- Small talk com informação contextual leve
- Confirmações ("ok, entendi", "pode continuar")
```

#### Camada 2: Scoring por Posição Temporal (contextual)

```python
def temporal_priority(msg: Message, conversation: Conversation) -> float:
    """
    Mensagens mais recentes têm maior prioridade.
    Mas o decay não é linear - depende da relevância.
    """
    minutes_ago = (conversation.now - msg.timestamp).total_minutes()
    
    # Decaimento adaptativo:
    # - Últimos 15 min: peso 1.0 (contexto fresco)
    # - 15-60 min atrás: peso 0.7 (ainda relevante)
    # - 1-3 horas atrás: peso 0.4 (contexto histórico)
    # - 3+ horas atrás: peso 0.15 (background)
    
    if minutes_ago <= 15:
        return 1.0
    elif minutes_ago <= 60:
        return 0.7
    elif minutes_ago <= 180:
        return 0.4
    else:
        return 0.15
```

#### Camada 3: Scoring por Referência Cruzada (estrutural)

```python
def cross_reference_priority(msg: Message, all_messages: list[Message]) -> float:
    """
    Se outras mensagens referenciam esta, sua prioridade sobe.
    """
    boost = 0.0
    
    for other in all_messages:
        if other.timestamp > msg.timestamp:
            # Mensagens posteriores que referenciam esta
            if references(msg, other):
                boost += 20  # Cada referência aumenta prioridade
    
    return boost


def references(original: Message, later: Message) -> bool:
    """Detecta se uma mensagem posterior referencia uma anterior."""
    reference_patterns = [
        "como você disse",
        "aquele produto que você mencionou",
        "voltando ao que você falou",
        "igual você recomendou",
        "você tinha dito",
        "sobre aquilo",
        "lembra que",
    ]
    return any(pattern in later.text.lower() for pattern in reference_patterns)
```

---

### Exemplo Completo de Priorização

```
CONVERSA DE 2 HORAS - 240 MENSAGENS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APÓS SCORING TRIPLO (keywords + temporal + cross-reference):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRÍTICAS (score > 120):
  [09:02] "Sou alérgico a amendoim" (score: 100 keywords + 20 referenciada 3x)
  [09:05] "Também sou intolerante à lactose" (score: 100 keywords + 15 referenciada 2x)
  [11:45] "Vou levar o Whey Vegano e o BCAA" (score: 100 keywords + 10 temporal)
  [11:52] "Endereço é Rua das Flores, 123 - SP" (score: 100 keywords)

🟡 IMPORTANTES (score 60-120):
  [09:30] "Qual a diferença entre whey isolado e concentrado?" (score: 50 pergunta + 30 referenciada)
  [10:15] "Prefiro baunilha, chocolate é muito doce" (score: 25 preferência + 20 temporal + 15 ref)
  [10:45] "Até R$150 posso gastar, mais que isso não" (score: 50 keyword + 20 temporal)
  [11:20] "Tem garantia de devolução se não gostar?" (score: 50 pergunta + 10 temporal)
  ... (34 mensagens nesta faixa)

🟢 TRIVIAIS (score < 60):
  [09:01] "bom dia" (score: 5)
  [09:08] "ok" (score: 2)
  [10:22] "haha verdade" (score: 3)
  [10:55] "entendi" (score: 2)
  [11:03] "deixa eu ver" (score: 5)
  ... (198 mensagens nesta faixa)

AÇÃO:
- 🔴 4 mensagens: PRESERVAR TEXTUALMENTE
- 🟡 38 mensagens: RESUMIR ABSTRATIVAMENTE
- 🟢 198 mensagens: DESCARTAR (com contagem para auditoria)

RESULTADO:
  240 mensagens → 4 citações + 38 resumidas = efetivamente ~42 unidades de informação
  Tokens: ~45K → ~8K (compressão de 82%)
  Informação crítica preservada: 100%
```

---

## 🪟 Parte 4: Sliding Windows Adaptativos

### O Conceito

Um **sliding window** (janela deslizante) é como uma lente que se move sobre a conversa, mantendo em foco o que está próximo e gradualmente "desfocando" o que está distante - mas nunca perdendo completamente.

```
JANELA DESLIZANTE SOBRE CONVERSA DE 4 HORAS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ┌─────────────────────────────────────────────────────────────┐
   │              CONVERSA COMPLETA (4 horas)                    │
   │  [09:00]──────────────────────────────────────────[13:00]   │
   └─────────────────────────────────────────────────────────────┘
        │          │              │               │          │
        ▼          ▼              ▼               ▼          ▼
   ┌────────┐ ┌────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────┐
   │ ZONA 4 │ │ ZONA 3 │ │   ZONA 2     │ │   ZONA 1     │ │ AGORA  │
   │ 3-4h   │ │ 1-3h   │ │  15-60min    │ │  Últimos 15  │ │ 0 min  │
   │ atrás  │ │ atrás  │ │   atrás      │ │   minutos    │ │        │
   └────────┘ └────────┘ └──────────────┘ └──────────────┘ └────────┘
        │          │              │               │          │
        ▼          ▼              ▼               ▼          ▼
   ┌────────┐ ┌────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────┐
   │RESUMO  │ │RESUMO  │ │   RESUMO     │ │   COMPLETO   │ │ 100%   │
   │COMPACTO│ │MÉDIO   │ │  DETALHADO   │ │   (fresco)   │ │ tokens │
   │10% tok │ │30% tok │ │  70% tokens  │ │  100% tokens │ │        │
   └────────┘ └────────┘ └──────────────┘ └──────────────┘ └────────┘
```

### Por Que Adaptativo?

Janelas de tamanho fixo são rígidas demais. Conversas têm ritmos diferentes:

```
CENÁRIO 1: Conversa de Decisão Rápida
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cliente entra, pergunta preço de 1 produto, compra em 8 minutos.

Janela fixa (15 min): ❌ Guarda 15 min de small talk que não aconteceu
Janela adaptativa: ✅ Reconhece que a conversa foi curta e decisiva,
                      mantém TUDO (só 8 min de histórico)


CENÁRIO 2: Conversa Exploratória Longa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cliente passa 3 horas comparando produtos, sem decidir.

Janela fixa (15 min): ❌ Perde 2:45h de contexto de comparação
Janela adaptativa: ✅ Detecta que é exploratória, expande zona 2
                      (15-60 min → 15-120 min) para capturar 
                      toda a jornada de comparação


CENÁRIO 3: Conversa com Pico de Decisão
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2 horas de exploração + 15 minutos de decisão intensa.

Janela fixa (15 min): ❌ 15 min finais capturam a decisão,
                      mas perdem o contexto que levou a ela
Janela adaptativa: ✅ Detecta o pico de decisão, mantém Zona 1
                      expandida em 30 min e Zona 2 em 90 min
```

### O Algoritmo Adaptativo

```python
class AdaptiveSlidingWindow:
    """
    Janela deslizante que se adapta ao ritmo e à densidade da conversa.
    """
    
    def __init__(self):
        # Configurações base
        self.zones = {
            "zone_now":     {"minutes": 0,    "keep_ratio": 1.0},   # Mensagem atual
            "zone_fresh":   {"minutes": 15,   "keep_ratio": 1.0},   # Últimos 15 min
            "zone_detail":  {"minutes": 45,   "keep_ratio": 0.7},   # 15-60 min
            "zone_compact": {"minutes": 120,  "keep_ratio": 0.3},   # 1-3 horas
            "zone_bg":      {"minutes": 240,  "keep_ratio": 0.1},   # 3+ horas
        }
    
    def adapt(self, conversation: Conversation):
        """
        Ajusta as zonas baseado nas características da conversa.
        """
        metrics = self._analyze_conversation(conversation)
        
        # 1. Densidade de decisão
        if metrics["decision_density"] > 0.7:
            # Muitas decisões concentradas → expandir zona fresca
            self.zones["zone_fresh"]["minutes"] = 30
        
        # 2. Ritmo de troca de tópicos
        if metrics["topic_volatility"] > 0.6:
            # Tópicos mudam rapidamente → manter mais contexto
            self.zones["zone_detail"]["minutes"] = 90
            self.zones["zone_detail"]["keep_ratio"] = 0.85
        
        # 3. Duração total
        if conversation.duration_hours < 0.5:
            # Conversa curta → manter tudo
            for zone in self.zones.values():
                zone["keep_ratio"] = 1.0
        elif conversation.duration_hours > 4:
            # Conversa muito longa → comprimir mais o background
            self.zones["zone_bg"]["keep_ratio"] = 0.05
        
        # 4. Presença de informações críticas no background
        if metrics["critical_info_in_bg"]:
            # Há alergias/restrições nas zonas antigas → garantir preservação
            self.zones["zone_bg"]["keep_ratio"] = max(
                self.zones["zone_bg"]["keep_ratio"], 0.2
            )
    
    def _analyze_conversation(self, conv: Conversation) -> dict:
        """
        Analisa características da conversa para adaptação.
        """
        return {
            "decision_density": self._calc_decision_density(conv),
            "topic_volatility": self._calc_topic_volatility(conv),
            "critical_info_in_bg": self._has_critical_in_background(conv),
        }
    
    def apply(self, messages: list[Message]) -> list[Message]:
        """
        Aplica a janela deslizante, retornando as mensagens
        que devem ser incluídas no contexto do agente.
        """
        now = messages[-1].timestamp  # Última mensagem = "agora"
        included = []
        
        for msg in messages:
            minutes_ago = (now - msg.timestamp).total_minutes()
            zone = self._get_zone(minutes_ago)
            keep_ratio = self.zones[zone]["keep_ratio"]
            
            if keep_ratio >= 1.0:
                included.append(msg)  # Manter completo
            elif msg.priority_score > (1.0 - keep_ratio) * 100:
                included.append(msg)  # Manter se prioridade compensa
            # else: descartar (será representada no resumo da zona)
        
        return included
```

---

### Exemplo Visual da Janela em Ação

```
CONVERSA DE 3 HORAS - MOMENTO 2h45min
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIMELINE:
  0min        60min        120min       150min      165min
  ├────────────┼────────────┼────────────┼───────────┤
  Início      1h           2h           2h30        2h45 (agora)

JANELA APLICADA NESTE MOMENTO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  165-150min (ZONA FRESCA - últimos 15 min):
  ┌──────────────────────────────────────────────────────────┐
  │ TODAS as mensagens preservadas (100%)                    │
  │ "Quero finalizar a compra então"                         │
  │ "Pode confirmar o endereço de entrega?"                  │
  │ "Meu CEP é 04567-000"                                    │
  │ ~45 mensagens, ~6K tokens                                │
  └──────────────────────────────────────────────────────────┘

  150-105min (ZONA DETALHADA - 15 a 60 min atrás):
  ┌──────────────────────────────────────────────────────────┐
  │ 70% das mensagens preservadas                            │
  │ Resumo narrativo + citações de mensagens críticas        │
  │ ~120 mensagens → ~84 mantidas + resumo de ~2K tokens     │
  │ Total: ~14K tokens                                      │
  └──────────────────────────────────────────────────────────┘

  105-45min (ZONA COMPACTA - 1h a 2h atrás):
  ┌──────────────────────────────────────────────────────────┐
  │ 30% das mensagens preservadas                            │
  │ Apenas resumo narrativo + citações 🔴                    │
  │ ~180 mensagens → resumo de ~3K tokens                    │
  └──────────────────────────────────────────────────────────┘

  45-0min (ZONA BACKGROUND - 2h a 3h atrás):
  ┌──────────────────────────────────────────────────────────┐
  │ 10% das mensagens preservadas                            │
  │ Resumo ultra-compacto                                    │
  │ ~120 mensagens → resumo de ~1K tokens                    │
  └──────────────────────────────────────────────────────────┘

  ────────────────────────────────────────────────────────────
  TOTAL NO CONTEXTO: ~6K + ~14K + ~3K + ~1K = ~24K tokens
  HISTÓRICO COMPLETO: ~180K tokens
  COMPRESSÃO: 86.7% (180K → 24K)
  ────────────────────────────────────────────────────────────
```

---

## 🔧 Parte 5: O Pipeline Completo de Compactação

### Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SERVER-SIDE COMPACTION PIPELINE                           │
│                                                                             │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐       │
│  │  INGESTÃO  │───▶│  CHUNKING  │───▶│ PRIORIZAÇÃO│───▶│ SUMARIZAÇÃO│       │
│  │  (API)     │    │  (Semântico│    │  (3-Layer  │    │  (Híbrida) │       │
│  │            │    │   + Tempo) │    │   Scoring) │    │            │       │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘       │
│        │                 │                 │                 │              │
│        ▼                 ▼                 ▼                 ▼              │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    STATE DATABASE (PostgreSQL)                    │       │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │       │
│  │  │ customer_profile│  │ compaction_log  │  │ chunk_summaries │   │       │
│  │  │ (alergias, pref)│  │ (audit trail)   │  │ (resumos)       │   │       │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘   │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│        │                                                                    │
│        ▼                                                                    │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐                         │
│  │ MONTAGEM DO│───▶│  VALIDAÇÃO │───▶│  INJEÇÃO   │                         │
│  │ CONTEXTO   │    │  (Evaluator│    │  NO KODA   │                         │
│  │ (Sliding   │    │   check)   │    │  (LLM)     │                         │
│  │  Window)   │    │            │    │            │                         │
│  └────────────┘    └────────────┘    └────────────┘                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Fase 1: Ingestão

```json
// POST /api/compaction/ingest
{
  "conversation_id": "conv_20260523_0900",
  "customer_id": "wa_5511987654321",
  "messages": [
    {
      "timestamp": "2026-05-23T09:00:00Z",
      "role": "customer",
      "text": "Bom dia KODA! Preciso montar minha suplementação completa."
    },
    // ... centenas de mensagens
  ],
  "trigger": "auto",  // auto | manual | threshold (80% da janela de contexto)
  "current_context_usage": 0.78  // 78% do contexto total já ocupado
}
```

### Fase 2: Chunking (Semântico + Temporal)

O sistema analisa a conversa e produz chunks. Cada chunk é armazenado com metadados:

```json
{
  "chunks": [
    {
      "chunk_id": "chunk_01",
      "time_range": "09:00-09:18",
      "dominant_topic": "apresentacao_perfil",
      "message_count": 45,
      "token_count": 8200,
      "critical_message_count": 2,
      "summary": null  // Ainda não sumarizado
    },
    {
      "chunk_id": "chunk_02",
      "time_range": "09:18-09:52",
      "dominant_topic": "produto_whey",
      "message_count": 95,
      "token_count": 18700,
      "critical_message_count": 1,
      "summary": null
    }
    // ... mais chunks
  ]
}
```

### Fase 3: Priorização (3-Layer Scoring)

Cada mensagem recebe um `priority_score` (0-200):

```json
{
  "message_id": "msg_0042",
  "text": "Sou alérgico a amendoim, risco de anafilaxia",
  "priority_score": 175,
  "scoring_breakdown": {
    "keyword_score": 100,
    "temporal_score": 45,
    "cross_reference_score": 30
  },
  "classification": "CRITICAL",
  "action": "PRESERVE_TEXTUAL"
}
```

### Fase 4: Sumarização (Híbrida)

Para cada chunk, o sistema decide a estratégia:

```
CHUNK 01 (09:00-09:18) - Apresentação
  🔴 2 mensagens críticas → PRESERVE
  🟡 15 mensagens importantes → SUMMARIZE (abstractive)
  🟢 28 mensagens triviais → DISCARD
  
  Resultado: 2 citações + resumo de 350 tokens
  Compressão: 8200 → 520 tokens (93.7%)

CHUNK 02 (09:18-09:52) - Whey Protein
  🔴 1 mensagem crítica → PRESERVE
  🟡 62 mensagens importantes → SUMMARIZE (abstractive)
  🟢 32 mensagens triviais → DISCARD
  
  Resultado: 4 citações + resumo de 920 tokens
  Compressão: 18700 → 1150 tokens (93.9%)

... (todos os chunks processados)
```

### Fase 5: Montagem do Contexto (Sliding Window)

O contexto final é montado combinando:

1. **State externo** (sempre incluído): perfil do cliente, alergias, preferências
2. **Zona fresca** (últimos 15 min): mensagens completas
3. **Zona detalhada** (15-60 min): resumo detalhado + citações 🔴
4. **Zona compacta** (1-3h): resumo narrativo
5. **Zona background** (3h+): resumo ultra-compacto

```json
{
  "context_assembly": {
    "total_tokens": 28340,
    "breakdown": {
      "state_context": 2100,
      "zone_fresh": 6200,
      "zone_detailed": 9800,
      "zone_compact": 7200,
      "zone_background": 3040
    },
    "compression_ratio": 0.84,
    "critical_info_preservation": 1.0,
    "estimated_quality_retention": 0.98
  }
}
```

### Fase 6: Validação (Evaluator Check)

Antes de injetar no KODA, o contexto montado passa por um Evaluator:

```
EVALUATOR CHECKLIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[✓] Todas as mensagens 🔴 estão preservadas textualmente?
     → 7 de 7 mensagens críticas encontradas no contexto

[✓] Informações do customer_profile estão presentes?
     → Alergias, preferências, histórico de compras: SIM

[✓] Contexto não excede o limite de tokens?
     → 28.340 / 200.000 tokens (14.2%) - OK

[✓] Resumos não contêm alucinações?
     → Cross-check com mensagens originais: sem discrepâncias

[✓] Ordem cronológica está mantida?
     → Sim, mensagens e resumos ordenados por timestamp

[✓] Decisões do cliente estão claras?
     → Última decisão: "Vou levar o Whey Vegano" (11:45)

VERDICT: ✅ APPROVED - Contexto pode ser injetado no KODA
```

### Fase 7: Injeção no KODA

```python
def inject_context(koda_session: KodaSession, compacted_context: CompactedContext):
    """
    Injeta o contexto compactado na sessão do KODA.
    """
    # Constrói o system prompt com o contexto compactado
    system_prompt = f"""
Você é o KODA, assistente de vendas da FutanBear Suplementos.

## PERFIL DO CLIENTE
{compacted_context.state_context}

## CONTEXTO RECENTE (últimos 15 minutos - COMPLETO)
{compacted_context.zone_fresh}

## CONTEXTO DETALHADO (15-60 minutos atrás)
{compacted_context.zone_detailed}

## CONTEXTO COMPACTO (1-3 horas atrás)
{compacted_context.zone_compact}

## CONTEXTO HISTÓRICO (3+ horas atrás)
{compacted_context.zone_background}

## REGRAS CRÍTICAS
- NUNCA recomende produtos que contenham alergênicos do cliente
- Sempre confirme preços e disponibilidade antes de finalizar
- Se não tiver certeza sobre algo, pergunte ao cliente
"""
    
    # Atualiza a sessão com o novo contexto
    koda_session.update_context(system_prompt)
    
    # Registra a compactação
    log_compaction(
        conversation_id=koda_session.conversation_id,
        original_tokens=compacted_context.original_tokens,
        compacted_tokens=compacted_context.total_tokens,
        compression_ratio=compacted_context.compression_ratio,
        quality_score=compacted_context.estimated_quality_retention
    )
```

---

## 📊 Parte 6: Métricas e Resultados - De 75% a 98% de Retenção de Contexto

### O Experimento

A equipe KODA conduziu um experimento controlado para medir o impacto do Server-Side Compaction:

**Setup:**
- 100 conversas simuladas de 4 horas cada
- Cenários variados: compra rápida, exploração longa, negociação, reclamação
- 3 configurações testadas:
  - **A: Sem compactação** (baseline) - contexto completo, até onde couber
  - **B: Compactação extrativa pura** - só mantém mensagens de alta prioridade
  - **C: Pipeline completo** - chunking + priorização + sumarização híbrida + sliding window

**Métrica principal:** "Se eu fizer uma pergunta sobre algo que aconteceu na hora X da conversa, o KODA consegue responder corretamente?"

### Resultados

```
RETENÇÃO DE CONTEXTO POR HORA DA CONVERSA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

100% ┤    ┌──────────────────────────────────────────
     │    │                       C) Pipeline Completo
 95% ┤    │                   ╱
     │    │                ╱
 90% ┤    │             ╱
     │  ╱ │          ╱
 85% ┤ ╱  │       ╱
     │╱   │    ╱
 80% ┤    │ ╱              B) Extrativa Pura
     │    │╱    ╲
 75% ┤   ╱│      ╲
     │  ╱ │        ╲
 70% ┤ ╱  │          ╲___ A) Sem Compactação
     │╱   │               ╲___
 65% ┤    │                    ╲___
     │    │                        ╲___
 60% ┤    │                             ╲___
     │    │
     └────┼──────────┼──────────┼──────────┼──────────┼────
         0h         1h         2h         3h         4h
              Tempo de Conversa Contínua


LEGENDA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A) Sem compactação: Começa em 98%, degrada para 62% em 4h
B) Extrativa pura: Começa em 95%, estabiliza em 78%
C) Pipeline completo: Começa em 98%, estabiliza em 96% 
   (média 4h: 97.2%)
```

### Métricas Detalhadas

| Métrica | Sem Compactação | Extrativa Pura | Pipeline Completo |
|---------|----------------|----------------|-------------------|
| **Retenção em 1h** | 95% | 94% | 98% |
| **Retenção em 2h** | 82% | 88% | 97% |
| **Retenção em 3h** | 70% | 82% | 96% |
| **Retenção em 4h** | 62% | 78% | 96% |
| **Retenção média (0-4h)** | 75% | 85% | **97.5%** |
| **Tokens no contexto (média)** | 180K (overflow) | 55K | 28K |
| **Compressão de tokens** | 0% (baseline) | 69% | 84% |
| **Custo por conversa (4h)** | R$ 0.12 | R$ 0.06 | R$ 0.04 |
| **Latência adicional** | 0ms | 150ms | 900ms |
| **Informação crítica perdida** | 8% | 3% | **0.2%** |
| **Satisfação do cliente (NPS)** | 62 | 74 | **89** |

### O Que os Números Significam

**75% → 98% não é mágica. É engenharia.**

```
ANTES (Sem compactação):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contexto: 180K tokens de "tudo"
Qualidade: O agente vê MUITA informação, mas não consegue
           distinguir o que importa. É como procurar uma
           agulha num palheiro - a agulha está lá, mas
           o agente não consegue encontrá-la no meio do ruído.
           
Retenção efetiva: 75% (a informação existe, mas não é usada)


DEPOIS (Pipeline completo):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contexto: 28K tokens de "sinal puro"
Qualidade: O agente vê MENOS informação, mas CADA token
           é relevante. Informações críticas são destacadas.
           O contexto recente está completo. O histórico
           está sumarizado de forma navegável.
           
Retenção efetiva: 98% (a informação certa, no momento certo)
```

---

## 🏪 Parte 7: Aplicação KODA - Compactação de Conversas 2h+

### Cenário Real: A Conversa de 4 Horas

Vamos acompanhar uma conversa real do KODA e ver como o pipeline de compactação atua em cada fase. Esta é a mesma conversa do prólogo, agora com a solução aplicada.

```
═══════════════════════════════════════════════════════════════
        KODA + SERVER-SIDE COMPACTION EM AÇÃO
═══════════════════════════════════════════════════════════════
```

#### 09:00-09:30: Início da Conversa

```
CLIENTE: "Bom dia KODA! Preciso montar minha suplementação completa."
KODA: "Bom dia! Vou te ajudar. Me conta sobre você e seus objetivos."

[Conversa flui naturalmente]

COMPACTION STATUS: INATIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contexto usado: 8K / 200K tokens (4%)
Motivo: Conversa ainda é curta, não precisa compactar
Estratégia: Todas as mensagens preservadas integralmente
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 10:15: Primeira Compactação (Threshold: 45% de uso)

```
⚠️  ALERTA DO SISTEMA: Contexto atingiu 45% de uso (90K tokens)
    Gatilho: Threshold automático
    Ação: Iniciar compactação de background

COMPACTION ENGINE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[FASE 1 - CHUNKING]
  Conversa analisada: 1h15min de duração, 385 mensagens
  Chunks detectados:
    Chunk 1 (09:00-09:18): Apresentação e perfil
    Chunk 2 (09:18-09:52): Discussão de Whey Protein
    Chunk 3 (09:52-10:15): Discussão de BCAA e Creatina

[FASE 2 - PRIORIZAÇÃO]
  Mensagens analisadas: 385
    🔴 Críticas: 5 (alergias, orçamento máximo)
    🟡 Importantes: 67 (preferências, perguntas)
    🟢 Triviais: 313 (small talk, confirmações)

[FASE 3 - SUMARIZAÇÃO]
  Chunk 1: 8.2K → 0.5K tokens (94% compressão)
  Chunk 2: 18.7K → 1.1K tokens (94% compressão)
  Chunk 3: 15.3K → 0.9K tokens (94% compressão)

[FASE 4 - MONTAGEM]
  Zona fresca (últimos 15 min): 8.4K tokens (completo)
  Zona detalhada (15-60 min): 4.2K tokens (resumo + citações)
  Zona compacta (1-1.25h): 2.5K tokens (resumo narrativo)
  State externo: 2.1K tokens (perfil, alergias)
  
  TOTAL: 17.2K tokens

[FASE 5 - VALIDAÇÃO]
  ✅ 5/5 mensagens críticas preservadas
  ✅ Perfil do cliente injetado
  ✅ Sem alucinações detectadas
  ✅ Ordem cronológica mantida

COMPRESSÃO: 90K → 17.2K (redução de 81%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 10:16: Imediatamente Após a Compactação

```
Cliente: "E aí, o que você acha do BCAA versus Creatina?"

KODA recebe o contexto compactado:

┌─────────────────────────────────────────────────────┐
│ SYSTEM PROMPT (Contexto após compactação)            │
│                                                     │
│ ## PERFIL DO CLIENTE                                │
│ Alergias: amendoim (grave), lactose                  │
│ Objetivo: hipertrofia, 78kg, treina há 3 anos        │
│ Orçamento: até R$200/mês                             │
│                                                     │
│ ## CONTEXTO RECENTE (últimos 15 min) - COMPLETO     │
│ [10:00] Cliente: "O BCAA é melhor que Creatina?"    │
│ [10:02] KODA: "Depende do objetivo..."              │
│ [10:05] Cliente: "Quero ganho de massa"             │
│ [10:08] KODA: "Nesse caso, Creatina tem mais..."    │
│ [10:12] Cliente: "E o preço? Qual vale mais?"       │
│ [10:15] KODA: "Vamos comparar..."                   │
│                                                     │
│ ## RESUMO DETALHADO (15-60 min atrás)                │
│ Cliente discutiu opções de Whey Protein.             │
│ Interessou-se no Whey Vegano Baunilha (R$89).        │
│ Recusou Whey Isolado Chocolate (R$120) - achou caro. │
│ Perguntou sobre diferenças entre isolado/vegano.     │
│                                                     │
│ ## RESUMO COMPACTO (1h-1h15 atrás)                   │
│ Cliente se apresentou, declarou alergias, definiu    │
│ orçamento. KODA explicou as 3 categorias principais  │
│ de suplementação.                                    │
│                                                     │
│ ⚠️ CRÍTICO: "Sou alérgico a amendoim" [09:02]      │
│ ⚠️ CRÍTICO: "Intolerante à lactose" [09:05]         │
│ ⚠️ CRÍTICO: "Orçamento máximo R$200" [09:30]        │
│ ⚠️ CRÍTICO: "Endereço: Rua das Flores, 123" [09:45] │
└─────────────────────────────────────────────────────┘

KODA (resposta rápida e precisa):
"Ótima pergunta! Para hipertrofia, a Creatina é a escolha 
número 1 comprovada cientificamente. O BCAA ajuda na 
recuperação, mas a Creatina tem mais evidências para ganho 
de massa. Considerando seu orçamento de até R$200, a Creatina 
(R$45) + Whey Vegano (R$89) que você gostou cabem perfeitamente!"

✅ KODA lembrou do orçamento (citado 45 min atrás)
✅ KODA lembrou do Whey Vegano que o cliente gostou (citado 30 min atrás)
✅ KODA fez uma recomendação coerente com o perfil
```

#### 11:45: Segunda Compactação (Threshold: 60% de uso)

```
⚠️  ALERTA DO SISTEMA: Contexto atingiu 60% de uso
    Gatilho: Threshold automático
    Conversa já tem 2h45min

COMPACTION ENGINE - SEGUNDA RODADA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Desta vez, o pipeline é mais agressivo com chunks antigos:

  ZONA BACKGROUND (2-3h atrás): keep_ratio reduzido para 5%
  → Chunks 1-3 são recomprimidos em resumo ultra-compacto
  
  NOVO CONTEXTO MONTADO:
  Zona fresca (15 min): 7.2K tokens
  Zona detalhada (15-60 min): 3.8K tokens  
  Zona compacta (1-2h): 3.1K tokens
  Zona background (2-3h): 1.2K tokens (ultra-compacto)
  State externo: 2.1K tokens
  
  TOTAL: 17.4K tokens
  
  Compressão acumulada: 175K → 17.4K (90% de redução)
  Qualidade estimada: 97% de retenção
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 13:00: Fim da Conversa - 4 Horas Depois

```
Cliente: "Beleza KODA, vou fechar o pedido então. 
         Whey Vegano Baunilha + Creatina + BCAA."

KODA (após 4 horas de conversa, com contexto compactado):
"Perfeito! Deixa eu confirmar seu pedido:

📦 Produto 1: Whey Vegano Baunilha (WHEY-VEG-001) - R$89
📦 Produto 2: Creatina Monohidratada (CREA-001) - R$45
📦 Produto 3: BCAA Premium (BCAA-001) - R$35

🚚 Entrega: Rua das Flores, 123 - São Paulo/SP
💰 Total: R$169 (dentro do seu orçamento de R$200!)
⚠️  Todos os produtos são sem lactose e sem amendoim

Confirma o pedido?"

Cliente: "Perfeito! Pode enviar. Obrigado KODA, você é fera!"

🎉 VENDA CONCLUÍDA! 4 horas de conversa. Zero erros. Cliente satisfeito.
```

### O Que Aconteceu nos Bastidores

```
RESUMO DA SESSÃO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Duração total: 4 horas
Mensagens trocadas: 1.247
Tokens totais gerados: ~310K

Compactações realizadas: 3
  - 1ª (10:15): 90K → 17.2K tokens
  - 2ª (11:45): 175K acumulado → 17.4K tokens  
  - 3ª (12:50): 280K acumulado → 18.1K tokens

Contexto médio mantido: ~17.5K tokens
  (nunca passou de 10% da janela de 200K)

Custo total de compactação: R$ 0.012 (3 chamadas Haiku)
Custo evitado (se tivesse usado contexto cheio): R$ 0.35
Economia: 96.6%

Informações críticas preservadas: 100% (12 de 12)
Satisfação do cliente: NPS 95 ⭐⭐⭐⭐⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### O Estado Final do Contexto (após 4 horas)

```
┌─────────────────────────────────────────────────────────┐
│              CONTEXTO INJETADO NO KODA                  │
│              (TOTAL: 18.1K tokens)                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🟢 PERFIL DO CLIENTE (2.1K tokens)                     │
│    Alergias, preferências, histórico, orçamento         │
│                                                         │
│ 🟢 ZONA FRESCA - últimos 15 min (6.8K tokens)          │
│    87 mensagens completas da finalização do pedido       │
│                                                         │
│ 🟡 ZONA DETALHADA - 15-60 min atrás (4.2K tokens)      │
│    Resumo: "Cliente comparou preços, negociou frete,     │
│    decidiu comprar 3 produtos. Confirmou endereço.        │
│    Perguntou sobre garantia e prazo de devolução."        │
│    + 3 citações críticas 🔴                              │
│                                                         │
│ 🟠 ZONA COMPACTA - 1-2h atrás (3.0K tokens)            │
│    Resumo: "Cliente discutiu BCAA vs Creatina.           │
│    KODA recomendou Creatina para hipertrofia.            │
│    Cliente interessou-se em Whey Vegano (R$89).          │
│    Recusou Whey Isolado (caro)."                         │
│    + 2 citações críticas 🔴                              │
│                                                         │
│ 🔴 ZONA BACKGROUND - 2-4h atrás (2.0K tokens)          │
│    Resumo ultra-compacto:                                │
│    "Cliente apresentou-se: 78kg, hipertrofia, 3 anos     │
│    de treino. Alergias: amendoim (grave), lactose.        │
│    Orçamento: R$200/mês. Prefere sabores baunilha e       │
│    chocolate. Busca custo-benefício."                     │
│    + 4 citações críticas 🔴 (alergias, endereço)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Tabela Comparativa: Estratégias de Coordenação de Contexto

Esta tabela compara todas as abordagens de gerenciamento de contexto que você aprendeu ao longo do programa:

### Estratégias de Gerenciamento de Contexto para Long-Running Agents

| Estratégia | Nível | Compressão | Custo | Complexidade | Quando Usar |
|------------|-------|------------|-------|-------------|-------------|
| **Contexto Bruto (sem gestão)** | 0 | 0% | Baixo | Nenhuma | Conversas <15 min. MVPs. Protótipos. |
| **Token Budgeting** | 1 | Manual (10-20%) | Baixo | Baixa | Conversas <1h. Quando você quer controle manual. |
| **State Persistence (DB)** | 1 | N/A (dados externos) | Médio | Média | Sempre. É a base para todas as outras estratégias. |
| **History Truncation** | 1 | Alta (80-90%) | Zero | Baixa | Quando informações antigas são definitivamente descartáveis. |
| **Extractive Summarization** | 3 | Média (50-60%) | Baixo | Média | Conversas de 1-3h. Quando factualidade é crítica. |
| **Abstractive Summarization** | 3 | Alta (85-95%) | Baixo (Haiku) | Alta | Conversas de 3-8h. Quando narrativa coerente importa. |
| **Server-Side Compaction (Pipeline)** | 3 | Muito Alta (80-95%) | Baixo-Médio | Alta | Conversas de 2-12h. Agentes de produção. |
| **Hybrid Summarization** | 3 | Alta (75-85%) | Baixo | Muito Alta | Agentes críticos (saúde, finanças). Zero tolerância a alucinação. |
| **Sliding Window (fixo)** | 3 | Média (50-70%) | Zero | Baixa | Conversas com ritmo uniforme. |
| **Sliding Window (adaptativo)** | 3 | Alta (70-90%) | Baixo | Alta | Conversas com ritmo variável. Uso geral em produção. |
| **Multi-Agent Shared State** | 3-4 | N/A (coordenação) | Alto | Muito Alta | Sistemas com 3+ agentes colaborando na mesma conversa. |
| **RLHF-Tuned Compaction** | 4 | Otimizada por feedback | Alto | Muito Alta | Quando você tem dados de treinamento de qualidade. Melhoria contínua. |

### Matriz de Decisão: Qual Estratégia Usar?

```
                     Duração da Conversa
                          │
           < 30 min ──────┼────── > 30 min ──────┼────── > 2h ──────┼────── > 6h
                │         │           │          │         │        │
                ▼         │           ▼          │         ▼        │
         Contexto Bruto   │    Token Budgeting   │  Server-Side     │
         + State Persist  │    + State Persist   │  Compaction      │
                          │    + Truncation      │  + Hybrid Summ   │
                          │                      │  + Adapt Window  │
                          │                      │                  │
     Complexidade da Tarefa                     Custo do Erro
              │                                      │
     Simples ─┼── Complexa                  Baixo ───┼─── Alto
        │     │       │                       │      │      │
        ▼     │       ▼                       ▼      │      ▼
     Bruto    │   Compaction              Truncation  │  Hybrid +
              │   + Summation                        │  Evaluator
```

---

## 🎓 O Que Você Aprendeu

### 1. **Server-Side vs. Client-Side Compaction**
Compactar no servidor oferece controle de qualidade, acesso a estado externo, auditabilidade e evolução independente. O custo extra de latência e processamento é mínimo comparado aos benefícios. Client-side só se justifica para offline, privacidade extrema ou MVPs com orçamento zero.

### 2. **Summarization Extractive vs. Abstractive**
Extrativa é rápida, factual e auditável - ideal para informações que não podem ser parafraseadas (alergias, valores, endereços). Abstractiva produz narrativas coerentes e comprime mais - ideal para contexto histórico. A estratégia híbrida combina as duas: críticos são preservados textualmente, o resto é sumarizado.

### 3. **Chunking Semântico + Priorização em 3 Camadas**
Dividir a conversa por tópicos (não por contagem fixa) produz chunks que fazem sentido isoladamente. O sistema de priorização em 3 camadas (keywords + temporal + cross-reference) garante que nenhuma informação crítica seja perdida, enquanto small talk é descartado com segurança.

### 4. **Sliding Windows Adaptativos**
Janelas fixas são rígidas demais para conversas reais. Janelas adaptativas ajustam a retenção baseado no ritmo da conversa, densidade de decisões e presença de informações críticas. Uma conversa de decisão rápida mantém mais contexto; uma conversa exploratória longa comprime mais o histórico.

### 5. **Pipeline Completo de Compaction**
O pipeline de 7 fases (Ingestão → Chunking → Priorização → Sumarização → Montagem → Validação → Injeção) transforma 300K+ tokens de ruído em ~18K tokens de sinal puro. O Evaluator final garante que a qualidade do contexto compactado atenda aos critérios antes de chegar ao KODA.

### 6. **Métricas de Impacto: 75% → 98%**
Com o pipeline completo, a retenção de contexto sobe de 75% (sem compactação, em 4h) para 98% (com pipeline). O contexto ocupa 84% menos tokens. O custo de API cai 67%. E a satisfação do cliente (NPS) sobe de 62 para 89.

---

## ✅ Checklist de Entendimento

Antes de avançar, verifique:

### Fundamentos
- [ ] Consigo explicar por que server-side compaction é superior ao client-side
- [ ] Entendo a diferença entre sumarização extrativa e abstrativa
- [ ] Sei quando usar cada estratégia (e quando usar a híbrida)

### Chunking e Priorização
- [ ] Consigo explicar por que chunking semântico é melhor que chunking por contagem fixa
- [ ] Entendo o sistema de scoring em 3 camadas (keywords, temporal, cross-reference)
- [ ] Consigo classificar uma mensagem como 🔴 CRÍTICA, 🟡 IMPORTANTE ou 🟢 TRIVIAL

### Sliding Windows
- [ ] Entendo as 4 zonas da janela deslizante (fresca, detalhada, compacta, background)
- [ ] Consigo explicar por que a janela precisa ser adaptativa
- [ ] Sei quando expandir ou contrair cada zona

### Pipeline
- [ ] Consigo desenhar o pipeline completo de 7 fases
- [ ] Entendo o papel do Evaluator na validação do contexto montado
- [ ] Consigo explicar como o contexto compactado é injetado no KODA

### Métricas e Impacto
- [ ] Entendo o experimento que mediu 75% → 98% de retenção
- [ ] Consigo interpretar a tabela de métricas (retenção, compressão, custo, latência)
- [ ] Sei calcular o ROI da compactação para um cenário específico

### KODA
- [ ] Entendi o cenário completo da conversa de 4 horas
- [ ] Consigo identificar os 3 momentos de compactação e o que mudou em cada um
- [ ] Consigo ler o contexto final montado e entender cada zona

---

## ❓ Perguntas Frequentes

### P: "Qual é o limite prático? Até quantas horas o pipeline aguenta?"
**R:** Testamos até 12 horas de conversa contínua. O pipeline mantém ~97% de retenção até 8 horas, caindo para ~92% em 12 horas. O limite não é técnico (sempre cabe em 200K tokens) - é que após 8+ horas, a conversa naturalmente muda de contexto tantas vezes que as primeiras horas se tornam genuinamente irrelevantes.

### P: "A sumarização abstrativa não alucina às vezes? Como vocês mitigam?"
**R:** Sim, pode alucinar. Nossa mitigação é tripla: (1) informações 🔴 NUNCA passam por sumarização abstrativa - são preservadas textualmente, (2) o Evaluator cross-checka os resumos contra as mensagens originais antes de aprovar, (3) mantemos o `temperature=0.1` nas chamadas de sumarização.

### P: "Por que não usar um modelo maior (como Opus) para sumarização?"
**R:** Custo e latência. Haiku faz sumarização excelente por ~1/50 do custo do Opus e em 1/3 do tempo. A sumarização não requer raciocínio complexo - requer extrair e reorganizar informação. Haiku é perfeitamente adequado.

### P: "O que acontece se a compactação falhar no meio?"
**R:** O sistema sempre mantém o histórico completo como backup. Se a compactação falhar (timeout, erro de API, rejeição do Evaluator), o KODA continua operando com o contexto anterior (que ainda está válido). Uma nova tentativa de compactação é agendada para 5 minutos depois.

### P: "Isso funciona com outros modelos além do Claude?"
**R:** Sim. O pipeline de chunking e priorização é agnóstico de modelo (usa regex + scoring determinístico). A sumarização abstrativa funciona com qualquer LLM competente. Testamos com GPT-4o-mini e Gemini Flash com resultados comparáveis.

### P: "Qual o impacto na latência percebida pelo cliente?"
**R:** A compactação roda em background, de forma assíncrona. O cliente **nunca espera** pela compactação. A latência adicional é zero do ponto de vista do usuário. O KODA continua respondendo normalmente enquanto o pipeline processa.

### P: "Como vocês lidam com conversas que alternam entre WhatsApp e outros canais?"
**R:** Como o estado do cliente é centralizado no servidor (state persistence), qualquer canal acessa o mesmo contexto compactado. Se o cliente muda do WhatsApp para o web chat, o KODA no web chat recebe o mesmo contexto compactado. O pipeline é channel-agnostic.

---

## 🔗 Próximos Passos

### Dentro do Nível 3
- **05-harness-evolution.md**: Como evoluir seus harnesses quando novos modelos são lançados
- **koda-applications/nivel-3-koda.md**: Aplicação integrada de todos os conceitos de Nível 3 ao KODA
- **exercises/**: Exercícios práticos de implementação do pipeline de compactação

### Preparação para Nível 4
O Nível 4 aplica todos os conceitos diretamente ao KODA em produção:
- **01-koda-architecture.md**: Arquitetura completa do KODA com compaction integrada
- **02-customer-journey-flows.md**: Jornadas do cliente que dependem de contexto de longa duração
- Case studies de conversas reais de 8+ horas processadas com o pipeline

### Implementação Prática
1. **Esta semana**: Implemente um chunking semântico simples para as conversas do KODA
2. **Próxima semana**: Adicione sumarização híbrida com Haiku
3. **Em 2 semanas**: Implemente o sliding window adaptativo
4. **Em 1 mês**: Pipeline completo com Evaluator de validação

---

## 💭 Reflexão Final

> *"A memória não é sobre guardar tudo. É sobre saber o que importa."*

Por 3 níveis, você aprendeu a construir agentes cada vez mais sofisticados. Aprendeu a evitar que esqueçam (Nível 1). Aprendeu a fazê-los confiáveis e auditáveis (Nível 2). Aprendeu a coordená-los e persistir estado (Nível 3).

Mas Server-Side Compaction fecha um ciclo. É a técnica que permite que tudo isso **escale**. Que permite que um agente comece uma conversa às 9 da manhã e termine às 6 da tarde sem nunca perder o fio da meada.

Não é sobre memória infinita - isso não existe. É sobre **memória inteligente**. Sobre saber que a alergia do cliente importa mais que o comentário sobre o clima. Sobre destilar 4 horas de conversa em 18 mil tokens que capturam tudo que realmente importa.

Quando Fernando implementou o pipeline no KODA, ele não estava apenas otimizando tokens. Ele estava respondendo a uma pergunta fundamental:

**"Como um agente pode estar presente por horas sem se perder?"**

A resposta está neste módulo. E agora está nas suas mãos.

---

## 🎬 Próxima Cena

Feche este arquivo.

Pense em uma conversa longa que você já teve - com um amigo, um cliente, um colega. Pense em como sua própria mente naturalmente prioriza, sumariza e descarta informações durante essa conversa.

Você não guarda cada palavra. Mas você lembra do que importa.

**Server-Side Compaction faz a mesma coisa para agentes.**

Agora você sabe como.

No próximo módulo, vamos falar sobre como tudo isso evolui - como seus harnesses, seus pipelines, suas estratégias se adaptam quando novos modelos chegam e o jogo muda.

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | 04-server-side-compaction.md |
| **Nível** | 3 - Arquitetura Avançada |
| **Tempo** | 120 minutos |
| **Status** | ✅ Completo |
| **Próximo** | 05-harness-evolution.md |
| **Dependência** | 02-state-persistence.md |
| **Crítica para** | Nível 4 (KODA em produção) |
| **Atualizado** | Maio 2026 |

---

*Escrito com foco em aplicação prática, métricas reais e o pipeline que transforma conversas de 4 horas em contexto de 18K tokens.*  
*Memória: Este documento habilita agentes a manterem coerência em sessões de 8+ horas.*

---

## 📊 Apêndice Técnico: Pseudocódigo do Pipeline

### Compactação Assíncrona em Background

```python
class CompactionPipeline:
    """
    Pipeline de compactação server-side para KODA.
    Roda em background, sem bloquear o agente principal.
    """
    
    def __init__(self, config: CompactionConfig):
        self.config = config
        self.state_db = StateDatabase(config.db_url)
        self.llm_summarizer = LLMClient(model="claude-haiku-4-6", temperature=0.1)
        self.evaluator = CompactionEvaluator()
    
    async def maybe_compact(self, session: KodaSession) -> bool:
        """
        Verifica se a compactação é necessária e a executa em background.
        Retorna True se a compactação foi iniciada.
        """
        # Threshold: compactar quando o contexto atingir 45% da janela
        usage_ratio = session.context_tokens / session.max_context_tokens
        
        if usage_ratio < self.config.compaction_threshold:
            return False  # Ainda não precisa compactar
        
        # Inicia compactação assíncrona (não bloqueia o KODA)
        asyncio.create_task(self._compact(session))
        return True
    
    async def _compact(self, session: KodaSession):
        """
        Executa o pipeline completo de compactação.
        """
        try:
            # Fase 1: Recupera o histórico completo
            messages = await self.state_db.get_messages(session.conversation_id)
            
            # Fase 2: Chunking semântico
            chunks = semantic_chunking(
                messages,
                max_chunk_tokens=self.config.max_chunk_tokens,
                min_chunk_minutes=self.config.min_chunk_minutes,
                max_chunk_minutes=self.config.max_chunk_minutes,
            )
            
            # Fase 3: Priorização
            for chunk in chunks:
                for msg in chunk.messages:
                    msg.priority_score = self._calculate_priority(msg, messages)
            
            # Fase 4: Sumarização híbrida
            summaries = []
            for chunk in chunks:
                summary = await self._summarize_chunk(chunk)
                summaries.append(summary)
            
            # Fase 5: Montagem do contexto (sliding window)
            context = self._assemble_context(messages, summaries, session)
            
            # Fase 6: Validação (Evaluator)
            validation = await self.evaluator.validate(context, messages)
            
            if not validation["approved"]:
                logger.warning(f"Compaction rejected: {validation['reason']}")
                return  # KODA continua com contexto anterior
            
            # Fase 7: Injeção no KODA
            await session.update_context(context)
            
            # Registra métricas
            await self._log_compaction(session, len(messages), context)
            
        except Exception as e:
            logger.error(f"Compaction failed: {e}")
            # KODA continua operando normalmente com contexto atual
    
    async def _summarize_chunk(self, chunk: Chunk) -> ChunkSummary:
        """
        Sumariza um chunk usando estratégia híbrida.
        """
        # Separa mensagens por classificação
        critical = [m for m in chunk.messages if m.classification == "CRITICAL"]
        important = [m for m in chunk.messages if m.classification == "IMPORTANT"]
        # triviais são descartados
        
        # Constrói prompt para sumarização abstrativa
        prompt = self._build_summary_prompt(chunk, critical, important)
        abstractive_summary = await self.llm_summarizer.complete(prompt)
        
        return ChunkSummary(
            chunk_id=chunk.chunk_id,
            time_range=f"{chunk.start_time}-{chunk.end_time}",
            critical_quotes=[m.text for m in critical],  # Preservação textual
            narrative=abstractive_summary,                # Sumarização abstrativa
            stats={
                "original_tokens": chunk.token_count,
                "critical_preserved": len(critical),
                "important_summarized": len(important),
                "trivial_discarded": chunk.message_count - len(critical) - len(important),
            }
        )
```

### Configuração do Pipeline

```json
{
  "compaction_config": {
    "compaction_threshold": 0.45,
    "max_chunk_tokens": 25000,
    "min_chunk_minutes": 15,
    "max_chunk_minutes": 45,
    "sliding_window": {
      "zone_fresh_minutes": 15,
      "zone_detail_minutes": 45,
      "zone_compact_minutes": 120,
      "zone_background_minutes": 240,
      "keep_ratios": {
        "zone_fresh": 1.0,
        "zone_detail": 0.7,
        "zone_compact": 0.3,
        "zone_background": 0.1
      }
    },
    "summarization": {
      "model": "claude-haiku-4-6",
      "temperature": 0.1,
      "max_output_tokens": 2000,
      "strategy": "hybrid"
    },
    "evaluator": {
      "enabled": true,
      "checks": [
        "critical_messages_preserved",
        "state_context_included",
        "token_limit_respected",
        "no_hallucination_detected",
        "chronological_order"
      ]
    },
    "logging": {
      "audit_trail": true,
      "metrics_export": true,
      "alert_on_failure": true
    }
  }
}
```

---

*Documento gerado para o time técnico FutanBear | KODA Project | v1.0 | Maio 2026*
