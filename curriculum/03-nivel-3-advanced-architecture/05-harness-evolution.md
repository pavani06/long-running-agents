---
title: "Harness Evolution: Quando Remover é Tão Importante Quanto Construir"
type: curriculum-lesson
nivel: 3
aliases: ["evolução harness", "harness lifecycle", "maturidade harness", "remoção componentes"]
tags: [curriculo-conteudo, nivel-3, arquitetura-avancada, evolucao-de-harness, simplificacao-arquitetural, remocao-de-componentes, shadow-testing, canary-deploy, feature-flags, roi-arquitetural, adrs, invariantes-arquiteturais, corpus-de-avaliacao]
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]"]
last_updated: 2026-06-10
---
# 🧬 Harness Evolution: Quando Remover é Tão Importante Quanto Construir
## Como Evoluir a Arquitetura de Agentes Conforme Modelos Melhoram, sem Deixar o Sistema Frágil

**Tempo Estimado:** 90 minutos  
**Nível:** 3 - Arquitetura Avançada  
**Pré-requisito:** Ter completado módulos 01-04 do Nível 3  
**Status:** 🟢 CRÍTICO - Fecha o ciclo de maturidade arquitetural do Nível 3  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Dia em Que Fernando Quis Remover Metade do Código

**Segunda-feira, 9h15. Sala de arquitetura do time KODA.**

Fernando entrou com um café na mão e uma expressão que misturava ansiedade com excitação. Na mesa, um print do changelog do novo modelo Claude — aquele que a Anthropic tinha lançado na sexta-feira.

O time estava reunido para a daily. Mas Fernando não começou com o ritual de sempre. Ele foi direto ao quadro branco e apontou para o diagrama da arquitetura do KODA. Onze componentes. Três camadas. Quatro agentes especializados.

```
┌──────────────────────────────────────────────────────────────┐
│                     KODA ARCHITECTURE v2.8                    │
│                                                              │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌───────────┐ │
│  │ Context │──▶│ Planning │──▶│ Generator│──▶│ Evaluator │ │
│  │ Loader  │   │ Agent    │   │ Agent    │   │ Agent     │ │
│  └─────────┘   └──────────┘   └──────────┘   └───────────┘ │
│       │              │               │               │       │
│       ▼              ▼               ▼               ▼       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              State Persistence Layer                  │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌───────────┐  │   │
│  │  │customer│  │  plan  │  │  draft │  │ evaluation│  │   │
│  │  │.json   │  │ .json  │  │ .json  │  │  .json    │  │   │
│  │  └────────┘  └────────┘  └────────┘  └───────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Validation & Guardrails Layer                │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐  │   │
│  │  │Constraint│ │  Budget  │ │  Format  │ │Fallback │  │   │
│  │  │ Checker  │ │  Guard   │ │ Validator│ │ Handler │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └─────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           History Compaction Layer                     │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │   │
│  │  │Summarizer│ │ Dedup    │ │ Priority Extractor   │  │   │
│  │  └──────────┘ └──────────┘ └──────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

Aquela arquitetura era o orgulho do time. Tinha resolvido os 3 problemas de Nível 1. Tinha implementado os 4 padrões de Nível 2. Quando um cliente reclamava de algo, o time abria o trace e sabia exatamente o que aconteceu. KODA era confiável.

Mas Fernando não estava ali para celebrar.

```
Fernando: "Vocês leram o changelog de sexta-feira?"

Dev Senior: "Li. Impressionante. Melhor instruction following, 
           janela de 200K, self-correction 3x melhor..."

Fernando: "Isso muda nossa arquitetura."

Dev Senior: "Como assim?"

Fernando: "A gente criou o Context Loader porque o modelo esquecia 
           informação depois de 40 minutos de conversa. O changelog 
           diz que o novo modelo mantém 98% de acurácia em 100K 
           tokens. Isso são umas 5 horas de conversa do KODA."

Dev Senior: "Então... o Context Loader..."

Fernando: "Talvez a gente não precise mais dele. Pelo menos não da 
           forma que está. E olha isso aqui — 'Auditable reasoning 
           chains now native'. Nós temos um Trace Layer inteiro para 
           forçar o modelo a expor raciocínio. Agora ele faz isso 
           sozinho."

Dev Junior: "Mas chefe, tudo isso funciona. Por que mexer?"
```

Esta é a pergunta que define a diferença entre um time que acumula complexidade e um time que a gerencia.

O Dev Junior não está errado. O sistema funciona. Os componentes fazem o que prometem. Mas a pergunta certa não é "funciona?". A pergunta certa é **"ainda é necessário?"**

```
Fernando: "Quanto custa o Context Loader?"

Dev Ops: "450ms de latência por turno. 1200 tokens por turno. 
         Em um mês típico, são 5.4 milhões de tokens e 3 horas 
         da gente mantendo."

Fernando: "E quantas falhas ele realmente preveniu nos últimos 
           90 dias?"

Dev Ops: "Deixa eu ver... [consulta dashboard]... 12 prevenções 
         reais em 145 mil turns. Mas também teve 340 falsos 
         positivos — bloqueou fluxos que estavam corretos."

Fernando: "12 em 145 mil. Isso é 0.008% de efetividade. A gente 
           gasta 5.4 milhões de tokens por mês, 450ms de latência 
           por turno, e 3 horas de manutenção... para prevenir 
           0.008% dos casos."
```

O silêncio que se seguiu foi o som de um time entendendo algo fundamental.

**O paradoxo do harness é este:** Ele existe para dar confiança. Mas se você nunca o revisa, ele se torna a própria fonte de fragilidade que deveria prevenir.

Cada componente desnecessário no harness significa:
- Mais superfície para bugs
- Mais latência entre o cliente perguntar e o KODA responder
- Mais tokens gastos em processamento que não agrega valor
- Mais complexidade para novos devs entenderem
- Mais arquivos de estado para manter e debugar
- Mais código para dar manutenção a cada mudança no modelo

Naquele dia, Fernando não decidiu remover nada. Ele decidiu algo mais importante: **criar um processo para decidir quando remover.**

```
Fernando: "A gente construiu esse harness para proteger um modelo 
           que não existe mais. O modelo de hoje é diferente. Mais 
           forte. E um harness desenhado para um modelo mais fraco 
           não é proteção — é peso morto."

Dev Junior: "Mas como a gente sabe o que pode remover sem quebrar 
            nada?"

Fernando: "Essa é exatamente a pergunta certa. E a resposta não é 
           'feeling'. A resposta é métricas, processo e coragem."
```

Este módulo é esse processo. É sobre como evoluir um harness de agente com a mesma disciplina que você usou para construí-lo. Porque construir é só metade do trabalho. **Saber quando desmontar é a outra metade.**

---

## 🎯 O Que É Harness Evolution?

### Definição Formal

**Harness Evolution** é a disciplina arquitetural de **revisar, simplificar e remover componentes do harness de agentes de IA** conforme:
1. Os modelos de linguagem subjacentes evoluem (novas capacidades, janelas maiores, melhor reasoning)
2. As métricas de produção mostram que proteções são redundantes ou de baixo valor
3. Os padrões de uso revelam que certas validações nunca disparam em cenários reais

Não é "jogar fora o que funciona". É **reconhecer que o harness certo para o modelo de 6 meses atrás pode ser o harness errado para o modelo de hoje.**

### Por Que Isso Importa — Os Números

Em sistemas tradicionais (APIs REST, bancos de dados, filas), você projeta uma arquitetura e ela dura anos. A peça central do sistema — Postgres, Redis, RabbitMQ — evolui lentamente e de forma previsível.

Em sistemas de agentes de IA, a peça central evolui a cada 3-6 meses:

| Período | Modelo | Janela de Contexto | Self-Correction | Harness Necessário |
|---------|--------|--------------------|----------------|-------------------|
| 6 meses atrás | Claude v1 | 32K tokens | Baixa (20%) | Pesado — 11 componentes |
| 3 meses atrás | Claude v2 | 100K tokens | Média (50%) | Médio — 8 componentes |
| Hoje | Claude v3 | 200K tokens | Alta (80%) | Leve — 5-6 componentes |

Se você não evolui o harness junto com o modelo, você mantém complexidade que o modelo já não precisa. É como manter as rodinhas de uma bicicleta depois que a criança aprendeu a se equilibrar. As rodinhas não ajudam mais — elas atrapalham.

### A Metáfora da Ponte

```
FASE 1: CONSTRUÇÃO — Andaimes são essenciais
  ┌──────────────────────────────────────────┐
  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ ← Andaimes (harness)
  │  ═══════════════════════════════════════  │ ← Ponte (modelo)
  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
  └──────────────────────────────────────────┘
  Se você tirar os andaimes agora, a ponte desaba.

FASE 2: ESTABILIZAÇÃO — Andaimes começam a ser removidos
  ┌──────────────────────────────────────────┐
  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
  │  ═══════════════════════════════════════  │
  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
  └──────────────────────────────────────────┘
  A ponte já se sustenta em várias seções.

FASE 3: OPERAÇÃO — Andaimes removidos
  ┌──────────────────────────────────────────┐
  │                                          │
  │  ═══════════════════════════════════════  │ ← Ponte independente
  │                                          │
  └──────────────────────────────────────────┘
  A ponte funciona sem suporte externo.

O ERRO COMUM: Nunca remover os andaimes.
O sistema "funciona", então ninguém mexe.
Mas os andaimes têm custo real.
```

**Harness Evolution é a disciplina de remover andaimes no momento certo — nem antes (a ponte cai), nem depois (você carrega peso morto para sempre).**

### O Que Não É Harness Evolution

- ❌ **Não é "jogar tudo fora e começar do zero".** Você remove componentes específicos, não o sistema inteiro.
- ❌ **Não é otimização prematura.** Você só simplifica depois de ter métricas reais de produção (60+ dias).
- ❌ **Não é "confiar cegamente no modelo".** Algumas proteções são invariantes e nunca saem.
- ❌ **Não é um projeto único.** É um ritmo — trimestral, como revisão de arquitetura.

---

## 🔄 O Ciclo de Vida do Harness

### As Quatro Fases

Todo componente de harness passa por um ciclo de vida previsível de 4 fases:

```
LANÇAMENTO DO MODELO (ou criação do componente)
      │
      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   ┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────┐│
│   │  BUILD   │──────▶│STABILIZE │──────▶│ SIMPLIFY │──────▶│REMOVE││
│   │          │       │          │       │          │       │      ││
│   └──────────┘       └──────────┘       └──────────┘       └──────┘│
│        │                  │                   │                  │  │
│        ▼                  ▼                   ▼                  ▼  │
│   "Preciso           "O harness         "O modelo           "Este  │
│    proteger           está confiá-       consegue            compo- │
│    o modelo           vel. Posso         lidar com           nente  │
│    das próprias       medir e            isso sem            não é  │
│    fraquezas"         observar"          tanta               mais   │
│                                          proteção"           neces- │
│                                                              sário" │
│                                                                     │
│   ═══════════════════════════════════════════════════════════════   │
│   CADA FASE TEM: Gatilhos → Atividades → Critérios de Saída         │
└─────────────────────────────────────────────────────────────────────┘
      │
      ▼
NOVO MODELO (ciclo reinicia com menos scaffolding inicial)
```

Vamos explorar cada fase em profundidade, com exemplos reais do KODA, código, e checklists.

---

### Fase 1: BUILD — "Preciso Proteger o Modelo das Próprias Fraquezas"

**Gatilho:** Um novo modelo é integrado, ou um novo padrão arquitetural é implementado pela primeira vez. Você ainda não conhece profundamente as capacidades e limitações do modelo em produção real.

**Mindset:** Defensivo. Você assume que o modelo vai falhar nos piores momentos possíveis e cria proteções para quando isso acontecer.

**Atividades desta fase:**

1. **Criar componentes de validação explícitos** — cada constraint que o modelo pode violar vira uma verificação separada
2. **Definir limites rígidos** — budgets de tokens, máximos de iterações, timeouts
3. **Implementar fallbacks generosos** — se uma estratégia falhar, tente outra, e outra, e outra
4. **Escrever system prompts longos e detalhados** — 2000-3000 tokens de instruções, exemplos, restrições
5. **Adicionar redundância** — dados críticos vão no system prompt E no user message E no state file
6. **Criar logs extensivos** — cada decisão, cada validação, cada bypass é registrado

**Exemplo KODA — O Context Loader Original (6 meses atrás):**

Quando o time implementou o Context Loader, o modelo da época (Claude v1, 32K tokens) tinha dificuldade real em manter acurácia após 30-40 minutos de conversa. Informações ditas no início da conversa simplesmente "desapareciam" da atenção do modelo.

A solução foi um componente robusto:

```json
{
  "component": "ContextLoader",
  "phase": "BUILD",
  "version": "1.0",
  "created": "2025-11-15",
  "rationale": "Modelo perde acurácia após ~40min de conversa. Informações críticas (alergias, orçamento, preferências) precisam ser re-carregadas explicitamente a cada turno.",
  
  "implementation": {
    "steps": [
      {
        "step": "pre_load_customer_profile",
        "action": "Ler customer_profile.json antes de CADA turno",
        "fields": ["alergias", "restrições", "objetivo", "orçamento", "histórico_compras"],
        "tokens": 400
      },
      {
        "step": "compress_history",
        "action": "Resumir mensagens com mais de 30 minutos em bullet points",
        "strategy": "Manter últimas 5 mensagens íntegras, resumir o resto",
        "tokens": 300
      },
      {
        "step": "tag_critical_info",
        "action": "Marcar alergias, restrições médicas e orçamento como HIGH_PRIORITY",
        "format": "[HIGH_PRIORITY] Cliente é ALÉRGICO A: glúten, amendoim",
        "tokens": 100
      },
      {
        "step": "inject_redundancy",
        "action": "Incluir dados críticos tanto no system prompt quanto no user message",
        "rationale": "Se o modelo ignorar um, lê o outro",
        "tokens": 400
      }
    ],
    "total_tokens_per_turn": 1200,
    "latency_added_ms": 450
  },

  "assumptions": [
    "Modelo NÃO mantém atenção em informações do início da conversa",
    "Modelo tende a priorizar informações recentes sobre informações antigas",
    "Redundância melhora recall de constraints críticas",
    "Compressão de histórico é lossy mas aceitável para informações não-críticas"
  ]
}
```

**Por que isso era correto na época:**
- O modelo realmente perdia contexto após ~40 minutos
- As 12 prevenções em 145K turns eram casos REAIS onde o cliente teria recebido recomendação errada
- O custo de 1200 tokens por turno se justificava pelo risco de perder um cliente

**O que NÃO era conhecido na época:**
- Que o próximo modelo teria 3x mais janela de contexto
- Que o próximo modelo teria instruction following muito melhor
- Que o próximo modelo naturalmente priorizaria constraints no system prompt

**Critério de saída do BUILD:**
- [x] Componente em produção por pelo menos 2 semanas
- [x] Zero incidentes críticos (P0/P1) atribuídos a falhas que o componente deveria prevenir
- [x] Time documentou o que o componente faz, por que existe, e quais assumptions justificam sua existência
- [x] Métricas básicas de latência e consumo de tokens estão sendo coletadas

---

### Fase 2: STABILIZE — "O Harness Está Confiável. Agora Posso Medir."

**Gatilho:** O componente está estável em produção por 60+ dias. Você tem dados suficientes para avaliar seu valor real — não o valor que você imaginava quando o criou.

**Mindset:** Observacional e analítico. Você confia que o componente funciona, mas quer PROVAS de que ele entrega valor proporcional ao seu custo.

**Atividades desta fase:**

1. **Dashboard de efetividade real** — quantas falhas o componente REALMENTE preveniu? (não "poderia prevenir")
2. **Análise de falsos positivos** — quantas vezes o componente bloqueou algo que estava correto?
3. **Custeio completo** — tokens, latência, horas de manutenção, custo de onboarding
4. **Testes A/B ou shadow mode** — rode COM e SEM o componente em paralelo e compare resultados
5. **Documentar o gap** — diferença entre "o que achávamos que prevenia" vs "o que realmente preveniu"

**Exemplo KODA — Context Loader após 3 meses em produção:**

```json
{
  "component": "ContextLoader",
  "phase": "STABILIZE",
  "version": "1.3",
  "in_production_since": "2025-11-20",
  "evaluation_date": "2026-02-20",

  "metrics_90_days": {
    "total_turns_processed": 145000,
    "avg_turns_per_conversation": 45,
    "avg_conversation_duration_min": 95,
    
    "effectiveness": {
      "critical_violations_prevented": 12,
      "non_critical_violations_prevented": 47,
      "effectiveness_rate": "0.04% (59 em 145000)",
      "note": "Apenas 1 a cada 2.500 turns resulta em prevenção real"
    },
    
    "false_positives": {
      "total": 340,
      "breakdown": {
        "alergia_mal_classificada": 120,
        "orçamento_interpretação_errada": 95,
        "preferência_detectada_errada": 85,
        "outros": 40
      },
      "note": "28x mais falsos positivos que prevenções reais"
    },
    
    "cost": {
      "tokens_per_turn": 1200,
      "tokens_monthly": 5400000,
      "api_cost_monthly_brl": 810,
      "latency_ms_per_turn": 450,
      "maintenance_hours_month": 3,
      "onboarding_complexity_score": "Alto (8/10) - novos devs levam 3-4 dias para entender"
    }
  },

  "shadow_test_results": {
    "period": "2026-02-01 a 2026-02-14",
    "traffic_split": "50% com ContextLoader, 50% sem",
    "findings": {
      "with_loader_accuracy": "97.2%",
      "without_loader_accuracy": "96.8%",
      "delta": "-0.4% (dentro da margem de erro)",
      "conclusion": "Diferença não é estatisticamente significativa"
    }
  },

  "model_update_note": "Desde upgrade para Claude v2 (2026-01-15), zero violações nos últimos 45 dias. O modelo mais forte parece estar tornando o Loader redundante."
}
```

**O Momento da Verdade:**

Esta é a fase onde a maioria dos times para. Eles veem as métricas, percebem que o componente tem custo desproporcional, mas decidem "não mexer no que está funcionando".

Este é o erro.

O propósito da fase STABILIZE não é eternizar o componente. É **produzir a evidência necessária para decidir se ele avança para SIMPLIFY ou permanece como está.**

**Critério de saída do STABILIZE:**
- [x] Pelo menos 60 dias de métricas em produção
- [x] Shadow test comparando com/sem o componente concluído
- [x] Dashboard mostrando taxa de acionamento real (não teórica)
- [x] Documento de gap analysis: esperado vs. real
- [x] Decisão explícita: AVANÇA PARA SIMPLIFY ou MANTÉM (com justificativa)

---

### Fase 3: SIMPLIFY — "O Modelo Agora Consegue Lidar com Isso"

**Gatilho:** Um dos três eventos ocorre:
1. Um novo modelo é lançado com capacidades documentadas que cobrem a fraqueza que o componente protegia
2. As métricas da fase STABILIZE mostram que o componente tem ROI negativo (custo > valor)
3. Um shadow test confirma que remover o componente não causa degradação significativa

**Mindset:** Cirúrgico e incremental. Você não arranca o componente de uma vez. Você reduz camada por camada, testa, observa, reduz mais. Cada redução é validada antes da próxima.

**O Que Simplificar (em ordem de segurança):**

```
NÍVEL DE RISCO DA SIMPLIFICAÇÃO
      ▲
      │  ALTO: Remover validações de segurança e constraints críticas
      │        ⚠️ Só faça com shadow test de 30+ dias
      │
      │  MÉDIO: Consolidar componentes redundantes
      │         ⚠️ Garanta que o componente absorvente cobre 100% dos casos
      │
      │  BAIXO: Remover redundância (dados duplicados, prompts longos)
      │         ⚠️ Comece por aqui — é o caminho mais seguro
      │
      │  MUITO BAIXO: Remover componentes que nunca disparam
      │              ✅ Faça primeiro — zero risco
      │
      └──────────────────────────────────────────────────────►
        ORDEM RECOMENDADA DE SIMPLIFICAÇÃO
```

**Exemplo KODA — Context Loader Simplificado (v2.0):**

Após o shadow test mostrar que a diferença sem o Loader era de apenas -0.4% (não significativo), o time planejou uma simplificação em 3 ondas:

```json
{
  "component": "ContextLoader",
  "phase": "SIMPLIFY",
  "version": "2.0",
  "simplification_date": "2026-03-01",
  
  "wave_1_remove_redundancy": {
    "date": "2026-03-01",
    "changes": [
      "Remover injeção dupla de dados críticos (system_prompt + user_message → só system_prompt)",
      "Remover tags HIGH_PRIORITY explícitas (modelo v2 prioriza naturalmente)",
      "Reduzir system prompt de 2000 para 800 tokens"
    ],
    "impact": {
      "tokens_saved_per_turn": 500,
      "latency_reduction_ms": 150,
      "risk": "BAIXO — dados críticos ainda estão no system prompt"
    },
    "validation_period": "7 dias",
    "result": "Acurácia manteve-se em 97.1%. Zero incidentes."
  },

  "wave_2_relax_constraints": {
    "date": "2026-03-15",
    "changes": [
      "Aumentar threshold de compressão de histórico: 30min → 90min",
      "Remover validação pós-turno de constraints (Evaluator já faz isso)",
      "Deixar de carregar customer_profile a cada turno — carregar só no início da conversa"
    ],
    "impact": {
      "tokens_saved_per_turn": 400,
      "latency_reduction_ms": 200,
      "risk": "MÉDIO — Validar com shadow test antes de 100%"
    },
    "validation_period": "14 dias com shadow test (50/50)",
    "result": "Acurácia 97.0% com loader simplificado vs 97.1% com loader completo. Delta não significativo. Avançar para 100%."
  },

  "wave_3_consolidate": {
    "date": "2026-04-01",
    "changes": [
      "Mover lógica residual do Context Loader para o History Compactor",
      "Context Loader deixa de existir como componente independente"
    ],
    "impact": {
      "tokens_saved_per_turn": 300,
      "latency_reduction_ms": 100,
      "risk": "MÉDIO — Consolidação exige refatoração",
      "total_impact": "1200 tokens/turno → 0 tokens/turno (absorvido pelo Compactor)"
    }
  }
}
```

**Resultado final da simplificação:**

| Métrica | Antes (v1.3) | Depois (v2.0) | Delta |
|---------|-------------|---------------|-------|
| Tokens/turno | 1200 | 0 (absorvido) | -100% |
| Latência/turno | 450ms | 0ms | -100% |
| Componentes | 1 dedicado | 0 (função absorvida) | -1 |
| Acurácia | 97.2% | 97.0% | -0.2% (não significativo) |
| Horas manutenção/mês | 3h | 0h | -100% |

O Context Loader não foi "deletado". Ele foi **absorvido**. A função essencial (garantir que informações críticas do cliente estejam disponíveis) continua existindo — mas agora como parte do History Compactor, sem a sobrecarga de um componente dedicado.

---

### Sinais de Que um Componente Está Pronto para Simplificação ou Remoção

Use esta tabela como um "scorecard" durante as revisões trimestrais:

| Sinal | O Que Observar | Threshold | Exemplo KODA |
|-------|----------------|-----------|--------------|
| **Taxa de acionamento baixa** | O componente raramente previne algo real | < 1% dos turns | Budget Guard: 0 disparos em 180 dias |
| **Falsos positivos altos** | Bloqueia mais fluxos corretos que incorretos | > 5x mais FPs que prevenções reais | Context Loader: 340 FPs vs 12 reais (28x) |
| **Modelo cobre a fraqueza** | Changelog do modelo documenta melhoria na área | Evidência no changelog + shadow test | "Improved instruction following across 100K+ contexts" |
| **Redundância entre componentes** | Dois componentes validam a mesma coisa | Overlap > 50% nas verificações | Context Loader + Constraint Checker + Evaluator validam alergias |
| **ROI negativo** | Custo (tokens + latência + manutenção) > valor (erros prevenidos × custo do erro) | Custo > 2× valor entregue | Budget Guard: R$ 200/mês em tokens para prevenir R$ 0 em erros |
| **Onboarding impactado** | Novos devs consistentemente perguntam "por que isso existe?" | > 2 perguntas de novos devs sobre o componente | Priority Extractor: "Por que não deixar o modelo decidir o que é prioritário?" |
| **Latência perceptível** | Usuário sente delay causado pelo componente | > 300ms adicionais por turno | Context Loader: 450ms/turno |

### Como Calcular o ROI de um Componente

```
ROI = (Erros Prevenidos × Custo Médio do Erro) / (Custo Operacional do Componente)

Onde:
- Erros Prevenidos = prevenções reais em 90 dias (não teóricas)
- Custo Médio do Erro = custo de um erro chegar ao cliente (reembolso + suporte + churn estimado)
- Custo Operacional = tokens (R$) + horas de manutenção (R$) + latência (custo de oportunidade)

Exemplo — Context Loader:
ROI = (59 × R$ 50) / (R$ 810 + R$ 450 + R$ 200)
ROI = R$ 2,950 / R$ 1,460
ROI = 2.0x (positivo mas marginal)

Exemplo — Budget Guard:
ROI = (0 × R$ 50) / (R$ 200 + R$ 100)
ROI = R$ 0 / R$ 300
ROI = 0x (negativo — remova imediatamente)
```

Se o ROI for menor que 1x por dois trimestres consecutivos, o componente é candidato a remoção.

---

### Fase 4: REMOVE — "Este Componente Cumpriu Seu Propósito"

**Gatilho:** O componente passou pela simplificação e mesmo na sua forma mais enxuta:
- Sua taxa de acionamento real é < 0.1%
- O shadow test confirma que removê-lo não causa degradação
- Nenhum incidente nos últimos 90 dias foi prevenido por ele
- O modelo atual cobre completamente a proteção que ele oferecia

**Mindset:** Decisivo e documentado. Você não está "jogando fora trabalho". Você está **reconhecendo que o trabalho cumpriu seu propósito e agora é desnecessário.**

**Atividades desta fase:**

1. **Remover o componente do fluxo principal** (atrás de feature flag, não delete direto)
2. **Observar por 14 dias** com monitoramento ativo
3. **Arquivar o código** em `archive/components/<nome>/` com README explicando:
   - Quando foi criado e por quê
   - Quando foi removido e por quê
   - Que modelo justificou a remoção
   - Lições aprendidas
4. **Atualizar documentação** de arquitetura, runbooks, playbooks
5. **Comunicar ao time** com um post-mortem positivo

**Exemplo KODA — Remoção do Budget Guard:**

```json
{
  "component": "BudgetGuard",
  "phase": "REMOVE",
  "created": "2025-10-01",
  "removed": "2026-04-15",
  
  "original_purpose": "Monitorar consumo de tokens por turno e truncar conversa ao atingir 80% da janela de contexto (32K tokens). Prevenir que o modelo recebesse input truncado e gerasse respostas incompletas.",
  
  "why_remove": {
    "primary_reason": "Janela de contexto expandiu de 32K para 200K tokens (6.25x maior). Conversas típicas do KODA consomem 50K tokens. O limite de 80% de 200K = 160K tokens nunca é atingido em produção.",
    "supporting_evidence": [
      "Zero disparos em 180 dias de produção",
      "Shadow test (30 dias, 50% tráfego): zero diferença entre com e sem o componente",
      "Custo operacional: R$ 200/mês em tokens + 1h/mês manutenção",
      "Modelo atual lida bem com contextos longos (documentado no changelog v3)"
    ]
  },
  
  "removal_process": {
    "week_1": "Feature flag: 5% tráfego sem Budget Guard",
    "week_2": "Feature flag: 25% tráfego sem Budget Guard",
    "week_3": "Feature flag: 100% tráfego sem Budget Guard",
    "week_4": "Remover código, arquivar em archive/components/budget-guard-v1/"
  },
  
  "post_removal_metrics": {
    "monitoring_period": "2026-04-15 a 2026-04-29 (14 dias)",
    "regressions": 0,
    "token_budget_exceeded": 0,
    "incomplete_responses": 0,
    "customer_satisfaction": "Estável (88% → 88%)",
    "incidents": 0
  },
  
  "archived_at": "archive/components/budget-guard-v1/",
  "archive_readme": "Budget Guard protegia o KODA quando o modelo tinha janela de 32K tokens. Com a migração para Claude v3 (200K tokens), tornou-se redundante. Removido em abril/2026 sem incidentes. Lição: componentes que dependem de limites de hardware evoluem quando o hardware evolui."
}
```

**O que acontece com o código removido:**

```
archive/
└── components/
    └── budget-guard-v1/
        ├── README.md           # Por que existiu, por que foi removido
        ├── src/                # Código original (referência futura)
        ├── metrics/
        │   └── 180-days.json   # Métricas que justificaram a remoção
        └── decisions/
            └── removal-adr.md  # ADR documentando a decisão
```

O código NÃO é deletado. É arquivado. Daqui a 2 anos, se alguém perguntar "por que o KODA não tem Budget Guard?", a resposta está documentada. Se um novo modelo tiver janela menor, o código está lá para ser reavaliado.

---

## ⚠️ Anti-Padrões de Harness Evolution

Saber o que NÃO fazer é tão importante quanto saber o que fazer.

### Anti-Padrão 1: "Big Bang Removal"

**O que é:** Remover múltiplos componentes do harness de uma vez, sem feature flags, sem shadow testing, sem canary deploy.

**Por que é perigoso:** Se algo quebrar, você não sabe qual remoção causou o problema. Rollback significa reverter TODAS as remoções, perdendo o trabalho das que estavam corretas.

**Como evitar:** Uma remoção por vez. Feature flag independente para cada componente. Período de observação de 14 dias entre remoções.

```
❌ ERRADO:
   Sprint 1: Remover Budget Guard + Format Validator + Dedup Layer
   Resultado: Algo quebrou. O que foi? Ninguém sabe.

✅ CERTO:
   Sprint 1: Remover Budget Guard → observar 14 dias → ✅ estável
   Sprint 2: Remover Format Validator → observar 14 dias → ✅ estável
   Sprint 3: Remover Dedup Layer → observar 14 dias → ✅ estável
```

---

### Anti-Padrão 2: "Nunca Remover Nada"

**O que é:** O time acumula componentes de harness indefinidamente. "Se funciona, não mexe." O sistema cresce em complexidade a cada trimestre.

**Por que é perigoso:** Complexidade acumulada não é neutra — ela é ativamente prejudicial. Cada componente extra:
- Torna o sistema mais lento
- Torna o debugging mais difícil (mais lugares para procurar)
- Torna o onboarding mais lento
- Aumenta a superfície para bugs
- Torna mudanças futuras mais arriscadas (medo de quebrar algo)

**Sinal de alerta:** Se o diagrama de arquitetura do seu harness é maior hoje do que era há 6 meses, você provavelmente está acumulando complexidade.

```
❌ ERRADO:
   Trimestre 1: +2 componentes (total: 8)
   Trimestre 2: +1 componente (total: 9)
   Trimestre 3: +2 componentes (total: 11)
   Trimestre 4: "Precisamos reescrever tudo, está complexo demais"

✅ CERTO:
   Trimestre 1: +2 componentes, -1 removido (total: 7)
   Trimestre 2: +1 componente, -2 removidos (total: 6)
   Trimestre 3: +1 componente, -1 removido (total: 6)
   Trimestre 4: Arquitetura estável, complexidade controlada
```

---

### Anti-Padrão 3: "Remover Porque o Modelo Novo é Melhor (sem testar)"

**O que é:** Ler o changelog de um modelo novo, assumir que ele resolve tudo, e remover componentes sem shadow testing.

**Por que é perigoso:** O changelog descreve benchmarks controlados, não seu caso de uso específico. O modelo pode ser melhor em média mas pior no caso específico que seu componente protegia.

**Como evitar:** SEMPRE faça shadow testing antes de remover. O changelog é uma hipótese, não uma prova.

```
❌ ERRADO:
   Changelog: "Self-correction improved 3x"
   Time: "Ótimo, vamos remover o Evaluator!"
   Resultado: Sycophancy volta. Recomendações erradas passam.

✅ CERTO:
   Changelog: "Self-correction improved 3x"
   Time: "Vamos fazer shadow test: 50% tráfego com Evaluator, 50% sem."
   Resultado (2 semanas depois): Sem Evaluator, acurácia cai 8%.
   Decisão: Manter Evaluator. A melhoria foi em tarefas gerais, não no domínio KODA.
```

---

### Anti-Padrão 4: "Simplificar Demais"

**O que é:** Remover tantos componentes que o harness fica frágil. O sistema funciona bem no caso comum mas quebra em edge cases.

**Por que é perigoso:** Edge cases em produção são justamente os casos que causam os piores incidentes (alergias não detectadas, cobranças erradas, dados perdidos).

**Como evitar:** Mantenha proteções para invariantes (segurança, compliance, decisões irreversíveis). Simplifique agressivamente o resto, mas NUNCA os invariantes.

```
❌ ERRADO — Harness simplificado demais:
   Sistema → Modelo → Cliente
   (Sem Evaluator, sem state persistence, sem fallback)
   Problema: Funciona 95% do tempo. Os 5% que falham são catastróficos.

✅ CERTO — Harness essencial:
   Sistema → State Loader → Modelo → Evaluator → Cliente
   (State para memória, Evaluator para qualidade)
   Complexidade: 2 componentes. Cobertura: 99.7%.
```

---

## 📊 Estratégias de Coordenação: O Antes e Depois da Evolução

Conforme o harness evolui, a forma como os componentes se coordenam também muda. Menos componentes significa menos coordenação necessária — e isso é bom.

### Tabela Comparativa de Estratégias

| Dimensão | Harness Pesado (Modelo Antigo) | Harness Evoluído (Modelo Atual) | Ganho |
|----------|-------------------------------|--------------------------------|-------|
| **Coordenação entre agentes** | File-based com 5-7 arquivos JSON por turno | File-based com 2-3 arquivos JSON por turno | -60% I/O, -40% latência |
| **Validação de output** | Evaluator dedicado + Constraint Checker + Format Validator (3 stages) | Evaluator unificado (cobre os 3 em 1 stage) | -2 componentes, -300 tokens/turno |
| **Gestão de contexto** | Context Loader (pré) + History Compactor (pós) + Dedup | History Compactor (pós) apenas para conversas > 2h | -2 componentes, -800 tokens/turno |
| **Planejamento** | Planner Agent dedicado — sempre roda, toda conversa | Planner condicional — só em 30% das jornadas (complexas) | -70% de chamadas de Planner |
| **Tratamento de erros** | 3 estratégias de fallback (retry → alternativa → humano) | 1 estratégia (retry simples, depois escala) | -2 code paths, -150ms |
| **System prompts** | 2000-3000 tokens detalhados | 500-800 tokens com princípios | -70% tokens de prompt |
| **Checagem de constraints** | Pré-validação + Pós-validação + Redundância (3 checkpoints) | Pós-validação única pelo Evaluator | -2 checkpoints, -200 tokens/turno |
| **Trace e auditoria** | 4 arquivos separados (plan.json, draft.json, eval.json, decision_log.jsonl) | 2 arquivos (state.json + audit_log.jsonl) | -50% arquivos, -30% complexidade de debug |

### O Pipeline Antes e Depois

**Antes (Harness Pesado — 11 componentes):**

```
CLIENTE PERGUNTA
      │
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Context     │────▶│ Dedup       │────▶│ Priority    │
│ Loader      │     │ Layer       │     │ Extractor   │
│ (450ms)     │     │ (200ms)     │     │ (150ms)     │
└─────────────┘     └─────────────┘     └─────────────┘
                                                │
      ┌─────────────────────────────────────────┘
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Planner     │────▶│ Generator   │────▶│ Constraint  │
│ Agent       │     │ Agent       │     │ Checker     │
│ (800ms)     │     │ (1200ms)    │     │ (300ms)     │
└─────────────┘     └─────────────┘     └─────────────┘
                                                │
      ┌─────────────────────────────────────────┘
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Format      │────▶│ Evaluator   │────▶│ Fallback    │
│ Validator   │     │ Agent       │     │ Handler     │
│ (100ms)     │     │ (600ms)     │     │ (200ms)     │
└─────────────┘     └─────────────┘     └─────────────┘
                                                │
      ┌─────────────────────────────────────────┘
      ▼
RESPOSTA AO CLIENTE

LATÊNCIA TOTAL: ~4000ms
TOKENS/TURNO: ~3200
COMPONENTES: 11
```

**Depois (Harness Evoluído — 6 componentes):**

```
CLIENTE PERGUNTA
      │
      ▼
┌─────────────────────────────────────────────┐
│ State Loader (apenas início da conversa)     │
│ Carrega customer_profile.json                │
│ (200ms, só na primeira mensagem)             │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Generator   │────▶│ Evaluator   │────▶│ History     │
│ Agent       │     │ Agent       │     │ Compactor   │
│ (800ms)     │     │ (500ms)     │     │ (condicional)│
└─────────────┘     └─────────────┘     └─────────────┘
                                                │
      ┌─────────────────────────────────────────┘
      ▼
RESPOSTA AO CLIENTE

LATÊNCIA TOTAL: ~1500ms (-62%)
TOKENS/TURNO: ~1400 (-56%)
COMPONENTES: 6 (-45%)
```

O pipeline simplificado é mais rápido, mais barato e mais fácil de debugar. E a acurácia? Praticamente a mesma — porque os componentes removidos não estavam mais prevenindo erros reais.

---

## 🧹 Checklist de Remoção de Scaffolding

Use este checklist ANTES de remover qualquer componente. Ele previne os dois erros mais comuns: remover cedo demais (causando regressão) e nunca remover (acumulando complexidade).

### Pré-Remoção: Evidências Necessárias

- [ ] **Métrica de acionamento real:** Taxa de disparo nos últimos 90 dias documentada
- [ ] **Métrica de falsos positivos:** Quantos fluxos corretos foram bloqueados nos últimos 90 dias
- [ ] **Custeio completo:** Tokens (R$), latência (ms), horas/manutenção (h/mês)
- [ ] **Cálculo de ROI:** (Erros prevenidos × custo do erro) / Custo operacional. Se < 1x, documentar
- [ ] **Cobertura redundante:** Algum outro componente existente cobre a mesma proteção? Qual?
- [ ] **Modelo atual:** Capacidades documentadas do modelo em produção (changelog, benchmarks internos)
- [ ] **Shadow test:** Concluído com pelo menos 14 dias de dados e diferença não significativa
- [ ] **Conjunto de testes de regressão:** Casos que exercitam os cenários que o componente protegia
- [ ] **Plano de rollback:** Código versionado, feature flag permite reativação em < 1 hora
- [ ] **Alerta configurado:** Dispara se a métrica protegida degradar > 10% após remoção

### Durante a Remoção: Passos Seguros

- [ ] **Feature flag:** Remoção atrás de `feature_flags.remove_<componente>` (NUNCA delete direto)
- [ ] **Shadow mode (se aplicável):** Rodar com componente desativado em ambiente de staging por 2 dias
- [ ] **Canary 5%:** Ativar sem o componente para 5% do tráfego por 24 horas
- [ ] **Canary 25%:** Expandir para 25% do tráfego por mais 24 horas
- [ ] **Canary 100%:** Expandir para 100% do tráfego
- [ ] **Monitoramento ativo:** Dashboard específico para o período (taxa de erro, latência, CSAT, acurácia)
- [ ] **Alerta ativo:** Notificação imediata se métricas degradarem além do threshold

### Pós-Remoção: Confirmação de Estabilidade

- [ ] **14 dias sem regressão:** Nenhum incidente P0/P1 atribuído à remoção
- [ ] **Métricas estáveis:** KPIs do sistema dentro da baseline pré-remoção
- [ ] **Satisfação do cliente:** NPS/CSAT sem queda significativa no período
- [ ] **Custo reduzido:** Tokens e latência diminuíram conforme esperado
- [ ] **Documentação atualizada:** Diagrama de arquitetura, runbooks e playbooks refletem a remoção
- [ ] **Código arquivado:** Componente em `archive/components/<nome>/` com README
- [ ] **ADR escrito:** Documento formal registrando a decisão de remoção e suas justificativas
- [ ] **Time comunicado:** Todos os desenvolvedores sabem que o componente foi removido e por quê
- [ ] **Post-mortem positivo:** Documento celebrando: "Removemos X. Nada quebrou. Ganhamos Y."

---

## 🧠 Quando Modelos Mais Fortes Mudam o Design

### O Ciclo de Feedback: Modelo → Arquitetura → Modelo

A evolução dos modelos de linguagem não é linear — cada salto de capacidade abre portas para simplificações arquiteturais que antes eram impensáveis.

```
CAPACIDADE DO MODELO
      ▲
      │                                    ┌─────────────┐
      │                                    │   REMOVER   │ ← Componentes se tornam
      │                              ┌─────│             │   desnecessários
      │                              │     └─────────────┘
      │                        ┌─────┤
      │                        │     │     ┌─────────────┐
      │                  ┌─────┤     └─────│ SIMPLIFICAR │ ← Reduzir redundância,
      │                  │     │           │             │   consolidar funções
      │            ┌─────┤     │           └─────────────┘
      │            │     │     │
      │      ┌─────┤     └─────┤           ┌─────────────┐
      │      │     │           └───────────│ ESTABILIZAR │ ← Coletar métricas,
      │      │     │                       │             │   provar valor real
      │      │     │                       └─────────────┘
      │      │     │
      │      │     └───────────────────────┌─────────────┐
      │      │                             │  CONSTRUIR  │ ← Proteger o modelo
      │      │                             │             │   das próprias fraquezas
      │      │                             └─────────────┘
      │      │
      └──────┴──────────────────────────────────────────────────►
         v1.0           v2.0           v3.0           v4.0
       32K ctx       100K ctx       200K ctx      native audit
       weak IF       better IF      strong IF     self-correct
       low recall    medium recall  high recall   structured out
```

### Impacto por Melhoria do Modelo

| Melhoria | Sinal no Changelog | Componentes Afetados | Ação Recomendada |
|----------|--------------------|--------------------|------------------|
| **Contexto 2x+ maior** | "Expanded context window to N tokens" | History Compactor, Context Loader, Dedup, Priority Extractor | Aumentar thresholds de compressão; remover redundância de carga de contexto |
| **Instruction Following melhor** | "Improved instruction following accuracy" | System Prompts longos, Constraint Checkers redundantes, Format Validators | Reduzir prompts (2000 → 500 tokens); consolidar checkers |
| **Raciocínio auditável nativo** | "Auditable reasoning chains now native" | Trace Layer customizado, Decision Logger, Reasoning Extractor | Usar output nativo do modelo em vez de forçar com prompting |
| **Auto-correção 3x+ melhor** | "Self-correction accuracy improved" | Fallback Handler complexo, múltiplas estratégias de retry, Evaluator redundante | Reduzir iterações de feedback; simplificar fallback |
| **Structured Output nativo** | "Native JSON mode / structured output" | Format Validator, Output Parser, Schema Enforcer | Remover (modelo produz JSON válido por construção) |
| **Grounding factual melhor** | "Improved factual accuracy" | Fact Checker, Source Validator, Hallucination Detector | Reduzir para domínios de alto risco apenas (saúde, finanças) |
| **Velocidade de inferência** | "Latency reduced by X%" | Cache Layer, Pre-computation, Batch Processing | Reavaliar necessidade de cache se latência não é mais problema |

### Quando NÃO Remover — Mesmo com Modelo Melhor

Algumas proteções são **invariantes arquiteturais**. Sua presença não depende da qualidade do modelo — depende da natureza do domínio ou do sistema.

| Invariante | Por Que É Permanente | Exemplo KODA |
|------------|---------------------|--------------|
| **Segurança do cliente** | Alergias, contraindicações, dados sensíveis não são "qualidade de output" — são proteção de vida e privacidade | Verificação de alergias: NUNCA removível |
| **Compliance regulatório** | LGPD, PCI-DSS, regulamentações de saúde exigem validações específicas, independentemente do modelo | Validação de consentimento LGPD: NUNCA removível |
| **Decisões irreversíveis** | Cobrança, envio de pedido, alteração de dados — precisam de checkpoint humano ou de sistema | Confirmação de pagamento: NUNCA removível |
| **Fallback de disponibilidade** | O modelo pode ficar offline (API outage, rate limit). Fallback não protege contra falha do modelo — protege contra falha do SERVIÇO | Retry + fila de mensagens: NUNCA removível |
| **Evaluator (gatekeeper)** | Sycophancy é um problema ESTRUTURAL de LLMs, não de qualidade de modelo. Mesmo modelos perfeitos podem ser sycophantic | Evaluator Agent: NUNCA removível |
| **State Persistence** | Auditabilidade, debugging, recuperação de falhas — sem estado persistente, não há como saber o que aconteceu | Arquivos JSON de estado: NUNCA removível |

---

## 🏛️ Arquitetura como Affordance de Agente: Refatorando para Deep Modules

Harness Evolution trata de remover componentes externos que se tornaram desnecessários. Mas há uma estratégia complementar e mais profunda: **refatorar o código da aplicação para que o próprio agente navegue melhor, reduzindo a necessidade de harness desde a raiz**.

O padrão **Architecture-as-Agent-Affordance Refactoring** (extraído do workflow de Matt Pocock) parte de uma premissa simples: agentes de IA sofrem com código acoplado, interfaces complexas e módulos rasos. Cada arquivo que o agente precisa ler para entender uma mudança é carga cognitiva que consome tokens e degrada a qualidade. A arquitetura do código é, portanto, uma **affordance** (uma propriedade do ambiente que convida a uma ação correta) — e pode ser melhorada deliberadamente para reduzir o custo cognitivo de sessões futuras de agente.

### Sinais de que a Arquitetura Está Dificultando o Agente

| Sinal | O Agente... | Causa Arquitetural |
|-------|------------|-------------------|
| **Exploração excessiva** | Lê 12+ arquivos para uma mudança de 1 arquivo | Dependências espalhadas, sem encapsulamento |
| **Erros de interface** | Chama função com parâmetros errados repetidamente | Interface pública complexa, muitos parâmetros opcionais |
| **Mudanças em cascata** | Altera 5 arquivos para uma feature que deveria tocar 1 | Módulos rasos que não encapsulam comportamento |
| **Testes frágeis** | Quebra testes não relacionados ao mudar uma função | Testes acoplados a implementação, não a comportamento |
| **Paralisia de decisão** | Fica indeciso sobre onde colocar o código novo | Módulo sem responsabilidade clara, múltiplos lugares "possíveis" |

### O Padrão Deep Module

Um **deep module** (termo de John Ousterhout, adaptado para contexto de agentes) é um módulo que:

1. **Esconde complexidade atrás de uma interface simples** — o agente vê 1-2 funções públicas, não 15 internals
2. **Encapsula comportamento, não apenas dados** — o módulo sabe "processar pedido", não apenas "guardar pedido"
3. **Tem boundary tests que verificam contrato, não implementação** — o agente pode refatorar internals sem quebrar testes

**Antes (módulo raso — difícil para o agente):**
```
order_utils.ts    — 15 funções exportadas, nenhuma ownership clara
order_validator.ts — 8 funções, algumas duplicam order_utils
pricing.ts         — 12 funções, acoplado a order_utils e cart.ts
cart.ts            — 20 funções, estado misturado com lógica
```
O agente precisa ler 4 arquivos e ~55 funções para entender como "aplicar desconto no pedido".

**Depois (deep module — o agente vê uma interface):**
```
order/
  index.ts          — 3 exports: createOrder, applyDiscount, submitOrder
  internals/        — complexidade escondida, agente não precisa ler
  order.test.ts     — testa createOrder, applyDiscount, submitOrder (boundary)
```
O agente lê 1 arquivo, 3 funções. Carga cognitiva reduzida em 90%.

### Refatoração como Estratégia de Harness Evolution

Esta abordagem complementa o ciclo BUILD → STABILIZE → SIMPLIFY → REMOVE com uma dimensão estrutural:

| Estratégia | Atua em | Exemplo |
|-----------|---------|---------|
| **Harness Evolution** | Componentes externos ao código (wrappers do modelo) | Remover Budget Guard porque o modelo já não estoura contexto |
| **Architecture Affordance** | Estrutura interna do código (módulos, interfaces, testes) | Extrair `order/` como deep module para que o agente não precise de Context Loader para navegar |

**Quando aplicar refatoração de affordance:**
- Durante o planejamento de uma feature, identifique se o código existente forçaria o agente a ler muitos arquivos
- Se sim, modele a refatoração como **primeira fatia vertical** do trabalho
- Crie issues de follow-up no backlog de arquitetura para módulos identificados como "rasos"
- Apply boundary tests ANTES da refatoração (lock behavior) e use-os como prova de que a refatoração não quebrou nada

**Exemplo KODA — aplicação em Order Processing:**
```
Diagnóstico: Agente lê 7 arquivos para processar validação de pedido
  → order_utils.ts, order_validator.ts, pricing.ts, cart.ts,
    promo_engine.ts, inventory.ts, shipping.ts

Plano de refatoração (fatia vertical):
  S1: Extrair Pricing deep module (applyDiscount, calculateTotal)
       → Boundary tests: desconto de clube, cupom, double-discount
  S2: Extrair Inventory deep module (checkAvailability, reserveStock)
       → Boundary tests: estoque regional, race condition
  S3: Extrair Order deep module (create, validate, submit)
       → Boundary tests: pedido completo, falha de pagamento, idempotência

Resultado: Agente lê 3 arquivos (pricing/index, inventory/index, order/index)
          em vez de 7. Tokens de exploração reduzidos em 60%.
          Menos necessidade de harness de contexto.
          Menos erros de interface.
```

### Checklist de Affordance Architecture

Antes de iniciar uma implementação com agente, verifique:
- [ ] O módulo que será alterado tem menos de 5 exports públicos?
- [ ] As funções públicas têm nomes que descrevem comportamento, não implementação?
- [ ] Existem boundary tests que sobreviveriam a uma refatoração interna?
- [ ] O agente consegue entender o contrato lendo apenas os testes?
- [ ] Dependências entre módulos são explícitas e unidirecionais?
- [ ] Há um "single place to look" para cada comportamento de negócio?

Se a resposta for NÃO para 2+ itens, a arquitetura está criando carga cognitiva que o harness precisará compensar. Considere refatorar como pré-requisito da feature.

Este padrão conecta-se ao [[curriculum/02-nivel-2-practical-patterns/02-sprint-contracts|Sprint Contracts]] (a interface do deep module é o contrato que o agente segue) e ao módulo de [[curriculum/05-core-concepts/06-harness-evolution|Harness Evolution Core Concept]] (a arquitetura bem fatorada reduz a necessidade de harness).

---

## 🗺️ Estratégia de Evolução Incremental

Evolução de harness não é um projeto com começo, meio e fim. É um **processo contínuo** integrado ao ritmo de desenvolvimento do time.

### O Ritmo Trimestral

```
TRIMESTRE 1              TRIMESTRE 2              TRIMESTRE 3
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ REVIEW + PLAN  │     │ REVIEW + PLAN  │     │ REVIEW + PLAN  │
│ (semana 1)     │     │ (semana 1)     │     │ (semana 1)     │
├────────────────┤     ├────────────────┤     ├────────────────┤
│ IMPLEMENT      │     │ IMPLEMENT      │     │ IMPLEMENT      │
│ (semanas 2-3)  │     │ (semanas 2-3)  │     │ (semanas 2-3)  │
├────────────────┤     ├────────────────┤     ├────────────────┤
│ OBSERVE        │     │ OBSERVE        │     │ OBSERVE        │
│ (semanas 4-12) │     │ (semanas 4-12) │     │ (semanas 4-12) │
└────────────────┘     └────────────────┘     └────────────────┘
```

**Review & Plan (Semana 1):**
- Analisar changelog do modelo mais recente
- Revisar métricas de todos os componentes do harness (dashboard)
- Classificar cada componente: KEEP, SIMPLIFY, REMOVE, INVESTIGATE
- Priorizar por impacto: maior redução de custo/latência primeiro
- Criar cards no board com plano de ação para cada componente classificado como SIMPLIFY ou REMOVE

**Implement (Semanas 2-3):**
- Aplicar simplificações atrás de feature flags
- Executar shadow tests para componentes candidatos a remoção
- Remover componentes classificados como REMOVE (com checklist)
- Atualizar documentação técnica e diagramas de arquitetura
- Rodar bateria completa de testes de regressão

**Observe (Semanas 4-12):**
- Monitorar métricas pós-mudança (dashboard dedicado)
- Coletar dados para o próximo ciclo de review
- NÃO fazer novas mudanças no harness neste período
- Documentar lições aprendidas para o próximo trimestre

### Tabela: Componentes Atuais do KODA → Evolução Planejada

| # | Componente | Função | Fase Atual | Ação | Gatilho | Prazo |
|---|-----------|--------|------------|------|---------|-------|
| 1 | Budget Guard | Monitorar consumo de tokens | REMOVE | ✅ Removido (Q1) | 0 disparos em 180 dias | Q1 2026 |
| 2 | Format Validator | Validar estrutura JSON do output | SIMPLIFY | Remover | 30 dias sem erro de formato | Q2 2026 |
| 3 | Context Loader | Recarregar dados do cliente a cada turno | SIMPLIFY | Absorver no History Compactor | Shadow test: delta < 0.5% | Q2 2026 |
| 4 | Constraint Checker | Validar constraints do cliente | SIMPLIFY | Consolidar no Evaluator | Evaluator cobre 100% dos casos | Q2 2026 |
| 5 | Dedup Layer | Remover informações duplicadas do contexto | INVESTIGATE | Avaliar se Compactor já resolve | Métricas de duplicação pós-Compactor | Q3 2026 |
| 6 | Priority Extractor | Marcar informações críticas | INVESTIGATE | Testar inferência nativa do modelo | Acurácia em constraints sem tags | Q3 2026 |
| 7 | Fallback Handler | Estratégias alternativas em falha | STABILIZE | Reduzir 3 → 1 estratégia | Taxa de falha do modelo < 0.1% | Q3 2026 |
| 8 | Planner Agent | Criar plano antes de executar | STABILIZE | Tornar condicional (30% dos casos) | Modelo planeja implicitamente em 70% | Q3 2026 |
| 9 | History Compactor | Comprimir conversas longas | KEEP | Manter (essencial para > 2h) | — | Permanente |
| 10 | Evaluator Agent | Validar outputs contra rubrics | KEEP | Manter (gatekeeper anticorrupção) | — | Permanente |
| 11 | State Persistence | Arquivos JSON fonte de verdade | KEEP | Manter (auditabilidade) | — | Permanente |
| 12 | Trace Layer | Registrar decisões para debug | KEEP | Manter (memória institucional) | — | Permanente |

### O Princípio "One In, One Out"

Para evitar que o harness cresça indefinidamente, adote esta regra:

> **Sempre que um componente novo é adicionado ao harness, um componente existente deve ser marcado para investigação de remoção no próximo ciclo trimestral.**

Isso não significa remover imediatamente. Significa criar uma hipótese: "Se este novo componente funciona, qual componente existente ele pode substituir?"

```
EXEMPLO:
  Adicionado: "Smart Context Loader v3" (usa embeddings para priorização)
  Marcado para investigação: "Priority Extractor" (função sobreposta)
  Hipótese: Smart Context Loader pode absorver a função do Priority Extractor
  Próximo ciclo: Shadow test para validar hipótese
```

---

## 🚀 Aplicação KODA: Roadmap de Evolução do Harness

### Onde Estamos Hoje (Maio 2026)

O harness do KODA está na transição entre STABILIZE e SIMPLIFY. Dos 11 componentes originais, 1 já foi removido (Budget Guard), 3 estão em simplificação ativa, e 2 estão sob investigação.

### Estado Atual do Harness

```
┌──────────────────────────────────────────────────────────────┐
│                KODA HARNESS — Maio 2026                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🔴 REMOVIDOS (1):                                     │   │
│  │    Budget Guard — removido Q1 2026, zero regressões   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🟡 SIMPLIFICANDO (3):                                  │   │
│  │    Context Loader — onda 2 de simplificação           │   │
│  │    Constraint Checker — consolidando no Evaluator     │   │
│  │    Format Validator — shadow test em andamento        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🔵 INVESTIGANDO (2):                                   │   │
│  │    Dedup Layer — avaliando redundância                │   │
│  │    Priority Extractor — testando inferência nativa    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🟢 PERMANENTES (5):                                    │   │
│  │    Generator Agent, Evaluator Agent,                  │   │
│  │    History Compactor, State Persistence, Trace Layer  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Métricas de Baseline (Maio 2026)

| Métrica | Antes da Evolução (Q4 2025) | Atual (Q2 2026) | Alvo (Q4 2026) |
|---------|---------------------------|-----------------|----------------|
| Latência média/turno | 1.8s | 1.4s | < 0.9s |
| Tokens/turno | 3,200 | 2,600 | < 1,500 |
| Componentes no harness | 11 | 10 ativos (1 removido) | 6-7 |
| Arquivos de estado/conversa | 7 | 6 | 4 |
| Horas manutenção/mês | 18h | 15h | 8h |
| Tempo onboarding novo dev | 3 semanas | 2.5 semanas | 1.5 semanas |
| Acurácia (avaliação humana) | 96.5% | 97.1% | ≥ 97% |
| Custo mensal API | R$ 4,200 | R$ 3,600 | R$ 2,500 |
| CSAT (satisfação) | 85% | 87% | ≥ 88% |

### Roadmap de Evolução (2026)

```
MAIO 2026 (Agora)
  │
  ├── SEMANA 1-2: Análise do Trimestre
  │   • Revisar métricas dos 10 componentes ativos
  │   • Concluir shadow test do Format Validator
  │   • Atualizar classificação: KEEP / SIMPLIFY / REMOVE / INVESTIGATE
  │   • Priorizar: maior economia de latência primeiro
  │
  ├── SEMANA 3-4: Onda 2 — Simplificações (Baixo-Médio Risco)
  │   • Remover Format Validator (shadow test mostrou zero degradação)
  │   • Concluir consolidação Constraint Checker → Evaluator
  │   • Avançar Context Loader para onda 3 (absorção pelo Compactor)
  │   • Feature flags: 5% → 25% → 100% para cada mudança
  │
  ├── JUNHO 2026: Observação
  │   • Monitorar Onda 2 por 4 semanas
  │   • Coletar métricas pós-simplificação
  │   • Validar que acurácia não degradou
  │   • Preparar casos de teste para Onda 3
  │
  ├── JULHO 2026: Onda 3 — Remoções Estruturais (Médio Risco)
  │   • Absorver Context Loader no History Compactor
  │   • Reduzir Fallback Handler de 3 para 1 estratégia
  │   • Aumentar threshold do History Compactor (30min → 2h)
  │   • Shadow test de 14 dias para cada mudança
  │
  ├── AGOSTO 2026: Observação
  │   • Monitorar Onda 3 por 4 semanas
  │   • Se novo modelo lançado, reavaliar componentes remanescentes
  │   • Decidir sobre Dedup Layer e Priority Extractor
  │
  └── SETEMBRO 2026: Onda 4 — Otimizações Condicionais (se aplicável)
      • Planner condicional (só em jornadas complexas)
      • Remover Dedup Layer (se Compactor resolver)
      • Remover Priority Extractor (se modelo inferir naturalmente)
      • Documentar arquitetura final simplificada (target: 6-7 componentes)
```

### Cenário: Evoluindo uma Jornada Completa do KODA

Vamos acompanhar a mesma jornada de cliente — uma descoberta de produto com recomendação — em três momentos diferentes da evolução do harness:

**Dezembro 2025 (Harness Pesado — 11 componentes):**

```
Cliente: "Quero um whey protein vegano, sem glúten, até R$ 150"

Pipeline:
Context Loader (450ms) → Dedup (200ms) → Priority Extractor (150ms)
→ Planner (800ms) → Generator (1200ms) → Constraint Checker (300ms)
→ Format Validator (100ms) → Evaluator (600ms) → Fallback Handler (200ms)

Latência total: ~4000ms
Tokens: ~3200
Componentes acionados: 9 de 11
Resultado: ✅ Recomendação correta
Custo/turno: R$ 0.048
```

**Junho 2026 (Harness em Simplificação — 8 componentes):**

```
Cliente: "Quero um whey protein vegano, sem glúten, até R$ 150"

Pipeline:
State Loader (200ms, só 1a msg) → Generator (800ms)
→ Evaluator + Constraint Check (500ms, unificados) → History Compactor (condicional)

Latência total: ~1500ms (-62%)
Tokens: ~1500 (-53%)
Componentes acionados: 4 de 8
Resultado: ✅ Recomendação correta (mesma acurácia)
Custo/turno: R$ 0.022 (-54%)
```

**Setembro 2026 (Harness Essencial — 6 componentes):**

```
Cliente: "Quero um whey protein vegano, sem glúten, até R$ 150"

Pipeline:
State Loader (200ms, só 1a msg) → Generator (700ms)
→ Evaluator (400ms) → History Compactor (condicional, > 2h)

Latência total: ~1300ms (-67% vs original)
Tokens: ~1200 (-62% vs original)
Componentes acionados: 3-4 de 6
Resultado: ✅ Recomendação correta
Custo/turno: R$ 0.018 (-62%)
```

A qualidade da recomendação é a mesma. Mas o sistema é 3x mais rápido, 2.6x mais barato, e tem metade dos componentes para manter e debugar.

---

## 🎯 Key Takeaways

1. **Harness Evolution é um ciclo, não um evento.** BUILD → STABILIZE → SIMPLIFY → REMOVE. A cada trimestre, revise. A cada novo modelo, reavalie.

2. **Remover é tão importante quanto construir.** Complexidade que não é mais necessária é dívida técnica ativa. Ela torna o sistema mais lento, mais caro e mais frágil.

3. **Decida com dados, não com intuição.** Se um componente previne 0.008% dos erros mas custa 15% dos tokens, as métricas respondem — seu instinto não.

4. **Simplifique incrementalmente, nunca em big bang.** Feature flags, shadow tests, canary deploy. Uma mudança por vez, validada por 14 dias.

5. **Modelos melhores mudam o design.** Contexto maior → menos compressão. Instruction following melhor → prompts mais curtos. Structured output nativo → menos validadores.

6. **Invariantes são permanentes.** Segurança, compliance, decisões irreversíveis, fallback de disponibilidade, Evaluator (gatekeeper) e State Persistence NUNCA saem.

7. **One In, One Out.** Cada componente novo força a investigação de um existente para remoção. O harness não cresce — ele se transforma.

---

## ✅ Checkpoint: O Que Você Aprendeu

### Fundamentos do Ciclo de Vida

- [ ] Consigo explicar as 4 fases (BUILD, STABILIZE, SIMPLIFY, REMOVE) e o que acontece em cada uma
- [ ] Entendo o mindset de cada fase e os critérios de saída
- [ ] Consigo dar exemplos reais do KODA para cada fase

### Sinais, Métricas e Decisões

- [ ] Consigo listar e aplicar os 7 sinais de que um componente pode ser removido
- [ ] Sei calcular o ROI real de um componente (prevenções × custo do erro / custo operacional)
- [ ] Entendo a diferença entre "taxa de acionamento teórica" e "taxa de acionamento real"
- [ ] Consigo identificar quando NÃO remover (invariantes arquiteturais)

### Processo de Remoção

- [ ] Consigo aplicar o checklist completo (pré-remoção, durante, pós-remoção)
- [ ] Entendo o valor de feature flags, shadow tests e canary deploy
- [ ] Sei que código removido deve ser ARQUIVADO com documentação, não deletado
- [ ] Sei que o período mínimo de observação pós-remoção é 14 dias

### Modelo, Arquitetura e Impacto

- [ ] Consigo mapear melhorias de changelog para componentes do harness que podem ser simplificados
- [ ] Entendo a diferença entre "proteção de arquitetura" (permanente) e "muleta de modelo" (temporária)
- [ ] Consigo explicar por que Evaluator, State Persistence e Trace Layer são permanentes no KODA
- [ ] Entendo o impacto de cada simplificação em latência, tokens e complexidade

### Estratégia KODA

- [ ] Consigo explicar o roadmap de evolução do KODA (Ondas 1-4, 2026)
- [ ] Consigo ler e interpretar a tabela de componentes atuais e evolução planejada
- [ ] Entendo o princípio "One In, One Out" e como aplicá-lo
- [ ] Consigo visualizar a diferença entre o pipeline pesado (2025) e o pipeline essencial (2026)

### Aplicação Prática

- [ ] Consigo identificar, no meu próprio sistema, pelo menos 1 componente candidato a simplificação
- [ ] Posso estimar o custo real de um componente (tokens + latência + manutenção) usando as fórmulas do módulo
- [ ] Entendo que evolução de harness é um ritmo trimestral contínuo, não um projeto único
- [ ] Sei que a pergunta certa não é "funciona?" — é "ainda é necessário?"

**Se respondeu NÃO a mais de 2 itens:** Releia a fase SIMPLIFY e o checklist de remoção. São as seções mais práticas e operacionais.

**Se respondeu SIM a todos:** Você está pronto para liderar a evolução do harness no seu time. O próximo passo é aplicar o checklist no seu próprio sistema.

---

## 📚 Referências & Próximas Leituras

### Dentro do Currículo (Nível 3)

- `01-multi-agent-systems.md` — A arquitetura multi-agente que a evolução vai simplificar
- `02-state-persistence.md` — Invariante: o componente que nunca sai do harness
- `03-file-based-coordination.md` — Como componentes se comunicam (e como simplificar essa comunicação)
- `04-server-side-compaction.md` — Técnica de compactação que substitui parte do harness de contexto

### Dentro do Currículo (Nível 2)

- `01-generator-evaluator-pattern.md` — O padrão que originou o Evaluator (componente permanente)
- `04-trace-reading.md` — Como usar traces para gerar métricas de efetividade do harness
- `koda-applications/nivel-2-koda.md` — O harness do KODA antes da evolução (para comparar)

### Próximo Nível

- `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md` — Arquitetura completa atual do KODA
- `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` — Melhorias contínuas e otimizações

### Guias e Ferramentas

- `IMPLEMENTATION_GUIDES/06-harness-evolution-playbook.md` — Playbook passo a passo da revisão trimestral
- `IMPLEMENTATION_GUIDES/03-harness-design-checklist.md` — Checklist de design inicial (baseline para comparar)
- `TEMPLATES/architecture-decision-record-template.md` — Template para ADR de remoção de componente

### Conceitos Core

- `CORE_CONCEPTS/06-harness-evolution.md` — Visão conceitual complementar
- `CORE_CONCEPTS/07-multi-agent-coordination.md` — Coordenação que evolui com o harness

### Externo

- Anthropic model changelogs — Fonte primária para identificar capacidades que permitem simplificação
- Documentação de feature flags (LaunchDarkly, Split.io, ou flags caseiras)
- "Kill Code" — práticas de remoção de código em sistemas distribuídos
- Post-mortems de times que removeram componentes com sucesso

---

## 💭 Reflexão Final

Existe uma frase que aparece em retrospectivas de times de engenharia no mundo todo:

> *"Esse sistema está complexo demais. Precisamos reescrever."*

A reescrita raramente é a resposta certa. O que o time está sentindo é o **peso acumulado de componentes que já cumpriram seu propósito e nunca foram removidos.**

Harness Evolution oferece uma alternativa à reescrita: a disciplina de remover o que não é mais necessário, com segurança, baseado em métricas.

Fernando não reescreveu o KODA. Em 6 meses, ele removeu 5 dos 11 componentes do harness. A latência caiu de 1.8s para 0.9s. O custo de API caiu 33%. O onboarding de novos devs ficou 30% mais rápido.

E a acurácia? **Subiu.** Porque um sistema mais simples:
- É mais fácil de debugar
- É mais fácil de monitorar
- É mais fácil de manter correto
- Tem menos superfície para bugs
- Deixa os devs focarem no que importa

A lição mais profunda do Nível 3 não é sobre adicionar complexidade. É sobre saber quando removê-la.

**Construir um harness é um ato de humildade.** Você reconhece que o modelo tem fraquezas e cria proteções.

**Evoluir um harness é um ato de confiança.** Você reconhece que o modelo melhorou, que as proteções fizeram seu trabalho, e que é hora de seguir em frente com uma arquitetura mais leve.

Bons arquitetos constroem sistemas que funcionam.

Grandes arquitetos constroem sistemas que **continuam simples** conforme evoluem.

Este módulo fecha o Nível 3. Você começou com sistemas multi-agente. Passou por persistência de estado, coordenação por arquivos e compactação de histórico.

Agora você sabe: **o destino de toda boa arquitetura de agentes não é crescer para sempre. É evoluir para o essencial.**

---

### Anti-Padrão 5: "Evoluir Sem Documentar"

**O que é:** Remover ou simplificar componentes sem registrar a decisão, as métricas que a justificaram, e o processo de validação.

**Por que é perigoso:** Daqui a 6 meses, ninguém vai lembrar por que o Budget Guard foi removido. Um novo dev pode recriá-lo. Um incidente pode fazer o time questionar a decisão sem ter os dados que a justificaram.

**Como evitar:** Para cada componente removido, escreva um ADR (Architecture Decision Record) com:
- Data da decisão
- Componente removido
- Métricas que justificaram a remoção
- Processo de validação (shadow test, canary, período de observação)
- Resultado pós-remoção
- Link para o código arquivado

```
❌ ERRADO:
   Remove Budget Guard. Duas semanas depois, ninguém lembra por quê.
   Seis meses depois: "Por que não temos Budget Guard? Vamos criar um!"

✅ CERTO:
   Remove Budget Guard. ADR escrito. Código arquivado com README.
   Seis meses depois: alguém pergunta, o ADR responde.
   Decisão informada: "O modelo atual tem 200K de contexto, não precisamos."
```

---

## ❓ Perguntas Frequentes

### P: "Se o harness funciona, por que eu deveria remover partes dele?"

**R:** Porque "funciona" não é o único critério. Cada componente tem custo real: latência que o cliente sente, tokens que você paga, complexidade que o time carrega. Se um componente previne 0.008% dos erros mas custa 15% dos tokens e 450ms de latência, o custo supera o benefício. A pergunta não é "funciona?" — é "ainda é necessário com este modelo?"

### P: "Como sei que não vou me arrepender de ter removido algo?"

**R:** Você não remove baseado em intuição. Você remove baseado em: (1) shadow test de 14+ dias mostrando que sem o componente a acurácia não cai, (2) 90 dias de métricas mostrando que o componente raramente previne erros reais, (3) changelog do modelo documentando que a fraqueza protegida foi resolvida, (4) feature flag que permite reativar em minutos se algo der errado. Se todos os 4 critérios são atendidos, a probabilidade de arrependimento é mínima.

### P: "Quanto tempo devo esperar antes de remover um componente?"

**R:** No mínimo 60 dias de métricas em produção + 14 dias de shadow test + 14 dias de canary deploy. Total: ~90 dias do início da investigação até a remoção completa. Isso parece muito, mas lembre-se: você está removendo uma proteção que existe há meses. A pressa é inimiga da segurança aqui.

### P: "E se o modelo for downgradado ou eu precisar voltar atrás?"

**R:** Por isso você ARQUIVA, não deleta. O código do componente removido fica em `archive/components/<nome>/` com README, métricas e ADR. Se um dia você precisar reativá-lo (modelo downgradado, novo caso de uso, regulação nova), o código está lá, documentado, pronto para ser reavaliado. Feature flag também permite reativação imediata sem deploy.

### P: "Posso automatizar a decisão de remover?"

**R:** Parcialmente. Você pode automatizar a coleta de métricas (dashboard que mostra taxa de acionamento, falsos positivos, ROI de cada componente). Mas a decisão final de remover deve ser humana — envolve julgamento sobre risco, contexto de negócio, e compreensão das invariantes arquiteturais. O que você pode automatizar é o alerta: "Componente X está com ROI < 1x há 2 trimestres. Agende revisão."

### P: "Qual a diferença entre Harness Evolution e otimização normal?"

**R:** Otimização normal foca em performance: "como fazer a mesma coisa mais rápido". Harness Evolution foca em necessidade: "essa coisa ainda precisa ser feita?" Otimização ajusta parâmetros. Harness Evolution remove componentes inteiros. São disciplinas complementares — você otimiza o que mantém, e remove o que não precisa mais.

### P: "Devo aplicar Harness Evolution em sistemas que não usam IA?"

**R:** O conceito de "remover proteções quando a peça central melhora" se aplica a qualquer sistema. Mas em sistemas tradicionais, a peça central (banco de dados, fila, cache) evolui lentamente. Em sistemas de IA, a peça central evolui a cada 3-6 meses. Por isso Harness Evolution é especialmente crítico para agentes de IA — a velocidade de evolução do modelo torna a revisão do harness uma necessidade trimestral, não anual.

---

## 🛠️ Ferramentas para Harness Evolution

Algumas ferramentas e padrões que ajudam a implementar Harness Evolution no dia a dia:

### Dashboard de Efetividade do Harness

Crie um dashboard que mostre, para cada componente:

```
┌────────────────────────────────────────────────────────────┐
│              HARNESS EFFECTIVENESS DASHBOARD                │
│                                                            │
│  Componente        Acionamentos  Falsos+   ROI    Status   │
│  ──────────────────────────────────────────────────────── │
│  Context Loader       0.04%       28x     2.0x   🟡 SIMP  │
│  Budget Guard         0.00%       N/A     0.0x   🔴 REMV  │
│  Format Validator     0.12%       3x      4.5x   🟢 KEEP  │
│  Constraint Checker   0.80%       1.2x    12x    🟢 KEEP  │
│  Dedup Layer          0.01%       15x     0.8x   🔵 INV   │
│  Evaluator Agent      8.50%       0.3x    45x    🟢 KEEP  │
│  Planner Agent        35.0%*      0.5x    18x    🟢 KEEP  │
│                                                            │
│  *Planner é condicional — só 35% das conversas acionam     │
│  🟢 KEEP  🟡 SIMPLIFY  🔵 INVESTIGATE  🔴 REMOVE          │
└────────────────────────────────────────────────────────────┘
```

### Script de Cálculo de ROI

Um script simples que o time pode rodar a cada trimestre:

```python
# harness_roi.py — calcule o ROI de cada componente
import json

def calculate_roi(component_name, metrics):
    errors_prevented = metrics["real_preventions_90d"]
    cost_per_error = metrics["avg_cost_per_error_brl"]
    tokens_cost = metrics["tokens_monthly_cost_brl"]
    maintenance_cost = metrics["maintenance_hours_month"] * 150  # R$/hora
    latency_cost = metrics["latency_ms"] * metrics["turns_month"] * 0.00001
    
    value_delivered = errors_prevented * cost_per_error
    operational_cost = tokens_cost + maintenance_cost + latency_cost
    
    roi = value_delivered / operational_cost if operational_cost > 0 else float('inf')
    
    status = "🔴 REMOVE" if roi < 0.5 else \
             "🔵 INVESTIGATE" if roi < 1.0 else \
             "🟡 SIMPLIFY" if roi < 2.0 else \
             "🟢 KEEP"
    
    return {
        "component": component_name,
        "roi": round(roi, 2),
        "value_delivered": value_delivered,
        "operational_cost": operational_cost,
        "status": status
    }

# Exemplo de uso
context_loader_metrics = {
    "real_preventions_90d": 59,
    "avg_cost_per_error_brl": 50,
    "tokens_monthly_cost_brl": 810,
    "maintenance_hours_month": 3,
    "latency_ms": 450,
    "turns_month": 45000
}

result = calculate_roi("ContextLoader", context_loader_metrics)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### Feature Flag Pattern

Implemente feature flags com granularidade por componente:

```yaml
# harness_flags.yaml
feature_flags:
  harness:
    budget_guard:
      enabled: false
      removed_date: 2026-04-15
      archive_path: archive/components/budget-guard-v1/
    
    format_validator:
      enabled: false
      canary_percentage: 100
      shadow_test_active: true
      shadow_test_since: 2026-05-01
    
    constraint_checker:
      enabled: true
      consolidation_target: evaluator_agent
      consolidation_date: 2026-06-15
    
    context_loader:
      enabled: true
      simplification_wave: 2
      simplified_version: "v2.0"
```

### Template de ADR para Remoção

```markdown
# ADR-0XX: Remoção do Componente [NOME]

**Data:** YYYY-MM-DD
**Status:** Aceito
**Decisão:** Remover o componente [NOME] do harness do KODA.

## Contexto
[Descreva o que o componente fazia, quando foi criado, e qual problema resolvia]

## Evidências
- Métricas de acionamento real (90 dias): [X%]
- Falsos positivos: [Y]
- Shadow test (14 dias): delta de acurácia [Z%] (não significativo)
- Custo operacional: [R$ tokens/mês + horas manutenção]
- Modelo atual: [versão, capacidades relevantes do changelog]

## Processo de Remoção
- Feature flag: [datas e percentuais do canary]
- Período de observação pós-remoção: [14 dias]
- Incidentes no período: [0]
- Métricas pós-remoção: [acurácia, latência, CSAT]

## Rollback
- Código arquivado em: `archive/components/[nome]/`
- Feature flag permite reativação em < 1 hora
- Alerta configurado para: [métrica] > [threshold]

## Consequências
- Positivas: [redução de latência, tokens, complexidade]
- Negativas: [nenhuma observada]
- Riscos aceitos: [descreva se houver]
```

---

**Pronto para o Nível 4? O KODA te espera.**

---

*Escrito com foco em clareza, relevância prática e a coragem de remover o que não serve mais.*  
*Memória: Um harness que nunca é revisado se torna o problema que deveria resolver.*

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` |
| **Nível** | 3 - Arquitetura Avançada |
| **Tempo** | 90 minutos |
| **Status** | ✅ Completo |
| **Próximo** | `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md` |
| **Dependências** | Módulos 01-04 do Nível 3 |
| **Atualizado** | Maio 2026 |
