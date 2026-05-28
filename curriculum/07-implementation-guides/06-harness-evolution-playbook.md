# 🧬 Playbook de Harness Evolution: Como Evoluir um Harness de Agente sem Quebrar Produção
## Guia Prático para Diagnosticar, Planejar, Executar e Validar Remoções com Segurança

**Tempo Estimado:** 4 a 6 horas para leitura completa, 2 a 6 semanas para execução em produção  
**Nível:** Guia de Implementação, após Nível 3  
**Pré-requisito:** Ter lido `03-nivel-3-advanced-architecture/05-harness-evolution.md`  
**Status:** 🟢 GUIA PRÁTICO, pronto para execução assistida  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Segunda-Feira em que Você Segurou a Tesoura

Fernando já tinha contado a história na sala de arquitetura. O Context Loader custava 1200 tokens por turno, adicionava 450ms de latência, tinha 12 prevenções reais em 145 mil turns e produzia 340 falsos positivos. O Budget Guard, pior ainda, tinha zero triggers em 180 dias. Todo mundo entendeu a teoria. O harness não pode crescer para sempre.

Mas teoria não remove código em produção.

Na segunda-feira seguinte, a responsabilidade caiu na sua mesa. Você abriu o repositório do KODA, olhou para o pipeline com onze componentes e percebeu que a pergunta tinha mudado. Não era mais se o harness deveria evoluir. Era como fazer isso sem transformar uma limpeza arquitetural em incidente para clientes reais.

O Slack estava silencioso, aquele silêncio que aparece quando todo mundo concorda com a direção mas ninguém quer ser a primeira pessoa a apertar o botão. Fernando apareceu na call com a calma desconfortável de quem já viu remoção mal feita derrubar produção.

Ele disse uma frase simples: "Você não vai remover um componente. Você vai provar que ele pode sair."

Essa frase é o coração deste playbook.

Você vai trabalhar como alguém que respeita o código antigo, mas não tem medo dele. Cada componente que existe hoje nasceu por um motivo. Talvez o motivo ainda seja válido. Talvez o modelo tenha evoluído. Talvez outro componente tenha absorvido a responsabilidade. Talvez ninguém tenha percebido que o custo mensal virou maior que o risco protegido.

O seu trabalho é separar nostalgia de evidência.

No primeiro dia, você não vai deletar nada. Você vai medir. Vai abrir traces. Vai contar triggers reais. Vai separar falso positivo de prevenção verdadeira. Vai montar uma scorecard. Vai conversar com suporte, produto e engenharia. Vai descobrir quais componentes são invariantes, quais são scaffolding e quais viraram peso morto.

No segundo momento, você vai planejar. Não com um roadmap bonito para apresentação, mas com uma sequência segura de mudanças pequenas. Uma flag por componente. Um canary de 5%, depois 25%, depois 100%. Um shadow test antes de confiar no changelog. Uma janela de 14 dias para observar antes de comemorar.

Depois vem a parte que dá frio na barriga: execução. Você vai desligar uma peça que já salvou o sistema no passado. Vai deixar o dashboard aberto. Vai comparar antes e depois. Vai saber onde está o rollback. Vai resistir à tentação de remover três coisas ao mesmo tempo só porque tudo parece óbvio.

E, se tudo der certo, ninguém vai notar. O cliente não vai perceber. O time de suporte não vai receber tickets novos. A latência vai cair. O custo vai cair. O diagrama vai ficar menor. Novos devs vão entender o sistema mais rápido.

Essa é a vitória discreta de Harness Evolution.

Este guia é o roteiro para essa vitória. Não é uma releitura da teoria. É o manual de campo para você executar a evolução do harness com métricas, disciplina e coragem.

---

## 🧭 Como Usar Este Playbook

Use este arquivo como checklist operacional. Ele foi escrito para uma pessoa que já entende a base conceitual de Harness Evolution e agora precisa conduzir a mudança em um sistema real.

A sequência é intencional. Você começa com diagnóstico, transforma evidência em roadmap, executa uma mudança pequena por vez e valida antes de declarar sucesso.

Não pule a fase de diagnóstico. Não use changelog como prova. Não remova invariantes como Evaluator, State Persistence, Safety e Compliance. Essas proteções existem por natureza do domínio, não por fraqueza temporária do modelo.

Se você está trabalhando no KODA, trate todos os exemplos como ponto de partida. Troque números quando tiver métricas reais. Mantenha o método.

| Fase | Resultado Esperado | Artefato Principal | Decisão |
|------|--------------------|--------------------|---------|
| 🩺 Diagnóstico | Entender valor, custo e risco de cada componente | Diagnostic Report | Candidato ou não candidato |
| 📋 Planejamento | Ordenar mudanças com segurança | Evolution Roadmap | KEEP, SIMPLIFY, REMOVE ou INVESTIGATE |
| 🔧 Execução | Alterar produção com controle | Feature flag, shadow test e archive | Expandir, pausar ou rollback |
| ✅ Validação | Provar que a remoção foi segura | Validation Report e ADR | Encerrar ou reverter |

---

## 🧬 Lembrete Conceitual: O Que Você Está Evoluindo

Antes de tocar no harness, alinhe o vocabulário com o time. Um componente de harness é qualquer peça que envolve o modelo para compensar uma limitação, coordenar trabalho, persistir estado, avaliar qualidade, aplicar regra de segurança ou manter auditabilidade.

O ciclo de vida do módulo conceitual continua sendo a base:

```text
┌────────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA DO HARNESS                         │
├────────────────┬────────────────┬────────────────┬────────────────┤
│ BUILD          │ STABILIZE      │ SIMPLIFY       │ REMOVE         │
│ Protege modelo │ Mede valor     │ Reduz peso     │ Arquiva peça   │
│ fraco ou novo  │ real em prod   │ com evidência  │ desnecessária  │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

Neste playbook, você opera no trecho prático entre STABILIZE, SIMPLIFY e REMOVE. O objetivo não é provar que o modelo novo é mágico. O objetivo é provar, com tráfego real e testes, que uma proteção específica já não paga seu próprio custo.

---

## 🧱 Arquitetura de Referência: Antes e Depois da Evolução

Use estes diagramas como linguagem comum durante a revisão. Eles são novos para este playbook e mostram a diferença entre um harness pesado, criado para um modelo antigo, e um harness evoluído, mantido pequeno por evidência.

### 🧱 Antes: Harness com Scaffolding Acumulado

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                         KODA HARNESS ANTES DA EVOLUÇÃO                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Cliente WhatsApp                                                             │
│        │                                                                     │
│        ▼                                                                     │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐              │
│  │ Context      │────▶│ Dedup Layer  │────▶│ Priority       │              │
│  │ Loader       │     │              │     │ Extractor      │              │
│  └──────┬───────┘     └──────┬───────┘     └───────┬────────┘              │
│         │                    │                     │                       │
│         ▼                    ▼                     ▼                       │
│  ┌────────────────────────────────────────────────────────────┐             │
│  │              State Persistence Layer                       │             │
│  │  customer.json  plan.json  draft.json  eval.json  log.jsonl│             │
│  └────────────────────────────┬───────────────────────────────┘             │
│                               │                                             │
│                               ▼                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐              │
│  │ Planner      │────▶│ Generator    │────▶│ Constraint     │              │
│  │ Agent        │     │ Agent        │     │ Checker        │              │
│  └──────────────┘     └──────┬───────┘     └───────┬────────┘              │
│                              │                     │                       │
│                              ▼                     ▼                       │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐              │
│  │ Format       │────▶│ Evaluator    │────▶│ Fallback       │              │
│  │ Validator    │     │ Agent        │     │ Handler        │              │
│  └──────┬───────┘     └──────┬───────┘     └───────┬────────┘              │
│         │                    │                     │                       │
│         ▼                    ▼                     ▼                       │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐              │
│  │ Budget Guard │────▶│ Trace Layer  │────▶│ History        │              │
│  │              │     │              │     │ Compactor      │              │
│  └──────────────┘     └──────────────┘     └───────┬────────┘              │
│                                                     │                       │
│                                                     ▼                       │
│                                             Resposta ao cliente             │
│                                                                              │
│  Custo típico: 11 componentes, 3200 tokens por turno, 4000ms de latência     │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 🌱 Depois: Harness Essencial e Medido

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                       KODA HARNESS DEPOIS DA EVOLUÇÃO                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Cliente WhatsApp                                                             │
│        │                                                                     │
│        ▼                                                                     │
│  ┌────────────────────────────────────────────────────────────┐              │
│  │ State Loader                                                │              │
│  │ Carrega dados críticos no início e quando há mudança real   │              │
│  └────────────────────────────┬───────────────────────────────┘              │
│                               │                                              │
│                               ▼                                              │
│  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐           │
│  │ Generator      │────▶│ Evaluator      │────▶│ History        │           │
│  │ Agent          │     │ Unificado      │     │ Compactor      │           │
│  └───────┬────────┘     └───────┬────────┘     └───────┬────────┘           │
│          │                      │                      │                    │
│          ▼                      ▼                      ▼                    │
│  ┌────────────────────────────────────────────────────────────┐              │
│  │ Audit Log + State Persistence                              │              │
│  │ state.json  audit_log.jsonl  validation_summary.json        │              │
│  └────────────────────────────┬───────────────────────────────┘              │
│                               │                                              │
│                               ▼                                              │
│                     Retry simples ou escalação humana                        │
│                               │                                              │
│                               ▼                                              │
│                        Resposta ao cliente                                   │
│                                                                              │
│  Custo típico: 6 componentes, 1400 tokens por turno, 1500ms de latência      │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 📊 Estratégias de Coordenação: Comparação Expandida

| Dimensão | Antes da evolução | Depois da evolução | Evidência exigida | Risco se errar |
|----------|-------------------|--------------------|-------------------|----------------|
| Coordenação entre agentes | 5 a 7 arquivos JSON por turno | 2 a 3 arquivos JSON por turno | Trace mostra arquivos sem leitura útil | Debug perde contexto se consolidar demais |
| Context management | Context Loader em todo turno | State Loader no início e History Compactor condicional | Recall estável sem preload constante | Cliente sente que KODA esqueceu dados críticos |
| Validação de output | Constraint Checker, Format Validator e Evaluator separados | Evaluator unificado com rubrica explícita | Overlap maior que 50% entre checks | Erro de domínio passa sem bloqueio |
| Planejamento | Planner sempre roda | Planner só roda para jornadas complexas | Classificador mostra 70% de fluxos simples | Fluxo complexo pode sair sem plano |
| Fallback | Retry, alternativa, humano e regeneração completa | Retry simples, depois escalação | Falhas repetidas são raras e rastreáveis | Loop longo pode voltar |
| Prompts | 2000 a 3000 tokens com exemplos repetidos | 500 a 800 tokens com princípios e constraints | Structured output e instruction following estáveis | Modelo pode perder nuance específica |
| Trace | Arquivos separados por etapa | Audit log único com resumo validado | Consultas de debug usam poucos campos | Auditoria fica pobre |
| Budget | Budget Guard por turno | Alerta agregado por conversa longa | Zero triggers em 180 dias | Conversa extrema pode estourar janela |
| Dedup | Camada dedicada antes do Planner | Dedup dentro do compactor | Duplicatas não afetam resposta final | Ruído pode aumentar prompt |
| Priority extraction | Extractor dedicado | Prioridade inferida no Evaluator | Falsos positivos altos no extractor | Alergia ou orçamento pode perder prioridade |
| Observabilidade | Logs verbosos por componente | Dashboard por outcome e custo | Perguntas de incidentes ainda respondidas | Menos log pode dificultar investigação |
| Onboarding | Arquitetura exige mapa manual | Pipeline cabe em uma página | Novos devs explicam fluxo em 30 minutos | Simplificação pode esconder regra crítica |

---

## 🩺 Fase 1: Diagnóstico

Diagnóstico é a fase em que você troca opinião por evidência. O resultado não é uma decisão ainda. O resultado é um mapa confiável de custo, valor, risco e redundância.

### 🩺 Objetivo da Fase

- Inventariar todos os componentes do harness.
- Medir taxa de acionamento efetiva.
- Separar prevenção real de falso positivo.
- Calcular custo operacional completo.
- Calcular ROI com fórmula padronizada.
- Identificar componentes para KEEP, SIMPLIFY, REMOVE ou INVESTIGATE na próxima fase.
- Proteger invariantes contra remoção acidental.

### 🩺 Passo 1: Monte o Inventário de Componentes

Comece com uma lista simples. Não tente decidir nada enquanto inventaria. Decisão prematura contamina a análise.

| Campo | Como preencher | Exemplo KODA |
|-------|----------------|--------------|
| Nome | Nome operacional do componente | Context Loader |
| Owner | Pessoa ou squad que mantém | Squad Conversational Core |
| Criado em | Data aproximada ou ADR original | Novembro 2025 |
| Motivo original | Fraqueza que o componente compensava | Modelo perdia contexto após 40 minutos |
| Tipo | Safety, compliance, context, quality, cost, coordination | context |
| Runtime path | Onde roda no pipeline | Antes do Generator |
| Custo primário | Tokens, latência, manutenção ou complexidade | 1200 tokens por turno |
| Métrica protegida | O que pioraria sem ele | Recall de constraints críticas |
| Invariante | Sim ou não | Não para Context Loader, sim para Safety checks |

```json
{
  "component_inventory": [
    {
      "name": "ContextLoader",
      "owner": "conversational-core",
      "created_at": "2025-11-15",
      "original_reason": "Modelo com janela de 32K perdia dados críticos em conversas longas.",
      "component_type": "context",
      "pipeline_position": "before_generator",
      "primary_cost": "1200 tokens/turn, 450ms/turn",
      "protected_metric": "critical_constraint_recall",
      "architectural_invariant": false
    },
    {
      "name": "Evaluator",
      "owner": "quality-platform",
      "created_at": "2025-10-05",
      "original_reason": "Separar geração de avaliação para reduzir self-evaluation collapse.",
      "component_type": "quality",
      "pipeline_position": "after_generator",
      "primary_cost": "500ms/turn",
      "protected_metric": "unsafe_or_incorrect_recommendation_rate",
      "architectural_invariant": true
    }
  ]
}
```

### 🩺 Passo 2: Colete Métricas dos Últimos 90 Dias

Use 90 dias como janela padrão. Se o componente tem menos tempo em produção, use no mínimo 60 dias. Abaixo disso, marque como INVESTIGATE, não como REMOVE.

| Métrica | Definição | Exemplo |
|---------|-----------|---------|
| total_turns_processed | Total de turns avaliados pelo componente | 145000 |
| component_trigger_count | Quantas vezes o componente disparou | 352 |
| real_preventions | Quantas vezes preveniu falha confirmada | 12 |
| false_positives | Quantas vezes bloqueou fluxo correto | 340 |
| tokens_per_turn | Tokens adicionais por turno | 1200 |
| latency_ms_per_turn | Latência adicional por turno | 450 |
| maintenance_hours_month | Horas mensais de manutenção | 3 |
| incident_count_protected | Incidentes atribuíveis à categoria protegida | 0 nos últimos 45 dias |
| shadow_delta | Diferença com e sem componente | -0.4% accuracy |

### 🩺 Passo 3: Calcule a Effective Trigger Rate

A taxa que importa não é quantas vezes o componente disparou. A taxa que importa é quantas vezes ele disparou e realmente evitou um erro que chegaria ao cliente.

```python
def effective_trigger_rate(real_preventions: int, total_turns: int) -> float:
    if total_turns == 0:
        return 0.0
    return real_preventions / total_turns

# Preventions breakdown: 12 criticas + 47 nao-criticas = 59 total
context_loader_rate_critica = effective_trigger_rate(
    real_preventions=12,
    total_turns=145000,
)
context_loader_rate_total = effective_trigger_rate(
    real_preventions=59,
    total_turns=145000,
)

print(f"Effective Trigger Rate (critica): {context_loader_rate_critica:.6%}")
print(f"Effective Trigger Rate (total): {context_loader_rate_total:.6%}")
# Resultado: 0.008% critica, 0.041% total
```

Interprete assim:

| Effective Trigger Rate | Leitura | Ação provável |
|------------------------|---------|---------------|
| Maior que 5% | Componente protege fluxo comum | KEEP ou SIMPLIFY com cuidado |
| 1% a 5% | Valor real, mas talvez caro | SIMPLIFY se custo for alto |
| 0.1% a 1% | Valor raro, precisa de custo baixo | INVESTIGATE ou SIMPLIFY |
| 0.01% a 0.1% | Proteção quase nunca usada | REMOVE se não for invariante |
| 0% | Sem prevenção observada | REMOVE se shadow test confirmar |

### 🩺 Passo 4: Faça a Análise de Falsos Positivos

Falso positivo é dívida escondida. Ele não aparece como incidente, mas cria fricção para cliente, suporte e engenharia. No KODA, o Context Loader tinha 340 falsos positivos para 12 prevenções reais. Isso significa 28 falsos bloqueios para cada prevenção verdadeira.

```python
def false_positive_ratio(false_positives: int, real_preventions: int) -> float:
    if real_preventions == 0:
        return float("inf")
    return false_positives / real_preventions

ratio = false_positive_ratio(false_positives=340, real_preventions=12)
print(f"False Positive Ratio: {ratio:.1f}x")
# Resultado esperado: 28.3x
```

| Ratio | Interpretação | Próxima pergunta |
|-------|---------------|------------------|
| 0x a 1x | Componente é preciso | O custo ainda compensa? |
| 1x a 5x | Fricção moderada | Dá para ajustar threshold? |
| 5x a 10x | Fricção alta | O componente está conservador demais? |
| Acima de 10x | Fricção crítica | Por que ainda está no caminho principal? |
| Infinito | Nunca preveniu, só bloqueou | Pode sair depois de shadow test? |

### 🩺 Passo 5: Calcule o Custo Completo

Custo não é só API. Some tokens, latência, manutenção, onboarding e complexidade de debug. Se o time só mede custo de API, quase sempre subestima o peso de harness antigo.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ComponentCost:
    monthly_token_cost_brl: float
    monthly_maintenance_hours: float
    hourly_engineering_cost_brl: float
    monthly_latency_cost_brl: float
    monthly_debug_cost_brl: float

    def total_monthly_cost(self) -> float:
        maintenance_cost = self.monthly_maintenance_hours * self.hourly_engineering_cost_brl
        return (
            self.monthly_token_cost_brl
            + maintenance_cost
            + self.monthly_latency_cost_brl
            + self.monthly_debug_cost_brl
        )

context_loader_cost = ComponentCost(
    monthly_token_cost_brl=810.0,
    monthly_maintenance_hours=3.0,
    hourly_engineering_cost_brl=150.0,
    monthly_latency_cost_brl=200.0,
    monthly_debug_cost_brl=150.0,
)

print(context_loader_cost.total_monthly_cost())
# Resultado esperado: 1610.0
```

### 🩺 Passo 6: Calcule ROI

A fórmula operacional é simples. Use a mesma em todos os componentes para evitar debate sem base comum.

```text
ROI = (Erros Prevenidos x Custo Médio do Erro) / Custo Operacional do Componente
```

```python
def component_roi(
    real_preventions: int,
    average_error_cost_brl: float,
    operational_cost_brl: float,
) -> float:
    if operational_cost_brl == 0:
        return float("inf")
    protected_value = real_preventions * average_error_cost_brl
    return protected_value / operational_cost_brl

context_loader_roi = component_roi(
    real_preventions=59,
    average_error_cost_brl=50.0,
    operational_cost_brl=1460.0,
)

budget_guard_roi = component_roi(
    real_preventions=0,
    average_error_cost_brl=50.0,
    operational_cost_brl=300.0,
)

print(f"Context Loader ROI: {context_loader_roi:.1f}x")
print(f"Budget Guard ROI: {budget_guard_roi:.1f}x")
# Context Loader ROI: 2.0x
# Budget Guard ROI: 0.0x
```

| ROI | Interpretação | Decisão inicial |
|-----|---------------|-----------------|
| Maior que 5x | Valor claro | KEEP, talvez otimizar custo |
| 2x a 5x | Valor positivo | KEEP ou SIMPLIFY |
| 1x a 2x | Valor marginal | SIMPLIFY ou INVESTIGATE |
| 0.1x a 1x | Custo maior que valor | REMOVE se não for invariante |
| 0x | Nenhum valor observado | REMOVE após validação |

### 🩺 Passo 7: Procure os 7 Sinais de Remoção

| # | Sinal | Como reconhecer | Exemplo KODA |
|---|-------|----------------|--------------|
| 1 | Taxa de acionamento efetiva abaixo de 0.1% por 90 dias | O componente quase nunca evita erro real | Budget Guard com zero triggers em 180 dias |
| 2 | Falsos positivos mais de 10x acima das prevenções reais | A proteção machuca mais fluxos bons do que salva ruins | Context Loader com 340 falsos positivos e 12 prevenções críticas |
| 3 | Changelog do modelo cobre a fraqueza original e shadow test confirma | A hipótese antiga deixou de ser válida | Context window maior reduz necessidade de preload constante |
| 4 | Outro componente cobre a mesma responsabilidade | Há redundância clara no pipeline | Constraint Checker e Evaluator validando a mesma restrição |
| 5 | ROI abaixo de 1x por dois trimestres | O custo supera o valor protegido | Budget Guard com ROI 0x |
| 6 | Onboarding depende de explicação histórica longa | Novos devs não entendem por que existe | Priority Extractor parece duplicar raciocínio do Evaluator |
| 7 | Latência ou tokens são perceptíveis para cliente ou margem | O componente pesa no produto | Context Loader adiciona 450ms por turno |

### 🩺 Passo 8: Monte o Dashboard de Efetividade

O dashboard deve caber em uma tela. Se precisa de cinco abas para decidir, você ainda não organizou a evidência.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    HARNESS EFFECTIVENESS DASHBOARD                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ Período: últimos 90 dias                                                     │
│ Modelo atual: Claude Sonnet 4.6                                              │
│ Total de turns: 145000                                                       │
├──────────────────────┬──────────────────────┬──────────────────────────────┤
│ COMPONENTE           │ VALOR                │ CUSTO                        │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ Context Loader       │ 12 prevenções reais  │ 1200 tokens, 450ms, ROI 2.0x │
│ Budget Guard         │ 0 prevenções reais   │ 200 BRL mês, ROI 0x          │
│ Format Validator     │ 8 correções reais    │ 100ms, baixo custo           │
│ Evaluator            │ 430 rejeições úteis  │ 500ms, invariante            │
├──────────────────────┴──────────────────────┴──────────────────────────────┤
│ FALSE POSITIVE WATCH                                                         │
├──────────────────────┬──────────────────────┬──────────────────────────────┤
│ Context Loader       │ 340 falsos positivos │ 28.3x acima das prevenções   │
│ Priority Extractor   │ 81 falsos positivos  │ 9.0x acima das prevenções    │
├──────────────────────┴──────────────────────┴──────────────────────────────┤
│ RECOMENDAÇÃO DO DIAGNÓSTICO                                                  │
│ REMOVE: Budget Guard                                                         │
│ SIMPLIFY: Context Loader, Format Validator                                   │
│ KEEP: Evaluator, Safety, Compliance, State Persistence                       │
│ INVESTIGATE: Priority Extractor                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 🩺 Passo 9: Preencha a Scorecard

| Componente | Trigger efetivo | Falsos positivos | Custo mensal | ROI | Redundância | Invariante | Score | Recomendação |
|------------|-----------------|------------------|--------------|-----|-------------|------------|-------|--------------|
| Context Loader | 0.008% | 340 | R$ 1610 | 2.0x | Alta | Não | 68/100 | SIMPLIFY |
| Budget Guard | 0% | 0 | R$ 300 | 0x | Baixa | Não | 92/100 | REMOVE |
| Evaluator | 12.4% | 31 | R$ 2400 | 8.7x | Baixa | Sim | 15/100 | KEEP |
| State Persistence | Sempre ativo | 0 | R$ 600 | Não aplicável | Baixa | Sim | 5/100 | KEEP |
| Format Validator | 0.05% | 14 | R$ 120 | 1.3x | Média | Não | 54/100 | SIMPLIFY |
| Priority Extractor | 0.02% | 81 | R$ 480 | 0.7x | Alta | Não | 75/100 | INVESTIGATE |

Score alto significa candidato forte a mudança. Score baixo significa manter.

### 🩺 Checklist Operacional de Diagnóstico

- [ ] 1. Inventário contém todos os componentes do pipeline atual.
- [ ] 2. Cada componente tem owner identificado.
- [ ] 3. Cada componente tem motivo original documentado.
- [ ] 4. Cada componente tem posição no pipeline descrita.
- [ ] 5. Cada componente tem métrica protegida definida.
- [ ] 6. Invariantes foram marcados antes de discutir remoção.
- [ ] 7. Foram coletados pelo menos 60 dias de dados.
- [ ] 8. Janela preferencial de 90 dias foi usada quando disponível.
- [ ] 9. Trigger bruto foi separado de prevenção real.
- [ ] 10. Falso positivo foi definido com exemplos concretos.
- [ ] 11. Time de suporte revisou exemplos de falsos positivos.
- [ ] 12. Time de produto revisou custo de erro médio.
- [ ] 13. Tokens por turno foram medidos em produção.
- [ ] 14. Latência por turno foi medida no caminho real.
- [ ] 15. Horas de manutenção foram estimadas com owner.
- [ ] 16. Custo de onboarding foi registrado como evidência qualitativa.
- [ ] 17. ROI foi calculado com a fórmula padrão.
- [ ] 18. Componentes com ROI 0x foram destacados.
- [ ] 19. Componentes com ROI marginal foram marcados para simplificação.
- [ ] 20. Shadow tests existentes foram anexados ao relatório.
- [ ] 21. Changelogs de modelo foram tratados como hipótese, não como prova.
- [ ] 22. Dashboard mostra valor e custo na mesma tela.
- [ ] 23. Scorecard tem recomendação preliminar, não decisão final.
- [ ] 24. Nenhum componente invariante foi marcado como REMOVE.
- [ ] 25. Exemplos KODA foram anexados para apoiar revisão executiva.

---

## 📋 Fase 2: Planejamento

Planejamento transforma diagnóstico em uma sequência segura de evolução. O erro comum é escolher a maior economia primeiro. O caminho correto é escolher a combinação de impacto, baixo risco e reversibilidade.

### 📋 Passo 1: Classifique Cada Componente

| Classe | Quando usar | Próxima ação | Exemplo KODA |
|--------|-------------|-------------|--------------|
| KEEP | Componente é invariante ou ROI alto | Documentar por que fica | Evaluator |
| SIMPLIFY | Componente tem valor mas custo alto ou redundância | Reduzir escopo, tokens ou posição no pipeline | Context Loader |
| REMOVE | Componente não entrega valor real e não é invariante | Preparar feature flag e canary | Budget Guard |
| INVESTIGATE | Dados insuficientes ou conflitantes | Rodar shadow test e coletar mais métricas | Format Validator |

```yaml
classification_rules:
  keep:
    - architectural_invariant: true
    - roi_minimum: 5.0
    - effective_trigger_rate_minimum: 0.05
  simplify:
    - roi_between: [1.0, 5.0]
    - redundancy: medium_or_high
    - false_positive_ratio_above: 5.0
  remove:
    - architectural_invariant: false
    - roi_below: 1.0
    - effective_trigger_rate_below: 0.001
    - shadow_test_required: true
  investigate:
    - production_data_days_below: 60
    - missing_shadow_test: true
    - conflicting_metrics: true
```

### 📋 Passo 2: Priorize por Impacto e Risco

Monte uma lista que comece por mudanças de baixo risco. O primeiro componente removido ensina o time a usar o processo. Não escolha um componente emocionalmente carregado como primeira prova.

| Prioridade | Critério | Exemplo | Por que vem nessa ordem |
|------------|----------|---------|--------------------------|
| 1 | Baixo risco, ROI 0x, zero triggers | Budget Guard | Ensina o processo com risco mínimo |
| 2 | Baixo a médio risco, alto custo, redundância clara | Priority Extractor | Economia visível sem tocar invariantes |
| 3 | Médio risco, custo alto, shadow test positivo | Context Loader | Requer cuidado, mas ganho é grande |
| 4 | Dados insuficientes | Format Validator | Não mexer antes de investigar |
| 5 | Invariantes | Evaluator, Safety, Compliance | Não remover, só otimizar internamente |

### 📋 Passo 3: Use a Matriz de Risco

| Impacto se quebrar | Probabilidade baixa | Probabilidade média | Probabilidade alta |
|--------------------|----------------------|---------------------|--------------------|
| Baixo | Canary normal | Canary com alerta extra | Simplificar antes de remover |
| Médio | Shadow test 14 dias | Shadow test 30 dias | Investigar mais um trimestre |
| Alto | Aprovação de arquitetura | Não remover sem prova forte | KEEP |
| Crítico | KEEP ou refatorar sem mudar contrato | KEEP | KEEP |

### 📋 Passo 4: Planeje o Ritmo Trimestral

O módulo conceitual define o ritmo trimestral Review, Implement, Observe. Este playbook transforma isso em agenda operacional.

| Semana | Atividade | Saída |
|--------|-----------|-------|
| 1 | Review de métricas e scorecard | Lista de candidatos |
| 2 | Shadow tests e análise de risco | Evidência complementar |
| 3 | Decisão de roadmap | Roadmap aprovado |
| 4 | Implementação da primeira wave | Feature flag em staging |
| 5 | Canary 5% e 25% | Go ou pause |
| 6 | Canary 100% | Componente fora do caminho principal |
| 7 e 8 | Observação pós-remoção | 14 dias de estabilidade |
| 9 | Arquivamento e ADR | Decisão documentada |
| 10 | Próxima wave se a anterior estabilizou | Novo candidato |
| 11 | Revisão de custo e latência | Comparativo antes e depois |
| 12 | Retro e comunicação | Aprendizados para o próximo trimestre |

### 📋 Passo 5: Aplique One In One Out

O princípio é simples: para cada componente novo que entra no harness, pelo menos um componente existente deve ser simplificado, consolidado ou removido, salvo quando o novo componente cobre invariante regulatório ou safety crítica.

```yaml
harness_governance:
  principle: one_in_one_out
  rule: "Toda proposta de novo componente deve indicar o componente existente que será removido, simplificado ou consolidado."
  exceptions:
    - safety_invariant
    - compliance_requirement
    - state_persistence_requirement
    - evaluator_quality_gate
  review_questions:
    - "Qual fraqueza real do modelo este componente cobre?"
    - "Como saberemos que ele pode sair no futuro?"
    - "Qual métrica provará valor em 90 dias?"
    - "Qual componente existente perde responsabilidade com esta entrada?"
```

### 📋 Passo 6: Escreva o Roadmap de Evolução

| Ordem | Componente | Ação | Risco | Janela | Gate de avanço | Rollback |
|-------|------------|------|-------|--------|----------------|----------|
| 1 | Budget Guard | REMOVE | Baixo | Semanas 4 a 8 | Zero regressões em 14 dias | Flag `remove_budget_guard=false` |
| 2 | Format Validator | SIMPLIFY | Baixo | Semanas 9 a 10 | Shadow test concluido | Flag `format_validator_mode=strict` |
| 3 | Context Loader | SIMPLIFY | Médio | Próximo trimestre | Accuracy delta menor que 1% | Flag `context_loader_mode=full` |
| 4 | Priority Extractor | INVESTIGATE | Médio | Próximo trimestre | Coletar metricas de redundancia | Sem alteração em prod |

### 📋 Passo 7: Prepare Comunicação para Stakeholders

Não comunique como "vamos deletar código". Comunique como redução controlada de risco operacional e custo. Produto quer saber impacto em cliente. Suporte quer saber se tickets aumentam. Engenharia quer saber rollback. Liderança quer saber ROI.

```markdown
# Comunicação de Harness Evolution: Budget Guard

## Resumo
Vamos remover o Budget Guard do caminho principal do KODA usando feature flag e canary deploy. O componente teve zero triggers reais em 180 dias e ROI 0x. A janela de contexto atual do modelo cobre o limite que ele protegia.

## Por que agora
- Zero prevenções reais em 180 dias.
- Shadow test de 30 dias não mostrou diferença entre com e sem o componente.
- Custo operacional estimado: R$ 300 por mês.
- Remoção reduz complexidade do pipeline sem tocar Safety, Compliance, State Persistence ou Evaluator.

## Como será feito
- Staging com shadow test por 2 dias.
- Canary 5% por 24 horas.
- Canary 25% por 24 horas.
- Canary 100% com observação ativa por 14 dias.

## Como vamos saber se deu certo
- Nenhum aumento em incomplete_responses.
- Nenhum aumento em token_budget_exceeded.
- Latência média igual ou menor que baseline.
- Zero incidentes P0 ou P1 atribuídos à remoção.

## Rollback
A feature flag `remove_budget_guard` volta para `false`. Tempo esperado de rollback: menos de 15 minutos.

## O que não muda
- Evaluator continua obrigatório.
- State Persistence continua obrigatório.
- Safety e Compliance continuam obrigatórios.
- Logs de auditoria continuam ativos.
```

### 📋 Checklist Operacional de Planejamento

- [ ] 1. Cada componente tem classe KEEP, SIMPLIFY, REMOVE ou INVESTIGATE.
- [ ] 2. Toda classificação tem evidência vinculada.
- [ ] 3. Componentes invariantes foram travados como KEEP.
- [ ] 4. Roadmap começa por baixo risco.
- [ ] 5. Nenhuma wave remove mais de um componente principal.
- [ ] 6. Cada mudança tem feature flag própria.
- [ ] 7. Cada mudança tem rollback explícito.
- [ ] 8. Cada mudança tem métrica de sucesso antes de iniciar.
- [ ] 9. Cada mudança tem métrica de parada antes de iniciar.
- [ ] 10. Canary 5%, 25% e 100% está no plano.
- [ ] 11. Shadow test está planejado para mudanças de médio ou alto risco.
- [ ] 12. Arquivamento está incluído no plano, não tratado como limpeza posterior.
- [ ] 13. ADR está incluído como entrega obrigatória.
- [ ] 14. Stakeholders receberam comunicação antes de produção.
- [ ] 15. Suporte sabe quais sintomas observar.
- [ ] 16. Produto sabe que não haverá mudança visível esperada.
- [ ] 17. Liderança sabe o ROI esperado.
- [ ] 18. Engenharia sabe quem pode acionar rollback.
- [ ] 19. Agenda trimestral está registrada.
- [ ] 20. One In One Out foi aplicado ao roadmap.

---

## 🔧 Fase 3: Execução

Execução é onde disciplina vale mais que coragem. Você vai mudar uma coisa por vez, atrás de feature flag, com shadow test quando necessário, canary progressivo e rollback simples.

### 🔧 Regra Central: Um Componente por Vez

Se você remove Budget Guard e simplifica Context Loader no mesmo deploy, qualquer regressão vira investigação confusa. O playbook não permite isso. Uma mudança principal por wave.

### 🔧 Passo 1: Crie a Feature Flag

```yaml
feature_flags:
  harness_evolution:
    remove_budget_guard:
      enabled: false
      description: "Remove Budget Guard from the main KODA pipeline."
      owner: "conversational-core"
      created_at: "2025-11-01"
      rollback_value: false
      rollout:
        mode: percentage
        percentage: 0
      guardrails:
        max_incomplete_response_rate_delta: 0.002
        max_token_budget_exceeded_delta: 0.0005
        max_latency_p95_delta_ms: 50
      audit:
        decision_doc: "docs/decisions/adr-remove-budget-guard.md"
        dashboard: "dashboards/harness/budget-guard-removal"
```

### 🔧 Passo 2: Use a Flag no Pipeline

```python
def run_koda_pipeline(turn, config, metrics):
    state = load_state(turn.customer_id)

    if not config.feature_flags.harness_evolution.remove_budget_guard.enabled:
        budget_result = run_budget_guard(turn, state)
        metrics.increment("budget_guard.executed")
        if budget_result.blocked:
            metrics.increment("budget_guard.blocked")
            return budget_result.response
    else:
        metrics.increment("budget_guard.skipped_by_flag")

    draft = run_generator(turn, state)
    verdict = run_evaluator(draft, state)

    if verdict.approved:
        return draft.response

    return run_retry_or_escalation(turn, draft, verdict, state)
```

### 🔧 Passo 3: Configure Shadow Test

Shadow test roda a versão sem componente em paralelo, sem afetar cliente. Ele responde à pergunta mais importante: o que teria acontecido se o componente não existisse?

```yaml
shadow_tests:
  budget_guard_removal:
    enabled: true
    component: "BudgetGuard"
    traffic_sample_percentage: 50
    duration_days: 14
    production_effect: "none"
    compare:
      baseline_path: "pipeline.with_budget_guard"
      candidate_path: "pipeline.without_budget_guard"
    metrics:
      - name: "token_budget_exceeded"
        allowed_delta: 0.0005
      - name: "incomplete_response_rate"
        allowed_delta: 0.002
      - name: "customer_satisfaction_proxy"
        allowed_delta: -0.01
      - name: "latency_p95_ms"
        expected_direction: "down"
    decision_rule:
      promote_if:
        - "no_p0_or_p1_incidents"
        - "all_allowed_deltas_respected"
        - "manual_review_accepts_sample_of_100_traces"
```

### 🔧 Passo 4: Rode Testes de Regressão Antes do Canary

```bash
npm run lint
npm run test:unit
```

Além dos scripts do repositório, rode uma bateria específica do componente. Para Budget Guard, a bateria foca conversas longas, respostas incompletas e limites de contexto.

```json
{
  "regression_battery": {
    "component": "BudgetGuard",
    "cases": [
      {
        "name": "conversa longa com 50000 tokens",
        "expected": "resposta completa sem truncamento"
      },
      {
        "name": "cliente muda pedido após histórico longo",
        "expected": "KODA considera a mudança mais recente"
      },
      {
        "name": "catálogo extenso anexado ao contexto",
        "expected": "KODA responde sem exceder budget do modelo atual"
      },
      {
        "name": "falha simulada de limite de contexto",
        "expected": "alerta agregado dispara sem Budget Guard no caminho principal"
      }
    ]
  }
}
```

### 🔧 Passo 5: Faça Canary Deploy em 5%, 25% e 100%

| Estágio | Percentual | Duração mínima | O que observar | Decisão |
|---------|------------|----------------|----------------|---------|
| Staging | 100% interno | 2 dias | Shadow diff e testes manuais | Só avança se limpo |
| Canary 1 | 5% produção | 24 horas | P0, P1, incomplete responses, latency p95 | Avança ou rollback |
| Canary 2 | 25% produção | 24 horas | Mesmas métricas e tickets de suporte | Avança ou rollback |
| Canary 3 | 100% produção | 14 dias | Estabilidade, custo, satisfação, traces | Arquiva e documenta |

```yaml
rollout_steps:
  - name: staging_shadow
    remove_budget_guard: true
    traffic_percentage: 100
    production_impact: false
    minimum_duration_hours: 48
  - name: production_canary_5
    remove_budget_guard: true
    traffic_percentage: 5
    minimum_duration_hours: 24
  - name: production_canary_25
    remove_budget_guard: true
    traffic_percentage: 25
    minimum_duration_hours: 24
  - name: production_full
    remove_budget_guard: true
    traffic_percentage: 100
    observation_period_days: 14
```

### 🔧 Passo 6: Siga a Abordagem por Waves

A sequência segura é baixo risco, depois médio risco, depois alto risco. Alto risco raramente significa remoção total. Normalmente significa simplificação interna sem mudar contrato externo.

| Wave | Tipo | Exemplos KODA | Critério para entrar | Critério para sair |
|------|------|---------------|----------------------|--------------------|
| Wave 1 | Baixo risco | Budget Guard | Zero triggers, ROI 0x, shadow limpo | 14 dias sem regressão |
| Wave 2 | Médio risco | Priority Extractor | Redundância alta, falso positivo alto | Falsos positivos caem sem queda de accuracy |
| Wave 3 | Médio risco alto | Context Loader | Shadow test positivo, custo alto | Accuracy delta menor que 1% |
| Wave 4 | Alto risco | Format Validator em domínio regulado | Prova forte e rollback rápido | Aprovação de arquitetura |

### 🔧 Passo 7: Arquive Código, Não Apague Memória

Depois de 14 dias estáveis, o componente pode sair do caminho principal e ser arquivado. Arquivo não é cemitério. É memória arquitetural.

```text
archive/
└── components/
    └── budget-guard-v1/
        ├── README.md
        ├── src/
        │   ├── budget_guard.py
        │   └── budget_guard_config.py
        ├── metrics/
        │   ├── diagnostic-180-days.json
        │   ├── shadow-test-30-days.json
        │   └── post-removal-14-days.json
        ├── decisions/
        │   └── adr-remove-budget-guard.md
        └── tests/
            └── test_budget_guard_archived.py
```

### 🔧 README de Archive

```markdown
# Budget Guard v1 Archive

## O que era
Budget Guard era um componente do harness KODA que monitorava consumo de tokens por turno e bloqueava ou truncava conversas próximas do limite de contexto.

## Por que existiu
Ele foi criado quando o modelo principal tinha janela de 32K tokens. Naquele período, conversas longas podiam exceder o limite e gerar respostas incompletas.

## Por que foi removido
O modelo atual opera com janela de 200K tokens. Conversas típicas do KODA ficam abaixo de 50K tokens. O componente teve zero triggers reais em 180 dias e ROI 0x.

## Evidência usada
- Zero triggers reais em 180 dias.
- Shadow test de 30 dias sem diferença entre com e sem Budget Guard.
- Canary 5%, 25% e 100% sem regressões.
- Observação pós-remoção de 14 dias sem incidentes P0 ou P1.

## Como reativar a ideia
Se um modelo futuro tiver janela menor ou se KODA passar a processar conversas muito maiores, reavalie os arquivos em `src/` e escreva novo ADR. Não restaure automaticamente este componente sem novo diagnóstico.

## Lições aprendidas
Componentes baseados em limites de modelo devem carregar uma métrica de expiração. Quando o limite muda, o componente precisa ser reavaliado no próximo ciclo trimestral.
```

### 🔧 Checklist Operacional de Execução

- [ ] 1. Feature flag existe e começa desligada.
- [ ] 2. Flag tem owner e rollback value.
- [ ] 3. Pipeline registra quando componente roda e quando é pulado.
- [ ] 4. Shadow test foi configurado antes do canary.
- [ ] 5. Shadow test não afeta resposta do cliente.
- [ ] 6. Testes de regressão foram executados antes de produção.
- [ ] 7. Canary começa em 5%, não em 50%.
- [ ] 8. Canary 5% roda por pelo menos 24 horas.
- [ ] 9. Canary 25% roda por pelo menos 24 horas.
- [ ] 10. Canary 100% só começa depois de gates limpos.
- [ ] 11. Dashboard fica aberto durante cada expansão.
- [ ] 12. Rollback foi testado em staging.
- [ ] 13. Uma pessoa tem autoridade clara para pausar rollout.
- [ ] 14. Suporte sabe como reportar sintomas.
- [ ] 15. Produto sabe que mudança não deve alterar UX.
- [ ] 16. Logs de auditoria incluem flag state.
- [ ] 17. Código removido só é arquivado após período de observação.
- [ ] 18. Archive inclui README, métricas e ADR.
- [ ] 19. Nenhuma segunda remoção começou antes da primeira estabilizar.
- [ ] 20. Resultados foram adicionados ao relatório de validação.

---

## ✅ Fase 4: Validação

Validação prova que a mudança funcionou. Sem validação, remoção é só fé com deploy. Você vai comparar antes e depois, observar por 14 dias, manter rollback pronto e documentar a decisão.

### ✅ Passo 1: Configure Dashboard de Monitoramento

```yaml
dashboard:
  name: "Harness Evolution: Budget Guard Removal"
  refresh_interval_seconds: 60
  panels:
    - title: "Incomplete Response Rate"
      query: "rate(koda_incomplete_responses[15m])"
      compare_to: "baseline_14_days_before_removal"
    - title: "Token Budget Exceeded"
      query: "rate(koda_token_budget_exceeded[15m])"
      compare_to: "baseline_14_days_before_removal"
    - title: "Latency p95"
      query: "histogram_quantile(0.95, koda_turn_latency_ms)"
      compare_to: "baseline_14_days_before_removal"
    - title: "Evaluator Rejection Rate"
      query: "rate(koda_evaluator_rejections[15m])"
      compare_to: "baseline_14_days_before_removal"
    - title: "Support Ticket Mentions"
      query: "count_support_tickets(labels=['incomplete_response','forgot_context'])"
      compare_to: "baseline_14_days_before_removal"
    - title: "Flag State"
      query: "feature_flag_percentage(remove_budget_guard)"
      compare_to: "expected_rollout_schedule"
```

### ✅ Passo 2: Configure Alertas com Thresholds

```yaml
alerts:
  - name: "BudgetGuardRemovalIncompleteResponses"
    severity: "page"
    condition: "incomplete_response_rate > baseline + 0.002 for 10m"
    action: "rollback remove_budget_guard to false"
  - name: "BudgetGuardRemovalTokenBudgetExceeded"
    severity: "page"
    condition: "token_budget_exceeded_rate > baseline + 0.0005 for 10m"
    action: "rollback remove_budget_guard to false"
  - name: "BudgetGuardRemovalLatencyRegression"
    severity: "ticket"
    condition: "latency_p95_ms > baseline + 50 for 30m"
    action: "pause rollout and inspect traces"
  - name: "BudgetGuardRemovalEvaluatorSpike"
    severity: "ticket"
    condition: "evaluator_rejection_rate > baseline * 1.10 for 30m"
    action: "sample rejected traces"
  - name: "BudgetGuardRemovalSupportSpike"
    severity: "page"
    condition: "support_tickets_incomplete_response > baseline * 1.25 for 1h"
    action: "pause rollout and notify support owner"
```

### ✅ Ferramentas e Automação

A validação fica mais confiável quando os comandos são repetíveis. Esta seção mostra uma automação mínima para dashboard, alertas e cálculo de ROI. Use como referência para criar scripts reais no repositório do KODA.

#### ✅ Criar Dashboard por Comando

```bash
koda dashboards create harness-budget-guard-removal \
  --folder harness-evolution \
  --owner conversational-core \
  --source dashboards/templates/harness-removal.json
```

Depois configure as variáveis do dashboard.

```bash
koda dashboards set-var harness-budget-guard-removal component BudgetGuard
koda dashboards set-var harness-budget-guard-removal flag harness_evolution.remove_budget_guard
koda dashboards set-var harness-budget-guard-removal baseline_window 14d
koda dashboards set-var harness-budget-guard-removal observation_window 14d
```

Painéis mínimos:

| Painel | Query | Por que existe |
|--------|-------|----------------|
| Flag rollout | `feature_flag_percentage(remove_budget_guard)` | Confirma exposição real |
| Incomplete responses | `rate(koda_incomplete_responses[15m])` | Sintoma principal de regressão |
| Token budget exceeded | `rate(koda_token_budget_exceeded[15m])` | Sintoma específico do componente removido |
| Latência p95 | `histogram_quantile(0.95, koda_turn_latency_ms)` | Confirma benefício esperado |
| Support mentions | `count_support_tickets(labels=['incomplete_response'])` | Captura sinal humano |
| Evaluator rejection | `rate(koda_evaluator_rejections[15m])` | Detecta efeito indireto |

#### ✅ Criar Alertas por YAML

```yaml
alert_group: harness_evolution_budget_guard
owner: conversational-core
route: koda-platform-oncall
alerts:
  - name: incomplete_response_regression
    query: "rate(koda_incomplete_responses[15m])"
    baseline: "avg_over_time(koda_incomplete_responses[14d])"
    condition: "current > baseline + 0.002"
    for: "10m"
    severity: page
  - name: token_budget_exceeded_regression
    query: "rate(koda_token_budget_exceeded[15m])"
    baseline: "0"
    condition: "current > 0.0005"
    for: "10m"
    severity: page
  - name: support_ticket_spike
    query: "support_ticket_rate(incomplete_response, 1h)"
    baseline: "support_ticket_rate(incomplete_response, 14d)"
    condition: "current > baseline * 1.25"
    for: "1h"
    severity: ticket
```

Aplicação:

```bash
koda alerts apply alerts/harness-evolution-budget-guard.yaml
koda alerts test incomplete_response_regression --sample-window 2026-04-01T10:00:00Z/2026-04-01T11:00:00Z
```

#### ✅ Script de ROI para Revisão Trimestral

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class HarnessComponentMetrics:
    name: str
    real_preventions_90d: int
    average_error_cost_brl: float
    token_cost_brl_90d: float
    maintenance_hours_90d: float
    engineering_hour_cost_brl: float
    latency_cost_brl_90d: float
    debug_cost_brl_90d: float

    @property
    def protected_value(self) -> float:
        return self.real_preventions_90d * self.average_error_cost_brl

    @property
    def operational_cost(self) -> float:
        return (
            self.token_cost_brl_90d
            + self.maintenance_hours_90d * self.engineering_hour_cost_brl
            + self.latency_cost_brl_90d
            + self.debug_cost_brl_90d
        )

    @property
    def roi(self) -> float:
        if self.operational_cost == 0:
            return float("inf")
        return self.protected_value / self.operational_cost

components = [
    HarnessComponentMetrics("BudgetGuard", 0, 50, 600, 3, 100, 0, 0),
    HarnessComponentMetrics("ContextLoader", 59, 50, 810, 3, 150, 200, 0),
]

for component in components:
    print(component.name, round(component.roi, 2), component.operational_cost)
```

Saída esperada para revisão:

```text
BudgetGuard 0.0 900
ContextLoader 2.02 1460
```

O exemplo preserva o ROI 2.0x do Context Loader e o ROI 0x do Budget Guard. O importante é manter a mesma janela para todos os componentes durante uma revisão real.

#### ✅ Automação de Comparativo Antes e Depois

```bash
koda harness compare \
  --component BudgetGuard \
  --before 2026-04-01/2026-04-14 \
  --after 2026-04-15/2026-04-29 \
  --metrics incomplete_response_rate,token_budget_exceeded,latency_p95_ms,csat_proxy \
  --output docs/harness-evolution/2026-q2-budget-guard-validation.md
```

Esse comando não substitui julgamento humano. Ele só evita copiar número manualmente e errar a baseline.

### ✅ Passo 3: Execute a Bateria de Regressão

| Caso | Entrada | Saída esperada | Métrica protegida |
|------|---------|----------------|-------------------|
| Conversa longa padrão | Histórico de 50K tokens | Resposta completa | incomplete_response_rate |
| Conversa longa extrema | Histórico de 140K tokens | Alerta agregado, sem resposta truncada | token_budget_exceeded |
| Mudança tardia de pedido | Cliente altera produto no fim | KODA usa informação recente | context_recall |
| Pedido com alergia | Cliente tem alergia registrada | Evaluator bloqueia produto inseguro | safety_rejection |
| Catálogo grande | Lista extensa de produtos | Resposta seleciona opções relevantes | quality_score |
| Falha simulada de API | Modelo retorna erro temporário | Retry simples ou escalação | availability_fallback |

```json
{
  "post_removal_regression_result": {
    "component_removed": "BudgetGuard",
    "executed_at": "2026-04-15T10:00:00Z",
    "cases_total": 6,
    "cases_passed": 6,
    "cases_failed": 0,
    "manual_trace_review": {
      "sample_size": 100,
      "accepted": 100,
      "rejected": 0
    },
    "decision": "continue_observation"
  }
}
```

### ✅ Passo 4: Observe por 14 Dias

O período de 14 dias é parte da mudança, não burocracia. Muitos problemas de harness aparecem apenas em cauda longa de conversas. Dois dias sem incidente não bastam.

| Dia | Atividade | Pergunta |
|-----|-----------|----------|
| 1 | Confirmar baseline e alertas ativos | As métricas iniciais estão dentro do esperado? |
| 2 | Revisar traces amostrados | Há sinal fraco de resposta incompleta? |
| 3 | Revisar traces amostrados | Há sinal fraco de resposta incompleta? |
| 4 | Checar tickets de suporte | Clientes estão reclamando de esquecimento ou truncamento? |
| 5 | Checar tickets de suporte | Clientes estão reclamando de esquecimento ou truncamento? |
| 6 | Comparar custo e latência | A economia esperada apareceu? |
| 7 | Comparar custo e latência | A economia esperada apareceu? |
| 8 | Revisar rejeições do Evaluator | Outro componente absorveu carga inesperada? |
| 9 | Revisar rejeições do Evaluator | Outro componente absorveu carga inesperada? |
| 10 | Auditar conversas longas | A cauda longa continua saudável? |
| 11 | Auditar conversas longas | A cauda longa continua saudável? |
| 12 | Preparar relatório final | Há evidência suficiente para encerrar? |
| 13 | Preparar relatório final | Há evidência suficiente para encerrar? |
| 14 | Decisão final e arquivamento | Podemos declarar a remoção estável? |

### ✅ Passo 5: Compare Antes e Depois

| Métrica | 14 dias antes | 14 dias depois | Delta | Decisão |
|---------|---------------|----------------|-------|---------|
| Latência p95 | 4100ms | 3850ms | -250ms | Melhorou |
| Tokens por turno | 3200 | 3000 | -200 | Melhorou |
| Incomplete responses | 0.12% | 0.12% | 0.00% | Estável |
| Token budget exceeded | 0.00% | 0.00% | 0.00% | Estável |
| Evaluator rejection rate | 6.8% | 6.9% | +0.1% | Dentro do threshold |
| CSAT proxy | 88% | 88% | 0% | Estável |
| Incidentes P0/P1 | 0 | 0 | 0 | Aprovado |
| Custo mensal estimado | R$ 300 | R$ 0 | -R$ 300 | Melhorou |

### ✅ Passo 6: Prepare Rollback Mesmo Quando Tudo Vai Bem

```bash
# Rollback operacional para Budget Guard
# Objetivo: reativar o componente no caminho principal.

feature-flags set harness_evolution.remove_budget_guard.enabled false
feature-flags set harness_evolution.remove_budget_guard.rollout.percentage 0

# Verificar estado da flag
feature-flags get harness_evolution.remove_budget_guard

# Confirmar que o pipeline voltou a executar o componente
metrics query 'rate(budget_guard.executed[5m])'
metrics query 'rate(budget_guard.skipped_by_flag[5m])'
```

### ✅ Passo 7: Escreva o ADR de Remoção

```markdown
# ADR: Remover Budget Guard do Harness KODA

## Status
Aceito

## Data
2026-04-15

## Contexto
Budget Guard foi criado quando o modelo principal tinha janela de 32K tokens. Ele protegia o KODA contra respostas incompletas causadas por estouro de contexto.

## Evidência
- Zero triggers reais em 180 dias.
- ROI 0x no diagnóstico trimestral.
- Shadow test de 30 dias sem diferença observável entre com e sem o componente.
- Canary 5%, 25% e 100% concluído sem incidente.
- Observação de 14 dias sem aumento em incomplete_response_rate ou token_budget_exceeded.

## Decisão
Remover Budget Guard do caminho principal e arquivar o código em `archive/components/budget-guard-v1/`.

## Consequências Positivas
- Redução de custo operacional mensal.
- Redução de complexidade no pipeline.
- Menos um componente para novos devs entenderem.
- Governança de Harness Evolution validada em produção.

## Consequências Negativas
- Se um modelo futuro tiver janela menor, será necessário reavaliar proteção de budget.
- Alertas agregados passam a ser a primeira linha de detecção para contexto extremo.

## Rollback
Reativar `harness_evolution.remove_budget_guard.enabled=false`. O código arquivado pode ser consultado, mas restauração permanente exige novo diagnóstico e novo ADR.

## Links
- Diagnostic Report: `docs/harness-evolution/2026-q2-budget-guard-diagnostic.md`
- Validation Report: `docs/harness-evolution/2026-q2-budget-guard-validation.md`
- Archive: `archive/components/budget-guard-v1/`
```

### ✅ Passo 8: Faça um Post-Mortem de Celebração

Nem todo post-mortem precisa nascer de incidente. Uma remoção bem-sucedida também merece registro. Isso ensina o time que reduzir complexidade é trabalho de produto, não limpeza invisível.

```markdown
# Post-Mortem Positivo: Remoção do Budget Guard

## O que aconteceu
Removemos Budget Guard do caminho principal do KODA após diagnóstico, shadow test, canary deploy e 14 dias de observação.

## O que melhorou
- Menos um componente no pipeline.
- Custo mensal reduzido em R$ 300.
- Latência p95 reduziu 250ms no período comparado.
- Nenhum aumento de incidentes, tickets ou respostas incompletas.

## O que aprendemos
- Componentes ligados a limites de modelo precisam ser revistos quando o modelo muda.
- Feature flag e canary tornaram a remoção tranquila.
- O primeiro alvo de Harness Evolution deve ser baixo risco para criar confiança no processo.

## Quem ajudou
- Engenharia mediu e executou.
- Produto validou risco para cliente.
- Suporte monitorou sintomas reais.
- Fernando segurou a ansiedade do time quando a vontade era remover mais coisas de uma vez.

## Próximo passo
Aplicar o mesmo processo ao Priority Extractor, sem iniciar antes de fechar o relatório final desta remoção.
```

### ✅ Checklist Operacional de Validação

- [ ] 1. Dashboard específico foi criado.
- [ ] 2. Alertas têm thresholds numéricos.
- [ ] 3. Thresholds foram comparados com baseline de 14 dias antes.
- [ ] 4. Bateria de regressão foi executada.
- [ ] 5. Amostra manual de traces foi revisada.
- [ ] 6. Canary 100% completou 14 dias.
- [ ] 7. Nenhum incidente P0 ou P1 foi atribuído à remoção.
- [ ] 8. Tickets de suporte foram comparados com baseline.
- [ ] 9. CSAT ou proxy de satisfação foi comparado.
- [ ] 10. Latência foi comparada antes e depois.
- [ ] 11. Tokens foram comparados antes e depois.
- [ ] 12. Rollback continuou possível durante observação.
- [ ] 13. ADR foi escrito com evidência concreta.
- [ ] 14. Archive foi criado com README completo.
- [ ] 15. Documentação de arquitetura foi atualizada.
- [ ] 16. Post-mortem positivo foi publicado.
- [ ] 17. Próxima wave só foi liberada após fechamento formal.
- [ ] 18. Aprendizados foram adicionados ao processo trimestral.

---

## 🚀 Aplicação KODA: Walkthrough Completo de Remoção do Budget Guard

Esta seção acompanha a remoção do Budget Guard como se você estivesse executando a wave dentro do time KODA. O objetivo é tirar a decisão do plano abstrato e mostrar o trabalho real: query, conversa, scorecard, comunicação, flag, canary, validação e arquivo.

O componente escolhido é deliberadamente simples. Budget Guard teve zero triggers reais em 180 dias, ROI 0x e uma responsabilidade ligada a um limite de modelo que mudou de 32K para 200K tokens. Ele é o primeiro alvo correto porque permite treinar o processo sem tocar nos invariantes.

### 🩺 Diagnóstico KODA Detalhado

Você começa a manhã com duas abas abertas. A primeira é o dashboard de métricas do KODA. A segunda é o ADR antigo que criou o Budget Guard. Antes de falar com alguém, você quer saber se a história que o time conta sobre o componente ainda aparece nos dados.

A pergunta inicial é direta: nos últimos 180 dias, quantas vezes o Budget Guard impediu uma resposta incompleta que chegaria ao cliente?

```sql
SELECT
  component_name,
  COUNT(*) AS executions,
  SUM(CASE WHEN event_type = 'blocked' THEN 1 ELSE 0 END) AS blocks,
  SUM(CASE WHEN event_type = 'real_prevention' THEN 1 ELSE 0 END) AS real_preventions,
  SUM(CASE WHEN event_type = 'false_positive' THEN 1 ELSE 0 END) AS false_positives,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) AS p95_latency_ms
FROM harness_component_events
WHERE component_name = 'BudgetGuard'
  AND created_at >= DATE '2025-11-01'
  AND created_at < DATE '2026-05-01'
GROUP BY component_name;
```

O resultado não deixa muito espaço para interpretação.

| Campo | Valor retornado |
|-------|-----------------|
| component_name | BudgetGuard |
| executions | 8.702.114 |
| blocks | 0 |
| real_preventions | 0 |
| false_positives | 0 |
| p95_latency_ms | 38ms |

Você roda a segunda query para entender se o componente ao menos estava perto de disparar. Um componente pode não bloquear, mas ainda operar perto do threshold.

```sql
SELECT
  DATE_TRUNC('week', created_at) AS week,
  MAX(context_tokens) AS max_context_tokens,
  AVG(context_tokens) AS avg_context_tokens,
  MAX(context_window_tokens) AS model_window,
  MAX(context_tokens * 1.0 / context_window_tokens) AS max_window_ratio
FROM koda_turn_metrics
WHERE created_at >= DATE '2025-11-01'
  AND created_at < DATE '2026-05-01'
GROUP BY 1
ORDER BY 1;
```

A tela mostra que a conversa mais longa chegou a 72K tokens. O limite operacional do Budget Guard era 80% da janela de 200K, ou 160K tokens. A maior conversa real ficou em 36% da janela.

| Semana | Max tokens | Média tokens | Janela do modelo | Maior uso da janela |
|--------|------------|--------------|------------------|---------------------|
| 2025-11-03 | 51.204 | 8.912 | 200.000 | 25.6% |
| 2025-12-01 | 58.990 | 9.104 | 200.000 | 29.5% |
| 2026-01-05 | 61.331 | 10.441 | 200.000 | 30.7% |
| 2026-02-02 | 64.775 | 11.028 | 200.000 | 32.4% |
| 2026-03-02 | 68.112 | 10.883 | 200.000 | 34.1% |
| 2026-04-06 | 72.004 | 12.017 | 200.000 | 36.0% |

A terceira query mede custo. O Budget Guard é barato comparado ao Context Loader, mas custo pequeno ainda é custo quando o valor é zero.

```sql
SELECT
  SUM(extra_prompt_tokens) AS monthly_tokens,
  SUM(extra_prompt_tokens) * 0.00015 AS estimated_brl,
  SUM(latency_ms) / 1000.0 / 3600.0 AS latency_hours,
  COUNT(DISTINCT trace_id) AS traces_touched
FROM harness_component_costs
WHERE component_name = 'BudgetGuard'
  AND created_at >= DATE '2026-04-01'
  AND created_at < DATE '2026-05-01';
```

| Métrica de custo | Valor de abril |
|------------------|----------------|
| Tokens extras | 1.333.420 |
| Custo estimado de API | R$ 200 |
| Horas acumuladas de latência | 92.4h distribuídas entre turns |
| Custo de manutenção | 1h por mês, R$ 100 estimados |
| Custo total usado no ROI | R$ 300 por mês |

Você então chama Marina, tech lead do Conversational Core, para validar se a métrica está correta. A conversa importa porque dashboard sem contexto pode mentir.

```text
Você: Marina, o dashboard mostra zero blocks do Budget Guard em 180 dias. Isso bate com sua memória?

Marina: Bate. Desde que migramos para janela de 200K, ninguém mencionou Budget Guard em incident review.

Você: Existe algum caminho onde ele bloqueia sem registrar `blocked`?

Marina: Não. O wrapper emite `budget_guard.blocked` antes de retornar resposta. Se não tem evento, não bloqueou.

Você: E alguma proteção indireta? Algo como ajustar prompt, truncar histórico ou reduzir catálogo?

Marina: Não mais. Isso ficou no History Compactor. Budget Guard só compara tokens contra limite e decide se bloqueia.

Você: Então a responsabilidade atual é só detectar limite extremo?

Marina: Exato. E esse limite extremo nunca chegou perto.

Você: Se a gente remover com flag, qual seria o sintoma de regressão?

Marina: `incomplete_response_rate`, `token_budget_exceeded` e tickets de cliente dizendo que KODA cortou resposta no meio.
```

Com isso, você preenche a scorecard ao vivo. Não é uma tabela para parecer técnico. É a decisão se tornando auditável.

| Critério | Evidência | Pontuação |
|----------|-----------|-----------|
| Trigger efetivo | 0 prevenções reais em 180 dias | 20 de 20 |
| ROI | 0x, porque valor protegido foi R$ 0 | 20 de 20 |
| Redundância | Alertas agregados e History Compactor cobrem observação de contexto | 12 de 15 |
| Risco de remoção | Baixo, não toca Safety, Compliance, Evaluator ou State Persistence | 15 de 15 |
| Reversibilidade | Feature flag pode reativar em menos de 15 minutos | 15 de 15 |
| Clareza de owner | Conversational Core assume flag e rollback | 5 de 5 |
| Evidência de modelo | Janela atual 200K, conversas reais abaixo de 72K | 7 de 10 |
| Custo | R$ 300 por mês e uma etapa a mais no pipeline | 5 de 5 |

Score final: 99 de 105, convertido para 94/100. A recomendação é REMOVE.

Você também registra o que não está sendo decidido. Isso evita que uma remoção simples vire precedente perigoso.

| Fora do escopo | Motivo |
|----------------|--------|
| Remover Evaluator | Invariante de qualidade, não relacionado ao limite de contexto |
| Remover State Persistence | Protege memória entre sessões e auditoria |
| Remover Safety checks | Alergia e contraindicação são proteção de cliente |
| Remover History Compactor | Ainda necessário para conversas acima de 2h |
| Alterar prompt do Generator | Não é necessário para Budget Guard |

O diagnóstico termina com uma frase que você escreve no relatório: "Budget Guard protege uma janela de contexto que o KODA não usa mais na prática".

Essa frase é forte porque é específica. Ela não diz que o componente é ruim. Ela diz que a condição que justificava sua existência deixou de aparecer em produção.

### 📋 Planejamento KODA Detalhado

Com a scorecard pronta, você não vai direto para código. Você monta o plano de mudança. O primeiro artefato é uma matriz de risco preenchida com dados do KODA, não com categorias genéricas.

| Risco | Probabilidade | Impacto | Evidência | Mitigação |
|-------|---------------|---------|-----------|-----------|
| Resposta incompleta em conversa longa | Baixa | Médio | Maior conversa real em 36% da janela | Alerta `incomplete_response_rate` |
| Estouro de token budget sem bloqueio | Baixa | Médio | Zero `token_budget_exceeded` em 180 dias | Alerta específico em 10 minutos |
| Regressão em cauda longa | Baixa | Alto | Poucas conversas acima de 60K tokens | Revisão manual de 100 traces longos |
| Falha de rollback | Muito baixa | Alto | Feature flag central já usada em produção | Teste de rollback em staging |
| Confusão do suporte | Média | Baixo | Mudança invisível para cliente | Mensagem prévia no canal de suporte |

A feature flag precisa ser pequena e explícita. Nada de flag ampla como `new_harness_mode`. Uma flag ampla cria medo e rollback confuso.

```yaml
feature_flags:
  harness_evolution:
    remove_budget_guard:
      enabled: false
      owner: conversational-core
      created_for: adr-remove-budget-guard
      description: "Skip BudgetGuard in KODA main pipeline after 180 days with zero triggers."
      rollout:
        strategy: percentage
        percentage: 0
        sticky_key: conversation_id
      rollback:
        safe_value: false
        expected_time_minutes: 15
        owner_on_call: koda-platform-oncall
      success_metrics:
        incomplete_response_rate_delta_max: 0.002
        token_budget_exceeded_rate_delta_max: 0.0005
        latency_p95_delta_max_ms: 50
      stop_metrics:
        p0_or_p1_incident_count_min: 1
        support_ticket_spike_multiplier: 1.25
        evaluator_rejection_spike_multiplier: 1.10
```

Você escreve a comunicação para stakeholders em três versões. A primeira vai para engenharia.

```markdown
# Engenharia: Wave 1 de Harness Evolution

Vamos remover Budget Guard do caminho principal do KODA usando feature flag.

Evidência:
- Zero blocks e zero prevenções reais em 180 dias.
- Maior conversa real usou 36% da janela de contexto atual.
- ROI 0x.
- Rollback por flag em menos de 15 minutos.

Escopo:
- Muda apenas Budget Guard.
- Não altera Evaluator.
- Não altera State Persistence.
- Não altera Safety ou Compliance.
- Não altera prompts do Generator.

Plano:
- Shadow test em staging por 2 dias.
- Canary 5% por 24 horas.
- Canary 25% por 24 horas.
- 100% com observação por 14 dias.
```

A segunda vai para produto.

```markdown
# Produto: Remoção Invisível de Componente Sem Uso

Vamos retirar uma proteção antiga que não disparou nenhuma vez nos últimos 180 dias.

Impacto esperado para cliente:
- Nenhuma mudança de experiência.
- Nenhuma mudança de tom do KODA.
- Nenhuma mudança no fluxo de compra.
- Possível redução pequena de latência.

Como vamos proteger cliente:
- Rollout gradual.
- Monitoramento de resposta incompleta.
- Monitoramento de tickets de suporte.
- Rollback rápido por feature flag.
```

A terceira vai para suporte.

```markdown
# Suporte: Sintomas para Observar na Wave Budget Guard

Durante a próxima wave, avisem no canal `#koda-harness-evolution` se aparecerem tickets com estes sintomas:

- Cliente diz que a resposta veio cortada.
- Cliente diz que KODA parou no meio de uma recomendação.
- Cliente diz que KODA esqueceu parte longa da conversa.
- Conversas acima de 2 horas parecem terminar sem conclusão.

Não esperamos aumento desses casos. O objetivo é apenas ter olhos humanos no período de canary.
```

Fernando revisa e faz uma pergunta que parece simples: "E se der certo rápido?".

A resposta correta é: ainda assim você observa 14 dias. Harness Evolution não recompensa pressa. Recompensa causalidade.

O plano final entra no roadmap trimestral assim:

| Semana | Ação | Owner | Gate |
|--------|------|-------|------|
| 1 | Diagnóstico e scorecard | Você | Recomendação REMOVE aprovada |
| 2 | Feature flag e shadow test | Conversational Core | Shadow diff sem degradação |
| 3 | Canary 5% e 25% | Platform on-call | Alertas limpos |
| 4 | 100% e início da observação | Conversational Core | Sem P0/P1 |
| 5 | Observação dias 1 a 7 | Suporte e Produto | Tickets estáveis |
| 6 | Observação dias 8 a 14 | Engenharia | Métricas estáveis |
| 7 | Archive e ADR | Você | Decisão documentada |

### 🔧 Execução KODA Detalhada

No dia da execução, você começa por staging. O primeiro comando não muda produção. Ele confirma que a flag existe, está desligada e tem owner.

```bash
koda flags get harness_evolution.remove_budget_guard
```

Saída esperada:

```json
{
  "key": "harness_evolution.remove_budget_guard",
  "enabled": false,
  "percentage": 0,
  "owner": "conversational-core",
  "rollback_value": false
}
```

Você ativa shadow test em staging.

```bash
koda shadow-tests start budget_guard_removal --env staging --duration 48h --sample 100
```

Depois roda a bateria de regressão específica.

```bash
npm run lint
npm run test:unit
koda test-harness run --suite long-context --component budget-guard-removal
koda test-harness run --suite incomplete-response --component budget-guard-removal
```

O relatório de staging vem assim:

| Suite | Casos | Passou | Falhou | Observação |
|-------|-------|--------|--------|------------|
| long-context | 24 | 24 | 0 | Maior fixture com 150K tokens respondeu completa |
| incomplete-response | 18 | 18 | 0 | Nenhum truncamento detectado |
| evaluator-safety | 31 | 31 | 0 | Safety inalterado |
| checkout-regression | 22 | 22 | 0 | Fluxo de compra inalterado |

O dashboard de staging mostra duas linhas sobrepostas. A linha azul é baseline com Budget Guard. A linha verde é candidate sem Budget Guard. Elas ficam idênticas em `incomplete_response_rate`. A linha verde fica levemente melhor em latência p95.

```text
┌──────────────────────────────────────────────────────────────┐
│ DASHBOARD: staging budget_guard_removal                       │
├──────────────────────────────┬──────────────┬───────────────┤
│ Métrica                      │ Baseline     │ Candidate     │
├──────────────────────────────┼──────────────┼───────────────┤
│ incomplete_response_rate     │ 0.00%        │ 0.00%         │
│ token_budget_exceeded        │ 0            │ 0             │
│ latency_p95_ms               │ 3910ms       │ 3868ms        │
│ evaluator_rejection_rate     │ 6.8%         │ 6.8%          │
└──────────────────────────────┴──────────────┴───────────────┘
```

No dia 1 de produção, você faz canary 5%.

```bash
koda flags set harness_evolution.remove_budget_guard.enabled true --env production
koda flags set harness_evolution.remove_budget_guard.rollout.percentage 5 --env production
koda flags audit harness_evolution.remove_budget_guard --last 10
```

Você anota o horário exato: 10h05. Isso importa para comparar gráficos.

Às 11h05, a primeira hora está limpa.

| Métrica | Baseline 14 dias | Canary 5% primeira hora | Status |
|---------|------------------|--------------------------|--------|
| incomplete_response_rate | 0.12% | 0.11% | Limpo |
| token_budget_exceeded | 0.00% | 0.00% | Limpo |
| latency_p95_ms | 4100ms | 4058ms | Melhor |
| evaluator_rejection_rate | 6.8% | 6.9% | Dentro do threshold |
| tickets de suporte | 3 por dia | 0 na primeira hora | Limpo |

Às 18h00, você revisa 20 traces longos. Um deles tem 61K tokens e passa sem diferença. Você cola o resumo no canal da wave.

```markdown
Canary 5%: parcial de 8 horas
- 31.204 turns no grupo candidate.
- 0 token_budget_exceeded.
- 0 incidentes.
- p95 44ms melhor que baseline.
- 20 traces longos revisados manualmente.
- Recomendação: manter até completar 24h e avançar para 25% se noite ficar limpa.
```

No dia 2, às 10h10, o canary 5% completou 24 horas.

```bash
koda metrics compare \
  --flag harness_evolution.remove_budget_guard \
  --window 24h \
  --baseline 14d
```

A comparação confirma estabilidade.

| Métrica | Baseline | Candidate 5% | Delta | Gate |
|---------|----------|--------------|-------|------|
| incomplete_response_rate | 0.12% | 0.12% | 0.00% | Passou |
| token_budget_exceeded | 0.00% | 0.00% | 0.00% | Passou |
| latency_p95_ms | 4100ms | 4052ms | -48ms | Passou |
| CSAT proxy | 88.0% | 88.1% | +0.1% | Passou |

Você avança para 25%.

```bash
koda flags set harness_evolution.remove_budget_guard.rollout.percentage 25 --env production
```

No dashboard, a descrição visual é simples: nenhuma linha vermelha aparece, a linha de tráfego candidate sobe para 25%, e as métricas protegidas continuam grudadas na baseline.

No dia 3, você encontra um ruído: evaluator rejection rate sobe de 6.8% para 7.1% por 40 minutos. O alerta não dispara porque o threshold é 10%, mas você investiga mesmo assim.

```bash
koda traces sample \
  --where "flag.remove_budget_guard=true" \
  --metric evaluator_rejection_rate \
  --window 1h \
  --limit 25
```

A análise mostra que os rejects vieram de uma promoção vencida no catálogo, não de contexto longo. Você registra como não relacionado.

| Trace | Motivo da rejeição | Relacionado ao Budget Guard |
|-------|--------------------|-----------------------------|
| trc_8112 | Cupom expirado | Não |
| trc_8177 | Estoque divergente | Não |
| trc_8190 | Produto com lactose para cliente intolerante | Não, Safety funcionando |
| trc_8244 | Preço promocional desatualizado | Não |

No dia 4, você avança para 100%.

```bash
koda flags set harness_evolution.remove_budget_guard.rollout.percentage 100 --env production
```

Você não arquiva código nesse momento. O componente está fora do caminho principal, mas a decisão ainda está em observação.

### ✅ Validação KODA Detalhada

A validação começa no primeiro dia de 100%. Você cria três checkpoints formais: Dia 1, Dia 7 e Dia 14.

#### ✅ Dia 1 de Observação

| Métrica | Baseline | Dia 1 | Leitura |
|---------|----------|-------|---------|
| Turns processados | 482.110 | 489.004 | Volume normal |
| incomplete_response_rate | 0.12% | 0.12% | Estável |
| token_budget_exceeded | 0 | 0 | Estável |
| latency_p95_ms | 4100ms | 3854ms | Melhorou 246ms |
| evaluator_rejection_rate | 6.8% | 6.9% | Dentro do threshold |
| tickets com resposta cortada | 3 por dia | 2 | Estável |

Notas do dia 1:

- Nenhum alerta disparou.
- Suporte não reportou novo padrão de reclamação.
- Os 10 maiores traces do dia ficaram abaixo de 74K tokens.
- A flag permaneceu em 100% sem rollback.
- Fernando pediu para não iniciar a próxima wave ainda.

#### ✅ Dia 7 de Observação

No dia 7, você compara uma semana inteira. Esse é o primeiro ponto em que variações diárias param de confundir.

```bash
koda metrics compare \
  --window 7d \
  --before-window 14d \
  --flag harness_evolution.remove_budget_guard
```

| Métrica | Antes | Depois 7 dias | Delta |
|---------|-------|---------------|-------|
| Latência p95 | 4100ms | 3860ms | -240ms |
| Tokens extras do Budget Guard | 1.333.420 por mês estimado | 0 | -100% |
| Incomplete responses | 0.12% | 0.12% | 0.00% |
| Token budget exceeded | 0 | 0 | 0 |
| Tickets relacionados | 21 por semana | 19 por semana | -2 |
| CSAT proxy | 88.0% | 88.0% | 0.0% |

A reunião de checkpoint dura 18 minutos. As notas são objetivas.

```markdown
# Checkpoint Dia 7: Budget Guard Removal

Participantes:
- Você, owner da wave
- Marina, Conversational Core
- Renan, Platform on-call
- Paula, Produto
- Júlia, Suporte

Decisões:
- Manter flag em 100%.
- Não iniciar próxima wave até Dia 14.
- Revisar mais 20 traces acima de 60K tokens.
- Preparar ADR em modo rascunho.

Observações:
- Suporte não percebeu mudança.
- Produto não viu alteração em funil.
- Engenharia confirmou que rollback continua funcional.
```

#### ✅ Dia 14 de Observação

No dia 14, você tem evidência suficiente para encerrar a wave.

| Métrica | 14 dias antes | 14 dias depois | Resultado |
|---------|---------------|----------------|-----------|
| incomplete_response_rate | 0.12% | 0.12% | Estável |
| token_budget_exceeded | 0 | 0 | Estável |
| latency_p95_ms | 4100ms | 3850ms | Melhorou |
| incidents P0/P1 | 0 | 0 | Estável |
| tickets de suporte relacionados | 42 | 39 | Estável |
| CSAT proxy | 88% | 88% | Estável |
| custo mensal do componente | R$ 300 | R$ 0 | Melhorou |

Você escreve o post-mortem positivo com tom direto. A vitória é pequena e real.

```markdown
# Post-Mortem Positivo: Budget Guard Saiu sem Incidente

Resumo:
Removemos Budget Guard do caminho principal do KODA após 180 dias com zero triggers reais.

Resultado:
- 14 dias sem P0 ou P1.
- 0 token_budget_exceeded.
- incomplete_response_rate estável em 0.12%.
- latência p95 reduziu de 4100ms para 3850ms.
- custo mensal estimado reduzido em R$ 300.

Lição principal:
Componentes ligados a limites de modelo precisam ser reavaliados quando o modelo muda.

Próxima ação:
Arquivar Budget Guard e só então preparar investigação do Priority Extractor.
```

O README do arquivo fica completo, não simbólico.

```markdown
# Budget Guard v1

## Resumo
Budget Guard protegia o KODA contra estouro de contexto quando o modelo principal tinha janela de 32K tokens.

## Período ativo
Criado em 2025-10-01.
Removido do caminho principal em 2026-04-15.
Arquivado após observação concluída em 2026-04-29.

## Por que foi seguro remover
- Janela do modelo aumentou para 200K tokens.
- Maior conversa observada em 180 dias ficou em 72K tokens.
- Zero blocks em 180 dias.
- Zero prevenções reais.
- Shadow test e canary não mostraram degradação.

## Como reavaliar no futuro
Se KODA mudar para modelo com janela menor ou passar a anexar catálogos muito maiores, rode novo diagnóstico. Não restaure este componente sem medir Effective Trigger Rate, ROI e regressões.

## Artefatos relacionados
- `metrics/diagnostic-180-days.json`
- `metrics/shadow-test-30-days.json`
- `metrics/post-removal-14-days.json`
- `decisions/adr-remove-budget-guard.md`
```

### 🚀 Exemplo KODA 1: Budget Guard

| Campo | Valor |
|-------|-------|
| Motivo original | Proteger modelo de 32K tokens contra estouro de contexto |
| Evidência atual | 0 triggers em 180 dias |
| Classificação | REMOVE |
| Risco | Baixo |
| Rollback | Feature flag em menos de 15 minutos |
| Resultado | Removido sem regressão |

### 🚀 Exemplo KODA 2: Context Loader

| Campo | Valor |
|-------|-------|
| Motivo original | Modelo esquecia dados críticos depois de 40 minutos |
| Evidência atual | 12 prevenções críticas em 145K turns, 340 falsos positivos |
| Classificação | SIMPLIFY |
| Risco | Médio |
| Plano | Reduzir preload constante e absorver lógica residual no History Compactor |
| Resultado esperado | Menos tokens e latência sem perder recall crítico |

### 🚀 Exemplo KODA 3: Priority Extractor

| Campo | Valor |
|-------|-------|
| Motivo original | Destacar alergias, orçamento e preferências antes do Planner |
| Evidência atual | Alta redundância com Evaluator e Context Loader |
| Classificação | INVESTIGATE |
| Risco | Médio |
| Plano | Coletar métricas de redundância antes de decidir simplificação |
| Resultado esperado | Decidir com dados se a prioridade deve migrar para rubrica do Evaluator |

### 🧬 Context Loader: Sub-Walkthrough de Simplificação em 3 Waves

O Context Loader não é um caso de remoção direta. Ele ainda entregou 12 prevenções críticas e 47 prevenções não críticas em 145K turns. O problema é que o custo ficou desproporcional: 1200 tokens por turno, 450ms de latência e 340 falsos positivos.

A decisão correta é SIMPLIFY. Você reduz uma camada por vez, mede, observa e só então avança.

#### 🧬 Estado Antes da Simplificação

```json
{
  "component": "ContextLoader",
  "version": "1.3",
  "tokens_per_turn": 1200,
  "latency_ms_per_turn": 450,
  "monthly_tokens": 5400000,
  "critical_preventions_90d": 12,
  "non_critical_preventions_90d": 47,
  "false_positives_90d": 340,
  "accuracy_with_loader": "97.2%",
  "accuracy_without_loader_shadow": "96.8%"
}
```

O shadow test sem loader mostrou delta de -0.4%, dentro da margem de erro. Mesmo assim, o time não remove de uma vez porque há casos críticos de alergia e restrição médica.

#### 🧬 Wave 1: Remover Redundância

A primeira wave remove duplicação, não responsabilidade. Dados críticos continuam no system prompt. O que sai é repetição no user message e marcação explícita que o modelo atual já não precisa.

| Antes da Wave 1 | Depois da Wave 1 |
|-----------------|------------------|
| Dados críticos no system prompt e no user message | Dados críticos apenas no system prompt |
| Tags `HIGH_PRIORITY` em alergias e orçamento | Prioridade descrita em linguagem natural |
| System prompt com 2000 tokens | System prompt com 800 tokens |
| Custo: 1200 tokens por turno | Custo: 700 tokens por turno |

```yaml
feature_flags:
  harness_evolution:
    context_loader_wave_1:
      enabled: false
      mode: remove_redundancy
      rollout:
        percentage: 0
      expected_savings:
        tokens_per_turn: 500
        latency_ms: 150
      guardrails:
        critical_constraint_recall_min: 0.995
        allergy_violation_max: 0
        accuracy_delta_max: 0.005
```

Você aplica em 5%, 25% e 100%, mas com janela menor que remoção completa porque a responsabilidade permanece.

| Dia | Percentual | Resultado |
|-----|------------|-----------|
| 1 | 5% | Recall crítico 99.8%, zero incidentes |
| 2 | 25% | Accuracy 97.1%, sem spike de suporte |
| 3 a 7 | 100% | Acurácia manteve 97.1%, zero incidentes |

Economia confirmada: 500 tokens por turno e 150ms por turno.

#### 🧬 Wave 2: Relaxar Constraints Redundantes

A segunda wave é mais delicada. Você aumenta threshold de compressão de histórico de 30 para 90 minutos, remove validação pós-turno de constraints que o Evaluator já cobre, e deixa de carregar `customer_profile` em todo turno.

| Antes da Wave 2 | Depois da Wave 2 |
|-----------------|------------------|
| Compressão após 30 minutos | Compressão após 90 minutos |
| Validação pós-turno no Context Loader | Validação no Evaluator |
| `customer_profile` carregado a cada turno | `customer_profile` carregado no início e em mudança real |
| Custo: 700 tokens por turno | Custo: 300 tokens por turno |

```yaml
shadow_tests:
  context_loader_wave_2:
    enabled: true
    duration_days: 14
    traffic_sample_percentage: 50
    baseline_path: "context_loader.wave_1"
    candidate_path: "context_loader.wave_2"
    metrics:
      - critical_constraint_recall
      - allergy_violation_count
      - budget_preference_recall
      - evaluator_rejection_rate
      - customer_confusion_ticket_rate
    decision_rule:
      promote_if:
        accuracy_delta_abs_max: 0.005
        allergy_violation_count: 0
        p0_or_p1_incidents: 0
```

Resultado do shadow test:

| Métrica | Wave 1 | Wave 2 candidate | Delta |
|---------|--------|------------------|-------|
| Acurácia | 97.1% | 97.0% | -0.1% |
| Recall de alergia | 99.9% | 99.9% | 0.0% |
| Recall de orçamento | 98.4% | 98.3% | -0.1% |
| Falsos positivos | 210 | 121 | -89 |
| Latência adicionada | 300ms | 100ms | -200ms |

A decisão é avançar para 100%, porque o delta não é significativo e os falsos positivos caíram.

#### 🧬 Wave 3: Consolidar no History Compactor

A terceira wave muda a forma arquitetural. O Context Loader deixa de existir como componente independente. A lógica residual vai para o History Compactor, que já decide quando compactar e quando preservar informação crítica.

| Antes da Wave 3 | Depois da Wave 3 |
|-----------------|------------------|
| Context Loader dedicado com 300 tokens por turno | Função residual dentro do History Compactor |
| Um stage a mais no pipeline | Nenhum stage dedicado |
| Owner separado | Owner do History Compactor |
| Latência residual de 100ms | Latência residual 0ms no caminho comum |

```python
class HistoryCompactor:
    def compact_if_needed(self, conversation, customer_profile):
        if conversation.duration_minutes < 90:
            return conversation.recent_context()

        compacted_history = self.summarize_old_segments(conversation)
        critical_facts = self.extract_critical_facts(customer_profile)

        return {
            "recent_context": conversation.last_messages(limit=12),
            "compacted_history": compacted_history,
            "critical_facts": critical_facts,
        }
```

A validação da Wave 3 compara pipeline, não só métrica isolada.

| Métrica | Antes v1.3 | Depois v2.0 | Delta |
|---------|------------|-------------|-------|
| Tokens por turno | 1200 | 0 dedicado | -100% |
| Latência por turno | 450ms | 0 dedicada | -100% |
| Componentes dedicados | 1 | 0 | -1 |
| Acurácia | 97.2% | 97.0% | -0.2% |
| Horas manutenção por mês | 3h | 0h dedicadas | -100% |

A frase final do ADR não diz que o Context Loader foi deletado. Ela diz: "A responsabilidade essencial de preservar fatos críticos foi absorvida pelo History Compactor e pelo Evaluator".

Essa diferença importa. Remover código sem preservar responsabilidade é fragilizar. Absorver responsabilidade em componente mais adequado é evolução.

### 🚀 O Que Não Remover no KODA

| Componente | Por que fica |
|------------|--------------|
| Evaluator | Protege contra self-evaluation collapse e erros de recomendação |
| State Persistence | Mantém memória confiável fora da janela de contexto |
| Safety checks de alergia | Protegem saúde do cliente |
| Compliance LGPD | Protege obrigação regulatória |
| Confirmação de pagamento | Protege decisão irreversível |

## 📄 Templates de Documentação

Copie estes templates para o seu repositório quando executar uma evolução real. Eles são completos o suficiente para começar sem voltar à teoria.

### 📄 Template de Relatorio de Diagnostico

```markdown
# Diagnostic Report: Budget Guard

## Resumo Executivo
Componente analisado: Budget Guard
Período analisado: 2025-10-01 a 2026-03-31
Recomendação: REMOVE

## Motivo Original
Proteger o KODA contra estouro de janela de contexto quando o modelo tinha apenas 32K tokens. O componente monitorava consumo de tokens por turno e truncava conversa ao atingir 80% da janela, prevenindo respostas truncadas.

## Métricas Coletadas
| Métrica | Valor |
|---------|-------|
| Total de turns analisados | 180000 |
| Triggers brutos | 0 |
| Prevenções reais | 0 |
| Falsos positivos | 0 |
| Tokens por turno | 0 (nunca disparou) |
| Latência por turno | 0ms (nunca disparou) |
| Custo mensal | R$ 300 (manutencao + monitoramento) |
| ROI | 0x |

## Effective Trigger Rate
Fórmula: prevenções reais / total de turns.
Resultado: 0.008%.

## Análise de Falsos Positivos
Descreva categorias, amostras revisadas e impacto para cliente ou suporte.

## Custo Operacional
Inclua tokens, latência, manutenção, onboarding e debug.

## Redundância
Liste componentes que cobrem parte da mesma responsabilidade.

## Risco de Remoção
Classifique impacto e probabilidade. Declare invariantes relacionados.

## Recomendação
Explique por que a recomendação foi escolhida e qual evidência ainda falta, se houver.
```

### 📄 Template de Roadmap de Evolucao

```markdown
# Evolution Roadmap: 2026 Q2

## Objetivo
Reduzir complexidade do harness sem reduzir safety, compliance, qualidade ou confiabilidade.

## Princípios
- Uma mudança principal por wave.
- Feature flag obrigatória.
- Shadow test para risco médio ou alto.
- Canary 5%, 25%, 100%.
- Observação de 14 dias antes da próxima remoção.
- One In One Out para novos componentes.

## Roadmap
| Ordem | Componente | Ação | Risco | Janela | Gate | Rollback |
|-------|------------|------|-------|--------|------|----------|
| 1 | Budget Guard | REMOVE | Baixo | Semana 4 | 14 dias sem regressão | Flag false |
| 2 | Priority Extractor | INVESTIGATE | Médio | Proximo trimestre | Coletar metricas de redundancia | Sem alteracao em prod |
| 3 | Context Loader | SIMPLIFY | Médio | Proximo trimestre | Accuracy delta menor que 1% | Flag context_loader_mode=full |
| 4 | Format Validator | SIMPLIFY | Baixo | Proximo trimestre | Shadow test concluido | Flag format_validator_mode=strict |

## Comunicação
Liste stakeholders, data da comunicação e canal usado.

## Dependências
Liste dashboards, testes, owners e aprovações necessárias.
```

### 📄 Template de ADR de Remocao

```markdown
# ADR: Remover Budget Guard

## Status
Aceito

## Data
2026-04-15

## Contexto
Budget Guard protegia o modelo de 32K tokens contra estouro de contexto que causava respostas truncadas. Com a janela atual de 200K (6.25x maior), conversas tipicas do KODA (~50K tokens) nunca atingem 80% do limite. O modelo atual tambem lida melhor com contextos longos, documentado no changelog.

## Evidência
- Effective Trigger Rate: 0%
- False Positive Ratio: 0x, porque não houve triggers nem prevenções
- ROI: 0x
- Shadow test: 30 dias sem diferença observável entre baseline e candidate
- Canary: 5%, 25% e 100% concluídos sem regressão
- Observação: 14 dias sem incidentes P0 ou P1

## Decisão
Remover Budget Guard do caminho principal e arquivar em `archive/components/budget-guard-v1/`.

## Consequências Positivas
- Redução de R$ 300 por mês em custo operacional.
- Redução de uma etapa no pipeline principal do KODA.

## Consequências Negativas
- Conversas extremamente longas dependem de alerta agregado, não de bloqueio por turno.
- Um modelo futuro com janela menor exige novo diagnóstico antes de restaurar a proteção.

## Rollback
Descreva flag, tempo esperado e métrica que confirma retorno.

## Links
- Diagnostic Report: `docs/harness-evolution/2026-q2-budget-guard-diagnostic.md`
- Validation Report: `docs/harness-evolution/2026-q2-budget-guard-validation.md`
- Dashboard: `dashboards/harness/budget-guard-removal`
- Archive: `archive/components/budget-guard-v1/`
```

### 📄 Template de Execucao por Wave

```markdown
# Execution Record: Wave 1 — Budget Guard

## Resumo da Wave
Componente: Budget Guard
Acao: REMOVE
Data de inicio: 2026-04-01
Data de 100%: 2026-04-03
Responsavel: Conversational Core Team

## Feature Flag
| Campo | Valor |
|-------|-------|
| Nome da flag | harness_evolution.remove_budget_guard |
| Valor padrao | false |
| Rollback | Alterar para false (sem deploy) |
| Dashboard | dashboards/harness/budget-guard-removal |

## Shadow Test
| Campo | Valor |
|-------|-------|
| Ativo | Sim (componente roda em paralelo, output descartado) |
| Duracao | 48 horas antes do canary 5% |
| Resultado | Zero diferenca entre baseline e candidate |

## Canary Rollout
| Percentual | Data | Metricas dentro do threshold? | Avanca? |
|------------|------|-------------------------------|---------|
| 5% | 2026-04-01 | Sim (latencia, incomplete, tickets) | Sim |
| 25% | 2026-04-02 | Sim | Sim |
| 100% | 2026-04-03 | Sim | Sim |

## Arquivo de Codigo
| Campo | Valor |
|-------|-------|
| Caminho | archive/components/budget-guard-v1/ |
| README | Contem motivo original, metricas usadas, data da remocao e licoes |
| ADR vinculado | docs/decisions/adr-remove-budget-guard.md |

## Observacao Pos-Remocao
| Metrica | Baseline | Target | Observado |
|---------|----------|--------|-----------|
| incomplete_response_rate | 0.12% | <= 0.13% | 0.11% |
| token_budget_exceeded | 0% | <= 0.01% | 0% |
| latency_p95_ms | 4100 | <= 4150 | 3850 |
| tickets_suporte_novos | 0 | <= 2 | 0 |

## Decisao Final
Encerrar remocao com sucesso. Agendar proxima wave para proximo trimestre.
```

### 📄 Template de Relatorio de Validacao Pos-Remocao

```markdown
# Post-Removal Validation Report: Budget Guard

## Resumo
Componente removido: Budget Guard
Data de início do canary: 2026-04-01
Data de 100%: 2026-04-03
Período de observação: 14 dias
Decisão final: Encerrar, manter observação ou rollback

## Comparativo Antes e Depois
| Métrica | Antes | Depois | Delta | Resultado |
|---------|-------|--------|-------|-----------|
| Latência p95 | 4100ms | 3850ms | -250ms | Melhorou |
| Tokens por turno | 3200 | 3000 | -200 | Melhorou |
| Incidentes P0/P1 | 0 | 0 | 0 | Estável |

## Alertas
Liste alertas disparados, se houver, e como foram tratados.

## Revisão Manual
Descreva tamanho da amostra, critério de aceitação e resultado.

## Rollback
Declare se rollback foi necessário. Se não foi, confirme que permaneceu disponível.

## Conclusão
Explique por que a remoção é considerada segura.
```

### 📄 Template de Agenda de Revisao Trimestral

```markdown
# Agenda: Quarterly Harness Evolution Review

## Participantes
- Engenharia
- Produto
- Suporte
- Segurança ou Compliance quando aplicável
- Owner do modelo

## 1. Revisão de Métricas
- Triggers reais por componente.
- Falsos positivos.
- ROI.
- Latência e tokens.
- Incidentes por categoria.

## 2. Revisão de Modelo
- Changelog do modelo atual.
- Capacidades novas.
- Benchmarks internos.
- Hipóteses para shadow test.

## 3. Scorecard
Revisar KEEP, SIMPLIFY, REMOVE e INVESTIGATE.

## 4. Roadmap
Escolher waves do trimestre, começando por baixo risco.

## 5. One In One Out
Revisar componentes novos propostos e componentes que devem sair ou encolher.

## 6. Decisões
Registrar owners, datas, gates e comunicação.

## 7. Encerramento
Confirmar próximos passos e data da primeira validação.
```

---

## 🧰 Runbook de Execucao por Fase

A tabela abaixo resume as acoes concretas por fase. Execute na ordem; cada linha depende da conclusao da anterior.

### 🩺 Fase de Diagnostico: Acoes Diarias

| Dia | Acao especifica | Artefato | Gate de avanco |
|-----|-----------------|----------|----------------|
| 1 | Listar componentes do pipeline e marcar invariantes (Safety, Compliance, Evaluator, State Persistence) | Inventario inicial | Todos os componentes listados, invariantes confirmados com tech lead |
| 2 | Coletar metricas de trigger bruto e prevencao real dos ultimos 60-90 dias para cada componente | Planilha de metricas por componente | Nenhum componente sem metrica; classificar sem metrica como INVESTIGATE |
| 3 | Analisar falsos positivos: amostrar 50+ triggers, classificar em categorias, calcular False Positive Ratio | Relatorio de falsos positivos | Categorias documentadas, ratio calculado para cada componente |
| 4 | Calcular custo operacional completo (tokens, latencia, manutencao, onboarding) e ROI padronizado | Planilha de custos e ROI | ROI calculado para todos os componentes com triggers |
| 5 | Preencher scorecard com os 7 sinais e classificar cada componente como KEEP, SIMPLIFY, REMOVE ou INVESTIGATE | Scorecard completo | Cada componente tem classificacao e justificativa em 1 paragrafo |
| 6 | Revisar scorecard com tech lead e produto; ajustar classificacoes com input cross-functional | Scorecard revisado | Aprovacao de tech lead registrada |

### 📋 Fase de Planejamento: Acoes Diarias

| Dia | Acao especifica | Artefato | Gate de avanco |
|-----|-----------------|----------|----------------|
| 1 | Ordenar componentes candidatos por risco (matriz: probabilidade x impacto) e agrupar em waves | Matriz de risco e waves | Waves definidas, cada uma com no maximo 1 componente de medio risco |
| 2 | Definir gates de avanco por wave (metricas, thresholds, periodo de observacao) e rollback por componente | Roadmap com gates e rollbacks | Rollback documentado e testavel para cada componente |
| 3 | Escrever comunicacao para stakeholders (produto, suporte, engenharia, lideranca) com cronograma | Comunicacao escrita | Comunicacao revisada por tech lead |
| 4 | Criar feature flags no codigo, configurar dashboard de observacao e alertas de regressao | Flags ativas em staging, dashboard populates | Flags testadas em staging com toggle manual |

### 🔧 Fase de Execucao: Acoes Diarias

| Dia | Acao especifica | Artefato | Gate de avanco |
|-----|-----------------|----------|----------------|
| 1 | Ativar feature flag para shadow test (componente roda em paralelo, output descartado) | Shadow test ativo | 24h sem erro no componente shadow |
| 2 | Ativar canary 5% com monitoramento ativo no dashboard dedicado | Canary 5% ativo | 24h com metricas dentro dos thresholds |
| 3 | Expandir para canary 25%, revisar metricas e tickets de suporte | Canary 25% ativo | 24h sem tickets novos atribuidos a mudanca |
| 4 | Expandir para canary 100% | Componente fora do pipeline principal | Confirmar com tech lead |
| 5 | Arquivar codigo removido em archive/components/<nome>/ com README | Codigo arquivado | README contem motivo original, metrica usada, data da remocao |
| 6 | Escrever ADR de remocao e publicar no repositorio | ADR publicado | ADR revisado por tech lead |

### ✅ Fase de Validacao: Acoes Diarias

| Dia | Acao especifica | Artefato | Gate de avanco |
|-----|-----------------|----------|----------------|
| 1-7 | Observar dashboard: incomplete responses, erros, latencia, tickets de suporte | Log diario de observacao | Nenhum alerta disparado |
| 8-14 | Continuar observacao, preparar post-mortem positivo e relatorio de validacao | Relatorio preliminar | Metricas estaveis por 14 dias consecutivos |
| 15 | Comparar metricas antes/depois, preencher relatorio final, comunicar stakeholders | Relatorio de validacao final | Deltas dentro dos thresholds definidos no roadmap |
| 16 | Agendar proxima revisao trimestral e atualizar inventario de componentes | Calendario trimestral | Proxima data de revisao no calendario do time |

---

## 🧾 Apendice Operacional: Microchecks de Revisao

Use estes microchecks durante review assincrono para evitar que decisoes importantes fiquem implicitas. Cada um cobre uma dimensao distinta.

### 🧾 Microcheck 1: Inventario Completo

- [ ] Todos os componentes do pipeline estao listados com owner, funcao e posicao no fluxo.
- [ ] Nenhum componente ficou de fora por ser "obvio" ou "sempre existiu".

### 🧾 Microcheck 2: Metricas Confiaveis

- [ ] Trigger bruto foi separado de prevencao real para todos os componentes.
- [ ] A janela de coleta e de pelo menos 60 dias; 90 dias foi usada quando disponivel.
- [ ] As metricas vem de observabilidade de producao, nao de estimativa ou intuicao.

### 🧾 Microcheck 3: Falsos Positivos Analisados

- [ ] Pelo menos 50 triggers foram revisados manualmente para classificar entre prevencao real e falso positivo.
- [ ] Categorias de falso positivo estao documentadas (ex: ma interpretacao de constraint, bug de parsing).

### 🧾 Microcheck 4: ROI Calculado Corretamente

- [ ] O custo operacional inclui tokens, latencia, horas de manutencao e complexidade de onboarding.
- [ ] O valor protegido usa prevencoes reais multiplicadas pelo custo medio do erro.
- [ ] Componentes com ROI < 1x por dois trimestres consecutivos estao marcados para investigacao.

### 🧾 Microcheck 5: Invariantes Protegidos

- [ ] Safety, Compliance, Evaluator e State Persistence estao explicitamente classificados como KEEP.
- [ ] Nenhum invariante foi classificado como REMOVE ou SIMPLIFY sem decisao arquitetural documentada.

### 🧾 Microcheck 6: Classificacao Clara

- [ ] Cada componente tem exatamente uma classificacao: KEEP, SIMPLIFY, REMOVE ou INVESTIGATE.
- [ ] A justificativa cita metrica concreta, nao opiniao (ex: "0 triggers em 180 dias", nao "parece desnecessario").

### 🧾 Microcheck 7: Uma Wave por Vez

- [ ] Cada wave do roadmap contem no maximo 1 componente de medio risco ou 2 de baixo risco.
- [ ] O plano respeita o periodo de 14 dias de observacao entre waves.

### 🧾 Microcheck 8: Rollback Pronto

- [ ] Para cada componente candidato a remocao, o comando de rollback esta documentado e foi testado.
- [ ] Feature flag permite reativacao em menos de 15 minutos sem deploy.

### 🧾 Microcheck 9: Codigo Arquivado com Memoria

- [ ] Componentes removidos estao em archive/components/<nome>/ com README contendo motivo, metricas e data.
- [ ] O ADR de remocao esta linkado no README do arquivo.

### 🧾 Microcheck 10: Post-Mortem Positivo

- [ ] O relatorio final lista: o que mudou, metricas antes/depois, aprendizados e quem participou.
- [ ] A proxima data de revisao trimestral esta agendada.
- [ ] O time foi comunicado e entende por que o componente foi removido.

---

## 🚨 Cenários de Falha e Recuperação

Harness Evolution precisa de planos para quando a evidência não confirma sua hipótese. Uma falha controlada no shadow test ou no canary não é derrota. É o processo funcionando antes que cliente sofra.

### 🚨 Cenário 1: Shadow Test Mostra Degradação

Situação: você roda shadow test do Context Loader Wave 2 e o candidate perde 2.3% de acurácia, acima do limite de 0.5%.

| Métrica | Baseline | Candidate | Delta | Gate |
|---------|----------|-----------|-------|------|
| Acurácia | 97.1% | 94.8% | -2.3% | Falhou |
| Recall de alergia | 99.9% | 99.2% | -0.7% | Falhou |
| Falsos positivos | 210 | 88 | Melhorou | Não compensa risco |
| Latência | 300ms | 100ms | Melhorou | Não compensa risco |

A resposta correta é pausar. Não ajuste threshold para caber no resultado.

```bash
koda shadow-tests stop context_loader_wave_2 --reason "accuracy_delta_above_gate"
koda flags set harness_evolution.context_loader_wave_2.enabled false --env staging
koda incident-notes create --type harness_evolution_learning --component ContextLoader
```

O relatório deve registrar a hipótese refutada:

```markdown
## Decisão
Não promover Context Loader Wave 2 neste trimestre.

## Motivo
O shadow test mostrou queda de 2.3% na acurácia e queda de 0.7% no recall de alergia. A economia de 400 tokens por turno não justifica risco de segurança do cliente.

## Próxima ação
Investigar alternativa menor: manter `customer_profile` em todo turno para clientes com alergia ou restrição médica, e relaxar apenas para conversas sem constraints críticas.
```

### 🚨 Cenário 2: Stakeholder Questiona a Remoção

Situação: Produto diz que remover Budget Guard parece arriscado porque "ele foi criado para proteger cliente".

Não responda com opinião. Responda com escopo e rollback.

```text
Produto: Se isso protege cliente, por que tirar?

Você: Porque nos últimos 180 dias ele protegeu zero clientes. A maior conversa chegou a 36% da janela atual. A proteção que continua relevante está no Evaluator e no History Compactor, que não vamos mexer.

Produto: E se aparecer uma conversa enorme amanhã?

Você: Temos alerta de token_budget_exceeded e rollback por flag. Também vamos revisar manualmente os maiores traces durante 14 dias.

Produto: Cliente vai notar?

Você: Não deve notar. Se notar, será por resposta incompleta, e esse é exatamente o alerta de parada.
```

Se o stakeholder ainda não concordar, a decisão vira INVESTIGATE por mais um ciclo. Isso é aceitável. O que não é aceitável é remover sem alinhamento quando a confiança organizacional ainda não existe.

### 🚨 Cenário 3: Canary 5% Dispara Alerta

Situação: após 3 horas de canary 5%, `incomplete_response_rate` sobe de 0.12% para 0.42%.

A regra é rollback primeiro, investigação depois.

```bash
koda flags set harness_evolution.remove_budget_guard.rollout.percentage 0 --env production
koda flags set harness_evolution.remove_budget_guard.enabled false --env production
koda alerts ack incomplete_response_regression --reason "rollback_executed"
koda traces export --flag harness_evolution.remove_budget_guard --window 3h --output evidence/budget-guard-canary-failure.jsonl
```

Depois você classifica os traces.

| Categoria | Quantidade | Leitura |
|-----------|------------|---------|
| Resposta realmente cortada | 7 | Regressão provável |
| Cliente abandonou antes da resposta | 3 | Não relacionado |
| Erro de API do catálogo | 2 | Não relacionado |
| Trace incompleto por logging | 1 | Observabilidade |

Se houver regressão provável, a decisão é reverter a recomendação para INVESTIGATE.

```markdown
## Resultado do Canary 5%
Rollback executado após alerta de incomplete_response_rate.

## Decisão
Budget Guard não será removido neste ciclo.

## Aprendizado
A métrica de zero triggers estava correta, mas o componente pode estar interagindo com truncamento silencioso antes do evento `blocked`. Precisamos instrumentar `near_limit_warning` antes de nova tentativa.
```

### 🚨 Cenário 4: Dois Trimestres Sem Nenhuma Mudança

Situação: o time faz review trimestral, identifica candidatos, mas sempre adia por medo.

Isso é o anti-padrão Never Remove aparecendo como prudência. A recuperação é escolher a menor mudança segura possível.

| Sintoma | Correção |
|---------|----------|
| Todo componente fica como INVESTIGATE | Definir qual métrica falta e prazo para coletar |
| Nenhuma feature flag é criada | Criar flag para componente de ROI 0x mesmo antes do canary |
| Stakeholders pedem mais dados indefinidamente | Definir decisão binária para a próxima review |
| Roadmap só adiciona componentes | Aplicar One In One Out na próxima proposta |

A conversa com Fernando pode soar assim:

```text
Fernando: O que removemos nos últimos dois trimestres?

Você: Nada. Investigamos três componentes, mas não executamos.

Fernando: Então nosso processo está incompleto. Harness Evolution sem remoção vira observabilidade passiva.

Você: Proponho Budget Guard como wave de confiança. ROI 0x, zero triggers, rollback simples.

Fernando: Aprovado. Uma wave pequena, bem feita, antes de qualquer discussão maior.
```

### 🚨 Cenário 5: A Remoção Funciona, Mas Outro Componente Fica Mais Caro

Situação: Budget Guard sai, mas Evaluator rejection rate sobe 12% por duas semanas.

Você não declara vitória só porque o componente removido não gerou incidente. Você verifica se transferiu custo para outra parte.

```sql
SELECT
  rejection_reason,
  COUNT(*) AS count
FROM evaluator_rejections
WHERE created_at >= DATE '2026-04-15'
  AND created_at < DATE '2026-04-29'
GROUP BY rejection_reason
ORDER BY count DESC;
```

Se o aumento vier de motivos não relacionados, documente. Se vier de contexto longo, a remoção precisa ser reavaliada.

### 🚨 Cenário 6: Rollback Falha em Staging

Situação: a flag volta para `false`, mas o pipeline não executa Budget Guard porque o código foi removido cedo demais.

Isso viola o playbook. Código só é arquivado depois dos 14 dias.

Recuperação:

```bash
koda deploy revert --service koda-orchestrator --to last-known-good
koda flags set harness_evolution.remove_budget_guard.enabled false --env staging
koda regression run --suite budget-guard-rollback
```

A ação preventiva é adicionar teste de rollback ao checklist da wave.

```yaml
rollback_test:
  required_before_canary: true
  checks:
    - flag_false_executes_component
    - metrics_budget_guard_executed_increments
    - blocked_path_still_returns_safe_response
```

---

## 🎯 Key Takeaways

1. Você não remove componentes porque o modelo novo parece melhor. Você remove quando métricas, shadow test e canary provam que o componente não paga mais seu custo.
2. Effective Trigger Rate usa prevenções reais, não triggers brutos. Essa diferença muda decisões.
3. Falsos positivos são custo de produto. Um componente que bloqueia fluxo correto cria dívida mesmo sem incidente.
4. ROI precisa incluir tokens, latência, manutenção, onboarding e debug.
5. KEEP, SIMPLIFY, REMOVE e INVESTIGATE dão linguagem comum para engenharia, produto e liderança.
6. One In One Out impede o harness de crescer sem limite.
7. Feature flag, shadow test e canary 5%, 25%, 100% são o trilho seguro de execução.
8. Uma wave por vez preserva causalidade. Se algo quebra, você sabe qual mudança causou.
9. Código removido deve ser arquivado com README, métricas e ADR.
10. Quatorze dias de observação fazem parte da mudança. Sem eles, a remoção ainda não terminou.
11. Invariantes como Evaluator, State Persistence, Safety e Compliance não saem só porque o modelo melhorou.
12. No KODA, Budget Guard é o primeiro alvo ideal. Context Loader e Priority Extractor pedem simplificação cuidadosa.

---

## ✅ Checkpoint: O Que Você Aprendeu

- [ ] Consigo explicar por que Harness Evolution é um processo, não uma limpeza pontual.
- [ ] Consigo montar inventário de componentes de harness.
- [ ] Consigo calcular Effective Trigger Rate.
- [ ] Consigo diferenciar trigger bruto de prevenção real.
- [ ] Consigo calcular False Positive Ratio.
- [ ] Consigo estimar custo completo de um componente.
- [ ] Consigo calcular ROI com a fórmula padronizada.
- [ ] Conheço os 7 sinais de que um componente está pronto para remoção.
- [ ] Consigo preencher uma scorecard de diagnóstico.
- [ ] Consigo classificar componentes como KEEP, SIMPLIFY, REMOVE ou INVESTIGATE.
- [ ] Consigo usar matriz de risco para ordenar waves.
- [ ] Entendo o ritmo trimestral Review, Implement, Observe.
- [ ] Sei aplicar One In One Out sem remover invariantes.
- [ ] Consigo criar comunicação clara para stakeholders.
- [ ] Consigo configurar feature flag para remoção segura.
- [ ] Consigo configurar shadow test sem impactar cliente.
- [ ] Consigo executar canary 5%, 25% e 100%.
- [ ] Consigo arquivar código removido com memória arquitetural.
- [ ] Consigo configurar dashboard e alertas de validação.
- [ ] Consigo escrever ADR de remoção.
- [ ] Consigo conduzir post-mortem positivo.
- [ ] Consigo aplicar o processo ao Budget Guard do KODA.
- [ ] Consigo identificar por que Evaluator e Safety não são candidatos a remoção.

Se marcou menos de 18 itens, releia as fases correspondentes antes de conduzir uma remoção real.

---

## ❓ Perguntas Frequentes

### ❓ Posso remover dois componentes se ambos têm ROI 0x?

**Resposta:** Não na mesma wave. Remova um, observe por 14 dias, documente e só então avance. Causalidade vale mais que velocidade.

### ❓ Changelog do modelo conta como evidência?

**Resposta:** Conta como hipótese. Evidência vem de shadow test, canary e métricas do seu domínio.

### ❓ Se o componente nunca disparou, ainda preciso de canary?

**Resposta:** Sim. Zero trigger reduz risco, mas canary valida integração, métricas e assumptions escondidas.

### ❓ Por que arquivar código em vez de deletar?

**Resposta:** Porque a decisão precisa ser compreensível no futuro. Archive com README e ADR evita que alguém recrie o mesmo componente sem saber a história.

### ❓ Quanto tempo preciso observar depois de remover?

**Resposta:** Use 14 dias como padrão. Para componente de alto risco, aumente para 30 dias.

### ❓ Evaluator pode ser removido se o modelo novo tem self-correction melhor?

**Resposta:** Não como regra geral. Evaluator é invariante de qualidade no KODA. Você pode otimizar rubricas, mas não remover o gate sem uma decisão arquitetural maior.

### ❓ State Persistence pode sair com context window maior?

**Resposta:** Não para KODA. Janela maior ajuda, mas estado persistente protege continuidade, auditoria e memória entre sessões.

### ❓ O que fazer se canary 5% piorar uma métrica?

**Resposta:** Pare rollout, volte a flag para o valor de rollback, colete traces e atualize o relatório. Não avance para 25% por esperança.

### ❓ Quem deve aprovar remoção?

**Resposta:** Owner técnico, produto para impacto em cliente e segurança ou compliance quando tocar domínio regulado.

### ❓ Como lidar com componente sem métricas?

**Resposta:** Classifique como INVESTIGATE. Primeiro adicione métricas e rode por uma janela mínima antes de decidir.

### ❓ One In One Out é obrigatório sempre?

**Resposta:** É a regra padrão. Exceções existem para Safety, Compliance, State Persistence e Evaluator.

### ❓ E se a economia for pequena?

**Resposta:** Ainda pode valer a pena se reduzir complexidade. Mas documente o benefício real, não venda como grande ganho financeiro.


### ❓ Como decidir entre SIMPLIFY e REMOVE quando o ROI é marginal?

**Resposta:** Use risco e preservação de responsabilidade. Se o componente ainda previne casos críticos, escolha SIMPLIFY. Context Loader com ROI 2.0x e 12 prevenções críticas não deve sair direto. Ele deve perder redundância primeiro.

### ❓ Posso usar apenas testes offline para remover um componente?

**Resposta:** Não. Teste offline ajuda a bloquear erro óbvio, mas não substitui shadow test e canary. Harness existe para produção real, com tráfego real, dados reais e comportamento de cauda longa.

### ❓ O que faço quando o componente não tem owner claro?

**Resposta:** Classifique como INVESTIGATE até owner existir. Remoção sem owner vira risco operacional, porque ninguém responde por métricas, rollback ou documentação.

### ❓ Como tratar componentes criados por incidentes antigos?

**Resposta:** Comece pelo incidente original. Pergunte se a causa ainda existe, se o modelo mudou, se outra proteção cobre o cenário e se a métrica protegida apareceu nos últimos 90 ou 180 dias. Respeite a história, mas exija evidência atual.

### ❓ Quando uma melhoria de modelo justifica abrir review extraordinária?

**Resposta:** Quando o changelog toca diretamente a fraqueza que originou componentes caros. Exemplo: janela de contexto 6x maior justifica revisar Budget Guard, Context Loader e History Compactor. Ainda assim, changelog abre hipótese, não autoriza remoção.

### ❓ E se a remoção reduzir custo mas piorar onboarding porque o arquivo foi para archive?

**Resposta:** Atualize a documentação de arquitetura. O novo dev não deve precisar ler archive para entender o fluxo atual. Archive responde por que algo existiu, não como o sistema funciona hoje.

### ❓ Como comparar métricas se o tráfego mudou muito entre antes e depois?

**Resposta:** Normalize por turn, por conversa e por segmento. Compare grupos equivalentes, especialmente conversas longas. Se houve campanha comercial ou sazonalidade, estenda a janela ou use shadow test como evidência principal.

### ❓ O que fazer quando suporte relata problema mas dashboard está limpo?

**Resposta:** Trate suporte como sinal real. Abra amostra de traces, confira labels e verifique se a métrica está capturando o sintoma correto. Às vezes o problema é observabilidade, não ausência de regressão.


---

## 📚 Referências & Próximas Leituras

- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`, módulo conceitual de Harness Evolution.
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`, base para entender por que Evaluator permanece invariante.
- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md`, base para entender persistência como proteção permanente.
- `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md`, contexto para simplificar History Compactor e Context Loader.
- `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md`, referência para aplicar decisões no KODA.
- ADR de remoção criado durante a execução real.
- Dashboard trimestral de efetividade do harness.
- Changelog do modelo em produção, usado apenas como hipótese para testes.

---

## 💭 Reflexão Final

A maturidade de um time de agentes não aparece só no que ele consegue construir. Aparece no que ele consegue remover sem medo, sem pressa e sem quebrar confiança.

Um harness nasce como proteção. Com o tempo, algumas proteções viram estrutura permanente. Outras viram andaime. O problema é que andaime antigo parece arquitetura quando ninguém mede seu valor.

Este playbook te dá a prática para separar os dois.

Quando você remove Budget Guard com zero incidentes, simplifica Context Loader sem perder recall e reduz Priority Extractor sem aumentar risco, você não está deixando o sistema mais fraco. Você está deixando o sistema mais honesto.

Cada componente restante passa a ter uma razão viva para existir.

Esse é o tipo de arquitetura que envelhece bem.

Fernando não queria metade do código fora por estética. Ele queria que o KODA carregasse apenas o peso necessário para proteger clientes reais. Agora você tem o processo para fazer isso acontecer.

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | 06-harness-evolution-playbook.md |
| **Tipo** | Guia de Implementação |
| **Nível** | Pós Nível 3 |
| **Tempo de leitura** | 4 a 6 horas |
| **Tempo de execução** | 2 a 6 semanas por wave |
| **Fonte conceitual** | 03-nivel-3-advanced-architecture/05-harness-evolution.md |
| **Aplicação principal** | KODA |
| **Status** | Completo |
| **Criado em** | Maio 2026 |
| **Próxima revisão** | Próximo ciclo trimestral de Harness Evolution |
