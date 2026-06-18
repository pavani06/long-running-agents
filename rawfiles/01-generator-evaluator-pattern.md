---
title: "Padrão Generator/Evaluator: Quando Um Agente Não É Suficiente"
type: source
date: 2026-05-26
tags:
  - curriculo-conteudo
  - agentes-orquestracao
aliases:
  - generator evaluator pattern
  - padrao generator evaluator
  - dual agent architecture
relates-to:
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[curriculum/05-core-concepts/03-generator-evaluator-pattern|Generator-Evaluator Core Concept]]"
---

# 🔄 Padrão Generator/Evaluator: Quando Um Agente Não É Suficiente
## Como Duas Mentes Colaborativas Criam Confiabilidade e Qualidade

**Tempo Estimado:** 90 minutos  
**Nível:** 2 - Padrões Práticos  
**Pré-requisito:** Ter completado Nível 1 (Context Management, Token Budgeting, Basic Harness)  
**Status:** 🟢 CRÍTICO - Padrão que escala KODA de 75% para 98% de precisão  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Descoberta Que Escalou KODA de 75% Para 98% de Precisão

Imagine uma reunião em março de 2026. A equipe KODA acabava de examinar 1000 recomendações de produtos feitas pelo sistema. O resultado: **75% estava correto**. 25% tinha algum problema — preço desatualizado, produto fora de estoque, recomendação inadequada para o cliente, ou explicação confusa.

Para um sistema que promete "amigo de confiança", 75% é inaceitável.

Naquela semana, um cliente recebeu uma recomendação de suplemento para ganho muscular. O agente tinha anotado corretamente: "intolerante à lactose". Recomendou três produtos. Mas quando o cliente perguntou "e esse aqui tem lactose?", o agente respondeu com confiança inabalável: "Não, é sem lactose!" — quando na verdade **tinha lactose**. O cliente comprou, sofreu uma reação alérgica, e deixou uma avaliação de 1 estrela.

O problema era fascinante: o agente **havia cometido o erro, mas quando perguntado, não reconheceu**. Ele "avaliava" seu próprio trabalho e sempre concluía que estava certo. Esta é uma característica bem documentada de LLMs chamada **sycophancy** — a tendência de um modelo concordar consigo mesmo, de sempre achar que fez bom trabalho, de racionalizar seus próprios erros em vez de reconhecê-los.

**E se você não deixasse o agente avaliar a si mesmo?**

E se você separasse a responsabilidade em duas entidades distintas? Uma focada em **gerar** uma boa recomendação (o Generator). Outra focada em **avaliar criticamente** essa recomendação (o Evaluator). Sem compromissos, sem incentivos para concordar.

Isso é o **padrão Generator/Evaluator**.

Quando KODA implementou esse padrão, algo mágico aconteceu:
- Recomendações precisas: 75% → **98%** ✅
- Taxa de devolução: 15% → **6%** ✅
- Satisfação do cliente: 70% → **88%** ✅
- Cobranças duplicadas: 1% → **0%** ✅

Não mudou o modelo. Não mudou a IA. Mudou apenas a **arquitetura** — como dois agentes colaboram.

### Conexão com Nível 1

Você aprendeu em Nível 1 sobre os **3 problemas fundamentais** que fazem agentes falharem:

1. **Context Amnesia:** Informações críticas são esquecidas em conversas longas
2. **Planning Paralysis:** Agentes ficam indecisos sem estrutura clara
3. **Harness Fraco:** Sem guardrails, o agente não tem como se auto-corrigir

Generator/Evaluator **não resolve** esses três problemas diretamente. Mas cria um **harness sofisticado** ao redor deles. Mesmo que o Generator sofra de Context Amnesia ou indecisão, o **Evaluator é um checkpoint crítico** que força rigor e consistência.

É como um hospital: não podemos eliminar o fato de que médicos são humanos. Mas podemos criar **protocolos de verificação dupla** que transformam humanos falíveis em um sistema confiável.

### O Que Você Vai Aprender

Neste módulo, você vai:

✅ Entender **por que** separação funciona melhor que auto-avaliação  
✅ Desenhar um padrão Generator/Evaluator do zero  
✅ Implementar com **arquivos JSON** como canal de comunicação  
✅ Aplicar a **5 features reais do KODA**  
✅ Medir sucesso com **KPIs concretos**  
✅ Debugar quando algo falhar usando **trace reading**

E ao final, você poderá fazer o que a equipe KODA fez: **triplicar a qualidade sem trocar a IA fundamental**.

---

## 🎯 O Que É o Padrão Generator/Evaluator?

### Definição Simples

O **padrão Generator/Evaluator** é a separação deliberada de duas responsabilidades que normalmente um agente tenta fazer sozinho:

- **Generator:** Cria, produz, gera uma solução sem se preocupar com perfeição
- **Evaluator:** Avalia, verifica, aprova ou rejeita a solução do Generator

Eles não são a mesma entidade. Trabalham em sequência. O Evaluator **não pode ser influenciado** pela confiança ou viés do Generator.

### Analogia: Linha de Manufatura

Pense em uma fábrica de automóveis:

**Estação 1: O Operário (Generator)**
- Monta o motor, instala as peças, segue o blueprint
- Objetivo: Completar a montagem rápido e bem
- Assume: "Provavelmente ficou bom"
- **Problema:** Se tiver pressa, não revisa o próprio trabalho

**Estação 2: O Inspetor (Evaluator)**
- Recebe o motor montado
- Verifica CADA especificação: torque dos parafusos, alinhamento, tolerâncias
- Não é amigo do operário — sua única lealdade é à qualidade
- Usa checklist rígido: ✅ ou ❌, sem meio-termo
- **Resultado:** Motores defeituosos não saem da linha

**O Magic:** O operário não precisa ser perfeito. O inspetor **garante** que nada errado passa adiante.

Se o operário tentasse inspecionar seu próprio trabalho? Ele diria "ficou bom, achei" — e 25% dos motores sairia defeituoso da linha. **Separação de responsabilidades resolve isso.**

---

### Componentes do Padrão

#### 1️⃣ **Generator** — O Criador

**Responsabilidades:**
- Recebe input (contexto do cliente, produtos disponíveis, dados de pedido)
- Gera uma solução completa (recomendação, preço, validação)
- **NÃO tenta se auto-validar** — confia que o Evaluator vai verificar
- Outputs são estruturados (JSON, markdown com seções claras)

**Mindset:** "Vou criar a melhor solução com base nas informações que tenho"

**Liberdade:** O Generator pode ser criativo, explorar opções, e **não precisa ser 100% confiante** no resultado. Sua job é explorar, não garantir.

#### 2️⃣ **Evaluator** — O Crítico

**Responsabilidades:**
- Recebe a solução do Generator
- Valida contra critérios explícitos (rubrica, checklist, contrato)
- Identifica problemas, inconsistências, erros
- Aprova (✅) ou rejeita (❌) com feedback específico
- **Pode devolver ao Generator** para refazimento, ou rejeitar completamente

**Mindset:** "Meu job é encontrar erros. Vou ser tão crítico quanto possível."

**Poder:** O Evaluator é o gatekeeper — nada passa sem sua aprovação.

---

### Fluxo: Como Funciona na Prática

```
INPUT (Cliente, Pedido, Contexto)
    ↓
┌─────────────────────────────────┐
│  GENERATOR (Agente 1)           │
│  Gera solução/recomendação      │
│  Output: draft.json             │
└────────────┬────────────────────┘
             ↓
   ┌─────────────────────┐
   │ Passa para Evaluator│
   └──────────┬──────────┘
             ↓
┌─────────────────────────────────┐
│  EVALUATOR (Agente 2)           │
│  Verifica contra rubrica        │
│  • Correto? ✅                  │
│  • Seguro? ✅                   │
│  • Completo? ✅                 │
└────────────┬────────────────────┘
             ↓
    ┌────────────────────┐
    │ Se REPROVADO       │
    │ Feedback → Generator
    │ Tenta novamente    │
    └────────────────────┘
             ↓
┌─────────────────────────────────┐
│  OUTPUT FINAL (Aprovado)        │
│  Vai para cliente/sistema       │
└─────────────────────────────────┘
```

---

### Por Que Esta Estrutura Funciona

**1. Separação Elimina Sycophancy**

Um agente sozinho pensa: "Fiz isso, parece bom, logo está bom." *(confirmation bias)*

Dois agentes: Generator cria, Evaluator é **incentivado a encontrar erros**. Sua métrica de sucesso é "quantos erros encontrei", não "quantos aprovei".

**2. Especialização**

- Generator: Otimizado para **criatividade e completude**
- Evaluator: Otimizado para **rigor e verificação**

Cada um tem um "job" claro. Sem competição de objetivos.

**3. Auditabilidade**

Quando algo falha, você vê EXATAMENTE onde:
- Generator criou errado? 
- Evaluator deixou passar errado?

Trace files mostram tudo. (Aprenderemos em Seção 6)

**4. Escalabilidade**

Um agente fazendo tudo: O(n) qualidade, porque atenção degrada com tamanho da resposta.

Dois agentes com divisão clara: O(1) qualidade, porque cada um foca seu pedaço.

---

### Quando Não Usar Generator/Evaluator

Este padrão **não é sempre necessário**:

❌ Respostas simples (confirmação de pagamento, leitura de estoque)
❌ Quando a única métrica é "responder rápido"
❌ Problemas que não têm critérios de qualidade claros

✅ Quando qualidade > velocidade
✅ Quando erros têm custo (dinheiro, satisfação, confiança)
✅ Quando há múltiplas maneiras de estar "errado"

---

## ⚖️ Generator/Evaluator vs. Self-Evaluation: O Contraste Crítico

### O Problema Fundamental: Sycophancy

Um agente avaliando seu próprio trabalho é como um aluno corrigindo a própria prova. A estrutura mental é:

1. "Eu fiz isso"
2. "Fiz bem?"
3. "Sim, ficou bom!" *(confirmação bias)*

Especialmente em LLMs, existe uma característica chamada **sycophancy** — a tendência de concorder consigo mesmo, de racionalizar seus próprios erros, de sempre encontrar uma razão pela qual sua resposta "está correta, na verdade".

### Cenário Real KODA: Recomendação de Produto

**Cliente:** "Preciso de um suplemento para ganhar massa. Sou intolerante à lactose."

Vamos ver o que acontece nos dois cenários:

---

### ❌ Cenário 1: Agente Único (Self-Evaluation)

**O que o agente faz:**
1. Recebe a pergunta
2. Pensa: "Intolerante à lactose, preciso evitar..."
3. Busca produtos na base
4. Encontra "Whey Isolado Premium" (contém lactose!)
5. Recomenda: "Este é perfeito para você!"
6. Pergunta interna: "Mas espera, era sem lactose?"
7. Pensa: "Ah, o Whey Isolado é geralmente isolado, então provavelmente não tem lactose... ou tem pouca. Vou confiar na recomendação que fiz."
8. Responde ao cliente com confiança

**O Erro:** O agente **criou o erro** e depois **avaliou seu próprio erro como correto**.

**Pseudocódigo do Agente Único:**
```json
{
  "system_prompt": "Você é um recomendador de produtos. Recomende produtos que atendam ao objetivo do cliente. Quando terminar, verifique se sua recomendação é boa.",
  
  "messages": [
    {
      "role": "user",
      "content": "Preciso de suplemento para ganhar massa. Sou intolerante à lactose."
    }
  ],
  
  "agent_thinking": {
    "step_1": "Cliente quer ganho muscular, sem lactose",
    "step_2": "Procurando em base de produtos...",
    "step_3": "Encontrei: Whey Isolado Premium - R$ 89",
    "step_4_generation": "Recomendo o Whey Isolado Premium",
    "step_5_self_evaluation": "Minha recomendação está boa? Deixe-me verificar...",
    "step_6_self_check": "Sim, é um suplemento de qualidade, preço bom, deve atender",
    "step_7_output": "Recomendo este produto com confiança!"
  },
  
  "problem": "Passo 4 (generation) e Passo 6 (evaluation) são feitos pelo MESMO agente. Bias natural = concordar consigo mesmo."
}
```

**Por que falha:**
- O agente não consultou se o Whey Isolado **realmente** é sem lactose
- Quando se avaliou, começou a racionalizar: "Isolado provavelmente significa sem lactose"
- Nunca reconheceu que poderia estar errado, porque não há incentivo para encontrar erros

---

### ✅ Cenário 2: Generator/Evaluator (Separação)

**Generator (Agente 1):**
1. Recebe: "Preciso de ganho muscular, intolerante à lactose"
2. Pensa: "Vou gerar a melhor recomendação que consigo"
3. Busca produtos para ganho muscular
4. Encontra: Whey Isolado Premium
5. Cria resposta estruturada: "Recomendo: Whey Isolado Premium, R$ 89, para ganho muscular"
6. **NÃO verifica a si mesmo** — apenas passa adiante

**Evaluator (Agente 2):**
1. Recebe a recomendação do Generator
2. Verifica contra rubrica rígida:
   - ✅ Produto existe? SIM (SKU validado)
   - ❓ Sem lactose? **PRECISA VERIFICAR NA TABELA DE NUTRIÇÃO**
   - Encontra: "Whey Isolado Premium: Contém lactose (6g por porção)"
   - ❌ REJEITA a recomendação
3. Envia feedback: "Produto contém lactose. Cliente é intolerante. Rejeitar."

**Generator recebe o feedback:**
1. "Entendi, preciso de algo sem lactose mesmo"
2. Busca novamente
3. Encontra: "Whey Vegano 100% - R$ 95, sem lactose confirmado"
4. Gera nova resposta

**Evaluator verifica novamente:**
- ✅ Sem lactose? SIM (confirmado)
- ✅ Para ganho muscular? SIM
- ✅ Preço razoável? SIM
- **APROVA**

**Resultado:** Cliente recebe a recomendação correta na segunda tentativa.

**Pseudocódigo com Dois Agentes:**
```json
{
  "step_1_input": {
    "customer_need": "ganho muscular",
    "restriction": "intolerante à lactose"
  },
  
  "step_2_generator": {
    "system_prompt": "Gere a melhor recomendação com base no objetivo. Não se auto-avalie.",
    "task": "Recomendar suplemento para ganho muscular",
    "output": {
      "product": "Whey Isolado Premium",
      "sku": "WHEY-001",
      "price": 89,
      "rationale": "Produto isolado, excelente para ganho muscular"
    },
    "note": "Generator não verifica — apenas gera"
  },
  
  "step_3_evaluator": {
    "system_prompt": "Você é crítico. Encontre erros. Seu sucesso é medido por ERROS ENCONTRADOS.",
    "rubric": {
      "product_exists": "Validar SKU",
      "lactose_free": "Verificar nutrição - cliente é intolerante",
      "price_reasonable": "Comparar com mercado",
      "clear_explanation": "Explicação ajuda cliente?"
    },
    "evaluation": {
      "product_exists": true,
      "lactose_free": false,  // ERRO ENCONTRADO
      "verdict": "REJECTED",
      "feedback": "Produto contém lactose (6g/porção). Cliente é intolerante. Rejeitar."
    }
  },
  
  "step_4_feedback_loop": {
    "generator_receives": "Seu produto tem lactose. Tente novamente.",
    "generator_generates_v2": {
      "product": "Whey Vegano 100%",
      "sku": "WHEY-VEGAN-001",
      "price": 95,
      "rationale": "100% vegano, sem lactose, proteína de alta qualidade"
    }
  },
  
  "step_5_evaluator_v2": {
    "evaluation": {
      "product_exists": true,
      "lactose_free": true,
      "price_reasonable": true,
      "verdict": "APPROVED"
    }
  },
  
  "final_output": "Whey Vegano 100% - Recomendação aprovada"
}
```

---

### 📊 Comparação Lado-a-Lado

| Aspecto | Agente Único (Self-Eval) | Generator/Evaluator |
|---------|--------------------------|-------------------|
| **Quem verifica?** | O próprio agente | Agente independente (Evaluator) |
| **Incentivo** | Concordar consigo mesmo | Encontrar erros |
| **Bias** | Alto (sycophancy) | Baixo (roles separados) |
| **Acurácia (exemplo)** | 25% (recomendação errada) | 98% (rejeita erro, aprova correto) |
| **Tempo** | Rápido, mas errado | Mais lento, mas confiável |
| **Transparência** | "Parecia bom pra mim" | "Avaliador rejeitou por X razão" |
| **Escalabilidade** | Piora com complexidade | Melhora (mais critérios, melhor filtro) |

---

### 🔧 Por Que G/E Funciona Melhor

**1. Incentivos Alinhados**
- Generator: "Crie a melhor solução possível"
- Evaluator: "Encontre erros e rejeite ruim"

Esses incentivos **não competem**. Em self-eval, são o mesmo agente, então há conflito.

**2. Especialização Cognitiva**
- Generator pode ser criativo, explorador, tomar riscos
- Evaluator pode ser rigoroso, crítico, sistemático

Um agente sozinho precisa ser ambos, e geralmente um lado vence.

**3. Auditabilidade**
- Quando erro passa: "O Evaluator deixou passar? Por quê?"
- Em self-eval: "Achei que estava certo"

Não há espaço para refutação. Com dois agentes, é fácil debugar.

**4. Escala**
- Agente único: qualidade degrada quando contexto fica complexo
- Generator/Evaluator: Evaluator pode aplicar **rubricas arbitrariamente rígidas**

Quanto mais complexa a tarefa, maior a vantagem do padrão.

---

### ✨ A Insight Final

Você não pode fazer um agente "ser ao mesmo tempo criativo e crítico". Isso é contraditório. 

Generator/Evaluator resolve isso reconhecendo que **criatividade e crítica são músculos diferentes**. Quando você tem dois agentes, cada um otimizado para seu papel, emerge algo que nenhum agente sozinho pode fazer: **confiabilidade sem sacrificar qualidade**.

---

## 🏗️ Arquitetura: Como Dois Agentes Colaboram

### Visão Conceitual: O Princípio Central

Generator/Evaluator funciona em torno de um princípio simples:

**Agentes não compartilham memória. Compartilham arquivos.**

Quando o Generator termina, ele escreve seu trabalho em um arquivo. Quando o Evaluator checa, ele lê esse arquivo. Quando rejeita, ele escreve feedback em outro arquivo. O Generator lê o feedback e tenta novamente.

É como uma fila de trabalho — cada etapa deixa seus artefatos para a próxima etapa ler.

---

### O Núcleo: State Files (Persistência de Estado)

Em vez de manter tudo na memória ou em chamadas API, você cria **arquivos JSON como fonte de verdade**.

Por quê? Porque:
1. **Agentes são stateless** — cada chamada começa do zero
2. **Auditabilidade** — arquivo é um log permanente de "quem fez o quê"
3. **Debugging** — você pode ler exatamente o que cada agente viu e criou
4. **Recuperação** — se algo falhar, você sabe exatamente em que ponto

### Os Arquivos Principais

Vamos usar um exemplo de **Recomendação de Produtos** (KODA). A estrutura de arquivos é:

```
recommendation-state/
├── customer_context.json       # Dados do cliente (immutável)
├── generator_draft.json        # Solução criada pelo Generator
├── evaluator_verdict.json      # Avaliação do Evaluator
├── feedback.json              # Se rejeitado, feedback para Generator
└── audit_log.jsonl            # Timestamp de cada mudança
```

---

### Arquivo 1: customer_context.json

Este arquivo **NÃO MUDA**. É criado uma vez e lido por todos.

```json
{
  "customer_id": "wa_5511987654321",
  "customer_name": "João Silva",
  "goal": "ganho_muscular",
  "level": "intermediário",
  "restrictions": {
    "lactose_intolerant": true,
    "allergic_to": ["amendoim"],
    "dietary_preference": "nenhuma"
  },
  "purchase_history": [
    "whey_protein_200g",
    "creatina_500g"
  ],
  "club_member": true,
  "club_discount": 0.15,
  "budget_max": 200,
  "created_at": "2026-05-23T10:00:00Z"
}
```

**Quem cria:** Sistema (antes de chamar Generator)  
**Quem lê:** Generator (para gerar), Evaluator (para validar contra restrições)

---

### Arquivo 2: generator_draft.json

O Generator escreve aqui após criar a recomendação.

```json
{
  "generation_id": "gen_001",
  "timestamp": "2026-05-23T10:01:30Z",
  "generator_input": "customer_context.json",
  "recommendations": [
    {
      "rank": 1,
      "sku": "WHEY-VEGAN-001",
      "name": "Whey Vegano 100% Premium",
      "price_base": 95.00,
      "price_with_discount": 80.75,
      "description": "Proteína vegana, sem lactose, alta absorção, ideal para ganho muscular",
      "in_stock": true,
      "stock_qty": 47,
      "rationale": "Vegano = sem lactose confirmado. Alta proteína (28g/porção). Preço bom com desconto de clube."
    },
    {
      "rank": 2,
      "sku": "BCAA-PREMIUM-001",
      "name": "BCAA Premium Chocolate",
      "price_base": 65.00,
      "price_with_discount": 55.25,
      "in_stock": true,
      "rationale": "Complemento. Sem lactose. Suporte para recuperação."
    }
  ],
  "generator_confidence": 0.75,
  "notes": "Recomendações baseadas em histórico + objetivo. PRECISA VALIDAR: lactose em todos produtos."
}
```

**Quem cria:** Generator (após análise)  
**Quem lê:** Evaluator (para validar cada item)  
**Importante:** Generator deixa uma nota de transparência: "PRECISA VALIDAR: lactose"

---

### Arquivo 3: evaluator_verdict.json

Depois de ler o draft, o Evaluator escreve sua avaliação.

**Se aprovado:**
```json
{
  "verdict_id": "eval_001",
  "generation_id": "gen_001",
  "timestamp": "2026-05-23T10:02:15Z",
  "verdict": "APPROVED",
  "rubric_scores": {
    "product_exists": {
      "score": true,
      "notes": "SKU WHEY-VEGAN-001 validado em inventário"
    },
    "lactose_free": {
      "score": true,
      "notes": "Produto marcado como 'vegan' = sem lactose confirmado. Verificado em nutrição DB."
    },
    "price_reasonable": {
      "score": true,
      "notes": "R$ 95 → R$ 80.75 com desconto. 15% abaixo da média do mercado."
    },
    "in_stock": {
      "score": true,
      "notes": "47 unidades em estoque. Entrega same-day possível."
    },
    "matches_goal": {
      "score": true,
      "notes": "28g de proteína por porção = excelente para ganho muscular"
    },
    "explanation_clarity": {
      "score": 8,
      "max": 10,
      "notes": "Explicação clara. Poderia mencionar timing de consumo."
    }
  },
  "overall_score": 9.2,
  "approval_threshold": 7.0,
  "status": "APPROVED"
}
```

**Se rejeitado:**
```json
{
  "verdict_id": "eval_001",
  "generation_id": "gen_001",
  "timestamp": "2026-05-23T10:02:15Z",
  "verdict": "REJECTED",
  "reason": "CRITICAL_ISSUE",
  "issues": [
    {
      "product_sku": "WHEY-VEGAN-001",
      "issue_type": "LACTOSE_PRESENT",
      "description": "Produto contém lactose (6g por porção). Cliente é intolerante. REJEITAR.",
      "severity": "CRITICAL"
    },
    {
      "product_sku": "BCAA-PREMIUM-001",
      "issue_type": "OUT_OF_STOCK",
      "description": "Estoque zerado. Recomendação menciona 'em estoque' mas verificação real mostra 0 unidades.",
      "severity": "HIGH"
    }
  ],
  "overall_score": 2.1,
  "approval_threshold": 7.0,
  "status": "REJECTED",
  "feedback_for_generator": "1) Primeiro item tem lactose — DEVE SER EVITADO. 2) Segundo item fora de estoque. Tente novamente com produtos que atendam TODAS as restrições."
}
```

---

### Arquivo 4: feedback.json (Se Rejeitado)

Se o Evaluator rejeitou, ele escreve feedback estruturado para o Generator ler.

```json
{
  "feedback_id": "fb_001",
  "verdict_id": "eval_001",
  "timestamp": "2026-05-23T10:02:15Z",
  "message": "Recomendação rejeitada. Leia as issues e tente novamente.",
  "issues": [
    {
      "severity": "CRITICAL",
      "message": "WHEY-VEGAN-001 contém lactose. Cliente é intolerante à lactose. Produto deve ser 100% livre de lactose.",
      "action": "REMOVE este produto das recomendações"
    },
    {
      "severity": "HIGH",
      "message": "BCAA-PREMIUM-001 está out of stock (0 unidades). Não recomende produtos indisponíveis.",
      "action": "REMOVA ou substitua por versão em estoque"
    }
  ],
  "retry_instruction": "Procure produtos que atendam TODOS os critérios: (1) sem lactose, (2) em estoque, (3) para ganho muscular, (4) preço ≤ R$ 200"
}
```

---

### Arquivo 5: audit_log.jsonl

Um log imutável de cada evento. Uma linha por evento, em ordem cronológica.

```json
{"timestamp":"2026-05-23T10:00:00Z","event":"context_created","customer_id":"wa_5511987654321"}
{"timestamp":"2026-05-23T10:01:30Z","event":"generation_completed","generation_id":"gen_001","generator_confidence":0.75}
{"timestamp":"2026-05-23T10:02:15Z","event":"evaluation_completed","verdict_id":"eval_001","verdict":"REJECTED"}
{"timestamp":"2026-05-23T10:02:20Z","event":"feedback_sent","feedback_id":"fb_001"}
{"timestamp":"2026-05-23T10:03:00Z","event":"generation_retried","generation_id":"gen_002","retry_attempt":1}
{"timestamp":"2026-05-23T10:03:45Z","event":"evaluation_completed","verdict_id":"eval_002","verdict":"APPROVED"}
```

**Por que JSON Lines (.jsonl)?** Cada linha é um documento JSON completo. Fácil de ler, parsear, e adicionar eventos sem reescrever o arquivo inteiro.

---

### O Ciclo Completo: Passo a Passo

```
1. SETUP (Sistema)
   └─ Cria customer_context.json
   └─ Valida que arquivo é legível

2. GENERATION (Generator)
   ├─ Lê customer_context.json
   ├─ Analisa restrições, histórico, objetivo
   ├─ Gera recomendações
   ├─ Escreve em generator_draft.json
   └─ Log: "generation_completed"

3. EVALUATION (Evaluator)
   ├─ Lê customer_context.json (para restrições)
   ├─ Lê generator_draft.json (o que foi gerado)
   ├─ Valida contra rubric rígida
   ├─ Escreve em evaluator_verdict.json
   └─ Log: "evaluation_completed"

4. DECISION POINT
   ├─ Se APPROVED (score ≥ 7.0)
   │  └─ Retorna recomendações ao cliente
   │  └─ Log: "approved_and_delivered"
   │
   └─ Se REJECTED (score < 7.0)
      ├─ Escreve feedback.json
      ├─ Log: "rejected_with_feedback"
      └─ Volta ao passo 2 (Generator tenta novamente)

5. MAX RETRIES (Segurança)
   └─ Se 3 tentativas falharem, escala para humano
```

---

### Checklist Arquitetural: 3 Decisões Críticas

Antes de implementar, você precisa decidir:

#### ❓ 1. Quantas iterações antes de desistir?

| Cenário | Recomendação |
|---------|-------------|
| Recomendação simples | 2-3 iterações máx |
| Processamento de pedido | 3-4 iterações máx |
| Tarefa complexa | 5 iterações máx |
| Indefinido = risco | Nunca deixe infinito |

**Implementação:**
```json
{
  "max_iterations": 3,
  "current_iteration": 2,
  "max_reached": false,
  "action_if_max": "escalate_to_human"
}
```

**Por quê?** Evita loops infinitos. Se Generator não consegue em 3 tentativas, o problema é maior — humano precisa intervir.

---

#### ❓ 2. Qual é o tamanho máximo de resposta do Generator?

O Generator pode gerar respostas muito longas (e caras). Você precisa de um limite.

| Limite | Use quando |
|--------|-----------|
| 500 tokens | Recomendações simples |
| 1000 tokens | Análises médias |
| 2000 tokens | Análises complexas |
| > 2000 tokens | Raro; geralmente sinal de problema |

**Implementação:**
```json
{
  "generator_config": {
    "max_tokens": 1000,
    "temperature": 0.7,
    "stop_sequences": ["Fim da recomendação", "---"]
  }
}
```

**Por quê?** Controla custo e evita responses bloated que o Evaluator tem que processar.

---

#### ❓ 3. Como o Evaluator comunica rejeição?

Feedback vago ("Não gostei") não ajuda Generator. Feedback específico ("Produto X contém Y, viola restrição Z") funciona.

**Estrutura de Feedback (obrigatória):**
```json
{
  "feedback": {
    "severity": "CRITICAL|HIGH|MEDIUM|LOW",
    "issue_code": "LACTOSE_PRESENT|OUT_OF_STOCK|PRICE_TOO_HIGH|...",
    "issue_text": "Descrição legível do que está errado",
    "affected_item": "SKU ou índice do problema",
    "fix_instruction": "Exatamente o que o Generator precisa fazer"
  }
}
```

**Por quê?** Generator aprende com feedback específico. Feedback vago = infinitas tentativas.

---

### Diagrama: Arquitetura de State Files

[Diagrama será criado na próxima seção]

A estrutura visual mostra como os arquivos fluem entre Generator e Evaluator, com audit log registrando cada passo.

---

## 📚 5 Casos de Estudo KODA

Os padrões que você aprendeu até aqui são abstratos. Agora vamos ver como eles funcionam **em produção, resolvendo problemas reais do KODA**.

---

## Caso 1: Promotion Application (Simples) 🎯

**O Problema**

Cliente faz um pedido e menciona: "Tenho código de promoção". KODA precisa:
1. Validar que o código é válido (não expirou, não foi usado)
2. Aplicar o desconto correto (pode ter regras complexas)
3. Garantir que o desconto não se sobrepõe a outros descontos

**Por que falha com agente único:**
- Generator aplica 15% de desconto "progressivo"
- Cliente também tem "desconto de clube" (10%)
- Agente único pensa: "Aplico ambos = 25% total" ❌ (double-discount)
- Evaluator nunca é chamado porque não existe Evaluator

**Solução: Generator + Evaluator**

**Generator:**
```
Input: order_total=100, promo_code=SUMMER15, customer_tier=club
Output: 
  - Base: R$ 100
  - Promo SUMMER15: -R$ 15 (15%)
  - Total com promo: R$ 85
```

**Evaluator (checklist rígido):**
```
✅ Código válido? SIM (em BD, não expirado)
✅ Já foi usado por este cliente? NÃO (primeira vez)
✅ Promo cumulativa com clube? NÃO (regra: aplica melhor, não soma)
✅ Desconto final razoável? SIM (15% é dentro da política)
→ APROVADO
```

**JSON Exemplo Completo:**

**generator_draft.json:**
```json
{
  "order_id": "ORD-2026-5523",
  "customer_id": "wa_5511987654321",
  "order_total": 100.00,
  "items": [
    {"sku": "WHEY-001", "qty": 1, "price": 89.90},
    {"sku": "CREATINE-001", "qty": 1, "price": 10.10}
  ],
  "discounts": {
    "promo_code": {
      "code": "SUMMER15",
      "discount_amount": 15.00,
      "discount_percent": 15,
      "description": "Promoção de verão 15% off"
    },
    "club_discount": {
      "club_member": true,
      "discount_amount": 0,
      "discount_percent": 0,
      "reason": "Promo supera desconto de clube, não é cumulativo"
    },
    "total_discount": 15.00
  },
  "final_total": 85.00,
  "generator_notes": "Aplicada promoção. Verificar: código era SUMMER15, não é cumulativo com clube."
}
```

**evaluator_verdict.json:**
```json
{
  "verdict": "APPROVED",
  "checks": {
    "promo_exists": {"status": "✓", "details": "SUMMER15 encontrado em BD"},
    "promo_expired": {"status": "✓", "details": "Válido até 2026-06-30"},
    "customer_used_before": {"status": "✓", "details": "Primeira vez usando este código"},
    "cumulativity_rules": {"status": "✓", "details": "Promo não é cumulativa, aplicada corretamente"},
    "discount_within_policy": {"status": "✓", "details": "15% dentro dos limites"}
  },
  "overall_score": 10,
  "status": "APPROVED",
  "final_total": 85.00
}
```

**Resultado:**
- ✅ Sem double-discount
- ✅ Cliente satisfeito
- ✅ Receita protegida
- ⏱️ Tempo: 2-3 segundos (Generator + Evaluator)

---

## Caso 2: Product Discovery (Médio) 🔍

**O Problema**

Cliente: "Procuro suplemento para ganhar massa. Sou intolerante à lactose e prefiro sabor chocolate."

KODA precisa gerar recomendações que **simultaneamente:**
1. Correspondem ao objetivo (ganho muscular)
2. Respeitam restrições (sem lactose)
3. Têm boa relação preço/benefício
4. Estão em estoque **agora**
5. São apresentadas com clareza

**O Desafio**

Antes de Generator/Evaluator: 75% de precisão. Recomendações erradas custavam:
- Devoluções (15% de taxa)
- Reclamações (feedback negativo)
- Perda de confiança do cliente

**Como Generator/Evaluator Resolve**

**Generator (criativo, explora opções):**
```
Gera 5 opções:
1. Whey Isolado Premium (R$ 89) - "proteína pura, sem lactose"
2. Whey Vegano 100% (R$ 95) - "100% vegano, sem lactose garantido"
3. BCAA Chocolate (R$ 45) - "suplemento de recuperação"
4. Creatina Monohidratada (R$ 65) - "básico mas eficaz"
5. Proteína Casein (R$ 110) - "absorção lenta, para noite"
```

**Evaluator (crítico, verifica cada uma):**
```
Produto 1: Whey Isolado
  ✅ Objetivo? SIM (ganho muscular)
  ❌ Sem lactose? NÃO (contém 2g/porção) → REJEITA
  
Produto 2: Whey Vegano
  ✅ Objetivo? SIM
  ✅ Sem lactose? SIM (verificado)
  ✅ Chocolate? SIM
  ✅ Em estoque? SIM (47 unidades)
  ✅ Preço OK? SIM (R$ 95, dentro do orçamento)
  ✅ Clareza? SIM (explicação inclui benefícios)
  → APROVA
  
Produto 3: BCAA
  ✅ Objetivo? SIM (complemento)
  ✅ Sem lactose? SIM
  ✅ Chocolate? SIM
  ✅ Em estoque? NÃO (0 unidades) → REJEITA
  
Produto 4: Creatina
  ✅ Objetivo? SIM
  ✅ Sem lactose? SIM
  ✅ Chocolate? NÃO → REJEITA
  
Produto 5: Casein
  ❌ Sem lactose? NÃO → REJEITA
```

**Resultado final ao cliente:**
✅ Whey Vegano 100% (APROVADO)
+ sugestões secundárias de complementos sem lactose

**Impacto Medido:**

| Métrica | Antes | Depois |
|---------|-------|--------|
| Precisão | 75% | 98% |
| Taxa de devolução | 15% | 6% |
| Satisfação | 70% | 88% |
| Recompra | 35% | 52% |
| ROI | - | 30x o custo adicional |

---

## Caso 3: Review Quality Verification (Médio) ⭐

**O Problema**

Clientes deixam reviews de produtos. Alguns são legítimos, outros são spam ou maliciosos:
- "Produto ruim" (sem detalhes, padrão spam)
- "COMPREM AQUI: [link malicioso]"
- Reviews de concorrentes
- Reviews verdadeiros mas confusos

KODA precisa **filtrar reviews ruins** sem rejeitar reviews legítimos negativos.

**Como Funciona**

**Generator:**
Lê review e categoriza:
- Tipo: "Negativo", "Neutro", "Positivo"
- Conteúdo: extrai pontos principais
- Autenticidade: "Parece legítimo?"

**Evaluator (rubric específica):**
```
✅ Menção específica do produto? (ou é genérico?)
✅ Detalhes técnicos ou apenas emoção?
✅ Sem links maliciosos?
✅ Linguagem natural (não spam)?
✅ Reviewers tem histórico de compra do produto?
```

**Resultado:**
- Spam rejeitado: 95% de acurácia
- Reviews legítimos aprovados: 99% de acurácia
- Impacto: Reviews mais confiáveis → clientes compram com mais confiança

---

## Caso 4: Order Processing (Complexo) 📦

**O Problema**

Processar um pedido envolve 6 etapas sequenciais, cada uma com potencial de erro:

1. Validar cliente (membro ativo? pagamento cadastrado?)
2. Verificar inventário (disponível? reservar unidades?)
3. Calcular preço (desconto de clube + bulk + promoções)
4. Aplicar promoções (sem double-discount)
5. Processar pagamento (cobrar exatamente uma vez)
6. Agendar fulfillment (same-day ou agendado?)

**Antes:** 95% de precisão = 5% de pedidos com erro
- Preço errado
- Cobranças duplicadas
- Endereço errado

**Solução: Generator + Evaluator em 6 Sprints**

Cada etapa é um **Generator/Evaluator pair** independente:

```
Sprint 1: Validar Cliente
  Generator: "Cliente existe, membro ativo, pagamento ok"
  Evaluator: "Verificado. ✓"

Sprint 2: Verificar Inventário
  Generator: "Reservei 2x WHEY-001, 1x BCAA-001"
  Evaluator: "Race condition check... sem problemas. ✓"

Sprint 3: Calcular Preço
  Generator: "Subtotal 354.80, desconto clube -35.48, promo -17.50, total 301.82"
  Evaluator: "Matemática OK, sem double-discount. ✓"

Sprint 4: Processar Pagamento
  Generator: "API de pagamento retornou txn_abc123"
  Evaluator: "Transação idempotente? Checado. Não cobrou duas vezes. ✓"

Sprint 5: Agendar Fulfillment
  Generator: "Agendei entrega 16h, tracking TRK-789456"
  Evaluator: "ETA realista? SIM. Endereço válido? SIM. ✓"

Sprint 6: Confirmar Tudo
  Generator: "Pedido completo, enviando confirmação ao cliente"
  Evaluator: "Todos os sprints aprovados. APROVA"
```

**Resultado:**
- Precisão: 95% → 99.8%
- Erros: 5% → 0.2%
- Cobranças duplas: 1% → 0%
- Satisfação: aumento significativo

---

## Caso 5: Fulfillment & Same-Day Delivery (Muito Complexo) 🚚

**O Problema**

KODA promete "entrega no mesmo dia" como diferencial. Mas é **intrinsecamente complexo:**

1. **Geograficamente disperso:** Múltiplos armazéns, múltiplas rotas
2. **Dependência de parceiros:** Entregadores, vans, motos
3. **Timing crítico:** Uma mudança minúscula no horário quebra a promessa
4. **Estado compartilhado:** Inventário em múltiplos lugares

**Como Generator/Evaluator Coordena**

**Generator (3 agentes paralelos):**
- **Agente A:** "Qual armazém tem o produto?"
- **Agente B:** "Qual é a melhor rota de entrega?"
- **Agente C:** "Qual entregador está disponível?"

**Evaluator (1 agente orquestrador):**
- Recebe respostas dos 3 generators
- Verifica se tudo é **coordenado e realista:**
  - ✅ Armazém tem estoque?
  - ✅ Rota + entregador combinam para ETA realista?
  - ✅ Sem conflitos (mesmo entregador não pode fazer 2 rotas)?
  - ✅ Margem de segurança? (sempre deixar 30min de buffer)

**Se tudo OK:** Cria ordem de fulfillment  
**Se problema:** Devolve feedback (Ex: "Entregador X indisponível, use Y" ou "Rota muito longa, use armazém diferente")

**Resultado:**
- Same-day delivery: 95%+ de sucesso
- Clientes chegam no horário: 92%+ satisfação
- Custo operacional: otimizado

---

### 📊 Resumo dos 5 Casos

| Caso | Complexidade | Ganho Principal | Métrica |
|------|-------------|-----------------|---------|
| Promotions | Simples | Zero double-discount | 100% acurácia |
| Product Discovery | Médio | 98% recomendações corretas | 30x ROI |
| Review Quality | Médio | 95% spam filtrado | Confiança +40% |
| Order Processing | Complexo | 99.8% pedidos sem erro | Devolução -80% |
| Fulfillment | Muito Complexo | Same-day delivery confiável | Satisfação +35% |

**A Pattern:** Quanto mais complexa a tarefa, mais Generator/Evaluator brilha.
- Simples: 10% de melhora
- Médio: 25% de melhora
- Complexo: 50%+ de melhora

---

## 💻 Implementação Prática: Do Conceito ao Código

Você agora entende **o quê** é Generator/Evaluator. Agora vamos ver **como implementar**.

---

### 1️⃣ Setup Básico: Começar do Zero

**Estrutura de diretórios:**
```
your-koda-project/
├── src/
│   ├── generator.py          # Agente que cria
│   ├── evaluator.py          # Agente que verifica
│   └── orchestrator.py        # Orquestra os dois
│
├── state/
│   ├── {customer_id}/
│   │   ├── customer_context.json
│   │   ├── generator_draft_v1.json
│   │   ├── evaluator_verdict_v1.json
│   │   ├── feedback_v1.json
│   │   └── audit_log.jsonl
│   └── {customer_id}/
│       └── ...
│
└── config/
    └── generator_evaluator_config.json
```

**Ficheiro de Configuração:**
```json
{
  "max_iterations": 3,
  "timeout_seconds": 30,
  "generator_config": {
    "model": "claude-sonnet-4-6",
    "max_tokens": 1000,
    "temperature": 0.7
  },
  "evaluator_config": {
    "model": "claude-sonnet-4-6",
    "max_tokens": 800,
    "temperature": 0.3
  },
  "paths": {
    "state_dir": "./state",
    "log_dir": "./logs"
  }
}
```

**Inicializar um novo caso:**
```json
{
  "case_id": "ORD-2026-5523",
  "customer_id": "wa_5511987654321",
  "task_type": "product_recommendation",
  "context": {
    "goal": "ganho_muscular",
    "restrictions": ["lactose_free"],
    "budget_max": 200
  },
  "created_at": "2026-05-23T10:00:00Z",
  "status": "initialized"
}
```

---

### 2️⃣ State Persistence: Estrutura de Arquivos

**Princípio:** Cada arquivo é uma "versão" de um estado. Versões permitem replay e debug.

**Convenção de nomes:**
```
{file_type}_v{iteration}.json

Exemplos:
- customer_context.json (v0, nunca muda)
- generator_draft_v1.json (1ª tentativa)
- evaluator_verdict_v1.json (1ª avaliação)
- feedback_v1.json (1º feedback se rejeitado)
- generator_draft_v2.json (2ª tentativa, após feedback)
- evaluator_verdict_v2.json (2ª avaliação)
...
```

**Script de inicialização (pseudocódigo):**
```python
# 1. Criar diretório para este caso
def initialize_case(customer_id, case_id):
    case_dir = f"state/{customer_id}/{case_id}"
    create_directory(case_dir)
    
    # 2. Fetch customer context (de BD ou API)
    customer_data = fetch_from_database(customer_id)
    
    # 3. Escrever customer_context.json (imutável)
    context = {
        "customer_id": customer_id,
        "customer_name": customer_data.name,
        "goal": customer_data.goal,
        "restrictions": customer_data.restrictions,
        "created_at": now(),
        "version": "immutable"
    }
    write_json(f"{case_dir}/customer_context.json", context)
    
    # 4. Log this event
    log_event(
        case_id=case_id,
        event="case_initialized",
        timestamp=now()
    )
```

---

### 3️⃣ Exemplo Completo: O Fluxo Inteiro

Vamos acompanhar um exemplo real de **recomendação de produto** do início ao fim.

**Setup:**
- Cliente: João Silva (wa_5511987654321)
- Objetivo: Ganho muscular
- Restrição: Sem lactose
- Orçamento: até R$ 200

**ITERAÇÃO 1:**

**Step 1: Generator cria (pseudocódigo com comentários)**
```python
def run_generator(iteration, customer_context, feedback=None):
    """
    Generator recebe:
    1. Contexto do cliente (imutável)
    2. Feedback da iteração anterior (se houver)
    
    Output: arquivo generator_draft_v{iteration}.json
    """
    
    system_prompt = """
    Você é um recomendador de produtos KODA.
    
    Gere recomendações que atendam:
    - Objetivo do cliente
    - Restrições alimentares
    - Orçamento
    
    Para cada produto, inclua:
    - SKU, nome, preço
    - Rationale (por que recomendo)
    - Verificação de restrições (SIM/NÃO para cada restrição)
    
    Não se preocupe em validar estoque ou preços finais.
    O Evaluator vai verificar.
    """
    
    # Se há feedback, incorpora na prompt
    if feedback:
        system_prompt += f"\n\nFeedback da iteração anterior:\n{feedback}"
    
    # Call Claude API
    response = call_claude(
        system_prompt=system_prompt,
        user_message=format_user_message(customer_context),
        max_tokens=1000,
        temperature=0.7
    )
    
    # Parse response into structured format
    draft = parse_response_to_json(response)
    
    # Write to file
    draft_output = {
        "generation_id": f"gen_{iteration}",
        "iteration": iteration,
        "timestamp": now(),
        "recommendations": draft["recommendations"],
        "generator_notes": draft["notes"],
        "generator_confidence": draft["confidence"]
    }
    
    write_json(f"state/{customer_id}/generator_draft_v{iteration}.json", draft_output)
    
    return draft_output
```

**Output do Generator (Iteração 1):**
```json
{
  "generation_id": "gen_1",
  "iteration": 1,
  "timestamp": "2026-05-23T10:01:30Z",
  "recommendations": [
    {
      "rank": 1,
      "sku": "WHEY-ISOLADO-001",
      "name": "Whey Isolado Premium",
      "price_base": 89.90,
      "restrictions_check": {
        "lactose_free": "SIM (isolado = sem lactose)"
      },
      "rationale": "Proteína isolada, absorção rápida, ideal para ganho muscular"
    },
    {
      "rank": 2,
      "sku": "BCAA-CHOCOLATE-001",
      "name": "BCAA Chocolate Premium",
      "price_base": 65.00,
      "restrictions_check": {
        "lactose_free": "SIM"
      },
      "rationale": "Complemento para recuperação, sabor chocolate conforme preferência"
    }
  ],
  "generator_notes": "Recomendações focadas em ganho muscular, sem lactose.",
  "generator_confidence": 0.8
}
```

**Step 2: Evaluator verifica (pseudocódigo com comentários)**
```python
def run_evaluator(iteration, generator_draft, customer_context):
    """
    Evaluator recebe:
    1. O draft do Generator
    2. O contexto imutável do cliente
    
    Verifica TUDO que o Generator não verificou.
    Output: evaluator_verdict_v{iteration}.json
    """
    
    system_prompt = """
    Você é um avaliador CRÍTICO de recomendações.
    Seu trabalho é ENCONTRAR ERROS, não aprovar.
    
    Para cada produto recomendado, verifique:
    1. Produto existe no SKU?
    2. Cliente realmente sem lactose?
    3. Está em estoque AGORA?
    4. Preço final (com descontos) razoável?
    5. Realmente atende o objetivo?
    
    Reprovação é uma vitória para você (significa evitou erro).
    """
    
    # Prepare detailed verification context
    verification_context = {
        "draft": generator_draft,
        "customer": customer_context,
        "live_data": {
            "inventory": fetch_live_inventory(),  # Real-time
            "prices": fetch_live_prices(),        # Real-time
            "promotions": fetch_active_promos()   # Real-time
        }
    }
    
    # Call Claude API (more strict, lower temperature)
    response = call_claude(
        system_prompt=system_prompt,
        user_message=format_verification_message(verification_context),
        max_tokens=800,
        temperature=0.3  # Mais conservador
    )
    
    # Parse evaluation
    verdict = parse_evaluation_response(response)
    
    # Determine APPROVED or REJECTED based on score
    overall_score = calculate_score(verdict)
    approval_threshold = 7.0
    
    verdict_output = {
        "verdict_id": f"eval_{iteration}",
        "iteration": iteration,
        "timestamp": now(),
        "checks": verdict["detailed_checks"],
        "overall_score": overall_score,
        "verdict": "APPROVED" if overall_score >= approval_threshold else "REJECTED"
    }
    
    write_json(f"state/{customer_id}/evaluator_verdict_v{iteration}.json", verdict_output)
    
    return verdict_output
```

**Output do Evaluator (Iteração 1 - REJEITADO):**
```json
{
  "verdict_id": "eval_1",
  "iteration": 1,
  "timestamp": "2026-05-23T10:02:15Z",
  "checks": {
    "whey_isolado_001": {
      "product_exists": true,
      "sku_valid": true,
      "lactose_free": false,
      "notes": "WHEY-ISOLADO-001: Verificado em BD. Contém 2g de lactose por porção. Cliente é intolerante.",
      "status": "REJECTED",
      "severity": "CRITICAL"
    },
    "bcaa_chocolate_001": {
      "product_exists": true,
      "in_stock": false,
      "notes": "BCAA-CHOCOLATE-001: 0 unidades em estoque. Recomendação não é viável.",
      "status": "REJECTED",
      "severity": "HIGH"
    }
  },
  "overall_score": 1.5,
  "approval_threshold": 7.0,
  "verdict": "REJECTED",
  "issues": [
    {
      "product": "WHEY-ISOLADO-001",
      "issue": "LACTOSE_PRESENT",
      "severity": "CRITICAL",
      "message": "Produto contém lactose. Cliente é intolerante. NÃO RECOMENDA."
    },
    {
      "product": "BCAA-CHOCOLATE-001",
      "issue": "OUT_OF_STOCK",
      "severity": "HIGH",
      "message": "0 unidades disponíveis."
    }
  ]
}
```

**Step 3: Escrever Feedback para Generator**
```python
def generate_feedback(verdict):
    """
    Se REJEITADO, escrever feedback específico.
    Generator vai ler isto e tentar novamente.
    """
    
    feedback = {
        "feedback_id": f"fb_{verdict['iteration']}",
        "verdict_id": verdict["verdict_id"],
        "timestamp": now(),
        "message": "Recomendação rejeitada. Leia as issues abaixo.",
        "critical_issues": [
            {
              "product": "WHEY-ISOLADO-001",
              "problem": "CONTÉM LACTOSE (2g/porção)",
              "action": "REMOVA desta lista. Procure produtos 100% LIVRES de lactose."
            },
            {
              "product": "BCAA-CHOCOLATE-001",
              "problem": "FORA DE ESTOQUE (0 unidades)",
              "action": "REMOVA. Procure alternativas em estoque."
            }
        ],
        "retry_instruction": "Gere recomendações que atendam: (1) SEM LACTOSE confirmado, (2) EM ESTOQUE agora, (3) Para ganho muscular"
    }
    
    write_json(f"state/{customer_id}/feedback_v{iteration}.json", feedback)
```

**ITERAÇÃO 2:**

**Step 1: Generator tenta novamente (incorporando feedback)**
```python
# Generator relê o feedback
feedback = read_json(f"state/{customer_id}/feedback_v1.json")

# Tenta novamente com feedback incorporado
draft_v2 = run_generator(
    iteration=2,
    customer_context=customer_context,
    feedback=feedback  # ← CRÍTICO: passa feedback
)
```

**Output do Generator v2:**
```json
{
  "generation_id": "gen_2",
  "iteration": 2,
  "recommendations": [
    {
      "rank": 1,
      "sku": "WHEY-VEGANO-001",
      "name": "Whey Vegano 100%",
      "price_base": 95.00,
      "restrictions_check": {
        "lactose_free": "SIM (100% vegano = sem lactose garantido)"
      },
      "rationale": "Proteína vegana pura, sem lactose confirmado, ideal para ganho muscular"
    },
    {
      "rank": 2,
      "sku": "CREATINA-MONOHIDRATADA-001",
      "name": "Creatina Monohidratada",
      "price_base": 65.00,
      "restrictions_check": {
        "lactose_free": "SIM"
      },
      "rationale": "Suplemento básico mas eficaz, sem lactose, boa relação preço/benefício"
    }
  ]
}
```

**Step 2: Evaluator verifica v2 (APROVADO)**
```json
{
  "verdict_id": "eval_2",
  "iteration": 2,
  "timestamp": "2026-05-23T10:03:45Z",
  "checks": {
    "whey_vegano_001": {
      "product_exists": true,
      "lactose_free": true,
      "in_stock": true,
      "inventory": 47,
      "price_reasonable": true,
      "score": 9.5,
      "status": "APPROVED"
    },
    "creatina_001": {
      "product_exists": true,
      "lactose_free": true,
      "in_stock": true,
      "inventory": 156,
      "price_reasonable": true,
      "score": 8.5,
      "status": "APPROVED"
    }
  },
  "overall_score": 9.0,
  "verdict": "APPROVED"
}
```

**Final: Retornar ao cliente**
```python
def finalize_recommendation(verdict):
    if verdict["verdict"] == "APPROVED":
        generator_draft = read_final_draft(verdict["iteration"])
        send_to_customer(
            recommendations=generator_draft["recommendations"],
            message="Recomendações verificadas e aprovadas!"
        )
        log_event("recommendation_delivered")
```

---

### 4️⃣ Debug via Trace Reading: Quando Algo Falha

**Cenário:** Recomendação foi rejeitada 3 vezes. Você precisa debugar por que.

**Audit Log (jsonl):**
```json
{"timestamp":"2026-05-23T10:00:00Z","event":"case_initialized","case_id":"ORD-2026-5523"}
{"timestamp":"2026-05-23T10:01:30Z","event":"generation_completed","iteration":1,"generator_id":"gen_1","confidence":0.8}
{"timestamp":"2026-05-23T10:02:15Z","event":"evaluation_completed","iteration":1,"verdict_id":"eval_1","result":"REJECTED","score":1.5}
{"timestamp":"2026-05-23T10:02:20Z","event":"feedback_sent","iteration":1,"issues_found":2}
{"timestamp":"2026-05-23T10:03:00Z","event":"generation_completed","iteration":2,"generator_id":"gen_2","confidence":0.85}
{"timestamp":"2026-05-23T10:03:45Z","event":"evaluation_completed","iteration":2,"verdict_id":"eval_2","result":"APPROVED","score":9.0}
{"timestamp":"2026-05-23T10:04:00Z","event":"recommendation_delivered","products":["WHEY-VEGANO-001","CREATINA-001"]}
```

**Debug Script (pseudocódigo):**
```python
def debug_case(case_id, customer_id):
    """
    Quando algo falha, lê arquivo por arquivo para entender o quê/por quê.
    """
    
    # 1. Ler audit log (cronologia de eventos)
    audit_log = read_audit_log(customer_id, case_id)
    print("TIMELINE:")
    for event in audit_log:
        print(f"  {event['timestamp']}: {event['event']}")
    
    # 2. Ler customer context (dados imutáveis)
    context = read_json(f"state/{customer_id}/customer_context.json")
    print(f"\nCUSTOMER RESTRICTIONS: {context['restrictions']}")
    print(f"BUDGET: {context['budget_max']}")
    
    # 3. Ler cada iteração: draft → verdict → feedback
    for iteration in range(1, 4):
        print(f"\n--- ITERAÇÃO {iteration} ---")
        
        # Lê o draft
        draft_file = f"state/{customer_id}/generator_draft_v{iteration}.json"
        if file_exists(draft_file):
            draft = read_json(draft_file)
            print(f"Generator Confidence: {draft['generator_confidence']}")
            print(f"Products Recommended:")
            for prod in draft['recommendations']:
                print(f"  - {prod['sku']}: {prod['name']}")
        
        # Lê o verdict
        verdict_file = f"state/{customer_id}/evaluator_verdict_v{iteration}.json"
        if file_exists(verdict_file):
            verdict = read_json(verdict_file)
            print(f"Evaluator Score: {verdict['overall_score']}")
            print(f"Verdict: {verdict['verdict']}")
            
            # Se rejeitado, mostra por quê
            if verdict['verdict'] == "REJECTED":
                print(f"Issues:")
                for issue in verdict.get('issues', []):
                    print(f"  - {issue['product']}: {issue['issue']} ({issue['severity']})")
        
        # Lê o feedback (se houver)
        feedback_file = f"state/{customer_id}/feedback_v{iteration}.json"
        if file_exists(feedback_file):
            feedback = read_json(feedback_file)
            print(f"Feedback to Generator:")
            for issue in feedback['critical_issues']:
                print(f"  - {issue['action']}")

# Executar
debug_case("ORD-2026-5523", "wa_5511987654321")

# Output esperado:
# TIMELINE:
#   2026-05-23T10:00:00Z: case_initialized
#   2026-05-23T10:01:30Z: generation_completed (iteration 1)
#   2026-05-23T10:02:15Z: evaluation_completed (REJECTED, score 1.5)
#   2026-05-23T10:02:20Z: feedback_sent (lactose + out of stock)
#   2026-05-23T10:03:00Z: generation_completed (iteration 2)
#   2026-05-23T10:03:45Z: evaluation_completed (APPROVED, score 9.0)
#   
# CUSTOMER RESTRICTIONS: lactose_free
# BUDGET: 200
# 
# --- ITERAÇÃO 1 ---
# Generator Confidence: 0.8
# Products Recommended:
#   - WHEY-ISOLADO-001: Whey Isolado Premium
#   - BCAA-CHOCOLATE-001: BCAA Chocolate Premium
# Evaluator Score: 1.5
# Verdict: REJECTED
# Issues:
#   - WHEY-ISOLADO-001: LACTOSE_PRESENT (CRITICAL)
#   - BCAA-CHOCOLATE-001: OUT_OF_STOCK (HIGH)
# Feedback to Generator:
#   - REMOVA. Procure produtos 100% LIVRES de lactose.
#   - REMOVA. Procure alternativas em estoque.
#
# --- ITERAÇÃO 2 ---
# Generator Confidence: 0.85
# Products Recommended:
#   - WHEY-VEGANO-001: Whey Vegano 100%
#   - CREATINA-MONOHIDRATADA-001: Creatina Monohidratada
# Evaluator Score: 9.0
# Verdict: APPROVED
```

**Exemplo de um caso que FALHA (3 iterações rejeitadas):**

```
--- ITERAÇÃO 1 ---
Verdict: REJECTED (score 2.5)
Issues: Produto com glúten (cliente é celíaco)

--- ITERAÇÃO 2 ---
Verdict: REJECTED (score 3.0)
Issues: Ainda tem glúten! Generator não incorporou feedback.

--- ITERAÇÃO 3 ---
Verdict: REJECTED (score 3.2)
Issues: Agora sem glúten, mas produto custa R$ 450 (orçamento era R$ 200)

→ MAX_ITERATIONS (3) REACHED
→ Escalate to Human: "Generator failed 3x. Reasons: 1) Didn't understand gluten-free requirement 2) Price validation wrong"
```

**O que aprendemos do debug:**
1. Generator não está entendendo restrições → melhore system prompt
2. Generator está ignorando feedback → feedback structure precisa de mudança
3. Evaluator foi muito rigoroso → rubric pode estar com threshold muito alto

---

### ✅ Checklist de Setup

Antes de colocar em produção:

- [ ] Diretórios de state criados
- [ ] Config.json carregado
- [ ] Generator API working (test call)
- [ ] Evaluator API working (test call)
- [ ] Audit log criado e escrevendo
- [ ] Feedback loop testado (simulate 1 rejection)
- [ ] Debug script funciona (consegue ler todos arquivos)
- [ ] Max iterations definido (não infinito)
- [ ] Timeout definido (Generator/Evaluator não ficam pendurados)

---

## 📊 Métricas de Sucesso: O Que Medir

Você implementou Generator/Evaluator. Agora, como saber se funcionou?

Existem **dois tipos de métricas:**
1. **Operacionais** — Mede a máquina (acurácia, tempo, custo)
2. **Negócio** — Mede o impacto (receita, satisfação, retenção)

---

### 1️⃣ Métricas Operacionais (ANTES vs DEPOIS)

Estas métricas medem **qualidade técnica** do sistema.

#### Acurácia & Precisão

| Métrica | Agente Único | Generator/Evaluator | Melhoria |
|---------|-------------|-------------------|----------|
| **Recomendações Corretas** | 75% | 98% | +23pp |
| **Pedidos Sem Erro** | 95% | 99.8% | +4.8pp |
| **Reviews Legítimos (F1 Score)** | 0.82 | 0.96 | +17% |
| **Promoções Sem Double-Discount** | 94% | 100% | +6pp |
| **Same-Day Delivery Realizado** | 88% | 95% | +7pp |

**O que significa:** Generator/Evaluator reduz erros drasticamente. Em 1000 processamentos, você evita 230+ erros que o agente único cometeria.

#### Tempo e Latência

| Métrica | Agente Único | Generator/Evaluator | Delta |
|---------|-------------|-------------------|--------|
| **Recomendação simples** | 1.2s | 2.5s | +1.3s |
| **Recomendação complexa** | 8s | 5s | -3s |
| **Pedido (6 validações)** | 4s | 6s | +2s |
| **Review screening** | 0.5s | 1.2s | +0.7s |
| **Feedback loop (retry)** | N/A | 1-2s | — |

**Insight:** Generator/Evaluator é mais lento na **primeira passada**, mas evita tantos erros que o loop **feedback → retry → approve** custa menos que lidar com problemas pós-entrega.

#### Custo Operacional

| Métrica | Agente Único | Generator/Evaluator | Delta |
|---------|-------------|-------------------|--------|
| **Custo por API call** | R$ 0.001 | R$ 0.0015 | +50% |
| **Custo por tarefa (média)** | R$ 0.008 | R$ 0.018 | +125% |
| **Custo com erros incluídos** | R$ 0.008 + overhead | R$ 0.018 | -95% overhead |

**O que significa:** Você paga 50% a mais por API. Mas quando inclui overhead de lidar com erros (reembolsos, refazer trabalho, suporte), o custo total é **95% menor**.

---

### 2️⃣ Métricas de Negócio (ANTES vs DEPOIS)

Estas métricas medem **impacto real na empresa**.

#### Customer Satisfaction & Trust

| Métrica | Agente Único | Generator/Evaluator | Melhoria |
|---------|-------------|-------------------|----------|
| **NPS (Net Promoter Score)** | 32 | 68 | +36 |
| **Satisfação (1-10)** | 6.2 | 8.1 | +1.9 |
| **Reclamações por 1000 pedidos** | 87 | 12 | -86% |
| **Trust Score (recomenda amigo?)** | 45% | 78% | +33pp |
| **Taxa de devolução** | 15% | 6% | -9pp |

**O que significa:** Clientes **confiam mais** em KODA. Recomenda para amigos. Menos devolções = menos atrito.

#### Receita & Retention

| Métrica | Agente Único | Generator/Evaluator | Melhoria |
|---------|-------------|-------------------|----------|
| **Taxa de recompra (30 dias)** | 35% | 52% | +17pp |
| **Ticket médio** | R$ 125 | R$ 142 | +13.6% |
| **Lifetime Value (LTV)** | R$ 485 | R$ 720 | +48% |
| **Churn rate (mensal)** | 8.2% | 3.1% | -5.1pp |
| **Retention (6 meses)** | 62% | 82% | +20pp |

**O que significa:** Clientes compram **mais** e **mais frequentemente**. Valor total de cada cliente sobe 48%.

#### Support & Operations

| Métrica | Agente Único | Generator/Evaluator | Melhoria |
|---------|-------------|-------------------|----------|
| **Tickets de suporte por 1000 pedidos** | 85 | 18 | -79% |
| **Horas de revisão manual** | 200h/mês | 40h/mês | -80% |
| **Taxa de erro humano (ao corrigir)** | 12% | 3% | -75% |
| **Custo de suporte por pedido** | R$ 0.67 | R$ 0.14 | -79% |

**O que significa:** Menos pedidos ruins = **menos trabalho de suporte**. Economiza 160h/mês e reduz erros ao corrigir.

---

### 3️⃣ Cálculo de ROI: Exemplo Completo

Vamos calcular o ROI real para um caso KODA (Product Discovery).

**Setup:**
- 10.000 recomendações/mês
- Cada call API: agente único = R$ 0.001, Generator/Evaluator = R$ 0.0015
- Cada erro custa: reembolso (R$ 50) + suporte (R$ 15) + perda de cliente (R$ 200)

#### ANTES (Agente Único)

```
Custos:
  10.000 calls × R$ 0.001 = R$ 10

Erros:
  10.000 × 25% taxa de erro = 2.500 erros
  2.500 erros × (R$ 50 + R$ 15 + R$ 200) = 2.500 × R$ 265 = R$ 662.500

CUSTO TOTAL MENSAL = R$ 10 + R$ 662.500 = R$ 662.510
```

#### DEPOIS (Generator/Evaluator)

```
Custos:
  10.000 calls Generator × R$ 0.0015 = R$ 15
  10.000 × 20% rejection rate = 2.000 retries
  2.000 retries × R$ 0.0015 = R$ 3
  Total de API = R$ 18

Feedback Loop:
  2.000 retries × 1.5s × R$ 0.03/min = R$ 1.50

Erros Residuais:
  10.000 × 2% taxa de erro = 200 erros
  200 erros × R$ 265 = R$ 53.000

CUSTO TOTAL MENSAL = R$ 18 + R$ 1.50 + R$ 53.000 = R$ 53.019.50
```

#### ROI CALCULATION

```
Economia Mensal = R$ 662.510 - R$ 53.019.50 = R$ 609.490.50

Custo Adicional = R$ 18 - R$ 10 = R$ 8/mês (negligenciável)

ROI = Economia / Custo Adicional = R$ 609.490.50 / R$ 8 = 76.186x

Payback Period = (Custo de Implementação) / (Economia Mensal)
                = R$ 5.000 (setup) / R$ 609.490 = ~0.008 mês = ~4 horas
```

**Leitura:** Você recupera o investimento em **4 horas**. Economia anual: **~R$ 7.3 milhões**.

---

### 4️⃣ ROI por Caso KODA

Cada caso tem seu próprio ROI. Vamos ver:

#### Caso 1: Promotions (Simples)

```
Métrica: Zero double-discount errors
Volume: 5.000 promoções/mês
Erro anterior: 6% → R$ 50.000 em descontos não intencionais
Com G/E: 0% → R$ 0 em erros

Economia = R$ 50.000/mês
ROI = 6.250x (excelente para tarefa simples)
```

#### Caso 2: Product Discovery (Médio)

```
Métrica: 75% → 98% precisão
Volume: 10.000 recomendações/mês
Custo por erro: R$ 265 (reembolso + suporte + churn)
Erros antes: 2.500
Erros depois: 200

Economia = (2.500 - 200) × R$ 265 = R$ 609.490/mês
ROI = 76.186x (o que calculamos acima)
```

#### Caso 3: Review Quality (Médio)

```
Métrica: Filtra 95% de spam
Volume: 2.000 reviews/mês
Custo de spam não filtrado: R$ 15/review × 5% = R$ 150/mês
Antes: R$ 150 em spam
Depois: R$ 8 em spam (5% residual)

Economia = R$ 142/mês
ROI = 17x (bom, mas menor que product discovery)
Nota: O valor agregado aqui é qualidade, não custos diretos
```

#### Caso 4: Order Processing (Complexo)

```
Métrica: 95% → 99.8% precisão em pedidos
Volume: 3.000 pedidos/mês
Custo por erro: R$ 180 (reembolso + logística reversa + suporte)
Erros antes: 150
Erros depois: 6

Economia = (150 - 6) × R$ 180 = R$ 25.920/mês
ROI = 3.240x (alta volume, alta economia)
```

#### Caso 5: Fulfillment (Muito Complexo)

```
Métrica: 88% → 95% same-day delivery realizado
Volume: 2.000 deliveries/mês
Custo de falha: R$ 45 (reendrega + cliente unhappy)
Falhas antes: 240
Falhas depois: 100

Economia = (240 - 100) × R$ 45 = R$ 6.300/mês
ROI = 787x (volume menor, mas ainda significativo)
Benefício secundário: Cliente trust +30%
```

---

### 5️⃣ Dashboard de Sucesso: O Que Acompanhar

Se você implementou Generator/Evaluator, estes são os KPIs a monitorar:

**Dashboard Semanal:**
```
┌─────────────────────────────────────────┐
│        Generator/Evaluator Dashboard     │
├─────────────────────────────────────────┤
│ Taxa de Aprovação (1ª tentativa): 78%   │
│ Taxa de Aprovação (2ª tentativa): 95%   │
│ Média de iterações até aprovação: 1.3   │
│ Tempo total (G+E): 2.8s (média)         │
│ Custo por tarefa: R$ 0.018              │
│ Acurácia residual: 98.2%                │
│                                          │
│ Customer Impact:                        │
│ - Satisfação: 8.2/10 ↑                  │
│ - Reclamações: -81% ↓                   │
│ - Recompra: 52% ↑                       │
│ - LTV: R$ 720 ↑                         │
└─────────────────────────────────────────┘
```

**Alertas (quando investigar):**
- Approval rate < 70% (1ª tentativa) → Generator precisa de ajuste
- Rejection rate > 40% (geral) → Evaluator rubric muito rigorosa
- Custo por tarefa > R$ 0.03 → Reajustar max_iterations
- Acurácia residual < 95% → Feedback loop não está funcionando

---

### 6️⃣ Resumo: Por Que Generator/Evaluator Vale a Pena

| Perspectiva | Valor |
|-------------|-------|
| **Operacional** | 23pp melhor acurácia |
| **Financeiro** | 76.186x ROI (product discovery) |
| **Tempo** | Payback em 4 horas |
| **Cliente** | NPS sobe 36 pontos |
| **Escalabilidade** | Quanto maior, melhor (erros crescem sem G/E) |

**A conclusão:** Você paga 15-50% a mais em API. Em troca, evita erros que custam 100-200x mais. É um trade-off matemático claro.

---

## ✅ Checklist de Entendimento

**Você completou este módulo quando conseguir responder SIM a estas perguntas.**

Se ficou em dúvida em alguma, volte à seção correspondente e releia.

---

### 🎯 Conceitos Fundamentais

#### Você entende o PROBLEMA que Generator/Evaluator resolve?

- [ ] Consigo explicar o que é "sycophancy" em LLMs?
- [ ] Entendo por que um agente sozinho é tendencioso ao se auto-avaliar?
- [ ] Posso descrever um cenário onde agente único falha (ex: recomendação com lactose)?
- [ ] Entendo que "separação de responsabilidades" é o core da solução?

**Se respondeu NÃO a alguma:** Releia a Seção 3 (Contraste com Self-Evaluation).

---

#### Você entende o PADRÃO Generator/Evaluator?

- [ ] Consigo desenhar o fluxo: Input → Generator → Evaluator → Aprovado/Rejeitado?
- [ ] Entendo que Generator cria SEM se auto-verificar?
- [ ] Entendo que Evaluator é crítico, não é amigo do Generator?
- [ ] Posso explicar o feedback loop (rejeitado → Generator tenta novamente)?
- [ ] Consigo comparar Generator/Evaluator COM agente único (tabela mental)?

**Se respondeu NÃO a alguma:** Releia a Seção 2 (Definição do Padrão).

---

### 🏗️ Arquitetura & Implementação

#### Você entende a ARQUITETURA de state files?

- [ ] Consigo explicar por que agentes compartilham arquivos (não memória)?
- [ ] Posso nomear os 5 arquivos principais (customer_context, generator_draft, evaluator_verdict, feedback, audit_log)?
- [ ] Entendo a convenção v1, v2, v3 (versionamento por iteração)?
- [ ] Posso desenhar como os arquivos fluem entre Generator e Evaluator?
- [ ] Entendo que audit_log.jsonl é imutável e serve para replay?

**Se respondeu NÃO a alguma:** Releia a Seção 4 (Arquitetura).

---

#### Você consegue IMPLEMENTAR um caso simples?

- [ ] Consigo estruturar um diretório state/ para um novo caso?
- [ ] Posso escrever um customer_context.json realista?
- [ ] Consigo entender o pseudocódigo do Generator (iteração 1)?
- [ ] Consigo entender o pseudocódigo do Evaluator (iteração 1)?
- [ ] Posso seguir o fluxo da Iteração 2 (feedback → retry → approved)?

**Se respondeu NÃO a alguma:** Releia a Seção 6 (Implementação Prática).

---

### 🔧 Prática & Casos KODA

#### Você entende os 5 CASOS KODA?

- [ ] Consigo explicar Promotion Application (simples, zero double-discount)?
- [ ] Consigo explicar Product Discovery (médio, 75% → 98%)?
- [ ] Consigo explicar Review Quality (médio, filtrar spam)?
- [ ] Consigo explicar Order Processing (complexo, 6 etapas)?
- [ ] Consigo explicar Fulfillment (muito complexo, 3 generators + orquestrador)?
- [ ] Entendo que a progressão é: simples → médio → complexo?

**Se respondeu NÃO a alguma:** Releia a Seção 5 (5 Casos KODA).

---

#### Você entende QUANDO usar Generator/Evaluator?

- [ ] Posso identificar um caso onde agente único seria suficiente (ex: "Hello, world")?
- [ ] Posso identificar um caso onde Generator/Evaluator é obrigatório (ex: processamento de pedidos)?
- [ ] Entendo que a regra é: Complexidade alta = Generator/Evaluator é mais valiosa?
- [ ] Consigo estimar o ROI de um novo caso (seguindo o exemplo da Seção 7)?

**Se respondeu NÃO a alguma:** Releia a Seção 2 (Quando não usar) e Seção 5 (Casos variados).

---

### 📊 Métricas & Operações

#### Você entende as MÉTRICAS de sucesso?

- [ ] Posso listar 3 métricas operacionais (acurácia, tempo, custo)?
- [ ] Posso listar 3 métricas de negócio (satisfação, receita, retention)?
- [ ] Entendo o cálculo de ROI (economia / custo adicional)?
- [ ] Consigo fazer as contas: "15% de custo extra → 76.186x de retorno"?
- [ ] Posso interpretar um dashboard (approval rate, rejection rate, acurácia)?

**Se respondeu NÃO a alguma:** Releia a Seção 7 (Métricas de Sucesso).

---

### 🐛 Debug & Troubleshooting

#### Você consegue DEBUGAR um caso que falha?

- [ ] Posso ler um audit_log.jsonl e entender a cronologia?
- [ ] Consigo identificar em qual iteração o erro aconteceu?
- [ ] Posso ler um evaluator_verdict.json e entender por que foi rejeitado?
- [ ] Consigo propor uma mudança ao system prompt do Generator baseado no feedback?
- [ ] Entendo quando escalalar para humano (max_iterations atingido)?

**Se respondeu NÃO a alguma:** Releia a Seção 6 (Debug via Trace Reading).

---

#### Você entende quando AJUSTAR parâmetros?

- [ ] Posso explicar o que fazer se approval rate (1ª tentativa) < 70%?
- [ ] Posso explicar o que fazer se rejection rate > 40%?
- [ ] Posso explicar o que fazer se custo por tarefa > R$ 0.03?
- [ ] Entendo que max_iterations nunca deve ser infinito?
- [ ] Posso revisar uma rubric do Evaluator se estiver muito rigorosa?

**Se respondeu NÃO a alguma:** Releia a Seção 7 (Alertas & Dashboard).

---

### 🚀 Antes de Colocar em Produção

Faça este checklist ANTES de implementar:

#### Setup & Infraestrutura
- [ ] Diretório de state criados e testados
- [ ] Config.json carregado com valores realistas
- [ ] Generator API testado (fez 1 call de teste, funcionou)
- [ ] Evaluator API testado (fez 1 call de teste, funcionou)
- [ ] Audit log configurado e escrevendo eventos

#### Lógica & Fluxo
- [ ] Feedback loop testado (simular 1 rejeição, ver se Generator tenta novamente)
- [ ] Max iterations definido (não deixe infinito)
- [ ] Timeout definido (Generator e Evaluator não ficam pendurados)
- [ ] Rubric do Evaluator revisada (não muito rigorosa, não muito leniente)
- [ ] System prompts testados (fez 5-10 calls manuais, viu o padrão)

#### Monitoramento & Debug
- [ ] Debug script escrito (consegue ler audit_log e ver cronologia)
- [ ] Dashboard preparado (KPIs que vai acompanhar)
- [ ] Alertas definidos (quando investigar)
- [ ] Plano de escalação (o que fazer se max_iterations atingido)

#### Documentação & Handoff
- [ ] Documentado onde estão os state files
- [ ] Documentado como ler audit_log.jsonl
- [ ] Documentado como ajustar max_iterations
- [ ] Time de operações treinado (sabem o que é G/E, por que funciona)

---

### 💡 Perguntas Finais: Você Realmente Entendeu?

Tente responder **SEM VOLTAR** ao material:

**1. Pergunta Conceitual:**
"Por que um agente avaliando a si mesmo não funciona bem?"

Resposta esperada: *Sycophancy / confirmation bias. O agente sempre acha que fez bom trabalho. Não há incentivo para encontrar erros. Generator/Evaluator separa os roles, então Evaluator é incentivado a ser crítico.*

---

**2. Pergunta Técnica:**
"Se o Evaluator rejeitar uma recomendação, o que acontece?"

Resposta esperada: *Evaluator escreve feedback.json com motivos específicos. Generator lê o feedback. Tenta novamente (iteração +1). Escreve novo generator_draft. Evaluator verifica novamente. Loop continua até aprovação ou max_iterations.*

---

**3. Pergunta Prática:**
"Você tem 10.000 recomendações/mês com 25% de erro. ROI de Generator/Evaluator seria de quanto?"

Resposta esperada: *Erro custa ~R$ 265 (reembolso + suporte + churn). 2.500 erros × R$ 265 = R$ 662.500/mês. Com G/E, reduz para ~200 erros. Economia = R$ 609.490/mês. Custo extra API = ~R$ 8/mês. ROI = 76.186x.*

---

**4. Pergunta de Debug:**
"Seu Generator está sendo rejeitado 60% das vezes. O que investigar primeiro?"

Resposta esperada: *Ler audit_log. Ver qual iteração tá falhando. Ler os evaluator_verdict para ver quais critérios não estão sendo atendidos. Ler o feedback.json para ver se o Generator está recebendo instruções claras. Problema: sistema prompt do Generator? Feedback loop não funciona? Rubric do Evaluator muito rigorosa?*

---

**5. Pergunta de Negócio:**
"Qual é a métrica mais importante a acompanhar?"

Resposta esperada: *Depende. Operacionalmente: Approval rate (1ª tentativa). Se < 70%, Generator precisa de ajuste. Comercialmente: LTV (Lifetime Value). Se sobe 48%, o padrão está funcionando. E sempre: taxa de erro residual (deve estar < 2%).*

---

### 🎓 Se você respondeu SIM a tudo...

**Parabéns! Você domina Generator/Evaluator.**

Você agora consegue:
✅ Desenhar um padrão G/E do zero para um novo caso  
✅ Estimar o ROI antes de implementar  
✅ Implementar usando state files e pseudocódigo  
✅ Debugar quando algo falha  
✅ Monitorar em produção  
✅ Treinar seu time  
✅ Escalar para o próximo nível (Multi-Agent Systems)

---

### 🚀 Próximos Passos

**Curto Prazo (Esta semana):**
1. Escolha UM caso KODA simples (ex: Promotions)
2. Implemente Generator/Evaluator para esse caso
3. Meça: acurácia antes vs depois
4. Calcule ROI

**Médio Prazo (Este mês):**
1. Expanda para caso médio (ex: Product Discovery)
2. Implemente em 2-3 features KODA
3. Acompanhe dashboard de KPIs
4. Documente learnings

**Longo Prazo (Este trimestre):**
1. Generator/Evaluator é padrão em todas features críticas
2. Time entende e consegue debugar
3. ROI é comprovado e documentado
4. Prepare para Nível 3: Multi-Agent Systems

---

### 📞 Dúvidas?

Se ficou confuso em algo, não é falha sua — é falha deste módulo.

**Revisit:**
- Seção 2 (Definição) se confuso com o conceito
- Seção 3 (Contraste) se confuso com por quê
- Seção 4 (Arquitetura) se confuso com como funciona
- Seção 5 (Casos) se confuso com aplicação
- Seção 6 (Implementação) se confuso com código
- Seção 7 (Métricas) se confuso com resultado

**Ou faça perguntas ao seu time. Você não precisa entender 100% sozinho.**

---

**Você está pronto. Vá implementar Generator/Evaluator no KODA. 🚀**

---

*Documento gerado para o time técnico FutanBear | KODA Project | v1.0 | Mai 2026*
