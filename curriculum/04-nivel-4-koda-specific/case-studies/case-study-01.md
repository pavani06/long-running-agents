---
title: "Case Study: Lançamento do KODA Same-Day Delivery"
type: curriculum-case-study
nivel: 4
aliases: []
tags: [curriculo-conteudo, nivel-4, caso-de-estudo, entrega-no-mesmo-dia, coordenacao-logistica, reserva-de-estoque, roteamento-e-eta, lock-files, state-persistence, rubricas-de-evaluacao, recuperacao-de-incidente, deploy-gradual, adr-arquitetural]
relates-to: ["[[curriculum/04-nivel-4-koda-specific/01-koda-architecture|KODA Architecture]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]"]
last_updated: 2026-06-10
---
# 🚀 Case Study: Lançamento do KODA Same-Day Delivery
## Como Padrões de Long-Running Agents Transformaram uma Promessa Arriscada em Vantagem Competitiva

**Tempo Estimado:** 90-120 minutos
**Nível:** 4 - KODA-Específico
**Pré-requisitos:** Ter completado Nível 1, Nível 2, Nível 3 e os módulos 01-03 do Nível 4
**Status:** ✅ COMPLETO - Case study de referência para implementação de features KODA
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Promessa que Quase Quebrou o KODA

Quarta-feira, 14h30. Sala de reunião principal da KODA.

Fernando estava de pé diante do quadro branco, um marcador vermelho na mão. Ao redor da mesa, o time de produto, engenharia e operações. A tensão era palpável.

No centro da mesa, um print de WhatsApp:

```
Cliente: "KODA, você prometeu que meu pedido chegaria hoje às 16h.
         São 19h e nada. Cancelei meu compromisso pra receber.
         Isso é a terceira vez esse mês. Não dá mais."
```

Fernando olhou para o time:
> *"Same-day delivery era nossa maior vantagem competitiva. Em 6 meses, virou nossa maior fonte de reclamações. O que aconteceu?"*

O silêncio durou 10 segundos.

A Diretora de Operações respondeu primeiro:
> *"Fernando, temos 3 armazéns, 12 entregadores parceiros, 5 regiões de entrega. O sistema atual simplesmente não consegue coordenar tudo isso em tempo real. Quando o cliente pergunta 'vai chegar hoje mesmo?', o KODA responde com base em estimativas de ontem."*

O Tech Lead completou:
> *"O problema é mais profundo. O KODA não tem como saber, em tempo real, se um entregador está disponível, se o armazém certo tem estoque, ou se a rota é viável. Cada parte do sistema opera isolada. E quando uma parte falha, ninguém avisa as outras."*

Fernando escreveu três palavras no quadro:

```
SAME-DAY DELIVERY = COORDENAÇÃO
```

> *"É isso. Não é um problema de modelo. Não é um problema de prompt. É um problema de coordenação entre agentes, estado e decisões em tempo real. Exatamente o que os padrões de long-running agents resolvem."*

Foi nesse momento que nasceu o projeto mais ambicioso da história do KODA: **refatorar o sistema de same-day delivery usando padrões de long-running agents de Nível 1 a Nível 4.**

Este case study documenta essa jornada. Do diagnóstico inicial ao rollout em produção. Das falhas do MVP à arquitetura final. Das métricas de antes às métricas de depois. E das lições que mudaram para sempre como o time KODA pensa sobre features complexas.

Se você quer entender como padrões de long-running agents se aplicam a um problema real — com prazos, pressão de negócio, clientes reais e sistemas legados — você está no lugar certo.

---

## 🎯 Objetivos Deste Case Study

Ao final deste case study, você será capaz de:

- ✅ **Diagnosticar um problema de coordenação multi-agente** usando os conceitos dos 4 níveis do programa
- ✅ **Desenhar uma arquitetura de agentes para coordenação em tempo real** com persistência de estado, file-based coordination e multi-agent orchestration
- ✅ **Aplicar Generator/Evaluator, Sprint Contracts e Rubric Design** em um cenário de negócio real com restrições de latência e confiabilidade
- ✅ **Implementar file-based coordination com lock files, status files e audit trail** para impedir conflitos entre agentes concorrentes
- ✅ **Comparar estratégias de coordenação** (centralizada, descentralizada, híbrida) e escolher a adequada para cada contexto
- ✅ **Medir impacto de mudanças arquiteturais** com métricas de antes/depois, análise de custo e ROI
- ✅ **Extrair lições transferíveis** que se aplicam a qualquer feature complexa do KODA

---

## 📊 Contexto do Problema: O Cenário Antes da Refatoração

### O KODA em Números (Dezembro 2025)

Antes do projeto de refatoração, o KODA operava com um sistema de fulfillment simplificado:

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Pedidos diários** | 340 | Volume médio de pedidos por dia |
| **Pedidos com same-day** | 120 (35%) | Clientes que escolhem entrega no mesmo dia |
| **Taxa de sucesso same-day** | 62% | Pedidos que realmente chegaram no mesmo dia |
| **Atrasos médios** | 3.2 horas | Tempo médio de atraso quando falha |
| **Reclamações same-day** | 18/dia | Reclamações específicas sobre atraso na entrega |
| **Cancelamentos pós-atraso** | 8/dia | Clientes que cancelam após atraso |
| **Churn por insatisfação** | 12/clientes/mês | Clientes que abandonam KODA por falhas de entrega |
| **Custo operacional** | R$ 4.200/dia | Custo de entregadores, rotas, reprocessamento |

Traduzindo em impacto de negócio:

- **Receita perdida por cancelamentos:** R$ 2.880/dia (8 cancelamentos × R$ 360 ticket médio)
- **Receita perdida por churn:** R$ 4.320/mês recorrente
- **Custo de suporte para reclamações:** R$ 540/dia (18 reclamações × R$ 30/cada)
- **Dano de reputação:** Avaliação do KODA no WhatsApp Business caiu de 4.7 para 4.1 em 3 meses

**Total de perda mensal estimada:** ~R$ 111.600

### A Arquitetura Original (Dezembro 2025)

O sistema de same-day delivery funcionava assim:

```
┌─────────────────────────────────────────────────────────────┐
│                 ARQUITETURA ORIGINAL                         │
│                 (Dezembro 2025)                              │
└─────────────────────────────────────────────────────────────┘

CLIENTE (WhatsApp)
       │
       ▼
┌──────────────────────┐
│    KODA (Agente      │
│    Único)            │
│                      │
│  Faz TUDO:           │
│  - Atende cliente    │
│  - Verifica estoque  │
│  - Calcula frete     │
│  - Promete entrega   │
│  - Confirma pedido   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  API de Logística    │
│  (REST)              │
│                      │
│  Consulta estática:  │
│  - Armazem X tem Y?  │
│  - Entregador Z livre?│
│  - ETA estimado      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Sistema Legado de   │
│  Entregas            │
│                      │
│  - Planilha Excel    │
│  - Atualização 2x/dia│
│  - Sem real-time     │
└──────────────────────┘
```

### Os 4 Pontos de Falha do Sistema Original

#### Ponto de Falha 1: Informação Desatualizada (Context Amnesia Estrutural)

O KODA consultava a API de logística no momento do pedido. Mas o estoque real e a disponibilidade de entregadores mudavam **minutos depois**. Quando o pedido chegava no armazém (30-60 minutos depois), o produto podia já ter sido vendido para outro cliente, ou o entregador podia já estar em outra rota.

```
Timeline Típica de Falha:

14:00 - Cliente pergunta: "Tem whey isolate em estoque? Chega hoje?"
14:01 - KODA consulta API: "Sim, 12 unidades no Armazem SP-ZL"
14:02 - KODA promete: "Sim! Chega hoje até 18h!"
14:03 - Cliente compra
14:30 - Pedido chega no armazem: 0 unidades (vendidas para loja física)
14:31 - Sistema legado: sem alerta automático
16:00 - Cliente pergunta: "Cadê meu pedido?"
16:01 - KODA: "Hmm... deixa eu verificar..."
```

**Raiz do problema:** O KODA não mantinha estado persistente. Cada consulta era stateless. A promessa de entrega era baseada em um snapshot que expirava em minutos.

#### Ponto de Falha 2: Coordenação Inexistente entre Componentes

O sistema tinha 4 componentes que nunca se comunicavam diretamente:

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  CATÁLOGO    │   │   ESTOQUE    │   │ ENTREGADORES │   │   ROTAS      │
│  (o que      │   │  (quantos    │   │  (quem está  │   │  (qual o      │
│   vender)    │   │   temos)     │   │   livre)     │   │   trajeto)    │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
       │                  │                  │                  │
       └──────────────────┴──────────────────┴──────────────────┘
                                  │
                          KODA consultava
                          cada um isoladamente
                          (sem coordenação)

Resultado comum:
- Catálogo: "Whey Isolado SP-ZL disponível" ✅
- Estoque: "12 unidades" ✅
- Entregadores: "João livre às 15h" ✅
- Rotas: "SP-ZL → Cliente = 45 min" ✅

Mas na realidade:
- Whey Isolado estava em SP-ZL mas o cliente estava em SP-Moema (outra zona)
- João estava livre mas tinha restrição de peso (máx 10kg, pedido tinha 12kg)
- Rota de 45min era sem trânsito (horário de pico = 90min)

NENHUM componente validava os outputs dos outros.
```

#### Ponto de Falha 3: Ausência de Feedback Loop

Quando uma entrega falhava, ninguém sabia exatamente por quê:

```
Ciclo de Falha sem Aprendizado:

1. Entrega atrasa
2. Cliente reclama
3. Suporte pede desculpas e oferece cupom
4. Ninguém investiga a causa raiz
5. Sistema continua igual
6. Próximo cliente sofre a mesma falha
7. Volta ao passo 1

Em 6 meses: 340+ falhas de same-day.
Causas documentadas: 12.
Padrões identificados: 0.
Melhorias implementadas: 0.
```

#### Ponto de Falha 4: O KODA Mentia sem Saber

O aspecto mais preocupante: o KODA, como agente único, **não tinha como saber que suas promessas eram falsas**. Ele consultava a API, recebia uma resposta positiva, e respondia com confiança. Não havia um Evaluator para verificar se a promessa era realista.

```
Conversa Real (Janeiro 2026):

Cliente: "KODA, se eu comprar agora, chega hoje?"
KODA: "Sim! Seu pedido chega até 18h. Pode confiar!"
       [KODA consultou API às 15:30. API disse "estoque OK, entregador OK"]
       
Cliente: "Perfeito! Pode fazer o pedido."
KODA: "Pedido #8941 confirmado. Entrega até 18h."

[16:00 - Sistema legado atualiza: entregador João teve problema com a moto]
[16:30 - Armazém SP-ZL fecha mais cedo (feriado municipal)]
[17:00 - Cliente pergunta: "Cadê?"]
[17:01 - KODA: "Hmm... estamos verificando..."]
[18:00 - KODA: "Houve um imprevisto. Seu pedido chega amanhã."]

Cliente: "VOCÊ PROMETEU."
```

O KODA não estava mentindo intencionalmente. Ele simplesmente não tinha os padrões arquiteturais necessários para **saber que não sabia**.

---

## 🔍 Abordagem Inicial e Falhas Encontradas

### MVP1: O "Fast Check" (Janeiro 2026 - 2 semanas)

A primeira tentativa do time foi um **quick fix**: adicionar uma validação extra antes de prometer same-day delivery.

**Abordagem:**
```
KODA, antes de prometer "chega hoje", faz 3 consultas:
1. API de estoque (real-time?)
2. API de entregadores (real-time?)
3. API de rotas (real-time?)

Se as 3 retornarem OK → promete same-day
Se qualquer uma falhar → oferece entrega normal
```

**Por que falhou:**

1. **Latência inaceitável:** 3 chamadas API sequenciais = 4-7 segundos de espera. Cliente no WhatsApp espera resposta em < 2 segundos.

2. **Falso positivo:** As 3 APIs retornavam "OK" baseadas em cache de 5-15 minutos. O problema de dados desatualizados continuava.

3. **Sem estado:** Cada consulta era independente. Se a API de estoque dizia "sim" às 15:00 e a de entregadores dizia "sim" às 15:01 (baseada em cache das 14:55), não havia garantia de que ambos os "sim" se referiam ao mesmo momento.

4. **Custo aumentou 3x:** 3 chamadas API por pedido = custo operacional subiu de R$ 0.03 para R$ 0.09 por consulta. Para 120 pedidos/dia, R$ 10.80/dia adicionais sem melhora na taxa de sucesso.

**Resultado do MVP1:**
- Taxa de sucesso same-day: 62% → 64% (melhora marginal)
- Tempo de resposta: 2.1s → 5.8s (piora significativa)
- Custo por pedido: aumentou 3x
- Reclamações: continuaram iguais

**Lição:** Adicionar verificações sem mudar a arquitetura não resolve. O problema não era "número de verificações", era "arquitetura de coordenação".

### MVP2: O "Promise Keeper" (Fevereiro 2026 - 3 semanas)

A segunda tentativa foi mais ambiciosa: criar um sistema que **registrava** promessas e **verificava** depois.

**Abordagem:**
```
1. KODA promete same-day → registra em promessas.json
2. Um worker (cron job) roda a cada 15 minutos:
   - Lê todas as promessas ativas
   - Verifica se ainda são viáveis
   - Se alguma quebrou, alerta suporte
3. Suporte contata cliente proativamente
```

**Arquitetura do MVP2:**
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  KODA            │────▶│  promessas.json   │────▶│  Worker          │
│  (faz promessa)  │     │  (persistência)   │     │  (verifica a     │
│                  │     │                    │     │   cada 15 min)   │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                           │
                                                    ┌──────▼────────┐
                                                    │  Alerta        │
                                                    │  Suporte       │
                                                    │  (se quebrou)  │
                                                    └───────────────┘
```

**Por que falhou:**

1. **Janela de 15 minutos é uma eternidade:** Se o estoque acaba às 14:01 e o worker roda às 14:15, são 14 minutos de promessa falsa ativa. Nesse período, outros clientes podem receber a mesma promessa.

2. **Worker é single-point-of-failure:** Se o worker falha (e falhou, 3 vezes na primeira semana), as promessas não são verificadas e ninguém sabe.

3. **Alerta ao suporte não resolve o problema real:** O suporte recebia o alerta, mas não tinha poder de ação. Não podia magicamente fazer o produto aparecer no estoque ou o entregador ficar livre.

4. **Sem feedback para o KODA:** O worker detectava o problema, mas o KODA continuava fazendo as mesmas promessas. O aprendizado não voltava para o sistema.

5. **Novo problema: duplicação de esforço:** Quando o suporte recebia o alerta, tentava contatar o cliente. Mas o KODA também tentava (na conversa original). Cliente recebia mensagens duplicadas e contraditórias.

**Resultado do MVP2:**
- Taxa de sucesso same-day: 64% → 67% (melhora pequena)
- Alertas gerados: 40/dia
- Alertas que resultaram em ação efetiva: 8/dia (20%)
- Clientes que receberam mensagens duplicadas: 12/dia
- Custo de desenvolvimento: 3 semanas do time

**Lição:** Monitorar promessas é útil, mas só monitorar sem capacidade de **reação automática** é insuficiente. O sistema precisa não apenas detectar falhas, mas **corrigi-las** em tempo real.

### MVP3: O "Rerouter" (Março 2026 - 4 semanas)

A terceira tentativa introduziu um conceito novo: se o plano A falha, executa-se o plano B automaticamente.

**Abordagem:**
```
Quando uma promessa de same-day é detectada como quebrada:
1. Sistema busca alternativas automaticamente:
   - Outro armazém?
   - Outro entregador?
   - Outra rota?
2. Se encontrar alternativa, re-roteia automaticamente
3. Se não encontrar, alerta suporte
4. Atualiza KODA para avisar cliente (se necessário)
```

**Por que ainda não foi suficiente:**

1. **Re-roteamento é computacionalmente caro:** Buscar alternativas envolve consultar 3 armazéns × 12 entregadores × N rotas = explosão combinatória. O sistema levava 30-45 segundos para encontrar alternativa — tempo suficiente para o cliente desistir.

2. **Condição de corrida:** Enquanto o sistema busca alternativa para o Pedido A, o Pedido B pode "roubar" o estoque ou entregador que seria a alternativa. Sem locking, dois pedidos competem pelos mesmos recursos.

3. **Latência em cascata:** O re-roteamento do Pedido A atrasa o processamento do Pedido B, que por sua vez também precisa de re-roteamento. Efeito dominó.

4. **KODA não sabe o que dizer:** Quando o sistema re-roteia, o KODA precisa atualizar o cliente. Mas o KODA não tem contexto do que aconteceu. A mensagem ficava genérica: "Seu pedido foi atualizado" — sem explicar por quê.

**Resultado do MVP3:**
- Taxa de sucesso same-day: 67% → 72% (melhora moderada)
- Tempo médio de re-roteamento: 38 segundos
- Condições de corrida: 5-8/dia
- Clientes confusos com mensagens genéricas: 15/dia
- Custo computacional: +R$ 1.200/mês em infra

**Lição:** Re-roteamento reativo funciona, mas sem coordenação entre agentes e estado compartilhado, o sistema cria novos problemas (condições de corrida, latência em cascata, má comunicação).

---

## 🧠 Diagnóstico Arquitetural: Por que os MVPs Falharam

Após 3 MVPs e 9 semanas de desenvolvimento, Fernando convocou uma reunião de retrospectiva. O diagnóstico foi cristalino:

### Os 5 Problemas Arquiteturais Raiz

| # | Problema | Categoria (Nível) | MVP1 | MVP2 | MVP3 | Resolvido? |
|---|----------|-------------------|------|------|------|------------|
| 1 | **Estado não persiste** — dados críticos existem apenas em memória/RAM, desaparecem em restarts | State Persistence (N3) | ❌ | ⚠️ Parcial | ⚠️ Parcial | ❌ |
| 2 | **Agentes não coordenam** — múltiplos componentes tomam decisões conflitantes sobre os mesmos recursos | Multi-Agent Coordination (N3) | ❌ | ❌ | ❌ | ❌ |
| 3 | **Sem Generator/Evaluator** — KODA promete sem verificação independente, auto-avaliação é falha | Generator/Evaluator (N2) | ❌ | ❌ | ❌ | ❌ |
| 4 | **Sem Sprint Contracts** — cada componente espera inputs diferentes, ninguém valida outputs | Sprint Contracts (N2) | ❌ | ❌ | ❌ | ❌ |
| 5 | **Sem Trace Reading** — quando algo falha, ninguém consegue rastrear o caminho completo da decisão | Trace Reading (N2) | ❌ | ❌ | ❌ | ❌ |

### A Causa Raiz Única

Fernando resumiu em uma frase:

> *"Nós não tínhamos um problema de same-day delivery. Nós tínhamos um problema de **sistema que não foi projetado para coordenação multi-agente com estado compartilhado**. Same-day delivery é apenas o sintoma mais visível."*

O time percebeu que nenhum dos MVPs atacava a arquitetura. Eram patches. Remendos. Cada MVP resolvia um sintoma, mas a doença continuava.

Era hora de parar de remendar e **redesenhar a arquitetura do zero**, aplicando todos os padrões de long-running agents do programa.

### Retrospectiva Técnica: O Que Cada MVP Ensinou

Antes de desenhar a nova arquitetura, o time fez uma retrospectiva técnica detalhada. Cada MVP deixou uma lição específica que moldou o design final:

#### MVP1 ensinou: Latência e Consistência são Inimigas

```
Anatomia de uma promessa falsa no MVP1:

T0 (15:00:00) - Cliente pergunta "chega hoje?"
T1 (15:00:01) - API de estoque: "WHEY-001 tem 12 unidades" ✅
              (Mas esse dado é do cache das 14:55)
T2 (15:00:03) - API de entregadores: "Entregador-007 livre" ✅
              (Mas esse dado é do cache das 14:52)
T3 (15:00:06) - API de rotas: "SP-ZL → Moema = 38 min" ✅
              (Mas esse dado é do cache das 14:58)
T4 (15:00:07) - KODA responde: "Sim! Chega hoje!"

PROBLEMA: As 3 respostas "OK" pertencem a snapshots diferentes.
Nenhuma delas é do momento T0 (15:00:00).

O que realmente aconteceu:
- 14:57: Estoque real de WHEY-001 caiu para 0 (venda na loja física)
- 14:59: Entregador-007 aceitou outra entrega
- 15:00: Trânsito na Marginal Tietê piorou para severo

Nenhuma dessas mudanças foi detectada.
O cache mentiu para o KODA.
```

**Lição para a arquitetura final:** Estado precisa ser consultado em tempo real, com locks que garantem que a informação não muda entre a consulta e a ação. Cache é aceitável apenas com TTL < 60 segundos e invalidação automática.

#### MVP2 ensinou: Monitorar sem Agir é Inútil

```
Ciclo de vida de um alerta no MVP2:

14:00 - Promessa registrada: Pedido #8912, ETA 16:00
14:15 - Worker roda: 27 promessas ativas, todas OK
14:30 - Worker roda: 27 promessas ativas, todas OK
14:45 - Worker roda: Pedido #8912: estoque zerado! 🚨
         └─ Alerta enviado para equipe de suporte
14:46 - Suporte vê o alerta (1 minuto depois)
14:47 - Suporte abre o pedido no sistema legado
14:48 - Suporte confirma: estoque realmente zerado
14:49 - Suporte tenta contatar cliente: "Houve um imprevisto..."
14:50 - Cliente: "Mas o KODA prometeu!"

Tempo entre falha real (14:16) e ação (14:49): 33 minutos.
Nesses 33 minutos, o cliente confiou em uma promessa quebrada.
```

**Lição para a arquitetura final:** Detecção e reação precisam ser automáticas e instantâneas. O sistema precisa não apenas detectar falhas, mas corrigi-las sem intervenção humana. O papel do suporte deve ser exceção, não regra.

#### MVP3 ensinou: Condições de Corrida São Inevitáveis sem Coordenação

```
Cenário real de race condition no MVP3:

Situação: Apenas 1 unidade de CREATINE-001 no armazém SP-ZL

T0 (15:00:00.000) - Pedido #9001 inicia re-roteamento
T1 (15:00:00.500) - Pedido #9002 inicia re-roteamento

T2 (15:00:01.000) - #9001 consulta estoque: CREATINE-001 = 1 unidade ✅
T3 (15:00:01.200) - #9002 consulta estoque: CREATINE-001 = 1 unidade ✅
                   (nenhum dos dois reservou ainda!)

T4 (15:00:02.000) - #9001 decide: "Vou usar CREATINE-001"
T5 (15:00:02.100) - #9002 decide: "Vou usar CREATINE-001"

T6 (15:00:03.000) - #9001 reserva CREATINE-001 ✅
T7 (15:00:03.500) - #9002 tenta reservar CREATINE-001 ❌ (já foi!)

Resultado: #9002 precisa de um TERCEIRO re-roteamento.
Enquanto isso, o cliente do #9002 espera há 45 segundos.

Ambos os pedidos atrasam. Ambos os clientes ficam insatisfeitos.
```

**Lição para a arquitetura final:** Lock files são obrigatórios para qualquer recurso compartilhado. A consulta e a reserva precisam ser atômicas. O sistema precisa detectar e resolver contenção automaticamente.

#### Síntese: O Padrão que Emergiu das Falhas

Analisando as falhas dos 3 MVPs, o time identificou um padrão recorrente:

```
PADRÃO DE FALHA EM SISTEMAS NÃO-COORDENADOS:

1. MÚLTIPLOS TOMADORES DE DECISÃO
   Cada componente decide isoladamente, sem visão global
   
2. ESTADO INCONSISTENTE
   Decisões são baseadas em snapshots de momentos diferentes
   
3. AUSÊNCIA DE SERIALIZAÇÃO
   Sem locks, operações concorrentes se sobrepõem
   
4. REAÇÃO TARDIA
   Falhas são detectadas, mas a correção é lenta ou manual
   
5. RASTREABILIDADE ZERO
   Quando algo falha, ninguém sabe reconstruir o que aconteceu

TODOS os 3 MVPs exibem esse padrão em diferentes graus.
A nova arquitetura precisa quebrar CADA um desses 5 pontos.
```

---

## 🏗️ A Solução Final: Arquitetura Baseada em Padrões de Long-Running Agents

### Princípios de Design

O redesign seguiu 5 princípios extraídos diretamente do programa:

1. **Estado como Fonte de Verdade (Nível 1 + Nível 3):** Toda informação crítica (estoque, entregadores, rotas, promessas) deve ser persistida em arquivos/SQLite, não apenas em memória. O estado sobrevive a restarts.

2. **Separação de Responsabilidades (Nível 2):** Generator propõe, Evaluator verifica, Planner coordena. Nenhum agente faz tudo sozinho.

3. **Coordenação por Arquivos (Nível 3):** Agentes se coordenam via lock files, status files e manifestos. Sem comunicação direta, sem surpresas.

4. **Contratos Explícitos (Nível 2):** Cada agente publica seu input contract e output contract. Ninguém assume nada sobre o que vai receber ou entregar.

5. **Rastreabilidade Total (Nível 2 + Nível 3):** Cada decisão, cada mudança de estado, cada promessa é registrada em audit trail. Debug não é adivinhação.

### A Nova Arquitetura: Visão Geral

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KODA SAME-DAY DELIVERY — ARQUITETURA FINAL                │
│                         (Padrões de Long-Running Agents)                     │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────┐
                              │    CLIENTE (WhatsApp) │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │  KODA INTERFACE       │
                              │  (Agente de Conversa) │
                              │  Nível 1 + Nível 2    │
                              └──────────┬───────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
          ┌─────────▼─────────┐ ┌───────▼───────┐ ┌─────────▼─────────┐
          │  PLANNER AGENT    │ │ GENERATOR     │ │ EVALUATOR         │
          │  (Coordenação)    │ │ (Proposta de  │ │ (Verificação de   │
          │                    │ │  Entrega)     │ │  Viabilidade)     │
          │  Nível 3           │ │               │ │                   │
          │                    │ │  Nível 2       │ │  Nível 2          │
          └─────────┬─────────┘ └───────┬───────┘ └─────────┬─────────┘
                    │                    │                    │
                    └────────────────────┼────────────────────┘
                                         │
                           ┌─────────────┼─────────────┐
                           │             │             │
                  ┌────────▼───┐ ┌───────▼──────┐ ┌───▼──────────┐
                  │ INVENTORY   │ │ DISPATCH     │ │ ROUTING      │
                  │ AGENT       │ │ AGENT        │ │ AGENT        │
                  │ (Estoque)   │ │ (Entregador) │ │ (Rota)       │
                  │             │ │              │ │              │
                  │ Nível 3      │ │ Nível 3      │ │ Nível 3      │
                  └──────┬──────┘ └──────┬───────┘ └──────┬───────┘
                         │              │                 │
                         └──────────────┼─────────────────┘
                                        │
                         ┌──────────────┼──────────────┐
                         │              │              │
                ┌────────▼───┐  ┌───────▼──────┐ ┌─────▼────────┐
                │ STATE STORE │  │ LOCK FILE    │ │ AUDIT TRAIL  │
                │ (SQLite)    │  │ SYSTEM       │ │ (JSONL)      │
                │             │  │              │ │              │
                │ Nível 3      │  │ Nível 3      │ │ Nível 2      │
                └─────────────┘  └──────────────┘ └──────────────┘
```

### Descrição dos Componentes

#### 1. KODA Interface (Agente de Conversa)

**Responsabilidade:** Interagir com o cliente. Entender intenção. Comunicar resultados. NUNCA tomar decisões de fulfillment.

**Padrões aplicados:**
- **Token Budgeting (N1):** Reserva 15K tokens de buffer para processamento de fulfillment
- **Context Management (N1):** Mantém estado do cliente separado do histórico de conversa
- **Harness Pattern (N1):** Antes de prometer qualquer prazo, DELEGA ao Planner — nunca decide sozinho

**O que NÃO faz:** Verificar estoque, calcular rota, prometer same-day sem aprovação do Evaluator.

#### 2. Planner Agent (Coordenador Central)

**Responsabilidade:** Orquestrar o fluxo de fulfillment. Recebe a intenção do KODA Interface, coordena Inventory + Dispatch + Routing, e retorna uma decisão.

**Padrões aplicados:**
- **Multi-Agent Coordination (N3):** Orquestra 3 agentes especializados em paralelo ou sequência, conforme o caso
- **File-Based Coordination (N3):** Usa lock files para evitar conflitos entre pedidos concorrentes
- **State Persistence (N3):** Persiste o plano de fulfillment em SQLite antes de executar

**Fluxo do Planner:**
```
1. Recebe: { customer_id, cart, delivery_preference: "same_day" }
2. Cria: plan_id = "PLAN-{timestamp}-{customer_hash}"
3. Adquire: lock file para recursos envolvidos (armazem, entregador)
4. Coordena: Inventory Agent → Dispatch Agent → Routing Agent
5. Consolida: plano de fulfillment completo
6. Submete: ao Evaluator para verificação
7. Se aprovado: libera locks e confirma
8. Se rejeitado: ajusta e tenta novamente (max 3 iterações)
```

#### 3. Generator Agent

**Responsabilidade:** Gerar uma proposta de fulfillment. Baseado nos dados dos agentes especializados, criar um plano concreto: qual armazém, qual entregador, qual rota, qual ETA.

**Padrões aplicados:**
- **Generator/Evaluator (N2):** Gera proposta, mas não a avalia
- **Sprint Contracts (N2):** Input contract define exatamente o que espera receber dos agentes especializados

**Exemplo de Output:**
```json
{
  "plan": {
    "warehouse": "SP-ZL",
    "products_reserved": ["WHEY-001:2", "CREATINE-001:1"],
    "dispatcher": "ENTREGADOR-007",
    "dispatcher_eta": "2026-05-28T15:30:00Z",
    "route": "SP-ZL → Moema (Av. Paulista, 1000)",
    "route_eta": "38 minutos (com trânsito moderado)",
    "delivery_window": "16:08 - 16:38",
    "confidence": 0.87
  }
}
```

#### 4. Evaluator Agent

**Responsabilidade:** Verificar se a proposta do Generator é REALMENTE viável. Aplicar rubrica rigorosa e aprovar ou rejeitar.

**Padrões aplicados:**
- **Generator/Evaluator (N2):** Avaliação independente, sem viés do Generator
- **Rubric Design (N2):** Critérios de avaliação explícitos com scores
- **Trace Reading (N2):** Registra toda avaliação para debug posterior

**Rubrica de Avaliação (Same-Day Delivery):**
```
RUBRIC: SAME_DAY_VIABILITY

DIMENSÃO 1: Disponibilidade de Estoque (peso 35%)
  5pts: Todos os itens confirmados em estoque NOW
  3pts: Itens reservados mas estoque baixo (< 5 unidades)
  1pt:  Estoque incerto (última verificação > 10 min)
  0pts: Item fora de estoque → REJEIÇÃO AUTOMÁTICA

DIMENSÃO 2: Disponibilidade de Entregador (peso 30%)
  5pts: Entregador confirmado, sem outras entregas no horário
  3pts: Entregador disponível mas com janela apertada
  1pt:  Entregador único, sem alternativa se falhar
  0pts: Nenhum entregador disponível → REJEIÇÃO AUTOMÁTICA

DIMENSÃO 3: Viabilidade da Rota (peso 20%)
  5pts: Rota direta, ETA ≤ 40 min, sem pontos de congestionamento
  3pts: Rota com alternativas, ETA ≤ 60 min
  1pt:  Rota única, ETA > 60 min ou com risco de trânsito
  0pts: Rota inviável → REJEIÇÃO AUTOMÁTICA

DIMENSÃO 4: Margem de Segurança (peso 15%)
  5pts: Buffer ≥ 90 min até deadline (18h)
  3pts: Buffer ≥ 60 min
  1pt:  Buffer ≥ 30 min
  0pts: Sem buffer → REJEIÇÃO AUTOMÁTICA

SCORE TOTAL: Soma ponderada (0-100)
APROVAÇÃO: Score ≥ 80
REJEIÇÃO: Score < 80 (devolve feedback ao Generator)
REJEIÇÃO AUTOMÁTICA: Qualquer dimensão com 0pts
```

#### 5. Inventory Agent

**Responsabilidade:** Gerenciar estoque em tempo real. Reservar produtos. Alertar quando estoque está baixo.

**Padrões aplicados:**
- **State Persistence (N3):** Estoque é persistido em SQLite com atualizações atômicas
- **File-Based Coordination (N3):** Lock file `inventory.lock.json` impede reservas conflitantes
- **Sprint Contracts (N2):** Contrato explícito de input/output

**Exemplo de Estado (SQLite):**
```sql
-- Tabela: inventory
-- Atualizada em tempo real por Inventory Agent

warehouse_id | sku          | qty_available | qty_reserved | last_updated
SP-ZL        | WHEY-001     | 47           | 3            | 2026-05-28T14:30:00Z
SP-ZL        | CREATINE-001 | 156          | 12           | 2026-05-28T14:30:00Z
SP-MOEMA     | WHEY-001     | 23           | 0            | 2026-05-28T14:28:00Z
SP-MOEMA     | BCAA-001     | 89           | 5            | 2026-05-28T14:29:00Z
```

#### 6. Dispatch Agent

**Responsabilidade:** Gerenciar entregadores. Alocar entregas. Monitorar capacidade.

**Padrões aplicados:**
- **Multi-Agent Coordination (N3):** Coordena com Routing Agent para otimizar alocação
- **State Persistence (N3):** Estado de cada entregador em arquivo JSON
- **File-Based Coordination (N3):** Lock por entregador impede double-booking

**Exemplo de Estado (dispatcher_state.json):**
```json
{
  "dispatchers": [
    {
      "id": "ENTREGADOR-007",
      "name": "João Silva",
      "status": "available",
      "vehicle": "moto",
      "max_weight_kg": 15,
      "current_location": "SP-ZL",
      "delivery_zones": ["SP-ZL", "SP-Moema", "SP-Vila Mariana"],
      "current_deliveries": [],
      "next_available": "2026-05-28T14:45:00Z",
      "lock_file": "ENTREGADOR-007.lock.json"
    }
  ]
}
```

#### 7. Routing Agent

**Responsabilidade:** Calcular rotas. Estimar ETA. Considerar trânsito em tempo real.

**Padrões aplicados:**
- **Sprint Contracts (N2):** Contrato de input/output para ETA e viabilidade
- **Trace Reading (N2):** Registra todas as estimativas para análise posterior de precisão

#### 8. State Store (SQLite)

**Responsabilidade:** Persistir todo estado crítico. Sobreviver a restarts, deploys e falhas.

**Padrões aplicados:**
- **State Persistence (N3):** Persistência completa de estado
- **Server-Side Compaction (N3):** Limpeza de registros antigos sem perder informações críticas

**Estrutura de Tabelas:**
```sql
CREATE TABLE plans (
  plan_id TEXT PRIMARY KEY,
  customer_id TEXT NOT NULL,
  cart_json TEXT NOT NULL,       -- JSON do carrinho
  status TEXT NOT NULL,           -- 'drafting','evaluating','approved','executing','completed','failed'
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE inventory_snapshots (
  snapshot_id TEXT PRIMARY KEY,
  plan_id TEXT NOT NULL,
  warehouse_id TEXT NOT NULL,
  sku TEXT NOT NULL,
  qty_reserved INTEGER NOT NULL,
  reserved_at TEXT NOT NULL,
  released_at TEXT,              -- NULL se ainda reservado
  FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);

CREATE TABLE dispatcher_assignments (
  assignment_id TEXT PRIMARY KEY,
  plan_id TEXT NOT NULL,
  dispatcher_id TEXT NOT NULL,
  assigned_at TEXT NOT NULL,
  completed_at TEXT,
  FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);

CREATE TABLE route_plans (
  route_id TEXT PRIMARY KEY,
  plan_id TEXT NOT NULL,
  origin TEXT NOT NULL,
  destination TEXT NOT NULL,
  estimated_eta_minutes INTEGER NOT NULL,
  actual_delivery_at TEXT,
  traffic_conditions TEXT,
  FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);
```

#### 9. Lock File System

**Responsabilidade:** Impedir conflitos de concorrência. Garantir que dois pedidos não reservem o mesmo estoque ou o mesmo entregador simultaneamente.

**Padrões aplicados:**
- **File-Based Coordination (N3):** Sistema completo de locking com TTL, ownership e deadlock detection

**Tipos de Lock Files:**

| Lock File | Protege | Adquirido por | TTL | Deadlock Strategy |
|-----------|---------|---------------|-----|-------------------|
| `inventory_{warehouse}_{sku}.lock` | Estoque de um SKU específico | Inventory Agent | 30s | Timeout + retry com backoff |
| `dispatcher_{id}.lock` | Disponibilidade de um entregador | Dispatch Agent | 30s | Timeout + fallback para outro |
| `plan_{id}.lock` | Estado de um plano de fulfillment | Planner Agent | 60s | Escalação para operador humano |

**Formato de Lock File:**
```json
{
  "lock_id": "LOCK-INV-SPZL-WHEY001-20260528-143000",
  "resource": "inventory_SP-ZL_WHEY-001",
  "acquired_by": "INVENTORY_AGENT",
  "acquired_at": "2026-05-28T14:30:00Z",
  "expires_at": "2026-05-28T14:30:30Z",
  "plan_id": "PLAN-20260528-143000-abc123",
  "action": "reserve_quantity",
  "quantity": 2,
  "status": "active",
  "owner_session": "agent_session_inv_001"
}
```

**Estratégia de Aquisição de Lock:**
```
Função: acquire_lock(resource, plan_id, action, ttl=30s)

1. Verifica se lock file existe
   ├─ NÃO EXISTE:
   │  ├─ Cria lock file com TTL
   │  ├─ Registra em audit trail
   │  └─ Retorna: { acquired: true, lock_id }
   │
   └─ EXISTE:
      ├─ Verifica se expirou (expires_at < now)
      │  ├─ EXPIRADO:
      │  │  ├─ Remove lock antigo
      │  │  ├─ Cria novo lock
      │  │  ├─ ALERTA: possível deadlock resolvido
      │  │  └─ Retorna: { acquired: true, lock_id, warning: "previous_lock_expired" }
      │  │
      │  └─ ATIVO:
      │     └─ Retorna: { acquired: false, reason: "locked_by", holder: "..." }
      │
      └─ Se não adquiriu, retry com exponential backoff (max 3 tentativas)
```

#### 10. Audit Trail (JSONL)

**Responsabilidade:** Registrar toda decisão, mudança de estado, lock e ação. Permitir trace reading completo.

**Padrões aplicados:**
- **Trace Reading (N2):** Log imutável e consultável de tudo que acontece
- **Server-Side Compaction (N3):** Rotação de logs a cada 7 dias com sumarização

**Exemplo de Entradas:**
```jsonl
{"ts":"2026-05-28T14:30:00Z","event":"plan_created","plan_id":"PLAN-abc123","customer_id":"wa_5511..."}
{"ts":"2026-05-28T14:30:01Z","event":"lock_acquired","lock_id":"LOCK-INV-...","resource":"inventory_SP-ZL_WHEY-001"}
{"ts":"2026-05-28T14:30:02Z","event":"inventory_reserved","plan_id":"PLAN-abc123","sku":"WHEY-001","qty":2}
{"ts":"2026-05-28T14:30:03Z","event":"dispatcher_assigned","plan_id":"PLAN-abc123","dispatcher":"ENTREGADOR-007"}
{"ts":"2026-05-28T14:30:04Z","event":"route_calculated","plan_id":"PLAN-abc123","eta_min":38,"confidence":0.87}
{"ts":"2026-05-28T14:30:05Z","event":"evaluation_started","plan_id":"PLAN-abc123","evaluator":"EVAL_AGENT"}
{"ts":"2026-05-28T14:30:06Z","event":"evaluation_completed","plan_id":"PLAN-abc123","score":89,"verdict":"APPROVED"}
{"ts":"2026-05-28T14:30:07Z","event":"plan_approved","plan_id":"PLAN-abc123","delivery_eta":"16:38"}
{"ts":"2026-05-28T14:30:08Z","event":"lock_released","lock_id":"LOCK-INV-...","resource":"inventory_SP-ZL_WHEY-001"}
{"ts":"2026-05-28T14:30:09Z","event":"customer_notified","plan_id":"PLAN-abc123","eta":"16:38"}
```

---

## 🔄 Fluxo Completo: Um Pedido Same-Day Passo a Passo

### Cenário: Cliente quer comprar com same-day delivery

```
CLIENTE: "KODA, quero 2 whey isolate e 1 creatina. Chega hoje?"
```

### Passo 1: KODA Interface recebe e delega

```
KODA Interface:
  ├─ Detecta intenção: "compra_com_same_day"
  ├─ Extrai: { items: ["WHEY-001:2", "CREATINE-001:1"], delivery: "same_day" }
  ├─ NÃO tenta verificar estoque ou prometer prazo
  └─ Delega para: Planner Agent
       └─ Mensagem: "Cliente quer same-day. Pode?"
```

### Passo 2: Planner inicia orquestração

```
Planner Agent:
  ├─ Cria plan_id: "PLAN-20260528-143000-wa5511"
  ├─ Registra em SQLite: status = "drafting"
  ├─ Escreve em audit trail: "plan_created"
  └─ Inicia coordenação dos agentes especializados
```

### Passo 3: Inventory Agent verifica e reserva estoque

```
Planner → Inventory Agent:
  "Preciso de WHEY-001 (2un) e CREATINE-001 (1un) para same-day"

Inventory Agent:
  ├─ Adquire lock: inventory_SP-ZL_WHEY-001.lock
  │   └─ Lock adquirido: { lock_id: "...", expires: "14:30:30" }
  ├─ Consulta SQLite: WHEY-001 no SP-ZL = 47 disponíveis
  ├─ Reserva 2 unidades: UPDATE qty_reserved = qty_reserved + 2
  ├─ Adquire lock: inventory_SP-ZL_CREATINE-001.lock
  ├─ Consulta SQLite: CREATINE-001 no SP-ZL = 156 disponíveis
  ├─ Reserva 1 unidade: UPDATE qty_reserved = qty_reserved + 1
  ├─ Libera locks
  └─ Responde ao Planner:
      {
        "status": "reserved",
        "warehouse": "SP-ZL",
        "items": [
          {"sku": "WHEY-001", "qty_reserved": 2},
          {"sku": "CREATINE-001", "qty_reserved": 1}
        ],
        "confidence": 1.0
      }
```

### Passo 4: Dispatch Agent aloca entregador

```
Planner → Dispatch Agent:
  "Preciso de entregador em SP-ZL, carga ~3.5kg, destino Moema"

Dispatch Agent:
  ├─ Lê dispatcher_state.json
  ├─ Filtra entregadores disponíveis em SP-ZL que atendem Moema
  ├─ Candidatos: ENTREGADOR-007 (livre), ENTREGADOR-003 (livre), ENTREGADOR-012 (ocupado)
  ├─ Adquire lock: dispatcher_ENTREGADOR-007.lock
  │   └─ Lock adquirido com sucesso
  ├─ Aloca: ENTREGADOR-007
  │   └─ Atualiza dispatcher_state.json: status = "assigned"
  ├─ Libera lock
  └─ Responde ao Planner:
      {
        "status": "assigned",
        "dispatcher_id": "ENTREGADOR-007",
        "dispatcher_name": "João Silva",
        "vehicle": "moto",
        "next_available": "2026-05-28T15:00:00Z",
        "confidence": 0.95
      }
```

### Passo 5: Routing Agent calcula rota e ETA

```
Planner → Routing Agent:
  "Rota: SP-ZL → Moema (Av. Paulista, 1000). Entregador saída 15:00."

Routing Agent:
  ├─ Calcula rota: SP-ZL → Av. Paulista, 1000
  ├─ Verifica trânsito em tempo real: moderado (Google Maps API)
  ├─ Distância: 12.3 km
  ├─ ETA estimado: 38 minutos
  ├─ Considera buffer: +15 min (trânsito pode piorar)
  ├─ Janela de entrega: 15:53 - 16:23
  └─ Responde ao Planner:
      {
        "status": "routable",
        "origin": "SP-ZL",
        "destination": "Av. Paulista, 1000 - Moema",
        "distance_km": 12.3,
        "eta_minutes": 38,
        "traffic": "moderate",
        "delivery_window": "15:53 - 16:23",
        "confidence": 0.87
      }
```

### Passo 6: Generator consolida proposta de fulfillment

```
Planner → Generator:
  "Consolide: inventory ok, dispatcher ok, route ok"

Generator:
  ├─ Recebe outputs dos 3 agentes especializados
  ├─ Valida Sprint Contracts (todos os campos obrigatórios presentes?)
  ├─ Consolida em um plano único:
  │   {
  │     "plan_id": "PLAN-20260528-143000-wa5511",
  │     "customer_id": "wa_5511...",
  │     "items": [
  │       {"sku": "WHEY-001", "qty": 2, "price_unit": 89.90},
  │       {"sku": "CREATINE-001", "qty": 1, "price_unit": 65.00}
  │     ],
  │     "total": 244.80,
  │     "delivery": {
  │       "type": "same_day",
  │       "warehouse": "SP-ZL",
  │       "dispatcher": "ENTREGADOR-007",
  │       "route": "SP-ZL → Moema",
  │       "eta_minutes": 38,
  │       "delivery_window": "15:53 - 16:23",
  │       "promised_by": "18:00"
  │     },
  │     "confidence": 0.89
  │   }
  └─ Submete ao Evaluator
```

### Passo 7: Evaluator aplica rubrica e aprova (ou rejeita)

```
Evaluator:
  ├─ Lê a proposta do Generator
  ├─ Lê o customer_context.json (restrições, histórico)
  ├─ Aplica RUBRIC: SAME_DAY_VIABILITY

  DIMENSÃO 1: Disponibilidade de Estoque (35%)
    ✅ Todos os itens confirmados e reservados → 5pts → 1.75/1.75

  DIMENSÃO 2: Disponibilidade de Entregador (30%)
    ✅ Entregador confirmado, sem outras entregas → 5pts → 1.50/1.50

  DIMENSÃO 3: Viabilidade da Rota (20%)
    ✅ Rota direta, ETA 38min ≤ 40min → 5pts → 1.00/1.00

  DIMENSÃO 4: Margem de Segurança (15%)
    ✅ Buffer = 97 min (até 18h). > 90 min → 5pts → 0.75/0.75

  SCORE TOTAL: 5.00 / 5.00 = 100/100
  VERDICT: ✅ APROVADO (score 100 ≥ 80)

  ├─ Registra em audit trail: "evaluation_completed", score=100, verdict=APPROVED
  └─ Retorna APPROVED ao Planner
```

### Passo 8: Planner finaliza e KODA comunica

```
Planner:
  ├─ Recebe APPROVED do Evaluator
  ├─ Atualiza SQLite: status = "approved"
  ├─ Libera todos os locks
  ├─ Registra em audit trail: "plan_approved"
  ├─ Notifica KODA Interface: "Plano aprovado. Pode prometer same-day."
  └─ Notifica Dispatch Agent para iniciar preparação

KODA Interface:
  ├─ Recebe confirmação do Planner
  ├─ Token Budgeting check: ainda tem 12K tokens livres? ✅
  ├─ Responde ao cliente:
  │   "Ótima notícia! Seu pedido com 2x Whey Isolate e 1x Creatina
  │    chega HOJE entre 15:53 e 16:23. Total: R$ 244,80.
  │    Posso confirmar o pedido?"
  └─ Aguarda confirmação do cliente
```

### Passo 9 (se rejeitado): Feedback loop

```
Cenário alternativo: Evaluator REJEITA (score 72)

Evaluator → Planner:
  "REJEITADO. Dimensão 3 (Rota) score baixo: ETA 58 min, trânsito pesado."
  
Planner → Generator:
  "Tente novamente. Problema: rota atual tem trânsito. Considere alternativas."

Generator (2ª tentativa):
  ├─ Consulta Routing Agent para rota alternativa
  ├─ Routing Agent: "Rota alternativa via Marginal Tietê: ETA 41 min"
  ├─ Novo plano consolidado: confidence 0.91
  └─ Submete ao Evaluator novamente

Evaluator (2ª verificação):
  DIMENSÃO 3 (Rota): 5pts ✅ (41 min ≤ 40 + margem)
  SCORE: 95/100 ✅ APROVADO
```

---

## 📊 Diagrama ASCII da Arquitetura Completa

```
+======================================================================+
|                    KODA SAME-DAY DELIVERY                             |
|                 Arquitetura de Long-Running Agents                    |
+======================================================================+

                         WHATSAPP (CLIENTE)
                              │
                              ▼
+──────────────────────────────────────────────────────────────────+
|                    KODA INTERFACE (N1 + N2)                       |
|  ┌─────────────────────────────────────────────────────────────┐ |
|  │ Token Budgeting: reserva 15K tokens para fulfillment        │ |
|  │ Context Management: estado cliente separado do histórico    │ |
|  │ Harness Pattern: nunca promete prazo sem aprovação          │ |
|  └─────────────────────────────────────────────────────────────┘ |
+────────────────────────────┬─────────────────────────────────────+
                             │ "Cliente quer same-day. Pode?"
                             ▼
+──────────────────────────────────────────────────────────────────+
|                    PLANNER AGENT (N3)                              |
|  ┌─────────────────────────────────────────────────────────────┐ |
|  │ • Orquestra fluxo de fulfillment                            │ |
|  │ • Gerencia locks e concorrência                             │ |
|  │ • Persiste planos em SQLite                                 │ |
|  │ • Coordena 3 agentes especializados                         │ |
|  │ • Max 3 iterações de tentativa                              │ |
|  └─────────────────────────────────────────────────────────────┘ |
+───┬──────────────────┬─────────────────────┬─────────────────────+
    │                  │                     │
    ▼                  ▼                     ▼
+──────────+    +──────────────+    +─────────────────+
|INVENTORY |    |  DISPATCH    |    |   ROUTING       |
|AGENT (N3)|    |  AGENT (N3)  |    |   AGENT (N3)    |
|          |    |              |    |                 |
|• Reserva |    |• Aloca       |    |• Calcula rota   |
| estoque  |    | entregador   |    |• Estima ETA     |
|• Lock    |    |• Lock        |    |• Trânsito real  |
| inventory|    | dispatcher   |    |• Fallback route |
|• SQLite  |    |• JSON state  |    |                 |
+────┬─────+    +──────┬───────+    +────────┬────────+
     │                │                     │
     └────────────────┼─────────────────────┘
                      │
                      ▼
+──────────────────────────────────────────────────────────────────+
|                    GENERATOR AGENT (N2)                            |
|  ┌─────────────────────────────────────────────────────────────┐ |
|  │ • Consolida outputs dos 3 agentes especializados            │ |
|  │ • Valida Sprint Contracts                                    │ |
|  │ • Gera plano de fulfillment unificado                        │ |
|  │ • NÃO avalia — apenas propõe                                 │ |
|  └─────────────────────────────────────────────────────────────┘ |
+────────────────────────────┬─────────────────────────────────────+
                             │ "Plano consolidado. Verifique."
                             ▼
+──────────────────────────────────────────────────────────────────+
|                    EVALUATOR AGENT (N2)                            |
|  ┌─────────────────────────────────────────────────────────────┐ |
|  │ • Aplica RUBRIC: SAME_DAY_VIABILITY                         │ |
|  │ • 4 dimensões, score 0-100                                  │ |
|  │ • Temperatura 0.2 (rigor máximo)                             │ |
|  │ • APROVA (≥ 80) ou REJEITA (< 80)                           │ |
|  │ • Se rejeita: feedback específico para Generator            │ |
|  └─────────────────────────────────────────────────────────────┘ |
+────────────────────────────┬─────────────────────────────────────+
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
              ✅ APROVADO      ❌ REJEITADO
              (score ≥ 80)     (score < 80)
                    │                 │
                    ▼                 ▼
        +──────────────────+  +──────────────────+
        | Confirma pedido   |  | Feedback loop:   |
        | Libera locks      |  | Generator tenta  |
        | Notifica KODA     |  | novamente        |
        | Inicia fulfillment|  | (max 3 iterações)|
        +──────────────────+  +──────────────────+
                    │
                    ▼
+──────────────────────────────────────────────────────────────────+
|                    INFRAESTRUTURA COMPARTILHADA                    |
|                                                                   |
|  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐ |
|  │ STATE STORE     │  │ LOCK FILE SYSTEM │  │ AUDIT TRAIL      │ |
|  │ (SQLite)        │  │                  │  │ (JSONL)          │ |
|  │                 │  │ • inventory locks│  │ • todas decisões │ |
|  │ • plans         │  │ • dispatcher lock│  │ • todos locks    │ |
|  │ • inventory     │  │ • plan locks     │  │ • todas mudanças │ |
|  │ • assignments   │  │ • TTL 30s-60s    │  │ • imutável       │ |
|  │ • route_plans   │  │ • deadlock detect│  │ • rotaciona 7d   │ |
|  └─────────────────┘  └──────────────────┘  └──────────────────┘ |
+======================================================================+
```

---

## 📊 Métricas Comparativas: Antes vs Depois

### Métricas de Negócio

| Métrica | Antes (Dez 2025) | MVP1-3 (Jan-Mar 2026) | Depois (Mai 2026) | Melhoria |
|---------|------------------|----------------------|-------------------|----------|
| **Taxa de sucesso same-day** | 62% | 64% → 67% → 72% | **94%** | **+32pp** |
| **Atrasos médios** | 3.2 horas | 2.8 → 2.1 → 1.4 horas | **18 minutos** | **-91%** |
| **Reclamações same-day/dia** | 18 | 17 → 15 → 12 | **2** | **-89%** |
| **Cancelamentos pós-atraso/dia** | 8 | 7 → 5 → 4 | **0.5** | **-94%** |
| **Churn por insatisfação/mês** | 12 | 10 → 8 → 6 | **2** | **-83%** |
| **Custo operacional/dia** | R$ 4.200 | R$ 4.300 → R$ 4.600 → R$ 5.400 | **R$ 3.800** | **-10%** |
| **Ticket médio (same-day)** | R$ 360 | R$ 355 → R$ 358 → R$ 362 | **R$ 385** | **+7%** |
| **NPS (same-day)** | 32 | 35 → 38 → 41 | **72** | **+40pp** |
| **Pedidos same-day/dia** | 120 | 115 → 118 → 122 | **178** | **+48%** |
| **Receita same-day/mês** | R$ 129.600 | R$ 122.820 → R$ 126.738 → R$ 132.438 | **R$ 205.860** | **+59%** |

### Métricas Técnicas

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Tempo de resposta (promessa same-day)** | 5.8s | **1.9s** | **-67%** |
| **Condições de corrida/dia** | 8 | **0** | **-100%** |
| **Promessas falsas/dia** | 38 | **6** | **-84%** |
| **Tempo de re-roteamento** | 38s | **4.2s** | **-89%** |
| **Deadlocks resolvidos/dia** | N/A (não detectava) | **0.3** (detecta e resolve) | Novo |
| **Disponibilidade do sistema** | 99.2% | **99.97%** | **+0.77pp** |
| **Tempo médio de debug (incidente)** | 8 horas | **45 minutos** | **-91%** |
| **Custo LLM por pedido** | R$ 0.09 | **R$ 0.06** | **-33%** |
| **Cobertura de audit trail** | 12% das decisões | **100%** | **+88pp** |

### Métricas de Qualidade do Agente

| Métrica | Antes | Depois |
|---------|-------|--------|
| **Acurácia do ETA (± 15 min)** | 58% | **91%** |
| **Taxa de falsos positivos (prometeu, não cumpriu)** | 38% | **6%** |
| **Taxa de falsos negativos (não prometeu, podia cumprir)** | 22% | **4%** |
| **Rubric scores médios (avaliações internas)** | 64/100 | **89/100** |
| **Sprint Contracts violados/dia** | 47 | **3** |
| **Tempo até detecção de falha** | 45 min (média) | **2.3 min** |
| **Tempo até correção de falha** | 3.2 horas | **6.5 min** |

### Análise de ROI

```
CUSTO DO PROJETO:
  Desenvolvimento (12 semanas, 4 engenheiros):  R$ 192.000
  Infraestrutura adicional (SQLite, locks):      R$   2.400/mês
  Custo LLM adicional (Generator + Evaluator):   R$   1.800/mês
  Treinamento do time:                           R$  12.000
  ─────────────────────────────────────────────────────────
  CUSTO TOTAL (primeiros 6 meses):               R$ 227.400

GANHO DO PROJETO (6 meses):
  Redução de cancelamentos:                      R$  51.840
  Redução de churn:                              R$  51.840
  Redução de custo operacional:                  R$  72.000
  Aumento de receita (mais pedidos same-day):    R$ 457.560
  Redução de suporte:                            R$   9.720
  ─────────────────────────────────────────────────────────
  GANHO TOTAL (6 meses):                         R$ 642.960

ROI (6 meses): (642.960 - 227.400) / 227.400 = 183%
PAYBACK: 2.1 meses
```

---

## 📋 Tabela Comparativa de Estratégias de Coordenação

Durante o desenvolvimento, o time avaliou 3 estratégias de coordenação entre agentes. Esta tabela documenta a análise:

| Dimensão | Coordenação Centralizada | Coordenação Descentralizada | Coordenação Híbrida (Escolhida) |
|----------|--------------------------|----------------------------|--------------------------------|
| **Descrição** | Um Planner Agent orquestra tudo. Agentes especializados são "burros" — só executam. | Cada agente é autônomo. Descobrem e negociam entre si. | Planner coordena a orquestração. Agentes têm autonomia para otimização local. |
| **Vantagens** | Simples de debugar. Fluxo previsível. Fácil de auditar. | Robusto a falhas do Planner. Escala bem com muitos agentes. Agents podem evoluir independentemente. | Melhor dos dois mundos. Flexibilidade local + coordenação global. |
| **Desvantagens** | Planner é single point of failure. Pode virar gargalo. Não escala para muitos agentes. | Debug complexo. Pode ter conflitos não detectados. Decisões locais podem ser sub-ótimas globalmente. | Mais complexo de implementar. Requer contratos bem definidos entre camadas. |
| **Latência** | Média (tudo passa pelo Planner) | Baixa (agentes agem em paralelo) | Baixa-média (paralelo onde possível) |
| **Confiabilidade** | Baixa (se Planner falha, sistema para) | Alta (sem single point) | Alta (Planner tem fallback) |
| **Debugabilidade** | Alta (audit trail linear) | Baixa (múltiplos timelines) | Média-alta (audit trail hierárquico) |
| **Custo de implementação** | Baixo | Alto | Médio-alto |
| **Adequação para same-day** | ⚠️ Bom para MVP, mas não escala com volume | ⚠️ Robusto mas difícil de garantir consistência | ✅ Melhor escolha para coordenação em tempo real com estado compartilhado |
| **Quando usar no KODA** | Features simples (promoções, recomendações) | Features assíncronas (notificações, relatórios) | Features complexas com estado compartilhado (fulfillment, pagamentos) |
| **Exemplo KODA** | Generator/Evaluator para recomendação (Planner = Evaluator) | Agentes de notificação independentes por canal (WhatsApp, Email, Push) | Same-day delivery: Planner coordena, Inventory/Dispatch/Routing otimizam localmente |
| **Risco de deadlock** | Baixo (centralizado) | Alto (múltiplos lock owners) | Médio (TTL + deadlock detection) |

### Decisão de Arquitetura

A estratégia **híbrida** foi escolhida para o same-day delivery porque:

1. **Estado compartilhado:** Inventory, Dispatch e Routing compartilham recursos (estoque, entregadores). Coordenação central evita conflitos.

2. **Otimização local:** Cada agente especializado conhece seu domínio melhor que o Planner. Inventory Agent sabe otimizar reserva de estoque. Dispatch Agent sabe balancear carga entre entregadores.

3. **Resiliência:** O Planner pode falhar, mas os locks e o state store garantem que o estado não corrompa. Se o Planner cair, um novo Planner lê o estado do SQLite e continua.

4. **Audit trail:** Estrutura hierárquica: Planner registra decisões de alto nível, agentes especializados registram decisões táticas. Debug é rápido e preciso.

---

## 💼 Aplicação KODA: Como Esse Padrão se Aplica a Outras Features

O padrão arquitetural desenvolvido para same-day delivery não é específico dessa feature. Ele estabelece um **template de arquitetura** que pode ser aplicado a qualquer feature complexa do KODA:

### Template de Arquitetura para Features KODA

```
Para qualquer feature complexa do KODA, siga este template:

1. IDENTIFIQUE os agentes especializados necessários
   └─ Cada agente = uma responsabilidade atômica

2. DEFINA os Sprint Contracts de cada agente
   └─ Input contract, output contract, guarantees

3. PROJETE o fluxo de coordenação
   └─ Planner orquestra, Generator consolida, Evaluator verifica

4. IMPLEMENTE file-based coordination
   └─ Lock files para recursos compartilhados
   └─ Status files para visibilidade
   └─ Audit trail para rastreabilidade

5. PERSISTA estado crítico
   └─ SQLite para dados estruturados
   └─ JSON files para configuração e estado simples

6. APLIQUE Rubric Design
   └─ 3-5 dimensões de avaliação
   └─ Score mínimo para aprovação
   └─ Rejeição com feedback específico

7. INSTRUMENTE com Trace Reading
   └─ Audit trail cobre 100% das decisões
   └─ Timestamps e IDs linkáveis
   └─ Scripts de debug pré-construídos
```

### Exemplo 1: Aplicação em Feature de Pagamentos

```
Feature: Processamento de Pagamento com Múltiplos Métodos

Agentes:
  ├─ Payment Method Agent (valida bandeira, parcelamento)
  ├─ Fraud Detection Agent (análise de risco)
  ├─ Payment Gateway Agent (comunicação com adquirente)
  └─ Receipt Agent (geração de comprovante)

Coordenação:
  Planner → Payment Method → Fraud Detection (paralelo com) → Payment Gateway → Receipt

Locks:
  payment_{order_id}.lock (impede cobrança duplicada)

Rubric:
  D1: Método válido (25%)
  D2: Fraude OK (35%)
  D3: Gateway responded (25%)
  D4: Comprovante gerado (15%)
  Score mín: 85
```

### Exemplo 2: Aplicação em Feature de Carrinho

```
Feature: Carrinho Persistente Multi-Sessão

Agentes:
  ├─ Cart State Agent (persiste estado do carrinho)
  ├─ Price Validation Agent (verifica preços atuais)
  ├─ Stock Validation Agent (verifica disponibilidade)
  └─ Cart Recovery Agent (restaura carrinho abandonado)

Coordenação:
  Planner → Cart State → Price Validation + Stock Validation (paralelo) → Cart Recovery

State Persistence:
  SQLite: cart_items, cart_snapshots, price_history

Locks:
  cart_{customer_id}.lock (impede conflitos entre sessões)

Rubric:
  D1: Preços atualizados (40%)
  D2: Estoque confirmado (30%)
  D3: Cupons aplicados (20%)
  D4: Frete calculado (10%)
  Score mín: 80
```

### Exemplo 3: Aplicação em Feature de Recomendações (já existente, com melhorias)

```
Feature: Recomendações Personalizadas (evolução do N2)

Agentes (adicionais ao Generator/Evaluator existente):
  ├─ History Analysis Agent (analisa histórico de compras e interações)
  ├─ Trend Detection Agent (identifica produtos em alta)
  └─ Personalization Agent (ajusta recomendações ao perfil)

Coordenação:
  Planner → History Analysis + Trend Detection (paralelo) → Personalization → Generator → Evaluator

Novo no N4:
  - History e Trend são agentes especializados (N3) que alimentam o Generator (N2)
  - Personalization Agent mantém perfil em SQLite (N3)
  - Rubric expandida para 6 dimensões (N2 melhorado)

Rubric expandida (6 dimensões):
  D1: Relevância ao perfil (25%)
  D2: Custo-benefício (20%)
  D3: Tendência de mercado (10%) ← NOVO
  D4: Histórico de satisfação (20%)
  D5: Disponibilidade (15%)
  D6: Margem do produto (10%) ← NOVO (negócio)
  Score mín: 78
```

---

## 🔬 Análise Técnica Profunda: Padrões em Ação

### Padrão 1: State Persistence com SQLite

O state store foi a mudança mais impactante. Antes, o KODA operava completamente stateless — cada requisição era independente. Depois, todo estado crítico passou a ser persistido.

**Estrutura completa do banco:**
```sql
-- Plans: cada plano de fulfillment
CREATE TABLE IF NOT EXISTS plans (
  plan_id TEXT PRIMARY KEY,
  customer_id TEXT NOT NULL,
  conversation_id TEXT NOT NULL,
  cart_json TEXT NOT NULL,
  delivery_type TEXT NOT NULL CHECK(delivery_type IN ('same_day', 'next_day', 'scheduled')),
  status TEXT NOT NULL CHECK(status IN (
    'drafting', 'evaluating', 'approved', 'executing',
    'out_for_delivery', 'delivered', 'failed', 'cancelled'
  )),
  evaluator_score REAL,
  evaluator_verdict TEXT,
  delivery_eta TEXT,
  actual_delivery_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Inventory snapshots: reservas atômicas
CREATE TABLE IF NOT EXISTS inventory_snapshots (
  snapshot_id TEXT PRIMARY KEY,
  plan_id TEXT NOT NULL,
  warehouse_id TEXT NOT NULL,
  sku TEXT NOT NULL,
  qty_reserved INTEGER NOT NULL CHECK(qty_reserved > 0),
  qty_released INTEGER DEFAULT 0,
  reserved_at TEXT NOT NULL DEFAULT (datetime('now')),
  released_at TEXT,
  FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);

-- Dispatcher assignments
CREATE TABLE IF NOT EXISTS dispatcher_assignments (
  assignment_id TEXT PRIMARY KEY,
  plan_id TEXT NOT NULL,
  dispatcher_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('assigned', 'en_route', 'delivered', 'failed')),
  assigned_at TEXT NOT NULL DEFAULT (datetime('now')),
  completed_at TEXT,
  FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);

-- Route plans
CREATE TABLE IF NOT EXISTS route_plans (
  route_id TEXT PRIMARY KEY,
  plan_id TEXT NOT NULL,
  origin TEXT NOT NULL,
  destination TEXT NOT NULL,
  distance_km REAL,
  eta_minutes INTEGER NOT NULL,
  traffic_condition TEXT CHECK(traffic_condition IN ('light', 'moderate', 'heavy', 'severe')),
  delivery_window_start TEXT,
  delivery_window_end TEXT,
  actual_delivery_at TEXT,
  FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);

-- Índices para queries frequentes
CREATE INDEX IF NOT EXISTS idx_plans_customer ON plans(customer_id, created_at);
CREATE INDEX IF NOT EXISTS idx_plans_status ON plans(status, created_at);
CREATE INDEX IF NOT EXISTS idx_inventory_warehouse ON inventory_snapshots(warehouse_id, sku);
CREATE INDEX IF NOT EXISTS idx_dispatcher ON dispatcher_assignments(dispatcher_id, status);
CREATE INDEX IF NOT EXISTS idx_routes_plan ON route_plans(plan_id);
```

**Transação de reserva de inventário (atômica):**
```sql
BEGIN TRANSACTION;

-- Verifica disponibilidade
SELECT qty_available - qty_reserved AS available
FROM inventory
WHERE warehouse_id = 'SP-ZL' AND sku = 'WHEY-001';

-- Se available >= quantidade_pedido:
UPDATE inventory
SET qty_reserved = qty_reserved + 2,
    updated_at = datetime('now')
WHERE warehouse_id = 'SP-ZL' AND sku = 'WHEY-001';

-- Registra snapshot
INSERT INTO inventory_snapshots (snapshot_id, plan_id, warehouse_id, sku, qty_reserved)
VALUES ('SNAP-' || hex(randomblob(8)), 'PLAN-abc123', 'SP-ZL', 'WHEY-001', 2);

COMMIT;
```

### Padrão 2: Lock Files com TTL

O sistema de lock files foi essencial para eliminar condições de corrida. O design segue princípios rigorosos:

**Princípios do Lock System:**
1. **Atomicidade:** Lock é criado via write atômico (arquivo não existia → agora existe)
2. **TTL obrigatório:** Todo lock expira. Nenhum lock é "permanente"
3. **Ownership clara:** Todo lock tem um `owner_session` rastreável
4. **Deadlock detection:** Sistema monitora locks com > 2x TTL e força release
5. **Audit trail:** Toda operação de lock é registrada

**Fluxo de Aquisição com Retry:**
```
acquire_lock_with_retry(resource, plan_id, action, max_retries=3):

  for attempt in 1..max_retries:
    result = try_acquire_lock(resource, plan_id, action)
    
    if result.acquired:
      return result
    
    # Lock não adquirido — verifica razão
    if result.reason == "locked_by_another":
      lock_holder = result.holder
      
      # Deadlock detection: lock ativo há > 2x TTL?
      if lock_age(lock_holder) > 2 * TTL:
        force_release_lock(lock_holder)
        log_event("deadlock_detected_and_resolved", holder=lock_holder)
        continue  # tenta novamente
      
      # Espera com exponential backoff
      wait_ms = 100 * (2 ** attempt)  # 100, 200, 400 ms
      sleep(wait_ms)
    
    elif result.reason == "owned_by_self":
      return result  # já tenho o lock, prossegue
    
    else:
      return result  # outro erro
  
  # Esgotou tentativas
  log_event("lock_acquisition_failed", resource=resource, attempts=max_retries)
  escalate_to_human(resource, plan_id)
```

### Padrão 3: Evaluator com Rubric Design

O Evaluator é o guardião da qualidade. Sua implementação usa temperatura baixa (0.2) e instruções explícitas para ser crítico:

**System Prompt do Evaluator:**
```
Você é o EVALUATOR do sistema de same-day delivery do KODA.

SUA MISSÃO: Encontrar problemas. Rejeitar planos que não são seguros.
Seu sucesso é medido por quantos falsos positivos você EVITOU.

VOCÊ NÃO É:
- Um aprovador automático
- Um otimista
- Um "amigo" do Generator

REGRAS:
1. Avalie cada dimensão independentemente
2. Score 0 em qualquer dimensão = REJEIÇÃO AUTOMÁTICA
3. NÃO justifique scores baixos com "mas talvez dê certo"
4. Se tiver dúvida entre 3 e 4 pontos, dê 3
5. Registre o raciocínio para CADA dimensão

RUBRIC:
[Incluir a rubrica completa aqui]

Responda em JSON com o formato:
{
  "verdict": "APPROVED|REJECTED",
  "overall_score": 0-100,
  "dimensions": {
    "inventory": { "score": 0-5, "reasoning": "..." },
    "dispatcher": { "score": 0-5, "reasoning": "..." },
    "routing": { "score": 0-5, "reasoning": "..." },
    "safety_margin": { "score": 0-5, "reasoning": "..." }
  },
  "issues": [...],
  "recommendation": "..."
}
```

### Padrão 4: Trace Reading e Debug

Com o audit trail completo, o time criou scripts de debug que reduziram o tempo de investigação de horas para minutos:

**Script de Debug de Entrega Falha:**
```python
def debug_failed_delivery(plan_id):
    """
    Reconstrói timeline completa de um plano que falhou.
    """
    
    # 1. Lê o plano do SQLite
    plan = db.query("SELECT * FROM plans WHERE plan_id = ?", [plan_id])
    
    # 2. Lê audit trail filtrado
    audit = read_audit_trail(filter_plan=plan_id)
    
    # 3. Reconstrói timeline
    print(f"=== DEBUG: PLAN {plan_id} ===")
    print(f"Status final: {plan['status']}")
    print(f"Criado em: {plan['created_at']}")
    print(f"Score do Evaluator: {plan['evaluator_score']}")
    print()
    
    print("TIMELINE:")
    for event in audit:
        timestamp = event['ts']
        event_type = event['event']
        details = {k: v for k, v in event.items() if k not in ['ts', 'event', 'plan_id']}
        print(f"  {timestamp} | {event_type:30s} | {details}")
    
    print()
    
    # 4. Identifica ponto de falha
    failure_event = next((e for e in audit if e['event'] in [
        'evaluation_rejected', 'lock_acquisition_failed',
        'inventory_insufficient', 'dispatcher_unavailable',
        'route_infeasible'
    ]), None)
    
    if failure_event:
        print(f"🔴 PONTO DE FALHA: {failure_event['event']}")
        print(f"   Timestamp: {failure_event['ts']}")
        print(f"   Detalhes: {failure_event}")
        
        # 5. Análise de causa raiz
        print()
        print("ANÁLISE DE CAUSA RAIZ:")
        
        if failure_event['event'] == 'inventory_insufficient':
            # Verifica se houve race condition
            nearby_reservations = db.query("""
                SELECT * FROM inventory_snapshots
                WHERE warehouse_id = ? AND sku = ?
                AND reserved_at BETWEEN datetime(?, '-5 minutes') AND datetime(?, '+5 minutes')
            """, [failure_event['warehouse_id'], failure_event['sku'],
                  failure_event['ts'], failure_event['ts']])
            
            if len(nearby_reservations) > 1:
                print(f"  ⚠️ Possível race condition: {len(nearby_reservations)} reservas")
                print(f"     no mesmo SKU em janela de 10 minutos")
```

---

## 📈 Resultados e Impacto no Negócio

### O Que Mudou para os Clientes

**Antes (Depoimento real — Janeiro 2026):**
> "KODA, você prometeu que chegava hoje. Já são 20h e nada. Isso já aconteceu 3 vezes. Estou muito frustrado. Vou procurar outro lugar para comprar meus suplementos." — Cliente R.S., 3 reclamações em 2 meses

**Depois (Depoimento real — Maio 2026):**
> "KODA, pedi às 15h e chegou 16h20! Incrível. Você é o único lugar onde confio para comprar suplementos com entrega rápida. Indiquei para 3 amigos da academia." — Cliente R.S., 5 compras em Maio, NPS 10

### O Que Mudou para o Time

**Antes:**
- 40% do tempo de engenharia gasto em debugging reativo
- Medo de deploy em dias de alto volume (segundas e sextas)
- "Funciona na minha máquina" era frase comum
- Incapazes de prever quando o sistema falharia

**Depois:**
- 10% do tempo em debugging (redução de 75%)
- Deploys em qualquer dia da semana com confiança
- Audit trail substituiu "funciona na minha máquina"
- Dashboards mostram saúde do sistema em tempo real

### O Que Mudou para o Negócio

| Indicador | Antes | Depois | Significado |
|-----------|-------|--------|-------------|
| **Same-day como % de pedidos** | 35% | **52%** | Clientes confiam mais na promessa |
| **Recompra em 30 dias** | 28% | **47%** | Experiência positiva gera fidelidade |
| **Indicações (word-of-mouth)** | 3/mês | **18/mês** | Clientes promovem o diferencial |
| **Avaliação WhatsApp Business** | 4.1 ⭐ | **4.8 ⭐** | Reputação recuperada |
| **Vantagem competitiva** | "Prometia mas não cumpria" | **"Único que entrega mesmo"** | Diferencial real |

---

## 🎓 Lições Aprendidas

### Lição 1: Não Remende — Redesenhe

Os 3 MVPs foram remendos. Cada um atacava um sintoma, não a causa. O time gastou 9 semanas em MVPs que melhoraram a taxa de sucesso em apenas 10pp (62% → 72%). A refatoração arquitetural levou 12 semanas e melhorou em 22pp adicionais (72% → 94%).

**Moral:** Quando o problema é arquitetural, patches não resolvem. Redesenhe.

### Lição 2: Coordenação é Mais Importante que Inteligência

O KODA não ficou "mais inteligente" com a refatoração. O modelo é o mesmo. O que mudou foi a **coordenação** entre componentes. A lição é que, para sistemas multi-agente, a arquitetura de coordenação importa mais que a capacidade individual de cada agente.

### Lição 3: Estado Persistente é a Base de Tudo

A maior transformação foi tirar o sistema de stateless para stateful. Com estado persistente:
- Promessas não desaparecem em restarts
- Concorrência pode ser controlada (locks)
- Decisões são rastreáveis (audit trail)
- Recuperação de falhas é possível (estado no SQLite)

### Lição 4: Rubrics Evitam Falsos Positivos

Antes do Evaluator com rubrica, o KODA prometia same-day com 38% de falsos positivos (prometia mas não cumpria). A rubrica forçou o sistema a ser honesto: se não há certeza razoável, não promete. Isso reduziu falsos positivos para 6%.

### Lição 5: Trace Reading Transforma Debug

O audit trail completo reduziu o tempo de debug de 8 horas para 45 minutos. Mas o benefício maior foi **cultural**: o time parou de ter medo de problemas. Com trace reading, todo problema é diagnosticável. Isso aumentou a velocidade de iteração e a confiança do time.

### Lição 6: O Custo da Coordenação se Paga

Generator + Evaluator + Planner + Locks + SQLite + Audit Trail aumentaram o custo operacional em 29% inicialmente. Mas a economia gerada (menos cancelamentos, menos churn, menos suporte, mais pedidos) pagou o investimento em 2.1 meses.

### Lição 7: Comece com Contratos, Não com Código

O time passou 2 semanas apenas desenhando Sprint Contracts antes de escrever uma linha de código. Esse investimento inicial em design de contratos evitou inúmeros problemas de integração. A lição: contratos são mais baratos que debugging.

### Lição 8: Padrões Não São Dogma — São Ferramentas

Nem todo padrão do programa foi aplicado em sua forma "pura". Server-side compaction, por exemplo, foi adaptado — em vez de sumarizar conversas (como no N3), ele sumariza audit trails antigos. A lição: entenda o princípio, adapte a implementação.

### Lição 9: A Complexidade Certa no Lugar Certo

O sistema ficou mais complexo. São 7 agentes, SQLite, lock files, audit trails. Mas a complexidade está **localizada** — cada componente é simples isoladamente. A complexidade do sistema anterior era **distribuída** — ninguém sabia onde estava o problema. Complexidade localizada é gerenciável. Complexidade distribuída é caos.

### Lição 10: Métricas Antes, Durante e Depois

O time aprendeu a medir tudo. Antes do projeto, as métricas eram superficiais ("quantos pedidos?"). Durante o projeto, métricas guiaram cada decisão ("MVP3 melhorou em 5pp mas custou 3x mais — vale a pena?"). Depois, métricas provaram o ROI e justificaram o investimento.

---

## 🛡️ Análise de Modos de Falha: O Que Pode Dar Errado e Como o Sistema Responde

Nenhum sistema é infalível. A arquitetura de long-running agents não elimina falhas — ela as torna **gerenciáveis**. Esta seção cataloga os modos de falha conhecidos e como o sistema responde a cada um.

### Modo de Falha 1: Inventory Agent Indisponível

**Cenário:** O Inventory Agent crasha ou fica inacessível durante o processo de fulfillment.

**Sintoma:** Planner tenta adquirir lock de inventory e timeout ocorre.

**Resposta do Sistema:**
```
1. Planner tenta lock com retry (3 tentativas, backoff exponencial)
2. Se todas falham:
   ├─ Planner consulta SQLite diretamente (bypass do agente)
   ├─ Último snapshot de inventory é usado (com flag "stale_data": true)
   ├─ Evaluator APLICA PENALIDADE na dimensão de estoque:
   │   score máximo = 3 (em vez de 5) — "estoque incerto"
   ├─ Se score total ainda ≥ 80: aprova com aviso
   └─ Se score < 80: rejeita e oferece next-day delivery
3. Alerta é enviado para equipe de infra
4. Inventory Agent é reiniciado automaticamente (systemd)
5. Próximo pedido já usa agente recuperado
```

**Impacto no cliente:** Se o estoque for suficiente e o resto do plano for robusto, o cliente nem percebe. Se não, recebe uma oferta de next-day com desconto compensatório.

### Modo de Falha 2: Condição de Corrida no Último Item em Estoque

**Cenário:** Apenas 1 unidade de um produto. Dois pedidos simultâneos tentam reservá-lo.

**Resposta do Sistema:**
```
Pedido A e Pedido B chegam ao mesmo tempo.

T0: Ambos consultam inventory (sem lock ainda)
T1: Ambos veem "1 unidade disponível"
T2: Pedido A adquire lock primeiro (atomic write vence)
T3: Pedido B tenta adquirir lock → FALHA (já locked)
T4: Pedido A reserva a unidade → UPDATE inventory SET qty_reserved = qty_reserved + 1
T5: Pedido A libera lock
T6: Pedido B re-tenta lock → SUCESSO
T7: Pedido B consulta inventory → 0 disponíveis (qty_available - qty_reserved = 0)
T8: Pedido B reporta ao Planner: "estoque insuficiente"
T9: Planner ativa re-roteamento:
    ├─ Tenta outro armazém → se encontrado, usa
    └─ Se não encontrado → oferece next-day ao cliente

Resultado: Sem race condition. Sem double-booking. Cliente B recebe alternativa.
```

### Modo de Falha 3: Entregador Fica Indisponível Após Alocação

**Cenário:** Entregador-007 foi alocado para o Pedido #8941. Antes da coleta, o entregador reporta problema (moto quebrou, emergência pessoal).

**Resposta do Sistema:**
```
Monitoramento contínuo do Dispatch Agent:

1. Dispatch Agent detecta: ENTREGADOR-007 marcou status = "unavailable"
2. Dispatch Agent verifica: entregador tinha entregas pendentes?
   └─ Sim: Pedido #8941
3. Dispatch Agent notifica Planner: "ENTREGADOR-007 indisponível. Re-roteie #8941."
4. Planner inicia re-roteamento de emergência:
   ├─ Adquire dispatcher lock para ENTREGADOR-003 (backup)
   ├─ Routing Agent recalcula ETA com novo entregador
   ├─ Generator consolida novo plano
   ├─ Evaluator re-avalia
   └─ Se APROVADO: novo ETA é comunicado ao cliente
5. Cliente recebe: "KODA: Pequeno ajuste na sua entrega. Novo horário: 16:45.
   Seu pedido ainda chega hoje. Desculpe o transtorno."
6. Se NENHUM entregador disponível:
   └─ Cliente recebe: "KODA: Tivemos um imprevisto com a entrega.
      Seu pedido chega amanhã às 10h, com frete grátis. Tudo bem para você?"
```

### Modo de Falha 4: Degradação do Evaluator (Overfitting de Rubrica)

**Cenário:** O Evaluator começa a rejeitar planos que deveriam ser aprovados — está "muito rigoroso". A taxa de falsos negativos sobe (não promete same-day quando poderia).

**Detecção:**
```
Métrica monitorada: "taxa_de_aprovacao_do_evaluator"

Normal: 82-88% dos planos são aprovados
Alerta: < 75% por mais de 1 hora
Crítico: < 65%

Possíveis causas:
- Mudança nas condições externas (trânsito pior, menos entregadores)
- Evaluator está com temperatura muito baixa (overfitting)
- Rubrica precisa de recalibragem
```

**Resposta do Sistema:**
```
1. Alerta é gerado: "Evaluator approval rate anômalo: 68% (normal: 82-88%)"
2. Time analisa os últimos 50 vereditos do Evaluator
3. Identifica padrão: "Dimensão 4 (margem de segurança) está baixando scores.
   Trânsito médio piorou 15% este mês."
4. Decisão: ajustar threshold de margem de segurança:
   Antes: buffer ≥ 90 min → 5pts
   Depois: buffer ≥ 75 min → 5pts (calibrado para nova realidade)
5. Próximos pedidos voltam à taxa normal de aprovação
```

### Modo de Falha 5: SQLite Corrompido

**Cenário:** Queda de energia durante escrita no SQLite causa corrupção no banco.

**Resposta do Sistema:**
```
1. Monitor detecta: SQLite não responde a queries
2. Sistema automaticamente:
   ├─ Isola o banco corrompido (renomeia para plans.db.corrupted.{timestamp})
   ├─ Restaura do último backup (backup a cada 5 minutos, retenção de 24h)
   ├─ Reconcilia com audit trail:
   │   └─ Lê audit_trail.jsonl desde o timestamp do backup
   │   └─ Re-executa transações registradas no audit trail
   │   └─ Estado é reconstruído com perda máxima de 5 minutos
   ├─ Alerta equipe: "SQLite recovered from backup. Data loss: max 5 min."
   └─ Continua operação normalmente
3. Equipe investiga causa raiz da corrupção posteriormente
```

**Impacto no cliente:** Planos em andamento no momento da falha podem ser perdidos. O Planner detecta timeouts e reinicia os planos afetados. Cliente pode experimentar um atraso de 30-60 segundos — o sistema se recupera sozinho.

### Modo de Falha 6: Ataque de Negação de Serviço nos Locks

**Cenário:** Um agente malicioso ou bugado adquire locks e nunca os libera (deadlock malicioso ou memory leak).

**Resposta do Sistema:**
```
Deadlock Detection Loop (roda a cada 15 segundos):

1. Scanner percorre todos os arquivos de lock ativos
2. Para cada lock:
   ├─ lock.expires_at < now?
   │  └─ Sim → lock EXPIROU → força release
   ├─ lock.age > 2x TTL?
   │  └─ Sim → possível deadlock → força release + alerta
   ├─ lock.owner_session ainda está ativa?
   │  └─ Não → sessão morreu → força release
   └─ Lock saudável → ignora

3. Locks liberados à força geram:
   ├─ Audit trail: "lock_force_released", motivo, lock_id
   ├─ Alerta: "Force-released 3 locks in last minute. Investigating."
   └─ Rollback seguro: desfaz operações parciais do owner original

4. Sistema continua operando. Recursos são liberados para outros planos.
```

### Tabela de Resiliência

| Modo de Falha | Detectado em | Recuperação | Impacto no Cliente | Intervenção Humana |
|---------------|-------------|-------------|-------------------|-------------------|
| Inventory indisponível | 3-9 segundos | Automática | Nenhum a leve | Não necessária |
| Race condition | Instantâneo | Automática | Nenhum | Não necessária |
| Entregador indisponível | 1-5 minutos | Automática | Leve (aviso de ajuste) | Não necessária |
| Evaluator overfitting | 1 hora (métrica) | Semi-automática | Moderado (menos same-day) | Sim (ajuste de rubrica) |
| SQLite corrompido | < 10 segundos | Automática | Leve (30-60s delay) | Sim (investigação post-mortem) |
| Lock denial-of-service | 15-45 segundos | Automática | Nenhum a leve | Sim (investigação) |

---

## 🏥 Operações e Monitoramento: Mantendo o Sistema Saudável

A arquitetura de long-running agents não termina no deploy. O time KODA aprendeu que operações são parte do design. Esta seção documenta como o sistema é monitorado, alertado e mantido.

### Dashboard de Saúde do Sistema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   KODA SAME-DAY DELIVERY — HEALTH DASHBOARD              │
│                   Atualizado a cada 60 segundos                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┬─────────────────────┬─────────────────────────────┐
│ TAXA DE SUCESSO     │ PLANOS ATIVOS        │ AVALIACOES (última hora)    │
│ Same-Day            │                      │                             │
│                     │                      │ ✅ Aprovados:  47 (84%)     │
│   ████████████████  │  ██████ 12           │ ❌ Rejeitados:  9 (16%)     │
│   94%               │                      │ 🔄 Em avaliacao: 3         │
│                     │  Em andamento         │                             │
└─────────────────────┴─────────────────────┴─────────────────────────────┘

┌─────────────────────┬─────────────────────┬─────────────────────────────┐
│ LOCKS ATIVOS         │ AGENTES              │ ESTOQUE CRÍTICO             │
│                     │                      │                             │
│ Inventory:  3       │ Planner:     ✅ UP  │ ⚠️ WHEY-001 (SP-ZL): 2 un   │
│ Dispatcher: 5       │ Inventory:   ✅ UP  │ ⚠️ CREATINE (SP-MOEMA): 1 un │
│ Plan:       12      │ Dispatch:    ✅ UP  │ ✅ BCAA-001: 89 un           │
│ Expirados:   0      │ Routing:     ✅ UP  │                             │
│ Force-rel:   0      │ Generator:   ✅ UP  │                             │
│                     │ Evaluator:   ✅ UP  │                             │
└─────────────────────┴─────────────────────┴─────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ LATÊNCIA MÉDIA (últimos 5 min)                                          │
│                                                                          │
│ Inventory Agent:   120ms ██                                              │
│ Dispatch Agent:    180ms ████                                            │
│ Routing Agent:     350ms ████████                                        │
│ Generator:         210ms █████                                           │
│ Evaluator:         580ms ██████████████                                  │
│ Pipeline Total:   1900ms ███████████████████████████████████████████████ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Alertas Configurados

| Alerta | Condição | Severidade | Canal | Runbook |
|--------|----------|-----------|-------|---------|
| **Taxa de sucesso same-day < 85%** | Média móvel de 1h abaixo de 85% | CRÍTICO | PagerDuty + Slack | Investigar causa raiz nos últimos 50 planos |
| **Lock force-release > 5/hora** | Mais de 5 locks liberados à força em 1h | ALTO | Slack #eng-alerts | Verificar deadlocks, memory leaks |
| **Avaliador approval < 70%** | Taxa de aprovação abaixo de 70% por > 30min | MÉDIO | Slack #eng-alerts | Verificar calibragem da rubrica |
| **Pipeline latency > 3s** | Latência total média > 3 segundos por > 10min | MÉDIO | Slack #eng-alerts | Verificar APIs externas, latência de rede |
| **Audit trail growth > 1GB/dia** | Crescimento anormal do audit trail | BAIXO | Slack #eng | Verificar compactação, possível bug de log |
| **SQLite connection failures** | Mais de 3 falhas de conexão em 5 min | CRÍTICO | PagerDuty + Slack | Iniciar recuperação de backup |
| **Agente offline > 2 min** | Qualquer agente sem heartbeat por > 2 min | ALTO | Slack #eng-alerts | Reiniciar agente, investigar crash |

### Runbook: Recuperação de Incidente Grave

```
PROCEDIMENTO: Queda total do sistema de same-day delivery

1. DETECÇÃO (automática):
   └─ Health check falha em 3 agentes simultaneamente
   └─ PagerDuty dispara para engenheiro on-call

2. TRIAGEM (engenheiro, 2-5 min):
   ├─ Acessar dashboard de saúde
   ├─ Identificar agente(s) afetado(s)
   ├─ Verificar logs: /var/log/koda/same-day/
   └─ Classificar severidade: parcial (≥ 1 agente UP) ou total

3. CONTENÇÃO (5-10 min):
   ├─ Se parcial: sistema continua operando com degradação
   │   └─ KODA Interface detecta e oferece next-day aos clientes
   ├─ Se total: ativar "modo de contingência"
   │   └─ KODA Interface: "Nosso sistema de entrega rápida está em
   │       manutenção. Posso processar seu pedido com entrega normal.
   │       Ofereço frete grátis como compensação."
   └─ Comunicar no canal #incidents

4. RECUPERAÇÃO (10-30 min):
   ├─ Reiniciar agentes afetados (systemd)
   ├─ Verificar SQLite: integridade do banco
   ├─ Verificar locks: force-release locks órfãos
   ├─ Rodar smoke test: "Plano de teste #9999"
   └─ Confirmar que pipeline voltou ao normal

5. PÓS-MORTEM (24-48h depois):
   ├─ Extrair audit trail do período do incidente
   ├─ Rodar script de análise de causa raiz
   ├─ Documentar: timeline, causa, impacto, ações
   ├─ Criar tickets para melhorias permanentes
   └─ Atualizar runbook se necessário
```

### Manutenção Programada

| Tarefa | Frequência | Duração | Impacto | Procedimento |
|--------|-----------|---------|---------|-------------|
| **Rotação de audit trail** | Diária (03:00 UTC) | < 1 min | Nenhum | Compactar logs > 7 dias, arquivar em cold storage |
| **Vacuum SQLite** | Semanal (Dom 04:00) | 2-5 min | Leve (locks pausados) | VACUUM para recuperar espaço, REINDEX |
| **Calibragem de rubrica** | Mensal | 1-2 horas | Nenhum | Analisar scores do mês, ajustar thresholds |
| **Teste de disaster recovery** | Trimestral | 4 horas | Moderado (ambiente staging) | Simular corrupção de SQLite, testar recuperação |
| **Atualização de modelos** | Conforme release | 2-4 horas | Leve (canary deploy) | Deploy gradual, monitorar métricas, rollback automático |

---

## 🎯 O Que Você Aprendeu (Resumo)

### Conceitos Aplicados do Programa

| Nível | Padrão | Como foi aplicado no case |
|-------|--------|---------------------------|
| **N1** | Context Management | KODA Interface mantém estado do cliente separado do histórico. Planner lê customer_context.json. |
| **N1** | Token Budgeting | KODA Interface reserva 15K tokens de buffer para processamento de fulfillment. |
| **N1** | Basic Harness | KODA nunca promete prazo sem aprovação do Evaluator. Harness obrigatório. |
| **N2** | Generator/Evaluator | Generator propõe plano de fulfillment. Evaluator verifica com rubrica rigorosa (score ≥ 80 para aprovar). |
| **N2** | Sprint Contracts | Cada agente tem input/output contracts explícitos. Violações são detectadas e logadas. |
| **N2** | Rubric Design | Rubrica SAME_DAY_VIABILITY com 4 dimensões, scores 0-5, aprovação ≥ 80. |
| **N2** | Trace Reading | Audit trail em JSONL cobre 100% das decisões. Scripts de debug reconstroem timelines. |
| **N3** | Multi-Agent Systems | Planner coordena 5 agentes especializados (Interface, Generator, Evaluator, Inventory, Dispatch, Routing). |
| **N3** | State Persistence | SQLite persiste plans, inventory snapshots, assignments, route_plans. Sobrevive a restarts. |
| **N3** | File-Based Coordination | Lock files com TTL impedem conflitos. Status files dão visibilidade. Manifestos documentam estrutura. |
| **N3** | Server-Side Compaction | Audit trails são rotacionados a cada 7 dias. Dados antigos são sumarizados para análise histórica. |
| **N3** | Harness Evolution | Componentes obsoletos (Fast Check, Promise Keeper, Rerouter) foram removidos com base em métricas. |
| **N4** | KODA Architecture | Template de arquitetura para features complexas. Padrão reaplicável a pagamentos, carrinho, recomendações. |
| **N4** | Feature Design Patterns | Estratégia híbrida de coordenação. Trade-offs documentados. Decisão baseada em evidências. |
| **N4** | Evaluation Rubrics KODA | Rubrica adaptada ao domínio de fulfillment. Dimensões específicas do negócio (margem de segurança). |

### Habilidades que Você Desenvolveu

- ✅ Diagnosticar falhas de coordenação em sistemas multi-agente
- ✅ Desenhar arquitetura com Generator/Evaluator para decisões críticas
- ✅ Implementar file-based coordination com locks, TTL e deadlock detection
- ✅ Persistir estado com SQLite para resiliência e rastreabilidade
- ✅ Criar rubricas de avaliação com dimensões ponderadas e thresholds
- ✅ Instrumentar sistemas com audit trail para trace reading
- ✅ Comparar estratégias de coordenação (centralizada, descentralizada, híbrida)
- ✅ Medir ROI de mudanças arquiteturais
- ✅ Extrair padrões reaplicáveis de implementações específicas

### Perguntas de Verificação

Antes de seguir, verifique seu entendimento:

1. **Por que os 3 MVPs falharam?** Consigo explicar a causa raiz de cada um.
2. **Qual o papel do Planner Agent?** Orquestra, mas não executa. Coordena, mas não decide sozinho.
3. **Por que locks com TTL?** Impede deadlocks permanentes e permite recuperação automática.
4. **Qual a diferença entre Generator e Evaluator?** Generator propõe (criativo), Evaluator verifica (crítico).
5. **Por que a estratégia híbrida foi escolhida?** Balanço entre coordenação global e otimização local.
6. **O que a rubrica impede?** Falsos positivos — prometer same-day quando não é seguro.
7. **Como o audit trail ajuda no debug?** Reconstroi timeline completa de qualquer decisão.
8. **Qual foi o ROI do projeto?** 183% em 6 meses, payback em 2.1 meses.

Se conseguiu responder todas com clareza, você entendeu o case study.

---

## 🔗 Próximos Passos

### Dentro do Nível 4

- **Módulo 01:** `01-koda-architecture.md` — Entenda a arquitetura macro do KODA e como este case se encaixa
- **Módulo 02:** `02-customer-journey-flows.md` — Mapeie as jornadas do cliente e os pontos de coordenação
- **Módulo 03:** `03-feature-design-patterns.md` — Aprofunde nos patterns de design para novas features
- **Próximo Case Study:** `case-study-02.md` — Case de otimização de custos com harness evolution

### Exercícios Práticos

#### Exercício 1: Modele a Feature de Pagamentos

**Objetivo:** Aplicar o template de arquitetura deste case study a uma feature diferente.

**Contexto:** O KODA quer implementar um sistema de pagamentos que suporte múltiplos métodos (cartão de crédito, PIX, boleto) com validação de fraude e conciliação automática.

**Tarefa:**
1. Identifique os agentes especializados necessários (mínimo 4)
2. Defina os Sprint Contracts de cada agente (input, output, guarantees)
3. Desenhe o fluxo de coordenação (Planner → Agentes → Generator → Evaluator)
4. Liste os lock files necessários e o que cada um protege
5. Crie uma rubrica de avaliação com 3-4 dimensões

**Template de Resposta:**
```
Agentes:
  ├─ [Nome do Agente 1]: [responsabilidade atômica]
  ├─ [Nome do Agente 2]: [responsabilidade atômica]
  └─ ...

Lock Files:
  ├─ payment_{order_id}.lock: protege [recurso]
  └─ ...

Rubrica:
  D1: [dimensão] (peso X%)
  D2: [dimensão] (peso Y%)
  Score mín: [valor]
```

**Tempo estimado:** 30-45 minutos

---

#### Exercício 2: Desenhe uma Rubrica Anti-Fraude

**Objetivo:** Criar uma rubrica de avaliação que balance segurança com experiência do cliente.

**Contexto:** O Fraud Detection Agent precisa avaliar cada transação. Falsos positivos (bloquear cliente legítimo) são tão ruins quanto falsos negativos (deixar fraude passar).

**Tarefa:**
1. Defina 4 dimensões de avaliação com seus respectivos pesos
2. Para cada dimensão, defina os critérios de score (0 a 5 pontos)
3. Defina o score mínimo para aprovação automática
4. Defina a zona cinzenta (que requer revisão humana)
5. Explique como você balancearia falsos positivos vs falsos negativos

**Dimensões sugeridas para considerar:**
- Histórico do cliente no KODA
- Valor e frequência da transação
- Consistência de dados (nome, CPF, endereço)
- Padrão de comportamento (horário, localização, device)

**Tempo estimado:** 30-45 minutos

---

#### Exercício 3: Implemente um Lock File System

**Objetivo:** Implementar um sistema de lock files com TTL e deadlock detection em Python.

**Especificação:**
```python
# Implemente as seguintes funções:

def acquire_lock(resource: str, owner: str, ttl_seconds: int = 30) -> dict:
    """
    Tenta adquirir lock para um recurso.
    
    Args:
        resource: nome do recurso (ex: "inventory_SP-ZL_WHEY-001")
        owner: identificador do dono (ex: "INVENTORY_AGENT")
        ttl_seconds: tempo de vida do lock
    
    Returns:
        {"acquired": True, "lock_id": "..."} ou
        {"acquired": False, "reason": "...", "holder": "..."}
    
    Regras:
    - Lock é um arquivo JSON: {resource}.lock.json
    - Se arquivo NÃO existe: cria e adquire
    - Se arquivo existe e expirou: remove antigo, cria novo
    - Se arquivo existe e ativo: retorna não adquirido
    - Operação de criação do arquivo deve ser atômica
    """

def release_lock(lock_id: str) -> bool:
    """
    Libera um lock previamente adquirido.
    Só o owner pode liberar seu próprio lock.
    """

def check_deadlocks(lock_dir: str) -> list:
    """
    Verifica todos os locks no diretório.
    Retorna lista de locks que excederam 2x TTL.
    """

def force_release(lock_id: str, reason: str) -> bool:
    """
    Força liberação de um lock (para recuperação de deadlock).
    Registra em audit trail o motivo.
    """
```

**Testes mínimos:**
1. Dois owners tentam adquirir o mesmo lock → segundo falha
2. Lock expira e um novo owner consegue adquirir
3. Deadlock detection encontra lock com 3x TTL
4. Force release funciona e registra em audit trail
5. Release por owner errado falha

**Tempo estimado:** 60-90 minutos

---

#### Exercício 4: Trace Reading — Diagnosticando uma Falha

**Objetivo:** Analisar um audit trail simulado e identificar a causa raiz de uma falha de same-day delivery.

**Cenário:** O Pedido #9056 foi prometido para same-day delivery às 16:30, mas não foi entregue. O cliente reclamou. Você recebeu o audit trail abaixo.

**Audit Trail (simplificado):**
```jsonl
{"ts":"14:00:00","event":"plan_created","plan_id":"PLAN-9056","customer_id":"wa_5511..."}
{"ts":"14:00:01","event":"lock_acquired","resource":"inventory_SP-ZL_WHEY-001","owner":"INVENTORY_AGENT"}
{"ts":"14:00:02","event":"inventory_reserved","sku":"WHEY-001","qty":2,"warehouse":"SP-ZL"}
{"ts":"14:00:03","event":"lock_released","resource":"inventory_SP-ZL_WHEY-001"}
{"ts":"14:00:04","event":"lock_acquired","resource":"dispatcher_ENTREGADOR-007","owner":"DISPATCH_AGENT"}
{"ts":"14:00:05","event":"dispatcher_assigned","dispatcher":"ENTREGADOR-007","status":"assigned"}
{"ts":"14:00:06","event":"lock_released","resource":"dispatcher_ENTREGADOR-007"}
{"ts":"14:00:07","event":"route_calculated","origin":"SP-ZL","dest":"Moema","eta_min":38}
{"ts":"14:00:08","event":"generation_completed","plan_id":"PLAN-9056","confidence":0.91}
{"ts":"14:00:09","event":"evaluation_started","evaluator":"EVAL_AGENT"}
{"ts":"14:00:10","event":"evaluation_completed","score":92,"verdict":"APPROVED"}
{"ts":"14:00:11","event":"plan_approved","delivery_eta":"16:08","plan_id":"PLAN-9056"}
{"ts":"14:00:12","event":"customer_notified","eta":"16:08"}
{"ts":"15:15:00","event":"dispatcher_status_change","dispatcher":"ENTREGADOR-007","from":"assigned","to":"unavailable","reason":"vehicle_breakdown"}
{"ts":"15:15:01","event":"dispatcher_unavailable_alert","plan_id":"PLAN-9056","dispatcher":"ENTREGADOR-007"}
{"ts":"15:15:02","event":"reroute_started","plan_id":"PLAN-9056","reason":"dispatcher_lost"}
{"ts":"15:15:03","event":"lock_acquired","resource":"dispatcher_ENTREGADOR-012","owner":"DISPATCH_AGENT"}
{"ts":"15:15:04","event":"lock_released","resource":"dispatcher_ENTREGADOR-012","reason":"dispatcher_weight_limit_exceeded"}
{"ts":"15:15:05","event":"lock_acquired","resource":"dispatcher_ENTREGADOR-003","owner":"DISPATCH_AGENT"}
{"ts":"15:15:06","event":"dispatcher_assigned","dispatcher":"ENTREGADOR-003","status":"assigned"}
{"ts":"15:15:07","event":"lock_released","resource":"dispatcher_ENTREGADOR-003"}
{"ts":"15:15:08","event":"route_calculated","origin":"SP-ZL","dest":"Moema","eta_min":52,"traffic":"heavy"}
{"ts":"15:15:09","event":"generation_completed","plan_id":"PLAN-9056","confidence":0.72}
{"ts":"15:15:10","event":"evaluation_started","evaluator":"EVAL_AGENT"}
{"ts":"15:15:11","event":"evaluation_completed","score":71,"verdict":"REJECTED","reason":"routing_score_low_and_safety_margin_insufficient"}
{"ts":"15:15:12","event":"feedback_to_generator","issues":["route_eta_52min_too_high","safety_margin_below_threshold"]}
{"ts":"15:15:13","event":"generation_completed","plan_id":"PLAN-9056_v3","confidence":0.68,"attempt":3}
{"ts":"15:15:14","event":"evaluation_completed","score":68,"verdict":"REJECTED","attempt":3}
{"ts":"15:15:15","event":"max_iterations_reached","plan_id":"PLAN-9056","attempts":3}
{"ts":"15:15:16","event":"plan_failed","reason":"max_iterations","escalated_to":"human_operator"}
{"ts":"15:15:17","event":"human_operator_notified","plan_id":"PLAN-9056","eta_response":"30_minutes"}
{"ts":"15:45:00","event":"human_operator_action","action":"manual_dispatch","dispatcher":"ENTREGADOR-022","eta":"18:30"}
{"ts":"15:45:01","event":"customer_notified","eta":"18:30","compensation":"free_shipping"}
```

**Perguntas:**
1. Qual foi a causa raiz da falha? Em que timestamp ela começou?
2. Por que o re-roteamento falhou na primeira tentativa (ENTREGADOR-012)?
3. Por que o plano v3 (terceira tentativa) foi rejeitado? O Evaluator foi muito rigoroso?
4. Quanto tempo o cliente esperou entre a promessa original (16:08) e a resolução (18:30)?
5. Que melhoria de sistema poderia ter evitado ou reduzido o impacto desta falha?
6. O tempo de resposta do operador humano (30 min) foi aceitável? Como poderia ser melhorado?

**Tempo estimado:** 45-60 minutos

---

#### Exercício 5: Proponha uma Evolução de Harness

**Objetivo:** Aplicar o padrão de Harness Evolution (N3) para propor remoção ou substituição de componentes.

**Contexto:** Após 6 meses de operação, o time KODA nota que:
- O Routing Agent consome 35% do tempo de pipeline, mas sua precisão melhorou apenas 3% em relação a uma estimativa simples baseada em distância
- 92% das rotas são "diretas" (< 15 km), onde o trânsito raramente afeta o ETA em mais de 10 minutos
- O custo mensal do Routing Agent (chamadas API + LLM) é de R$ 2.400

**Tarefa:**
1. Analise se o Routing Agent como está implementado ainda agrega valor
2. Proponha uma versão simplificada para rotas curtas (< 15 km)
3. Mantenha a versão completa para rotas longas (> 15 km) ou horários de pico
4. Estime a economia de custo e o impacto na precisão
5. Escreva uma ADR (Architecture Decision Record) de 1 parágrafo justificando a mudança

**Template de ADR:**
```
# ADR: [Titulo]
  Status: [Proposed / Accepted / Deprecated]
  Context: [Por que esta decisao e necessaria]
  Decision: [O que decidimos]
  Consequences: [O que fica melhor, pior, ou diferente]

Conteudo de cada secao em paragrafos claros.
```

**Tempo estimado:** 30-45 minutos

---

### Leituras Relacionadas

- `docs/canonical/koda-architecture-overview.md` — Documentação oficial da arquitetura KODA
- `docs/decisions/006-same-day-architecture.md` — ADR da decisão de arquitetura híbrida
- `docs/evidence/same-day-metrics-dashboard.md` — Métricas em tempo real do sistema

---

## 📊 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | case-study-01.md |
| **Nível** | 4 - KODA-Específico |
| **Tipo** | Case Study |
| **Tempo** | 90-120 minutos |
| **Status** | ✅ Completo |
| **Pré-requisitos** | Níveis 1, 2 e 3 completos + Módulos 01-03 do Nível 4 |
| **Feature KODA** | Same-Day Delivery (Fulfillment) |
| **Padrões aplicados** | 11 de 16 padrões do programa |
| **Data** | Maio 2026 |
| **Próximo** | case-study-02.md (Otimização de Custos) |

---

*Escrito com base na experiência real do time KODA refatorando o sistema de same-day delivery.*
*Este case study é o documento de referência para qualquer feature complexa que envolva coordenação multi-agente no KODA.*

---

## 📋 Architecture Decision Records (ADRs)

Durante o projeto, o time documentou decisões arquiteturais críticas no formato ADR. Esta seção reproduz as 4 ADRs mais importantes, no formato compacto usado pelo time KODA.

### ADR-001: Estratégia de Coordenação Híbrida

```
Status: ACCEPTED
Data: 2026-03-15
Deciders: Fernando (CTO), Tech Lead, 2 Senior Engineers

CONTEXT:
Precisamos decidir como os agentes do sistema de same-day delivery
vão se coordenar. Três opções foram consideradas:

1. CENTRALIZADA: Planner controla tudo, agentes são passivos
2. DESCENTRALIZADA: Agentes negociam entre si, sem orquestrador
3. HÍBRIDA: Planner coordena macro, agentes otimizam micro

DECISION:
Adotamos a estratégia HÍBRIDA.

RATIONALE:
- Estado compartilhado (estoque, entregadores) exige coordenação
  central para evitar conflitos → Planner é necessário
- Cada agente especializado conhece seu domínio melhor que o Planner
  → autonomia local melhora qualidade das decisões
- Deadlocks são gerenciáveis com TTL + force-release
- Estratégia escala melhor que centralizada pura e é mais simples
  de debugar que descentralizada pura

CONSEQUENCES:
✅ Melhor balanço entre coordenação global e otimização local
✅ Debug é viável (audit trail hierárquico)
✅ Pode evoluir para descentralizada se volume crescer 10x
⚠️ Implementação mais complexa que centralizada
⚠️ Requer disciplina nos Sprint Contracts entre Planner e agentes
```

### ADR-002: SQLite como State Store

```
Status: ACCEPTED
Data: 2026-03-18
Deciders: Tech Lead, DevOps Lead

CONTEXT:
Precisamos de um mecanismo de persistência de estado para o sistema
de same-day delivery. Opções consideradas:

1. PostgreSQL (banco externo)
2. Redis (cache persistente)
3. SQLite (banco embarcado)
4. Arquivos JSON (file-based)

DECISION:
SQLite como state store primário, JSON files como fallback.

RATIONALE:
- Volume atual (~340 pedidos/dia, ~2000 transações/dia) é bem
  suportado por SQLite
- Zero dependências externas (sem servidor de banco para gerenciar)
- Backup simples: copiar o arquivo .db
- Transações ACID garantem atomicidade nas reservas de inventário
- WAL mode permite leituras concorrentes sem bloquear escritas
- JSON files servem como fallback e fonte de verdade alternativa
- Migração para PostgreSQL é possível se volume crescer 10x

CONSEQUENCES:
✅ Simplicidade operacional (sem DBA, sem servidor)
✅ Transações ACID para operações críticas
✅ Backup e restore triviais
⚠️ Write concurrency limitado (single-writer)
⚠️ Não escala horizontalmente (mas não precisamos ainda)
⚠️ Monitoramento de integridade precisa ser implementado
```

### ADR-003: Lock Files com TTL vs Distributed Lock Manager

```
Status: ACCEPTED
Data: 2026-03-22
Deciders: Tech Lead, 2 Senior Engineers

CONTEXT:
Precisamos de um mecanismo de locking para impedir race conditions
em recursos compartilhados (estoque, entregadores). Opções:

1. Redis-based distributed lock (Redlock)
2. ZooKeeper/etcd
3. File-based locks com TTL

DECISION:
File-based locks com TTL de 30-60 segundos.

RATIONALE:
- Volume de locks é baixo (~500 locks/dia)
- File-based locks são inspecionáveis diretamente (cat file.json)
- Audit trail natural: o lock file é o registro
- TTL previne deadlocks permanentes
- Deadlock detection via scanner de locks expirados
- Não introduz dependência externa (Redis/ZK)
- Atomicidade via filesystem (O_EXCL | O_CREAT)
- Se o volume crescer, migrar para Redis é direto (mesmo padrão)

CONSEQUENCES:
✅ Simplicidade máxima (arquivos no filesystem)
✅ Debug trivial (ler o arquivo de lock)
✅ Sem single-point-of-failure externo
⚠️ Performance depende do filesystem (mas volume é baixo)
⚠️ Precisa de scanner de deadlocks (implementado em 2 dias)
⚠️ Não funciona em filesystems distribuídos (NFS pode ter
   problemas com O_EXCL — mas usamos filesystem local)
```

### ADR-004: Evaluator com Rubrica Ponderada vs Regras Determinísticas

```
Status: ACCEPTED
Data: 2026-03-28
Deciders: Fernando (CTO), Tech Lead, ML Engineer

CONTEXT:
O Evaluator precisa decidir se um plano de same-day delivery é
viável. Duas abordagens:

1. REGRAS DETERMINÍSTICAS: if-else baseado em thresholds
   (estoque > 0 AND entregador livre AND rota < 40min)
2. RUBRICA COM LLM: avaliar múltiplas dimensões com julgamento
   contextual (estoque suficiente? entregador confiável?
   margem de segurança adequada?)
3. HÍBRIDA: regras para decisões binárias + LLM para nuanced

DECISION:
HÍBRIDA: regras determinísticas para "deal-breakers" (estoque = 0
→ rejeição automática), LLM com rubrica para avaliação qualitativa
(margem de segurança, risco de trânsito, confiabilidade do
entregador).

RATIONALE:
- Verificações binárias (estoque > 0) são triviais e determinísticas
  → não justificam custo de LLM call
- Avaliações contextuais ("buffer de 30 min é suficiente?") exigem
  julgamento → LLM é superior a regras rígidas
- Temperatura 0.2 garante consistência nas avaliações
- Rubrica com scoring (0-5 por dimensão) torna o processo auditável
- Feedback específico do Evaluator melhora o Generator ao longo
  do tempo (learning loop implícito)
- Custo adicional do LLM (R$ 0.02 por avaliação) é justificado
  pela redução de falsos positivos (38% → 6%)

CONSEQUENCES:
✅ Melhor balanço entre precisão e custo
✅ Decisões de rejeição são explicáveis (rubric scores)
✅ Regras determinísticas cobrem casos óbvios sem custo
⚠️ Rubrica precisa de calibragem periódica (mensal)
⚠️ Dependência de LLM para avaliações nuanced (mas com fallback
   para regras se LLM indisponível)
⚠️ Overfitting da rubrica é possível (monitorado via métrica de
   approval rate)
```

---

## 🔄 Estratégia de Migração: Do Legado ao Novo Sistema

Migrar um sistema em produção sem downtime, especialmente um que processa pedidos e lida com promessas de entrega, exige cuidado. O time KODA executou a migração em 4 fases ao longo de 3 semanas.

### Fase 1: Shadow Mode (Semana 1)

O novo sistema roda em paralelo com o antigo, mas suas decisões não afetam clientes reais.

```
┌─────────────────┐         ┌─────────────────┐
│ SISTEMA ANTIGO  │────────▶│ CLIENTE          │
│ (em produção)   │         │ (recebe resposta) │
└─────────────────┘         └─────────────────┘

┌─────────────────┐         ┌─────────────────┐
│ SISTEMA NOVO    │────────▶│ SHADOW LOG       │
│ (shadow mode)   │         │ (análise apenas) │
└─────────────────┘         └─────────────────┘

Objetivo: Comparar decisões dos dois sistemas sem impacto.
Métrica: "Taxa de concordância" entre sistema antigo e novo.
Resultado: 87% de concordância nas primeiras 48h.
          13% de discordância analisados manualmente.
          → 10% eram o sistema novo certo e o antigo errado.
          → 3% eram bugs no sistema novo (corrigidos antes da Fase 2).
```

### Fase 2: Canary Release (Semana 2)

10% do tráfego real é roteado para o novo sistema. Clientes reais recebem respostas do novo sistema, mas com fallback automático para o antigo se algo falhar.

```
Critérios de promoção:
- Taxa de sucesso same-day ≥ 85% (vs 62% do antigo)
- Latência média < 3s
- Zero incidentes críticos em 48h

Resultado: Todos os critérios atingidos em 72h.
```

### Fase 3: Gradual Rollout (Semanas 2-3)

Incremento gradual: 10% → 25% → 50% → 75% → 100%.

```
Cada incremento requer:
- 24h de operação estável no patamar atual
- Métricas dentro dos thresholds
- Zero regressões detectadas

Duração total: 12 dias até 100%.
```

### Fase 4: Descomissionamento (Semana 4)

Sistema antigo é desligado. Componentes obsoletos (Fast Check, Promise Keeper, Rerouter) são removidos. Documentação é atualizada.

```
Removido:
- MVP1 "Fast Check" (3 chamadas API sequenciais)
- MVP2 "Promise Keeper" (worker de 15 minutos)
- MVP3 "Rerouter" (sistema de re-roteamento legado)
- Planilha Excel de entregas (finalmente!)

Economia: R$ 1.800/mês em infraestrutura obsoleta.
```

---

## ❓ Perguntas Frequentes

### P: "Por que não usar uma fila de mensagens (RabbitMQ/Kafka) em vez de file-based coordination?"

**R:** Ótima pergunta! Para o volume atual do KODA (~340 pedidos/dia), file-based coordination é suficiente e tem vantagens:
1. Zero dependências externas (sem broker para gerenciar)
2. Debug simples (arquivos são inspecionáveis diretamente)
3. Audit trail natural (arquivos são o próprio log)

Se o volume crescer 10x, uma fila de mensagens seria recomendada. O design com locks e TTL é compatível com essa migração futura.

### P: "O Evaluator não poderia ser substituído por regras determinísticas?"

**R:** Parcialmente. Verificações como "estoque > 0" podem ser determinísticas. Mas avaliações como "margem de segurança adequada" ou "risco de trânsito" se beneficiam do julgamento do LLM. O design atual usa LLM para avaliação qualitativa e regras determinísticas para verificações binárias (estoque = 0 → rejeição automática).

### P: "Qual o custo de latência de todo esse pipeline?"

**R:** O pipeline completo (Planner → Inventory → Dispatch → Routing → Generator → Evaluator) leva em média 1.9 segundos. Os agentes rodam em paralelo onde possível. O maior custo de latência é o Evaluator (0.6s), mas ele roda apenas 1-2 vezes por pedido.

### P: "O que acontece se o SQLite corromper?"

**R:** O SQLite tem backup automático a cada 5 minutos. O audit trail em JSONL é independente e serve como fonte de verdade secundária. Em caso de corrupção, o sistema restaura do backup e reconcilia com o audit trail.

### P: "Este padrão funciona para features menores?"

**R:** Sim, mas com simplificações. Para features simples (ex: validação de cupom), você pode usar apenas Generator/Evaluator + SQLite, sem Planner e sem locks. O template é escalável: use os componentes que fizerem sentido para a complexidade da feature.

---

*Case Study 01 — Same-Day Delivery — Documento de Referência para Features Complexas no KODA*
