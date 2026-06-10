---
title: "Guia de Análise de Traces: Do Sintoma ao Diagnóstico"
type: curriculum-guide
aliases: []
tags: [curriculo-conteudo, guia-implementacao, traces, debugging, diagnostico, troubleshooting, analise-temporal, causa-raiz, observabilidade, incidentes]
relates-to: ["[[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[curriculum/02-nivel-2-practical-patterns/04-trace-reading|Trace Reading Lesson]]"]
last_updated: 2026-06-10
---
# 🔍 Guia de Análise de Traces: Do Sintoma ao Diagnóstico
## Como Identificar, Diagnosticar e Resolver Problemas em Agentes Através de Trace Reading

**Tempo Estimado:** 90 minutos
**Nível:** Guia Prático de Implementação
**Pré-requisito:** Ter completado `02-nivel-2-practical-patterns/04-trace-reading.md`
**Status:** 🟢 REFERÊNCIA ATIVA - Guia de troubleshooting para engenheiros
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Bug Que Ninguém Conseguia Reproduzir

**Segunda-feira, 9h15. O alerta chegou no canal #koda-critical:**

```
🚨 ALERTA CRÍTICO - KODA Production
┌─────────────────────────────────────────────────────────┐
│ Cliente #8741 reportou recomendação incorreta           │
│ Esperado: Whey Isolado (R$ 120)                        │
│ Recebido: Creatina (R$ 45) - produto completamente      │
│           diferente do solicitado                       │
│                                                         │
│ Conversa durou 3h12min. Múltiplas mudanças de opinião.  │
│ Cliente ameaçou ação judicial.                          │
│                                                         │
│ Impacto: 1 estrela no Reclame Aqui + processo no PROCON │
└─────────────────────────────────────────────────────────┘
```

A engenheira Mariana abriu o trace da conversa. 847 eventos registrados. 3 horas de interação. O cliente mudou de ideia **7 vezes** sobre qual suplemento queria. O Generator produziu **21 recomendações** diferentes ao longo da conversa. O Evaluator aprovou **19 delas**.

O problema? Na decisão final, o Evaluator aprovou uma recomendação que o Generator havia feito **2 horas atrás** — não a mais recente.

Mariana passou **45 minutos** lendo o trace linha por linha até encontrar o momento exato: o campo `generation_id` da recomendação final era `rec-00421`, mas o Generator já estava em `rec-00893`. O Evaluator recebeu o contexto errado porque um filtro de `LIMIT 1` no middleware de passagem de contexto estava pegando a **primeira** recomendação da lista, não a **última**.

O bug era uma linha de código. Encontrá-lo exigiu 45 minutos de análise de trace. **Sem o trace, teria sido impossível.**

---

### O Que Este Guia É (E O Que Não É)

Este guia **não** ensina o que é uma trace ou como estruturá-la — isso está coberto em [`04-trace-reading.md`](../02-nivel-2-practical-patterns/04-trace-reading.md). Aquele módulo é a **teoria**. Este guia é a **prática de campo**.

| Se você quer... | Vá para... |
|---|---|
| Entender o que é uma trace | `04-trace-reading.md` |
| Saber como estruturar traces em JSON | `04-trace-reading.md` |
| **Diagnosticar um bug usando uma trace** | **Este guia** ✅ |
| **Identificar padrões de falha recorrentes** | **Este guia** ✅ |
| **Ter um checklist de troubleshooting** | **Este guia** ✅ |

Este é o guia que você abre **quando algo já quebrou** e você precisa descobrir o quê, onde e por quê.

---

### Como Usar Este Guia

1. **Se você está debugando um incidente agora:** Vá direto para a [Checklist de Troubleshooting](#-checklist-de-troubleshooting).
2. **Se você quer aprender a diagnosticar:** Comece pela [Taxonomia de Padrões de Falha](#-padrões-de-falha-taxonomia-completa).
3. **Se você quer exemplos práticos:** Vá para [Exemplos de Traces Comentados](#-exemplos-de-traces-reais-comentados).
4. **Se você é novo no KODA:** Leia em ordem — cada seção constrói sobre a anterior.

---

## 🎯 Anatomia de um Agent Trace: O Essencial Para Diagnóstico

### Resumo Rápido (Referência)

Para fins de diagnóstico, focamos em 6 áreas da trace (o `04-trace-reading.md` apresenta o schema completo com 7 componentes). Você precisa saber **o que cada área te conta** sobre o problema:

```
TRACE COMPLETA
═══════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────┐
│ 1. HEADER (trace_id, session_id, timestamp)             │
│    → Identidade: QUAL conversa? QUANDO?                 │
├─────────────────────────────────────────────────────────┤
│ 2. INPUT (user_message, intent, entities)               │
│    → Entrada: O que o usuário REALMENTE disse?          │
├─────────────────────────────────────────────────────────┤
│ 3. CONTEXT (history, preferences, constraints)          │
│    → Estado: O que o agente SABIA naquele momento?      │
├─────────────────────────────────────────────────────────┤
│ 4. DECISION (recommendation, action, generation_id)      │
│    → Ação: O que o agente DECIDIU fazer?                │
├─────────────────────────────────────────────────────────┤
│ 5. REASONING (thought_process, confidence, evidence)     │
│    → Lógica: POR QUE o agente tomou essa decisão?       │
├─────────────────────────────────────────────────────────┤
│ 6. EVALUATION (checks, result, mismatch_detection)       │
│    → Validação: O Evaluator CONFIRMOU ou REJEITOU?      │
└─────────────────────────────────────────────────────────┘
```

### O Mapa Mental do Diagnóstico

Quando você abre uma trace para diagnosticar um problema, a primeira pergunta é sempre a mesma:

> **"Qual seção contém a discrepância?"**

A resposta determina sua linha de investigação:

| Se a discrepância está em... | O problema provável é... | Vá para a seção... |
|---|---|---|
| **INPUT** | Mensagem do usuário não foi capturada ou foi mal interpretada | [Input Capture Failure](#padrão-1-input-capture-failure) |
| **CONTEXT** | Agente está operando com informações desatualizadas ou incompletas | [Context Amnesia](#padrão-2-context-amnesia) |
| **DECISION** | Decisão contradiz input ou contexto disponível | [Decision Contradiction](#padrão-3-decision-contradiction) |
| **REASONING** | Raciocínio tem gaps lógicos, confiança baixa, ou passos inconsistentes | [Reasoning Collapse](#padrão-4-reasoning-collapse) |
| **EVALUATION** | Evaluator aprovou algo errado ou rejeitou algo correto | [Evaluation Failure](#padrão-5-evaluation-failure) |
| **MÚLTIPLAS seções** | Falha sistêmica de coordenação | [Coordination Failure](#padrão-6-coordination-failure) |

Guarde esta tabela. É seu ponto de partida para **qualquer** investigação de trace.

---

## 🔍 Padrões de Falha: Taxonomia Completa

Agentes long-running falham de maneiras previsíveis. Após analisar centenas de traces do KODA, identificamos **6 padrões de falha fundamentais** que cobrem 95% dos incidentes reais. (Veja também o [Exemplo 3: O Loop Infinito](#exemplo-3-o-loop-infinito-de-recomendações) para um caso clássico de loop — que se manifesta como Decision Contradiction repetida ou Coordination Failure entre iterações.)

Cada padrão inclui:
- 🔴 **Sintoma:** O que o cliente/usuário observa
- 🔎 **Assinatura na Trace:** O que procurar nos dados
- 🧪 **Teste de Confirmação:** Como confirmar o diagnóstico
- 💊 **Correção Típica:** O que geralmente resolve

---

### Padrão 1: Input Capture Failure

#### 🔴 Sintoma

O agente responde a algo que o usuário **não disse** — ou ignora algo que o usuário **disse claramente**. O cliente sente que "o agente não está me ouvindo".

**Exemplo real KODA:**
```
Cliente: "Quero whey de BAUNILHA, não de chocolate"
KODA:   "Ótimo! Aqui está o Whey Chocolate que você pediu!"
Cliente: "???"
```

#### 🔎 Assinatura na Trace

Compare os campos `input.content` e `input.entities_extracted`:

```json
// TRACE DO PROBLEMA
{
  "input": {
    "content": "Quero whey de BAUNILHA, não de chocolate",
    "entities_extracted": {
      "flavor_preference": "Chocolate",  // ← ERRO! Capturou "chocolate" em vez de "baunilha"
      "negation_detected": false         // ← ERRO! Não detectou a negação "não de chocolate"
    }
  }
}
```

**O que procurar:**
- `entities_extracted` contradiz o texto literal em `input.content`
- Campos de entidade ausentes (ex: `flavor_preference: null` quando o texto menciona sabor)
- `negation_detected: false` quando o texto contém "não", "nunca", "prefiro evitar"
- `intent_detected` incorreto (ex: classifica "reclamação" como "pedido")

#### 🧪 Teste de Confirmação

1. Leia `input.content` — o texto literal que o usuário enviou
2. Leia `input.entities_extracted` — o que o parser extraiu
3. Pergunte: "Se eu lesse APENAS o `entities_extracted`, tomaria a mesma decisão que lendo o `content` original?"
4. Se a resposta for **não**, confirma Input Capture Failure

#### 💊 Correção Típica

- **Parser de entidades:** Adicionar regra de negação ("não quero X" → excluir X das entidades)
- **Intent classifier:** Revisar threshold de confiança para intents ambíguos
- **Input validation:** Adicionar step de verificação que compara `content` original com `entities_extracted` antes de passar adiante

#### 📊 Frequência em KODA

- **Ocorrência:** ~12% dos incidentes de qualidade
- **Gravidade:** Alta (decisão baseada em informação errada)
- **Detectabilidade:** Fácil (basta comparar input.content com entities_extracted)

---

### Padrão 2: Context Amnesia

#### 🔴 Sintoma

O agente "esquece" informações que o cliente forneceu anteriormente na conversa. A resposta é correta para o **momento atual**, mas ignora o **histórico relevante**.

**Exemplo real KODA:**
```
[Minuto 5]  Cliente: "Sou alérgico a glúten"
[Minuto 45] KODA:   "Recomendo Whey Premium (contém glúten)"
[Minuto 46] Cliente: "Você esqueceu que sou alérgico???"
```

#### 🔎 Assinatura na Trace

Compare `context.conversation_history` com `context.current_user_profile`:

```json
// TRACE DO PROBLEMA
{
  "context": {
    "conversation_history": [
      {
        "timestamp": "2026-05-15T14:05:00Z",
        "message": "Sou alérgico a glúten",
        "extracted_constraint": "no_gluten"    // ← HISTÓRICO tem a restrição
      }
    ],
    "current_user_profile": {
      "dietary_restrictions": []               // ← PERFIL atual NÃO tem a restrição!
    }
  },
  "decision": {
    "product_has_gluten": true                 // ← Decisão ignora restrição
  }
}
```

**O que procurar:**
- Informação aparece em `conversation_history` mas **não** está em `current_user_profile`
- `context.flavor_preference_timestamp` é muito antigo (mais de 30 min) comparado ao `decision.timestamp`
- `context.flavor_preference_current` é diferente do que o histórico recente indica
- Campos de constraint (dietary, budget, location) estão vazios quando deveriam estar preenchidos

#### 🧪 Teste de Confirmação

1. Extraia todas as restrições/preferências de `conversation_history` (últimos N eventos)
2. Compare com `current_user_profile`
3. Se há divergência → Context Amnesia confirmada
4. Identifique qual evento do histórico **deveria** ter atualizado o perfil mas não atualizou

#### 💊 Correção Típica

- **State persistence:** Garantir que atualizações de perfil sejam síncronas e imediatas
- **Context window check:** Verificar se a restrição caiu fora da janela de contexto (token budgeting)
- **History compaction:** Se estiver usando compaction, verificar se restrições críticas estão sendo preservadas
- **Forced refresh:** Adicionar step que re-valida `current_user_profile` antes de decisões críticas

#### 📊 Frequência em KODA

- **Ocorrência:** ~28% dos incidentes de qualidade (o MAIS COMUM)
- **Gravidade:** Crítica (pode causar dano físico ao cliente — alergias)
- **Detectabilidade:** Moderada (requer correlação entre histórico e perfil)

---

### Padrão 3: Decision Contradiction

#### 🔴 Sintoma

O agente toma uma decisão que contradiz diretamente o contexto disponível ou decisões anteriores. Diferente de Context Amnesia (onde a informação foi perdida), aqui a informação **está presente** mas a decisão a **ignora**.

**Exemplo real KODA:**
```
Contexto:       "Cliente quer vegano, budget R$ 100"
Decisão:         Recomendar Whey (não-vegano, R$ 150)
Contexto estava: CORRETO e ATUALIZADO
```

#### 🔎 Assinatura na Trace

A decisão viola constraints que estão **explicitamente presentes** no contexto:

```json
// TRACE DO PROBLEMA
{
  "context": {
    "current_user_profile": {
      "dietary_restrictions": ["vegan"],    // ← CONTEXTO DIZ: vegano
      "budget_max": 100.00                   // ← CONTEXTO DIZ: máximo R$ 100
    }
  },
  "decision": {
    "product_name": "Whey Premium",
    "product_vegan": false,                  // ← DECISÃO: não-vegano!
    "price": 150.00                          // ← DECISÃO: acima do budget!
  },
  "reasoning": {
    "thought_process": [
      {
        "step": 1,
        "reasoning": "Cliente quer proteína de qualidade"  // ← Ignorou restrições!
      }
    ]
  }
}
```

**O que procurar:**
- `decision.price > context.current_user_profile.budget_max`
- `decision.product_vegan == false` quando `dietary_restrictions` contém "vegan"
- `decision.flavor != context.flavor_preference_current`
- O `reasoning` não menciona as constraints violadas (sinal de que o modelo as ignorou)

#### 🧪 Teste de Confirmação

1. Liste todas as constraints em `context.current_user_profile`
2. Para cada constraint, verifique se a `decision` a respeita
3. Se N constraints foram violadas → Decision Contradiction de gravidade N
4. Leia o `reasoning` — se as constraints não são mencionadas, é **cegueira seletiva do modelo**

#### 💊 Correção Típica

- **Prompt injection:** Injetar constraints como REQUISITOS (não sugestões) no prompt do Generator
- **Pre-decision validation:** Validar constraints ANTES de gerar a decisão (pré-filtro)
- **Decision structure enforcement:** Estruturar o output da decisão para incluir campos de compliance explícitos
- **Temperature reduction:** Reduzir temperatura do modelo para decisões com constraints rígidas

#### 📊 Frequência em KODA

- **Ocorrência:** ~18% dos incidentes de qualidade
- **Gravidade:** Alta (decisão ativamente errada, não por falta de informação)
- **Detectabilidade:** Fácil (comparação direta de campos)

---

### Padrão 4: Reasoning Collapse

#### 🔴 Sintoma

O agente produz uma decisão razoável, mas o raciocínio por trás dela é frágil, circular ou contraditório. A decisão "funciona por sorte", mas não é confiável.

**Exemplo real KODA:**
```
Reasoning: "Recomendo X porque é bom. É bom porque tem qualidade. 
           Tem qualidade porque é bom." [raciocínio circular]
           
Decision: Produto X (que por coincidência era o correto)
```

#### 🔎 Assinatura na Trace

Analise a estrutura do `reasoning.thought_process`:

```json
// TRACE DO PROBLEMA
{
  "reasoning": {
    "thought_process": [
      {
        "step": 1,
        "reasoning": "Cliente quer whey protein"
      },
      {
        "step": 2,
        "reasoning": "Whey protein é bom para músculos"      // ← Irrelevante
      },
      {
        "step": 3,
        "reasoning": "Vou recomendar o mais popular"          // ← Não usa preferências
      }
    ],
    "confidence_score": 0.42,                                  // ← BAIXA confiança
    "evidence_used": []                                        // ← NENHUMA evidência
  }
}
```

**O que procurar:**
- `confidence_score < 0.6` — o modelo não está confiante na própria decisão
- `thought_process` com passos circulares (step N referencia step N-1 sem adicionar informação)
- `thought_process` ignorando constraints críticas (não menciona budget, dietary, preference)
- `evidence_used` vazio quando deveria citar dados do catálogo ou perfil
- `thought_process` com saltos lógicos (ex: "Cliente quer X, logo recomendo Y" sem explicar por que Y)

#### 🧪 Teste de Confirmação

1. Leia cada step do `thought_process` em sequência
2. Pergunte para cada step: "Este step adiciona informação nova ou apenas repete o anterior?"
3. Verifique `confidence_score` — se < 0.6, a decisão é frágil
4. Verifique se os passos mencionam TODAS as constraints relevantes
5. Se 2+ passos são redundantes ou irrelevantes → Reasoning Collapse

#### 💊 Correção Típica

- **Chain-of-thought prompting:** Forçar o modelo a explicitar cada passo de raciocínio
- **Evidence requirements:** Exigir que o modelo cite evidência específica para cada afirmação
- **Confidence threshold:** Rejeitar decisões com confidence < 0.7 e re-gerar
- **Reasoning validation:** Adicionar Evaluator check específico para qualidade do reasoning
- **Structured reasoning:** Usar template de reasoning (Observation → Analysis → Conclusion)

#### 📊 Frequência em KODA

- **Ocorrência:** ~15% dos incidentes de qualidade
- **Gravidade:** Moderada (decisão pode estar correta, mas não é reproduzível)
- **Detectabilidade:** Difícil (requer análise qualitativa do reasoning)

---

### Padrão 5: Evaluation Failure

#### 🔴 Sintoma

O Evaluator aprova uma recomendação que deveria ter sido rejeitada, ou rejeita uma recomendação que estava correta. O gatekeeper falhou.

**Exemplo real KODA:**
```
Generator: Recomendou Whey Chocolate (CORRETO)
Evaluator: ❌ REJEITOU — "Cliente prefere Baunilha" (preferência ANTIGA)
Resultado: Cliente não recebeu recomendação nenhuma
```

#### 🔎 Assinatura na Trace

Compare `decision` (Generator output) com `evaluation.recommendation_received`:

```json
// TRACE DO PROBLEMA - Caso A: Evaluator rejeitou corretamente
// mas por motivo errado (usou contexto antigo)
{
  "decision": {
    "generation_id": "rec-00893",
    "product_name": "Whey Chocolate",
    "flavor": "Chocolate"
  },
  "evaluation": {
    "recommendation_received": {
      "generation_id": "rec-00893",       // ← Mesmo ID (OK - recebeu a certa)
      "product_name": "Whey Chocolate"
    },
    "evaluation_result": "REJECTED",
    "rejection_reason": "Client prefers Baunilha, not Chocolate",  // ← ERRO!
    "context_used_for_evaluation": {
      "flavor_preference": "Baunilha",    // ← Context ANTIGO!
      "flavor_preference_timestamp": "2026-05-15T12:00:00Z" // ← 2h atrás!
    }
  }
}

// TRACE DO PROBLEMA - Caso B: Gen/Eval Mismatch
{
  "decision": {
    "generation_id": "rec-00893",         // Generator criou ESTA
    "product_name": "Whey Chocolate"
  },
  "evaluation": {
    "recommendation_received": {
      "generation_id": "rec-00421",       // ← ID DIFERENTE! Recebeu OUTRA!
      "product_name": "Creatina"
    },
    "evaluation_result": "APPROVED"       // ← Aprovou a errada!
  }
}
```

**O que procurar:**
- `decision.generation_id != evaluation.recommendation_received.generation_id` → Gen/Eval Mismatch
- `evaluation.evaluation_result == "APPROVED"` mas a decisão viola constraints óbvias
- `evaluation.evaluation_result == "REJECTED"` mas a decisão está claramente correta
- `evaluation.checks_performed` está incompleto (faltam checks críticos)
- `evaluation.context_used_for_evaluation` tem timestamp muito diferente de `decision.timestamp`

#### 🧪 Teste de Confirmação

1. Compare `generation_id` do Generator com o do Evaluator — se diferentes, é Mismatch
2. Se iguais, verifique `context_used_for_evaluation` — está atualizado?
3. Leia `rejection_reason` ou `checks_performed` — fazem sentido lógico?
4. Simule mentalmente: "Se EU lesse os checks, aprovaria/rejeitaria da mesma forma?"

#### 💊 Correção Típica

- **ID tracking:** Garantir que a `generation_id` é propagada corretamente entre Generator e Evaluator
- **Context freshness:** Evaluator deve receber contexto com timestamp <= 1 minuto do `decision.timestamp`
- **Rubric validation:** Revisar a rubrica do Evaluator — está atualizada? Cobre todos os casos?
- **Dual evaluation:** Rodar Evaluator 2x com parâmetros ligeiramente diferentes e comparar resultados

#### 📊 Frequência em KODA

- **Ocorrência:** ~22% dos incidentes de qualidade (o SEGUNDO mais comum)
- **Gravidade:** Crítica (o gatekeeper falhou — tudo que vem depois está comprometido)
- **Detectabilidade:** Moderada (requer comparação de IDs e timestamps)

---

### Padrão 6: Coordination Failure

#### 🔴 Sintoma

Múltiplos componentes do sistema estão individualmente corretos, mas a **interação entre eles** produz um resultado errado. É o padrão mais difícil de diagnosticar porque cada peça, isoladamente, parece funcionar.

**Exemplo real KODA:**
```
Generator 1 (Sprint 1): "Cliente quer whey. Budget: R$ 100"
Generator 2 (Sprint 2): "Recomendo Whey Elite R$ 150" [VIOLOU budget]
Evaluator (Sprint 2):   "Budget check: R$ 150 <= R$ 100? NÃO! REJEITADO!"
Evaluator (Sprint 1):   "Budget definido como R$ 100. OK!"

Problema real: O budget foi atualizado entre Sprints
mas o Evaluator do Sprint 2 não recebeu a atualização.
```

#### 🔎 Assinatura na Trace

Este padrão se manifesta como **inconsistências entre múltiplas traces** (não dentro de uma única trace):

```json
// TRACE DO SPRINT 1
{
  "trace_id": "trace-sprint1-001",
  "phase": { "sprint_number": 1 },
  "context": {
    "sprint_contract": {
      "contract_id": "contract-001",
      "max_budget": 100.00,
      "version": 1
    }
  }
}

// TRACE DO SPRINT 2
{
  "trace_id": "trace-sprint2-001",
  "phase": { "sprint_number": 2 },
  "context": {
    "sprint_contract": {
      "contract_id": "contract-001",
      "max_budget": 150.00,    // ← Orçamento MUDOU entre sprints
      "version": 2             // ← Versão diferente
    }
  },
  "evaluation": {
    "checks_performed": [
      {
        "check": "budget_compliance",
        "contract_version_used": 1,    // ← Avaliador usou versão ANTIGA!
        "max_budget_checked": 100.00
      }
    ]
  }
}
```

**O que procurar:**
- `sprint_contract.version` difere entre traces do mesmo `contract_id`
- `evaluation.checks_performed[].contract_version_used` é diferente do `sprint_contract.version` atual
- Timestamps mostram que eventos em sprints diferentes estão fora de ordem cronológica
- `context.flavor_preference_timestamp` em Sprint 2 é MAIS ANTIGO que em Sprint 1 (deveria ser mais recente ou igual)
- Diferentes componentes do sistema discordam sobre o estado atual

#### 🧪 Teste de Confirmação

1. Colete TODAS as traces da mesma `session_id`, ordenadas por timestamp
2. Para cada campo de estado (budget, preference, restrictions), trace sua evolução temporal
3. Identifique momentos onde o valor muda em uma trace mas outras traces ainda usam o valor antigo
4. Se há defasagem temporal > 1 minuto entre mudança e propagação → Coordination Failure

#### 💊 Correção Típica

- **Event sourcing:** Usar event store centralizado em vez de estado distribuído
- **Contract versioning:** Cada componente deve verificar `contract_version` antes de usar
- **State propagation guarantee:** Garantir que mudanças de estado são propagadas em < 1s
- **Cross-sprint validation:** Adicionar checkpoint entre sprints que valida consistência de estado
- **Distributed trace ID:** Usar `trace_id` + `parent_trace_id` para rastrear cadeias de decisão

#### 📊 Frequência em KODA

- **Ocorrência:** ~5% dos incidentes de qualidade
- **Gravidade:** Crítica (difícil de detectar, fácil de causar danos em cascata)
- **Detectabilidade:** Muito difícil (requer análise cross-trace)

---

### 📊 Tabela Resumo dos Padrões de Falha

| Padrão | Frequência | Gravidade | Detectabilidade | Tempo Médio de Diagnóstico |
|---|---|---|---|---|
| Input Capture Failure | 12% | Alta | Fácil | 5 min |
| Context Amnesia | 28% | Crítica | Moderada | 15 min |
| Decision Contradiction | 18% | Alta | Fácil | 5 min |
| Reasoning Collapse | 15% | Moderada | Difícil | 20 min |
| Evaluation Failure | 22% | Crítica | Moderada | 10 min |
| Coordination Failure | 5% | Crítica | Muito Difícil | 45 min |

---

## 🛠️ Técnicas de Diagnóstico

Dominar a taxonomia de falhas é o primeiro passo. Agora você precisa das **técnicas** para aplicar esse conhecimento em traces reais.

---

### Técnica 1: Análise Temporal (Timeline Reconstruction)

#### Quando Usar

Sempre. É a primeira técnica a aplicar em qualquer investigação.

#### Como Fazer

1. Extraia todos os timestamps da trace
2. Ordene eventos cronologicamente
3. Identifique gaps, inversões e anomalias temporais

```
RECONSTRUÇÃO TEMPORAL
═══════════════════════════════════════════════════════════

14:05:00  [INPUT]   Cliente: "Sou alérgico a glúten"
14:05:02  [CONTEXT] dietary_restrictions atualizado: ["no_gluten"]
14:05:05  [DECISION] Generator: Whey Sem Glúten (CORRETO)
14:05:08  [EVAL]    Evaluator: APPROVED
          ─────────────────────────────────────────────────
14:32:00  [INPUT]   Cliente: "Mudei de ideia, quero o mais barato"
14:32:01  [CONTEXT] budget_priority: "lowest_price"
          ⚠️ GAP: dietary_restrictions NÃO foi reafirmado!
14:32:05  [DECISION] Generator: Whey Mais Barato (contém glúten!)
                     ERRO: priorizou preço sobre restrição alimentar
14:32:08  [EVAL]    Evaluator: APPROVED (não checou dietary!)
          ─────────────────────────────────────────────────
14:32:10  [OUTPUT]  Cliente recebe recomendação com glúten
```

#### O Que Procurar

- **Gaps temporais:** Intervalos > 30 segundos entre input e decisão (possível processamento assíncrono com race condition)
- **Inversões:** `decision.timestamp < input.timestamp` (bug de ordenação)
- **Timestamps idênticos:** Múltiplos eventos com mesmo timestamp até o milissegundo (possível batch processing)

---

### Técnica 2: Rastreamento de Fluxo de Dados (Data Lineage)

#### Quando Usar

Quando você suspeita que uma informação foi perdida, corrompida ou transformada entre componentes.

#### Como Fazer

1. Escolha um dado crítico (ex: `flavor_preference`)
2. Siga seu caminho através de cada seção da trace
3. Identifique exatamente ONDE o valor muda

```
DATA LINEAGE: flavor_preference
═══════════════════════════════════════════════════════════

[INPUT]       content: "quero chocolate"
              entities_extracted.flavor_preference: "Chocolate"  ✅
                  ↓
[CONTEXT]     current_user_profile.flavor_preference_current: "Chocolate"  ✅
              flavor_preference_timestamp: 14:37:00Z
                  ↓
[DECISION]    Generator usou: "Chocolate"  ✅
              decision.flavor: "Chocolate"  ✅
              generation_id: "rec-00893"
                  ↓
[EVALUATION]  recommendation_received.generation_id: "rec-00421"  ❌ MISMATCH!
              recommendation_received.flavor: "Morango"  ❌ DADO CORROMPIDO!
              
              DIAGNÓSTICO: Entre DECISION e EVALUATION, o generation_id
              foi trocado. O Evaluator recebeu uma recomendação diferente
              da que o Generator produziu.
```

#### O Que Procurar

- **Transformação inesperada:** Valor muda de tipo ou formato sem explicação
- **Queda silenciosa:** Campo existe no CONTEXT mas desaparece no DECISION
- **Adição espúria:** Campo aparece no DECISION que não existia no CONTEXT (alucinação)
- **Desvio de referência:** `generation_id` muda entre componentes (o dado certo foi perdido e outro foi usado)

---

### Técnica 3: Correlação de Gerações (ID Tracking)

#### Quando Usar

Especificamente para diagnosticar Evaluation Failures e Coordination Failures.

#### Como Fazer

1. Extraia `generation_id` de cada decisão do Generator
2. Extraia `generation_id` recebido pelo Evaluator
3. Compare — se diferentes, há um bug de roteamento

```
ID TRACKING MATRIX
═══════════════════════════════════════════════════════════

Generator Decision ID    →    Evaluator Received ID    →    Match?
─────────────────────────────────────────────────────────────
rec-00891 (Baunilha)          rec-00891 (Baunilha)          ✅
rec-00892 (Chocolate)         rec-00892 (Chocolate)         ✅
rec-00893 (Morango)           rec-00421 (Creatina)          ❌ MISMATCH
rec-00894 (Whey)              rec-00894 (Whey)              ✅

Diagnóstico: Na terceira geração, o Evaluator recebeu um ID de uma
geração COMPLETAMENTE DIFERENTE (rec-00421 é de 2 horas atrás).
```

#### Checklist de ID Tracking

- [ ] Todo `decision.generation_id` tem um correspondente em `evaluation.recommendation_received.generation_id`
- [ ] IDs são únicos por sessão (não se repetem)
- [ ] IDs são sequenciais (ou timestamp-based) — IDs fora de ordem indicam processamento assíncrono bugado
- [ ] O `generation_id` no `evaluation.recommendation_received` NUNCA é mais antigo que o `generation_id` no `decision`

---

### Técnica 4: Verificação de Contratos (Contract Compliance)

#### Quando Usar

Quando há suspeita de violação de Sprint Contract, budget, ou restrições declaradas.

#### Como Fazer

1. Extraia o `sprint_contract` da trace (ou do `context.phase.sprint_contract`)
2. Extraia a `decision`
3. Compare cada termo do contrato com a decisão

```
CONTRACT COMPLIANCE CHECK
═══════════════════════════════════════════════════════════

CONTRACT (Sprint 1):
  contract_id: "contract-001"
  version: 2
  max_budget: 100.00
  constraints: ["only_vegan", "muscle_gain_goal"]
  duration_minutes: 10

DECISION:
  product_name: "Whey Premium"
  price: 150.00           ← ❌ VIOLA max_budget (150 > 100)
  product_vegan: false    ← ❌ VIOLA only_vegan
  product_goal: "muscle_gain"  ← ✅ Atende muscle_gain_goal

COMPLIANCE SCORE: 1/3 (33%)  ← APENAS 1 de 3 constraints atendidas
```

#### Checklist de Contract Compliance

- [ ] `decision.price <= sprint_contract.max_budget`
- [ ] `decision.product_vegan == true` (se `only_vegan` em constraints)
- [ ] `decision.product_gluten_free == true` (se `no_gluten` em constraints)
- [ ] `decision.timestamp - sprint_start_timestamp <= sprint_contract.duration_minutes`
- [ ] `evaluation.contract_version_used == sprint_contract.version`

---

### Técnica 5: Análise de Confiança (Confidence Profiling)

#### Quando Usar

Para identificar decisões frágeis que o modelo tomou com baixa confiança — estas são as mais propensas a erro.

#### Como Fazer

1. Extraia `confidence_score` de todas as decisões na sessão
2. Identifique decisões abaixo do threshold de segurança (tipicamente < 0.7)
3. Analise o `reasoning` dessas decisões de baixa confiança

```
CONFIDENCE PROFILE DA SESSÃO
═══════════════════════════════════════════════════════════

Decisão    Timestamp   Confidence   Produto                Status
─────────────────────────────────────────────────────────────
rec-001    14:05       0.92         Whey Baunilha          ✅
rec-002    14:12       0.88         Creatina               ✅
rec-003    14:18       0.45 ⚠️      Whey Chocolate         ⚠️ BAIXA
rec-004    14:25       0.91         Whey Morango           ✅
rec-005    14:32       0.38 ⚠️      Whey Mais Barato       ⚠️ BAIXA
rec-006    14:40       0.87         Whey Isolado           ✅
rec-007    14:48       0.51 ⚠️      Creatina (alternativa) ⚠️ BAIXA

Decisões com baixa confiança: rec-003, rec-005, rec-007 (3 de 7 = 43%)
⚠️ ALERTA: 43% das decisões nesta sessão foram tomadas com baixa confiança.
```

#### Interpretação

- **Confiança < 0.5:** Decisão essencialmente aleatória — NUNCA deve ser aprovada pelo Evaluator
- **Confiança 0.5-0.7:** Decisão incerta — requer verificação adicional
- **Confiança 0.7-0.85:** Decisão moderadamente confiável — aceitável com Evaluator check
- **Confiança > 0.85:** Decisão confiante — baixo risco de erro

---

### Técnica 6: Diff de Decisões (Decision Comparison)

#### Quando Usar

Quando o agente tomou múltiplas decisões sobre o mesmo tópico e você precisa entender por que a decisão final foi diferente.

#### Como Fazer

1. Agrupe decisões pelo `intent` ou tópico
2. Compare `decision`, `context`, e `reasoning` entre a primeira e a última decisão do grupo
3. Identifique o que MUDOU entre elas (e se a mudança foi legítima)

```
DECISION DIFF: Recomendações de Whey
═══════════════════════════════════════════════════════════

DECISÃO 1 (14:05)                  DECISÃO 5 (14:32)
─────────────────────────────────────────────────────────
Produto: Whey Baunilha             Produto: Whey Mais Barato
Preço: R$ 89.90                   Preço: R$ 49.90
Motivo: "Sabor preferido"          Motivo: "Mais barato"
Budget: R$ 100                     Budget: R$ 100
Restrições: no_gluten              Restrições: (não verificadas) ← PERDA!
Confiança: 0.92                    Confiança: 0.38 ← QUEDA!

DIAGNÓSTICO: Entre a decisão 1 e a decisão 5, as restrições
alimentares foram PERDIDAS do contexto. O agente passou a
otimizar apenas por preço, ignorando a alergia ao glúten.
```

---

## 📊 Tabela Comparativa: Estratégias de Diagnóstico

Existem três abordagens fundamentais para diagnosticar problemas em agentes. Cada uma tem seu lugar.

| Dimensão | 🔍 **Diagnóstico Manual** | 🤖 **Diagnóstico Automatizado** | 🔄 **Diagnóstico Híbrido** |
|---|---|---|---|
| **Descrição** | Engenheiro lê traces linha por linha, aplica técnicas manualmente | Scripts/ferramentas analisam traces automaticamente e geram relatórios | Automação faz primeira passagem; engenheiro revisa alertas e decide |
| **Ferramentas** | Editor de JSON, `jq`, grep, planilha | `trace_analyzer.py`, sistemas de alerta, dashboards | Pipeline: script → alerta → investigação manual |
| **Tempo por trace** | 15-45 minutos | < 1 segundo | 2-5 minutos (só traces com alertas) |
| **Precisão** | Alta (humano entende contexto) | Média (script detecta padrões, não nuance) | Alta (script + humano) |
| **Cobertura** | Baixa (máx 20 traces/dia) | Alta (100% das traces) | Alta (100% com revisão seletiva) |
| **Detecta padrões sutis?** | ✅ Sim (ex: reasoning circular) | ❌ Não (requer compreensão semântica) | ✅ Sim (humano nos casos difíceis) |
| **Detecta violações óbvias?** | ✅ Sim (mas lento) | ✅ Sim (ideal para isso) | ✅ Sim |
| **Escalabilidade** | ❌ Não escala | ✅ Escala infinitamente | ✅ Escala bem |
| **Custo operacional** | Alto (horas de engenharia) | Baixo (custo de computação) | Médio |
| **Ideal para...** | Incidentes críticos, debugs complexos | Monitoramento contínuo, alertas automáticos | Operação diária do KODA |
| **Setup inicial** | Nenhum | 2-4 semanas para desenvolver scripts | 3-6 semanas (scripts + processos) |
| **Manutenção** | Nenhuma | Contínua (atualizar regras) | Contínua (moderada) |

### Quando Usar Cada Estratégia

```
Fluxo de Decisão: Qual Estratégia Usar?
═══════════════════════════════════════════════════════════

Nova trace chegou
    │
    ├─→ É incidente crítico? (cliente reclamou, PROCON)
    │       └─→ SIM: Diagnóstico MANUAL + HÍBRIDO
    │              (Humano lidera, script auxilia)
    │
    ├─→ É monitoramento de rotina? (100+ traces/dia)
    │       └─→ SIM: Diagnóstico AUTOMATIZADO
    │              (Script analisa, só alerta exceções)
    │
    └─→ É investigação de padrão? (entender recorrência)
            └─→ SIM: Diagnóstico HÍBRIDO
                   (Script agrupa padrões, humano interpreta)
```

---

## 🏥 Exemplos de Traces Reais Comentados

Esta seção apresenta **4 exemplos completos** de traces com análise passo a passo — incluindo uma trace saudável (Exemplo 1) para você aprender a reconhecer quando uma trace está CORRETA, além de três traces com problemas reais. Para cada exemplo, você verá a trace, o diagnóstico e a correção aplicada (quando houver).

---

### Exemplo 1: O Caso do Sabor Fantasma

#### Contexto

Cliente interagiu com KODA por 2h15min. No final, reclamou que o produto recomendado não correspondia ao sabor que ele havia pedido.

#### Trace (Simplificada)

```json
{
  "trace_id": "trace-exemplo-1",
  "session_id": "session-9921",
  "timestamp": "2026-05-20T16:45:00Z",

  "input": {
    "timestamp": "2026-05-20T16:42:00Z",
    "content": "Então, qual você recomenda? Lembra que eu falei que prefiro morango?",
    "intent_detected": "recommendation_request",
    "entities_extracted": {
      "flavor_preference": "Morango"
    }
  },

  "context": {
    "conversation_history": [
      {
        "timestamp": "2026-05-20T14:30:00Z",
        "message": "prefiro chocolate",
        "extracted_preference": { "flavor": "Chocolate" }
      },
      {
        "timestamp": "2026-05-20T15:45:00Z",
        "message": "mudei de ideia, quero baunilha",
        "extracted_preference": { "flavor": "Baunilha" }
      }
    ],
    "current_user_profile": {
      "flavor_preference_current": "Baunilha",
      "flavor_preference_timestamp": "2026-05-20T15:45:00Z"
    }
  },

  "decision": {
    "generation_id": "rec-5521",
    "timestamp": "2026-05-20T16:42:05Z",
    "product_name": "Whey Baunilha Premium",
    "flavor": "Baunilha",
    "price": 89.90,
    "decision_status": "FINAL"
  },

  "reasoning": {
    "thought_process": [
      {
        "step": 1,
        "reasoning": "Cliente pergunta sobre recomendação e menciona 'morango', mas perfil indica preferência atual é Baunilha (atualizado em 15:45)"
      },
      {
        "step": 2,
        "reasoning": "A menção a 'morango' parece ser referência ao que ele 'falou' antes, não uma nova preferência. A frase 'Lembra que eu falei' sugere isso."
      },
      {
        "step": 3,
        "reasoning": "Recomendação correta: Baunilha (preferência atual), não Morango (preferência antiga mencionada de passagem)"
      }
    ],
    "confidence_score": 0.89
  },

  "evaluation": {
    "recommendation_received": {
      "generation_id": "rec-5521",
      "product_name": "Whey Baunilha Premium"
    },
    "evaluation_result": "APPROVED",
    "checks_performed": [
      { "check": "flavor_match", "result": "PASS" },
      { "check": "budget_compliance", "result": "PASS" },
      { "check": "dietary_compliance", "result": "PASS" }
    ]
  }
}
```

#### Análise

```
DIAGNÓSTICO DO EXEMPLO 1
═══════════════════════════════════════════════════════════

PASSO 1: Input Capture
├─ input.content: "prefiro morango?" (em tom de pergunta/confirmação)
├─ entities_extracted.flavor_preference: "Morango"
└─ ⚠️ ALERTA: Parser extraiu "Morango" de uma PERGUNTA, não de uma afirmação

PASSO 2: Context Check
├─ current_user_profile.flavor_preference_current: "Baunilha"
├─ context.flavor_preference_timestamp: 15:45 (1 hora atrás)
└─ ✅ Context está correto (Baunilha é a preferência atual)

PASSO 3: Decision Check
├─ decision.flavor: "Baunilha"
├─ generation_id: "rec-5521"
└─ ✅ Decisão usou preferência correta (Baunilha, não Morango)

PASSO 4: Reasoning Check
├─ reasoning mostra que o modelo ENTENDEU que "morango" era referência antiga
├─ confidence_score: 0.89 (alta)
└─ ✅ Raciocínio sólido

PASSO 5: Evaluation Check
├─ generation_id match: ✅
├─ checks_performed: flavor_match ✅, budget ✅, dietary ✅
└─ ✅ Evaluator aprovou corretamente

VEREDITO FINAL: ✅ ESTA TRACE ESTÁ CORRETA!
O agente interpretou corretamente que "morango" era uma referência
à preferência antiga, não uma nova preferência.
```

#### Lição

**Nem toda menção a uma preferência é uma mudança de preferência.** O contexto da frase ("Lembra que eu falei...") é crucial. Este exemplo mostra como um parser ingênuo teria extraído "Morango" e causado um erro — mas o raciocínio do modelo evitou isso.

---

### Exemplo 2: O Budget Que Desapareceu

#### Contexto

Cliente definiu budget de R$ 80 no início da conversa. Após 90 minutos, KODA recomendou produto de R$ 120. Cliente reclamou.

#### Trace (Trechos Relevantes)

**Trace do Momento 1 (14:00) — Definição do Budget:**

```json
{
  "trace_id": "trace-exemplo-2a",
  "timestamp": "2026-05-20T14:00:00Z",
  "input": {
    "content": "Meu orçamento é R$ 80, não posso passar disso",
    "entities_extracted": { "budget_max": 80.00 }
  },
  "context": {
    "current_user_profile": {
      "budget_max": 80.00,
      "budget_set_timestamp": "2026-05-20T14:00:00Z"
    }
  }
}
```

**Trace do Momento 2 (15:30) — Recomendação Final:**

```json
{
  "trace_id": "trace-exemplo-2b",
  "timestamp": "2026-05-20T15:30:00Z",
  "input": {
    "content": "Qual o melhor whey que você tem?",
    "entities_extracted": {}
  },
  "context": {
    "current_user_profile": {
      "budget_max": null,
      "budget_set_timestamp": null
    },
    "conversation_history": []
  },
  "decision": {
    "generation_id": "rec-7734",
    "product_name": "Whey Elite",
    "price": 120.00,
    "decision_status": "FINAL"
  },
  "reasoning": {
    "thought_process": [
      { "step": 1, "reasoning": "Cliente quer o melhor whey. Sem restrição de orçamento definida." }
    ],
    "confidence_score": 0.91
  }
}
```

#### Análise

```
DIAGNÓSTICO DO EXEMPLO 2
═══════════════════════════════════════════════════════════

PASSO 1: Comparação Temporal
├─ Trace A (14:00): budget_max = R$ 80 ✅
├─ Trace B (15:30): budget_max = null ❌
└─ GAP: 90 minutos entre as traces

PASSO 2: Context Check (Trace B)
├─ current_user_profile.budget_max: null ❌
├─ conversation_history: [] (VAZIO!) ❌
└─ ⚠️ ALERTA CRÍTICO: Contexto completamente perdido!

PASSO 3: Investigação da Causa
├─ O que aconteceu entre 14:00 e 15:30?
├─ Hipótese 1: Token budget excedido → compaction removeu informações antigas
├─ Hipótese 2: State persistence falhou → perfil não foi salvo
├─ Hipótese 3: Nova sessão iniciada → contexto resetado
└─ Diagnóstico provável: Context Amnesia por compaction agressiva

PASSO 4: Confirmação
├─ conversation_history VAZIO na Trace B confirma que houve reset de contexto
├─ budget_max: null confirma que a informação foi perdida
└─ ✅ DIAGNÓSTICO CONFIRMADO: Context Amnesia

CORREÇÃO APLICADA:
1. Ajustar política de compaction para preservar constraints críticas
2. Adicionar budget_max como campo "sticky" (nunca removido)
3. Implementar alerta quando current_user_profile tem campos críticos nulos
```

#### Lição

**Constraints críticas (budget, alergias, restrições dietéticas) devem ser "sticky"** — nunca removidas durante compaction ou reset de contexto. A perda de uma constraint de budget é um inconveniente; a perda de uma restrição alimentar pode ser perigosa.

---

### Exemplo 3: O Loop Infinito de Recomendações

#### Contexto

KODA entrou em um ciclo: recomendava um produto, cliente pedia alternativa, KODA recomendava o mesmo produto novamente. Isso se repetiu 4 vezes até o cliente desistir.

#### Trace (Ciclo Detectado)

```json
// Iteração 1
{
  "trace_id": "trace-exemplo-3a",
  "timestamp": "2026-05-20T10:00:00Z",
  "input": { "content": "Quero whey de chocolate" },
  "decision": {
    "generation_id": "rec-1001",
    "product_name": "Whey Chocolate Premium",
    "product_id": "prod-055"
  },
  "evaluation": { "evaluation_result": "APPROVED" }
}

// Iteração 2
{
  "trace_id": "trace-exemplo-3b",
  "timestamp": "2026-05-20T10:02:00Z",
  "input": { "content": "Tem outra opção de chocolate?" },
  "decision": {
    "generation_id": "rec-1002",
    "product_name": "Whey Chocolate Premium",
    "product_id": "prod-055"
  },
  "reasoning": {
    "thought_process": [
      { "step": 1, "reasoning": "Cliente quer whey de chocolate. Whey Chocolate Premium é a melhor opção." }
    ]
  },
  "evaluation": { "evaluation_result": "APPROVED" }
}

// Iteração 3
{
  "trace_id": "trace-exemplo-3c",
  "timestamp": "2026-05-20T10:04:00Z",
  "input": { "content": "Não, essa você já recomendou. Tem OUTRA?" },
  "decision": {
    "generation_id": "rec-1003",
    "product_name": "Whey Chocolate Premium",
    "product_id": "prod-055"
  },
  "reasoning": {
    "thought_process": [
      { "step": 1, "reasoning": "Cliente quer whey de chocolate. Whey Chocolate Premium é a melhor opção." }
    ]
  },
  "evaluation": { "evaluation_result": "APPROVED" }
}

// Iteração 4
{
  "trace_id": "trace-exemplo-3d",
  "timestamp": "2026-05-20T10:06:00Z",
  "input": { "content": "VOCÊ JÁ RECOMENDOU ESSA 3 VEZES!!!" },
  "decision": {
    "generation_id": "rec-1004",
    "product_name": "Whey Chocolate Premium",
    "product_id": "prod-055"
  },
  "evaluation": { "evaluation_result": "APPROVED" }
}
```

#### Análise

```
DIAGNÓSTICO DO EXEMPLO 3
═══════════════════════════════════════════════════════════

PASSO 1: Detecção de Loop
├─ 4 decisões consecutivas com o MESMO product_id: "prod-055"
├─ Mesmo reasoning em cada iteração
└─ ⚠️ LOOP CONFIRMADO

PASSO 2: Causa do Loop
├─ input da iteração 2: "Tem OUTRA opção?"
├─ input da iteração 3: "Você já recomendou essa. OUTRA?"
├─ entities_extracted NÃO capturou "already_recommended: [prod-055]"
├─ context NÃO inclui histórico de recomendações já feitas
└─ CAUSA: O Generator não sabe quais produtos já recomendou

PASSO 3: Por que o Evaluator não bloqueou?
├─ checks_performed: apenas "product_quality", "budget_compliance"
├─ FALTA check: "novelty_check" (produto já foi recomendado?)
└─ Evaluator não tinha regra para detectar repetição

CORREÇÃO APLICADA:
1. Adicionar campo "previously_recommended_products" ao contexto
2. Generator deve excluir produtos já recomendados (ou justificar repetição)
3. Evaluator: adicionar check "no_repetition_without_justification"
4. Se 3+ recomendações idênticas → força diversificação
```

#### Lição

**O contexto do agente precisa incluir não apenas o que o cliente quer, mas também o que o agente JÁ FEZ.** Sem memória das próprias ações, o agente repete comportamentos indefinidamente.

---

### Exemplo 4: O Falso Positivo do Evaluator

#### Contexto

Cliente com restrição "vegano" e "sem lactose". Generator recomendou produto que atendia "vegano" mas não "sem lactose". Evaluator aprovou — mas a rubrica do Evaluator só verificava "vegano", não "sem lactose".

#### Trace

```json
{
  "trace_id": "trace-exemplo-4",
  "timestamp": "2026-05-20T11:30:00Z",

  "context": {
    "current_user_profile": {
      "dietary_restrictions": ["vegan", "no_lactose"]
    }
  },

  "decision": {
    "generation_id": "rec-3391",
    "product_name": "Proteína Vegana Mix",
    "product_vegan": true,
    "product_lactose_free": false,
    "decision_status": "FINAL"
  },

  "evaluation": {
    "recommendation_received": {
      "generation_id": "rec-3391"
    },
    "evaluation_result": "APPROVED",
    "checks_performed": [
      {
        "check": "dietary_compliance",
        "result": "PASS",
        "details": "Product is vegan ✅"
      }
    ],
    "rubric_version": "1.2"
  }
}
```

#### Análise

```
DIAGNÓSTICO DO EXEMPLO 4
═══════════════════════════════════════════════════════════

PASSO 1: Constraint vs Decision
├─ constraints: ["vegan", "no_lactose"]
├─ decision.product_vegan: true ✅
├─ decision.product_lactose_free: false ❌
└─ ⚠️ Violação detectada: lactose

PASSO 2: Evaluation Check
├─ checks_performed: APENAS 1 check ("dietary_compliance")
├─ O check verificou SOMENTE "vegan"
├─ NÃO verificou "no_lactose"
└─ ⚠️ CAUSA RAIZ: Rubrica incompleta!

PASSO 3: Investigação da Rubrica
├─ rubric_version: "1.2"
├─ Esta versão só tinha regra para "vegan" (adicionada na v1.1)
├─ "no_lactose" foi adicionada como constraint na v1.3 do sistema
├─ Mas a rubrica NÃO foi atualizada para validar "no_lactose"!
└─ ⚠️ DÉFICIT DE SINCRONIZAÇÃO: Rubrica desatualizada vs. sistema

CORREÇÃO APLICADA:
1. Atualizar rubrica para v1.4 incluindo validação de "no_lactose"
2. Implementar sync-check: toda constraint no perfil DEVE ter
   um check correspondente na rubrica
3. Adicionar alerta: se constraint no perfil não tem check na rubrica → WARN
```

#### Lição

**A rubrica do Evaluator deve evoluir em sincronia com o resto do sistema.** Constraints adicionadas ao perfil do usuário sem checks correspondentes na rubrica criam uma falsa sensação de segurança — o Evaluator aprova porque "não sabia" que precisava verificar.

---

## 📐 Arquitetura de Diagnóstico: O Fluxo Completo

Este diagrama mostra o fluxo completo de diagnóstico de traces em um sistema como KODA, desde a captura até a ação corretiva.

```
ARQUITETURA DE DIAGNÓSTICO DE TRACES
═══════════════════════════════════════════════════════════════════════════════

                          ┌──────────────────────────────────┐
                          │     KODA PRODUCTION SYSTEM       │
                          │                                  │
                          │  ┌──────────┐   ┌────────────┐  │
                          │  │ Generator│──▶│ Evaluator  │  │
                          │  └──────────┘   └────────────┘  │
                          │       │               │          │
                          └───────┼───────────────┼──────────┘
                                  │               │
                                  ▼               ▼
                    ┌─────────────────────────────────────┐
                    │         TRACE COLLECTOR              │
                    │  (Captura traces em tempo real)      │
                    │  Formato: JSON estruturado           │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │       TRACE STORAGE (DB)             │
                    │  Organizado por: session_id,         │
                    │  timestamp, trace_id                 │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────┴───────────────────┐
                    │                                     │
                    ▼                                     ▼
     ┌──────────────────────────┐          ┌──────────────────────────┐
     │   AUTOMATED ANALYSIS     │          │    MANUAL ANALYSIS       │
     │   (trace_analyzer.py)    │          │    (Engenheiro)          │
     │                          │          │                          │
     │  ✅ Validação estrutural │          │  🔍 Técnica 1: Timeline  │
     │  ✅ Detecção de patterns │          │  🔍 Técnica 2: Lineage   │
     │  ✅ Contract compliance  │          │  🔍 Técnica 3: ID Track  │
     │  ✅ Confidence profiling │          │  🔍 Técnica 4: Contract  │
     │  ✅ Score generation     │          │  🔍 Técnica 5: Confidence│
     │                          │          │  🔍 Técnica 6: Decision  │
     └────────────┬─────────────┘          └────────────┬─────────────┘
                  │                                     │
                  ▼                                     │
     ┌──────────────────────────┐                       │
     │     ALERT SYSTEM         │                       │
     │                          │                       │
     │  🚨 CRITICAL: score < 50 │                       │
     │  ⚠️  WARNING:  score < 70│                       │
     │  ℹ️  INFO:    anomaly    │                       │
     └────────────┬─────────────┘                       │
                  │                                     │
                  └──────────────┬──────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────────────────┐
                    │       DIAGNOSIS DASHBOARD            │
                    │                                     │
                    │  ┌─────────────────────────────┐    │
                    │  │ Session Health Overview      │    │
                    │  │ Score: 85/100 🟢            │    │
                    │  └─────────────────────────────┘    │
                    │  ┌─────────────────────────────┐    │
                    │  │ Pattern Distribution         │    │
                    │  │ Context Amnesia:   █████ 28% │    │
                    │  │ Eval Failure:      ████  22% │    │
                    │  │ Decision Contra:   ███   18% │    │
                    │  └─────────────────────────────┘    │
                    │  ┌─────────────────────────────┐    │
                    │  │ Recent Alerts                │    │
                    │  │ 🚨 Session #9921: Budget lost│    │
                    │  │ ⚠️  Session #7734: Loop      │    │
                    │  └─────────────────────────────┘    │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │       CORRECTIVE ACTION              │
                    │                                     │
                    │  ┌─────────────────────────────┐    │
                    │  │ Auto-fix (score > 90):       │    │
                    │  │  - Re-run with fixed context │    │
                    │  │  - Adjust compaction params  │    │
                    │  └─────────────────────────────┘    │
                    │  ┌─────────────────────────────┐    │
                    │  │ Manual-fix (score < 90):     │    │
                    │  │  - Engineer investigates     │    │
                    │  │  - Code/rubric updated       │    │
                    │  │  - Regression test added     │    │
                    │  └─────────────────────────────┘    │
                    └─────────────────────────────────────┘
```

### Componentes do Sistema de Diagnóstico

| Componente | Responsabilidade | Tecnologia Típica |
|---|---|---|
| **Trace Collector** | Capturar traces em tempo real do Generator e Evaluator | Middleware hook, event bus |
| **Trace Storage** | Persistir traces para consulta e análise | PostgreSQL, Elasticsearch |
| **Automated Analysis** | Primeira passagem: validação, scoring, detecção de padrões | Python scripts, cron jobs |
| **Alert System** | Notificar engenheiros sobre anomalias | PagerDuty, Slack webhooks |
| **Diagnosis Dashboard** | Visualizar saúde do sistema, padrões, e alertas | Grafana, custom dashboard |
| **Corrective Action** | Aplicar correções baseadas no diagnóstico | CI/CD pipeline, feature flags |

---

## 🚀 Aplicação no KODA: Trace Analysis em Produção

### Como KODA Usa Trace Analysis Hoje

O KODA processa centenas de conversas por dia. Cada conversa gera dezenas de traces. O sistema de trace analysis é o que permite à equipe:

1. **Detectar problemas antes dos clientes:** Alertas automáticos disparam quando uma trace tem score < 60
2. **Diagnosticar rapidamente:** Quando um cliente reclama, a equipe puxa a trace em segundos
3. **Medir melhorias:** Comparando scores de trace antes/depois de mudanças no sistema

### Pipeline de Trace Analysis do KODA

```
PIPELINE KODA DE TRACE ANALYSIS
═══════════════════════════════════════════════════════════

[1] CAPTURA
    ├─ Toda interação Generator/Evaluator gera uma trace
    ├─ Trace é enfileirada no message broker (Redis/Kafka)
    └─ Formato: JSON com schema versionado

[2] ANÁLISE EM TEMPO REAL
    ├─ trace_analyzer.py processa cada trace em < 100ms
    ├─ Gera score de saúde (0-100)
    ├─ Detecta padrões de falha conhecidos
    └─ Se score < 60: ALERTA é disparado

[3] ARMAZENAMENTO
    ├─ Trace completa → Elasticsearch (para busca full-text)
    ├─ Métricas agregadas → PostgreSQL (para dashboards)
    └─ Retenção: 90 dias (compliance + debug histórico)

[4] DASHBOARD
    ├─ Visão em tempo real: quantas traces/minuto, score médio
    ├─ Distribuição de padrões de falha (pizza chart)
    ├─ Top 10 sessões problemáticas (lista ordenada por score)
    └─ Drill-down: clique em uma sessão → trace completa

[5] AÇÃO
    ├─ Score > 85: Nenhuma ação (trace saudável)
    ├─ Score 60-85: Log de warning para revisão semanal
    ├─ Score 40-60: Alerta no Slack #koda-quality
    └─ Score < 40: PagerDuty → engenheiro on-call
```

### Ferramentas Específicas do KODA

#### `koda-trace-analyzer` (CLI)

Ferramenta de linha de comando usada pela equipe KODA para análise manual:

```bash
# Analisar uma trace específica
koda-trace-analyzer analyze --trace-id trace-abc123

# Analisar todas as traces de uma sessão
koda-trace-analyzer session --session-id session-9921

# Buscar traces com padrão específico
koda-trace-analyzer find --pattern context-amnesia --date 2026-05-20

# Gerar relatório de saúde do dia
koda-trace-analyzer report --date 2026-05-20 --output report.html
```

#### `koda-quality-dashboard`

Dashboard em tempo real acessível em `https://koda-internal.company.com/quality`:

- **Session Health Score:** Média móvel das últimas 100 sessões
- **Pattern Breakdown:** Distribuição dos 6 padrões de falha
- **Trace Search:** Busca full-text por conteúdo de trace
- **Alert History:** Timeline de alertas disparados
- **Sprint Contract Compliance:** % de traces que respeitaram contratos

### Métricas de Qualidade do KODA

A equipe KODA monitora estas métricas diariamente:

| Métrica | Definição | Target | Alerta se... |
|---|---|---|---|
| **Trace Health Score** | Média de scores de todas as traces do dia | > 85 | < 70 |
| **Pattern Detection Rate** | % de traces onde um padrão de falha foi detectado | < 10% | > 20% |
| **Gen/Eval Mismatch Rate** | % de traces com generation_id mismatch | < 2% | > 5% |
| **Contract Compliance Rate** | % de decisões que respeitaram Sprint Contracts | > 95% | < 90% |
| **Mean Time To Diagnose (MTTD)** | Tempo médio entre alerta e diagnóstico | < 10 min | > 30 min |
| **False Positive Rate** | % de alertas que eram falsos positivos | < 5% | > 10% |

### Processo de Resposta a Incidentes

Quando um alerta crítico dispara (score < 40), o processo é:

```
PROCESSO DE RESPOSTA A INCIDENTES KODA
═══════════════════════════════════════════════════════════

T+0min   🚨 PagerDuty alerta engenheiro on-call
         ├─ Inclui: session_id, trace_id, score, pattern detectado
         └─ Link direto para a trace no dashboard

T+2min   🔍 Engenheiro abre a trace no dashboard
         ├─ Roda koda-trace-analyzer para análise detalhada
         └─ Identifica padrão de falha (usa taxonomia deste guia)

T+5min   📋 Diagnóstico preliminar
         ├─ Documenta: qual padrão, qual seção da trace, causa provável
         └─ Posta no Slack #koda-incidents

T+10min  🔧 Se correção é simples (config, threshold, parâmetro):
         ├─ Aplica hotfix via feature flag
         └─ Monitora score da sessão por 15 min

T+15min  📊 Se correção requer código:
         ├─ Cria issue no GitHub com trace anexada
         ├─ Escala para time de desenvolvimento
         └─ Continua monitorando

T+30min  ✅ Validação
         ├─ Confirma que scores voltaram ao normal
         └─ Postmortem agendado para próxima sprint review
```

---

## 💻 Ferramentas Práticas de Linha de Comando

Além do `koda-trace-analyzer`, engenheiros experientes usam ferramentas Unix padrão para análise rápida de traces. Aqui estão os comandos mais úteis.

### Extração Rápida com `jq`

```bash
# Extrair todos os generation_id de uma trace (para ID Tracking)
cat trace.json | jq '.decision.generation_id, .evaluation.recommendation_received.generation_id'

# Verificar se há mismatch
GEN=$(cat trace.json | jq -r '.decision.generation_id')
EVAL=$(cat trace.json | jq -r '.evaluation.recommendation_received.generation_id')
if [ "$GEN" != "$EVAL" ]; then
  echo "❌ GEN/EVAL MISMATCH: $GEN vs $EVAL"
fi

# Extrair confidence_score de todas as traces de uma sessão
for f in traces/session-9921/*.json; do
  echo "$(basename $f): $(cat $f | jq -r '.reasoning.confidence_score // "N/A"')"
done

# Listar todas as constraints do perfil vs. checks do Evaluator
echo "=== CONSTRAINTS ==="
cat trace.json | jq '.context.current_user_profile.dietary_restrictions[]'
echo "=== CHECKS PERFORMED ==="
cat trace.json | jq '.evaluation.checks_performed[].check'

# Verificar contract compliance (budget)
BUDGET=$(cat trace.json | jq '.context.current_user_profile.budget_max')
PRICE=$(cat trace.json | jq '.decision.price')
echo "Budget: R$ $BUDGET | Price: R$ $PRICE"
if [ "$(echo "$PRICE > $BUDGET" | bc -l)" -eq 1 ]; then
  echo "❌ BUDGET VIOLATION"
fi
```

### Análise Batch com Script Shell

```bash
#!/bin/bash
# batch-trace-analyzer.sh — Analisa todas as traces de um diretório
# Uso: ./batch-trace-analyzer.sh traces/session-9921/

DIR="$1"
TOTAL=0
ISSUES=0

echo "=== BATCH TRACE ANALYSIS ==="
echo "Session: $(basename $DIR)"
echo ""

for trace in "$DIR"/*.json; do
  TOTAL=$((TOTAL + 1))
  SCORE=$(cat "$trace" | jq -r '.trace_health_score // 100')
  CONFIDENCE=$(cat "$trace" | jq -r '.reasoning.confidence_score // 1.0')

  if [ "$(echo "$SCORE < 70" | bc -l)" -eq 1 ]; then
    echo "⚠️  $(basename $trace): Score=$SCORE (LOW)"
    ISSUES=$((ISSUES + 1))
  elif [ "$(echo "$CONFIDENCE < 0.6" | bc -l)" -eq 1 ]; then
    echo "⚠️  $(basename $trace): Confidence=$CONFIDENCE (LOW)"
    ISSUES=$((ISSUES + 1))
  fi
done

echo ""
echo "Total traces: $TOTAL"
echo "Issues found: $ISSUES"
echo "Health: $(echo "scale=1; ($TOTAL - $ISSUES) * 100 / $TOTAL" | bc)% clean"
```

### Busca Rápida com `grep` em Traces JSON

```bash
# Encontrar todas as traces onde o Evaluator REJEITOU
grep -l '"evaluation_result": "REJECTED"' traces/session-*/*.json

# Encontrar traces com confidence_score abaixo de 0.5
grep -l '"confidence_score": 0\.[0-4]' traces/session-*/*.json

# Contar ocorrências de cada padrão de falha em um dia de logs
grep -oh '"pattern_detected": "[^"]*"' logs/2026-05-20/*.log | sort | uniq -c | sort -rn

# Encontrar traces com generation_id mismatch
for f in traces/session-*/*.json; do
  GEN=$(jq -r '.decision.generation_id' "$f")
  EVAL=$(jq -r '.evaluation.recommendation_received.generation_id' "$f")
  if [ "$GEN" != "$EVAL" ] && [ "$GEN" != "null" ] && [ "$EVAL" != "null" ]; then
    echo "MISMATCH: $f — Gen:$GEN vs Eval:$EVAL"
  fi
done
```

### Visualização Rápida de Timeline

```bash
# Extrair e ordenar timestamps de uma sessão
for f in traces/session-9921/*.json; do
  TS=$(cat "$f" | jq -r '.timestamp')
  DECISION=$(cat "$f" | jq -r '.decision.product_name // "N/A"')
  CONFIDENCE=$(cat "$f" | jq -r '.reasoning.confidence_score // "N/A"')
  printf "%-25s | %-30s | confidence: %s\n" "$TS" "$DECISION" "$CONFIDENCE"
done | sort
```

**Output típico:**
```
2026-05-20T14:05:00Z      | Whey Baunilha                  | confidence: 0.92
2026-05-20T14:12:00Z      | Creatina                       | confidence: 0.88
2026-05-20T14:18:00Z      | Whey Chocolate                 | confidence: 0.45  ⚠️
2026-05-20T14:25:00Z      | Whey Morango                   | confidence: 0.91
2026-05-20T14:32:00Z      | Whey Mais Barato               | confidence: 0.38  ⚠️
```

---

## 📡 Guia de Interpretação de Sinais

Nem todo problema é binário (bug ou não-bug). Muitos são **sinais** — indicadores de que algo precisa de atenção antes que vire um incidente.

### Sinal 1: Score em Queda Gradual

**O que você vê:** O score médio das traces está caindo 2-3 pontos por dia ao longo de uma semana.

```
Dia 1: score médio = 91
Dia 2: score médio = 89
Dia 3: score médio = 86
Dia 4: score médio = 84
Dia 5: score médio = 81  ← Atenção!
```

**Interpretação:** Algo está degradando gradualmente. Pode ser:
- Modelo está "envelhecendo" (model drift)
- Volume de conversas aumentou e o sistema está sob stress
- Uma mudança recente (prompt, rubrica, parâmetro) está surtindo efeito cumulativo

**Ação:** Investigar PROATIVAMENTE — não espere o score cair abaixo de 70.

### Sinal 2: Pico de um Padrão Específico

**O que você vê:** Um padrão de falha que normalmente ocorre em 5% das traces de repente salta para 20%.

```
Semana anterior: Context Amnesia = 5% das traces
Hoje:            Context Amnesia = 22% das traces  ← Alerta!
```

**Interpretação:** Algo específico mudou que está causando este padrão. Possíveis causas:
- Deploy recente alterou a política de compaction
- Nova feature está gerando conversas mais longas (mais risco de amnesia)
- Mudança no modelo base está afetando a retenção de contexto

**Ação:** Correlacionar o pico com o changelog de deploy. Reverter a mudança mais recente se necessário.

### Sinal 3: Dispersão de Scores Aumentando

**O que você vê:** A variância entre scores está aumentando — algumas traces têm score 95, outras score 40.

```
Semana passada: scores entre 80-95 (dispersão baixa)
Hoje:           scores entre 40-98 (dispersão alta)
```

**Interpretação:** O sistema está se comportando de forma inconsistente. Umas conversas vão bem, outras vão mal — sem padrão claro. Possíveis causas:
- Race condition intermitente
- Dependência de fatores externos (latência de API, disponibilidade de catálogo)
- Modelo com temperature alta demais (comportamento não-determinístico)

**Ação:** Separar traces de alto e baixo score. Procurar o que as de baixo score têm em comum (horário, tipo de produto, duração da conversa).

### Sinal 4: Falsos Positivos Aumentando

**O que você vê:** Mais alertas estão sendo disparados, mas quando investigados, as traces estão corretas.

```
Mês passado: 5 alertas, 1 falso positivo (20%)
Este mês:    20 alertas, 12 falsos positivos (60%)  ← Problema!
```

**Interpretação:** Os thresholds de alerta estão muito sensíveis ou a definição de "problema" mudou. Possíveis causas:
- Threshold foi reduzido recentemente
- O padrão de conversas mudou (ex: mais clientes mudando de ideia = mais "mudanças legítimas" sendo classificadas como erro)
- O script de análise está com um bug

**Ação:** Revisar thresholds. Se 60% dos alertas são falsos positivos, a equipe vai parar de confiar nos alertas (fadiga de alarme).

### Sinal 5: Tempo de Diagnóstico Aumentando

**O que você vê:** O MTTD (Mean Time To Diagnose) está subindo — está levando mais tempo para diagnosticar cada incidente.

```
Trimestre 1: MTTD = 8 minutos
Trimestre 2: MTTD = 15 minutos
Trimestre 3: MTTD = 25 minutos  ← Preocupante!
```

**Interpretação:** Os problemas estão ficando mais complexos OU a equipe está perdendo familiaridade com as ferramentas. Possíveis causas:
- Sistema ficou mais complexo (mais componentes = Coordination Failures mais frequentes)
- Novos engenheiros na equipe (curva de aprendizado)
- Ferramentas de diagnóstico não acompanharam a evolução do sistema

**Ação:** Investir em treinamento, melhorar dashboards, ou simplificar a arquitetura se a complexidade estiver prejudicando a operação.

---

## 🔧 Checklist de Troubleshooting

Esta é sua referência rápida. Quando um incidente acontecer, siga esta checklist em ordem.

### Fase 1: Triagem (2 minutos)

- [ ] **Qual é o sintoma reportado?**
  - Cliente recebeu recomendação errada?
  - Cliente recebeu recomendação repetida?
  - Agente "esqueceu" algo que o cliente disse?
  - Agente ficou em loop?
  - Resposta demorou muito?
  - Erro técnico (timeout, crash)?

- [ ] **Qual o session_id?**
  - Anote para buscar todas as traces da sessão

- [ ] **Qual o impacto?**
  - Cliente reclamou? (→ prioridade ALTA)
  - Foi detectado por alerta automático? (→ prioridade MÉDIA)
  - Foi encontrado em revisão proativa? (→ prioridade BAIXA)

### Fase 2: Coleta de Evidências (5 minutos)

- [ ] **Puxe todas as traces da sessão** (ordenadas por timestamp)
- [ ] **Identifique a trace específica do incidente** (pelo timestamp da reclamação)
- [ ] **Extraia os campos críticos:**
  - `input.content` e `input.entities_extracted`
  - `context.current_user_profile`
  - `decision.product_name`, `decision.price`, `decision.flavor`
  - `reasoning.confidence_score`
  - `evaluation.evaluation_result` e `evaluation.checks_performed`

### Fase 3: Aplicação da Taxonomia (5-10 minutos)

Para cada padrão, execute o teste de confirmação:

- [ ] **Padrão 1 - Input Capture Failure:**
  - `entities_extracted` contradiz `input.content`? (Se sim → P1 ✅)

- [ ] **Padrão 2 - Context Amnesia:**
  - Constraint no histórico mas NÃO no `current_user_profile`? (Se sim → P2 ✅)
  - `conversation_history` está vazio quando não deveria? (Se sim → P2 ✅)

- [ ] **Padrão 3 - Decision Contradiction:**
  - Decisão viola constraint presente no contexto? (Se sim → P3 ✅)

- [ ] **Padrão 4 - Reasoning Collapse:**
  - `confidence_score < 0.6`? (Se sim → P4 ✅)
  - `thought_process` tem passos circulares ou irrelevantes? (Se sim → P4 ✅)

- [ ] **Padrão 5 - Evaluation Failure:**
  - `generation_id` do Generator ≠ `generation_id` do Evaluator? (Se sim → P5 ✅)
  - Evaluator aprovou violação óbvia? (Se sim → P5 ✅)
  - Evaluator rejeitou decisão correta? (Se sim → P5 ✅)

- [ ] **Padrão 6 - Coordination Failure:**
  - Estado (budget, preference) difere entre traces da mesma sessão? (Se sim → P6 ✅)
  - `contract_version_used` < `contract_version` atual? (Se sim → P6 ✅)

### Fase 4: Aplicação de Técnicas (10-20 minutos)

- [ ] **Técnica 1 - Timeline:** Reconstrua a ordem cronológica dos eventos. Há gaps ou inversões?
- [ ] **Técnica 2 - Data Lineage:** Trace o caminho do dado crítico do INPUT ao EVALUATION. Onde ele muda?
- [ ] **Técnica 3 - ID Tracking:** Todos os `generation_id` têm match 1:1 entre Generator e Evaluator?
- [ ] **Técnica 4 - Contract Compliance:** A decisão respeita TODOS os termos do Sprint Contract?
- [ ] **Técnica 5 - Confidence Profile:** Qual o `confidence_score`? Está acima do threshold de segurança?
- [ ] **Técnica 6 - Decision Diff:** Se houve múltiplas decisões, o que mudou entre a primeira e a última?

### Fase 5: Diagnóstico e Correção (10-30 minutos)

- [ ] **Documente o diagnóstico:**
  - Qual padrão de falha?
  - Qual seção da trace contém a discrepância?
  - Qual a causa raiz?

- [ ] **Classifique a severidade:**
  - 🚨 CRÍTICA: Afeta segurança/saúde do cliente (alergias, medicamentos)
  - ⚠️ ALTA: Causa insatisfação significativa ou perda financeira
  - ℹ️ MÉDIA: Degradação de qualidade sem impacto imediato
  - 📝 BAIXA: Oportunidade de melhoria

- [ ] **Determine a correção:**
  - Ajuste de configuração? (threshold, parâmetro) → Aplicar imediatamente
  - Mudança de código? (parser, prompt, lógica) → Criar issue + PR
  - Atualização de rubrica? → Atualizar Evaluator checks
  - Mudança de arquitetura? → Discutir em planning

- [ ] **Valide a correção:**
  - Re-executou a mesma sessão com a correção?
  - Score da trace voltou a > 85?
  - Nenhum novo padrão de falha introduzido?

### Fase 6: Prevenção (após correção)

- [ ] **Adicione teste de regressão** para o padrão de falha encontrado
- [ ] **Atualize a rubrica do Evaluator** se necessário
- [ ] **Documente no postmortem** para compartilhar com a equipe
- [ ] **Verifique se outras sessões** têm o mesmo padrão (busca retroativa)
- [ ] **Atualize alertas automáticos** se o padrão não estava sendo detectado

---

## ⚡ Sub-Padrões de Falha: Variações dos 6 Padrões Principais

Cada um dos 6 padrões principais tem variantes comuns que merecem atenção específica. Conhecer estas variações acelera o diagnóstico.

---

### Sub-Padrões de Context Amnesia (Padrão 2)

#### 2a. Amnésia por Compaction Agressiva

**Sintoma:** Informações das primeiras interações desaparecem, mas informações recentes estão intactas.

**Assinatura na trace:**
```
Trace inicial (T+0min):
  context.conversation_history.length = 45 eventos
  context.current_user_profile: COMPLETO (todas as constraints)

Trace intermediária (T+60min):
  context.conversation_history.length = 12 eventos  ← REDUZIDO
  context.current_user_profile.dietary_restrictions: ["vegan"]
  context.current_user_profile.budget_max: 100.00

Trace final (T+120min):
  context.conversation_history.length = 3 eventos   ← MUITO REDUZIDO
  context.current_user_profile.dietary_restrictions: []  ← PERDIDO
  context.current_user_profile.budget_max: null     ← PERDIDO
```

**Diagnóstico:** Compaction está removendo constraints críticas junto com histórico de conversa.

**Correção:** Implementar política de "sticky fields" — campos críticos (dietary_restrictions, budget_max, allergies) são preservados independentemente do compaction.

#### 2b. Amnésia por Troca de Sessão

**Sintoma:** Agente "recomeça do zero" no meio de uma conversa longa — como se fosse um novo cliente.

**Assinatura na trace:**
```
Trace A: session_id = "session-9921-a"
Trace B: session_id = "session-9921-b"  ← SESSÃO DIFERENTE!

Mesma conversa do WhatsApp, mas o sistema criou duas sessões internas.
A Trace B não tem acesso ao contexto da Trace A.
```

**Diagnóstico:** O middleware de sessão está criando sessões novas quando a conversa excede um limite de tempo ou tokens.

**Correção:** Garantir que `session_id` seja estável para toda a duração da conversa do WhatsApp, independentemente de reinicializações internas.

#### 2c. Amnésia Seletiva (Esquece Restrições, Lembra Preferências)

**Sintoma:** O agente lembra o sabor preferido do cliente (Chocolate), mas esquece que ele é alérgico a glúten.

**Assinatura na trace:**
```
context.current_user_profile.flavor_preference_current: "Chocolate"  ← LEMBROU
context.current_user_profile.dietary_restrictions: []                ← ESQUECEU
```

**Diagnóstico:** O sistema prioriza "preferências" sobre "restrições" durante a montagem do contexto — ou as restrições têm um TTL diferente.

**Correção:** Restrições (dietary, allergies, medical) devem ter prioridade MÁXIMA no contexto e nunca ser removidas antes de preferências cosméticas.

---

### Sub-Padrões de Evaluation Failure (Padrão 5)

#### 5a. Evaluator Cego por Rubrica Incompleta

**Sintoma:** Evaluator aprova tudo porque a rubrica não cobre o caso específico.

**Assinatura na trace:**
```
evaluation.checks_performed: [
  { "check": "budget_compliance", "result": "PASS" },
  { "check": "product_exists", "result": "PASS" }
]
// FALTANDO: dietary_compliance, allergy_check, price_comparison

evaluation.evaluation_result: "APPROVED"
// Aprovou porque só verificou 2 de 7 constraints possíveis
```

**Diagnóstico:** A rubrica está desatualizada — constraints foram adicionadas ao sistema mas a rubrica não foi atualizada.

**Correção:** Implementar sync automático: toda constraint no perfil DEVE ter um check correspondente na rubrica do Evaluator.

#### 5b. Evaluator com Viés de Aprovação

**Sintoma:** Evaluator aprova consistentemente mais do que deveria — taxa de aprovação > 95% quando a taxa de erro real é ~15%.

**Assinatura na trace:**
```
Últimas 100 traces:
  evaluation.evaluation_result = "APPROVED":  97 traces (97%)
  evaluation.evaluation_result = "REJECTED":   3 traces (3%)
  
Taxa de erro reportada por clientes: 15%
GAP: 15% - 3% = 12% de falsos positivos
```

**Diagnóstico:** O Evaluator está com um viés de aprovação (sycophancy do avaliador). Pode ser causado por temperature muito baixa, prompt muito permissivo, ou rubrica com thresholds muito baixos.

**Correção:** Aumentar temperature do Evaluator para 0.3-0.5, revisar thresholds da rubrica, adicionar checks negativos ("procure razões para REJEITAR").

#### 5c. Evaluator Lento (Timeout Silencioso)

**Sintoma:** Decisões são aprovadas sem verificação porque o Evaluator excedeu o timeout e o sistema usou um fallback de "aprovar por padrão".

**Assinatura na trace:**
```
decision.timestamp: 14:32:05.000
evaluation.timestamp_received: 14:32:05.050
evaluation.evaluation_result: "APPROVED"
evaluation.checks_performed: []  ← VAZIO! Nenhum check executado
evaluation.evaluation_timeout: true  ← TIMEOUT
```

**Diagnóstico:** O Evaluator está levando tempo demais para processar traces complexas e o sistema está aprovando por padrão para não bloquear o fluxo.

**Correção:** Aumentar timeout do Evaluator, otimizar checks mais lentos, ou implementar "rejeitar por padrão" em vez de "aprovar por padrão" em caso de timeout.

---

### Sub-Padrões de Coordination Failure (Padrão 6)

#### 6a. Race Condition entre Sprints

**Sintoma:** Duas atualizações de estado acontecem simultaneamente em sprints diferentes, e uma sobrescreve a outra.

**Assinatura na trace:**
```
Trace Sprint 1 (14:30:00.100): budget_max = 100.00
Trace Sprint 2 (14:30:00.150): budget_max = 80.00  ← Quase simultâneo
Trace Sprint 1 (14:30:00.200): budget_max = 100.00 ← Sobrescreveu o 80!

Ordem temporal: o último write (Sprint 1) sobrescreveu o Sprint 2,
mas o cliente QUERIA o budget de 80 (atualização mais recente).
```

**Diagnóstico:** Não há lock ou versioning no estado compartilhado entre sprints.

**Correção:** Implementar optimistic locking com `state_version` — cada write inclui a versão que leu, e writes conflitantes são detectados e resolvidos.

#### 6b. Propagação Assíncrona com Lag

**Sintoma:** Uma mudança de estado (ex: atualização de preferência) leva segundos ou minutos para propagar para todos os componentes.

**Assinatura na trace:**
```
Trace do state update (14:30:00): flavor_preference = "Chocolate"
Trace do Generator (14:30:02):    flavor_preference = "Baunilha" ← AINDA antigo
Trace do Evaluator (14:30:03):    flavor_preference = "Baunilha" ← AINDA antigo
Trace do Generator (14:30:05):    flavor_preference = "Chocolate" ← FINALMENTE atualizado
```

**Diagnóstico:** O barramento de eventos tem latência de propagação. O Generator e Evaluator estão lendo de caches locais que ainda não foram invalidados.

**Correção:** Reduzir TTL de cache de estado para < 1s, ou usar leitura direta (sem cache) para campos críticos.

#### 6c. Dead Letter: Evento Perdido na Fila

**Sintoma:** Uma atualização de estado foi enviada mas nunca chegou ao destino — como se nunca tivesse acontecido.

**Assinatura na trace:**
```
Trace do Event Emitter (14:30:00): event_sent = "preference_update",
                                    new_flavor = "Chocolate",
                                    event_id = "evt-0055"

Trace do Event Consumer: event_id "evt-0055" NÃO APARECE em nenhuma trace
do consumer. O evento foi perdido.

Trace do Context (14:35:00): flavor_preference ainda é "Baunilha" ← NUNCA atualizou
```

**Diagnóstico:** O evento foi publicado mas não foi consumido — pode ser bug na fila, Dead Letter Queue sem handler, ou consumer crash antes de processar.

**Correção:** Implementar monitoramento de eventos (pub/sub confirmation), Dead Letter Queue com alerta, e reconciliação periódica de estado.

---

## 🧠 Erros Comuns no Diagnóstico de Traces

Mesmo engenheiros experientes cometem estes erros ao analisar traces. Conhecê-los antecipadamente economiza horas.

### Erro 1: Olhar Só a Trace do Incidente

**O erro:** Abrir apenas a trace onde o problema foi detectado, ignorando as traces anteriores da mesma sessão.

**Por que é um problema:** O erro pode ter sido causado 10 traces atrás — um context corrompido que se propagou silenciosamente até explodir na trace final.

**O correto:** SEMPRE puxe TODAS as traces da `session_id`. O problema raramente está na última trace — a última trace é apenas onde o problema se tornou visível.

```
Exemplo real KODA:
- Trace #47 (14:30): contexto corrompido (bug silencioso)
- Trace #48-#52: operação normal, ninguém notou
- Trace #53 (15:45): cliente reclama (problema visível)

Se você olhar SÓ a trace #53, vai achar que o Evaluator falhou.
Se você olhar a sequência, vai ver que foi a trace #47 que iniciou o problema.
```

### Erro 2: Confiar Cegamente no confidence_score

**O erro:** Assumir que `confidence_score > 0.8` significa que a decisão está correta.

**Por que é um problema:** Confidence score mede a **certeza do modelo**, não a **correção factual**. Um modelo pode estar 95% confiante em uma recomendação completamente errada.

**O correto:** Use confidence_score como um sinal, não como validação. Combine com contract compliance check e data lineage.

```
Exemplo: confidence_score = 0.92, mas:
- decision.price = 200.00 (budget_max = 100.00)
- decision.product_vegan = false (restriction = "vegan")

O modelo estava MUITO confiante. E MUITO errado.
```

### Erro 3: Assumir Que o Problema É Sempre do Modelo

**O erro:** Concluir "o LLM alucinou" sem verificar se o input/contexto estava correto.

**Por que é um problema:** Muitos "erros do modelo" são na verdade erros de contexto — o modelo produziu uma resposta lógica para o contexto que recebeu, mas o contexto estava errado.

**O correto:** Antes de culpar o modelo, verifique:
1. O input foi capturado corretamente? (Input Capture check)
2. O contexto estava atualizado? (Context Amnesia check)
3. O modelo recebeu todas as constraints? (Contract Compliance check)

```
Cenário típico:
- Modelo recomendou produto não-vegano
- Engenheiro: "O modelo alucinou a restrição!"
- Realidade: context.dietary_restrictions = [] (contexto veio vazio)
- O modelo fez o melhor que podia com o contexto que recebeu
```

### Erro 4: Tratar Sintoma em Vez da Causa

**O erro:** Corrigir o output errado sem investigar por que o output foi gerado errado.

**Por que é um problema:** O mesmo bug vai se manifestar novamente em outra decisão, outro produto, outro cliente.

**O correto:** Siga a cadeia causal até a raiz:
- Output errado → Decisão errada → Contexto errado → Input mal capturado → Parser com bug
- Cada camada é uma oportunidade de correção, mas só a raiz previne recorrência

### Erro 5: Não Diferenciar Erro de Mudança Legítima

**O erro:** Classificar como "erro" uma mudança de decisão que foi legítima.

**Por que é um problema:** Gera falsos positivos, alertas desnecessários, e intervenções que pioram a experiência do cliente.

**O correto:** Antes de classificar como erro, pergunte: "O cliente mudou de ideia entre essas duas decisões?"

```
Trace A: "Recomendo Whey Chocolate" (cliente pedia chocolate)
Trace B: "Recomendo Whey Baunilha" (cliente MUDOU para baunilha)

Isso NÃO é um erro. É o agente respondendo a uma mudança legítima.
O trace reading revela: input da Trace B contém "mudei para baunilha".
```

### Erro 6: Ignorar a Ordem Temporal dos Eventos

**O erro:** Ler traces em ordem de `trace_id` em vez de ordem de `timestamp`.

**Por que é um problema:** Se o sistema processa eventos assincronamente, `trace_id` pode não refletir a ordem cronológica real. Uma trace com ID maior pode ter timestamp mais antigo.

**O correto:** SEMPRE ordene traces por `timestamp`, nunca por `trace_id` ou ordem de inserção no banco.

---

## 🔄 Padrões de Recuperação: O Que Fazer Depois de Diagnosticar

Diagnosticar é metade do trabalho. A outra metade é implementar a correção de forma que o problema não retorne.

### Padrão de Recuperação 1: Hotfix por Feature Flag

**Quando usar:** Correção simples (threshold, parâmetro, configuração) que não requer deploy.

**Processo:**
```
1. Diagnosticar → identificar parâmetro incorreto
2. Atualizar feature flag no dashboard de configuração
3. Monitorar score da sessão por 15 min
4. Se score normalizar → documentar no #koda-incidents
5. Se score não normalizar → escalar para correção via código
```

**Exemplo KODA:**
```
Problema: Evaluator aprovando produtos acima do budget
Diagnóstico: threshold de budget_compliance estava em 1.2 (20% de tolerância)
Hotfix: Reduzir FEATURE_BUDGET_THRESHOLD de 1.2 para 1.0
Resultado: Scores voltaram ao normal em 5 minutos
```

### Padrão de Recuperação 2: Re-processamento com Contexto Corrigido

**Quando usar:** O erro foi causado por contexto incorreto, mas a decisão pode ser re-gerada com contexto correto.

**Processo:**
```
1. Diagnosticar → identificar que contexto estava desatualizado
2. Corrigir o contexto (atualizar cache, forçar refresh)
3. Re-executar Generator com contexto corrigido
4. Passar pelo Evaluator normalmente
5. Comparar decisão original vs. re-processada
6. Se diferentes → enviar correção pro cliente (se ainda relevante)
```

**Exemplo KODA:**
```
Problema: Cliente recebeu recomendação baseada em preferência antiga
Diagnóstico: current_user_profile.flavor_preference_current estava desatualizado
Recuperação: Atualizou contexto, re-gerou recomendação (Chocolate em vez de Baunilha)
Resultado: Cliente recebeu follow-up: "Corrigindo: Whey Chocolate é a melhor opção!"
```

### Padrão de Recuperação 3: Correção por Atualização de Rubrica

**Quando usar:** O Evaluator falhou porque a rubrica não cobria o caso.

**Processo:**
```
1. Diagnosticar → identificar check ausente na rubrica
2. Escrever novo check para a rubrica (ex: "no_lactose_check")
3. Testar novo check em 100 traces históricas (não deve quebrar casos corretos)
4. Deploy da nova versão da rubrica
5. Monitorar taxa de rejeição: deve AUMENTAR levemente (detectando erros que antes passavam)
6. Se taxa de rejeição DISPARAR (>20% de aumento) → rollback e investigar
```

**Exemplo KODA:**
```
Problema: Evaluator aprovava produtos com lactose para clientes com restrição
Diagnóstico: Rubrica v1.2 não tinha check de "no_lactose"
Recuperação: Rubrica v1.3 adicionou no_lactose_check
Resultado: 3% de aumento em rejeições — todas legítimas (produtos com lactose)
```

### Padrão de Recuperação 4: Correção Arquitetural (Longo Prazo)

**Quando usar:** O problema é estrutural — não é um parâmetro ou uma rubrica, mas um design flaw.

**Processo:**
```
1. Diagnosticar → identificar que é Coordination Failure ou Race Condition
2. Documentar no ADR (Architecture Decision Record)
3. Propor solução arquitetural (ex: event sourcing, distributed lock)
4. Implementar em branch separada com testes extensivos
5. Deploy com feature flag (on/off para rollback rápido)
6. Monitorar por 1 semana antes de remover feature flag
```

**Exemplo KODA:**
```
Problema: Estado inconsistente entre sprints (Coordination Failure)
Diagnóstico: Sistema usava cache local com TTL de 5min
Recuperação: Migração para Redis compartilhado com TTL de 1s + invalidação ativa
Resultado: Incidência de Coordination Failure caiu de 5% para < 0.5%
```

---

## ❓ FAQ de Troubleshooting: Perguntas Que Recebemos Toda Semana

### "O score da trace está 85, mas o cliente reclamou. Como pode?"

**Resposta:** O score é uma heurística, não uma garantia. Score 85 indica que a trace passou em validações estruturais e de contrato, mas não detecta problemas sutis como:
- Tom inadequado na resposta (cliente se sentiu ofendido)
- Recomendação tecnicamente correta mas contextualmente ruim
- Produto correto mas explicação confusa

Nestes casos, vá para a [Técnica 6: Decision Diff](#técnica-6-diff-de-decisões-decision-comparison) e analise o `reasoning` qualitativamente.

### "Como sei se uma mudança de decisão é bug ou mudança legítima?"

**Resposta:** Compare os `input.content` entre a primeira e a última decisão:

- Se o input mais recente contém frases como "mudei de ideia", "agora prefiro", "na verdade" → mudança legítima
- Se o input NÃO contém indicação de mudança e a decisão mudou mesmo assim → possível bug
- Se o `context.flavor_preference_timestamp` é mais recente que o timestamp da primeira decisão → mudança legítima (perfil foi atualizado)

### "Por que o Evaluator aprovou algo claramente errado?"

**Resposta:** Três causas mais comuns, em ordem:

1. **Rubrica incompleta (50% dos casos):** O check específico não existe na rubrica. Ex: rubrica verifica "vegan" mas não "lactose_free".
2. **Contexto do Evaluator diferente (30% dos casos):** O Evaluator recebeu um contexto diferente do Generator. Verifique `evaluation.context_used_for_evaluation`.
3. **Sycophancy do Evaluator (20% dos casos):** O modelo do Evaluator tem viés de aprovação. Aumente a temperature ou ajuste o prompt.

### "Quanto tempo leva para diagnosticar uma trace?"

**Resposta:** Depende do padrão e da sua experiência:

| Padrão | Iniciante | Intermediário | Expert |
|---|---|---|---|
| Input Capture Failure | 10 min | 3 min | 1 min |
| Context Amnesia | 25 min | 10 min | 5 min |
| Decision Contradiction | 10 min | 3 min | 1 min |
| Reasoning Collapse | 30 min | 15 min | 8 min |
| Evaluation Failure | 20 min | 8 min | 3 min |
| Coordination Failure | 60 min | 30 min | 15 min |

Com prática diária, você chega ao nível "Intermediário" em 2 semanas e "Expert" em 2 meses.

### "Devo analisar TODAS as traces ou só as que têm alerta?"

**Resposta:** Use a matriz de priorização:

- **100% das traces:** análise automatizada (scripts) — custo quase zero
- **Traces com score < 70:** revisão humana semanal (30 min por semana)
- **Traces com score < 50:** investigação imediata (alerta)
- **Traces de clientes VIP:** revisão humana em 100% dos casos, independente do score

### "Como evito que o mesmo bug aconteça de novo?"

**Resposta:** O ciclo de prevenção tem 4 passos:

1. **Teste de regressão:** Escreva um teste que reproduz o padrão de falha encontrado
2. **Alerta automático:** Configure o `trace_analyzer.py` para detectar esse padrão no futuro
3. **Rubrica update:** Se o Evaluator não detectou, atualize a rubrica
4. **Postmortem:** Compartilhe com a equipe — se uma pessoa aprendeu, todos aprendem

---

## 📝 Exercícios Práticos de Diagnóstico

### Exercício 1: Identifique o Padrão

**Trace fornecida:**
```json
{
  "trace_id": "ex-001",
  "input": {
    "content": "Quero o whey mais barato que vocês têm, mas sem lactose",
    "entities_extracted": {
      "price_preference": "cheapest",
      "dietary_restriction": "no_lactose"
    }
  },
  "context": {
    "current_user_profile": {
      "budget_priority": "lowest_price",
      "dietary_restrictions": ["no_lactose"]
    }
  },
  "decision": {
    "product_name": "Whey Econômico",
    "price": 49.90,
    "product_lactose_free": false
  },
  "reasoning": {
    "thought_process": [
      { "step": 1, "reasoning": "Cliente quer o mais barato. Whey Econômico é R$ 49,90." }
    ],
    "confidence_score": 0.94
  },
  "evaluation": {
    "evaluation_result": "APPROVED",
    "checks_performed": [
      { "check": "price_check", "result": "PASS" }
    ]
  }
}
```

**Perguntas:**
1. Qual padrão de falha esta trace exibe? (Dica: não é apenas um padrão)
2. Quais seções da trace contêm a discrepância?
3. Qual seria a correção mais adequada?

---

### Exercício 2: Diagnóstico Cross-Trace

**Duas traces da mesma sessão:**

*Trace A (timestamp: 10:00:00)*
```json
{
  "context": {
    "current_user_profile": {
      "dietary_restrictions": ["vegan", "no_gluten"],
      "budget_max": 150.00
    }
  }
}
```

*Trace B (timestamp: 11:30:00)*
```json
{
  "context": {
    "current_user_profile": {
      "dietary_restrictions": ["vegan"],
      "budget_max": 150.00
    }
  },
  "decision": {
    "product_vegan": true,
    "product_gluten_free": false,
    "price": 120.00
  },
  "evaluation": {
    "checks_performed": [
      { "check": "dietary_compliance", "result": "PASS", "details": "Product is vegan" }
    ],
    "rubric_version": "1.0"
  }
}
```

**Perguntas:**
1. O que mudou entre a Trace A e a Trace B?
2. Isso é um bug ou uma mudança legítima?
3. Se for bug, qual o padrão e a causa raiz?
4. Se for legítimo, como você confirmaria?

---

### Exercício 3: Monte um Plano de Correção

**Cenário:**
Você diagnosticou um Coordination Failure: o budget definido no Sprint 1 (R$ 100) não foi propagado para o Sprint 2, que usou o budget padrão (R$ 200) e recomendou um produto de R$ 180.

**Tarefa:**
Monte um plano de correção seguindo os [Padrões de Recuperação](#-padrões-de-recuperação-o-que-fazer-depois-de-diagnosticar). Inclua:
1. Qual padrão de recuperação usar
2. Passos específicos de implementação
3. Como validar que a correção funcionou
4. Como prevenir recorrência

---

*(Respostas comentadas no [Apêndice: Respostas dos Exercícios](#-apêndice-respostas-dos-exercícios))*

---

## 📎 Apêndice: Respostas dos Exercícios

### Resposta Exercício 1

1. **Padrões de falha:** Decision Contradiction (Padrão 3) — a decisão ignora a constraint `no_lactose` que está presente no contexto. TAMBÉM: Evaluation Failure (Padrão 5) — o Evaluator só verificou `price_check` e ignorou `dietary_compliance`.

2. **Seções com discrepância:**
   - `context.current_user_profile.dietary_restrictions` contém "no_lactose"
   - `decision.product_lactose_free` é `false` → contradição direta
   - `evaluation.checks_performed` não inclui dietary check → rubrica incompleta

3. **Correção mais adequada:**
   - Curto prazo: Atualizar rubrica do Evaluator para incluir `dietary_compliance` check
   - Médio prazo: Adicionar pre-decision validation no Generator (verificar constraints antes de gerar)
   - Prevenção: Implementar sync-check que garante que toda constraint no perfil tem check correspondente na rubrica

### Resposta Exercício 2

1. **O que mudou:** `dietary_restrictions` na Trace B perdeu a restrição "no_gluten" que estava presente na Trace A.

2. **Bug!** É um caso de Context Amnesia seletiva — a restrição "vegan" sobreviveu mas "no_gluten" foi perdida.

3. **Padrão:** Context Amnesia (Padrão 2), subtipo Amnésia Seletiva (2c). Causa provável: o campo `dietary_restrictions` foi parcialmente sobrescrito por uma atualização que só incluía "vegan", removendo "no_gluten".

4. **Confirmação:** Verificar as traces entre 10:00 e 11:30 — em qual trace exata `dietary_restrictions` mudou de `["vegan", "no_gluten"]` para `["vegan"]`? Naquela trace, o que causou a mudança? Foi uma atualização de perfil mal feita?

### Resposta Exercício 3

**Plano de correção para Coordination Failure de Budget:**

1. **Padrão de recuperação:** Recuperação 4 (Correção Arquitetural) + Recuperação 1 (Hotfix por Feature Flag)

2. **Passos de implementação:**
   - **Hotfix imediato:** Adicionar validação cross-sprint — antes de recomendar, verificar se `budget_max` do contexto atual corresponde ao `sprint_contract.budget_max` do sprint ativo
   - **Correção estrutural:** Implementar versionamento de contrato com propagação síncrona:
     - Todo sprint contract tem `version` e `last_updated`
     - Ao iniciar sprint, o sistema lê o contrato diretamente da fonte (não de cache)
     - Se `version` do contrato no contexto != `version` da fonte → força refresh

3. **Validação:**
   - Re-executar as traces da sessão problemática com a correção
   - Confirmar que `budget_max` na decisão do Sprint 2 = R$ 100 (não R$ 200)
   - Rodar 1000 simulações com mudanças de budget entre sprints — 0% de propagation failure

4. **Prevenção:**
   - Adicionar alerta: se `decision.price > sprint_contract.max_budget * 1.0`, disparar WARNING mesmo que Evaluator aprove
   - Teste de regressão automatizado: simular mudança de budget entre sprints e verificar propagação
   - Dashboard: métrica "Cross-Sprint Contract Consistency" — deve permanecer em 100%

---

## 🎓 Resumo: O Que Você Aprendeu

Neste guia, você aprendeu a transformar uma trace — antes um bloco opaco de JSON — em uma janela de diagnóstico que revela exatamente o que aconteceu dentro do agente.

### Os 6 Padrões de Falha

Você agora consegue identificar e diagnosticar os 6 padrões de falha que cobrem 95% dos incidentes:

1. **Input Capture Failure** — quando o parser entende errado o que o cliente disse
2. **Context Amnesia** — quando o agente esquece informações críticas (o mais comum: 28%)
3. **Decision Contradiction** — quando a decisão ignora constraints que estão presentes
4. **Reasoning Collapse** — quando o raciocínio é frágil, circular ou de baixa confiança
5. **Evaluation Failure** — quando o gatekeeper aprova o que deveria rejeitar (ou vice-versa)
6. **Coordination Failure** — quando componentes individuais funcionam mas a interação falha

### As 6 Técnicas de Diagnóstico

Você domina 6 técnicas para extrair a verdade de qualquer trace:

1. **Análise Temporal** — reconstruir a timeline de eventos
2. **Data Lineage** — rastrear o caminho de um dado através do sistema
3. **ID Tracking** — verificar que cada decisão do Generator chegou corretamente ao Evaluator
4. **Contract Compliance** — validar que cada decisão respeita os contratos definidos
5. **Confidence Profiling** — identificar decisões frágeis antes que causem problemas
6. **Decision Diff** — comparar decisões para entender o que mudou e por quê

### O Sistema de Diagnóstico

Você entendeu como construir um pipeline completo de trace analysis:

- **Captura** → Toda decisão gera uma trace
- **Análise Automatizada** → Scripts detectam padrões conhecidos em < 100ms
- **Alertas** → Notificações proporcionais à severidade
- **Dashboard** → Visibilidade em tempo real da saúde do sistema
- **Ação Corretiva** → Correções rápidas para problemas simples, issues para problemas complexos

### A Aplicação Prática

Você sabe como o KODA usa trace analysis em produção:

- Pipeline que processa centenas de traces por dia
- Ferramentas CLI (`koda-trace-analyzer`) para diagnóstico manual
- Dashboard de qualidade com métricas em tempo real
- Processo de resposta a incidentes com SLAs de diagnóstico
- Métricas de qualidade que guiam melhorias contínuas

### O Checklist

Você tem um checklist prático de 6 fases que cobre desde a triagem inicial até a prevenção de recorrências. Na próxima vez que um alerta disparar, você não vai começar do zero — vai seguir o checklist.

---

### Para Onde Ir Agora

| Se você quer... | Próximo passo |
|---|---|
| **Praticar com mais exemplos** | Execute `koda-trace-analyzer` em traces reais do ambiente de staging |
| **Implementar trace analysis no seu sistema** | Comece pelo Trace Collector e Automated Analysis |
| **Aprender sobre padrões avançados** | Vá para `03-nivel-3-advanced-architecture/` |
| **Ver como traces se conectam com Gen/Eval** | Reveja `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` |
| **Contribuir com um novo padrão de falha** | Documente no canal #koda-quality com trace de exemplo |

---

### Uma Nota Final

Lembre-se do que Mariana descobriu no prólogo: o bug era uma linha de código — `LIMIT 1` em vez de `ORDER BY timestamp DESC LIMIT 1`. Mas sem a trace, ela teria passado dias procurando.

**A trace não resolve o bug. A trace torna o bug visível.**

E visibilidade é o primeiro passo para consertar qualquer coisa.

---

---

## 📚 Leitura Complementar

| Recurso | Onde Encontrar |
|---|---|
| Estrutura de traces e JSON schema | [`02-nivel-2-practical-patterns/04-trace-reading.md`](../02-nivel-2-practical-patterns/04-trace-reading.md) |
| Padrão Generator/Evaluator (base das traces) | [`02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`](../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md) |
| Sprint Contracts (validados nas traces) | [`02-nivel-2-practical-patterns/02-sprint-contracts.md`](../02-nivel-2-practical-patterns/02-sprint-contracts.md) |
| Rubric Design (rubricas do Evaluator) | [`02-nivel-2-practical-patterns/03-rubric-design.md`](../02-nivel-2-practical-patterns/03-rubric-design.md) |
| Glossário de termos técnicos | [`../GLOSSARY.md`](../GLOSSARY.md) |
| Script trace_analyzer.py (código fonte) | `scripts/trace_analyzer.py` no repositório KODA |

---

**Criado para a Equipe KODA**  
*Guia de Análise de Traces | v1.0 | Maio 2026*
