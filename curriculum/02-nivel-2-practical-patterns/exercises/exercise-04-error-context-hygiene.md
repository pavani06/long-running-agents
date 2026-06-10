---
title: "Exercicio 4: Implementar Error Context Hygiene no Loop de Ferramentas"
type: curriculum-exercise
nivel: 2
aliases: []
tags: [curriculo-conteudo, nivel-2, exercicio, error-context-hygiene, context-pollution, error-summarization, tool-loop, retry-with-feedback, clear-on-success, token-economy, stack-trace-filtering, pinecone-fallback, python]
relates-to: ["[[docs/canonical/error-context-hygiene|Error Context Hygiene]]"]
last_updated: 2026-06-10
---
# Exercicio 4: Implementar Error Context Hygiene no Loop de Ferramentas
## Nivel 2 - Padroes Praticos

**Tempo Estimado:** 45-60 minutos
**Dificuldade:** (Intermediario)
**Pre-requisito:** Ter lido `03-basic-harness-patterns.md` (Nivel 1) + completado Exercicio 2
**Objetivo:** Diagnosticar context pollution em um agent trace e implementar as 4 regras de Error Context Hygiene

---

## Prologo: O Agente Que Entrou em Espiral

### Terca-feira, 10h30. Uma busca que deveria ser simples.

```
CLIENTE: "KODA, me mostra whey protein ate R$ 100"

KODA: [Chamando search_products...]
      ERRO: Pinecone connection refused

KODA: [Chamando search_products de novo...]
      ERRO: Pinecone connection refused

KODA: [Chamando search_products com fallback...]
      ERRO: Pinecone connection refused

KODA: "Desculpe, estou com dificuldades tecnicas. Tente novamente mais tarde."
```

**O que aconteceu nos bastidores?** O context window do agente acumulou:

```
[Historico de conversa...]
Tool: search_products → ERRO: PineconeServiceError: Connection refused
    at PineconeClient.query (/app/src/services/vector/PineconeClient.ts:47:15)
    at SearchProductsTool.execute (/app/src/agents/tools/SearchProductsTool.ts:89:22)
    ... 15 stack frames ...

Tool: search_products → ERRO: PineconeServiceError: Connection refused
    at PineconeClient.query (/app/src/services/vector/PineconeClient.ts:47:15)
    ... (mesmo stack trace, de novo)

Tool: search_products → ERRO: PineconeServiceError: Connection refused
    ... (terceira vez)
```

**O problema:** O modelo leu 3 vezes o mesmo stack trace de 40 linhas. Esses 120 tokens de stack trace ensinaram ao modelo que "o sistema esta quebrado". Na quarta tentativa, ele nem tentou mais — foi direto para a mensagem de fallback.

**O que deveria ter acontecido:**

```
[Historico de conversa...]
[error] search_products: Pinecone connection refused. Retrying with broader query.
[error] search_products: Pinecone connection refused (attempt 2/3). Trying fallback: local catalog.
[error] search_products: Pinecone connection refused (attempt 3/3). Escalating to human.
```

3 linhas. 15 tokens. O modelo teria contexto suficiente para tentar uma estrategia diferente, sem ser intoxicado pelo stack trace.

**Sua missao:** Consertar esse loop. Implementar Error Context Hygiene em um agente simulado e impedir que erros poluam a janela de contexto.

---

## O Cenario: ProdutoAgent com Ferramentas Instaveis

### Contexto

Voce recebeu o codigo de um `ProdutoAgent` que busca produtos em 3 fontes:

1. **Pinecone** (busca vetorial) — instavel, cai com frequencia
2. **Catalogo Local** (PostgreSQL) — estavel, mas resultados menos relevantes
3. **API de Fornecedores** (HTTP externa) — lenta, timeout de 5s

O agente atual implementa fallback em cascata (Pinecone → Catalogo → Fornecedores), mas **nao implementa Error Context Hygiene**. Cada falha joga o stack trace inteiro no contexto, e o agente frequentemente "desiste" depois de 2 erros.

### Dados de Entrada

O agente recebe:

```json
{
  "query": "whey protein isolate 1kg",
  "max_price": 120.00,
  "user_id": "wa_5511987654321",
  "dietary_restrictions": ["lactose_intolerant"]
}
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Summarize Errors:** Todo erro de ferramenta deve ser convertido em uma unica linha no formato `[error] <tool>: <type>. <hint>`
2. **RF2 - Clear on Success:** Quando uma ferramenta sucede apos falhas, todos os erros pendentes devem ser removidos do contexto
3. **RF3 - Never Blind-Append:** Nenhum stack trace, corpo de resposta HTTP, ou erro cru deve entrar no contexto
4. **RF4 - Retry with Feedback:** A cada retry, o hint deve evoluir (ex: "retrying" → "attempt 2/3: trying fallback" → "max retries exceeded")
5. **RF5 - Max 3 Retries:** Apos 3 tentativas, escalar para fallback final ou humano

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Error Summarizer separado:** A funcao `summarize_error()` deve ser reutilizavel para qualquer ferramenta
3. **RT3 - Contexto como lista:** O contexto do agente e uma `list[str]`. Cada entrada e uma mensagem ou erro sumarizado
4. **RT4 - Teste com trace realista:** O cenario de teste deve incluir falhas genuinas e verificar que o contexto final nao contem stack traces

---

## Sua Tarefa

Voce vai implementar Error Context Hygiene em 3 partes.

---

### Parte 1: Diagnosticar o Contexto Poluido (10 min)

Analise o trace abaixo. Este e o estado atual do agente — sem Error Context Hygiene.

```python
# Trace real de uma sessao do ProdutoAgent (ANTES da higiene)
CONTEXT_SEM_HIGIENE = [
    # Mensagens normais da conversa
    "USER: Me mostra whey protein ate R$ 100",

    # Tentativa 1: Pinecone
    "TOOL: search_products_pinecone",
    "ERROR: PineconeServiceError: Connection refused\n"
    "    at PineconeClient.query (/app/src/services/vector/PineconeClient.ts:47:15)\n"
    "    at SearchProductsTool.execute (/app/src/agents/tools/SearchProductsTool.ts:89:22)\n"
    "    at AgentNode.invoke (/app/src/agents/nodes/ecommerceNode.ts:156:10)\n"
    "    at AgentGraph.run (/app/src/agents/agentsGraph.ts:89:5)\n"
    "    ... 12 more stack frames ...",

    # Tentativa 2: Pinecone de novo (mesmo erro)
    "TOOL: search_products_pinecone",
    "ERROR: PineconeServiceError: Connection refused\n"
    "    at PineconeClient.query (/app/src/services/vector/PineconeClient.ts:47:15)\n"
    "    ... (mesmo stack trace de 40 linhas)",

    # Tentativa 3: Catalogo Local (sucesso!)
    "TOOL: search_products_catalog",
    "RESULT: Encontrados 3 produtos: Whey Vegano (R$ 95), Whey Isolado (R$ 110), Whey Concentrado (R$ 75)",

    # Mas os erros do Pinecone ainda estao no contexto!
    # O modelo ve 80 linhas de stack trace + 3 produtos.
]

# TAREFA: Responda no seu codigo como comentario:
#
# 1. Quantos tokens aproximadamente sao gastos com stack traces nesse contexto?
# 2. Que vies esses erros podem criar no modelo?
# 3. Qual seria o contexto equivalente COM Error Context Hygiene? (escreva manualmente)
```

**Resposta esperada (em comentario):**

```python
# 1. ~20 linhas de stack trace × 2 tentativas × ~6 tokens/linha ≈ 240 tokens desperdicados
# 2. Vies: "o sistema esta instavel" → modelo evita novas tool calls, gera fallback prematuro
# 3. Contexto com higiene:
#    "USER: Me mostra whey protein ate R$ 100"
#    "[error] search_products_pinecone: connectivity. Retrying with broader query."
#    "[error] search_products_pinecone: connectivity (attempt 2/3). Trying fallback: local catalog."
#    "[recovered] search_products_catalog: Found 3 products."
```

---

### Parte 2: Implementar o Error Summarizer (20 min)

Implemente as funcoes de higiene. Use este esqueleto:

```python
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Any
from enum import Enum
import json


# ============================================================
# DATA MODELS
# ============================================================

class ErrorType(Enum):
    CONNECTIVITY = "connectivity"
    BAD_REQUEST = "bad_request"
    AUTH = "auth"
    NOT_FOUND = "not_found"
    RATE_LIMIT = "rate_limit"
    UPSTREAM = "upstream"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    data: Optional[Any] = None
    error: Optional[Exception] = None
    error_message: str = ""


@dataclass
class ErrorSummary:
    tool_name: str
    error_type: ErrorType
    hint: str
    attempt: int = 1
    max_attempts: int = 3

    def format(self) -> str:
        """Formata o erro como uma unica linha."""
        if self.attempt >= self.max_attempts:
            return f"[error] {self.tool_name}: {self.error_type.value}. {self.hint}"
        return f"[error] {self.tool_name}: {self.error_type.value} (attempt {self.attempt}/{self.max_attempts}). {self.hint}"


# ============================================================
# ERROR CLASSIFIER
# ============================================================

def classify_error(error: Exception) -> ErrorType:
    """
    Classifica um erro em um dos tipos conhecidos.
    Inspecione a mensagem e o tipo da excecao para decidir.
    """
    msg = str(error).lower()

    if any(kw in msg for kw in ["connection refused", "econnrefused", "timeout"]):
        return ErrorType.CONNECTIVITY
    if any(kw in msg for kw in ["400", "bad request", "validation"]):
        return ErrorType.BAD_REQUEST
    if any(kw in msg for kw in ["401", "403", "unauthorized"]):
        return ErrorType.AUTH
    if any(kw in msg for kw in ["404", "not found"]):
        return ErrorType.NOT_FOUND
    if any(kw in msg for kw in ["429", "rate limit"]):
        return ErrorType.RATE_LIMIT
    if any(kw in msg for kw in ["500", "internal server", "502", "503"]):
        return ErrorType.UPSTREAM
    if any(kw in msg for kw in ["timeout", "timed out"]):
        return ErrorType.TIMEOUT

    return ErrorType.UNKNOWN


# ============================================================
# HINT GENERATOR
# ============================================================

def derive_hint(error_type: ErrorType, attempt: int, max_attempts: int) -> str:
    """
    Gera uma dica acionavel baseada no tipo de erro e na tentativa atual.

    A dica deve EVOLUIR a cada tentativa:
    - Tentativa 1: sugestao de retry com parametro ajustado
    - Tentativa 2: sugestao de fallback para fonte alternativa
    - Tentativa 3 (ultima): escala para humano ou fallback final
    """
    # SEU CODIGO AQUI
    # Dica: use um dicionario de hints por ErrorType, adaptando pela tentativa
    pass


# ============================================================
# ERROR SUMMARIZER
# ============================================================

def summarize_error(
    tool_name: str,
    error: Exception,
    attempt: int = 1,
    max_attempts: int = 3
) -> ErrorSummary:
    """
    Converte um erro cru em um ErrorSummary higienico.

    Regras:
    1. Classifique o tipo de erro
    2. Gere uma dica acionavel
    3. Retorne um ErrorSummary (NUNCA o stack trace)
    """
    # SEU CODIGO AQUI
    pass


# ============================================================
# CONTEXT HYGIENE
# ============================================================

def clear_pending_errors(context: List[str]) -> List[str]:
    """
    Remove todas as mensagens de erro do contexto.
    Uma mensagem de erro e qualquer string que comece com '[error]'.
    """
    # SEU CODIGO AQUI
    return [msg for msg in context if not msg.startswith("[error]")]


def inject_recovery(context: List[str], tool_name: str, result_count: int) -> None:
    """
    Apos uma recuperacao bem-sucedida, injeta uma mensagem de recuperacao
    no contexto para sinalizar ao modelo que o erro foi superado.

    Formato: "[recovered] <tool_name>: Found <n> results. Errors cleared."
    """
    # SEU CODIGO AQUI
    pass


# ============================================================
# TESTE RAPIDO: Error Summarizer
# ============================================================

if __name__ == "__main__":
    # Teste 1: Classificar um erro de conexao
    conn_error = ConnectionRefusedError("Connection refused")
    error_type = classify_error(conn_error)
    assert error_type == ErrorType.CONNECTIVITY, f"Esperado CONNECTIVITY, obtido {error_type}"

    # Teste 2: Sumarizar um erro com hint evolutivo
    summary = summarize_error("search_products_pinecone", conn_error, attempt=1, max_attempts=3)
    assert summary.format().startswith("[error]"), "Erro deve comecar com [error]"
    assert "Connection refused" not in summary.format(), "Nao deve conter mensagem crua do erro"
    assert "connectivity" in summary.format(), "Deve conter o tipo de erro classificado"
    print("Teste 2 passou:", summary.format())

    # Teste 3: Hint evolutivo
    s1 = summarize_error("search_products", conn_error, attempt=1, max_attempts=3)
    s2 = summarize_error("search_products", conn_error, attempt=2, max_attempts=3)
    s3 = summarize_error("search_products", conn_error, attempt=3, max_attempts=3)
    assert s1.hint != s2.hint, "Hint deve evoluir entre tentativas"
    assert s2.hint != s3.hint, "Hint deve evoluir entre tentativas"
    print("Teste 3 passou: Hints evolutivos OK")
    print("  Tentativa 1:", s1.format())
    print("  Tentativa 2:", s2.format())
    print("  Tentativa 3:", s3.format())

    # Teste 4: clear_pending_errors
    ctx = [
        "USER: busca whey",
        "[error] tool1: connectivity. Retrying.",
        "[error] tool1: connectivity. Fallback.",
        "RESULT: 3 produtos encontrados",
    ]
    cleaned = clear_pending_errors(ctx)
    assert len(cleaned) == 2, f"Esperado 2 mensagens, obtido {len(cleaned)}"
    assert "[error]" not in cleaned[0], "Primeira mensagem nao deve ser erro"
    assert "[error]" not in cleaned[1], "Segunda mensagem nao deve ser erro"
    print("Teste 4 passou: clear_pending_errors OK")

    print("\nTodos os testes do Error Summarizer passaram!")
```

---

### Parte 3: Pipeline do ProdutoAgent com Higiene (25 min)

Agora implemente o `ProdutoAgent` completo com o pipeline de busca e Error Context Hygiene:

```python
# ============================================================
# MOCK TOOLS (simulando ferramentas reais)
# ============================================================

def search_products_pinecone(query: str, max_price: float) -> ToolResult:
    """
    Simula busca no Pinecone.
    INSTAVEL: 40% de chance de falha.
    """
    import random
    if random.random() < 0.4:
        return ToolResult(
            tool_name="search_products_pinecone",
            success=False,
            error=ConnectionRefusedError("Connection refused"),
            error_message="Connection refused"
        )
    return ToolResult(
        tool_name="search_products_pinecone",
        success=True,
        data=[
            {"name": "Whey Isolado 1kg", "price": 110.00, "score": 0.95},
            {"name": "Whey Vegano 900g", "price": 95.00, "score": 0.88},
        ]
    )


def search_products_catalog(query: str, max_price: float) -> ToolResult:
    """
    Simula busca no catalogo local.
    ESTAVEL: sempre funciona, mas resultados menos relevantes.
    """
    return ToolResult(
        tool_name="search_products_catalog",
        success=True,
        data=[
            {"name": "Whey Concentrado 1kg", "price": 75.00, "score": 0.70},
            {"name": "Whey Isolado 1kg", "price": 110.00, "score": 0.65},
            {"name": "Whey Vegano 900g", "price": 95.00, "score": 0.60},
        ]
    )


def search_products_suppliers(query: str, max_price: float) -> ToolResult:
    """
    Simula busca em API de fornecedores.
    LENTO e com timeout frequente.
    """
    import random
    if random.random() < 0.3:
        return ToolResult(
            tool_name="search_products_suppliers",
            success=False,
            error=TimeoutError("Request timed out after 5s"),
            error_message="Request timed out after 5s"
        )
    return ToolResult(
        tool_name="search_products_suppliers",
        success=True,
        data=[
            {"name": "Whey Isolado Importado 1kg", "price": 130.00, "score": 0.92},
        ]
    )


# ============================================================
# PRODUTO AGENT COM ERROR CONTEXT HYGIENE
# ============================================================

def produto_agent_search(
    query: str,
    max_price: float,
    context: List[str],
    max_retries_per_tool: int = 3
) -> List[str]:
    """
    Pipeline de busca do ProdutoAgent COM Error Context Hygiene.

    Fluxo:
    1. Tenta Pinecone (ate max_retries_per_tool vezes)
       - Cada falha: sumariza erro e adiciona ao contexto
       - Se sucesso: limpa erros, adiciona resultado ao contexto, RETORNA
    2. Tenta Catalogo Local
       - Se Pinecone falhou, tenta catalogo
       - Se sucesso: limpa erros, adiciona resultado, RETORNA
    3. Tenta API de Fornecedores (fallback final)
       - Se ambos falharam, tenta fornecedores
       - Se sucesso: limpa erros, adiciona resultado, RETORNA
    4. Se tudo falhar: adiciona mensagem de fallback humano ao contexto

    REGRA CRITICA: Em NENHUM momento um stack trace ou mensagem de erro crua
    deve entrar no contexto. Apenas ErrorSummary.format().

    Args:
        query: termo de busca
        max_price: preco maximo
        context: lista de strings (contexto atual do agente)
        max_retries_per_tool: maximo de tentativas por ferramenta

    Returns:
        context atualizado (a mesma lista, modificada in-place)
    """
    # SEU CODIGO AQUI

    # Tool chain: Pinecone → Catalogo → Fornecedores
    tools = [
        ("search_products_pinecone", search_products_pinecone),
        ("search_products_catalog", search_products_catalog),
        ("search_products_suppliers", search_products_suppliers),
    ]

    for tool_name, tool_fn in tools:
        # Tenta a ferramenta ate max_retries_per_tool vezes
        for attempt in range(1, max_retries_per_tool + 1):
            result = tool_fn(query, max_price)

            if result.success:
                # SUCESSO: limpa erros pendentes e injeta resultado
                # SEU CODIGO:
                # 1. clear_pending_errors(context)
                # 2. inject_recovery(context, tool_name, len(result.data))
                # 3. Adiciona resultado formatado ao contexto
                # 4. Retorna context
                pass
            else:
                # FALHA: sumariza o erro e adiciona ao contexto
                # SEU CODIGO:
                # 1. summary = summarize_error(tool_name, result.error, attempt, max_retries_per_tool)
                # 2. Adiciona summary.format() ao contexto
                # 3. Continua para proxima tentativa
                pass

        # Se chegou aqui, todas as tentativas dessa ferramenta falharam
        # Continua para a proxima ferramenta na cadeia

    # Se todas as ferramentas falharam
    context.append("[escalated] All search tools failed. Escalating to human agent.")
    return context


# ============================================================
# TESTE COMPLETO DO PIPELINE
# ============================================================

if __name__ == "__main__":
    # Executa o pipeline 5 vezes (Pinecone e Suppliers sao instaveis)
    for run in range(1, 6):
        print(f"\n{'='*60}")
        print(f"EXECUCAO {run}")
        print(f"{'='*60}")

        context = ["USER: Me mostra whey protein ate R$ 100"]

        result_context = produto_agent_search(
            query="whey protein",
            max_price=100.0,
            context=context,
            max_retries_per_tool=3
        )

        # VERIFICACOES AUTOMATICAS
        errors_in_context = [m for m in result_context if m.startswith("[error]")]
        raw_errors = [m for m in result_context if "stack trace" in m.lower()
                      or "traceback" in m.lower()
                      or "connection refused" in m.lower()]  # so msg crua, nao sumarizada

        print(f"\nContexto final ({len(result_context)} mensagens):")
        for i, msg in enumerate(result_context):
            print(f"  [{i}] {msg[:100]}...")

        print(f"\nMetricas:")
        print(f"  Erros sumarizados no contexto: {len(errors_in_context)}")
        print(f"  Erros crus (stack traces): {len(raw_errors)}")

        # ASSERT: NUNCA deve ter stack trace no contexto
        assert len(raw_errors) == 0, \
            f"FALHA: {len(raw_errors)} stack traces encontrados no contexto!"

        # ASSERT: Se ha resultado, nao deve ter erros pendentes
        has_result = any("Found" in m for m in result_context)
        if has_result:
            assert len(errors_in_context) == 0, \
                f"FALHA: {len(errors_in_context)} erros pendentes apos sucesso!"

        print(f"  VERIFICACAO: PASSOU (sem stack traces, contexto limpo)")
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Error Summarizer funcional

- [ ] `classify_error()` classifica corretamente ConnectionRefusedError como CONNECTIVITY
- [ ] `derive_hint()` gera hints diferentes para tentativas 1, 2 e 3
- [ ] `summarize_error().format()` produz exatamente 1 linha, comecando com `[error]`
- [ ] Nenhum `ErrorSummary.format()` contem stack trace ou mensagem crua

### Criterio 2: Context Hygiene funcional

- [ ] `clear_pending_errors()` remove todas as linhas `[error]` do contexto
- [ ] `inject_recovery()` adiciona `[recovered]` apos sucesso

### Criterio 3: Pipeline com higiene

- [ ] O pipeline NUNCA insere stack traces no contexto (verifique com assert)
- [ ] Apos uma ferramenta ter sucesso, o contexto nao contem `[error]` pendentes
- [ ] Hints evoluem entre tentativas (nao repetem a mesma mensagem)
- [ ] Se todas as ferramentas falharem, o contexto termina com `[escalated]`

### Criterio 4: Trace comparativo

- [ ] Voce consegue explicar a diferenca entre o contexto COM e SEM higiene
- [ ] Voce consegue estimar a economia de tokens

---

## Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou os problemas | Identificou 1-2 problemas | Identificou os 3 problemas | Analise quantitativa (tokens, vies, correcao) |
| **Summarizer (Parte 2)** | 35% | Nao implementado ou com erros | Classifica mas hints sao estaticos | Classifica + hints evolutivos | Cobre todos os ErrorTypes com hints contextuais |
| **Pipeline (Parte 3)** | 35% | Nao implementado | Pipeline funciona mas sem higiene | Pipeline com higiene, sem stack traces | Clear on success + recovery injection + evolutive hints |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 2 criterios passam | 3 criterios passam | Todos os 4 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o Error Summarizer

1. **Hints evolutivos sao a chave.** "Tentando de novo" nao ajuda o modelo. "Tentativa 2/3: mudando para busca por categoria em vez de texto livre" ajuda.
2. **O formato e sagrado.** `[error] <tool>: <type>. <hint>` — sempre. Consistencia permite que o modelo reconheca erros como um padrao, nao como surpresas.
3. **Nao invente hints.** Se voce nao sabe o que sugerir, use "Log for investigation; continue with available data."

### Para o Pipeline

1. **Clear on success e a regra mais importante.** Se o Pinecone falhou 2 vezes mas o Catalogo funcionou, os erros do Pinecone sao irrelevantes. Remova-os.
2. **Recovery injection faz diferenca.** `[recovered] search_products_catalog: Found 3 products. Errors cleared.` sinaliza ao modelo: "acabou o periodo de erro, volte ao modo normal."
3. **Teste com seed fixo.** O Pinecone e Suppliers sao instaveis (random). Para debugging, use `random.seed(42)` para ter reprodutibilidade.

---

## Duvidas Comuns

**P: O que acontece se o Error Summarizer falhar?**
R: Tradeoff documentado no canonical doc: se a sumarizacao falhar, o erro原始 deve ser logado (fora do contexto), e um resumo generico `[error] <tool>: unknown. Logged for investigation.` deve entrar no contexto.

**P: Devo manter os erros no contexto para "debug"?**
R: Nao. Debug vai para logs (Winston, CloudWatch, arquivo). Contexto e para o modelo decidir o proximo passo. Sao propositos diferentes.

**P: Isso nao esconde informacao importante do modelo?**
R: O modelo precisa saber QUE ferramenta falhou e QUAL a proxima acao sugerida. Ele NAO precisa do stack trace, dos headers HTTP, ou do corpo da resposta de erro. Isso e higiene, nao censura.

**P: Como isso se relaciona com o Fallback & Retry do Nivel 1?**
R: Fallback & Retry e a camada de infraestrutura (tente de novo, mude de ferramenta). Error Context Hygiene e a camada de contexto (o que o modelo VE sobre essas falhas). Elas sao complementares.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `docs/canonical/error-context-hygiene.md` para entender o padrao completo
2. Compare seu codigo com a habilidade em `.opencode/skills/error-context-hygiene/SKILL.md`
3. (Opcional) Aplique o padrao ao Exercicio 2: adicione Error Context Hygiene ao `checkout_pipeline()`

---

*Exercicio 4 | Nivel 2 - Padroes Praticos | Error Context Hygiene*

**Hora de limpar o contexto!**
