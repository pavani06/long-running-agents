---
title: "Exercício 3: Plano de Evolução do Harness KODA"
type: curriculum-exercise
nivel: 3
aliases: []
tags: [curriculo-conteudo, nivel-3, exercicio, harness-evolution, architecture-review, roi-analysis, component-removal, build-stabilize-simplify-remove, changelog-driven-decisions, false-positive-analysis, shadow-test, feature-flag, cost-optimization, exercicio-conceitual]
relates-to: ["[[curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination|File-Based Coordination]]"]
last_updated: 2026-06-10
---
# ⚙️ Exercício 3: Plano de Evolução do Harness KODA
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 60–90 minutos
**Dificuldade:** ⭐⭐⭐ (Intermediário-Avançado)
**Pré-requisito:** Ter completado `05-harness-evolution.md` e os Exercícios 1–2 do Nível 3
**Objetivo:** Analisar um harness real do KODA com métricas de produção e propor um plano de evolução arquitetural em 3 fases, aplicando o ciclo BUILD → STABILIZE → SIMPLIFY → REMOVE

---

## 📖 Prólogo: A Planilha Que Mudou Tudo

**Quinta-feira, 14h30. War room do time KODA.**

Fernando estava em silêncio há quase dois minutos. Isso era incomum. Normalmente ele já teria coberto o quadro branco com setas, círculos e a frase "a pergunta certa é..." escrita em letras garrafais.

Mas dessa vez ele só olhava para a tela do notebook. E pedia para o time fazer o mesmo.

Na tela, uma planilha simples. Três abas: **Métricas**, **Custos**, **Incidentes**.

```
═══════════════════════════════════════════════════════════════
                  KODA HARNESS — RELATÓRIO TRIMESTRAL
                        Período: Fev–Abr 2026
═══════════════════════════════════════════════════════════════

COMPONENTE            ACIONAMENTOS  FALSOS+   TOKENS/MÊS   ROI
───────────────────────────────────────────────────────────────
Context Loader            0.04%       28x     5.400.000    0.8x
Budget Guard              0.00%       N/A       800.000    0.0x
Format Validator          0.12%        3x     1.200.000    8.8x
Constraint Checker        0.80%       1.2x    3.100.000   25.0x
Dedup Layer               0.01%       15x     2.000.000    0.4x
Priority Extractor        0.05%        8x     1.500.000    2.7x
Planner Agent            35.00%       0.5x    8.200.000    N/A†
Fallback Handler          0.02%        6x       900.000    1.7x
Generator Agent         100.00%       0.1x   22.000.000    N/A‡
Evaluator Agent           8.50%       0.3x   12.000.000   45.0x
History Compactor        12.00%       0.2x    4.500.000    N/A†

*Generator é o core — não se aplica ROI

LATÊNCIA MÉDIA POR TURNO: 1.8s
TOKENS TOTAIS/MÊS: 61.700.000
CUSTO API MENSAL: R$ 9.240
HORAS MANUTENÇÃO/MÊS: 18h
═══════════════════════════════════════════════════════════════
```

O time ficou em silêncio também. Não porque os números fossem chocantes. Mas porque ninguém nunca tinha olhado para o harness **desse jeito** — como uma carteira de investimentos onde cada ativo precisa justificar seu retorno.

```
Dev Senior: "Budget Guard... zero acionamentos em três meses?"

Fernando: "Zero. E custa R$ 800 mil tokens por mês. Isso são 
           R$ 120 que a gente gasta para prevenir... nada."

Dev Ops: "Mas o Budget Guard foi uma das primeiras coisas que a 
         gente construiu. Era essencial quando o modelo tinha 
         32K de contexto."

Fernando: "Exatamente. Era. O modelo de hoje tem 200K. Esse 
           componente não está protegendo nada — está só 
           consumindo recurso."

Dev Junior: "Se a gente remover, e algo quebrar?"

Fernando: "Essa é a pergunta errada. A pergunta certa é: 'Se a 
           gente remover, qual a probabilidade real de algo 
           quebrar?' E a resposta está na planilha: 0.00% em 90 
           dias. Não é 'provavelmente seguro remover'. É 
           'comprovadamente seguro remover'."
```

O Dev Ops começou a anotar. O Dev Senior abriu o editor de código. Mas Fernando os interrompeu:

```
Fernando: "Antes de abrir o editor, quero que vocês percebam uma 
           coisa. O Budget Guard é o caso óbvio. Zero acionamentos, 
           zero risco. Mas olhem essa linha aqui."

Ele destacou três componentes na planilha:

Fernando: "Dedup Layer — ROI de 0.8x. Fallback Handler — ROI de 
           0.6x. Priority Extractor — ROI de 1.1x. Esses três estão 
           na zona cinzenta. Não são obviamente removíveis. Mas 
           também não estão claramente se pagando."

Dev Senior: "O Dedup Layer remove informações duplicadas do 
            contexto. Mas o History Compactor já faz compressão. 
            Se o Compactor já reduz redundância, a Dedup está 
            fazendo trabalho duplicado?"

Fernando: "Excelente pergunta. É exatamente esse tipo de raciocínio 
           que eu quero. Não 'funciona?'. Mas 'outro componente já 
           faz isso?'"

Dev Ops: "E o Fallback Handler? Três estratégias de fallback. Mas 
         o modelo atual falha em menos de 0.1% dos turns. Três 
         estratégias é over-engineering?"

Fernando: "Provavelmente. Mas aqui é diferente do Budget Guard. 
           Fallback tem 29 acionamentos reais em 90 dias. Pouco, 
           mas não zero. A pergunta é: quantos desses 29 teriam 
           sido resolvidos com UMA estratégia de fallback em vez 
           de três?"

Dev Junior: "Como a gente descobre isso?"

Fernando: "Shadow test. Roda 50% do tráfego com 1 estratégia, 50% 
           com 3. Compara taxa de sucesso. Se for igual, reduzimos. 
           Essa é a diferença entre 'achar' e 'saber'."
```

E então, no momento em que o time já estava convencido de que precisava agir, Fernando fez a jogada que definiu a reunião. Ele projetou o changelog do modelo recém-lançado na parede:

```
═══════════════════════════════════════════════════════════════
           NOVO MODELO — CLAUDE v4 (LANÇAMENTO: MAIO 2026)
═══════════════════════════════════════════════════════════════

✅ Janela de contexto: 200K → 500K tokens (2.5x maior)
✅ Instruction following: 94% → 98.7% de acurácia
✅ Self-correction: 3x melhor em domínios de e-commerce
✅ Raciocínio auditável: reasoning chains nativas no output
✅ Structured Output: JSON mode nativo com validação de schema
✅ Grounding factual: +40% de precisão em dados de produto
✅ Latência de inferência: -35% em relação ao modelo anterior

NOTAS DO CHANGELOG:
"O modelo agora mantém >99% de acurácia em contextos de até 
 300K tokens sem perda de atenção. Informações no system 
 prompt são priorizadas automaticamente, sem necessidade de 
 tags explícitas. O JSON mode garante conformidade de schema 
 sem validação pós-output."
═══════════════════════════════════════════════════════════════
```

O silêncio voltou. Mas dessa vez era diferente. Não era o silêncio de quem está processando dados. Era o silêncio de quem está vendo o chão se mover.

```
Dev Senior: "Isso muda... quase tudo."

Fernando: "Muda. A pergunta não é mais 'o que podemos melhorar?' 
           A pergunta é: 'Quais desses 11 componentes ainda são 
           necessários com ESSE modelo?'"

Dev Junior: "Mas chefe, a gente vai mesmo redesenhar a 
            arquitetura inteira?"

Fernando: "Não. A gente vai fazer algo mais inteligente. A 
           gente vai criar um plano. Três fases. Cada fase 
           remove ou simplifica um conjunto de componentes. 
           Cada remoção é validada antes da próxima. Nada de 
           big bang. Nada de 'confiar no modelo e torcer'. 
           Métricas, feature flags, shadow tests. Disciplina."
```

Ele abriu um documento em branco e escreveu no topo:

```
PLANO DE EVOLUÇÃO DO HARNESS KODA — v4.0
Modelo-alvo: Claude v4 (Maio 2026)
Duração: 3 fases, 12 semanas
Objetivo: Reduzir 11 componentes para 6–7 essenciais
```

```
Dev Ops: "E se algo der errado na Fase 2?"

Fernando: "Feature flag. A gente reverte em minutos. Código 
           arquivado, não deletado. Se o modelo for downgradado 
           amanhã, o Budget Guard está lá, documentado, pronto 
           para ser reavaliado. A gente não está queimando pontes. 
           Está removendo andaimes de uma ponte que já se sustenta 
           sozinha."

Dev Junior: "E como a gente convence o resto da empresa de que 
            remover código é tão importante quanto escrever?"

Fernando: "Mostra essa planilha. R$ 9.240 por mês. 18 horas de 
           manutenção. 3 semanas de onboarding. Isso não é custo 
           de infraestrutura. É custo de complexidade que a gente 
           carrega porque nunca parou para perguntar 'ainda 
           precisamos disso?'"
```

**Agora é a sua vez.**

Você é o arquiteto que vai preencher esse plano. Você tem os mesmos dados que o time do Fernando. As mesmas métricas, o mesmo changelog, os mesmos 11 componentes.

A diferença entre um sistema que custa R$ 9.240/mês e outro que custa R$ 6.000/mês — com a mesma qualidade — não está no modelo. Está nas decisões que você vai tomar agora.

---

## 🧭 Como Ler Este Exercício

Este exercício é extenso porque simula uma situação real de arquitetura. Você não está respondendo perguntas de múltipla escolha — está tomando decisões de design com consequências de custo, latência e risco.

### Estrutura de Navegação

O exercício está organizado em camadas de profundidade:

1. **O Cenário** — Os dados brutos que você precisa analisar (métricas, changelog, descrições de componentes). Leia uma vez com atenção. Depois volte para consultar.

2. **Sua Tarefa (Partes 1–5)** — O trabalho que você vai entregar. As 5 partes são progressivas: da análise individual de cada componente até a visão agregada do plano completo.

3. **Templates e Exemplos** — Estruturas prontas para você preencher. Use os exemplos como referência de profundidade esperada, não como gabarito.

4. **Rubric de Avaliação** — Os critérios que definem a diferença entre um plano nota 7 e um plano nota 10. Leia antes de começar para saber o que é valorizado.

5. **Referências e Solução** — Material de apoio e solução de referência para comparar depois.

### Tempo Recomendado por Parte

| Parte | Atividade | Tempo |
|-------|----------|-------|
| Leitura do cenário | Absorver métricas e changelog | 10 min |
| Parte 1 — Análise de Impacto | Classificar 11 componentes com justificativas | 15 min |
| Parte 2 — Plano de 3 Fases | Estruturar fases com ações, gates e estimativas | 20 min |
| Parte 3 — Critérios de Validação | Definir thresholds e métodos | 10 min |
| Parte 4 — Tabela Comparativa | Preencher Antes/Depois | 10 min |
| Parte 5 — Invariantes e Riscos | Identificar o que nunca sai e por quê | 10 min |
| Revisão final | Verificar consistência entre partes | 5 min |

### Princípios Que Você Deve Aplicar

Antes de começar, mantenha estes princípios em mente. Eles são o "norte" que deve guiar suas decisões:

1. **Dados acima de intuição.** Se as métricas mostram que um componente nunca dispara, a resposta é "remover", não "mas e se um dia precisar?"

2. **Risco incremental.** A Fase 1 deve ser a de menor risco possível. Isso gera confiança no time, dados para as fases seguintes, e um track record de "removemos X, nada quebrou".

3. **Simplificar antes de remover.** Se um componente tem ROI marginal (0.5x–1.5x), considere reduzir seu escopo antes de eliminá-lo. Exemplo: reduzir de 3 estratégias de fallback para 1, em vez de remover o Fallback Handler inteiro.

4. **Invariantes não se negociam.** Existe uma diferença entre "proteção que o modelo não precisa mais" e "proteção que transcende a qualidade do modelo". Alergias, compliance, decisões irreversíveis — esses são invariantes.

5. **Uma fase por vez, validada.** Nada de remover 5 componentes de uma vez. Se algo quebrar, você não sabe qual remoção causou o problema. Cada fase tem seu período de shadow test, canary deploy e observação.

6. **O changelog é uma hipótese, não uma prova.** "Self-correction 3x melhor" é um dado de benchmark, não de produção. Antes de remover uma proteção baseada nisso, valide com shadow test no seu domínio específico.

---

## 🎯 O Contexto

### O Que É o Harness do KODA?

O KODA é um agente de vendas via WhatsApp que conduz conversas de 2+ horas com clientes. Para garantir que essas conversas sejam seguras, precisas e auditáveis, o KODA não depende apenas do modelo de linguagem — ele usa um **harness**: uma camada de componentes arquiteturais que orquestram, validam e protegem cada interação.

O harness atual tem **11 componentes**, construídos ao longo de 12 meses para proteger um modelo (Claude v2, 32K tokens) que já não está mais em produção. O time de desenvolvimento nunca fez uma revisão sistemática de quais componentes ainda são necessários — eles foram acumulando proteções a cada trimestre, sem nunca remover as antigas.

Este exercício é exatamente essa revisão.

### O Que Você Vai Fazer

Você vai receber três conjuntos de dados e, com base neles, vai tomar decisões arquiteturais:

1. **O estado atual do harness** — Métricas reais de 90 dias de produção, incluindo taxa de acionamento, falsos positivos, consumo de tokens, custo operacional e ROI de cada componente
2. **O changelog de um novo modelo** — Capacidades documentadas que potencialmente tornam várias proteções do harness redundantes
3. **Um template de plano de evolução** — Estruturado em 3 fases progressivas, com gates de validação entre elas

Você vai entregar:
- Análise de impacto de cada componente (Parte 1)
- Plano de evolução em 3 fases com ações, estimativas e cronograma (Parte 2)
- Critérios de validação com thresholds numéricos (Parte 3)
- Tabela comparativa Antes/Depois (Parte 4)
- Análise de invariantes e riscos (Parte 5)

### Por Que Este Exercício É Diferente

Nos exercícios anteriores do Nível 3, você aprendeu a:
- **Exercício 1:** Mapear o fluxo de comunicação entre agentes em um sistema multi-agente
- **Exercício 2:** Projetar arquivos de estado e estratégias de persistência para jornadas longas

Este exercício vai além de projetar — ele testa sua capacidade de **julgar**. Você não está construindo algo novo. Você está olhando para algo que existe, que funciona, e decidindo o que manter, o que reduzir e o que eliminar.

Essa é a habilidade mais difícil em arquitetura de software — e a mais valiosa.

---

## 🔍 O Cenário: Harness Atual do KODA

### Arquitetura Atual (11 Componentes)

```
┌──────────────────────────────────────────────────────────────────┐
│                    KODA HARNESS — ABRIL 2026                       │
│                                                                    │
│  CLIENTE PERGUNTA                                                  │
│       │                                                            │
│       ▼                                                            │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌───────────┐       │
│  │ Context │──▶│  Dedup   │──▶│ Priority │──▶│  Budget   │       │
│  │ Loader  │   │  Layer   │   │Extractor │   │  Guard    │       │
│  │ (450ms) │   │ (200ms)  │   │ (150ms)  │   │ (100ms)   │       │
│  └─────────┘   └──────────┘   └──────────┘   └───────────┘       │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │                 CORE AGENTS                               │     │
│  │  ┌──────────┐   ┌────────────┐   ┌───────────────────┐   │     │
│  │  │ Planner  │──▶│ Generator  │──▶│    Evaluator      │   │     │
│  │  │ Agent    │   │ Agent      │   │    Agent          │   │     │
│  │  │ (800ms)  │   │ (1200ms)   │   │    (600ms)        │   │     │
│  │  └──────────┘   └────────────┘   └───────────────────┘   │     │
│  └──────────────────────────────────────────────────────────┘     │
│       │                                                            │
│       ▼                                                            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Format     │  │  Constraint  │  │  Fallback    │             │
│  │  Validator  │  │  Checker     │  │  Handler     │             │
│  │  (100ms)    │  │  (300ms)     │  │  (200ms)     │             │
│  └─────────────┘  └──────────────┘  └──────────────┘             │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │              HISTORY & STATE LAYER                         │     │
│  │  ┌──────────────────┐   ┌────────────────────────────┐    │     │
│  │  │ History Compactor│   │  7 × JSON State Files      │    │     │
│  │  │ (condicional)    │   │  (plan, draft, eval,       │    │     │
│  │  │ (300ms)          │   │   decisions, trace,        │    │     │
│  │  └──────────────────┘   │   constraints, budget)     │    │     │
│  │                         └────────────────────────────┘    │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                    │
│  RESPOSTA AO CLIENTE                                               │
│                                                                    │
│  LATÊNCIA TOTAL: ~4000ms                                           │
│  TOKENS/TURNO MÉDIO: ~3200                                         │
│  ARQUIVOS DE ESTADO: 7 por conversa                                │
│  CUSTO MENSAL API: R$ 9.240                                        │
└──────────────────────────────────────────────────────────────────┘
```

### As Três Camadas do Harness

O harness atual está organizado em três camadas conceituais. Entender essa organização ajuda a identificar redundâncias entre camadas:

**Camada 1 — Pré-Processamento (antes do modelo ver o input):**
- **Context Loader:** Recarrega dados do cliente a cada turno
- **Dedup Layer:** Remove informações duplicadas do contexto
- **Priority Extractor:** Marca dados críticos com tags `[HIGH_PRIORITY]`
- **Budget Guard:** Monitora consumo de tokens e trunca se necessário

**Camada 2 — Core Agents (onde o modelo age):**
- **Planner Agent:** Cria plano estruturado antes da execução
- **Generator Agent:** Produz resposta ao cliente
- **Evaluator Agent:** Avalia output contra rubrics de qualidade

**Camada 3 — Pós-Processamento (depois do modelo gerar output):**
- **Format Validator:** Valida estrutura JSON/schema
- **Constraint Checker:** Verifica restrições do cliente (alergias, orçamento)
- **Fallback Handler:** Estratégias alternativas em caso de falha

**Camada Transversal (opera em todas as camadas):**
- **History Compactor:** Comprime histórico de conversas longas
- **State Persistence:** 7 arquivos JSON que registram estado de cada etapa

### Visualização do Fluxo de Dados Entre Camadas

Entender como os dados fluem entre as camadas é essencial para identificar redundâncias. O mesmo dado (ex: alergia do cliente) passa por múltiplos componentes em sequência:

```
DADO: "Cliente é alérgico a lactose"

Fluxo atual (11 componentes):
───────────────────────────────────────────────────────────────
Context Loader → carrega alergia do perfil (450ms)
     │
     ▼
Dedup Layer → verifica se alergia já foi carregada por outro componente
     │         (se sim, remove duplicata — mas raramente acontece)
     ▼
Priority Extractor → adiciona tag [HIGH_PRIORITY] Alergia: lactose (150ms)
     │
     ▼
Planner Agent → inclui alergia como constraint no plano (800ms)
     │
     ▼
Generator Agent → gera recomendação considerando alergia (1200ms)
     │
     ▼
Constraint Checker → verifica se output respeita alergia (300ms)
     │
     ▼
Evaluator Agent → verifica se output respeita alergia (600ms) ← REDUNDANTE
     │
     ▼
Resposta ao cliente

TEMPO TOTAL PARA VALIDAR ALERGIA: ~3500ms
COMPONENTES QUE TOCAM O DADO "ALERGIA": 7 de 11
```

Este é o coração do problema: um dado crítico (alergia) passa por 7 componentes, com validação redundante em 2 deles (Constraint Checker + Evaluator). A evolução do harness deve reduzir este número drasticamente — mantendo a proteção, mas eliminando a redundância.

### Por Que a Redundância Existe

A redundância não é incompetência do time — é consequência de um processo de desenvolvimento sem revisão:

1. **Context Loader** foi criado primeiro (modelo fraco, precisava recarregar a cada turno)
2. **Constraint Checker** foi adicionado depois (medo de que o Evaluator sozinho não bastasse para alergias)
3. **Evaluator** já existia (mas validava qualidade geral, não constraints específicas)
4. **Priority Extractor** foi uma tentativa de "forçar" o modelo a prestar atenção em alergias

Resultado: 4 componentes diferentes foram criados em momentos diferentes para resolver o mesmo problema (garantir que alergias sejam respeitadas), sem que ninguém consolidasse a estratégia. Este é exatamente o tipo de descoberta que uma revisão trimestral de harness deve produzir.

### Descrição Detalhada de Cada Componente

Para cada componente, você precisa entender três coisas:
1. **O que faz** — Função técnica no pipeline
2. **Por que existe** — Qual fraqueza do modelo antigo ele protegia
3. **Premissa original** — Qual suposição sobre o modelo justificou sua criação

Use estas descrições como base para sua análise de impacto na Parte 1.

---

**#1 — Context Loader**
- **Função:** Recarrega o perfil completo do cliente (alergias, restrições alimentares, orçamento, objetivo, histórico de compras) antes de CADA turno de conversa. Os dados são injetados tanto no system prompt quanto no user message como redundância.
- **Por que existe:** O modelo da época em que o harness foi originalmente projetado (Claude v2, 32K tokens) perdia acurácia de atenção após ~40 minutos de conversa. Informações ditas no início simplesmente desapareciam. A solução foi recarregar explicitamente os dados críticos a cada turno. Nota: o modelo atualmente em produção é Claude v3 (200K), e o changelog analisado é para Claude v4 (500K) — o harness nunca foi atualizado para refletir essas melhorias.
- **Premissa original:** "O modelo NÃO mantém atenção em informações do início da conversa. Dados críticos precisam ser re-carregados em todo turno para garantir que o modelo os considere."
- **Custo operacional:** 5.4M tokens/mês (R$ 810), 450ms de latência/turno, 3h de manutenção/mês
- **Sinal de alerta:** ROI de 0.8x — está abaixo de 1x (custa mais do que entrega). 28x mais falsos positivos que prevenções reais (340 FPs vs 12 prevenções).

---

**#2 — Dedup Layer**
- **Função:** Varre o contexto que será enviado ao modelo e remove informações duplicadas. Por exemplo, se o perfil do cliente aparece no Context Loader E no History Compactor E no system prompt, a Dedup Layer elimina as cópias redundantes.
- **Por que existe:** Com tantos componentes injetando contexto (Context Loader, History Compactor, Priority Extractor), duplicação era comum. Tokens duplicados são tokens pagos que não agregam valor.
- **Premissa original:** "Redundância entre componentes do harness causa tokens desperdiçados. Uma camada de deduplicação reduz o consumo sem perder informação."
- **Custo operacional:** 2M tokens/mês (R$ 300), 200ms de latência/turno, 2h de manutenção/mês
- **Sinal de alerta:** ROI de 0.4x (custa mais do que entrega). 15x mais falsos positivos que prevenções reais.

---

**#3 — Priority Extractor**
- **Função:** Analisa os dados do cliente e marca informações críticas com tags explícitas como `[HIGH_PRIORITY] Cliente é ALÉRGICO A: glúten, amendoim` e `[CRITICAL] Orçamento máximo: R$ 220`. Estas tags são injetadas no início do user message para forçar a atenção do modelo.
- **Por que existe:** O modelo antigo tinha viés de recência — priorizava informações das últimas mensagens sobre informações do início da conversa. Constraints críticas (como alergias) precisavam de destaque explícito para competir com informações recentes.
- **Premissa original:** "O modelo prioriza informações recentes sobre informações antigas. Constraints críticas precisam de marcadores explícitos de prioridade para garantir que sejam consideradas."
- **Custo operacional:** 1.5M tokens/mês (R$ 225), 150ms de latência/turno, 1.5h de manutenção/mês
- **Sinal de alerta:** ROI de 1.1x — no limite. 8x mais falsos positivos que prevenções reais.

---

**#4 — Budget Guard**
- **Função:** Monitora o consumo de tokens acumulado na conversa. Quando atinge 80% da janela de contexto do modelo (que era 32K), trunca as mensagens mais antigas para evitar que o modelo receba input truncado e gere respostas incompletas.
- **Por que existe:** O modelo antigo tinha janela de apenas 32K tokens. Conversas do KODA frequentemente chegavam a 25K-30K tokens, muito próximas do limite. O Budget Guard era uma proteção de último recurso.
- **Premissa original:** "32K tokens é insuficiente para conversas de 2h. Precisamos de um guardrail que evite estouro de contexto."
- **Custo operacional:** 800K tokens/mês (R$ 120), 100ms de latência/turno, 1h de manutenção/mês
- **Sinal de alerta:** ZERO acionamentos em 90 dias. ROI de 0.0x. Componente mais óbvio para remoção imediata.

---

**#5 — Planner Agent**
- **Função:** Antes de cada resposta ao cliente, analisa o contexto da conversa e gera um plano estruturado: steps necessários, decisões a tomar, critérios de sucesso. Este plano é passado ao Generator Agent como contexto adicional.
- **Por que existe:** O modelo antigo tentava resolver tudo de uma vez (recomendar produto, explicar por quê, comparar preços, verificar restrições) — o resultado era confuso e frequentemente incompleto. O Planner força uma decomposição explícita.
- **Premissa original:** "O modelo não decompõe tarefas complexas naturalmente. Um agente de planejamento explícito melhora a qualidade do output."
- **Custo operacional:** 8.2M tokens/mês (R$ 1.230), 800ms de latência/turno, 4h de manutenção/mês
- **Sinal de alerta:** É acionado em 35% das conversas. ROI de 18x — excelente. Mas o changelog menciona "self-correction 3x melhor" e "raciocínio auditável nativo" — o modelo pode estar planejando implicitamente.

---

**#6 — Generator Agent**
- **Função:** É o core do sistema. Recebe o contexto enriquecido (output do Planner + dados do cliente) e gera a resposta ao cliente: recomendação de produto, explicação, comparação, follow-up.
- **Por que existe:** Sem ele, não há sistema. É o componente que efetivamente produz a resposta.
- **Premissa original:** Permanente. Não se aplica análise de remoção.
- **Custo operacional:** 22M tokens/mês (R$ 3.300), 1200ms de latência/turno, 2h de manutenção/mês
- **Sinal de alerta:** Nenhum. Componente core.

---

**#7 — Evaluator Agent**
- **Função:** Recebe o output do Generator e avalia contra rubrics de qualidade, segurança e compliance. Verifica se a recomendação respeita alergias, se o preço está dentro do orçamento, se o tom é adequado, se há informação factual correta. Se o output não passa, força regeneração.
- **Por que existe:** Sycophancy — LLMs têm viés de concordância com o usuário. Se o cliente diz "quero o mais barato", o modelo pode recomendar um produto inadequado só para agradar. O Evaluator é um gatekeeper independente.
- **Premissa original:** "O modelo não auto-avalia com precisão. Sycophancy é um problema estrutural de LLMs, não de qualidade de modelo. Um gatekeeper externo é necessário."
- **Custo operacional:** 12M tokens/mês (R$ 1.800), 600ms de latência/turno, 3h de manutenção/mês
- **Sinal de alerta:** ROI de 45x — o melhor de todo o harness. Menos de 1 falso positivo para cada 3 acionamentos reais (0.3x FP rate).

---

**#8 — Format Validator**
- **Função:** Após o Generator produzir output, verifica se o JSON está bem formado, se todos os campos obrigatórios estão presentes, se os tipos estão corretos (string, number, array). Também valida o schema do output contra a especificação da API do WhatsApp.
- **Por que existe:** O modelo antigo produzia JSON malformado em ~3% dos turns. Campos faltando, tipos errados, estruturas aninhadas incorretas. Isso quebrava o parsing downstream.
- **Premissa original:** "O modelo não garante conformidade de schema. Precisamos de validação pós-output para evitar erros de parsing."
- **Custo operacional:** 1.2M tokens/mês (R$ 180), 100ms de latência/turno, 1h de manutenção/mês
- **Sinal de alerta:** ROI de 4.5x ainda positivo. Mas o changelog documenta JSON mode nativo com schema validation e <0.01% de erro — o modelo novo virtualmente elimina o problema que o Format Validator resolve.

---

**#9 — Constraint Checker**
- **Função:** Verifica se o output do Generator respeita as constraints do cliente: alergias (o produto contém algo que o cliente é alérgico?), orçamento (o preço está dentro do limite?), preferências (o produto é vegano? sem glúten?).
- **Por que existe:** Constraints de saúde (alergias) são críticas demais para depender de um único checkpoint. O Constraint Checker foi adicionado como redundância ao Evaluator — dois componentes independentes validando as mesmas coisas.
- **Premissa original:** "Um checkpoint só não é suficiente para constraints de saúde. Redundância entre Constraint Checker e Evaluator reduz probabilidade de falsos negativos."
- **Custo operacional:** 3.1M tokens/mês (R$ 465), 300ms de latência/turno, 2h de manutenção/mês
- **Sinal de alerta:** ROI de 12x — muito bom. Mas há sobreposição de ~70% com o Evaluator (validam as mesmas constraints). A pergunta é: dá para consolidar?

---

**#10 — Fallback Handler**
- **Função:** Quando o fluxo principal falha (modelo retorna erro, output não passa no Evaluator, timeout), executa estratégias de recuperação em cascata: (1) retry com prompt ajustado, (2) estratégia alternativa (muda a abordagem), (3) escala para atendente humano.
- **Por que existe:** O modelo antigo falhava com frequência em edge cases. Três camadas de fallback cobriam desde falhas simples (retry resolve) até falhas complexas (humano assume).
- **Premissa original:** "Precisamos de 3 camadas de fallback para cobrir todo o espectro de falhas possíveis."
- **Custo operacional:** 900K tokens/mês (R$ 135), 200ms de latência/turno, 1h de manutenção/mês
- **Sinal de alerta:** ROI de 1.7x — marginalmente positivo. Mas 29 acionamentos em 90 dias. A pergunta: desses 29, quantos precisaram das 3 camadas vs. apenas 1?

---

**#11 — History Compactor**
- **Função:** Quando uma conversa ultrapassa 2 horas, comprime o histórico: resume mensagens antigas em bullet points, mantém as últimas 5 mensagens íntegras, remove saudações e repetições. Isso mantém o contexto total dentro da janela do modelo.
- **Por que existe:** Conversas do KODA frequentemente passam de 2 horas. Sem compressão, o contexto acumulado excederia a janela do modelo, causando truncamento.
- **Premissa original:** "Compressão de histórico é necessária para conversas longas. Sem ela, conversas > 2h sofreriam perda de contexto."
- **Custo operacional:** 4.5M tokens/mês (R$ 675), 300ms de latência/turno (quando acionado), 2h de manutenção/mês
- **Sinal de alerta:** Nenhum. ROI de 8x — excelente. Mas com janela de 500K tokens no modelo novo, o threshold de acionamento (2h) pode ser aumentado.

---

### Métricas de Produção (90 Dias: Fevereiro – Abril 2026)

Esta tabela é a fonte primária de verdade para suas decisões. Cada linha é um componente. Cada coluna é uma dimensão de análise.

| # | Componente | Acionamentos Reais | Falsos Positivos | Tokens/Mês | Custo Mensal (R$) | Latência (ms) | Manutenção (h/mês) | ROI |
|---|-----------|--------------------|--------------------|------------|--------------------|--------------|--------------------|------|
| 1 | Context Loader | 0.04% (58 em 145K) | 340 (28.3x) | 5.400.000 | R$ 810 | 450ms | 3h | 0.8x |
| 2 | Dedup Layer | 0.01% (14 em 145K) | 210 (15.0x) | 2.000.000 | R$ 300 | 200ms | 2h | 0.4x |
| 3 | Priority Extractor | 0.05% (72 em 145K) | 576 (8.0x) | 1.500.000 | R$ 225 | 150ms | 1.5h | 2.7x |
| 4 | Budget Guard | 0.00% (0 em 145K) | 0 | 800.000 | R$ 120 | 100ms | 1h | 0.0x |
| 5 | Planner Agent | 35.00% (50.750)* | 250 (0.5x) | 8.200.000 | R$ 1.230 | 800ms | 4h | N/A† |
| 6 | Generator Agent | 100% (todos) | 145 (0.1x) | 22.000.000 | R$ 3.300 | 1200ms | 2h | N/A‡ |
| 7 | Evaluator Agent | 8.50% (12.325) | 37 (0.3x) | 12.000.000 | R$ 1.800 | 600ms | 3h | 45.0x |
| 8 | Format Validator | 0.12% (174) | 522 (3.0x) | 1.200.000 | R$ 180 | 100ms | 1h | 8.8x |
| 9 | Constraint Checker | 0.80% (1.160) | 1.392 (1.2x) | 3.100.000 | R$ 465 | 300ms | 2h | 25.0x |
| 10 | Fallback Handler | 0.02% (29) | 174 (6.0x) | 900.000 | R$ 135 | 200ms | 1h | 1.7x |
| 11 | History Compactor | 12.00% (17.400)* | 35 (0.2x) | 4.500.000 | R$ 675 | 300ms | 2h | N/A† |

*\*Planner Agent e History Compactor: acionamentos representam frequência de uso, não erros prevenidos. Para estes componentes, o ROI tradicional não se aplica — eles são medidos por melhoria de qualidade/eficiência, não por prevenção de erros.*

*†N/A: componente de qualidade/infraestrutura — ROI não se aplica diretamente.*

*‡Generator é o componente core — não se aplica ROI (sem ele não há sistema).*

### Como Interpretar as Métricas

**Acionamentos Reais:** Percentual de turns em que o componente detectou e preveniu um erro REAL. Não é "poderia prevenir" — é "preveniu". Calculado sobre 145.000 turns em 90 dias.

**Falsos Positivos:** Número de vezes que o componente bloqueou ou alterou um fluxo que estava CORRETO. A razão Falsos Positivos / Acionamentos Reais indica se o componente está causando mais problemas do que resolvendo.

**ROI (Return on Investment):** Fórmula completa abaixo. Um ROI < 1.0x significa que o componente custa mais do que o valor que entrega. Um ROI entre 0.5x e 1.5x é zona cinzenta — requer investigação.

**Tokens/Mês:** Consumo médio mensal de tokens. Inclui tokens de input (contexto injetado) e output (validações, verificações).

### Fórmula do ROI e Como Interpretá-la

```
ROI (janela de 90 dias) = (Erros Prevenidos × Custo Médio do Erro) / Custo Operacional

Onde:
  Erros Prevenidos = número de prevenções reais nos últimos 90 dias
  Custo Médio do Erro = R$ 50 por erro para o KODA
    (soma de: reembolso médio R$ 25 + suporte R$ 15 + churn estimado R$ 10)
  Custo Operacional (90 dias) = Custo de Tokens (R$) + Custo de Manutenção (R$)
    Custo de Tokens (90d) = tokens/mês × 3 × R$ 0,15 por 1K tokens
    Custo de Manutenção (90d) = horas/mês × 3 × R$ 150/hora
    Nota: O custo de latência é irrelevante para o KODA e foi omitido.
```

**Exemplo de cálculo — Context Loader:**
```
Erros Prevenidos (90d) = 58
Valor Entregue = 58 × R$ 50 = R$ 2.900
Custo Operacional (90d) = R$ 810×3 (tokens) + 3h×3×R$150 (manutenção)
                        = R$ 2.430 + R$ 1.350 = R$ 3.780
ROI = R$ 2.900 / R$ 3.780 = 0.77x → arredondado para 0.8x na tabela
```

**Exemplo de cálculo — Budget Guard:**
```
Erros Prevenidos (90d) = 0
Valor Entregue = 0 × R$ 50 = R$ 0
Custo Operacional (90d) = R$ 120×3 + 1h×3×R$150 = R$ 360 + R$ 450 = R$ 810
ROI = R$ 0 / R$ 810 = 0.0x
```

**Interpretação das faixas de ROI:**

| ROI | Classificação | Ação Recomendada |
|-----|--------------|-------------------|
| > 5.0x | Essencial | Manter. O componente entrega muito mais valor do que custa. |
| 1.5x – 5.0x | Positivo | Manter, mas monitorar tendência. Se estiver caindo trimestre a trimestre, investigar. |
| 0.5x – 1.5x | Zona cinzenta | Investigar. O componente está no limite de se pagar. Considere simplificar antes de remover. |
| < 0.5x | Prejuízo | Remover ou simplificar agressivamente. O componente custa mais do que entrega. |
| 0.0x | Obsoleto | Remover imediatamente. Zero prevenções = zero valor. |

---

## 📋 O Changelog Que Muda Tudo

O novo modelo (Claude v4, Maio 2026) foi lançado. Estas são as capacidades documentadas:

```
═══════════════════════════════════════════════════════════════
           NOVO MODELO — CLAUDE v4 (LANÇAMENTO: MAIO 2026)
═══════════════════════════════════════════════════════════════

CAPACIDADE                     ANTES (v3)        DEPOIS (v4)
───────────────────────────────────────────────────────────────
Janela de contexto              200K tokens       500K tokens
Instruction following            94.0%              98.7%
Self-correction (domínio)        2.1/5              4.8/5
Raciocínio auditável             Prompt-forçado     Nativo no output
Structured output                Pós-validação     JSON mode com schema validation
Grounding factual (produtos)     72%                 98%
Latência de inferência           baseline           -35%
Atenção em contexto longo        97% @ 100K         99.3% @ 300K

NOTAS DO CHANGELOG (TRECHOS RELEVANTES):
───────────────────────────────────────────────────────────────
"O modelo agora mantém >99% de acurácia em atenção para 
 contextos de até 300K tokens. Informações no system 
 prompt são priorizadas automaticamente — não é mais 
 necessário usar tags explícitas como [HIGH_PRIORITY] ou 
 [CRITICAL]."

"O JSON mode com schema validation garante que todo output 
 estruturado esteja em conformidade com o schema definido. 
 Outputs malformados são virtualmente eliminados (<0.01% 
 em benchmarks internos)."

"A capacidade de self-correction em domínios de e-commerce 
 melhorou 3x. O modelo identifica e corrige inconsistências 
 em recomendações de produto, comparações de preço e 
 verificação de restrições com mínima intervenção externa."

"Com 500K tokens de contexto, conversas de longa duração 
 (>4 horas) raramente atingem o limite. O modelo gerencia 
 atenção ao longo de todo o contexto sem degradação 
 significativa."
═══════════════════════════════════════════════════════════════
```

### Mapeamento: Capacidade do Changelog → Componentes Afetados

Use esta tabela como referência rápida para sua análise de impacto. Cada linha mapeia uma capacidade documentada do modelo novo para os componentes cuja premissa original ela desafia.

| Capacidade do Modelo Novo | Componentes Afetados | Por Que Afeta |
|---------------------------|---------------------|---------------|
| Janela 500K (2.5x maior) | Budget Guard, History Compactor, Dedup Layer | Orçamento de tokens deixa de ser restrição; compressão pode ser adiada; duplicação de contexto importa menos |
| Atenção >99% @ 300K | Context Loader, Priority Extractor | Modelo não perde informações antigas; não precisa de tags explícitas de prioridade |
| Instruction following 98.7% | Constraint Checker, System Prompts longos | Modelo segue instruções com alta fidelidade; menos necessidade de validação redundante |
| Self-correction 3x melhor | Evaluator (parcial), Fallback Handler, Planner Agent | Modelo corrige os próprios erros; menos necessidade de fallback complexo; planejamento pode ser implícito |
| JSON mode nativo | Format Validator | Output malformado virtualmente eliminado; validação pós-output desnecessária |
| Grounding factual +98% | Constraint Checker (parcial) | Menos erros factuais sobre produtos; validação de factualidade menos necessária |
| Raciocínio auditável nativo | Trace Layer, Decision Logger | Modelo expõe raciocínio sem prompting forçado; logging pode ser simplificado |

### Impacto do Changelog nos Componentes do Harness — Tabela Para Preencher

Preencha a coluna "Sua Decisão" para cada componente baseado na sua análise cruzada de métricas + changelog. Use os símbolos:

- ⬆️ **MANTÉM** — O componente continua essencial, mesmo com o modelo novo
- ➡️ **SIMPLIFICA** — O componente ainda é útil, mas pode ter escopo reduzido
- ⬇️ **REMOVE** — O componente se tornou desnecessário com o modelo novo

| # | Componente | Capacidade do Changelog Que Impacta | Sua Decisão |
|---|-----------|--------------------------------------|-------------|
| 1 | Context Loader | Atenção >99% @ 300K tokens; system prompt priorizado automaticamente | |
| 2 | Dedup Layer | Janela 500K (2.5x maior); menos pressão por tokens; duplicação menos crítica | |
| 3 | Priority Extractor | System prompt priorizado automaticamente — tags explícitas desnecessárias | |
| 4 | Budget Guard | Janela 500K — conversas típicas (50K) são apenas 10% da nova janela | |
| 5 | Planner Agent | Self-correction 3x melhor; raciocínio nativo (planejamento implícito) | |
| 6 | Generator Agent | Nenhuma — componente core, permanente por definição | ⬆️ MANTÉM |
| 7 | Evaluator Agent | Self-correction 3x melhor — mas sycophancy é estrutural, não de qualidade | |
| 8 | Format Validator | JSON mode nativo com schema validation (<0.01% erro) | |
| 9 | Constraint Checker | Self-correction 3x + grounding +98% factual + instruction following 98.7% | |
| 10 | Fallback Handler | Latência -35%; taxa de falha do modelo historicamente <0.1% | |
| 11 | History Compactor | Janela 500K; atenção >99% @ 300K — compressão pode ser adiada | |

---

## 📝 Sua Tarefa

Você deve criar um **Plano de Evolução do Harness KODA** em 3 fases, aplicando a disciplina de Harness Evolution estudada no módulo `05-harness-evolution.md`.

### Estrutura do Exercício

O exercício está dividido em 5 partes progressivas:

1. **Análise de Impacto** — Preencha a tabela com sua decisão para cada componente e justifique com métricas + changelog
2. **Plano de Evolução (3 Fases)** — Proponha as 3 fases, da menos arriscada para a mais estrutural
3. **Critérios de Validação por Fase** — Defina thresholds mensuráveis que funcionam como gates entre fases
4. **Tabela Comparativa Antes/Depois** — Estime o impacto agregado do plano em métricas de sistema
5. **Análise de Riscos e Invariantes** — Identifique o que NUNCA deve ser removido e por quê

### Metodologia de Análise: O Framework de 4 Perguntas

Para cada componente, siga este roteiro mental de 4 perguntas. Este framework é o mesmo que o time do Fernando usou naquela reunião — e que você deve internalizar para qualquer decisão de evolução de arquitetura:

1. **As métricas justificam sua existência?** — Olhe para acionamentos reais (não teóricos), falsos positivos e ROI. Se ROI < 1x, o componente é candidato.
2. **O changelog cobre a premissa original?** — Compare a premissa original do componente com as capacidades documentadas do modelo novo. Se o changelog diz "modelo agora faz X" e a premissa era "modelo não faz X", o componente perdeu sua razão de existir.
3. **Outro componente já cobre essa proteção?** — Se dois componentes validam a mesma coisa (ex: Constraint Checker e Evaluator), um deles pode ser redundante.
4. **É um invariante arquitetural?** — Segurança, compliance, decisões irreversíveis, sycophancy. Se sim, NÃO remove, independentemente das métricas.

### Matriz de Decisão Rápida

Use esta matriz como atalho mental durante a análise. Ela cruza ROI com evidência do changelog para sugerir uma ação:

| ROI | Changelog Cobre a Premissa? | Ação Sugerida | Exemplo no KODA |
|-----|---------------------------|---------------|-----------------|
| < 0.5x | Sim | ⬇️ Remove (Fase 1) | Budget Guard: ROI 0.0x + janela 500K |
| < 0.5x | Não | 🔍 Investiga por que ROI é tão baixo | — |
| 0.5x–1.5x | Sim | ➡️ Simplifica (Fase 1–2) | Dedup Layer: ROI 0.8x + janela maior |
| 0.5x–1.5x | Não | 🔍 Investiga se changelog está errado ou métricas estão incompletas | Fallback Handler: ROI 0.6x mas ainda tem 29 acionamentos |
| 1.5x–5.0x | Sim | ➡️ Simplifica (Fase 2–3) | Format Validator: ROI 4.5x + JSON mode nativo |
| 1.5x–5.0x | Não | ⬆️ Mantém (monitorar) | Context Loader: ROI 2.0x, atenção >99% cobre parcialmente |
| > 5.0x | Sim ou Não | ⬆️ Mantém | Evaluator: ROI 45x. Planner: ROI 18x |

### Exemplo de Raciocínio Completo: Cruzando as 4 Perguntas

Vamos aplicar o framework a um componente específico para você ver como as 4 perguntas se conectam:

**Componente: Dedup Layer (ROI 0.8x)**

**Pergunta 1 — Métricas:** ROI de 0.8x (custa mais do que entrega). 14 acionamentos reais em 145K turns (0.01%). 15x mais FPs que prevenções. A curva é clara: o componente está no prejuízo.

**Pergunta 2 — Changelog:** Janela de 500K tokens (2.5x maior). Com mais espaço, duplicação de tokens é menos crítica. Além disso, se simplificarmos o Context Loader (que é a principal fonte de duplicação), a Dedup Layer perde seu principal input. É um efeito cascata: simplificar A reduz a necessidade de B.

**Pergunta 3 — Sobreposição:** O History Compactor já lida com redundância de contexto (remove repetições, sumariza). Se o Compactor é mantido e otimizado, a Dedup Layer é redundante para a maioria dos casos. A pergunta é: o Compactor cobre 100% dos casos que a Dedup cobre? Se sim, remover. Se ~80%, simplificar Dedup para cobrir só os 20% restantes.

**Pergunta 4 — Invariante:** Não. Dedup é puramente uma otimização de tokens — não protege segurança, compliance ou decisões irreversíveis.

**Decisão:** ⬇️ REMOVE (Fase 1) — absorvida pelo History Compactor após simplificação do Context Loader.

---

## 📊 Parte 1: Análise de Impacto

Preencha a coluna "Sua Decisão" da tabela na seção anterior para cada um dos 11 componentes. O Generator Agent já está preenchido como exemplo.

Para cada componente que você marcar como ➡️ Simplifica ou ⬇️ Remove, produza uma análise no formato abaixo. Você deve produzir análises para **no mínimo 6 componentes**.

### Template de Análise por Componente

```
═══════════════════════════════════════════════════════════
COMPONENTE: [Nome]
DECISÃO: [⬆️ Mantém / ➡️ Simplifica / ⬇️ Remove]
═══════════════════════════════════════════════════════════

📊 EVIDÊNCIA DAS MÉTRICAS:
  • Acionamentos reais: [X em 145K turns = Y%]
  • Falsos positivos: [Número] ([X]x mais que prevenções reais)
  • ROI: [X]x — [interpretação: essencial / zona cinzenta / prejuízo]
  • Tendência: [estável / caindo / subindo nos últimos 90 dias]

🔬 EVIDÊNCIA DO CHANGELOG:
  • Capacidade relevante: [qual linha do changelog impacta este componente]
  • Como impacta: [explicação de por que essa capacidade desafia a premissa original]
  • Nível de confiança: [Alto / Médio / Baixo]

🔄 SOBREPOSIÇÃO COM OUTROS COMPONENTES:
  • [Componente X] já cobre [Y]% da mesma proteção? [Sim/Não]
  • Se sim: [dá para consolidar? qual componente absorve o outro?]

⚠️ ANÁLISE DE RISCO:
  • Pior cenário se remover: [descrição]
  • Probabilidade: [Alta / Média / Baixa]
  • Mitigação: [feature flag, shadow test, rollback, alerta]

🎯 PRIORIDADE SUGERIDA: [Fase 1 / Fase 2 / Fase 3]
  • Justificativa da prioridade: [por que esta fase e não outra?]
```

### Exemplo de Análise — Budget Guard

```
═══════════════════════════════════════════════════════════
COMPONENTE: Budget Guard
DECISÃO: ⬇️ REMOVE
═══════════════════════════════════════════════════════════

📊 EVIDÊNCIA DAS MÉTRICAS:
  • Acionamentos reais: 0 em 145K turns = 0.00%
  • Falsos positivos: 0 (nunca dispara, nunca bloqueia)
  • ROI: 0.0x — prejuízo líquido. Custa R$ 120/mês para prevenir zero erros.
  • Tendência: estável em zero há 3 trimestres

🔬 EVIDÊNCIA DO CHANGELOG:
  • Capacidade relevante: Janela de contexto expandida para 500K tokens
  • Como impacta: A premissa original era "32K tokens é insuficiente". Conversas típicas consomem 50K — são apenas 10% da nova janela de 500K. O limite de 80% (400K) nunca será atingido.
  • Nível de confiança: Alto — documentado e matematicamente demonstrável

🔄 SOBREPOSIÇÃO COM OUTROS COMPONENTES:
  • Nenhum. Budget Guard é proteção de infraestrutura, não de qualidade.

⚠️ ANÁLISE DE RISCO:
  • Pior cenário se remover: Conversa atinge 500K tokens e modelo recebe input truncado.
  • Probabilidade: Baixíssima (<0.001%). Conversa típica = 50K. Recorde histórico = 180K.
  • Mitigação: Feature flag `harness_remove_budget_guard`. Alerta se atingir 400K tokens. Código arquivado em archive/components/.

🎯 PRIORIDADE SUGERIDA: Fase 1
  • Justificativa: Zero risco, zero acionamentos, economia imediata de R$ 120/mês + 100ms latência. Gera confiança no time para fases seguintes.
```

### Exemplo de Análise — Context Loader

```
═══════════════════════════════════════════════════════════
COMPONENTE: Context Loader
DECISÃO: ➡️ SIMPLIFICA
═══════════════════════════════════════════════════════════

📊 EVIDÊNCIA DAS MÉTRICAS:
  • Acionamentos reais: 58 em 145K turns = 0.04%
  • Falsos positivos: 340 (28.3x mais que prevenções reais)
  • ROI: 0.8x — zona cinzenta. O componente está no limite de se pagar.
  • Tendência: caindo. Era 1.3x há 6 meses (modelo mais fraco).

🔬 EVIDÊNCIA DO CHANGELOG:
  • Capacidade relevante: Atenção >99% @ 300K tokens; system prompt priorizado automaticamente
  • Como impacta: Premissa original era "modelo perde atenção após 40 minutos". Changelog documenta >99% de atenção em 300K tokens (~5 horas de conversa KODA). O modelo novo não perde informações antigas.
  • Nível de confiança: Alto — documentado, mas validar com shadow test no domínio KODA

🔄 SOBREPOSIÇÃO COM OUTROS COMPONENTES:
  • History Compactor cobre parcialmente. Em vez de recarregar perfil a cada turno, o Compactor pode manter dados críticos no contexto comprimido.
  • Constraint Checker + Evaluator também validam alergias — a proteção não depende só do Context Loader.

⚠️ ANÁLISE DE RISCO:
  • Pior cenário: Informação de alergia não disponível no momento da recomendação.
  • Probabilidade: Baixa — dados ainda estarão no system prompt. Só paramos de recarregar a cada turno.
  • Mitigação: Simplificar em ondas. Primeiro remover redundância (system_prompt + user_message → só system_prompt). Depois aumentar threshold de recarga (todo turno → só início da conversa).

🎯 PRIORIDADE SUGERIDA: Fase 2
  • Justificativa: Não é risco zero (ainda previne 58 erros reais). A simplificação deve ser gradual. A Fase 1 remove casos de risco zero, gerando confiança para esta decisão.
```

### Exemplo de Análise — Format Validator (risco controlado com changelog forte)

```
═══════════════════════════════════════════════════════════
COMPONENTE: Format Validator
DECISÃO: ⬇️ REMOVE
═══════════════════════════════════════════════════════════

📊 EVIDÊNCIA DAS MÉTRICAS:
  • Acionamentos reais: 174 em 145K turns = 0.12%
  • Falsos positivos: 522 (3.0x mais que prevenções reais)
  • ROI: 4.5x — positivo, mas a razão é que erros de formato são baratos (R$ 50)
  • Tendência: caindo. Com modelo v3 (200K), caiu de 0.3% para 0.12%. Com v4, deve cair mais.

🔬 EVIDÊNCIA DO CHANGELOG:
  • Capacidade relevante: JSON mode nativo com schema validation. Outputs malformados < 0.01%
  • Como impacta: A premissa original era "modelo produz JSON malformado ~3% das vezes". O changelog documenta <0.01% — uma redução de 300x. O modelo novo resolve o problema na origem, não no pós-processamento.
  • Nível de confiança: Alto — JSON mode é uma feature binária (ou está ativo ou não está), não depende de interpretação de benchmark

🔄 SOBREPOSIÇÃO COM OUTROS COMPONENTES:
  • Nenhuma sobreposição significativa. Format Validator é especializado em schema — outros componentes validam conteúdo, não estrutura.

⚠️ ANÁLISE DE RISCO:
  • Pior cenário: Um output com JSON malformado chega ao cliente e quebra a renderização no WhatsApp.
  • Probabilidade: Muito baixa (<0.01% segundo o changelog, validável em shadow test)
  • Mitigação: Shadow test de 14 dias monitorando taxa de erro de parsing. Se > 0.05%, reavaliar. Feature flag para rollback imediato. Alerta no dashboard de erros de parsing.

🎯 PRIORIDADE SUGERIDA: Fase 2
  • Justificativa: O changelog é forte (JSON mode é binário), mas ainda há 174 acionamentos reais em 90 dias. A Fase 1 gera confiança no processo de remoção. A Fase 2 remove este componente com shadow test robusto. Se o JSON mode funcionar como documentado, a economia é de R$ 180/mês + 100ms.
```

### Exemplo de Análise — Evaluator Agent (invariante que NUNCA sai)

```
═══════════════════════════════════════════════════════════
COMPONENTE: Evaluator Agent
DECISÃO: ⬆️ MANTÉM (INVARIANTE)
═══════════════════════════════════════════════════════════

📊 EVIDÊNCIA DAS MÉTRICAS:
  • Acionamentos reais: 12.325 em 145K turns = 8.50%
  • Falsos positivos: 37 (0.3x — menos de 1 FP para cada 3 acionamentos)
  • ROI: 45.0x — o maior de todo o harness. Cada R$ 1 gasto no Evaluator previne R$ 45 em erros.
  • Tendência: estável. Acurácia se manteve mesmo com modelos melhores — porque sycophancy é estrutural.

🔬 EVIDÊNCIA DO CHANGELOG:
  • Capacidade relevante: Self-correction 3x melhor
  • Como impacta: Self-correction melhor pode REDUZIR a carga do Evaluator (menos regenerações necessárias), mas NÃO elimina a necessidade dele. Sycophancy é um viés estrutural de LLMs — nenhum changelog de modelo promete "zero sycophancy".
  • Nível de confiança: Alto — a literatura de ML é consistente: sycophancy não se resolve com escala ou qualidade de modelo

🔄 SOBREPOSIÇÃO COM OUTROS COMPONENTES:
  • Constraint Checker tem ~70% de sobreposição funcional com o Evaluator. Esta é uma oportunidade de CONSOLIDAÇÃO: absorver as verificações do Constraint Checker no Evaluator, em vez de remover o Evaluator.
  • A consolidação reduz componentes (2→1) sem perder cobertura de proteção.

⚠️ ANÁLISE DE RISCO:
  • Pior cenário se remover: Cliente diz "quero o mais barato", modelo recomenda produto de baixíssima qualidade para agradar. Cliente recebe produto ruim, pede reembolso, não volta. Custo: R$ 50/erro × potencialmente milhares de erros/mês.
  • Probabilidade: Alta. Shadow test interno (Fev/2026) mostrou queda de 8% na acurácia sem Evaluator.
  • Mitigação: NUNCA REMOVER. Invariante arquitetural. Pode ser otimizado (prompts mais curtos, menos tokens), consolidado (absorver Constraint Checker), mas NUNCA removido.

🎯 PRIORIDADE SUGERIDA: N/A (PERMANENTE)
  • Justificativa: Invariante arquitetural. Sycophancy é estrutural. O Evaluator é o gatekeeper que impede que o viés de concordância do modelo prejudique o cliente. Nenhum ROI, por melhor que seja, justificaria sua remoção — mas o ROI de 45x confirma que, além de essencial, é o componente de melhor custo-benefício do harness.
```

---

## 🗺️ Parte 2: Plano de Evolução em 3 Fases

Proponha 3 fases de evolução, seguindo o princípio: **da menos arriscada para a mais estrutural.**

### Regras do Plano

1. **Cada fase remove ou simplifica no máximo 3 componentes.** Mais que isso e você perde rastreabilidade.
2. **Cada fase tem shadow test + canary deploy + observação.** Mínimo de 14 dias de observação entre fases.
3. **Fases posteriores só começam quando a anterior é validada.** Os gates da Parte 3 definem "validada".
4. **Nenhuma fase remove invariantes.** Invariantes (segurança, compliance, sycophancy, disponibilidade) são permanentes. Podem ser simplificados ou otimizados, mas nunca removidos.
5. **Componentes com ROI < 1x devem ser tratados nas fases iniciais (Fase 1 ou 2).**
6. **Simplificações vêm antes de remoções totais, sempre que possível.**
7. **Feature flags padronizados:** `harness_remove_[componente]` ou `harness_simplify_[componente]`.

### Template para Cada Fase

```
═══════════════════════════════════════════════════════════
FASE [N]: [Nome Descritivo da Fase]
Duração: [X semanas]
Risco: [Baixo / Médio / Alto]
═══════════════════════════════════════════════════════════

🎯 OBJETIVO DA FASE:
[1–2 frases sobre o que esta fase alcança e por que esta ordem]

📦 COMPONENTES AFETADOS:

  ┌─────────────────────────────────────────────────────┐
  │ 1. [Componente A] — [⬇️ Remove / ➡️ Simplifica]      │
  ├─────────────────────────────────────────────────────┤
  │ Ação específica: [o que exatamente será feito]       │
  │ Feature flag: harness_[remove|simplify]_[nome]       │
  │ Gatilho: [métrica ou changelog que justifica]         │
  │ Shadow test: [50/50 split, N dias]                   │
  │ Canary: [X% → Y% → Z% ao longo de N dias]            │
  │ Rollback: [como reverter em < 1 hora]                │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ 2. [Componente B] — [⬇️ Remove / ➡️ Simplifica]      │
  ├─────────────────────────────────────────────────────┤
  │ Ação específica: [...]                               │
  │ Feature flag: harness_[remove|simplify]_[nome]       │
  │ Gatilho: [...]                                       │
  │ Shadow test: [...]                                   │
  │ Canary: [...]                                        │
  │ Rollback: [...]                                      │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ 3. [Componente C] — [⬇️ Remove / ➡️ Simplifica]      │
  ├─────────────────────────────────────────────────────┤
  │ Ação específica: [...]                               │
  │ Feature flag: harness_[remove|simplify]_[nome]       │
  │ Gatilho: [...]                                       │
  │ Shadow test: [...]                                   │
  │ Canary: [...]                                        │
  │ Rollback: [...]                                      │
  └─────────────────────────────────────────────────────┘

📊 IMPACTO ESTIMADO DA FASE:

  Métrica                    Antes da Fase        Depois da Fase        Delta
  ─────────────────────      ───────────────      ───────────────      ─────
  Componentes ativos         [N]                  [N]                  [-X]
  Latência média/turno       [X]ms                [X]ms                [-Xms]
  Tokens/mês                 [X]M                 [X]M                 [-X%]
  Custo API mensal           R$ [X]               R$ [X]               [-R$ X]
  Horas manutenção/mês       [X]h                 [X]h                 [-Xh]

📅 CRONOGRAMA DA FASE:

  Semana 1: [shadow test, preparação de feature flags]
  Semana 2: [análise de resultados do shadow test]
  Semana 3: [canary deploy progressivo]
  Semana 4: [observação, documentação, ADRs]

⚠️ RISCOS E MITIGAÇÕES:

  Risco 1: [descrição]
    → Mitigação: [feature flag, alerta, rollback]
    → Probabilidade: [Alta / Média / Baixa]
    → Impacto se ocorrer: [Crítico / Alto / Médio / Baixo]

✅ CRITÉRIOS DE SUCESSO DA FASE (GATES):

  - [ ] Acurácia ≥ 97% (sem queda > 0.5% vs baseline)
  - [ ] Zero incidentes P0/P1 atribuídos às mudanças
  - [ ] CSAT sem queda > 2% vs baseline
  - [ ] Latência reduziu conforme estimado (±10%)
  - [ ] Tokens reduziram conforme estimado (±10%)
  - [ ] ADR escrito para cada componente removido
  - [ ] Código arquivado em archive/components/[nome]/ com README

🚦 GATE PARA PRÓXIMA FASE:

  [Condição para avançar: "14 dias sem incidentes + critérios atendidos + time aprovou"]
```

---

## ✅ Parte 3: Critérios de Validação por Fase

Defina critérios MENSURÁVEIS. "Funcionar bem" ou "estar estável" não são aceitos.

### Checklist de Validação — Geral (Todas as Fases)

| # | Critério | Como Medir | Threshold | Frequência |
|---|---------|------------|-----------|------------|
| 1 | Acurácia do sistema | Amostra de 200 conversas/mês, 2 revisores humanos | ≥ 97% (sem queda > 0.5% vs baseline) | Semanal |
| 2 | Latência média por turno | Dashboard de performance (P50, P95, P99) | Redução conforme estimado (±10%) | Diário |
| 3 | Incidentes P0/P1 | Tracked issues com tag [harness-evolution] | Zero incidentes atribuídos às mudanças | Contínuo |
| 4 | CSAT (satisfação) | Pesquisa pós-conversa (% notas 4–5) | Sem queda > 2pp vs baseline | Semanal |
| 5 | Consumo de tokens | Dashboard de custos por componente | Redução conforme estimado (±10%) | Semanal |
| 6 | Taxa de erro do sistema | Erros 5xx / total de requests | Sem aumento > 0.1% vs baseline | Diário |

### Checklist Específico por Fase

Preencha critérios específicos para cada fase:

```
FASE 1 — CHECKLIST ESPECÍFICO:
  - [ ] [Critério mensurável — ex: "Shadow test 7 dias, delta de acurácia < 0.3%"]
  - [ ] [Critério — ex: "Canary 5% (3d) → 25% (3d) → 100% (3d) sem incidentes"]
  - [ ] Feature flags de rollback testadas: reversão < 10 minutos
  - [ ] ADRs escritos e aprovados para componentes removidos

FASE 2 — CHECKLIST ESPECÍFICO:
  - [ ] [Critério específico]
  - [ ] 14 dias de observação sem regressão
  - [ ] Documentação de arquitetura atualizada

FASE 3 — CHECKLIST ESPECÍFICO:
  - [ ] [Critério específico]
  - [ ] Métricas de baseline pós-evolução documentadas
  - [ ] Post-mortem positivo publicado para o time
```

---

## 📊 Parte 4: Tabela Comparativa — Antes e Depois

Preencha com as estimativas do seu plano.

### Comparação Agregada

| Métrica | Antes (Abr 2026) | Após Fase 1 | Após Fase 2 | Após Fase 3 (Target) | Redução Total |
|---------|--------------------|-------------|-------------|----------------------|---------------|
| Componentes ativos | 11 | | | | |
| Latência média/turno | 1.8s | | | | |
| Tokens/mês (milhões) | 61.7M | | | | |
| Custo API mensal | R$ 9.240 | | | | |
| Horas manutenção/mês | 18h | | | | |
| Arquivos de estado/conversa | 7 | | | | |
| Tempo onboarding (semanas) | 3 | | | | |
| Acurácia (avaliação humana) | 97.1% | | | | ≥ 97% |

### Comparação do Pipeline por Turno

| Etapa do Pipeline | Antes (11 componentes) | Depois (Seu Target) | Ganho |
|-------------------|------------------------|---------------------|-------|
| Pré-processamento | Context Loader (450ms) + Dedup (200ms) + Priority Extractor (150ms) + Budget Guard (100ms) = 900ms | | |
| Core Agents | Planner (800ms) + Generator (1200ms) + Evaluator (600ms) = 2600ms | | |
| Pós-processamento | Format Validator (100ms) + Constraint Checker (300ms) + Fallback Handler (200ms) = 600ms | | |
| History & State | History Compactor (300ms, condicional) + 7 state files | | |
| **Total por Turno** | **~4000ms** | | |

### Comparação de Estratégias de Coordenação

| Dimensão | Harness Atual (11 comp.) | Harness Evoluído (Seu Target) | Ganho Estimado |
|----------|--------------------------|------------------------------|----------------|
| Coordenação entre agentes | File-based com 7 arquivos JSON por turno | | |
| Validação de output | Evaluator + Constraint Checker + Format Validator (3 stages) | | |
| Gestão de contexto | Context Loader + Dedup + Priority Extractor + History Compactor (4 componentes) | | |
| Planejamento | Planner Agent dedicado — toda conversa (35% acionamento) | | |
| Tratamento de erros | 3 estratégias de fallback (retry → alternativa → humano) | | |
| System prompts | ~2000 tokens com tags explícitas e instruções redundantes | | |
| Rastreabilidade | 7 arquivos de estado + trace layer customizada | | |

---

## ⚠️ Parte 5: Invariantes e Análise de Riscos

### O Que São Invariantes

Invariantes são componentes cuja presença **não depende da qualidade do modelo**. Eles protegem contra riscos de domínio, regulatórios ou estruturais — riscos que nenhum modelo, por melhor que seja, elimina.

### Tabela de Invariantes do KODA

Identifique o componente correspondente para cada invariante:

| Invariante | Componente Correspondente | Por Que É Permanente |
|------------|--------------------------|---------------------|
| Segurança do cliente | | Alergias, contraindicações — não é "qualidade de output", é proteção de vida |
| Compliance regulatório (LGPD) | | Consentimento, rastreabilidade — exigências legais independentes do modelo |
| Decisões irreversíveis | | Cobrança, envio de pedido — precisam de checkpoint de sistema |
| Fallback de disponibilidade | | API do modelo pode ficar offline — proteção contra falha do SERVIÇO |
| Gatekeeper de qualidade (anti-sycophancy) | | Sycophancy é estrutural em LLMs — nunca zero, independente da qualidade |
| Auditabilidade | | Sem state persistence, não há como debugar, auditar ou aprender com incidentes |

### Perguntas Que Você Deve Responder

1. **Quais componentes você classificou como invariantes e por quê?**
2. **Qual componente tem o MAIOR potencial de economia (tokens + latência) se removido?** Justifique com números.
3. **Qual componente, se removido incorretamente, causaria o MAIOR dano ao cliente?** Descreva o cenário.
4. **Se o modelo for downgradado no futuro, quais componentes seriam reativados primeiro?** Em que ordem?
5. **Qual o plano de rollback se a Fase 2 causar degradação de acurácia de 97.1% para 95.5%?**
6. **Existe algum componente que você manteve mesmo com ROI < 1x? Se sim, qual e por quê?**

---

## 🚀 Aplicação KODA: Impacto no Mundo Real

### Cenário: Uma Jornada de Cliente Antes e Depois

```
Cliente: "Quero um whey protein vegano, sem gluten, ate R$ 150.
          Treino 4x por semana e tenho intolerancia a lactose.
          Tambem tomo cafe a tarde, entao nada com cafeina."
```

**Antes da Evolução (Pipeline Atual — 11 componentes):**

```
Context Loader (450ms) → Dedup (200ms) → Priority Extractor (150ms)
→ Budget Guard (100ms) → Planner (800ms) → Generator (1200ms)
→ Constraint Checker (300ms) → Format Validator (100ms)
→ Evaluator (600ms) → Fallback Handler (200ms)
→ History Compactor (300ms, condicional)

Latência total: ~4000ms | Tokens/turno: ~3200
Custo/turno: R$ 0.048 | Componentes: 9 de 11
```

**Depois da Evolução (Seu Pipeline Target):**

```
[Descreva aqui o pipeline simplificado que você projetou]

Latência total: [sua estimativa]
Tokens/turno: [sua estimativa]
Custo/turno: [sua estimativa]
Componentes acionados: [sua estimativa]
```

### O Que Muda Para o Time KODA

| Aspecto | Antes (11 comp.) | Depois (Seu Target) | Impacto no Dia a Dia |
|---------|--------------------|--------------------|-----------------------|
| Debugging | 7 state files para analisar | | |
| Onboarding | 3 semanas | | |
| Manutenção | 18h/mês | | |
| Confiabilidade | "Funciona mas ninguém mexe" | | |
| Velocidade de iteração | Cada feature nova impacta 11 componentes | | |

### One In, One Out

Após a evolução, o time adotou a regra: **"Sempre que um componente novo entra, um existente deve ser marcado para investigação de remoção no próximo ciclo."**

**Pergunta:** Se daqui a 6 meses o time precisar adicionar um "Smart Fraud Detector", qual componente existente você marcaria para investigação? Por quê?

### Lições do Mundo Real: O Que Aconteceu com o KODA Após a Evolução

Seis meses depois da reunião do Fernando, o harness do KODA tinha 6 componentes (redução de 45%). Aqui estão os resultados reais que o time reportou na retrospectiva:

| Resultado | Métrica | Impacto no Time |
|-----------|---------|-----------------|
| "Debugging ficou 3x mais rápido" | De 7 state files para 3 | "Antes, quando algo quebrava, a gente abria 7 arquivos e tentava achar onde foi. Agora são 3 — e 2 deles (eval.json e state.json) têm 90% da informação que a gente precisa." — Dev Senior |
| "Onboarding caiu de 3 para 1.5 semanas" | 11 conceitos → 6 conceitos | "Novo dev chegou na segunda e fez o primeiro commit na quarta. Antes levava 2 semanas só para entender o harness." — Tech Lead |
| "Sobrou tempo para features" | 18h → 8h de manutenção/mês | "As 10 horas que a gente ganhou por mês foram para o backlog de features. Em 6 meses, entregamos 4 features que estavam paradas há um ano." — PM |
| "Medo de mexer desapareceu" | Mudança cultural | "O maior ganho não foi técnico. Foi psicológico. O time parou de ter medo do próprio código." — Fernando |

A lição mais importante não está nos números — está na última linha. Um harness mais simples não é apenas mais barato. É um sistema onde as pessoas têm coragem de melhorar.

---

## 🧨 Armadilhas Comuns

### Armadilha 1: "Remover Tudo Que o Changelog Menciona"

**O erro:** Ler "self-correction 3x melhor" e remover o Evaluator.

**Por que é erro:** Changelog descreve benchmarks, não o domínio KODA. Sycophancy é estrutural — o modelo pode ser melhor em self-correction geral e ainda ser sycophantic em recomendações com constraints de saúde.

**Como evitar:** Pergunte: "Isso se aplica ao domínio específico do KODA?" Se não for "sim" com evidência, não remova.

---

### Armadilha 2: "ROI Baixo = Remove Imediatamente"

**O erro:** Ver ROI 0.6x no Fallback Handler e marcar remoção total na Fase 1.

**Por que é erro:** ROI baixo pode significar que o componente está superdimensionado, não que é desnecessário. Você precisa de fallback — só não de 3 estratégias.

**Como evitar:** Antes de remover, pergunte: "Este componente pode ser reduzido em vez de eliminado?"

---

### Armadilha 3: "Todos os Casos Óbvios de Uma Vez"

**O erro:** Colocar 4+ componentes na Fase 1 porque "são todos claros".

**Por que é erro:** Se algo quebrar, você não sabe qual remoção causou. Rollback reverte TUDO.

**Como evitar:** Máximo 3 por fase. Idealmente 2 na Fase 1.

---

### Armadilha 4: "Métricas São a Única Verdade"

**O erro:** Ver ROI 12x no Constraint Checker e manter sem questionar.

**Por que é erro:** ROI alto pode mascarar redundância. Se Constraint Checker e Evaluator validam 70% das mesmas coisas, você paga duas vezes.

**Como evitar:** Cruze métricas com análise de sobreposição.

---

### Armadilha 5: "Esquecer os Invariantes"

**O erro:** Tratar todos os 11 componentes como "potencialmente removíveis".

**Por que é erro:** Alguns componentes não estão no harness porque o modelo é fraco — estão porque o domínio exige. Removê-los porque "o modelo melhorou" é confundir proteção de modelo com proteção de domínio.

**Como evitar:** Pergunte: "Esta proteção depende da qualidade do modelo ou da natureza do domínio?"

---

## 💬 Dúvidas Comuns (FAQ)

**P: Preciso analisar todos os 11 componentes na Parte 1?**
R: A tabela de decisão deve ser preenchida para todos. As análises detalhadas (template) são obrigatórias para no mínimo 6 componentes.

**P: E se minha análise discordar dos exemplos?**
R: Os exemplos são ilustrativos. Se você tem justificativa sólida baseada em métricas + changelog para uma decisão diferente, ela é válida. O que importa é o raciocínio.

**P: Posso propor uma Fase 4?**
R: O exercício pede 3 fases. Se há otimizações adicionais, mencione como "Próximos Passos".

**P: Como calculo o impacto em tokens de uma simplificação?**
R: Use a tabela de métricas como baseline. Se você simplifica o Context Loader (1200 → 400 tokens/turno), economia = 800 × turns/mês. Se remove Budget Guard, economia = 800K tokens/mês.

**P: Preciso ser 100% preciso nas estimativas de latência?**
R: Não. Margem de ~20% é aceitável. O importante é que sejam direcionalmente corretas e proporcionais.

**P: E se o modelo for downgradado?**
R: Por isso o exercício insiste em ARQUIVAR, não DELETAR. Na Parte 5, a pergunta 4 aborda este cenário.

**P: Posso usar os modelos do módulo 05-harness-evolution.md como referência?**
R: Sim. O módulo base contém exemplos detalhados de cada fase com código, métricas e checklists.

**P: Qual a diferença entre "shadow test" e "canary deploy" neste contexto?**
R: Shadow test: você roda o sistema COM e SEM o componente em paralelo (ex: 50% do tráfego cada), mas o cliente SEMPRE vê o output do fluxo COM componente. Você compara os resultados offline para ver se são equivalentes. Canary deploy: você REDIRECIONA uma parcela do tráfego real para o fluxo SEM componente (começando com 5%) e os clientes nessa parcela recebem o output sem o componente. Shadow test é mais seguro (cliente não é impactado). Canary é o passo seguinte (cliente real valida).

**P: Como sei se meu plano está "bom o suficiente"?**
R: Aplique o teste do Fernando: "Se eu mostrar este plano para o time, eles conseguem executá-lo sem me perguntar 'mas como?' ou 'mas e se?'" Se a resposta for sim, o plano está bom. Se houver perguntas sem resposta no plano, ele precisa de mais detalhes.

**P: Posso consolidar dois componentes em um só como parte da evolução?**
R: Sim. Consolidação é uma forma de simplificação. Exemplo: absorver o Constraint Checker no Evaluator. Isso conta como "simplificar" o Constraint Checker (ele deixa de existir como componente independente) e "manter" o Evaluator (que absorve a função). Documente claramente no plano.

**P: O que acontece com os 7 arquivos de estado depois da evolução?**
R: Conforme você remove componentes, os arquivos de estado correspondentes também podem ser consolidados. Se remover Budget Guard, o arquivo `budget.json` some. Se consolidar Constraint Checker no Evaluator, `constraints.json` é absorvido por `eval.json`. O target é reduzir de 7 para 3–4 arquivos de estado.

---

## 📋 Rubric de Avaliação

| Dimensão | Peso | Insuficiente (0–4) | Básico (5–6) | Proficiente (7–8) | Excelente (9–10) |
|----------|------|--------------------|-------------|-------------------|-------------------|
| **Análise de Impacto** (Parte 1) | 20% | Decisões sem justificativa. < 4 componentes analisados. | Baseada só em métricas OU changelog. | Métricas E changelog para maioria. | Métricas + changelog + ciclo de vida + sobreposição. |
| **Plano de 3 Fases** (Parte 2) | 25% | Fases genéricas, sem componentes ou estimativas. | Componentes identificados mas sem ações concretas. | Ações específicas, feature flags, estimativas, cronograma. | Estimativas quantificadas, análise de risco por fase, gates e rollback. |
| **Critérios de Validação** (Parte 3) | 20% | Critérios vagos ("funcionar bem"). | Menciona métricas mas sem thresholds. | Thresholds numéricos e método de medição. | Thresholds + método + frequência + plano de contingência. |
| **Tabela Comparativa** (Parte 4) | 15% | Incompleta ou estimativas irreais. | Preenchida sem justificativa. | Estimativas baseadas nos dados e direcionalmente corretas. | Estimativas precisas com justificativa e trade-offs. |
| **Invariantes e Riscos** (Parte 5) | 20% | Não identifica ou identifica incorretamente. | Identifica sem justificativa. | Justificativa baseada no domínio KODA. | Invariantes + riscos + rollback + cenário de downgrade. |

### Nota Mínima para Aprovação: 7.0

### O Que Diferencia um 7 de um 10

| Nota 7 (Proficiente) | Nota 10 (Excelente) |
|---------------------|---------------------|
| "Remover Budget Guard — sem acionamentos." | "Remover Budget Guard — 0 acionamentos em 145K turns. Janela 32K→500K (15.6x). Conversas típicas = 50K (10% da janela). Custo R$ 120/mês para evento que nunca ocorre. Shadow test 14 dias, delta 0.0%. Feature flag com rollback < 1h. ADR escrito, código arquivado." |
| "Fase 1: remover componentes com ROI baixo." | "Fase 1 — Low-Hanging Fruit: Remover Budget Guard (ROI 0.0x) e simplificar Fallback Handler (3→1 estratégia, ROI 0.6x). Shadow test 7 dias 50/50. Canary 5%→25%→100% em 14 dias. Alerta se taxa erro > 0.5%. Gate: 14 dias sem incidentes. Impacto: -2 comp, -300ms, -R$ 255/mês." |
| "Manter Evaluator — é importante." | "Manter Evaluator — sycophancy é estrutural em LLMs. Shadow test Fev/2026: sem Evaluator, acurácia cai 8% em recomendação. ROI 45x confirma. Invariante arquitetural — NUNCA removível." |

---

## ✍️ Entrega

- [ ] **Parte 1:** Tabela preenchida para 11 componentes + análises detalhadas para ≥ 6
- [ ] **Parte 2:** 3 fases com componentes, ações, feature flags, estimativas, cronograma, riscos e gates
- [ ] **Parte 3:** 6 critérios gerais com thresholds + 3–5 critérios específicos por fase
- [ ] **Parte 4:** 3 tabelas comparativas totalmente preenchidas
- [ ] **Parte 5:** Tabela de invariantes preenchida + 6 perguntas respondidas

---

## 💡 Dicas

1. **Comece pelos casos óbvios.** Budget Guard (ROI 0.0x) e Dedup Layer (ROI 0.8x) → Fase 1.
2. **Use o changelog como guia, não como verdade.** Sempre valide com shadow test.
3. **Simplificar é mais seguro que remover.** Context Loader, Fallback Handler, Priority Extractor → simplifique antes de remover.
4. **Ordem importa.** Fase 1 de menor risco gera confiança para fases seguintes.
5. **Pense no time.** Cada componente removido = menos código, menos debug, menos onboarding.
6. **Documente tudo.** ADR para cada remoção. Código arquivado, não deletado.
7. **Invariantes não se negociam.** Evaluator, State Persistence, verificações de alergia são permanentes.
8. **Seja específico.** "Latência vai cair" ≠ "Latência cai de 4000ms para ~1500ms (-62%: Context Loader -450ms + Dedup -200ms + Budget Guard -100ms + simplificação Fallback -150ms + consolidação pós-processamento -300ms)".

---

## 🔍 Solução

Uma solução de referência completa em:

**`curriculum/03-nivel-3-advanced-architecture/exercises/solutions/exercise-03-solution.md`**

Inclui: análise completa dos 11 componentes, plano em 3 fases, critérios com thresholds, tabelas comparativas, invariantes e riscos.

**Sua solução pode diferir** em ordem de fases ou decisões de simplificação vs remoção — desde que justificadas com métricas e changelog. O que NÃO pode diferir: invariantes (Evaluator, State Persistence, verificações de alergia) e componentes com ROI 0.0x e zero acionamentos (devem ser removidos).

---

## 🎯 Próximos Passos

1. Revise sua solução contra a de referência
2. Entenda o racional das diferenças
3. Aplique o framework a um sistema real
4. Avance para Nível 4: `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md`

---

## 🏆 O Que Você Aprendeu

### Análise Baseada em Dados
- [ ] Interpretar métricas de produção (acionamentos reais vs teóricos, FPs, ROI)
- [ ] Calcular ROI: (Erros Prevenidos × Custo do Erro) / Custo Operacional
- [ ] Mapear capacidades de changelog para decisões arquiteturais
- [ ] Distinguir proteção necessária (ROI > 5x) de proteção teórica (ROI < 1x)
- [ ] Identificar redundância entre componentes

### Planejamento Arquitetural
- [ ] Estruturar evolução em fases de risco controlado
- [ ] Definir gates com thresholds numéricos
- [ ] Estimar impacto em latência, tokens, custo e complexidade
- [ ] Projetar feature flags, shadow tests e canary deploys
- [ ] Balancear economia contra risco de regressão

### Disciplina de Harness Evolution
- [ ] Aplicar BUILD → STABILIZE → SIMPLIFY → REMOVE a um sistema real
- [ ] Identificar invariantes (nunca removíveis)
- [ ] Diferenciar simplificar de remover
- [ ] Aplicar "One In, One Out"
- [ ] Documentar remoções com ADRs

### Pensamento Crítico
- [ ] Questionar "funciona?" com "ainda é necessário?"
- [ ] Tratar changelog como hipótese, não verdade
- [ ] Justificar decisões com evidências quantitativas e qualitativas
- [ ] Reconhecer que complexidade tem custo real
- [ ] Aceitar que "não mexer no que funciona" é uma decisão com custo documentável

### Habilidades de Comunicação Técnica
- [ ] Apresentar um plano de evolução para stakeholders não-técnicos (usando R$ e horas, não latência e tokens)
- [ ] Escrever um ADR que documenta uma remoção com evidências e plano de rollback
- [ ] Conduzir uma architectural review onde o time debate trade-offs de remoção vs simplificação
- [ ] Criar um dashboard de efetividade que o time consulta trimestralmente
- [ ] Liderar pelo exemplo: propor a remoção de um componente que você mesmo construiu

**Se completou com nota ≥ 7:** Pronto para liderar evolução de harness em produção.

**Se teve dificuldade:** Releia as seções correspondentes de `05-harness-evolution.md`.

---

## 📋 Rubric de Auto-Avaliação

| Pergunta | Sim | Parcialmente | Não |
|----------|-----|-------------|-----|
| Consigo explicar cada decisão (Mantém/Simplifica/Remove)? | | | |
| Decisões baseadas em métricas E changelog? | | | |
| Plano segue ordem de risco (baixo → médio → alto)? | | | |
| Cada fase ≤ 3 componentes, cada remoção com feature flag + rollback? | | | |
| Critérios de validação MENSURÁVEIS com thresholds? | | | |
| Consigo estimar impacto em latência e tokens? | | | |
| Identifiquei corretamente os invariantes? | | | |
| Tenho plano de rollback documentado? | | | |
| Entendo diferença entre simplificar e remover? | | | |
| Entendo diferença entre proteção de modelo e proteção de domínio? | | | |

**2+ "Não":** Releia fases SIMPLIFY e REMOVE de `05-harness-evolution.md`.

**Todos "Sim":** Você internalizou o conceito mais importante do Nível 3: **maturidade arquitetural não está em construir mais — está em saber quando remover.**

---

## 💭 Reflexão Final

O desenvolvedor pergunta: **"O que mais posso adicionar para proteger o sistema?"**

O arquiteto pergunta: **"O que posso remover porque o sistema já não precisa dessa proteção?"**

Este exercício testou sua capacidade de pensar como arquiteto. Você analisou 11 componentes, identificou quais ainda são necessários e quais viraram peso morto, e propôs um plano para removê-los com segurança baseado em métricas, não em intuição.

No mundo real, a diferença entre R$ 9.240/mês e R$ 6.000/mês — com a mesma qualidade — é esta disciplina.

> *"A gente construiu esse harness para proteger um modelo que não existe mais. O modelo de hoje é diferente. Mais forte. E um harness desenhado para um modelo mais fraco não é proteção — é peso morto."* — Fernando

**Construir um harness é um ato de humildade.** Você reconhece fraquezas e cria proteções.

**Evoluir um harness é um ato de confiança.** Você reconhece que o modelo melhorou, que as proteções fizeram seu trabalho, e que é hora de seguir em frente com uma arquitetura mais leve.

Bons arquitetos constroem sistemas que funcionam.
Grandes arquitetos constroem sistemas que **continuam simples** conforme evoluem.

**Agora, olhe para o harness do seu próprio sistema. O que você pode remover hoje?**

---

*Exercício 3 — Plano de Evolução do Harness KODA | Nível 3 — Arquitetura Avançada*

---

## 🔍 Checklist de Consistência: Valide Seu Próprio Plano

Antes de considerar o exercício concluído, passe seu plano por este checklist. Ele verifica se não há contradições internas — o erro mais comum em planos de arquitetura.

### Consistência Entre Partes

| Verificação | O Que Checar | Exemplo de Inconsistência |
|-------------|-------------|--------------------------|
| Parte 1 → Parte 2 | Todo componente marcado como ⬇️ Remove ou ➡️ Simplifica na Parte 1 aparece em alguma fase na Parte 2? | Marcou Dedup Layer como Remove na Parte 1 mas esqueceu de incluí-lo em qualquer fase na Parte 2. |
| Parte 2 → Parte 4 | As estimativas de latência/tokens na Parte 4 são consistentes com as ações descritas na Parte 2? | Na Parte 2 removeu Budget Guard (100ms) + Dedup (200ms) mas na Parte 4 a latência só caiu 150ms. |
| Parte 2 → Parte 3 | Os critérios de validação na Parte 3 cobrem todos os riscos identificados na Parte 2? | Na Parte 2 identificou risco de "degradação de acurácia" mas na Parte 3 não tem critério de acurácia. |
| Parte 5 → Parte 1 | Nenhum componente listado como invariante na Parte 5 está marcado como Remove na Parte 1? | Marcou "Segurança do cliente → Constraint Checker" como invariante, mas na Parte 1 marcou Constraint Checker como Remove. |
| Parte 4 → Métricas | As estimativas da Parte 4 são matematicamente possíveis com os dados fornecidos? | Estimou economia de R$ 3.000/mês mas a soma de todos os componentes com ROI < 1x é apenas R$ 555/mês. |
| Regra das Fases | Nenhuma fase tem mais de 3 componentes? Fases seguem risco crescente? | Fase 1: 4 componentes (viola regra). Fase 1: alto risco, Fase 2: baixo risco (ordem invertida). |

### Perguntas de Sanity Check

Responda estas perguntas para validar que seu plano faz sentido como um todo:

1. **Se eu executar a Fase 1 e algo quebrar, eu sei exatamente qual componente reverter?** Se a Fase 1 tem 3 componentes e você não consegue apontar qual deles provavelmente causaria o problema, a fase tem componentes demais ou muito similares entre si.

2. **Meu plano reduz COMPLEXIDADE ou só reduz CUSTO?** Um plano que remove 5 componentes baratos (Budget Guard, Dedup, Fallback) reduz custo mas não necessariamente complexidade. Um plano que consolida Constraint Checker + Evaluator reduz complexidade (2 code paths → 1). O ideal é fazer ambos, mas priorize redução de complexidade.

3. **Se eu mostrar este plano para o Dev Junior que entrou ontem, ele entende o que vai mudar e por quê?** Se a resposta for não, o plano precisa de mais clareza nas justificativas.

4. **Daqui a 12 meses, com um modelo ainda mais novo, quais componentes deste plano sobreviveriam a OUTRA rodada de evolução?** Se a resposta for "todos", seu plano provavelmente é conservador demais. Se for "nenhum", é agressivo demais.

5. **O cliente do KODA sentiria alguma diferença se este plano fosse executado?** A resposta deve ser "não" para qualidade (a acurácia se mantém) e "sim" para velocidade (a latência cai). Se o cliente sentir diferença na qualidade, o plano foi longe demais.

---

## 🎤 Dicas Para Apresentar Seu Plano

Se você precisar apresentar este plano para o time (como o Fernando fez), aqui estão algumas dicas baseadas no que funcionou na reunião real:

### A Ordem Que Convence

1. **Comece pelos números, não pelas opiniões.** "O Budget Guard teve zero acionamentos em 145 mil turns" convence mais que "eu acho que o Budget Guard não é necessário". A planilha do Fernando convenceu o time em 2 minutos.

2. **Mostre o custo em dinheiro, não em tokens.** "R$ 9.240 por mês" é mais impactante que "61.7 milhões de tokens". Stakeholders não-técnicos entendem dinheiro. Devs entendem os dois — mostre ambos.

3. **Comece pela Fase 1 (risco zero).** Se a primeira coisa que você propuser for "remover o Evaluator", o time vai travar. Se for "remover o Budget Guard que nunca disparou", o time vai concordar. Use a Fase 1 para construir credibilidade.

4. **Tenha o plano de rollback pronto antes que perguntem.** Quando alguém perguntar "e se der errado?", você já tem o slide com "Feature flag `harness_remove_X`, reversão em < 1 hora, código arquivado em `archive/`". Isso transforma objeção em confiança.

5. **Termine com o impacto humano.** "Onboarding cai de 3 para 1.5 semanas" e "10 horas por mês liberadas para features" são os argumentos que convertem céticos. Todo mundo já sofreu com onboarding lento ou backlog infinito.

### O Que NÃO Fazer na Apresentação

- ❌ Começar com diagrama de arquitetura (as pessoas se perdem antes de chegar nos argumentos)
- ❌ Usar jargão sem explicar ("vamos fazer shadow test com canary deploy progressivo" — explique cada termo uma vez)
- ❌ Propor remover algo que um colega construiu sem reconhecer o valor que teve ("o Budget Guard foi essencial por 12 meses — agora o modelo evoluiu e podemos aposentá-lo com honra")
- ❌ Apresentar sem ter testado os números ("latência deve cair uns 30%" — "deve" não convence; "latência cai de 1.8s para 1.3s, redução de 28%, baseado na remoção de X, Y e Z" convence)

### Template de Slide Executivo

Se você tiver 5 minutos com um stakeholder, use este template:

```
═══════════════════════════════════════════════════════════
           EVOLUÇÃO DO HARNESS KODA — PROPOSTA
═══════════════════════════════════════════════════════════

ONDE ESTAMOS:
  11 componentes | R$ 9.240/mês | 1.8s/turno | 18h manutenção

ONDE QUEREMOS CHEGAR (3 fases, 12 semanas):
  6 componentes | R$ 6.000/mês | 0.9s/turno | 8h manutenção

COMO (Fase 1 — risco zero, 4 semanas):
  Remover Budget Guard (0 acionamentos) + Dedup Layer (ROI 0.8x)
  Shadow test → canary → observação → documentação

E SE DER ERRADO?
  Feature flag. Rollback em < 1 hora. Código arquivado, não deletado.

GANHO PARA O TIME:
  10h/mês liberadas para features | Onboarding 2x mais rápido
═══════════════════════════════════════════════════════════
```

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-03.md` |
| **Nível** | 3 — Arquitetura Avançada |
| **Tempo Estimado** | 60–90 minutos |
| **Dificuldade** | ⭐⭐⭐ (Intermediário-Avançado) |
| **Status** | ✅ Completo |
| **Pré-requisito** | `05-harness-evolution.md` |
| **Solução** | `exercises/solutions/exercise-03-solution.md` |
| **Próximo** | `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md` |
| **Atualizado** | Maio 2026 |
