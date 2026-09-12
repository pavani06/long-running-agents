# extracts/youtube/ai-learning

Camada de **extração** (Nível 1) sobre os transcripts de [`raw/youtube/ai-learning`](../../../raw/youtube/ai-learning).
Triagem + grafo implícito, **automatizada**. **Não** substitui o `analyze-and-improve`
(Nível 2, curadoria profunda manual por vídeo) — só destila um extrato leve por vídeo
e sinaliza quais valem o deep-dive.

## Conteúdo
Um `.md` por vídeo, mesmo stem do transcript (`<data>-<slug>--<video_id>.md`), com:

- **Frontmatter** (legível por máquina): `title, type:extract, video_id, url, channel,
  extracted, model, extract_version, transcript` (wikilink de volta ao raw), `tags`
  (vocabulário controlado), `thesis`, `concepts`, `tools`, `people`, `claims`,
  `deep_dive` (`high|medium|low`) + `deep_dive_reason`.
- **Corpo** (legível no Obsidian): Tese / Conceitos-chave / Ferramentas & pessoas / Claims.

## Grafo
Implícito via `tags` + `concepts` (o Obsidian indexa todo `.md` do vault). As **arestas
explícitas** entre extratos (`relates-to` cross-vídeo) são um passo futuro (`build_connections`).
Esta pasta fica **fora do escopo** do `validate-obsidian.ts` (é bulk auto-gerado).

## Como é gerado
- **Motor:** GLM 5.3 (`zai-coding-plan`, endpoint OpenAI-compat), 1 chamada por vídeo.
- **Enumeração:** YouTube Data API v3 (títulos/canais pro frontmatter).
- **Diff stateless:** `transcripts/` − `extracts/` (chave = `video_id`).
- **Workflow:** `.github/workflows/youtube-extracts.yml`, disparado por `workflow_run`
  após o de transcripts + `workflow_dispatch` (`incremental` / `full` / `rebuild`).
- **Secrets:** `ZAI_API_KEY`, `YOUTUBE_API_KEY`.

## Fluxo típico
- **Backfill (uma vez):** dispatch modo `full`.
- **Incremental:** roda sozinho após cada run diário de transcripts (cap 50).
- **Re-extração:** bump de `extract_version` no código → dispatch modo `rebuild`.

## Deep-dive
Filtre `deep_dive: high` no Obsidian pra achar os vídeos que valem rodar o
`ingest-and-improve` / `analyze-and-improve` completo.

## Código & testes
`scripts/youtube-extracts/` — `pipeline.py` + `glm.py` / `render.py` / `store.py`
/ `taxonomy.py` / `naming.py`. Testes: `tests/unit/youtube_extracts_test.py`
(funções puras, sem rede):

```bash
python3 tests/unit/youtube_extracts_test.py
```
