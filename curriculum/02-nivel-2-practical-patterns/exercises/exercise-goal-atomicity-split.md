---
title: "Exercicio: Decompor Metas Multiplas com Goal Atomicity Split"
type: curriculum-exercise
nivel: 2
aliases: ["goal atomicity split", "atomic goal decomposition", "divisao atomica metas", "one goal one sentence", "conjunction split", "multi-goal intent"]
tags: [curriculo-conteudo, nivel-2, exercicio, agentes-orquestracao, spec-driven-development, decision-discipline, intent-structure, harness-engineering, python, dataclass]
relates-to: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]", "[[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]"]
last_updated: 2026-06-14
---
# Exercicio: Decompor Metas Multiplas com Goal Atomicity Split
## Nivel 2 - Padroes Praticos

**Tempo Estimado:** 45-60 minutos
**Dificuldade:** (Intermediario)
**Pre-requisito:** Ter completado Exercicio 5 (Intent Five-Part Primitive) + Exercicio Two-Implementations Goal Test
**Objetivo:** Diagnosticar os danos de intents multi-meta e implementar um GoalAtomicitySplitter que garante uma meta por sentenca, detectando e dividindo em conjuncoes

---

## Prologo: O Intent Que Tinha 3 Metas e Nenhum Resultado

### Quinta-feira, 9h00. Um card que o time de produto escreveu em 3 minutos.

```
PM: "@dev_agent implementa o novo checkout do KODA. Adiciona suporte
     a cupom de desconto, calcula frete pelos Correios, e envia
     confirmacao por email e WhatsApp."
```

**O que o agente fez nas 7 horas seguintes:**

O agente leu o intent e identificou 4 coisas para fazer: cupom, frete, email, WhatsApp. Ele estimou 2 horas por item e comecou:

```
09:00-10:15  Cupom de desconto: implementado. Testes passam.
10:15-12:30  Calculo de frete: integrado com API dos Correios. OK.
12:30-13:45  Email de confirmacao: template HTML, SMTP configurado. OK.
13:45-15:00  WhatsApp: integracao com Twilio. Testes passam.
15:00-16:00  Testes de integracao. Tudo verde.
```

Sete horas. Quatro funcionalidades. Pull request de 3.100 linhas. **Review rejeitado em 12 minutos.**

```
REVIEWER: "Isso sao QUATRO tarefas diferentes. Nao da para revisar.
          E o cupom nao funciona com frete gratis -- nao foi testado.
          E o email esta em HTML mas o KODA e so texto.
          E o WhatsApp usa Twilio mas o contrato e com a Zenvia.
          E o calculo de frete dos Correios nao considera o desconto
          do cupom -- o cliente recebeu desconto no produto mas pagou
          frete cheio. Isso e um bug de consistencia."
```

**O que aconteceu:**

O intent era "adiciona cupom E calcula frete E envia email E envia WhatsApp". Quatro metas em uma sentenca, zero coordenacao entre elas. O agente implementou cada uma isoladamente, sem perceber que elas interagiam. O cupom nao afetava o frete. O email nao combinava com o WhatsApp. Cada meta foi entregue, mas o resultado integrado era pior que a soma das partes.

```
╔══════════════════════════════════════════════════════════════════╗
║           CUSTO DO INTENT MULTI-META                             ║
║                                                                  ║
║  O que foi pedido:  4 funcionalidades em 1 sentenca              ║
║  O que foi feito:   4 implementacoes isoladas, 3.100 linhas      ║
║  O que deu errado:                                               ║
║    - Cupom e frete nao interagem (bug de consistencia)           ║
║    - Email usa HTML mas KODA e texto (formato errado)            ║
║    - WhatsApp usa Twilio mas contrato e Zenvia (API errada)      ║
║    - Nenhum teste cross-feature foi escrito                      ║
║                                                                  ║
║  Codigo descartado:  2.400 linhas (77%)                          ║
║  Tempo ate rework:   3 dias (revisao + reimplementacao)          ║
║                                                                  ║
║  Se o intent tivesse sido dividido em 4 metas atomicas:          ║
║  - Cada meta teria seu proprio intent com constraints            ║
║  - Dependencias entre metas seriam explicitas                    ║
║  - Cada meta seria revisada e testada independentemente          ║
║  - A integracao seria um quinto intent, nao uma surpresa         ║
╚══════════════════════════════════════════════════════════════════╝
```

**A regra que teria evitado tudo:**

> Uma meta = uma sentenca. Sem "e". Sem "tambem". Sem "alem disso". Se a sentenca tem conjuncao, sao duas metas.

- "Adiciona suporte a cupom de desconto" → 1 meta
- "Calcula frete pelos Correios" → 1 meta
- "Envia confirmacao por email" → 1 meta
- "Envia confirmacao por WhatsApp" → 1 meta
- "Integra cupom com calculo de frete" → 1 meta (a interacao que ninguem especificou)

**Sua missao:** Construir um `GoalAtomicitySplitter` que detecta metas multiplas em uma unica sentenca, divide-as em metas atomicas, e estabelece dependencias explicitas entre elas.

---

## O Cenario: Pipeline de Intent com Metas Sobrepostas

### Contexto

Voce recebeu o codigo de um `IntentSplitter` que recebe descricoes de trabalho e as divide em tarefas. O splitter atual e rudimentar -- divide por paragrafos, nao por conjuncoes. O resultado e que "adiciona cupom, calcula frete e envia email" vira UMA meta, quando deveriam ser tres.

Voce vai adicionar um `GoalAtomicitySplitter` que:

1. Recebe uma declaracao de meta candidata
2. Detecta conjuncoes ("e", "tambem", "alem disso", "bem como") e multi-clausulas
3. Divide a declaracao em metas atomicas -- uma por resultado distinto
4. Detecta dependencias entre as metas atomicas (ordem, dado compartilhado, interacao)
5. Gera um `SplitReport` com as metas atomicas, suas dependencias, e a ordem sugerida de execucao

### Dados de Entrada

O splitter recebe declaracoes como estas:

```json
{
  "intent_id": "INT-2026-112",
  "author": "pm_carla",
  "description": "Adiciona suporte a cupom de desconto no checkout e calcula o frete pelos Correios e envia uma confirmacao por email e WhatsApp apos a compra",
  "domain": "checkout"
}
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Deteccao de conjuncao:** O splitter detecta palavras de conjuncao: "e", "tambem", "alem disso", "bem como", ", e", "; e". Cada conjuncao que separa verbos de acao distintos e um ponto de divisao
2. **RF2 - Divisao atomica:** Cada meta atomica resultante contem exatamente UMA acao principal com UM resultado. "Envia confirmacao por email e WhatsApp" se divide em duas metas: "envia confirmacao por email" e "envia confirmacao por WhatsApp"
3. **RF3 - Preservacao de contexto:** Cada meta atomica herda o contexto da meta original (dominio, author, conexoes). Nenhuma informacao e perdida na divisao
4. **RF4 - Deteccao de dependencias:** O splitter identifica dependencias entre metas atomicas: SEQUENTIAL (B so pode comecar depois de A), DATA_DEPENDENCY (B consome dados produzidos por A), INTEGRATION (A e B precisam de um terceiro intent para integrar)
5. **RF5 - Ordem sugerida:** O splitter produz uma ordem de execucao sugerida baseada nas dependencias detectadas
6. **RF6 - Alerta de interacao:** Quando duas metas atomicas operam no mesmo componente ou compartilham dados, o splitter emite um alerta sugerindo um intent de integracao

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Split deterministico:** `split_goal(description) -> list[AtomicGoal]` e deterministico
3. **RT3 - Heuristica lexica:** A deteccao de conjuncoes opera no nivel lexico, nao requer LLM
4. **RT4 - Dependencias inferidas:** A deteccao de dependencias usa palavras-chave de compartilhamento ("calculo do frete COM desconto", "frete APOS cupom")

---

## Sua Tarefa

Voce vai implementar o GoalAtomicitySplitter em 3 partes.

---

### Parte 1: Diagnosticar Metas Sobrepostas (15 min)

Analise as 3 declaracoes abaixo. Para cada uma, identifique manualmente as conjuncoes e divida em metas atomicas.

```python
# Declaracoes multi-meta — quantas metas atomicas cada uma contem?
MULTI_GOAL_CANDIDATES = [
    # A: Quantas metas?
    "Corrige o bug de timeout na busca e adiciona cache de resultados frequentes e melhora a mensagem de erro quando o catalogo esta offline",

    # B: Quantas metas?
    "Migra o banco de dados do KODA para PostgreSQL 16 com particionamento por data e atualiza todas as queries para usar os novos indices particionados e implementa um health check que monitora a latencia das particoes",

    # C: Quantas metas? (cuidado — tem conjuncoes que nao sao divisoes)
    "Implementa a busca de produtos com filtro de preco e categoria e garante que o resultado retorna em menos de 200 milissegundos",
]

# TAREFA: Responda no seu codigo como comentario:
#
# Para cada candidato (A, B, C):
# 1. Liste as conjuncoes encontradas (palavras que indicam divisao)
# 2. Divida em metas atomicas (uma por linha)
# 3. Identifique dependencias entre as metas atomicas
# 4. Para o candidato C: explique por que "filtro de preco e categoria" NAO e uma
#    divisao de meta (e uma lista de filtros, nao duas metas distintas)
```

**Resposta esperada (em comentario):**

```python
# CANDIDATE A: 3 metas atomicas
# Conjuncoes: "e adiciona", "e melhora"
# Meta 1: "Corrige o bug de timeout na busca"
# Meta 2: "Adiciona cache de resultados frequentes na busca"
# Meta 3: "Melhora a mensagem de erro quando o catalogo esta offline"
# Dependencias: Meta 2 depende de Meta 1? NAO — sao independentes.
#   Mas Meta 2 e Meta 1 operam no mesmo componente (busca). Alerta: integration.
#
# CANDIDATE C: 1 meta (a conjuncao e de filtros, nao de metas)
# "filtro de preco e categoria" — aqui "e" conecta DOIS FILTROS da mesma
# funcionalidade, nao duas metas distintas. "preco e categoria" e uma lista
# de parametros de uma unica funcionalidade (busca com filtros).
# A segunda parte ("garante que o resultado retorna em menos de 200ms")
# e uma CONSTRAINT de performance, nao uma meta separada.
# Total: 1 meta atomica: "Implementa busca com filtro de preco e categoria"
#        + 1 constraint: "resultado < 200ms"
```

---

### Parte 2: Implementar o GoalAtomicitySplitter (30 min)

Implemente o splitter. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class DependencyType(Enum):
    NONE = "none"                   # metas independentes
    SEQUENTIAL = "sequential"       # B so pode comecar depois de A terminar
    DATA_DEPENDENCY = "data_dep"    # B consome dados que A produz
    INTEGRATION_REQUIRED = "integration"  # A e B precisam de um intent de integracao


@dataclass
class AtomicGoal:
    """
    Uma meta atomica: uma unica acao com um unico resultado.
    Uma sentenca. Sem "e". Sem "tambem".
    """
    goal_id: str  # derivado do intent original + indice
    description: str
    original_intent_id: str
    author: str
    domain: str
    position: int  # ordem na sentenca original (0, 1, 2...)
    conjunctions_found: list[str] = field(default_factory=list)


@dataclass
class GoalDependency:
    """Dependencia entre duas metas atomicas."""
    source_goal_id: str
    target_goal_id: str
    dep_type: DependencyType
    rationale: str = ""


@dataclass
class SplitResult:
    """Resultado de uma divisao atomica."""
    original_intent_id: str
    original_description: str
    atomic_goals: list[AtomicGoal] = field(default_factory=list)
    dependencies: list[GoalDependency] = field(default_factory=list)
    suggested_order: list[str] = field(default_factory=list)  # goal_ids em ordem
    integration_alerts: list[str] = field(default_factory=list)
    was_split: bool = False
    split_reason: str = ""


@dataclass
class SplitReport:
    """Relatorio completo de uma sessao de divisao."""
    report_id: str = ""
    results: list[SplitResult] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def total_atomic_goals(self) -> int:
        return sum(len(r.atomic_goals) for r in self.results)

    @property
    def total_dependencies(self) -> int:
        return sum(len(r.dependencies) for r in self.results)


# ============================================================
# CONJUNCTION DETECTION
# ============================================================

# Conjuncoes que indicam divisao de meta.
# IMPORTANTE: "e" sozinho e ambiguo — pode conectar metas ou pode
# conectar itens de uma lista. O contexto decide.
GOAL_CONJUNCTIONS: list[str] = [
    " e ",           # ambiguo — precisa de contexto
    ", e ",          # geralmente divide metas (virgula + e)
    " também ",      # "adiciona X e também Y" — divisao
    " além disso ",  # claramente divisao
    " bem como ",    # formal, divisao
    "; e ",          # ponto-e-virgula + e = divisao
    "; também ",     # ponto-e-virgula + tambem = divisao
]

# Verbos de acao — cada verbo distinto sugere uma meta distinta
# quando aparece apos uma conjuncao
ACTION_VERBS: list[str] = [
    "adiciona", "implementa", "cria", "remove", "corrige",
    "melhora", "migra", "atualiza", "configura", "integra",
    "envia", "calcula", "garante", "permite", "bloqueia",
    "verifica", "valida", "converte", "substitui", "redesenha",
]


# ============================================================
# GOAL ATOMICITY SPLITTER — nucleo do exercicio
# ============================================================

def find_goal_conjunctions(description: str) -> list[tuple[int, str]]:
    """
    Encontra conjuncoes que indicam divisao de meta.
    Retorna posicoes e o texto da conjuncao encontrada.

    Args:
        description: A descricao da meta candidata.

    Returns:
        Lista de tuplas (posicao na string, texto da conjuncao).
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Converter description para lowercase para busca case-insensitive
    # 2. Para cada conjuncao em GOAL_CONJUNCTIONS:
    #    a. Buscar todas as ocorrencias na string
    #    b. Para cada ocorrencia, verificar se ha um ACTION_VERB
    #       depois da conjuncao (a ~5 palavras de distancia)
    #    c. Se ha verbo de acao depois: registrar como ponto de divisao
    #    d. Se nao ha verbo: provavelmente e uma lista de itens,
    #       nao uma divisao de meta (ex: "preco e categoria")
    # 3. Retornar lista ordenada por posicao
    pass


def split_by_conjunctions(description: str) -> list[str]:
    """
    Divide a descricao em sentencas atomicas nos pontos de conjuncao.

    Args:
        description: A descricao da meta candidata.

    Returns:
        Lista de sentencas atomicas (uma por meta).
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Executar find_goal_conjunctions(description)
    # 2. Se nao encontrou conjuncoes de meta: retornar [description]
    # 3. Dividir a string nos pontos de conjuncao
    # 4. Para cada fragmento:
    #    a. Remover a conjuncao do inicio
    #    b. Capitalizar primeira letra
    #    c. Garantir que o fragmento tem um verbo de acao
    #    d. Se o fragmento nao tem verbo: junta-lo ao fragmento anterior
    #       (era uma lista de itens, nao uma meta separada)
    # 5. Retornar lista de sentencas atomicas
    pass


def detect_dependencies(goals: list[AtomicGoal]) -> list[GoalDependency]:
    """
    Detecta dependencias entre metas atomicas.

    Heuristicas:
    - SEQUENTIAL: se ambas operam no mesmo componente e a segunda
      menciona "apos", "depois", "entao", "em seguida"
    - DATA_DEPENDENCY: se Goal B menciona um dado que Goal A produz
      (ex: Goal A "calcula frete", Goal B "aplica desconto no frete")
    - INTEGRATION_REQUIRED: se ambas operam no mesmo componente
      com acoes diferentes (ex: "adiciona cupom ao checkout" e
      "calcula frete no checkout" — ambas mexem no checkout)

    Args:
        goals: Lista de metas atomicas.

    Returns:
        Lista de GoalDependency detectadas.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Para cada par de metas (g1, g2) com g1.position < g2.position:
    #    a. Extrair componentes mencionados em cada meta
    #       (palavras como "busca", "checkout", "catalogo", "banco")
    #    b. Se compartilham componente:
    #       - Procurar palavras de sequencia ("apos", "depois") → SEQUENTIAL
    #       - Procurar dados compartilhados ("frete", "cupom", "desconto") → DATA_DEPENDENCY
    #       - Senao → INTEGRATION_REQUIRED
    #    c. Se nao compartilham componente: NONE (nao registrar)
    # 2. Retornar apenas dependencias != NONE
    pass


def compute_suggested_order(goals: list[AtomicGoal], dependencies: list[GoalDependency]) -> list[str]:
    """
    Calcula a ordem sugerida de execucao baseada nas dependencias.

    Algoritmo de ordenacao topologica simplificado:
    - Metas sem dependencias de entrada podem executar em paralelo
    - Metas com dependencia SEQUENTIAL ou DATA_DEPENDENCY devem
      executar apos suas dependencias

    Args:
        goals: Lista de metas atomicas.
        dependencies: Dependencias detectadas.

    Returns:
        Lista de goal_ids em ordem sugerida de execucao.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Construir grafo de dependencias: {goal_id: [deps]}
    # 2. Ordenacao topologica:
    #    a. Comecar com metas que nao tem dependencias
    #    b. Conforme metas sao "executadas", liberar suas dependentes
    #    c. Metas sem dependencia entre si podem ser agrupadas
    #       como paralelizaveis (representado por ordem relativa)
    # 3. Retornar lista ordenada de goal_ids
    pass


def check_integration_alerts(goals: list[AtomicGoal]) -> list[str]:
    """
    Emite alertas quando metas atomicas operam no mesmo componente
    sem dependencia explicita -- sugerindo que um intent de integracao
    pode ser necessario.

    Args:
        goals: Lista de metas atomicas.

    Returns:
        Lista de strings de alerta.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Agrupar metas por componente mencionado (busca, checkout, etc.)
    # 2. Para cada grupo com 2+ metas:
    #    a. Emitir alerta: "Metas X e Y operam em [componente].
    #       Considere um intent de integracao para garantir consistencia."
    # 3. Retornar lista de alertas
    pass


def split_goal(
    intent_id: str,
    author: str,
    description: str,
    domain: str = "",
) -> SplitResult:
    """
    Analisa uma descricao de meta e a divide em metas atomicas se
    conjuncoes de meta forem detectadas.

    Args:
        intent_id: ID do intent original.
        author: Autor do intent.
        description: A descricao da meta candidata.
        domain: Dominio do trabalho.

    Returns:
        SplitResult com metas atomicas, dependencias, e alertas.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. atomic_sentences = split_by_conjunctions(description)
    # 2. Se len(atomic_sentences) == 1:
    #    a. was_split = False
    #    b. atomic_goals = [AtomicGoal com a sentenca unica]
    # 3. Se len(atomic_sentences) > 1:
    #    a. was_split = True
    #    b. Criar AtomicGoal para cada sentenca
    #    c. dependencies = detect_dependencies(atomic_goals)
    #    d. suggested_order = compute_suggested_order(atomic_goals, dependencies)
    #    e. integration_alerts = check_integration_alerts(atomic_goals)
    # 4. Retornar SplitResult
    pass


# ============================================================
# TESTES RAPIDOS: Splitter
# ============================================================

if __name__ == "__main__":
    # Teste 1: Meta atomica nao deve ser dividida
    result = split_goal("INT-001", "pm_test", "Adiciona suporte a cupom de desconto no checkout")
    assert not result.was_split, "Meta atomica nao deve ser dividida"
    assert len(result.atomic_goals) == 1, f"Esperado 1 goal, obtido {len(result.atomic_goals)}"
    print("Teste 1 passou: meta atomica preservada")

    # Teste 2: Multi-meta com 3 conjuncoes deve gerar 4 metas
    result = split_goal(
        "INT-002", "pm_carla",
        "Adiciona cupom de desconto e calcula frete e envia email e envia WhatsApp",
        domain="checkout",
    )
    assert result.was_split, "Multi-meta deve ser dividida"
    assert len(result.atomic_goals) == 4, f"Esperado 4 goals, obtido {len(result.atomic_goals)}"
    print(f"\nTeste 2 passou: {len(result.atomic_goals)} metas atomicas geradas")
    for g in result.atomic_goals:
        print(f"  [{g.position}] {g.description}")

    # Teste 3: "e" entre itens de lista nao deve dividir
    result = split_goal(
        "INT-003", "pm_test",
        "Implementa busca com filtro de preco e categoria e garante latencia < 200ms",
        domain="search",
    )
    # "preco e categoria" e lista. "garante latencia" e constraint, nao meta.
    assert len(result.atomic_goals) == 1, (
        f"'preco e categoria' e lista de filtros, nao metas. "
        f"Esperado 1 goal, obtido {len(result.atomic_goals)}"
    )
    print(f"\nTeste 3 passou: lista de itens nao foi incorretamente dividida")

    # Teste 4: Dependencias devem ser detectadas
    result = split_goal(
        "INT-004", "pm_carla",
        "Calcula o frete pelos Correios e aplica o desconto do cupom no valor do frete",
        domain="checkout",
    )
    assert result.was_split, "Deve detectar a conjuncao 'e aplica'"
    assert len(result.dependencies) >= 1, (
        f"Deve detectar dependencia entre as metas, obtido {len(result.dependencies)}"
    )
    print(f"\nTeste 4 passou: {len(result.dependencies)} dependencia(s) detectada(s)")
    for d in result.dependencies:
        print(f"  {d.source_goal_id} --[{d.dep_type.value}]--> {d.target_goal_id}")

    # Teste 5: Alertas de integracao
    result = split_goal(
        "INT-005", "pm_test",
        "Adiciona cupom ao checkout e melhora a UI do checkout e adiciona step de review no checkout",
        domain="checkout",
    )
    assert len(result.integration_alerts) >= 1, (
        f"Deve emitir alerta de integracao, obtido {len(result.integration_alerts)}"
    )
    print(f"\nTeste 5 passou: {len(result.integration_alerts)} alerta(s) de integracao")
    for alert in result.integration_alerts:
        print(f"  ALERTA: {alert}")

    # Teste 6: SplitReport agrega corretamente
    report = SplitReport(report_id="RPT-002")
    for intent_id, desc in [
        ("INT-010", "Corrige timeout e adiciona cache e melhora mensagem de erro"),
        ("INT-011", "Migra banco de dados e atualiza queries"),
    ]:
        report.results.append(split_goal(intent_id, "pm_test", desc))
    assert report.total_atomic_goals == 5, (
        f"Esperado 5 metas atomicas totais, obtido {report.total_atomic_goals}"
    )
    print(f"\nTeste 6 passou: relatorio com {report.total_atomic_goals} metas atomicas, "
          f"{report.total_dependencies} dependencias")

    print("\nTodos os testes do GoalAtomicitySplitter passaram!")
```

---

### Parte 3: Pipeline de Intent com Divisao Atomica (20 min)

Agora implemente o pipeline que integra o `GoalAtomicitySplitter` ao fluxo de criacao de intents:

```python
# ============================================================
# INTENT FACTORY COM GOAL ATOMICITY SPLITTER
# ============================================================

@dataclass
class IntentManifest:
    """Manifesto de intents gerados apos divisao atomica."""
    original_intent_id: str
    original_description: str
    atomic_intents: list[dict] = field(default_factory=list)
    dependency_graph: dict[str, list[str]] = field(default_factory=dict)
    parallel_groups: list[list[str]] = field(default_factory=list)


def create_atomic_intents(
    intent_id: str,
    author: str,
    description: str,
    domain: str = "",
) -> IntentManifest:
    """
    Cria intents atomicos a partir de uma descricao potencialmente multi-meta.

    Fluxo:
    1. split_goal() para dividir em metas atomicas
    2. Para cada meta atomica: criar um novo intent_id derivado
       (ex: INT-112-1, INT-112-2, INT-112-3)
    3. Construir dependency_graph
    4. Agrupar metas independentes em parallel_groups
    5. Retornar IntentManifest

    Args:
        intent_id: ID do intent original.
        author: Autor.
        description: Descricao potencialmente multi-meta.
        domain: Dominio do trabalho.

    Returns:
        IntentManifest com intents atomicos e grafo de dependencias.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. result = split_goal(intent_id, author, description, domain)
    # 2. Para cada AtomicGoal em result.atomic_goals:
    #    a. Criar derived_intent_id = f"{intent_id}-{goal.position + 1}"
    #    b. Criar dict com intent_id, description, author, domain, position
    #    c. Adicionar a atomic_intents
    # 3. Construir dependency_graph a partir de result.dependencies
    # 4. Agrupar metas sem dependencias entre si em parallel_groups
    # 5. Retornar IntentManifest
    pass


# ============================================================
# TESTE COMPLETO DO PIPELINE
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTE DO PIPELINE DE INTENTS ATOMICOS")
    print("=" * 60)

    # Cenario: o intent original do checkout que deu errado
    manifest = create_atomic_intents(
        intent_id="INT-2026-112",
        author="pm_carla",
        description="Adiciona suporte a cupom de desconto no checkout e "
                    "calcula o frete pelos Correios e envia confirmacao "
                    "por email e WhatsApp apos a compra",
        domain="checkout",
    )

    print(f"\nIntent original: INT-2026-112")
    print(f"Descricao original: {manifest.original_description[:80]}...")
    print(f"\nIntents atomicos gerados: {len(manifest.atomic_intents)}")
    for intent in manifest.atomic_intents:
        print(f"  {intent['intent_id']}: {intent['description']}")

    print(f"\nGrafo de dependencias:")
    for src, targets in manifest.dependency_graph.items():
        print(f"  {src} → {targets}")

    print(f"\nGrupos paralelizaveis:")
    for i, group in enumerate(manifest.parallel_groups):
        print(f"  Grupo {i+1}: {group}")

    # Verificacoes
    assert len(manifest.atomic_intents) >= 3, (
        f"Deve gerar ao menos 3 intents atomicos, gerou {len(manifest.atomic_intents)}"
    )
    # "envia confirmacao por email e WhatsApp" deve gerar 2 intents
    email_whatsapp = [i for i in manifest.atomic_intents if "whatsapp" in i["description"].lower()]
    assert len(email_whatsapp) >= 1, "Deve ter um intent separado para WhatsApp"

    print("\n" + "=" * 60)
    print("PIPELINE DE INTENTS ATOMICOS COMPLETO")
    print("=" * 60)
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce identificou corretamente as conjuncoes nos 3 candidatos (A, B, C)
- [ ] Voce dividiu corretamente cada candidato em metas atomicas
- [ ] Voce explicou por que "filtro de preco e categoria" (Candidato C) nao e divisao de meta

### Criterio 2: Splitter funcional

- [ ] `find_goal_conjunctions()` detecta ", e ", " e tambem ", " alem disso " corretamente
- [ ] `find_goal_conjunctions()` NAO divide quando "e" conecta itens de lista ("preco e categoria")
- [ ] `split_by_conjunctions()` gera sentencas atomicas com verbos de acao
- [ ] `detect_dependencies()` encontra SEQUENTIAL, DATA_DEPENDENCY, e INTEGRATION_REQUIRED

### Criterio 3: Casos de borda

- [ ] Meta ja atomica nao e dividida (`was_split=False`)
- [ ] Descricao multi-meta com 4 metas gera 4 AtomicGoals
- [ ] Dependencia entre metas que compartilham dados e detectada

### Criterio 4: Pipeline

- [ ] `create_atomic_intents()` gera intents com IDs derivados (INT-X-1, INT-X-2, ...)
- [ ] Grupos paralelizaveis sao identificados corretamente
- [ ] Alertas de integracao sao emitidos quando 3+ metas operam no mesmo componente

### Criterio 5: Testes

- [ ] Teste 1: meta atomica nao dividida
- [ ] Teste 2: 4 metas geradas de 3 conjuncoes
- [ ] Teste 3: lista de itens nao dividida incorretamente
- [ ] Teste 4: dependencias detectadas
- [ ] Teste 5: alertas de integracao emitidos
- [ ] Teste 6: relatorio agrega 5 metas atomicas

---

## Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou conjuncoes | Identificou parcialmente | Identificou todas + dividiu corretamente | Diagnostico completo + distincao lista vs meta |
| **Splitter (Parte 2)** | 40% | Nao implementado | Divide por "e" mas sem contexto | Divide com contexto (lista vs meta) + dependencias | Splitter completo com dependencias, ordem, e alertas de integracao |
| **Pipeline (Parte 3)** | 30% | Nao implementado | Pipeline gera intents mas sem dependencias | Pipeline com dependencias e grupos paralelos | Pipeline completo com IDs derivados, grafo, e grupos paralelizaveis |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 5 criterios passam | Todos os 6 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para a Deteccao de Conjuncoes

1. **"e" e a conjuncao mais traicoeira.** "Adiciona cupom e calcula frete" → duas metas. "Filtro de preco e categoria" → uma meta. A diferenca: depois do "e", ha um VERBO DE ACAO ("calcula") ou um SUBSTANTIVO ("categoria")? Se ha verbo, e outra meta. Se ha substantivo, e continuacao da lista.

2. **Procure o verbo depois da conjuncao.** Regra pratica: escaneie as proximas 5 palavras apos a conjuncao. Se encontrar um verbo de acao (adiciona, implementa, cria, corrige, etc.), e uma divisao. Se encontrar um substantivo (categoria, preco, tamanho, cor), e uma lista.

3. **Virgula antes do "e" e um sinal forte.** "adiciona cupom, calcula frete, e envia email" — a virgula antes do "e" (Oxford comma) quase sempre indica itens de uma enumeracao de metas.

### Para Dependencias

1. **Dados compartilhados criam dependencias.** Se a Meta 1 "calcula frete" e a Meta 2 "aplica desconto no frete", a Meta 2 precisa do resultado da Meta 1. Isso e DATA_DEPENDENCY.

2. **Mesmo componente sem coordenacao = risco.** Se 3 metas diferentes mexem no "checkout", mesmo sem dependencia de dados, elas vao colidir. Emita INTEGRATION_REQUIRED.

3. **Nem toda dependencia e sequencial.** "Envia email" e "envia WhatsApp" sao independentes — podem rodar em paralelo. Nao crie dependencias artificiais.

### Para o Pipeline

1. **IDs derivados criam rastreabilidade.** `INT-112-1`, `INT-112-2`, `INT-112-3` — o prefixo comum vincula as metas atomicas ao intent original. Isso permite rastrear a cadeia de decomposicao.

2. **Grupos paralelos economizam tempo.** Se 3 de 5 metas atomicas sao independentes, elas podem executar simultaneamente em agentes diferentes. O `parallel_groups` sinaliza isso para o orquestrador.

---

## Duvidas Comuns

**P: Isso nao vai gerar intents minusculos? "Adiciona cupom" e uma meta muito pequena.**
R: "Adiciona cupom" e uma meta atomica, mas nao e um intent completo. O intent completo inclui a meta + constraints + failure scenarios + success scenarios + connections. A meta e so o campo `description`. Quatro metas atomicas geram quatro intents completos, cada um com suas proprias constraints e cenarios. Sim, e mais trabalho de especificacao — mas evita o retrabalho de integrar 4 funcionalidades que foram implementadas sem coordenacao.

**P: E se as metas realmente precisam ser implementadas juntas?**
R: O splitter nao IMPEDE que metas sejam implementadas juntas. Ele as separa para que sejam ESPECIFICADAS separadamente. O orquestrador pode decidir executa-las sequencialmente ou em paralelo. A separacao e de especificacao, nao de execucao.

**P: Como isso se relaciona com Vertical Slice Issue Generation?**
R: Vertical slices cortam o sistema em camadas (UI → logica → dados) para uma unica funcionalidade. Goal Atomicity Split corta o intent em funcionalidades atomicas. Sao eixos de decomposicao diferentes e complementares: primeiro divida por meta (Goal Atomicity Split), depois para cada meta, gere uma vertical slice (Vertical Slice Issue Generation).

**P: "e" entre adverbios conta? "rapida e eficientemente"**
R: Nao. "rapida e eficientemente" modifica o mesmo verbo — e uma lista de qualidades, nao de metas. A regra e: a conjuncao separa VERBOS de acao distintos ou SUBSTANTIVOS que sao objetos de verbos diferentes.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns.md` para entender o contexto completo do padrao
2. Compare com `docs/canonical/vertical-slice-issue-generation.md` — observe como a decomposicao por meta atomica e a decomposicao por camada se complementam
3. (Opcional) Integre o GoalAtomicitySplitter ao Intent Five-Part Primitive: apos dividir metas atomicas, cada uma recebe seu proprio conjunto de constraints, failure scenarios, success scenarios, e connections

---

*Exercicio Goal Atomicity Split | Nivel 2 - Padroes Praticos*

**Uma meta, uma sentenca. Sem "e".**
