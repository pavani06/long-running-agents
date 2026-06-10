---
title: "Model Capability Timeline: A Evolução que Possibilitou Long-Running Agents"
type: curriculum-reference
aliases: []
tags: [curriculo-conteudo, referencia, evolucao-de-modelos, linha-do-tempo, capacidades-de-llms, historico-de-modelos, planejamento-de-harness]
relates-to: ["[[curriculum/MASTER_PLAN|Master Plan]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
last_updated: 2026-06-10
---
# 🕰️ Model Capability Timeline: A Evolução que Possibilitou Long-Running Agents
## Como Cada Salto em Capacidade de LLM Redefiniu o Que é Possível em Agentes Autônomos

**Tempo Estimado:** 75 minutos
**Nível:** Referência - Todos os Níveis
**Pré-requisito:** Familiaridade com conceitos básicos de LLMs (tokens, prompting, fine-tuning)
**Status:** 🟢 REFERÊNCIA - Linha do tempo viva, atualizada conforme novos modelos surgem
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Que Torna um Agente Possível?

**2018.** Você está em uma sala de reunião com seu time de engenharia. Alguém pergunta:

> "E se a gente construísse um agente de IA que conversa com clientes por 2 horas, lembra de tudo que foi dito, faz recomendações precisas, processa pedidos, verifica estoque, calcula frete, aplica descontos, e nunca erra?"

Você olha para o quadro branco. Pega o marcador. Começa a desenhar...

...e para.

Porque você sabe que **os modelos de 2018 simplesmente não conseguem fazer isso.** Não é uma questão de engenharia criativa. É uma impossibilidade física:

- **Context window de 512 tokens:** Uma conversa de WhatsApp de 15 minutos já estoura. Duas horas? Impossível.
- **Zero capacidade de reasoning:** O modelo pode completar frases, mas não pode "pensar" sobre o que fazer a seguir.
- **Zero tool use:** O modelo gera texto. Ponto. Não pode consultar um banco de dados, chamar uma API, ler um arquivo.
- **Alucinação descontrolada:** O modelo inventa fatos com confiança absoluta e não tem mecanismo para verificar.

**Fast forward para 2026.** Você está na mesma sala. Só que agora você já construiu o KODA. Ele conversa por horas. Lembra de alergias. Processa pedidos. Verifica estoque em tempo real. Aplica descontos sem double-dipping. Coordena entregas same-day.

**O que mudou?**

Não foi sua engenharia que magicamente evoluiu. Foram os **modelos** que tornaram possível o que antes era impossível.

Este documento conta essa história. A história de como, salto por salto, os LLMs foram desbloqueando capacidades que transformaram agentes de "science fiction" em "production-ready". E mais importante: **como cada capacidade nova redefine o design de harness que você precisa construir.**

Porque aqui está a verdade que ninguém te conta: **cada nova capacidade do modelo não elimina a necessidade de engenharia — ela simplesmente muda QUAL engenharia você precisa fazer.**

Vamos viajar no tempo.

### Como Ler Este Documento

Este não é um documento para ler de uma vez. Use-o como referência:

- **Se você é novo no time:** Leia o Prólogo e a Timeline Visual. Depois leia uma era por dia durante 6 dias. É muito conteúdo para absorver de uma vez — cada era merece reflexão.

- **Se você precisa tomar uma decisão de arquitetura:** Vá direto para a seção da era do seu modelo e para o Guia Prático de Escolha de Modelo. Use a tabela "Modelos por Era: Compatibilidade com Padrões de Harness" para validar sua escolha.

- **Se você está debugando:** Leia a seção "O Dia em que o KODA Quebrou" e a tabela de métricas de evolução. Compare seu harness atual com o que seria esperado para a era do seu modelo.

- **Se você está planejando evolução:** Vá para as Projeções Futuras e para a seção "Além de 2030". Use os 11 princípios como checklist para planejar o próximo passo do seu harness.

- **Para consulta rápida:** Use a tabela "Catálogo de Modelos" no final do documento para ver capacidades de qualquer modelo em 5 segundos.



---

## 🗺️ A Timeline Visual: 2018-2026

```
2018 ──── 2019 ──── 2020 ──── 2021 ──── 2022 ──── 2023 ──── 2024 ──── 2025 ──── 2026
  │          │          │          │          │          │          │          │          │
  │          │          │          │          │          │          │          │          │
GPT-1       │       GPT-3       │    InstructGPT  GPT-4       │    Claude 3.5  Claude 4
BERT        │    (175B params)  │    ChatGPT      Gemini      │    GPT-4o      Opus 4.6
(2018)   GPT-2      │          │    (RLHF)       Claude 2    │    Gemini 2.0  (1M ctx)
           │     Scaling Laws   │          │          │          │          │
           │     (Kaplan 2020)  │          │          │          │          │
           │          │          │          │          │          │          │
     ERA 1:      ERA 2:      ERA 3:      ERA 4:      ERA 5:      ERA 6:
     FOUNDATION  SCALE        ALIGNMENT   MULTIMODAL  AGENT-NATIVE POST-AGENT
     
     Context:    Context:     Context:    Context:    Context:    Context:
     512-1024    2048         4K-8K       32K-128K    200K-1M     1M-10M
     
     Reasoning:  Reasoning:   Reasoning:  Reasoning:  Reasoning:  Reasoning:
     None        Pattern      Basic       Chain-of-   Multi-step  Autonomous
                 Match        Logic       Thought     Planning    Metacognition
     
     Tool Use:   Tool Use:    Tool Use:   Tool Use:   Tool Use:   Tool Use:
     None        None         None        Basic       Native      Orchestrated
                                         (plugins)   (function    (agent
                                                     calling)     frameworks)
```

Cada era não é apenas "modelos melhores". Cada era é uma **revolução arquitetural** no que é possível construir. Vamos entender cada uma.

---

## 🏛️ Era 1: Foundation (2018-2019) — "O Que é um LLM?"

### Modelos-chave
- **GPT-1** (OpenAI, Junho 2018): 117M parâmetros, contexto de 512 tokens
- **BERT** (Google, Outubro 2018): 340M parâmetros, bidirecional, contexto de 512 tokens
- **GPT-2** (OpenAI, Fevereiro 2019): 1.5B parâmetros, contexto de 1024 tokens
- **T5** (Google, Outubro 2019): 11B parâmetros, text-to-text framework

### Capacidades

| Capacidade | Status | Detalhe |
|---|---|---|
| **Geração de texto** | ✅ Básico | Coerente por 2-3 parágrafos, depois degrada |
| **Contexto contínuo** | ❌ 512-1024 tokens | ~400-800 palavras. Uma conversa curta de WhatsApp já satura. |
| **Reasoning** | ❌ Inexistente | Pattern matching, não raciocínio |
| **Tool Use** | ❌ Inexistente | Só gera texto. Zero integração externa. |
| **Multimodal** | ❌ Inexistente | Texto apenas |
| **Instrução** | ❌ Inexistente | Só completa texto (next-token prediction) |
| **Confiabilidade** | ❌ Baixíssima | Alucina com frequência. Sem mecanismo de verificação. |
| **Fine-tuning** | ✅ Disponível | Mas caro e requer datasets grandes |

### O Que Isso Significa para Agentes

Nesta era, **agentes autônomos são impossíveis.** Ponto.

Você pode construir:
- ✅ Chatbots simples (pergunta-resposta, sem memória)
- ✅ Classificadores de texto
- ✅ Geradores de conteúdo curto
- ❌ Qualquer coisa que precise de contexto > 1 minuto
- ❌ Qualquer coisa que precise raciocinar sobre múltiplos passos
- ❌ Qualquer coisa que precise interagir com sistemas externos

**Para o KODA:** Se você tentasse construir o KODA em 2019, você teria um chatbot que:
- Esquece o nome do cliente depois de 5 mensagens
- Não consegue consultar catálogo de produtos
- Inventa preços e disponibilidade
- Não tem noção do que é "alergia" vs "preferência"
- É essencialmente inútil para e-commerce real

### O Padrão de Arquitetura da Era

```
┌──────────────────────────────────────────┐
│           ERA 1: Foundation              │
│                                          │
│  INPUT → LLM → OUTPUT                    │
│                                          │
│  Sem memória. Sem tools. Sem reasoning.  │
│  O LLM é uma caixa preta que gera texto. │
└──────────────────────────────────────────┘
```

**O harness era inexistente** porque não havia nada para "harnessar". O modelo era chamado, gerava resposta, fim.

### Lição para Long-Running Agents

> **Princípio 1:** A capacidade do seu agente é limitada pelo menor denominador comum entre o modelo e seu harness. Você pode construir excelente engenharia, mas se o modelo tem contexto de 512 tokens, seu agente tem "memória" de 512 tokens.

---

## 🔬 Deep Dive: A Matemática do Contexto

Entender a evolução dos modelos exige entender a matemática do contexto. Vamos mergulhar nos números.

### O Que é um Token?

```
1 token ≈ 0.75 palavras em português (média)
1 token ≈ 4 caracteres em inglês
1 token ≈ 3 caracteres em português (acentos consomem mais)

Exemplos:
  "casa" → 1 token
  "coração" → 2 tokens (o 'ç' e 'ã' podem ser tokens separados)
  "KODA recomenda Whey Protein por R$ 89,90" → ~12 tokens
  Uma mensagem de WhatsApp típica → 20-100 tokens
  Uma página A4 de texto → ~500 tokens
  "Guerra e Paz" (livro completo) → ~500.000 tokens
```

### A Fórmula do Contexto Efetivo

Nem todo token no contexto é igual. Tokens no início e no fim recebem mais atenção. Tokens no meio sofrem do "lost-in-the-middle" problem:

```
Atenção por posição no contexto (estilizado):

100% ┤ ████████░░░░░░░░░░░░░░░░░░░░████████
     │ ████████░░░░░░░░░░░░░░░░░░░░████████
 75% ┤ ████████░░░░░░░░░░░░░░░░░░░░████████
     │ ████████░░░░░░░░░░░░░░░░░░░░████████
 50% ┤ ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
     │ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░████
 25% ┤ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░████
     │ ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
  0% └──┴──────────────────────────────┴──
      Início          Meio              Fim
      do contexto     do contexto       do contexto
```

**Implicação prática:** Se você tem 100K tokens de contexto, a região de "alta atenção" cobre aproximadamente:
- Primeiros 10%: 10K tokens (atenção máxima)
- Últimos 10%: 10K tokens (atenção máxima)
- Meio 80%: 80K tokens (atenção reduzida)

**Para agentes:** Informações críticas (alergias, preferências, restrições) devem ficar no início ou no fim do contexto. O meio é para informações de "background" que o agente pode consultar mas não precisa decorar.

### Contexto Real vs. Contexto Efetivo

| Modelo | Contexto Anunciado | Contexto Efetivo (atenção alta) | Conversas que cabem |
|---|---|---|---|
| GPT-1 (2018) | 512 tokens | ~100 tokens | 5 minutos |
| GPT-3 (2020) | 2,048 tokens | ~400 tokens | 15 minutos |
| GPT-4 (2023) | 8,192 tokens | ~1,600 tokens | 1 hora |
| Claude 2 (2023) | 100,000 tokens | ~20,000 tokens | 12 horas |
| Claude 3 (2024) | 200,000 tokens | ~40,000 tokens | 24 horas |
| Opus 4.6 (2026) | 1,000,000 tokens | ~200,000 tokens | 4 dias |
| Projeção 2027 | 10,000,000 tokens | ~2,000,000 tokens | 40 dias |

**Observação fundamental:** "Contexto efetivo" não é uma métrica oficial — é uma heurística baseada em benchmarks de "needle-in-a-haystack". Em tarefas reais de agente, o desempenho depende muito de COMO o contexto está estruturado, não apenas do tamanho.

### A Regra de Ouro do Contexto para Agentes

```
Contexto necessário = (duração da conversa em horas) × (tokens por hora)

Onde:
  tokens por hora ≈ 10,000-20,000 para conversa natural
                  ≈ 30,000-50,000 para conversa intensa (muitos produtos, dados)
                  
Exemplo: Conversa de 3 horas (intensa)
  Contexto necessário = 3 × 40,000 = 120,000 tokens
  
  Modelos que suportam:
  ✅ Claude 3 (200K)
  ✅ GPT-4 Turbo (128K - apertado)
  ❌ GPT-4 (32K)
  ❌ GPT-3 (2K)
```

---

## 🚀 Era 2: Scale (2020-2021) — "Maior é Melhor"

### Modelos-chave
- **GPT-3** (OpenAI, Junho 2020): 175B parâmetros, contexto de 2048 tokens
- **Scaling Laws** (Kaplan et al., Janeiro 2020): Paper que demonstrou que performance escala previsivelmente com tamanho do modelo
- **Codex** (OpenAI, Agosto 2021): GPT-3 fine-tuned para código, 12B parâmetros
- **Gopher** (DeepMind, Dezembro 2021): 280B parâmetros
- **Jurassic-1** (AI21 Labs, 2021): 178B parâmetros

### Capacidades

| Capacidade | Status | Detalhe |
|---|---|---|
| **Geração de texto** | ✅ Bom | Coerente por múltiplos parágrafos. Narrativas longas possíveis. |
| **Contexto contínuo** | ⚠️ 2048 tokens | ~1500 palavras. Conversa de ~15-20 minutos. Ainda crítico. |
| **Reasoning** | ⚠️ Emergente | Few-shot learning mostra capacidade de "imitar" raciocínio |
| **Tool Use** | ❌ Inexistente | Ainda não |
| **Multimodal** | ❌ Inexistente | Texto apenas |
| **Instrução** | ⚠️ Via prompting | Prompt engineering pode "simular" seguir instruções |
| **In-context learning** | ✅ Revolucionário | Modelo aprende com exemplos no prompt, sem fine-tuning |
| **Fine-tuning** | ✅ Disponível | API da OpenAI torna acessível |

### O Que Isso Significa para Agentes

O GPT-3 foi um **divisor de águas psicológico**. De repente, dava para construir coisas que pareciam "inteligentes":

- ✅ Chatbots com personalidade consistente por ~20 mensagens
- ✅ Sistemas de Q&A com contexto de documento
- ✅ Geradores de código (Codex → GitHub Copilot)
- ⚠️ Agentes simples (poucos passos, contexto curto)
- ❌ Conversas longas (além de 2048 tokens, começa a alucinar)
- ❌ Tarefas multi-step complexas

**Para o KODA:** Você já consegue construir um protótipo! Mas com limitações severas:
- A conversa precisa ser curta (< 15 minutos)
- Informações críticas precisam ser repetidas frequentemente
- O agente não pode consultar sistemas externos (catálogo, estoque, pagamento)
- Se o cliente divagar, o contexto é perdido

```python
# Era 2: O máximo que você consegue fazer
def koda_era2_simples():
    prompt = """
    Você é KODA, assistente de vendas.
    
    Contexto da conversa (últimas 2048 tokens):
    {historico_recente}
    
    Responda à última mensagem do cliente.
    """
    # Problemas:
    # - Se histórico > 2048 tokens, tem que truncar
    # - Informações do início da conversa são perdidas
    # - Não pode consultar catálogo em tempo real
    # - Não pode processar pagamento
```

### O Padrão de Arquitetura da Era

```
┌─────────────────────────────────────────────────────────┐
│                  ERA 2: Scale                           │
│                                                         │
│  INPUT → [Prompt Engineering] → LLM → OUTPUT            │
│                                                         │
│  Prompt engineering começa a ser "harness".             │
│  Técnicas: few-shot, chain-of-thought rudimentar,       │
│  persona prompting, output formatting.                  │
│                                                         │
│  Limite: 2048 tokens. Sem tools. Sem memória externa.   │
└─────────────────────────────────────────────────────────┘
```

**Prompt engineering** se torna o primeiro "harness" real. Engenheiros descobrem que podem:
- Dar exemplos no prompt (few-shot) para guiar comportamento
- Pedir para o modelo "pensar passo a passo" (early chain-of-thought)
- Definir persona e tom de voz via system prompt
- Formatar output (JSON, markdown) via instruções

Mas continua sendo um castelo de cartas: se o contexto estourar, tudo desmorona.

### Lição para Long-Running Agents

A Era 2 introduziu dois conceitos fundamentais:

> **Princípio 2 (Scaling Laws):** Performance do modelo escala previsivelmente com tamanho. Isso significa que você pode *planejar* o futuro: se hoje 175B parâmetros permitem conversas de 15 minutos, 1T parâmetros permitirão conversas de 2 horas. A engenharia de harness deve ser desenhada para essa inevitabilidade.

> **Princípio 3 (In-Context Learning):** O modelo pode "aprender" com exemplos no prompt. Isso significa que seu harness pode ensinar o modelo a se comportar de formas específicas *sem fine-tuning*. Cada invocação do agente é uma oportunidade de "re-treinar" via prompt.

---

## 🎯 Era 3: Alignment (2022-2023) — "O Modelo Me Entende"

### Modelos-chave
- **InstructGPT** (OpenAI, Janeiro 2022): GPT-3 + RLHF (Reinforcement Learning from Human Feedback)
- **ChatGPT** (OpenAI, Novembro 2022): GPT-3.5 + RLHF + interface conversacional
- **GPT-4** (OpenAI, Março 2023): Contexto de 8K (depois 32K). Multimodal (texto + imagem). Significativamente melhor em reasoning.
- **Claude 1** (Anthropic, Março 2023): Contexto de 9K tokens
- **Claude 2** (Anthropic, Julho 2023): Contexto de 100K tokens
- **Llama 2** (Meta, Julho 2023): Open-source, 7B-70B parâmetros, contexto de 4K
- **PaLM 2** (Google, Maio 2023): Contexto de 8K

### O Salto Quântico: RLHF

**Reinforcement Learning from Human Feedback** foi a inovação que transformou LLMs de "completadores de texto" em "assistentes":

```
Antes do RLHF:
  Usuário: "Quanto é 2+2?"
  Modelo: "2+2=4. 2+2=5. 2+2=3. 2+2=4." (completações possíveis)

Depois do RLHF:
  Usuário: "Quanto é 2+2?"
  Modelo: "2+2 é igual a 4." (resposta útil, direta)
```

O RLHF ensinou aos modelos:
1. **Seguir instruções** (não apenas completar texto)
2. **Ser útil** (responder à intenção do usuário)
3. **Ser seguro** (evitar conteúdo danoso)
4. **Admitir ignorância** ("Não sei" vs inventar)
5. **Manter persona consistente** (assistente, não oráculo aleatório)

### Capacidades

| Capacidade | Status | Detalhe |
|---|---|---|
| **Geração de texto** | ✅ Excelente | Coerente, útil, segue instruções |
| **Contexto contínuo** | ✅ 4K-100K | De ~3000 a ~75000 palavras. Conversas longas possíveis. |
| **Reasoning** | ✅ Bom | Chain-of-thought funciona bem. Pode raciocinar sobre problemas complexos. |
| **Tool Use** | ⚠️ Via prompting só | Sem function calling nativo. Hacks: "Use este formato para chamar API..." |
| **Multimodal** | ⚠️ GPT-4 apenas | Imagem → texto. Não gera imagens. |
| **Instrução** | ✅ Nativo | Segue instruções complexas com alta fidelidade |
| **Segurança** | ✅ Básico | RLHF reduziu toxicidade e alucinações perigosas |
| **System prompt** | ✅ Disponível | Permite definir comportamento base do modelo |

### O Que Isso Significa para Agentes

**Pela primeira vez, agentes de longa duração são tecnicamente possíveis.**

Com 100K tokens de contexto (Claude 2), uma conversa de 2-3 horas cabe inteira na memória do modelo. Com RLHF, o modelo segue instruções de forma confiável. E com GPT-4, o reasoning é bom o suficiente para tarefas multi-step.

Mas ainda há problemas fundamentais:

| Problema | Descrição | Impacto no KODA |
|---|---|---|
| **Contexto passivo** | O modelo "lembra" mas não "gerencia" memória | Informações críticas se perdem no meio de ruído |
| **Sem tool use nativo** | Não pode chamar APIs, consultar DBs, ler arquivos | Catálogo precisa estar no prompt (impraticável) |
| **Alucinação residual** | Ainda inventa fatos, especialmente em contexto longo | Pode recomendar produtos inexistentes |
| **Custo de contexto** | Cada token no contexto custa dinheiro. 100K tokens = caro. | Conversas longas são proibitivamente caras |
| **Latência** | Modelos grandes = respostas lentas | Experiência do cliente degrada |

**Para o KODA:** Agora você pode construir um agente funcional, mas ele ainda é "cego" e "caro":

```
KODA ERA 3:
  ✅ Conversa de 2 horas cabe no contexto
  ✅ Segue instruções de forma confiável
  ✅ Raciocina sobre recomendações
  ❌ Não consulta catálogo em tempo real (catálogo no prompt)
  ❌ Não processa pagamento (sem API calls)
  ❌ Não verifica estoque (sem tool use)
  ❌ Custo alto (R$ 0.50-2.00 por conversa longa)
  ❌ Lentidão (5-15 segundos por resposta)
```

### O Padrão de Arquitetura da Era

```
┌──────────────────────────────────────────────────────────┐
│                   ERA 3: Alignment                       │
│                                                          │
│  INPUT → [System Prompt] → [Context Window] → LLM → OUTPUT│
│            │                    │                         │
│            │                    │                         │
│     Define persona      Histórico completo               │
│     e restrições        da conversa cabe                 │
│                         no contexto (100K)                │
│                                                          │
│  Primeiros harness patterns:                             │
│  - State persistence externa (arquivos JSON)             │
│  - History compression (resumir conversa)                │
│  - Validation layers (checar output)                     │
└──────────────────────────────────────────────────────────┘
```

Esta era introduz os **3 problemas fundamentais** que você estuda no Nível 1:
1. **Context Amnesia:** Mesmo com 100K tokens, informações se perdem em conversas muito longas
2. **Planning-Execution Collapse:** Sem tool use, o agente tenta "pensar" e "fazer" na mesma chamada
3. **Self-Evaluation Collapse:** Sem ferramentas externas, o agente se auto-avalia (mal)

### Lição para Long-Running Agents

> **Princípio 4 (Context Window é Memória, Não Inteligência):** Um contexto de 100K tokens permite que o modelo "lembre" de mais coisas, mas não que ele "saiba" o que é importante lembrar. O harness precisa decidir o que manter e o que descartar — o modelo não faz isso sozinho.

> **Princípio 5 (Alinhamento ≠ Confiabilidade):** RLHF faz o modelo seguir instruções, mas não garante que ele vai acertar. Um agente alinhado ainda pode recomendar produto errado com confiança absoluta. A diferença é que agora ele pede desculpas depois.

---

## 🌐 Era 4: Multimodal & Reasoning (2023-2024) — "O Modelo Vê e Pensa"

### Modelos-chave
- **GPT-4 Turbo** (OpenAI, Novembro 2023): Contexto de 128K tokens, JSON mode, cheaper
- **Claude 3** (Anthropic, Março 2024): Família Opus/Sonnet/Haiku. Contexto de 200K. Visão.
- **Gemini 1.5** (Google, Fevereiro 2024): Contexto de 1M tokens (experimental). Multimodal nativo.
- **Llama 3** (Meta, Abril 2024): 8B e 70B. Contexto de 8K.
- **GPT-4o** (OpenAI, Maio 2024): Omni-modal. Real-time voice. Mais rápido e barato.
- **Claude 3.5 Sonnet** (Anthropic, Junho 2024): Melhor custo-benefício. 200K contexto.

### Capacidades

| Capacidade | Status | Detalhe |
|---|---|---|
| **Geração de texto** | ✅ Excelente | Qualidade de produção |
| **Contexto contínuo** | ✅ 128K-1M | 100K-750K palavras. Múltiplas horas de conversa. |
| **Reasoning** | ✅ Muito bom | Chain-of-thought avançado. Pode decompor problemas complexos. |
| **Tool Use** | ✅ Emergente | Function calling começa a aparecer como feature nativa |
| **Multimodal** | ✅ Nativo | Imagem, áudio, vídeo → texto. Visão é padrão. |
| **Instrução** | ✅ Nativo | System prompts complexos. Multi-turn consistency. |
| **JSON Mode** | ✅ Disponível | Structured outputs garantidos. Crítico para agentes. |
| **Velocidade** | ✅ Melhorou | GPT-4o e Claude 3.5 Sonnet são significativamente mais rápidos |
| **Custo** | ✅ Caindo | GPT-4 Turbo 3x mais barato que GPT-4. Claude Haiku é muito barato. |

### O Que Isso Significa para Agentes

**Tool use e structured outputs mudam tudo.**

Pela primeira vez, o modelo pode:
- **Chamar APIs:** Consultar catálogo, verificar estoque, processar pagamento
- **Ler e escrever arquivos:** Persistir estado entre chamadas
- **Executar código:** Fazer cálculos, validar dados, transformar formatos
- **Emitir JSON estruturado:** Comunicação confiável entre componentes do harness

```
ANTES (Era 3):
  KODA: "Baseado no que sei, recomendo Whey X por R$ 120"
  [Espera que o preço esteja correto. Não está. Cliente reclama.]

DEPOIS (Era 4):
  KODA: [Chama API de catálogo] → Recebe preço real: R$ 125
  KODA: [Chama API de estoque] → Recebe qtd: 47 unidades
  KODA: [Chama API de desconto] → Calcula: R$ 125 - 15% = R$ 106.25
  KODA: "Recomendo Whey X por R$ 106.25 (15% off). 47 em estoque."
  [Tudo verificado em tempo real. Confiável.]
```

**Para o KODA:** O agente agora pode ser "conectado" ao mundo real:

```
KODA ERA 4:
  ✅ Conversa longa com contexto de 200K tokens
  ✅ Consulta catálogo em tempo real (function calling)
  ✅ Verifica estoque (API call)
  ✅ Calcula preços com desconto (API call + math)
  ✅ Processa pagamento (API call)
  ✅ Emite JSON estruturado para coordinacão entre componentes
  ✅ Custo médio (R$ 0.10-0.50 por conversa)
  ✅ Latência aceitável (2-5 segundos por resposta)
  ❌ Planejamento multi-step ainda frágil
  ❌ Auto-correção limitada
  ❌ Sem coordenação entre múltiplos agentes
```

### O Padrão de Arquitetura da Era

```
┌──────────────────────────────────────────────────────────────┐
│                    ERA 4: Multimodal                         │
│                                                              │
│                        ┌──────────┐                          │
│  USER INPUT ──────────→│  ROUTER  │                          │
│                        └────┬─────┘                          │
│                             │                                │
│              ┌──────────────┼──────────────┐                │
│              │              │              │                 │
│         ┌────▼────┐   ┌────▼────┐   ┌─────▼─────┐          │
│         │  LLM    │   │ TOOLS   │   │  MEMORY   │          │
│         │ (brain) │   │ (hands) │   │  (state)  │          │
│         └────┬────┘   └────┬────┘   └─────┬─────┘          │
│              │              │              │                 │
│              └──────────────┼──────────────┘                │
│                             │                                │
│                        ┌────▼─────┐                          │
│                        │ VALIDATOR│                          │
│                        └────┬─────┘                          │
│                             │                                │
│                        ┌────▼─────┐                          │
│                        │  OUTPUT  │                          │
│                        └──────────┘                          │
│                                                              │
│  Três componentes separados: cérebro (LLM), mãos (tools),   │
│  memória (state). Coordenados por router e validator.        │
└──────────────────────────────────────────────────────────────┘
```

Esta arquitetura de 3 componentes é a base de todo agente moderno:
1. **Brain (LLM):** Raciocina, decide o que fazer, gera respostas
2. **Hands (Tools):** Executa ações no mundo real (APIs, DBs, arquivos)
3. **Memory (State):** Persiste informações entre chamadas (arquivos JSON, DB)

### Lição para Long-Running Agents

> **Princípio 6 (Tool Use é o Divisor de Águas):** Um agente sem tools é um oráculo. Um agente com tools é um executor. A diferença é a mesma que entre "saber a resposta" e "fazer acontecer". Tool use transforma agentes de "consultivos" para "transacionais".

> **Princípio 7 (Structured Outputs São Contratos):** JSON mode e function calling não são conveniências — são contratos de comunicação. Quando o LLM emite JSON estruturado, o harness pode validar, transformar, e rotear sem ambiguity parsing.

---

## 🤖 Era 5: Agent-Native (2024-2025) — "Modelos Construídos Para Agentes"

### Modelos-chave
- **Claude 3.5 Opus** (Anthropic, 2024): Contexto de 200K, tool use nativo, computer use (beta)
- **GPT-4.5** (OpenAI, 2024): Melhor reasoning, tool use otimizado, parallel function calling
- **Gemini 2.0** (Google, Dezembro 2024): Agente nativo. Multimodal completo. Agenteic capabilities.
- **Claude 4 Sonnet** (Anthropic, 2025): Contexto 200K. Computer use público. Fast.
- **GPT-5** (OpenAI, 2025): Reasoning avançado. Agentic workflow nativo.
- **DeepSeek-R1** (DeepSeek, 2025): Open-source reasoning model. Chain-of-thought público.

### O Salto Quântico: Modelos Pensam Como Agentes

Esta era não é sobre "modelos melhores". É sobre **modelos que foram treinados especificamente para serem agentes:**

```
ANTES (Era 4):
  Modelo: "Sou um assistente. Me pergunte coisas."
  Você: "Processa esse pedido."
  Modelo: "Claro! Deixa eu... hmm... como eu faço isso?"
  [Você precisa ensinar o modelo a ser agente via prompt engineering]

DEPOIS (Era 5):
  Modelo: "Sou um agente. Me dê objetivos."
  Você: "Processa esse pedido."
  Modelo: [Automaticamente: planeja → executa → verifica → reporta]
  [O modelo já sabe o workflow de um agente]
```

### Capacidades

| Capacidade | Status | Detalhe |
|---|---|---|
| **Geração de texto** | ✅ Excelente | Qualidade indistinguível de humano |
| **Contexto contínuo** | ✅ 200K-2M | 150K-1.5M palavras. Dias de conversa. |
| **Reasoning** | ✅ Avançado | Multi-step planning. Self-correction. Metacognition emergente. |
| **Tool Use** | ✅ Nativo | Function calling otimizado. Parallel tool execution. |
| **Computer Use** | ✅ Beta/Público | Modelo pode controlar mouse/teclado. Navegar web. |
| **Multimodal** | ✅ Completo | Texto, imagem, áudio, vídeo. Input e output. |
| **Agentic Training** | ✅ Especializado | Modelos treinados em workflows de agente (plan→execute→verify) |
| **Long-horizon tasks** | ✅ Emergente | Pode executar tarefas de 50+ passos sem degradação |
| **Cost efficiency** | ✅ Otimizado | Modelos pequenos (Haiku, Flash) fazem tarefas simples por fração de centavo |

### O Que Isso Significa para Agentes

**Os modelos agora são agent-native.** Isso significa que:

1. **Planejamento autônomo:** O modelo pode decompor "processa esse pedido" em 6 sub-tarefas automaticamente, sem você precisar programar cada passo.

2. **Self-correction:** O modelo detecta quando algo deu errado e tenta de novo com abordagem diferente. O harness não precisa mais implementar toda a lógica de retry.

3. **Parallel execution:** O modelo pode chamar múltiplas tools simultaneamente. Verificar catálogo, estoque E preço ao mesmo tempo.

4. **Computer use:** O modelo pode literalmente usar um computador: abrir browser, navegar, clicar, preencher formulários. Isso abre possibilidades que não existiam.

5. **Metacognition emergente:** O modelo começa a "saber o que não sabe" e pedir clarificação ou buscar informação.

**Para o KODA:** O agente agora pode operar com autonomia muito maior:

```
KODA ERA 5:
  ✅ Conversa de múltiplos dias com contexto de 200K+
  ✅ Planejamento autônomo de pedidos complexos
  ✅ Tool use paralelo (consulta catálogo + estoque + preço de uma vez)
  ✅ Self-correction (detecta e corrige erros sem intervenção)
  ✅ Computer use (navega sistemas legados se necessário)
  ✅ Custo baixo (modelos pequenos para tarefas simples: R$ 0.001)
  ✅ Latência baixa (modelos rápidos: < 1 segundo)
  ⚠️ Coordenação multi-agente ainda manual
  ⚠️ Garantias de segurança ainda dependem do harness
```

### O Padrão de Arquitetura da Era

```
┌──────────────────────────────────────────────────────────────────┐
│                     ERA 5: Agent-Native                          │
│                                                                  │
│  USER GOAL ──→ ┌──────────────┐                                  │
│                │   PLANNER    │ ← Modelo decompõe objetivo       │
│                └──────┬───────┘   em sub-tarefas automaticamente │
│                       │                                          │
│          ┌────────────┼────────────┐                            │
│          │            │            │                             │
│     ┌────▼────┐  ┌────▼────┐  ┌───▼──────┐                      │
│     │EXECUTOR │  │EXECUTOR │  │EXECUTOR  │  ← Paralelo          │
│     │  (LLM)  │  │  (LLM)  │  │  (LLM)   │                      │
│     └────┬────┘  └────┬────┘  └───┬──────┘                      │
│          │            │            │                             │
│          └────────────┼────────────┘                            │
│                       │                                          │
│                ┌──────▼───────┐                                  │
│                │  VERIFIER    │ ← Modelo verifica cada resultado │
│                └──────┬───────┘                                  │
│                       │                                          │
│                ┌──────▼───────┐                                  │
│                │  AGGREGATOR  │ ← Junta resultados,              │
│                └──────┬───────┘   self-correct se necessário     │
│                       │                                          │
│                ┌──────▼───────┐                                  │
│                │   OUTPUT     │                                  │
│                └──────────────┘                                  │
│                                                                  │
│  O harness agora é mais "orquestrador" que "controlador".        │
│  O modelo tem agência. O harness define guardrails.              │
└──────────────────────────────────────────────────────────────────┘
```

### Lição para Long-Running Agents

> **Princípio 8 (Agência vs Controle):** Quanto mais agent-native o modelo, menos controle procedural você precisa exercer. Mas MAIS importante se tornam os guardrails. Um modelo com agência sem guardrails é um risco. Com guardrails, é uma força multiplicadora.

> **Princípio 9 (O Harness Migra de "Como Fazer" para "O Que Não Fazer"):** Nas eras anteriores, o harness dizia ao modelo COMO fazer cada coisa. Na Era 5, o modelo já sabe COMO. O harness agora define O QUE NÃO FAZER: constraints, limites, verificações de segurança.

---

## 🌌 Era 6: Post-Agent (2025-2026+) — "Agentes que Constroem Agentes"

### Modelos-chave
- **Claude Opus 4.5** (Anthropic, 2025): Contexto de 500K. Metacognition avançada.
- **Claude Sonnet 4.6** (Anthropic, 2026): Contexto de 200K, otimizado para custo. Agentic workflows nativos.
- **Claude Opus 4.6** (Anthropic, 2026): Contexto de 1M tokens. Agentic reasoning. Multi-agent coordination nativa.
- **DeepSeek-V4** (DeepSeek, 2026): Open-source, reasoning avançado.
- **Gemini 3.0** (Google, 2026): 2M contexto. Agente nativo. Integração Google ecosystem.

### Capacidades

| Capacidade | Status | Detalhe |
|---|---|---|
| **Geração de texto** | ✅ Excelente | Qualidade super-humana em domínios específicos |
| **Contexto contínuo** | ✅ 1M-10M | 750K-7.5M palavras. Semanas de conversa contínua. |
| **Reasoning** | ✅ Super-humano | Metacognition. Self-reflection. Multi-perspective analysis. |
| **Tool Use** | ✅ Nativo e Rico | Centenas de tools simultâneas. Tool discovery. Tool composition. |
| **Computer Use** | ✅ Nativo | Interage com qualquer interface. Automação de workflows complexos. |
| **Multimodal** | ✅ Ubíquo | Todos os modelos são multimodais. Input/output em qualquer formato. |
| **Multi-agent** | ✅ Emergente | Modelos podem coordenar múltiplas instâncias de si mesmos |
| **Autonomous planning** | ✅ Avançado | Planejamento de 100+ passos. Replanning dinâmico. |
| **Safety** | ✅ Constitucional | Modelos têm "constituição" interna. Auto-regulação. |
| **Cost** | ✅ Democratizado | Agentes custam centavos por hora de operação |

### O Que Isso Significa para Agentes

**O conceito de "agente" e "modelo" começa a se fundir.**

Na Era 6:
- O modelo não é mais um "componente" do agente — o modelo **é** o agente
- Coordenação multi-agente é nativa, não construída externamente
- O modelo pode spawnar sub-agentes, delegar tarefas, consolidar resultados
- Contexto de 1M+ tokens elimina a distinção entre "memória de curto prazo" (context window) e "memória de longo prazo" (state persistence)
- Metacognition permite que o modelo avalie sua própria performance e melhore continuamente

```
ERA 1:    LLM é um componente passivo. Você constrói o agente.
ERA 3:    LLM pode ser o cérebro. Você constrói o corpo (tools, state).
ERA 5:    LLM é o agente. Você constrói os guardrails.
ERA 6:    O agente constrói outros agentes. Você define objetivos e constraints.
```

**Para o KODA:** O agente atinge um nível de autonomia antes impensável:

```
KODA ERA 6:
  ✅ Conversas de semanas sem perda de contexto
  ✅ Planejamento e execução completamente autônomos
  ✅ Coordenação multi-agente nativa (KODA spawna sub-agentes para
     busca, validação, pagamento, fulfillment)
  ✅ Self-improvement (aprende com cada interação)
  ✅ Custo marginal próximo de zero
  ✅ Latência imperceptível (< 500ms)
  ✅ Segurança constitucional (não precisa de validação externa
     para casos simples)
  ⚠️ Governança: como auditar um agente que se auto-modifica?
  ⚠️ Alinhamento: se o agente é totalmente autônomo, como garantir
     que ele continua alinhado com objetivos do negócio?
```

### O Padrão de Arquitetura da Era

```
┌──────────────────────────────────────────────────────────────────┐
│                     ERA 6: Post-Agent                           │
│                                                                  │
│                   ┌──────────────────┐                          │
│  BUSINESS GOAL ──→│  ORCHESTRATOR    │                          │
│                   │  (Meta-Agente)   │                          │
│                   └────────┬─────────┘                          │
│                            │                                     │
│            ┌───────────────┼───────────────┐                    │
│            │               │               │                     │
│       ┌────▼────┐    ┌────▼────┐    ┌─────▼─────┐              │
│       │ AGENTE  │    │ AGENTE  │    │ AGENTE    │              │
│       │  KODA   │    │  KODA   │    │  KODA     │   ← Spawned  │
│       │ (vendas)│    │(estoque)│    │(fulfill)  │     on demand│
│       └────┬────┘    └────┬────┘    └─────┬─────┘              │
│            │               │               │                     │
│            └───────────────┼───────────────┘                    │
│                            │                                     │
│                   ┌────────▼─────────┐                          │
│                   │   GOVERNANCE     │                          │
│                   │   (Constituição) │  ← Regras imutáveis      │
│                   └────────┬─────────┘                          │
│                            │                                     │
│                   ┌────────▼─────────┐                          │
│                   │  HUMAN-IN-THE-   │                          │
│                   │  LOOP (opcional) │  ← Intervenção só quando │
│                   └──────────────────┘    necessário             │
│                                                                  │
│  O harness como "meta-agente". O código define a constituição.  │
│  Os agentes operam dentro dela com autonomia quase total.        │
└──────────────────────────────────────────────────────────────────┘
```

### Lição para Long-Running Agents

> **Princípio 10 (A Constituição é o Novo Código):** Quando agentes são autônomos, o código procedural perde relevância. O que importa são as regras constitucionais: o que o agente NUNCA pode fazer, independentemente do objetivo. A engenharia de harness migra de "como fazer" para "constituição + auditoria".

> **Princípio 11 (O Paradoxo da Autonomia):** Quanto mais autônomo o agente, mais importante é o design das constraints. Um agente da Era 1 não pode causar dano porque não pode fazer nada. Um agente da Era 6 pode causar dano em escala — a não ser que a constituição seja robusta.

---

## 📊 Tabela Comparativa: Capacidades por Era

| Dimensão | Era 1 (2018-19) | Era 2 (2020-21) | Era 3 (2022-23) | Era 4 (2023-24) | Era 5 (2024-25) | Era 6 (2025-26+) |
|---|---|---|---|---|---|---|
| **Contexto máximo** | 512-1024 tokens | 2048 tokens | 4K-100K tokens | 128K-1M tokens | 200K-2M tokens | 1M-10M tokens |
| **Horas de conversa** | < 5 min | ~15 min | ~2 horas | ~8 horas | ~24 horas | Semanas |
| **Reasoning** | Pattern match | Few-shot | Chain-of-thought | Multi-step planning | Autônomo | Metacognition |
| **Tool Use** | Nenhum | Nenhum | Via prompt | Function calling | Nativo e paralelo | Composição de tools |
| **Multimodal** | Não | Não | Imagem (GPT-4) | Completo | Ubíquo | Nativo total |
| **Self-correction** | Não | Não | Limitada | Básica | Boa | Avançada |
| **Multi-agent** | Não | Não | Não | Manual | Orquestrado | Autônomo |
| **Custo/conversa** | N/A (inviável) | $0.50-2.00 | $0.10-0.50 | $0.05-0.20 | $0.01-0.05 | < $0.01 |
| **Latência/resposta** | 10-30s | 5-15s | 3-10s | 1-5s | 0.5-2s | < 500ms |
| **Confiabilidade** | < 60% | ~70% | ~85% | ~92% | ~97% | ~99%+ |
| **Agente possível?** | Não | Protótipo | Sim, com limitações | Sim, funcional | Sim, avançado | Sim, autônomo |
| **Padrão de harness** | Prompt | Prompt + compress | State + validation | Gen/Eval + Contracts | Guardrails + Orchestration | Constitution + Audit |

---

## 🔀 O Impacto de Cada Era no Design de Harness

### A Migração do Esforço de Engenharia

Cada nova capacidade do modelo não elimina a necessidade de engenharia — ela **move o esforço** para outra camada:

```
ERA 1-2:    95% do esforço → Prompt Engineering
              5% do esforço → Infraestrutura básica
             
ERA 3:      60% do esforço → State Management (combater amnesia)
             25% do esforço → Validation (combater alucinação)
             15% do esforço → Prompt Engineering

ERA 4:      40% do esforço → Tool Integration (function calling)
             30% do esforço → State Management
             20% do esforço → Validation
             10% do esforço → Prompt Engineering

ERA 5:      35% do esforço → Guardrails & Safety
             25% do esforço → Multi-agent Coordination
             20% do esforço → Tool Integration
             15% do esforço → Validation
              5% do esforço → Prompt Engineering

ERA 6:      40% do esforço → Constitution Design
             30% do esforço → Audit & Governance
             20% do esforço → Guardrails & Safety
             10% do esforço → Tool Integration
              0% do esforço → Prompt Engineering (modelo sabe)
```

### Visualização: O Deslocamento do Esforço

```
ESFORÇO DE ENGENHARIA POR CAMADA AO LONGO DO TEMPO:

100% ┤
     │  ████████░░░░░░░░░░░░░░░░░░  Era 1-2
     │  ██████░░░░░░░░░░░░░░░░░░░░
     │  
 80% ┤  ████████████░░░░░░░░░░░░░░  Era 3
     │  ████████████████░░░░░░░░░░
     │  
 60% ┤  ████████████████████░░░░░░  Era 4
     │  ████████████████████████░░
     │  
 40% ┤  ██████████████████████████  Era 5
     │  ██████████████████████████
     │  
 20% ┤  ██████████████████████████  Era 6
     │  ██████████████████████████
     │  
  0% └──┴─────┴─────┴─────┴─────┴──
       Prompt  State  Tools  Safety  Audit
       
  ████ = Onde o esforço está concentrado
  ░░░░ = Onde o esforço é mínimo (modelo resolve)
```

**Interpretação:**
- Prompt engineering domina as primeiras eras, depois desaparece
- State management cresce na Era 3, depois estabiliza (modelos têm mais contexto)
- Tool integration explode na Era 4, depois estabiliza
- Safety/guardrails cresce continuamente — nunca desaparece
- Audit/governance é o novo fronteira — surge na Era 5-6 e tende a dominar

### O Que Isso Significa Para Seu Time

Se você está construindo um agente hoje (2026, Era 6):

| Seu foco deve ser | Não perca tempo com |
|---|---|
| **Constitution Design:** Regras imutáveis que o agente nunca viola | Prompt engineering elaborado (modelo já entende) |
| **Audit Trail:** Todo ação do agente é rastreável e auditável | State management manual (modelo tem 1M contexto) |
| **Guardrails:** Limites claros do que o agente pode fazer | Validação de output simples (modelo já é confiável) |
| **Human-in-the-loop:** Quando e como escalar para humano | Tool integration básica (modelo descobre tools) |
| **Multi-agent governance:** Como agentes coordenam sem conflitos | Single-agent optimization (vários agentes são o padrão) |

---

## 🧬 As Capacidades que Possibilitaram Long-Running Agents

Nem toda capacidade de modelo é igualmente importante para agentes de longa duração. Algumas são **critical path** — sem elas, o agente simplesmente não funciona. Outras são **nice-to-have** — melhoram a experiência mas não bloqueiam.

### Critical Path (Sem Isso, Não Dá)

```
CAPACIDADE                 ERA EM QUE       IMPACTO NO AGENTE
                           SURGIU

Context Window Longa        Era 3 (2022)    Permite que o agente "lembre" de conversas
(100K+ tokens)                              inteiras sem perder informações. Sem isso,
                                            agentes de > 30 min são impossíveis.

Instruction Following       Era 3 (2022)    O agente precisa seguir instruções de forma
(RLHF)                                      confiável. Se o modelo "faz o que quer",
                                            você não tem agente, você tem arte generativa.

Tool Use /                   Era 4 (2023)    O agente precisa interagir com o mundo:
Function Calling                            consultar DBs, chamar APIs, ler/escrever
                                            arquivos. Sem tools, o agente é um oráculo
                                            que só fala, não age.

Structured Outputs           Era 4 (2023)    Comunicação entre componentes do harness
(JSON Mode)                                 depende de outputs estruturados e confiáveis.
                                            Sem JSON mode, cada parse é uma aposta.

Reasoning                    Era 4 (2023)    Para tarefas multi-step, o agente precisa
(Chain-of-Thought)                          decompor problemas, planejar passos, e
                                            verificar resultados intermediários.

Multi-turn Consistency       Era 5 (2024)    Em conversas longas, o agente precisa manter
                                            personalidade, tom, e conhecimento consistente
                                            ao longo de dezenas de turnos.
```

### Nice-to-Have (Melhora, Mas Não Bloqueia)

```
CAPACIDADE                 ERA EM QUE       IMPACTO NO AGENTE
                           SURGIU

Multimodal Input             Era 4 (2023)    Permite que o agente entenda imagens, áudio.
                                            Útil para KODA (cliente manda foto de produto),
                                            mas não essencial para o core loop.

Computer Use                 Era 5 (2024)    Permite que o agente interaja com sistemas
                                            que não têm API. Útil para integração com
                                            sistemas legados, mas não essencial.

Real-time Voice              Era 5 (2024)    Latência de voz é importante para experiência
                                            do cliente (WhatsApp voice notes), mas o core
                                            do agente funciona sem isso.

Multimodal Output            Era 5 (2024)    Gerar imagens, áudio, vídeo. Útil para
                                            marketing (gerar imagem do produto), mas
                                            não essencial para vendas.

Metacognition                Era 6 (2025)    "Saber o que não sabe" melhora confiabilidade,
                                            mas um harness bem desenhado supre essa
                                            necessidade com validation layers.
```

### Como o KODA se Beneficiou de Cada Capacidade

| Capacidade | Quando KODA Adotou | Impacto Medido |
|---|---|---|
| Contexto 100K+ (Era 3) | Março 2024 (Claude 3) | Conversas de 2h+ se tornaram viáveis. Antes: máx 30 min. |
| Instruction Following (Era 3) | Março 2024 (Claude 3) | Seguir rubrics de recomendação. Precisão subiu de 65% para 82%. |
| Tool Use (Era 4) | Junho 2024 (Claude 3.5) | Catálogo e estoque em tempo real. Recomendações erradas caíram 80%. |
| Structured Outputs (Era 4) | Junho 2024 (GPT-4o JSON) | Comunicação entre Generator e Evaluator. Debugging ficou 10x mais rápido. |
| Reasoning (Era 4) | Setembro 2024 (o1-preview) | Decompor pedidos complexos em sprints. Erros de processamento caíram 60%. |
| Agent-Native (Era 5) | Março 2025 (Claude 4) | Planejamento autônomo de fulfillment. Same-day delivery: 92% → 98%. |
| Contexto 1M (Era 6) | Maio 2026 (Opus 4.6) | Memória de cliente multi-sessão. LTV aumentou 40%. |

---

## 🔮 Projeções Futuras: O Que Vem Depois de 2026?

### Curto Prazo (2026-2027): Consolidação

```
Tendências:
  1. Contexto 10M+ tokens se torna padrão
     → "Memória infinita" para agentes. State persistence manual
       começa a ser substituído por contexto nativo.
  
  2. Multi-agent coordination se torna nativa
     → Frameworks como o harness do KODA são absorvidos pelos
       próprios modelos. Você não "programa" coordenação;
       você "declara" objetivos de coordenação.
  
  3. Computer use se torna mainstream
     → Agentes podem operar qualquer sistema com interface
       gráfica. O "tool use" via API é complementado por
       "computer use" para sistemas sem API.
  
  4. Custo marginal → zero
     → Modelos pequenos (tipo Haiku) fazem 90% das tarefas
       por frações de centavo. Modelos grandes são reservados
       para tarefas complexas. Custo total de um agente 24/7
       fica abaixo de $10/mês.
```

### Médio Prazo (2027-2028): Autonomia

```
Tendências:
  1. Agentes auto-evolutivos
     → O agente aprende com cada interação e melhora seu próprio
       comportamento sem intervenção humana. Harness patterns
       são auto-otimizados.
  
  2. Continuous learning
     → Fine-tuning contínuo baseado em interações reais.
       O agente de hoje é melhor que o de ontem. Sempre.
  
  3. Cross-agent memory
     → Memória compartilhada entre agentes. Se um agente KODA
       aprende que um cliente prefere entrega noturna, todos
       os agentes KODA sabem disso instantaneamente.
  
  4. Agent marketplaces
     → Agentes especializados são "contratados" on-demand.
       KODA pode contratar um "agente de logística" terceirizado
       para otimizar rotas de entrega.
```

### Longo Prazo (2028-2030): Invisibilidade

```
Tendências:
  1. Agentes como infraestrutura
     → Agentes são tão ubíquos quanto servidores web hoje.
       Você não "constrói" um agente; você "configura" um.
  
  2. The Harness Disappears
     → O que hoje chamamos de "harness" (state persistence,
       validation, coordination) é absorvido pelo runtime
       do modelo. Assim como ninguém mais escreve seu próprio
       memory manager, ninguém mais escreverá seu próprio
       agent harness.
  
  3. AI-Native Businesses
     → Empresas são construídas com agentes como first-class
       citizens. O organograma inclui agentes ao lado de
       humanos. KPIs medem performance mista humano+agente.
  
  4. The Agent-Human Symbiosis
     → Agentes não substituem humanos — eles amplificam.
       Um vendedor humano + 5 agentes KODA atende 50 clientes
       simultaneamente. O humano faz o que humanos fazem melhor
       (empatia, negociação complexa, criatividade); os agentes
       fazem o que máquinas fazem melhor (memória, velocidade,
       consistência).
```

---

## 📐 Linha do Tempo Visual Detalhada (ASCII Art)

```
═══════════════════════════════════════════════════════════════════════════════
                    MODEL CAPABILITY TIMELINE 2018-2030
═══════════════════════════════════════════════════════════════════════════════

2018 ─┐
      │  GPT-1 (117M params, 512 ctx)
      │  BERT (340M, 512 ctx)
      │  ▸ Era 1: FOUNDATION
      │  ▸ Agentes: IMPOSSÍVEIS
      │
2019 ─┤
      │  GPT-2 (1.5B, 1024 ctx)
      │  T5 (11B)
      │  ▸ Scaling começa a mostrar resultados
      │
2020 ─┤
      │  GPT-3 (175B, 2048 ctx) ← DIVISOR DE ÁGUAS
      │  Scaling Laws paper
      │  ▸ Era 2: SCALE
      │  ▸ Agentes: PROTÓTIPOS
      │
2021 ─┤
      │  Codex (12B)
      │  Gopher (280B)
      │  ▸ Few-shot learning se prova poderoso
      │
2022 ─┤
      │  InstructGPT (GPT-3 + RLHF)
      │  ChatGPT (GPT-3.5 + chat interface)
      │  ▸ Era 3: ALIGNMENT ← DIVISOR DE ÁGUAS
      │  ▸ Agentes: POSSÍVEIS COM LIMITAÇÕES
      │
2023 ─┤
      │  GPT-4 (8K-32K ctx)
      │  Claude 2 (100K ctx) ← PRIMEIRO CONTEXTO LONGO
      │  Llama 2 (open-source)
      │  ▸ Contexto 100K: game-changer para agentes
      │
2024 ─┤
      │  GPT-4 Turbo (128K ctx)
      │  Claude 3 Opus/Sonnet/Haiku (200K ctx)
      │  Gemini 1.5 (1M ctx experimental)
      │  GPT-4o (omni-modal)
      │  Claude 3.5 Sonnet (tool use nativo)
      │  ▸ Era 4: MULTIMODAL & REASONING ← DIVISOR DE ÁGUAS
      │  ▸ Agentes: FUNCIONAIS
      │
2025 ─┤
      │  Claude 4 Sonnet (computer use)
      │  GPT-5 (agentic workflow nativo)
      │  Gemini 2.0 (agent-native)
      │  DeepSeek-R1 (open-source reasoning)
      │  ▸ Era 5: AGENT-NATIVE ← DIVISOR DE ÁGUAS
      │  ▸ Agentes: AVANÇADOS
      │
2026 ─┤ ← ESTAMOS AQUI
      │  Claude Opus 4.6 (1M ctx, agentic reasoning)
      │  Claude Sonnet 4.6 (200K ctx, custo otimizado)
      │  Gemini 3.0 (2M ctx, multi-agent nativo)
      │  ▸ Era 6: POST-AGENT
      │  ▸ Agentes: AUTÔNOMOS
      │
2027 ─┤ ← PROJEÇÃO
      │  Contexto 10M+ padrão
      │  Multi-agent nativo
      │  Computer use mainstream
      │  ▸ Agentes: UBIQUOS
      │
2028 ─┤
      │  Agentes auto-evolutivos
      │  Continuous learning
      │  Cross-agent memory
      │  ▸ Agentes: AUTO-MELHORÁVEIS
      │
2029 ─┤
      │  Agent marketplaces
      │  AI-native businesses
      │  ▸ Agentes: ECONÔMICOS
      │
2030 ─┘
         Agentes como infraestrutura
         Harness desaparece (absorvido pelo runtime)
         Simbiose humano-agente
         ▸ Agentes: INVISÍVEIS

═══════════════════════════════════════════════════════════════════════════════
```

---

---

## 🔗 Estratégias de Coordenação: Como o Design de Agentes Evoluiu

Uma coisa é ter um modelo capaz. Outra é coordenar esse modelo (ou múltiplos modelos) para realizar trabalho útil. As **estratégias de coordenação** evoluíram tanto quanto os próprios modelos.

### Tabela Comparativa de Estratégias de Coordenação

| Estratégia | Era | Descrição | Força | Fraqueza | Exemplo KODA |
|---|---|---|---|---|---|
| **Single-Shot** | 1-2 | Um único prompt → uma única resposta. Sem estado, sem iteração. | Simplicidade extrema. Zero overhead. | Sem memória. Sem correção. Frágil. | KODA responde "temos 3 opções" sem contexto. |
| **Prompt Chain** | 2-3 | Output de um prompt é input do próximo. Pipeline linear. | Decompõe tarefa. Cada passo é focado. | Erro em um passo contamina toda a chain. Sem branches. | Cliente → Classificar intenção → Buscar produtos → Formatar resposta. |
| **Stateful Loop** | 3 | LLM + estado externo (arquivos/DB). Loop: ler estado → gerar → atualizar estado. | Mantém contexto entre turnos. Memória "infinita". | Estado pode corromper. Complexidade de gerenciamento. | KODA mantém customer_context.json entre mensagens. |
| **Generator/Evaluator** | 4 | Dois agentes: um gera, outro avalia. Feedback loop até aprovação. | Qualidade muito superior. Erros detectados e corrigidos. | 2x custo LLM por iteração. Latência maior. | KODA recomenda produto → Evaluator checa alergias → aprova/rejeita. |
| **Sprint Contracts** | 4 | Módulos com contratos explícitos de input/output. Composição garantida. | Confiabilidade entre módulos. Debug fácil. Refatoração segura. | Overhead de definição de contratos. Rigidez vs flexibilidade. | Módulo Search promete: "5 produtos, cada um com {id, preço, lactose_free}". |
| **Tree-of-Thought** | 4-5 | Explora múltiplos caminhos de reasoning em paralelo. Escolhe o melhor. | Melhor decisão em problemas complexos. Explora espaço de soluções. | Custo 3-5x maior. Latência alta. Overkill para tarefas simples. | KODA explora 3 estratégias de recomendação, escolhe a melhor. |
| **Multi-Agent Orchestration** | 5 | Múltiplos agentes especializados coordenados por orquestrador. Paralelismo. | Escalabilidade. Especialização. Tarefas complexas decomponíveis. | Complexidade de coordenação. Possíveis conflitos entre agentes. | KODA spawna agentes de busca, validação, pagamento, fulfillment. |
| **Swarm Intelligence** | 5-6 | Múltiplos agentes colaboram sem orquestrador central. Emergência. | Robusto (sem single point of failure). Adaptável. | Imprevisível. Difícil de debugar. Resultados não determinísticos. | Múltiplos KODAs negociam entre si para achar melhor rota de entrega. |
| **Constitutional Governance** | 6 | Agentes autônomos operam dentro de uma "constituição" de regras imutáveis. | Autonomia com segurança. Escalabilidade máxima. | Design da constituição é crítico. Difícil prever todas as situações. | Constituição KODA: "Nunca recomendar produto que viole restrição médica do cliente." |
| **Meta-Agent Self-Organization** | 6+ | Um meta-agente spawna, monitora, e destrói sub-agentes conforme necessidade. | Adaptação dinâmica. Eficiência (só spawna o necessário). | Altíssima complexidade. Requer modelos com metacognition. | KODA detecta pico de demanda → spawna 10 agentes de vendas temporários → destrói quando pico passa. |

### Qual Estratégia Usar? Fluxo de Decisão

```
"Preciso coordenar agentes para esta tarefa. Qual estratégia?"
                          │
          ┌───────────────┴───────────────┐
          │ A tarefa tem critérios        │
          │ de qualidade objetivos?       │
          └───────────────┬───────────────┘
                          │
              ┌───────────┴───────────┐
              │ SIM                   │ NÃO
              ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐
    │ A tarefa pode    │     │ A tarefa precisa │
    │ ser decomposta   │     │ de criatividade? │
    │ em sub-tarefas   │     └────────┬────────┘
    │ independentes?   │              │
    └────────┬─────────┘     ┌────────┴────────┐
             │               │ SIM    │ NÃO    │
     ┌───────┴───────┐       ▼        ▼         │
     │SIM    │ NÃO   │  Tree-of-  Single-      │
     ▼        ▼       │  Thought   Shot         │
  ┌──────┐ ┌────────┐ │                         │
  │Multi-│ │Gen/Eval│ │                         │
  │Agent │ │+ Sprint│ │                         │
  │+     │ │Contracts│                         │
  │Guard-│ └────────┘ │                         │
  │rails │            │                         │
  └──────┘            │                         │
                      │                         │
          ┌───────────┴───────────┐             │
          │ O agente opera com    │             │
          │ alta autonomia?       │             │
          └───────────┬───────────┘             │
                      │                         │
              ┌───────┴───────┐                │
              │SIM    │ NÃO   │                 │
              ▼        ▼                        │
        ┌──────────┐ ┌────────┐                │
        │Constitu- │ │Stateful│                │
        │tional    │ │Loop +  │                │
        │Governance│ │Human-in│                │
        └──────────┘ │-Loop   │                │
                     └────────┘                │
                                               │
                                               │
```

### Exemplo: Como a Estratégia Mudou para o Mesmo Problema

**Problema:** KODA precisa recomendar um produto para um cliente.

| Era | Estratégia | Implementação |
|---|---|---|
| **Era 2** | Single-Shot | Prompt: "Cliente quer whey até R$ 150. Recomende." → resposta. |
| **Era 3** | Stateful Loop | Lê customer_context.json → Prompt com histórico → resposta → salva estado. |
| **Era 4** | Generator/Evaluator | Generator gera 5 opções → Evaluator aprova melhor → resposta. |
| **Era 5** | Multi-Agent | Agente-Search busca produtos, Agente-Validate checa restrições, Agente-Price calcula desconto, em paralelo. |
| **Era 6** | Constitutional | Meta-agente decide automaticamente qual estratégia usar baseado na complexidade do pedido e nas regras da constituição. |

---

## 🎯 Aplicação em KODA: Como Cada Era Moldou Nossa Arquitetura

O KODA não foi construído de uma vez. Ele evoluiu junto com os modelos. Vamos ver como as decisões arquiteturais do KODA foram diretamente influenciadas pelas capacidades disponíveis em cada era.

### Linha do Tempo do KODA vs. Timeline dos Modelos

```
KODA v0.1 (2023-Q4)     KODA v1.0 (2024-Q2)    KODA v2.0 (2025-Q1)    KODA v3.0 (2026-Q2)
     │                       │                      │                      │
     │  Era 3                │  Era 4               │  Era 5               │  Era 6
     │  GPT-4 (8K)           │  Claude 3.5 (200K)   │  Claude 4 (agente)   │  Opus 4.6 (1M)
     │                       │                      │                      │
     ▼                       ▼                      ▼                      ▼
┌─────────────┐     ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ Prompt      │     │ Generator/    │      │ Multi-Agent   │      │ Autonomous    │
│ Engineering │ ──→ │ Evaluator     │ ──→  │ Orchestration │ ──→  │ Constitution  │
│ + Regras    │     │ + Tool Use    │      │ + Guardrails  │      │ + Audit       │
└─────────────┘     └───────────────┘      └───────────────┘      └───────────────┘
```

### Era 3 → KODA v0.1: "O Protótipo"

**Contexto:** GPT-4 com 8K tokens. Sem function calling maduro.

**Arquitetura:**
- Prompt engineering pesado para definir persona e comportamento
- Catálogo de produtos hardcoded no system prompt (sim, sério — 200 produtos no prompt)
- Validação manual por regex ("se output contém 'R$', é um preço?")
- Sem integração com sistemas reais (tudo mockado)
- Conversas máximas de 30 minutos

**Resultado:** Funcionava em demo. Quebrava em produção.
**Precisão:** ~65%
**Custo por conversa:** R$ 1.50

### Era 4 → KODA v1.0: "O Agente Funcional"

**Contexto:** Claude 3.5 com 200K tokens. Function calling nativo. JSON mode.

**Migração arquitetural:**
- Catálogo migrou do system prompt para API calls (function calling)
- Generator/Evaluator pattern implementado
- State persistence via arquivos JSON
- Sprint contracts para coordenação de módulos
- Contexto de 200K tokens → conversas de 2h+ sem compressão

**Arquitetura:**
```
┌─────────────────────────────────────────────┐
│                KODA v1.0                     │
│                                              │
│  WhatsApp ──→ Router ──→ Generator           │
│                  │         (LLM call 1)       │
│                  │              │             │
│                  │         ┌────▼────┐        │
│                  │         │  Tools  │        │
│                  │         │ catalog │        │
│                  │         │ stock   │        │
│                  │         │ pricing │        │
│                  │         └────┬────┘        │
│                  │              │             │
│                  │         ┌────▼────┐        │
│                  │         │Evaluator│        │
│                  │         │(LLM 2)  │        │
│                  │         └────┬────┘        │
│                  │              │             │
│                  └──────────────┘             │
│                         │                     │
│                    ┌────▼────┐                │
│                    │ Response│                │
│                    └─────────┘                │
└─────────────────────────────────────────────┘
```

**Resultado:** Funcionava em produção. Confiável para casos simples.
**Precisão:** ~87%
**Custo por conversa:** R$ 0.35

### Era 5 → KODA v2.0: "O Agente Avançado"

**Contexto:** Claude 4. Modelos agent-native. Multi-agent coordination. Computer use.

**Migração arquitetural:**
- Planner autônomo (modelo decompõe pedidos em sprints)
- Multi-agent: KODA spawna agentes especializados (busca, validação, fulfillment)
- Guardrails substituem validação procedural
- Tool use paralelo (consulta catálogo + estoque + preço simultaneamente)
- Computer use para sistemas legados (ERP sem API)

**Arquitetura:**
```
┌──────────────────────────────────────────────────────┐
│                   KODA v2.0                           │
│                                                       │
│  WhatsApp ──→ Orchestrator (Claude 4)                 │
│                   │                                   │
│       ┌───────────┼───────────┐                      │
│       │           │           │                       │
│  ┌────▼────┐ ┌───▼────┐ ┌───▼────┐                  │
│  │ Search  │ │Validate│ │Fulfill │  ← Agentes        │
│  │ Agent   │ │ Agent  │ │ Agent  │    especializados │
│  └────┬────┘ └───┬────┘ └───┬────┘                  │
│       │           │           │                       │
│       └───────────┼───────────┘                      │
│                   │                                   │
│              ┌────▼────┐                             │
│              │Guardrails│  ← Safety layer             │
│              └────┬────┘                             │
│                   │                                   │
│              ┌────▼────┐                             │
│              │Response │                             │
│              └─────────┘                             │
└──────────────────────────────────────────────────────┘
```

**Resultado:** Altamente confiável. Autônomo para 90% dos casos.
**Precisão:** ~97%
**Custo por conversa:** R$ 0.08

### Era 6 → KODA v3.0: "O Agente Autônomo"

**Contexto:** Claude Opus 4.6. 1M tokens. Metacognition. Multi-agent nativo.

**Migração arquitetural:**
- Constitution design: regras imutáveis que governam todos os agentes
- Audit trail completo e imutável
- Self-improvement: KODA aprende com cada interação
- Human-in-the-loop apenas para exceções (não para supervisão)
- Memória cross-session: cliente volta depois de 1 semana, KODA lembra de tudo

**Arquitetura:**
```
┌──────────────────────────────────────────────────────────┐
│                     KODA v3.0                             │
│                                                           │
│                   ┌─────────────────┐                    │
│  CONSTITUTION ──→ │  Meta-Agente    │                    │
│  (regras imutáveis)│  (Opus 4.6)    │                    │
│                   └────────┬────────┘                    │
│                            │                              │
│         ┌──────────────────┼──────────────────┐          │
│         │                  │                  │           │
│    ┌────▼────┐       ┌────▼────┐       ┌─────▼─────┐    │
│    │  KODA   │       │  KODA   │       │  KODA     │    │
│    │ Vendas  │       │ Logíst. │       │ Financ.   │    │
│    └────┬────┘       └────┬────┘       └─────┬─────┘    │
│         │                  │                  │           │
│         └──────────────────┼──────────────────┘          │
│                            │                              │
│                   ┌────────▼────────┐                    │
│                   │   AUDIT TRAIL   │ ← Imutável         │
│                   └────────┬────────┘                    │
│                            │                              │
│                   ┌────────▼────────┐                    │
│                   │ HUMAN-IN-LOOP   │ ← Só exceções      │
│                   └────────┬────────┘                    │
│                            │                              │
│                        CLIENTE                            │
└──────────────────────────────────────────────────────────┘
```

**Resultado:** Near-autônomo. Intervenção humana em < 2% dos casos.
**Precisão:** ~99.2%
**Custo por conversa:** R$ 0.02

### Lições da Evolução do KODA

1. **Cada salto de modelo permite simplificar o harness:**
   - KODA v0.1: 2000 linhas de prompt engineering
   - KODA v3.0: 200 linhas de constitution

2. **Mas cada salto também demanda novas capacidades de engenharia:**
   - KODA v0.1: Saber escrever prompts
   - KODA v3.0: Saber desenhar constituições, audit trails, multi-agent governance

3. **O que nunca muda: a necessidade de engenharia de qualidade:**
   - Em 2018, o desafio era "como fazer o modelo gerar texto coerente"
   - Em 2026, o desafio é "como governar 50 agentes autônomos sem caos"
   - A complexidade não desaparece — ela migra de camada

### Métricas Reais de Evolução: KODA em Números

| Métrica | KODA v0.1 (Era 3) | KODA v1.0 (Era 4) | KODA v2.0 (Era 5) | KODA v3.0 (Era 6) |
|---|---|---|---|---|
| **Precisão de recomendação** | 65% | 87% | 97% | 99.2% |
| **Taxa de devolução** | 18% | 9% | 4% | 2.1% |
| **Tempo máx de conversa** | 30 min | 2 horas | 8 horas | 72 horas |
| **Custo por conversa** | R$ 1.50 | R$ 0.35 | R$ 0.08 | R$ 0.02 |
| **Latência por resposta** | 12s | 4s | 1.5s | 0.6s |
| **Cobertura autônoma** | 40% | 75% | 90% | 98% |
| **Intervenção humana** | 60% | 25% | 10% | 2% |
| **Linhas de código do harness** | 3,200 | 8,500 | 5,200 | 2,100 |
| **Complexidade do harness** | Baixa | Alta | Média | Média-Baixa |
| **NPS do cliente** | 32 | 58 | 74 | 87 |

**Observação importante:** Note que as linhas de código do harness sobem de v0.1 para v1.0 (quando você adiciona state management, validation, tool integration) e depois CAEM de v1.0 para v3.0 (quando o modelo assume responsabilidades que antes eram do código). Isso é o "harness paradox": um harness maduro para um modelo avançado tem MENOS código que um harness para um modelo intermediário.

### Visualização do Harness Paradox

```
Linhas de código do harness do KODA ao longo do tempo:

10K ┤
    │                    ┌────── Era 4
    │                    │      (Gen/Eval + Sprint Contracts + Rubrics + Trace)
  8K ┤                   ╱
    │                  ╱
  6K ┤                ╱
    │               ╱
  4K ┤         ┌───╱───── Era 3          ┌────── Era 5
    │         ╱   (State +               │      (Guardrails + Orchestration)
  2K ┤    ┌──╱    Validation)          ╱
    │   ╱                             ╱
    │  ╱ Era 2                      ╱────── Era 6
  0K └─┴──────────────────────────┴──────────────►
     2021  2022  2023  2024  2025  2026

O paradoxo: complexidade SOBE (2022→2024) e depois DESCE (2024→2026).
Isso NÃO significa que o harness ficou mais simples.
Significa que a complexidade migrou do código para a constituição.
```

### O Que Cada Versão do KODA Nos Ensinou

| Versão | Principal Lição | Citação do Time |
|---|---|---|
| **v0.1** | "Não adianta ter o melhor prompt do mundo se seu contexto é de 8K tokens." | "A gente passou 3 semanas tweaking prompts. A solução era trocar de modelo." |
| **v1.0** | "Generator/Evaluator dobra a precisão. Mas também dobra o custo. Vale cada centavo." | "75% → 98% de precisão. O CFO parou de reclamar do custo quando viu a taxa de devolução cair." |
| **v1.5** | "JSON mode não é luxo — é necessidade. Sem structured outputs, cada parse é uma roleta russa." | "Depois que migramos pra JSON mode, bugs de parsing caíram 95%. O time dorme melhor." |
| **v2.0** | "Multi-agent parece overengineering até você ter 100 conversas simultâneas. Aí é a única coisa que funciona." | "3 agentes especializados batem 1 agente generalista em qualquer métrica que você quiser medir." |
| **v2.5** | "O modelo melhorou. O harness ficou obsoleto em partes. Tivemos que REMOVER código." | "Deletar 3000 linhas de validação que o modelo agora faz sozinho foi a melhor sprint do ano." |
| **v3.0** | "Constitution não é documento — é código executável. Se não é testável, não é constitution." | "Toda regra da constituição tem um teste automatizado. Se o agente viola, o deploy é bloqueado." |

### O Dia em que o KODA Quebrou (E o que Aprendemos)

**12 de março de 2025, 14h32.** Um cliente chamado Roberto está conversando com KODA há 3 horas. Ele já:
- Pediu recomendações de 8 produtos diferentes
- Comparou preços entre 4 marcas
- Perguntou sobre 3 promoções
- Adicionou 5 itens ao carrinho
- Removeu 2 itens
- Mudou o endereço de entrega 2 vezes
- Aplicou 2 cupons de desconto

**14h35.** Roberto diz: "Fechou! Pode processar o pedido."

KODA processa. E... cobra o valor errado. Aplica apenas 1 cupom em vez de 2. O total está R$ 47 acima do esperado.

Roberto percebe. Fica furioso. Abandona o carrinho.

**O que aconteceu?**

O time de engenharia investigou o trace. Descobriu que:

1. **Às 14h15,** KODA fez uma chamada de API para validar o cupom #2. A API retornou timeout (3 segundos). KODA registrou: "cupom #2 válido" (errado — o timeout não foi tratado).

2. **Às 14h20,** o módulo de desconto processou o pedido com apenas 1 cupom. O contrato do sprint dizia: "aplicar TODOS os cupons válidos". Mas como o cupom #2 foi marcado como "válido" erroneamente, o módulo tentou aplicá-lo... e falhou silenciosamente.

3. **Às 14h32,** quando Roberto confirmou, o Evaluator checou: "todos os cupons aplicados?" Viu que SIM (porque o registro dizia que ambos eram válidos). Aprovou.

**Root cause:** O harness não tinha **timeout handling** nas chamadas de API. O modelo não podia saber que a API falhou — ele só via o resultado "válido" que o código registrou.

**A solução (implementada em 24h):**
- Adicionar timeout handling com retry (3 tentativas, exponential backoff)
- Se API falhar após retries, marcar como "UNVERIFIED" (não "válido")
- Evaluator agora verifica não só "está marcado como válido?" mas também "a verificação foi bem-sucedida?"
- Adicionar ao audit log: `api_call_result: SUCCESS | TIMEOUT | ERROR`

**Lição:** Conforme o harness fica mais complexo (Era 4-5), novos modos de falha emergem. A engenharia de harness não é "construir uma vez e pronto" — é **iteração contínua**. Cada nova capacidade do modelo expõe uma nova classe de bugs no harness.

---

## 📐 A Evolução do Código: Como o Harness Mudou

Nada ilustra melhor a evolução do que código real. Vamos ver como a mesma funcionalidade — "recomendar um produto" — foi implementada em cada era.

### Era 3 (2023): Prompt Engineering + Regras

```python
# KODA v0.1 - Recomendação de produto (Era 3)
# Modelo: GPT-4 (8K contexto)
# Sem function calling, sem state persistence robusta

def recomendar_produto_era3(historico_conversa, preferencias_cliente):
    catalogo_hardcoded = """
    PRODUTOS DISPONÍVEIS:
    1. Whey Gold Standard - R$ 120 - 4.5 estrelas - SEM lactose
    2. Whey Isolado Premium - R$ 180 - 4.8 estrelas - SEM lactose
    3. Whey Vegano 100% - R$ 95 - 4.3 estrelas - SEM lactose
    4. Creatina Monohidratada - R$ 65 - 4.6 estrelas - SEM lactose
    5. BCAA Premium - R$ 85 - 4.2 estrelas - COM lactose
    """
    
    prompt = f"""
    Você é KODA, assistente de vendas de suplementos.
    
    REGRAS:
    - Se cliente tem alergia, NUNCA recomende produto com alérgeno
    - Se cliente tem orçamento, respeite o limite
    - Recomende no máximo 3 produtos
    - Explique sua recomendação
    
    CATÁLOGO:
    {catalogo_hardcoded}
    
    HISTÓRICO DA CONVERSA:
    {historico_conversa[-3000:]}  # Trunca — só últimos ~3000 caracteres
    
    PREFERÊNCIAS DO CLIENTE:
    {preferencias_cliente}
    
    Recomende produtos para este cliente.
    """
    
    response = call_llm(prompt)
    
    # Validação manual (regex)
    if "COM lactose" in response and "alergia" in preferencias_cliente:
        return "ERRO: Recomendação contém produto com lactose para cliente alérgico!"
    
    return response

# Problemas deste código:
# 1. Catálogo hardcoded → se produto muda, precisa editar código
# 2. Histórico truncado → informações antigas se perdem
# 3. Validação frágil → regex não pega todos os casos
# 4. Sem tratamento de erro → se LLM falhar, função quebra
```

### Era 4 (2024): Generator/Evaluator + Tools

```python
# KODA v1.0 - Recomendação de produto (Era 4)
# Modelo: Claude 3.5 Sonnet (200K contexto)
# Function calling, JSON mode, state persistence

from typing import List, Dict
import json
from pathlib import Path

STATE_DIR = Path("./state")

def carregar_contexto_cliente(customer_id: str) -> Dict:
    """Carrega estado persistente do cliente de arquivo JSON."""
    state_file = STATE_DIR / f"{customer_id}" / "customer_context.json"
    return json.loads(state_file.read_text())

def salvar_draft_recomendacao(customer_id: str, draft: Dict) -> None:
    """Persiste draft do Generator para Evaluator ler."""
    draft_file = STATE_DIR / f"{customer_id}" / "generator_draft.json"
    draft_file.parent.mkdir(parents=True, exist_ok=True)
    draft_file.write_text(json.dumps(draft, indent=2, ensure_ascii=False))

def generator(customer_id: str) -> Dict:
    """Generator: cria recomendações usando function calling."""
    contexto = carregar_contexto_cliente(customer_id)
    
    tools = [
        {
            "name": "search_products",
            "description": "Busca produtos no catálogo em tempo real",
            "parameters": {
                "budget_max": contexto["budget_max"],
                "restrictions": contexto["restrictions"],
                "goal": contexto["goal"]
            }
        },
        {
            "name": "check_stock",
            "description": "Verifica estoque de um SKU específico",
            "parameters": {"sku": "string"}
        },
        {
            "name": "calculate_discount",
            "description": "Calcula preço com desconto de clube",
            "parameters": {"base_price": "number", "club_member": "boolean"}
        }
    ]
    
    response = call_llm_with_tools(
        system_prompt="Você é um recomendador. Gere opções e chame tools para verificar.",
        tools=tools,
        temperature=0.7
    )
    
    draft = {
        "generation_id": f"gen_{customer_id}_{timestamp()}",
        "recommendations": response.recommendations,
        "tools_called": response.tool_calls,
        "confidence": response.confidence
    }
    
    salvar_draft_recomendacao(customer_id, draft)
    return draft

def evaluator(customer_id: str) -> Dict:
    """Evaluator: verifica draft do Generator contra rubrica."""
    contexto = carregar_contexto_cliente(customer_id)
    draft = json.loads(
        (STATE_DIR / f"{customer_id}" / "generator_draft.json").read_text()
    )
    
    rubric = {
        "product_exists": "Verificar SKU no catálogo",
        "lactose_free": "Se cliente tem restrição, checar lactose",
        "in_stock": "Verificar estoque > 0",
        "price_ok": "Preço <= budget_max",
        "matches_goal": "Produto atende objetivo do cliente"
    }
    
    response = call_llm(
        system_prompt="Você é um avaliador CRÍTICO. Encontre erros.",
        messages=[{
            "role": "user",
            "content": f"""
            CONTEXTO DO CLIENTE: {json.dumps(contexto)}
            DRAFT DO GENERATOR: {json.dumps(draft)}
            RUBRIC: {json.dumps(rubric)}
            
            Avalie cada recomendação. Score 0-100. 
            Se score < 70, REJEITE com feedback específico.
            """
        }],
        temperature=0.2  # Rigoroso
    )
    
    verdict = {
        "verdict_id": f"eval_{customer_id}_{timestamp()}",
        "score": response.score,
        "approved": response.score >= 70,
        "issues": response.issues if response.score < 70 else [],
        "feedback": response.feedback if response.score < 70 else None
    }
    
    # Persiste verdict
    verdict_file = STATE_DIR / f"{customer_id}" / "evaluator_verdict.json"
    verdict_file.write_text(json.dumps(verdict, indent=2, ensure_ascii=False))
    
    return verdict

def recomendar_produto_era4(customer_id: str, max_retries: int = 3):
    """Pipeline completo Generator → Evaluator com retry."""
    for attempt in range(max_retries):
        draft = generator(customer_id)
        verdict = evaluator(customer_id)
        
        if verdict["approved"]:
            return draft["recommendations"]
        
        # Se rejeitado, o feedback é injetado na próxima iteração
        # O Generator lê o feedback do arquivo de estado
        if attempt == max_retries - 1:
            raise Exception(f"Falha após {max_retries} tentativas. "
                           f"Último feedback: {verdict['feedback']}")
    
    return None

# Melhorias sobre Era 3:
# ✅ Catálogo em tempo real (function calling, não hardcoded)
# ✅ Estado persistido em arquivos (auditável, recuperável)
# ✅ Generator/Evaluator com critérios explícitos
# ✅ Retry com feedback (auto-correção)
# ✅ JSON estruturado (contratos claros entre componentes)
```

### Era 5-6 (2025-2026): Constitution + Audit

```python
# KODA v3.0 - Recomendação de produto (Era 6)
# Modelo: Claude Opus 4.6 (1M contexto, agentic reasoning)
# Constitution design, multi-agent, audit trail imutável

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import hashlib

# ═══════════════════════════════════════════════════
# CONSTITUIÇÃO DO KODA (regras imutáveis)
# ═══════════════════════════════════════════════════

KODA_CONSTITUTION = """
## Constituição do Agente KODA

### Artigo 1: Segurança do Cliente (PRIORIDADE MÁXIMA)
1.1. NUNCA recomendar produto que viole restrição médica documentada do cliente.
1.2. Se houver dúvida sobre segurança de um produto, NÃO recomendar.
1.3. Alergias, intolerâncias e condições médicas têm precedência sobre preço e disponibilidade.

### Artigo 2: Transparência
2.1. Toda recomendação deve incluir justificativa clara.
2.2. Preços devem ser exatos (calculados em tempo real, não estimados).
2.3. Disponibilidade deve refletir estado real do inventário (não cache antigo).

### Artigo 3: Autonomia com Limites
3.1. Pedidos até R$ 500: processamento autônomo.
3.2. Pedidos entre R$ 500-2000: verificação adicional automática.
3.3. Pedidos acima de R$ 2000: escalar para humano.
3.4. Qualquer pedido com 3+ itens restritos: verificação adicional.

### Artigo 4: Auditabilidade
4.1. Toda ação do agente deve ser registrada em audit trail imutável.
4.2. Toda decisão deve ser rastreável até seus inputs.
4.3. Nenhuma ação pode ser realizada sem registro correspondente.

### Artigo 5: Aprendizado Contínuo
5.1. Após cada interação, registrar métricas de sucesso/fracasso.
5.2. Feedbacks negativos devem gerar análise de root cause em 24h.
5.3. Padrões de falha devem ser incorporados à constituição como novas regras.
"""

@dataclass
class AuditEntry:
    """Entrada imutável no audit trail."""
    timestamp: datetime
    agent_id: str
    action: str
    inputs_hash: str  # SHA256 dos inputs (privacidade)
    decision: str
    constitution_article: str  # Artigo relevante da constituição
    human_review: bool = False
    outcome: Optional[str] = None
    
    def to_jsonl(self) -> str:
        return json.dumps(self.__dict__, default=str)

class KodaAuditTrail:
    """Audit trail imutável (append-only JSONL)."""
    
    def __init__(self, customer_id: str):
        self.path = STATE_DIR / customer_id / "audit_trail.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
    
    def record(self, entry: AuditEntry) -> None:
        """Append-only: nunca modifica entradas existentes."""
        with open(self.path, 'a') as f:
            f.write(entry.to_jsonl() + '\n')
    
    def verify_integrity(self) -> bool:
        """Verifica que o audit trail não foi adulterado."""
        # Em produção, usaria blockchain ou hash chain
        entries = []
        with open(self.path) as f:
            for line in f:
                entries.append(json.loads(line))
        # Verifica timestamps monotônicos
        for i in range(1, len(entries)):
            if entries[i]["timestamp"] < entries[i-1]["timestamp"]:
                return False
        return True

class ConstitutoAgent:
    """Agente que opera dentro de uma constituição."""
    
    def __init__(self, constitution: str):
        self.constitution = constitution
        self.audit = None  # Setado por customer_id
    
    def recommend(self, customer_id: str, query: str) -> Dict:
        """Recomendação autônoma dentro das regras constitucionais."""
        self.audit = KodaAuditTrail(customer_id)
        
        # Passo 1: Registrar intenção
        self.audit.record(AuditEntry(
            timestamp=datetime.utcnow(),
            agent_id=f"koda-recommend-{customer_id}",
            action="recommendation_requested",
            inputs_hash=hashlib.sha256(query.encode()).hexdigest()[:16],
            decision="initiated",
            constitution_article="Art 2.1 (transparência)"
        ))
        
        # Passo 2: Delegar para meta-agente (que decide estratégia)
        meta_agent = MetaAgent(self.constitution)
        strategy = meta_agent.select_strategy(customer_id, query)
        
        self.audit.record(AuditEntry(
            timestamp=datetime.utcnow(),
            agent_id="meta-agent",
            action="strategy_selected",
            inputs_hash=strategy,
            decision=f"Estratégia: {strategy}",
            constitution_article="Art 3 (autonomia)"
        ))
        
        # Passo 3: Executar com a estratégia escolhida
        if strategy == "single_agent":
            result = self._run_single_agent(customer_id, query)
        elif strategy == "multi_agent":
            result = self._run_multi_agent(customer_id, query)
        elif strategy == "escalate_to_human":
            result = self._escalate(customer_id, query)
        
        # Passo 4: Verificar contra constituição
        violations = self._check_constitution(result, customer_id)
        
        if violations:
            self.audit.record(AuditEntry(
                timestamp=datetime.utcnow(),
                agent_id="constitution-checker",
                action="constitution_violation_detected",
                inputs_hash=hashlib.sha256(str(violations).encode()).hexdigest()[:16],
                decision="blocked",
                constitution_article=violations[0],
                human_review=True
            ))
            return {"error": "Recomendação bloqueada pela constituição", 
                    "violations": violations}
        
        # Passo 5: Registrar sucesso
        self.audit.record(AuditEntry(
            timestamp=datetime.utcnow(),
            agent_id="koda-recommend",
            action="recommendation_delivered",
            inputs_hash="completed",
            decision="approved",
            constitution_article="Art 2.1",
            outcome="success"
        ))
        
        return result
    
    def _check_constitution(self, result: Dict, customer_id: str) -> List[str]:
        """Verifica se o resultado viola algum artigo da constituição."""
        violations = []
        contexto = carregar_contexto_cliente(customer_id)
        
        # Art 1.1: Segurança do cliente
        if "restrictions" in contexto:
            for restriction in contexto["restrictions"]:
                for rec in result.get("recommendations", []):
                    if restriction in rec.get("contains", []):
                        violations.append(
                            f"Art 1.1: Produto {rec['name']} contém {restriction}. "
                            f"Cliente tem restrição documentada."
                        )
        
        # Art 3.3: Limite de autonomia
        total = sum(r.get("price", 0) for r in result.get("recommendations", []))
        if total > 2000:
            violations.append(
                f"Art 3.3: Total R$ {total} excede limite de autonomia (R$ 2000)."
            )
        
        return violations


# Uso:
# agent = ConstitutoAgent(KODA_CONSTITUTION)
# result = agent.recommend("wa_5511987654321", "Quero whey protein")
```

**Comparação entre as 3 implementações:**

| Aspecto | Era 3 (Prompt) | Era 4 (Gen/Eval) | Era 6 (Constitution) |
|---|---|---|---|
| **Linhas de código** | ~40 | ~150 | ~200 |
| **Catálogo** | Hardcoded | API (tools) | Descoberto pelo agente |
| **Validação** | Regex manual | Rubric (LLM) | Constituição (regras) |
| **Auditoria** | Nenhuma | Arquivos JSON | Audit trail imutável |
| **Retry** | Manual | Generator/Evaluator loop | Meta-agente decide |
| **Segurança** | Frágil (regex) | Robusta (rubric) | Constitucional (multi-camada) |
| **Manutenção** | Editar código | Editar código | Editar constituição |
| **Escala** | 1 conversa | 100 conversas | 10,000 conversas |

---

## 🧠 O Lado Humano: Como os Engenheiros Evoluíram

Não são só os modelos que evoluíram. Os **engenheiros** também. As habilidades necessárias para construir agentes mudaram radicalmente:

### Perfil do Engenheiro de Agentes por Era

| Era | Nome do Perfil | Habilidades Principais | Ferramentas | "Hello World" |
|---|---|---|---|---|
| **Era 1-2** | Prompt Engineer | Criatividade textual. Intuição sobre linguagem. Tentativa e erro. | Playground da OpenAI | "Complete this sentence: The best way to..." |
| **Era 3** | AI Integrator | Prompt engineering + backend básico. API integration. Tratamento de erros. | Python + OpenAI SDK | "System: You are a helpful assistant..." |
| **Era 4** | Agent Architect | Design de padrões (Gen/Eval, Contracts). Tool integration. State management. Debugging de traces. | Python + Claude SDK + JSON Schema + Pydantic | Sistema Generator/Evaluator funcional |
| **Era 5** | Multi-Agent Orchestrator | Coordenação de agentes. Guardrails. Paralelismo. Otimização de custo/latência. | Python + Async + Queue systems + Monitoring | 3 agentes coordenados resolvendo tarefa |
| **Era 6** | AI Governor | Constitution design. Audit systems. Ética de IA. Governança. Métricas de qualidade em escala. | Python + Constitution DSL + Blockchain audit + Dashboards | Constituição + meta-agente + audit trail |

### A Curva de Aprendizado

```
Complexidade
do conhecimento
necessário
      ▲
      │                                        ┌───── Era 6
      │                                   ┌────┘     (Governance)
      │                              ┌────┘
      │                         ┌────┘ Era 5 (Orchestration)
      │                    ┌────┘
      │               ┌────┘ Era 4 (Architecture)
      │          ┌────┘
      │     ┌────┘ Era 3 (Integration)
      │┌────┘
      ││ Era 1-2 (Prompt)
      └┴─────────────────────────────────────────────► Tempo
      2018    2020    2022    2024    2026    2028

Cada era REQUER o conhecimento das eras anteriores + novas habilidades.
Você não pode pular de Era 2 para Era 6 sem passar pelas intermediárias.
```

### O que Isso Significa Para Seu Time Hoje (2026)

Se você está montando um time de agentes em 2026:

1. **Contrate para Era 6, treine para Era 4:**
   - Contrate pessoas com mentalidade de governança (Era 6)
   - Mas elas precisam entender os fundamentos (Era 4) para debugar quando algo falha
   - Ninguém consegue desenhar uma constituição sem entender Generator/Evaluator

2. **A habilidade mais valiosa em 2026: Debugging de agentes autônomos**
   - Quando 50 agentes estão operando simultaneamente e algo dá errado, COMO você encontra o problema?
   - Audit trail, trace reading, e análise de root cause são as habilidades premium

3. **Prompt engineering não morreu — se transformou**
   - Você não escreve mais prompts de 2000 linhas
   - Mas você escreve constituições, que são "meta-prompts" que governam múltiplos agentes
   - A habilidade de "falar com LLMs" evoluiu de tática para estratégica

---

## 📖 Padrões de Harness por Era: Um Guia de Referência

Esta seção é um **guia prático**: para cada era, qual padrão de harness usar e por quê.

### Era 1-2 (2018-2021): Prompt Engineering Patterns

```
Padrões relevantes:
  ✗ Nenhum padrão formal de harness existe ainda
  ✓ Few-shot prompting: incluir exemplos no prompt
  ✓ Persona prompting: definir tom e comportamento
  ✓ Output formatting: pedir formato específico (JSON, markdown)
  ✓ Chain-of-thought básico: "pense passo a passo"

Quando usar:
  Se você está preso em um modelo antigo (por legacy ou custo),
  estes padrões são seu único recurso.

Não use para:
  Qualquer coisa que precise de contexto > 2048 tokens
  Qualquer coisa que precise de tool use
  Qualquer coisa que precise de confiabilidade > 80%
```

### Era 3 (2022-2023): State Management Patterns

```
Padrões relevantes:
  ✓ State Persistence (Nível 1)
  ✓ History Compression (Nível 1)
  ✓ Validation Layers (Nível 1)
  ✓ Basic Harness Patterns (Nível 1)

Quando usar:
  Modelos com 4K-100K contexto, sem function calling nativo.
  Você precisa gerenciar estado manualmente porque o modelo
  não tem tools para auto-gerenciar.

Arquitetura recomendada:
  System Prompt (persona) + Context (histórico comprimido) +
  State Files (JSON externo) + Validation (regex/heurísticas)
```

### Era 4 (2023-2024): Generator/Evaluator + Contracts

```
Padrões relevantes:
  ✓ Generator/Evaluator (Nível 2)
  ✓ Sprint Contracts (Nível 2)
  ✓ Rubric Design (Nível 2)
  ✓ Trace Reading (Nível 2)
  ✓ Tool Integration patterns

Quando usar:
  Modelos com function calling, JSON mode, 128K-1M contexto.
  Este é o sweet spot para os padrões de Nível 2.

Arquitetura recomendada:
  Generator (LLM 1) → Tools (APIs) → Evaluator (LLM 2) →
  Sprint Contracts (validação) → Rubric (score) → Response
```

### Era 5 (2024-2025): Guardrails + Orchestration

```
Padrões relevantes:
  ✓ Multi-Agent Coordination (Nível 3)
  ✓ Guardrails & Safety Layers (Nível 3)
  ✓ Autonomous Planning (Nível 3)
  ✓ Harness Evolution (Nível 3)

Quando usar:
  Modelos agent-native. O modelo já sabe "ser agente".
  Seu trabalho é coordenar múltiplos agentes e definir limites.

Arquitetura recomendada:
  Orchestrator → [Agent 1, Agent 2, Agent N] (paralelo) →
  Guardrails (constraints) → Aggregator → Response
```

### Era 6 (2025-2026+): Constitution + Audit

```
Padrões relevantes:
  ✓ Constitution Design (Nível 4)
  ✓ Audit Trail Architecture (Nível 4)
  ✓ Human-in-the-Loop Patterns (Nível 4)
  ✓ Continuous Improvement Loops (Nível 4)

Quando usar:
  Modelos com 1M+ contexto, metacognition, multi-agent nativo.
  O agente é quase totalmente autônomo. Você define a constituição
  e audita os resultados.

Arquitetura recomendada:
  Constitution (regras imutáveis) → Meta-Agent (orquestrador) →
  Specialized Agents (spawned) → Audit Trail (imutável) →
  Human-in-Loop (exceções apenas)
```

---

## 🧭 Mapa de Decisão: Qual Padrão Usar em Qual Contexto?

```
                    "Que padrão de harness devo usar?"
                                  │
                    ┌─────────────┴─────────────┐
                    │ Qual é o contexto máximo  │
                    │ do seu modelo?            │
                    └─────────────┬─────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
     < 4K tokens            4K-128K tokens           > 128K tokens
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────────┐        ┌──────────────┐
    │ Era 1-2  │           │  Tem tool     │        │  Tem agent-  │
    │ padrões  │           │  use nativo?  │        │  native?     │
    └──────────┘           └──────┬───────┘        └──────┬───────┘
                                  │                       │
                          ┌───────┴───────┐       ┌───────┴───────┐
                          │ SIM   │ NÃO   │       │ SIM   │ NÃO   │
                          ▼       ▼        │       ▼       ▼        │
                    ┌─────────┐ ┌───────┐  │  ┌─────────┐ ┌───────┐ │
                    │ Nível 2 │ │Nível 1│  │  │ Nível 4 │ │Nível 3│ │
                    │Gen/Eval │ │State  │  │  │Const+A. │ │Multi- │ │
                    │Contract │ │Persist│  │  │         │ │Agent  │ │
                    └─────────┘ └───────┘  │  └─────────┘ └───────┘ │
                                           │                       │
                                     ┌─────┴─────┐          ┌─────┴─────┐
                                     │ Contexto  │          │ Contexto  │
                                     │ > 200K?   │          │ > 1M?     │
                                     └─────┬─────┘          └─────┬─────┘
                                           │                      │
                                     ┌─────┴─────┐          ┌─────┴─────┐
                                     │SIM │ NÃO  │          │SIM │ NÃO  │
                                     ▼     ▼      │          ▼     ▼     │
                                   ┌───┐ ┌─────┐ │        ┌───┐ ┌─────┐ │
                                   │L2 │ │L1+L2│ │        │L4 │ │L3+L4│ │
                                   │   │ │híbrido│        │   │ │híbrido│
                                   └───┘ └─────┘ │        └───┘ └─────┘ │
                                                 │                       │
                                                 └───────────────────────┘
```

---

## 🎓 O Que Você Aprendeu

### 1. A Evolução dos Modelos Não é Linear — É em Saltos Quânticos

Cada era (Foundation, Scale, Alignment, Multimodal, Agent-Native, Post-Agent) não é "um pouco melhor que a anterior". É uma **mudança de paradigma** que redefine o que é possível. Um engenheiro em 2020 dizendo "agentes autônomos são impossíveis" estava certo — para os modelos de 2020. Mas as regras mudaram. E continuam mudando.

### 2. Cada Nova Capacidade Não Elimina Engenharia — Redireciona

Contexto maior? Você não precisa mais de state persistence manual. Mas agora precisa de constitution design. Tool use nativo? Você não precisa mais de prompt engineering para simular API calls. Mas agora precisa de guardrails para garantir que as tools são usadas corretamente.

**A engenharia de harness nunca desaparece. Ela muda de forma.**

### 3. O Harness Evolui Junto com o Modelo

```
Modelo simples → Harness complexo (você compensa limitações)
Modelo avançado → Harness simples (modelo resolve o básico)
                  mas Harness SOFISTICADO (você governa autonomia)
```

O harness da Era 6 não é "mais simples" que o da Era 3. Ele é **diferente**. Na Era 3, você gastava energia ensinando o modelo a "não alucinar". Na Era 6, você gasta energia desenhando uma constituição que governa 50 agentes autônomos. A complexidade não some — ela sobe de nível.

### 4. Context Window é o Teto — Mas Não É a Única Variável

Sim, contexto maior é o maior unlock para long-running agents. Mas não adianta ter 1M tokens de contexto se o modelo:
- Não segue instruções (sem RLHF)
- Não interage com sistemas externos (sem tool use)
- Não raciocina sobre múltiplos passos (sem reasoning)
- Não emite outputs estruturados (sem JSON mode)

Todas as capacidades evoluem juntas. Um bom engenheiro de agentes conhece o **perfil completo** de capacidades do modelo que está usando.

### 5. O Futuro é Agentes que Constroem Agentes

Na Era 6 (2026+), a pergunta deixa de ser "como construo um agente?" e passa a ser "quais são as regras que governam meus agentes?". O código se torna constituição. A engenharia se torna governança. O harness se torna audit trail.

E você, que leu este documento, está preparado para essa transição.

---

## 🔗 Próximos Passos

Este documento é uma referência. Use-o quando precisar:

- **Contextualizar uma decisão de arquitetura:** "Dado que estamos usando Claude Opus 4.6 (Era 6), nosso harness deve focar em constitution e audit, não em state management manual."
- **Planejar migração de modelo:** "Vamos migrar de GPT-4 (Era 4) para Claude 4 (Era 5). Precisamos adicionar multi-agent coordination e simplificar validation layers."
- **Educar novos membros do time:** "Leia a timeline de modelos para entender por que nossa arquitetura é como é."

### Documentos Relacionados

- `01-why-agents-lose-plot.md` — Os 3 problemas fundamentais (Nível 1)
- `01-generator-evaluator-pattern.md` — Padrão principal da Era 4 (Nível 2)
- `03-multi-agent-systems.md` — Coordenação multi-agente (Nível 3)
- `01-koda-architecture.md` — Arquitetura atual do KODA (Nível 4)
- `05-harness-evolution.md` — Como evoluir o harness ao longo do tempo (Nível 3)

---

## 🧰 Guia Prático: Escolhendo o Modelo Certo para Seu Agente (2026)

Com tantos modelos disponíveis, como escolher? Este guia prático mapeia modelos às suas melhores aplicações.

### Modelos Frontier (Era 6)

| Modelo | Contexto | Força Principal | Melhor Para | Custo (por 1M tokens) |
|---|---|---|---|---|
| **Claude Opus 4.6** | 1M | Metacognition. Agentic reasoning superior. Multi-agent nativo. | Agentes complexos. Coordenação multi-agent. Tarefas críticas. | $$$ (alto) |
| **Claude Sonnet 4.6** | 200K | Melhor custo-benefício. Rápido. Tool use otimizado. | 90% das tarefas de agente. Recomendações. Validações. | $$ (médio) |
| **Claude Haiku 4.6** | 200K | Muito barato. Muito rápido. Suficiente para tarefas simples. | Tarefas simples (confirmação, formatação). Alto volume. | $ (baixo) |
| **Gemini 3.0** | 2M | Contexto massivo. Integração Google ecosystem. | Memória de longo prazo. Search integrado. Documentos longos. | $$ (médio) |
| **DeepSeek-V4** | 128K | Open-source. Excelente reasoning. Custo zero (self-hosted). | Tarefas especializadas com fine-tuning. Privacy-critical. | $ (self-hosted) |

### Estratégia de Uso (Padrão KODA 2026)

```
Distribuição de chamadas por modelo no KODA v3.0:

Haiku 4.6 ──────────────────────── 65% das chamadas
  ▸ Confirmações ("seu pedido foi recebido")
  ▸ Formatação de texto
  ▸ Validações simples (preço > 0?)
  ▸ Custo: ~R$ 0.001 por chamada

Sonnet 4.6 ──────────── 25% das chamadas
  ▸ Recomendações de produto
  ▸ Avaliação de qualidade (Evaluator)
  ▸ Processamento de pedidos simples
  ▸ Custo: ~R$ 0.01 por chamada

Opus 4.6 ──── 8% das chamadas
  ▸ Pedidos complexos (múltiplos itens, restrições)
  ▸ Coordenação multi-agent (orquestração)
  ▸ Decisões de alto valor (pedidos > R$ 500)
  ▸ Custo: ~R$ 0.05 por chamada

Falha/Escala ── 2% das chamadas
  ▸ Se nenhum modelo conseguiu resolver
  ▸ Escala para humano
  ▸ Registra para fine-tuning futuro
```

**Economia com esta estratégia:** R$ 0.008 por chamada em média (vs R$ 0.05 se usasse Opus para tudo). Para 1 milhão de chamadas/mês: economia de R$ 42.000/mês.

### Modelos por Era: Compatibilidade com Padrões de Harness

| Se você está usando... | Você está na... | Padrões de harness recomendados | Padrões que NÃO funcionam bem |
|---|---|---|---|
| **GPT-4 (8K)** | Era 3-4 | State Persistence. History Compression. Validation Layers. | Multi-Agent (sem tool use nativo). Constitution (contexto pequeno). |
| **GPT-4 Turbo / Claude 3** | Era 4 | Generator/Evaluator. Sprint Contracts. Tool Integration. | Multi-agent autônomo. Metacognition-based patterns. |
| **Claude 3.5 / GPT-4o** | Era 4-5 | Todos os de Nível 2 + início de Multi-Agent. Guardrails básicos. | Constitution governance (modelo não tem metacognition suficiente). |
| **Claude 4 / GPT-5** | Era 5 | Multi-Agent Orchestration. Guardrails. Parallel execution. | Constitution ainda é prematuro (mas pode começar a prototipar). |
| **Opus 4.6 / Gemini 3.0** | Era 6 | Constitution Governance. Audit Trails. Meta-Agent patterns. | Padrões de Era 3-4 como primários (usar modelos de Era 6 com padrões de Era 4 é desperdício de capacidade). |

---

## 🔭 Além de 2030: Especulações Informadas

O que vem depois de agentes serem infraestrutura invisível?

### Cenário A: "The Great Consolidation" (Provável)
- 2-3 provedores de "agent runtime" dominam o mercado (como AWS/Azure/GCP para cloud)
- Você não escolhe um modelo — você escolhe um runtime que automaticamente seleciona o melhor modelo para cada tarefa
- O "harness" é um serviço gerenciado, não código que você escreve
- Engenheiros de agente se tornam "agent operators" (como SREs para cloud)

### Cenário B: "The Agent Explosion" (Possível)
- Milhares de agentes especializados por domínio
- Marketplaces de agentes (como app stores)
- "Agent composability": você combina agentes como combina microserviços
- O desafio deixa de ser "construir um agente" e passa a ser "orquestrar 500 agentes de terceiros"

### Cenário C: "The Symbiosis" (Desejável)
- Agentes e humanos trabalham em parceria real
- Cada humano tem um "agent twin" que aprende seus padrões, preferências, estilo
- O agent twin participa de reuniões, escreve código, responde emails no estilo do humano
- A linha entre "o que eu fiz" e "o que meu agente fez" se torna indistinguível

### O Que Permanece Constante em Todos os Cenários

Independentemente de qual cenário se materialize:

1. **Alguém precisa definir as regras.** Sejam constituições, guardrails, ou políticas — agentes autônomos precisam de limites. Esse "alguém" é o engenheiro de agentes.

2. **Alguém precisa auditar.** Quando algo der errado (e vai dar), alguém precisa rastrear o que aconteceu. Audit trails não são opcionais — são a única defesa contra o caos.

3. **Alguém precisa decidir quando escalar.** Agentes vão falhar. A decisão de "quando parar de tentar e chamar um humano" é crítica e não pode ser deixada para o próprio agente.

4. **Alguém precisa medir.** Sem métricas, você não sabe se seus agentes estão melhorando ou piorando. KPIs de qualidade, custo, latência, e satisfação são permanentes.

**Estas 4 responsabilidades — definir regras, auditar, escalar, medir — são o coração da engenharia de agentes em qualquer era.**

---

## 📊 Quick Reference: Catálogo de Modelos (2018-2026)

Uma tabela compacta para consulta rápida de todos os modelos mencionados neste documento.

| Ano | Modelo | Parâmetros | Contexto | Tool Use | Multimodal | Reasoning | Era | Open-Source? |
|---|---|---|---|---|---|---|---|---|
| 2018 | GPT-1 | 117M | 512 | Não | Não | Não | 1 | Não |
| 2018 | BERT | 340M | 512 | Não | Não | Não | 1 | Sim |
| 2019 | GPT-2 | 1.5B | 1024 | Não | Não | Não | 1 | Não |
| 2019 | T5 | 11B | 512 | Não | Não | Não | 1 | Sim |
| 2020 | GPT-3 | 175B | 2048 | Não | Não | Few-shot | 2 | Não |
| 2021 | Codex | 12B | 2048 | Não | Não | Few-shot | 2 | Não |
| 2021 | Gopher | 280B | 2048 | Não | Não | Few-shot | 2 | Não |
| 2022 | InstructGPT | 175B | 2048 | Não | Não | Básico | 3 | Não |
| 2022 | ChatGPT | ~175B | 4096 | Não | Não | Básico | 3 | Não |
| 2023 | GPT-4 | ~1.8T | 8K-32K | Básico | Imagem | Avançado | 3 | Não |
| 2023 | Claude 1 | — | 9K | Não | Não | Bom | 3 | Não |
| 2023 | Claude 2 | — | 100K | Não | Não | Bom | 3 | Não |
| 2023 | Llama 2 | 7B-70B | 4K | Não | Não | Básico | 3 | Sim |
| 2023 | PaLM 2 | — | 8K | Não | Não | Bom | 3 | Não |
| 2024 | GPT-4 Turbo | — | 128K | Nativo | Imagem | Excelente | 4 | Não |
| 2024 | Claude 3 Opus | — | 200K | Nativo | Imagem | Excelente | 4 | Não |
| 2024 | Claude 3 Sonnet | — | 200K | Nativo | Imagem | Excelente | 4 | Não |
| 2024 | Claude 3 Haiku | — | 200K | Nativo | Imagem | Bom | 4 | Não |
| 2024 | Gemini 1.5 | — | 1M | Nativo | Completo | Excelente | 4 | Não |
| 2024 | Llama 3 | 8B-70B | 8K | Básico | Não | Bom | 4 | Sim |
| 2024 | GPT-4o | — | 128K | Nativo | Omni | Excelente | 4 | Não |
| 2024 | Claude 3.5 Sonnet | — | 200K | Nativo | Imagem | Excelente | 4 | Não |
| 2025 | Claude 4 Sonnet | — | 200K | Nativo | Imagem | Super | 5 | Não |
| 2025 | GPT-5 | — | 256K | Nativo | Completo | Super | 5 | Não |
| 2025 | Gemini 2.0 | — | 2M | Nativo | Completo | Super | 5 | Não |
| 2025 | DeepSeek-R1 | — | 128K | Básico | Não | Super | 5 | Sim |
| 2026 | Claude Opus 4.6 | — | 1M | Nativo | Completo | Meta | 6 | Não |
| 2026 | Claude Sonnet 4.6 | — | 200K | Nativo | Completo | Excelente | 6 | Não |
| 2026 | Gemini 3.0 | — | 2M | Nativo | Completo | Meta | 6 | Não |
| 2026 | DeepSeek-V4 | — | 128K | Nativo | Básico | Super | 6 | Sim |

**Notas:**
- "—" em Parâmetros: muitos modelos modernos não divulgam contagem de parâmetros
- "Omni" em Multimodal: input e output em múltiplas modalidades
- "Meta" em Reasoning: metacognition — o modelo sabe o que não sabe
- As datas refletem disponibilidade em API pública, não anúncio

### O Que Esta Tabela Mostra

1. **A explosão de contexto:** De 512 tokens (2018) para 2M tokens (2026) — um aumento de 4000x.
2. **A democratização do tool use:** Em 2022, nenhum modelo tinha tool use. Em 2026, é padrão até em modelos open-source.
3. **A convergência multimodal:** Em 2023, só GPT-4 era multimodal. Em 2026, é ubíquo.
4. **A ascensão open-source:** Llama 2 (2023) → Llama 3 (2024) → DeepSeek-R1 (2025) → DeepSeek-V4 (2026). A diferença entre frontier e open-source está diminuindo.
5. **O desaparecimento da contagem de parâmetros:** De 2018-2021, parâmetros eram a métrica principal. De 2023 em diante, as empresas pararam de divulgar porque parâmetros não são mais o principal indicador de capacidade (training data quality, arquitetura, e fine-tuning importam mais).

---

## ❓ Perguntas Frequentes

### P: "Por que 2018 e não antes? Já existiam redes neurais antes disso."
**R:** 2018 marca o surgimento da arquitetura Transformer (GPT-1, BERT), que é a base de TODOS os LLMs modernos. Redes neurais anteriores (LSTM, GRU) não são LLMs como entendemos hoje e têm capacidades fundamentalmente diferentes (contexto fixo de ~50 tokens, sem attention mechanism eficiente).

### P: "O GPT-5 não foi lançado em 2024?"
**R:** O GPT-4o foi lançado em 2024. As datas nesta timeline são baseadas em quando as capacidades se tornaram disponíveis para uso em produção (API pública), não em anúncios. O GPT-5 efetivamente chegou em 2025 com agentic workflows nativos.

### P: "Por que o Claude aparece tanto e outros modelos menos?"
**R:** Esta timeline é contada da perspectiva do KODA, que usa majoritariamente modelos Anthropic (Claude). Isso não significa que outros modelos não sejam importantes — significa que nossa experiência prática é centrada em Claude. Os princípios arquiteturais se aplicam a qualquer modelo.

### P: "1M tokens de contexto realmente funciona? Ou é marketing?"
**R:** Funciona, mas com nuance. Em 1M tokens, o modelo consegue "ver" tudo, mas a qualidade da atenção não é uniforme — tokens no meio do contexto tendem a receber menos atenção que tokens no início e no fim (lost-in-the-middle problem). O harness ainda precisa garantir que informações críticas estejam posicionadas estrategicamente.

### P: "Se o custo marginal tende a zero, por que se preocupar com otimização?"
**R:** Custo marginal por token tende a zero. Mas o custo total de um agente 24/7 com milhões de clientes ainda é relevante. E mais importante: latência. Modelos mais baratos tendem a ser mais rápidos (menos parâmetros). Para experiência do cliente, latência de 500ms vs 5s é a diferença entre "conversa natural" e "estou esperando o robô pensar".

### P: "Qual foi o maior salto de capacidade? Context window ou tool use?"
**R:** Tool use, sem dúvida. Context window permite que o agente "lembre" de mais coisas. Tool use permite que o agente "aja" no mundo. Um agente com contexto infinito mas sem tools ainda é um oráculo — ele pode saber tudo mas não pode fazer nada. Um agente com tools mas contexto limitado pode realizar ações reais (consultar APIs, modificar dados), o que o torna transacional. Dito isso, o ideal são ambos: contexto longo + tool use é a combinação que viabilizou agentes de produção.

### P: "Como você sabe que estamos na Era 6 e não ainda na Era 5?"
**R:** As eras se sobrepõem — não há uma linha clara. O que define a Era 6 é: (1) modelos com metacognition (sabem o que não sabem), (2) agentes que spawnam outros agentes autonomamente, (3) constitution governance como padrão, não exceção. Se seu time ainda está fazendo prompt engineering pesado ou state management manual, você está operando com práticas de Era 4, mesmo usando modelos de Era 6. A era é definida pelo seu harness, não pelo modelo.

### P: "Devo migrar meu agente para o modelo mais novo sempre que um sai?"
**R:** Não necessariamente. Modelos mais novos são melhores em quase tudo, mas considere: (1) **Custo de migração:** Seu harness pode depender de comportamentos específicos do modelo atual (ex: formato de function calling, viés de resposta). Migrar requer re-validação completa. (2) **Estabilidade:** Modelos novos podem ter regressões em comportamentos que seu harness depende. (3) **ROI:** A melhoria de performance justifica o custo de migração? Para KODA, migrar de Claude 3.5 para Claude 4 deu +10% de precisão. Migrar de Claude 4 para Opus 4.6 deu +2%. A primeira migração valeu muito; a segunda, menos. Regra: migre quando o ganho esperado > 5% de melhoria em métrica crítica.

### P: "E os modelos open-source (Llama, Mistral, DeepSeek)? Onde eles se encaixam?"
**R:** Modelos open-source tipicamente estão 6-18 meses atrás dos modelos frontier em capacidades agenticas. Llama 3 (2024) tem capacidades de Era 4. DeepSeek-R1 (2025) compete em reasoning mas não em tool use nativo ou multi-modal. Para agentes de produção, modelos open-source são excelentes para: (1) tarefas especializadas onde você pode fazer fine-tuning, (2) reduzir custo em 90%+ das chamadas (usar Llama para tarefas simples, Claude para complexas), (3) manter controle sobre o modelo (privacy, compliance). Padrão comum em 2026: Haiku/Flash para 80% das chamadas, Opus para 15%, open-source fine-tuned para 5% de tarefas específicas.

### P: "O que significa 'metacognition' na prática?"
**R:** Metacognition é a capacidade do modelo de "saber o que não sabe". Exemplo prático: um modelo sem metacognition, quando perguntado "este produto contém lactose?", vai responder "Sim" ou "Não" baseado no que ele "lembra" — e pode estar errado. Um modelo com metacognition vai responder: "Não tenho certeza. Deixe-me verificar na base de dados de nutrição." E então chama uma tool para verificar. Isso reduz dramaticamente alucinações porque o modelo não tenta "adivinhar" — ele reconhece os limites do seu conhecimento e busca informação externa.

### P: "Se agentes se tornam autônomos na Era 6, qual é o papel do engenheiro?"
**R:** O engenheiro migra de "construtor" para "governador". Em vez de escrever código que diz COMO o agente deve processar um pedido, o engenheiro escreve: (1) a constituição (o que o agente NUNCA pode fazer), (2) os sistemas de auditoria (como verificar se o agente está operando corretamente), (3) os dashboards de monitoramento (visibilidade em tempo real da operação de centenas de agentes), (4) os critérios de escalação (quando um humano deve intervir). É uma mudança de "programar comportamento" para "programar governança".

### P: "Qual a maior lição que você tirou desses 8 anos de evolução?"
**R:** Que **o teto de hoje é o chão de amanhã.** Em 2018, 512 tokens era o teto. Em 2020, 2048 tokens era o teto. Em 2026, 1M tokens é o padrão. Toda vez que alguém diz "X é impossível para LLMs", o que essa pessoa está realmente dizendo é "X é impossível com os modelos de hoje". A história mostra que esses "impossíveis" caem um por um. Como engenheiro de agentes, sua job não é otimizar para os limites de hoje — é construir harnesses que estão prontos para os modelos de amanhã. Porque quando o próximo salto quântico vier, a diferença entre você e seus concorrentes não será o modelo (todo mundo terá acesso ao mesmo modelo). Será a qualidade do seu harness.

---

## 🚀 Checkpoint: Você Aprendeu?

Antes de seguir, verifique:

- [ ] Consigo listar as 6 eras e o principal avanço de cada uma
- [ ] Entendo por que agentes eram impossíveis antes de 2022
- [ ] Sei explicar como tool use mudou o design de agentes
- [ ] Consigo mapear qual padrão de harness usar para cada era
- [ ] Entendo que o harness evolui junto com o modelo — não desaparece
- [ ] Consigo olhar para um modelo (ex: GPT-4o) e deduzir quais padrões de harness são apropriados
- [ ] Entendo a diferença entre "construir um agente" (Era 1-5) e "governar agentes" (Era 6)

Se respondeu "não" para qualquer uma:
- Releia a seção correspondente
- Use a tabela comparativa de eras como referência rápida
- Pense em um modelo que você usa e tente classificá-lo em uma era

---

## 📚 Referências & Leitura Adicional

### Dentro deste Programa
- `GLOSSARY.md` — Definição de termos técnicos (context window, RLHF, chain-of-thought)
- `MASTER_PLAN.md` — Visão geral do programa e como as eras se conectam aos níveis
- `01-nivel-1-fundamentals/` — Padrões básicos de harness
- `02-nivel-2-practical-patterns/` — Padrões práticos
- `03-nivel-3-advanced-architecture/` — Arquitetura avançada
- `04-nivel-4-koda-specific/` — Aplicação específica no KODA

### Externo
- **"Scaling Laws for Neural Language Models"** (Kaplan et al., 2020) — O paper que mostrou que performance escala com tamanho
- **"Training Language Models to Follow Instructions"** (OpenAI, 2022) — O paper do InstructGPT/RLHF
- **"Chain-of-Thought Prompting Elicits Reasoning"** (Wei et al., 2022) — O paper que introduziu chain-of-thought
- **"GPT-4 Technical Report"** (OpenAI, 2023) — Detalhes sobre GPT-4
- **"The Claude Model Family"** (Anthropic, 2024-2026) — Documentação dos modelos Claude
- **"Constitutional AI"** (Anthropic, 2023) — O paper sobre AI com constituição interna

---

## 📜 Os 11 Princípios: Consolidação

Ao longo deste documento, 11 princípios emergiram. Aqui estão todos reunidos para referência:

| # | Princípio | Era de Origem | Essência |
|---|---|---|---|
| **1** | O Teto do Modelo é o Teto do Agente | Era 1 | Contexto de 512 tokens = agente com "memória" de 512 tokens. Não importa o harness. |
| **2** | Scaling Laws Permitem Planejar o Futuro | Era 2 | Se performance escala previsivelmente, você pode projetar para modelos que ainda não existem. |
| **3** | In-Context Learning é Re-treinamento Instantâneo | Era 2 | Cada prompt é uma oportunidade de ensinar o modelo sem fine-tuning. |
| **4** | Context Window é Memória, Não Inteligência | Era 3 | Modelo "lembrar" de mais coisas não significa que ele sabe o que é importante lembrar. |
| **5** | Alinhamento ≠ Confiabilidade | Era 3 | RLHF faz o modelo seguir instruções, mas não garante acerto. Bias de confirmação persiste. |
| **6** | Tool Use é o Divisor de Águas | Era 4 | Sem tools: oráculo. Com tools: executor. É a diferença entre "saber" e "fazer". |
| **7** | Structured Outputs São Contratos | Era 4 | JSON mode não é conveniência — é contrato de comunicação entre componentes. |
| **8** | Agência vs. Controle | Era 5 | Quanto mais agent-native o modelo, menos controle procedural e mais guardrails você precisa. |
| **9** | O Harness Migra de "Como" para "O Que Não" | Era 5 | Modelo sabe COMO fazer. Harness define O QUE NÃO FAZER. |
| **10** | A Constituição é o Novo Código | Era 6 | Regras imutáveis substituem código procedural. Engenharia vira governança. |
| **11** | O Paradoxo da Autonomia | Era 6 | Quanto mais autônomo o agente, mais crítico é o design das constraints. |

### Como Usar Estes Princípios

- **Ao avaliar um novo modelo:** Percorra a lista. Quais princípios se aplicam? Quais capacidades o modelo tem que desbloqueiam novos padrões?
- **Ao debugar um agente:** Identifique qual princípio está sendo violado. Ex: agente esquece informações críticas → Princípio 4 (contexto ≠ inteligência). A solução não é "mais contexto" — é "posicionar informação estrategicamente".
- **Ao planejar evolução do harness:** Use os princípios como checklist. "Já que vamos migrar para um modelo com tool use nativo (Princípio 6), precisamos adicionar structured outputs (Princípio 7) e começar a pensar em guardrails (Princípio 9)."

---

## 🧬 A Conexão com o Harness: Como Este Documento se Relaciona com os Níveis

Este documento não existe isolado. Ele é a **fundação histórica e teórica** que justifica todos os padrões ensinados no programa:

```
MODEL CAPABILITY TIMELINE (este documento)
  │
  ├─→ NÍVEL 1 (Fundamentos)
  │     Os 3 problemas (amnesia, planning collapse, self-eval)
  │     são CONSEQUÊNCIAS DIRETAS das limitações de Era 3.
  │     As soluções de Nível 1 (state persistence, history
  │     compression) são WORKAROUNDS para essas limitações.
  │
  ├─→ NÍVEL 2 (Padrões Práticos)
  │     Generator/Evaluator, Sprint Contracts, Rubrics, Trace
  │     Reading são PADRÕES ÓTIMOS para Era 4-5.
  │     Eles existem porque os modelos dessas eras TÊM tool use
  │     mas NÃO TÊM metacognition.
  │
  ├─→ NÍVEL 3 (Arquitetura Avançada)
  │     Multi-agent systems, state persistence avançada, harness
  │     evolution são PADRÕES para Era 5-6.
  │     Eles assumem que o modelo é agent-native e pode coordenar
  │     múltiplas instâncias.
  │
  └─→ NÍVEL 4 (KODA-Específico)
        Constitution design, audit trails, human-in-the-loop são
        PADRÕES para Era 6.
        Eles assumem autonomia quase total do agente e focam em
        governança, não em controle procedural.
```

**Regra de ouro:** O padrão de harness que você usa DEVE ser compatível com a era do seu modelo. Usar padrões de Era 3 com um modelo de Era 6 é sub-utilizar o modelo. Usar padrões de Era 6 com um modelo de Era 3 é pedir para falhar.

---

## 💭 Reflexão Final

> "O futuro já chegou. Só não está distribuído uniformemente." — William Gibson

Em 2018, um agente que conversa por 2 horas era ficção científica.
Em 2022, era um protótipo frágil.
Em 2024, era um produto funcional.
Em 2026, é infraestrutura.

A pergunta não é mais "é possível construir um long-running agent?".
A pergunta é: **"quais regras vão governar seus agentes quando eles forem mais capazes que os sistemas que você construiu para controlá-los?"**

Essa é a pergunta da Era 6. E você, tendo lido este documento, está entre os poucos engenheiros no mundo preparados para respondê-la.

---

## 🎬 Continue Sua Jornada

Feche este documento.

Pense no modelo que você está usando hoje para construir agentes.

Classifique-o em uma era.

Agora olhe para seu harness.

Pergunte-se: **"Meu harness está otimizado para a era do meu modelo, ou estou usando padrões de uma era passada?"**

Se você está usando prompt engineering pesado com Claude Opus 4.6... você está na era errada.

Ajuste. Evolua. O modelo já deu o salto. Seu harness precisa dar também.

---

**Pronto para continuar? O próximo nível te espera.**

---

*Escrito em Maio de 2026, na Era 6.*
*Este documento será atualizado conforme novos modelos e capacidades surgirem.*
*Última atualização: Maio 2026*
*Próxima atualização prevista: Julho 2026 (após próximo grande lançamento)*

### Como Contribuir para Este Documento

Este é um documento vivo. Quando um novo modelo flagship é lançado:

1. **Adicione o modelo** à tabela "Catálogo de Modelos"
2. **Atualize a timeline visual** (ASCII art no topo)
3. **Avalie:** O novo modelo define uma nova era? Se sim, crie a seção correspondente
4. **Revise os princípios:** Algum princípio novo emergiu? Algum precisa ser ajustado?
5. **Atualize o KODA:** Como o novo modelo impacta nossa arquitetura?
6. **Atualize a data** de "Última atualização" no metadata footer

**Checklist de atualização:**
- [ ] Modelo adicionado ao catálogo
- [ ] Timeline visual atualizada
- [ ] Nova era? Seção criada (ou era existente expandida)
- [ ] Princípios revisados
- [ ] Seção KODA atualizada com impacto
- [ ] FAQ atualizada se necessário
- [ ] Metadata footer atualizado

---

## 📋 Metadata

| Campo | Valor |
|---|---|
| **Arquivo** | model-capability-timeline.md |
| **Seção** | 10 - References |
| **Nível** | Todos os níveis |
| **Tempo** | 75 minutos |
| **Status** | ✅ Completo |
| **Cobre eras** | 2018-2030 (com projeções) |
| **Modelos cobertos** | 40+ |
| **Diagramas** | 8+ ASCII diagrams |
| **Tabelas comparativas** | 5 tabelas |
| **Crítica para** | Todas as decisões de arquitetura de agentes |
| **Próxima atualização** | Quando próximo modelo flagship for lançado |
| **Criado** | Maio 2026 |
| **Mantenedor** | Time KODA - Engenharia de Agentes |
| **Contribuidores** | Ver git blame para histórico completo |
| **Licença** | Interno - Uso exclusivo FutanBear |
| **Classificação** | Público interno (não confidencial) |
