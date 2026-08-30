---
title: "Exercício 7: Consolidar Especialistas em um Mega-Expert"
type: curriculum-exercise
nivel: 3
aliases: ["mega-expert consolidation", "mega expert", "fusão de especialistas", "superhuman benchmark", "deflection bot", "specialist fragmentation", "fragmentação de especialistas"]
tags: [curriculo-conteudo, nivel-3, exercicio, mega-expert, specialist-fusion, superhuman-benchmark, benchmark-gate, deflection-bot, customer-experience, no-regression, python, dataclass]
relates-to: ["[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]", "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification|Kavak Playbook Classification]]", "[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]", "[[docs/canonical/goal-atomicity-split|Goal Atomicity Split]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-05-persona-based-documentation|Exercício 5: Persona-Based Documentation]]", "[[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|Multi-Agent Systems]]", "[[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|Customer Journey Flows]]"]
last_updated: 2026-08-30
---

# 🧬 Exercício 7: Consolidar Especialistas em um Mega-Expert
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter lido `01-multi-agent-systems.md` (Nível 3) + Exercício 5 (`exercise-05-persona-based-documentation.md`)
**Objetivo:** Construir o pipeline completo de consolidação de especialistas: diagnosticar a fragmentação da experiência do cliente, aplicar um gate de benchmark superhumano (o agente só funde depois de vencer o melhor humano individual da especialidade), e fundir os aprovados em um único mega-expert voltado para o cliente — com escalonamento humano contextualizado onde a barra ainda não foi batida

---

## 📖 Prólogo: A Cliente Que Foi Passada de Robô em Robô

**Sábado, 14h20. Marina quer comprar suplementos. Uma pergunta, na verdade duas.**

```
Marina: "Oi! Tomo remédio para pressão. Posso tomar creatina?
         E se eu pagar no Pix hoje, dá pra reembolsar se eu
         não me adaptar?"

NUTRI-BOT:  "Ótima pergunta! Mas pagamentos não é comigo.
             Vou te transferir para o setor responsável."
             [TRANSFERINDO... ▶ 1º handoff]

PAY-BOT:    "Bem-vinda! Me informe CPF, e-mail e número do pedido."
Marina:     "Eu já passei tudo no início da conversa..."
PAY-BOT:    "Não tenho acesso ao histórico do outro atendente.
             Preciso que repita."
             [▶ 2ª repetição de informação]

Marina:     "Poxa, ok: CPF 333.444.555-66... E sobre a creatina
             com pressão alta?"

PAY-BOT:    "Sobre nutricionismo, consulte nosso blog:
             futanbear.com/blog/saude"
             [▶ 1º deflection: jogou pro blog em vez de responder]

Marina:     "Eu quero comprar, não ler blog..."
PAY-BOT:    "Pedido Pix registrado! Para trocas, fale com LOGI-BOT."
             [TRANSFERINDO... ▶ 2º handoff]

LOGI-BOT:   "Olá! Meu sistema mostra outro CPF. Repete o seu?"
             [▶ 3ª repetição]

Marina:     "SERIAMENTE? 333.444.555-66. Vocês têm programa de
             pontos? Compro todo mês."
LOGI-BOT:   "Fidelidade é o LOYA-BOT."
             [TRANSFERINDO... ▶ 3º handoff]

LOYA-BOT:   "Opa! Para consultar pontos, acesse o portal web
             e faça login no menu Minha Conta > Saldo."
             [▶ 2º deflection: mandou pro portal]

Marina:     "Pelo app não dá?"
LOYA-BOT:   "Pontos é só no portal. Outra coisa? Retorno ao
             NUTRI-BOT, que iniciou seu atendimento."
             [TRANSFERINDO... ▶ 4º handoff]

NUTRI-BOT:  "Aqui é nutrição. Pagamentos resolve no PAY-BOT."
             [TRANSFERINDO... ▶ 5º handoff → a conversa dá a volta]

PAY-BOT:    "Bem-vindo de volta! Me confirma CPF e e-mail?"
             [▶ 4ª repetição]

Marina:     "Tchau."
```

**O relatório da semana seguinte:**

```
╔══════════════════════════════════════════════════════════════════╗
║           A CONVERSA QUE NINGUÉM FECHOU                          ║
║                                                                  ║
║  Duração até a desistência:        43 minutos                    ║
║  Handoffs entre robôs:             6                             ║
║  Informações repetidas pela cliente: 4 vezes (CPF, pedido, e-mail)║
║  Deflections ("veja o blog/portal"): 2                           ║
║  Perguntas respondidas por completo: 0 de 4                      ║
║  Carrinho abandonado:              R$ 387,00                     ║
║                                                                  ║
║  Cada robô, isoladamente, bateu sua meta:                        ║
║    NUTRI-BOT   tempo de resposta médio    ✅ meta: < 30s         ║
║    PAY-BOT     taxa de registro de Pix    ✅ meta: 95%           ║
║    LOGI-BOT    SLA de transferência       ✅ meta: < 60s         ║
║    LOYA-BOT    deflection rate (portal)   ✅ meta: 70%           ║
║                                                                  ║
║  A experiência do cliente: fragmentada em 5 pedaços.             ║
║  Nenhum robô viu a conversa inteira. Nenhum podia resolver       ║
║  a pergunta real, que atravessava duas especialidades.           ║
╚══════════════════════════════════════════════════════════════════╝
```

Na retrospectiva de segunda-feira:

```
Head de Ops: "Como assim NPS despencando? Cada bot tem 95%+ na
              própria métrica!"

Arquiteta:   "Exatamente esse o problema. Cada métrica mede um
              pedaço. Nenhuma mede a pergunta da Marina — que
              era UMA pergunta atravessando nutrição E pagamentos."

Dev Senior:  "A gente podia colocar um roteador melhor, com mais
              regras de handoff..."

Arquiteta:   "Mais regras de handoff é mais fragmentação. A
              alternativa é o oposto: UM agente de frente pro
              cliente com TODAS as especialidades fundidas dentro.
              Mas com duas regras duras:

              Regra 1 — NINGUÉM entra na fusão sem antes vencer o
              melhor humano individual da sua especialidade, em
              benchmark. Fusão de mediocridade é mediocridade
              integrada.

              Regra 2 — Especialidade que ainda não bateu o melhor
              humano NÃO vira deflection bot ('veja o portal').
              Vira escalonamento pra humano COM o contexto todo
              da conversa, na MESMA thread."

Head de Ops: "E como a gente sabe que a fusão não degradou alguma
              especialidade?"

Arquiteta:   "Invariantes de fusão: o mega-expert tem que pontuar
              >= que cada especialista sozinho no eval da própria
              especialidade dela. Fusão soma capacidade — nunca
              subtrai."
```

**Sua missão:** implementar o pipeline completo — diagnóstico de fragmentação, gate de benchmark superhumano, fusão sem regressão e escalonamento contextual. Este padrão não existe em nenhum lugar do repositório (classificado como `Missing` em `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:315-335`) — você está construindo a primeira implementação.

---

## 🧠 O Contexto

### O Modelo Mental: Fragmentação vs. Deflection vs. Mega-Expert

O padrão vem da Kavak: a organização antiga exigia ~15 especialistas distribuídos em 15 times (financiamento, consultoria de carro, compra, seguro, cotação de trade-in). O padrão é: **primeiro construir um agente que vence cada especialista individual, depois fundi-los em um único "mega especialista" que atende o cliente** (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:88-89`).

Três arquiteturas competem pelo front do cliente:

| Arquitetura | Como funciona | Por que falha |
|---|---|---|
| **Especialistas fragmentados** | N bots, cada um com sua métrica, cliente passado entre eles | Ninguém vê a conversa inteira; perguntas que atravessam domínios nunca fecham; handoffs com repetição de informação |
| **Deflection bot** | Um bot na frente que despacha ("veja o blog/portal", "fale com o setor X") | Resolve o SLA do bot, não o problema do cliente; abre mão da venda/relacionamento |
| **Mega-expert** | Um agente de frente com as especialidades fundidas DENTRO, cada uma vencedora do melhor humano | É a única que coloca a barra superhumana como seletor de arquitetura |

A escolha entre mega-expert e deflection bot não é estética — ela deriva da barra escolhida: mirar "melhor que o melhor humano já contratado" em vez de "bom o suficiente" muda qual arquitetura você constrói (`...analysis.md:148`). A aposta superhumana é uma das três decisões estruturais do playbook: **a barra é superar o melhor humano já contratado em cada dimensão que importa** (`...analysis.md:26-28`).

### Fronteiras do padrão (o que NÃO é mega-expert)

1. **Mega-expert ≠ mega-prompt.** A fusão aqui é de *capacidades avaliadas e gateadas por especialidade* — não um prompt denso e gigante. O repositório já rejeita "dense mega-prompts" como anti-padrão: escala-se por decomposição, um outcome por intenção (`docs/canonical/goal-atomicity-split.md:92`). Dentro do mega-expert, as especialidades continuam decompostas; o que funde é a *fronteira com o cliente* e o *benchmark que habilita a fusão*.

2. **Mega-expert ≠ captura de conhecimento em docs.** O `docs/canonical/persona-based-documentation.md:23` documenta o problema vizinho — especialistas cujo conhecimento não é capturado em superfícies que agentes carregam — mas a solução lá é documentação por persona (Exercício 5). Aqui a unidade é o **agente especialista com benchmark**, e a fusão é arquitetural, não documental.

3. **Escalonamento ≠ deflection.** Quando uma especialidade ainda não bateu o melhor humano, o cliente não é despachado: um humano entra **na mesma thread, com o contexto acumulado**. O anti-padrão open-loop ("agente entrega pra fila humana e esquece → nenhum dado de melhoria → sistema empaca") está documentado em `...analysis.md:164`.

4. **Thread única = relacionamento.** O journey do KODA trata o cliente como relacionamento de longo prazo ("OBJETIVO: Construir relacionamento de longo prazo", `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:715-722`). Fragmentar a thread em 5 robôs destrói exatamente o ativo que o journey quer construir.

### O Que Você Vai Construir

1. **`FragmentationAnalyzer`** (Parte 1 — Diagnóstico): lê um log de conversa e quantifica a fragmentação (handoffs, repetições, deflections)
2. **`BenchmarkResult` + gate superhumano** (Parte 2): cada `SpecialistAgent` só entra na fusão se `agent_score >= best_human_score` com dataset de eval suficiente
3. **`MegaExpert` + `MegaExpertPipeline`** (Parte 3 — Pipeline de fusão): fusão com invariante de no-regression, ganho cross-domain e escalonamento contextual

O domínio de exemplo é o KODA: 5 especialidades (consultoria nutricional, recomendação de produto, pagamentos, logística, fidelidade). Quatro batem o melhor humano. Uma — fidelidade — ainda não: ela testa o caminho de escalonamento.

---

## ✅ Requisitos

### Funcionais

- [ ] `FragmentationAnalyzer.diagnose()` produz um `FragmentationDiagnosis` com: contagem de handoffs, repetições de informação, deflections, robôs distintos na conversa e escalonamentos humanos
- [ ] `is_fragmented` retorna `True` quando: handoffs >= 3 OU deflections >= 1 OU repetições >= 2
- [ ] `BenchmarkResult.beats_best_human()` exige `agent_score >= best_human_score` E `eval_case_count >= MIN_EVAL_CASES` (30) — benchmark sem dataset suficiente não habilita fusão
- [ ] `MegaExpertPipeline.select_candidates()` separa aprovados (passam no gate) de bloqueados (não passam) — bloqueado NÃO enfrenta cliente
- [ ] `MegaExpert.handle_question()` funde as capacidades: a resposta agrega os fatos de TODOS os especialistas fundidos relevantes à pergunta (perguntas cross-domain recebem resposta completa, não metade + handoff)
- [ ] `MegaExpert.handle_question()` escala para humano — na mesma thread, com contexto acumulado — quando a pergunta exige especialidade não fundida; NUNCA retorna deflection
- [ ] `MegaExpertPipeline.run_fusion_report()` verifica o invariante de no-regression: o mega-expert pontua >= que cada especialista sozinho no eval da própria especialidade dele, e reporta o ganho cross-domain

### Técnicos

- [ ] Python 3.9+ com type hints
- [ ] `dataclasses` para todos os modelos de dados (`SpecialistAgent`, `BenchmarkResult`, `MegaExpert`, `FragmentationDiagnosis`, `EvalCase`, `MegaExpertResponse`, `FusionReport`)
- [ ] `score_answer()` é função pura: fatos respondidos + fatos exigidos → cobertura 0.0-1.0
- [ ] `beats_best_human()` é determinístico e sem estado
- [ ] `MegaExpert.conversation_state` acumula fatos entre perguntas respondidas na mesma thread
- [ ] Thresholds (`MIN_EVAL_CASES`, limiares de fragmentação) são constantes nomeadas no módulo

### Validação

- [ ] Cenário 1: Conversa fragmentada (6 handoffs, 3+ repetições, 2 deflections) → `is_fragmented == True`
- [ ] Cenário 2: Conversa unificada (0 handoffs, 1 escalonamento humano) → `is_fragmented == False`
- [ ] Cenário 3: Gate bloqueia fidelidade (0.71 < 0.83 e n=12 < 30) e aprova as outras 4
- [ ] Cenário 4: No-regression — mega-expert >= especialista solo em TODAS as 4 especialidades fundidas
- [ ] Cenário 5: Cross-domain — mega-expert >= 0.99 onde o melhor solo <= 0.6
- [ ] Cenário 6: Escalonamento com contexto, sem deflection, thread preservada

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│                 MEGA-EXPERT CONSOLIDATION PIPELINE                │
│                                                                   │
│  PARTE 1 — DIAGNÓSTICO                                            │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              FRAGMENTATION ANALYZER                       │     │
│  │                                                            │     │
│  │  Log da conversa:                                          │     │
│  │  ┌──────────────────────────────────────────────────────┐ │     │
│  │  │ customer → NUTRI → PROD → PAY → LOGI → LOYA → (volta) │ │     │
│  │  │    ▲ 6 handoffs   ▲ 4 repetições   ▲ 2 deflections   │ │     │
│  │  └──────────────────────────────────────────────────────┘ │     │
│  │  → FragmentationDiagnosis { is_fragmented: True }          │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              ▼                                      │
│  PARTE 2 — GATE SUPERHUMANO (antes de fundir)                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Specialista      agent  best_human  n_cases  gate      │     │
│  │  ┌──────────────┬───────┬────────────┬────────┬───────┐ │     │
│  │  │ NUTRI-001    │ 0.94  │   0.90     │   52   │  ✅   │ │     │
│  │  │ PROD-002     │ 0.91  │   0.89     │   48   │  ✅   │ │     │
│  │  │ PAY-003      │ 0.97  │   0.92     │   61   │  ✅   │ │     │
│  │  │ LOGI-004     │ 0.88  │   0.86     │   35   │  ✅   │ │     │
│  │  │ LOYA-005     │ 0.71  │   0.83     │   12   │  ❌   │ │     │
│  │  └──────────────┴───────┴────────────┴────────┴───────┘ │     │
│  │  Regra: agent >= best_human AND n >= 30                   │     │
│  │  ❌ bloqueado NÃO enfrenta cliente                        │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              ▼                                      │
│  PARTE 3 — FUSÃO                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                    MEGA EXPERT                            │     │
│  │                                                           │     │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │     │
│  │  │ NUTRI   │ │  PROD   │ │   PAY   │ │  LOGI   │        │     │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘        │     │
│  │       └───────────┴─────┬─────┴───────────┘              │     │
│  │                         ▼                                 │     │
│  │            fusão de capacidades (front único)             │     │
│  │                         │                                 │     │
│  │      ┌──────────────────┴──────────────────┐             │     │
│  │      ▼                                     ▼             │     │
│  │  pergunta na especialidade          pergunta cross-domain │     │
│  │  fundida? → resposta completa       → união de fatos de   │     │
│  │  (sem handoff, sem repetição)         2-3 especialistas   │     │
│  │                                                           │     │
│  │  pergunta em especialidade NÃO fundida (LOYA)?            │     │
│  │      ▼                                                    │     │
│  │  ESCALONAMENTO humano NA MESMA THREAD                     │     │
│  │  com conversation_state como contexto — nunca deflection  │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              FUSION REPORT                                 │     │
│  │                                                            │     │
│  │  Invariante no-regression (por especialidade fundida):     │     │
│  │    score_mega(exp_specialty) >= score_solo(exp_specialty)  │     │
│  │                                                            │     │
│  │  Ganho cross-domain:                                       │     │
│  │    mega: 1.00   melhor solo: 0.42   → gain: +0.58          │     │
│  └──────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnóstico (`FragmentationAnalyzer.diagnose`)
Implemente a contagem de sintomas de fragmentação a partir de um `ConversationLog`. O diagnóstico é o que justifica a consolidação: sem números, "experiência ruim" é anecdota.

### Parte 2 — Gate superhumano (`BenchmarkResult.beats_best_human` + `MegaExpertPipeline.select_candidates`)
Nenhum especialista funde antes de vencer o melhor humano individual com dataset suficiente. Implemente a regra do gate e a separação aprovados/bloqueados.

### Parte 3 — Pipeline de fusão (`MegaExpertPipeline.fuse` + `MegaExpert.handle_question` + `run_fusion_report`)
Funda os aprovados, responda perguntas single-domain e cross-domain sem handoff, escale com contexto o que não está fundido, e verifique o invariante de no-regression.

---

## 💻 Starter Code

```python
"""
Exercício 7 — Consolidar Especialistas em um Mega-Expert
Nível 3 — Arquitetura Avançada

Pipeline: diagnóstico de fragmentação → gate de benchmark superhumano
→ fusão em um único mega-expert voltado para o cliente.

Fonte do padrão: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-
a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-
around-ai-analysis.md:88-89 (seção 2.6, Mega-expert consolidation).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# CONSTANTES DE GATE E THRESHOLDS
# ============================================================================

MIN_EVAL_CASES = 30  # benchmark com dataset menor não habilita fusão

FRAGMENTATION_THRESHOLDS = {
    "handoffs": 3,      # 3+ handoffs entre robôs = fragmentado
    "repeats": 2,       # 2+ repetições de informação = fragmentado
    "deflections": 1,   # 1+ deflection = fragmentado
}


# ============================================================================
# DOMÍNIO: especialidades do KODA
# ============================================================================

class Specialty(Enum):
    NUTRITION_CONSULT = "nutrition_consult"            # consultoria nutricional
    PRODUCT_RECOMMENDATION = "product_recommendation"  # composição de carrinho
    PAYMENTS = "payments"                              # pix, parcelamento, reembolso
    LOGISTICS = "logistics"                            # entrega, rastreio, troca
    LOYALTY_RETENTION = "loyalty_retention"            # fidelidade, recompra


# ============================================================================
# PARTE 1 — DIAGNÓSTICO DE FRAGMENTAÇÃO
# ============================================================================

@dataclass
class Turn:
    """Um turno da conversa entre cliente e agentes."""
    speaker: str                     # "customer" ou id do agente
    text: str
    is_handoff: bool = False         # agente transferiu a conversa p/ outro agente
    repeats_info: bool = False       # agente pediu info que o cliente já deu
    is_deflection: bool = False      # agente despachou p/ canal externo sem resolver
    escalated_to_human: bool = False # agente escalonou p/ humano NA MESMA thread


@dataclass
class ConversationLog:
    """Log completo de uma conversa com um cliente."""
    session_id: str
    turns: list[Turn] = field(default_factory=list)


@dataclass
class FragmentationDiagnosis:
    """Diagnóstico quantitativo da fragmentação da experiência."""
    session_id: str
    total_turns: int
    handoff_count: int            # transferências entre robôs
    repeated_info_count: int      # vezes que o cliente repetiu informação
    deflection_count: int         # despachos para canal externo sem resolução
    distinct_agent_count: int     # quantos robôs diferentes atenderam
    human_escalations: int        # escalonamentos humanos (não são deflection!)

    def is_fragmented(self) -> bool:
        """
        TODO (Parte 1): retornar True quando a conversa exceder QUALQUER
        um dos limiares de FRAGMENTATION_THRESHOLDS:
          handoff_count  >= thresholds["handoffs"]
          OR repeated_info_count >= thresholds["repeats"]
          OR deflection_count     >= thresholds["deflections"]
        """
        # TODO: Implementar
        pass


class FragmentationAnalyzer:
    """Analisa logs de conversa e produz diagnósticos de fragmentação."""

    @staticmethod
    def diagnose(log: ConversationLog) -> FragmentationDiagnosis:
        """
        TODO (Parte 1): percorrer os turnos e contar:
          - handoff_count:        turnos com is_handoff=True
          - repeated_info_count:  turnos com repeats_info=True
          - deflection_count:     turnos com is_deflection=True
          - human_escalations:    turnos com escalated_to_human=True
          - distinct_agent_count: speakers distintos != "customer"
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 2 — GATE SUPERHUMANO
# ============================================================================

@dataclass
class BenchmarkResult:
    """
    Benchmark do agente especialista contra o MELHOR HUMANO INDIVIDUAL
    já contratado na especialidade — não contra a média da equipe.
    """
    specialty: Specialty
    agent_score: float        # 0.0-1.0 no eval da especialidade
    best_human_score: float   # 0.0-1.0, melhor humano individual
    eval_case_count: int      # tamanho do dataset de avaliação

    def beats_best_human(self) -> bool:
        """
        TODO (Parte 2): retornar True somente quando:
          1. agent_score >= best_human_score  (barra superhumana)
          2. eval_case_count >= MIN_EVAL_CASES (dataset suficiente)
        Benchmark pequeno não autoriza fusão — evals fracos degradam
        a confiança do gate inteiro.
        """
        # TODO: Implementar
        pass


@dataclass
class SpecialistAgent:
    """
    Um agente especialista de UMA especialidade, com benchmark anexado.

    A simulação de resposta usa fatos: `facts` mapeia pergunta → conjunto
    de fatos que a resposta do especialista cobre.
    """
    agent_id: str
    specialty: Specialty
    benchmark: BenchmarkResult
    facts: dict[str, set[str]] = field(default_factory=dict)

    def answer(self, question: str) -> set[str]:
        """Fatos cobertos pela resposta deste especialista à pergunta."""
        return set(self.facts.get(question, set()))

    def qualifies_for_fusion(self) -> bool:
        """TODO (Parte 2): delegar para benchmark.beats_best_human()."""
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 3 — MEGA-EXPERT E PIPELINE DE FUSÃO
# ============================================================================

@dataclass
class EvalCase:
    """Um caso de eval: pergunta, fatos exigidos, especialidades exigidas."""
    case_id: str
    question: str
    required_facts: set[str]
    required_specialties: set[Specialty]

    @property
    def cross_domain(self) -> bool:
        """Caso cross-domain exige 2+ especialidades na mesma resposta."""
        return len(self.required_specialties) > 1


def score_answer(answered_facts: set[str], required_facts: set[str]) -> float:
    """
    TODO (Parte 3): cobertura da resposta = |respondidos ∩ exigidos| /
    |exigidos|. Função pura. Se exigidos é vazio, retornar 1.0.
    """
    # TODO: Implementar
    pass


def solo_score(agent: SpecialistAgent, suite: list[EvalCase]) -> float:
    """Score de um especialista agindo SOZINHO num suite de eval."""
    if not suite:
        return 0.0
    return sum(score_answer(agent.answer(c.question), c.required_facts) for c in suite) / len(suite)


@dataclass
class MegaExpertResponse:
    """Resposta do mega-expert a uma pergunta do cliente."""
    answer_facts: set[str] = field(default_factory=set)
    escalated: bool = False                 # humano entrou NA MESMA thread
    deflected: bool = False                 # ANTI-PADRÃO — deve ser sempre False
    escalation_context: list[str] = field(default_factory=list)


@dataclass
class MegaExpert:
    """
    O mega-expert: UM agente de frente para o cliente com as
    especialidades gateadas fundidas dentro.

    Invariantes:
      1. No-regression: score do mega no eval de cada especialidade
         fundida >= score do especialista solo no mesmo eval.
      2. Fusão soma capacidade: perguntas cross-domain recebem a UNIÃO
         dos fatos dos especialistas relevantes — nunca metade + handoff.
      3. Especialidade não fundida → escalonamento humano COM contexto,
         na mesma thread. deflected é sempre False.
    """
    mega_expert_id: str
    fused_specialists: list[SpecialtyAgent] = field(default_factory=list)
    conversation_state: set[str] = field(default_factory=set)  # fatos acumulados

    @property
    def covered_specialties(self) -> set[Specialty]:
        """TODO (Parte 3): especialidades com especialista fundido."""
        # TODO: Implementar
        pass

    def handle_question(
        self, question: str, required_specialties: set[Specialty]
    ) -> MegaExpertResponse:
        """
        TODO (Parte 3): responder UMA pergunta do cliente.

        Algoritmo:
          1. Se ALGUMA especialidade exigida não está em covered_specialties:
             - retornar MegaExpertResponse com escalated=True,
               answer_facts=vazio(), deflected=False
             - escalation_context = sorted(self.conversation_state) + [question]
               (o humano entra na thread COM o contexto acumulado)
             - NÃO despachar para canal externo (deflection é anti-padrão)
          2. Senão:
             - union dos facts de TODOS os fused_specialists para `question`
             - acumular os fatos em self.conversation_state
             - retornar MegaExpertResponse(answer_facts=união)
        """
        # TODO: Implementar
        pass

    def run_eval(self, suite: list[EvalCase]) -> float:
        """
        TODO (Parte 3): score do mega-expert no suite — média de
        score_answer(handle_question(caso).answer_facts, caso.required_facts).
        """
        # TODO: Implementar
        pass


@dataclass
class FusionReport:
    """Relatório de verificação da fusão."""
    mega_expert_id: str
    per_specialty_scores: dict[Specialty, tuple[float, float]] = field(default_factory=dict)
    # ^ especialidade → (score_solo, score_mega)
    cross_domain_mega: float = 0.0
    cross_domain_best_solo: float = 0.0

    @property
    def no_regression_holds(self) -> bool:
        """TODO (Parte 3): mega >= solo em TODAS as especialidades fundidas."""
        # TODO: Implementar
        pass

    @property
    def cross_domain_gain(self) -> float:
        """TODO (Parte 3): quanto o mega supera o melhor solo no cross-domain."""
        # TODO: Implementar
        pass


class MegaExpertPipeline:
    """Pipeline completo: gate → fusão → verificação."""

    @staticmethod
    def select_candidates(
        specialists: list[SpecialistAgent],
    ) -> tuple[list[SpecialistAgent], list[SpecialistAgent]]:
        """
        TODO (Parte 2): separar (aprovados, bloqueados) pelo gate
        superhumano. Bloqueado NÃO enfrenta cliente.
        """
        # TODO: Implementar
        pass

    @staticmethod
    def fuse(mega_expert_id: str, approved: list[SpecialistAgent]) -> MegaExpert:
        """TODO (Parte 3): construir o MegaExpert com os aprovados."""
        # TODO: Implementar
        pass

    @staticmethod
    def run_fusion_report(
        mega: MegaExpert,
        approved: list[SpecialistAgent],
        per_specialty_suites: dict[Specialty, list[EvalCase]],
        cross_domain_suite: list[EvalCase],
    ) -> FusionReport:
        """
        TODO (Parte 3): montar o FusionReport:
          - per_specialty_scores: para cada especialista aprovado,
            (solo_score(agente, suite_da_especialidade),
             mega.run_eval(suite_da_especialidade))
          - cross_domain_mega: mega.run_eval(cross_domain_suite)
          - cross_domain_best_solo: melhor solo_score no cross_domain_suite
        """
        # TODO: Implementar
        pass


# ============================================================================
# DADOS DE TESTE (determinísticos)
# ============================================================================

def build_koda_specialists() -> list[SpecialistAgent]:
    """
    5 especialistas do KODA. 4 batem o melhor humano; fidelidade (LOYA-005)
    ainda não — 0.71 < 0.83 e dataset n=12 < MIN_EVAL_CASES.
    """
    return [
        SpecialistAgent(
            agent_id="NUTRI-001",
            specialty=Specialty.NUTRITION_CONSULT,
            benchmark=BenchmarkResult(Specialty.NUTRITION_CONSULT, 0.94, 0.90, 52),
            facts={
                "creatina_treino": {"creatina_ok_treino", "hidratacao_aumentada"},
                "dose_whey": {"30g_por_dose", "janela_pos_treino"},
                # cross-domain (com PAY-003):
                "creatina_hipertensao_pix": {"cuidado_hipertensao"},
                # cross-domain (com PROD-002 e PAY-003):
                "stack_emagrecimento_reembolso": {"tireoide_alerta"},
            },
        ),
        SpecialistAgent(
            agent_id="PROD-002",
            specialty=Specialty.PRODUCT_RECOMMENDATION,
            benchmark=BenchmarkResult(Specialty.PRODUCT_RECOMMENDATION, 0.91, 0.89, 48),
            facts={
                "whey_isolado_vs_concentrado": {"isolado_menos_lactose", "concentrado_mais_barato"},
                "stack_emagrecimento_reembolso": {"termogenico_top", "bundle_15_off"},
            },
        ),
        SpecialistAgent(
            agent_id="PAY-003",
            specialty=Specialty.PAYMENTS,
            benchmark=BenchmarkResult(Specialty.PAYMENTS, 0.97, 0.92, 61),
            facts={
                "pix_parcelado": {"pix_5_off", "parcela_sem_juros_3x"},
                "creatina_hipertensao_pix": {"pix_reembolso_7d"},
                "stack_emagrecimento_reembolso": {"reembolso_integral_30d"},
            },
        ),
        SpecialistAgent(
            agent_id="LOGI-004",
            specialty=Specialty.LOGISTICS,
            benchmark=BenchmarkResult(Specialty.LOGISTICS, 0.88, 0.86, 35),
            facts={
                "prazo_entrega_capital": {"prazo_2_dias_uteis", "frete_gratis_acima_149"},
                "troca_produto": {"troca_ate_7d", "envio_reverso_gratuito"},
            },
        ),
        SpecialistAgent(
            agent_id="LOYA-005",
            specialty=Specialty.LOYALTY_RETENTION,
            benchmark=BenchmarkResult(Specialty.LOYALTY_RETENTION, 0.71, 0.83, 12),
            facts={
                "pontos_expiram": {"pontos_validos_12m", "resgate_min_500"},
                "recompra_desconto": {"cupom_aniversario_mes"},
            },
        ),
    ]


def build_per_specialty_suites() -> dict[Specialty, list[EvalCase]]:
    """Suites single-domain — um por especialidade."""
    return {
        Specialty.NUTRITION_CONSULT: [
            EvalCase("NC-01", "creatina_treino",
                     {"creatina_ok_treino", "hidratacao_aumentada"},
                     {Specialty.NUTRITION_CONSULT}),
            EvalCase("NC-02", "dose_whey",
                     {"30g_por_dose", "janela_pos_treino"},
                     {Specialty.NUTRITION_CONSULT}),
        ],
        Specialty.PRODUCT_RECOMMENDATION: [
            EvalCase("PR-01", "whey_isolado_vs_concentrado",
                     {"isolado_menos_lactose", "concentrado_mais_barato"},
                     {Specialty.PRODUCT_RECOMMENDATION}),
        ],
        Specialty.PAYMENTS: [
            EvalCase("PA-01", "pix_parcelado",
                     {"pix_5_off", "parcela_sem_juros_3x"},
                     {Specialty.PAYMENTS}),
        ],
        Specialty.LOGISTICS: [
            EvalCase("LO-01", "prazo_entrega_capital",
                     {"prazo_2_dias_uteis", "frete_gratis_acima_149"},
                     {Specialty.LOGISTICS}),
            EvalCase("LO-02", "troca_produto",
                     {"troca_ate_7d", "envio_reverso_gratuito"},
                     {Specialty.LOGISTICS}),
        ],
        Specialty.LOYALTY_RETENTION: [
            EvalCase("LR-01", "pontos_expiram",
                     {"pontos_validos_12m", "resgate_min_500"},
                     {Specialty.LOYALTY_RETENTION}),
        ],
    }


def build_cross_domain_suite() -> list[EvalCase]:
    """
    Casos que atravessam especialidades — a pergunta da Marina.
    Solo cobre no máximo metade (XD-01) ou um terço (XD-02) dos fatos.
    """
    return [
        EvalCase("XD-01", "creatina_hipertensao_pix",
                 {"cuidado_hipertensao", "pix_reembolso_7d"},
                 {Specialty.NUTRITION_CONSULT, Specialty.PAYMENTS}),
        EvalCase("XD-02", "stack_emagrecimento_reembolso",
                 {"tireoide_alerta", "termogenico_top", "reembolso_integral_30d"},
                 {Specialty.NUTRITION_CONSULT, Specialty.PRODUCT_RECOMMENDATION,
                  Specialty.PAYMENTS}),
    ]


def build_fragmented_log() -> ConversationLog:
    """A conversa da Marina ANTES: 5 robôs, 6 handoffs, 4 repetições, 2 deflections."""
    customer = "customer"
    return ConversationLog("KODA-2026-08-30-FRAGMENTADA", [
        Turn(customer, "Oi! Tomo remédio pra pressão. Posso tomar creatina? E Pix reembolsa?"),
        Turn("NUTRI-BOT", "Composição de produto não é comigo. Transferindo pro PROD-BOT.", is_handoff=True),
        Turn("PROD-BOT", "Bem-vinda! CPF, e-mail e número do pedido, por favor."),
        Turn(customer, "Já passei tudo no início da conversa..."),
        Turn("PROD-BOT", "Não tenho acesso ao histórico do outro atendente. Repita o CPF.", repeats_info=True),
        Turn(customer, "333.444.555-66. E sobre a creatina com pressão alta?"),
        Turn("PROD-BOT", "Sobre nutricionismo, consulte futanbear.com/blog/saude", is_deflection=True),
        Turn(customer, "Quero comprar, não ler blog..."),
        Turn("PROD-BOT", "Pagamentos são com o PAY-BOT. Transferindo.", is_handoff=True),
        Turn("PAY-BOT", "Pedido Pix registrado! Antes, confirma o CPF pra mim?", repeats_info=True),
        Turn(customer, "De novo?? 333.444.555-66."),
        Turn("PAY-BOT", "Trocas e prazos são com o LOGI-BOT.", is_handoff=True),
        Turn("LOGI-BOT", "Olá! Meu sistema mostra outro CPF. Repete o seu?", repeats_info=True),
        Turn(customer, "SERIAMENTE? 333.444.555-66. Vocês têm programa de pontos? Compro todo mês."),
        Turn("LOGI-BOT", "Fidelidade é o LOYA-BOT. Transferindo.", is_handoff=True),
        Turn("LOYA-BOT", "Pra consultar pontos, acesse o portal: futanbear.com/minha-conta", is_deflection=True),
        Turn(customer, "Pelo app não dá?"),
        Turn("LOYA-BOT", "Pontos é só no portal. Outra coisa? Retorno ao NUTRI-BOT.", is_handoff=True),
        Turn("NUTRI-BOT", "Aqui é nutrição. Pagamentos resolve no PAY-BOT.", is_handoff=True),
        Turn("PAY-BOT", "Bem-vindo de volta! Me confirma CPF e e-mail?", repeats_info=True),
        Turn(customer, "Tchau."),
    ])


def build_unified_log() -> ConversationLog:
    """
    A conversa da Marina DEPOIS: mega-expert responde tudo numa thread.
    A pergunta de fidelidade (especialidade ainda não gateada) escala
    para humano COM contexto — e a thread continua depois.
    """
    customer = "customer"
    return ConversationLog("KODA-2026-08-30-UNIFICADA", [
        Turn(customer, "Oi! Tomo remédio pra pressão. Posso tomar creatina? E Pix reembolsa?"),
        Turn("MEGA-KODA", "Compressão controlada + creatina: ok com acompanhamento. "
                          "Pix hoje tem 5% off e reembolso em 7 dias."),
        Turn(customer, "E um stack pra emagrecer? Pode reembolsar se não me adaptar?"),
        Turn("MEGA-KODA", "Termogênico + alerta de tireoide + reembolso integral em 30d."),
        Turn(customer, "Meus pontos de fidelidade valem desconto nessa compra?"),
        Turn("MEGA-KODA", "Fidelidade: humano entrando NA CONVERSA com todo o contexto.",
             escalated_to_human=True),
        Turn("MEGA-KODA", "Humano resolveu os pontos. Seguimos com o fechamento do pedido."),
    ])


# ============================================================================
# TESTES
# ============================================================================

def test_diagnostico_conversa_fragmentada():
    """Cenário 1: conversa fragmentada → is_fragmented True."""
    print("\n" + "=" * 60)
    print("TESTE 1: Diagnóstico — Conversa Fragmentada")
    print("=" * 60)

    diag = FragmentationAnalyzer.diagnose(build_fragmented_log())

    print(f"\n  Handoffs:            {diag.handoff_count}")
    print(f"  Repetições:          {diag.repeated_info_count}")
    print(f"  Deflections:         {diag.deflection_count}")
    print(f"  Robôs distintos:     {diag.distinct_agent_count}")

    assert diag.handoff_count >= 5, "Log fragmentado tem 5+ handoffs"
    assert diag.repeated_info_count >= 3, "Log fragmentado tem 3+ repetições"
    assert diag.deflection_count >= 2, "Log fragmentado tem 2+ deflections"
    assert diag.distinct_agent_count >= 4, "5 robôs distintos na conversa"
    assert diag.is_fragmented(), "Conversa fragmentada deve diagnosticar is_fragmented"
    print("  TESTE 1 PASSOU")


def test_diagnostico_conversa_unificada():
    """Cenário 2: mega-expert numa thread → is_fragmented False."""
    print("\n" + "=" * 60)
    print("TESTE 2: Diagnóstico — Conversa Unificada")
    print("=" * 60)

    diag = FragmentationAnalyzer.diagnose(build_unified_log())

    print(f"\n  Handoffs:            {diag.handoff_count}")
    print(f"  Deflections:         {diag.deflection_count}")
    print(f"  Escalonamentos:      {diag.human_escalations}")

    assert diag.handoff_count == 0, "Mega-expert não gera handoffs"
    assert diag.deflection_count == 0, "Mega-expert não gera deflections"
    assert diag.human_escalations == 1, "Fidelidade escala 1x para humano"
    assert not diag.is_fragmented(), "Conversa unificada não é fragmentada"
    print("  TESTE 2 PASSOU")


def test_gate_benchmark_superhumano():
    """Cenário 3: gate aprova 4, bloqueia fidelidade."""
    print("\n" + "=" * 60)
    print("TESTE 3: Gate Superhumano")
    print("=" * 60)

    specialists = build_koda_specialists()
    approved, blocked = MegaExpertPipeline.select_candidates(specialists)

    approved_set = {s.specialty for s in approved}
    blocked_set = {s.specialty for s in blocked}

    print(f"\n  Aprovados:  {sorted(a.value for a in approved_set)}")
    print(f"  Bloqueados: {sorted(b.value for b in blocked_set)}")

    assert len(approved) == 4, "Exatamente 4 especialistas passam no gate"
    assert Specialty.LOYALTY_RETENTION in blocked_set, "Fidelidade NÃO passou no gate"
    for s in approved:
        assert s.benchmark.beats_best_human(), (
            f"{s.agent_id} aprovado deve bater o melhor humano"
        )
    loya = next(s for s in specialists if s.agent_id == "LOYA-005")
    assert not loya.benchmark.beats_best_human(), (
        "0.71 < 0.83 e n=12 < 30: fidelidade não bate o gate"
    )
    print("  TESTE 3 PASSOU")


def test_fusao_sem_regressao():
    """Cenário 4: mega >= solo em TODAS as especialidades fundidas."""
    print("\n" + "=" * 60)
    print("TESTE 4: Fusão — Invariante de No-Regression")
    print("=" * 60)

    specialists = build_koda_specialists()
    approved, _ = MegaExpertPipeline.select_candidates(specialists)
    mega = MegaExpertPipeline.fuse("MEGA-KODA-001", approved)
    report = MegaExpertPipeline.run_fusion_report(
        mega, approved, build_per_specialty_suites(), build_cross_domain_suite()
    )

    for specialty, (solo, fused) in report.per_specialty_scores.items():
        print(f"\n  {specialty.value:24s} solo={solo:.2f}  mega={fused:.2f}")
        assert fused >= solo, (
            f"No-regression violado em {specialty.value}: "
            f"mega ({fused:.2f}) < solo ({solo:.2f})"
        )

    assert report.no_regression_holds, "Invariante de no-regression deve segurar"
    print("\n  TESTE 4 PASSOU")


def test_fusao_cross_domain():
    """Cenário 5: cross-domain — mega completo, solo pela metade."""
    print("\n" + "=" * 60)
    print("TESTE 5: Fusão — Ganho Cross-Domain")
    print("=" * 60)

    specialists = build_koda_specialists()
    approved, _ = MegaExpertPipeline.select_candidates(specialists)
    mega = MegaExpertPipeline.fuse("MEGA-KODA-001", approved)
    report = MegaExpertPipeline.run_fusion_report(
        mega, approved, build_per_specialty_suites(), build_cross_domain_suite()
    )

    cross_suite = build_cross_domain_suite()
    print(f"\n  Mega no cross-domain:        {report.cross_domain_mega:.2f}")
    print(f"  Melhor solo no cross-domain: {report.cross_domain_best_solo:.2f}")
    print(f"  Ganho:                       {report.cross_domain_gain:+.2f}")

    assert report.cross_domain_mega >= 0.99, (
        "Mega-expert responde perguntas cross-domain por completo"
    )
    for s in approved:
        solo = solo_score(s, cross_suite)
        assert solo <= 0.6, (
            f"{s.agent_id} solo deve cobrir no máximo metade do cross-domain, "
            f"obteve {solo:.2f}"
        )
    assert report.cross_domain_gain > 0, "Fusão deve gerar ganho cross-domain"
    print("  TESTE 5 PASSOU")


def test_escalonamento_sem_deflection():
    """Cenário 6: especialidade não fundida → humano com contexto, nunca deflection."""
    print("\n" + "=" * 60)
    print("TESTE 6: Escalonamento Contextual (não deflection)")
    print("=" * 60)

    specialists = build_koda_specialists()
    approved, _ = MegaExpertPipeline.select_candidates(specialists)
    mega = MegaExpertPipeline.fuse("MEGA-KODA-001", approved)

    # Conversa flui normalmente em 2 perguntas fundidas (acumula contexto)
    r1 = mega.handle_question(
        "creatina_hipertensao_pix",
        {Specialty.NUTRITION_CONSULT, Specialty.PAYMENTS},
    )
    r2 = mega.handle_question(
        "stack_emagrecimento_reembolso",
        {Specialty.NUTRITION_CONSULT, Specialty.PRODUCT_RECOMMENDATION, Specialty.PAYMENTS},
    )
    assert not r1.escalated and r1.answer_facts, "Pergunta fundida responde direto"
    assert not r2.escalated and r2.answer_facts, "Pergunta fundida responde direto"

    # Pergunta de fidelidade — especialidade BLOQUEADA no gate
    r3 = mega.handle_question(
        "pontos_expiram", {Specialty.LOYALTY_RETENTION}
    )

    print(f"\n  Escalado:      {r3.escalated}")
    print(f"  Defletido:     {r3.deflected}")
    print(f"  Contexto:      {r3.escalation_context}")

    assert r3.escalated, "Especialidade não fundida escala para humano"
    assert not r3.deflected, "Mega-expert NUNCA deflectiona"
    assert r3.answer_facts == set(), "Sem resposta inventada fora da fronteira"
    assert "pontos_expiram" in r3.escalation_context, (
        "Contexto inclui a pergunta que disparou o escalonamento"
    )
    assert len(r3.escalation_context) > 1, (
        "Contexto inclui os fatos já acumulados da thread"
    )
    # Thread preservada: o estado da conversa sobrevive ao escalonamento
    r4 = mega.handle_question(
        "pix_parcelado", {Specialty.PAYMENTS}
    )
    assert r4.answer_facts and not r4.escalated, (
        "Após escalonamento, a MESMA thread continua respondendo"
    )
    print("  TESTE 6 PASSOU")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 7: MEGA-EXPERT CONSOLIDATION")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_diagnostico_conversa_fragmentada()
    # test_diagnostico_conversa_unificada()
    # test_gate_benchmark_superhumano()
    # test_fusao_sem_regressao()
    # test_fusao_cross_domain()
    # test_escalonamento_sem_deflection()

    print("\nTODO: Implemente as partes acima!")
    print("   1. FragmentationAnalyzer.diagnose() + FragmentationDiagnosis.is_fragmented()")
    print("   2. BenchmarkResult.beats_best_human() + SpecialistAgent.qualifies_for_fusion()")
    print("   3. MegaExpertPipeline.select_candidates() / fuse() / run_fusion_report()")
    print("   4. score_answer() + MegaExpert.covered_specialties / handle_question / run_eval")
    print("   5. FusionReport.no_regression_holds / cross_domain_gain")
    print("   Após implementar, descomente os testes em main()")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

### Critério 1: Diagnóstico de fragmentação (Parte 1)

- [ ] `diagnose()` conta handoffs, repetições, deflections e robôs distintos corretamente
- [ ] `escalated_to_human` NÃO conta como deflection nem handoff (escalamento fica na mesma thread)
- [ ] Conversa fragmentada: `is_fragmented() == True`
- [ ] Conversa unificada: `is_fragmented() == False` com `human_escalations == 1`

### Critério 2: Gate superhumano (Parte 2)

- [ ] `beats_best_human()` exige `agent_score >= best_human_score` E `eval_case_count >= 30`
- [ ] LOYA-005 (0.71 vs 0.83, n=12) bloqueado; os outros 4 aprovados
- [ ] `select_candidates()` retorna `(aprovados, bloqueados)` com 4 e 1 elementos

### Critério 3: Fusão e no-regression (Parte 3)

- [ ] `handle_question()` une os fatos de todos os especialistas fundidos relevantes
- [ ] Pergunta cross-domain (`creatina_hipertensao_pix`) responde completa — 0 handoffs
- [ ] `run_eval()` do mega no eval de cada especialidade fundida >= score solo
- [ ] `FusionReport.no_regression_holds == True` e `cross_domain_gain > 0`

### Critério 4: Escalonamento contextual (Parte 3)

- [ ] Especialidade não fundida → `escalated=True`, `deflected=False`, `answer_facts` vazio
- [ ] `escalation_context` contém a pergunta E os fatos acumulados da thread
- [ ] A thread continua respondendo depois do escalonamento

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnóstico (Parte 1)** | 20% | Não implementado | Conta turnos mas confunde handoff com escalamento | Contadores corretos + limiares aplicados | Diagnóstico completo distinguindo deflection de escalonamento humano |
| **Gate Superhumano (Parte 2)** | 25% | Não implementado | Compara só scores | Compara scores E tamanho do dataset | Gate como regra única e testável, bloqueados explícitos, justificativa da barra contra o melhor humano |
| **Fusão + No-Regression (Parte 3)** | 35% | Não implementado | Mega responde mas degrada especialidade | União de fatos + invariante segurando nos 4 suits | Fusão completa com cross-domain fechado, ganho quantificado e report auditável |
| **Escalonamento Contextual (Parte 3)** | 20% | Não implementado | Escalona sem contexto | Contexto acumulado + thread preservada | Contraste explícito deflection × escalonamento fechado na mesma thread |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

### Para o diagnóstico

1. **Escalonamento humano não é sintoma de fragmentação.** É a saída correta quando a especialidade ainda não bateu o melhor humano. Os sintomas são handoffs entre robôs, repetição de informação e deflection — três formas diferentes de empurrar o cliente.
2. **O diagnóstico justifica o projeto.** "6 handoffs, 3 repetições, 2 deflections, 0 perguntas fechadas" é o que transforma reclamação difusa em caso de consolidação.

### Para o gate

1. **A barra é o melhor humano individual, não a média.** `best_human_score` representa o melhor já contratado — fusão de medianos produz um mediano integrado, que perde para o especialista humano original (`...analysis.md:26-28`).
2. **Dataset pequeno invalida o benchmark.** n=12 casos não autoriza declarar superhumanidade. O gate aqui reflete o princípio de que evals são projetados junto com o agente, não deixados para depois (`...analysis.md:162`).
3. **Bloqueado ≠ descartado.** O especialista bloqueado continua em treino/eval até bater a barra — só não enfrenta cliente enquanto isso.

### Para a fusão

1. **Fusão soma, nunca subtrai.** O invariante de no-regression (`mega >= solo` por especialidade) é o que separa fusão de diluição. Se sua fusão derruba qualquer especialidade abaixo do score solo, ela é uma regressão arquitetural.
2. **O valor da fusão mora no cross-domain.** A pergunta da Marina (`creatina + hipertensão + Pix`) é intratável para qualquer especialista solo (máx 0.5) e trivial para o mega (1.0). Esse delta — não a economia de bots — é o business case.
3. **Mega-expert não é mega-prompt.** Dentro do mega-expert as especialidades continuam decompostas e gateadas individualmente; o repositório escala por decomposição, não por prompts densos (`docs/canonical/goal-atomicity-split.md:92`). Não "resolva" o exercício colapsando os especialistas num único blob.

### Para o escalonamento

1. **Deflection abre mão do cliente; escalonamento contrata um humano.** A diferença mecânica: no escalonamento o contexto viaja junto (`conversation_state`) e a thread continua depois que o humano resolve. Deflection joga o cliente para outro canal e esquece — o anti-padrão open-loop (`...analysis.md:164`).

---

## ❓ Dúvidas Comuns

**P: Isso não vira um mega-prompt denso com 5 especialidades?**
R: Não. O mega-expert funde a *fronteira com o cliente* e o *gate de benchmark* — internamente as especialidades continuam decompostas, cada uma com eval próprio. O anti-padrão "dense mega-prompts" é explicitamente rejeitado pelo repo (`docs/canonical/goal-atomicity-split.md:92`): escala-se por decomposição, um outcome por intenção. Se sua implementação depende de um prompt único gigante, ela está no padrão errado.

**P: Por que benchmark contra o melhor humano e não contra a média da equipe?**
R: Porque a barra define a arquitetura. "Bom o suficiente" produz deflection bots; "melhor que o melhor humano já contratado" produz mega-expert (`...analysis.md:148`). Comparar com a média aprovaria mediocridade para fusão — e um mega-expert fundido a partir de medianos perde para o humano especialista que ele deveria superar.

**P: O que faço com a especialidade bloqueada no gate?**
R: Mantenha-a longe do cliente e escale para humano com contexto — enquanto investe no eval dela. O bloqueio é temporário por construção: quando `agent_score >= best_human_score` com dataset suficiente, ela entra na fusão pelo mesmo gate.

**P: Qual a relação com o Exercício 5 (persona-based documentation)?**
R: São vizinhos, não duplicatas. O `docs/canonical/persona-based-documentation.md:23` parte do mesmo problema — especialistas cujo conhecimento não é capturado — mas resolve com *documentação* que agentes carregam. Aqui a unidade é o *agente especialista com benchmark* e a fusão é arquitetural. No KODA real, os dois se compõem: a persona documenta o conhecimento, o gate decide quem funde.

**P: Por que escalonamento não conta como fragmentação no diagnóstico?**
R: Fragmentação é o cliente sendo *empurrado* (handoff/repetição/deflection) — ninguém resolve nada. Escalonamento contextual é o sistema *puxando* um humano qualificado para uma especialidade que ainda não bateu a barra, sem perder a thread. Um é o sintoma da doença; o outro é o tratamento temporário.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia a seção 2.6 ("Mega-expert consolidation") e a seção 5 (failure patterns) em `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:88-89` — e a entrada completa da classificação `Missing` em `...classification.yaml:315-335`
2. Compare com `docs/canonical/persona-based-documentation.md:23` — mesmo problema de partida (conhecimento de especialistas não capturado), solução diferente (docs vs. fusão de agentes com gate)
3. (Opcional) Extensão KODA: conecte o `MegaExpert` aos journey states do Nível 4 (`curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:715-722`) — o mega-expert é quem sustenta "construir relacionamento de longo prazo" sem quebrar a thread entre DISCOVERY, PURCHASE e RETENTION

---

*Exercício 7 | Nível 3 — Arquitetura Avançada | Mega-Expert Consolidation*

**Nenhum especialista funde antes de vencer o melhor humano. Nenhum cliente entregue a um robô de despacho.**
