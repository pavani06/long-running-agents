# Plano: Integração Curricular — Context Management Patterns

**Data:** 2026-06-10
**Fonte:** `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/`
**5 novos canônicos:** `docs/canonical/{head-tail-context-truncation, addressable-memory-catalog, n-plus-one-long-session-evals, stable-harness-prompt, late-failure-regression-suite}.md`
**Objetivo:** Atualizar o currículo do `long-running-agents` para cobrir os 5 padrões Partial Coverage, integrando-os aos módulos existentes sem reescrever a narrativa-base.

---

## Ordem de dependência

Cada área constrói sobre a anterior — executar nessa ordem:

1. **Stable Harness Prompt** — invariante arquitetural (o prompt não é reduzível)
2. **Addressable Memory Catalog** — interface de recuperação (catálogo entre retrieval e state)
3. **Head-Tail Context Truncation** — estratégia de redução (usa o catálogo para middle recovery)
4. **N+1 Long-Session Evals** — validação (prova que as estratégias 1-3 funcionam em sessões longas)
5. **Late-Failure Regression Suite** — proteção contínua (congela falhas encontradas pelos evals N+1)

---

## Área 1: Stable Harness Prompt

**Canônico:** `docs/canonical/stable-harness-prompt.md`
**Canônico de suporte:** `docs/canonical/owned-agent-control-loop.md:47-54, 87-98`

### Arquivo 1.1 — `curriculum/07-implementation-guides/03-harness-design-checklist.md`

**Seção:** Contexto (linhas 269-356)
**Inserção:** Após o bloco `critical_state` / `history_summary` / `recent_window` (~linha 300), adicionar:

```
### X. Stable Harness Prompt (NÃO redutível por compactação)

**O que um bom harness faz:** O system prompt do harness é tratado como âncora estável. Compactação e truncation reduzem history, tool calls e payload — nunca o harness prompt. O prompt tem budget próprio, versionamento explícito e é avaliado separadamente da política de redução de contexto.

**Por que importa:** Se o harness for truncado ou resumido junto com o payload, o agente perde as instruções que governam seu comportamento. Falhas de contexto que corrompem o harness são silenciosas e catastróficas — o agente para de seguir regras sem emitir erro.

**Checklist:**
| # | Item | PASS/FAIL |
|---|---|---|
| 1 | O system prompt tem budget de tokens separado do payload | |
| 2 | A política de compactação NUNCA resume ou trunca o harness prompt | |
| 3 | Cada versão do harness prompt tem ID semântico versionado | |
| 4 | Mudanças no harness prompt são testadas com evals dedicados (não misturados com evals de contexto) | |
| 5 | O metadata de replay inclui `prompt_version` | |
| 6 | Existe teste que falha se a compactação mutar o harness | |
```

**Seção:** Evolução (linhas 839-846)
**Inserção:** Adicionar item sobre prompt versioning nas perguntas de auditoria:

```
- O harness prompt tem versionamento independente da política de contexto?
- Mudanças no harness passam pelo mesmo gate de regressão que mudanças de compactação?
```

---

## Área 2: Addressable Memory Catalog

**Canônico:** `docs/canonical/addressable-memory-catalog.md`

### Arquivo 2.1 — `curriculum/05-core-concepts/01-context-management.md`

**Seção:** Strategies → após "Retrieval (Vector/Embedding-based)" (~linha 613)
**Inserção:** Novo sub-bloco:

```
### Addressable Memory Catalog

Enquanto retrieval semântico busca por similaridade, o **catálogo de memória endereçável** expõe o conteúdo omitido como uma lista navegável de handles. Cada entrada contém:

- `id` — identificador estável
- `kind` — tipo (message, tool_call, span, trace)
- `location` — onde o conteúdo completo está armazenado
- `preview` — resumo de 1-2 linhas para decisão
- `scope` — qual conversa/sessão/span o item pertence
- `fetch` — como recuperar o conteúdo completo

O catálogo é compacto o suficiente para viver no contexto ativo. O agente consulta o catálogo, decide quais IDs são relevantes, e recupera apenas esses. Sem o catálogo, retrieval semântico pode trazer chunks similares mas errados; com o catálogo, a recuperação é determinística e auditável.

**Exemplo (KODA):** Após head-tail truncation de um trace de 500 spans, o catálogo lista 30 spans omitidos com tipo, preview e ID. Quando o avaliador pergunta "o span de checkout teve erro?", KODA consulta o catálogo, identifica o span relevante pelo preview, e recupera só ele.

**Riscos:** Preview grande demais vira outro blob; preview pequeno demais esconde relevância. Staleness: o catálogo envelhece se o conteúdo omitido muda. Escopo: IDs precisam ser únicos e estáveis entre sessões.
```

### Arquivo 2.2 — `curriculum/05-core-concepts/05-state-persistence.md`

**Seção:** Aplicação prática KODA → após "Contratos de Persistência" (~linha 586)
**Inserção:** Adicionar referência ao catálogo como interface entre retrieval e state:

```
O Addressable Memory Catalog complementa a persistência de estado: enquanto o estado durável guarda facts, decisões e checkpoints, o catálogo guarda handles para conteúdo omitido que pode ser relevante em turns futuros. No KODA, o `retrieval_manifest.json` já cumpre parte desse papel — a diferença é que o catálogo adiciona `preview` e `kind` para decisão rápida sem recarregar o conteúdo completo.
```

**Seção:** Notas de Decisão → `Manifest` (~linhas 1864-1872)
**Inserção:** Reforçar com menção ao catálogo:

```
> [!note] O catálogo de memória endereçável (Addressable Memory Catalog) estende o conceito de manifest com campos `kind`, `preview` e `fetch`. Enquanto o manifest descreve O QUE foi usado na decisão, o catálogo descreve O QUE está disponível para recuperação futura.
```

---

## Área 3: Head-Tail Context Truncation

**Canônico:** `docs/canonical/head-tail-context-truncation.md`
**Depende de:** Áreas 1 (stable harness) e 2 (memory catalog)

### Arquivo 3.1 — `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md`

**Seção:** Requisitos (linhas 38-59)
**Modificação:** Adicionar variante head-tail aos requisitos:

No bloco `## Requisitos`, após os requisitos existentes, adicionar:

```
### Requisitos Adicionais — Variante Head-Tail

**Funcional:**
- O windowing deve preservar o system prompt INTACTO (nunca reduzido).
- As primeiras N mensagens (head) e as últimas M mensagens (tail) ficam no contexto ativo.
- As mensagens entre head e tail (middle) são removidas do contexto ativo mas armazenadas com identificadores únicos.

**Técnico:**
- Cada mensagem do middle deve ser armazenada com `id`, `role`, `preview` (primeiros 80 chars) e `full_text`.
- O contexto ativo final deve ter: `[system_prompt] + [head] + [tail] + [latest_result]`.
- O agente deve ter acesso a uma função `fetch_omitted(id)` para recuperar conteúdo do middle.

**Validação:**
- O contexto ativo contém system prompt, primeiro turno, último turno e resultado mais recente.
- O middle está ausente do contexto ativo mas recuperável por ID.
- Um follow-up que referencia uma mensagem do middle deve ser respondido corretamente após `fetch_omitted(id)`.
```

**Seção:** Starter Code (linhas 62-188)
**Modificação:** Adicionar dataclasses para o catálogo:

```python
@dataclass
class OmittedMessage:
    id: str
    role: str  # "user" | "assistant" | "tool"
    preview: str  # primeiros 80 caracteres
    full_text: str

@dataclass
class ContextWindow:
    system_prompt: str
    head: list[Message]
    tail: list[Message]
    latest_result: str
    memory_catalog: list[OmittedMessage]  # middle armazenado
```

**Seção:** TESTS (linhas 190-321)
**Modificação:** Adicionar testes para a variante head-tail:

```python
def test_head_tail_preserves_anchors():
    """System prompt, primeira e última mensagens estão no contexto ativo."""
    ...

def test_middle_is_recoverable():
    """Mensagem do middle pode ser recuperada por fetch_omitted(id)."""
    ...

def test_followup_after_truncation():
    """Follow-up que referencia middle ainda é respondido corretamente."""
    ...
```

### Arquivo 3.2 — `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md`

**Seção:** O Que Você Vai Aprender (linhas 113-125)
**Inserção:** Adicionar bullet:

```
- A variante **head-tail com middle recuperável**: quando manter tudo é impossível e sumarizar é arriscado, preserve as âncoras e externalize o meio com recuperação exata.
```

**Seção:** Após "Parte 1" / antes da aplicação prática — ou como nova subseção após a comparação sliding window vs sumarização (~linha 178)
**Inserção:**

```
### Head-Tail com Middle Recuperável

Enquanto sliding window mantém as últimas K mensagens e sumarização comprime tudo, **head-tail com middle recuperável** preserva três âncoras:

1. **Head** — O início da conversa (contexto original, intenção do usuário)
2. **Tail** — As últimas interações (estado atual, recência)
3. **System prompt** — As instruções do harness (NUNCA reduzidas)

O middle (tudo entre head e tail) é removido do contexto ativo e armazenado em um **catálogo de memória endereçável** com ID, preview e localização. O agente pode recuperar qualquer item do middle sob demanda.

**Quando usar:**
- Contexto grande demais para sliding window
- Sumarização é arriscada (dados estruturados, traces, spans)
- Follow-ups precisam referenciar partes específicas do histórico

**Quando NÃO usar:**
- Contexto cabe inteiro na janela (não complique)
- As mensagens do middle são homogêneas e sem necessidade de recuperação pontual (sumarização basta)
- O overhead de manter o catálogo supera o benefício
```

### Arquivo 3.3 — `curriculum/05-core-concepts/01-context-management.md`

**Seção:** Strategies → após "Compaction/Compression" (~linha 664)
**Modificação:** Adicionar a variante head-tail como sub-padrão nomeado:

```
#### Head-Tail Truncation (variante de Compaction)

Uma forma específica de compaction que preserva duas âncoras temporais — início e fim da conversa — enquanto externaliza o meio. Diferente de sliding window (que descarta o passado) e summarization (que comprime sem recuperação exata), head-tail mantém o conteúdo omitido acessível via catálogo endereçável.

**Exemplo KODA:** Numa sessão de 2h com 40 turnos, o contexto ativo mantém:
- System prompt do harness
- Turnos 1-3 (cliente explicou alergia e preferências)
- Turnos 37-40 (discutindo frete e pagamento)
- Turnos 4-36 no catálogo, recuperáveis se o cliente perguntar "aquele suplemento que você mencionou antes..."
```

---

## Área 4: N+1 Long-Session Evals

**Canônico:** `docs/canonical/n-plus-one-long-session-evals.md`
**Depende de:** Área 3 (head-tail truncation)

### Arquivo 4.1 — `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`

**Seção:** P4: Compactação server-side (~linhas 488-506)
**Reforço:** Adicionar ao bloco:

```
**N+1 Long-Session Evals como gate de P4:**
- Criar fixtures de 10 turnos realistas com a política de compactação aplicada
- O 11º turno testa: continuidade, follow-up, e ausência de alucinação por perda de contexto
- Aprovação de P4 requer ≥95% de acerto no N+1 eval
```

**Seção:** Playbook de Shadow Test (linhas 844-940)
**Inserção:** Após os passos existentes, adicionar:

```
### Shadow Test N+1 (específico para compactação)

1. **Fixture:** 10 conversas reais de KODA com 15+ turnos cada
2. **Aplicar:** Política de compactação atual (head-tail com catálogo)
3. **Testar:** Para cada conversa, fazer a 16ª pergunta — uma que depende de contexto dos turnos 5-10
4. **Medir:** Taxa de acerto do 16º turno vs baseline (conversa sem compactação)
5. **Gate:** Shadow N+1 ≥ baseline −5% → aprova; abaixo → revisa política antes de canary
```

### Arquivo 4.2 — `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`

**Seção:** Passo 4: Rode Testes de Regressão Antes do Canary (linhas 741-769)
**Inserção:** Adicionar bateria N+1:

```
**Bateria N+1 Long-Session (contexto):**
Antes do canary, rode também:
1. 5 fixtures N+1 pré-gravadas (10 turnos + 11º pergunta)
2. Aplicar a política de contexto atual em cada fixture
3. Comparar resposta do 11º turno com expected_output
4. Qualquer regressão → abortar rollout, revisar política de compactação
```

**Seção:** Tabela da bateria (linhas 1083-1090)
**Inserção:** Adicionar linha:

```
| Long-Session N+1 | 5 fixtures × 11 turnos | Degradação após compactação | Bloqueia rollout | Context & Retrieval |
```

### Arquivo 4.3 — `curriculum/08-tools-templates/evaluation-rubric-template.md`

**Seção:** Passo 8: Rodar regression set (linhas 812-814)
**Reforço:** Adicionar bullet:

```
- Inclua N+1 long-session fixtures no regression set: conversas de 10+ turnos com compactação aplicada, onde o 11º turno testa continuidade e ausência de degradação contextual.
```

---

## Área 5: Late-Failure Regression Suite

**Canônico:** `docs/canonical/late-failure-regression-suite.md`
**Depende de:** Área 4 (N+1 evals)

### Arquivo 5.1 — `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`

**Seção:** Após a tabela da bateria (~linha 1090) ou como nova seção antes de "Observação de 14 dias" (~linha 1110)
**Inserção:**

```
### Late-Failure Regression Suite (contexto)

Falhas de contexto que aparecem tardiamente (turno 15+) devem ser capturadas como casos de regressão permanente:

1. **Captura:** Todo incidente de "KODA esqueceu X depois de Y turnos" gera um caso na suite
2. **Fixture:** session_fixture (conversa completa até o turno da falha), next_turn (pergunta que expôs a falha), expected_behavior (o que deveria ter acontecido)
3. **Metadados:** context_strategy (qual política estava ativa), failure_class (forgetting, hallucination, wrong_retrieval, prompt_corruption), evidence (logs, trace, timestamp)
4. **Gate:** A suite roda ANTES de qualquer mudança em truncation, retrieval, prompt ou memória
5. **Ownership:** Responsável designado revisa a suite mensalmente; casos que passam 3 meses sem falhar podem ser arquivados

Exemplo de caso:
```
fixture: session_2026-05-12_koda_checkout_22_turns.json
next_turn: "Qual era o prazo de entrega que você mencionou?"
expected: mencionar "5 dias úteis" (turno 8)
strategy: head-tail com catálogo
failure: KODA respondeu "não tenho essa informação" — o turno 8 estava no middle e não foi recuperado
```
```

### Arquivo 5.2 — `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`

**Seção:** Governança P7 (~linhas 548-566)
**Reforço:** Adicionar:

```
**Late-Failure Regression Suite como requisito de governança:**
- Toda mudança em compactação/retrieval/memória requer rodar a suite antes do merge
- Novos casos são adicionados automaticamente quando um incidente de contexto tardio é resolvido
- A suite é parte do cycle REVIEW trimestral
```

**Seção:** Fase 3: Shadow test de qualidade (linhas 786-794)
**Inserção:** Adicionar ao checklist:

```
- [ ] Late-failure regression suite passou (0 regressões)
```

### Arquivo 5.3 — `curriculum/08-tools-templates/evaluation-rubric-template.md`

**Seção:** Quality Checklist (linhas 859-871)
**Inserção:** Adicionar item:

```
- [ ] Context degradation cases (late-failure fixtures) estão incluídos no regression set
```

---

## Registro e índices

### `curriculum/INDEX.md`
Se novos exercícios foram criados (apenas modificações neste plano — sem exercícios novos), não requer atualização.

### `curriculum/README.md`
A árvore de diretórios não muda (sem novos arquivos no currículo). Não requer atualização.

### `docs/system-of-record.md`
Já atualizado com os 5 canônicos. Se o plano criar novos docs canônicos, atualizar novamente.

---

## Resumo de arquivos alterados

| # | Arquivo | Tipo de mudança | Áreas |
|---|---|---|---|
| 1 | `curriculum/07-implementation-guides/03-harness-design-checklist.md` | Inserção | 1 |
| 2 | `curriculum/05-core-concepts/01-context-management.md` | Inserção | 2, 3 |
| 3 | `curriculum/05-core-concepts/05-state-persistence.md` | Inserção | 2 |
| 4 | `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md` | Modificação | 3 |
| 5 | `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md` | Inserção | 3 |
| 6 | `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` | Reforço + Inserção | 4, 5 |
| 7 | `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Inserção | 4, 5 |
| 8 | `curriculum/08-tools-templates/evaluation-rubric-template.md` | Reforço | 4, 5 |

Total: 8 arquivos. Nenhum arquivo novo no currículo (só modificações em existentes).
