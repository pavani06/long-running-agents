---
id: docs.cross-vault-taxonomy
title: "Cross-Vault Tag Taxonomy"
type: reference
tags: [documentation, taxonomy, cross-vault]
status: stable
date: 2026-06-21
relates-to:
  - "[[system-of-record|System of Record]]"
  - "[[ecosystem-glossary|Ecosystem Glossary]]"
---

# Cross-Vault Tag Taxonomy

Mapeamento de equivalencia entre as taxonomias de tags dos 4 vaults do ecossistema.
Cada vault tem suas proprias convencoes de nomenclatura, herdadas do dominio e do
proposito do repositorio. Este documento lista os equivalentes funcionais para cada
dominio conceitual e mostra como fazer consultas cross-vault com tags como chave de
busca.

## Convencoes por Vault

| Vault | Convencao | Exemplo |
|---|---|---|
| `long-running-agents` | Tags planas em portugues, derivadas dos dominios do [[system-of-record]] | `agentes-orquestracao`, `context-engineering`, `governanca` |
| `mhc-knowledge-base` | Tags hierarquicas com namespace: `categoria/valor` | `domain/ecommerce-koda`, `artifact/intent`, `capability/checkout` |
| `raw-knowledge` | Tags planas em ingles, vocabulario aberto por topico | `ai`, `agents`, `context`, `evals`, `harness` |
| `sisyphus-runtime` | Tags planas em ingles, vocabulario fechado (runtime state) | `runtime-state`, `telemetry`, `trace` |

## Tabela de Equivalencia por Dominio

Cada linha mapeia um dominio conceitual para as tags equivalentes em cada vault.
Celulas vazias (`--`) indicam que o vault nao tem documentos naquele dominio.

### Agentes e Orquestracao

| Conceito | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Agentes e orquestracao | `agentes-orquestracao` | -- | `agents`, `agentic-ai` | -- |
| Coordenacao multi-agente | `agentes-orquestracao` | -- | `multi-agent`, `collaboration` | -- |
| Coding agentic | `agentic-coding` | -- | `coding-agents`, `coding-workflow` | -- |
| Orquestracao de pipeline | `agentes-orquestracao` | -- | `workflow`, `automation` | -- |
| Design de agentes | `agentes-orquestracao`, `arquitetura` | -- | `architecture`, `framework` | -- |
| Especificacao por contrato | `spec-driven-development` | `artifact/intent`, `artifact/expectation` | -- | -- |
| Harness / Infra de agente | `harness`, `harness-engineering` | -- | `harness`, `harness-engineering` | -- |

### E-commerce / KODA

| Conceito | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Dominio KODA | `koda` | `domain/ecommerce-koda` | -- | -- |
| Checkout / Pedidos | `koda` | `capability/checkout` | -- | -- |
| Artefatos de decisao | -- | `artifact/decision`, `artifact/evidence` | -- | -- |
| Cenarios de venda | `koda` | `artifact/context`, `artifact/brief` | -- | -- |

### Contexto e Memoria

| Conceito | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Context engineering | `context-engineering` | -- | `context`, `context-engineering` | -- |
| Context window management | `context-engineering`, `context-window` | -- | `context-management` | -- |
| Memoria / State | `memory`, `state`, `persistence` | -- | `memory`, `state` | `runtime-state` |
| Gerenciamento de contexto | `context-engineering` | -- | `context-management` | -- |
| Handoff / Continuidade | `context-engineering` | -- | -- | `session-handoff` |

### Evals e Qualidade

| Conceito | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Avaliacao / Evals | `evals` | -- | `evals`, `evaluation` | -- |
| Validacao de saida | `evals`, `validacao` | -- | `verification`, `testing` | -- |
| Qualidade de codigo | `evals` | -- | `quality`, `code-review` | -- |
| Rubricas de avaliacao | `evals` | -- | `evaluation`, `methodology` | -- |
| Testes / QA | `testes-qa` | -- | `testing`, `debugging` | -- |

### Tooling e Infraestrutura

| Conceito | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Stack e tooling | `stack-tooling` | -- | `tooling`, `tools`, `cli` | -- |
| Infraestrutura / DevOps | `stack-tooling` | -- | `infrastructure`, `ci-cd`, `docker` | -- |
| Observabilidade | `stack-tooling` | -- | `observability`, `monitoring` | `telemetry` |
| Tracing | `stack-tooling` | -- | -- | `trace` |
| Software engineering | `stack-tooling` | -- | `software-engineering`, `software-architecture` | -- |
| Runtime / Build | `stack-tooling` | `runtime/mhc-backend` | `release`, `sdk` | -- |

### Governanca

| Conceito | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Governanca de repositorio | `governanca` | `artifact/system-of-record` | `governance` | `system-of-record` |
| Decisoes arquiteturais | `decision-discipline`, `adr-arquitetural` | `artifact/decision` | -- | -- |
| Compliance e seguranca | `governanca` | `concern/safety`, `concern/privacy` | `compliance`, `safety`, `security` | -- |
| Risk management | `governanca` | -- | `risk-management` | -- |
| Revisao / Gate de qualidade | `governanca`, `evals` | -- | `code-review`, `verification` | -- |

### Documentacao

| Conceito | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Documentacao de referencia | `reference` | `artifact/index`, `artifact/system-of-record` | `documentation` | `system-of-record` |
| Indices / MOCs | `index` | `artifact/index` | `moc` | -- |
| Canonical docs | `reference` | -- | -- | -- |
| Glossarios | `reference` | -- | `terminology` | -- |

## Tags Estruturais (independentes de dominio)

Tags que descrevem o papel do documento, nao o conteudo. Equivalentes aproximados:

| Funcao | long-running-agents | mhc-knowledge-base | raw-knowledge | sisyphus-runtime |
|---|---|---|---|---|
| Indice / Catalogo | `index` | `artifact/index` | `moc` | -- |
| Referencia | `reference` | `artifact/system-of-record` | `documentation` | `system-of-record` |
| Status de processamento | `status/stable` (frontmatter) | `status: draft\|active\|deprecated` (frontmatter) | `status: unprocessed\|processed` (frontmatter) | -- |
| Em construcao | -- | -- | `clippings` (placeholder) | -- |
| Conteudo didatico | `curriculo-conteudo` | -- | `beginner`, `fundamentals` | -- |
| Diagnostico / Analise | `diagnostico` | -- | `analysis` | -- |

## Como Usar

### Buscar por dominio conceitual em todos os vaults

Para encontrar documentos sobre um tema (ex: "evals"), use a tabela de equivalencia
para identificar as tags em cada vault e rode queries separadas:

```bash
# 1. long-running-agents: tags planas
obsidian-eval /mnt/c/Users/pavan/long-running-agents query \
  "filter(n => n.frontmatter.tags.includes('evals'))"

# 2. mhc-knowledge-base: tags hierarquicas (nao tem dominio de evals)
#    Nao aplicavel — sem equivalente direto.

# 3. raw-knowledge: vocabulario ingles
obsidian-eval /mnt/c/Users/pavan/raw-knowledge query \
  "filter(n => n.frontmatter.tags.includes('evals'))" && \
obsidian-eval /mnt/c/Users/pavan/raw-knowledge query \
  "filter(n => n.frontmatter.tags.includes('evaluation'))"

# 4. sisyphus-runtime: sem documentos de evals
#    Nao aplicavel.
```

### Buscar por tipo de artefato (intents, decisoes) no mhc-knowledge-base

```bash
# Todos os intents do dominio KODA
obsidian-eval /mnt/c/Users/pavan/mhc-knowledge-base query \
  "filter(n => n.frontmatter.tags.includes('artifact/intent'))"

# Todas as decisoes arquiteturais
obsidian-eval /mnt/c/Users/pavan/mhc-knowledge-base query \
  "filter(n => n.frontmatter.tags.includes('artifact/decision'))"
```

### Buscar fontes nao processadas no raw-knowledge

```bash
# Fontes com placeholder clippings (ainda nao indexadas)
obsidian-eval /mnt/c/Users/pavan/raw-knowledge query \
  "filter(n => n.frontmatter.tags.includes('clippings'))"
```

### Buscar estado de runtime no sisyphus-runtime

```bash
# Documentos de estado corrente
obsidian-eval ~/sisyphus-runtime query \
  "filter(n => n.frontmatter.tags.includes('runtime-state'))"

# Traces de sessoes anteriores
obsidian-eval ~/sisyphus-runtime query \
  "filter(n => n.frontmatter.tags.includes('trace'))"
```

### Consulta combinada cross-vault (script helper)

```bash
# Funcao bash para buscar em todos os vaults por conceito
cross-vault-search() {
  local concept="$1"
  echo "=== long-running-agents ==="
  obsidian-eval /mnt/c/Users/pavan/long-running-agents query \
    "filter(n => n.frontmatter.tags.includes('$concept'))" --json | \
    jq -r '.[].path' 2>/dev/null
  echo "=== mhc-knowledge-base ==="
  obsidian-eval /mnt/c/Users/pavan/mhc-knowledge-base query \
    "filter(n => n.frontmatter.tags.includes('$concept'))" --json | \
    jq -r '.[].path' 2>/dev/null
  echo "=== raw-knowledge ==="
  obsidian-eval /mnt/c/Users/pavan/raw-knowledge query \
    "filter(n => n.frontmatter.tags.includes('$concept'))" --json | \
    jq -r '.[].path' 2>/dev/null
  echo "=== sisyphus-runtime ==="
  obsidian-eval ~/sisyphus-runtime query \
    "filter(n => n.frontmatter.tags.includes('$concept'))" --json | \
    jq -r '.[].path' 2>/dev/null
}

# Uso: buscar documentos sobre "evals" em todo o ecossistema
cross-vault-search "evals"
```

## Notas sobre Discrepancias

**long-running-agents vs raw-knowledge (idioma).** As tags do `long-running-agents`
usam portugues para dominios canonizados no system-of-record (`agentes-orquestracao`,
`governanca`, `curriculo-conteudo`) e ingles para subtopicos tecnicos
(`context-engineering`, `evals`, `harness`). O `raw-knowledge` usa ingles
exclusivamente. A equivalencia nao e 1:1 — um conceito em portugues pode mapear
para 2-3 tags em ingles.

**mhc-knowledge-base (hierarquico).** Tags com `categoria/valor` sao semanticamente
diferentes de tags planas. `domain/ecommerce-koda` nao equivale a `ecommerce-koda` —
o namespace `domain/` classifica o tipo de relacao do documento com o topico, nao
apenas o topico em si. Ao cruzar com tags planas de outros vaults, ignore o prefixo
de namespace para o proposito de equivalencia tematica.

**sisyphus-runtime (vocabulario fechado).** As tags do vault de runtime sao
intencionalmente minimas. So existem tags para `runtime-state`, `system-of-record`,
`trace` e `telemetry`. A maioria dos dominios conceituais (agentes, KODA, evals)
nao tem representacao em tags neste vault — o estado relevante esta no corpo dos
documentos (handoffs, fatos, traces) e nao no sistema de tags.
