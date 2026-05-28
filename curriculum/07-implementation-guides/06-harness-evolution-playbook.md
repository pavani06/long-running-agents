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

context_loader_rate = effective_trigger_rate(
    real_preventions=12,
    total_turns=145000,
)

print(f"Effective Trigger Rate: {context_loader_rate:.6%}")
# Resultado esperado: 0.008276%
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
│ SIMPLIFY: Context Loader, Priority Extractor                                 │
│ KEEP: Evaluator, Safety, Compliance, State Persistence                       │
│ INVESTIGATE: Format Validator                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 🩺 Passo 9: Preencha a Scorecard

| Componente | Trigger efetivo | Falsos positivos | Custo mensal | ROI | Redundância | Invariante | Score | Recomendação |
|------------|-----------------|------------------|--------------|-----|-------------|------------|-------|--------------|
| Context Loader | 0.008% | 340 | R$ 1610 | 2.0x | Alta | Não | 68/100 | SIMPLIFY |
| Budget Guard | 0% | 0 | R$ 300 | 0x | Baixa | Não | 92/100 | REMOVE |
| Evaluator | 12.4% | 31 | R$ 2400 | 8.7x | Baixa | Sim | 15/100 | KEEP |
| State Persistence | Sempre ativo | 0 | R$ 600 | Não aplicável | Baixa | Sim | 5/100 | KEEP |
| Format Validator | 0.05% | 14 | R$ 120 | 1.3x | Média | Não | 54/100 | INVESTIGATE |
| Priority Extractor | 0.02% | 81 | R$ 480 | 0.7x | Alta | Não | 75/100 | SIMPLIFY |

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
| 2 | Priority Extractor | SIMPLIFY | Médio | Semanas 9 a 10 | False positives caem 50% | Flag `priority_extractor_mode=full` |
| 3 | Context Loader | SIMPLIFY | Médio | Próximo trimestre | Accuracy delta menor que 1% | Flag `context_loader_mode=full` |
| 4 | Format Validator | INVESTIGATE | Médio | Próximo trimestre | Shadow test concluído | Sem alteração em prod |

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
      created_at: "2026-05-28"
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
    "executed_at": "2026-05-28T10:00:00Z",
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
2026-05-28

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

Esta seção mostra uma execução concreta no KODA, do diagnóstico à celebração. O componente escolhido é Budget Guard porque ele é o melhor primeiro alvo: zero triggers em 180 dias, ROI 0x, baixo risco e rollback simples.

### 🩺 Diagnóstico KODA

Você abre o dashboard de 180 dias e confirma que `budget_guard.blocked` está em zero. O modelo atual tem janela de 200K tokens. Conversas típicas do KODA ficam em 50K tokens. O componente custa R$ 300 por mês entre tokens, manutenção e debug. A scorecard marca 92/100 para remoção.

### 📋 Planejamento KODA

Você classifica Budget Guard como REMOVE. O roadmap coloca a remoção na Wave 1. Fernando aprova porque Safety, Compliance, Evaluator e State Persistence não mudam. Produto valida que não há mudança esperada para cliente.

### 🔧 Execução KODA

Você cria `remove_budget_guard`, roda shadow test, depois canary 5%, 25% e 100%. Durante todo o rollout, o dashboard observa `incomplete_response_rate`, `token_budget_exceeded`, `latency_p95_ms` e tickets de suporte.

### ✅ Validação KODA

Depois de 14 dias, incomplete responses ficam estáveis em 0.12%, token budget exceeded continua em 0%, latência p95 cai 250ms e nenhum ticket novo aparece. O código vai para `archive/components/budget-guard-v1/` com README e ADR.

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
| Classificação | SIMPLIFY |
| Risco | Médio |
| Plano | Mover prioridade para rubrica do Evaluator e remover extractor dedicado |
| Resultado esperado | Menos falsos positivos e menos uma etapa no pipeline |

### 🚀 O Que Não Remover no KODA

| Componente | Por que fica |
|------------|--------------|
| Evaluator | Protege contra self-evaluation collapse e erros de recomendação |
| State Persistence | Mantém memória confiável fora da janela de contexto |
| Safety checks de alergia | Protegem saúde do cliente |
| Compliance LGPD | Protege obrigação regulatória |
| Confirmação de pagamento | Protege decisão irreversível |

---

## 📄 Templates de Documentação

Copie estes templates para o seu repositório quando executar uma evolução real. Eles são completos o suficiente para começar sem voltar à teoria.

### 📄 Diagnostic Report Template

```markdown
# Diagnostic Report: Budget Guard

## Resumo Executivo
Componente analisado: Budget Guard
Período analisado: 2025-11-28 a 2026-05-28
Recomendação: KEEP, SIMPLIFY, REMOVE ou INVESTIGATE

## Motivo Original
Descreva por que o componente foi criado, qual fraqueza do modelo ele cobria e qual incidente ou risco motivou sua criação.

## Métricas Coletadas
| Métrica | Valor |
|---------|-------|
| Total de turns analisados | 145000 |
| Triggers brutos | 352 |
| Prevenções reais | 12 |
| Falsos positivos | 340 |
| Tokens por turno | 1200 |
| Latência por turno | 450ms |
| Custo mensal | R$ 1610 |
| ROI | 2.0x |

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

### 📄 Evolution Roadmap Template

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
| 2 | Priority Extractor | SIMPLIFY | Médio | Semana 9 | FP reduzido sem accuracy cair | Mode full |

## Comunicação
Liste stakeholders, data da comunicação e canal usado.

## Dependências
Liste dashboards, testes, owners e aprovações necessárias.
```

### 📄 Removal ADR Template

```markdown
# ADR: Remover Budget Guard

## Status
Proposto

## Data
2026-05-28

## Contexto
Descreva por que o componente existia e qual mudança tornou a remoção possível.

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

### 📄 Post-Removal Validation Report Template

```markdown
# Post-Removal Validation Report: Budget Guard

## Resumo
Componente removido: Budget Guard
Data de início do canary: 2026-05-14
Data de 100%: 2026-05-16
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

### 📄 Quarterly Review Agenda Template

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

## 🧰 Runbook Detalhado por Dia

Esta seção transforma o playbook em uma rotina de execução. Use quando você estiver conduzindo a mudança em produção e quiser reduzir ambiguidade operacional.

### 🧰 Dia 1: Execução Guiada

O foco do dia é inventário e alinhamento de invariantes. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para inventário e alinhamento de invariantes | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para inventário e alinhamento de invariantes | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para inventário e alinhamento de invariantes | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para inventário e alinhamento de invariantes | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para inventário e alinhamento de invariantes | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que inventário e alinhamento de invariantes tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que inventário e alinhamento de invariantes tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que inventário e alinhamento de invariantes tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que inventário e alinhamento de invariantes tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que inventário e alinhamento de invariantes tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que inventário e alinhamento de invariantes tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que inventário e alinhamento de invariantes tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 2: Execução Guiada

O foco do dia é coleta de métricas e validação de fontes. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para coleta de métricas e validação de fontes | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para coleta de métricas e validação de fontes | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para coleta de métricas e validação de fontes | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para coleta de métricas e validação de fontes | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para coleta de métricas e validação de fontes | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que coleta de métricas e validação de fontes tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que coleta de métricas e validação de fontes tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que coleta de métricas e validação de fontes tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que coleta de métricas e validação de fontes tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que coleta de métricas e validação de fontes tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que coleta de métricas e validação de fontes tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que coleta de métricas e validação de fontes tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 3: Execução Guiada

O foco do dia é análise de falsos positivos. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para análise de falsos positivos | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para análise de falsos positivos | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para análise de falsos positivos | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para análise de falsos positivos | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para análise de falsos positivos | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que análise de falsos positivos tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que análise de falsos positivos tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que análise de falsos positivos tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que análise de falsos positivos tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que análise de falsos positivos tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que análise de falsos positivos tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que análise de falsos positivos tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 4: Execução Guiada

O foco do dia é cálculo de custo e ROI. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para cálculo de custo e ROI | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para cálculo de custo e ROI | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para cálculo de custo e ROI | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para cálculo de custo e ROI | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para cálculo de custo e ROI | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que cálculo de custo e ROI tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que cálculo de custo e ROI tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que cálculo de custo e ROI tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que cálculo de custo e ROI tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que cálculo de custo e ROI tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que cálculo de custo e ROI tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que cálculo de custo e ROI tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 5: Execução Guiada

O foco do dia é scorecard e classificação preliminar. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para scorecard e classificação preliminar | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para scorecard e classificação preliminar | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para scorecard e classificação preliminar | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para scorecard e classificação preliminar | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para scorecard e classificação preliminar | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que scorecard e classificação preliminar tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que scorecard e classificação preliminar tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que scorecard e classificação preliminar tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que scorecard e classificação preliminar tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que scorecard e classificação preliminar tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que scorecard e classificação preliminar tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que scorecard e classificação preliminar tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 6: Execução Guiada

O foco do dia é revisão com engenharia. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para revisão com engenharia | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para revisão com engenharia | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para revisão com engenharia | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para revisão com engenharia | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para revisão com engenharia | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que revisão com engenharia tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que revisão com engenharia tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que revisão com engenharia tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que revisão com engenharia tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que revisão com engenharia tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que revisão com engenharia tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que revisão com engenharia tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 7: Execução Guiada

O foco do dia é revisão com produto e suporte. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para revisão com produto e suporte | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para revisão com produto e suporte | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para revisão com produto e suporte | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para revisão com produto e suporte | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para revisão com produto e suporte | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que revisão com produto e suporte tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que revisão com produto e suporte tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que revisão com produto e suporte tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que revisão com produto e suporte tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que revisão com produto e suporte tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que revisão com produto e suporte tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que revisão com produto e suporte tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 8: Execução Guiada

O foco do dia é roadmap e matriz de risco. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para roadmap e matriz de risco | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para roadmap e matriz de risco | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para roadmap e matriz de risco | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para roadmap e matriz de risco | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para roadmap e matriz de risco | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que roadmap e matriz de risco tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que roadmap e matriz de risco tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que roadmap e matriz de risco tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que roadmap e matriz de risco tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que roadmap e matriz de risco tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que roadmap e matriz de risco tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que roadmap e matriz de risco tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 9: Execução Guiada

O foco do dia é comunicação de stakeholders. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para comunicação de stakeholders | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para comunicação de stakeholders | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para comunicação de stakeholders | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para comunicação de stakeholders | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para comunicação de stakeholders | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que comunicação de stakeholders tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que comunicação de stakeholders tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que comunicação de stakeholders tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que comunicação de stakeholders tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que comunicação de stakeholders tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que comunicação de stakeholders tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que comunicação de stakeholders tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 10: Execução Guiada

O foco do dia é feature flag e configuração de shadow test. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para feature flag e configuração de shadow test | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para feature flag e configuração de shadow test | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para feature flag e configuração de shadow test | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para feature flag e configuração de shadow test | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para feature flag e configuração de shadow test | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que feature flag e configuração de shadow test tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que feature flag e configuração de shadow test tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que feature flag e configuração de shadow test tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que feature flag e configuração de shadow test tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que feature flag e configuração de shadow test tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que feature flag e configuração de shadow test tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que feature flag e configuração de shadow test tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 11: Execução Guiada

O foco do dia é shadow test em staging. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para shadow test em staging | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para shadow test em staging | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para shadow test em staging | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para shadow test em staging | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para shadow test em staging | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que shadow test em staging tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que shadow test em staging tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que shadow test em staging tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que shadow test em staging tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que shadow test em staging tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que shadow test em staging tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que shadow test em staging tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 12: Execução Guiada

O foco do dia é shadow test com amostra de produção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para shadow test com amostra de produção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para shadow test com amostra de produção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para shadow test com amostra de produção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para shadow test com amostra de produção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para shadow test com amostra de produção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que shadow test com amostra de produção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que shadow test com amostra de produção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que shadow test com amostra de produção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que shadow test com amostra de produção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que shadow test com amostra de produção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que shadow test com amostra de produção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que shadow test com amostra de produção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 13: Execução Guiada

O foco do dia é revisão manual de traces. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para revisão manual de traces | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para revisão manual de traces | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para revisão manual de traces | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para revisão manual de traces | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para revisão manual de traces | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que revisão manual de traces tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que revisão manual de traces tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que revisão manual de traces tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que revisão manual de traces tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que revisão manual de traces tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que revisão manual de traces tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que revisão manual de traces tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 14: Execução Guiada

O foco do dia é go ou pause antes do canary. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para go ou pause antes do canary | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para go ou pause antes do canary | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para go ou pause antes do canary | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para go ou pause antes do canary | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para go ou pause antes do canary | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que go ou pause antes do canary tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que go ou pause antes do canary tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que go ou pause antes do canary tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que go ou pause antes do canary tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que go ou pause antes do canary tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que go ou pause antes do canary tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que go ou pause antes do canary tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 15: Execução Guiada

O foco do dia é canary 5%. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para canary 5% | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para canary 5% | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para canary 5% | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para canary 5% | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para canary 5% | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que canary 5% tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que canary 5% tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que canary 5% tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que canary 5% tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que canary 5% tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que canary 5% tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que canary 5% tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 16: Execução Guiada

O foco do dia é revisão do canary 5%. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para revisão do canary 5% | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para revisão do canary 5% | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para revisão do canary 5% | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para revisão do canary 5% | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para revisão do canary 5% | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que revisão do canary 5% tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que revisão do canary 5% tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que revisão do canary 5% tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que revisão do canary 5% tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que revisão do canary 5% tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que revisão do canary 5% tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que revisão do canary 5% tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 17: Execução Guiada

O foco do dia é canary 25%. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para canary 25% | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para canary 25% | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para canary 25% | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para canary 25% | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para canary 25% | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que canary 25% tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que canary 25% tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que canary 25% tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que canary 25% tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que canary 25% tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que canary 25% tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que canary 25% tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 18: Execução Guiada

O foco do dia é revisão do canary 25%. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para revisão do canary 25% | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para revisão do canary 25% | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para revisão do canary 25% | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para revisão do canary 25% | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para revisão do canary 25% | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que revisão do canary 25% tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que revisão do canary 25% tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que revisão do canary 25% tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que revisão do canary 25% tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que revisão do canary 25% tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que revisão do canary 25% tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que revisão do canary 25% tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 19: Execução Guiada

O foco do dia é canary 100%. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para canary 100% | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para canary 100% | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para canary 100% | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para canary 100% | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para canary 100% | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que canary 100% tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que canary 100% tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que canary 100% tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que canary 100% tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que canary 100% tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que canary 100% tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que canary 100% tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 20: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 21: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 22: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 23: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 24: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 25: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 26: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 27: Execução Guiada

O foco do dia é observação pós-remoção. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para observação pós-remoção | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para observação pós-remoção | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para observação pós-remoção | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para observação pós-remoção | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para observação pós-remoção | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que observação pós-remoção tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que observação pós-remoção tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 28: Execução Guiada

O foco do dia é comparativo final antes e depois. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para comparativo final antes e depois | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para comparativo final antes e depois | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para comparativo final antes e depois | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para comparativo final antes e depois | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para comparativo final antes e depois | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que comparativo final antes e depois tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que comparativo final antes e depois tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que comparativo final antes e depois tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que comparativo final antes e depois tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que comparativo final antes e depois tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que comparativo final antes e depois tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que comparativo final antes e depois tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 29: Execução Guiada

O foco do dia é ADR, archive e documentação. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para ADR, archive e documentação | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para ADR, archive e documentação | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para ADR, archive e documentação | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para ADR, archive e documentação | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para ADR, archive e documentação | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que ADR, archive e documentação tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que ADR, archive e documentação tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que ADR, archive e documentação tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que ADR, archive e documentação tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que ADR, archive e documentação tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que ADR, archive e documentação tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que ADR, archive e documentação tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

### 🧰 Dia 30: Execução Guiada

O foco do dia é post-mortem positivo e próxima wave. Não avance se a evidência do dia anterior estiver incompleta.

| Bloco | Ação | Saída esperada |
|-------|------|----------------|
| 1 | Executar verificação 1 para post-mortem positivo e próxima wave | Evidência registrada no artefato da fase |
| 2 | Executar verificação 2 para post-mortem positivo e próxima wave | Evidência registrada no artefato da fase |
| 3 | Executar verificação 3 para post-mortem positivo e próxima wave | Evidência registrada no artefato da fase |
| 4 | Executar verificação 4 para post-mortem positivo e próxima wave | Evidência registrada no artefato da fase |
| 5 | Executar verificação 5 para post-mortem positivo e próxima wave | Evidência registrada no artefato da fase |

Checklist do dia:
- [ ] Passo 1: confirmar que post-mortem positivo e próxima wave tem evidência verificável e owner definido.
- [ ] Passo 2: confirmar que post-mortem positivo e próxima wave tem evidência verificável e owner definido.
- [ ] Passo 3: confirmar que post-mortem positivo e próxima wave tem evidência verificável e owner definido.
- [ ] Passo 4: confirmar que post-mortem positivo e próxima wave tem evidência verificável e owner definido.
- [ ] Passo 5: confirmar que post-mortem positivo e próxima wave tem evidência verificável e owner definido.
- [ ] Passo 6: confirmar que post-mortem positivo e próxima wave tem evidência verificável e owner definido.
- [ ] Passo 7: confirmar que post-mortem positivo e próxima wave tem evidência verificável e owner definido.

Critério de parada: se uma métrica crítica piorar além do threshold, pause a wave e volte para a última decisão aprovada.

---

## 🧾 Apêndice Operacional: Microchecks de Revisão

Use estes microchecks durante review assíncrono. Eles evitam que decisões importantes fiquem implícitas.

### 🧾 Microcheck 1: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 1 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 1 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 1 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 1 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 1 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 1 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 1 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 2: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 2 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 2 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 2 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 2 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 2 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 2 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 2 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 3: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 3 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 3 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 3 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 3 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 3 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 3 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 3 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 4: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 4 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 4 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 4 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 4 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 4 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 4 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 4 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 5: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 5 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 5 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 5 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 5 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 5 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 5 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 5 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 6: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 6 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 6 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 6 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 6 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 6 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 6 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 6 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 7: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 7 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 7 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 7 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 7 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 7 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 7 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 7 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 8: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 8 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 8 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 8 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 8 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 8 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 8 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 8 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 9: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 9 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 9 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 9 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 9 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 9 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 9 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 9 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 10: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 10 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 10 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 10 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 10 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 10 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 10 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 10 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 11: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 11 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 11 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 11 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 11 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 11 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 11 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 11 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 12: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 12 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 12 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 12 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 12 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 12 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 12 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 12 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 13: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 13 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 13 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 13 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 13 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 13 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 13 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 13 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 14: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 14 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 14 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 14 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 14 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 14 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 14 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 14 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 15: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 15 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 15 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 15 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 15 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 15 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 15 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 15 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 16: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 16 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 16 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 16 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 16 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 16 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 16 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 16 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 17: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 17 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 17 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 17 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 17 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 17 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 17 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 17 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 18: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 18 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 18 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 18 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 18 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 18 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 18 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 18 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 19: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 19 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 19 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 19 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 19 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 19 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 19 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 19 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 20: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 20 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 20 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 20 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 20 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 20 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 20 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 20 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 21: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 21 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 21 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 21 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 21 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 21 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 21 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 21 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 22: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 22 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 22 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 22 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 22 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 22 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 22 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 22 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 23: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 23 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 23 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 23 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 23 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 23 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 23 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 23 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 24: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 24 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 24 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 24 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 24 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 24 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 24 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 24 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 25: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 25 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 25 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 25 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 25 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 25 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 25 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 25 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 26: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 26 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 26 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 26 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 26 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 26 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 26 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 26 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 27: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 27 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 27 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 27 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 27 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 27 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 27 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 27 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 28: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 28 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 28 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 28 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 28 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 28 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 28 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 28 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 29: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 29 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 29 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 29 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 29 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 29 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 29 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 29 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 30: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 30 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 30 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 30 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 30 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 30 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 30 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 30 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 31: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 31 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 31 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 31 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 31 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 31 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 31 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 31 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 32: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 32 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 32 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 32 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 32 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 32 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 32 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 32 tem decisão documentada no relatório da wave.

### 🧾 Microcheck 33: Evidência Antes de Opinião

- [ ] O componente avaliado no microcheck 33 tem métrica de valor real, não apenas descrição de intenção.
- [ ] O componente avaliado no microcheck 33 tem custo de tokens registrado.
- [ ] O componente avaliado no microcheck 33 tem custo de latência registrado.
- [ ] O componente avaliado no microcheck 33 tem owner técnico identificado.
- [ ] O componente avaliado no microcheck 33 não é Safety, Compliance, Evaluator ou State Persistence.
- [ ] O componente avaliado no microcheck 33 tem rollback definido antes de qualquer deploy.
- [ ] O componente avaliado no microcheck 33 tem decisão documentada no relatório da wave.

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
