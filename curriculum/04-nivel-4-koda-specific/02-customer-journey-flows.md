---
title: "Customer Journey Flows: A Máquina de Estados que Guia Cada Cliente"
type: curriculum-lesson
nivel: 4
aliases: ["jornada cliente", "customer journey", "fluxos KODA", "máquina estados"]
tags: [curriculo-conteudo, nivel-4, koda, maquina-de-estados, jornada-do-cliente, aarrr-adaptado, guard-conditions, sub-estados, metricas-por-etapa, tratamento-de-excecoes, handoff-humano, testes-property-based, novos-fluxos]
relates-to: ["[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]"]
last_updated: 2026-06-10
---
# 🗺️ Customer Journey Flows: A Máquina de Estados que Guia Cada Cliente
## Como KODA Gerencia Awareness, Consideration, Decision e Retention com Precisao Cirurgica

**Tempo Estimado:** 120-150 minutos
**Nivel:** 4 - KODA-Especifico
**Pre-requisitos:** Ter completado Nivel 1, Nivel 2, Nivel 3, `nivel-1-koda.md`, `nivel-2-koda.md`, `nivel-3-koda.md` e `01-koda-architecture.md`
**Status:** 🟢 CRITICO - Fundacao para toda feature do KODA
**Data de Criacao:** Maio 2026

---

## 📖 Prologo: A Jornada de Marina — 4 Etapas, 1 Agente, Zero Erros

Quarta-feira, 09h15.

Marina abriu o WhatsApp com uma necessidade simples: precisava de um suplemento para melhorar o sono. Ela nao sabia qual. Nao sabia se existia. Nao sabia quanto custava.

Ela digitou a primeira mensagem sem pensar muito:

```
Marina: "Oi! Vcs tem algo pra ajudar a dormir?"
```

O que aconteceu nos proximos 47 minutos e o que separa um chatbot simples de um **agente de negocios real**.

---

### Etapa 1 — Awareness (Minuto 0 ao 5)

KODA recebeu a mensagem. Mas nao respondeu imediatamente com uma lista de produtos. Primeiro, ele precisava **entender**:

```
[KODA — STATE: AWARENESS]
├── Trigger: primeira mensagem do cliente
├── Goal: classificar intencao, coletar contexto minimo
├── Guard: cliente nao esta em nenhum fluxo ativo
└── Output: intencao classificada + proximo estado
```

O agente consultou o state file de Marina — vazio. Cliente novo. Nenhum historico. Nenhuma preferencia salva.

KODA respondeu:

```
KODA: "Oi Marina! Temos sim 🌙
Me conta um pouco mais: voce tem dificuldade pra pegar no sono,
ou acorda varias vezes durante a noite?"
```

Essa pergunta nao foi aleatoria. Foi o **guard condition** que determina se a jornada segue para `CONSIDERATION` ou volta para coletar mais contexto.

Marina respondeu:

```
Marina: "Demoro pra pegar no sono. Fico na cama pensando em trabalho."
```

Pronto. Intencao classificada: `SLEEP_ONSET`. Contexto coletado: `first_time_buyer`, `canal=whatsapp`, `timestamp=09:15`.

KODA fez a transicao:

```
AWARENESS ──[intencao_classificada + contexto_minimo_ok]──► CONSIDERATION
```

---

### Etapa 2 — Consideration (Minuto 5 ao 22)

Agora KODA entrou no estado onde a mágica (ou o desastre) acontece. O objetivo nao era vender — era **ajudar Marina a decidir**.

```
[KODA — STATE: CONSIDERATION]
├── Trigger: intencao classificada com contexto suficiente
├── Goal: explorar opcoes, aplicar restricoes, educar cliente
├── Sub-states: DISCOVERY → FILTERING → COMPARISON → VALIDATION
└── Guard: cliente ativamente explorando opcoes (nao decidiu ainda)
```

O que aconteceu em sequencia:

**Sub-state: DISCOVERY**
```
KODA: "Entendi! Para quem demora a pegar no sono, temos 3 categorias:
1️⃣ Melatonina — ajuda a regular o ciclo
2️⃣ Magnesio — relaxa o sistema nervoso
3️⃣ Blend herbal — camomila, valeriana, passiflora

Quer que eu explique cada uma?"
```

**Sub-state: FILTERING**
```
Marina: "Sou vegetariana. Algum problema?"

KODA: "Boa pergunta! A Melatonina de origem animal nao serve.
Mas tenho duas opcoes 100% vegetais:
🌿 Magnesio Quelato — R$ 59,90
🌿 Blend Herbal Noturno — R$ 72,00"
```

Aqui aconteceu algo critico: KODA aplicou uma **restricao de negocio** (vegetariano) como guard condition no sub-estado FILTERING. Se a restricao nao fosse respeitada, o Evaluator teria rejeitado a recomendacao.

**Sub-state: COMPARISON**
```
Marina: "Qual a diferenca?"

KODA: "Excelente pergunta! Vou comparar pra voce:

📊 Magnesio Quelato:
✅ Acao em 40-60 min
✅ Ajuda tambem com ansiedade
✅ 120 capsulas (2 meses)
💰 R$ 59,90

📊 Blend Herbal Noturno:
✅ Acao em 20-30 min
✅ 100% natural, sem hormonios
✅ 90 capsulas (1 mes)
⚠️ Pode dar sonolencia de manha nos primeiros dias
💰 R$ 72,00"
```

**Sub-state: VALIDATION**
```
Marina: "Acho que vou de Magnesio. Nao quero sonolencia de manha."

KODA: "Otima escolha! So pra confirmar:
✅ Vegano — sim, Magnesio Quelato e 100% vegetal
✅ Sem gluten — sim, certificado
✅ Preco — R$ 59,90
✅ Entrega — 3 dias uteis para SP

Confirma que e isso mesmo?"
```

```
Marina: "Perfeito! Pode fechar."
```

Transicao acontecendo:

```
CONSIDERATION ──[cliente_decidiu + produto_validado]──► DECISION
```

---

### Etapa 3 — Decision (Minuto 22 ao 28)

Agora e o momento da verdade. KODA esta no estado onde **dinheiro troca de maos**. Nao pode errar.

```
[KODA — STATE: DECISION]
├── Trigger: cliente confirmou produto com validacao completa
├── Goal: processar pedido com zero erros
├── Sub-states: CHECKOUT → PAYMENT → CONFIRMATION
└── Guard: produto validado em CONSIDERATION (SKU, preco, restricoes)
```

**Sub-state: CHECKOUT**
```
KODA: "Perfeito, Marina! Vamos finalizar:
📦 Produto: Magnesio Quelato 120 caps
💰 Valor: R$ 59,90
🚚 Frete: Gratis (SP capital)
📍 Endereco de entrega?"

Marina: "Rua Augusta, 1500, ap 42, Consolacao, SP"
```

**Sub-state: PAYMENT**
```
KODA: "Recebido! Forma de pagamento?
💳 Cartao de credito (ate 3x sem juros)
📱 Pix (5% de desconto)
🏦 Boleto (2 dias uteis pra compensar)"

Marina: "Pix! Tem desconto ne?"

KODA: "Tem sim! Com Pix fica R$ 56,90 💚
Chave Pix enviada no proximo email.
Assim que confirmar, seu pedido ja entra em separacao."
```

**Sub-state: CONFIRMATION**
```
[5 minutos depois...]

Marina: "Pix feito!"

KODA: "Pagamento confirmado! 🎉
📦 Pedido #KDA-2847
🚚 Entrega prevista: Sexta-feira, 29/05
📧 Enviamos tudo por email tambem"

KODA: "Ah, e ja anotei que voce prefere produtos veganos.
Na proxima vez que falar comigo, ja vou saber direto. 😊"
```

```
DECISION ──[pagamento_confirmado + pedido_criado]──► RETENTION
```

---

### Etapa 4 — Retention (Minuto 28 ao 47... e alem)

Este e o estado que a maioria dos chatbots **nao tem**. E e exatamente o que transforma um comprador unico em um **cliente fiel**.

```
[KODA — STATE: RETENTION]
├── Trigger: pedido concluido com sucesso
├── Goal: fidelizar, antecipar proxima compra, coletar feedback
├── Sub-states: ONBOARDING → FOLLOW_UP → RE-ENGAGEMENT → SUPPORT
└── Guard: cliente tem pedido ativo ou historico de compras
```

**Sub-state: ONBOARDING (imediatamente apos compra)**
```
KODA: "Marina, 3 dias uteis e seu Magnesio chega!
Enquanto isso: quer que eu te avise quando estiver
perto de acabar? Assim voce nunca fica sem."

Marina: "Nossa, otimo! Pode sim."

KODA: "Combinado! Daqui a ~55 dias (quando tiver ~1 semana
de produto) eu te mando uma mensagem. 😊"
```

**Sub-state: FOLLOW_UP (3 dias depois — entrega)**
```
KODA: "Marina! Seu Magnesio Quelato foi entregue hoje as 14h20 🌙
Como foram as primeiras noites? Alguma duvida sobre como tomar?"

Marina: "Recebi sim! To tomando 1 capsula antes de dormir.
To dormindo bem melhor!!"

KODA: "Que noticia maravilhosa! 🎉 Fico muito feliz!
Qualquer duvida e so chamar."
```

**Sub-state: RE-ENGAGEMENT (55 dias depois — previsao de fim de estoque)**
```
KODA: "Marina! Saudades 🌙
Pelas minhas contas, seu Magnesio Quelato deve estar acabando
essa semana. Quer que eu separe outro pra voce?
(Ai ja aplico o desconto de cliente fiel: 10% off)"
```

**Sub-state: SUPPORT (a qualquer momento)**
```
Marina: "KODA, sera que posso tomar 2 capsulas em vez de 1?"

KODA: "Hmm, otima pergunta! Me deixa consultar a bula...
📋 Dose recomendada: 1 capsula/dia (400mg)
⚠️ Doses acima de 800mg podem causar desconforto estomacal

Recomendo manter 1 capsula. Se quiser potencializar o efeito,
posso sugerir um cha de camomila antes de dormir. 🍵"
```

---

### O Que Aconteceu em 47 Minutos?

Marina entrou no WhatsApp com uma pergunta vaga. Saiu com:
- Um produto adequado as restricoes dela (vegetariano)
- Um pedido processado sem erros
- Uma experiencia personalizada
- Um acompanhamento programado para daqui a 55 dias
- Confianca para voltar a qualquer momento

Isso nao e um chatbot. E um **sistema de negocios com maquina de estados**.

E o que torna isso possivel e exatamente o que voce vai aprender neste modulo.

---

## 🎯 O Que E uma Jornada de Cliente em KODA?

### Definicao Simples

A **Customer Journey** do KODA e o mapeamento completo de todos os estados pelos quais um cliente passa — desde o primeiro "oi" ate a recompra meses depois — com regras explicitas de:
- Como avancar entre estados
- Quando voltar para um estado anterior
- O que fazer quando algo sai do fluxo esperado

### Por Que Isso Importa?

Sem uma maquina de estados explicita, um agente de vendas vira uma maquina de "responder qualquer coisa". Com ela, vira uma **operacao comercial automatizada**.

A diferenca e a mesma entre:

```
SEM STATE MACHINE: KODA processa 500 conversas/dia.
                    40% terminam em venda.
                    15% tem erro no pedido.
                    Ninguem sabe por que 60% nao compraram.
```

```
COM STATE MACHINE:  KODA processa 500 conversas/dia.
                    65% terminam em venda.
                    2% tem erro no pedido.
                    Voce sabe EXATAMENTE onde cada cliente parou.
```

### Os 4 Macro-Estados (AARRR Framework Adaptado)

KODA implementa uma versao adaptada do framework **AARRR** (tambem chamado Pirate Metrics), ajustado para o contexto de conversa por WhatsApp:

| Macro-Estado | Nome Original | Nome KODA | Objetivo |
|---|---|---|---|
| **A** | Awareness | Descoberta | Cliente sabe que KODA existe e inicia conversa |
| **C** | Consideration | Exploração | Cliente explora produtos, tira duvidas, compara |
| **D** | Decision | Decisao | Cliente escolhe, paga e finaliza pedido |
| **R** | Retention | Relacionamento | Cliente volta, recebe follow-up, vira fiel |
| **R** | Revenue | Receita | Upsell, cross-sell, aumento de ticket medio |

> **Nota:** No KODA, os dois "R"s finais (Retention e Revenue) sao gerenciados como sub-estados do macro-estado RETENTION, porque no contexto de conversa, fidelizacao e receita estao entrelacados.

---

### Por Que Maquina de Estados e Nao Regras If/Else?

Uma pergunta comum: "Nao da pra fazer isso com if/else?" Tecnicamente, sim. Mas a diferenca e a mesma entre uma lista de compras e um sistema de GPS:

**Abordagem If/Else (Lista de Compras):**
```python
if "oi" in message:
    respond("Ola! Como posso ajudar?")
elif "preco" in message:
    respond("Temos opcoes a partir de R$ 29,90")
elif "comprar" in message:
    iniciar_checkout()
else:
    respond("Nao entendi. Pode reformular?")
```

Problemas:
- Nao mantem estado entre mensagens — cada interacao e isolada
- Nao ha memoria do que aconteceu antes
- Nao ha como "voltar" atras se o cliente mudar de ideia
- Impossivel diagnosticar onde um cliente parou (estado e invisivel)

**Abordagem State Machine (GPS):**
```json
{
  "current_state": "CONSIDERATION",
  "sub_state": "COMPARISON",
  "history": ["AWARENESS", "CONSIDERATION:DISCOVERY", "CONSIDERATION:FILTERING"],
  "context": {
    "intent": "SLEEP_ONSET",
    "filters_applied": ["vegetariano"],
    "candidates": ["SKU-001", "SKU-003"],
    "client_preferences": {"budget_max": 80, "formato": "capsulas"}
  }
}
```

Vantagens:
- Estado e explicito e persistente — sobrevive a reinicios do servidor
- Cada transicao tem condicoes verificaveis — sem "magica"
- Historico completo — da pra reconstruir exatamente o que aconteceu
- Metricas por estado — voce sabe exatamente onde esta o gargalo
- Recuperacao — se algo falhar, volta ao ultimo estado valido

### Analogia: O Garcom Perfeito

Pense em KODA como um garcom de restaurante cinco estrelas que atende o cliente do inicio ao fim:

**Fase 1 — Awareness (Recepcao):**
O garcom ve o cliente entrar. Nao corre com o cardapio. Primeiro pergunta: "Quantas pessoas? Tem reserva? Alguma restricao alimentar?" Coleta contexto.

**Fase 2 — Consideration (Cardapio):**
O garcom explica os pratos. Pergunta preferencias. "Gosta de peixe? Prefere carne? Quer vinho?" Ajuda o cliente a explorar sem pressionar.

**Fase 3 — Decision (Pedido):**
O garcom anota o pedido. Confirma cada item. "File ao ponto, sem gluten, com pure em vez de fritas. Correto?" Valida antes de enviar para cozinha.

**Fase 4 — Retention (Pos-refeicao):**
O garcom volta depois da sobremesa. "Como estava? Alguma sobremesa ou cafe?" E na saida: "Volte sempre! Vou anotar que o senhor prefere mesa na varanda."

Um garcom ruim faz tudo isso ao mesmo tempo, sem ordem, esquecendo restricoes. Um garcom excelente segue uma **maquina de estados invisivel**. KODA torna isso explicito e programatico.

---

## 🏗️ A Maquina de Estados do KODA: Visao Completa

### Diagrama ASCII da State Machine

```
                              ┌─────────────────────────────────────────────────────────────┐
                              │                     KODA CUSTOMER JOURNEY                     │
                              │                  State Machine — Visao Completa               │
                              └─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  ENTRY_POINT │  (Cliente envia primeira mensagem no WhatsApp)
    └──────┬───────┘
           │
           ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │   ╔══════════════════════════════════════════════════════════╗   │
    │   ║               ESTADO 1: AWARENESS                        ║   │
    │   ╠══════════════════════════════════════════════════════════╣   │
    │   ║  Goal: Classificar intencao, coletar contexto inicial    ║   │
    │   ║                                                          ║   │
    │   ║  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐  ║   │
    │   ║  │ INTENT      │──►│ CONTEXT      │──►│ ROUTING      │  ║   │
    │   ║  │ CLASSIFY    │   │ COLLECTION   │   │ DECISION     │  ║   │
    │   ║  └─────────────┘   └──────────────┘   └──────┬───────┘  ║   │
    │   ║                                              │          ║   │
    │   ╚══════════════════════════════════════════════╪══════════╝   │
    │                                                  │              │
    │                    ┌─────────────────────────────┼──────┐       │
    │                    │  Guard Conditions:          │      │       │
    │                    │  - intencao classificada?   │      │       │
    │                    │  - contexto suficiente?     │      │       │
    │                    │  - cliente novo/existente?  │      │       │
    │                    └─────────────┬───────────────┘      │       │
    │                                  │                      │       │
    │              ┌───────────────────┼───────────────────┐  │       │
    │              │                   │                   │  │       │
    │           [FALHA]          [SUCESSO]           [DESVIO] │       │
    │              │                   │                   │  │       │
    │              ▼                   ▼                   ▼  │       │
    │   ┌──────────────────┐ ┌───────────────┐ ┌──────────────────┐ │
    │   │ RECONTEXTUALIZAR │ │               │ │ HANDOFF_HUMANO   │ │
    │   │ (loop awareness) │ │               │ │ (cliente pede    │ │
    │   └──────────────────┘ │               │ │  atendente real) │ │
    │                        │               │ └──────────────────┘ │
    └────────────────────────┼───────────────┼──────────────────────┘
                             │               │
                             │               ▼
                             │   ┌──────────────────────────────────────────────────────┐
                             │   │                                                      │
                             │   │   ╔══════════════════════════════════════════════╗   │
                             │   │   ║          ESTADO 2: CONSIDERATION            ║   │
                             │   │   ╠══════════════════════════════════════════════╣   │
                             │   │   ║  Goal: Explorar, filtrar, comparar, validar ║   │
                             │   │   ║                                              ║   │
                             │   │   ║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ║   │
                             │   │   ║  │DISCOVERY │─►│FILTERING │─►│COMPARISON│  ║   │
                             │   │   ║  └──────────┘  └──────────┘  └────┬─────┘  ║   │
                             │   │   ║                                    │        ║   │
                             │   │   ║                                    ▼        ║   │
                             │   │   ║                              ┌──────────┐  ║   │
                             │   │   ║                              │VALIDATION│  ║   │
                             │   │   ║                              └────┬─────┘  ║   │
                             │   │   ║                                   │        ║   │
                             │   │   ╚═══════════════════════════════════╪════════╝   │
                             │   │                                       │            │
                             │   │              ┌────────────────────────┼─────┐      │
                             │   │              │ Guard Conditions:      │     │      │
                             │   │              │ - produto validado?    │     │      │
                             │   │              │ - restricoes ok?       │     │      │
                             │   │              │ - cliente decidiu?     │     │      │
                             │   │              └────────────┬───────────┘     │      │
                             │   │                           │                 │      │
                             │   │         ┌─────────────────┼──────────┐      │      │
                             │   │         │                 │          │      │      │
                             │   │     [FALHA]         [SUCESSO]   [ABANDONO]  │      │
                             │   │         │                 │          │      │      │
                             │   │         ▼                 │          ▼      │      │
                             │   │  ┌──────────────┐         │  ┌──────────────┐│      │
                             │   │  │ REPLANEJAR   │         │  │ IDLE_TIMEOUT ││      │
                             │   │  │ (volta para  │         │  │ (salva estado ││      │
                             │   │  │  DISCOVERY)  │         │  │  para retomar)││      │
                             │   │  └──────────────┘         │  └──────────────┘│      │
                             │   │                           │                  │      │
                             │   └───────────────────────────┼──────────────────┘      │
                             │                               │                         │
                             │                               ▼                         │
                             │   ┌──────────────────────────────────────────────────┐  │
                             │   │                                                  │  │
                             │   │   ╔══════════════════════════════════════════╗   │  │
                             │   │   ║             ESTADO 3: DECISION           ║   │  │
                             │   │   ╠══════════════════════════════════════════╣   │  │
                             │   │   ║  Goal: Processar pedido com zero erros   ║   │  │
                             │   │   ║                                          ║   │  │
                             │   │   ║  ┌──────────┐  ┌──────────┐  ┌────────┐ ║   │  │
                             │   │   ║  │ CHECKOUT │─►│ PAYMENT  │─►│CONFIRM │ ║   │  │
                             │   │   ║  └──────────┘  └──────────┘  └───┬────┘ ║   │  │
                             │   │   ║                                   │      ║   │  │
                             │   │   ╚═══════════════════════════════════╪══════╝   │  │
                             │   │                                       │          │  │
                             │   │              ┌────────────────────────┼───┐      │  │
                             │   │              │ Guard Conditions:      │   │      │  │
                             │   │              │ - pagamento ok?        │   │      │  │
                             │   │              │ - estoque confirmado?  │   │      │  │
                             │   │              │ - endereco valido?     │   │      │  │
                             │   │              └──────────┬─────────────┘   │      │  │
                             │   │                         │                 │      │  │
                             │   │        ┌────────────────┼──────────┐      │      │  │
                             │   │        │                │          │      │      │  │
                             │   │    [FALHA]        [SUCESSO]   [RECUSA]    │      │  │
                             │   │        │                │          │      │      │  │
                             │   │        ▼                │          ▼      │      │  │
                             │   │ ┌──────────────┐        │  ┌──────────────┐│      │  │
                             │   │ │ PAYMENT_RETRY│        │  │ CANCEL_ORDER ││      │  │
                             │   │ │ (3 tentativas)│       │  │ (volta para  ││      │  │
                             │   │ └──────────────┘        │  │ CONSIDERATION)│     │  │
                             │   │                         │  └──────────────┘│      │  │
                             │   └─────────────────────────┼──────────────────┘      │  │
                             │                             │                         │  │
                             │                             ▼                         │  │
                             │   ┌──────────────────────────────────────────────────┐  │
                             │   │                                                  │  │
                             │   │   ╔══════════════════════════════════════════╗   │  │
                             │   │   ║            ESTADO 4: RETENTION           ║   │  │
                             │   │   ╠══════════════════════════════════════════╣   │  │
                             │   │   ║  Goal: Fidelizar, re-engajar, suportar  ║   │  │
                             │   │   ║                                          ║   │  │
                             │   │   ║  ┌──────────┐  ┌──────────┐  ┌────────┐ ║   │  │
                             │   │   ║  │ONBOARDING│─►│FOLLOW_UP │─►│RE-ENGAGE│║   │  │
                             │   │   ║  └──────────┘  └──────────┘  └───┬────┘ ║   │  │
                             │   │   ║                                   │      ║   │  │
                             │   │   ║                                   ▼      ║   │  │
                             │   │   ║                              ┌────────┐  ║   │  │
                             │   │   ║                              │SUPPORT │  ║   │  │
                             │   │   ║                              └────────┘  ║   │  │
                             │   │   ╚══════════════════════════════════════════╝   │  │
                             │   │                                                  │  │
                             │   └──────────────────────────────────────────────────┘  │
                             │                                                         │
                             └─────────────────────────────────────────────────────────┘

                              ┌──────────────────────────────────────────┐
                              │  LEGENDA:                                │
                              │  ──► Transicao normal (sucesso)          │
                              │  - -► Transicao de fallback (retry)      │
                              │  ....► Transicao de excecao (desvio)     │
                              │  [GUARD] Condicao de guarda             │
                              └──────────────────────────────────────────┘
```

---

## 🔧 Implementacao Tecnica: Como a Maquina de Estados Funciona

Antes de mergulhar em cada estado, e importante entender o mecanismo que faz a state machine funcionar.

### Estrutura do State File

Cada cliente tem um arquivo JSON que representa o estado atual da jornada:

```json
{
  "client_id": "wa_5511999999999",
  "session_id": "sess_20260527_0915_8f3a",
  "conversation_started_at": "2026-05-27T09:15:00Z",
  "last_activity_at": "2026-05-27T09:42:00Z",
  "current_state": "CONSIDERATION",
  "current_sub_state": "COMPARISON",
  "state_history": [
    {
      "from": "ENTRY_POINT",
      "to": "AWARENESS",
      "sub_state": "INTENT_CLASSIFICATION",
      "timestamp": "2026-05-27T09:15:01Z",
      "trigger": "first_message",
      "guard_evaluation": "ALL_PASS"
    },
    {
      "from": "AWARENESS",
      "to": "CONSIDERATION",
      "sub_state": "DISCOVERY",
      "timestamp": "2026-05-27T09:18:00Z",
      "trigger": "intent_classified",
      "guard_evaluation": "ALL_PASS"
    }
  ],
  "context": {
    "intent": "SLEEP_ONSET",
    "intent_confidence": 0.94,
    "collected_preferences": {
      "dietary": ["vegetariano"],
      "budget_max": null,
      "formato_preferido": "capsulas"
    },
    "applied_filters": [
      {"filter": "dietary", "value": "vegetariano", "applied_at": "..."}
    ]
  },
  "checkpoint_data": {
    "last_valid_state": "CONSIDERATION:FILTERING",
    "last_valid_context_hash": "a3f8c2e1b4d5",
    "recovery_points": 3
  },
  "metrics": {
    "messages_exchanged": 14,
    "products_shown": 3,
    "time_in_current_state_seconds": 340,
    "total_session_time_seconds": 1620
  }
}
```

### O Loop de Processamento de Mensagem

Cada nova mensagem do cliente passa por este pipeline:

```
NOVA MENSAGEM DO CLIENTE
    │
    ▼
┌───────────────────────────────────────┐
│ 1. CARREGAR STATE FILE                │
│    Se nao existe: criar novo (ENTRY)  │
│    Se existe: carregar do disco/redis │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│ 2. AVALIAR GUARD CONDITIONS           │
│    Dado o estado ATUAL, quais sao as  │
│    transicoes possiveis?             │
│    Para cada uma: checar condicoes    │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│ 3. SELECIONAR TRANSICAO               │
│    Prioridade:                        │
│    1. Handoff humano (se solicitado)  │
│    2. Timeout (se inativo > 30 min)   │
│    3. Transicao natural (guard ok)    │
│    4. Loop (permanece no estado)      │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│ 4. GERAR RESPOSTA                     │
│    System prompt varia por estado!    │
│    Cada estado tem seu proprio tom,   │
│    objetivo e restricoes de output    │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│ 5. VALIDAR RESPOSTA                   │
│    Generator/Evaluator (se estado     │
│    requer validacao de qualidade)     │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│ 6. PERSISTIR NOVO ESTADO              │
│    Atualizar state file               │
│    Registrar evento no audit_log      │
│    Atualizar metricas                 │
└───────────────┬───────────────────────┘
                │
                ▼
           ENVIAR RESPOSTA
```

### System Prompts por Estado

Cada estado tem um system prompt diferente, otimizado para seu objetivo:

**AWARENESS — System Prompt:**
```
Voce e KODA, assistente de vendas da loja FutanBear.
Estado atual: AWARENESS / INTENT_CLASSIFICATION.

SUA UNICA MISSÃO: Entender o que o cliente precisa.
- NAO recomende produtos ainda
- NAO tente vender
- FACA perguntas curtas e naturais para classificar a intencao
- SE a intencao estiver clara: colete contexto minimo necessario
- SE a intencao estiver confusa: peca para o cliente reformular
- MAXIMO 2 perguntas por mensagem (WhatsApp = conversa, nao interrogatorio)
```

**CONSIDERATION — System Prompt:**
```
Voce e KODA, assistente de vendas da loja FutanBear.
Estado atual: CONSIDERATION.

OBJETIVO: Ajudar o cliente a encontrar o produto ideal.
- MOSTRE opcoes por categoria, nao mais de 5 por mensagem
- APLIQUE todas as restricoes do cliente (alergias, dieta, orcamento)
- COMPARE produtos com honestidade: mencione pontos negativos tambem
- VALIDE a escolha final antes de passar para checkout
- NAO pressione para comprar — deixe o cliente no controle
```

**DECISION — System Prompt:**
```
Voce e KODA, assistente de vendas da loja FutanBear.
Estado atual: DECISION.

OBJETIVO: Processar o pedido com ZERO erros.
- CONFIRA cada dado antes de prosseguir
- VALIDE CEP, endereco, metodo de pagamento
- SE algo falhar: explique claramente e ofereca alternativa
- CONFIRME o pedido com numero, valor, prazo
- NUNCA cobre um valor diferente do que foi acordado em CONSIDERATION
```

**RETENTION — System Prompt:**
```
Voce e KODA, assistente de vendas da loja FutanBear.
Estado atual: RETENTION.

OBJETIVO: Construir relacionamento de longo prazo.
- SEJA proativo: antecipe necessidades, lembre de recompras
- OFERECA valor: dicas, descontos, conteudo relevante
- RESPEITE o espaco do cliente: nao faca spam
- SUPORTE: responda duvidas com precisao, escale quando necessario
- LEMBRE: um cliente fiel vale 5x mais que um cliente novo
```

---

## 🔍 Estado 1: AWARENESS — O Primeiro Contato

### Objetivo

Transformar "oi" em "sei exatamente o que voce precisa".

O estado AWARENESS nao tenta vender. Nao tenta recomendar. Seu unico objetivo e **coletar contexto suficiente** para que os proximos estados possam trabalhar com precisao.

### Sub-Estados Internos

#### 1. INTENT CLASSIFICATION

KODA classifica a primeira mensagem do cliente em uma das categorias de intencao:

| Categoria de Intencao | Exemplo de Mensagem | Gatilho |
|---|---|---|
| `PRODUCT_DISCOVERY` | "tem whey?" | Cliente quer explorar catalogo |
| `SPECIFIC_PRODUCT` | "quero Whey Isolado" | Cliente ja sabe o que quer |
| `ORDER_STATUS` | "cade meu pedido?" | Cliente quer rastrear pedido |
| `SUPPORT_GENERAL` | "posso tomar 2 capsulas?" | Cliente tem duvida de uso |
| `COMPLAINT` | "produto chegou errado" | Cliente insatisfeito |
| `CHITCHAT` | "bom dia" | Cliente testando ou casual |
| `UNKNOWN` | mensagem confusa/ambigua | Necessario esclarecer |

**Implementacao no KODA:**

```json
{
  "state": "AWARENESS",
  "sub_state": "INTENT_CLASSIFICATION",
  "input": {
    "message": "Oi! Vcs tem algo pra ajudar a dormir?",
    "timestamp": "2026-05-27T09:15:00Z",
    "client_id": "wa_5511999999999"
  },
  "intent_classifier": {
    "primary_intent": "PRODUCT_DISCOVERY",
    "confidence": 0.94,
    "secondary_intents": [
      {"intent": "SPECIFIC_PRODUCT", "confidence": 0.23}
    ],
    "entities_detected": {
      "problem": "sleep",
      "product_category": null,
      "budget": null
    }
  }
}
```

#### 2. CONTEXT COLLECTION

Depois de classificar a intencao, KODA coleta contexto adicional. Cada intencao tem seu proprio conjunto minimo de dados necessarios antes de poder avancar:

| Intencao | Contexto Minimo Necessario |
|---|---|
| `PRODUCT_DISCOVERY` | Problema/necessidade, preferencias basicas |
| `SPECIFIC_PRODUCT` | SKU ou nome exato, quantidade |
| `ORDER_STATUS` | Numero do pedido OU email/CPF |
| `SUPPORT_GENERAL` | Produto em uso, duvida especifica |
| `COMPLAINT` | Numero do pedido, descricao do problema |

**Guard Conditions para avancar:**

```
AWARENESS → CONSIDERATION:
  ✅ intencao classificada com confidence > 0.7
  ✅ contexto minimo da intencao coletado
  ✅ cliente nao pediu atendente humano
  ✅ nao e CHITCHAT ou UNKNOWN (precisa de mais iteracoes)

AWARENESS → AWARENESS (loop):
  ❌ intencao com confidence < 0.7 → pede esclarecimento
  ❌ contexto insuficiente → faz pergunta especifica
  ❌ intencao UNKNOWN → pede para reformular

AWARENESS → HANDOFF_HUMANO:
  🔄 cliente explicitamente pede "falar com pessoa"
  🔄 3 tentativas de classificar intencao falharam
```

### Roteamento por Perfil de Cliente

KODA consulta o state file do cliente antes de decidir a rota:

```json
{
  "client_profile": {
    "is_new": true,
    "previous_purchases": 0,
    "known_restrictions": [],
    "known_preferences": [],
    "last_interaction": null,
    "lifetime_value": 0
  },
  "routing_decision": "FULL_JOURNEY",
  "reason": "Cliente novo. Seguir fluxo completo: AWARENESS → CONSIDERATION → DECISION → RETENTION"
}
```

Se o cliente ja tem historico:

```json
{
  "client_profile": {
    "is_new": false,
    "previous_purchases": 3,
    "known_restrictions": ["vegetariano", "sem_gluten"],
    "known_preferences": ["sono", "vegano"],
    "last_interaction": "2026-04-15T14:30:00Z",
    "lifetime_value": 187.50
  },
  "routing_decision": "ACCELERATED_CONSIDERATION",
  "reason": "Cliente recorrente. Pular discovery generica, ir direto para recomendacoes personalizadas."
}
```

---

## 🔍 Estado 2: CONSIDERATION — Onde a Decisao Acontece

### Objetivo

Este e o estado mais complexo. KODA precisa equilibrar **exploracao** (mostrar opcoes) com **foco** (nao sobrecarregar o cliente). A estrutura de sub-estados garante que cada iteracao tenha um unico objetivo claro.

### Sub-Estado: DISCOVERY

**Objetivo:** Apresentar o catalogo de forma estruturada, educando o cliente.

**Regras:**
- Nunca listar mais de 5 produtos por mensagem (WhatsApp e conversa, nao e-commerce)
- Agrupar por categoria, nao por preco
- Cada produto deve vir com: nome, preco, 1-2 beneficios, 1 limitacao (transparencia)
- Sempre perguntar se cliente quer detalhe de algum especifico

**Exemplo de saida KODA:**

```
KODA: "Para melhorar o sono, temos 3 abordagens:

🌙 MELATONINA (acao hormonal):
• Melatonina Pura 3mg — R$ 39,90
  ✅ Regula o ciclo circadiano em 1-2 semanas
  ⚠️ Nao recomendado para gestantes

🪨 MAGNESIO (acao mineral):
• Magnesio Quelato 400mg — R$ 59,90
  ✅ Relaxa musculatura + sistema nervoso
  ⚠️ Pode causar leve sonolencia diurna nos primeiros dias

🌿 BLEND HERBAL (acao natural):
• Sonus Herbal Complex — R$ 72,00
  ✅ 100% natural, zero efeitos colaterais
  ⚠️ Efeito mais sutil, ideal para insonia leve

Quer que eu explique mais detalhes de alguma dessas categorias?"
```

### Sub-Estado: FILTERING

**Objetivo:** Aplicar restricoes do cliente e refinar opcoes.

**Regras:**
- Toda restricao deve ser armazenada no state file (nao apenas "lembrada" no contexto)
- Restricoes sao cumulativas: vegetariano + sem gluten + orcamento maximo
- Se uma restricao eliminar TODAS as opcoes, KODA deve informar (nao recomendar algo que nao serve)

**Exemplo de state file no meio do FILTERING:**

```json
{
  "state": "CONSIDERATION",
  "sub_state": "FILTERING",
  "context": {
    "intent": "SLEEP_ONSET",
    "budget_max": null,
    "applied_filters": [
      {
        "filter": "dietary_restriction",
        "value": "vegetariano",
        "source": "cliente disse 'sou vegetariana' em msg_004",
        "applied_at": "2026-05-27T09:20:00Z"
      }
    ],
    "candidate_products_before_filter": ["SKU-001", "SKU-002", "SKU-003"],
    "candidate_products_after_filter": ["SKU-001", "SKU-003"],
    "eliminated_reason": {
      "SKU-002": "contem gelatina de origem animal"
    }
  }
}
```

### Sub-Estado: COMPARISON

**Objetivo:** Ajudar o cliente a decidir entre 2-3 opcoes finais.

**Regras:**
- Maximo 3 produtos para comparacao (mais que isso = paralisia de decisao)
- Tabela de comparacao com no maximo 5 criterios
- Sempre destacar o "melhor custo-beneficio" e o "melhor qualidade"
- Nao enviesar a recomendacao para o mais caro

**Formato de saida:**

```
KODA: "Sobraram duas excelentes opcoes veganas:

📊 COMPARATIVO RAPIDO:

                    Magnesio Quelato    Sonus Herbal
Preco               R$ 59,90            R$ 72,00
Tempo para efeito   40-60 min           20-30 min
Duracao do frasco   60 dias             30 dias
Efeito extra        Anti-ansiedade      Relaxante natural
Melhor para         Insonia moderada    Insonia leve

🏆 Melhor custo-beneficio: Magnesio Quelato
🏆 Mais rapido e natural: Sonus Herbal

Qual faz mais sentido pra voce?"
```

### Sub-Estado: VALIDATION

**Objetivo:** Confirmar que a escolha do cliente respeita TODAS as restricoes e garantir que nao ha surpresas.

Este sub-estado e o **ultimo checkpoint antes de dinheiro trocar de maos**. E onde o Generator/Evaluator do KODA mais atua.

**Checklist de validacao:**

```json
{
  "validation_checklist": {
    "product_exists": {"status": "PASS", "detail": "SKU-001 encontrado no catalogo"},
    "price_current": {"status": "PASS", "detail": "R$ 59,90 confirmado via API de precos"},
    "stock_available": {"status": "PASS", "detail": "142 unidades em SP"},
    "dietary_restrictions": {"status": "PASS", "detail": "Vegetariano — Magnesio Quelato e vegano certificado"},
    "allergy_check": {"status": "NOT_APPLICABLE", "detail": "Cliente nao reportou alergias"},
    "budget_check": {"status": "NOT_APPLICABLE", "detail": "Cliente nao definiu orcamento maximo"},
    "delivery_estimate": {"status": "PASS", "detail": "3 dias uteis para SP capital"}
  },
  "overall": "APPROVED"
}
```

**Guard Conditions para avancar:**

```
CONSIDERATION → DECISION:
  ✅ cliente explicitamente confirma ("pode fechar", "quero esse", "vou levar")
  ✅ validation_checklist.overall == "APPROVED"
  ✅ produto em estoque

CONSIDERATION → CONSIDERATION (loop):
  ❌ cliente pede para ver outras opcoes → volta para DISCOVERY
  ❌ cliente adiciona nova restricao → volta para FILTERING
  ❌ cliente quer comparar de novo → volta para COMPARISON

CONSIDERATION → ABANDONO:
  ⏱️ cliente nao responde por 30 minutos → salva estado, permite retomar
  ⏱️ cliente diz "depois eu vejo" → salva estado com lembrete
```

---

## 🔍 Estado 3: DECISION — O Fechamento

### Objetivo

Processar o pedido com **zero erros**. Este e o estado onde erros custam dinheiro real e confianca do cliente.

### Sub-Estado: CHECKOUT

**Objetivo:** Coletar dados de entrega e pagamento sem atrito.

**Regras:**
- Pedir um dado por vez (WhatsApp = conversa, nao formulario)
- Validar cada campo imediatamente (CEP existe? Endereco completo?)
- Se cliente for recorrente, oferecer "mesmo endereco da ultima vez?"

**Exemplo:**

```
KODA: "Perfeito! Vamos finalizar. Qual o CEP de entrega?"

Marina: "01310-100"

KODA: [Consulta API de CEP]
"Rua Augusta, Consolacao, SP — confere?"

Marina: "Isso! Numero 1500, ap 42"

KODA: "Anotado! E a forma de pagamento?"
```

### Sub-Estado: PAYMENT

**Objetivo:** Processar pagamento com maximo de opcoes e minimo de friccao.

**Metodos suportados:**

| Metodo | Desconto | Prazo Compensacao | Custo KODA |
|---|---|---|---|
| Pix | 5% | Instantaneo | 0.99% |
| Cartao Credito 1x | 0% | Instantaneo | 2.49% |
| Cartao Credito 2-3x | 0% | Instantaneo | 3.99% |
| Boleto | 0% | 2 dias uteis | 1.99% |

**Tratamento de falhas de pagamento:**

```
Tentativa 1: Erro "saldo insuficiente"
  → KODA: "Ops, o banco retornou saldo insuficiente.
          Quer tentar outro cartao ou prefere Pix?"

Tentativa 2: Erro "timeout gateway"
  → KODA: "O gateway de pagamento esta lento agora.
          Vou tentar mais uma vez automaticamente..."

Tentativa 3: Erro "cartao bloqueado"
  → KODA: "Seu banco bloqueou a transacao.
          As vezes acontece por seguranca. Quer tentar
          outro metodo? Pix costuma ser instantaneo. 😊"

Apos 3 falhas:
  → Salva carrinho, estado volta para CONSIDERATION (CHECKPOINT)
  → Cliente pode retomar sem perder o que escolheu
```

### Sub-Estado: CONFIRMATION

**Objetivo:** Garantir que o cliente saiba exatamente o que comprou, quando chega, e como acompanhar.

**Regras:**
- Confirmacao deve incluir: numero do pedido, produto, valor, prazo, link de rastreio
- Se a forma de pagamento tem compensacao (boleto), avisar que pedido so entra em separacao apos
- Salvar pedido no state file (nao depende de memoria de contexto)

**State file apos CONFIRMATION:**

```json
{
  "state": "DECISION",
  "sub_state": "CONFIRMATION",
  "order": {
    "order_id": "KDA-2847",
    "status": "PAID",
    "products": [
      {
        "sku": "SKU-001",
        "name": "Magnesio Quelato 400mg",
        "quantity": 1,
        "unit_price": 59.90,
        "total": 56.90
      }
    ],
    "payment": {
      "method": "PIX",
      "discount_applied": 5.0,
      "transaction_id": "px_20260527_0915_8f3a",
      "paid_at": "2026-05-27T09:25:00Z"
    },
    "delivery": {
      "cep": "01310-100",
      "address": "Rua Augusta, 1500, ap 42",
      "city": "Sao Paulo",
      "state": "SP",
      "estimated_delivery": "2026-05-29",
      "tracking_code": null
    },
    "created_at": "2026-05-27T09:25:30Z"
  }
}
```

**Guard Conditions para avancar:**

```
DECISION → RETENTION:
  ✅ pagamento confirmado (Pix/Cartao: instantaneo; Boleto: apos compensacao)
  ✅ pedido criado no sistema
  ✅ confirmacao enviada ao cliente

DECISION → DECISION (retry):
  ❌ pagamento falhou → PAYMENT_RETRY (max 3 tentativas)
  ❌ endereco invalido → volta para CHECKOUT

DECISION → CONSIDERATION (recusa):
  🔄 cliente desiste no checkout → salva estado, volta para CONSIDERATION
  🔄 cliente quer adicionar/remover produto → volta para CONSIDERATION
```

---

## 🔍 Estado 4: RETENTION — Alem da Venda

### Objetivo

Este estado e o que diferencia KODA de um e-commerce tradicional. O objetivo nao e "vender uma vez" — e **criar um relacionamento continuo**.

### Sub-Estado: ONBOARDING

Comeca imediatamente apos a confirmacao do pedido.

**Objetivo:** Configurar a experiencia pos-compra antes mesmo do produto chegar.

**Acoes:**
- Perguntar se cliente quer lembrete de recompra (quando produto estiver perto de acabar)
- Salvar preferencias detectadas durante a conversa (restricoes, preferencias, frequencia)
- Oferecer canal de suporte prioritario para duvidas sobre uso

### Sub-Estado: FOLLOW_UP

Disparado em 3 momentos:

1. **Na entrega** (via webhook da transportadora): "Seu produto chegou! Como esta sendo a experiencia?"
2. **7 dias apos entrega**: "Suas primeiras noites com Magnesio — como foram?"
3. **30 dias apos entrega**: "1 mes usando Magnesio! Notou diferenca no seu sono?"

**Regras de FOLLOW_UP:**
- Maximo 3 mensagens proativas por pedido (sem spam)
- Cada mensagem deve agregar valor (dica, cupom, pergunta util)
- Se cliente nao responder a 2 mensagens seguidas, pausar follow-ups por 30 dias

### Sub-Estado: RE-ENGAGEMENT

**Objetivo:** Antecipar a proxima compra antes do cliente ficar sem produto.

**Calculo de timing:**

```
dias_para_reengajar = (duracao_frasco_em_dias * percentual_consumo) - dias_para_entrega

Exemplo:
  Magnesio Quelato: 120 capsulas (60 dias para 2/dia ou 120 dias para 1/dia)
  Assumindo 1 capsula/dia: 120 dias
  Re-engajar em: 120 * 0.90 = 108 dias (quando ~10% do frasco restar)
  Menos 3 dias de entrega = 105 dias
```

**Mensagem tipica:**

```
KODA: "Marina! Saudades 🌙
Pelas minhas contas, seu Magnesio Quelato deve estar acabando
essa semana. Quer que eu separe outro pra voce?
(Ai ja aplico o desconto de cliente fiel: 10% off)"
```

### Sub-Estado: SUPPORT

**Objetivo:** Responder qualquer duvida sobre o produto comprado.

KODA esta sempre disponivel para suporte. Mas tem regras claras:
- Duvidas sobre uso: responder com base na bula e guidelines do fabricante
- Duvidas sobre saude: encaminhar para profissional ("consulte seu medico")
- Reclamacoes: seguir fluxo de complaint (registrar, escalar se necessario)

### Sub-Estado: QA_TO_BACKLOG — Fechando o Ciclo de Feedback

O padrão **QA-to-Backlog Feedback Loop** (extraído do workflow de Matt Pocock) estabelece que observações de QA, revisão e suporte não são eventos terminais — são **entradas para o backlog de melhorias**. Sem este ciclo, defeitos descobertos permanecem como memória informal do time e não geram ação estruturada.

**O ciclo de feedback fechado no KODA:**

```
SUPPORT (cliente reporta problema)
       ↓
QA_TO_BACKLOG (triagem e classificação)
       ↓
┌──────────────────────────────────────────────┐
│ 1. Capturar finding como structured observation │
│    → severity, affected_state, reproduction   │
│ 2. Triar: é defeito, melhoria ou feature nova? │
│    → blocker: impede transição de estado?      │
│ 3. Converter em ação de backlog                 │
│    → vertical-slice issue OU regression case   │
│ 4. Devolver ao Kanban (intake lane)            │
│    → rotular AFK-ready ou human-in-loop        │
└──────────────────────────────────────────────┘
       ↓
Novo item no board → execução → verificação → closed loop
```

**Matriz de triagem QA-to-Backlog:**

| Severidade | Tipo | Ação no Backlog | Afeta estado da jornada? |
|-----------|------|----------------|-------------------------|
| CRITICAL | Defeito — cliente recebeu produto errado | Criar regression case + blocker issue | Sim: bloquear transição para DECISION até correção |
| HIGH | Defeito — cupom não aplicado em produto elegível | Criar vertical-slice issue de correção | Sim: adicionar guard condition extra em DECISION:CHECKOUT |
| MEDIUM | Melhoria — explicação da recomendação ficou confusa | Criar issue de melhoria no backlog | Não: fluxo continua, melhoria é assíncrona |
| LOW | UX — mensagem poderia ser mais curta | Agregar em epic de UX, revisar no trimestre | Não |

**Exemplo KODA — uma observação de QA vira ação de backlog:**

```
[QA finding capturado durante revisão de conversa]:
  "Cliente perguntou 'tem algo mais barato?' e KODA recomendou 
   produto R$ 5 mais barato mas com lactose. Cliente era intolerante."
  
  Severity: HIGH
  Type: DEFECT
  Affected state: CONSIDERATION:COMPARISON
  Root cause: FILTERING não reaplicou restrição após cliente mudar critério
  
  → Backlog issue criada:
    Title: "FILTERING deve reaplicar todas as restrições quando cliente 
            altera critério de ordenação (preço, popularidade)"
    Labels: AFK-ready, vertical-slice, consideration-filtering
    Acceptance criteria:
      - Ao mudar ordenação de produtos, restrições (dieta, alergia) 
        são reaplicadas antes da nova lista ser exibida
      - Teste: cliente intolerante à lactose filtra por 'mais barato' 
        → nenhum produto com lactose aparece
    Blocker for: CONSIDERATION → VALIDATION (se restrições não mantidas)
```

**Integração com o board Kanban:**

O KODA mantém um board com lanes específicas para o ciclo QA-to-Backlog:

```
BACKLOG → READY (AFK) → IN PROGRESS → REVIEW → DONE
   ↑                                              │
   └──── QA_INTAKE ←──── QA findings ─────────────┘
```

A lane `QA_INTAKE` recebe observações de:
- **Review findings:** segunda passagem de agente revisor encontra problemas
- **Customer support:** tickets de suporte revelam padrões de defeito
- **Production monitoring:** métricas mostram degradação em estado específico
- **Human QA:** revisões manuais de amostras de conversa

Cada item em `QA_INTAKE` passa pela matriz de triagem antes de ser convertido em issue e movido para `BACKLOG` com as labels apropriadas.

**Checklist de integridade do ciclo QA-to-Backlog:**
- [ ] Toda observação de QA/review gera um artefato rastreável (não fica em memória de time)
- [ ] Cada finding tem severity, affected_state, e root cause registrados
- [ ] Defeitos críticos bloqueiam a transição de estado correspondente
- [ ] Regression cases são criados para defeitos que não devem recorrer
- [ ] O board reflete a distinção entre trabalho novo (features) e trabalho corretivo (QA findings)
- [ ] Tempo médio de QA_INTAKE → BACKLOG é medido e otimizado (< 48h para HIGH/CRITICAL)

Este padrão conecta-se diretamente ao [[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|Multi-Agent Systems]] (o board multi-agente recebe os itens de QA) e ao [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]] (os findings de QA alimentam a calibração das rubricas do Evaluator).

---

## 📊 Metricas por Etapa: O Painel de Controle do KODA

Cada estado da maquina tem metricas especificas que permitem diagnosticar exatamente onde esta o gargalo.

### Tabela de Metricas por Macro-Estado

| Estado | Metrica Principal | Alvo | Alerta Amarelo | Alerta Vermelho | Formula |
|---|---|---|---|---|---|
| **AWARENESS** | Taxa de Classificacao | > 90% | < 85% | < 75% | intencoes_classificadas / total_entradas |
| **AWARENESS** | Tempo Medio Classificacao | < 5s | > 8s | > 12s | soma_tempo_classificacao / total_entradas |
| **AWARENESS** | Taxa de Handoff Humano | < 5% | > 8% | > 15% | handoffs_solicitados / total_entradas |
| **CONSIDERATION** | Taxa de Engajamento | > 70% | < 60% | < 45% | clientes_que_exploram / clientes_em_consideration |
| **CONSIDERATION** | Produtos Vistos por Sessao | 2-4 | < 2 ou > 6 | < 1 ou > 8 | total_produtos_apresentados / total_em_consideration |
| **CONSIDERATION** | Taxa de Abandono | < 20% | > 28% | > 40% | sessoes_abandonadas / total_em_consideration |
| **CONSIDERATION** | Taxa de Conversao para Decision | > 40% | < 30% | < 20% | transicoes_para_decision / total_em_consideration |
| **DECISION** | Taxa de Checkout Iniciado | > 60% | < 45% | < 30% | checkouts_iniciados / clientes_em_decision |
| **DECISION** | Taxa de Pagamento Sucesso | > 90% | < 82% | < 70% | pagamentos_aprovados / tentativas_pagamento |
| **DECISION** | Ticket Medio | R$ 65-85 | < R$ 55 | < R$ 40 | receita_total / total_pedidos |
| **DECISION** | Tempo Medio Fechamento | < 8 min | > 12 min | > 18 min | soma_tempo_decision / total_pedidos |
| **RETENTION** | Taxa de Recompra (30 dias) | > 30% | < 20% | < 12% | clientes_recompraram_30d / clientes_com_pedido |
| **RETENTION** | NPS (Net Promoter Score) | > 70 | < 55 | < 40 | %promotores - %detratores |
| **RETENTION** | LTV (Lifetime Value) | > R$ 250 | < R$ 180 | < R$ 120 | soma_gastos_total / total_clientes |
| **RETENTION** | Taxa de Reativacao | > 25% | < 15% | < 8% | inativos_reativados / total_inativos_mes |

### Como Ler as Metricas

**Exemplo 1 — AWARENESS saudavel:**
```
Taxa de Classificacao: 93% ✅
Tempo Medio: 4.2s ✅
Handoff Humano: 3.1% ✅

Diagnostico: KODA esta entendendo bem as intencoes dos clientes.
```

**Exemplo 2 — CONSIDERATION com problema:**
```
Taxa de Engajamento: 58% ⚠️
Produtos Vistos: 1.2 ⚠️
Abandono: 35% 🔴
Conversao para Decision: 22% 🔴

Diagnostico: Clientes estao vendo poucos produtos e abandonando.
Possivel causa: DISCOVERY nao esta sendo atrativa ou FILTERING
esta eliminando opcoes demais. Investigar sub-estados.
```

**Exemplo 3 — DECISION com gargalo:**
```
Checkout Iniciado: 65% ✅
Pagamento Sucesso: 68% 🔴
Ticket Medio: R$ 72 ✅
Tempo Fechamento: 16 min ⚠️

Diagnostico: Clientes querem comprar mas pagamento esta falhando 32%.
Investigar: gateway fora? muitos erros de saldo? metodo Pix funcionando?
```

### Como Usar as Metricas para Diagnostico

O verdadeiro poder das metricas por estado nao e o numero isolado — e a **correlacao entre metricas de estados consecutivos**.

**Padrao de Diagnostico: O Funil de Estados**

```
                    ENTRARAM NO WHATSAPP
                    1000 clientes/mes
                           │
                           ▼
                    ╔═══════════════╗
                    ║  AWARENESS    ║
                    ╠═══════════════╣
                    ║ 1000 (100%)   ║ ← total que inicia conversa
                    ║  930 (93%)    ║ ← classificados com sucesso
                    ║   70 (7%)     ║ ← handoff ou reclassificacao
                    ╚═══════╤═══════╝
                            │
                            ▼
                    ╔═══════════════╗
                    ║ CONSIDERATION ║
                    ╠═══════════════╣
                    ║  930 (100%)   ║ ← entram em consideration
                    ║  650 (70%)    ║ ← engajam (exploram produtos)
                    ║  280 (30%)    ║ ← abandonam (nao exploram)
                    ║  420 (45%)    ║ ← chegam em VALIDATION
                    ║  230 (25%)    ║ ← dropout entre discovery e validation
                    ╚═══════╤═══════╝
                            │
                            ▼
                    ╔═══════════════╗
                    ║   DECISION    ║
                    ╠═══════════════╣
                    ║  420 (100%)   ║ ← validaram produto
                    ║  340 (81%)    ║ ← iniciam checkout
                    ║   80 (19%)    ║ ← desistem antes do checkout
                    ║  310 (74%)    ║ ← pagamento aprovado
                    ║   30 (7%)     ║ ← falha de pagamento
                    ╚═══════╤═══════╝
                            │
                            ▼
                    ╔═══════════════╗
                    ║  RETENTION    ║
                    ╠═══════════════╣
                    ║  310 (100%)   ║ ← compraram
                    ║  220 (71%)    ║ ← aceitam follow-up
                    ║   90 (29%)    ║ ← recompram em 30 dias
                    ║  155 (50%)    ║ ← LTV > R$ 200
                    ╚═══════════════╝
```

**Diagnostico Rapido pelo Funil:**

| Sinal | Localizacao | Possivel Causa |
|---|---|---|
| Menos de 90% classificados | AWARENESS | Intent classifier com baixa confianca. Mensagens ambiguas sem esclarecimento. |
| Menos de 60% engajam | CONSIDERATION (topo) | DISCOVERY nao atraente. Cliente ve produtos e desiste. |
| Mais de 30% dropout discovery→validation | CONSIDERATION (meio) | FILTERING removendo opcoes demais. COMPARISON confusa. |
| Menos de 80% iniciam checkout | DECISION (topo) | Falta de confianca. VALIDATION nao foi convincente. |
| Mais de 15% falha de pagamento | DECISION (meio) | Problema no gateway. Poucas opcoes de pagamento. |
| Menos de 20% recompram em 30 dias | RETENTION | FOLLOW_UP fraco. Sem RE-ENGAGEMENT efetivo. Produto nao gera recompra natural. |

**Exemplo Real de Diagnostico:**

```
Cenario: Metrica de "Conversao para Decision" caiu de 42% para 28%
         em duas semanas.

Investigacao:
1. Olhar sub-metricas de CONSIDERATION:
   - DISCOVERY: 72% → 70% (estavel)
   - FILTERING: 85% → 82% (estavel)
   - COMPARISON: 65% → 38% 🔴 (queda brusca!)
   - VALIDATION: 90% → 88% (estavel)

2. Hipoteses para COMPARISON com queda:
   a) Template de comparacao mudou? → Verificar changelog
   b) Novos produtos adicionados que confundem a decisao?
   c) Precos subiram e clientes estao hesitando?

3. Acao:
   - Revisar template de COMPARISON
   - Limitar a 3 opcoes (estava mostrando 5)
   - Adicionar "melhor custo-beneficio" destacado
   
Resultado apos correcao: Conversao voltou para 40%.
```

### Metricas de Sinal Vital (Operacionais)

Alem das metricas de negocio, KODA monitora sinais vitais operacionais:

| Metrica Operacional | Alvo | O Que Indica se Ruim |
|---|---|---|
| Latencia state file load | < 50ms | Disco lento, Redis saturado, network issue |
| Latencia guard evaluation | < 10ms | Guard conditions complexas demais |
| Taxa de lock contention | < 2% | Muitas sessoes paralelas para mesmo cliente |
| State file corruption rate | 0% | Bug em serialize/deserialize |
| Audit log write latency | < 20ms | Disco cheio, I/O saturation |
| Transicoes invalidas bloqueadas | < 0.1% | Guard condition com bug (falso positivo) |

---

## ⚠️ Tratamento de Excecoes e Desvios

Nenhum fluxo real e linear. Clientes mudam de ideia, se distraem, tem duvidas inesperadas. KODA precisa tratar essas situacoes sem quebrar.

### Catalogo de Excecoes

| Excecao | Estado Origem | Comportamento | Recuperacao |
|---|---|---|---|
| Cliente pergunta sobre produto que nao existe | CONSIDERATION | Informa que nao encontrou, sugere alternativas | Volta para DISCOVERY |
| Cliente quer produto fora de estoque | CONSIDERATION | Informa indisponibilidade, oferece lista de espera | Volta para DISCOVERY |
| Cliente muda de ideia no checkout | DECISION | Salva estado atual, volta para CONSIDERATION | Retoma de onde parou |
| Pagamento negado 3x | DECISION | Oferece metodos alternativos (Pix, boleto) | Volta para CHECKOUT |
| Cliente some por 30+ minutos | QUALQUER | Salva snapshot completo do estado | Envia mensagem proativa apos 24h |
| Cliente insatisfeito ("quero cancelar") | RETENTION | Inicia fluxo de cancelamento/devolucao | Escala para humano se necessario |
| Cliente pede atendente humano | QUALQUER | Transfere com contexto completo | Handoff estruturado (state file) |
| Gateway de pagamento offline | DECISION | Informa instabilidade, agenda retentativa | Notifica quando gateway volta |
| Produto teve aumento de preco | DECISION | Informa novo preco ANTES de cobrar | Cliente decide se continua |
| Pedido extraviado na entrega | RETENTION | Inicia processo de reenvio ou reembolso | Escala para operacoes |

### Excecoes Complexas: Fluxos Detalhados

#### Excecao: Carrinho Abandonado com Prazo de Preco

Um dos cenarios mais delicados: o cliente monta um carrinho em CONSIDERATION, avanca para DECISION, mas abandona antes de pagar. Enquanto isso, o preco do produto mudou.

**Fluxo de tratamento:**

```
1. Cliente em DECISION/CHECKOUT abandona sessao
   └── State file: snapshot salvo com precos do momento

2. 2 horas depois: preco do SKU-001 sobe de R$ 59,90 para R$ 64,90

3. 4 horas depois: cliente retorna (nova mensagem)
   └── KODA carrega state file

4. KODA detecta: "Preco mudou desde o snapshot"
   └── Avalia guard condition: "preco_atual == preco_snapshot?"

5. GUARD FALHA → KODA informa o cliente:
   "Marina, o Magnesio Quelato que voce escolheu estava
   R$ 59,90, mas o preco atualizou para R$ 64,90.
   Ainda quer levar? Se preferir, posso mostrar opcoes
   similares na faixa dos R$ 59,90."

6. Cliente decide:
   ├── Aceita novo preco → continua DECISION/CHECKOUT
   ├── Quer alternativas → volta para CONSIDERATION/DISCOVERY
   └── Desiste → salva preferencia, estado vai para RETENTION
```

**Por que isso importa:** Nada irrita mais um cliente do que ver um preco na tela e outro na cobranca. KODA detecta a mudanca ANTES de cobrar.

#### Excecao: Concorrencia de Sessoes

Um cliente abre duas conversas simultaneas no WhatsApp (ex: celular + WhatsApp Web). Dois webhooks chegam ao mesmo tempo.

**Fluxo de tratamento:**

```
1. Webhook A (celular): "Quero Magnesio Quelato" — timestamp: 09:15:01.002
2. Webhook B (Web):    "Quero Vitamina D3"     — timestamp: 09:15:01.008

3. KODA processa Webhook A:
   └── Adquire lock no state file: "lock:wa_5511999999999:sess_A"
   └── State esta em CONSIDERATION/DISCOVERY
   └── Processa como "cliente quer Magnesio Quelato"
   └── Avanca para CONSIDERATION/VALIDATION
   └── Libera lock

4. KODA processa Webhook B:
   └── Tenta adquirir lock: CONFLITO (state foi alterado por A)
   └── Le o novo estado: CONSIDERATION/VALIDATION (Magnesio Quelato)
   └── Detecta: cliente disse "Vitamina D3" mas carrinho tem Magnesio
   └── Responde: "Percebi que voce mencionou Vitamina D3 em outra
        conversa. Mas seu carrinho atual tem Magnesio Quelato.
        Qual dos dois voce quer levar? Ou prefere os dois? 😊"
```

**Por que isso importa:** Sem lock, dois webhooks paralelos poderiam criar dois carrinhos diferentes para o mesmo cliente.

#### Excecao: Cliente em Divida Tecnica de Contexto

Cliente novo que ja falou com KODA ha 6 meses, mas o state file foi perdido (migracao de banco, bug, etc.). KODA trata como cliente novo, mas o cliente ESPERA que KODA lembre.

**Fluxo de tratamento:**

```
1. Cliente: "Oi KODA, de novo! Quero o mesmo de sempre."
   
2. KODA: carrega state file → VAZIO (cliente novo?)
   └── Mas o cliente disse "de novo" e "o mesmo de sempre"
   └── Detecta: "Este cliente FALA como se eu devesse lembrar"

3. KODA adapta resposta:
   "Oi! Me desculpa, nao to conseguindo acessar seu historico
   agora. Me lembra qual produto voce costuma levar?
   Ai eu anoto e nao esqueco mais. 😊"
   
   [NAO responde como se fosse cliente novo — seria frustrante]

4. KODA registra internamente:
   └── Flag: "client_with_lost_history" = true
   └── Prioridade: reconstruir preferencias nas proximas interacoes
```

#### Excecao: Produto Descontinuado Durante Jornada

Cliente esta em CONSIDERATION/COMPARISON quando o SKU que ele esta olhando e descontinuado (webhook do ERP).

**Fluxo:**

```
1. KODA recebe webhook: SKU-002 status = "DISCONTINUED"

2. KODA verifica: algum cliente ativo em CONSIDERATION com este SKU?
   └── Sim: Marina (state atual: COMPARISON, candidates: [SKU-001, SKU-002])

3. KODA envia mensagem PROATIVA:
   "Marina, uma atualizacao: o Blend Herbal Noturno que estavamos
   comparando foi descontinuado pelo fornecedor. 😔
   Mas o Magnesio Quelato continua disponivel — e eu encontrei
   uma alternativa ao Blend: Sonus Herbal Complex (R$ 69,90).
   Quer que eu compare os dois?"
```

**Por que isso importa:** Sem proatividade, o cliente descobriria a descontinuacao apenas quando tentasse comprar — gerando frustracao.

### Exemplo de Handoff para Humano

Quando um cliente pede para falar com um atendente, KODA nao simplesmente "desaparece". Ele prepara um pacote de contexto:

```
[KODA → Atendente Humano]
Cliente: Marina (+55 11 99999-9999)
Pedido: #KDA-2847
Estado atual: DECISION / PAYMENT
Problema: Cliente discorda do valor do frete

Contexto da conversa (ultimas 5 mensagens):
- Cliente montou carrinho com Magnesio Quelato
- Pagamento escolhido: Pix
- Cliente questiona: "Frete pra SP nao era gratis?"

Produtos no carrinho:
- 1x Magnesio Quelato 400mg (SKU-001) — R$ 56,90

Historico do cliente:
- Primeira compra
- Restricoes: vegetariana
- Nenhum incidente anterior
```

---

## 📱 Exemplo de Dialogo WhatsApp Real: Jornada Completa

Abaixo, uma transcricao anotada de uma jornada real do KODA. Cada mensagem e marcada com o estado e sub-estado ativo no momento.

```
═══════════════════════════════════════════════════════════════
MINUTO 0 | ESTADO: AWARENESS / INTENT_CLASSIFICATION
═══════════════════════════════════════════════════════════════

Cliente: "Bom dia! Me indicaram voces. To precisando de uma vitamina."

KODA: "Bom dia! Que otimo que te indicaram a gente 😊
Me conta: voce ta sentindo falta de energia no dia a dia,
ou tem alguma preocupacao especifica de saude?"

[KODA classificou: INTENT=PRODUCT_DISCOVERY, ENTITIES={problem: "vitamin_deficiency"}]
[KODA pergunta contextual para refinar intencao]

═══════════════════════════════════════════════════════════════
MINUTO 2 | ESTADO: AWARENESS / CONTEXT_COLLECTION
═══════════════════════════════════════════════════════════════

Cliente: "Cansaco mesmo. Trabalho o dia inteiro no computador,
chego em casa morto. E meu medico falou que minha vitamina D ta baixa."

KODA: "Entendi! Vitamina D baixa e bem comum em quem trabalha
em escritorio. Vou te mostrar o que temos especifico pra isso.
So uma pergunta antes: voce tem alguma restricao alimentar
ou alergia que eu deva saber?"

[KODA coletou: problem=fatigue_vitamin_d, context=office_worker, doctor_recommended]
[KODA pergunta sobre restricoes — guard condition para FILTERING]

═══════════════════════════════════════════════════════════════
MINUTO 4 | ESTADO: CONSIDERATION / DISCOVERY
═══════════════════════════════════════════════════════════════

Cliente: "Nao, nada. Pode me mandar as opcoes?"

KODA: "Claro! Para vitamina D, temos 3 excelentes opcoes:

☀️ VITAMINA D3 2000UI — R$ 34,90
   ✅ Dose diaria ideal para adultos
   ✅ 120 capsulas (4 meses)
   ⚠️ Tomar junto com refeicao (precisa de gordura pra absorver)

☀️ VITAMINA D3 + K2 — R$ 59,90
   ✅ D3 + K2 trabalham juntas (K2 ajuda a fixar calcio nos ossos)
   ✅ 90 capsulas (3 meses)
   ⚠️ Um pouco mais caro, mas absorcao superior

☀️ VITAMINA D3 Liquida — R$ 49,90
   ✅ Sublingual (absorve mais rapido)
   ✅ 30ml (2 meses)
   ⚠️ Sabor levemente oleoso

Quer que eu explique a diferenca entre eles em mais detalhes?"

═══════════════════════════════════════════════════════════════
MINUTO 8 | ESTADO: CONSIDERATION / FILTERING
═══════════════════════════════════════════════════════════════

Cliente: "Nao curto coisa liquida nao. E o medico recomendou 2000UI.
O de 34,90 serve?"

KODA: "Serve perfeitamente! 2000UI e exatamente a dose que
seu medico recomendou. E como sao 120 capsulas, sao 4 meses
de tratamento por R$ 34,90 — menos de R$ 9 por mes."

[KODA aplicou filtro: formato=solido, dosagem=2000UI]
[Resultado: 2 produtos eliminados, 1 candidato ideal]

═══════════════════════════════════════════════════════════════
MINUTO 10 | ESTADO: CONSIDERATION / VALIDATION
═══════════════════════════════════════════════════════════════

Cliente: "Perfeito! Vou levar esse mesmo. Pode fechar?"

KODA: "So pra confirmar:
✅ Vitamina D3 2000UI — 120 capsulas
✅ Dose recomendada pelo seu medico
✅ R$ 34,90
✅ Frete gratis (SP capital)

E isso mesmo?"

Cliente: "Isso!"

[VALIDATION checklist: ALL PASS]
[Transicao: CONSIDERATION → DECISION]

═══════════════════════════════════════════════════════════════
MINUTO 12 | ESTADO: DECISION / CHECKOUT
═══════════════════════════════════════════════════════════════

KODA: "Perfeito! Pra finalizar: CEP de entrega?"

Cliente: "04538-132"

KODA: "Av Brigadeiro Faria Lima, Itaim Bibi, SP — confere?"

Cliente: "Isso! Numero 3500, ap 121"

KODA: "Anotado! Forma de pagamento?"

═══════════════════════════════════════════════════════════════
MINUTO 14 | ESTADO: DECISION / PAYMENT
═══════════════════════════════════════════════════════════════

Cliente: "Cartao de credito"

KODA: "Link seguro de pagamento: pay.koda.app/8f3a
E so clicar e finalizar. Leva 30 segundos."

[3 minutos depois...]

Cliente: "Pago!"

KODA: "Confirmado! 🎉"

═══════════════════════════════════════════════════════════════
MINUTO 17 | ESTADO: DECISION / CONFIRMATION
═══════════════════════════════════════════════════════════════

KODA: "Resumo do seu pedido:
📦 Pedido #KDA-2891
☀️ Vitamina D3 2000UI — 120 caps
💰 R$ 34,90
📍 Av Brigadeiro Faria Lima, 3500, ap 121
🚚 Entrega: ate 29/05
📧 Confirmacao enviada por email"

═══════════════════════════════════════════════════════════════
MINUTO 19 | ESTADO: RETENTION / ONBOARDING
═══════════════════════════════════════════════════════════════

KODA: "Ah! Quer que eu te avise quando tiver perto de acabar?
Como sao 120 capsulas — 4 meses de uso — posso te lembrar
la por setembro. Ai voce ja garante o precinho de hoje."

Cliente: "Boa! Pode sim."

KODA: "Combinado! ☀️ Qualquer duvida sobre como tomar,
efeitos, ou qualquer coisa — e so me chamar. To sempre aqui."
```

**Metricas desta jornada:**
- Tempo total: 19 minutos
- Estados percorridos: AWARENESS → CONSIDERATION → DECISION → RETENTION
- Sub-estados: 9 de 12 possiveis
- Mensagens trocadas: 14 (cliente) + 13 (KODA) = 27
- Satisfacao: cliente concluiu compra com zero atritos

---

## 🎛️ Tabela Comparativa: Estrategias de Coordenacao de Fluxo

KODA implementa multiplas estrategias de coordenacao para gerenciar a maquina de estados. Cada uma resolve um problema diferente:

| Estrategia | Problema que Resolve | Como KODA Usa | Complexidade | Custo |
|---|---|---|---|---|
| **State File (JSON)** | Persistencia entre sessoes | Um arquivo `state/{client_id}.json` mantem estado atual, historico, preferencias | Baixa | Baixo |
| **Guard Conditions** | Transicoes invalidas | Cada transicao so ocorre se condicoes explicitas sao atendidas | Media | Zero (logica) |
| **Timeout + Snapshot** | Abandono de sessao | Apos 30 min sem resposta, estado e salvo e cliente pode retomar depois | Media | Baixo |
| **Generator/Evaluator** | Qualidade de recomendacoes | Generator cria recomendacao, Evaluator valida contra rubrica e restricoes | Alta | 2x LLM calls |
| **Sprint Contracts** | Planejamento de multiplos passos | No sub-estado COMPARISON, KODA planeja o que vai apresentar antes de gerar | Media | 1.5x LLM calls |
| **Human Handoff** | Incapacidade do agente resolver | Quando KODA detecta que nao consegue avancar, prepara contexto e transfere | Media | Custo humano |
| **Idempotency Keys** | Duplicacao de pedidos | Cada checkout gera uma chave unica; pagamentos duplicados sao rejeitados | Baixa | Zero (logica) |
| **Dead Letter Queue** | Falhas em webhooks | Se webhook de pagamento falha, vai para DLQ e e reprocessado com backoff | Alta | Infra |
| **Circuit Breaker** | Gateway de pagamento fora | Se 5 falhas consecutivas, KODA para de oferecer aquele metodo por 5 min | Media | Zero (logica) |
| **Event Sourcing** | Auditabilidade completa | Cada transicao de estado gera evento imutavel no `audit_log.jsonl` | Alta | Storage |

### Detalhamento das Estrategias

#### State File: O Coracao da Persistencia

```
Estrutura no disco (ou Redis):

state/
├── wa_5511999999999.json          ← state file ativo
├── wa_5511999999999.snapshot.1    ← snapshot #1 (30 min timeout)
├── wa_5511999999999.snapshot.2    ← snapshot #2 (mais recente)
├── wa_5511888888888.json
└── wa_5511777777777.json

Cada state file:
- Tamanho medio: 2-8 KB
- Tempo de carga: < 50ms (Redis) / < 5ms (cache local)
- Escrita: atomica (write temp → rename)
- Lock: Redis SETNX com TTL de 30s (evita lock eterno)
```

#### Guard Conditions: Protecao Declarativa

```javascript
// Exemplo: todas as guards de uma transicao
const TRANSITION_GUARDS = {
  'CONSIDERATION→DECISION': [
    {
      name: 'cliente_confirmou',
      description: 'Cliente disse explicitamente que quer comprar',
      fn: (ctx) => ctx.last_message_intent === 'CONFIRM_PURCHASE',
      error_message: 'Cliente ainda nao confirmou a compra'
    },
    {
      name: 'produto_validado',
      description: 'Produto passou pelo Evaluator (VALIDATION sub-state)',
      fn: (ctx) => ctx.context.validation_checklist?.overall === 'APPROVED',
      error_message: 'Produto nao foi validado — executar VALIDATION primeiro'
    },
    {
      name: 'estoque_disponivel',
      description: 'SKU tem estoque > 0 no centro de distribuicao do cliente',
      fn: async (ctx) => {
        const stock = await inventoryAPI.check(ctx.context.selected_sku, ctx.context.delivery_region);
        return stock.available > 0;
      },
      error_message: 'Produto sem estoque na regiao do cliente'
    },
    {
      name: 'preco_atualizado',
      description: 'Preco no state file bate com preco atual do catalogo',
      fn: async (ctx) => {
        const currentPrice = await catalogAPI.getPrice(ctx.context.selected_sku);
        return Math.abs(currentPrice - ctx.context.agreed_price) < 0.01;
      },
      error_message: 'Preco mudou desde que cliente escolheu — informar antes de cobrar'
    }
  ]
};
```

#### Idempotency Keys: Protecao Contra Duplicatas

```javascript
// Cada tentativa de checkout gera uma chave unica
function generateIdempotencyKey(clientId, orderData) {
  const components = [
    clientId,
    orderData.sku,
    orderData.quantity,
    orderData.timestamp.substring(0, 16)  // precisao de minuto
  ];
  return `idem_${crypto.createHash('sha256').update(components.join('|')).digest('hex').substring(0, 12)}`;
}

// Antes de processar pagamento, verifica se a chave ja foi usada
async function processPayment(idempotencyKey, paymentData) {
  const existing = await db.findProcessedPayment(idempotencyKey);
  if (existing) {
    return { status: 'DUPLICATE', original_result: existing.result };
  }
  
  const result = await gateway.charge(paymentData);
  await db.saveProcessedPayment(idempotencyKey, result);
  return { status: 'OK', result };
}
```

#### Circuit Breaker: Protecao Contra Servicos Instaveis

```javascript
class PaymentCircuitBreaker {
  constructor() {
    this.state = 'CLOSED';     // CLOSED → OPEN → HALF_OPEN → CLOSED
    this.failureCount = 0;
    this.failureThreshold = 5;
    this.resetTimeout = 300000;  // 5 minutos
    this.lastFailureTime = null;
  }

  async charge(paymentData) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('CIRCUIT_OPEN: Payment gateway temporariamente indisponivel');
      }
    }

    try {
      const result = await gateway.charge(paymentData);
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.state = 'CLOSED';
    this.failureCount = 0;
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      notifyOps('Payment circuit breaker OPEN — investigar gateway');
    }
  }
}
```

---

## ⚡ Anti-Padroes: O Que NAO Fazer

Estes sao os erros mais comuns ao implementar state machines no KODA:

### Anti-Padrao 1: Estado Implicito

```javascript
// ❌ ERRADO: Estado deduzido de variaveis soltas
if (carrinho.temProdutos && !pagamento.feito) {
  // "provavelmente estamos em checkout..."
}

// ✅ CORRETO: Estado explicito
if (state.current === 'DECISION' && state.sub_state === 'CHECKOUT') {
  // certeza absoluta de onde estamos
}
```

**Problema:** Estado implicito leva a bugs sutis onde o sistema "acha" que esta em um estado mas nao esta.

### Anti-Padrao 2: Guard Conditions com Efeitos Colaterais

```javascript
// ❌ ERRADO: Guard altera estado!
const guard_produto_valido = async (ctx) => {
  ctx.context.product_validated = true;  // EFEITO COLATERAL!
  return await checkProduct(ctx.context.selected_sku);
};

// ✅ CORRETO: Guard apenas avalia
const guard_produto_valido = async (ctx) => {
  return await checkProduct(ctx.context.selected_sku);
};
```

**Problema:** Guards com efeitos colaterais tornam o sistema imprevisivel. A ordem de avaliacao das guards importa (quando nao deveria).

### Anti-Padrao 3: Estado Guarda Toda a Conversa

```json
// ❌ ERRADO: State file de 2 MB com historico completo de mensagens
{
  "context": {
    "full_conversation": [
      {"role": "user", "content": "Oi", "timestamp": "..."},
      {"role": "assistant", "content": "Ola!", "timestamp": "..."},
      // ... 500+ mensagens
    ]
  }
}

// ✅ CORRETO: State file enxuto, conversa em storage separado
{
  "context": {
    "conversation_summary": "Cliente busca suplemento para sono, vegetariano",
    "key_facts": ["vegetariano", "orçamento_max: R$ 80", "prefere capsulas"],
    "conversation_ref": "s3://koda-conversations/wa_5511999999999/2026-05-27.jsonl"
  }
}
```

**Problema:** State files inchados sao lentos para carregar, caros para armazenar, e misturam responsabilidades (estado vs. historico).

### Anti-Padrao 4: Timeout Unico para Tudo

```javascript
// ❌ ERRADO: Mesmo timeout para todos os estados
const TIMEOUT_SECONDS = 1800;  // 30 minutos para tudo

// ✅ CORRETO: Timeout por contexto
const TIMEOUTS = {
  'AWARENESS': 600,        // 10 min — so coletando contexto, cliente pode voltar rapido
  'CONSIDERATION': 1800,   // 30 min — cliente comparando produtos, precisa de tempo
  'DECISION:CHECKOUT': 300, // 5 min — checkout, se demorar e suspeito
  'DECISION:PAYMENT': 900,  // 15 min — pagamento pode demorar (Pix, app do banco)
  'RETENTION': null         // sem timeout — cliente pode voltar semanas depois
};
```

**Problema:** Um timeout unico e sempre errado — muito curto para uns estados, muito longo para outros.

### Anti-Padrao 5: Sem Validacao de Schema

```javascript
// ❌ ERRADO: Salvar qualquer objeto como state file
fs.writeFileSync(statePath, JSON.stringify(stateObject));

// ✅ CORRETO: Validar schema antes de persistir
const validation = STATE_SCHEMA_VALIDATOR.validate(stateObject);
if (!validation.valid) {
  logger.error('State file schema violation', {
    client_id: stateObject.client_id,
    errors: validation.errors
  });
  throw new StateSchemaError(validation.errors);
}
fs.writeFileSync(statePath, JSON.stringify(stateObject));
```

**Problema:** Sem validacao de schema, um bug simples (ex: campo com tipo errado) pode corromper o state file e causar falhas em cascata dias depois.

### Quando Usar Cada Estrategia

```
                    ┌────────────────────────────────────────────┐
                    │     ARVORE DE DECISAO: ESTRATEGIA          │
                    └────────────────────────────────────────────┘

Problema: Cliente some no meio da conversa?
  ├── Sim → TIMEOUT + SNAPSHOT
  └── Nao → Continue

Problema: Preciso garantir que uma transicao so aconteca quando fizer sentido?
  ├── Sim → GUARD CONDITIONS
  └── Nao → Continue

Problema: A qualidade da resposta e critica (ex: recomendacao com alergia)?
  ├── Sim → GENERATOR/EVALUATOR
  └── Nao → Continue

Problema: Pagamento pode ser processado 2x por engano?
  ├── Sim → IDEMPOTENCY KEYS
  └── Nao → Continue

Problema: Preciso de auditoria completa de cada passo?
  ├── Sim → EVENT SOURCING
  └── Nao → Continue

Problema: Servico externo (pagamento, frete) esta instavel?
  ├── Sim → CIRCUIT BREAKER + DEAD LETTER QUEUE
  └── Nao → Continue

Problema: Agente nao consegue resolver a situacao?
  ├── Sim → HUMAN HANDOFF
  └── Nao → Continue
```

---

## 🚀 KODA Application: Implementando um Novo Fluxo

Esta secao mostra como aplicar o padrao de state machine a uma feature real do KODA: **Fluxo de Assinatura (Subscription)**.

### Contexto

KODA quer lancar um programa de assinatura mensal. O cliente recebe o mesmo produto todo mes, com 15% de desconto, e pode pausar/cancelar a qualquer momento.

### Modelagem da State Machine

```
                    ┌─────────────────────────────────┐
                    │  SUBSCRIPTION STATE MACHINE     │
                    └─────────────────────────────────┘

    ┌──────────────┐
    │  SUB_OFFER   │  (KODA oferece assinatura durante RETENTION)
    └──────┬───────┘
           │ [cliente aceita]
           ▼
    ┌──────────────┐
    │  SUB_SETUP   │  (Escolhe produto, frequencia, endereco)
    └──────┬───────┘
           │ [setup completo]
           ▼
    ┌──────────────┐      [pagamento falha]       ┌──────────────┐
    │  SUB_ACTIVE  │─────────────────────────────►│ SUB_PAST_DUE │
    └──────┬───────┘                              └──────┬───────┘
           │                                             │
           │ [cliente pausa]                   [pagamento ok]
           ▼                                             │
    ┌──────────────┐                                     │
    │  SUB_PAUSED  │◄────────────────────────────────────┘
    └──────┬───────┘
           │ [cliente cancela]      [cliente reativa]
           ▼                              │
    ┌──────────────┐                      │
    │ SUB_CANCELED │      ┌───────────────┘
    └──────────────┘      │
                          ▼
                   ┌──────────────┐
                   │  SUB_ACTIVE  │
                   └──────────────┘
```

### Guard Conditions

```
SUB_OFFER → SUB_SETUP:
  ✅ cliente esta em RETENTION
  ✅ cliente comprou produto compativel com assinatura
  ✅ cliente nao tem assinatura ativa

SUB_SETUP → SUB_ACTIVE:
  ✅ produto selecionado (SKU valido)
  ✅ frequencia escolhida (mensal, bimestral, trimestral)
  ✅ endereco de entrega confirmado
  ✅ pagamento recorrente configurado

SUB_ACTIVE → SUB_PAUSED:
  ✅ cliente solicita pausa
  ✅ periodo minimo de 2 ciclos ja cobrados (evita abuso)

SUB_ACTIVE → SUB_PAST_DUE:
  ❌ pagamento recorrente falhou
  ❌ 3 tentativas de recobranca em 5 dias

SUB_PAST_DUE → SUB_ACTIVE:
  ✅ pagamento pendente regularizado

SUB_PAST_DUE → SUB_CANCELED:
  ⏱️ 14 dias sem regularizar pagamento

SUB_PAUSED → SUB_ACTIVE:
  ✅ cliente solicita reativacao
  ✅ proximo ciclo agendado

SUB_PAUSED → SUB_CANCELED:
  ✅ cliente solicita cancelamento definitivo
```

### Exemplo de Dialogo — Offer de Assinatura

```
[Estado: RETENTION / RE-ENGAGEMENT]

KODA: "Marina! Seu Magnesio Quelato esta acabando.
E se eu te contar que da pra economizar 15% todo mes? 🌙

Nosso plano de assinatura:
📦 Magnesio Quelato entregue todo mes
💰 R$ 50,90/mes (em vez de R$ 59,90)
⏸️ Pode pausar ou cancelar quando quiser
🚚 Frete gratis sempre

Quer ativar?"

Marina: "Nossa, otimo! Pode ser."

KODA: "Perfeito! Entao fica assim:
📦 Magnesio Quelato 400mg — 120 caps/mes
💰 R$ 50,90/mes (15% off)
📅 Primeira entrega: 05/06
💳 Cobranca recorrente: dia 01 de cada mes

So pra confirmar: mesmo endereco da ultima compra?
Rua Augusta, 1500, ap 42?"

Marina: "Isso mesmo!"

KODA: "Assinatura ativada! 🎉
Todo dia 01, R$ 50,90 serao cobrados e seu
Magnesio chega ate dia 05. Se quiser pausar,
cancelar ou trocar o produto, e so me chamar."
```

### Implementacao: Estrutura de Codigo para o Fluxo de Assinatura

Abaixo, como a estrutura de state machine se traduz em codigo:

```javascript
// koda-states/subscription.js — Maquina de estados do fluxo de assinatura

const SUBSCRIPTION_STATES = {
  SUB_OFFER: {
    description: 'Oferecer assinatura durante retencao',
    allowed_transitions: ['SUB_SETUP'],
    guard_conditions: [
      { name: 'cliente_em_retencao', fn: (ctx) => ctx.current_state === 'RETENTION' },
      { name: 'produto_compativel', fn: (ctx) => ctx.context.product_category in ['suplementos', 'vitaminas'] },
      { name: 'sem_assinatura_ativa', fn: (ctx) => !ctx.context.has_active_subscription },
      { name: 'cliente_aceitou_oferta', fn: (ctx) => ctx.last_message_intent === 'ACCEPT_OFFER' }
    ],
    system_prompt: 'subscription_offer_prompt',
    evaluator_rubric: 'subscription_offer_rubric',
    timeout_seconds: 300,
    on_timeout: 'SUB_OFFER_EXPIRED'
  },

  SUB_SETUP: {
    description: 'Configurar produto, frequencia, endereco',
    allowed_transitions: ['SUB_ACTIVE', 'SUB_OFFER'],
    required_fields: ['product_sku', 'frequency', 'delivery_address', 'payment_token'],
    guard_conditions: [
      { name: 'sku_valido', fn: (ctx) => ctx.catalog.has(ctx.context.selected_sku) },
      { name: 'frequencia_valida', fn: (ctx) => ['monthly', 'bimonthly', 'quarterly'].includes(ctx.context.frequency) },
      { name: 'endereco_completo', fn: (ctx) => ctx.context.delivery_address.isComplete() },
      { name: 'pagamento_configurado', fn: (ctx) => ctx.context.payment_token !== null }
    ],
    system_prompt: 'subscription_setup_prompt',
    max_retries: 3,
    on_max_retries: 'SUB_OFFER'  // volta para oferta se setup falhar
  },

  SUB_ACTIVE: {
    description: 'Assinatura ativa, cobranca recorrente',
    allowed_transitions: ['SUB_PAUSED', 'SUB_PAST_DUE', 'SUB_CANCELED'],
    guard_conditions: [
      { name: 'pagamento_em_dia', fn: (ctx) => ctx.context.last_payment_status === 'PAID' }
    ],
    recurring_tasks: [
      { name: 'monthly_charge', cron: '0 8 1 * *', fn: chargeSubscription },
      { name: 'delivery_webhook', trigger: 'DELIVERY_STATUS_CHANGE', fn: updateDeliveryStatus }
    ],
    circuit_breaker: {
      max_failures: 5,
      window_seconds: 300,
      on_open: 'SUB_PAST_DUE'
    }
  },

  SUB_PAUSED: {
    description: 'Assinatura pausada pelo cliente',
    allowed_transitions: ['SUB_ACTIVE', 'SUB_CANCELED'],
    guard_conditions: [
      { name: 'minimo_2_ciclos', fn: (ctx) => ctx.context.cycles_completed >= 2 },
      { name: 'cliente_quer_reativar', fn: (ctx) => ctx.last_message_intent === 'RESUME_SUBSCRIPTION' }
    ],
    max_pause_days: 90,
    on_max_pause: 'SUB_CANCELED'
  },

  SUB_PAST_DUE: {
    description: 'Pagamento pendente, em periodo de regularizacao',
    allowed_transitions: ['SUB_ACTIVE', 'SUB_CANCELED'],
    guard_conditions: [
      { name: 'pagamento_regularizado', fn: (ctx) => ctx.context.last_payment_status === 'PAID' },
      { name: 'prazo_expirado', fn: (ctx) => ctx.context.days_past_due > 14 }
    ],
    retry_schedule: [1, 3, 5],  // dias para tentar recobranca
    notification_schedule: [7, 14],  // dias para avisar cliente
    on_prazo_expirado: 'SUB_CANCELED'
  },

  SUB_CANCELED: {
    description: 'Assinatura encerrada (cliente ou sistema)',
    allowed_transitions: [],  // estado terminal para assinatura
    guard_conditions: [],
    on_enter: [
      { action: 'release_discount', description: 'Remover desconto de assinante' },
      { action: 'send_feedback_survey', description: 'Perguntar motivo do cancelamento' },
      { action: 'save_winback_opportunity', description: 'Salvar para campanha de reativacao futura' }
    ]
  }
};

// Funcao core: avaliar se uma transicao e valida
async function evaluateTransition(clientId, fromState, toState) {
  const ctx = await loadClientContext(clientId);
  const stateConfig = SUBSCRIPTION_STATES[fromState];

  if (!stateConfig.allowed_transitions.includes(toState)) {
    return { allowed: false, reason: `Transicao ${fromState} → ${toState} nao permitida` };
  }

  const targetConfig = SUBSCRIPTION_STATES[toState];
  for (const guard of targetConfig.guard_conditions) {
    const result = await guard.fn(ctx);
    if (!result) {
      return { allowed: false, reason: `Guard '${guard.name}' falhou` };
    }
  }

  return { allowed: true };
}
```

### Cenarios de Teste para o Fluxo de Assinatura

| ID | Cenario | Caminho Esperado | Resultado |
|---|---|---|---|
| SUB-01 | Cliente aceita oferta, setup completo | OFFER → SETUP → ACTIVE | ✅ Assinatura ativa |
| SUB-02 | Cliente recusa oferta | OFFER → OFFER (loop, KODA agradece) | ✅ Continua em RETENTION |
| SUB-03 | Setup incompleto (falta endereco) | SETUP → SETUP (loop ate completar) | ✅ Nao avanca sem campos |
| SUB-04 | Pagamento falha 1x | ACTIVE → ACTIVE (retry dia 1) | ✅ Recuperacao automatica |
| SUB-05 | Pagamento falha 5x em 5 min | ACTIVE → PAST_DUE (circuit breaker) | ✅ Protecao contra loop |
| SUB-06 | Cliente pausa apos 2 ciclos | ACTIVE → PAUSED | ✅ Pausa permitida |
| SUB-07 | Cliente tenta pausar no 1o ciclo | ACTIVE → ACTIVE (bloqueado) | ❌ Guard bloqueia |
| SUB-08 | 14 dias past due sem pagamento | PAST_DUE → CANCELED | ✅ Cancelamento automatico |
| SUB-09 | Pagamento regularizado no dia 10 | PAST_DUE → ACTIVE | ✅ Assinatura reativada |
| SUB-10 | Cliente solicita cancelamento | PAUSED → CANCELED | ✅ Cancelamento manual |

### Padroes de Design para Novos Fluxos

Quando voce for modelar um novo fluxo no KODA, siga estes 5 passos:

**Passo 1: Identifique os Estados de Repouso**

Um "estado de repouso" e onde o cliente pode ficar indefinidamente sem que nada de errado acontenca. Exemplos:
- `SUB_ACTIVE`: cliente pagando normalmente, assinatura rolando
- `SUB_PAUSED`: cliente pausou, aguardando reativacao
- `SUB_CANCELED`: terminal, nada mais acontece

Estados de repouso devem ser o destino final de transicoes bem-sucedidas.

**Passo 2: Identifique os Estados de Transicao**

Estados onde o cliente nao deve ficar por muito tempo. Exemplos:
- `SUB_SETUP`: configuracao inicial, cliente deve sair em minutos
- `SUB_PAST_DUE`: pagamento pendente, prazo maximo de 14 dias

Estados de transicao devem ter timeout.

**Passo 3: Modele Transicoes Unidirecionais Primeiro**

Comece modelando o "caminho feliz" (happy path) como uma linha reta:

```
OFFER → SETUP → ACTIVE
```

Depois adicione os desvios:

```
ACTIVE → PAUSED → ACTIVE   (pausa e retorno)
ACTIVE → PAST_DUE → ACTIVE  (problema de pagamento e regularizacao)
ACTIVE → CANCELED            (cancelamento direto)
PAST_DUE → CANCELED          (cancelamento por inadimplencia)
```

**Passo 4: Escreva Guard Conditions como Testes Unitarios**

Cada guard condition deve poder ser testada isoladamente:

```javascript
describe('Guard: minimo_2_ciclos', () => {
  it('permite pausa quando cliente tem 2+ ciclos', () => {
    const ctx = { cycles_completed: 2 };
    expect(minimo_2_ciclos(ctx)).toBe(true);
  });

  it('bloqueia pausa quando cliente tem 1 ciclo', () => {
    const ctx = { cycles_completed: 1 };
    expect(minimo_2_ciclos(ctx)).toBe(false);
  });

  it('bloqueia pausa quando cliente tem 0 ciclos', () => {
    const ctx = { cycles_completed: 0 };
    expect(minimo_2_ciclos(ctx)).toBe(false);
  });
});
```

**Passo 5: Defina Metricas Antes de Implementar**

Para cada estado, responda: "O que eu gostaria de saber daqui a 1 mes?"

| Estado | Pergunta | Metrica |
|---|---|---|
| SUB_OFFER | Quantos clientes aceitam a oferta? | Taxa de conversao: OFFER → SETUP |
| SUB_SETUP | Onde o setup trava? | Campo com maior taxa de abandono |
| SUB_ACTIVE | Quanto tempo dura em media? | Tempo medio ate primeiro PAUSE/CANCEL |
| SUB_PAUSED | Clientes voltam depois de pausar? | Taxa de reativacao apos pausa |
| SUB_PAST_DUE | Quanto tempo leva para regularizar? | Tempo medio em PAST_DUE |
| SUB_CANCELED | Por que cancelam? | Top 3 motivos (via feedback survey) |

---

## 🧪 Testando a Maquina de Estados

Testar state machines e diferente de testar funcoes puras. Voce precisa testar **sequencias de transicoes**, nao apenas transicoes isoladas.

### Estrategia de Teste: Property-Based Testing

Em vez de escrever casos especificos, defina propriedades que devem ser sempre verdadeiras:

```
PROPRIEDADE 1: INVARIANTES GLOBAIS
"Em qualquer estado, estas condicoes devem ser verdadeiras:"
  ✅ cliente_id nunca e null
  ✅ session_id nunca e null
  ✅ state_history nunca esta vazio
  ✅ last_activity_at > conversation_started_at

PROPRIEDADE 2: TRANSICOES NAO-REVERSIVEIS
"Se a transicao OFFER → SETUP ocorreu, entao:"
  ✅ state_history contem a transicao
  ✅ current_state !== 'SUB_OFFER'

PROPRIEDADE 3: TIMEOUTS SAO RESPEITADOS
"Se um estado de transicao tem timeout de N segundos:"
  ✅ apos N+1 segundos sem atividade, estado muda
  ✅ on_timeout e executado exatamente 1 vez

PROPRIEDADE 4: GUARD CONDITIONS SAO ATOMICAS
"Se uma transicao requer N guards:"
  ✅ se 1 guard falha, estado NAO muda
  ✅ ordem das guards nao altera resultado (idempotencia)
```

### Teste de Regressao: Cenarios Canonicos

Mantenha uma suite de cenarios canonicos que representam jornadas reais:

```javascript
const CANONICAL_SCENARIOS = [
  {
    name: 'Jornada feliz completa',
    steps: [
      { action: 'first_message', intent: 'PRODUCT_DISCOVERY' },
      { action: 'explore_products', expected_state: 'CONSIDERATION:DISCOVERY' },
      { action: 'apply_filter', filter: 'vegetariano', expected_state: 'CONSIDERATION:FILTERING' },
      { action: 'select_product', expected_state: 'CONSIDERATION:VALIDATION' },
      { action: 'confirm_purchase', expected_state: 'DECISION:CHECKOUT' },
      { action: 'provide_address', expected_state: 'DECISION:CHECKOUT' },
      { action: 'pay', method: 'PIX', expected_state: 'DECISION:CONFIRMATION' },
      { action: 'payment_confirmed', expected_state: 'RETENTION:ONBOARDING' }
    ],
    expected_final_state: 'RETENTION:ONBOARDING',
    expected_state_count: 8
  },

  {
    name: 'Cliente abandona e retorna no dia seguinte',
    steps: [
      { action: 'first_message', intent: 'PRODUCT_DISCOVERY' },
      { action: 'explore_products' },
      { action: 'select_product' },
      { action: 'timeout', seconds: 1800 },  // 30 min
      { action: 'return_next_day', message: 'Oi, quero continuar' },
      { action: 'resume_from_snapshot' }
    ],
    expected_final_state: 'CONSIDERATION:VALIDATION',
    expected_resume_success: true
  },

  {
    name: 'Pagamento falha 3x e cliente muda de metodo',
    steps: [
      { action: 'start_checkout' },
      { action: 'pay', method: 'CREDIT_CARD', result: 'FAILED' },
      { action: 'pay', method: 'CREDIT_CARD', result: 'FAILED' },
      { action: 'pay', method: 'CREDIT_CARD', result: 'FAILED' },
      { action: 'switch_method', to: 'PIX' },
      { action: 'pay', method: 'PIX', result: 'SUCCESS' }
    ],
    expected_final_state: 'DECISION:CONFIRMATION',
    expected_retry_count: 3,
    expected_method_switch: true
  },

  {
    name: 'Cliente pede humano durante checkout',
    steps: [
      { action: 'start_checkout' },
      { action: 'request_human', message: 'Quero falar com pessoa real' },
      { action: 'handoff_prepared' }
    ],
    expected_state: 'HANDOFF_HUMANO',
    expected_context_package_complete: true
  }
];
```

### Validacao de Consistencia do State File

Todo state file deve passar por uma validacao de schema antes de ser salvo:

```javascript
const STATE_FILE_SCHEMA = {
  type: 'object',
  required: ['client_id', 'current_state', 'state_history', 'context', 'last_activity_at'],
  properties: {
    client_id: { type: 'string', pattern: '^wa_[0-9]+$' },
    current_state: { type: 'string', enum: ALL_VALID_STATES },
    current_sub_state: { type: 'string', enum: ALL_VALID_SUB_STATES },
    state_history: {
      type: 'array',
      minItems: 1,
      items: {
        type: 'object',
        required: ['from', 'to', 'timestamp', 'trigger', 'guard_evaluation'],
        properties: {
          guard_evaluation: { type: 'string', enum: ['ALL_PASS', 'GUARD_FAILED', 'TIMEOUT', 'HANDOFF'] }
        }
      }
    },
    context: {
      type: 'object',
      required: ['intent', 'intent_confidence'],
      properties: {
        intent_confidence: { type: 'number', minimum: 0, maximum: 1 }
      }
    }
  }
};
```

### Checklist de Teste para Novos Fluxos

Antes de colocar um novo fluxo em producao:

- [ ] Teste do caminho feliz (happy path) completo
- [ ] Teste de cada guard condition isoladamente
- [ ] Teste de cada transicao invalida (deve ser rejeitada)
- [ ] Teste de timeout (30 min, 24h, 14 dias)
- [ ] Teste de recuperacao de snapshot apos abandono
- [ ] Teste de concorrencia (2 mensagens simultaneas)
- [ ] Teste de handoff humano (contexto completo?)
- [ ] Teste de schema validation (state file corrupto?)
- [ ] Teste de idempotencia (mesmo evento 2x nao causa duplicata)
- [ ] Teste de metricas (contadores incrementam corretamente?)

---

## 🧠 O Que Voce Aprendeu

### 1. **KODA e uma Maquina de Estados, Nao um Chatbot**
Cada interacao com cliente passa por estados bem definidos (AWARENESS → CONSIDERATION → DECISION → RETENTION), com regras claras de transicao.

### 2. **Cada Estado Tem um Unico Objetivo**
- AWARENESS: classificar intencao, coletar contexto
- CONSIDERATION: explorar, filtrar, comparar, validar
- DECISION: processar pedido com zero erros
- RETENTION: fidelizar, re-engajar, suportar

### 3. **Guard Conditions Tornam o Sistema Previsivel**
Toda transicao de estado tem condicoes explicitas. Nada acontece "porque sim". Isso elimina comportamentos erraticos.

### 4. **Sub-Estados Decompõem Complexidade**
Cada macro-estado e decomposto em sub-estados com responsabilidade unica. CONSIDERATION vira DISCOVERY → FILTERING → COMPARISON → VALIDATION.

### 5. **Metricas por Estado Permitem Diagnostico Preciso**
Voce nao precisa adivinhar onde esta o gargalo. As metricas mostram exatamente qual estado (e sub-estado) precisa de atencao.

### 6. **Excecoes Sao Tratadas como Estados, Nao como Erros**
Timeout, abandono, recusa de pagamento, handoff humano — todos sao estados validos com caminhos de recuperacao definidos.

### 7. **Coordenacao Multi-Estrategia e Essencial**
State files, guard conditions, Generator/Evaluator, idempotency keys, circuit breakers — cada estrategia resolve um problema especifico. Nenhuma resolve tudo sozinha.

### 8. **Novos Fluxos Seguem o Mesmo Padrao**
Seja subscription, reembolso, ou programa de fidelidade — modele como state machine, defina guard conditions, implemente. O padrao e reutilizavel.

---

## ✅ Checkpoint: Voce Aprendeu?

Antes de seguir, verifique:

- [ ] Consigo desenhar a state machine completa do KODA (4 macro-estados)
- [ ] Entendo o que cada sub-estado faz e qual seu objetivo unico
- [ ] Sei escrever guard conditions para qualquer transicao
- [ ] Consigo diagnosticar um gargalo usando a tabela de metricas
- [ ] Entendo como excecoes (timeout, abandono, handoff) sao tratadas
- [ ] Consigo modelar um novo fluxo (ex: reembolso) usando o mesmo padrao
- [ ] Entendo a diferenca entre as estrategias de coordenacao e quando usar cada uma
- [ ] Consigo ler um state file JSON e reconstruir a jornada do cliente

Se respondeu "nao" para qualquer uma:
- Releia a secao correspondente
- Tente desenhar a state machine no papel (ajuda a fixar)
- Pense em uma jornada real que voce viveu como consumidor no WhatsApp

---

## 🔗 Conexoes com Outros Modulos

| Modulo | Conexao |
|---|---|
| **Nivel 1: 01-why-agents-lose-plot.md** | Guard conditions resolvem Context Amnesia; sub-estados resolvem Planning-Execution Collapse |
| **Nivel 2: 01-generator-evaluator-pattern.md** | VALIDATION (sub-estado de CONSIDERATION) usa Generator/Evaluator para validar recomendacoes |
| **Nivel 2: 02-sprint-contracts.md** | Sub-estados sao implementados como sprints atomicos com contrato claro de entrada/saida |
| **Nivel 2: 03-rubric-design.md** | Cada guard condition e essencialmente uma rubrica de validacao |
| **Nivel 3: 02-state-persistence.md** | State file da jornada e o mecanismo de persistencia que permite retomar sessoes |
| **Nivel 3: 03-file-based-coordination.md** | State files e audit_log usam coordenacao por arquivo para evitar race conditions |
| **Nivel 4: 01-koda-architecture.md** | A maquina de estados e o coracao da arquitetura do KODA |
| **Nivel 4: 03-feature-design-patterns.md** | Todo feature novo deve ser modelado como state machine antes de implementar |

---

## 🚀 Proximos Passos

### Curto Prazo (Esta Semana)
1. Desenhe a state machine de UM fluxo KODA que voce conhece bem
2. Liste 3 guard conditions que poderiam evitar erros nesse fluxo
3. Calcule as metricas atuais desse fluxo e compare com os alvos da tabela

### Medio Prazo (Este Mes)
1. Modele um fluxo novo (ex: programa de fidelidade) usando o padrao de state machine
2. Implemente guard conditions para todas as transicoes
3. Adicione metricas de monitoramento para cada sub-estado

### Longo Prazo (Este Trimestre)
1. Todos os fluxos KODA estao modelados como state machines
2. Dashboard mostra metricas em tempo real por estado
3. Novos fluxos sao desenhados no padrao ANTES de implementar
4. Time consegue diagnosticar gargalos olhando exclusivamente para as metricas de estado

---

## 📞 Duvidas?

Se algo nao ficou claro:
- Releia o Prologo — a jornada da Marina exemplifica tudo
- Revise o diagrama ASCII — ele e a referencia visual completa
- Consulte a tabela de metricas — ela mostra o que medir em cada etapa
- Pergunte ao time — modelagem de estado e um exercicio coletivo

---

## 📚 Referencias

### Dentro deste Programa
- `01-koda-architecture.md` — Arquitetura completa do KODA
- `03-feature-design-patterns.md` — Como modelar features como state machines
- `case-studies/` — Estudos de caso com jornadas reais
- `exercises/` — Exercicios praticos de modelagem de fluxos

### Externo
- AARRR Pirate Metrics Framework (Dave McClure, 2007)
- Finite State Machines in Distributed Systems (Amazon Builders' Library)
- WhatsApp Business API — Message Templates and Session Management

---

## 💭 Reflexao Final

> "Um agente sem state machine e um barco sem leme. Ele vai para onde a corrente levar. Com state machine, voce define o destino — e garante que cada remada leva para la."

A jornada do cliente nao e linear. Clientes mudam de ideia, se distraem, fazem perguntas inesperadas. Mas com uma maquina de estados bem definida, KODA sabe exatamente:

- **Onde** o cliente esta agora
- **Para onde** pode ir em seguida
- **O que** precisa acontecer para avancar
- **O que** fazer quando algo sai do esperado

Isso nao e apenas engenharia. E empatia automatizada.

Voce agora entende como KODA transforma "oi" em "obrigado, compro sempre com voces".

---

**Pronto para `03-feature-design-patterns.md`? Continue. O sistema te espera.**

---

*Escrito com foco em clareza, relevancia pratica e aplicacao imediata.*
*Cada estado, transicao e guard condition aqui descrito e implementavel em codigo real.*

---

## 📋 Metadata

| Campo | Valor |
|---|---|
| **Arquivo** | 02-customer-journey-flows.md |
| **Nivel** | 4 — KODA-Especifico |
| **Tempo** | 120-150 minutos |
| **Status** | ✅ Completo |
| **Proximo** | 03-feature-design-patterns.md |
| **Dependencia** | 01-koda-architecture.md |
| **Critica para** | Todas as features do KODA |
| **Atualizado** | Maio 2026 |
