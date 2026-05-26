# 🧬 Solucao: Exercicio 3 — Harness Evolution
## Plano de Evolucao Completo para o Harness de um Agente de Recomendacao com 3 Fases

**Tempo Estimado:** 60-90 minutos
**Nivel:** 3 — Arquitetura Avancada
**Pre-requisito:** Ter lido `05-harness-evolution.md` e completado Exercicios 1 e 2 do Nivel 3
**Status:** Solucao Completa — Modelo de Referencia
**Data de Criacao:** Maio 2026

---

## 📖 Prologo: O Dia em Que Mariana Herdou um Harness de 14 Componentes

**Quarta-feira, 14h30. Sala de arquitetura do time Yggdrasil Supplements.**

Mariana acabara de ser promovida a Tech Lead do time de agentes. Seu primeiro desafio na nova posicao era um que ninguem queria pegar: revisar o harness do agente de recomendacao de suplementos, carinhosamente apelidado de "Golem" pelo time.

Golem estava em producao havia 9 meses. Funcionava — os clientes recebiam recomendacoes corretas na maioria das vezes. Mas "funcionar" ja nao era suficiente.

```
┌──────────────────────────────────────────────────────────────────┐
│                    GOLEM HARNESS v2.1 — Estado Atual              │
│                                                                  │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐          │
│  │ Context     │──▶│ Deduplication│──▶│ Critical     │          │
│  │ Hydrator    │   │ Engine       │   │ Tag Marker   │          │
│  │ (550ms)     │   │ (250ms)      │   │ (180ms)      │          │
│  └─────────────┘   └──────────────┘   └──────────────┘          │
│        │                 │                    │                   │
│        ▼                 ▼                    ▼                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               Core Pipeline                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │ Intent   │─▶│ Product  │─▶│ Generator│─▶│ Constraint│  │   │
│  │  │ Classifier│ │ Selector │  │ Agent    │  │ Validator │  │   │
│  │  │ (300ms)  │  │ (400ms)  │  │ (900ms)  │  │ (350ms)   │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               Validation Stack                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │ Format   │─▶│ Allergen ▶│  │ Budget   │─▶│ Fallback │  │   │
│  │  │ Enforcer │  │ Filter    │  │ Governor  │  │ Resolver │  │   │
│  │  │ (120ms)  │  │ (250ms)   │  │ (200ms)   │  │ (400ms)  │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               Audit Layer                                  │   │
│  │  ┌──────────┐  ┌──────────┐                               │   │
│  │  │ Trace    │─▶│ Decision │                               │   │
│  │  │ Recorder │  │ Archiver │                               │   │
│  │  │ (180ms)  │  │ (100ms)  │                               │   │
│  │  └──────────┘  └──────────┘                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  LATENCIA MEDIA POR TURNO: 3780ms                                │
│  TOKENS POR TURNO: ~3800                                         │
│  COMPONENTES ATIVOS: 14                                          │
│  CUSTO MENSAL API: R$ 6.400                                      │
│  HORAS MANUTENCAO/MES: 22h                                       │
└──────────────────────────────────────────────────────────────────┘
```

O diagrama ocupava a parede inteira. Quatorze componentes. Tres camadas. Cada um com seu proposito documentado. Cada um adicionado por uma boa razao em algum momento dos ultimos 9 meses.

```
Mariana: "Gente, antes de comecar, quero que cada um puxe no dashboard 
         as metricas do componente que criou."

Dev A (Context Hydrator): "550ms de latencia. 1400 tokens por turno. 
    12 prevencoes reais nos ultimos 90 dias."

Dev B (Deduplication Engine): "250ms. 600 tokens. 3 prevencoes reais. 
    Mas 89 falsos positivos — removeu informacao que era relevante 
    mas parecia duplicada."

Dev C (Intent Classifier): "300ms. 850 tokens. 47 acionamentos. 
    Desses, 41 foram classificacoes corretas, 6 erradas."

Dev D (Format Enforcer): "120ms. 300 tokens. Zero violacoes de formato 
    nos ultimos 90 dias. O modelo atual — Claude v3 — produz JSON 
    valido consistentemente."

Dev E (Budget Governor): "200ms. 400 tokens. Zero disparos em 180 dias. 
    A janela de contexto foi de 32K para 200K. Nunca chegamos perto 
    do limite novo."

Dev F (Allergen Filter): "250ms. 500 tokens. 145 prevencoes reais. 
    Zero falsos positivos. Esse aqui salvou 3 clientes com alergias 
    graves nos ultimos 90 dias."
```

O silencio que se seguiu foi revelador. Alguns componentes eram herois silenciosos. Outros eram peso morto que ninguem tinha coragem de remover.

```
Mariana: "Temos 14 componentes. Tres deles — Context Hydrator, 
         Deduplication Engine, Budget Governor — juntos consomem 
         1000ms de latencia, 2400 tokens por turno e previnem 
         menos de 1% dos erros reais."

Dev A: "Mas o Context Hydrator foi o primeiro componente que eu 
       construi aqui. Ele funciona."

Mariana: "Funciona para que? O modelo de 9 meses atras esquecia 
         informacao depois de 30 minutos de conversa. O modelo 
         de hoje — Claude v3, 200K tokens de contexto, 98% de 
         retencao em 100K tokens — nao esquece mais."

Dev B: "Entao... a gente remove?"

Mariana: "A gente nao 'remove'. A gente evolui. Com processo, 
         com dados, com seguranca. Em tres fases. E e exatamente 
         isso que vamos planejar hoje."
```

Este documento e a resposta da Mariana. E o plano completo de evolucao do harness do Golem — da versao inchada de 14 componentes ate uma arquitetura essencial de 7 componentes. Tres fases. Cada fase com suas decisoes, suas metricas, seus riscos e suas mitigacoes.

---

## 🎯 O Que Este Exercicio Pede

### Enunciado Original

> Voce e o Tech Lead de um agente de recomendacao que esta em producao ha 9 meses. O harness atual tem 14 componentes, muitos dos quais foram criados para proteger um modelo que ja nao e o mesmo. Sua tarefa e elaborar um plano de evolucao em 3 fases, detalhando:
> 1. Quais componentes serao removidos, simplificados ou mantidos em cada fase
> 2. A justificativa tecnica baseada em metricas para cada decisao
> 3. Os riscos especificos de cada remocao e como mitiga-los
> 4. O impacto esperado em latencia, tokens e complexidade
> 5. Como a coordenacao entre componentes muda apos cada fase

### Estrutura da Solucao

Esta solucao esta organizada em 6 secoes principais:

| Secao | Conteudo | Pagina Mental |
|-------|----------|---------------|
| **1. Avaliacao Inicial** | Classificacao dos 14 componentes com metricas e justificativas | "O que temos e o que vale a pena manter?" |
| **2. Fase 1 — Remover o Obviamente Desnecessario** | 3 remocoes de baixo risco com evidencias contundentes | "Arrancar o peso morto primeiro" |
| **3. Fase 2 — Simplificar o Redundante** | 3 simplificacoes/consolidacoes com shadow testing | "Juntar o que faz a mesma coisa" |
| **4. Fase 3 — Evoluir para o Essencial** | 1 absorcao estrutural + reavaliacao final | "O harness minimo que entrega o mesmo valor" |
| **5. Tabela Comparativa de Coordenacao** | Antes, durante e depois — como a orquestracao muda | "Menos componentes = menos coordenacao necessaria" |
| **6. KODA Application** | Paralelo com a evolucao real do harness KODA | "O que o Golem ensina sobre o KODA" |

---

## 🔍 1. Avaliacao Inicial: Classificando os 14 Componentes

Antes de planejar qualquer evolucao, e necessario classificar cada componente em uma das quatro categorias do ciclo de vida do harness.

### Metodologia de Classificacao

Cada componente foi avaliado em 5 dimensoes, cada uma com peso de 0 a 4 pontos (maximo 20 pontos):

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SCORECARD DE AVALIACAO                            │
│                                                                     │
│  Dimensao          Peso   Pergunta-Chave                             │
│  ─────────────────────────────────────────────────────────────────  │
│  Taxa de Acion.    0-4    Quantos % dos turns este componente        │
│                           realmente previne um erro?                 │
│                           (4 = > 5%, 3 = 1-5%, 2 = 0.1-1%,          │
│                            1 = < 0.1%, 0 = nunca dispara)            │
│                                                                     │
│  Custo Operac.     0-4    Qual o custo em tokens + latencia?        │
│                           (4 = < 100 tokens, 3 = 100-300,           │
│                            2 = 300-600, 1 = 600-1000, 0 = > 1000)   │
│                                                                     │
│  Falsos Posit.     0-4    Quantos fluxos corretos bloqueia?         │
│                           (4 = zero FPs, 3 = < 1x prevencoes,       │
│                            2 = 1-3x, 1 = 3-10x, 0 = > 10x)         │
│                                                                     │
│  Cobertura Mod.    0-4    O modelo atual cobre esta protecao?       │
│                           (4 = modelo nao cobre, 3 = cobre          │
│                            parcialmente, 2 = cobre bem,              │
│                            1 = cobre quase totalmente,               │
│                            0 = cobre completamente)                  │
│                                                                     │
│  Invariante?       0-4    E uma protecao permanente do dominio?     │
│                           (4 = seguranca/compliance,                 │
│                            3 = decisao irreversivel,                 │
│                            2 = auditabilidade,                       │
│                            1 = qualidade, 0 = conveniencia)          │
│                                                                     │
│  PONTUACAO FINAL:  0-20                                            │
│    0-5  = REMOVE (remova com confianca)                             │
│    6-10 = SIMPLIFY (reduza escopo, consolide)                       │
│    11-15 = KEEP (mantenha, otimize parametros)                      │
│    16-20 = PROTECT (invariante — nunca remova)                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Tabela de Classificacao — Estado Atual (Maio 2026)

| # | Componente | Acion. | Custo | FPs | Cob. Mod. | Invar. | Score | Acao |
|---|-----------|--------|-------|-----|-----------|--------|-------|------|
| 1 | Context Hydrator | 0.008% (1) | 0 (1400tk/550ms) | 28x FPs (0) | Modelo cobre (0) | 0 | **3** | 🟡 SIMPLIFY (absorver) |
| 2 | Deduplication Engine | 0.002% (1) | 1 (600tk/250ms) | 30x FPs (0) | Modelo cobre (1) | 0 | **3** | 🔴 REMOVE |
| 3 | Critical Tag Marker | 0.05% (1) | 2 (400tk/180ms) | 2x FPs (2) | Cobre parcial (2) | 0 | **7** | 🟡 SIMPLIFY |
| 4 | Intent Classifier | 0.03% (1) | 2 (850tk/300ms) | 15% erros (2) | Cobre bem (2) | 0 | **7** | 🟡 SIMPLIFY |
| 5 | Product Selector | 8.2% (4) | 2 (600tk/400ms) | 1x FPs (2) | Nao cobre (4) | 1 (qualidade) | **13** | 🟢 KEEP |
| 6 | Generator Agent | 100% (4) | 2 (1200tk/900ms) | N/A | Nao cobre (4) | 2 (audit.) | **12** | 🟢 KEEP |
| 7 | Constraint Validator | 2.1% (3) | 2 (500tk/350ms) | 0.5x FPs (3) | Cobre parcial (3) | 2 (qualidade) | **13** | 🟢 KEEP |
| 8 | Format Enforcer | 0% (0) | 3 (300tk/120ms) | N/A | Cobre compl. (0) | 0 | **3** | 🔴 REMOVE |
| 9 | Allergen Filter | 8.5% (4) | 2 (500tk/250ms) | 0 FPs (4) | Nao cobre (4) | 4 (segur.) | **18** | 🛡️ PROTECT |
| 10 | Budget Governor | 0% (0) | 2 (400tk/200ms) | N/A | Cobre compl. (0) | 0 | **2** | 🔴 REMOVE |
| 11 | Fallback Resolver | 0.8% (2) | 2 (800tk/400ms) | 0 FPs (4) | Cobre parcial (3) | 2 (disp.) | **13** | 🟢 KEEP |
| 12 | Trace Recorder | 100% (4) | 2 (300tk/180ms) | 0 FPs (4) | Nao cobre (4) | 3 (audit.) | **17** | 🛡️ PROTECT |
| 13 | Decision Archiver | 100% (4) | 3 (150tk/100ms) | 0 FPs (4) | Nao cobre (4) | 2 (audit.) | **17** | 🛡️ PROTECT |
| 14 | Pre-Validation Hook | 0.01% (1) | 2 (350tk/150ms) | 8x FPs (1) | Cobre bem (2) | 0 | **6** | 🟡 SIMPLIFY |

### Resumo da Classificacao

```
COMPONENTES POR CATEGORIA:

🛡️ PROTECT (3):  Allergen Filter, Trace Recorder, Decision Archiver
                  → Nunca remova. Invariantes de seguranca e auditoria.

🟢 KEEP (4):      Product Selector, Generator Agent, Constraint Validator,
                  Fallback Resolver
                  → Mantenha. Entregam valor comprovado e consistente.

🟡 SIMPLIFY (4):  Context Hydrator, Critical Tag Marker, Intent Classifier, Pre-Validation Hook
                  → Reduza escopo ou consolide com outro componente.

🔴 REMOVE (4):    Context Hydrator, Deduplication Engine, Format Enforcer,
                  Budget Governor
                  → Remova. Metricas mostram custo >> valor.
```

Os 3 componentes marcados para remocao (Budget Governor, Format Enforcer, Deduplication Engine) consomem, juntos:
- **1080ms de latencia** (28.6% do total de 3780ms)
- **2700 tokens por turno** (71% dos 3800 tokens de overhead)
- **R$ 2.100/mes em custo de API** (33% do custo mensal de R$ 6.400)
- **8h/mes de manutencao** (36% das 22h mensais)

E previnem, combinados, apenas 0.01% dos erros reais em producao.

---

## 🗑️ 2. Fase 1 — Remover o Obviamente Desnecessario (Semanas 1-4)

**Objetivo:** Remover os componentes com score mais baixo (0-3) que tem evidencias contundentes de desnecessidade. Zero risco estrutural — sao componentes cuja funcao o modelo atual ja cobre totalmente.

**Mindset:** "Arrancar o peso morto primeiro." Nao ha duvida sobre estes. As metricas sao inequivocas. O modelo atual tornou estas protecoes redundantes.

### Componentes Removidos Nesta Fase

```
┌──────────────────────────────────────────────────────────────────┐
│                   FASE 1 — REMOCOES (3 componentes)               │
│                                                                  │
│  🔴 Budget Governor        (score: 2)                            │
│  🔴 Format Enforcer        (score: 3)                            │
│  🔴 Deduplication Engine   (score: 3)                            │
│                                                                  │
│  Impacto Agregado:                                               │
│  Latencia:    -570ms (-15.1%)                                    │
│  Tokens:      -1300/turno (-34.2%)                               │
│  Componentes: 14 → 11                                            │
│  Custo/mes:   -R$ 980                                            │
└──────────────────────────────────────────────────────────────────┘
```

### 2.1 Budget Governor — Justificativa de Remocao

**O que fazia:** Monitorava o consumo de tokens por turno. Quando a conversa atingia 80% da janela de contexto do modelo (32K tokens na epoca), truncava mensagens antigas para evitar que o modelo recebesse input cortado.

**Por que remover agora:**

```json
{
  "component": "Budget Governor",
  "created": "2025-08-15",
  "original_problem": "Janela de contexto de 32K tokens. Conversas longas do Golem (3h+) podiam ultrapassar o limite, causando truncamento silencioso e respostas incompletas.",
  "current_state": {
    "model_context_window": "200K tokens (6.25x maior)",
    "avg_tokens_per_conversation": "45K tokens",
    "max_tokens_observed_90d": "82K tokens",
    "threshold_to_trigger": "160K tokens (80% de 200K)",
    "times_triggered_180d": 0,
    "conclusion": "A conversa mais longa registrada usa apenas 41% da janela atual. O Budget Governor nunca dispara porque o limite efetivo esta 6.25x acima do necessario."
  },
  "cost_analysis": {
    "tokens_per_turn": 400,
    "tokens_monthly": 1800000,
    "api_cost_monthly_brl": 270,
    "latency_ms_per_turn": 200,
    "maintenance_hours_month": 1.5
  },
  "risk_assessment": {
    "risk": "BAIXO — O modelo atual tem 200K de contexto. O Golem nunca usou mais que 82K. Mesmo se dobras de uso, ainda estaria abaixo do limite.",
    "mitigation": "Manter alerta no dashboard: se consumo medio de tokens ultrapassar 140K (70% da janela), reavaliar. Feature flag permite reativacao em < 1 hora.",
    "rollback_plan": "Codigo arquivado em archive/components/budget-governor-v1/. Feature flag: harness.budget_governor.enabled (default: false)."
  }
}
```

**Processo de remocao:**

```
SEMANA 1: Feature flag — 5% do trafego sem Budget Governor
          → Monitorar: nenhum turno com tokens > 160K
          → Resultado: 0 incidentes. Consumo maximo: 78K tokens.

SEMANA 2: Feature flag — 25% do trafego sem Budget Governor
          → Monitorar: consistencia das respostas, satisfacao do cliente
          → Resultado: CSAT estavel em 86%. Zero respostas truncadas.

SEMANA 3: Feature flag — 100% do trafego sem Budget Governor
          → Monitorar ativamente por 7 dias
          → Resultado: Nenhuma regressao. Latencia reduziu 200ms.

SEMANA 4: Remover codigo. Arquivar em archive/components/budget-governor-v1/.
          → Atualizar documentacao e diagrama de arquitetura.
```

### 2.2 Format Enforcer — Justificativa de Remocao

**O que fazia:** Validava que o output do Generator Agent era JSON estruturalmente valido. Em caso de JSON malformado, rejeitava o output e solicitava regeneracao.

**Por que remover agora:**

```json
{
  "component": "Format Enforcer",
  "created": "2025-09-01",
  "original_problem": "Modelo da epoca (Claude v1) produzia JSON malformado em aproximadamente 3% dos turns. JSON invalido quebrava o parsing downstream e causava fallback para resposta generica.",
  "current_state": {
    "model": "Claude v3 com suporte nativo a Structured Output (JSON mode)",
    "violations_90d": 0,
    "violations_180d": 1,
    "note": "A unica violacao em 180 dias foi um campo com aspas nao escapadas — um bug no template de prompt, nao no modelo. Corrigido em 2 horas.",
    "conclusion": "O modelo atual produz JSON estruturalmente valido por construcao. O Format Enforcer e um safety net para um problema que ja nao existe."
  },
  "cost_analysis": {
    "tokens_per_turn": 300,
    "tokens_monthly": 1350000,
    "api_cost_monthly_brl": 202,
    "latency_ms_per_turn": 120
  },
  "risk_assessment": {
    "risk": "MUITO BAIXO — Zero violacoes em 90 dias com o modelo atual. O unico caso em 180 dias foi um bug de prompt, nao do modelo.",
    "mitigation": "Adicionar validacao de schema no parser downstream (custo: ~5ms, zero tokens adicionais). Se o JSON estiver malformado, o parser rejeita com erro claro — sem a sobrecarga de um componente dedicado.",
    "rollback_plan": "Codigo arquivado em archive/components/format-enforcer-v1/. Feature flag: harness.format_enforcer.enabled (default: false)."
  }
}
```

**Nota tecnica:** A validacao de schema no parser downstream e diferente do Format Enforcer. O Enforcer fazia uma chamada extra ao modelo para verificar o JSON (300 tokens, 120ms). O parser downstream e uma validacao estrutural pura (regex + JSON.parse) que custa 5ms e zero tokens. E uma substituicao de um componente pesado por uma verificacao leve no ponto de consumo — exatamente o tipo de simplificacao que o Harness Evolution promove.

### 2.3 Deduplication Engine — Justificativa de Remocao

**O que fazia:** Identificava e removia informacoes duplicadas do contexto antes de envia-lo ao Generator Agent. Por exemplo, se o cliente mencionasse "sou alergico a gluten" tres vezes na conversa, o Dedup Engine mantinha apenas uma ocorrencia.

**Por que remover agora:**

```json
{
  "component": "Deduplication Engine",
  "created": "2025-10-10",
  "original_problem": "Contexto longo com informacoes repetidas consumia tokens e confundia o modelo antigo, que as vezes tratava repeticoes como novas constraints conflitantes.",
  "current_state": {
    "real_preventions_90d": 3,
    "false_positives_90d": 89,
    "fp_ratio": "30x mais falsos positivos que prevencoes reais",
    "fp_examples": [
      "Cliente diz 'prefiro whey' e depois 'whey e minha escolha' → marcado como duplicata, mas a segunda mencao adicionava contexto de decisao.",
      "Cliente lista 3 alergias e depois repete uma delas em contexto diferente → informacao removida, contexto perdido."
    ],
    "conclusion": "O Dedup Engine causa mais dano que beneficio. O modelo atual lida bem com repeticoes naturais — elas reforcam constraints, nao as confundem. Remover informacao 'duplicada' frequentemente remove contexto util."
  },
  "cost_analysis": {
    "tokens_per_turn": 600,
    "tokens_monthly": 2700000,
    "api_cost_monthly_brl": 405,
    "latency_ms_per_turn": 250
  },
  "risk_assessment": {
    "risk": "BAIXO — O modelo atual (200K contexto, instruction following melhorado) nao so tolera repeticoes como se beneficia delas para reforcar constraints importantes.",
    "mitigation": "O History Compactor (introduzido em modulos anteriores do Nivel 3) ja lida com compressao de conversas longas. Repeticoes naturais em conversas de < 2h nao causam problemas de contexto com 200K de janela.",
    "rollback_plan": "Codigo arquivado em archive/components/deduplication-engine-v1/. Feature flag: harness.dedup_engine.enabled (default: false)."
  }
}
```

**Licao importante:** O Deduplication Engine e um exemplo classico de um componente que foi criado com boa intencao mas cujo custo em falsos positivos supera em muito o beneficio. Ele ilustra o principio central do Harness Evolution: **"funcionar" nao e suficiente — e preciso provar que o valor entregue supera o custo (incluindo o custo dos falsos positivos).**

### Resultado Apos Fase 1

```
┌──────────────────────────────────────────────────────────────────┐
│                GOLEM HARNESS — Apos Fase 1 (11 componentes)       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🟡 Context Hydrator  🟡 Critical Tag Marker             │   │
│  │  (mantidos — reavaliados na Fase 2)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🟡 Intent Classifier  🟢 Product Selector               │   │
│  │  🟢 Generator Agent    🟢 Constraint Validator            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🛡️ Allergen Filter   🟡 Pre-Validation Hook             │   │
│  │  🟢 Fallback Resolver                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🛡️ Trace Recorder    🛡️ Decision Archiver              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  LATENCIA: 3210ms (-15.1%)    TOKENS: 2500/turno (-34.2%)       │
│  COMPONENTES: 11 (-3)         CUSTO/MES: R$ 5.420 (-15.3%)      │
└──────────────────────────────────────────────────────────────────┘
```

### Validacao de Regressao — Fase 1

| Metrica | Antes (14 comp.) | Apos Fase 1 (11 comp.) | Delta |
|---------|-----------------|----------------------|-------|
| Acuracia (avaliacao humana) | 95.8% | 95.7% | -0.1% (nao significativo) |
| CSAT | 86% | 87% | +1% (latencia menor ajudou) |
| P95 latencia | 5.2s | 4.1s | -21% |
| Tokens/turno | 3800 | 2500 | -34% |
| Incidentes P0/P1 | 0 | 0 | — |
| Falsos positivos/turno | 0.8% | 0.3% | -62% (Dedup Engine era o maior fonte) |

---

## 🔄 3. Fase 2 — Simplificar o Redundante (Semanas 5-10)

**Objetivo:** Consolidar componentes com funcoes sobrepostas e reduzir o escopo de componentes que ainda sao uteis mas estao superdimensionados. Estas mudancas tem risco medio — exigem shadow testing antes da implementacao completa.

**Mindset:** "Juntar o que faz a mesma coisa, reduzir o que esta grande demais." Nao e remocao — e simplificacao cirurgica.

### Componentes Afetados Nesta Fase

```
┌──────────────────────────────────────────────────────────────────┐
│              FASE 2 — SIMPLIFICACOES (3 acoes)                    │
│                                                                  │
│  🟡 Context Hydrator + Critical Tag Marker → History Compactor   │
│     (absorver funcoes em componente existente)                    │
│                                                                  │
│  🟡 Intent Classifier → Simplificar para modo condicional        │
│     (so rodar em 20% dos casos ambiguos)                          │
│                                                                  │
│  🟡 Pre-Validation Hook → Consolidar no Constraint Validator     │
│     (eliminar validacao duplicada)                                │
│                                                                  │
│  Impacto Agregado:                                               │
│  Latencia:    -780ms (-24.3% vs Fase 1)                          │
│  Tokens:      -900/turno (-36.0% vs Fase 1)                      │
│  Componentes: 11 → 8                                             │
│  Custo/mes:   -R$ 1.240                                          │
└──────────────────────────────────────────────────────────────────┘
```

### 3.1 Absorver Context Hydrator + Critical Tag Marker no History Compactor

**Situacao atual:** Tres componentes lidam com aspectos diferentes da gestao de contexto:

```
COMPONENTE                  FUNCAO                          CUSTO
─────────────────────────────────────────────────────────────────
Context Hydrator     Recarrega dados do cliente a     550ms, 1400tk
                     cada turno (alergias, budget,
                     preferencias, historico)

Critical Tag Marker  Marca informacoes como            180ms, 400tk
                     HIGH_PRIORITY no prompt

History Compactor    Comprime conversas longas (>2h)   300ms, 600tk
                     em resumos estruturados           (condicional)
─────────────────────────────────────────────────────────────────
TOTAL (overhead):                                      1030ms, 2400tk
```

**Problema:** O History Compactor ja gerencia contexto historico. O Context Hydrator e o Critical Tag Marker sao essencialmente funcoes de pre-processamento de contexto que poderiam ser absorvidas pelo Compactor, que ja toca o contexto a cada ciclo.

**Plano de simplificacao:**

```json
{
  "action": "ABSORB",
  "absorbed": ["Context Hydrator", "Critical Tag Marker"],
  "absorber": "History Compactor",
  "plan": {
    "wave_1_context_loading": {
      "date": "Semana 5",
      "changes": [
        "Mover logica de carga de dados do cliente (Context Hydrator) para o History Compactor",
        "Carregar customer_profile.json apenas no INICIO da conversa, nao a cada turno",
        "Manter cache em memoria do Compactor — se perfil mudar (raro), invalida e recarrega"
      ],
      "impact": {
        "tokens_saved_per_turn": 1400,
        "latency_reduction_ms": 550,
        "risk": "BAIXO — Dados do cliente raramente mudam durante uma conversa. O modelo atual mantem retencao por toda a sessao."
      },
      "shadow_test": {
        "duration": "7 dias",
        "traffic_split": "50% com carga a cada turno, 50% com carga so no inicio",
        "result": "Acurácia 95.7% vs 95.6%. Delta de -0.1% — nao significativo. Zero incidentes de contexto perdido."
      }
    },
    "wave_2_tag_removal": {
      "date": "Semana 7",
      "changes": [
        "Remover tags HIGH_PRIORITY explicitas do Critical Tag Marker",
        "Confiar que o modelo atual (Claude v3) prioriza naturalmente constraints no system prompt",
        "Mover dados criticos (alergias, budget) para o inicio do system prompt — posicao de maxima atencao"
      ],
      "impact": {
        "tokens_saved_per_turn": 400,
        "latency_reduction_ms": 180,
        "risk": "BAIXO-MEDIO — Validar que constraints continuam sendo respeitadas sem tags explicitas"
      },
      "shadow_test": {
        "duration": "14 dias",
        "traffic_split": "50% com tags, 50% sem tags",
        "result": "Constraint adherence: 98.2% com tags vs 97.9% sem tags. Delta de -0.3% — dentro da margem. Zero violacoes de alergia."
      }
    }
  },
  "final_state": {
    "component": "History Compactor (ampliado)",
    "responsibilities": [
      "Carregar perfil do cliente no inicio da conversa",
      "Comprimir conversas > 2h em resumos estruturados",
      "Servir como unico ponto de entrada de contexto para o Generator Agent"
    ],
    "tokens_per_turn": 800,
    "latency_ms": 350,
    "note": "Absorveu funcoes de 2 componentes. Custo aumentou de 600tk/300ms para 800tk/350ms, mas eliminou 1800tk/730ms dos componentes absorvidos. Economia liquida: -1600tk, -560ms."
  }
}
```

### 3.2 Intent Classifier — Simplificar para Modo Condicional

**Situacao atual:** O Intent Classifier analisa TODA mensagem do cliente para determinar a intencao (descobrir produto, comparar, comprar, suporte, etc.) e rotear para o fluxo correto.

**Problema:** Em 85% dos casos, a intencao e obvia pelo contexto da conversa. O Generator Agent, com o modelo atual, consegue inferir a intencao implicitamente sem precisar de um componente dedicado.

```json
{
  "component": "Intent Classifier",
  "current_mode": "Always-on — classifica toda mensagem",
  "proposed_mode": "Conditional — so classifica quando ambiguo",
  "analysis": {
    "turns_analyzed_90d": 45000,
    "classification_breakdown": {
      "obvious_from_context": "85% (38250 turns) — a intencao era clara pelo fluxo da conversa",
      "truly_ambiguous": "15% (6750 turns) — sem o classificador, o modelo poderia interpretar errado"
    },
    "current_accuracy": "87% (41 corretas a cada 47 acionamentos reais)",
    "cost_per_classification": "300ms, 850 tokens",
    "waste": "85% das chamadas sao desnecessarias — custam R$ 870/mes e 255ms/turno em media sem agregar valor"
  },
  "simplification": {
    "approach": "Classifier condicional com gatilho de ambiguidade",
    "logic": "Se a intencao for clara pelo estado atual da conversa (sprint contract ativo, fluxo definido) → pular classificacao. Se ambiguo (cliente muda de assunto abruptamente, pergunta generica) → acionar classificador.",
    "expected_reduction": "-80% de chamadas do classificador (de 100% para ~20% dos turns)",
    "impact": {
      "tokens_saved_per_turn": 680,
      "latency_reduction_ms": 240,
      "risk": "MEDIO — Classificacoes erradas em casos ambiguos podem rotear para o fluxo errado"
    }
  },
  "mitigation": {
    "safety_net": "Se o Generator Agent detectar que esta no fluxo errado (output nao corresponde ao esperado), sinaliza ao orquestrador para reclassificar.",
    "shadow_test": "14 dias. Rodar classificador em background para todos os turns mas so usar resultado quando ambiguo. Comparar decisoes.",
    "rollback": "Feature flag: harness.intent_classifier.mode = 'always' | 'conditional'. Reversao instantanea."
  }
}
```

### 3.3 Pre-Validation Hook — Consolidar no Constraint Validator

**Situacao atual:** O Pre-Validation Hook e o Constraint Validator fazem validacoes sobrepostas:

```
PRE-VALIDATION HOOK (antes do Generator):
  - Verifica se os produtos selecionados tem informacao completa
  - Valida que as constraints do cliente estao disponiveis no contexto
  - Checa se o sprint contract atual e valido

CONSTRAINT VALIDATOR (depois do Generator):
  - Verifica se a recomendacao respeita alergias
  - Valida se o preco esta dentro do budget
  - Checa se as preferencias foram consideradas
  - Confere se o formato da resposta esta correto
```

**Overlap identificado:** Ambos validam constraints do cliente. O Pre-Validation Hook valida PRE-Generator (as constraints estao disponiveis?). O Constraint Validator valida POS-Generator (as constraints foram respeitadas?). A validacao pre e redundante porque se as constraints nao estiverem disponiveis, o Constraint Validator POS-Generator vai detectar a violacao de qualquer forma.

```json
{
  "action": "CONSOLIDATE",
  "source": "Pre-Validation Hook",
  "target": "Constraint Validator",
  "rationale": "A validacao pre-generator e um safety net que raramente dispara (0.01% dos turns) e cujo custo (350ms, 500 tokens) nao se justifica. O Constraint Validator pos-generator ja cobre 100% dos cenarios que o Pre-Validation Hook cobre — e com mais precisao, porque valida o output real, nao a disponibilidade teorica das constraints.",
  "cost_analysis": {
    "pre_validation_hook": {
      "tokens_per_turn": 500,
      "latency_ms": 150,
      "real_preventions_90d": 2,
      "false_positives_90d": 16,
      "fp_ratio": "8x",
      "note": "A maioria dos falsos positivos ocorre quando o hook detecta uma constraint 'faltando' que na verdade esta no system prompt, mas o hook so verifica o user message."
    }
  },
  "implementation": {
    "step_1": "Adicionar verificacao de completude de constraints ao Constraint Validator (+50 tokens, +10ms)",
    "step_2": "Shadow test: 14 dias com Pre-Validation Hook desativado",
    "step_3": "Se zero regressoes, remover Pre-Validation Hook"
  },
  "risk": "BAIXO — A funcao de validacao e absorvida, nao eliminada. O Constraint Validator se torna mais completo."
}
```

### Resultado Apos Fase 2

```
┌──────────────────────────────────────────────────────────────────┐
│              GOLEM HARNESS — Apos Fase 2 (8 componentes)          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🟢 History Compactor (ampliado)                          │   │
│  │  Carrega perfil, comprime historico, serve contexto       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🟡 Intent Classifier (condicional)                       │   │
│  │  🟢 Product Selector    🟢 Generator Agent                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🟢 Constraint Validator (ampliado)                       │   │
│  │  🛡️ Allergen Filter     🟢 Fallback Resolver             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🛡️ Trace Recorder      🛡️ Decision Archiver            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  LATENCIA: 2430ms (-24.3%)    TOKENS: 1600/turno (-36.0%)       │
│  COMPONENTES: 8 (-3)           CUSTO/MES: R$ 4.180 (-22.9%)     │
└──────────────────────────────────────────────────────────────────┘
```

### Validacao de Regressao — Fase 2

| Metrica | Apos Fase 1 | Apos Fase 2 | Delta |
|---------|------------|------------|-------|
| Acuracia (avaliacao humana) | 95.7% | 95.5% | -0.2% (nao significativo) |
| CSAT | 87% | 88% | +1% |
| P95 latencia | 4.1s | 3.2s | -22% |
| Tokens/turno | 2500 | 1600 | -36% |
| Constraint adherence | 97.9% | 97.8% | -0.1% |
| Incidentes P0/P1 | 0 | 0 | — |

---

## ✨ 4. Fase 3 — Evoluir para o Essencial (Semanas 11-16)

**Objetivo:** Fazer a ultima transformacao estrutural — absorver o Intent Classifier condicional em uma funcao interna do Generator Agent e confirmar que o harness com 7 componentes entrega o mesmo nivel de qualidade do harness original com 14.

**Mindset:** "O harness minimo que entrega o mesmo valor." Cada componente que permanece tem uma razao clara e metricas que o justificam.

### 4.1 Absorver Intent Classifier no Generator Agent

**Contexto:** Apos a Fase 2, o Intent Classifier roda apenas em ~20% dos turns (casos ambiguos). Nestes 3 meses de operacao condicional, o time acumulou dados suficientes para avaliar se ate mesmo esses 20% poderiam ser absorvidos.

```json
{
  "component": "Intent Classifier (condicional)",
  "phase": "Fase 3 — Absorcao final",
  "analysis_90d": {
    "conditional_triggers": 13500,
    "classification_accuracy": "91% (em modo condicional, so casos dificeis)",
    "generator_without_classifier_accuracy": "89% (quando o classificador nao rodou em casos ambiguos)",
    "delta": "-2% em casos ambiguos, mas o impacto final no cliente e mitigado porque:",
    "mitigation_factors": [
      "O Generator Agent detecta quando esta no fluxo errado e auto-corrige em 78% dos casos",
      "Dos 22% restantes, o Constraint Validator pega 95% das violacoes",
      "Resultado: apenas 1.1% dos casos ambiguos resultam em experiencia subotima para o cliente"
    ],
    "cost_benefit": {
      "cost_to_keep": "R$ 280/mes, 60ms/turno (media amortizada pelos 20% de acionamento)",
      "errors_prevented": "~148 por mes (1.1% de 13500)",
      "cost_per_error_prevented": "R$ 1.89",
      "avg_cost_of_error": "R$ 3.50 (cliente levemente confuso, resolve na proxima mensagem)",
      "roi": "1.85x (positivo mas marginal)"
    }
  },
  "decision": "Absorver no Generator Agent",
  "implementation": {
    "approach": "Adicionar prompt instruction ao Generator Agent: 'Se a intencao do cliente nao estiver clara, pergunte educadamente antes de prosseguir.'",
    "rationale": "Em vez de classificar a intencao com um componente separado, deixe o Generator Agent — que ja esta no fluxo — lidar com a ambiguidade diretamente, perguntando ao cliente. Isso e mais barato (zero tokens extras), mais natural (conversa flui) e mais preciso (cliente confirma a intencao).",
    "cost": "Zero tokens adicionais. Zero latencia adicional. O Generator Agent ja esta no pipeline.",
    "risk": "BAIXO — O impacto nos 1.1% de casos e uma pergunta extra ao cliente, que e uma interacao natural."
  }
}
```

### Plano de Execucao — Fase 3

```
SEMANA 11-12: Preparacao
  - Atualizar prompt do Generator Agent com instrucao de esclarecimento
  - Configurar shadow test: 50% trafego com Intent Classifier, 50% com
    Generator self-clarification

SEMANA 13-14: Shadow Test
  - Monitorar: taxa de esclarecimento, satisfacao, tempo ate resolucao
  - Resultado esperado: Generator pede esclarecimento em ~15% dos casos
    ambiguos (vs 20% que o Classifier cobria). Os 5% restantes sao
    resolvidos naturalmente pelo contexto.
  - Resultado real: Clientes responderam bem a perguntas de esclarecimento.
    CSAT subiu 0.5% (clientes percebem que o agente "presta atencao").

SEMANA 15: Migracao
  - Feature flag: 100% trafego sem Intent Classifier
  - Monitorar por 7 dias
  - Resultado: Zero regressoes. Zero incidentes.

SEMANA 16: Finalizacao
  - Remover codigo do Intent Classifier
  - Arquivar em archive/components/intent-classifier-v1/
  - Atualizar documentacao
  - Publicar post-mortem positivo
```

### Arquitetura Final — Golem Harness Essencial (7 componentes)

```
┌──────────────────────────────────────────────────────────────────┐
│              GOLEM HARNESS v3.0 — Arquitetura Essencial            │
│              "7 componentes. Mesma qualidade. Metade do custo."   │
│                                                                  │
│                       CLIENTE PERGUNTA                            │
│                             │                                     │
│                             ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  🟢 HISTORY COMPACTOR (ampliado)                          │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ • Carrega perfil do cliente (so 1a mensagem)       │  │   │
│  │  │ • Comprime conversas > 2h                          │  │   │
│  │  │ • Serve contexto unificado ao Generator            │  │   │
│  │  │ • Substitui: Context Hydrator + Critical Tag Marker│  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │  Latencia: 350ms | Tokens: 800                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             │                                     │
│              ┌──────────────┴──────────────┐                      │
│              ▼                             ▼                      │
│  ┌──────────────────────┐    ┌──────────────────────┐            │
│  │                      │    │                      │            │
│  │  🟢 PRODUCT SELECTOR │    │  🛡️ ALLERGEN FILTER  │            │
│  │  ┌────────────────┐  │    │  ┌────────────────┐  │            │
│  │  │ Busca catalogo │  │    │  │ Valida alergias│  │            │
│  │  │ Filtra por     │  │    │  │ e restricoes   │  │            │
│  │  │ preferencias   │  │    │  │ medicas do     │  │            │
│  │  │ Ordena por     │  │    │  │ cliente        │  │            │
│  │  │ relevancia     │  │    │  │ (INVARIAVEL)   │  │            │
│  │  └────────────────┘  │    │  └────────────────┘  │            │
│  │  350ms | 500tk       │    │  250ms | 500tk        │            │
│  └──────────────────────┘    └──────────────────────┘            │
│              │                             │                      │
│              └──────────────┬──────────────┘                      │
│                             ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  🟢 GENERATOR AGENT                                      │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ • Gera recomendacao personalizada                  │  │   │
│  │  │ • Self-clarification em caso de ambiguidade        │  │   │
│  │  │ • Substitui: Intent Classifier (funcao absorvida)  │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │  Latencia: 700ms | Tokens: 1000                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             │                                     │
│                             ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  🟢 CONSTRAINT VALIDATOR (ampliado)                       │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ • Valida constraints do cliente (budget, pref.)    │  │   │
│  │  │ • Verifica completude da resposta                  │  │   │
│  │  │ • Substitui: Pre-Validation Hook                   │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │  Latencia: 300ms | Tokens: 450                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             │                                     │
│              ┌──────────────┴──────────────┐                      │
│              ▼                             ▼                      │
│  ┌──────────────────────┐    ┌──────────────────────┐            │
│  │                      │    │                      │            │
│  │  🟢 FALLBACK RESOLVER│    │  🛡️ TRACE + ARCHIVE  │            │
│  │  ┌────────────────┐  │    │  ┌────────────────┐  │            │
│  │  │ Se validacao   │  │    │  │ Registra todas │  │            │
│  │  │ falhar: retry  │  │    │  │ as decisoes    │  │            │
│  │  │ simples, depois│  │    │  │ para debug e   │  │            │
│  │  │ escala para    │  │    │  │ auditoria      │  │            │
│  │  │ humano         │  │    │  │ (INVARIAVEL)   │  │            │
│  │  └────────────────┘  │    │  └────────────────┘  │            │
│  │  200ms | 300tk       │    │  200ms | 250tk        │            │
│  └──────────────────────┘    └──────────────────────┘            │
│                             │                                     │
│                             ▼                                     │
│                    RESPOSTA AO CLIENTE                            │
│                                                                  │
│  ═══════════════════════════════════════════════════════════════  │
│  LATENCIA TOTAL: ~2350ms (-37.8% vs original 3780ms)             │
│  TOKENS/TURNO: ~1500 (-60.5% vs original 3800)                   │
│  COMPONENTES: 7 (-50% vs original 14)                            │
│  CUSTO MENSAL API: R$ 3.100 (-51.6% vs original R$ 6.400)       │
│  HORAS MANUTENCAO/MES: 10h (-54.5% vs original 22h)              │
│  TEMPO ONBOARDING: 1 semana (-66% vs original 3 semanas)         │
└──────────────────────────────────────────────────────────────────┘
```

### Metricas Finais — Antes e Depois da Evolucao Completa

| Metrica | Antes (14 comp.) | Depois (7 comp.) | Delta |
|---------|-----------------|-----------------|-------|
| **Latencia media/turno** | 3780ms | 2350ms | **-37.8%** |
| **P95 latencia** | 5.2s | 3.1s | **-40.4%** |
| **Tokens/turno** | 3800 | 1500 | **-60.5%** |
| **Componentes** | 14 | 7 | **-50%** |
| **Custo API/mes** | R$ 6.400 | R$ 3.100 | **-51.6%** |
| **Horas manutencao/mes** | 22h | 10h | **-54.5%** |
| **Tempo onboarding** | 3 semanas | 1 semana | **-66.7%** |
| **CSAT** | 86% | 88% | **+2%** |
| **Acuracia (humana)** | 95.8% | 95.6% | **-0.2%** (nao signif.) |
| **Incidentes P0/P1** | 0 | 0 | — |
| **Falsos positivos/turno** | 0.8% | 0.1% | **-87.5%** |

A acuracia caiu 0.2% — uma perda estatisticamente insignificante e dentro da margem de erro da avaliacao humana. Em troca, o sistema ficou 38% mais rapido, 60% mais barato em tokens, e tem metade dos componentes para manter e debugar.

### Componentes Removidos — Destino e Licoes

| Componente | Destino | Licao Aprendida |
|-----------|---------|-----------------|
| Budget Governor | Arquivado. 0 disparos/180d. | "Componentes que dependem de limites de hardware evoluem quando o hardware evolui." |
| Format Enforcer | Arquivado. JSON nativo no modelo. | "Validacao de formato e funcao do parser, nao do harness." |
| Deduplication Engine | Arquivado. 30x mais FPs. | "Remover informacao e perigoso. Confie no modelo para lidar com repeticoes." |
| Context Hydrator | Absorvido pelo History Compactor. | "Carga por turno → carga por sessao. O modelo lembra." |
| Critical Tag Marker | Absorvido pelo History Compactor. | "Tags explicitas sao desnecessarias quando o modelo prioriza naturalmente." |
| Pre-Validation Hook | Absorvido pelo Constraint Validator. | "Pre-validacao redundante: pos-validacao cobre os mesmos cenarios." |
| Intent Classifier | Absorvido pelo Generator Agent. | "Self-clarification e mais barato, mais natural e mais preciso." |

---

## 📊 5. Tabela Comparativa de Estrategias de Coordenacao

Conforme o harness evolui, a forma como os componentes se coordenam muda radicalmente. Menos componentes significam menos handoffs, menos arquivos de estado e menos pontos de falha.

### 5.1 Evolucao da Coordenacao por Fase

| Dimensao | Harness Original (14 comp.) | Apos Fase 1 (11 comp.) | Apos Fase 2 (8 comp.) | Harness Essencial (7 comp.) | Ganho Total |
|----------|---------------------------|----------------------|---------------------|---------------------------|-------------|
| **Handoffs entre componentes** | 13 handoffs sequenciais | 10 handoffs | 7 handoffs | 6 handoffs | **-54% handoffs** |
| **Arquivos de estado/turno** | 8 arquivos JSON | 6 arquivos | 4 arquivos | 3 arquivos | **-62% I/O** |
| **Chamadas ao modelo/turno** | 6 chamadas (algumas leves) | 4 chamadas | 3 chamadas | 2 chamadas | **-67% API calls** |
| **Coordenacao file-based** | 5-7 leituras + 5-7 escritas | 3-4 leituras + 3-4 escritas | 2-3 leituras + 2-3 escritas | 1-2 leituras + 1-2 escritas | **-70% file I/O** |
| **Validacao de output** | 4 stages (Format → Allergen → Constraint → Fallback) | 3 stages | 2 stages (Constraint + Allergen) | 2 stages (Constraint unificado + Allergen) | **-50% stages** |
| **Gestao de contexto** | 3 componentes (Hydrator + Dedup + Tag Marker) | 3 componentes | 1 componente (Compactor ampliado) | 1 componente (Compactor ampliado) | **-67% componentes** |
| **Roteamento de intencao** | 1 componente dedicado sempre-on | 1 componente dedicado sempre-on | 1 componente condicional (~20%) | 0 (funcao absorvida) | **-100% componente** |
| **Tratamento de erros** | 3 fallback strategies + retry loop | 3 fallback strategies | 2 fallback strategies | 1 fallback (retry simples + escala) | **-67% code paths** |
| **System prompt tokens** | 2800 tokens | 2200 tokens | 1200 tokens | 800 tokens | **-71% prompt tokens** |
| **Superficie para bugs** | 14 modulos, ~8500 LOC | 11 modulos, ~6200 LOC | 8 modulos, ~4200 LOC | 7 modulos, ~3500 LOC | **-59% LOC** |

### 5.2 Diagrama de Coordenacao — Antes e Depois

**Antes (14 componentes, coordenacao pesada):**

```
ORQUESTRADOR CENTRAL (1 chamada a cada 2 turnos em media)
       │
       ├──▶ Context Hydrator     ──▶ le customer_profile.json
       │                              └──▶ escreve hydrated_context.json
       │
       ├──▶ Deduplication Engine ──▶ le hydrated_context.json
       │                              └──▶ escreve deduped_context.json
       │
       ├──▶ Critical Tag Marker  ──▶ le deduped_context.json
       │                              └──▶ escreve tagged_context.json
       │
       ├──▶ Intent Classifier    ──▶ le tagged_context.json
       │                              └──▶ escreve intent.json
       │
       ├──▶ Product Selector     ──▶ le intent.json + tagged_context.json
       │                              └──▶ escreve product_shortlist.json
       │
       ├──▶ Pre-Validation Hook  ──▶ le product_shortlist.json
       │                              └──▶ escreve validation_pre.json
       │
       ├──▶ Generator Agent      ──▶ le validation_pre.json + tagged_context.json
       │                              └──▶ escreve draft_response.json
       │
       ├──▶ Format Enforcer      ──▶ le draft_response.json
       │                              └──▶ escreve valid_json.json (ou rejeita)
       │
       ├──▶ Allergen Filter      ──▶ le valid_json.json
       │                              └──▶ escreve allergen_safe.json (ou bloqueia)
       │
       ├──▶ Constraint Validator ──▶ le allergen_safe.json + product_shortlist.json
       │                              └──▶ escreve final_response.json
       │
       ├──▶ Budget Governor      ──▶ monitora tokens totais
       │
       ├──▶ Fallback Resolver    ──▶ se qualquer passo falhar, executa fallback
       │
       ├──▶ Trace Recorder       ──▶ le todas as saidas
       │                              └──▶ escreve trace.jsonl
       │
       └──▶ Decision Archiver    ──▶ le trace.jsonl + final_response.json
                                      └──▶ escreve decision_archive.jsonl

TOTAL I/O POR TURNO: 8 arquivos lidos, 8 arquivos escritos = 16 operacoes
TOTAL CHAMADAS AO MODELO: 6 (algumas com prompts leves de validacao)
```

**Depois (7 componentes, coordenacao leve):**

```
ORQUESTRADOR LEVE (1 chamada por turno, logica simples)
       │
       ├──▶ History Compactor   ──▶ le customer_profile.json (so 1a msg)
       │    (ampliado)              └──▶ escreve context.json
       │
       ├──▶ Product Selector    ──▶ le context.json
       │                             └──▶ (em memoria, sem arquivo)
       │
       ├──▶ Allergen Filter     ──▶ le context.json (alergias)
       │                             └──▶ (em memoria, resultado booleano)
       │
       ├──▶ Generator Agent     ──▶ le context.json
       │                             └──▶ escreve draft_response.json
       │
       ├──▶ Constraint Validator──▶ le draft_response.json + context.json
       │    (ampliado)              └──▶ escreve final_response.json
       │
       ├──▶ Fallback Resolver   ──▶ se Constraint Validator rejeitar
       │
       └──▶ Trace + Archive     ──▶ le final_response.json
                                     └──▶ escreve audit_log.jsonl

TOTAL I/O POR TURNO: 2 arquivos lidos, 3 arquivos escritos = 5 operacoes (-69%)
TOTAL CHAMADAS AO MODELO: 2 (-67%)
```

### 5.3 Impacto da Simplificacao na Coordenacao

A reducao de 14 para 7 componentes nao e apenas uma questao de "menos codigo". Ela transforma a natureza da coordenacao:

```
COORDENACAO PESADA (14 componentes):
  Problema: "Como garantir que 14 componentes executem na ordem certa,
            com os dados certos, e que falhas em qualquer ponto sejam
            tratadas sem corromper o estado?"
  Solucao: Orquestrador central complexo, arquivos de estado
           intermediarios, retry loops, health checks.

COORDENACAO LEVE (7 componentes):
  Problema: "Como encadear 7 componentes de forma linear, onde cada um
            tem uma responsabilidade clara e nao-overlapping?"
  Solucao: Pipeline linear simples. Orquestrador leve gerencia
           sequencia. Menos arquivos = menos corrupcao possivel.
           Menos handoffs = menos pontos de falha.
```

O principio fundamental: **a complexidade da coordenacao cresce exponencialmente com o numero de componentes, nao linearmente.** Cada componente adicionado nao adiciona apenas seu proprio custo — adiciona custo de integracao com TODOS os outros componentes.

Com 14 componentes, o numero potencial de interacoes e `14 * 13 / 2 = 91`. Com 7 componentes, e `7 * 6 / 2 = 21`. Uma reducao de 77% nas interacoes potenciais — mesmo com apenas 50% de reducao no numero de componentes.

---

## 🚀 6. Aplicacao KODA: O Que o Golem Ensina Sobre o KODA

### 6.1 Paralelos Diretos entre Golem e KODA

O exercicio do Golem nao e um exercicio academico. Ele espelha diretamente a evolucao real do harness do KODA, documentada no modulo `05-harness-evolution.md`:

| Golem (Exercicio) | KODA (Real) | Padrao |
|-------------------|-------------|--------|
| Budget Governor (0 disparos/180d) | Budget Guard (0 disparos/180d) | Componentes que dependem de janela de contexto → obsoletos com modelos maiores |
| Format Enforcer (JSON nativo) | Format Validator (JSON nativo) | Structured Output nativo do modelo elimina validadores de formato |
| Deduplication Engine (30x FPs) | Dedup Layer (em investigacao) | Removedores de duplicacao causam mais dano que beneficio |
| Context Hydrator (absorvido) | Context Loader (em simplificacao) | Carga de contexto a cada turno → carga so no inicio |
| Critical Tag Marker (absorvido) | Priority Extractor (em investigacao) | Tags de prioridade → confiar na inferencia nativa do modelo |
| Pre-Validation Hook (consolidado) | Constraint Checker (consolidando) | Pre + Pos validacao → so Pos validacao unificada |
| Intent Classifier (absorvido) | Planner Agent (tornando condicional) | Componentes always-on → condicionais → absorvidos |

### 6.2 O Que o KODA Ja Fez e o Que Ainda Vai Fazer

```
KODA HARNESS EVOLUTION — Estado Atual vs Golem

KODA (Maio 2026):                    Golem (Exercicio):
  ✅ Budget Guard removido             ✅ Budget Governor removido (Fase 1)
  🟡 Context Loader simplificando      ✅ Context Hydrator absorvido (Fase 2)
  🟡 Constraint Checker consolidando   ✅ Pre-Validation Hook consolidado (Fase 2)
  🟡 Format Validator em shadow test   ✅ Format Enforcer removido (Fase 1)
  🔵 Dedup Layer investigando          ✅ Deduplication Engine removido (Fase 1)
  🔵 Priority Extractor investigando   ✅ Critical Tag Marker absorvido (Fase 2)
  🟢 Planner condicional em estudo     ✅ Intent Classifier absorvido (Fase 3)

LICOES DO GOLEM PARA O KODA:

1. O Dedup Layer do KODA provavelmente tem o mesmo problema do
   Deduplication Engine do Golem: falsos positivos > prevencoes reais.
   Acelere a investigacao. Rode a metrica de FPs esta semana.

2. O Priority Extractor do KODA e o Critical Tag Marker do Golem
   tem a mesma funcao. Se o shadow test do Golem mostrou que tags
   explicitas sao desnecessarias, o KODA provavelmente pode absorver
   essa funcao no History Compactor sem perda.

3. O Planner Agent do KODA e o Intent Classifier do Golem seguem
   a mesma trajetoria: always-on → condicional → absorvido.
   Acelere o plano de tornar o Planner condicional (so em jornadas
   complexas) — o Golem mostrou que funciona.
```

### 6.3 Previsao: KODA em Setembro 2026

Baseado na trajetoria do Golem (que e mais agressiva na evolucao), o KODA poderia acelerar seu roadmap:

```
ROADMAP ATUAL DO KODA (do modulo):
  Q2 2026: Remover Format Validator, consolidar Constraint Checker
  Q3 2026: Absorver Context Loader, reduzir Fallback, Planner condicional
  Q4 2026: Alvo: 6-7 componentes

ROADMAP ACELERADO (inspirado pelo Golem):
  Q2 2026: Remover Format Validator + Dedup Layer + Priority Extractor
           (3 remocoes no mesmo trimestre, cada uma com feature flag e
            observacao independente — o Golem validou que sao seguras)
  Q3 2026: Absorver Context Loader + consolidar Constraint Checker
           Planner condicional imediato (nao esperar Q3)
  Q4 2026: Alvo: 6 componentes (1 a menos que o planejado)
```

A licao principal: **o Golem mostra que e seguro ser mais agressivo na remocao de componentes com metricas contundentes.** O medo de remover e o maior inimigo da evolucao do harness.

---

## ⚠️ Riscos e Mitigacoes — Matriz Completa por Fase

### Fase 1 — Riscos

| Risco | Probabilidade | Impacto | Mitigacao | Indicador de Alerta |
|-------|-------------|---------|-----------|-------------------|
| Consumo de tokens ultrapassar 140K apos remover Budget Governor | 2% | Medio | Alerta no dashboard: `tokens_per_turn > 140000`. Feature flag para reativar em < 1h. | Dashboard: consumo medio de tokens (diario) |
| JSON malformado aparecer apos remover Format Enforcer | 1% | Baixo | Parser downstream com validacao de schema captura e rejeita JSON invalido. Custo: 5ms. | Log de erros: `JSONParseError` count |
| Repeticoes confundirem o modelo apos remover Deduplication Engine | 3% | Baixo | Modelo atual lida bem com repeticoes. Se necessario, adicionar nota no prompt: "Repeticoes sao normais — use-as para reforcar constraints." | QA manual: avaliar se recomendacoes consideram constraints repetidas |

### Fase 2 — Riscos

| Risco | Probabilidade | Impacto | Mitigacao | Indicador de Alerta |
|-------|-------------|---------|-----------|-------------------|
| Perda de contexto do cliente apos carga so no inicio | 5% | Alto | Shadow test de 14 dias antes da migracao. Fallback: se o Generator detectar que faltam dados do cliente, solicita recarga ao Compactor. | Metrica: `context_completeness_score` |
| Constraints nao priorizadas corretamente sem tags HIGH_PRIORITY | 8% | Alto | Mover constraints para o inicio do system prompt (posicao de maxima atencao). Shadow test 50/50 por 14 dias. | Metrica: `constraint_adherence_rate` |
| Classificacao errada em casos ambiguos sem Intent Classifier sempre-on | 6% | Medio | Rodar classificador em shadow mode para comparar decisoes. Se delta > 3%, reverter. | Metrica: `intent_misclassification_rate` |
| Violacoes nao detectadas apos remover Pre-Validation Hook | 3% | Medio | Constraint Validator ampliado cobre os mesmos cenarios POS-Generator. Shadow test confirma cobertura. | Metrica: `constraint_violation_rate` |

### Fase 3 — Riscos

| Risco | Probabilidade | Impacto | Mitigacao | Indicador de Alerta |
|-------|-------------|---------|-----------|-------------------|
| Clientes frustrados com perguntas de esclarecimento | 10% | Baixo | Perguntas de esclarecimento sao curtas e naturais ("Voce quer comparar produtos ou ver detalhes de um especifico?"). Clientes tendem a responder positivamente — mostra atencao. | CSAT pos-esclarecimento |
| Degradacao em jornadas complexas sem Intent Classifier | 5% | Medio | Manter classificador em shadow mode por 30 dias apos remocao. Se jornadas complexas (multiplos produtos, restricoes conflitantes) mostrarem degradacao > 5%, reativar condicionalmente. | Acuracia em jornadas complexas (segmentada) |

### Risco Transversal (Todas as Fases)

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|-------------|---------|-----------|
| **"Big Bang Removal" acidental** — time remove varios componentes sem intervalo de observacao | 15% | Alto | REGRA: uma remocao/simplificacao por vez. Feature flag independente para cada. Periodo MINIMO de 14 dias entre mudancas. Dashboard dedicado para cada mudanca ativa. |

---

## 🧹 Checklist de Remocao — Template Reutilizavel

Baseado no processo usado em cada componente removido, este checklist pode ser reutilizado para qualquer evolucao futura de harness:

### Pre-Remocao: Evidencias

- [ ] Metrica de acionamento real documentada (90 dias)
- [ ] Metrica de falsos positivos documentada (90 dias)
- [ ] Custeio completo: tokens (R$), latencia (ms), manutencao (h/mes)
- [ ] Calculo de ROI: (prevencoes × custo do erro) / custo operacional
- [ ] Cobertura redundante: outro componente cobre a mesma protecao?
- [ ] Capacidades do modelo atual que cobrem a fraqueza original
- [ ] Shadow test concluido (14+ dias, delta nao significativo)
- [ ] Testes de regressao que exercitam cenarios protegidos
- [ ] Plano de rollback documentado (feature flag, codigo versionado)

### Durante a Remocao: Passos

- [ ] Feature flag criada: `harness.<componente>.enabled` (default: false)
- [ ] Canary 5% — 24 horas
- [ ] Canary 25% — 24 horas
- [ ] Canary 100% — 7 dias
- [ ] Dashboard de monitoramento ativo configurado
- [ ] Alerta configurado: metrica protegida degradar > 10%

### Pos-Remocao: Confirmacao

- [ ] 14 dias sem regressao
- [ ] Metricas estaveis dentro da baseline pre-remocao
- [ ] CSAT sem queda significativa
- [ ] Custo e latencia reduziram conforme esperado
- [ ] Documentacao atualizada (diagrama, runbooks)
- [ ] Codigo arquivado em `archive/components/<nome>/`
- [ ] ADR escrito documentando a decisao
- [ ] Time comunicado
- [ ] Post-mortem positivo publicado

---

## ⚠️ Anti-Padroes que Esta Solucao Evitou

Refletir sobre o que NAO foi feito e tao importante quanto entender o que foi feito. Esta solucao evitou ativamente cinco anti-padroes classicos de Harness Evolution.

### Anti-Padrao 1: "Big Bang Removal"

**O que seria:** Remover Budget Governor, Format Enforcer, Deduplication Engine, Context Hydrator, Critical Tag Marker, Pre-Validation Hook e Intent Classifier de uma vez. "Aproveita que ja vai mexer e tira tudo."

```
❌ BIG BANG (nao foi feito):
   Sprint 1: Remove 7 componentes de uma vez
   Resultado: Algo quebrou. O que foi? Ninguem sabe.
   Rollback: Reverter TUDO, perder todo o trabalho.

✅ ONDAS (o que foi feito):
   Fase 1: Remove 3 (baixo risco) → observa 4 semanas
   Fase 2: Simplifica 3 (medio risco) → observa 4 semanas
   Fase 3: Absorve 1 (estrutural) → observa 4 semanas
   Resultado: Zero incidentes. Cada mudanca rastreada individualmente.
```

### Anti-Padrao 2: "Remover Porque o Changelog Disse"

**O que seria:** Ler "Modelo agora tem 200K de contexto" e imediatamente remover Budget Governor sem testar.

```
❌ CONFIANCA CEGA NO CHANGELOG (nao foi feito):
   Changelog: "Context window: 200K tokens"
   Time: "Otimo, Budget Governor nao precisa mais!"
   Acao: Remove sem testar.
   Resultado: O changelog descreve benchmarks. O Golem tinha um
             caso especifico onde 82K tokens era o pico, mas um
             novo fluxo de cliente corporativo consome 170K tokens.
             Sem Budget Governor, respostas truncadas.

✅ SHADOW TEST ANTES (o que foi feito):
   Changelog: "Context window: 200K tokens"
   Time: "Vamos ver se realmente nao precisamos."
   Acao: Shadow test 14 dias. Monitora consumo maximo.
   Resultado: Confirmado — consumo maximo 82K, bem abaixo de 200K.
             Remocao segura porque FOI TESTADA, nao assumida.
```

### Anti-Padrao 3: "Nunca Remover Nada"

**O que seria:** Manter os 14 componentes indefinidamente porque "tudo funciona". O time acumularia complexidade a cada trimestre. Em 12 meses, seriam 18 componentes. Em 24 meses, 24 componentes. O sistema se tornaria uma pilha de camadas sobre camadas, onde ninguem sabe mais o que e essencial e o que e legacy.

```
❌ ACUMULACAO ETERNA (nao foi feito):
   Trimestre 1: +2 componentes (total: 16)
   Trimestre 2: +1 componente (total: 17)
   Trimestre 3: "Precisamos reescrever tudo, esta complexo demais"

✅ EVOLUCAO ATIVA (o que foi feito):
   Trimestre 1: +0 componentes, -3 removidos (total: 11)
   Trimestre 2: +0 componentes, -3 simplificados (total: 8)
   Trimestre 3: +0 componentes, -1 absorvido (total: 7)
   Trimestre 4: Arquitetura estavel, complexidade controlada
```

### Anti-Padrao 4: "Simplificar Demais"

**O que seria:** Remover tambem o Allergen Filter e o Fallback Resolver porque "o modelo e muito bom, nao precisa disso".

```
❌ OVER-SIMPLIFICATION (nao foi feito):
   Harness de 2 componentes: Generator → Cliente
   Sem Allergen Filter, sem Constraint Validator, sem Fallback.
   Resultado: Funciona 95% do tempo.
             Os 5% que falham: cliente recebe produto com alergeno.
             Custo: processo, reembolso, perda de cliente, dano a saude.

✅ ESSENCIAL SEGURO (o que foi feito):
   Allergen Filter: INVARIAVEL — saude do cliente nao negocia.
   Constraint Validator: INVARIAVEL — qualidade e compliance.
   Fallback Resolver: INVARIAVEL — disponibilidade do servico.
   Trace + Archive: INVARIAVEL — auditabilidade.
```

### Anti-Padrao 5: "Evoluir Sem Documentar"

**O que seria:** Remover componentes e nao deixar rastro. Seis meses depois, um novo dev pergunta "por que nao temos Deduplication Engine?" e ninguem lembra.

```
❌ REMOCAO SEM RASTRO (nao foi feito):
   Remove Budget Governor. Duas semanas depois, ninguem lembra por que.
   Seis meses depois: "Por que nao temos Budget Governor? Vamos criar um!"
   Ciclo se repete. Componente e recriado. Complexidade volta.

✅ REMOCAO DOCUMENTADA (o que foi feito):
   Cada componente removido tem:
   - Codigo arquivado em archive/components/<nome>-v1/
   - README com: quando foi criado, quando foi removido, por que, metricas
   - ADR documentando a decisao formal
   - Dashboard historico mostrando metricas pre-remocao
   Daqui a 2 anos: alguem pergunta, o arquivo responde.
```

### Resumo: O Que Cada Anti-Padrao Custa

| Anti-Padrao | Custo se Praticado | Como Esta Solucao Evita |
|-------------|--------------------|------------------------|
| Big Bang Removal | Rollback total, perda de trabalho, medo de mexer de novo | Uma mudanca por vez, feature flags independentes |
| Confiar no Changelog | Regressao em casos especificos nao cobertos por benchmarks | Shadow test de 14+ dias sempre |
| Nunca Remover Nada | Complexidade cresce 30-50% ao ano, reescrita inevitavel | Ritmo trimestral de review com metricas |
| Simplificar Demais | Edge cases catastroficos (alergias, cobrancas, dados) | Invariantes identificados e protegidos |
| Evoluir Sem Documentar | Decisoes se perdem, componentes sao recriados, ciclo vicioso | Archive + ADR + README para cada remocao |

---

## ❓ Perguntas Frequentes Sobre Esta Solucao

### P: "Por que 3 fases e nao 2 ou 4?"

**R:** Tres fases e um equilibrio entre agressividade e seguranca. Duas fases seriam muito agressivas (remover 7 componentes em 2 ondas — risco de Big Bang). Quatro fases seriam muito conservadoras (esticar o processo alem do necessario, acumulando custo operacional). Tres fases permitem:

- Fase 1: Ganhos rapidos e seguros (3 remocoes, zero risco estrutural)
- Fase 2: Simplificacoes com validacao (3 consolidacoes, shadow testing)
- Fase 3: Transformacao final (1 absorcao, confirmacao do estado essencial)

O padrao de 3 fases e reutilizavel para qualquer harness com 10-20 componentes. Para harnesses menores (5-8 componentes), 2 fases podem bastar. Para harnesses maiores (20+), 4-5 fases podem ser necessarias.

### P: "O que fazer se o shadow test mostrar degradacao?"

**R:** Esta e a situacao mais importante — e a que justifica todo o processo. Se o shadow test mostrar que remover um componente causa degradacao significativa (>2% de delta na metrica principal):

1. **NAO remova.** O shadow test fez exatamente o seu trabalho: preveniu uma remocao prejudicial.
2. **Investigue a causa.** Por que o componente ainda e necessario? O modelo nao cobre tao bem quanto o changelog sugeria? O caso de uso do Golem e diferente dos benchmarks?
3. **Reclassifique o componente.** Se ele previne erros reais com delta significativo, ele sobe de REMOVE para KEEP (ou SIMPLIFY, se der para reduzir escopo).
4. **Documente a nao-remocao.** Tao importante quanto documentar remocoes e documentar QUAIS componentes foram investigados e MANTIDOS com justificativa. Isso evita re-investigar o mesmo componente no proximo ciclo.

```
EXEMPLO HIPOTETICO (nao aconteceu no Golem, mas ilustra):

   Componente: Allergen Filter
   Shadow test: 50% trafego com, 50% sem
   Resultado: Com Allergen Filter = 0 violacoes de alergia.
             Sem Allergen Filter = 12 violacoes em 14 dias.
   Delta: Infinito (0 → 12 e inaceitavel)
   Conclusao: MANTER. Allergen Filter e invariante.
   Licao: Seguranca do cliente nao e negociada por latencia.
```

### P: "Como lidar com a resistencia do time a remover componentes?"

**R:** A resistencia e natural e saudavel — significa que o time se importa com a qualidade. O caminho para vencer a resistencia nao e autoridade ("sou o tech lead, vou remover"). E transparencia com dados:

1. **Mostre as metricas, nao as conclusoes.** Em vez de dizer "vamos remover o Deduplication Engine", mostre o dashboard: "3 prevencoes reais vs 89 falsos positivos nos ultimos 90 dias. Isso significa que 97% das vezes que este componente agiu, ele atrapalhou."

2. **Comece pelo obvio.** Budget Governor (0 disparos em 180 dias) e impossivel de defender. Comece por ele. Quando o time ver que a primeira remocao foi segura, a confianca no processo aumenta.

3. **Envolva o criador na remocao.** O Dev A criou o Context Hydrator. Em vez de remove-lo sem ele, envolva-o no planejamento da absorcao pelo History Compactor. Ele conhece o componente melhor que ninguem — pode ajudar a garantir que a absorcao e segura.

4. **Celebre as remocoes.** Quando um componente e removido com sucesso (zero regressoes), publique um post-mortem POSITIVO. "Removemos o Budget Governor. Ganhamos 200ms de latencia e R$ 270/mes. Nada quebrou." Isso muda a cultura de "remover e perigoso" para "remover o que nao e necessario e vitoria".

### P: "Este plano funcionaria para um harness que nao e de recomendacao?"

**R:** Sim. O processo (scorecard → classificar → 3 fases → validar) e independente do dominio. O que muda e:
- O peso de cada dimensao no scorecard (em um sistema financeiro, "Invariante" teria mais peso)
- O threshold de shadow test (em um sistema medico, delta maximo aceitavel seria 0.1%, nao 1%)
- A velocidade das fases (em um sistema de missao critica, cada fase poderia ser 8 semanas, nao 4)

O que NAO muda: a logica de metricas > intuicao, remocao incremental > big bang, e invariantes > tudo.

### P: "E se um novo modelo for lancado durante a evolucao?"

**R:** Esta e uma situacao comum e desejavel — significa que o mercado esta evoluindo. O processo para lidar com isso:

1. **Termine a fase atual** antes de reavaliar. Nao pare uma simplificacao no meio para incorporar o novo modelo.
2. **Apos a fase, reexecute o scorecard** com as capacidades do novo modelo. Componentes que eram KEEP podem virar SIMPLIFY. Componentes que eram SIMPLIFY podem virar REMOVE.
3. **Acelere se fizer sentido.** Se o novo modelo tem "Native Structured Output", o Format Enforcer (se ainda existisse) poderia ser removido na Fase 1 em vez da Fase 2.

No caso do Golem, se um novo modelo fosse lancado durante a Fase 2 com "Instruction Following 2x melhor", o Intent Classifier poderia ser absorvido ja na Fase 2 (em vez de esperar a Fase 3), acelerando o roadmap.

---

## 🧮 Calculadora de Impacto: Como Quantificar o Valor da Evolucao

Para medir o impacto financeiro e operacional da evolucao, use estas formulas. Elas foram aplicadas ao Golem e podem ser reutilizadas em qualquer harness.

### Formula 1: ROI de um Componente

```
ROI = (Erros Prevenidos em 90 dias × Custo Medio do Erro) /
      (Custo de Tokens + Custo de Manutencao + Custo de Latencia)

Onde:
  Custo de Tokens = tokens_por_turno × turns_por_mes × 3 × preco_por_token
  Custo de Manutencao = horas_manutencao_mes × 3 × custo_hora_dev
  Custo de Latencia = latencia_ms × turns_por_mes × 3 × custo_por_ms

  custo_por_ms = (receita_mensal / turns_por_mes) / tempo_medio_sessao_ms
               × taxa_de_abandono_por_latencia

Exemplo — Deduplication Engine do Golem:
  Erros Prevenidos = 3
  Custo Medio do Erro = R$ 50 (cliente confuso, suporte humano)
  Custo de Tokens = 600 × 45000 × 3 × R$ 0.000015 = R$ 1.215
  Custo de Manutencao = 2h × 3 × R$ 150/h = R$ 900
  Custo de Latencia = 250ms × 45000 × 3 × R$ 0.0000008 = R$ 27
  Custo Operacional Total = R$ 2.142

  ROI = (3 × R$ 50) / R$ 2.142
  ROI = R$ 150 / R$ 2.142
  ROI = 0.07x (MUITO NEGATIVO — cada R$ 1 gasto entrega R$ 0.07 de valor)
```

### Formula 2: Custo da Complexidade (Lei de Metcalfe Aplicada)

```
Complexidade de Coordenacao = n × (n - 1) / 2

Onde n = numero de componentes no harness.

Esta formula representa o numero potencial de interacoes entre componentes.
Cada interacao e uma oportunidade para:
  - Bug de integracao
  - Corrupcao de estado em arquivo compartilhado
  - Race condition
  - Dependencia quebrada em refatoracao

Golem Antes (14 componentes):
  Interacoes = 14 × 13 / 2 = 91 interacoes potenciais

Golem Depois (7 componentes):
  Interacoes = 7 × 6 / 2 = 21 interacoes potenciais

Reducao: 77% menos interacoes potenciais.
Isso explica por que o tempo de onboarding caiu de 3 semanas para 1 semana.
```

### Formula 3: Payback da Evolucao

```
Payback (meses) = Custo Total da Evolucao / Economia Mensal

Onde:
  Custo Total da Evolucao = (horas_engenharia × custo_hora_dev) +
                             (custo_shadow_test_tokens) +
                             (custo_oportunidade_latencia_durante_testes)

  Economia Mensal = tokens_economizados_mes +
                    manutencao_economizada_mes +
                    valor_latencia_reduzida_mes

Exemplo — Evolucao Completa do Golem:
  Custo Total da Evolucao:
    Horas engenharia: 120h × R$ 150/h = R$ 18.000
    Tokens em shadow tests: ~R$ 2.400
    Total: R$ 20.400

  Economia Mensal:
    Tokens: R$ 3.300 (de R$ 6.400 para R$ 3.100)
    Manutencao: R$ 1.800 (de 22h para 10h/mes × R$ 150/h)
    Total: R$ 5.100

  Payback = R$ 20.400 / R$ 5.100 = 4 meses

A partir do mes 5, a evolucao gerou economia liquida.
No primeiro ano: (12 - 4) × R$ 5.100 = R$ 40.800 de economia.
```

### Impacto Financeiro Anual Projetado

| Metrica | Antes (anual) | Depois (anual) | Economia |
|---------|-------------|---------------|----------|
| Custo API | R$ 76.800 | R$ 37.200 | **R$ 39.600** |
| Manutencao (devs) | R$ 39.600 | R$ 18.000 | **R$ 21.600** |
| Onboarding (2 novos devs/ano) | R$ 36.000 | R$ 12.000 | **R$ 24.000** |
| Incidentes evitados (FP reduzidos) | R$ 8.400 | R$ 1.800 | **R$ 6.600** |
| **TOTAL** | **R$ 160.800** | **R$ 69.000** | **R$ 91.800** |

Economia anual: **R$ 91.800** — suficiente para pagar 1 dev senior por 7 meses.

---

## 🎯 Key Takeaways da Solucao

1. **Classifique antes de agir.** O scorecard de 5 dimensoes (Acionamento, Custo, Falsos Positivos, Cobertura do Modelo, Invariante) transforma intuicoes em decisoes baseadas em dados.

2. **Remova em ondas de risco crescente.** Fase 1: baixo risco, evidencias contundentes. Fase 2: medio risco, shadow testing. Fase 3: mudancas estruturais, validacao prolongada.

3. **Absorver e melhor que deletar.** Componentes como Context Hydrator e Critical Tag Marker nao foram deletados — foram absorvidos pelo History Compactor. A funcao essencial permaneceu, a sobrecarga foi eliminada.

4. **Falsos positivos sao tao importantes quanto prevencoes reais.** O Deduplication Engine foi removido nao porque nao prevenia nada (prevenia 3 erros), mas porque causava 89 falsos positivos — 30x mais dano que beneficio.

5. **A complexidade da coordenacao e exponencial.** Reduzir de 14 para 7 componentes reduziu as interacoes potenciais em 77%, nao 50%. Cada componente removido simplifica nao so a si mesmo, mas sua interacao com todos os outros.

6. **Invariantes sao sagrados.** Allergen Filter, Trace Recorder e Decision Archiver nunca foram questionados. Seguranca, auditoria e disponibilidade sao permanentes.

7. **"One In, One Out" previne o inchaco.** A cada novo componente adicionado, investigue um existente para remocao. O harness nao cresce — ele se transforma.

8. **O payback e rapido.** O custo da evolucao (engenharia + shadow tests) se pagou em 4 meses. Do mes 5 em diante, e economia liquida. A maioria dos times superestima o custo de evoluir e subestima o custo de nao evoluir.

---

## ✅ Checkpoint: O Que Voce Aprendeu

### Fundamentos do Ciclo de Vida

- [ ] Consigo classificar componentes usando o scorecard de 5 dimensoes (Acionamento, Custo, FPs, Cobertura do Modelo, Invariante) e justificar cada nota
- [ ] Entendo a diferenca essencial entre REMOVE (o modelo cobre), SIMPLIFY (reduzir escopo), KEEP (valor comprovado) e PROTECT (invariante)
- [ ] Consigo explicar por que a ordem das fases importa: baixo risco primeiro, medio depois, estrutural por ultimo
- [ ] Sei que cada componente removido deve deixar um rastro: metricas, shadow test, ADR, codigo arquivado

### Metricas e Decisoes

- [ ] Consigo calcular o ROI real de um componente e decidir com base nele
- [ ] Entendo que falsos positivos sao tao importantes quanto prevencoes reais — e frequentemente mais numerosos
- [ ] Sei interpretar um shadow test: delta < 1% e nao significativo = seguro remover; delta > 2% = investigar; delta > 5% = nao remover
- [ ] Consigo identificar quando um componente e "invariante" e nunca deve ser removido (seguranca, compliance, auditoria, disponibilidade)

### Processo de Evolucao

- [ ] Consigo aplicar o checklist completo de remocao (pre, durante, pos) em qualquer componente
- [ ] Entendo o valor de feature flags, canary deploy e periodos de observacao
- [ ] Sei que codigo removido deve ser ARQUIVADO (com README, metricas e ADR), nunca deletado
- [ ] Consigo desenhar um diagrama de arquitetura antes/depois e quantificar o impacto de cada fase

### Coordenacao e Complexidade

- [ ] Consigo explicar por que a complexidade de coordenacao cresce exponencialmente com o numero de componentes
- [ ] Entendo que ABSORVER funcoes (nao apenas remove-las) e a estrategia mais segura de simplificacao
- [ ] Sei ler a tabela comparativa de coordenacao e identificar onde estao os maiores ganhos
- [ ] Consigo projetar o estado final do harness apos a evolucao e comparar com o estado inicial

### Aplicacao Pratica

- [ ] Consigo aplicar o mesmo processo em um harness real (meu ou de um time proximo)
- [ ] Sei que o medo de remover e o maior inimigo da evolucao — e que metricas e processo vencem o medo
- [ ] Entendo que Harness Evolution nao e um projeto — e um ritmo trimestral continuo
- [ ] Posso liderar uma sessao de "Review & Plan" trimestral seguindo o template desta solucao

**Se respondeu NAO a mais de 3 itens:** Releia a secao de Avaliacao Inicial (scorecard) e a Fase 1 (remocoes de baixo risco). Sao os fundamentos que sustentam todo o resto.

**Se respondeu SIM a todos:** Voce esta pronto para liderar a evolucao de harness em qualquer sistema de agentes. O template de checklist e a matriz de riscos sao reutilizaveis. O scorecard e adaptavel a qualquer dominio.

---

## 📚 Referencias e Leituras Complementares

### Dentro do Curriculo (Nivel 3)

- `05-harness-evolution.md` — O modulo completo que este exercicio pratica. Contem o ciclo BUILD → STABILIZE → SIMPLIFY → REMOVE em detalhe.
- `01-multi-agent-systems.md` — A arquitetura multi-agente que a evolucao vai simplificar.
- `02-state-persistence.md` — Invariante: o componente que nunca sai do harness.
- `03-file-based-coordination.md` — Como componentes se comunicam via arquivos (e como simplificar essa comunicacao).
- `04-server-side-compaction.md` — O History Compactor que absorve varios componentes nesta solucao.

### Dentro do Curriculo (Nivel 2)

- `01-generator-evaluator-pattern.md` — O padrao que inspira o Constraint Validator como gatekeeper.
- `04-trace-reading.md` — Como usar traces para gerar metricas de efetividade do harness.
- `koda-applications/nivel-2-koda.md` — O harness do KODA antes da evolucao (para comparar).

### Templates e Ferramentas

- `IMPLEMENTATION_GUIDES/06-harness-evolution-playbook.md` — Playbook passo a passo da revisao trimestral.
- `IMPLEMENTATION_GUIDES/03-harness-design-checklist.md` — Checklist de design inicial.
- `TEMPLATES/architecture-decision-record-template.md` — Template para ADR de remocao.

### Externo

- *The Last Harness You'll Ever Build* (arXiv 2604.21003) — Define formalmente o ciclo de evolucao de harness e meta-evolucao.
- LangChain — The Anatomy of an Agent Harness — Artigo sobre componentes essenciais de harness.
- Documentacao de feature flags (LaunchDarkly, Split.io, ou solucoes caseiras).
- Anthropic model changelogs — Fonte primaria para identificar capacidades que permitem simplificacao.

---

## 💭 Reflexao Final

A Mariana comecou com 14 componentes e um time que tinha medo de remover qualquer coisa. Em 16 semanas, ela entregou um harness com 7 componentes que e 38% mais rapido, 60% mais barato em tokens, e tem a MESMA qualidade de recomendacao.

O segredo nao foi tecnologia nova. Foi disciplina: metricas em vez de intuicao, shadow tests em vez de esperanca, feature flags em vez de "deploy e reza".

**Construir um harness e um ato de humildade.** Voce reconhece que o modelo tem fraquezas e cria protecoes.

**Evoluir um harness e um ato de confianca.** Voce reconhece que o modelo melhorou, que as protecoes fizeram seu trabalho, e que e hora de seguir em frente com uma arquitetura mais leve.

**A pergunta mais importante nao e "funciona?". E "ainda e necessario?"**

O Golem comecou como um sistema de 14 componentes que "funcionava". Terminou como um sistema de 7 componentes que funciona — melhor, mais rapido, mais barato.

A diferenca entre os dois nao foi o modelo. Foi a coragem de perguntar: **"isso ainda precisa existir?"**

---

*Solucao do Exercicio 3 | Nivel 3 — Arquitetura Avancada | Curriculo Long-Running Agents*

*"O destino de toda boa arquitetura de agentes nao e crescer para sempre. E evoluir para o essencial."*

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | `curriculum/03-nivel-3-advanced-architecture/exercises/solutions/exercise-03-solution.md` |
| **Nivel** | 3 — Arquitetura Avancada |
| **Tempo** | 60-90 minutos |
| **Status** | Solucao Completa — Modelo de Referencia |
| **Modulo Correspondente** | `05-harness-evolution.md` |
| **Dependencias** | Exercicios 1 e 2 do Nivel 3, leitura do modulo `05-harness-evolution.md` |
| **Criado** | Maio 2026 |
