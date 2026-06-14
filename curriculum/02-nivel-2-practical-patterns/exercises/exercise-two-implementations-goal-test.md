---
title: "Exercicio: Distinguir Metas de Especificacoes com o Teste das Duas Implementacoes"
type: curriculum-exercise
nivel: 2
aliases: ["two implementations goal test", "goal vs spec test", "teste duas implementacoes", "meta vs especificacao", "heuristic goal specification", "intent goal purity"]
tags: [curriculo-conteudo, nivel-2, exercicio, agentes-orquestracao, spec-driven-development, decision-discipline, intent-structure, harness-engineering, python, dataclass]
relates-to: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]"]
last_updated: 2026-06-14
---
# Exercicio: Distinguir Metas de Especificacoes com o Teste das Duas Implementacoes
## Nivel 2 - Padroes Praticos

**Tempo Estimado:** 45-60 minutos
**Dificuldade:** (Intermediario)
**Pre-requisito:** Ter lido `02-sprint-contracts.md` (Nivel 2) + completado Exercicio 5 (Intent Five-Part Primitive)
**Objetivo:** Diagnosticar intents que misturam metas com especificacoes e implementar um classificador que distingue o que o agente deve alcancar do que o agente deve escolher

---

## Prologo: O Agente Que Virou Datilografo

### Quarta-feira, 15h00. Uma feature que o PM jurou que era simples.

```
PM: "Precisamos que o KODA mostre produtos ordenados por relevancia
     usando TF-IDF com similaridade de cosseno no Pinecone."

DEV_AGENT: [Analisando... 2 segundos]
           "Entendido. Implementar busca com TF-IDF e Pinecone."
```

**O que o agente fez nas 8 horas seguintes:**

O agente implementou exatamente o que foi pedido. Ele:

1. Configurou um cluster Pinecone dedicado (custo: R$ 1.200/mes)
2. Implementou tokenizacao TF-IDF do zero (840 linhas de Python)
3. Escreveu uma funcao de similaridade de cosseno otimizada em NumPy
4. Criou um pipeline de indexacao batch com 4 etapas
5. Migrou 47.000 produtos do catalogo para o Pinecone
6. Escreveu 32 testes de integracao

O codigo estava limpo. Os testes passavam. A documentacao era impecavel. **E o PM odiou.**

```
PM: "Isso nao era o que eu queria!"
DEV: "Mas voce pediu TF-IDF com Pinecone. Esta aqui, funcionando."

PM: "Eu nao quero TF-IDF! Eu quero que o cliente encontre o produto
     certo em menos de 3 segundos! O time de search que sugeriu
     TF-IDF -- eu so repeti o que eles falaram."
```

**O que o PM realmente queria:**

Que a busca retornasse produtos relevantes em menos de 3 segundos. O PM nao queria TF-IDF, nao queria Pinecone, nao queria similaridade de cosseno. Ele queria um resultado -- e enunciou o meio como se fosse o fim.

```
╔══════════════════════════════════════════════════════════════════╗
║           CUSTO DE CONFUNDIR META COM ESPECIFICACAO              ║
║                                                                  ║
║  O que foi pedido:  "TF-IDF com similaridade de cosseno no      ║
║                      Pinecone"                                   ║
║  O que foi feito:   Cluster Pinecone + TF-IDF customizado +      ║
║                     batch indexing (8h, R$ 1.200/mes)            ║
║  O que era preciso: busca retornar produtos relevantes em        ║
║                     menos de 3 segundos                          ║
║                                                                  ║
║  Token waste:        6.400.000                                   ║
║  Horas descartadas:  8                                           ║
║  Custo Pinecone:     R$ 1.200/mes (contrato de 12 meses)        ║
║  Solucao real:       indice GIN no PostgreSQL (20 min, R$ 0)    ║
║                                                                  ║
║  Se o intent tivesse sido "busca retorna produtos relevantes     ║
║  em < 3s" em vez de "implemente TF-IDF no Pinecone":            ║
║  - Agente teria liberdade para escolher a melhor solucao         ║
║  - PostgreSQL GIN index resolveria em 20 minutos                 ║
║  - Zero custo adicional de infraestrutura                        ║
╚══════════════════════════════════════════════════════════════════╝
```

**O que aconteceu:**

O PM confundiu uma **meta** (encontrar o produto certo em < 3s) com uma **especificacao disfarcada de meta** (usar TF-IDF no Pinecone). O agente, obediente, implementou a especificacao com excelencia -- e o resultado foi uma solucao 40x mais cara e 20x mais complexa que o necessario.

**O teste que teria evitado tudo:**

> "Duas implementacoes substancialmente diferentes conseguiriam satisfazer isso?"

- "Usar TF-IDF com similaridade de cosseno no Pinecone" → **NAO.** So existe UMA implementacao que satisfaz isso: a que usa TF-IDF no Pinecone. Isso e uma especificacao.
- "Busca retorna produtos relevantes em menos de 3 segundos" → **SIM.** PostgreSQL GIN index, Elasticsearch, Pinecone com embeddings, Redis Search -- todas satisfazem. Isso e uma meta.

**Sua missao:** Construir um `GoalSpecClassifier` que aplica o Teste das Duas Implementacoes para separar metas de especificacoes e impedir que o agente vire um datilografo de luxo.

---

## O Cenario: Pipeline de Intent com Metas Contaminadas

### Contexto

Voce recebeu o codigo de um `IntentReceiver` que recebe descricoes de trabalho em linguagem natural e as encaminha diretamente para agentes. O receiver atual **nao distingue metas de especificacoes** -- tudo que chega e tratado como meta. O resultado e previsivel: agentes implementam exatamente o que foi pedido, nao o que era preciso.

Voce vai adicionar um `GoalSpecClassifier` que:

1. Recebe uma declaracao candidata a meta
2. Aplica o Teste das Duas Implementacoes: "Duas implementacoes substancialmente diferentes conseguiriam satisfazer isso?"
3. Classifica como `GOAL` (meta genuina) ou `SPEC_IN_DISGUISE` (especificacao mascarada)
4. Para `SPEC_IN_DISGUISE`: extrai a verdadeira meta subjacente e sugere reescrita
5. Gera um `ClassificationReport` que o outcome owner usa para revisar o intent antes do dispatch

### Dados de Entrada

O classificador recebe declaracoes como estas:

```json
[
  {
    "id": "INT-2026-089",
    "statement": "Adicionar um cache Redis de 3 camadas com warming preditivo na busca de produtos",
    "author": "pm_joao",
    "domain": "product_search"
  },
  {
    "id": "INT-2026-090",
    "statement": "Reduzir o tempo de resposta da busca de produtos para menos de 200ms no p95",
    "author": "pm_maria",
    "domain": "product_search"
  },
  {
    "id": "INT-2026-091",
    "statement": "Migrar o sistema de notificacao de polling para WebSockets com Socket.io",
    "author": "dev_carlos",
    "domain": "notifications"
  }
]
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Classificacao binaria:** O `GoalSpecClassifier` classifica cada declaracao como `GOAL` ou `SPEC_IN_DISGUISE`
2. **RF2 - Teste das Duas Implementacoes:** A classificacao usa a pergunta-heuristica: "Duas implementacoes substancialmente diferentes conseguiriam satisfazer esta declaracao?" Se sim → `GOAL`. Se nao → `SPEC_IN_DISGUISE`
3. **RF3 - Extracao da meta subjacente:** Para cada `SPEC_IN_DISGUISE`, o classificador propoe uma reescrita que remove ferramentas, tecnologias, e metodos -- deixando apenas o resultado desejado
4. **RF4 - Deteccao de palavras-sinal:** O classificador detecta palavras que indicam especificacao: nomes de ferramentas (Redis, Pinecone, PostgreSQL, Socket.io), padroes de implementacao (cache, polling, batch, cron), e verbos de implementacao (migrar, configurar, instalar)
5. **RF5 - Alternativas geradas:** Para cada `GOAL`, o classificador sugere de 2 a 4 implementacoes diferentes que satisfariam a meta -- provando que ela e genuinamente uma meta
6. **RF6 - ClassificationReport:** Toda analise gera um `ClassificationReport` com a sentenca original, o veredito, a justificativa, a reescrita sugerida (se aplicavel), e alternativas (se aplicavel)

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Classificador deterministico:** `classify_statement(statement) -> ClassificationResult` e deterministico -- mesma entrada sempre produz mesma saida
3. **RT3 - Heuristica lexica:** A deteccao de palavras-sinal opera no nivel lexico (substrings), nao requer LLM -- e rapida e explicavel
4. **RT4 - Reescrita generativa limitada:** A reescrita de `SPEC_IN_DISGUISE` para `GOAL` segue templates pre-definidos baseados no tipo de contaminacao detectada

---

## Sua Tarefa

Voce vai implementar o GoalSpecClassifier em 3 partes.

---

### Parte 1: Diagnosticar Metas Contaminadas (15 min)

Analise as 5 declaracoes abaixo. Para cada uma, aplique manualmente o Teste das Duas Implementacoes e classifique como `GOAL` ou `SPEC_IN_DISGUISE`.

```python
# Declaracoes candidatas -- quais sao metas genuinas?
CANDIDATES = [
    # A
    "Implementar autocomplete com prefix tree e cache Redis de 3 camadas na busca do KODA",
    # B
    "Permitir que o cliente encontre um produto em menos de 3 segundos apos digitar a terceira letra",
    # C
    "Migrar o banco de dados do KODA de PostgreSQL para MongoDB com sharding automatico",
    # D
    "Garantir que o catalogo de produtos suporte 10x o volume atual sem degradacao de latencia",
    # E
    "Adicionar um worker Celery com Redis broker para processar notificacoes de pedidos em background",
]

# TAREFA: Responda no seu codigo como comentario:
#
# Para cada candidato (A, B, C, D, E):
# 1. Duas implementacoes substancialmente diferentes conseguiriam satisfazer isso?
#    Liste 2-3 implementacoes possiveis (ou explique por que so existe uma).
# 2. Classifique como GOAL ou SPEC_IN_DISGUISE.
# 3. Se for SPEC_IN_DISGUISE, reescreva como GOAL extraindo apenas o resultado desejado.
# 4. Identifique as palavras-sinal que denunciaram a especificacao.
```

**Resposta esperada (em comentario):**

```python
# CANDIDATE A: "Implementar autocomplete com prefix tree e cache Redis..."
# 1. Duas implementacoes diferentes? NAO.
#    - A unica implementacao que "implementa prefix tree com Redis" e... prefix tree com Redis.
#    - Se voce usar Elasticsearch Suggest, ja nao satisfaz "prefix tree".
# 2. Classificacao: SPEC_IN_DISGUISE
# 3. Meta subjacente: "Permitir que o cliente veja sugestoes de busca enquanto digita,
#    com latencia de resposta < 100ms entre cada tecla"
# 4. Palavras-sinal: "prefix tree" (estrutura de dados especifica), "Redis" (ferramenta),
#    "cache de 3 camadas" (arquitetura especifica), "implementar" (verbo de implementacao)
```

---

### Parte 2: Implementar o GoalSpecClassifier (30 min)

Implemente o classificador. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class ClassificationVerdict(Enum):
    GOAL = "goal"
    SPEC_IN_DISGUISE = "spec_in_disguise"


@dataclass
class CandidateStatement:
    """Uma declaracao candidata a ser classificada como meta ou especificacao."""
    statement_id: str
    author: str
    statement: str
    domain: str = ""


@dataclass
class ClassificationResult:
    """Resultado da classificacao de uma declaracao."""
    statement_id: str
    original: str
    verdict: ClassificationVerdict
    rationale: str
    signal_words_found: list[str] = field(default_factory=list)
    rewritten_goal: str = ""             # preenchido se SPEC_IN_DISGUISE
    alternative_implementations: list[str] = field(default_factory=list)  # preenchido se GOAL


@dataclass
class ClassificationReport:
    """Relatorio completo de uma sessao de classificacao."""
    report_id: str = ""
    candidates: list[CandidateStatement] = field(default_factory=list)
    results: list[ClassificationResult] = field(default_factory=list)
    classified_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def goal_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == ClassificationVerdict.GOAL)

    @property
    def spec_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == ClassificationVerdict.SPEC_IN_DISGUISE)


# ============================================================
# SIGNAL WORDS — palavras que indicam especificacao
# ============================================================

# Ferramentas e tecnologias especificas (substantivos proprios ou nomes de produto)
TOOL_SIGNALS: list[str] = [
    "redis", "pinecone", "postgresql", "postgres", "mongodb", "elasticsearch",
    "socket.io", "websocket", "celery", "kafka", "rabbitmq", "docker",
    "kubernetes", "nginx", "haproxy", "aws", "gcp", "azure",
    "s3", "lambda", "dynamodb", "cloudfront", "cloudflare",
]

# Padroes de implementacao e arquitetura
PATTERN_SIGNALS: list[str] = [
    "cache", "caching", "cache de", "prefix tree", "trie",
    "similaridade de cosseno", "tf-idf", "batch", "polling",
    "cron", "worker", "sharding", "particionamento",
    "3 camadas", "two-phase", "event sourcing", "cqrs",
    "bloom filter", "consistent hashing",
]

# Verbos que descrevem COMO fazer, nao O QUE alcancar
IMPLEMENTATION_VERBS: list[str] = [
    "migrar", "configurar", "instalar", "refatorar",
    "reescrever", "substituir", "atualizar biblioteca",
    "trocar", "mudar de", "adicionar dependencia",
]


# ============================================================
# GOALSPEC CLASSIFIER — nucleo do exercicio
# ============================================================

def find_signal_words(statement: str) -> list[str]:
    """
    Encontra palavras-sinal na declaracao que indicam especificacao.

    Args:
        statement: A declaracao a ser analisada.

    Returns:
        Lista de palavras-sinal encontradas (em lowercase).
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Converter statement para lowercase
    # 2. Para cada palavra em TOOL_SIGNALS + PATTERN_SIGNALS + IMPLEMENTATION_VERBS:
    #    a. Verificar se aparece como substring na declaracao
    #    b. Se sim, adicionar a lista de encontradas
    # 3. Remover duplicatas
    # 4. Retornar lista ordenada
    pass


def two_implementations_test(statement: str) -> tuple[bool, str]:
    """
    Aplica o Teste das Duas Implementacoes.

    Pergunta central: "Duas implementacoes substancialmente diferentes
    conseguiriam satisfazer esta declaracao?"

    Heuristica pratica:
    - Se a declaracao contem ferramentas, tecnologias, ou padroes de
      implementacao especificos, elas RESTRINGEM o espaco de solucoes
      a uma unica implementacao. Isso indica SPEC_IN_DISGUISE.
    - Se a declaracao descreve um RESULTADO (latencia, comportamento
      do usuario, metrica de negocio) sem mencionar COMO, multiplas
      implementacoes sao possiveis. Isso indica GOAL.

    Args:
        statement: A declaracao a ser analisada.

    Returns:
        Tupla (is_goal, rationale).
        - is_goal: True se for uma meta genuina.
        - rationale: Justificativa em uma frase.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Executar find_signal_words(statement)
    # 2. Se encontrou palavras-sinal de ferramenta OU padrao:
    #    a. Contar quantas ferramentas/padroes sao mencionados
    #    b. Se >= 2: fortemente sugere SPEC_IN_DISGUISE
    #       (ex: "Redis" + "cache de 3 camadas" + "prefix tree")
    #    c. Se 1: possivelmente contaminado, verificar contexto
    #       (ex: "usando Redis" vs "com tolerancia a falhas como Redis")
    # 3. Se encontrou verbos de implementacao:
    #    a. "migrar", "configurar", "instalar" — fortemente sugere SPEC
    # 4. Verificar se a declaracao contem metricas de resultado:
    #    a. Palavras como "menos de", "maximo", "ate", "p95", "garantir que"
    #    b. Essas sugerem GOAL (descrevem resultado, nao metodo)
    # 5. Se a declaracao menciona o que o USUARIO experimenta (nao o que o
    #    sistema faz): sugere GOAL
    # 6. Montar rationale explicando a decisao
    pass


def extract_underlying_goal(statement: str) -> str:
    """
    Para uma declaracao classificada como SPEC_IN_DISGUISE, extrai
    a meta subjacente removendo ferramentas, tecnologias, e metodos.

    Args:
        statement: A declaracao contaminada.

    Returns:
        Uma reescrita que expressa apenas o resultado desejado.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido (reescrita por template):
    # 1. Detectar o tipo de contaminacao:
    #    a. "Ferramenta mention": "usar X para Y" → "Y"
    #    b. "Padrao mention": "implementar X com padrao Y" → resultado de X
    #    c. "Verbo implementacao": "migrar X de A para B" → "X com as mesmas capacidades"
    # 2. Aplicar template de reescrita correspondente:
    #    a. Se contem nome de ferramenta: extrair a CLAUSULA DE RESULTADO
    #       Ex: "Adicionar cache Redis para busca ficar rapida" →
    #           "Busca retorna resultados em < 200ms"
    #    b. Se e puramente ferramenta sem resultado:
    #       Ex: "Migrar para MongoDB" →
    #           "Banco de dados com [pergunta: o que MongoDB oferece que o atual nao oferece?]"
    # 3. Substituir verbos de implementacao por verbos de resultado:
    #    "migrar" → "garantir que"
    #    "configurar" → "permitir que"
    #    "implementar X" → "X funciona"
    pass


def suggest_alternatives(statement: str) -> list[str]:
    """
    Para uma declaracao classificada como GOAL, sugere de 2 a 4
    implementacoes diferentes que satisfariam a meta.

    Args:
        statement: A meta genuina.

    Returns:
        Lista de implementacoes alternativas (uma por linha).
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Identificar o dominio da meta (busca, notificacao, banco, etc.)
    # 2. Para cada dominio, manter um catalogo de alternativas conhecidas:
    #    a. Busca/ search: PostgreSQL GIN, Elasticsearch, Pinecone, Redis Search, Meilisearch
    #    b. Notificacao: Polling simples, WebSockets, Server-Sent Events, Push API
    #    c. Cache: Redis, Memcached, in-memory LRU, CDN edge cache
    #    d. Banco: indice composto, particionamento, replicas de leitura, sharding
    # 3. Retornar 2-4 alternativas que NAO estao mencionadas na declaracao original
    pass


def classify_statement(candidate: CandidateStatement) -> ClassificationResult:
    """
    Classifica uma declaracao candidata como GOAL ou SPEC_IN_DISGUISE.

    Args:
        candidate: A declaracao a ser classificada.

    Returns:
        ClassificationResult com veredito, justificativa, e sugestoes.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Executar two_implementations_test(candidate.statement)
    # 2. Se is_goal:
    #    a. verdict = GOAL
    #    b. alternative_implementations = suggest_alternatives(statement)
    # 3. Se nao:
    #    a. verdict = SPEC_IN_DISGUISE
    #    b. rewritten_goal = extract_underlying_goal(statement)
    # 4. Preencher signal_words_found = find_signal_words(statement)
    # 5. Retornar ClassificationResult
    pass


# ============================================================
# TESTES RAPIDOS: Classificador
# ============================================================

if __name__ == "__main__":
    # Teste 1: Especificacao pura deve ser detectada
    spec = CandidateStatement(
        statement_id="TEST-001", author="test",
        statement="Adicionar um cache Redis de 3 camadas com warming preditivo na busca",
        domain="search",
    )
    result = classify_statement(spec)
    assert result.verdict == ClassificationVerdict.SPEC_IN_DISGUISE, (
        f"Esperado SPEC_IN_DISGUISE, obtido {result.verdict.value}"
    )
    assert len(result.signal_words_found) >= 3, (
        f"Deve encontrar ao menos 3 palavras-sinal, encontrou {len(result.signal_words_found)}: {result.signal_words_found}"
    )
    assert result.rewritten_goal != "", "Deve propor reescrita da meta"
    print("Teste 1 passou: especificacao detectada")
    print(f"  Palavras-sinal: {result.signal_words_found}")
    print(f"  Meta subjacente: {result.rewritten_goal}")

    # Teste 2: Meta genuina deve ser reconhecida
    goal = CandidateStatement(
        statement_id="TEST-002", author="test",
        statement="Reduzir o tempo de resposta da busca para menos de 200ms no p95",
        domain="search",
    )
    result = classify_statement(goal)
    assert result.verdict == ClassificationVerdict.GOAL, (
        f"Esperado GOAL, obtido {result.verdict.value}"
    )
    assert len(result.alternative_implementations) >= 2, (
        f"Deve sugerir ao menos 2 alternativas, sugeriu {len(result.alternative_implementations)}"
    )
    print("\nTeste 2 passou: meta genuina reconhecida")
    print(f"  Alternativas: {result.alternative_implementations}")

    # Teste 3: "migrar" denuncia especificacao
    migration = CandidateStatement(
        statement_id="TEST-003", author="test",
        statement="Migrar o banco de dados do KODA de PostgreSQL para MongoDB com sharding automatico",
        domain="database",
    )
    result = classify_statement(migration)
    assert result.verdict == ClassificationVerdict.SPEC_IN_DISGUISE, (
        f"Esperado SPEC_IN_DISGUISE, obtido {result.verdict.value}"
    )
    print("\nTeste 3 passou: verbo 'migrar' detectado como sinal de especificacao")

    # Teste 4: Declaracao sem ferramentas nem padroes deve ser GOAL
    pure_goal = CandidateStatement(
        statement_id="TEST-004", author="test",
        statement="Garantir que o cliente veja apenas produtos compativeis com suas restricoes alimentares",
        domain="product_search",
    )
    result = classify_statement(pure_goal)
    assert result.verdict == ClassificationVerdict.GOAL, (
        f"Esperado GOAL, obtido {result.verdict.value}"
    )
    print("\nTeste 4 passou: meta pura (sem ferramentas) classificada como GOAL")

    # Teste 5: ClassificationReport agrega corretamente
    candidates = [spec, goal, migration, pure_goal]
    report = ClassificationReport(
        report_id="RPT-001",
        candidates=candidates,
    )
    for c in candidates:
        report.results.append(classify_statement(c))

    assert report.goal_count == 2, f"Esperado 2 GOALs, obtido {report.goal_count}"
    assert report.spec_count == 2, f"Esperado 2 SPECs, obtido {report.spec_count}"
    print("\nTeste 5 passou: relatorio agregado corretamente")
    print(f"  GOALs: {report.goal_count}, SPECs: {report.spec_count}")

    print("\nTodos os testes do GoalSpecClassifier passaram!")
```

---

### Parte 3: Pipeline de Intent com Classificador (20 min)

Agora implemente o pipeline completo que integra o `GoalSpecClassifier` ao `IntentReceiver`. O receiver modificado NAO pode encaminhar intents cuja descricao e uma `SPEC_IN_DISGUISE` sem antes reescreve-la como `GOAL`.

```python
# ============================================================
# INTENT RECEIVER COM GOALSPEC CLASSIFIER
# ============================================================

@dataclass
class DispatchResult:
    """Resultado de uma tentativa de dispatch."""
    statement_id: str
    dispatched: bool
    classification: ClassificationResult
    error: str = ""


class IntentReceiver:
    """
    Receiver que classifica intents antes do dispatch.

    Fluxo:
    1. Receber declaracao do outcome owner
    2. Classificar com GoalSpecClassifier
    3. Se GOAL: encaminhar para dispatch imediato
    4. Se SPEC_IN_DISGUISE:
       a. Registrar no ClassificationReport
       b. Retornar a meta reescrita para o author revisar
       c. NAO encaminhar para dispatch ate que o author confirme
    5. Se o author discorda da reclassificacao, registrar o overrule
    """

    def __init__(self):
        # TODO: Inicializar listas de espera e historico
        self.pending_rewrites: dict[str, ClassificationResult] = {}
        self.dispatched: list[DispatchResult] = []
        pass

    def receive(self, candidate: CandidateStatement) -> DispatchResult:
        """
        Recebe uma declaracao e decide se pode ser dispatcher.

        Args:
            candidate: A declaracao do outcome owner.

        Returns:
            DispatchResult com status do dispatch.
        """
        # SEU CODIGO AQUI
        #
        # Algoritmo sugerido:
        # 1. result = classify_statement(candidate)
        # 2. Se result.verdict == GOAL:
        #    a. dispatched = True
        #    b. Registrar dispatch
        # 3. Se result.verdict == SPEC_IN_DISGUISE:
        #    a. dispatched = False
        #    b. Armazenar em pending_rewrites
        #    c. Retornar com rewritten_goal para o author
        # 4. Retornar DispatchResult
        pass

    def author_confirms_rewrite(self, statement_id: str) -> DispatchResult:
        """
        Author revisou a meta reescrita e confirmou que esta correta.

        Args:
            statement_id: ID da declaracao original.

        Returns:
            DispatchResult com dispatched=True e a meta reescrita.
        """
        # SEU CODIGO AQUI
        #
        # 1. Buscar em pending_rewrites
        # 2. Se encontrado: marcar como dispatcher, remover de pending
        # 3. Se nao encontrado: erro
        pass

    def author_overrules(self, statement_id: str, reason: str) -> DispatchResult:
        """
        Author discorda da reclassificacao. Ex: "TF-IDF no Pinecone e
        uma constraint externa -- o time de arquitetura decidiu."

        Args:
            statement_id: ID da declaracao original.
            reason: Justificativa do author.

        Returns:
            DispatchResult com dispatched=True e a declaracao original.
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# TESTE COMPLETO DO PIPELINE
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTE DO PIPELINE DE DISPATCH COM GOALSPEC CLASSIFIER")
    print("=" * 60)

    receiver = IntentReceiver()

    # Cenario 1: Meta genuina → dispatch imediato
    print("\n--- Cenario 1: Meta Genuina ---")
    goal = CandidateStatement("INT-101", "pm_maria",
        "Reduzir latencia da busca para < 200ms p95",
        domain="search")
    result = receiver.receive(goal)
    print(f"  Dispatched: {result.dispatched}")
    print(f"  Verdict: {result.classification.verdict.value}")
    assert result.dispatched, "Meta genuina deve ser dispatcher imediatamente"

    # Cenario 2: Especificacao → bloqueado, reescrita sugerida
    print("\n--- Cenario 2: Especificacao Mascarada ---")
    spec = CandidateStatement("INT-102", "dev_carlos",
        "Adicionar um worker Celery com Redis broker para processar notificacoes",
        domain="notifications")
    result = receiver.receive(spec)
    print(f"  Dispatched: {result.dispatched}")
    print(f"  Verdict: {result.classification.verdict.value}")
    print(f"  Meta sugerida: {result.classification.rewritten_goal}")
    assert not result.dispatched, "Especificacao NAO deve ser dispatcher sem revisao"

    # Cenario 3: Author confirma reescrita → dispatch liberado
    print("\n--- Cenario 3: Author Confirma Reescrita ---")
    result = receiver.author_confirms_rewrite("INT-102")
    print(f"  Dispatched: {result.dispatched}")
    assert result.dispatched, "Apos confirmacao, dispatch deve ser liberado"

    print("\n" + "=" * 60)
    print("PIPELINE DE DISPATCH COM GOALSPEC CLASSIFIER COMPLETO")
    print("=" * 60)
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce classificou corretamente os 5 candidatos (A-E) como GOAL ou SPEC_IN_DISGUISE
- [ ] Para cada SPEC_IN_DISGUISE, voce propos uma reescrita que remove ferramentas e metodos
- [ ] Voce identificou as palavras-sinal que denunciaram cada especificacao

### Criterio 2: Classificador funcional

- [ ] `find_signal_words()` detecta Redis, Pinecone, PostgreSQL, cache, polling, migrar, etc.
- [ ] `two_implementations_test()` classifica corretamente o caso "Redis + cache + prefix tree" como SPEC
- [ ] `two_implementations_test()` classifica corretamente "reduzir latencia para < 200ms" como GOAL
- [ ] `extract_underlying_goal()` produz reescritas que removem mencoes a ferramentas
- [ ] `suggest_alternatives()` retorna de 2 a 4 implementacoes diferentes para uma meta genuina

### Criterio 3: Pipeline de dispatch

- [ ] Meta genuina → dispatch imediato (`dispatched=True`)
- [ ] Especificacao mascarada → dispatch bloqueado (`dispatched=False`), reescrita sugerida
- [ ] Author confirma reescrita → dispatch liberado

### Criterio 4: Testes

- [ ] Teste 1: especificacao detectada com ao menos 3 palavras-sinal
- [ ] Teste 2: meta genuina reconhecida com ao menos 2 alternativas
- [ ] Teste 3: verbo "migrar" detectado como sinal
- [ ] Teste 4: meta pura classificada como GOAL
- [ ] Teste 5: relatorio agrega corretamente (2 GOALs, 2 SPECs)

---

## Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao classificou os candidatos | Classificou parcialmente | Classificou todos + identificou palavras-sinal | Diagnostico completo + reescrita de todos os SPECs |
| **Classificador (Parte 2)** | 40% | Nao implementado ou heuristicas ausentes | Detecta palavras-sinal mas nao classifica | Classifica corretamente + extrai meta subjacente | Classificador completo com reescrita por template e alternativas |
| **Pipeline (Parte 3)** | 30% | Nao implementado | Pipeline funciona mas sem bloqueio de SPECs | Pipeline bloqueia SPECs e permite confirmacao | Pipeline completo com overrule, confirmacao, e historico |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 2 criterios passam | 4 criterios passam | Todos os 5 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o Classificador

1. **Ferramentas sao o sinal mais forte.** Se a declaracao nomeia uma tecnologia especifica (Redis, Pinecone, Kafka), ha 90% de chance de ser uma especificacao. A excecao e quando a ferramenta JA e uma constraint externa (ex: "usar a API da Loggi" -- se o contrato com a Loggi ja existe, isso e uma constraint, nao uma especificacao).

2. **Metricas de resultado sao o sinal de meta.** "menos de 200ms", "p95", "maximo 3 segundos", "ate 10x o volume atual" -- essas frases descrevem O QUE alcancar, nao COMO. Sao fortes indicadores de GOAL.

3. **O teste nao e binario -- e um gradiente.** "Usar PostgreSQL" pode ser meta se o contexto for "qual banco de dados adotar?" e especificacao se o contexto for "como otimizar a busca?". O classificador deve considerar o dominio da declaracao.

### Para a Reescrita

1. **Pergunte "para que?" a cada ferramenta.** "Redis" → para que? Cache. "Cache" → para que? Latencia baixa. "Latencia baixa" → isso e uma meta! A cadeia "ferramenta → proposito → resultado" revela a meta subjacente.

2. **Templates salvam tempo.** Em vez de gerar reescrita criativa, mantenha 3-4 templates:
   - "Usar [ferramenta] para [proposito]" → "[Proposito] com [metrica de resultado]"
   - "Migrar [X] de [A] para [B]" → "Garantir que [X] suporte [requisito nao atendido por A]"
   - "Implementar [padrao] em [sistema]" → "[Sistema] com [resultado que o padrao entrega]"

### Para Alternativas

1. **Alternativas provam que e meta.** Se voce consegue listar 3 implementacoes diferentes que satisfazem a declaracao, ela e uma meta. Se nao consegue listar 2, e uma especificacao. Use esta propriedade como verificacao circular do seu proprio classificador.

2. **Mantenha um catalogo por dominio.** Busca: PostgreSQL GIN, Elasticsearch, Pinecone, Meilisearch, Redis Search. Notificacao: Polling, WebSocket, SSE, Push API. Nao precisa ser exaustivo -- 3-4 por dominio bastam.

---

## Duvidas Comuns

**P: E se a ferramenta for uma constraint externa? "Usar a API da Loggi" -- o contrato ja existe.**
R: O classificador detecta a ferramenta e classifica como SPEC_IN_DISGUISE. Isso esta correto -- o receiver deve devolver a reescrita "Garantir tracking de pedidos em tempo real" e o author pode fazer overrule: "A API da Loggi e uma constraint externa -- o contrato ja foi assinado." O overrule e uma decisao consciente, nao um deslize.

**P: Toda meta com nome de ferramenta e realmente uma especificacao?**
R: Nao. "Adotar PostgreSQL como banco de dados principal" pode ser uma meta arquitetural legitima se a decisao e sobre qual banco usar. O contexto importa: se o dominio e "database_selection", nomear uma ferramenta pode ser a meta. Se o dominio e "product_search", nomear PostgreSQL e provavelmente uma especificacao.

**P: Isso nao e obvio demais? As pessoas realmente confundem meta com especificacao?**
R: E o erro mais comum em intents para agentes. Acontece porque humanos estao acostumados a dar instrucoes passo-a-passo para outros humanos ("faca X, depois Y, usando Z"). Para agentes, instrucoes passo-a-passo REMOVEM o valor do agente -- se voce ja decidiu COMO, o agente e so um datilografo. O Teste das Duas Implementacoes existe para preservar o espaco de decisao do agente.

**P: Como isso se relaciona com o Intent Five-Part Primitive?**
R: O GoalSpecClassifier atua ANTES do Intent Completeness Gate. Primeiro voce garante que a descricao e uma meta genuina (GoalSpecClassifier), depois garante que a meta esta completa com constraints, failure scenarios, etc. (Intent Completeness Gate). Sao dois gates em sequencia: pureza → completude.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns.md` para entender o contexto completo do padrao
2. Compare com `docs/canonical/intent-five-part-primitive.md` -- observe como o GoalSpecClassifier garante que o campo `description` do intent seja uma meta pura
3. (Opcional) Integre o GoalSpecClassifier ao Grill-Me Alignment Interview: adicione a pergunta "Duas implementacoes diferentes conseguiriam satisfazer isso?" ao questionario

---

*Exercicio Two-Implementations Goal Test | Nivel 2 - Padroes Praticos*

**Nunca mais "implemente TF-IDF no Pinecone".**
