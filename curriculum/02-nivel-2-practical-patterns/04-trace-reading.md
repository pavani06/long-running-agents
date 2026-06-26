---
title: "Padrão Trace Reading: Transformando a Caixa-Preta em Glass Box"
type: curriculum-lesson
nivel: 2
aliases: ["leitura traces", "debug traces", "análise execução", "glass box"]
tags: [curriculo-conteudo, nivel-2, padroes-praticos, observabilidade, leitura-de-traces, logs-estruturados, rastreamento-de-decisoes, analise-de-falhas, diagnostico-de-bugs, linha-do-tempo, transparencia-arquitetural]
relates-to: ["[[docs/canonical/error-context-hygiene|Error Context Hygiene]]"]
last_updated: 2026-06-10
---
# 📊 Padrão Trace Reading: Transformando a Caixa-Preta em Glass Box
## Como Debugar Agentes Long-Running Através de Trails Completos de Decisão

**Tempo Estimado:** 120 minutos  
**Nível:** 2 - Padrões Práticos  
**Pré-requisito:** Ter completado Nível 1 + `01-generator-evaluator-pattern.md` + `02-sprint-contracts.md`  
**Status:** 🟢 PADRÃO CRÍTICO - Transforma Debug de "Impossível" para "5 Minutos"  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Conversa Que Perdemos

### O Começo: Esperança e Confiança

Era uma terça-feira. Um cliente novo entrou no WhatsApp do KODA com uma meta clara:

```
👤 Cliente: "Oi KODA! Tô querendo ganhar massa muscular. 
            Qual whey protein vocês recomendam?"

🤖 KODA: "Ótimo! Vou te ajudar. Primeiro, me fala:
         qual é seu sabor preferido?"

👤 Cliente: "Morango, com certeza. Tenho dificuldade 
            com sabores muito fortes."

🤖 KODA: "Perfeito! Encontrei a opção ideal para você:
         Whey Premium Morango - R$ 89,90
         ✅ Alta qualidade
         ✅ Sabor suave (como você prefere)
         ✅ Recomendado por nutricionistas"

👤 Cliente: "Ótimo! Vou comprar agora mesmo."

[Cliente compra. Satisfeito. Confiante no KODA.]
```

**Naquele momento, o cliente pensava:** *"Legal, esse agente realmente entendeu minha preferência."*

Ele nunca mais pensaria isso sobre o KODA.

---

### O Problema: A Mudança Que Ninguém Viu

Enquanto KODA preparava o pedido, o cliente teve um insight:

```
👤 Cliente: "Espera... meu nutricionista falou que 
            sabores mais intensos ajudam na absorção.
            Mudei de ideia. Prefiro sabor Chocolate 
            agora, que é mais forte."

🤖 KODA Generator: "Entendido! Vou buscar a opção 
                   de Chocolate Intenso para você.
                   
                   Whey Premium Chocolate Intenso - R$ 89,90
                   ✅ Sabor forte (como novo preferência)
                   ✅ Melhor absorção
                   ✅ Recomendado!"

👤 Cliente: "Perfeito! Essa é minha recomendação?"

🤖 KODA Evaluator: "Claro! Recomendo: 
                   Whey Premium Morango - R$ 89,90
                   
                   [Avaliar? ✅ Aprovado!]"
```

**O que aconteceu aqui?**

- ✅ **Generator viu corretamente:** Cliente mudou para Chocolate
- ❌ **Evaluator não viu a mudança:** Aprovou baseado na PRIMEIRA recomendação (Morango)
- ❌ **Resultado:** Cliente recebeu Morango quando esperava Chocolate

---

### O Calvário: Lendo JSON em Raw por 2 Horas

Quando o cliente reclamou, a equipe KODA entrou em pânico.

```
👤 Cliente: "KODA, recebi Morango, mas a ÚLTIMA 
            recomendação que você deu foi Chocolate!"

🤖 KODA (interno): "...ué? Que estranho. Deixa a 
                   gente revisar."
```

**O que se seguiu foi um calvário técnico:**

A equipe abriu o arquivo de logs bruto (JSON puro, não estruturado):

```json
[
  {
    "timestamp": "2026-05-15T14:32:00Z",
    "event": "user_message",
    "content": "Morango, com certeza. Tenho dificuldade com sabores muito fortes.",
    "type": "preference"
  },
  {
    "timestamp": "2026-05-15T14:35:00Z",
    "event": "generator_output",
    "recommendation": {
      "product": "Whey Premium Morango",
      "price": 89.90,
      "reasoning": "High quality, smooth flavor"
    },
    "status": "generated"
  },
  {
    "timestamp": "2026-05-15T14:37:00Z",
    "event": "user_message",
    "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
    "type": "preference_update"
  },
  {
    "timestamp": "2026-05-15T14:38:00Z",
    "event": "generator_output",
    "recommendation": {
      "product": "Whey Premium Chocolate Intenso",
      "price": 89.90,
      "reasoning": "Strong flavor, better absorption"
    },
    "status": "generated"
  },
  {
    "timestamp": "2026-05-15T14:40:00Z",
    "event": "evaluator_output",
    "decision": "APPROVE",
    "evaluated_recommendation": {
      "product": "Whey Premium Morango",
      "price": 89.90
    },
    "reasoning": "Quality product, matches preferences",
    "status": "approved"
  }
]
```

Vendo este JSON, a equipe KODA começou a investigar:

> *"Ok, vejo que o Generator recomendou Chocolate em 14:38. Mas qual foi a recomendação que o Evaluator realmente validou? Deixa procurar por 'evaluated_recommendation'... encontrei em 14:40... mas que diabos é 'Morango'? O Generator recomendou Chocolate!"*

Passaram **30 minutos** procurando por "Chocolate" no JSON.

Depois mais **20 minutos** tentando entender a sequência de eventos.

Depois mais **40 minutos** rodando a lógica do Evaluator manualmente pra ver onde errou.

**No total: 90 minutos de debug.**

No final, descobriram:

> *"Aaah, achamos! O Evaluator olhou para o histórico de recomendações, e por algum motivo, capturou a PRIMEIRA recomendação (Morango) em vez da ÚLTIMA (Chocolate). Deve ser um bug na forma como a gente passa o contexto pro Evaluator."*

---

### O Custo: Cliente Perdido, Confiança Abalada

Quando a equipe KODA explicou o que aconteceu, o cliente ficou furioso:

```
👤 Cliente: "Vocês estão me dizendo que levou 90 
            minutos para vocês MESMOS descobrir 
            um erro no próprio sistema?
            
            Se vocês não conseguem nem ler o chat 
            de vocês mesmos, como vou confiar em 
            recomendações sobre suplementos?
            
            Não quero mais usar KODA."
```

**Os números:**
- ❌ Cliente perdido (nunca mais voltou)
- ❌ Avaliação 1⭐ deixada
- ❌ Produto enviado de graça: R$ 89,90
- ❌ Horas de engenheiro debugando: 2h
- ❌ Reputação abalada: "Se KODA não consegue debugar a si mesmo, como pode recomendações médicas?"

---

### O Insight: "Se Tivéssemos Uma Trace..."

Uma semana depois, a equipe KODA estava em uma reunião de postmortem.

Um dos engenheiros falou algo que ecoou pela sala:

> *"Gente, sabe qual era o problema? Não era o Evaluator estar bugado. O Evaluator simplesmente não tinha **visibilidade** de qual era a recomendação mais recente do Generator."*
>
> *"Se tivéssemos uma TRACE estruturada — um registro limpo que dissesse explicitamente 'Generator recomendou X em tempo T1, Evaluator recebeu X ou Y em tempo T2?' — teríamos achado a resposta em **30 segundos**, não em 2 horas."*

E aí veio a realização devastadora:

> *"...e isso vai acontecer novamente. E novamente. E novamente."*
>
> *"Toda vez que um agente errar, vamos estar aqui, desesperados, lendo JSON em raw, tentando reconstituir o que aconteceu."*

**Naquele momento, ficou claro:**

Não é que o KODA seja ruim. É que o **KODA é invisível**.

A lógica está funcionando. As decisões estão sendo feitas. Mas **não há janela** para ver o que está acontecendo dentro.

---

### A Ponte: Do Black Box ao Glass Box

Essa conversa perdida não foi um bug. Foi um **sinal de alerta**.

O sinal de alerta dizia: *"Você precisa de visibilidade estruturada. Agora."*

**E é isso que você vai aprender neste módulo.**

Você vai aprender a criar **Traces completas e estruturadas** que tornam o invisível visível. Traces que permitem que você:

✅ Debug um erro em **30 segundos** em vez de 2 horas  
✅ Veja exatamente **quando** e **onde** uma informação se perdeu  
✅ Entenda **por quê** cada decisão foi tomada  
✅ Confie no KODA porque você consegue **verificar** o que ele fez  

E mais importante: **evitar que essa conversa seja perdida novamente.**

---

## 🎯 O Problema Fundacional

Você aprendeu em Nível 2 sobre dois padrões poderosos:

- **Generator/Evaluator (Doc 01):** Separa criação de validação para garantir qualidade
- **Sprint Contracts (Doc 02):** Define acordos claros entre agente e cliente para evitar contradições

No caso do Prólogo, AMBOS os padrões foram implementados. Generator viu a mudança de preferência. Evaluator aprovou uma recomendação.

**Mas ainda assim, o cliente recebeu a recomendação errada.**

Por quê?

Porque **ambos os padrões foram implementados, mas sem visibilidade interna.**

---

### Por Que Generator/Evaluator Sem Visibilidade Falha

Vamos dissecar exatamente o que aconteceu no Prólogo usando o padrão Gen/Eval:

**Generator (funcionamento correto):**
```
Input: "Cliente prefere Chocolate agora"
↓
Generator Process: "Ok, mudança registrada. Vou buscar Chocolate Intenso"
↓
Output: {
  "recommendation": "Whey Premium Chocolate Intenso",
  "reasoning": "Strong flavor, better absorption as requested",
  "timestamp": "2026-05-15T14:38:00Z"
}
```

Generator **viu corretamente** a mudança. Fez seu trabalho.

**Evaluator (onde tudo quebrou):**
```
Input para Evaluator: ??? 

Qual foi o input?
- A recomendação mais RECENTE (Chocolate)?
- A recomendação mais ANTIGA (Morango)?
- Ambas?
- O "contexto correto" (preferência atual do cliente)?

Ninguém sabe.
```

Esse é o problema.

O Generator criou uma recomendação correta. Mas **o que foi passado pro Evaluator?**

No caso do Prólogo, foi passado **o sabor que o agente havia oferecido inicialmente** (Morango), não **o sabor que o cliente pediu depois** (Chocolate).

Isso não foi intencional. Foi um **bug de context management** entre Generator e Evaluator.

Mas como você descobre isso? Como você **verifica** o que o Evaluator realmente viu?

**Sem uma trace estruturada, você não consegue.**

Você fica fazendo perguntas no escuro:
- "O Evaluator viu a primeira recomendação ou a segunda?"
- "O Evaluator sabia que era a versão FINAL?"
- "Qual foi o exato contexto que chegou no Evaluator?"

---

### O Que O Evaluator Precisava Ver (Mas Não Viu)

Em um cenário ideal, a trace passada pro Evaluator seria assim:

```json
{
  "evaluation_request": {
    "timestamp": "2026-05-15T14:38:00Z",
    "generator_id": "gen-12345",
    "generation_id": "rec-67890",
    "status": "FINAL",
    "recommendation": {
      "product": "Whey Premium Chocolate Intenso",
      "price": 89.90,
      "reasoning": "Strong flavor, better absorption"
    },
    "context_used_by_generator": {
      "user_preference_current": "Chocolate",
      "user_preference_timestamp": "2026-05-15T14:37:00Z",
      "user_goal": "Gain muscle mass",
      "constraints": "Strong flavor preferred"
    }
  }
}
```

**Com isso, o Evaluator poderia:**
- ✅ Ver o `status: "FINAL"` e saber que não há recomendação mais recente
- ✅ Ver a `generation_id` única para esta recomendação
- ✅ Ver o timestamp exato quando foi gerada
- ✅ Comparar com a preferência atual do cliente ("Chocolate")
- ✅ Validar que está tudo alinhado

**Mas sem uma trace, o Evaluator recebe:**
- ❌ Um objeto JSON solto
- ❌ Sem context de qual foi o "input" que gerou
- ❌ Sem garantia de que é a recomendação FINAL
- ❌ Sem timestamp para comparar com quando a preferência mudou
- ❌ Sem como verificar se o "contexto correto" foi usado

E aprova baseado no que consegue adivinhar.

---

### Por Que Sprint Contracts Sem Traces Não É Suficiente

Sprint Contracts (documento anterior) estabelece um **contrato claro** entre agente e cliente:

```
CONTRATO DO SPRINT 1 (Descobrir Produtos)
═══════════════════════════════════════════
✅ Orçamento máximo: R$ 100
✅ Apenas produtos veganos (100%)
✅ Preferência de sabor: será definida pelo cliente
✅ Tempo máximo: 10 minutos
```

Isso é excelente. Define expectativas. Evita gaslighting.

**MAS:** Como você **verifica** que o contrato foi respeitado durante a execução?

Hoje, a única forma é:
1. Conversa termina
2. Cliente reclama (ou não)
3. Você abre o histórico WhatsApp
4. **Lê manualmente** o chat inteiro
5. Procura por "orçamento", "vegano", "sabor"
6. Tenta reconstituir se o contrato foi respeitado

Isso é **retrospectivo**. Você descobre a violação DEPOIS.

---

### Exemplos KODA de Violação de Contrato

**Exemplo 1: Orçamento Violado**
```
Contrato: "Máximo R$ 100"
Cliente pediu: "Whey protein para ganhar músculo"

Generator recomendou: "Whey Premium Elite - R$ 150"
Evaluator aprovou: ✅

Cliente: "MAS VOCÊS FALARAM QUE ERA ATÉ R$ 100!"

Investigação manual: 2 horas para achar que o agente ESQUECEU
do contrato entre Sprint 1 e Sprint 2.
```

**Exemplo 2: Restrição Ignorada**
```
Contrato: "Apenas produtos 100% veganos"
Cliente pediu: "Preciso de proteína vegana"

Generator recomendou: "Plant Whey (com alguns aditivos derivados de soro)"
Evaluator aprovou: ✅ "É vegano"

Cliente descobriu depois: "Isso não é 100% vegano!"

Investigação: Qual foi o "contexto" que o Evaluator viu? Ele sabia
que a restrição era "100%"? Ou leu só "vegano"?
Sem trace: Impossível saber.
```

**Por que sem trace isso é impossível de detectar rápido?**

Porque o contrato está em um **banco de dados separado** (Sprint Contracts), e a **execução está em outro lugar** (logs de chat).

Você tem que:
1. Puxar o contrato
2. Puxar os logs
3. Manualmente comparar
4. Adivinhar quando/onde o contrato foi violado

**Com trace completa:**
Cada decisão do agente estaria ligada ao contrato original. Você veria EXATAMENTE quando uma recomendação violou um termo.

---

### A Caixa-Preta de Decisões

Aqui está a ironia mais dura:

Você implementou Generator/Evaluator com rigor. Você implementou Sprint Contracts com clareza. **Sua arquitetura é sólida.**

Mas do ponto de vista do **cliente**, o KODA ainda parece:

> *"Um agente bem-intencionado, mas que comete **erros básicos** que não conseguem resolver. Um sistema que foi trabalhado, mas ainda tem bugs fundamentais."*

O cliente não vê:
- ✅ Que o Generator está funcionando corretamente
- ✅ Que há um Evaluator fazendo validação
- ✅ Que há um contrato definido

O cliente vê:
- ❌ "Recomendou Morango quando pedi Chocolate"
- ❌ "Disseram que era até R$ 100, recomendaram R$ 150"
- ❌ "Falaram 100% vegano, recomendaram com aditivos"

E pensa: *"Isso parece um LLM com problema. Não confio mais."*

Porque **sem visibilidade interna, padrões bem desenhados parecem bugs mal corrigidos.**

---

### A Equação da Invisibilidade

```
Padrão Bem Desenhado + Visibilidade = Confiança
├─ Cliente vê a decisão
├─ Você consegue explicar a decisão
├─ Você consegue debugar rapidamente
└─ Você consegue melhorar

Padrão Bem Desenhado + Invisibilidade = Desconfiança
├─ Cliente vê só o resultado (errado)
├─ Você não consegue explicar por quê
├─ Você gasta 2 horas debugando
└─ Você não consegue melhorar (não vê o que quebrou)
```

E é nessa invisibilidade que vivemos hoje.

---

### A Solução: Traces Estruturadas

O que falta não é **padrão melhor**. O padrão está bom.

O que falta é **janela de visibilidade**.

Você precisa de uma **trace completa e estruturada** que captura:

✅ **O que entrou** (user input, preferences, constraints)  
✅ **O que o agente sabia** (context naquele momento)  
✅ **Como foi a decisão** (qual foi o raciocínio)  
✅ **O que foi feito** (a saída, a ação)  
✅ **Quando tudo isso aconteceu** (timestamps para correlacionar)  

Com isso, você transforma a caixa-preta em um **glass box** onde cada decisão é visível, rastreável e verificável.

E quando algo dá errado, você não fica no escuro. Você tem a trace. Você sabe exatamente onde procurar. **30 segundos, não 2 horas.**

---

## 📐 Padrão: Estrutura de Trace Completa

### O que é uma Trace?

Pense em uma **trace** como um **registro de voo de um avião**.

Quando um avião voa, ele registra continuamente:
- **Altitude atual** (onde está agora?)
- **Velocidade** (como está se movendo?)
- **Direção** (para onde vai?)
- **Combustível** (quais são os recursos?)
- **Decisões do piloto** (por que fez essa manobra?)
- **Temperatura externa** (qual é o contexto?)

Se algo dá errado, a caixa-preta (flight data recorder) tem tudo. Investigators conseguem reconstruir EXATAMENTE o que aconteceu.

**Uma trace de agente é a mesma coisa.**

É um registro estruturado que captura:
- Cada **input** que o agente recebeu
- O **contexto** que o agente tinha naquele momento
- A **decisão** que o agente tomou
- O **raciocínio** por trás da decisão
- O **output** que o agente produziu
- **Quando** tudo isso aconteceu (timestamps)

Com a trace, você consegue **reconstruir a decisão**, não o voo.

---

### JSON Schema Completo

Aqui está a estrutura completa de uma trace bem-formada em Node.js:

```json
{
  "trace_id": "trace-550e8400-e29b-41d4-a716-446655440000",
  "session_id": "session-client-12345",
  "timestamp": "2026-05-15T14:38:00Z",
  "agent_name": "KODA",
  "agent_version": "2.1.0",
  
  "phase": {
    "sprint_number": 1,
    "sprint_name": "Discover Products",
    "sprint_contract": {
      "contract_id": "contract-sprint-1-12345",
      "max_budget": 100.00,
      "constraints": ["only_vegan", "muscle_gain_goal"],
      "duration_minutes": 10
    }
  },

  "input": {
    "type": "user_message",
    "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
    "timestamp": "2026-05-15T14:37:00Z",
    "user_id": "user-98765",
    "message_id": "msg-789456",
    "intent_detected": "preference_update",
    "entities_extracted": {
      "flavor_preference": "Chocolate",
      "intensity": "strong"
    }
  },

  "context": {
    "conversation_history": [
      {
        "timestamp": "2026-05-15T14:32:00Z",
        "role": "user",
        "message": "Morango, com certeza. Tenho dificuldade com sabores muito fortes.",
        "extracted_preference": {
          "flavor": "Morango",
          "intensity_preference": "suave"
        }
      },
      {
        "timestamp": "2026-05-15T14:37:00Z",
        "role": "user",
        "message": "Mudei de ideia. Prefiro sabor Chocolate agora.",
        "extracted_preference": {
          "flavor": "Chocolate",
          "intensity_preference": "strong"
        }
      }
    ],
    "current_user_profile": {
      "goal": "gain_muscle_mass",
      "budget_max": 100.00,
      "dietary_restrictions": ["vegan"],
      "flavor_preference_current": "Chocolate",
      "flavor_preference_timestamp": "2026-05-15T14:37:00Z",
      "flavor_preference_previous": "Morango",
      "flavor_preference_previous_timestamp": "2026-05-15T14:32:00Z"
    },
    "available_products": [
      {
        "id": "prod-001",
        "name": "Whey Premium Morango",
        "price": 89.90,
        "flavor": "Morango",
        "vegan": false
      },
      {
        "id": "prod-002",
        "name": "Whey Premium Chocolate Intenso",
        "price": 89.90,
        "flavor": "Chocolate",
        "intensity": "strong",
        "vegan": false
      }
    ]
  },

  "decision": {
    "agent_role": "generator",
    "generator_id": "gen-12345",
    "generation_id": "rec-67890",
    "decision_type": "product_recommendation",
    "decision_status": "FINAL",
    "recommendation": {
      "product_id": "prod-002",
      "product_name": "Whey Premium Chocolate Intenso",
      "price": 89.90,
      "flavor": "Chocolate",
      "reasoning_key_factors": [
        "matches_current_user_preference",
        "within_budget",
        "strong_flavor_as_requested"
      ]
    }
  },

  "reasoning": {
    "thought_process": [
      {
        "step": 1,
        "reasoning": "User explicitly changed preference from Morango to Chocolate at 2026-05-15T14:37:00Z"
      },
      {
        "step": 2,
        "reasoning": "Client has muscle gain goal, strong flavors aid absorption per latest research"
      },
      {
        "step": 3,
        "reasoning": "Whey Premium Chocolate Intenso matches: flavor preference, budget (R$ 89.90 < R$ 100), goal"
      },
      {
        "step": 4,
        "reasoning": "This is the FINAL recommendation for this sprint"
      }
    ],
    "confidence_score": 0.95,
    "alternative_considered": [
      {
        "product": "Whey Premium Morango",
        "why_rejected": "User explicitly changed preference away from this"
      }
    ]
  },

  "output": {
    "type": "recommendation",
    "content": "Whey Premium Chocolate Intenso - R$ 89,90",
    "formatted_for_user": "Perfeito! Vou buscar a opção de Chocolate Intenso para você.\n\nWhey Premium Chocolate Intenso - R$ 89,90\n✅ Sabor forte (como sua nova preferência)\n✅ Melhor absorção\n✅ Recomendado!",
    "timestamp": "2026-05-15T14:38:00Z"
  },

  "evaluation": {
    "evaluator_id": "eval-54321",
    "evaluation_id": "eval-12345",
    "timestamp_received": "2026-05-15T14:40:00Z",
    "recommendation_received": {
      "generation_id": "???",
      "product_name": "???"
    },
    "evaluation_result": "APPROVED",
    "evaluation_confidence": 0.85,
    "checks_performed": [
      {
        "check": "budget_compliance",
        "result": "PASS",
        "detail": "R$ 89.90 <= R$ 100"
      },
      {
        "check": "dietary_compliance",
        "result": "PASS",
        "detail": "Product matches vegan requirement"
      },
      {
        "check": "goal_alignment",
        "result": "PASS",
        "detail": "Matches muscle gain goal"
      }
    ],
    "evaluation_reasoning": "Quality product, matches preferences",
    "timestamp_approval": "2026-05-15T14:40:00Z"
  },

  "metadata": {
    "trace_version": "1.0",
    "environment": "production",
    "latency_ms": {
      "generator_latency": 800,
      "evaluator_latency": 450,
      "total_decision_latency": 1250
    },
    "error_flags": [],
    "warnings": []
  }
}
```

---

#### Os 7 Componentes Explicados

**1️⃣ Header da Trace:**
```json
{
  "trace_id": "trace-550e8400-e29b-41d4-a716-446655440000",
  "session_id": "session-client-12345",
  "timestamp": "2026-05-15T14:38:00Z"
}
```
**Por que?** Identificação única + Link com sessão do cliente + Timestamp exato.

**2️⃣ Phase (Sprint Contract):**
```json
{
  "phase": {
    "sprint_number": 1,
    "sprint_contract": {
      "max_budget": 100.00,
      "constraints": ["only_vegan", "muscle_gain_goal"]
    }
  }
}
```
**Por que?** Qual contrato deveria ter sido respeitado? Compare depois com a decisão.

**3️⃣ Input (O que entrou?):**
```json
{
  "input": {
    "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
    "intent_detected": "preference_update",
    "entities_extracted": {
      "flavor_preference": "Chocolate"
    }
  }
}
```
**Por que?** Exatamente o que o cliente disse + O que foi entendido.

**4️⃣ Context (O que o agente sabia?):**
```json
{
  "context": {
    "current_user_profile": {
      "flavor_preference_current": "Chocolate",
      "flavor_preference_timestamp": "2026-05-15T14:37:00Z",
      "flavor_preference_previous": "Morango"
    }
  }
}
```
**Por que?** Qual era o "conhecimento" do agente naquele momento?

**5️⃣ Decision (Qual foi a escolha?):**
```json
{
  "decision": {
    "generation_id": "rec-67890",
    "decision_status": "FINAL",
    "recommendation": {
      "product_name": "Whey Premium Chocolate Intenso"
    }
  }
}
```
**Por que?** A decisão específica + ID único (crucial para comparar com Evaluator).

**6️⃣ Reasoning (Por quê?):**
```json
{
  "reasoning": {
    "thought_process": [
      {
        "step": 1,
        "reasoning": "User explicitly changed preference from Morango to Chocolate"
      }
    ],
    "confidence_score": 0.95
  }
}
```
**Por que?** Entender como o agente pensou (e se errou).

**7️⃣ Evaluation (O Evaluator viu tudo isto?):**
```json
{
  "evaluation": {
    "recommendation_received": {
      "generation_id": "???",
      "product_name": "???"
    }
  }
}
```
**Por que?** **AQUI é onde você descobre o erro do Prólogo em 30 segundos!**
- Se `generation_id` no Evaluation ≠ `generation_id` no Decision → **BUG ENCONTRADO**

---

### Pontos Críticos de Captura

**Onde você registra esses dados?**

| Ponto | O que registrar | Quando |
|-------|-----------------|--------|
| **1** | Input + Timestamp | Logo após cliente enviar mensagem |
| **2** | Context (perfil, histórico, produtos) | Antes do Generator pensar |
| **3** | Decision + ID único + "FINAL" status | Quando Generator cria recomendação |
| **4** | Reasoning (passos de pensamento) | Durante geração (capture de logs) |
| **5** | Qual generation_id o Evaluator RECEBEU | Quando Evaluator inicia avaliação |
| **6** | Evaluation result + checks | Quando Evaluator aprova/rejeita |
| **7** | Output final + Timestamp | Quando cliente recebe resposta |

---

### Exemplo Prático: Debug em 30 Segundos

**Sem trace (Prólogo):**
```bash
# Você está perdido
"Por que o cliente recebeu Morango em vez de Chocolate?"
# 90 minutos de investigação manual
```

**Com trace estruturada:**
```bash
$ cat trace-client-12345.json | jq '.evaluation.recommendation_received'
{
  "generation_id": "rec-64321",
  "product_name": "Whey Premium Morango"
}

$ cat trace-client-12345.json | jq '.decision.generation_id'
"rec-67890"

# ⚠️ MISMATCH!
# Generator criou rec-67890 (Chocolate)
# Evaluator recebeu rec-64321 (Morango)
# BUG: Qual recomendação chegou ao Evaluator? A errada!
```

**Tempo: 30 segundos. Resposta clara. Bug identificado.**

---

### Resumo: Uma Trace Bem-Formada Oferece

✅ **Rastreabilidade** — Cada decisão tem ID único  
✅ **Auditoria** — Veja o pensamento passo-a-passo  
✅ **Contrato Compliance** — Compare com Sprint Contracts  
✅ **Debug Rápido** — 30 segundos, não 2 horas  
✅ **Validação G/E** — Veja se Evaluator recebeu contexto correto  
✅ **Melhoria Contínua** — Patterns de erro ficam visíveis  

Tudo isso em um JSON estruturado, consultável, automatizável.

---

## 🔍 Anatomy of a Trace: Como Ler Manualmente

Você recebeu uma trace. Um cliente reclamou. Você quer debugar.

**Como você lê uma trace estruturada?**

Aqui está o passo-a-passo que funciona tanto para devs quanto para PMs.

---

### Passo 1: Ler o Input (O que entrou?)

**Onde procurar:**
```json
"input": {
  "type": "user_message",
  "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
  "timestamp": "2026-05-15T14:37:00Z",
  "intent_detected": "preference_update",
  "entities_extracted": {
    "flavor_preference": "Chocolate",
    "intensity": "strong"
  }
}
```

**O que você está verificando:**

1. ✅ **O cliente realmente disse isso?**
   - Leia o campo `content` — é a mensagem EXATA que entrou
   - Compare com o histórico do WhatsApp se necessário

2. ✅ **Quando entrou?**
   - Campo `timestamp` — hora exata
   - Se o cliente diz "mudei de ideia" às 14:37, mas a ação foi às 14:40, há um delay de 3 minutos
   - Isso importa se houver múltiplas mudanças rápidas

3. ✅ **O agente entendeu corretamente?**
   - Campo `intent_detected` — qual foi o entendimento?
   - Campo `entities_extracted` — quais dados foram extraídos?
   - Se o cliente falou "Chocolate" e `flavor_preference` = "Chocolate" ✅
   - Se o cliente falou "Chocolate" e `flavor_preference` = "Morango" ❌ **RED FLAG**

4. ✅ **E se o campo estiver vazio ou nulo?**
   - Se `content` está vazio → O agente não recebeu a mensagem
   - Se `intent_detected` está vazio → O NLU (processamento de linguagem) falhou
   - Se `entities_extracted` está vazio → O agente não extraiu nenhuma informação
   - **Nesses casos, o problema começou AQUI, não depois**

**Exemplo de Input BOM:**
```json
✅ {
  "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
  "intent_detected": "preference_update",
  "entities_extracted": {
    "flavor_preference": "Chocolate"
  }
}
```

**Exemplo de Input RUIM:**
```json
❌ {
  "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
  "intent_detected": null,  // ← NLU falhou!
  "entities_extracted": {}
}
```

---

### Passo 2: Ler o Context (O que o agente sabia?)

**Onde procurar:**
```json
"context": {
  "current_user_profile": {
    "flavor_preference_current": "Chocolate",
    "flavor_preference_timestamp": "2026-05-15T14:37:00Z",
    "flavor_preference_previous": "Morango",
    "flavor_preference_previous_timestamp": "2026-05-15T14:32:00Z"
  },
  "conversation_history": [...]
}
```

**O que você está verificando:**

1. ✅ **O agente tinha a informação mais RECENTE?**
   - Compare `flavor_preference_current` com o input
   - Se input diz "Chocolate" em 14:37:00Z
   - E `flavor_preference_current` = "Chocolate" com timestamp 14:37:00Z ✅
   - Significao agente sabia da mudança

2. ✅ **Há histórico de mudanças?**
   - Campo `flavor_preference_previous` mostra a preferência anterior
   - Se há múltiplas mudanças, o agente conhece o histórico completo ✅
   - Se só há a preferência atual, o agente não tem contexto histórico ❌

3. ✅ **O contexto estava atualizado no momento certo?**
   - Timestamp do Input: 14:37:00Z
   - Timestamp do Context: Deve ser ≥ 14:37:00Z
   - Se Context tem timestamp 14:35:00Z (mais antigo) → **PROBLEMA: contexto desatualizado**

4. ✅ **E se campos estão vazios ou nulos?**
   - Se `flavor_preference_current` é nulo → Agente não sabe qual é a preferência AGORA
   - Se `conversation_history` está vazio → Agente não tem contexto de conversa anterior
   - Se `current_user_profile` está vazio → **SERIOUS: Agente está cego**
   - **Nestes casos, o Generator tomou uma decisão sem informação essencial**

**Exemplo de Context BOM:**
```json
✅ {
  "flavor_preference_current": "Chocolate",
  "flavor_preference_timestamp": "2026-05-15T14:37:00Z",
  "flavor_preference_previous": "Morango",
  "conversation_history": [
    { "timestamp": "14:32", "preference": "Morango" },
    { "timestamp": "14:37", "preference": "Chocolate" }
  ]
}
```

**Exemplo de Context RUIM:**
```json
❌ {
  "flavor_preference_current": null,  // ← Agente não sabe!
  "flavor_preference_timestamp": null,
  "conversation_history": []  // ← Sem histórico!
}
```

---

### Passo 3: Ler o Decision (Qual foi a escolha?)

**Onde procurar:**
```json
"decision": {
  "generation_id": "rec-67890",
  "decision_status": "FINAL",
  "recommendation": {
    "product_name": "Whey Premium Chocolate Intenso",
    "price": 89.90,
    "flavor": "Chocolate"
  }
}
```

**O que você está verificando:**

1. ✅ **Qual foi a decisão exata?**
   - Campo `product_name` — qual produto foi escolhido?
   - Leia com cuidado — "Chocolate Intenso" é diferente de "Chocolate Suave"

2. ✅ **Tem um ID único?**
   - Campo `generation_id` → "rec-67890"
   - **CRÍTICO:** Este ID é importante para comparar com o que o Evaluator recebeu depois
   - Se Decision tem `generation_id: "rec-67890"` mas Evaluation tem `generation_id: "rec-64321"` → **MISMATCH!**

3. ✅ **É a FINAL?**
   - Campo `decision_status`
   - Se = "FINAL" → Esta é a recomendação que deve ir pro cliente
   - Se = "DRAFT" ou "PENDING" → Pode haver outra recomendação depois
   - Se = null → **AMBÍGUO: é final ou não?**

4. ✅ **E se campos estão vazios ou nulos?**
   - Se `product_name` é nulo → Generator não conseguiu encontrar produto
   - Se `generation_id` é nulo → **BIG PROBLEM: Sem ID, você não consegue rastrear se Evaluator viu ISTO ou AQUILO**
   - Se `decision_status` é nulo → Você não sabe se é final ou preliminar
   - **Qualquer um desses é um problema sério**

**Exemplo de Decision BOM:**
```json
✅ {
  "generation_id": "rec-67890",
  "decision_status": "FINAL",
  "product_name": "Whey Premium Chocolate Intenso",
  "price": 89.90
}
```

**Exemplo de Decision RUIM:**
```json
❌ {
  "generation_id": null,  // ← SEM RASTREAMENTO!
  "decision_status": "DRAFT",  // ← NÃO FINAL!
  "product_name": null  // ← VAZIO!
}
```

---

### Passo 4: Ler o Reasoning (Por quê?)

**Onde procurar:**
```json
"reasoning": {
  "thought_process": [
    {
      "step": 1,
      "reasoning": "User explicitly changed preference from Morango to Chocolate"
    },
    {
      "step": 2,
      "reasoning": "Client has muscle gain goal, strong flavors aid absorption"
    }
  ],
  "confidence_score": 0.95,
  "alternative_considered": [
    {
      "product": "Whey Premium Morango",
      "why_rejected": "User explicitly changed preference away from this"
    }
  ]
}
```

**O que você está verificando:**

1. ✅ **O raciocínio faz sentido?**
   - Leia `thought_process` passo-a-passo
   - "Step 1: User changed preference" ✅ Faz sentido
   - "Step 2: Strong flavors aid absorption" ✅ Faz sentido
   - Resultado: Chocolate Intenso ✅ Logicamente consistente

2. ✅ **O agente considerou alternativas?**
   - Campo `alternative_considered`
   - Se mostra "consideramos Morango mas rejeitamos porque user mudou" ✅ Bom raciocínio
   - Se está vazio → Agente não considerou alternativas (pode ser problema ou não)

3. ✅ **Qual é a confiança?**
   - Campo `confidence_score`
   - Se = 0.95 (95%) → Agente tem muita confiança
   - Se = 0.60 (60%) → Agente tem dúvida, mas ainda assim recomendou
   - Se está vazio ou muito baixo (< 0.5) → **RED FLAG: Decisão com pouca confiança**

4. ✅ **E se campos estão vazios ou nulos?**
   - Se `thought_process` está vazio → Agente não explicou seu pensamento (opaco!)
   - Se `confidence_score` é nulo → Não se sabe se agente tinha certeza
   - Se `alternative_considered` está vazio → Agente tomou decisão sem avaliar alternativas
   - **Nestes casos, você está no escuro sobre o "por quê" da decisão**

**Exemplo de Reasoning BOM:**
```json
✅ {
  "thought_process": [
    { "step": 1, "reasoning": "User changed preference to Chocolate" },
    { "step": 2, "reasoning": "Chocolate matches budget and goal" }
  ],
  "confidence_score": 0.95,
  "alternative_considered": [
    { "product": "Morango", "why_rejected": "User changed preference away" }
  ]
}
```

**Exemplo de Reasoning RUIM:**
```json
❌ {
  "thought_process": [],  // ← SEM EXPLICAÇÃO!
  "confidence_score": 0.45,  // ← MUITO BAIXA!
  "alternative_considered": null  // ← NÃO CONSIDEROU ALTERNATIVAS!
}
```

---

### Passo 5: Ler o Output (Qual foi o resultado?)

**Onde procurar:**
```json
"output": {
  "type": "recommendation",
  "content": "Whey Premium Chocolate Intenso - R$ 89,90",
  "formatted_for_user": "Perfeito! Vou buscar a opção...",
  "timestamp": "2026-05-15T14:38:00Z"
}
```

**O que você está verificando:**

1. ✅ **Qual foi a mensagem que o cliente recebeu?**
   - Campo `formatted_for_user` — isto é o que o cliente VIU
   - Compara com a reclamação do cliente: "Recebi Morango" vs "Recebi Chocolate"?
   - Se o cliente diz "recebi Morango" mas `formatted_for_user` mostra "Chocolate" → **Problema no sistema de fulfillment, não na IA**

2. ✅ **Quando foi enviado?**
   - Campo `timestamp`
   - Compara com quando o cliente fez a reclamação
   - Se cliente reclamou em 15:30 e output foi em 14:38, há várias horas de diferença (pode haver múltiplas recomendações)

3. ✅ **Qual é o tipo?**
   - Campo `type`
   - "recommendation" é o esperado
   - Se é "error" ou "no_result" → Agente falhou em encontrar algo

4. ✅ **E se campos estão vazios ou nulos?**
   - Se `formatted_for_user` é nulo → Mensagem não foi formatada (que o cliente viu?)
   - Se `timestamp` é nulo → Você não sabe QUANDO isso foi enviado (crítico para timeline)
   - Se `content` é nulo → **PROBLEMA: Não há conteúdo de output**
   - **Qualquer um destes significa que o cliente pode ter recebido "nada" ou algo incompleto**

**Exemplo de Output BOM:**
```json
✅ {
  "type": "recommendation",
  "formatted_for_user": "Whey Premium Chocolate Intenso - R$ 89,90\n✅ Sabor forte...",
  "timestamp": "2026-05-15T14:38:00Z"
}
```

**Exemplo de Output RUIM:**
```json
❌ {
  "type": null,  // ← TIPO NÃO DEFINIDO!
  "formatted_for_user": null,  // ← SEM MENSAGEM!
  "timestamp": null  // ← SEM TIMESTAMP!
}
```

---

### Passo 6 (Bonus): Ler o Evaluation (O Evaluator Viu Tudo?)

**Onde procurar:**
```json
"evaluation": {
  "evaluator_id": "eval-54321",
  "timestamp_received": "2026-05-15T14:40:00Z",
  "recommendation_received": {
    "generation_id": "???",
    "product_name": "???"
  },
  "evaluation_result": "APPROVED",
  "checks_performed": [
    {
      "check": "budget_compliance",
      "result": "PASS"
    }
  ]
}
```

**O que você está verificando:**

1. ✅ **Qual foi a recomendação que o Evaluator RECEBEU?**
   - Campo `recommendation_received.generation_id`
   - **COMPARA com `decision.generation_id`**
   - Se forem iguais ✅
   - Se forem diferentes ❌ **MISMATCH: Evaluator viu recomendação diferente!**

2. ✅ **O Evaluator aprovou ou rejeitou?**
   - Campo `evaluation_result`
   - "APPROVED" = passou nos checks
   - "REJECTED" = não passou
   - Se "APPROVED" mas havia problemas óbvios → Evaluator falhou

3. ✅ **Quais checks foram feitos?**
   - Campo `checks_performed`
   - Se inclui `budget_compliance`, `dietary_constraints`, `goal_alignment` ✅
   - Se está vazio → **PROBLEMA: Evaluator não fez nenhuma verificação!**

4. ✅ **E se campos estão vazios?**
   - Se `recommendation_received` está vazio → Evaluator não sabe o que está avaliando
   - Se `checks_performed` está vazio → Nenhuma validação foi feita
   - Se `evaluation_result` está vazio → Você não sabe se foi aprovado ou rejeitado
   - **Isto significa Evaluator era um "rubber stamp" que aprovava tudo**

---

## 🚨 Red Flags: Sinais de Alerta

Quando você está lendo uma trace, procure por estes padrões problemáticos:

### ❌ Red Flag 1: Timestamps Inconsistentes

```json
"input": { "timestamp": "2026-05-15T14:37:00Z" },
"decision": { "timestamp": "2026-05-15T14:36:00Z" }  // ← ANTES do input!
```

**O que significa:** A decisão foi tomada ANTES do input? Impossível!  
**Possível causa:** Bug no sistema de logging, ou ordem de eventos incorreta.

---

### ❌ Red Flag 2: Preference Mudou Mas Generator Não Viu

```json
"input": {
  "content": "Mudei para Chocolate",
  "entities_extracted": { "flavor": "Chocolate" }
},
"context": {
  "flavor_preference_current": "Morango"  // ← ANTIGA!
},
"decision": {
  "product_name": "Whey Premium Morango"  // ← USA PREFERÊNCIA ANTIGA!
}
```

**O que significa:** O input foi capturado, mas o context não foi atualizado.  
**Possível causa:** Context está desatualizado, há lag entre input e processamento.

---

### ❌ Red Flag 3: Evaluator Recebeu Recomendação Diferente

```json
"decision": {
  "generation_id": "rec-67890",
  "product_name": "Whey Premium Chocolate"
},
"evaluation": {
  "recommendation_received": {
    "generation_id": "rec-64321",  // ← DIFERENTE!
    "product_name": "Whey Premium Morango"
  }
}
```

**O que significa:** Generator criou uma coisa, mas Evaluator viu outra.  
**Possível causa:** Bug na forma como a recomendação foi passada pro Evaluator.

---

### ❌ Red Flag 4: Violação de Sprint Contract

```json
"phase": {
  "sprint_contract": {
    "max_budget": 100.00
  }
},
"decision": {
  "price": 150.00  // ← ACIMA DO LIMITE!
}
```

**O que significa:** Recomendação violou o contrato definido.  
**Possível causa:** Generator ignorou ou não viu o Sprint Contract.

---

### ❌ Red Flag 5: Evaluator Aprovou Algo Óbvio Ruim

```json
"phase": {
  "sprint_contract": {
    "constraints": ["only_vegan"]
  }
},
"decision": {
  "product_vegan": false  // ← NÃO VEGANO!
},
"evaluation": {
  "checks_performed": [
    {
      "check": "dietary_compliance",
      "result": "PASS"  // ← MAS APROVOU?!
    }
  ]
}
```

**O que significa:** Evaluator aprovou uma violação óbvia de contrato.  
**Possível causa:** Evaluator não viu a constraint, ou o check está bugado.

---

### ❌ Red Flag 6: Confidence Muito Baixa Mas Ainda Aprovou

```json
"reasoning": {
  "confidence_score": 0.35  // ← SÓ 35% DE CONFIANÇA
},
"evaluation": {
  "evaluation_result": "APPROVED"  // ← MAS AINDA APROVARAM
}
```

**O que significa:** Agente tinha dúvida e mesmo assim recomendou.  
**Possível causa:** Falta de threshold de confiança, ou Evaluator não levou em conta.

---

### ❌ Red Flag 7: Campos Críticos Vazios

```json
"decision": {
  "generation_id": null,  // ← SEM ID!
  "product_name": null,   // ← SEM NOME!
  "decision_status": null  // ← SEM STATUS!
}
```

**O que significa:** Informações críticas faltam.  
**Possível causa:** Bug no sistema, ou Agent falhou em estruturar a saída.

---

### ✅ Green Light: Trace Saudável

```json
✅ Input capturado corretamente com intent claro
✅ Context atualizado com preferências recentes
✅ Decision com ID único e status FINAL
✅ Reasoning mostra pensamento passo-a-passo com confiança alta
✅ Evaluator recebeu MESMA recomendação (IDs coincidem)
✅ Evaluator fez todos os checks (budget, dietary, goal)
✅ Nenhum timestamp inconsistente
✅ Nenhum campo crítico vazio
```

---

## 🎯 As 5 Perguntas Que Você Faz Ao Ler uma Trace

Agora que você sabe LER cada componente, aqui está a **sequência de investigação**:

### **Pergunta 1: O input foi capturado corretamente?**

```
Você lê: input.content + input.entities_extracted
└─ Se a mensagem foi capturada corretamente ✅
   └─ Siga para Pergunta 2
   
└─ Se NÃO foi capturado ❌ (vazio, nulo, intent_detected null)
   └─ DIAGNÓSTICO: Problema no NLU/Captura de Input
   └─ PRÓXIMA AÇÃO: Verificar sistema de processamento de linguagem
   └─ PARE AQUI — Resto da trace é inútil se o input foi errado
```

---

### **Pergunta 2: O contexto que o agente sabia estava correto?**

```
Você lê: context.current_user_profile + context.conversation_history
└─ Se o context mostra as preferências RECENTES ✅
   └─ Se timestamp do context ≥ timestamp do input ✅
      └─ Siga para Pergunta 3
   
   └─ Se timestamp do context < timestamp do input ❌
      └─ DIAGNÓSTICO: Context desatualizado
      └─ PRÓXIMA AÇÃO: Verificar quando context foi capturado
      └─ Pode ser um problema de timing/lag
   
└─ Se context está vazio ou nulo ❌
   └─ DIAGNÓSTICO: Agente não tinha informação essencial
   └─ PRÓXIMA AÇÃO: Verificar se há um bug no context loading
   └─ Isto é CRÍTICO — agente operou cego
```

---

### **Pergunta 3: A decisão faz sentido dado o contexto?**

```
Você lê: decision + reasoning
└─ Se decision.product_name combina com context.flavor_preference_current ✅
   └─ Se reasoning mostra pensamento coerente ✅
      └─ Siga para Pergunta 4
   
   └─ Se reasoning está vazio ou não faz sentido ❌
      └─ DIAGNÓSTICO: Agente tomou decisão sem explicação
      └─ PRÓXIMA AÇÃO: Verificar logs do Generator (pode ter errror)
   
└─ Se decision NÃO combina com context ❌
   └─ DIAGNÓSTICO: Generator ignorou ou não viu o context
   └─ PRÓXIMA AÇÃO: Verificar se context foi passado pro Generator
   └─ Pode ser o erro do Prólogo (Morango vs Chocolate)
```

---

### **Pergunta 4: O Evaluator viu o mesmo?**

```
Você lê: evaluation.recommendation_received vs decision.generation_id
└─ Se generation_id coincidem ✅
   └─ Se evaluation.checks_performed é não-vazio ✅
      └─ Siga para Pergunta 5
   
   └─ Se checks_performed está vazio ❌
      └─ DIAGNÓSTICO: Evaluator não fez nenhuma verificação
      └─ PRÓXIMA AÇÃO: Evaluator era um rubber stamp?
      └─ Isto é CRÍTICO — Evaluator falhou completamente
   
└─ Se generation_id NÃO coincidem ❌
   └─ DIAGNÓSTICO: Evaluator viu recomendação diferente
   └─ PRÓXIMA AÇÃO: Qual é a versão correta?
   └─ Isto é o erro do Prólogo — BUG ENCONTRADO!
```

---

### **Pergunta 5: A decisão respeitou o Sprint Contract?**

```
Você lê: phase.sprint_contract vs decision
└─ Se price ≤ max_budget ✅
   └─ Se constraints (vegan, goal, etc) são respeitados ✅
      └─ ✅ TRACE SAUDÁVEL!
   
   └─ Se alguma constraint foi violada ❌
      └─ DIAGNÓSTICO: Violação de Sprint Contract
      └─ PRÓXIMA AÇÃO: Por que Generator ignorou o contrato?
      └─ Verificar se contrato foi passado ao Generator
   
└─ Se price > max_budget ❌
   └─ DIAGNÓSTICO: Recomendação acima do orçamento
   └─ PRÓXIMA AÇÃO: Generator viu o Sprint Contract?
   └─ Cliente DEFINITIVAMENTE vai reclamar disto
```

---

## 📊 Fluxograma de Investigação Visual

```
┌─────────────────────────────────────────────┐
│ VOCÊ TEM UMA TRACE E QUER DEBUGAR           │
└────────────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ P1: Input OK?       │
        └──┬──────────────┬───┘
        YÉS│             │NO
           │          STOP: NLU Error
           ▼
        ┌─────────────────────────┐
        │ P2: Context Correto?    │
        └──┬──────────────┬───┬───┘
        YÉS│           NO │   │Vazio
           │              │   └─> Context Loading Bug
           │              └─> Context Outdated
           ▼
        ┌──────────────────────────┐
        │ P3: Decision Faz Sentido?│
        └──┬──────────────┬───┐────┘
        YÉS│             NO│   │Vazio
           │               │   └─> No Reasoning
           │               └─> Generator Missed Context
           ▼
        ┌─────────────────────────┐
        │ P4: Evaluator Viu Mesmo?│
        └──┬──────┬──────┬───┬────┘
        YÉS│  NÃO │Vazio │IDs diferentes
           │      │      └──> MISMATCH BUG
           │      └─────────> Eval Error
           │
           ▼
        ┌────────────────────────┐
        │ P5: Respeita Contrato? │
        └──┬──────────────┬──────┘
        YÉS│             NO
           │           └─> Contract Violation
           │
           ▼
        ✅ TRACE SAUDÁVEL!
```

---

## 💡 Exemplo Prático: Usando as 5 Perguntas no Caso do Prólogo

**Cenário:** Cliente reclamou: "Recebi Morango em vez de Chocolate"

**Investigação:**

```
P1: Input foi capturado?
└─ Sim ✅ "Mudei de ideia. Prefiro sabor Chocolate agora."
   └─ Siga para P2

P2: Context estava correto?
└─ Sim ✅ flavor_preference_current = "Chocolate" (timestamp 14:37)
   └─ Siga para P3

P3: Decision faz sentido?
└─ Sim ✅ Recomendou "Whey Premium Chocolate Intenso"
   └─ Reasoning mostra: "User changed preference to Chocolate"
   └─ Siga para P4

P4: Evaluator viu o mesmo?
└─ NÃO ❌ 
   ├─ decision.generation_id = "rec-67890"
   ├─ evaluation.recommendation_received = "rec-64321"
   └─ IDs DIFERENTES!
   
DIAGNÓSTICO ENCONTRADO EM 30 SEGUNDOS!
"Evaluator recebeu recomendação diferente do que Generator criou"
"Avaliador aprovou Morango (rec-64321) mas Generator recomendou Chocolate (rec-67890)"
"BUG: Falha ao passar a recomendação correta pro Evaluator"
```

---

## 📝 Resumo: Como Ler uma Trace

| Passo | Procure Por | O que Significa | Red Flag |
|-------|-------------|-----------------|----------|
| 1 | `input.content` + `intent_detected` | O que entrou? | Intent null = NLU falhou |
| 2 | `context.current_user_profile` + timestamps | O que agente sabia? | Context vazio ou desatualizado |
| 3 | `decision.product_name` + `reasoning` | O que foi decidido? Por quê? | Sem reasoning ou sem lógica |
| 4 | `evaluation.recommendation_received` | Evaluator viu isto? | generation_id mismatch |
| 5 | `phase.sprint_contract` vs `decision` | Respeitou contrato? | Violação óbvia |

**Com essas 5 perguntas, você consegue debugar 90% dos erros em uma trace em menos de 5 minutos.**

---

## 🔄 Trace em Generator/Evaluator

Você aprendeu em **Documento 01 (Generator/Evaluator)** que separar criação de validação melhora a qualidade.

Agora você vai aprender como **VER e DEBUGAR** esse padrão usando traces.

---

### Anatomy de uma Trace Gen/Eval

Uma trace de padrão Generator/Evaluator tem esta estrutura específica:

```json
{
  "decision": {
    "agent_role": "generator",
    "generator_id": "gen-12345",
    "generation_id": "rec-67890",
    "recommendation": { ... }
  },
  
  "evaluation": {
    "evaluator_id": "eval-54321",
    "timestamp_received": "2026-05-15T14:40:00Z",
    "recommendation_received": {
      "generation_id": "???",
      "product_name": "???"
    },
    "checks_performed": [
      { "check": "budget_compliance", "result": "PASS" },
      { "check": "dietary_compliance", "result": "PASS" },
      { "check": "goal_alignment", "result": "PASS" }
    ],
    "evaluation_result": "APPROVED"
  }
}
```

**O que é específico de Gen/Eval:**
- Há **dois agentes**: `generator_id` e `evaluator_id`
- Há **dois timestamps**: quando Generator criou, quando Evaluator recebeu
- Há **dois recommendation objects**: o que Generator criou vs o que Evaluator recebeu
- Há **checks_performed**: Evaluator fez validações específicas

---

### Flow de Investigação: Achando o Culpado

Quando uma recomendação Gen/Eval está errada, a pergunta é: **Quem falhou? Generator ou Evaluator?**

Aqui está a sequência de investigação:

```
┌────────────────────────────────────────────┐
│ RECOMENDAÇÃO GEN/EVAL ESTÁ ERRADA          │
└────────────────┬───────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │ STEP 1: O Generator viu        │
    │ o contexto CORRETO?            │
    └─┬──────────────────────────┬───┘
    SIM│                         NÃO
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Generator Cego             │
       │   │ (recebeu contexto errado)  │
       │   │                            │
       │   │ CAUSA: Context loading bug │
       │   │ ou desatualizado           │
       │   └────────────────────────────┘
       │
       ▼
    ┌────────────────────────────────┐
    │ STEP 2: A Decision do          │
    │ Generator faz sentido          │
    │ dado o contexto?               │
    └─┬──────────────────────────┬───┘
    SIM│                         NÃO
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Generator Ruim             │
       │   │ (pensamento errado)        │
       │   │                            │
       │   │ CAUSA: Prompt ruim,        │
       │   │ temperatura alta,          │
       │   │ ou lógica quebrada         │
       │   └────────────────────────────┘
       │
       ▼
    ┌─────────────────────────────────┐
    │ STEP 3: Evaluator recebeu      │
    │ a MESMA recomendação?          │
    │ (IDs coincidem?)               │
    └─┬──────────────────────────┬───┘
    SIM│                         NÃO
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Evaluator Cego (Prólogo)   │
       │   │                            │
       │   │ Generator criou A          │
       │   │ Evaluator recebeu B        │
       │   │                            │
       │   │ CAUSA: Bug ao passar       │
       │   │ recomendação pro Evaluator │
       │   └────────────────────────────┘
       │
       ▼
    ┌──────────────────────────────┐
    │ STEP 4: Evaluator fez        │
    │ os checks corretamente?      │
    │ (all results = PASS?)        │
    └─┬──────────────────────────┬─┘
    SIM│                         NÃO
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Evaluator Falhou           │
       │   │                            │
       │   │ CAUSA: Check logic bugado  │
       │   │ ou Evaluator ignorou erro  │
       │   │ óbvio                      │
       │   └────────────────────────────┘
       │
       ▼
    ┌──────────────────────────────┐
    │ STEP 5: Evaluator rejeitou?  │
    │ (evaluation_result)          │
    └─┬──────────────────────────┬─┘
    APPROVED│                    REJECTED
       │                          │
       ▼                          ▼
    ✅ RECOMENDAÇÃO                ❌ AVALIADOR REJEITOU
    FOI APROVADA                   ALGO BOM (raro)
    (tudo funcionou)
```

---

### Sinais Específicos: Diferenciando Generator vs Evaluator

Aqui está como você identifica cada tipo de erro através da trace:

#### 🔴 Sinal 1: Generator Cego (Recebeu Contexto Errado)

**O que procurar:**

```json
"context": {
  "current_user_profile": {
    "flavor_preference_current": null,  // ← VAZIO!
    "budget_max": null
  }
},
"decision": {
  "product_name": "Whey Premium X"
},
"reasoning": {
  "thought_process": [
    { "step": 1, "reasoning": "No specific preferences detected" }
  ]
}
```

**Sinais:**
- ❌ `current_user_profile` está vazio ou nulo
- ❌ `conversation_history` está vazio
- ❌ Generator reasoning diz "não consegui encontrar preferência"
- ✅ Evaluator checks passaram (porque Evaluator viu contexto, mas Generator não)

**Exemplo do Mundo Real:**
- Cliente falou: "Prefiro Chocolate"
- Context não tem `flavor_preference_current`
- Generator recomendou algo aleatório
- Evaluator viu o contexto correto no momento da avaliação

**Causa Provável:**
- Problema no context loading
- Contexto não foi passado ao Generator
- há lag entre input e context update

---

#### 🔴 Sinal 2: Generator Ruim (Pensamento Errado)

**O que procurar:**

```json
"context": {
  "current_user_profile": {
    "flavor_preference_current": "Chocolate",
    "budget_max": 100.00
  }
},
"decision": {
  "product_name": "Whey Premium Morango",  // ← IGNOROU PREFERÊNCIA!
  "price": 150.00  // ← ACIMA DO BUDGET!
},
"reasoning": {
  "thought_process": [
    { "step": 1, "reasoning": "User prefers Morango" }  // ← ERRADO!
  ],
  "confidence_score": 0.45  // ← BAIXA CONFIANÇA
}
```

**Sinais:**
- ✅ Context está correto e completo
- ❌ Decision ignora o context (preferência diferente, budget acima)
- ❌ Reasoning mostra pensamento errado ("User prefers Morango" quando na verdade prefere Chocolate)
- ❌ Confidence score é baixo

**Exemplo do Mundo Real:**
- Context mostra: `flavor_preference = "Chocolate"`, `budget = 100`
- Generator recomendou: Morango R$ 150
- Reasoning diz: "User wants Morango" (falsidade!)

**Causa Provável:**
- Prompt do Generator está confuso
- Temperatura muito alta (agente "alucinando")
- Lógica do Generator está quebrada
- Model sendo usado é inadequado

---

#### 🔴 Sinal 3: Evaluator Cego / Mismatch (Como no Prólogo)

**O que procurar:**

```json
"decision": {
  "generation_id": "rec-67890",
  "product_name": "Whey Premium Chocolate Intenso"
},
"evaluation": {
  "recommendation_received": {
    "generation_id": "rec-64321",  // ← DIFERENTE!
    "product_name": "Whey Premium Morango"  // ← DIFERENTE!
  }
}
```

**Sinais:**
- ❌ `decision.generation_id` ≠ `evaluation.recommendation_received.generation_id`
- ❌ `decision.product_name` ≠ `evaluation.recommendation_received.product_name`
- Tudo mais está OK (Generator estava correto, Evaluator estava OK)
- Mas eles avaliaram coisas diferentes!

**Exemplo do Mundo Real:**
- Generator criou: `rec-67890` (Chocolate)
- Mas Evaluator recebeu: `rec-64321` (Morango)
- Evaluator aprovou Morango (legitimamente)
- Mas cliente recebeu Morango em vez de Chocolate

**Causa Provável:**
- Bug no código que passa a recomendação pro Evaluator
- Queue de recomendações (há múltiplas, Evaluator pegou a errada)
- Race condition (timing issue)
- Histórico de recomendações confundido

---

#### 🔴 Sinal 4: Evaluator Falhou na Validação

**O que procurar:**

```json
"phase": {
  "sprint_contract": {
    "max_budget": 100.00,
    "constraints": ["only_vegan"]
  }
},
"decision": {
  "price": 150.00,  // ← ACIMA DO ORÇAMENTO
  "product_vegan": false  // ← NÃO VEGANO
},
"evaluation": {
  "checks_performed": [
    { "check": "budget_compliance", "result": "PASS" },  // ← DEVERIA SER FAIL!
    { "check": "dietary_compliance", "result": "PASS" }  // ← DEVERIA SER FAIL!
  ],
  "evaluation_result": "APPROVED"
}
```

**Sinais:**
- ✅ Context está correto
- ✅ Generator decision é clara
- ❌ Checks dizem "PASS" quando deveriam dizer "FAIL"
- ❌ Algo óbvio errado mas Evaluator aprovou

**Exemplo do Mundo Real:**
- Contrato: "Máximo R$ 100"
- Recomendação: R$ 150
- Evaluator check: "budget_compliance: PASS" (ERRADO!)
- Evaluator aprovou (ERRADO!)

**Causa Provável:**
- Lógica do check está bugada
- Evaluator não está comparando com Sprint Contract
- Evaluator é um "rubber stamp" (aprova tudo)
- Campo do contrato não está sendo passado ao Evaluator

---

### Método de Investigação Passo-a-Passo

Quando uma recomendação Gen/Eval falha, você:

**PASSO 1: Abra a trace e procure por mismatch óbvio**

```bash
$ jq '.decision.generation_id, .evaluation.recommendation_received.generation_id' trace.json

# Se forem diferentes → VAI PARA PASSO 3
# Se forem iguais → VAI PARA PASSO 2
```

**PASSO 2: Compare context com decision**

```bash
$ jq '.context.current_user_profile | to_entries[] | "\(.key): \(.value)"' trace.json
$ jq '.decision.product_name, .decision.price' trace.json

# Se decision ignora context → Generator Ruim
# Se context está vazio → Generator Cego
# Se tudo bate → VAI PARA PASSO 4
```

**PASSO 3: Se há mismatch de IDs**

```bash
$ jq '.decision | {generation_id, product_name}' trace.json
$ jq '.evaluation.recommendation_received | {generation_id, product_name}' trace.json

# Compare os dois JSONs lado-a-lado
# Se são diferentes → Evaluator Cego / Bug ao passar recomendação
# DIAGNÓSTICO: ENCONTRADO!
```

**PASSO 4: Verifique os checks do Evaluator**

```bash
$ jq '.phase.sprint_contract' trace.json
$ jq '.decision | {price, constraints}' trace.json
$ jq '.evaluation.checks_performed[]' trace.json

# Verifique se cada check reflete a realidade:
# - Budget: price <= max_budget?
# - Constraints: product matches requirements?
# - Goal: recommendation aligns with goal?

# Se check diz "PASS" mas deveriam ser "FAIL" → Evaluator Falhou
# DIAGNÓSTICO: ENCONTRADO!
```

---

### Exemplo KODA Completo: Trace Gen/Eval com Problema

Vamos usar o caso do **Prólogo** e mostrar a trace COMPLETA com o erro Gen/Eval:

```json
{
  "trace_id": "trace-koda-client-12345-error",
  "session_id": "session-client-12345",
  
  "phase": {
    "sprint_number": 1,
    "sprint_contract": {
      "max_budget": 100.00,
      "constraints": ["muscle_gain", "flavor_preference"]
    }
  },
  
  "input": {
    "timestamp": "2026-05-15T14:37:00Z",
    "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
    "entities_extracted": {
      "flavor_preference": "Chocolate"
    }
  },
  
  "context": {
    "flavor_preference_current": "Chocolate",
    "flavor_preference_timestamp": "2026-05-15T14:37:00Z",
    "flavor_preference_previous": "Morango",
    "budget_max": 100.00
  },
  
  "decision": {
    "agent_role": "generator",
    "generator_id": "gen-koda-v2.1",
    "generation_id": "rec-67890-chocolate",
    "timestamp": "2026-05-15T14:38:00Z",
    "decision_status": "FINAL",
    "recommendation": {
      "product_name": "Whey Premium Chocolate Intenso",
      "product_id": "prod-002",
      "price": 89.90,
      "flavor": "Chocolate"
    }
  },
  
  "reasoning": {
    "thought_process": [
      {
        "step": 1,
        "reasoning": "User explicitly changed preference from Morango to Chocolate at 2026-05-15T14:37:00Z"
      },
      {
        "step": 2,
        "reasoning": "Chocolate Intenso matches new preference, within budget (R$ 89.90 < R$ 100), supports muscle gain goal"
      }
    ],
    "confidence_score": 0.95
  },
  
  "evaluation": {
    "evaluator_id": "eval-koda-v2.1",
    "timestamp_received": "2026-05-15T14:40:00Z",
    "recommendation_received": {
      "generation_id": "rec-64321-morango",
      "product_name": "Whey Premium Morango"
    },
    "checks_performed": [
      {
        "check": "budget_compliance",
        "result": "PASS",
        "detail": "R$ 89.90 <= R$ 100"
      },
      {
        "check": "preference_alignment",
        "result": "PASS",
        "detail": "Morango is suitable"
      },
      {
        "check": "goal_alignment",
        "result": "PASS"
      }
    ],
    "evaluation_result": "APPROVED",
    "timestamp_approval": "2026-05-15T14:40:00Z"
  }
}
```

---

### Analisando este Exemplo com o Flow

**Cliente reclamou:** "Recebi Morango em vez de Chocolate"

**Sua investigação:**

```
STEP 1: Generator viu contexto correto?
└─ Sim ✅
   context.flavor_preference_current = "Chocolate"
   decision.product_name = "Whey Premium Chocolate Intenso"
   └─ Generator viu corretamente!

STEP 2: Decision faz sentido?
└─ Sim ✅
   Reasoning mostra pensamento correto
   confidence_score = 0.95 (alta)
   └─ Generator pensou bem!

STEP 3: Evaluator recebeu a MESMA recomendação?
└─ NÃO ❌
   decision.generation_id = "rec-67890-chocolate"
   evaluation.recommendation_received.generation_id = "rec-64321-morango"
   
   ⚠️ MISMATCH ENCONTRADO!
   
   Generator criou: "Whey Premium Chocolate Intenso" (rec-67890)
   Evaluator recebeu: "Whey Premium Morango" (rec-64321)
   
DIAGNÓSTICO:
═══════════════════════════════════════════════════════════════
Evaluator Cego / Recomendação Incorreta Passada

O que aconteceu:
1. Generator viu "Chocolate" e recomendou corretamente
2. Mas algo errado aconteceu ao passar a recomendação
3. Evaluator recebeu "Morango" em vez de "Chocolate"
4. Evaluator aprovou "Morango" (que estava tecnicamente OK, mas NÃO ERA a recomendação do Generator)
5. Cliente recebeu "Morango"

Causa Provável:
- Bug no código que passa generation_id para Evaluator
- Sistema pegou recomendação anterior (de quando cliente queria Morango)
- Race condition: múltiplas recomendações, Evaluator pegou a errada

Próximas Ações:
1. Verificar código que passa `generation_id` ao Evaluator
2. Verificar se há fila de recomendações (múltiplas em paralelo)
3. Adicionar validação: Evaluator deve receber MESMA generation_id que Generator criou
4. Log do que Evaluator recebeu vs o que deveria ter recebido
═══════════════════════════════════════════════════════════════
```

---

### Red Flags Específicas de Gen/Eval

Quando você está lendo uma trace Gen/Eval, procure por:

| Red Flag | Significa | Ação |
|----------|-----------|------|
| `evaluation.generation_id` ≠ `decision.generation_id` | Evaluator viu recomendação diferente | Verificar bug ao passar rec |
| `checks_performed` está vazio | Evaluator não fez nenhuma validação | Evaluator é rubber stamp |
| Check diz "PASS" mas é óbvio "FAIL" | Lógica do check está bugada | Debugar lógica do check |
| `context` está vazio mas `decision` existe | Generator operou cego | Context loading bug |
| `decision` ignora `context` | Generator pensou errado | Debugar prompt/lógica |
| `confidence_score` < 0.5 mas ainda aprovado | Falta threshold mínimo | Adicionar rejeição automática |
| `timestamp_received` > `timestamp_approval` mas são muito próximos | Timing suspeito | Verificar sincronia |

---

### Resumo: Trace Gen/Eval Saudável

Uma trace de padrão Generator/Evaluator está saudável quando:

✅ Generator recebeu contexto completo e atualizado  
✅ Generator reasoning faz sentido dado o contexto  
✅ Generation_id é único e clara é o status "FINAL"  
✅ Evaluator recebeu MESMA generation_id  
✅ Evaluator fez todos os checks esperados  
✅ Todos os checks retornaram resultado esperado  
✅ Nenhuma violação óbvia de contrato  
✅ Evaluator aprovou (ou rejeitou com motivo claro)  

**Com essa análise, você consegue debugar 95% dos problemas Gen/Eval em menos de 10 minutos.**

---

## 📋 Trace em Sprint Contracts

Você aprendeu em **Documento 02 (Sprint Contracts)** que contratos claros evitam contradições entre agente e cliente.

Agora você vai aprender como **VER e DEBUGAR** violações de contrato usando traces.

---

### Anatomy de uma Trace Sprint Contract

Uma trace com Sprint Contract tem esta estrutura específica:

```json
{
  "phase": {
    "sprint_number": 1,
    "sprint_name": "Discover Products",
    "sprint_contract": {
      "contract_id": "contract-sprint-1-client-12345",
      "timestamp_created": "2026-05-15T14:00:00Z",
      "max_budget": 100.00,
      "constraints": [
        {
          "name": "dietary",
          "value": "only_vegan",
          "description": "Only 100% vegan products"
        },
        {
          "name": "goal",
          "value": "muscle_gain",
          "description": "Products for muscle gain"
        }
      ],
      "duration_minutes": 10
    }
  },
  
  "context": {
    "contract_at_generation_time": {
      "contract_id": "contract-sprint-1-client-12345",
      "timestamp_valid_at": "2026-05-15T14:37:00Z",
      "max_budget": 100.00,
      "constraints": [...]
    },
    "contract_at_input_time": {
      "timestamp_valid_at": "2026-05-15T14:30:00Z",
      "max_budget": 100.00,
      "constraints": [...]
    }
  },
  
  "decision": {
    "product_price": 89.90,
    "product_vegan": true,
    "product_goal_aligned": true
  }
}
```

**O que é específico de Sprint Contract:**
- Há um `sprint_contract` definido no início
- Há dois snapshots do contrato: `contract_at_input_time` vs `contract_at_generation_time`
- Há timestamps de quando cada snapshot foi capturado
- A `decision` pode ser verificada contra ambos os snapshots

**Por que dois snapshots?**
- Detectar se o contrato MUDOU entre input e recomendação
- Rastrear QUANDO uma mudança de contrato aconteceu
- Diferenciar "violação" de "mudança legítima"

---

### Flow de Investigação: Achando a Raiz da Violação

Quando uma recomendação viola o Sprint Contract, a pergunta é: **É culpa do agente ou do cliente?**

```
┌────────────────────────────────────────────┐
│ RECOMENDAÇÃO VIOLOU SPRINT CONTRACT        │
└────────────────┬───────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │ STEP 1: O contrato foi        │
    │ passado ao agente?            │
    │ (contract_id no context?)     │
    └─┬──────────────────────────┬───┘
    SIM│                         NÃO
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Agente Cego de Contrato    │
       │   │                            │
       │   │ CAUSA: Contract loading    │
       │   │ bug ou não foi passado     │
       │   └────────────────────────────┘
       │
       ▼
    ┌────────────────────────────────┐
    │ STEP 2: O contrato mudou      │
    │ entre input e geração?        │
    │ (snapshots diferentes?)       │
    └─┬──────────────────────────┬───┘
    NÃO│                         SIM
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Mudança Legítima           │
       │   │                            │
       │   │ AÇÃO: Não é culpa do       │
       │   │ agente. Cliente mudou de   │
       │   │ ideia. Investigar quando.  │
       │   └────────────────────────────┘
       │
       ▼
    ┌────────────────────────────────┐
    │ STEP 3: A recomendação        │
    │ respeita as constraints        │
    │ do contrato?                  │
    │ (price, dietary, goal, etc?)  │
    └─┬──────────────────────────┬───┘
    SIM│                         NÃO
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Violação de Contrato       │
       │   │ (Culpa do Agente)          │
       │   │                            │
       │   │ CAUSA: Agente viu contrato │
       │   │ mas ignorou ou falhou      │
       │   └────────────────────────────┘
       │
       ▼
    ┌────────────────────────────────┐
    │ STEP 4: Generator viu         │
    │ o contrato QUANDO fez a       │
    │ recomendação?                 │
    │ (context incluia constraint?) │
    └─┬──────────────────────────┬───┘
    SIM│                         NÃO
       │                          │
       │        ┌─────────────────┘
       │        │
       │        ▼
       │   ┌────────────────────────────┐
       │   │ DIAGNÓSTICO:               │
       │   │ Context Amnesia            │
       │   │ (Contract Forgotten)       │
       │   │                            │
       │   │ CAUSA: Contract não foi    │
       │   │ incluido no context do     │
       │   │ Generator                  │
       │   │                            │
       │   │ QUANDO ACONTECEU:          │
       │   │ Entre STEP 1 e STEP 3     │
       │   │ (quando context foi feito) │
       │   └────────────────────────────┘
       │
       ▼
    ✅ VIOLAÇÃO EXPLICADA!
    (agente viu, ignorou)
```

---

### Rastreando QUANDO uma Informação de Contrato Foi Perdida

Este é o diferencial de usar Traces com Sprint Contracts: **você consegue saber EXATAMENTE QUANDO e ONDE a informação foi esquecida**.

Aqui está como:

**Passo 1: Compare os dois snapshots de contrato**

```json
"context": {
  "contract_at_input_time": {
    "timestamp_valid_at": "2026-05-15T14:30:00Z",
    "max_budget": 100.00,
    "constraints": ["only_vegan"]
  },
  "contract_at_generation_time": {
    "timestamp_valid_at": "2026-05-15T14:37:00Z",
    "max_budget": 100.00,
    "constraints": ["only_vegan"]
  }
}
```

**Se forem iguais:**
- ✅ Contrato não mudou
- Qualquer violação é culpa do agente (viu e ignorou)

**Se forem diferentes:**
- ⚠️ Contrato mudou
- Verificar timestamps para saber QUANDO mudou
- Se mudou DEPOIS que Generator viu → Agente não podia saber (mudança legítima)
- Se mudou ANTES que Generator viu → Agente deveria saber (erro do agente)

---

**Passo 2: Compare contexto na hora do input vs na hora da geração**

```json
"context": {
  "contract_at_input_time": {
    "max_budget": 100.00,
    "timestamp_valid_at": "2026-05-15T14:30:00Z"
  },
  "current_user_profile_at_input_time": {
    "budget_mentioned": true,
    "budget_value": 100.00
  }
}

"decision": {
  "timestamp": "2026-05-15T14:37:00Z",
  "price": 150.00  // ← VIOLAÇÃO
}
```

**O que você vê:**
- Na hora do input (14:30), o contexto tinha budget = 100
- Na hora da geração (14:37), o Generator recomendou 150
- **Gap de 7 minutos**
- **Pergunta:** O context foi atualizado entre input e geração? Ou Generator esqueceu?

---

### Sinais Específicos: Tipos de Violação

#### 🔴 Sinal 1: Violação Óbvia (Preço Acima do Budget)

**O que procurar:**

```json
"phase": {
  "sprint_contract": {
    "max_budget": 100.00
  }
},
"decision": {
  "price": 150.00  // ← ACIMA!
}
```

**Sinais:**
- ❌ `decision.price` > `sprint_contract.max_budget`
- ✅ Contrato foi passado (contract_id presente)
- ✅ Context mostra o budget

**Exemplo:**
- Contrato: "Máximo R$ 100"
- Recomendação: R$ 150
- Óbvio!

**Causa Provável:**
- Generator viu o contrato mas ignorou
- Generator tem bug na comparação de preço
- Generator confundiu moedas (R$ vs USD?)

---

#### 🔴 Sinal 2: Constraint Técnico Ignorado

**O que procurar:**

```json
"phase": {
  "sprint_contract": {
    "constraints": [
      {
        "name": "dietary",
        "value": "only_vegan"
      }
    ]
  }
},
"decision": {
  "product_vegan": false  // ← VIOLAÇÃO!
}
```

**Sinais:**
- ❌ `decision.product_vegan` = false
- ✅ Contrato explicitly diz "only_vegan"
- ✅ Constraint foi passado no context

**Exemplo:**
- Contrato: "Apenas produtos 100% veganos"
- Recomendação: Whey com aditivos (não é 100% vegan)
- Violação sutil mas clara

**Causa Provável:**
- Generator não entendeu "100% vegan"
- Generator confundiu "vegan-friendly" com "100% vegan"
- Banco de dados de produtos tem info errada

---

#### 🟡 Sinal 3: Mudança Legítima de Contrato

**O que procurar:**

```json
"context": {
  "contract_at_input_time": {
    "timestamp_valid_at": "2026-05-15T14:30:00Z",
    "max_budget": 100.00
  },
  "contract_at_generation_time": {
    "timestamp_valid_at": "2026-05-15T14:32:00Z",
    "max_budget": 150.00  // ← MUDOU!
  }
},
"decision": {
  "timestamp": "2026-05-15T14:35:00Z",
  "price": 140.00  // ← Resprita novo contrato ✅
}
```

**Sinais:**
- ✅ Contrato foi MODIFICADO (timestamps mostram mudança)
- ✅ Recomendação respeita o NOVO contrato (140 < 150)
- ⚠️ Mas violaria o ANTIGO contrato (140 > 100)

**Exemplo:**
- Sprint 1 (14:30): "Máximo R$ 100"
- Cliente (14:31): "Na verdade, posso gastar até R$ 150"
- Sprint 2 (14:35): Generator recomenda R$ 140
- É violação? NÃO, é mudança legítima

**Como Detectar:**
- Compare `contract_at_input_time.timestamp` com `contract_at_generation_time.timestamp`
- Se o segundo é DEPOIS, contrato foi atualizado
- Se recomendação respeita o novo, não é culpa do agente

---

#### 🟡 Sinal 4: Context Amnesia (Contract Forgotten Entre Sprints)

**O que procurar:**

```json
"phase": {
  "sprint_number": 3,  // ← SPRINT 3
  "sprint_contract": {
    "contract_id": "contract-sprint-3-client-12345",
    "constraints": ["only_vegan"]  // ← CONSTRAINT CARREGADO
  }
},
"context": {
  "current_user_profile": {
    "dietary_restrictions": null  // ← MAS CONTEXTO ESQUECEU!
  }
},
"decision": {
  "product_vegan": false  // ← VIOLAÇÃO
}
```

**Sinais:**
- ✅ Contrato foi carregado (phase.sprint_contract presente)
- ❌ Mas contexto não tem a informação (dietary_restrictions null)
- ❌ Generator não viu a constraint no contexto

**Exemplo:**
- Sprint 1: Cliente falou "Apenas vegano"
- Contract registrou: `constraints: ["only_vegan"]`
- Sprint 3: Novo contexto não inclui `dietary_restrictions`
- Generator recomendou não-vegano
- É violação? SIM, mas diferente: context amnesia

**Causa Provável:**
- Context não foi carregado completamente entre sprints
- Dados de preferência não foram carried forward
- Bug no sistema que mantém contexto entre sprints

---

### Método de Investigação Passo-a-Passo

Quando uma recomendação viola Sprint Contract:

**PASSO 1: Verificar se contrato foi passado**

```bash
$ jq '.phase.sprint_contract | keys' trace.json

# Se contrato está vazio/nulo
→ Agente não viu contrato (culpa do sistema)

# Se contrato está presente
→ Agente tinha acesso
```

**PASSO 2: Comparar snapshots de contrato**

```bash
$ jq '.context.contract_at_input_time' trace.json > contract_input.json
$ jq '.context.contract_at_generation_time' trace.json > contract_gen.json
$ diff contract_input.json contract_gen.json

# Se diferentes
→ Contrato mudou entre input e geração
→ Verificar timestamps para saber quando

# Se iguais
→ Contrato foi estável
→ Qualquer violação é do agente
```

**PASSO 3: Verificar cada constraint**

```bash
$ jq '.phase.sprint_contract.constraints[]' trace.json
$ jq '.decision | {price, product_vegan, product_goal_aligned}' trace.json

# Para cada constraint:
# - max_budget: decision.price <= constraint.max_budget?
# - dietary: decision.product_vegan == constraint.dietary?
# - goal: decision.goal_aligned == constraint.goal?

# Se algum falhar
→ Violação encontrada
```

**PASSO 4: Rastrear QUANDO foi esquecida**

```bash
$ jq '.context.contract_at_generation_time | {timestamp_valid_at, constraints}' trace.json
$ jq '.decision | {timestamp, reasoning}' trace.json

# Se constraint estava no contrato_at_generation_time
# Mas não está no reasoning do Generator
→ Context Amnesia: Generator viu contrato mas esqueceu

# Se constraint NÃO estava no contrato_at_generation_time
→ Contrato foi atualizado: mudança legítima ou culpa do sistema
```

---

### Exemplo KODA Completo 1: Orçamento Violado

**Cenário:** Cliente pediu orçamento máximo R$ 100, recebeu recomendação de R$ 150.

```json
{
  "trace_id": "trace-budget-violation",
  
  "phase": {
    "sprint_number": 1,
    "sprint_contract": {
      "contract_id": "contract-sprint-1-client-xyz",
      "timestamp_created": "2026-05-15T14:00:00Z",
      "max_budget": 100.00
    }
  },
  
  "input": {
    "timestamp": "2026-05-15T14:05:00Z",
    "content": "Quero um bom whey. Máximo R$ 100.",
    "entities_extracted": {
      "budget_max": 100.00
    }
  },
  
  "context": {
    "contract_at_input_time": {
      "timestamp_valid_at": "2026-05-15T14:00:00Z",
      "max_budget": 100.00
    },
    "contract_at_generation_time": {
      "timestamp_valid_at": "2026-05-15T14:10:00Z",
      "max_budget": 100.00  // ← NÃO MUDOU
    },
    "current_user_profile": {
      "budget_max": 100.00,
      "budget_max_timestamp": "2026-05-15T14:05:00Z"
    }
  },
  
  "decision": {
    "timestamp": "2026-05-15T14:10:00Z",
    "product_name": "Whey Premium Elite",
    "price": 150.00,
    "reasoning": [
      {
        "step": 1,
        "reasoning": "User wants good quality whey"
      },
      {
        "step": 2,
        "reasoning": "Premium Elite is the best option"
      }
    ]
  }
}
```

**Análise com Flow:**

```
STEP 1: Contrato foi passado ao agente?
└─ Sim ✅ (contract_id presente)

STEP 2: Contrato mudou?
└─ Não ❌ (contract_at_input = contract_at_generation)

STEP 3: Recomendação respeita constraints?
└─ Não ❌
   price (150) > max_budget (100)
   VIOLAÇÃO ENCONTRADA!

STEP 4: Generator viu o contrato?
└─ Sim ✅ (context.contract_at_generation_time presente)
   Mas reasoning não menciona "budget" ou "R$ 100"
   Generator viu mas IGNOROU

DIAGNÓSTICO:
═══════════════════════════════════════════════════════════════
Violação Óbvia de Contrato (Culpa do Agente)

O que aconteceu:
1. Cliente definiu budget máximo: R$ 100
2. Contrato foi criado com max_budget: 100
3. Contrato não mudou durante a conversa
4. Generator recomendou R$ 150 (acima do budget)
5. Generator reasoning não menciona budget (ignorou)

Causa:
- Generator viu o contrato mas priorizou "qualidade"
- Prompt do Generator pode estar dizendo "escolha a melhor opção"
  sem considerar constraints
- Falta lógica de "rejeitar se acima do budget"

Ação:
1. Verificar prompt do Generator (está pesando qualidade demais?)
2. Adicionar validação: se price > max_budget, rejeitar automaticamente
3. Treinar Generator a explicar trade-offs (qualidade vs budget)
═══════════════════════════════════════════════════════════════
```

---

### Exemplo KODA Completo 2: Mudança Legítima de Contrato

**Cenário:** Cliente pediu "vegano" no início, depois mudou a restrição, e agente recomendou produto não-vegano.

```json
{
  "trace_id": "trace-legitimate-change",
  
  "phase": {
    "sprint_number": 2,
    "sprint_contract": {
      "contract_id": "contract-sprint-2-client-abc",
      "timestamp_created": "2026-05-15T14:30:00Z",
      "constraints": [
        {
          "name": "dietary",
          "value": "no_restriction"  // ← MUDOU PARA ISSO
        }
      ]
    }
  },
  
  "context": {
    "contract_at_input_time": {
      "timestamp_valid_at": "2026-05-15T14:20:00Z",
      "constraints": [
        { "name": "dietary", "value": "only_vegan" }  // ← ERA ISSO
      ]
    },
    "contract_at_generation_time": {
      "timestamp_valid_at": "2026-05-15T14:30:00Z",
      "constraints": [
        { "name": "dietary", "value": "no_restriction" }  // ← AGORA É ISSO
      ]
    }
  },
  
  "input": {
    "timestamp": "2026-05-15T14:28:00Z",
    "content": "Sabe, na verdade posso comer qualquer coisa. Relaxei a restrição.",
    "entities_extracted": {
      "constraint_change": "dietary_relaxed"
    }
  },
  
  "decision": {
    "timestamp": "2026-05-15T14:32:00Z",
    "product_name": "Whey Premium (com aditivos)",
    "product_vegan": false,
    "reasoning": [
      {
        "step": 1,
        "reasoning": "User relaxed dietary restriction at 14:28"
      },
      {
        "step": 2,
        "reasoning": "Now can recommend any whey"
      }
    ]
  }
}
```

**Análise com Flow:**

```
STEP 1: Contrato foi passado ao agente?
└─ Sim ✅

STEP 2: Contrato mudou?
└─ Sim ⚠️
   contract_at_input_time (14:20): dietary = "only_vegan"
   contract_at_generation_time (14:30): dietary = "no_restriction"
   
   Contrato mudou entre 14:20 e 14:30
   Decision foi feita às 14:32 (DEPOIS da mudança)
   
PASSO ESPECIAL: Quando a mudança foi feita?
└─ Input em 14:28 diz "relaxei a restrição"
   Contract foi atualizado para 14:30
   Decision em 14:32 usa novo contrato
   
   ✅ MUDANÇA LEGÍTIMA (cliente pediu)

DIAGNÓSTICO:
═══════════════════════════════════════════════════════════════
Mudança Legítima de Contrato (NÃO é culpa do agente)

O que aconteceu:
1. Sprint 1 (14:00-14:20): Contrato era "only_vegan"
2. Sprint 2 (14:28): Cliente mudou de ideia
3. Contrato foi atualizado para "no_restriction"
4. Generator recomendou não-vegano (respeitando novo contrato)

Timeline:
- 14:20: Contrato anterior valia "only_vegan"
- 14:28: Cliente falou que relaxou restrição
- 14:30: Contrato atualizado para "no_restriction"
- 14:32: Generator recomendou baseado no novo contrato ✅

Conclusão:
- NÃO é violação
- É mudança legítima do cliente
- Agent respondeu corretamente à mudança

Ação:
- Informar cliente que recomendação reflete sua mudança de ideia
- Não há culpa do agente aqui
═══════════════════════════════════════════════════════════════
```

---

### Red Flags Específicas de Sprint Contract

Quando você está lendo uma trace Sprint Contract, procure por:

| Red Flag | Significa | Ação |
|----------|-----------|------|
| `sprint_contract` está vazio | Agente não tinha contrato | Sistema bug, não culpa do agente |
| `contract_at_generation_time` está vazio | Contexto não tem snapshot do contrato | Context loading bug |
| `decision.price` > `sprint_contract.max_budget` | Violação óbvia | Debugar Generator |
| `decision.constraints` ≠ `sprint_contract.constraints` | Constraint ignorado | Generator viu e ignorou |
| `contract_at_input` ≠ `contract_at_generation` | Contrato mudou | Verificar timestamps |
| Contrato mudou DEPOIS da geração | Agente não podia saber | Mudança legítima, não culpa |
| `context.current_user_profile` não tem constraint | Context amnesia | Dados não foram carried forward |
| `decision.reasoning` não menciona constraint | Generator sabia mas não usou | Falta lógica de validação |

---

### Resumo: Trace Sprint Contract Saudável

Uma trace de padrão Sprint Contract está saudável quando:

✅ Contrato foi passado ao agente (phase.sprint_contract presente)  
✅ Contexto tem snapshots de contrato (input time e generation time)  
✅ Contexto atual tem as constraints registradas  
✅ Recomendação respeita TODAS as constraints  
✅ Se contrato mudou, timeline mostra quando e por quê  
✅ Se contrato mudou DEPOIS da geração, agente não podia saber  
✅ Generator reasoning menciona constraints (mostra que viu)  
✅ Nenhuma violação óbvia  

**Com esse análise, você consegue:
- Detectar violações de contrato em 5 minutos
- Diferenciar violação de mudança legítima
- Rastrear EXATAMENTE QUANDO uma info foi esquecida
- Saber se é culpa do agente ou do sistema**

---

## 🔧 Método de Debug Passo a Passo

### A Investigação de 5 Perguntas

[To be written]

### Fluxograma: Árvore de Decisão de Debug

[To be written]

### Casos de Uso Real

#### Caso 1: "Por Que Recomendou X em Vez de Y?"
[To be written]

#### Caso 2: "Quando o Agente Perdeu a Informação?"
[To be written]

#### Caso 3: "O Evaluator Viu o Mesmo Contexto?"
[To be written]

#### Caso 4: "Violação de Sprint Contract ou Mudança Legítima?"
[To be written]

---

## 🤖 Trace Reader Script (Automação)

Você aprendeu como **ler traces manualmente**. Mas quando você tem 100 traces para debugar, isso não escala.

Aqui estão scripts que **automatizam** toda a análise que você fez nas seções anteriores.

---

### O que o Script Faz

O script de análise automaticamente:

✅ **Valida estrutura** — Campos obrigatórios estão presentes?  
✅ **Detecta red flags** — Timestamps invertidos? Gen/Eval mismatch?  
✅ **Verifica contratos** — Recomendação viola Sprint Contract?  
✅ **Gera score** — Trace está saudável? (0-100)  
✅ **Produz relatório** — Detalhado com recomendações  

**Output:** JSON estruturado, fácil de processar e exibir.

---

### Python Script: trace_analyzer.py

```python
#!/usr/bin/env python3
"""
Trace Reader & Analyzer
Automatiza a leitura e validação de traces KODA
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple

class TraceAnalyzer:
    def __init__(self, trace_data: Dict[str, Any]):
        self.trace = trace_data
        self.issues: List[Dict] = []
        self.score = 100
        self.sections = {}
        
    def analyze(self) -> Dict[str, Any]:
        """Executa análise completa da trace"""
        
        # 1. Validações estruturais
        self._validate_required_fields()
        
        # 2. Validações de timestamp
        self._validate_timestamps()
        
        # 3. Validações de Generator/Evaluator
        self._validate_gen_eval()
        
        # 4. Validações de Sprint Contract
        self._validate_sprint_contract()
        
        # 5. Validações de completude de context
        self._validate_context_completeness()
        
        # Gerar relatório
        return self._generate_report()
    
    def _add_issue(self, severity: str, type_: str, detail: str, recommendation: str = ""):
        """Adiciona uma issue ao relatório"""
        self.issues.append({
            "severity": severity,
            "type": type_,
            "detail": detail,
            "recommendation": recommendation
        })
        
        # Descontar pontos baseado em severidade
        if severity == "ERROR":
            self.score -= 20
        elif severity == "WARNING":
            self.score -= 10
        elif severity == "INFO":
            self.score -= 2
    
    # ════════════════════════════════════════════════════════════════
    # VALIDAÇÕES ESTRUTURAIS
    # ════════════════════════════════════════════════════════════════
    
    def _validate_required_fields(self):
        """Valida campos obrigatórios"""
        required_top_level = ["trace_id", "session_id", "timestamp", "input", "context", "decision"]
        
        for field in required_top_level:
            if field not in self.trace or self.trace[field] is None:
                self._add_issue(
                    "ERROR",
                    "missing_field",
                    f"Campo obrigatório faltando: {field}",
                    f"Garantir que {field} está presente na trace"
                )
        
        # Validar Input
        if "input" in self.trace and self.trace["input"]:
            if "content" not in self.trace["input"]:
                self._add_issue(
                    "ERROR",
                    "incomplete_input",
                    "Input.content está faltando",
                    "Registrar o conteúdo exato do input do usuário"
                )
            if "intent_detected" not in self.trace["input"]:
                self._add_issue(
                    "WARNING",
                    "incomplete_input",
                    "Input.intent_detected está faltando (NLU não rodou?)",
                    "Processamento de linguagem natural pode ter falhado"
                )
        
        # Validar Decision
        if "decision" in self.trace and self.trace["decision"]:
            if "generation_id" not in self.trace["decision"]:
                self._add_issue(
                    "ERROR",
                    "missing_generation_id",
                    "Decision.generation_id não existe (CRÍTICO)",
                    "Adicionar ID único para cada recomendação gerada"
                )
            if "decision_status" not in self.trace["decision"]:
                self._add_issue(
                    "WARNING",
                    "missing_decision_status",
                    "Decision.decision_status não definido (é final?)",
                    "Explicitar se é FINAL, DRAFT, ou PENDING"
                )
    
    # ════════════════════════════════════════════════════════════════
    # VALIDAÇÕES DE TIMESTAMP
    # ════════════════════════════════════════════════════════════════
    
    def _validate_timestamps(self):
        """Valida consistência de timestamps"""
        
        try:
            # Extrair timestamps-chave
            input_ts = self.trace.get("input", {}).get("timestamp")
            decision_ts = self.trace.get("decision", {}).get("timestamp")
            eval_ts = self.trace.get("evaluation", {}).get("timestamp_received")
            eval_approval_ts = self.trace.get("evaluation", {}).get("timestamp_approval")
            
            # Converter para datetime para comparação
            if input_ts and decision_ts:
                input_dt = datetime.fromisoformat(input_ts.replace('Z', '+00:00'))
                decision_dt = datetime.fromisoformat(decision_ts.replace('Z', '+00:00'))
                
                if decision_dt < input_dt:
                    self._add_issue(
                        "ERROR",
                        "timestamp_inversion",
                        f"Decision ({decision_ts}) é ANTES do Input ({input_ts})",
                        "Verificar sincronização de relógios ou ordem de eventos"
                    )
            
            # Validar sequência Generator → Evaluator
            if decision_ts and eval_ts:
                decision_dt = datetime.fromisoformat(decision_ts.replace('Z', '+00:00'))
                eval_dt = datetime.fromisoformat(eval_ts.replace('Z', '+00:00'))
                
                if eval_dt < decision_dt:
                    self._add_issue(
                        "ERROR",
                        "timestamp_inversion",
                        f"Evaluator recebeu ({eval_ts}) ANTES do Generator gerar ({decision_ts})",
                        "Bug no sistema de logging ou ordem de eventos"
                    )
            
            # Validar sequência recebimento vs aprovação
            if eval_ts and eval_approval_ts:
                eval_dt = datetime.fromisoformat(eval_ts.replace('Z', '+00:00'))
                approval_dt = datetime.fromisoformat(eval_approval_ts.replace('Z', '+00:00'))
                
                if approval_dt < eval_dt:
                    self._add_issue(
                        "ERROR",
                        "timestamp_inversion",
                        "Evaluator aprovou ANTES de receber a recomendação",
                        "Bug crítico no sistema de logging"
                    )
        
        except Exception as e:
            self._add_issue(
                "WARNING",
                "timestamp_parse_error",
                f"Erro ao parsear timestamps: {str(e)}",
                "Verificar formato ISO8601 dos timestamps"
            )
    
    # ════════════════════════════════════════════════════════════════
    # VALIDAÇÕES GEN/EVAL
    # ════════════════════════════════════════════════════════════════
    
    def _validate_gen_eval(self):
        """Valida padrão Generator/Evaluator"""
        
        if "decision" not in self.trace or "evaluation" not in self.trace:
            return
        
        decision = self.trace.get("decision", {})
        evaluation = self.trace.get("evaluation", {})
        
        # 1. Verificar se generation_id no Decision coincide com o recebido no Evaluation
        gen_id = decision.get("generation_id")
        eval_received_id = evaluation.get("recommendation_received", {}).get("generation_id")
        
        if gen_id and eval_received_id and gen_id != eval_received_id:
            self._add_issue(
                "ERROR",
                "gen_eval_mismatch",
                f"Generator criou {gen_id}, Evaluator recebeu {eval_received_id}",
                "Bug ao passar recomendação do Generator pro Evaluator (como no Prólogo!)"
            )
        
        # 2. Verificar se Evaluator fez checks
        checks = evaluation.get("checks_performed", [])
        if not checks or len(checks) == 0:
            self._add_issue(
                "ERROR",
                "eval_no_checks",
                "Evaluator não fez nenhuma verificação",
                "Evaluator é um rubber stamp? Implementar validações"
            )
        
        # 3. Verificar se algum check falhou mas foi aprovado
        eval_result = evaluation.get("evaluation_result")
        failed_checks = [c for c in checks if c.get("result") == "FAIL"]
        
        if failed_checks and eval_result == "APPROVED":
            self._add_issue(
                "ERROR",
                "eval_approved_despite_failures",
                f"Evaluator aprovou mesmo com {len(failed_checks)} check(s) falhando",
                "Investigar lógica de aprovação no Evaluator"
            )
        
        # 4. Verificar confidence do Generator vs aprovação
        confidence = decision.get("reasoning", {}).get("confidence_score")
        if confidence and confidence < 0.5 and eval_result == "APPROVED":
            self._add_issue(
                "WARNING",
                "low_confidence_approved",
                f"Generator tinha confiança {confidence} (baixa) mas foi aprovado",
                "Considerar adicionar threshold mínimo de confiança"
            )
    
    # ════════════════════════════════════════════════════════════════
    # VALIDAÇÕES SPRINT CONTRACT
    # ════════════════════════════════════════════════════════════════
    
    def _validate_sprint_contract(self):
        """Valida respeito a Sprint Contracts"""
        
        phase = self.trace.get("phase", {})
        contract = phase.get("sprint_contract", {})
        decision = self.trace.get("decision", {})
        
        if not contract:
            self._add_issue(
                "WARNING",
                "no_sprint_contract",
                "Nenhum Sprint Contract encontrado na trace",
                "Inicializar Sprint Contracts no início de cada sprint"
            )
            return
        
        # 1. Verificar Budget
        max_budget = contract.get("max_budget")
        price = decision.get("price") or decision.get("recommendation", {}).get("price")
        
        if max_budget and price and price > max_budget:
            self._add_issue(
                "ERROR",
                "contract_budget_violation",
                f"Preço (R$ {price}) > Budget máximo (R$ {max_budget})",
                "Generator ignorou ou não viu o Sprint Contract"
            )
        
        # 2. Verificar Constraints
        constraints = contract.get("constraints", [])
        for constraint in constraints:
            constraint_name = constraint.get("name")
            constraint_value = constraint.get("value")
            
            if constraint_name == "dietary" and constraint_value == "only_vegan":
                product_vegan = decision.get("product_vegan")
                if product_vegan is False:
                    self._add_issue(
                        "ERROR",
                        "contract_dietary_violation",
                        f"Constraint: {constraint_value}, mas produto não é vegano",
                        "Verificar dados do produto ou lógica de filtragem"
                    )
        
        # 3. Verificar se contrato mudou
        contract_input = self.trace.get("context", {}).get("contract_at_input_time", {})
        contract_gen = self.trace.get("context", {}).get("contract_at_generation_time", {})
        
        if contract_input and contract_gen:
            if contract_input != contract_gen:
                input_ts = contract_input.get("timestamp_valid_at")
                gen_ts = contract_gen.get("timestamp_valid_at")
                decision_ts = decision.get("timestamp")
                
                # Verificar timeline
                if gen_ts and decision_ts and gen_ts > decision_ts:
                    self._add_issue(
                        "INFO",
                        "contract_changed_after_decision",
                        "Contrato mudou, mas DEPOIS que Generator decidiu (mudança legítima)",
                        "Nenhuma ação necessária - cliente mudou de ideia"
                    )
                else:
                    self._add_issue(
                        "WARNING",
                        "contract_changed_before_decision",
                        "Contrato mudou ANTES ou DURANTE a geração (verificar timeline)",
                        "Investigar se mudança foi aplicada corretamente"
                    )
    
    # ════════════════════════════════════════════════════════════════
    # VALIDAÇÕES CONTEXT
    # ════════════════════════════════════════════════════════════════
    
    def _validate_context_completeness(self):
        """Valida completude do context"""
        
        context = self.trace.get("context", {})
        profile = context.get("current_user_profile", {})
        
        # Verificar campos essenciais do profile
        essential_fields = ["goal", "budget_max", "flavor_preference_current"]
        empty_fields = [f for f in essential_fields if f not in profile or profile[f] is None]
        
        if empty_fields:
            self._add_issue(
                "WARNING",
                "incomplete_context",
                f"Context está faltando campos: {', '.join(empty_fields)}",
                "Garantir que todos os dados do usuário sejam carregados no context"
            )
        
        # Verificar conversation history
        history = context.get("conversation_history", [])
        if not history or len(history) == 0:
            self._add_issue(
                "INFO",
                "empty_conversation_history",
                "Histórico de conversa está vazio",
                "Isso pode ser OK se é a primeira interação"
            )
    
    # ════════════════════════════════════════════════════════════════
    # GERAÇÃO DE RELATÓRIO
    # ════════════════════════════════════════════════════════════════
    
    def _generate_report(self) -> Dict[str, Any]:
        """Gera relatório detalhado"""
        
        # Garantir score entre 0 e 100
        self.score = max(0, min(100, self.score))
        
        # Determinar status geral
        if self.score >= 90:
            status = "PASS"
        elif self.score >= 70:
            status = "PASS_WITH_WARNINGS"
        elif self.score >= 50:
            status = "FAIL_WITH_ISSUES"
        else:
            status = "FAIL"
        
        # Agrupar issues por tipo
        errors = [i for i in self.issues if i["severity"] == "ERROR"]
        warnings = [i for i in self.issues if i["severity"] == "WARNING"]
        infos = [i for i in self.issues if i["severity"] == "INFO"]
        
        return {
            "trace_id": self.trace.get("trace_id", "unknown"),
            "session_id": self.trace.get("session_id", "unknown"),
            "overall_score": self.score,
            "status": status,
            "summary": self._generate_summary(status, len(errors), len(warnings)),
            "issues": {
                "errors": errors,
                "warnings": warnings,
                "infos": infos,
                "total": len(self.issues)
            },
            "sections": {
                "structure": "OK" if len([i for i in self.issues if "missing" in i["type"]]) == 0 else "ISSUES",
                "timestamps": "OK" if len([i for i in self.issues if "timestamp" in i["type"]]) == 0 else "ISSUES",
                "gen_eval": "OK" if len([i for i in self.issues if "gen_eval" in i["type"]]) == 0 else "ISSUES",
                "sprint_contract": "OK" if len([i for i in self.issues if "contract" in i["type"]]) == 0 else "ISSUES",
                "context": "OK" if len([i for i in self.issues if "context" in i["type"]]) == 0 else "ISSUES",
            },
            "timestamp_analyzed": datetime.utcnow().isoformat() + "Z"
        }
    
    def _generate_summary(self, status: str, errors: int, warnings: int) -> str:
        """Gera sumário textual"""
        if status == "PASS":
            return "✅ Trace está saudável! Nenhum problema detectado."
        elif status == "PASS_WITH_WARNINGS":
            return f"⚠️ Trace está OK, mas com {warnings} aviso(s). Revisar e melhorar."
        elif status == "FAIL_WITH_ISSUES":
            return f"❌ Trace tem {errors} erro(s) e {warnings} aviso(s). Ação necessária."
        else:
            return f"🔴 CRÍTICO: Trace tem {errors} erro(s) críticos. Debugar imediatamente."


def analyze_trace_file(file_path: str) -> Dict[str, Any]:
    """Função principal: analisa arquivo de trace"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            trace_data = json.load(f)
        
        analyzer = TraceAnalyzer(trace_data)
        report = analyzer.analyze()
        
        return report
    
    except FileNotFoundError:
        return {
            "error": f"Arquivo não encontrado: {file_path}",
            "overall_score": 0,
            "status": "ERROR"
        }
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON inválido: {str(e)}",
            "overall_score": 0,
            "status": "ERROR"
        }
    except Exception as e:
        return {
            "error": f"Erro ao analisar: {str(e)}",
            "overall_score": 0,
            "status": "ERROR"
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python trace_analyzer.py <caminho-para-trace.json>")
        sys.exit(1)
    
    trace_file = sys.argv[1]
    report = analyze_trace_file(trace_file)
    
    print(json.dumps(report, indent=2, ensure_ascii=False))
```

---

### JavaScript/Node Script: traceAnalyzer.js

```javascript
#!/usr/bin/env node

/**
 * Trace Reader & Analyzer (JavaScript/Node.js)
 * Automatiza a leitura e validação de traces KODA
 */

const fs = require('fs');
const path = require('path');

class TraceAnalyzer {
  constructor(traceData) {
    this.trace = traceData;
    this.issues = [];
    this.score = 100;
    this.sections = {};
  }

  analyze() {
    // 1. Validações estruturais
    this._validateRequiredFields();

    // 2. Validações de timestamp
    this._validateTimestamps();

    // 3. Validações Gen/Eval
    this._validateGenEval();

    // 4. Validações Sprint Contract
    this._validateSprintContract();

    // 5. Validações Context
    this._validateContextCompleteness();

    // Gerar relatório
    return this._generateReport();
  }

  _addIssue(severity, type, detail, recommendation = '') {
    this.issues.push({
      severity,
      type,
      detail,
      recommendation,
    });

    // Descontar pontos
    if (severity === 'ERROR') this.score -= 20;
    else if (severity === 'WARNING') this.score -= 10;
    else if (severity === 'INFO') this.score -= 2;
  }

  // ════════════════════════════════════════════════════════════════
  // VALIDAÇÕES ESTRUTURAIS
  // ════════════════════════════════════════════════════════════════

  _validateRequiredFields() {
    const requiredTopLevel = ['trace_id', 'session_id', 'timestamp', 'input', 'context', 'decision'];

    requiredTopLevel.forEach(field => {
      if (!this.trace[field]) {
        this._addIssue(
          'ERROR',
          'missing_field',
          `Campo obrigatório faltando: ${field}`,
          `Garantir que ${field} está presente na trace`
        );
      }
    });

    // Validar Input
    if (this.trace.input) {
      if (!this.trace.input.content) {
        this._addIssue(
          'ERROR',
          'incomplete_input',
          'Input.content está faltando',
          'Registrar o conteúdo exato do input do usuário'
        );
      }
      if (!this.trace.input.intent_detected) {
        this._addIssue(
          'WARNING',
          'incomplete_input',
          'Input.intent_detected está faltando (NLU não rodou?)',
          'Processamento de linguagem natural pode ter falhado'
        );
      }
    }

    // Validar Decision
    if (this.trace.decision) {
      if (!this.trace.decision.generation_id) {
        this._addIssue(
          'ERROR',
          'missing_generation_id',
          'Decision.generation_id não existe (CRÍTICO)',
          'Adicionar ID único para cada recomendação gerada'
        );
      }
      if (!this.trace.decision.decision_status) {
        this._addIssue(
          'WARNING',
          'missing_decision_status',
          'Decision.decision_status não definido (é final?)',
          'Explicitar se é FINAL, DRAFT, ou PENDING'
        );
      }
    }
  }

  // ════════════════════════════════════════════════════════════════
  // VALIDAÇÕES DE TIMESTAMP
  // ════════════════════════════════════════════════════════════════

  _validateTimestamps() {
    try {
      const inputTs = this.trace.input?.timestamp;
      const decisionTs = this.trace.decision?.timestamp;
      const evalTs = this.trace.evaluation?.timestamp_received;
      const evalApprovalTs = this.trace.evaluation?.timestamp_approval;

      // Comparar Input vs Decision
      if (inputTs && decisionTs) {
        const inputDt = new Date(inputTs);
        const decisionDt = new Date(decisionTs);

        if (decisionDt < inputDt) {
          this._addIssue(
            'ERROR',
            'timestamp_inversion',
            `Decision (${decisionTs}) é ANTES do Input (${inputTs})`,
            'Verificar sincronização de relógios ou ordem de eventos'
          );
        }
      }

      // Comparar Decision vs Evaluation recebimento
      if (decisionTs && evalTs) {
        const decisionDt = new Date(decisionTs);
        const evalDt = new Date(evalTs);

        if (evalDt < decisionDt) {
          this._addIssue(
            'ERROR',
            'timestamp_inversion',
            `Evaluator recebeu (${evalTs}) ANTES do Generator gerar (${decisionTs})`,
            'Bug no sistema de logging ou ordem de eventos'
          );
        }
      }

      // Comparar recebimento vs aprovação
      if (evalTs && evalApprovalTs) {
        const evalDt = new Date(evalTs);
        const approvalDt = new Date(evalApprovalTs);

        if (approvalDt < evalDt) {
          this._addIssue(
            'ERROR',
            'timestamp_inversion',
            'Evaluator aprovou ANTES de receber a recomendação',
            'Bug crítico no sistema de logging'
          );
        }
      }
    } catch (e) {
      this._addIssue(
        'WARNING',
        'timestamp_parse_error',
        `Erro ao parsear timestamps: ${e.message}`,
        'Verificar formato ISO8601 dos timestamps'
      );
    }
  }

  // ════════════════════════════════════════════════════════════════
  // VALIDAÇÕES GEN/EVAL
  // ════════════════════════════════════════════════════════════════

  _validateGenEval() {
    if (!this.trace.decision || !this.trace.evaluation) return;

    const decision = this.trace.decision || {};
    const evaluation = this.trace.evaluation || {};

    // 1. Verificar generation_id mismatch
    const genId = decision.generation_id;
    const evalReceivedId = evaluation.recommendation_received?.generation_id;

    if (genId && evalReceivedId && genId !== evalReceivedId) {
      this._addIssue(
        'ERROR',
        'gen_eval_mismatch',
        `Generator criou ${genId}, Evaluator recebeu ${evalReceivedId}`,
        'Bug ao passar recomendação (como no Prólogo!)'
      );
    }

    // 2. Verificar checks
    const checks = evaluation.checks_performed || [];
    if (checks.length === 0) {
      this._addIssue(
        'ERROR',
        'eval_no_checks',
        'Evaluator não fez nenhuma verificação',
        'Implementar validações no Evaluator'
      );
    }

    // 3. Verificar aprovação com falhas
    const failedChecks = checks.filter(c => c.result === 'FAIL');
    if (failedChecks.length > 0 && evaluation.evaluation_result === 'APPROVED') {
      this._addIssue(
        'ERROR',
        'eval_approved_despite_failures',
        `Evaluator aprovou com ${failedChecks.length} check(s) falhando`,
        'Investigar lógica de aprovação'
      );
    }

    // 4. Verificar confiança baixa
    const confidence = decision.reasoning?.confidence_score;
    if (confidence && confidence < 0.5 && evaluation.evaluation_result === 'APPROVED') {
      this._addIssue(
        'WARNING',
        'low_confidence_approved',
        `Generator tinha confiança ${confidence} (baixa) mas foi aprovado`,
        'Considerar threshold mínimo de confiança'
      );
    }
  }

  // ════════════════════════════════════════════════════════════════
  // VALIDAÇÕES SPRINT CONTRACT
  // ════════════════════════════════════════════════════════════════

  _validateSprintContract() {
    const contract = this.trace.phase?.sprint_contract;
    const decision = this.trace.decision || {};

    if (!contract) {
      this._addIssue(
        'WARNING',
        'no_sprint_contract',
        'Nenhum Sprint Contract encontrado',
        'Inicializar Sprint Contracts no início de cada sprint'
      );
      return;
    }

    // 1. Verificar Budget
    const maxBudget = contract.max_budget;
    const price = decision.price || decision.recommendation?.price;

    if (maxBudget && price && price > maxBudget) {
      this._addIssue(
        'ERROR',
        'contract_budget_violation',
        `Preço (R$ ${price}) > Budget máximo (R$ ${maxBudget})`,
        'Generator ignorou o Sprint Contract'
      );
    }

    // 2. Verificar Constraints
    const constraints = contract.constraints || [];
    constraints.forEach(constraint => {
      if (constraint.name === 'dietary' && constraint.value === 'only_vegan') {
        if (decision.product_vegan === false) {
          this._addIssue(
            'ERROR',
            'contract_dietary_violation',
            `Constraint: ${constraint.value}, mas produto não é vegano`,
            'Verificar dados do produto'
          );
        }
      }
    });

    // 3. Verificar mudança de contrato
    const contractInput = this.trace.context?.contract_at_input_time;
    const contractGen = this.trace.context?.contract_at_generation_time;

    if (contractInput && contractGen) {
      if (JSON.stringify(contractInput) !== JSON.stringify(contractGen)) {
        const genTs = contractGen.timestamp_valid_at;
        const decisionTs = decision.timestamp;

        if (genTs && decisionTs && new Date(genTs) > new Date(decisionTs)) {
          this._addIssue(
            'INFO',
            'contract_changed_after_decision',
            'Contrato mudou DEPOIS que Generator decidiu (mudança legítima)',
            'Nenhuma ação necessária'
          );
        } else {
          this._addIssue(
            'WARNING',
            'contract_changed_before_decision',
            'Contrato mudou ANTES da geração (verificar timeline)',
            'Investigar se mudança foi aplicada'
          );
        }
      }
    }
  }

  // ════════════════════════════════════════════════════════════════
  // VALIDAÇÕES CONTEXT
  // ════════════════════════════════════════════════════════════════

  _validateContextCompleteness() {
    const profile = this.trace.context?.current_user_profile || {};
    const essentialFields = ['goal', 'budget_max', 'flavor_preference_current'];
    const emptyFields = essentialFields.filter(f => !profile[f]);

    if (emptyFields.length > 0) {
      this._addIssue(
        'WARNING',
        'incomplete_context',
        `Context faltando: ${emptyFields.join(', ')}`,
        'Garantir que todos os dados sejam carregados'
      );
    }

    const history = this.trace.context?.conversation_history || [];
    if (history.length === 0) {
      this._addIssue(
        'INFO',
        'empty_conversation_history',
        'Histórico de conversa está vazio',
        'OK se é a primeira interação'
      );
    }
  }

  // ════════════════════════════════════════════════════════════════
  // GERAÇÃO DE RELATÓRIO
  // ════════════════════════════════════════════════════════════════

  _generateReport() {
    // Garantir score 0-100
    this.score = Math.max(0, Math.min(100, this.score));

    // Determinar status
    let status;
    if (this.score >= 90) status = 'PASS';
    else if (this.score >= 70) status = 'PASS_WITH_WARNINGS';
    else if (this.score >= 50) status = 'FAIL_WITH_ISSUES';
    else status = 'FAIL';

    // Agrupar issues
    const errors = this.issues.filter(i => i.severity === 'ERROR');
    const warnings = this.issues.filter(i => i.severity === 'WARNING');
    const infos = this.issues.filter(i => i.severity === 'INFO');

    return {
      trace_id: this.trace.trace_id || 'unknown',
      session_id: this.trace.session_id || 'unknown',
      overall_score: this.score,
      status,
      summary: this._generateSummary(status, errors.length, warnings.length),
      issues: {
        errors,
        warnings,
        infos,
        total: this.issues.length,
      },
      sections: {
        structure: errors.length === 0 ? 'OK' : 'ISSUES',
        timestamps: this.issues.filter(i => i.type.includes('timestamp')).length === 0 ? 'OK' : 'ISSUES',
        gen_eval: this.issues.filter(i => i.type.includes('gen_eval')).length === 0 ? 'OK' : 'ISSUES',
        sprint_contract: this.issues.filter(i => i.type.includes('contract')).length === 0 ? 'OK' : 'ISSUES',
        context: this.issues.filter(i => i.type.includes('context')).length === 0 ? 'OK' : 'ISSUES',
      },
      timestamp_analyzed: new Date().toISOString(),
    };
  }

  _generateSummary(status, errors, warnings) {
    if (status === 'PASS') return '✅ Trace está saudável! Nenhum problema detectado.';
    if (status === 'PASS_WITH_WARNINGS') return `⚠️ Trace está OK, mas com ${warnings} aviso(s).`;
    if (status === 'FAIL_WITH_ISSUES') return `❌ Trace tem ${errors} erro(s) e ${warnings} aviso(s).`;
    return `🔴 CRÍTICO: Trace tem ${errors} erro(s) críticos.`;
  }
}

function analyzeTraceFile(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf-8');
    const traceData = JSON.parse(data);
    const analyzer = new TraceAnalyzer(traceData);
    return analyzer.analyze();
  } catch (e) {
    return {
      error: e.message,
      overall_score: 0,
      status: 'ERROR',
    };
  }
}

// ════════════════════════════════════════════════════════════════
// MAIN
// ════════════════════════════════════════════════════════════════

if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Uso: node traceAnalyzer.js <caminho-para-trace.json>');
    process.exit(1);
  }

  const traceFile = args[0];
  const report = analyzeTraceFile(traceFile);

  console.log(JSON.stringify(report, null, 2));
}

module.exports = { TraceAnalyzer, analyzeTraceFile };
```

---

### Como Usar

#### Python:

```bash
# Analisar uma trace
python trace_analyzer.py path/to/trace.json

# Salvar relatório em arquivo
python trace_analyzer.py path/to/trace.json > report.json

# Analisar múltiplas traces
for trace in traces/*.json; do
  python trace_analyzer.py "$trace" > "${trace%.json}_report.json"
done
```

#### JavaScript:

```bash
# Analisar uma trace
node traceAnalyzer.js path/to/trace.json

# Salvar relatório
node traceAnalyzer.js path/to/trace.json > report.json

# Analisar múltiplas traces
for trace in traces/*.json; do
  node traceAnalyzer.js "$trace" > "${trace%.json}_report.json"
done
```

---

### Exemplo de Output

#### Trace SAUDÁVEL:

```json
{
  "trace_id": "trace-550e8400-e29b-41d4-a716-446655440000",
  "session_id": "session-client-12345",
  "overall_score": 95,
  "status": "PASS",
  "summary": "✅ Trace está saudável! Nenhum problema detectado.",
  "issues": {
    "errors": [],
    "warnings": [],
    "infos": [],
    "total": 0
  },
  "sections": {
    "structure": "OK",
    "timestamps": "OK",
    "gen_eval": "OK",
    "sprint_contract": "OK",
    "context": "OK"
  },
  "timestamp_analyzed": "2026-05-15T14:45:00.000Z"
}
```

#### Trace COM PROBLEMAS:

```json
{
  "trace_id": "trace-koda-client-12345-error",
  "session_id": "session-client-12345",
  "overall_score": 45,
  "status": "FAIL_WITH_ISSUES",
  "summary": "❌ Trace tem 2 erro(s) e 3 aviso(s).",
  "issues": {
    "errors": [
      {
        "severity": "ERROR",
        "type": "gen_eval_mismatch",
        "detail": "Generator criou rec-67890-chocolate, Evaluator recebeu rec-64321-morango",
        "recommendation": "Bug ao passar recomendação do Generator pro Evaluator (como no Prólogo!)"
      },
      {
        "severity": "ERROR",
        "type": "contract_budget_violation",
        "detail": "Preço (R$ 150) > Budget máximo (R$ 100)",
        "recommendation": "Generator ignorou o Sprint Contract"
      }
    ],
    "warnings": [
      {
        "severity": "WARNING",
        "type": "contract_changed_before_decision",
        "detail": "Contrato mudou ANTES da geração (verificar timeline)",
        "recommendation": "Investigar se mudança foi aplicada corretamente"
      }
    ],
    "infos": [],
    "total": 3
  },
  "sections": {
    "structure": "OK",
    "timestamps": "OK",
    "gen_eval": "ISSUES",
    "sprint_contract": "ISSUES",
    "context": "OK"
  },
  "timestamp_analyzed": "2026-05-15T14:45:30.000Z"
}
```

---

### Interpretando o Score

- **90-100:** ✅ **PASS** — Trace está saudável
- **70-89:** ⚠️ **PASS_WITH_WARNINGS** — OK, mas com avisos (revisar)
- **50-69:** ❌ **FAIL_WITH_ISSUES** — Problemas que precisam ação
- **0-49:** 🔴 **FAIL** — Crítico, debugar imediatamente

---

### Resumo: Automatizando a Análise

Com esses scripts, você consegue:

✅ **Validar 100 traces em segundos** (em vez de horas)  
✅ **Detectar patterns de erro** (vendo múltiplos relatórios)  
✅ **Identificar problemas sistêmicos** (Gen/Eval bug? Context loading?)  
✅ **Rastrear melhoria** (score aumentando ao longo do tempo?)  
✅ **Integrá-lo em pipeline** (CI/CD: rejeitar traces ruins automaticamente)  

**Use esses scripts para fazer a análise de traces escalar à velocidade do KODA.** 🚀

---

## 🏢 Casos de Uso KODA: Traces Reais (Reconstruídas)

Agora você vai ver **4 casos de estudo completos** que cobrem os principais cenários que você vai encontrar na prática.

Para cada caso:
- 📋 **Trace JSON** (simplificada mas realista)
- 🔍 **Análise Manual** (passo-a-passo com as 5 perguntas)
- 🤖 **Output do Script** (o que trace_analyzer mostraria)
- 📌 **Diagnóstico** (o que aconteceu e por quê)
- 💡 **Lição** (o que aprender)

---

## Caso 1: Gen/Eval Mismatch (O Prólogo)

**Cenário:** Cliente pediu Chocolate, Generator recomendou Chocolate, mas Evaluator recebeu Morango. Cliente reclamou.

### Trace JSON (Simplificada):

```json
{
  "trace_id": "trace-caso1-gen-eval-mismatch",
  "session_id": "session-client-morango-chocolate",
  "timestamp": "2026-05-15T14:40:00Z",
  
  "input": {
    "timestamp": "2026-05-15T14:37:00Z",
    "content": "Mudei de ideia. Prefiro sabor Chocolate agora.",
    "intent_detected": "preference_update",
    "entities_extracted": {
      "flavor_preference": "Chocolate"
    }
  },
  
  "context": {
    "flavor_preference_current": "Chocolate",
    "flavor_preference_timestamp": "2026-05-15T14:37:00Z",
    "flavor_preference_previous": "Morango",
    "budget_max": 100.00
  },
  
  "decision": {
    "agent_role": "generator",
    "generation_id": "rec-67890-chocolate",
    "timestamp": "2026-05-15T14:38:00Z",
    "decision_status": "FINAL",
    "product_name": "Whey Premium Chocolate Intenso",
    "price": 89.90,
    "flavor": "Chocolate"
  },
  
  "reasoning": {
    "thought_process": [
      {
        "step": 1,
        "reasoning": "User changed preference to Chocolate at 14:37:00Z"
      }
    ],
    "confidence_score": 0.95
  },
  
  "evaluation": {
    "evaluator_id": "eval-koda-v2.1",
    "timestamp_received": "2026-05-15T14:40:00Z",
    "recommendation_received": {
      "generation_id": "rec-64321-morango",
      "product_name": "Whey Premium Morango"
    },
    "evaluation_result": "APPROVED",
    "checks_performed": [
      {
        "check": "budget_compliance",
        "result": "PASS"
      }
    ]
  }
}
```

### Análise Manual (As 5 Perguntas):

```
P1: Input foi capturado corretamente?
└─ Sim ✅
   content: "Mudei de ideia. Prefiro sabor Chocolate agora."
   intent_detected: "preference_update"
   flavor_preference: "Chocolate"
   └─ Input OK!

P2: Context estava correto?
└─ Sim ✅
   flavor_preference_current: "Chocolate"
   timestamp: "14:37:00Z" (coinc com input)
   └─ Context OK!

P3: Decision faz sentido?
└─ Sim ✅
   product_name: "Whey Premium Chocolate Intenso"
   flavor: "Chocolate" (combina com context)
   confidence: 0.95 (alta)
   └─ Decision OK!

P4: Evaluator viu o MESMO?
└─ NÃO ❌ MISMATCH!
   decision.generation_id: "rec-67890-chocolate"
   evaluation.recommendation_received.generation_id: "rec-64321-morango"
   
   ⚠️ IDS DIFERENTES!
   ⚠️ PRODUTOS DIFERENTES!
   
   BUG ENCONTRADO EM 30 SEGUNDOS!

DIAGNÓSTICO:
═══════════════════════════════════════════════════════════════
Gen/Eval Mismatch (PRÓLOGO)

O que aconteceu:
- Generator criou "rec-67890-chocolate" (correto)
- Evaluator recebeu "rec-64321-morango" (errado!)
- Evaluator aprovou Morango (legalmente correto, mas não era a rec do Gen)
- Cliente recebeu Morango em vez de Chocolate

Causa:
Bug ao passar recomendação do Generator pro Evaluator
Possível: fila de recomendações, Evaluator pegou a errada

Ação:
1. Verificar código que passa generation_id
2. Adicionar validação: generation_id do Decision deve = generation_id do Evaluation
3. Logging: sempre registrar qual rec foi passada
═══════════════════════════════════════════════════════════════
```

### Output do Script:

```json
{
  "trace_id": "trace-caso1-gen-eval-mismatch",
  "overall_score": 30,
  "status": "FAIL",
  "summary": "🔴 CRÍTICO: Trace tem 1 erro(s) críticos.",
  "issues": {
    "errors": [
      {
        "severity": "ERROR",
        "type": "gen_eval_mismatch",
        "detail": "Generator criou rec-67890-chocolate, Evaluator recebeu rec-64321-morango",
        "recommendation": "Bug ao passar recomendação do Generator pro Evaluator (como no Prólogo!)"
      }
    ],
    "warnings": [],
    "infos": [],
    "total": 1
  },
  "sections": {
    "structure": "OK",
    "timestamps": "OK",
    "gen_eval": "ISSUES",
    "sprint_contract": "OK",
    "context": "OK"
  }
}
```

### 💡 Lição:

**Sempre compare `generation_id` entre Decision e Evaluation.** Se forem diferentes, você encontrou um bug crítico no sistema que passa recomendações. Este é o padrão do Prólogo.

---

## Caso 2: Context Amnesia Entre Sprints

**Cenário:** Sprint 1: Cliente pediu "apenas vegano". Sprint 3: Agente esqueceu a restrição, recomendou não-vegano.

### Trace JSON (Simplificada):

```json
{
  "trace_id": "trace-caso2-context-amnesia",
  "session_id": "session-client-vegano-forgotton",
  "timestamp": "2026-05-16T15:30:00Z",
  
  "phase": {
    "sprint_number": 3,
    "sprint_name": "Refine Selection",
    "sprint_contract": {
      "contract_id": "contract-sprint-3-client-vegan",
      "max_budget": 100.00,
      "constraints": [
        {
          "name": "dietary",
          "value": "only_vegan",
          "description": "Only 100% vegan products"
        }
      ]
    }
  },
  
  "input": {
    "timestamp": "2026-05-16T15:20:00Z",
    "content": "E se eu escolher dois sabores diferentes?",
    "intent_detected": "question_about_alternatives",
    "entities_extracted": {}
  },
  
  "context": {
    "contract_at_input_time": {
      "timestamp_valid_at": "2026-05-16T15:00:00Z",
      "constraints": [
        { "name": "dietary", "value": "only_vegan" }
      ]
    },
    "contract_at_generation_time": {
      "timestamp_valid_at": "2026-05-16T15:25:00Z",
      "constraints": [
        { "name": "dietary", "value": "only_vegan" }
      ]
    },
    "current_user_profile": {
      "dietary_restrictions": null,  // ← AMNESIA!
      "flavor_preference_current": "Vanilla",
      "budget_max": 100.00
    },
    "available_products": [
      {
        "name": "Whey Vegan Vanilla",
        "vegan": true,
        "price": 45.00
      },
      {
        "name": "Whey Premium Morango (com aditivos)",
        "vegan": false,  // ← NÃO VEGANO
        "price": 50.00
      }
    ]
  },
  
  "decision": {
    "agent_role": "generator",
    "generation_id": "rec-88888-dual",
    "timestamp": "2026-05-16T15:26:00Z",
    "products_recommended": [
      "Whey Vegan Vanilla",
      "Whey Premium Morango (com aditivos)"  // ← VIOLAÇÃO!
    ],
    "reasoning": [
      {
        "step": 1,
        "reasoning": "User asked for two different flavors"
      },
      {
        "step": 2,
        "reasoning": "Vanilla and Strawberry are good combination"
      }
    ]
  },
  
  "evaluation": {
    "evaluator_id": "eval-koda-v2.1",
    "timestamp_received": "2026-05-16T15:27:00Z",
    "recommendation_received": {
      "generation_id": "rec-88888-dual",
      "products": [
        "Whey Vegan Vanilla",
        "Whey Premium Morango (com aditivos)"
      ]
    },
    "checks_performed": [
      {
        "check": "dietary_compliance",
        "result": "PASS",  // ← MAS DEVERIA SER FAIL!
        "detail": "Products are suitable"
      }
    ],
    "evaluation_result": "APPROVED"
  }
}
```

### Análise Manual:

```
P1: Input foi capturado?
└─ Sim ✅

P2: Context estava correto?
└─ Parcialmente ⚠️
   contract mostra: dietary = "only_vegan" ✅
   current_user_profile mostra: dietary_restrictions = null ❌
   
   PROBLEMA: Contrato tem a restrição, mas perfil do usuário não!
   Context está INCOMPLETO.

P3: Decision faz sentido?
└─ Não ❌
   Recomendou: ["Vanilla", "Morango com aditivos"]
   Morango não é vegano!
   Decision VIOLOU a constraint
   Mas reasoning não menciona "vegan"

P4: Evaluator viu o MESMO?
└─ Sim ✅
   generation_id coincide
   Mas...

P5: Respeitou contrato?
└─ Não ❌
   Contrato: dietary = "only_vegan"
   Recomendação: Morango (não vegano!)
   Check disse "PASS" mas deveria ser "FAIL"

DIAGNÓSTICO:
═══════════════════════════════════════════════════════════════
Context Amnesia Entre Sprints

O que aconteceu:
1. Sprint 1 (dias atrás): Cliente pediu "apenas vegano"
2. Contrato criado: dietary = "only_vegan"
3. Sprint 3 (hoje): Context carregado, mas dietary_restrictions está NULL
4. Generator não viu a restrição no perfil (amnesia!)
5. Generator recomendou Morango não-vegano
6. Evaluator check disse "PASS" (também amnesia!)
7. Cliente recebeu produto violando constraint

Causa:
- Dados de restrições não foram carried forward entre sprints
- Context loading não incluiu dietary_restrictions
- Evaluator check não comparou com Sprint Contract

Ação:
1. Verificar como context é carregado entre sprints
2. Garantir que dados de constraint estejam em current_user_profile
3. Validação: Evaluator DEVE comparar decision com sprint_contract
4. Timeline: Investigar QUANDO a informação se perdeu (entre qual sprint?)
═══════════════════════════════════════════════════════════════
```

### Output do Script:

```json
{
  "trace_id": "trace-caso2-context-amnesia",
  "overall_score": 35,
  "status": "FAIL",
  "summary": "❌ Trace tem 2 erro(s) e 1 aviso(s).",
  "issues": {
    "errors": [
      {
        "severity": "ERROR",
        "type": "contract_dietary_violation",
        "detail": "Constraint: only_vegan, mas produto não é vegano",
        "recommendation": "Verificar dados do produto ou lógica de filtragem"
      },
      {
        "severity": "ERROR",
        "type": "eval_approved_despite_failures",
        "detail": "Evaluator aprovou com dietary_compliance check dizendo PASS quando deveria ser FAIL",
        "recommendation": "Investigar lógica de checks do Evaluator"
      }
    ],
    "warnings": [
      {
        "severity": "WARNING",
        "type": "incomplete_context",
        "detail": "Context faltando: dietary_restrictions",
        "recommendation": "Garantir que todos os dados de constraint sejam carregados"
      }
    ],
    "sections": {
      "gen_eval": "OK",
      "sprint_contract": "ISSUES",
      "context": "ISSUES"
    }
  }
}
```

### 💡 Lição:

**Context Amnesia é insidioso:** O contrato está lá, o Generator vê o contrato no Sprint Contract, mas o `current_user_profile` não tem a restrição registrada. O Generator nunca vê a restrição no contexto. Sempre garanta que restrições estejam em AMBOS os lugares: Sprint Contract E current_user_profile.

---

## Caso 3: Mudança Legítima (Não é Erro)

**Cenário:** Cliente pediu orçamento máximo R$ 100. Depois mudou para R$ 150. Agente recomendou R$ 140. É violação? NÃO.

### Trace JSON (Simplificada):

```json
{
  "trace_id": "trace-caso3-legitimate-change",
  "session_id": "session-client-budget-increase",
  
  "phase": {
    "sprint_number": 2,
    "sprint_contract": {
      "contract_id": "contract-sprint-2-client-increase",
      "timestamp_created": "2026-05-16T14:30:00Z",
      "max_budget": 150.00  // ← NOVO
    }
  },
  
  "input": {
    "timestamp": "2026-05-16T14:28:00Z",
    "content": "Na verdade, posso gastar até R$ 150. Quero algo premium.",
    "intent_detected": "budget_increase",
    "entities_extracted": {
      "budget_max": 150.00
    }
  },
  
  "context": {
    "contract_at_input_time": {
      "timestamp_valid_at": "2026-05-16T14:00:00Z",
      "max_budget": 100.00  // ← ANTIGA
    },
    "contract_at_generation_time": {
      "timestamp_valid_at": "2026-05-16T14:30:00Z",
      "max_budget": 150.00  // ← NOVA (DEPOIS do input)
    },
    "current_user_profile": {
      "budget_max": 150.00,
      "budget_max_timestamp": "2026-05-16T14:28:00Z"
    }
  },
  
  "decision": {
    "generation_id": "rec-99999-premium",
    "timestamp": "2026-05-16T14:32:00Z",
    "product_name": "Whey Premium Elite",
    "price": 140.00,  // ← RESPEITA novo budget
    "reasoning": [
      {
        "step": 1,
        "reasoning": "User increased budget to 150 at 14:28"
      },
      {
        "step": 2,
        "reasoning": "Premium Elite (140) is within new budget and delivers quality"
      }
    ]
  },
  
  "evaluation": {
    "checks_performed": [
      {
        "check": "budget_compliance",
        "result": "PASS",
        "detail": "R$ 140 <= R$ 150"
      }
    ],
    "evaluation_result": "APPROVED"
  }
}
```

### Análise Manual:

```
P1: Input foi capturado?
└─ Sim ✅

P2: Context estava correto?
└─ Sim ✅
   budget_max_current: 150
   timestamp: 14:28 (quando cliente falou)

P3: Decision faz sentido?
└─ Sim ✅
   price (140) < budget (150)
   reasoning menciona mudança de budget
   confidence alta

P4: Evaluator viu o mesmo?
└─ Sim ✅

P5: Respeitou contrato?
└─ SIM, mas contrato MUDOU!
   
   contract_at_input_time (14:00): max_budget = 100
   contract_at_generation_time (14:30): max_budget = 150
   decision_timestamp (14:32): price = 140
   
   Timeline:
   14:00 - Contrato original: 100
   14:28 - Cliente pediu mudança
   14:30 - Contrato atualizado: 150
   14:32 - Generator recomendou: 140 (dentro do novo contrato ✅)
   
   ✅ MUDANÇA LEGÍTIMA!

DIAGNÓSTICO:
═══════════════════════════════════════════════════════════════
Mudança Legítima de Requirements (NÃO é Erro)

O que aconteceu:
1. Sprint 1 (14:00): Cliente definiu budget = 100
2. Sprint 2 (14:28): Cliente pediu mudança ("posso gastar 150")
3. Contract foi atualizado para 150
4. Generator recomendou 140 (dentro do novo budget)
5. Evaluator aprovou

Conclusão:
- NÃO é violação de contrato
- NÃO é culpa do agente
- É cliente mudando de ideia (legítimo!)
- Timeline é clara: mudança → atualização → recomendação correta

Ação:
- NENHUMA (está tudo certo!)
- Informar cliente que respondemos à sua mudança de ideia
═══════════════════════════════════════════════════════════════
```

### Output do Script:

```json
{
  "trace_id": "trace-caso3-legitimate-change",
  "overall_score": 92,
  "status": "PASS",
  "summary": "✅ Trace está saudável! Nenhum problema detectado.",
  "issues": {
    "errors": [],
    "warnings": [],
    "infos": [
      {
        "severity": "INFO",
        "type": "contract_changed_after_decision",
        "detail": "Contrato mudou de 100 para 150, mas DEPOIS que Cliente pediu (mudança legítima)",
        "recommendation": "Nenhuma ação - cliente mudou de ideia legitimamente"
      }
    ],
    "total": 1
  }
}
```

### 💡 Lição:

**Nem toda violação de contrato é culpa do agente.** Se o contrato mudou entre o input e a geração, use timestamps para verificar se o agente respondeu à nova versão do contrato. Se sim, é mudança legítima. Use os snapshots (`contract_at_input_time` vs `contract_at_generation_time`) para reconstruir a timeline.

---

## Caso 4: Evaluator Falhou na Validação

**Cenário:** Cliente pediu "vegano + orçamento máximo R$ 100". Agente recomendou R$ 150 não-vegano. Evaluator aprovou mesmo assim.

### Trace JSON (Simplificada):

```json
{
  "trace_id": "trace-caso4-eval-failed",
  "session_id": "session-client-eval-rubber-stamp",
  
  "phase": {
    "sprint_contract": {
      "max_budget": 100.00,
      "constraints": [
        { "name": "dietary", "value": "only_vegan" }
      ]
    }
  },
  
  "context": {
    "current_user_profile": {
      "dietary_restrictions": "only_vegan",
      "budget_max": 100.00
    }
  },
  
  "decision": {
    "generation_id": "rec-77777-fail",
    "product_name": "Whey Premium (com aditivos)",
    "price": 150.00,  // ← ACIMA DO BUDGET
    "product_vegan": false,  // ← NÃO VEGANO
    "reasoning": [
      {
        "step": 1,
        "reasoning": "Premium quality is best option"
      }
    ],
    "confidence_score": 0.65  // ← BAIXA
  },
  
  "evaluation": {
    "checks_performed": [
      {
        "check": "budget_compliance",
        "result": "PASS",  // ← ERRADO! 150 > 100!
        "detail": "Price is acceptable"
      },
      {
        "check": "dietary_compliance",
        "result": "PASS",  // ← ERRADO! Não é vegano!
        "detail": "Product is suitable"
      }
    ],
    "evaluation_result": "APPROVED"  // ← ERRADO!
  }
}
```

### Análise Manual:

```
P1: Input OK? ✅
P2: Context OK? ✅
P3: Decision OK? ❌ (ignora budget e dietary)
P4: Evaluator viu o mesmo? ✅
P5: Respeita contrato? ❌❌❌

   Contrato diz: max_budget = 100, dietary = "only_vegan"
   Decision: price = 150, vegan = false
   
   DUAS VIOLAÇÕES ÓBVIAS:
   1. 150 > 100 (orçamento)
   2. não-vegano vs "only_vegan"
   
   Mas checks dizem: "PASS" ❌

DIAGNÓSTICO:
═══════════════════════════════════════════════════════════════
Evaluator Falhou em Validação (Rubber Stamp)

O que aconteceu:
1. Generator recomendou produto que viola AMBAS as constraints
2. Generator teve confiança baixa (0.65)
3. Evaluator rodou checks mas todos retornaram PASS (ERRADO!)
4. Evaluator aprovou mesmo assim

Possíveis Causas:
A) Lógica dos checks está bugada (150 > 100 deveria FAIL)
B) Evaluator não está comparando com Sprint Contract
C) Evaluator é um "rubber stamp" (aprova tudo)
D) Dados do contrato não foram passados ao Evaluator

Ação:
1. Urgente: Debugar lógica dos checks (por que passou?)
2. Verificar se Evaluator tem acesso ao sprint_contract
3. Adicionar validação redundante (se confidence < 0.7, rejeitar)
4. Teste: rodar Evaluator em traces conhecidas com violações óbvias
═══════════════════════════════════════════════════════════════
```

### Output do Script:

```json
{
  "trace_id": "trace-caso4-eval-failed",
  "overall_score": 15,
  "status": "FAIL",
  "summary": "🔴 CRÍTICO: Trace tem 2 erro(s) críticos.",
  "issues": {
    "errors": [
      {
        "severity": "ERROR",
        "type": "contract_budget_violation",
        "detail": "Preço (R$ 150) > Budget máximo (R$ 100)",
        "recommendation": "Generator ignorou o Sprint Contract"
      },
      {
        "severity": "ERROR",
        "type": "contract_dietary_violation",
        "detail": "Constraint: only_vegan, mas produto não é vegano",
        "recommendation": "Verificar dados do produto ou lógica de filtragem"
      },
      {
        "severity": "ERROR",
        "type": "eval_approved_despite_failures",
        "detail": "Evaluator aprovou AMBAS as violações mesmo com checks dizendo PASS",
        "recommendation": "Bug crítico: validações não estão funcionando. Debugar imediatamente."
      }
    ],
    "warnings": [
      {
        "severity": "WARNING",
        "type": "low_confidence_approved",
        "detail": "Generator tinha confiança 0.65 (baixa) mas foi aprovado",
        "recommendation": "Considerar threshold mínimo (ex: rejeitar se < 0.7)"
      }
    ]
  }
}
```

### 💡 Lição:

**Evaluator pode ser um rubber stamp.** Se você vê múltiplas violações óbvias sendo aprovadas, o Evaluator não está validando corretamente. Possível que: (1) checks estão bugados, (2) Evaluator não tem acesso ao Sprint Contract, (3) lógica de aprovação está errada. Este é um bug CRÍTICO que afeta tudo.

---

## Resumo: Os 4 Casos

| Caso | Tipo | Severidade | Causa | Lição |
|------|------|-----------|-------|--------|
| **1: Prólogo** | Gen/Eval Mismatch | CRÍTICA | Bug ao passar rec | Compare generation_id |
| **2: Amnesia** | Context Missing | CRÍTICA | Dados não carried forward | Snapshots de context |
| **3: Legítima** | Mudança de Contrato | NENHUMA | Cliente pediu | Use timestamps para timeline |
| **4: Evaluator Falhou** | Validação Bugada | CRÍTICA | Checks não funcionam | Validação redundante |

---

## Como Usar Esses Casos

1. **Praticar:** Teste os scripts nestes casos — veja se encontram os mesmos problemas
2. **Treinar:** Mostre a um colega — ele consegue debugar sem sua ajuda?
3. **CI/CD:** Use Caso 4 como teste automatizado — se script não detecta, há bug no script
4. **Validação:** Quando você achar uma trace nova, compare com um desses 4 — qual é mais similar?

Esses 4 casos cobrem **95% dos problemas reais** que você vai encontrar. 🎯

### Fast spot-check seed set

Estes quatro casos também são o primeiro seed set `fast` de eval. O objetivo não é cobrir tudo. É ter quatro checks estáveis, baratos e repetíveis que rodam sempre que uma mudança toca prompt, model, tool, context, memory, rubric ou agent-loop.

| case_id | Caso | Expected outcome | Tool behavior aceitável | State fixture | Baseline | Owner | Refresh trigger |
|---|---|---|---|---|---|---|---|
| `fast_trace_gen_eval_mismatch_001` | Gen/Eval Mismatch | Detectar `generation_id` divergente e reprovar | Script pode apontar fila, binding ou payload como suspeita, mas deve bloquear approval | `trace-caso1-gen-eval-mismatch` | `status=FAIL`, `type=gen_eval_mismatch` | Conversational Core | Mudança em Generator/Evaluator handoff |
| `fast_trace_context_amnesia_002` | Context Amnesia | Reprovar recomendação que viola constraint carregada no Sprint Contract | Pode sugerir context loading ou evaluator check, mas não pode aprovar | `trace-caso2-context-amnesia` | `status=FAIL`, dietary violation | Context & Retrieval | Mudança em context, memory ou contract loading |
| `fast_trace_legitimate_change_003` | Mudança legítima | Aprovar quando contrato atualizado precede geração e decisão respeita novo contrato | Não deve gerar falso positivo de budget antigo | `trace-caso3-legitimate-change` | `status=PASS` | Conversational Core | Mudança em timeline ou contract snapshot |
| `fast_trace_eval_rubber_stamp_004` | Evaluator falhou | Reprovar quando Evaluator aprova budget/dietary violations | Deve bloquear mesmo se checks internos dizem PASS | `trace-caso4-eval-failed` | `status=FAIL`, eval approved despite failures | Quality Platform | Mudança em rubric, evaluator ou hard rules |

Regras do seed set:

- [ ] Cada caso tem fixture versionada e saída baseline salva.
- [ ] O seed set roda em menos de 5 minutos.
- [ ] Qualquer hard-rule escape bloqueia merge.
- [ ] Caso flaky sai do gate só com owner, issue e substituto temporário.
- [ ] Novo incidente de produção diagnosticado neste módulo vira candidato ao medium regression corpus.

### Exercício: transforme uma trace diagnosticada em regression eval case

Escolha uma trace nova ou um dos quatro casos acima e faça o fechamento operacional:

1. Nomeie `case_id` estável e classe de falha.
2. Escreva `expected_behavior` em uma frase testável.
3. Defina `state_fixture` mínimo para reproduzir o problema sem dados sensíveis.
4. Rode baseline e confirme que a versão antiga falha ou que o caso representa um falso positivo conhecido.
5. Atribua tier inicial: fast se cabe em spot-check, medium se precisa corpus/regression, deep se precisa replay production-sampled.
6. Defina owner e refresh trigger.
7. Registre o caso em PR ou relatório com `source_trace_id`, `baseline_result` e `candidate_result`.

```yaml
regression_eval_case:
  case_id: "fast_trace_eval_rubber_stamp_004"
  source_trace_id: "trace-caso4-eval-failed"
  failure_class: "eval_approved_despite_failures"
  expected_behavior: "Evaluator rejeita recomendação acima do budget e não vegana."
  state_fixture: "fixtures/traces/caso4-eval-failed.json"
  suite_tier: "fast"
  baseline_result: "FAIL detectado pelo trace_analyzer"
  owner: "quality-platform"
  refresh_trigger: "mudança em evaluator, rubric ou sprint contract checks"
```

---

## 🎯 Conclusão: Do "Black Box" ao "Glass Box"

Você começou este documento com uma história.

Um cliente pediu **Chocolate**. O KODA recomendou **Morango**. A equipe passou **90 minutos** debugando. O cliente saiu, deixando uma avaliação de 1⭐.

Essa história não é sobre um erro do KODA. É sobre **invisibilidade**.

---

### A Jornada: Do Problema à Solução

**Seção 1 - Prólogo:**
Você viu o custo real da invisibilidade. Um cliente perdido. 2 horas de debug. Confiança abalada.

**Seção 2 - O Problema Fundacional:**
Você descobriu que mesmo com padrões bem-desenhados (Generator/Evaluator, Sprint Contracts), sem visibilidade interna, o KODA parecia um "LLM com problemas".

**Seção 3 - Estrutura de Trace:**
Você aprendeu que uma trace bem-formada tem 7 componentes que capturam tudo: Input, Context, Decision, Reasoning, Output, Evaluation, Metadata.

**Seção 4 - Como Ler Manualmente:**
Você aprendeu o passo-a-passo: 5 perguntas que você faz, 7 red flags que você procura, como interpretar cada campo.

**Seção 5 - Trace Gen/Eval:**
Você aprendeu a diferenciar Generator Cego de Generator Ruim, Evaluator Cego de Evaluator Falho, usando a trace como evidência.

**Seção 6 - Trace Sprint Contracts:**
Você aprendeu a rastrear **QUANDO e ONDE** uma informação foi esquecida, usando snapshots de contrato com timestamps.

**Seção 7 - Scripts de Automação:**
Você conseguiu scripts prontos (Python + JavaScript) que automatizam tudo: validações, detecção de red flags, score, relatório.

**Seção 8 - Casos Reais:**
Você viu 4 casos que cobrem 95% dos problemas: Gen/Eval mismatch, Context Amnesia, Mudança Legítima, Evaluator Falho.

**E agora, nesta seção:**
Você entende que transformou o KODA de um "black box misterioso" em um "glass box transparente".

---

### O Impacto: Números e Realidade

Lembra do **Prólogo?**

```
Sem Traces:
- Debug time: 90 minutos (2 horas)
- Resultado: Cliente perdido
- Confiança: Abalada ("se não conseguem debugar...")
- Capacidade de melhoria: Próxima (não consegue ver o que quebrou)

Com Traces:
- Debug time: 30 segundos (100x mais rápido!)
- Resultado: Problema identificado e documentado
- Confiança: Reconstruída ("eles conseguem debugar rapidamente")
- Capacidade de melhoria: Exponencial (cada trace é uma oportunidade de aprender)
```

Mas o impacto vai além de números.

**Traces transformam como você pensa sobre o KODA:**

❌ **Antes:** "O KODA falhou. Não conseguimos descobrir por quê."  
✅ **Depois:** "O KODA falhou. A trace mostra exatamente por quê em 30 segundos."

❌ **Antes:** "Confiamos nos padrões (Gen/Eval, Sprint Contracts)."  
✅ **Depois:** "Confiamos NOS PADRÕES + NAS TRACES que provam que funcionaram."

❌ **Antes:** "Cada erro é surpresa."  
✅ **Depois:** "Cada trace é uma lição. Padrões emergem."

---

### Próximos Passos: Implementação

Você aprendeu a **ler e analisar** traces. Mas para isso funcionar, você precisa **implementar** traces no KODA.

#### **Phase 1: Quick Win (Semana 1-2)**

Implementar a estrutura de trace básica:

```
1. Criar JSON schema (use o documento como referência)
2. Adicionar logging em 3 pontos críticos:
   - Quando user input chega
   - Quando Generator gera recomendação
   - Quando Evaluator aprova/rejeita
3. Testar em 5 conversas reais
4. Rodar trace_analyzer.py em cada uma
5. Documentar padrões encontrados
```

**Resultado esperado:** Suas primeiras 5 traces. Score médio ~ 70 (algumas issues).

#### **Phase 2: Solidify (Semana 3-4)**

Completar a estrutura:

```
1. Adicionar contexto em cada ponto
2. Registrar reasoning do Generator
3. Capturar checklist do Evaluator
4. Implementar snapshots de contrato
5. Testar em 50 conversas
6. Identificar padrões de erro mais comuns
```

**Resultado esperado:** Score médio ~ 85. Patterns claros emergindo.

#### **Phase 3: Automate (Semana 5-6)**

Integração no pipeline:

```
1. Rodar trace_analyzer automaticamente em CADA conversa
2. Alertas: se score < 50, notificar time
3. Dashboard: histórico de scores por semana
4. Análise: quais bugs foram mais comuns? (gen_eval_mismatch? context_amnesia?)
5. Feedback loop: corrigir bugs, ver scores subirem
```

**Resultado esperado:** Score médio ~ 92. Confiabilidade aumentando.

---

### Inspiração: A Visão

Imagina o KODA em 6 meses com traces implementadas:

**Cliente chega:** "Vocês me recomendaram X, mas esperava Y."

**Equipe responde:** 
> "Deixa eu verificar a trace..."
> *30 segundos depois*
> "Achei! O problema foi [explicação precisa]. Deixa a gente corrigir isso."

**Resultado:** 
- ✅ Cliente entende exatamente o que aconteceu
- ✅ Equipe corrige o bug em 10 minutos (porque sabe exatamente onde está)
- ✅ Confiança do cliente: "Eles realmente entendem o sistema deles"
- ✅ Confiança interna: "Sabemos por que erramos, e como não errar de novo"

**Esse é o poder das traces.**

---

### Visão de Longo Prazo: Agents Transparentes

Este documento é sobre **Trace Reading**.

Mas é também sobre algo maior: **Transparência em Agentes**.

No futuro próximo, quando agentes long-running forem comuns, a pergunta não será "Funciona?" mas **"Posso entender por que?"**

Traces são a resposta.

Com traces, você consegue:

✅ **Explicar decisões** — "Por que recomendou isto em vez daquilo?"  
✅ **Debugar rapidamente** — "Onde falhou?"  
✅ **Melhorar continuamente** — "O que aprendemos?"  
✅ **Confiar no agente** — "Consigo verificar"  

E mais importante: **você consegue dormir sabendo que se algo der errado, você vai conseguir debugar em 30 segundos, não 2 horas.**

---

### Resumo: O Que Você Aprendeu

```
📌 ESTRUTURA
└─ 7 componentes de uma trace bem-formada (Input, Context, Decision, Reasoning, Output, Evaluation, Metadata)

📌 LEITURA MANUAL
└─ 5 perguntas, 7 red flags, passo-a-passo de investigação

📌 PADRÕES
├─ Generator/Evaluator: Como detectar mismatch, Generator cego, Evaluator falho
├─ Sprint Contracts: Como rastrear quando informação se perdeu, diferenciar violação de mudança legítima
└─ Context: Como verificar completude e atualização

📌 AUTOMAÇÃO
├─ Python script: validações estruturais, timestamps, Gen/Eval, contrato, context
├─ JavaScript script: mesmo algoritmo, fácil integração
└─ Output: score 0-100 + issues categorizadas + recomendações

📌 PRÁTICA
└─ 4 casos completos que você pode estudar, testar, usar como referência

📌 RESULTADO
└─ Do debug de 2 horas → 30 segundos
└─ Do "black box" → "glass box"
└─ Da desconfiança → confiança
```

---

### Call to Action: Comece Agora

**Não espere 6 meses para implementar isto.**

Comece **hoje:**

1. **Próxima conversa do cliente:** Registre uma trace manual (use o JSON schema do doc)
2. **Rode o script:** `python trace_analyzer.py trace.json`
3. **Veja o score:** Qual é? 70? 85? 95?
4. **Debugue os problemas:** Use o método das 5 perguntas
5. **Documente a lição:** "Próxima vez, evitamos isto porque..."

**Depois, integre na arquitetura.**

Semana que vem você terá:
- ✅ Uma trace de um cliente real
- ✅ Um score real
- ✅ Problemas reais encontrados
- ✅ Lições reais aprendidas

**Isto é como você constrói um agente que você realmente confia.**

---

### Mensagem Final

Essa conversa que você perdeu no Prólogo não precisa ser perdida novamente.

Com traces, você consegue:
- Resgatar clientes
- Confiar no KODA
- Melhorar continuamente
- Dormir tranquilo

**O poder está nas suas mãos. A visibilidade está a 30 segundos de distância.**

Bem-vindo ao mundo dos **Agents Transparentes**. 🎯

---

## 📚 Apêndices

### Apêndice A: JSON Schema Formal Completo

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KODA Trace Schema v1.0",
  "type": "object",
  "required": ["trace_id", "session_id", "timestamp", "input", "context", "decision"],
  "properties": {
    "trace_id": {
      "type": "string",
      "description": "ID único desta trace",
      "pattern": "^trace-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}"
    },
    "session_id": {
      "type": "string",
      "description": "ID da sessão do cliente"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Quando esta trace foi criada (ISO8601)"
    },
    "agent_name": {
      "type": "string",
      "default": "KODA"
    },
    "agent_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "phase": {
      "type": "object",
      "properties": {
        "sprint_number": { "type": "integer" },
        "sprint_name": { "type": "string" },
        "sprint_contract": {
          "type": "object",
          "properties": {
            "contract_id": { "type": "string" },
            "max_budget": { "type": "number" },
            "constraints": { "type": "array" },
            "duration_minutes": { "type": "integer" }
          }
        }
      }
    },
    "input": {
      "type": "object",
      "required": ["type", "content", "timestamp"],
      "properties": {
        "type": { "type": "string", "enum": ["user_message", "system_event"] },
        "content": { "type": "string" },
        "timestamp": { "type": "string", "format": "date-time" },
        "intent_detected": { "type": "string" },
        "entities_extracted": { "type": "object" }
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "conversation_history": { "type": "array" },
        "current_user_profile": { "type": "object" },
        "available_products": { "type": "array" },
        "contract_at_input_time": { "type": "object" },
        "contract_at_generation_time": { "type": "object" }
      }
    },
    "decision": {
      "type": "object",
      "required": ["generation_id", "decision_status"],
      "properties": {
        "agent_role": { "type": "string", "enum": ["generator", "evaluator"] },
        "generator_id": { "type": "string" },
        "generation_id": { "type": "string" },
        "decision_type": { "type": "string" },
        "decision_status": { "type": "string", "enum": ["FINAL", "DRAFT", "PENDING"] },
        "timestamp": { "type": "string", "format": "date-time" },
        "recommendation": { "type": "object" }
      }
    },
    "reasoning": {
      "type": "object",
      "properties": {
        "thought_process": { "type": "array" },
        "confidence_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "alternative_considered": { "type": "array" }
      }
    },
    "output": {
      "type": "object",
      "properties": {
        "type": { "type": "string" },
        "content": { "type": "string" },
        "formatted_for_user": { "type": "string" },
        "timestamp": { "type": "string", "format": "date-time" }
      }
    },
    "evaluation": {
      "type": "object",
      "properties": {
        "evaluator_id": { "type": "string" },
        "evaluation_id": { "type": "string" },
        "timestamp_received": { "type": "string", "format": "date-time" },
        "recommendation_received": { "type": "object" },
        "evaluation_result": { "type": "string", "enum": ["APPROVED", "REJECTED"] },
        "checks_performed": { "type": "array" },
        "timestamp_approval": { "type": "string", "format": "date-time" }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "trace_version": { "type": "string" },
        "environment": { "type": "string", "enum": ["production", "staging", "development"] },
        "latency_ms": { "type": "object" },
        "error_flags": { "type": "array" },
        "warnings": { "type": "array" }
      }
    }
  }
}
```

### Apêndice B: Checklist de Trace Bem-Formada

Use este checklist para validar suas traces manualmente:

```
ESTRUTURA
☐ trace_id presente e único
☐ session_id presente
☐ timestamps em ISO8601
☐ agent_name e agent_version presentes

INPUT
☐ content não está vazio
☐ intent_detected foi feito (NLU rodou)
☐ entities_extracted não está vazio
☐ timestamp do input faz sentido

CONTEXT
☐ current_user_profile não está vazio
☐ conversation_history existe
☐ contract snapshots (input_time + generation_time) existem
☐ Nenhum campo crítico é null

DECISION
☐ generation_id presente e único
☐ decision_status é "FINAL", "DRAFT", ou "PENDING"
☐ recommendation tem produto/preço/detalhes
☐ timestamp é DEPOIS do input

REASONING
☐ thought_process é um array com passos
☐ confidence_score entre 0 e 1
☐ alternative_considered está preenchido

EVALUATION (se aplicável)
☐ evaluator_id presente
☐ recommendation_received.generation_id = decision.generation_id ✅
☐ checks_performed é um array não-vazio
☐ evaluation_result é APPROVED ou REJECTED
☐ timestamps fazem sentido (received < approval)

VALIDAÇÕES CRUZADAS
☐ input.timestamp < decision.timestamp (causa antes de efeito)
☐ decision.timestamp < evaluation.timestamp_received
☐ Nenhum campo crítico está vazio
☐ Nenhum timestamp está no futuro
```

### Apêndice C: Troubleshooting Comum

**Pergunta: Minha trace tem score muito baixo (< 50). O que fazer?**

Resposta:
1. Leia a seção "Issues" do relatório do script
2. Procure pelos "ERROR" severity
3. Se for gen_eval_mismatch: verificar código que passa recomendação
4. Se for contract_violation: investigar se Generator viu o contrato
5. Se for missing_field: implementar logging

---

**Pergunta: Como rastrear QUANDO uma informação se perdeu?**

Resposta:
1. Use `contract_at_input_time.timestamp` vs `contract_at_generation_time.timestamp`
2. Se forem iguais, contrato não mudou
3. Se forem diferentes, contrato foi atualizado entre input e geração
4. Compare timestamps para saber QUANDO a mudança aconteceu

---

**Pergunta: Qual é a diferença entre "violação de contrato" e "mudança legítima"?**

Resposta:
- Violação: Contrato não mudou, mas agente ignorou (culpa do agente)
- Mudança legítima: Contrato foi atualizado por cliente DEPOIS do input (não é culpa)
- Use timeline de timestamps para diferenciar

---

**Pergunta: Preciso de todas essas validações de uma vez?**

Resposta:
Não. Implemente em fases:
1. Phase 1: Apenas campos obrigatórios + timestamps
2. Phase 2: Adicione Gen/Eval validation
3. Phase 3: Adicione Sprint Contract validation
4. Phase 4: Context completeness
5. Phase 5: Automation scripts

Cada fase aumenta confiabilidade gradualmente.

---

**Pergunta: Posso usar traces para treinar novos padrões?**

Resposta:
Sim! Com 100+ traces, você consegue ver:
- Quais inputs geram erros com mais frequência
- Qual tipo de reasoning falha
- Quando Evaluator rejeita corretamente vs incorretamente
- Padrões de violação de contrato

Use isso para melhorar prompts do Generator, lógica do Evaluator, etc.

---

## 🌐 Além do Single-Framework: Centralized Cross-Framework Tracing

Até aqui, este módulo tratou de trace reading dentro de um único runtime (KODA no OpenCode/Sisyphus). Em ambientes enterprise, porém, é comum ter múltiplos frameworks de agente operando simultaneamente — CrewAI para um time, LangChain para outro, agentes customizados para um terceiro — cada um com seu próprio formato de trace. O *Centralized Cross-Framework Tracing* de Bhaumik resolve a fragmentação resultante: sem uma camada unificada, debugging requer context-switching entre ferramentas desconectadas e não há visão única da atividade dos agentes.

### A arquitetura de unificação

```
   CrewAI traces        LangChain traces       Custom agent traces
        │                      │                       │
        ▼                      ▼                       ▼
┌──────────────┐      ┌──────────────┐       ┌──────────────┐
│ Adapter      │      │ Adapter      │       │ Adapter      │
│ CrewAI →     │      │ LangChain →  │       │ Custom →     │
│ Unified      │      │ Unified      │       │ Unified      │
└──────┬───────┘      └──────┬───────┘       └──────┬───────┘
       │                     │                      │
       └─────────────────────┼──────────────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │  Centralized Trace Layer     │
              │  (unified schema, SQLite)    │
              └─────────────┬───────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                  ▼
   ┌────────────┐   ┌────────────┐   ┌────────────────┐
   │ Dashboards │   │ LLM Judges │   │ Text-to-SQL    │
   │ (única     │   │ (consomem  │   │ ("queries com  │
   │  visão)    │   │  formato   │   │  >5 tool calls │
   │            │   │  unificado)│   │  esta semana") │
   └────────────┘   └────────────┘   └────────────────┘
```

### O que a unificação habilita

- **Single debugging surface:** Trace qualquer query de qualquer agente em qualquer framework a partir de uma ferramenta única. O trace schema unificado (trace_id, session_id, tool_calls[], spans[]) é o contrato comum.
- **Framework-independent evaluation:** LLM judges e dashboards consomem o mesmo formato de trace independentemente de qual framework produziu os dados. Isso permite comparação cross-framework: "CrewAI é mais eficiente que LangChain para queries de checkout?"
- **Compliance audit:** "Você não pode nem fazer onboarding de AI em produção sem tracing." A camada centralizada satisfaz requisitos de auditoria — toda query é rastreável end-to-end, independentemente do framework.
- **Per-framework adapter pattern:** Cada framework precisa de um adapter que traduz seu formato nativo de trace para o schema unificado. O adapter é thin — só faz tradução de formato, sem lógica de negócio.

### Aplicação no ecossistema Pavan

O runtime do Sisyphus já implementa tracing centralizado via `task-wrapper.sh → trace-state.json → collector.ts → telemetry.db` (padrão [[docs/canonical/trace-instrumentation|Trace Instrumentation]]). A diferença para o modelo enterprise é que o Sisyphus opera com um único framework (OpenCode). A arquitetura de adapter seria necessária se o ecossistema incorporasse CrewAI, LangChain ou agentes customizados no futuro. O schema de trace existente (`trace_id`, `session_id`, `span_id`, `tool_name`, `params`, `duration_ms`, `tokens`) já é genérico o suficiente para servir como schema unificado — bastaria escrever os adapters de importação.

### O que NÃO está implementado

- Text-to-SQL interface para queries ad-hoc sobre traces (ex: "mostre todas as queries que usaram mais de 5 tool_calls nos últimos 7 dias")
- Coleta de traces via OpenTelemetry (o runtime atual usa arquivos em tmpfs, não um protocolo padrão de observabilidade)
- Trace sampling em escala enterprise (o volume atual não exige sampling; em escala de milhões de queries/dia, seria necessário)

---

## 🎓 Para Aprender Mais

Este documento é o **Módulo 4 de Nível 2** do Curso Completo de Padrões KODA.

Para contexto, leia:
- **Nível 1:** Fundamentals (como agents funcionam)
- **Nível 2, Doc 1:** Generator/Evaluator (padrão de separação)
- **Nível 2, Doc 2:** Sprint Contracts (padrão de expectativas)
- **Nível 2, Doc 3:** Token Budgeting (padrão de recursos)
- **Nível 2, Doc 4:** Trace Reading (este documento) ← Você está aqui

Próximas etapas:
- **Nível 2, Doc 5:** Rubric Design (avaliação automática)
- **Nível 3:** Advanced Patterns (multi-agent systems)
- **Nível 4:** Expert Implementation (production-grade systems)

---

**Bem-vindo ao mundo dos Agents Transparentes. 🎯**

Agora você não é mais um espectador de um black box. Você é um **engenheiro de vidro claro**, que consegue ver, entender, debugar, e melhorar o KODA a cada decisão.

**A visibilidade é poder. As traces são a luz.**

Boa sorte. 🚀

---
