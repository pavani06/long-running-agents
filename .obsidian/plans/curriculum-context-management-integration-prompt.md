# Prompt para Agente Executor — Integração Curricular Context Management

Execute as modificações abaixo em 8 arquivos do currículo do `long-running-agents`, na ordem especificada. Cada área depende da anterior — siga a sequência. NÃO crie arquivos novos no currículo; apenas modifique os existentes. NÃO altere os canônicos em `docs/canonical/` (já estão prontos).

Leia cada arquivo ANTES de editar. Insira conteúdo novo no local exato indicado. Preserve o estilo, formatação e idioma (PT-BR) de cada arquivo. Use `edit` para inserções cirúrgicas.

---

## PREPARAÇÃO

Antes de começar, leia estes 5 canônicos para referência:
- `/mnt/c/Users/pavan/long-running-agents/docs/canonical/stable-harness-prompt.md`
- `/mnt/c/Users/pavan/long-running-agents/docs/canonical/addressable-memory-catalog.md`
- `/mnt/c/Users/pavan/long-running-agents/docs/canonical/head-tail-context-truncation.md`
- `/mnt/c/Users/pavan/long-running-agents/docs/canonical/n-plus-one-long-session-evals.md`
- `/mnt/c/Users/pavan/long-running-agents/docs/canonical/late-failure-regression-suite.md`

E leia também: `/mnt/c/Users/pavan/long-running-agents/docs/canonical/owned-agent-control-loop.md` (linhas 47-54, 87-98).

---

## ÁREA 1: Stable Harness Prompt

### Arquivo: `curriculum/07-implementation-guides/03-harness-design-checklist.md`

**1a.** Na seção "Contexto" (~linha 300), após os blocos de `critical_state`/`history_summary`/`recent_window`, adicione uma NOVA subseção de checklist:

Título: `### X. Stable Harness Prompt (NÃO redutível por compactação)`

Corpo: parágrafo "O que um bom harness faz" explicando que o system prompt do harness é âncora estável — compactação reduz history/tool calls/payload, NUNCA o harness prompt. O prompt tem budget próprio, versionamento e é avaliado separadamente.

Parágrafo "Por que importa": se o harness for truncado junto com o payload, o agente perde instruções silenciosamente.

Tabela checklist com 6 itens:
1. System prompt tem budget de tokens separado do payload
2. Política de compactação NUNCA resume ou trunca o harness prompt
3. Cada versão do harness prompt tem ID semântico versionado
4. Mudanças no harness prompt são testadas com evals dedicados
5. Metadata de replay inclui `prompt_version`
6. Existe teste que falha se a compactação mutar o harness

**1b.** Na seção "Evolução" (~linha 839-846), adicione nas perguntas de auditoria:
- "O harness prompt tem versionamento independente da política de contexto?"
- "Mudanças no harness passam pelo mesmo gate de regressão que mudanças de compactação?"

---

## ÁREA 2: Addressable Memory Catalog

### Arquivo: `curriculum/05-core-concepts/01-context-management.md`

**2a.** Na seção de estratégias, APÓS a subseção "Retrieval (Vector/Embedding-based)" (~linha 613) e ANTES de "Compaction/Compression", INSIRA uma nova subseção:

Título: `### Addressable Memory Catalog`

Corpo explicando que enquanto retrieval busca por similaridade, o catálogo de memória endereçável expõe conteúdo omitido como lista navegável de handles. Liste os 6 campos com descrição curta: `id`, `kind`, `location`, `preview`, `scope`, `fetch`.

Explique que o catálogo é compacto para viver no contexto ativo e permite recuperação determinística.

Inclua exemplo KODA: após head-tail truncation de 500 spans, catálogo lista 30 omitidos com tipo/preview/ID; quando o avaliador pergunta sobre um span específico, KODA consulta o catálogo e recupera só ele.

Liste riscos: preview grande vira blob, preview pequeno esconde relevância, staleness, unicidade de IDs entre sessões.

### Arquivo: `curriculum/05-core-concepts/05-state-persistence.md`

**2b.** Na seção de aplicação KODA, após "Contratos de Persistência" (~linha 586), adicione um parágrafo:

O Addressable Memory Catalog complementa a persistência de estado: estado durável guarda facts/checkpoints; catálogo guarda handles para conteúdo omitido recuperável. No KODA, `retrieval_manifest.json` já cumpre parte — a diferença é `preview` e `kind`.

**2c.** Na seção "Notas de Decisão", no bloco sobre Manifest (~linhas 1864-1872), adicione uma nota:

> O catálogo de memória endereçável estende o conceito de manifest com campos `kind`, `preview` e `fetch`. Enquanto o manifest descreve O QUE foi usado na decisão, o catálogo descreve O QUE está disponível para recuperação futura.

---

## ÁREA 3: Head-Tail Context Truncation

### Arquivo: `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md`

**3a.** Na seção `## Requisitos` (~linhas 38-59), APÓS os requisitos existentes, adicione:

Título: `### Requisitos Adicionais — Variante Head-Tail`

Sub-blocos:
- **Funcional:** preservar system prompt intacto; head (N mensagens iniciais) e tail (M finais) no contexto ativo; middle removido mas armazenado com IDs
- **Técnico:** cada mensagem do middle com `id`, `role`, `preview` (80 chars), `full_text`; contexto final = `[system_prompt] + [head] + [tail] + [latest_result]`; função `fetch_omitted(id)`
- **Validação:** contexto ativo contém system prompt + primeiro/last turno + resultado; middle ausente mas recuperável; follow-up ao middle respondido corretamente após fetch

**3b.** Na seção `## Starter Code` (~linhas 62-188), ADICIONE os dataclasses:

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

**3c.** Na seção `## TESTS / EXEMPLOS` (~linhas 190-321), ADICIONE 3 novos testes:

```python
def test_head_tail_preserves_anchors():
    """System prompt, primeira e última mensagens estão no contexto ativo."""
    ...

def test_middle_is_recoverable():
    """Mensagem do middle pode ser recuperada por fetch_omitted(id)."""
    ...

def test_followup_after_truncation():
    """Follow-up que referencia middle ainda é respondido corretamente após fetch."""
    ...
```

Use o mesmo estilo dos testes existentes (funções com docstring + asserts).

### Arquivo: `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md`

**3d.** Na seção "O Que Você Vai Aprender" (~linhas 113-125), adicione um bullet:
- "A variante head-tail com middle recuperável: preserve âncoras e externalize o meio com recuperação exata."

**3e.** Após a Parte 1 / antes da aplicação prática (~linha 178), INSIRA nova subseção:

Título: `### Head-Tail com Middle Recuperável`

Explique que sliding window mantém últimas K mensagens e sumarização comprime tudo, enquanto head-tail preserva 3 âncoras: Head (início/contexto original), Tail (últimas interações/estado atual), System prompt (instruções NUNCA reduzidas). O middle vai para catálogo endereçável.

Inclua "Quando usar" (3 bullets) e "Quando NÃO usar" (3 bullets).

### Arquivo: `curriculum/05-core-concepts/01-context-management.md`

**3f.** Na seção de estratégias, APÓS "Compaction/Compression" (~linha 664), adicione sub-bloco:

Título: `#### Head-Tail Truncation (variante de Compaction)`

Explique como variante de compaction que preserva duas âncoras temporais enquanto externaliza o meio. Diferente de sliding window (descarta) e summarization (comprime sem recuperação), head-tail mantém omitido acessível via catálogo.

Inclua exemplo KODA: sessão de 2h com 40 turnos, contexto ativo mantém system prompt + turnos 1-3 (alergia) + 37-40 (frete); turnos 4-36 no catálogo.

---

## ÁREA 4: N+1 Long-Session Evals

### Arquivo: `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`

**4a.** No bloco P4: Compactação server-side (~linhas 488-506), REFORCE com:

```
**N+1 Long-Session Evals como gate de P4:**
- Fixtures de 10 turnos realistas com política de compactação aplicada
- O 11º turno testa continuidade, follow-up, ausência de alucinação
- Aprovação requer ≥95% de acerto
```

**4b.** No Playbook de Shadow Test (~linha 940, após passos existentes), ADICIONE:

```
### Shadow Test N+1 (específico para compactação)

1. **Fixture:** 10 conversas reais de KODA com 15+ turnos cada
2. **Aplicar:** Política de compactação atual (head-tail com catálogo)
3. **Testar:** Para cada conversa, 16ª pergunta dependente de contexto dos turnos 5-10
4. **Medir:** Taxa de acerto vs baseline (sem compactação)
5. **Gate:** N+1 ≥ baseline −5% → aprova; abaixo → revisa política antes de canary
```

### Arquivo: `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`

**4c.** No "Passo 4: Rode Testes de Regressão Antes do Canary" (~linhas 741-769), ADICIONE bloco:

```
**Bateria N+1 Long-Session (contexto):**
Antes do canary, rode:
1. 5 fixtures N+1 pré-gravadas (10 turnos + 11º pergunta)
2. Aplicar política de contexto atual em cada fixture
3. Comparar resposta do 11º turno com expected_output
4. Qualquer regressão → abortar rollout, revisar política de compactação
```

**4d.** Na tabela da bateria de regressão (~linhas 1083-1090), ADICIONE linha:

```
| Long-Session N+1 | 5 fixtures × 11 turnos | Degradação após compactação | Bloqueia rollout | Context & Retrieval |
```

### Arquivo: `curriculum/08-tools-templates/evaluation-rubric-template.md`

**4e.** No "Passo 8: Rodar regression set" (~linhas 812-814), ADICIONE bullet:
- "Inclua N+1 long-session fixtures: conversas 10+ turnos com compactação, 11º turno testa continuidade contextual."

---

## ÁREA 5: Late-Failure Regression Suite

### Arquivo: `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`

**5a.** Após a tabela da bateria ou antes de "Observação de 14 dias" (~linha 1110), INSIRA nova seção:

Título: `### Late-Failure Regression Suite (contexto)`

Corpo explicando que falhas tardias (turno 15+) viram casos de regressão permanente com:
1. Captura: todo incidente gera caso na suite
2. Fixture: session_fixture, next_turn, expected_behavior
3. Metadados: context_strategy, failure_class, evidence
4. Gate: suite roda ANTES de mudanças em truncation/retrieval/prompt/memória
5. Ownership: revisão mensal; casos 3 meses sem falhar podem ser arquivados

Inclua exemplo concreto de caso (formato fixture + next_turn + expected + failure).

### Arquivo: `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`

**5b.** Na governança P7 (~linhas 548-566), REFORCE:
- "Late-Failure Regression Suite como requisito: toda mudança em compactação/retrieval/memória requer suite antes do merge. Novos casos adicionados automaticamente quando incidente de contexto é resolvido."

**5c.** Na "Fase 3: Shadow test de qualidade" (~linhas 786-794), ADICIONE ao checklist:
- `[ ] Late-failure regression suite passou (0 regressões)`

### Arquivo: `curriculum/08-tools-templates/evaluation-rubric-template.md`

**5d.** No "Quality Checklist" (~linhas 859-871), ADICIONE:
- `[ ] Context degradation cases (late-failure fixtures) incluídos no regression set`

---

## VERIFICAÇÃO FINAL

Após todas as edições:
1. Rode `lsp_diagnostics` em cada arquivo alterado
2. Rode `git diff --stat` para confirmar que apenas os 8 arquivos esperados foram modificados
3. NÃO crie arquivos novos no currículo
4. NÃO modifique os canônicos em `docs/canonical/`
5. NÃO faça commit
