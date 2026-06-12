---
title: "Exercicio 5: Formalizar Intent como Primitiva de Cinco Partes"
type: curriculum-exercise
nivel: 2
aliases: ["intent five-part primitive", "intent completeness gate", "intent estruturado", "five-field intent", "primitive de intencao", "gate de completude de intent"]
tags: [curriculo-conteudo, nivel-2, exercicio, agentes-orquestracao, spec-driven-development, intent-structure, constraint-engineering, harness-engineering, decision-discipline, python, dataclass]
relates-to: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[curriculum/02-nivel-2-practical-patterns/02-sprint-contracts|Sprint Contracts]]"]
last_updated: 2026-06-12
---
# Exercicio 5: Formalizar Intent como Primitiva de Cinco Partes
## Nivel 2 - Padroes Praticos

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** (Intermediario-Avancado)
**Pre-requisito:** Ter lido `02-sprint-contracts.md` (Nivel 2) + completado Exercicio 2
**Objetivo:** Diagnosticar os danos causados por intent subespecificado e implementar um Intent Completeness Gate que exige cinco campos antes de liberar um agente para execucao

---

## Prologo: O Agente Que Construiu a Coisa Errada com Excelencia

### Quinta-feira, 14h30. Uma feature que parecia simples.

```
CLIENTE: "A busca do KODA esta muito lenta. Precisamos melhorar."

PM: [Abre o Slack]
    "@dev_agent melhora a busca de produtos do KODA.
     Os clientes estao reclamando de lentidao."

DEV_AGENT: [Analisa o pedido... 3 segundos]
           "Entendido. Melhorar a busca de produtos."
```

**O que o agente fez nas 4 horas seguintes:**

O agente interpretou "melhorar a busca" como "reescrever o sistema de busca do zero". Ele:

1. Migrou de PostgreSQL full-text search para Elasticsearch
2. Implementou fuzzy matching com distancia de Levenshtein
3. Adicionou autocomplete com prefix tree
4. Criou um cache Redis de 3 camadas com warming preditivo
5. Reescreveu 2.400 linhas do codigo de busca

O resultado era tecnicamente impressionante. Latencia caiu de 800ms para 12ms. Throughput
subiu 40x. O codigo estava limpo, testado, documentado.

**O que o PM realmente queria:**

Que a busca respeitasse as restricoes alimentares do cliente. O problema nao era a engine
de busca -- era que o filtro de alergias estava sendo aplicado DEPOIS da busca, entao
clientes com restricao de lactose viam Whey Concentrado nos resultados e recebiam "produto
indisponivel" ao clicar. A "lentidao" era na verdade frustracao com resultados irrelevantes.

**O custo do mal-entendido:**

```
╔══════════════════════════════════════════════════════════════════╗
║           CUSTO DO INTENT SUBESPECIFICADO                        ║
║                                                                  ║
║  O que foi pedido:  "melhora a busca de produtos do KODA"       ║
║  O que foi feito:   Elasticsearch + fuzzy match + autocomplete   ║
║  O que era preciso: filtro de alergia ANTES da busca             ║
║                                                                  ║
║  Tokens gastos:      3.200.000                                   ║
║  Horas de agente:    4h12min                                     ║
║  Horas de rollback:  1h45min                                     ║
║  Codigo descartado:  2.400 linhas                                ║
║  Problema real:      NAO RESOLVIDO                               ║
║                                                                  ║
║  Se o intent tivesse sido especificado com 5 campos:             ║
║  Tokens gastos:      180.000                                     ║
║  Horas de agente:    22min                                       ║
║  Problema real:      RESOLVIDO na primeira tentativa             ║
╚══════════════════════════════════════════════════════════════════╝
```

**O que faltou no intent?**

O pedido "melhora a busca de produtos do KODA" tinha apenas 1 dos 5 campos necessarios
(descricao). Faltaram:

| Campo | Status | Consequencia da Ausencia |
|---|---|---|
| **Descricao** | Presente | "melhora a busca" -- ok |
| **Constraints** | AUSENTE | Agente nao sabia que alergias sao bloqueantes, orcamento e teto, apenas produtos em estoque |
| **Failure Scenarios** | AUSENTE | Agente nao sabia que "produto com lactose aparece e depois some" era o bug real |
| **Success Scenarios** | AUSENTE | Agente nao sabia que "cliente com restricao de lactose ve 3 produtos seguros" era o objetivo |
| **Connections** | AUSENTE | Agente nao sabia que a busca compartilha catalogo com recomendacao e checkout |

**Sua missao:** Construir um Intent Completeness Gate que impede que um agente comece a
trabalhar antes que todos os 5 campos estejam preenchidos e validados.

---

## O Cenario: Pipeline de Dispatch do KODA sem Gate de Intent

### Contexto

Voce recebeu o codigo de um `AgentDispatcher` que recebe intents em linguagem natural e
dispara agentes para implementa-los. O dispatcher atual **nao valida a completude do intent**
antes de liberar o agente. O resultado e previsivel: agentes passam horas implementando a
coisa errada com excelencia.

O `AgentDispatcher` atual:

```python
def dispatch_agent(intent_text: str):
    """Dispatcher atual -- SEM validacao de completude."""
    agent = Agent()
    agent.execute(intent_text)  # vai fundo sem checar nada
```

Voce vai adicionar um `IntentCompletenessGate` que:

1. Exige que o intent seja estruturado em 5 campos
2. Valida cada campo contra criterios minimos de qualidade
3. Rejeita intents incompletos com perguntas especificas para o outcome owner
4. So libera o agente quando todos os 5 campos passam

### Dados de Entrada

O gate recebe um `RawIntent` -- o que o outcome owner (PM, stakeholder) escreveu:

```json
{
  "intent_id": "INT-2026-047",
  "author": "pm_fernanda",
  "raw_text": "Melhora a busca de produtos do KODA. Os clientes estao reclamando de lentidao.",
  "domain": "product_search",
  "urgency": "high"
}
```

E produz um `StructuredIntent` com os 5 campos preenchidos e validados -- ou uma lista de
perguntas pendentes para o author.

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Cinco campos obrigatorios:** O `StructuredIntent` deve conter: `description`, `constraints`, `failure_scenarios`, `success_scenarios`, `connections`
2. **RF2 - Gate de completude:** O `IntentCompletenessGate` avalia cada campo e retorna `PASS`, `FAIL`, ou `NEEDS_CLARIFICATION`
3. **RF3 - Perguntas direcionadas:** Para cada campo que falha, o gate gera de 1 a 3 perguntas especificas para o author -- nunca genericas como "descreva melhor"
4. **RF4 - Minimo de 1 por campo:** Cada campo deve ter pelo menos 1 entrada. Campos vazios sao automaticamente `FAIL`
5. **RF5 - Connections devem ser wikilinks:** O campo `connections` referencia outros intents, sistemas, ou documentos por ID. Conexoes sem ID sao rejeitadas
6. **RF6 - Constraints sao verificaveis:** Cada constraint deve ser redigida como uma afirmacao booleana (passivel de verificacao automatizada). Constraints vagas como "deve ser bom" sao rejeitadas
7. **RF7 - Audit trail:** Toda decisao do gate (PASS/FAIL/NEEDS_CLARIFICATION) gera um `GateDecision` com timestamp, racional, e perguntas pendentes

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Gate como funcao pura:** `evaluate_intent(intent) -> GateDecision` -- deterministico, sem efeitos colaterais
3. **RT3 - Validacao por campo:** Cada um dos 5 campos tem sua propria funcao de validacao
4. **RT4 - StructuredIntent imutavel:** Uma vez aprovado, o `StructuredIntent` nao pode ser alterado

---

## Sua Tarefa

Voce vai implementar o Intent Completeness Gate em 3 partes.

---

### Parte 1: Diagnosticar Intents Incompletos (15 min)

Analise os 3 intents abaixo. Cada um foi responsavel por um agente que construiu a coisa
errada. Para cada intent, identifique quais campos estao ausentes e qual foi o dano.

```python
# Intent A: "Adiciona dark mode no dashboard do KODA"
# O que o agente fez: reescreveu todo o CSS do dashboard (1.800 linhas),
# introduziu 14 bugs visuais, e o time de analytics (unico usuario do
# dashboard) nunca pediu dark mode -- pediu exportacao de CSV.
INTENT_A = {
    "description": "Adiciona dark mode no dashboard do KODA",
    "constraints": [],
    "failure_scenarios": [],
    "success_scenarios": [],
    "connections": [],
}

# Intent B: "Otimiza o pipeline de recomendacao para ser mais rapido"
# O que o agente fez: removeu a etapa de verificacao de alergia do pipeline
# porque era o passo mais lento (2.3s). Latencia caiu de 4.1s para 0.9s.
# Primeiro teste em producao: cliente com alergia a lactose recebeu Whey
# Concentrado como recomendacao principal.
INTENT_B = {
    "description": "Otimiza o pipeline de recomendacao para ser mais rapido",
    "constraints": [],
    "failure_scenarios": [],
    "success_scenarios": ["Recomendacao gerada em menos de 1 segundo"],
    "connections": [],
}

# Intent C: "Integra o KODA com o sistema de logistica para tracking de pedidos"
# O que o agente fez: construiu uma integracao completa com a API dos Correios,
# mas o sistema de logistica que o time usa e uma API interna (Loggi), nao os
# Correios. O agente passou 6 horas integrando com a API errada.
INTENT_C = {
    "description": "Integra o KODA com o sistema de logistica para tracking de pedidos",
    "constraints": ["Usar API REST", "Timeout maximo de 5 segundos"],
    "failure_scenarios": ["Tracking indisponivel: mostrar mensagem amigavel"],
    "success_scenarios": ["Cliente digita codigo e ve status do pedido em segundos"],
    "connections": [],
}

# TAREFA: Responda no seu codigo como comentario:
#
# Para cada intent (A, B, C):
# 1. Quais campos estao vazios ou insuficientes?
# 2. Qual foi o dano causado pela ausencia de cada campo?
# 3. Reescreva o intent com TODOS os 5 campos preenchidos adequadamente
#    (minimo 1 entrada por campo, constraints como booleanos verificaveis)
```

**Resposta esperada (em comentario):**

```python
# INTENT_A: "Adiciona dark mode no dashboard do KODA"
# 1. Campos ausentes: constraints (vazio), failure_scenarios (vazio),
#    success_scenarios (vazio), connections (vazio)
# 2. Dano: sem constraints = sem verificacao de "quem precisa disso?".
#    Sem connections = agente nao sabia que o time de analytics queria CSV,
#    nao dark mode. 1.800 linhas de CSS descartadas.
# 3. StructuredIntent reescrito:
#    description: "Adicionar toggle de tema claro/escuro no dashboard do KODA"
#    constraints: [
#      "Tema escuro nao altera layout ou posicao de elementos",
#      "Toggle persiste preferencia por usuario (localStorage)",
#      "Contraste de texto >= 4.5:1 em todas as combinacoes de cor",
#    ]
#    failure_scenarios: [
#      "Toggle quebrado: dashboard permanece funcional com tema claro",
#      "Texto ilegivel: reverter para tema claro e logar violacao de contraste",
#    ]
#    success_scenarios: [
#      "Usuario clica toggle e dashboard alterna entre claro e escuro em <200ms",
#      "Preferencia de tema sobrevive a refresh de pagina e nova sessao",
#    ]
#    connections: [
#      "ANALYTICS-002 (exportacao CSV -- NAO escopo deste intent)",
#      "DASHBOARD-V2 (design system de cores do dashboard)",
#    ]
```

---

### Parte 2: Implementar o Intent Completeness Gate (30 min)

Implemente as funcoes de validacao e o gate. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class GateVerdict(Enum):
    PASS = "pass"
    FAIL = "fail"
    NEEDS_CLARIFICATION = "needs_clarification"


@dataclass
class StructuredIntent:
    """
    Intent formalizado como primitiva de cinco partes.

    Cada campo e obrigatorio e deve ter pelo menos 1 entrada.
    Uma vez aprovado pelo gate, este objeto e imutavel -- o agente
    usa exatamente estas especificacoes para guiar a execucao.
    """
    intent_id: str
    author: str

    # Campo 1: O que deve ser feito (uma frase)
    description: str

    # Campo 2: Limites que o trabalho DEVE respeitar
    # Cada constraint e uma afirmacao booleana verificavel.
    # Ex: "Nenhum produto recomendado contem alergeno do cliente"
    constraints: list[str] = field(default_factory=list)

    # Campo 3: Cenarios que definem output ERRADO
    # Cada cenario descreve uma situacao especifica de falha e o
    # comportamento esperado do sistema nessa situacao.
    failure_scenarios: list[str] = field(default_factory=list)

    # Campo 4: Cenarios que definem output CERTO
    # Cada cenario descreve o que o usuario ve/experimenta quando
    # o trabalho esta concluido com sucesso.
    success_scenarios: list[str] = field(default_factory=list)

    # Campo 5: Conexoes com outros intents, sistemas, docs
    # Cada conexao referencia um ID externo (outro intent, sistema,
    # documento canonical). Conexoes sem ID sao rejeitadas.
    connections: list[str] = field(default_factory=list)

    def is_complete(self) -> bool:
        """Verifica se todos os 5 campos tem pelo menos 1 entrada."""
        return all([
            bool(self.description.strip()),
            len(self.constraints) >= 1,
            len(self.failure_scenarios) >= 1,
            len(self.success_scenarios) >= 1,
            len(self.connections) >= 1,
        ])


@dataclass
class FieldValidation:
    """Resultado da validacao de um unico campo do intent."""
    field_name: str
    verdict: GateVerdict
    issues: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)


@dataclass
class GateDecision:
    """Decisao completa do Intent Completeness Gate."""
    intent_id: str
    verdict: GateVerdict
    field_validations: list[FieldValidation] = field(default_factory=list)
    pending_questions: list[str] = field(default_factory=list)
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evaluated_by: str = "IntentCompletenessGate"

    @property
    def passed_fields(self) -> list[str]:
        return [fv.field_name for fv in self.field_validations if fv.verdict == GateVerdict.PASS]

    @property
    def failed_fields(self) -> list[str]:
        return [fv.field_name for fv in self.field_validations if fv.verdict != GateVerdict.PASS]


# ============================================================
# FIELD VALIDATORS
# ============================================================

def validate_description(intent: StructuredIntent) -> FieldValidation:
    """
    Valida o campo 'description'.

    Criterios:
    1. Nao pode ser vazio
    2. Deve ter pelo menos 10 palavras (nao e um titulo, e uma descricao)
    3. Deve conter um verbo de acao ("implementar", "corrigir", "adicionar",
       "remover", "alterar", "migrar")
    4. Deve mencionar o sistema ou componente afetado
    5. Nao deve conter palavras ambiguas como "melhorar", "otimizar" sem
       especificar a metrica (ex: "melhorar a busca" -> NEEDS_CLARIFICATION)
    """
    # SEU CODIGO AQUI
    pass


def validate_constraints(intent: StructuredIntent) -> FieldValidation:
    """
    Valida o campo 'constraints'.

    Criterios:
    1. Deve ter pelo menos 1 constraint
    2. Cada constraint deve ser redigida como afirmacao booleana verificavel:
       - CORRETO: "Nenhum produto recomendado contem alergeno do cliente"
       - ERRADO: "Deve ser bom" (vago, nao verificavel)
       - ERRADO: "Performance aceitavel" (nao define o que e aceitavel)
    3. Constraints nao podem conter palavras ambiguas sem quantificador:
       "rapido", "bom", "eficiente", "escalavel", "robusto" -- todas
       precisam de definicao numerica ou booleana
    4. Constraints devem ser independentes entre si (nao redundantes)
    """
    # SEU CODIGO AQUI
    pass


def validate_failure_scenarios(intent: StructuredIntent) -> FieldValidation:
    """
    Valida o campo 'failure_scenarios'.

    Criterios:
    1. Deve ter pelo menos 1 cenario
    2. Cada cenario deve descrever:
       a. O que especificamente falhou (condicao)
       b. Qual o comportamento esperado do sistema nessa falha
       Ex: "API de catalogo indisponivel: exibir produtos cacheados
            com aviso 'resultados podem estar desatualizados'"
    3. Cenarios vagos como "se der erro, tratar" sao rejeitados
    4. Deve cobrir pelo menos 2 tipos de falha diferentes (ex: timeout
       e dados invalidos, nao apenas 2 variacoes de timeout)
    """
    # SEU CODIGO AQUI
    pass


def validate_success_scenarios(intent: StructuredIntent) -> FieldValidation:
    """
    Valida o campo 'success_scenarios'.

    Criterios:
    1. Deve ter pelo menos 1 cenario
    2. Cada cenario deve descrever o estado OBSERVAVEL apos o sucesso --
       o que o usuario ve, ouve, ou pode fazer que antes nao podia
    3. Cenarios devem ser da perspectiva do OUTCOME OWNER, nao do desenvolvedor:
       - CORRETO: "Cliente com restricao de lactose ve apenas produtos seguros"
       - ERRADO: "Codigo passa nos testes" (perspectiva errada)
    4. Cenarios devem ser independentes -- nao podem ser o mesmo cenario
       com palavras diferentes
    """
    # SEU CODIGO AQUI
    pass


def validate_connections(intent: StructuredIntent) -> FieldValidation:
    """
    Valida o campo 'connections'.

    Criterios:
    1. Deve ter pelo menos 1 conexao
    2. Cada conexao deve referenciar um ID externo no formato:
       "TYPE-ID (descricao curta)"
       Ex: "INTENT-042 (recomendacao cross-sell)"
       Ex: "CANONICAL-allergy-blocking (constraint de alergia)"
    3. Conexoes sem ID (apenas descricao) sao rejeitadas
    4. Conexoes devem ser relevantes -- mencionar sistemas, intents ou
       docs que seriam AFETADOS ou que AFETAM este trabalho
    5. Pelo menos 1 conexao deve ser um intent ID ou canonical doc ID
    """
    # SEU CODIGO AQUI
    pass


# ============================================================
# INTENT COMPLETENESS GATE
# ============================================================

def evaluate_intent(intent: StructuredIntent) -> GateDecision:
    """
    Avalia um StructuredIntent contra os 5 criterios de completude.

    Esta funcao e o nucleo do Intent Completeness Gate. Ela executa
    os 5 validadores de campo e produz um GateDecision.

    Regras de verdict agregado:
    - Se TODOS os campos passam: verdict = PASS
    - Se ALGUM campo falha com FAIL: verdict = FAIL
    - Se nenhum campo falha com FAIL mas ALGUM retorna NEEDS_CLARIFICATION:
      verdict = NEEDS_CLARIFICATION

    Para cada campo que nao passa, o gate gera perguntas direcionadas
    para o author. As perguntas NAO devem ser genericas -- devem ser
    especificas ao conteudo do campo.

    Args:
        intent: O StructuredIntent a ser avaliado.

    Returns:
        GateDecision com verdict, validacoes por campo, e perguntas pendentes.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Executar os 5 validadores
    #    fv_desc = validate_description(intent)
    #    fv_cons = validate_constraints(intent)
    #    fv_fail = validate_failure_scenarios(intent)
    #    fv_succ = validate_success_scenarios(intent)
    #    fv_conn = validate_connections(intent)
    #
    # 2. Coletar field_validations em uma lista
    #
    # 3. Determinar verdict agregado:
    #    - Se existe algum FAIL: verdict = FAIL
    #    - Senao, se existe algum NEEDS_CLARIFICATION: NEEDS_CLARIFICATION
    #    - Senao: PASS
    #
    # 4. Coletar perguntas de todos os campos que nao passaram
    #
    # 5. Retornar GateDecision
    pass


# ============================================================
# TESTES RAPIDOS: Validadores de Campo
# ============================================================

if __name__ == "__main__":
    # Teste 1: Description vazia deve falhar
    intent_vazio = StructuredIntent(
        intent_id="TEST-001", author="test",
        description="",
    )
    fv = validate_description(intent_vazio)
    assert fv.verdict != GateVerdict.PASS, "Descricao vazia deve falhar"
    print("Teste 1 passou: descricao vazia rejeitada")

    # Teste 2: Description com "melhorar" sem metrica
    intent_vago = StructuredIntent(
        intent_id="TEST-002", author="test",
        description="Melhora a busca de produtos",
    )
    fv = validate_description(intent_vago)
    assert fv.verdict == GateVerdict.NEEDS_CLARIFICATION, (
        f"Descricao vaga deve pedir clarificacao, obtido {fv.verdict}"
    )
    print("Teste 2 passou: descricao vaga detectada")

    # Teste 3: Constraints com palavras ambiguas
    intent_ambiguo = StructuredIntent(
        intent_id="TEST-003", author="test",
        description="Implementar busca de produtos com filtro de alergia",
        constraints=["Deve ser rapido", "Performance aceitavel"],
    )
    fv = validate_constraints(intent_ambiguo)
    assert fv.verdict != GateVerdict.PASS, (
        f"Constraints ambiguas devem falhar, obtido {fv.verdict}"
    )
    print("Teste 3 passou: constraints ambiguas rejeitadas")

    # Teste 4: Intent completo deve passar
    intent_completo = StructuredIntent(
        intent_id="TEST-004", author="pm_fernanda",
        description="Implementar filtro de alergia no pipeline de busca para que produtos com alergenos do cliente nunca aparecam nos resultados",
        constraints=[
            "Nenhum produto com alergeno do cliente aparece nos resultados de busca",
            "Filtro de alergia e aplicado ANTES da busca, nao depois",
            "Tempo de resposta da busca nao aumenta mais que 15%",
            "Catalogo de produtos mantem a flag lactose_free como source of truth",
        ],
        failure_scenarios=[
            "Catalogo indisponivel: busca retorna resultados sem filtro MAS com aviso 'Verifique restricoes alimentares' em negrito",
            "Cliente sem perfil de alergia: busca funciona normalmente sem filtro",
            "Filtro remove todos os resultados: exibir 'Nenhum produto compativel encontrado. Um atendente humano entrara em contato.'",
        ],
        success_scenarios=[
            "Cliente com restricao de lactose busca 'whey' e ve apenas produtos com lactose_free=True",
            "Cliente sem restricoes busca 'whey' e ve todos os produtos (sem mudanca de comportamento)",
            "Cliente adiciona nova alergia no perfil e a busca seguinte ja reflete a restricao",
        ],
        connections=[
            "INTENT-041 (catalogo de produtos com flag de alergeno)",
            "INTENT-012 (perfil de cliente com restricoes alimentares)",
            "CANONICAL-allergy-blocking (constraint de alergia como invariante)",
        ],
    )
    decision = evaluate_intent(intent_completo)
    assert decision.verdict == GateVerdict.PASS, (
        f"Intent completo deve passar, obtido {decision.verdict}. "
        f"Falhas: {decision.failed_fields}"
    )
    print("Teste 4 passou: intent completo aprovado")
    print(f"  Campos aprovados: {decision.passed_fields}")

    # Teste 5: Connections sem IDs
    intent_sem_ids = StructuredIntent(
        intent_id="TEST-005", author="test",
        description="Implementar filtro de alergia no pipeline de busca",
        constraints=["Alergenos bloqueiam produtos"],
        failure_scenarios=["Erro de API: mostrar fallback"],
        success_scenarios=["Cliente ve produtos seguros"],
        connections=["sistema de catalogo", "perfil do cliente"],  # sem IDs
    )
    fv = validate_connections(intent_sem_ids)
    assert fv.verdict != GateVerdict.PASS, (
        f"Conexoes sem IDs devem falhar, obtido {fv.verdict}"
    )
    print("Teste 5 passou: conexoes sem ID rejeitadas")

    print("\nTodos os testes dos validadores passaram!")
```

---

### Parte 3: Pipeline de Dispatch com Gate (25 min)

Agora implemente o pipeline completo que integra o `IntentCompletenessGate` ao
`AgentDispatcher`. O dispatcher modificado NAO pode liberar o agente enquanto o
gate nao retornar PASS.

```python
# ============================================================
# AGENT DISPATCHER COM INTENT COMPLETENESS GATE
# ============================================================

@dataclass
class DispatchResult:
    """Resultado de uma tentativa de dispatch."""
    intent_id: str
    dispatched: bool
    gate_decision: GateDecision
    agent_output: str = ""
    error: str = ""


def dispatch_with_gate(intent: StructuredIntent, max_clarification_rounds: int = 3) -> DispatchResult:
    """
    Pipeline de dispatch COM Intent Completeness Gate.

    Fluxo:
    1. Avaliar intent com evaluate_intent()
    2. Se PASS: liberar agente para execucao
    3. Se NEEDS_CLARIFICATION:
       a. Retornar perguntas para o author
       b. Author revisa o intent e reenvia
       c. Re-avaliar (ate max_clarification_rounds vezes)
    4. Se FAIL: retornar erros especificos -- intent precisa ser reescrito
    5. Registrar GateDecision no audit trail

    Args:
        intent: O StructuredIntent a ser avaliado e potencialmente executado.
        max_clarification_rounds: Numero maximo de rodadas de clarificacao.

    Returns:
        DispatchResult com status do dispatch.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Avaliar intent
    # 2. Se PASS: chamar simulated_agent_execute(intent) e retornar DispatchResult
    # 3. Se NEEDS_CLARIFICATION:
    #    a. Coletar perguntas do gate_decision
    #    b. Simular resposta do author (funcao simulate_author_clarification)
    #    c. Aplicar clarificacao ao intent e reavaliar
    #    d. Repetir ate max_clarification_rounds
    # 4. Se FAIL: retornar DispatchResult com dispatched=False
    pass


def simulated_agent_execute(intent: StructuredIntent) -> str:
    """
    Simula a execucao do agente (NAO implemente o agente de verdade).

    Retorna uma string descrevendo o que o agente faria, baseado nos
    5 campos do intent. Esta funcao serve apenas para demonstrar que
    o gate liberou o agente.
    """
    return (
        f"[AGENTE] Iniciando execucao do intent {intent.intent_id}\n"
        f"  Descricao: {intent.description[:80]}...\n"
        f"  Constraints: {len(intent.constraints)} ativas\n"
        f"  Failure scenarios: {len(intent.failure_scenarios)} mapeados\n"
        f"  Success scenarios: {len(intent.success_scenarios)} definidos\n"
        f"  Connections: {len(intent.connections)} referencias\n"
        f"  Status: EXECUTANDO (gate aprovou dispatch)"
    )


# ============================================================
# TESTE COMPLETO DO PIPELINE
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTE DO PIPELINE DE DISPATCH COM GATE")
    print("=" * 60)

    # Cenario 1: Intent completo -> dispatch imediato
    print("\n--- Cenario 1: Intent Completo ---")
    intent_ok = StructuredIntent(
        intent_id="INT-042", author="pm_fernanda",
        description="Implementar filtro de alergia no pipeline de busca para KODA",
        constraints=[
            "Nenhum produto com alergeno do cliente aparece nos resultados",
            "Filtro aplicado ANTES da consulta ao catalogo",
        ],
        failure_scenarios=[
            "Catalogo offline: exibir mensagem com fallback para busca sem filtro",
            "Cliente sem perfil: busca normal sem filtro de alergia",
        ],
        success_scenarios=[
            "Cliente com alergia a lactose busca 'whey' e ve apenas produtos lactose_free=True",
            "Cliente sem alergia nao percebe diferenca no comportamento da busca",
        ],
        connections=[
            "INTENT-041 (catalogo com flag lactose_free)",
            "CANONICAL-allergy-blocking (constraint de dominio)",
        ],
    )
    result = dispatch_with_gate(intent_ok)
    print(f"  Dispatched: {result.dispatched}")
    print(f"  Gate verdict: {result.gate_decision.verdict.value}")
    assert result.dispatched, "Intent completo deve ser dispatcher!"
    assert result.gate_decision.verdict == GateVerdict.PASS

    # Cenario 2: Intent incompleto -> rejeitado
    print("\n--- Cenario 2: Intent Incompleto ---")
    intent_ruim = StructuredIntent(
        intent_id="INT-043", author="dev_carlos",
        description="Melhora a busca",
        # todos os outros campos vazios
    )
    result = dispatch_with_gate(intent_ruim)
    print(f"  Dispatched: {result.dispatched}")
    print(f"  Gate verdict: {result.gate_decision.verdict.value}")
    print(f"  Campos reprovados: {result.gate_decision.failed_fields}")
    assert not result.dispatched, "Intent incompleto NAO deve ser dispatcher!"

    # Cenario 3: Intent com clarificacao -> perguntas geradas
    print("\n--- Cenario 3: Intent com Clarificacao Pendente ---")
    intent_vago = StructuredIntent(
        intent_id="INT-044", author="pm_fernanda",
        description="Otimiza o pipeline de recomendacao para ser mais rapido",
        constraints=["Deve ser eficiente"],
        failure_scenarios=["Se der erro, tratar"],
        success_scenarios=["Pipeline mais rapido"],
        connections=["sistema de recomendacao"],
    )
    result = dispatch_with_gate(intent_vago)
    print(f"  Dispatched: {result.dispatched}")
    print(f"  Gate verdict: {result.gate_decision.verdict.value}")
    if result.gate_decision.pending_questions:
        print(f"  Perguntas pendentes ({len(result.gate_decision.pending_questions)}):")
        for q in result.gate_decision.pending_questions:
            print(f"    - {q}")

    print("\n" + "=" * 60)
    print("PIPELINE DE DISPATCH COM GATE COMPLETO")
    print("=" * 60)
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Validadores de campo funcionais

- [ ] `validate_description()` detecta descricao vazia, vaga ("melhorar"/"otimizar" sem metrica) e muito curta (< 10 palavras)
- [ ] `validate_constraints()` detecta constraints ambiguas ("bom", "rapido", "eficiente" sem quantificador)
- [ ] `validate_failure_scenarios()` detecta cenarios vagos que nao descrevem condicao + comportamento
- [ ] `validate_success_scenarios()` detecta cenarios escritos da perspectiva errada ("codigo passa nos testes")
- [ ] `validate_connections()` detecta conexoes sem ID externo

### Criterio 2: Gate funcional

- [ ] `evaluate_intent()` retorna `PASS` apenas quando TODOS os 5 campos passam
- [ ] `evaluate_intent()` retorna `FAIL` quando pelo menos 1 campo falha com FAIL
- [ ] `evaluate_intent()` retorna `NEEDS_CLARIFICATION` quando campos sao insuficientes mas nao totalmente invalidos
- [ ] Perguntas geradas sao ESPECIFICAS ao conteudo do campo, nao genericas

### Criterio 3: Pipeline de dispatch

- [ ] Intent completo (5 campos validos) -> dispatch imediato (`dispatched=True`)
- [ ] Intent incompleto (campos vazios) -> dispatch bloqueado (`dispatched=False`)
- [ ] Intent vago (precisa clarificacao) -> perguntas geradas, dispatch bloqueado

### Criterio 4: Diagnostico (Parte 1)

- [ ] Voce consegue identificar os campos ausentes nos Intents A, B, C
- [ ] Voce consegue reescrever cada intent com todos os 5 campos
- [ ] Voce consegue explicar como cada campo ausente contribuiu para o dano

---

## Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou campos ausentes | Identificou parcialmente | Identificou todos os campos ausentes e o dano | Diagnostico completo + reescrita de todos os 3 intents |
| **Validadores (Parte 2)** | 35% | Validadores nao implementados ou sem criterios | Validam campos vazios mas nao detectam vagueza | Detectam vagueza, ambiguidade, e falta de verificabilidade | Cobertura completa: 5 validadores com criterios especificos e perguntas direcionadas |
| **Gate e Pipeline (Parte 3)** | 35% | Gate nao implementado | Gate avalia mas pipeline nao integra | Pipeline integrado: gate bloqueia dispatch de intents incompletos | Pipeline completo com audit trail,clarification rounds, e mensagens de erro informativas |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 2 criterios passam | 3 criterios passam | Todos os 4 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para os Validadores

1. **Constraints como booleanos.** "Deve ser rapido" e inutil. "Tempo de resposta p95 <= 200ms" e verificavel. Treine seu validador para rejeitar a primeira e aceitar a segunda.
2. **Failure scenarios precisam de condicao + comportamento.** "Se der erro" nao e um cenario. "Se API de catalogo retornar 503: exibir produtos cacheados com aviso de dados potencialmente desatualizados" e um cenario.
3. **Success scenarios sao da perspectiva do outcome owner.** O PM nao quer saber se o codigo passa nos testes. Ele quer saber se o cliente consegue buscar produtos sem ver alergenos.

### Para o Gate

1. **A distincao FAIL vs NEEDS_CLARIFICATION e crucial.** FAIL = "este campo esta objetivamente errado" (vazio, formato invalido). NEEDS_CLARIFICATION = "este campo existe mas nao tem qualidade suficiente para guiar um agente" (vago, ambiguo).
2. **Perguntas direcionadas economizam mais tokens que o gate gasta.** Uma pergunta especifica como "Qual a metrica de latencia que define 'rapido'? (ex: p95 < 200ms)" gera uma resposta que fecha o gap. Uma pergunta generica como "Descreva melhor" gera mais idas e vindas.
3. **Connections previnem o maior desperdicio: integrar com a API errada.** Se o INTENT-C tivesse `connections: ["LOGISTICS-Loggi (API interna de tracking)"]`, o agente nao teria passado 6 horas integrando com os Correios.

---

## Duvidas Comuns

**P: Isso nao e burocracia? O agente nao consegue inferir o que falta?**
R: O agente CONSEGUE inferir. Esse e exatamente o problema. Quando o agente infere constraints, ele infere as constraints que tornam a implementacao mais FACIL, nao as que tornam o resultado mais UTIL para o outcome owner. O gate existe para que o humano tome decisoes de valor e o agente execute decisoes de implementacao.

**P: Todo intent precisa passar pelo gate? E spikes exploratorios?**
R: Intents marcados como `experiment` ou `spike` podem ter um gate mais leve (apenas description + success_scenarios obrigatorios). Mas intents que vao para producao ou afetam usuarios precisam dos 5 campos. O gate pode ser configurado com diferentes niveis de rigor.

**P: Como isso se relaciona com o Grill-Me Alignment Interview?**
R: O Grill-Me captura decisoes via entrevista estruturada. O Intent Completeness Gate valida que o output da entrevista (ou de qualquer outra fonte de intent) tem a estrutura minima para guiar um agente. Sao complementares: Grill-Me produz o intent, o Gate valida se ele esta completo.

**P: O que acontece se o author nao souber responder uma pergunta do gate?**
R: Isso e um sinal de que o trabalho nao esta pronto para ser implementado. O gate registra um `DEFER` e o intent volta para a fase de discovery. E melhor descobrir que "ninguem sabe qual metrica define sucesso" ANTES de gastar 3.2 milhoes de tokens.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns.md` para entender o contexto completo do padrao
2. Compare com o canonical doc `docs/canonical/grill-me-alignment-interview.md` -- observe como a entrevista produz intents e como o gate os validaria
3. (Opcional) Adapte o gate para validar intents em formato JSON Schema e integre com o pipeline de dispatch do KODA

---

*Exercicio 5 | Nivel 2 - Padroes Praticos | Intent as Five-Part Primitive*

**Nunca mais "melhora a busca".**
