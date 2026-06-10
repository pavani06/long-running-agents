---
title: "Estudos de Caso: Padrões de Agentes de Longa Duração"
type: curriculum-case-study
aliases: []
tags: [curriculo-conteudo, caso-de-estudo, compilacao-de-casos, visao-geral, padroes-de-agentes, arquitetura-aplicada, multi-agentes]
relates-to: ["[[curriculum/09-case-studies/01-retro-game-maker|Retro Game Maker]]", "[[curriculum/09-case-studies/03-koda-product-discovery|KODA Product Discovery]]"]
last_updated: 2026-06-10
---
# Estudos de Caso: Padrões de Agentes de Longa Duração

**Audiência:** Time Técnico FutanBear  
**Objetivo:** Demonstrar a aplicação real dos padrões de agentes de longa duração  
**Formato:** 5 estudos de caso detalhados — 2 genéricos \+ 3 específicos do KODA

---

# Estudo de Caso 1: Retro Game Maker

**Nível de Complexidade:** Nível 2–3  
**Duração de Runtime:** 6+ horas  
**Foco:** Planner/Generator/Evaluator · Sprint Contracts · Context Management

---

## Problema

Um desenvolvedor precisa construir uma aplicação web de criação de jogos retrô a partir de um único comando: *"Build a retro game maker with sprite editor and level designer."* O escopo é vasto — editor de sprites, designer de fases, modo de jogo, ferramentas de animação e suporte a IA. A tentação natural é atacar tudo de uma vez com um único agente. O resultado foi um fracasso previsível.

---

## Abordagem Inicial (Falha)

Agente Único:

├─ Recebe o prompt

├─ Tenta construir tudo simultaneamente

├─ Contexto esgotado após 2 horas

├─ Resultado: App quebrado e incompleto

└─ Custo: $200 \+ 6 horas desperdiçadas

**Por que falhou:** Um agente único não consegue manter coerência sobre um projeto tão extenso. Sem separação de responsabilidades, o contexto se fragmenta, o código de módulos anteriores é esquecido e a qualidade degrada progressivamente.

---

## Solução: Multi-Agent Harness com Sprint Contracts

A solução dividiu o trabalho em três papéis distintos, operando em ciclos iterativos:

FASE 1 — Planner (5 minutos)

├─ Input: "Build a retro game maker"

├─ Processo: Decompõe em 10 sprints estruturados

├─ Output: spec.md com escopo, critérios de aceitação e sequência

└─ Sprints definidos: Sprite Editor → Level Designer → Play Mode

                     → Animation Tool → Export → AI Assist

                     → Sound → Multiplayer → Marketplace → Polish

FASE 2 — Generator (Sprint 1: 2 horas)

├─ Input: Sprint 1 do spec.md

├─ Processo: Constrói o Sprite Editor com React \+ Canvas

├─ Output: Código funcional \+ documentação do que foi construído

└─ Sem knowledge de sprints futuros (contexto isolado)

FASE 3 — Evaluator (Sprint 1: 10 minutos)

├─ Input: Código do Generator \+ rubrica de aceitação

├─ Processo: Testa se o usuário consegue criar sprites

├─ Grades: Cada critério da rubrica pontuado de 0–10

└─ Output: Aprovado / Ajustes necessários → Generator revisa

REPETE para Sprints 2–10 (total \~4 horas adicionais)

### Sprint Contract (Exemplo — Sprint 1\)

\#\# Sprint 1: Sprite Editor

\#\#\# Input esperado

\- Canvas 16x16 com grid visível

\- Paleta de 16 cores

\#\#\# Critérios de Aceitação

1\. Usuário consegue desenhar pixel a pixel

2\. Ferramenta de borracha funcional

3\. Exportação como PNG

4\. Preview em tamanho real

\#\#\# Definição de "Done"

\- Todos os 4 critérios com nota ≥ 7/10 na avaliação

\- Zero erros no console do browser

---

## Arquitetura

Harness Controller

│

├── spec.md (compartilhado por todos os agentes)

│

├── Sprint Loop (x10)

│   ├── Generator Agent

│   │   ├── Lê: spec.md \+ sprint\_N\_contract.md

│   │   ├── Escreve: sprint\_N\_output/

│   │   └── Contexto resetado a cada sprint

│   │

│   └── Evaluator Agent

│       ├── Lê: sprint\_N\_output/ \+ rubrica

│       ├── Grava: sprint\_N\_eval.md

│       └── Decide: Approve / Request Revision

│

└── Final Assembly Agent

    ├── Integra todos os sprints

    └── Produz: game-maker-final/

---

## Gerenciamento de Estado

project-state/

├── spec.md                    \# Plano mestre (imutável após Fase 1\)

├── sprint\_progress.json       \# Sprint atual, status de cada um

├── sprint\_1\_eval.md           \# Avaliação do Sprint 1

├── sprint\_2\_eval.md           \# Avaliação do Sprint 2

└── sprint\_N\_output/           \# Código gerado por sprint

    ├── index.html

    ├── sprite-editor.js

    └── styles.css

O isolamento de contexto por sprint é a chave: o Generator não carrega o código dos sprints anteriores — apenas o contrato do sprint atual. Isso previne o colapso de contexto que derrubou a abordagem inicial.

---

## Resultados

Abordagem Anterior (Agente Único):

├─ Conclusão: Nunca (contexto esgotado)

├─ Output: App quebrado

├─ Custo: $200 jogados fora

└─ Qualidade: Inutilizável

Abordagem Generator/Evaluator (10 Sprints):

├─ Conclusão: 6 horas de runtime

├─ Output: Game maker completamente funcional

├─ Features: Sprite editor, level designer, play mode, AI assist

├─ Custo: $200 — mas com valor entregue

└─ Qualidade: Coerente, polido, com features extras emergentes

---

## Padrões-Chave Utilizados

1. **Planner:** Decomposição antecipada em 10 sprints com escopo claro  
2. **Sprint Contracts:** Critérios de aceitação explícitos por sprint  
3. **Generator/Evaluator:** Separação entre construção e verificação de qualidade  
4. **Trace Reading:** Debug estruturado quando um sprint falha  
5. **Context Management:** Reset de contexto entre sprints previne degradação

---

## Lições Aprendidas

1. **Planejamento funciona:** A decomposição em sprints preveniu o colapso de contexto fatal  
2. **Separação de concerns:** O Evaluator capturou problemas que o Generator não viu  
3. **Contratos importam:** Critérios claros \= output consistente e previsível  
4. **Iteração vence:** Multi-pass supera amplamente a tentativa única  
5. **Token budgeting:** Sprints evitam o desperdício de contexto acumulado

---

## Aplicação no KODA

Este padrão mapeia diretamente para o ciclo de vendas do KODA no WhatsApp:

- **Planner:** Mapeia a jornada do cliente em etapas (descoberta → recomendação → pedido → fulfillment)  
- **Generator:** Executa cada etapa da conversa com foco total  
- **Evaluator:** Verifica a precisão do pedido antes de enviar para fulfillment  
- **Sprint Contracts:** Define o que "conversa bem-sucedida" significa em cada etapa

---

---

# Estudo de Caso 2: Browser DAW (Digital Audio Workstation)

**Nível de Complexidade:** Nível 3–4  
**Duração de Runtime:** 3h 50min  
**Foco:** State Persistence · File-Based Coordination · Continuous Build

---

## Problema

Construir uma ferramenta de produção musical no browser, com: timeline de áudio, controles de sintetizador, gravação e playback sincronizado. O desafio central não é apenas a complexidade técnica — é a necessidade de que múltiplos agentes compartilhem estado ao longo de horas, sem perder coerência.

---

## Solução: Sistema de 3 Agentes com Estado em Arquivo

Browser DAW: 3-Agent System

├── Planner Agent (estrategista)

│   ├─ Input: Requisitos do projeto musical

│   ├─ Output: Build plan com 4 sprints

│   └─ Tempo: 5 minutos ($0.46)

│

├── Generator Agent (construtor)

│   ├─ Constrói um sprint por vez

│   ├─ Lê e escreve state files continuamente

│   ├─ Sem resets de contexto (modelo Opus 4.6)

│   └─ Tempo: \~90 min por sprint

│

└── Evaluator Agent (crítico)

    ├─ Executa o áudio gerado

    ├─ Testa interações do usuário

    ├─ Avalia contra rubrica

    └─ Tempo: 5–10 min por sprint

---

## Arquitetura de State Persistence

A grande inovação deste caso é o uso de arquivos JSON como fonte de verdade compartilhada entre agentes:

project-files/

│

├── state.json                    \# Estado central do projeto

│   {

│     "project\_name": "Summer Song",

│     "bpm": 120,

│     "tracks": \[

│       {"id": "synth1", "notes": \[...\]},

│       {"id": "drums", "notes": \[...\]}

│     \],

│     "timeline\_length": 8

│   }

│

├── generator\_progress.md         \# Progresso em tempo real

│   "Construindo: Synth controls"

│   "Concluído: Timeline UI, Note entry"

│   "Próximo: Audio playback"

│

├── evaluator\_findings.md         \# Findings do Evaluator

│   "Sprint 1 Results:"

│   "✓ Timeline renderiza 8 compassos"

│   "✗ Notas não sincronizam com playback"

│   "→ Recomendação: Implementar audio clock"

│

└── audit\_log.json                \# Log imutável de mudanças

    \[timestamps de cada alteração de estado\]

**Por que arquivos e não variáveis em memória?** Agentes não compartilham memória entre chamadas. Arquivos são o único canal confiável de comunicação entre agentes independentes — persistem entre sessões, sobrevivem a falhas e criam um audit trail natural.

---

## Sprint Plan (Gerado pelo Planner)

Sprint 1: Timeline UI \+ Note Entry (2h 7min)

  ├─ Componentes: Timeline bar, note grid, input

  ├─ Stack: React \+ Web Audio API

  └─ Contrato: Usuário consegue inserir notas na grid

Sprint 2: Synth Controls \+ Knobs (45min)

  ├─ Componentes: Oscillator controls, envelope

  ├─ Estado: Parâmetros salvos em state.json

  └─ Contrato: Mudanças no synth afetam o som em tempo real

Sprint 3: Recording \+ Playback Sync (45min)

  ├─ Componentes: Record button, playback engine

  ├─ Desafio: Sincronizar audio clock com visual timeline

  └─ Contrato: Playback renderiza exatamente o que foi gravado

---

## Resultados com Breakdown de Custo

Runtime total: 3 horas 50 minutos

Custo total:   $124.70

Breakdown por fase:

├─ Planner:                      5 min    ($0.46)

├─ Generator Sprint 1:          2h 7min   ($71.08)

├─ Evaluator Sprint 1:          8.8 min   ($3.24)

├─ Generator Sprint 2:         45 min     ($25.00)

├─ Evaluator Sprint 2:          5 min     ($1.50)

├─ Generator Sprint 3:         45 min     ($23.00)

└─ Evaluator Sprint 3:          5 min     ($1.42)

Output final:

✓ Timeline editor completo

✓ Synth controls com knobs

✓ Funcionalidade de gravação

✓ Playback com sincronização

✓ UI polida e responsiva

✓ Handles real music workflows

---

## Padrões-Chave Utilizados

1. **Multi-Agent Coordination:** Planner → Generator → Evaluator com responsabilidades claras  
2. **File-Based State:** JSON files persistem estado entre sessões e agentes  
3. **Continuous Build:** Opus 4.6 habilita build de 2+ horas sem reset de contexto  
4. **Progressive Evaluation:** Cada sprint avaliado antes do próximo começar  
5. **Harness Simplification:** Modelo mais capaz reduz overhead de orquestração

---

## Lições Aprendidas

1. **State files são poderosos:** Serialização JSON previne bloat de contexto e cria rastreabilidade  
2. **Continuous build funciona:** Modelos de última geração suportam builds de 2+ horas  
3. **Qualidade melhora com iteração:** Passar por múltiplos sprints gera sistemas coerentes  
4. **Features emergentes:** O Generator adicionou capacidades não previstas no spec original  
5. **Naming é arquitetura:** Bons nomes de arquivo previnem confusão de estado entre agentes

---

## Aplicação no KODA

O padrão DAW mapeia elegantemente para os sistemas do KODA:

| Conceito DAW | Conceito KODA |
| :---- | :---- |
| Timeline | Histórico de conversa (sequencial) |
| Synth controls | Catálogo de produtos (opções configuráveis) |
| Recording | Histórico de pedidos (o que aconteceu) |
| Playback | Replay de conversa (verificação de precisão) |
| state.json | session\_state.json (estado da conversa) |
| audit\_log.json | order\_audit.json (rastreabilidade de pedidos) |

---

---

# Estudo de Caso 3 (KODA): Product Discovery

**Nível de Complexidade:** Nível 2–3  
**Foco:** Generator/Evaluator para qualidade de recomendação  
**Contexto:** Vendas via WhatsApp de suplementos esportivos

---

## Problema

O KODA precisa recomendar produtos que simultaneamente:

1. Correspondam à necessidade real do cliente  
2. Estejam em estoque no momento da conversa  
3. Ofereçam valor genuíno (preço, promoção, adequação)  
4. Sejam apresentados com clareza e persuasão

**Cenário real:** Cliente envia no WhatsApp: *"Estou treinando para uma maratona e preciso de nutrição"*

Com um agente único, 25% das recomendações tinham algum problema — produto fora de estoque, preço desatualizado, ou escolha inadequada para o nível do atleta.

---

## Solução: Generator/Evaluator com Rubrica

GENERATOR (Recomendador de Produtos)

│

├─ Input: Contexto do cliente (treino de maratona)

├─ Processo:

│   ├─ Consulta base de produtos via API

│   ├─ Filtra por categoria (nutrição esportiva)

│   ├─ Cruza com nível do cliente (amador/avançado)

│   ├─ Verifica estoque em tempo real

│   └─ Aplica promoções ativas do clube

│

├─ Output: 3 recomendações estruturadas

│   Exemplo: "Mix de carbo-loading \- 5kg \- R$175 (era R$250)"

│            "Gel energético isotônico \- pack 24 \- R$89"

│            "Proteína de recuperação \- 2kg \- R$199"

│

└─ Sem verificação própria — confia no Evaluator

EVALUATOR (QA de Recomendações)

│

├─ Verifica cada recomendação do Generator:

│   ├─ Produto existe? (valida SKU na base)

│   ├─ Preço correto? (checa promoção em tempo real)

│   ├─ Em estoque? (confirma inventário atual)

│   ├─ Relevante para o objetivo? (avalia coerência)

│   └─ O cliente ficaria satisfeito? (assessment de valor)

│

├─ Rubrica de avaliação:

│   ├─ Relevância para o objetivo: 8/10 ✓

│   ├─ Valor percebido do preço: 9/10 ✓

│   ├─ Clareza da explicação: 7/10 (pode melhorar)

│   └─ Score geral: 8/10 → Aprovado

│

└─ Se problema encontrado: Devolve ao Generator com feedback específico

SPRINT CONTRACT

"O Generator recomendará produtos que:

  1\. Apoiem diretamente o objetivo declarado

  2\. Estejam em estoque agora (verificação ao vivo)

  3\. Tenham preço com margem de ±5% do valor promocional atual

  4\. Incluam explicação clara do motivo da recomendação

  

  O Evaluator verificará os 4 critérios antes de aprovar.

  Itens reprovados retornam ao Generator com feedback específico."

---

## Arquitetura de Dados

recommendation-state/

│

├── customer\_context.json

│   {

│     "customer\_id": "wa\_5511999999999",

│     "goal": "marathon\_training",

│     "level": "intermediate",

│     "club\_member": true,

│     "purchase\_history": \["whey\_protein", "creatine"\]

│   }

│

├── generator\_draft.json

│   {

│     "recommendations": \[

│       {

│         "sku": "CARBO-001",

│         "name": "Mix Carbo-Loading 5kg",

│         "price": 175.00,

│         "promo\_price": 175.00,

│         "rationale": "Alta densidade energética para long runs"

│       }

│     \],

│     "draft\_timestamp": "2026-05-23T10:30:00Z"

│   }

│

└── evaluator\_verdict.json

    {

      "verdict": "approved",

      "scores": {"relevance": 8, "price": 9, "clarity": 7},

      "overall": 8,

      "notes": "Aumentar explicação sobre timing de consumo"

    }

---

## Resultados

ANTES (Agente Único):

├─ Tempo de resposta: 2–5 minutos

├─ Precisão: 75% (às vezes estoque errado)

├─ Qualidade: Variada (algumas recomendações mediocres)

└─ Satisfação do cliente: 70%

DEPOIS (Generator/Evaluator):

├─ Tempo de resposta: 3–5 minutos (overhead pequeno)

├─ Precisão: 98% (Evaluator captura problemas)

├─ Qualidade: 92% (rubrica garante padrão)

└─ Satisfação do cliente: 88%

---

## Métricas de Impacto

Melhorias operacionais:

├─ Precisão de estoque: 75% → 98%

├─ Recomendações erradas: 20% → 2%

├─ Satisfação do cliente: 70% → 88%

├─ Taxa de recompra: 35% → 52%

└─ Taxa de devolução: 15% → 6%

Impacto financeiro:

├─ Custo adicional: \+15% (2 chamadas de API ao invés de 1\)

├─ Latência adicionada: \+1–2 segundos

├─ Impacto na receita: \+52% recompras \= \+30% receita

└─ ROI: 2x custo → 30x benefício

O trade-off é claro: pagar 15% a mais em custo de modelo para obter 30x de retorno em receita recorrente.

---

## Padrões-Chave Utilizados

1. **Generator/Evaluator:** Separação entre geração e verificação de qualidade  
2. **Rubric Design:** Grades objetivos e subjetivos com pesos claros  
3. **Sprint Contracts:** Define explicitamente o que "boa recomendação" significa  
4. **Trace Reading:** Debug estruturado quando recomendações falham  
5. **Real-time Verification:** Evaluator sempre consulta inventário ao vivo

---

## Lições Aprendidas

1. **Separação funciona:** O Evaluator captura erros que o Generator ignora  
2. **Rubricas habilitam escala:** Critérios claros \= qualidade consistente sem supervisão humana  
3. **Pequeno custo, grande benefício:** \+15% custo → \+30% receita  
4. **Confiança via verificação:** Clientes confiam em recomendações verificadas  
5. **Padrões são universais:** O mesmo padrão Generator/Evaluator serve para múltiplas features

---

---

# Estudo de Caso 4 (KODA): Order Processing

**Nível de Complexidade:** Nível 3  
**Foco:** Sprint Contracts para workflows multi-step  
**Contexto:** Processamento de pedidos com preço de clube e fulfillment same-day

---

## Problema

O processamento de pedidos do KODA é intrinsecamente complexo — 6 etapas sequenciais com dependências críticas entre si:

1. Validar cliente (membro ativo? pagamento cadastrado?)  
2. Verificar inventário (disponível? reservar unidades?)  
3. Calcular preço (desconto de clube \+ bulk \+ promoções)  
4. Aplicar promoções (sem double-discount)  
5. Processar pagamento (cobrar valor correto uma única vez)  
6. Agendar fulfillment (same-day ou agendado)

Com um agente único, \~5% dos pedidos apresentavam erros — preço errado, cobranças duplicadas, endereço incorreto. Cada erro custava tempo de suporte, reembolsos e erosão de confiança do cliente.

---

## Solução: Sprint Contracts Multi-Step

Cada etapa do processamento foi modelada como um sprint independente, com contrato explícito de input/output:

SPRINT 1 — Validar Cliente

Contrato: "Recebe customer\_id → retorna {valid: bool, customer\_data: {...}}"

Generator: Consulta base de clientes

Evaluator: Verifica existência, status ativo, pagamento cadastrado

Teste: 10 IDs reais e fictícios

Critério de aprovação: 100% de precisão (zero falsos positivos)

SPRINT 2 — Verificar Inventário

Contrato: "Recebe \[sku\] → retorna \[{sku, qty\_available, reserved: bool}\]"

Generator: Consulta inventário em tempo real

Evaluator: Verifica quantidades, reserva itens, trata race conditions

Teste: Pedidos concorrentes, cenários de estoque baixo

Critério: Race conditions tratadas, reserva atômica

SPRINT 3 — Calcular Preço

Contrato: "Recebe {customer, items} → retorna {subtotal, discounts, total}"

Generator: Aplica preço de clube, desconto por volume, promoções

Evaluator: Verifica matemática, confere termos da promoção, previne double-discount

Teste: Edge cases (promos expiradas, descontos conflitantes)

Critério: Zero erros de arredondamento, sem double-discount

SPRINT 4 — Processar Pagamento

Contrato: "Recebe {customer, total} → retorna {success: bool, transaction\_id: str}"

Generator: Chama API de pagamento

Evaluator: Verifica transação, checa duplicatas, grava recibo

Teste: Flows reais de pagamento, tratamento de erros

Critério: Idempotência garantida (nunca cobrar duas vezes)

SPRINT 5 — Agendar Fulfillment

Contrato: "Recebe {order\_id, address} → retorna {tracking\_id, eta}"

Generator: Contata sistema de fulfillment, agenda entrega

Evaluator: Verifica endereço válido, ETA razoável, confirmação completa

Teste: Same-day delivery, localizações extremas

Critério: ETA realista, tracking ativo em \< 60 segundos

---

## State Persistence por Pedido

// order-state/order\_12345.json

{

  "customer\_id": "cust\_999",

  "items": \[

    {"sku": "WHEY-001", "qty": 2, "price": 89.90},

    {"sku": "CARBO-001", "qty": 1, "price": 175.00}

  \],

  "validations": {

    "customer\_valid": true,

    "inventory\_reserved": true,

    "price\_calculated": true,

    "payment\_processed": true,

    "fulfillment\_scheduled": true

  },

  "financials": {

    "subtotal": 354.80,

    "club\_discount": \-35.48,

    "promo\_discount": \-17.50,

    "total": 301.82

  },

  "status": "confirmed",

  "created": "2026-05-23T10:30:00Z",

  "tracking\_id": "TRK-789456",

  "eta": "2026-05-23T16:00:00Z"

}

// order-state/order\_audit.log

2026-05-23T10:30:00Z \- Pedido criado (wa\_5511999999999)

2026-05-23T10:30:15Z \- Cliente validado (cust\_999, membro ativo)

2026-05-23T10:30:45Z \- Inventário reservado (WHEY-001 x2, CARBO-001 x1)

2026-05-23T10:31:00Z \- Preço calculado (R$354.80 → R$301.82 com descontos)

2026-05-23T10:31:30Z \- Pagamento processado (txn\_abc123, R$301.82)

2026-05-23T10:32:00Z \- Fulfillment agendado (TRK-789456, ETA 16h00)

O audit log é fundamental: quando um pedido falha, sabe-se exatamente em qual sprint e por quê.

---

## Resultados

ANTES (Agente Único):

├─ Precisão do pedido: 95% (5% com erros)

├─ Breakdown de erros:

│   ├─ Preço errado:       2%

│   ├─ Cobranças duplas:   1%

│   ├─ Endereço errado:    1%

│   └─ Não fulfillado:     1%

├─ Reclamações de clientes: Alto

└─ Taxa de revisão manual: 10%

DEPOIS (Sprint Contracts):

├─ Precisão do pedido: 99.8% (0.2% com erros)

├─ Breakdown de erros:

│   ├─ Preço errado:       0.05%

│   ├─ Cobranças duplas:   0%

│   ├─ Endereço errado:    0.1%

│   └─ Não fulfillado:     0.05%

├─ Reclamações de clientes: Redução de 80%

└─ Taxa de revisão manual: 1%

---

## Padrões-Chave Utilizados

1. **Sprint Contracts:** Critérios de aceitação claros por etapa — sem ambiguidade  
2. **State Persistence:** Rastreamento do pedido através das 6 etapas via JSON  
3. **Multi-Agent:** Cada sprint é um subprocesso isolado  
4. **Evaluation Layer:** Verificação antes de prosseguir para a próxima etapa  
5. **Error Localization:** Falha em sprint específico \= localização imediata do problema

---

## Lições Aprendidas

1. **Contratos previnem erros:** Definições claras de input/output eliminam ambiguidade  
2. **State tracking é crítico:** Sempre saber exatamente em que etapa o pedido está  
3. **Fail early é mais seguro:** Melhor rejeitar na Sprint 1 do que processar dados ruins  
4. **Camadas de validação funcionam:** Cada sprint verifica o trabalho do anterior  
5. **Audit trail é obrigatório:** Recuperação de falhas requer saber o que aconteceu quando

---

---

# Estudo de Caso 5 (KODA): Fulfillment & Same-Day Delivery

**Nível de Complexidade:** Nível 4  
**Foco:** State Persistence complexo · Coordenação multi-agente · Operação contínua  
**Contexto:** KODA promete entrega no mesmo dia como diferencial competitivo

---

## Problema

A promessa de same-day delivery é um diferencial crítico do KODA — e também seu desafio operacional mais complexo. Cada entrega requer:

1. Coordenação com o estoque do armazém  
2. Verificação de packing correto  
3. Atribuição de motorista disponível  
4. Otimização de rota em tempo real  
5. Atualizações contínuas ao cliente  
6. Confirmação de entrega com assinatura/foto

Tudo isso deve acontecer em horas, com alta confiabilidade, para dezenas de pedidos simultâneos. Um sistema manual ou de agente único não escala nem garante a consistência necessária.

---

## Solução: 3-Agent System com Persistent State

AGENT 1 — Logistics Planner

├─ Execução: A cada 30 minutos (de 6h às 18h)

├─ Input: Pedidos do dia \+ motoristas disponíveis \+ mapa de tráfego

├─ Processo: Otimização de rotas, balanceamento de carga por motorista

├─ Output: fulfillment\_plan.json (atualizado a cada ciclo)

└─ Custo: $0.15 por execução, 2 minutos de runtime

AGENT 2 — Fulfillment Executor

├─ Execução: Contínua das 6h às 20h (14 horas de runtime)

├─ Input: fulfillment\_plan.json (lido a cada 5 min)

├─ Processo: Coordena armazém, despacha motoristas, envia updates aos clientes

├─ Output: fulfillment\_status.json (atualizado a cada 5 min)

└─ Custo: $1.20/hora → \~$16.80/dia

AGENT 3 — Quality Verifier

├─ Execução: Spot checks durante o dia \+ relatório final às 20h

├─ Input: fulfillment\_status.json \+ feedback de clientes

├─ Processo: Verifica amostra de 10% das entregas, captura anomalias

├─ Output: verification\_report.json

└─ Custo: $0.80/dia (spot checks \+ EOD report)

---

## State Files — Fonte de Verdade Distribuída

// fulfillment-state/fulfillment\_plan.json (atualizado a cada 30 min)

{

  "timestamp": "2026-05-23T08:00:00Z",

  "orders\_to\_fulfill": 47,

  "drivers\_available": 8,

  "routes": \[

    {

      "driver\_id": "drv\_001",

      "driver\_name": "Carlos Silva",

      "orders": \["ord\_123", "ord\_124", "ord\_125"\],

      "estimated\_time\_minutes": 90,

      "stops": 3,

      "zone": "Pinheiros"

    },

    {

      "driver\_id": "drv\_002",

      "orders": \["ord\_126", "ord\_127", "ord\_128", "ord\_129"\],

      "estimated\_time\_minutes": 110,

      "stops": 4,

      "zone": "Vila Madalena"

    }

  \]

}

// fulfillment-state/fulfillment\_status.json (atualizado a cada 5 min — LIVE)

{

  "timestamp": "2026-05-23T14:30:00Z",

  "orders\_progress": {

    "ord\_123": {

      "status": "delivered",

      "delivered\_at": "2026-05-23T11:15:00Z",

      "signature": "verified",

      "customer\_rating": 5

    },

    "ord\_126": {

      "status": "in\_transit",

      "driver": "drv\_002",

      "current\_stop": 2,

      "eta": "2026-05-23T15:00:00Z",

      "customer\_notified": true,

      "last\_update": "2026-05-23T14:25:00Z"

    },

    "ord\_131": {

      "status": "issue\_detected",

      "issue": "Endereço não localizado",

      "agent\_action": "Contacting customer via WhatsApp",

      "resolution\_eta": "2026-05-23T15:30:00Z"

    }

  }

}

// fulfillment-state/verification\_report.json (EOD)

{

  "date": "2026-05-23",

  "orders\_fulfilled": 47,

  "on\_time": 46,

  "late": 1,

  "quality\_score": 98,

  "issues\_detected": \[

    {

      "order\_id": "ord\_999",

      "issue": "Endereço inicial incorreto",

      "resolution": "Corrigido via agente, re-roteado em 8 min",

      "impact": "Atraso de 15 min — still same-day"

    }

  \],

  "learnings\_for\_tomorrow": \[

    "Zona Sul: tráfego pesado às 17h — alocar 15min extra",

    "Motorista drv\_003: rota otimizada renderizou 2 paradas extras"

  \]

}

---

## Fluxo de Coordenação em Tempo Real

06:00 — Planner acorda

        Lê: Pedidos confirmados desde 20h (ontem) \+ novos pedidos da madrugada

        Processa: Otimização de rotas para 8 motoristas, 47 pedidos

        Escreve: fulfillment\_plan.json

        Custo: $0.15, 2 minutos

06:30 — Executor inicia operação

        Lê: fulfillment\_plan.json

        Despacha: Notificações ao armazém, briefing dos motoristas

        Monitora: Status de packing (ETA 08:00 para maioria)

08:00 — Motoristas partem

        Executor atualiza: fulfillment\_status.json a cada 5 min

        Envia: Updates de ETA ao cliente via WhatsApp

        Trata: Anomalias em tempo real (endereço errado, cliente ausente)

10:00 — Verifier faz primeiro spot check

        Amostra: 5 entregas aleatórias (10% do total)

        Verifica: Produto correto? Condição do pacote? Cliente satisfeito?

        Grava: Findings parciais em verification\_report.json

14:00 — Planner re-executa (ciclo de 30 min)

        Re-otimiza: Rotas com base em tráfego atual

        Reatribui: Pedidos de motoristas com atraso para outros disponíveis

20:00 — Executor encerra operação

        Status final: 47/47 pedidos processados

        Verifier: Gera relatório EOD completo

        Planner: Lê learnings para ajustar amanhã

---

## Resultados

ANTES (Manual \+ Agente Único):

├─ Pedidos fulfillados same-day: 85%

├─ Entregas com atraso: 12%

├─ Endereço errado: 3%

├─ Satisfação do cliente: 72%

└─ Trabalho manual: \~30 horas/dia de operação

DEPOIS (3-Agent System \+ State Persistence):

├─ Pedidos fulfillados same-day: 99.5%

├─ Entregas com atraso: 1%

├─ Endereço errado: 0.1%

├─ Satisfação do cliente: 94%

└─ Trabalho manual: \~2 horas/dia (apenas exceções críticas)

---

## Padrões-Chave Utilizados

1. **Planner/Executor/Verifier:** Separação clara de concerns estratégicos, operacionais e de qualidade  
2. **Persistent State:** JSON files como única fonte de verdade — sobrevivem a falhas de agente  
3. **Real-Time Updates:** fulfillment\_status.json atualizado a cada 5 minutos  
4. **Continuous Operation:** Executor roda 14+ horas com suporte a compaction  
5. **Verification Loop:** Spot checks capturam problemas sem verificar tudo (eficiência)  
6. **Learning Loop:** Relatório EOD alimenta otimizações do dia seguinte

---

## Lições Aprendidas

1. **Persistent state é inegociável:** Não se pode perder o rastro de pedidos em trânsito  
2. **Real-time updates importam:** Clientes informados aceitam pequenos atrasos com muito mais tolerância  
3. **Operação contínua é viável:** Agentes com compaction suportam 12+ horas sem degradação  
4. **Spot verification é suficiente:** Verificar 10% captura \>85% dos problemas sistêmicos  
5. **Learning loop amplifica valor:** Cada dia o sistema fica marginalmente melhor  
6. **Custo não cresce linearmente:** 47 pedidos custam apenas 20% mais que 10 — escala favorável

---

## Custo Total de Operação por Dia

Agent 1 (Planner):     24 execuções × $0.15 \= $3.60/dia

Agent 2 (Executor):    14 horas × $1.20    \= $16.80/dia

Agent 3 (Verifier):    Spot checks \+ EOD   \= $0.80/dia

                                             ─────────

TOTAL:                                       $21.20/dia

Com 47 pedidos/dia:    $0.45 por pedido

Margem adicional:      Bem abaixo do custo de um erro (\~$30 em suporte/reembolso)

ROI do sistema:        \~66x (custo de erro prevenido vs. custo do agente)

---

# Sumário Comparativo

| Estudo de Caso | Padrão Principal | Complexidade | ROI Estimado |
| :---- | :---- | :---- | :---- |
| Retro Game Maker | Planner \+ Sprint Contracts | Nível 2–3 | Viabilidade (projeto concluído vs. falha) |
| Browser DAW | File-Based State \+ Continuous Build | Nível 3–4 | $124 em valor entregue |
| KODA Product Discovery | Generator/Evaluator | Nível 2–3 | 2x custo → 30x receita |
| KODA Order Processing | Multi-Step Sprint Contracts | Nível 3 | 80% redução em reclamações |
| KODA Fulfillment | 3-Agent \+ Persistent State | Nível 4 | 66x ROI por pedido |

---

## Princípios Unificadores

Todos os 5 casos compartilham três verdades fundamentais:

**1\. Separação de concerns supera o agente onisciente** Especialização é mais confiável que generalização. Planner pensa, Generator executa, Evaluator verifica. Cada agente faz uma coisa bem.

**2\. Estado persistido é a memória do sistema** Agentes não têm memória entre chamadas — arquivos têm. JSON files bem nomeados são a cola que transforma agentes isolados em sistemas coerentes.

**3\. Contratos claros produzem qualidade previsível** "Done" precisa ser definido antes de começar. Sprint contracts, rubricas e critérios de aceitação eliminam ambiguidade e permitem escala sem supervisão constante.

---

*Documento gerado para o time técnico FutanBear | KODA Project | v1.0 | Mai 2026*  
