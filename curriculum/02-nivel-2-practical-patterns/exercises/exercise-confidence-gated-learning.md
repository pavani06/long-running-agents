---
title: "Exercicio: Confidence-Gated Continual Learning com Deploy Automatico"
type: exercise
level: "N2"
aliases: ["confidence-gated learning", "aprendizado continuo com confianca", "ghostwriter deploy gate", "fyi vs approval", "auto-deploy fixes", "continual improvement pipeline"]
tags: [curriculo-conteudo, nivel-2, exercicio, harness-engineering, evals, governanca, continual-learning, confidence-scoring, ghostwriter, auto-deploy, fyi-approval]
duration: "60-75 min"
relates-to: ["[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-patterns|Sierra Patterns]]", "[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-classification|Classification]]", "[[docs/canonical/garbage-collection-day-meta-loop|GC Day Meta-Loop]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]"]
last_updated: 2026-06-26
---
# Exercicio: Confidence-Gated Continual Learning com Deploy Automatico
## Nivel 2 - Padroes Praticos

**Tempo Estimado:** 60-75 minutos
**Dificuldade:** Intermediario
**Pre-requisito:** Ter lido `02-sprint-contracts.md` (Nivel 2) + completado Exercicio 2
**Objetivo:** Construir um pipeline de melhoria continua que classifica sugestoes por confianca e decide automaticamente entre deploy, revisao humana, ou descarte

---

## Prologo: O Ghostwriter Que Sugeriu 200 Melhorias e Ninguem Revisou

### Quarta-feira, 14h30. O backlog de melhorias transbordou.

```
PM: "O Ghostwriter gerou 47 sugestoes essa semana. Quem vai revisar?"
ENG: "Ninguem. A gente nao tem tempo. Mas 4 sao correcoes triviais de
     artigos contraditorios na base de conhecimento. Essas eram obvias."
PM: "Entao por que nao foram deployadas?"
ENG: "Porque o pipeline trata tudo igual. Toda sugestao — desde 'corrigir
     virgula no artigo X' ate 'reescrever a politica de reembolso' —
     passa pelo mesmo gate manual. O gate virou um gargalo."
```

O `Ghostwriter` da **Sierra** era um agente que analisava conversas de producao e gerava sugestoes de melhoria. Funcionava bem: toda semana, 30-50 sugestoes de alta qualidade. Mas o pipeline de deploy era binario: ou revisao humana para tudo, ou deploy automatico cego para tudo.

Nao havia meio-termo. As 4 correcoes obvias (artigos contraditorios com resposta clara) esperavam na mesma fila que as 43 sugestoes complexas (novas jornadas de conversa, reescrita de politicas). O PM revisava 5 por semana. Em 10 semanas, 200 sugestoes acumuladas.

**O que deveria ter acontecido:**

```
[confidence] score=0.94 → FYI notification + auto-deploy (artigo contraditorio)
[confidence] score=0.87 → FYI notification + auto-deploy (correcao de preco)
[confidence] score=0.52 → human review required (nova jornada de upsell)
[confidence] score=0.31 → human review required (reescrita de politica)
[confidence] score=0.12 → auto-discard (sugestao sem evidencias suficientes)
```

**Sua missao:** Construir um `ConfidenceGate` que classifica sugestoes do Ghostwriter por score de confianca e decide automaticamente o destino: auto-deploy (FYI), revisao humana, ou descarte.

---

## Cenario: Ghostwriter com 50 Sugestoes Acumuladas

### Contexto

O Ghostwriter analisou 10 mil conversas de producao do agente de suporte da **Sierra** e gerou 50 sugestoes de melhoria. Cada sugestao tem:

```json
{
  "suggestion_id": "GW-0042",
  "type": "knowledge_fix",
  "summary": "Artigo A diz 'frete gratis acima de R$200'; Artigo B diz 'frete gratis acima de R$150'. Resposta correta: R$150 (politica atualizada em 2026-05).",
  "source_conversations": ["CONV-8821", "CONV-9104", "CONV-9230", "CONV-9401"],
  "evidence_count": 4,
  "affected_artifacts": ["help_center/frete.md", "help_center/promocoes.md"],
  "verifiability": "trivially_verifiable",
  "risk_level": "low",
  "automation_history": null
}
```

O campo `verifiability` e classificado pelo Ghostwriter em 3 niveis:
- `trivially_verifiable` — contradicao obvia, resposta correta unica
- `verifiable_with_context` — requer contexto adicional para confirmar
- `requires_judgment` — envolve trade-off ou julgamento subjetivo

O campo `risk_level` e classificado em:
- `low` — correcao de texto, atualizacao de preco documentado
- `medium` — mudanca em jornada de conversa, alteracao de tom
- `high` — reescrita de politica financeira, mudanca em fluxo de pagamento

### Dados de Entrada

Voce recebe um dataset com 8 sugestoes representativas (das 50 totais):

```python
GHOSTWRITER_SUGGESTIONS = [
    {
        "id": "GW-001", "type": "knowledge_fix",
        "verifiability": "trivially_verifiable", "risk_level": "low",
        "evidence_count": 12, "summary": "Preco do Whey Isolado: artigo diz R$110, sistema diz R$120. Correto: R$120."
    },
    {
        "id": "GW-002", "type": "knowledge_fix",
        "verifiability": "trivially_verifiable", "risk_level": "low",
        "evidence_count": 8, "summary": "Artigo A: 'frete gratis acima de R$200'; Artigo B: 'acima de R$150'. Correto: R$150."
    },
    {
        "id": "GW-003", "type": "response_tone",
        "verifiability": "requires_judgment", "risk_level": "medium",
        "evidence_count": 15, "summary": "Tom muito formal para clientes jovens. Sugestao: adotar linguagem casual para faixa 18-25."
    },
    {
        "id": "GW-004", "type": "journey_change",
        "verifiability": "verifiable_with_context", "risk_level": "medium",
        "evidence_count": 6, "summary": "Adicionar upsell de creatina apos compra de whey. 22% dos clientes compram creatina em 7 dias."
    },
    {
        "id": "GW-005", "type": "policy_rewrite",
        "verifiability": "requires_judgment", "risk_level": "high",
        "evidence_count": 3, "summary": "Politica de reembolso: estender de 7 para 15 dias. 18% de churn por insatisfacao com prazo."
    },
    {
        "id": "GW-006", "type": "knowledge_fix",
        "verifiability": "trivially_verifiable", "risk_level": "low",
        "evidence_count": 2, "summary": "Link quebrado na pagina de FAQ de entrega."
    },
    {
        "id": "GW-007", "type": "journey_change",
        "verifiability": "requires_judgment", "risk_level": "high",
        "evidence_count": 1, "summary": "Cliente sugeriu: 'poderiam mandar foto do produto antes de enviar'."
    },
    {
        "id": "GW-008", "type": "knowledge_fix",
        "verifiability": "trivially_verifiable", "risk_level": "low",
        "evidence_count": 25, "summary": "Endereco da loja fisica desatualizado em 3 artigos. Correto: Av. Paulista, 1000."
    },
]
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Confidence scoring:** Cada sugestao recebe um score de confianca (0.0 a 1.0) calculado a partir de `verifiability`, `risk_level` e `evidence_count`
2. **RF2 - Auto-deploy gate (FYI):** Sugestoes com `score >= 0.80` sao deployadas automaticamente com notificacao FYI para o time
3. **RF3 - Human review gate:** Sugestoes com `0.40 <= score < 0.80` vao para revisao humana com prazo de 5 dias uteis
4. **RF4 - Auto-discard gate:** Sugestoes com `score < 0.40` sao descartadas automaticamente (insuficiencia de evidencias)
5. **RF5 - Evidence threshold:** `evidence_count < 3` reduz o score em 0.15 (sugestoes com pouca evidencia sao menos confiaveis)
6. **RF6 - Risk dampening:** `risk_level: high` aplica um multiplicador de 0.7 ao score (sugestoes de alto risco exigem mais confianca para auto-deploy)
7. **RF7 - Override manual:** Qualquer sugestao pode ser manualmente promovida de `discard` para `review` ou de `review` para `deploy` por um operador

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Pipeline determinista:** Dado o mesmo conjunto de sugestoes, o pipeline produz a mesma classificacao
3. **RT3 - Audit trail:** Cada decisao gera uma entrada de log com score, thresholds aplicados e justificativa

---

## Sua Tarefa

Voce vai implementar o `ConfidenceGate` em 3 partes.

---

### Parte 1: Diagnosticar o Gargalo de Revisao (10 min)

Analise as 8 sugestoes do `GHOSTWRITER_SUGGESTIONS` e responda manualmente:

```python
# TAREFA: Classifique cada sugestao manualmente antes de implementar o scorer.
# Depois compare sua intuicao com o score calculado.

# Para cada GW-001 a GW-008, responda:
# 1. Esta sugestao deveria ser auto-deploy (FYI), human review, ou discard?
# 2. Qual o fator mais importante na sua decisao? (verifiability, risk, evidence_count)
# 3. Se voce fosse o PM, qual seria seu criterio de override para esta sugestao?

# Exemplo:
# GW-001: auto-deploy — preco documentado no sistema > artigo desatualizado.
#          Fator: verifiability=trivially_verifiable + evidencia forte (12 conversas)
#          Override: nenhum, decisao e clara.
```

---

### Parte 2: Implementar o Confidence Gate (40 min)

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class Verifiability(Enum):
    TRIVIALLY_VERIFIABLE = "trivially_verifiable"
    VERIFIABLE_WITH_CONTEXT = "verifiable_with_context"
    REQUIRES_JUDGMENT = "requires_judgment"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SuggestionType(Enum):
    KNOWLEDGE_FIX = "knowledge_fix"
    RESPONSE_TONE = "response_tone"
    JOURNEY_CHANGE = "journey_change"
    POLICY_REWRITE = "policy_rewrite"


class Decision(Enum):
    AUTO_DEPLOY = "auto_deploy"    # FYI notification
    HUMAN_REVIEW = "human_review"  # requer aprovacao
    AUTO_DISCARD = "auto_discard"  # evidencias insuficientes


@dataclass
class Suggestion:
    suggestion_id: str
    type: SuggestionType
    verifiability: Verifiability
    risk_level: RiskLevel
    evidence_count: int
    summary: str
    affected_artifacts: list[str] = field(default_factory=list)
    manual_override: Optional[Decision] = None


@dataclass
class DecisionRecord:
    suggestion_id: str
    confidence_score: float
    decision: Decision
    reason: str
    overridden: bool = False


# ============================================================
# CONFIDENCE SCORING
# ============================================================

# Pesos base por verifiability
VERIFIABILITY_BASE_SCORE = {
    Verifiability.TRIVIALLY_VERIFIABLE: 0.85,
    Verifiability.VERIFIABLE_WITH_CONTEXT: 0.55,
    Verifiability.REQUIRES_JUDGMENT: 0.25,
}

# Multiplicador de risco
RISK_MULTIPLIER = {
    RiskLevel.LOW: 1.0,
    RiskLevel.MEDIUM: 0.85,
    RiskLevel.HIGH: 0.70,
}

# Thresholds de decisao
AUTO_DEPLOY_THRESHOLD = 0.80
HUMAN_REVIEW_MIN_THRESHOLD = 0.40

# Penalidade por baixa evidencia
LOW_EVIDENCE_THRESHOLD = 3
LOW_EVIDENCE_PENALTY = 0.15

# Bonus por alta evidencia
HIGH_EVIDENCE_THRESHOLD = 10
HIGH_EVIDENCE_BONUS = 0.10


def compute_confidence_score(suggestion: Suggestion) -> float:
    """
    Calcula o score de confianca de uma sugestao do Ghostwriter.

    Formula:
      base = VERIFIABILITY_BASE_SCORE[verifiability]
      evidence_adjustment = -LOW_EVIDENCE_PENALTY (se evidence_count < 3)
                            +HIGH_EVIDENCE_BONUS (se evidence_count >= 10)
                            +0.0 (caso contrario)
      risk_adjusted = base * RISK_MULTIPLIER[risk_level]
      score = min(1.0, max(0.0, risk_adjusted + evidence_adjustment))

    Args:
        suggestion: Sugestao do Ghostwriter.

    Returns:
        Score de confianca entre 0.0 e 1.0.
    """
    # SEU CODIGO AQUI
    pass


def decide(suggestion: Suggestion) -> DecisionRecord:
    """
    Decide o destino de uma sugestao baseado no score de confianca.

    Regras:
    1. Se manual_override definido: usar override
    2. Se score >= AUTO_DEPLOY_THRESHOLD: AUTO_DEPLOY
    3. Se score >= HUMAN_REVIEW_MIN_THRESHOLD: HUMAN_REVIEW
    4. Senao: AUTO_DISCARD

    O reason deve explicar a decisao em uma frase.
    """
    # SEU CODIGO AQUI
    pass


# ============================================================
# CONFIDENCE GATE — pipeline completo
# ============================================================

@dataclass
class ConfidenceGate:
    suggestions: list[Suggestion] = field(default_factory=list)
    decisions: list[DecisionRecord] = field(default_factory=list)

    def process_all(self) -> dict[str, list[DecisionRecord]]:
        """
        Processa todas as sugestoes e agrupa por decisao.

        Returns:
            {
                "auto_deploy": [...],
                "human_review": [...],
                "auto_discard": [...],
            }
        """
        # SEU CODIGO AQUI
        pass

    def apply_manual_override(self, suggestion_id: str, decision: Decision) -> bool:
        """
        Aplica um override manual a uma sugestao.
        Retorna False se a sugestao nao existe.
        """
        # SEU CODIGO AQUI
        pass

    def get_fyi_notifications(self) -> list[str]:
        """
        Gera notificacoes FYI para sugestoes em auto_deploy.

        Formato: "FYI: {suggestion_id} auto-deployed — {summary[:80]}... (score: {score:.2f})"
        """
        # SEU CODIGO AQUI
        pass

    def get_review_queue(self) -> list[dict]:
        """
        Retorna a fila de revisao humana, ordenada por score decrescente.
        Cada item: {id, score, summary, risk_level, evidence_count}
        """
        # SEU CODIGO AQUI
        pass

    def summary(self) -> dict:
        """
        Retorna um resumo do pipeline: contagem por decisao, score medio,
        total de sugestoes processadas.
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# TESTES RAPIDOS
# ============================================================

if __name__ == "__main__":
    # Construir sugestoes a partir das fixtures
    suggestions = []
    for raw in GHOSTWRITER_SUGGESTIONS:
        s = Suggestion(
            suggestion_id=raw["id"],
            type=SuggestionType(raw["type"]),
            verifiability=Verifiability(raw["verifiability"]),
            risk_level=RiskLevel(raw["risk_level"]),
            evidence_count=raw["evidence_count"],
            summary=raw["summary"],
        )
        suggestions.append(s)

    gate = ConfidenceGate(suggestions=suggestions)
    results = gate.process_all()

    print("=" * 60)
    print("CONFIDENCE GATE — RESULTADOS")
    print("=" * 60)

    # Teste 1: Auto-deploys devem existir
    deploys = results["auto_deploy"]
    print(f"\nAuto-Deploy (FYI): {len(deploys)} sugestoes")
    for d in deploys:
        print(f"  {d.suggestion_id}: score={d.confidence_score:.2f} — {d.reason[:80]}")
    assert len(deploys) >= 2, f"Esperado >= 2 auto-deploys, obtido {len(deploys)}"
    print("  OK: sugestoes trivially_verifiable com baixo risco sao auto-deploy")

    # Teste 2: Human reviews devem existir
    reviews = results["human_review"]
    print(f"\nHuman Review: {len(reviews)} sugestoes")
    for d in reviews:
        print(f"  {d.suggestion_id}: score={d.confidence_score:.2f} — {d.reason[:80]}")
    assert len(reviews) >= 2, f"Esperado >= 2 human reviews, obtido {len(reviews)}"
    print("  OK: sugestoes com risco medio ou verifiability parcial vao para revisao")

    # Teste 3: Auto-discards devem existir
    discards = results["auto_discard"]
    print(f"\nAuto-Discard: {len(discards)} sugestoes")
    for d in discards:
        print(f"  {d.suggestion_id}: score={d.confidence_score:.2f} — {d.reason[:80]}")
    assert len(discards) >= 1, f"Esperado >= 1 auto-discard, obtido {len(discards)}"
    print("  OK: sugestoes com baixa evidencia ou alto risco + baixa verifiability sao descartadas")

    # Teste 4: Override manual
    gate.apply_manual_override("GW-007", Decision.HUMAN_REVIEW)
    gw7 = next(d for d in gate.decisions if d.suggestion_id == "GW-007")
    assert gw7.overridden, "GW-007 deve estar marcada como overridden"
    assert gw7.decision == Decision.HUMAN_REVIEW, "Override deve mudar para HUMAN_REVIEW"
    print(f"\n  OK: override manual de GW-007 para HUMAN_REVIEW aplicado")

    # Teste 5: FYI notifications
    fyi = gate.get_fyi_notifications()
    print(f"\nFYI Notifications: {len(fyi)}")
    for n in fyi:
        print(f"  {n[:100]}...")
    assert len(fyi) == len(deploys), "Numero de FYIs deve corresponder aos auto-deploys"

    # Teste 6: Review queue ordenada por score
    queue = gate.get_review_queue()
    print(f"\nReview Queue (ordenada por score):")
    for item in queue:
        print(f"  {item['id']}: score={item['score']:.2f}, risk={item['risk_level']}, evidence={item['evidence_count']}")
    if len(queue) >= 2:
        assert queue[0]["score"] >= queue[-1]["score"], "Fila deve estar ordenada por score decrescente"
    print("  OK: fila ordenada por score")

    # Resumo final
    s = gate.summary()
    print(f"\nRESUMO:")
    print(f"  Total processado: {s['total']}")
    print(f"  Auto-deploy: {s['auto_deploy']}")
    print(f"  Human review: {s['human_review']}")
    print(f"  Auto-discard: {s['auto_discard']}")
    print(f"  Score medio: {s['avg_score']:.2f}")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO CONFIDENCE GATE PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Pipeline com Historico de Automacao (25 min)

```python
# ============================================================
# EXTENSAO: Automation History Weight
# ============================================================

# Quando um tipo de sugestao tem historico de ser aprovada consistentemente
# em revisao humana, o score de confianca para futuras sugestoes do mesmo
# tipo deve aumentar (o sistema "aprende" que knowledge_fix e confiavel).

AUTOMATION_HISTORY = {
    "knowledge_fix": {"total": 45, "approved": 43, "reverted": 0},
    "response_tone": {"total": 12, "approved": 7, "reverted": 2},
    "journey_change": {"total": 8, "approved": 3, "reverted": 4},
    "policy_rewrite": {"total": 3, "approved": 1, "reverted": 2},
}

def compute_historical_bonus(suggestion_type: SuggestionType) -> float:
    """
    Calcula um bonus (ou penalidade) baseado no historico de aprovacao.

    Formula:
      approval_rate = approved / total
      penalty = reverted / total * 0.5  (reversoes sao penalizadas)
      bonus = (approval_rate - penalty) * 0.15  # max +0.15, min -0.10

    Returns:
        Bonus entre -0.10 e +0.15.
    """
    # SEU CODIGO AQUI
    pass


# Aplique o historical_bonus ao compute_confidence_score() e compare
# os resultados com e sem historico. O knowledge_fix (43/45 aprovadas)
# deve ganhar bonus; o journey_change (3/8, 4 revertidas) deve perder.

# TAREFA:
# 1. Recalcule os scores com compute_historical_bonus()
# 2. Alguma sugestao mudou de categoria (review → deploy ou discard → review)?
# 3. Isso e desejavel? Por que ou por que nao?
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce classificou manualmente as 8 sugestoes com justificativa
- [ ] Suas decisoes manuais sao consistentes com um criterio explicito

### Criterio 2: Confidence scoring

- [ ] `compute_confidence_score()` retorna scores > 0.80 para `trivially_verifiable + low_risk + alta_evidencia`
- [ ] `compute_confidence_score()` retorna scores < 0.40 para `requires_judgment + high_risk + baixa_evidencia`
- [ ] `risk_level: high` reduz o score (multiplicador 0.70)
- [ ] `evidence_count < 3` aplica penalidade de -0.15

### Criterio 3: Decision pipeline

- [ ] Pelo menos 2 sugestoes sao classificadas como AUTO_DEPLOY
- [ ] Pelo menos 2 sugestoes sao classificadas como HUMAN_REVIEW
- [ ] Pelo menos 1 sugestao e classificada como AUTO_DISCARD
- [ ] Override manual funciona corretamente

### Criterio 4: Audit trail

- [ ] Cada `DecisionRecord` tem `reason` explicativo
- [ ] `get_fyi_notifications()` gera notificacoes para todos os auto-deploys
- [ ] `get_review_queue()` retorna fila ordenada por score decrescente

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao classificou ou sem criterio | Classificou mas criterio inconsistente | Classificacao consistente com justificativa | Criterio explicito que antecipa o scorer |
| **Scoring (Parte 2)** | 35% | Scorer nao implementado | Scorer basico sem todos os fatores | Scorer completo com verifiability + risk + evidence | Historical bonus calibrado com dados de aprovacao |
| **Pipeline (Parte 2)** | 30% | Pipeline nao implementado | Processa mas sem audit trail | Pipeline completo com overrides e notificacoes | Pipeline + historical learning (Parte 3) |
| **Testes e verificacao** | 20% | Nenhum cenario passa | 2 criterios passam | 3 criterios passam | Todos os 4 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o Confidence Scorer

1. **Verifiability e o sinal mais forte.** Uma correcao `trivially_verifiable` (artigo A contradiz artigo B, resposta correta e unica) e intrinsecamente mais confiavel que uma sugestao que `requires_judgment` (tom de voz, politica de reembolso). O base score reflete isso: 0.85 vs 0.25.

2. **Risco multiplica, nao subtrai.** Um multiplicador de 0.70 significa que mesmo uma sugestao `trivially_verifiable` com `risk: high` tem score maximo de 0.85 * 0.70 = 0.595 — abaixo do threshold de auto-deploy. Isso e intencional: alto risco exige revisao humana independente da verifiability.

3. **Evidencia e um ajuste fino.** O evidence_count ajusta o score em +/- 0.10-0.15. Nao e o fator dominante — uma sugestao com 50 evidencias mas `requires_judgment + high_risk` ainda vai para revisao humana. Evidencia forte nao substitui julgamento.

### Para o Pipeline

1. **O threshold 0.80 nao e arbitrario.** Ele reflete o "customer comfort" da Sierra: "We don't want to pull the future forward too quickly." Auto-deploy so para o que e indiscutivelmente correto. Tudo que tem qualquer ambiguidade vai para revisao humana.

2. **Auto-discard nao e "jogar fora".** Sugestoes descartadas devem ser logadas com o motivo. Se 3 meses depois o mesmo problema aparecer em 50 conversas, o evidence_count sobe e a sugestao e reavaliada. O descarte e temporario, nao definitivo.

3. **O historical bonus fecha o loop.** Quando um tipo de sugestao tem 95% de aprovacao em revisao humana, o sistema aprende que pode confiar mais nesse tipo. Mas revertidas penalizam — uma unica reversao de `policy_rewrite` reduz a confianca em futuras sugestoes desse tipo.

---

## Duvidas Comuns

**P: Por que nao deployar tudo automaticamente e reverter se der problema?**
R: Porque reverter uma mudanca em producao que afetou 500 clientes e pior que revisar antes. O custo de uma revisao humana de 5 minutos e menor que o custo de uma reversao + pedido de desculpas + perda de confianca. O confidence gate existe para minimizar reversoes, nao para eliminar revisoes.

**P: Como calibrar os thresholds (0.80, 0.40)?**
R: Comece conservador (0.90, 0.50) e va reduzindo conforme o historico mostrar que o scorer e confiavel. Monitore a taxa de reversao das sugestoes auto-deployadas. Se for zero por 3 meses, reduza o threshold para 0.80. Se aparecer uma reversao, suba para 0.85 temporariamente.

**P: Isso nao e so um sistema de regras deterministicas?**
R: Sim, e intencional. A confianca e calculada deterministicamente a partir de sinais observaveis (verifiability, risk, evidence). Nao e uma caixa-preta de ML. Isso permite auditar cada decisao e ajustar os pesos com evidencias. O "aprendizado" vem do historical bonus — que e alimentado por dados reais de aprovacao e reversao.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/garbage-collection-day-meta-loop|GC Day Meta-Loop]]` — o padrao complementar de revisao periodica manual
2. Leia `[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]` para entender como o confidence gate se integra ao ciclo Analyze → Build → Release
3. (Opcional) Estenda o sistema com `stale_suggestion_detector`: sugestoes em `human_review` ha mais de 10 dias sem acao disparam um alerta

---

*Exercicio Confidence-Gated Learning | Nivel 2 - Padroes Praticos*

**Deploy automatico nao e sobre remover humanos — e sobre gastar atencao humana onde ela realmente importa.**
