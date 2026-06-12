---
title: "Exercício 4: Projetar o Papel de Owner-of-No"
type: curriculum-exercise
nivel: 3
aliases: ["owner of no", "dono da recusa", "refusal owner", "role design", "negativa construtiva", "accountability negativa"]
tags: [curriculo-conteudo, nivel-3, exercicio, governanca, agentes-orquestracao, decision-discipline, role-design, refusal-ownership, accountability, harness-governance, python, dataclass]
relates-to: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]"]
last_updated: 2026-06-11
---

# 🚫 Exercício 4: Projetar o Papel de Owner-of-No
## Nível 3 — Arquiteto

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** ⭐⭐⭐ (Intermediário-Avançado)
**Pré-requisito:** Ter completado os módulos de governança do Nível 3 + `docs/canonical/split-brain-planning-review.md`
**Objetivo:** Projetar e formalizar um papel organizacional cuja responsabilidade explícita é recusar trabalho de baixo valor — transformando o "não" de um ato de coragem individual em uma função de design do harness

---

## 📖 Prólogo: A Sala Onde Ninguém Podia Dizer Não

**Quarta-feira, 10h. Planejamento de sprint do time KODA.**

A reunião tinha 14 cards na pauta. O time tinha capacidade para 7. Todo mundo sabia disso. Mas a dinâmica era previsível:

```
Product Manager: "Beleza, primeiro card: recomendação cross-sell 
                  baseada em histórico de navegação."

Tech Lead: "Faz sentido. O agente consegue?"

Dev Senior: "Consegue. O modelo novo tem grounding factual. 
             Umas 4 horas de tokens."

Product Manager: "Segundo: dashboard de analytics com filtro 
                  por persona."

Tech Lead: "Os PMs pediram isso?"

Product Manager: "Na verdade... ninguém pediu. Mas seria legal 
                 ter. E o agente faz rápido."

Tech Lead: "Ok. Terceiro: pipeline de dados..."

[90 minutos depois]

Product Manager: "Fechamos 14 cards. Todo mundo confortável?"

[Silêncio. Ninguém disse não. Mas ninguém disse sim também.]

Dev Senior (baixinho, para o colega do lado): 
    "Metade disso ninguém pediu. A outra metade ninguém sabe 
     se funciona. Mas... quem sou eu para dizer não?"
```

Essa reunião se repetiu por 6 meses. O resultado:

```
═══════════════════════════════════════════════════════════════
          6 MESES DE PLANEJAMENTO SEM RECUSA
             Janeiro – Junho 2026
═══════════════════════════════════════════════════════════════

Cards aceitos no planejamento:        312
Cards completados:                    287
Cards que chegaram a usuário real:     41  (14%)
Cards que alguém pediu:                38  (13%)
Cards que mudaram métrica de negócio:   7  (2.4%)

"Quem disse não a algum card?":        0 pessoas, 0 vezes
═══════════════════════════════════════════════════════════════
```

O problema não era que as pessoas não sabiam identificar trabalho de baixo valor. Era que **ninguém era pago para fazer isso**. Nenhum papel no time incluía "recusar trabalho" na descrição. O Product Manager era pago para priorizar — mas priorizar é ordenar, não recusar. O Tech Lead era pago para garantir qualidade técnica — mas "não tem usuário" não é um problema técnico. O Engineering Manager era pago para entregar — e dizer não parece o oposto de entregar.

E então, numa retrospectiva trimestral, a arquiteta do time — Mariana — propôs algo que ninguém esperava:

```
Mariana: "O problema não é que a gente não sabe dizer não.
         O problema é que dizer não não é trabalho de ninguém.
         Está acontecendo por acidente — ou não acontecendo."

Tech Lead: "Mas eu digo não quando algo é tecnicamente inviável."

Mariana: "Exato. Você diz não ao INVIAVEL. Mas quem diz não 
         ao INÚTIL? Quem diz não ao 'ninguém pediu'? Quem diz 
         não ao 'é legal mas não agora'?"

Product Manager: "Tecnicamente... eu priorizo."

Mariana: "Priorizar é ordenar. O card que ficou em 14º ainda 
         está na lista. Ainda vai ser feito 'um dia'. Priorizar 
         não é recusar. Recusar é dizer: 'isso NUNCA deveria ser 
         construído, com ou sem tempo.'"

Dev Senior: "Então você está propondo... um papel novo?"

Mariana: "Estou propondo um Owner-of-No. Uma pessoa cujo trabalho 
         — explícito, documentado, avaliado — é recusar trabalho 
         que não deveria existir. Não é o vilão. Não é o chato. 
         É o papel que transforma o 'não' de um ato de coragem 
         individual em uma função de design do harness."
```

Ela projetou a descrição do papel:

```
╔═══════════════════════════════════════════════════════════════╗
║                    OWNER-OF-NO                                 ║
║                                                                ║
║  Responsabilidade primária:                                    ║
║    Recusar, deferir ou redirecionar trabalho de baixo valor    ║
║    antes que ele consuma tempo de agente e atenção do time.    ║
║                                                                ║
║  Autoridade:                                                   ║
║    - Pode recusar qualquer card sem necessidade de escalação   ║
║    - Pode exigir intents documentados antes da aprovação       ║
║    - Pode converter build requests em experiments time-boxed   ║
║    - NÃO pode aprovar — apenas recusar, deferir ou redirecionar║
║                                                                ║
║  Métrica de sucesso:                                           ║
║    - NÃO é "quantos cards recusou"                             ║
║    - SIM é "quantos cards recusados teriam sido construídos    ║
║      e abandonados sem usuário" — medido por follow-up em      ║
║      90 dias                                                   ║
║                                                                ║
║  A recusa é construtiva:                                       ║
║    - Todo "não" vem com um "em vez disso":                     ║
║      "Não vamos construir X. Em vez disso, vamos investigar    ║
║       se Y resolve o mesmo problema com 1/10 do esforço."      ║
╚═══════════════════════════════════════════════════════════════╝
```

```
Dev Junior: "Isso não vai criar atrito? Alguém cujo trabalho 
            é dizer não..."

Mariana: "O atrito já existe. A diferença é que hoje ele é 
         pessoal — 'o Paulo não gostou da minha ideia'. 
         Amanhã ele é estrutural — 'o Owner-of-No recusou 
         porque o card não tem intenção documentada'. 
         A primeira dói. A segunda é processo."

Tech Lead: "E quem seria o Owner-of-No?"

Mariana: "Essa é a pergunta errada. A pergunta certa é: qual 
         o PERFIL do Owner-of-No? Porque se for uma pessoa 
         específica, o papel morre quando a pessoa sai. 
         Se for um papel definido por atributos, qualquer um 
         com esses atributos pode ocupá-lo."
```

**Agora é a sua vez.**

Você é o arquiteto organizacional que vai projetar o papel de Owner-of-No. Você não está escolhendo uma pessoa — está projetando uma função. Sua missão: definir os atributos, a autoridade, os critérios de decisão, os limites do papel, e o protocolo de recusa construtiva. Depois, implementar um sistema que operacionaliza esse papel no harness de governança.

---

## 🎯 O Contexto

### O Problema: A Gravidade Natural Puxa Para Construir

Em times que usam agentes de IA para implementação, existe uma assimetria fundamental:

- **Construir** é fácil, rápido, barato, visível, e recompensado (métricas de velocidade, cards completados)
- **Recusar** é difícil, lento, invisível, e não recompensado (não aparece em nenhum dashboard)

Essa assimetria cria uma gravidade natural: tudo que pode ser construído, será construído. A única força contrária é a disciplina individual — alguém que, por coragem pessoal, diz "isso não deveria existir". Mas disciplina individual não escala. O que escala é papel desenhado.

### A Solução: Owner-of-No como Função de Design

O Owner-of-No não é uma pessoa. É um papel com cinco atributos:

| Atributo | Definição | Por Que Importa |
|---|---|---|
| **Autoridade explícita** | O papel tem autoridade documentada para recusar — não precisa convencer ninguém | Transforma "não" de ato político em ato processual |
| **Recusa construtiva** | Todo "não" vem com uma alternativa: investigar, experimentar, redirecionar, ou substituir | Impede que o papel seja visto como bloqueador |
| **Critérios objetivos** | A recusa é baseada em critérios públicos, não em opinião: usuário documentado? custo justificado? dono nomeado? | Remove subjetividade e favoritismo |
| **Limites definidos** | O papel NÃO aprova — apenas recusa, deferre, ou redireciona. A aprovação é de outro papel (Product Owner, Tech Lead) | Evita concentração de poder |
| **Accountability reversa** | Se o Owner-of-No recusou algo que depois se provou essencial, isso é um evento de aprendizado, não uma falha pessoal | Permite que o papel opere sem medo de errar |

### O Que Você Vai Construir

Você vai projetar e implementar dois artefatos:

1. **OwnerOfNoRoleSpec**: a especificação formal do papel (atributos, autoridade, limites, métricas)
2. **RefusalProtocol**: o protocolo operacional que o Owner-of-No segue ao avaliar uma requisição

Depois, vai implementar um `RefusalDecisionEngine` que aplica os critérios do Owner-of-No a um conjunto de cards reais do backlog do KODA, demonstrando que as recusas são baseadas em critérios objetivos, não em preferência pessoal.

---

## 📋 O Cenário: O Backlog Que Ninguém Recusou

### Dados de Entrada

Você recebe o backlog da sprint atual do time KODA. Cada card é uma `BuildRequest` que passou pelo planejamento sem nenhuma recusa:

```python
BACKLOG_CARDS = [
    {
        "card_id": "CARD-201",
        "title": "Recomendação cross-sell por histórico de navegação",
        "requester": "pm_fernanda",
        "has_documented_user": True,
        "user_count_affected": 1200,
        "user_pain_description": "Clientes compram 1 produto e abandonam. Perda estimada: R$ 8K/mês",
        "cost_proxy_survives": True,
        "cost_proxy_rationale": "R$ 8K/mês perdido vs R$ 3K de engenharia — se paga em 2 semanas",
        "has_refusal_owner": True,
        "refusal_owner": "Fernanda (PO)",
        "estimated_agent_tokens": 800000,
        "depends_on_unstable_service": False,
    },
    {
        "card_id": "CARD-202",
        "title": "Tema dark no dashboard interno de analytics",
        "requester": "dev_maria",
        "has_documented_user": False,
        "user_count_affected": 4,
        "user_pain_description": "",
        "cost_proxy_survives": False,
        "cost_proxy_rationale": "",
        "has_refusal_owner": False,
        "refusal_owner": "",
        "estimated_agent_tokens": 450000,
        "depends_on_unstable_service": False,
    },
    {
        "card_id": "CARD-203",
        "title": "Pipeline de re-treinamento semanal do modelo",
        "requester": "dev_joao",
        "has_documented_user": True,
        "user_count_affected": 1200,
        "user_pain_description": "Recomendações usam dados de 3 meses atrás — produtos fora de estoque",
        "cost_proxy_survives": True,
        "cost_proxy_rationale": "Perda de R$ 15K/mês vs R$ 8K one-time",
        "has_refusal_owner": True,
        "refusal_owner": "Rafael (Tech Lead)",
        "estimated_agent_tokens": 2800000,
        "depends_on_unstable_service": True,
    },
    {
        "card_id": "CARD-204",
        "title": "Migrar notificações de polling para WebSockets",
        "requester": "dev_carlos",
        "has_documented_user": False,
        "user_count_affected": 0,
        "user_pain_description": "",
        "cost_proxy_survives": False,
        "cost_proxy_rationale": "",
        "has_refusal_owner": False,
        "refusal_owner": "",
        "estimated_agent_tokens": 1500000,
        "depends_on_unstable_service": False,
    },
    {
        "card_id": "CARD-205",
        "title": "Exportação de relatório em PDF para clientes corporate",
        "requester": "pm_fernanda",
        "has_documented_user": True,
        "user_count_affected": 80,
        "user_pain_description": "Clientes corporate (B2B) precisam de relatório mensal. Hoje é manual: 4h/semana",
        "cost_proxy_survives": True,
        "cost_proxy_rationale": "4h/semana × R$ 200/h × 52 semanas = R$ 41.600/ano. Custo: R$ 5K one-time",
        "has_refusal_owner": True,
        "refusal_owner": "Fernanda (PO)",
        "estimated_agent_tokens": 1200000,
        "depends_on_unstable_service": False,
    },
    {
        "card_id": "CARD-206",
        "title": "Refatorar sistema de cache de sessão (Redis → memcached)",
        "requester": "dev_paulo",
        "has_documented_user": False,
        "user_count_affected": 0,
        "user_pain_description": "",
        "cost_proxy_survives": False,
        "cost_proxy_rationale": "",
        "has_refusal_owner": False,
        "refusal_owner": "",
        "estimated_agent_tokens": 900000,
        "depends_on_unstable_service": False,
    },
]
```

### Perfis dos Decisores

| Nome | Papel Atual | Pode Aprovar? | Pode Recusar? | Propensão a Recusar |
|---|---|---|---|---|
| Fernanda | Product Owner | Sim | Informalmente | Baixa — prioriza, não recusa |
| Rafael | Tech Lead | Sim | Informalmente | Média — recusa por inviabilidade técnica |
| Juliana | Engineering Manager | Não | Não | Nenhuma — focada em entrega |
| Owner-of-No | (papel novo) | NÃO | Sim — formalmente | Alta — avaliada por valor evitado |

---

## 📋 Requisitos

### Funcionais

- [ ] Definir `OwnerOfNoRoleSpec` com 5 atributos: autoridade, escopo, critérios, limites, métricas
- [ ] Definir `RefusalProtocol` com passos documentados: receber card → avaliar critérios → decidir → registrar
- [ ] A decisão do Owner-of-No é uma de: `APPROVE` (não recusa), `DEFER` (adiar com condições), `REDIRECT` (substituir por alternativa menor), `REFUSE` (recusar permanentemente)
- [ ] Toda decisão produz um `RefusalRecord` com card_id, decisão, critérios aplicados, alternativa oferecida, e racional
- [ ] O Owner-of-No NUNCA aprova — apenas não-recusa (APPROVE significa "não encontrei razão para recusar"). A aprovação final é de outro papel
- [ ] O protocolo registra métricas: taxa de recusa, valor estimado evitado, follow-up em 90 dias
- [ ] Critérios de recusa são objetivos e públicos — qualquer pessoa pode verificar se um card seria recusado

### Técnicos

- [ ] Python 3.9+ com type hints
- [ ] Usar `dataclasses` e `Enum` para os modelos
- [ ] `RefusalCriteria` encapsula os critérios de decisão (checks booleanos)
- [ ] `RefusalDecisionEngine.apply_criteria()` é uma função pura: card → decisão
- [ ] `RefusalLedger` armazena histórico de decisões e calcula métricas
- [ ] O sistema deve ser auditável: dado um card_id, é possível reconstruir exatamente por que foi recusado

### Validação

- [ ] Cenário 1: CARD-201 (cross-sell, usuário real, custo justificado) → APPROVE (não recusa)
- [ ] Cenário 2: CARD-202 (dark theme, sem usuário, sem custo) → REFUSE
- [ ] Cenário 3: CARD-203 (pipeline, usuário real mas depende de serviço instável) → DEFER (resolva dependência primeiro)
- [ ] Cenário 4: CARD-204 (WebSockets, sem usuário, alto custo) → REFUSE
- [ ] Cenário 5: CARD-205 (PDF corporate, usuário real, custo justificado) → APPROVE
- [ ] Cenário 6: CARD-206 (Redis→memcached, sem usuário) → REDIRECT (experimente com benchmark primeiro)

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│                     OWNER-OF-NO ROLE SYSTEM                        │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              OWNER-OF-NO ROLE SPEC                         │    │
│  │                                                            │    │
│  │  Atributos do papel:                                       │    │
│  │  ┌──────────────────────────────────────────────────────┐ │    │
│  │  │ 1. AUTORIDADE: Pode recusar, deferir, redirecionar    │ │    │
│  │  │    NÃO pode aprovar — aprovação é de outro papel      │ │    │
│  │  │                                                        │ │    │
│  │  │ 2. ESCOPO: Cards de build, features, experimentos      │ │    │
│  │  │    NÃO cobre: hotfixes, incidents, compliance          │ │    │
│  │  │                                                        │ │    │
│  │  │ 3. CRITÉRIOS: Objetivos, públicos, auditáveis          │ │    │
│  │  │    - Usuário documentado?                              │ │    │
│  │  │    - Custo justificado?                                │ │    │
│  │  │    - Dono da recusa nomeado?                           │ │    │
│  │  │    - Dependência instável?                             │ │    │
│  │  │                                                        │ │    │
│  │  │ 4. LIMITES: NÃO aprova, NÃO prioriza, NÃO implementa   │ │    │
│  │  │                                                        │ │    │
│  │  │ 5. MÉTRICAS: Valor evitado, taxa de recusa,            │ │    │
│  │  │    follow-up 90 dias, falsos positivos                 │ │    │
│  │  └──────────────────────────────────────────────────────┘ │    │
│  └───────────────────────────┬────────────────────────────────┘    │
│                              │                                      │
│                              ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              REFUSAL PROTOCOL                              │    │
│  │                                                            │    │
│  │  Para cada card recebido:                                  │    │
│  │                                                            │    │
│  │  PASSO 1: AVALIAR CRITÉRIOS                                │    │
│  │    ├── Tem usuário documentado com dor real?               │    │
│  │    ├── O custo sobrevive ao cost proxy (1 semana)?         │    │
│  │    ├── Tem dono da recusa nomeado?                         │    │
│  │    └── Depende de serviço instável ou não monitorado?      │    │
│  │                                                            │    │
│  │  PASSO 2: CLASSIFICAR                                      │    │
│  │    ├── Todos critérios passam → APPROVE (não recusa)       │    │
│  │    ├── Usuário OK mas dependência instável → DEFER         │    │
│  │    ├── Usuário OK mas escopo grande → REDIRECT             │    │
│  │    └── Sem usuário OU sem custo → REFUSE                   │    │
│  │                                                            │    │
│  │  PASSO 3: CONSTRUIR ALTERNATIVA                            │    │
│  │    ├── REFUSE: "Em vez disso, investigue se Y resolve"     │    │
│  │    ├── DEFER: "Resolva X primeiro, reenvie depois"         │    │
│  │    └── REDIRECT: "Experimente versão mínima de Z primeiro" │    │
│  │                                                            │    │
│  │  PASSO 4: REGISTRAR                                        │    │
│  │    └── RefusalRecord no RefusalLedger                      │    │
│  └───────────────────────────┬────────────────────────────────┘    │
│                              │                                      │
│                              ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              REFUSAL LEDGER                                │    │
│  │                                                            │    │
│  │  Histórico de decisões + métricas:                         │    │
│  │  - Taxa de recusa por mês                                  │    │
│  │  - Valor estimado evitado (tokens + manutenção)            │    │
│  │  - Follow-up: cards recusados que se provaram necessários  │    │
│  │  - Taxa de falsos positivos (recusou mas faria diferença)  │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### Matriz de Decisão do Owner-of-No

| Usuário Documentado | Custo Justificado | Dono Nomeado | Dependência Instável | Decisão |
|---|---|---|---|---|
| Sim | Sim | Sim | Não | APPROVE |
| Sim | Sim | Sim | Sim | DEFER (resolva dependência) |
| Sim | Sim | Não | Não | DEFER (designe owner) |
| Sim | Não | qualquer | qualquer | REDIRECT (reduza escopo) |
| Não | Sim | qualquer | qualquer | REDIRECT (investigue usuário) |
| Não | Não | qualquer | qualquer | REFUSE |
| qualquer | qualquer | qualquer | Sim (sem eval) | DEFER (adicione eval) |

---

## 🚀 Starter Code

```python
"""
Exercício 4 — Projetar o Papel de Owner-of-No
Nível 3 — Arquiteto

Projete e implemente o papel organizacional cuja responsabilidade
explícita é recusar trabalho de baixo valor antes que ele consuma
tempo de agente e atenção do time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================================
# DATA MODELS
# ============================================================================

class RefusalDecision(Enum):
    """
    Decisões que o Owner-of-No pode tomar.

    APPROVE não significa "aprovar" — significa "não encontrei razão
    para recusar". A aprovação final é de outro papel (PO, Tech Lead).
    """
    APPROVE = "approve"       # não recusa — card pode seguir para aprovação
    DEFER = "defer"           # adiar com condições — "resolva X e reenvie"
    REDIRECT = "redirect"     # substituir por alternativa de menor escopo
    REFUSE = "refuse"         # recusar permanentemente — "não construa"


class RefusalCriterion(Enum):
    """Critérios objetivos que o Owner-of-No aplica."""
    HAS_DOCUMENTED_USER = "has_documented_user"
    COST_PROXY_SURVIVES = "cost_proxy_survives"
    HAS_REFUSAL_OWNER = "has_refusal_owner"
    NO_UNSTABLE_DEPENDENCY = "no_unstable_dependency"


@dataclass
class CardRequest:
    """
    Uma requisição de build (card) submetida ao Owner-of-No.

    Representa qualquer coisa que um agente construiria: feature,
    refactor, experimento, melhoria interna.
    """
    card_id: str
    title: str
    requester: str
    has_documented_user: bool           # usuário real com dor documentada?
    user_count_affected: int            # quantos usuários afetados
    user_pain_description: str          # descrição da dor (vazia se não tem)
    cost_proxy_survives: bool           # sobrevive ao cost proxy (1 semana)?
    cost_proxy_rationale: str           # justificativa (vazia se não sobrevive)
    has_refusal_owner: bool             # tem dono da recusa nomeado?
    refusal_owner: str                  # nome do dono (vazio se não tem)
    estimated_agent_tokens: int         # estimativa de tokens
    depends_on_unstable_service: bool   # depende de serviço não monitorado?
    description: str = ""


@dataclass
class OwnerOfNoRoleSpec:
    """
    Especificação formal do papel de Owner-of-No.

    Define os 5 atributos do papel: autoridade, escopo, critérios,
    limites e métricas. Esta especificação é o "contrato" do papel —
    qualquer pessoa que ocupe o papel opera dentro destes limites.
    """
    role_name: str = "Owner-of-No"
    version: str = "1.0"

    # Atributo 1: AUTORIDADE
    can_refuse: bool = True
    can_defer: bool = True
    can_redirect: bool = True
    can_approve: bool = False  # NUNCA aprova — aprovação é de outro papel

    # Atributo 2: ESCOPO
    scope_includes: list[str] = field(default_factory=lambda: [
        "Build requests (features, refactors, experiments)",
        "Agent dispatch requests",
        "Infrastructure changes",
    ])
    scope_excludes: list[str] = field(default_factory=lambda: [
        "Production hotfixes",
        "Security incidents",
        "Compliance requirements",
        "Data recovery operations",
    ])

    # Atributo 3: CRITÉRIOS (checks objetivos e auditáveis)
    refusal_criteria: list[str] = field(default_factory=lambda: [
        "has_documented_user: O card identifica um usuário/persona real com dor documentada?",
        "cost_proxy_survives: O valor sobrevive ao cost proxy (1 semana de engenharia)?",
        "has_refusal_owner: Existe uma pessoa nomeada com autoridade para dizer não?",
        "no_unstable_dependency: O card NÃO depende de serviço instável sem monitoramento?",
    ])

    # Atributo 4: LIMITES
    boundaries: list[str] = field(default_factory=lambda: [
        "NÃO aprova cards — apenas não-recusa. Aprovação é do PO/Tech Lead.",
        "NÃO prioriza — não decide ordem. Apenas decide se deve existir.",
        "NÃO implementa — não escreve código. Apenas decide valor.",
        "NÃO substitui o Product Owner — complementa com a dimensão de recusa.",
    ])

    # Atributo 5: MÉTRICAS
    success_metrics: list[str] = field(default_factory=lambda: [
        "Valor estimado evitado (tokens + manutenção de artefatos recusados)",
        "Taxa de falsos positivos (cards recusados que se provaram necessários em 90 dias)",
        "Taxa de recusa construtiva (% de recusas que ofereceram alternativa)",
        "Tempo médio de decisão (minutos entre receber card e emitir decisão)",
        "Cobertura (% de cards do backlog que passaram pelo Owner-of-No)",
    ])


@dataclass
class RefusalRecord:
    """
    Registro de uma decisão do Owner-of-No.

    Cada registro é imutável e contém toda a informação necessária
    para auditar a decisão posteriormente.
    """
    card_id: str
    decision: RefusalDecision
    criteria_applied: list[RefusalCriterion] = field(default_factory=list)
    criteria_failed: list[RefusalCriterion] = field(default_factory=list)
    alternative_offered: str = ""      # "Em vez disso, ..."
    rationale: str = ""                # por que essa decisão
    decided_by: str = "Owner-of-No"
    decided_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# REFUSAL CRITERIA ENGINE (função pura)
# ============================================================================

def check_has_documented_user(card: CardRequest) -> tuple[bool, str]:
    """
    Verifica se o card tem usuário documentado com dor real.

    Critério: has_documented_user == True E user_pain_description não vazio
              E user_count_affected > 0

    Returns:
        Tupla (passou, racional).
    """
    # TODO: Implementar verificação
    pass


def check_cost_proxy_survives(card: CardRequest) -> tuple[bool, str]:
    """
    Verifica se o valor do card sobrevive ao cost proxy.

    Critério: cost_proxy_survives == True E cost_proxy_rationale não vazio

    Returns:
        Tupla (passou, racional).
    """
    # TODO: Implementar verificação
    pass


def check_has_refusal_owner(card: CardRequest) -> tuple[bool, str]:
    """
    Verifica se o card tem um dono da recusa nomeado.

    Critério: has_refusal_owner == True E refusal_owner não vazio

    Returns:
        Tupla (passou, racional).
    """
    # TODO: Implementar verificação
    pass


def check_no_unstable_dependency(card: CardRequest) -> tuple[bool, str]:
    """
    Verifica se o card NÃO depende de serviço instável.

    Critério: depends_on_unstable_service == False

    Returns:
        Tupla (passou, racional).
    """
    # TODO: Implementar verificação
    pass


# ============================================================================
# REFUSAL DECISION ENGINE (função pura)
# ============================================================================

def apply_criteria(card: CardRequest) -> RefusalRecord:
    """
    Aplica todos os critérios do Owner-of-No a um card e retorna a decisão.

    Esta é a função central do Owner-of-No. Ela deve ser 100% determinística:
    mesmo card → mesma decisão, sempre.

    Algoritmo:
    1. Executar os 4 checks
    2. Coletar critérios que passaram e que falharam
    3. Aplicar matriz de decisão:
       - Se check_dependency falha → DEFER
       - Se check_user falha E check_cost falha → REFUSE
       - Se check_user falha MAS check_cost passa → REDIRECT
       - Se check_cost falha → REDIRECT
       - Se check_owner falha → DEFER
       - Se todos passam → APPROVE
    4. Construir alternativa construtiva
    5. Retornar RefusalRecord

    Args:
        card: Card a ser avaliado.

    Returns:
        RefusalRecord com decisão e racional.
    """
    # TODO: Implementar a engine de decisão completa
    #
    # Passo 1: Executar checks
    # user_ok, user_rationale = check_has_documented_user(card)
    # cost_ok, cost_rationale = check_cost_proxy_survives(card)
    # owner_ok, owner_rationale = check_has_refusal_owner(card)
    # dep_ok, dep_rationale = check_no_unstable_dependency(card)
    #
    # Passo 2: Coletar resultados
    # criteria_passed = []
    # criteria_failed = []
    # (preencher listas)
    #
    # Passo 3: Matriz de decisão
    # if not dep_ok:
    #     decision = RefusalDecision.DEFER
    #     alternative = "..."
    # elif not user_ok and not cost_ok:
    #     decision = RefusalDecision.REFUSE
    #     alternative = "..."
    # ...
    #
    # Passo 4: Retornar RefusalRecord
    pass


def generate_alternative(card: CardRequest, decision: RefusalDecision) -> str:
    """
    Gera uma alternativa construtiva para a decisão.

    Regra: toda recusa/defer/redirect deve vir acompanhada de uma
    alternativa acionável. "Não" sem "em vez disso" é bloqueio;
    "Não, mas..." é governança.

    Args:
        card: Card que está sendo decidido.
        decision: Decisão tomada.

    Returns:
        String com a alternativa.
    """
    # TODO: Implementar geração de alternativas
    #
    # REFUSE: "Em vez de construir {card.title}, investigue se [alternativa
    #          mais simples] resolve o mesmo problema com 1/10 do esforço."
    #
    # DEFER: "Resolva [condição] primeiro, depois reenvie o card.
    #         Condição pendente: [detalhe]."
    #
    # REDIRECT: "Em vez do escopo completo, experimente [versão mínima]
    #            primeiro. Se houver tração, expanda."
    #
    # APPROVE: "" (não precisa de alternativa — o card segue para aprovação)
    pass


# ============================================================================
# REFUSAL LEDGER
# ============================================================================

class RefusalLedger:
    """
    Registro histórico de todas as decisões do Owner-of-No.

    Responsabilidades:
    1. Armazenar RefusalRecords
    2. Calcular métricas do papel
    3. Permitir auditoria: por que o card X foi recusado?
    4. Rastrear falsos positivos (follow-up em 90 dias)
    """

    def __init__(self):
        """Inicializa o ledger vazio."""
        # TODO: Implementar
        pass

    def record(self, record: RefusalRecord) -> None:
        """Registra uma decisão. Levanta ValueError se card_id duplicado."""
        # TODO: Implementar
        pass

    def get(self, card_id: str) -> RefusalRecord | None:
        """Recupera a decisão para um card_id."""
        # TODO: Implementar
        pass

    def get_by_decision(self, decision: RefusalDecision) -> list[RefusalRecord]:
        """Filtra por tipo de decisão."""
        # TODO: Implementar
        pass

    def audit(self, card_id: str) -> str:
        """
        Reconstrói o racional completo da decisão para auditoria.

        Formato:
        "CARD-202: REFUSE
         Critérios aplicados: has_documented_user, cost_proxy_survives
         Critérios falhos: has_documented_user (sem usuário),
                           cost_proxy_survives (sem justificativa)
         Alternativa: investigue se o time realmente precisa de tema dark
         Decidido por: Owner-of-No em 2026-06-11"
        """
        # TODO: Implementar
        pass

    def metrics(self) -> dict:
        """
        Calcula métricas do papel de Owner-of-No.

        Returns:
            {
                "total_decisions": int,
                "by_decision": {"approve": int, "defer": int, ...},
                "refusal_rate": float,       # (defer + redirect + refuse) / total
                "constructive_rate": float,  # recusas com alternativa / total de recusas
                "avg_decision_time_minutes": float,
                "estimated_value_avoided_tokens": int,
                "estimated_value_avoided_brl": float,
            }
        """
        # TODO: Implementar métricas
        pass


# ============================================================================
# BACKLOG DATA
# ============================================================================

def build_koda_backlog() -> list[CardRequest]:
    """Constrói o backlog do KODA com 6 cards para avaliação."""
    raw = [
        {
            "card_id": "CARD-201",
            "title": "Recomendação cross-sell por histórico de navegação",
            "requester": "pm_fernanda",
            "has_documented_user": True,
            "user_count_affected": 1200,
            "user_pain_description": "Clientes compram 1 produto e abandonam. Perda: R$ 8K/mês",
            "cost_proxy_survives": True,
            "cost_proxy_rationale": "R$ 8K/mês perdido vs R$ 3K de engenharia — se paga em 2 semanas",
            "has_refusal_owner": True,
            "refusal_owner": "Fernanda (PO)",
            "estimated_agent_tokens": 800000,
            "depends_on_unstable_service": False,
        },
        {
            "card_id": "CARD-202",
            "title": "Tema dark no dashboard interno de analytics",
            "requester": "dev_maria",
            "has_documented_user": False,
            "user_count_affected": 4,
            "user_pain_description": "",
            "cost_proxy_survives": False,
            "cost_proxy_rationale": "",
            "has_refusal_owner": False,
            "refusal_owner": "",
            "estimated_agent_tokens": 450000,
            "depends_on_unstable_service": False,
        },
        {
            "card_id": "CARD-203",
            "title": "Pipeline de re-treinamento semanal do modelo",
            "requester": "dev_joao",
            "has_documented_user": True,
            "user_count_affected": 1200,
            "user_pain_description": "Recomendações usam dados de 3 meses atrás",
            "cost_proxy_survives": True,
            "cost_proxy_rationale": "Perda de R$ 15K/mês vs R$ 8K one-time",
            "has_refusal_owner": True,
            "refusal_owner": "Rafael (Tech Lead)",
            "estimated_agent_tokens": 2800000,
            "depends_on_unstable_service": True,
        },
        {
            "card_id": "CARD-204",
            "title": "Migrar notificações de polling para WebSockets",
            "requester": "dev_carlos",
            "has_documented_user": False,
            "user_count_affected": 0,
            "user_pain_description": "",
            "cost_proxy_survives": False,
            "cost_proxy_rationale": "",
            "has_refusal_owner": False,
            "refusal_owner": "",
            "estimated_agent_tokens": 1500000,
            "depends_on_unstable_service": False,
        },
        {
            "card_id": "CARD-205",
            "title": "Exportação de relatório em PDF para clientes corporate",
            "requester": "pm_fernanda",
            "has_documented_user": True,
            "user_count_affected": 80,
            "user_pain_description": "Clientes B2B precisam de relatório mensal. Hoje manual: 4h/semana",
            "cost_proxy_survives": True,
            "cost_proxy_rationale": "4h/sem × R$200/h × 52 sem = R$41.600/ano. Custo: R$5K one-time",
            "has_refusal_owner": True,
            "refusal_owner": "Fernanda (PO)",
            "estimated_agent_tokens": 1200000,
            "depends_on_unstable_service": False,
        },
        {
            "card_id": "CARD-206",
            "title": "Refatorar sistema de cache de sessão (Redis → memcached)",
            "requester": "dev_paulo",
            "has_documented_user": False,
            "user_count_affected": 0,
            "user_pain_description": "",
            "cost_proxy_survives": False,
            "cost_proxy_rationale": "",
            "has_refusal_owner": False,
            "refusal_owner": "",
            "estimated_agent_tokens": 900000,
            "depends_on_unstable_service": False,
        },
    ]
    return [CardRequest(**r) for r in raw]


# ============================================================================
# TESTS / EXEMPLOS DE USO
# ============================================================================

def test_role_spec_is_valid():
    """Cenário 0: A especificação do papel é internamente consistente."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 0: OwnerOfNoRoleSpec — Consistência Interna")
    print("=" * 60)

    spec = OwnerOfNoRoleSpec()

    # O papel NUNCA pode aprovar
    assert not spec.can_approve, "Owner-of-No nunca deve poder aprovar"
    # O papel DEVE poder recusar
    assert spec.can_refuse, "Owner-of-No deve poder recusar"
    # Deve ter critérios documentados
    assert len(spec.refusal_criteria) >= 3, "Deve ter ao menos 3 critérios"
    # Deve ter limites explícitos
    assert len(spec.boundaries) >= 3, "Deve ter ao menos 3 limites"
    # Deve ter métricas de sucesso
    assert len(spec.success_metrics) >= 3, "Deve ter ao menos 3 métricas"

    print(f"   Role: {spec.role_name} v{spec.version}")
    print(f"   Pode aprovar: {spec.can_approve}")
    print(f"   Pode recusar: {spec.can_refuse}")
    print(f"   Critérios: {len(spec.refusal_criteria)}")
    print(f"   Limites: {len(spec.boundaries)}")
    print(f"   Métricas: {len(spec.success_metrics)}")
    print("✅ Teste 0 concluído!")


def test_card_with_user_and_cost_approved():
    """Cenário 1: Card com usuário real, custo justificado, dono → APPROVE."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: Card Completo → APPROVE")
    print("=" * 60)

    card = CardRequest(
        card_id="CARD-201",
        title="Recomendação cross-sell",
        requester="pm_fernanda",
        has_documented_user=True,
        user_count_affected=1200,
        user_pain_description="Clientes compram 1 produto e abandonam. Perda: R$ 8K/mês",
        cost_proxy_survives=True,
        cost_proxy_rationale="Se paga em 2 semanas",
        has_refusal_owner=True,
        refusal_owner="Fernanda (PO)",
        estimated_agent_tokens=800000,
        depends_on_unstable_service=False,
    )

    record = apply_criteria(card)
    assert record.decision == RefusalDecision.APPROVE, (
        f"Card completo deve ser APPROVE, obtido {record.decision.value}"
    )
    assert len(record.criteria_failed) == 0, "Nenhum critério deve falhar"
    print(f"   Card: {card.card_id} — {card.title}")
    print(f"   Decisão: {record.decision.value}")
    print(f"   Critérios passaram: {[c.value for c in record.criteria_applied]}")
    print("✅ Teste 1 concluído!")


def test_card_without_user_refused():
    """Cenário 2: Card sem usuário, sem custo → REFUSE."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: Card Sem Usuário → REFUSE")
    print("=" * 60)

    card = CardRequest(
        card_id="CARD-202",
        title="Tema dark no dashboard interno",
        requester="dev_maria",
        has_documented_user=False,
        user_count_affected=4,
        user_pain_description="",
        cost_proxy_survives=False,
        cost_proxy_rationale="",
        has_refusal_owner=False,
        refusal_owner="",
        estimated_agent_tokens=450000,
        depends_on_unstable_service=False,
    )

    record = apply_criteria(card)
    assert record.decision == RefusalDecision.REFUSE, (
        f"Card sem usuário e sem custo deve ser REFUSE, obtido {record.decision.value}"
    )
    assert len(record.criteria_failed) >= 2, "Múltiplos critérios devem falhar"
    assert record.alternative_offered != "", "Deve oferecer alternativa construtiva"
    print(f"   Card: {card.card_id} — {card.title}")
    print(f"   Decisão: {record.decision.value}")
    print(f"   Critérios falhos: {[c.value for c in record.criteria_failed]}")
    print(f"   Alternativa: {record.alternative_offered}")
    print("✅ Teste 2 concluído!")


def test_card_with_unstable_dependency_deferred():
    """Cenário 3: Card bom mas depende de serviço instável → DEFER."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: Dependência Instável → DEFER")
    print("=" * 60)

    card = CardRequest(
        card_id="CARD-203",
        title="Pipeline de re-treinamento semanal",
        requester="dev_joao",
        has_documented_user=True,
        user_count_affected=1200,
        user_pain_description="Recomendações usam dados de 3 meses atrás",
        cost_proxy_survives=True,
        cost_proxy_rationale="Perda de R$ 15K/mês vs R$ 8K one-time",
        has_refusal_owner=True,
        refusal_owner="Rafael (Tech Lead)",
        estimated_agent_tokens=2800000,
        depends_on_unstable_service=True,
    )

    record = apply_criteria(card)
    assert record.decision == RefusalDecision.DEFER, (
        f"Card com dependência instável deve ser DEFER, obtido {record.decision.value}"
    )
    assert RefusalCriterion.NO_UNSTABLE_DEPENDENCY in record.criteria_failed
    # A alternativa deve mencionar a dependência
    assert "dependência" in record.alternative_offered.lower() or "estabil" in record.alternative_offered.lower() or "monitor" in record.alternative_offered.lower() or "eval" in record.alternative_offered.lower(), (
        f"Alternativa deve mencionar a dependência: {record.alternative_offered}"
    )
    print(f"   Card: {card.card_id} — {card.title}")
    print(f"   Decisão: {record.decision.value}")
    print(f"   Alternativa: {record.alternative_offered}")
    print("✅ Teste 3 concluído!")


def test_card_high_cost_no_user_redirected():
    """Cenário 4: Card sem usuário, alto custo → REDIRECT ou REFUSE."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: Sem Usuário, Alto Custo → REDIRECT/REFUSE")
    print("=" * 60)

    card = CardRequest(
        card_id="CARD-204",
        title="Migrar notificações para WebSockets",
        requester="dev_carlos",
        has_documented_user=False,
        user_count_affected=0,
        user_pain_description="",
        cost_proxy_survives=False,
        cost_proxy_rationale="",
        has_refusal_owner=False,
        refusal_owner="",
        estimated_agent_tokens=1500000,
        depends_on_unstable_service=False,
    )

    record = apply_criteria(card)
    assert record.decision in (RefusalDecision.REDIRECT, RefusalDecision.REFUSE), (
        f"Card sem usuário deve ser REDIRECT ou REFUSE, obtido {record.decision.value}"
    )
    print(f"   Card: {card.card_id} — {card.title}")
    print(f"   Decisão: {record.decision.value}")
    print(f"   Racional: {record.rationale}")
    print("✅ Teste 4 concluído!")


def test_full_backlog_evaluation():
    """Cenário 5: Avaliar o backlog completo de 6 cards."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: Backlog Completo — 6 Cards")
    print("=" * 60)

    backlog = build_koda_backlog()
    ledger = RefusalLedger()

    decisions = []
    for card in backlog:
        record = apply_criteria(card)
        ledger.record(record)
        decisions.append(record)
        print(f"   {card.card_id}: {record.decision.value} — {card.title[:50]}...")

    assert len(decisions) == 6

    # Estatísticas rápidas
    approves = sum(1 for d in decisions if d.decision == RefusalDecision.APPROVE)
    refuses = sum(1 for d in decisions if d.decision == RefusalDecision.REFUSE)
    defers = sum(1 for d in decisions if d.decision == RefusalDecision.DEFER)
    redirects = sum(1 for d in decisions if d.decision == RefusalDecision.REDIRECT)

    print(f"\n   APPROVE: {approves}")
    print(f"   DEFER: {defers}")
    print(f"   REDIRECT: {redirects}")
    print(f"   REFUSE: {refuses}")
    print(f"   Taxa de recusa: {(defers + redirects + refuses) / 6:.0%}")

    # Pelo menos alguns cards devem ser recusados/redirecionados/deferidos
    assert refuses >= 1, "Pelo menos 1 card deve ser REFUSE"
    assert approves >= 1, "Pelo menos 1 card deve ser APPROVE"

    # Verificar auditoria
    audit = ledger.audit("CARD-202")
    assert "CARD-202" in audit
    assert "REFUSE" in audit
    print(f"\n   Auditoria CARD-202:\n{audit}")

    print("✅ Teste 5 concluído!")


def test_all_refusals_have_alternatives():
    """Cenário 6: Toda recusa oferece alternativa construtiva."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 6: Recusas Sempre Oferecem Alternativa")
    print("=" * 60)

    backlog = build_koda_backlog()

    for card in backlog:
        record = apply_criteria(card)
        if record.decision != RefusalDecision.APPROVE:
            assert record.alternative_offered != "", (
                f"Decisão {record.decision.value} no card {card.card_id} "
                f"deve oferecer alternativa"
            )
            # Alternativa deve ser diferente do racional genérico
            assert len(record.alternative_offered) > 10, (
                f"Alternativa muito curta para {card.card_id}: '{record.alternative_offered}'"
            )

    print(f"   Verificados {len(backlog)} cards")
    non_approves = sum(1 for c in backlog if apply_criteria(c).decision != RefusalDecision.APPROVE)
    print(f"   {non_approves} decisões não-APPROVE — todas com alternativa construtiva")
    print("✅ Teste 6 concluído!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 4: PROJETAR O PAPEL DE OWNER-OF-NO")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_role_spec_is_valid()
    # test_card_with_user_and_cost_approved()
    # test_card_without_user_refused()
    # test_card_with_unstable_dependency_deferred()
    # test_card_high_cost_no_user_redirected()
    # test_full_backlog_evaluation()
    # test_all_refusals_have_alternatives()

    print("\n📝 TODO: Implemente as funções acima!")
    print("   1. check_has_documented_user()")
    print("   2. check_cost_proxy_survives()")
    print("   3. check_has_refusal_owner()")
    print("   4. check_no_unstable_dependency()")
    print("   5. apply_criteria() — a engine de decisão")
    print("   6. generate_alternative()")
    print("   7. RefusalLedger (todas as operações)")
    print("   Após implementar, descomente os testes em main()")
```

---

## 🏗️ Como Começar

### Passo 1: Entender a Distinção Entre Aprovar e Não-Recusar (5 min)

O Owner-of-No NUNCA aprova. Esta é a distinção mais importante do exercício. O papel diz: "não encontrei razão para recusar este card" — e o card segue para aprovação pelo Product Owner ou Tech Lead. Isso mantém a separação de poderes: um papel recusa, outro aprova.

### Passo 2: Implementar os 4 Checks (15 min)

Implemente `check_has_documented_user()`, `check_cost_proxy_survives()`, `check_has_refusal_owner()`, `check_no_unstable_dependency()`. Cada check é uma função pura que retorna `(bool, str)`.

### Passo 3: Implementar a Matriz de Decisão (20 min)

Implemente `apply_criteria()`. Siga a matriz documentada. A ordem dos checks importa: verifique dependência primeiro (se falhar → DEFER imediato), depois usuário+custo combinados (se ambos falharem → REFUSE).

### Passo 4: Implementar Alternativas Construtivas (15 min)

Implemente `generate_alternative()`. Esta é a diferença entre um Owner-of-No que bloqueia e um que governa. Toda recusa deve vir com "em vez disso...".

### Passo 5: Implementar o RefusalLedger (15 min)

Implemente `record()`, `get()`, `audit()`, `metrics()`. O ledger é a memória institucional: quando alguém perguntar "por que aquele card foi recusado?", a resposta precisa estar documentada.

### Passo 6: Avaliar o Backlog (10 min)

Rode `test_full_backlog_evaluation()`. Observe as decisões. Compare com o que você decidiria intuitivamente. Se houver discrepância, ajuste os critérios.

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

### Critério 1: OwnerOfNoRoleSpec é consistente

- [ ] `can_approve == False` (nunca aprova)
- [ ] `can_refuse == True`
- [ ] Pelo menos 3 critérios documentados
- [ ] Pelo menos 3 limites explícitos
- [ ] Pelo menos 3 métricas de sucesso

### Critério 2: Checks são funções puras

- [ ] `check_has_documented_user()` retorna False para card sem usuário
- [ ] `check_cost_proxy_survives()` retorna False para card sem justificativa
- [ ] `check_has_refusal_owner()` retorna False para card sem dono
- [ ] `check_no_unstable_dependency()` retorna False para card com dependência instável

### Critério 3: Matriz de decisão correta

- [ ] CARD-201 (completo) → APPROVE
- [ ] CARD-202 (sem usuário, sem custo) → REFUSE
- [ ] CARD-203 (dependência instável) → DEFER
- [ ] CARD-205 (completo, corporate) → APPROVE

### Critério 4: Alternativas construtivas

- [ ] Toda decisão não-APPROVE tem `alternative_offered` não vazia
- [ ] Alternativas mencionam ação concreta ("investigue", "resolva", "experimente")
- [ ] APPROVE tem `alternative_offered` vazia (não precisa)

### Critério 5: RefusalLedger funcional

- [ ] `audit(card_id)` reconstrói o racional completo
- [ ] `metrics()` retorna estatísticas corretas
- [ ] Duplicata de card_id → ValueError

### Critério 6: Testes passam

- [ ] Todos os 7 testes em `main()` passam (incluindo test_role_spec_is_valid)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Role Spec** | 10% | Não definida | Atributos incompletos | 5 atributos definidos | Spec consistente + limites claros |
| **Checks (4 funções)** | 20% | Não implementados | 2 checks funcionam | 4 checks funcionam | Checks com racional informativo |
| **Matriz de Decisão** | 30% | Não implementada | Cobre APPROVE/REFUSE | Cobre os 4 tipos de decisão | Matriz completa + borda (card sem campos) |
| **Alternativas Construtivas** | 15% | Não implementadas | Alternativas genéricas | Alternativas específicas por decisão | Alternativas acionáveis com next step claro |
| **RefusalLedger** | 15% | Não implementado | record/get funcionam | record/get/audit funcionam | Todas operações + métricas |
| **Testes** | 10% | Nenhum teste passa | 3-4 testes passam | 5-6 testes passam | Todos os 7 testes passam |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

### Para a Matriz de Decisão

1. **Ordem dos checks importa.** Verifique `depends_on_unstable_service` primeiro — se um card depende de serviço instável, a resposta é sempre DEFER, independente dos outros critérios.
2. **A combinação usuário+custo é a mais poderosa.** Sem usuário E sem custo → REFUSE. Sem usuário MAS com custo → REDIRECT (o custo indica que ALGUÉM se importa, só não está documentado).
3. **APPROVE é raro.** No backlog de exemplo, apenas 2 de 6 cards recebem APPROVE (33%). Isso é intencional — o Owner-of-No existe para filtrar, não para carimbar.

### Para as Alternativas Construtivas

1. **"Em vez disso" é a frase mais importante.** Toda alternativa deve começar com uma ação: "investigue", "resolva", "experimente", "documente", "meça".
2. **Alternativas são proporcionais ao escopo recusado.** Recusou 1.500.000 tokens? A alternativa deve sugerir um experimento de 100.000 tokens. Recusou um refactor de cache? A alternativa deve sugerir um benchmark primeiro.

### Para o Design do Papel

1. **O Owner-of-No não é o vilão.** O papel é desenhado para ser respeitado, não temido. As métricas (valor evitado, não quantidade de recusas) reforçam isso.
2. **Accountability reversa é essencial.** Se o Owner-of-No recusou algo que depois se provou crítico, isso é um evento de aprendizado — os critérios são refinados, não a pessoa é punida. Sem essa segurança, ninguém recusa nada.

---

## 🔗 Referências

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|Análise: The Trap SDD Is Setting]] — seções 2.1 (Manual Brake), 2.5 (Ownership-of-No as Role Design)
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|Padrões: SDD Trap]] — padrão #5 (Owner-of-No Role)
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] — entrevista de alinhamento (mecanismo complementar de questionamento)
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] — revisão de planos com rubricas duplas (precedente de múltiplos papeis de avaliação)

---

*Exercício 4 | Nível 3 — Arquiteto | Owner-of-No Role*

**Dizer não não é um ato de coragem. É uma função de design.**
