---
title: "Programa: digest de bookmarks do X (ingest → extract profundo → connections → themes → digest)"
type: plan
date: 2026-09-13
aliases: ["x-bookmarks digest", "digest program", "x-digest"]
tags: ["corpus-pipelines", "agentes-orquestracao", "stack-tooling", "governanca"]
relates-to: ["[[raw/x/bookmarks/README|raw/x/bookmarks]]", "[[docs/plans/2026-09-12-x-bookmarks-pipeline|Pipeline de bookmarks do X]]", "[[docs/system-of-record|system-of-record]]"]
---

# Programa: digest de bookmarks do X

**Data:** 2026-09-13 · **Operador:** Fernando Pavani (@fepavani)
**Decidido via** sessão de grilling (`/grill-me`) sobre cada ponto do digest.

O digest é o **valor final** da rotina de bookmarks. O grilling revelou que ele é a
**ponta de um programa de 5 camadas** — porque o valor de um bookmark do X frequentemente
está no **conteúdo linkado** (artigo/thread), não no texto do tweet. Este plano é a fonte
de verdade do programa; o épico e as sub-issues do GitHub apontam pra cá.

## Arquitetura

```
raw (tweet + links)   ✓ já existe (raw/x/bookmarks/)
  1. x-ingest        NOVO   — busca+limpa o conteúdo linkado → ingest/x/ + fetch_status
  2. x-extract v2    ALTERA — extract profundo (lê o ingerido) + key_points + grounded_in; re-extrai os 299
  3. x-connections   NOVO   — espelha youtube-connections (embeddings OpenAI) → connections.json
  4. x-themes        NOVO   — espelha youtube-themes (community detection) → themes.json + MOCs
  5. x-digest        NOVO   — síntese sobre temas + connections + projects.md (bootstrap + daily)
```

## Ledger de decisões (grilling 2026-09-13)

| Tema | Decisão | Porquê |
|---|---|---|
| Bootstrap | Digest do acervo **por tema sobre os 299**, aberto com "leia nesta ordem" | Colher o acervo agora; os temas dão navegabilidade aos 299 |
| Cadência | **Diária** (degrada em dia magro; dia vazio = cabeçalho + nota) | Operador marca bastante por dia |
| Conteúdo | **Buscar o linkado** em camadas + `fetch_status` de proveniência | O valor está no link; falha vira sinal re-tentável, não silêncio |
| Arquitetura | **Camada de ingestão separada** (`raw→ingest→extract→digest`) | Idempotente, re-tentável, snapshot contra link-rot; separa ingestão de síntese |
| Fetcher | **Jina Reader** (anônimo; key só se rate) **+ trafilatura** fallback | Reader renderiza JS/soft-paywall; fallback evita dependência dura; volume baixo = grátis |
| Escopo ingest V1 | **Só artigo/link externo**; thread/YouTube/PDF = `unsupported` | Maior balde claro (~68); tipos adiados ficam flagueados/re-processáveis |
| Extract | **Profundo** + `key_points` (vazio se raso) + `grounded_in` (factual) | Capturar substância; card navegável rico e honesto |
| Cruzamento + temas | **Espelhar `x-connections` + `x-themes`** (embeddings + community) | Máquina já existe/provada no youtube; cruzamento semântico + temas de corpus estáveis |
| Ações | `projects.md` **manual, tier por nó**; semeado local dos repos; **CI só lê** | Prioridade/profundidade sem PAT amplo; manutenção assistida localmente |
| LLM | **GLM** (`glm-5.3`), mesmo dos extracts | Consistência; barato |
| Saída | `digests/x/<data>.md` (daily) + `digests/x/bootstrap/` (acervo); email adiado | Obsidian-first; email por cima depois |

## Mecanismos modernos adotados

- **Extração:** Jina Reader (`r.jina.ai`, markdown LLM-ready com JS render) + trafilatura fallback.
- **Proveniência:** `fetch_status` por link (`ok`/`paywall`/`failed`/`unsupported`) + `content_hash` + `final_url` — retry idempotente, snapshot contra link-rot.
- **Cruzamento semântico:** embeddings OpenAI (reuso do padrão `youtube-connections`).
- **Temas:** community detection (networkx) sobre o grafo de connections (reuso de `youtube-themes`).
- **Roteamento por tipo** (fast-follow): thread→Scrape Creators; YouTube→pipeline de transcript; PDF/arXiv→extração de PDF.

## Fases (sub-issues do épico)

| # | Fase | Escopo | Dep. |
|---|---|---|---|
| 0 | `projects.md` seed | Semear `digests/x/projects.md` dos repos ativos + teses, tier por nó | — |
| 1 | `x-ingest` | Jina+trafilatura+router, `ingest/x/` + `fetch_status`, naming, pipeline, workflow, testes | — |
| 2 | `x-extract v2` | Extract profundo (lê ingest) + `key_points` + `grounded_in`; re-extrai 299 | 1 |
| 3 | `x-connections` | Espelha `youtube-connections` (embeddings) → `connections.json` | 2 |
| 4 | `x-themes` | Espelha `youtube-themes` (community) → `themes.json` + MOCs | 3 |
| 5a | `x-digest` core | Síntese sobre temas+connections+projects (render + GLM) | 4 |
| 5b | `x-digest` workflow + bootstrap | Encadeia no x-extracts + dispatch; roda o bootstrap dos 299 | 5a |

## Metodologia de execução (por sub-issue)

Cada sub-issue é **auto-contida** e **loop-executável**, com corpo seguindo o template:
1. **Contexto auto-contido** (entende sem a conversa; links pros padrões a espelhar).
2. **Definition of Done** verificável (Rule 4).
3. **Escopo atômico** + o que está fora (dimensionada pra uma sessão).
4. **Dependências**.
5. **Fluxo:** `issue-start → build (TDD onde couber) → gates → issue-review → issue-finish → housekeeping`.
6. **Topologia agêntica recomendada:** solo (padrão, módulo coeso); subagentes paralelos (N arquivos independentes / review multi-dimensão); background+monitor (runs longos: re-extract, embeddings, fetches, bootstrap).

**Ritual de fim-de-fase:** ao fechar cada fase, atualizar o **épico** (check + aprendizados) e **revisitar as sub-issues restantes**, ajustando escopo/premissas com o que a fase revelou. Isso impede fases de baixo de herdarem premissas invalidadas.

## Restrições

- Rule 9: nenhum secret em código/log/fixture (chaves só em env/secret).
- Rule 2: mudança mínima; espelhar padrões existentes (`youtube-*`) antes de inventar.
- Falha explícita: `fetch_status` nunca vira silêncio; run vermelho quando a chave/enum quebra.
- Custo GLM/embeddings capado e resumível por run.

## Fora de escopo (adiado)

Email do digest; roteador de thread/YouTube/PDF na ingestão; migração do catálogo (983);
Medium/Substack. A API do X expõe só ~299 (janela recente) → backfill do histórico não rola.
