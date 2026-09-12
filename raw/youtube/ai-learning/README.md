# raw/youtube/ai-learning

Camada **raw** de transcripts da playlist do YouTube **AI - Learning**
(owner: Futan Bear / @Futanbear). Alimenta o modelo raw → conexões → extrato.

## Conteúdo
- `transcripts/<YYYY-MM-DD>-<title-slug>--<video_id>.txt` — 1 arquivo por vídeo,
  texto limpo (trechos unidos, sem timestamps). A data é a **data de extração**
  (America/Sao_Paulo); o `<video_id>` (11 chars) é a chave estável do diff.
- `index.json` — regenerado do disco a cada run: `id`, `url`, `file`, `chars` e,
  para os buscados sob esta pipeline, `lang`/`segments`.
- `missing.json` — vídeos sem legenda em nenhum idioma (pulados no diff diário,
  re-tentados no run semanal / sob demanda).

## Como é atualizado
Rotina diária em **GitHub Actions** (`.github/workflows/youtube-transcripts.yml`),
sem depender de máquina local ligada:

- **Enumeração:** YouTube Data API v3 (`playlistItems.list`) — oficial, paginada,
  grátis dentro da quota, sem bloqueio de IP no runner.
- **Transcript:** SerpApi (engine `youtube_video_transcript`), `en` com fallback
  para qualquer idioma disponível.
- **Diff stateless:** o repositório é a fonte de verdade — a cada run enumera a
  playlist e subtrai o que já está em `transcripts/` + `missing.json`.
- **Commit:** direto na `main` como `github-actions[bot]`, tocando só esta pasta.

### Agendamento
- Diário `30 8 * * *` UTC (05:30 SP) → busca vídeos novos.
- Domingo `30 8 * * 0` UTC → também re-tenta os `missing`.
- `workflow_dispatch` → modos `daily` / `retry-missing` / `full-rescan` / `migrate`
  e override do teto (`max_fetch`).

### Comportamento
- Teto `MAX_FETCH=25` por run; exceder → run **vermelho** (anomalia).
- 429: pacing + backoff; o que sobrar fica pro próximo run → **verde com aviso**.
- **Vermelho** (email nativo do GitHub): chave inválida (401/403), enumeração
  retornou 0 vídeos, ou diff acima do teto.

## Secrets (repo → Settings → Secrets → Actions)
- `YOUTUBE_API_KEY` — chave gratuita do Google Cloud (YouTube Data API v3).
- `SERPAPI_API_KEY` — chave da SerpApi.

## Código
Lógica em `scripts/youtube-transcripts/` (`pipeline.py` + `youtube.py` /
`serpapi.py` / `store.py` / `naming.py`). Testes em
`tests/unit/youtube_transcripts_test.py` (funções puras, sem rede):

```bash
python3 tests/unit/youtube_transcripts_test.py
```

Rodar a pipeline manualmente (as chaves só em env var — nunca commitadas):

```bash
export YOUTUBE_API_KEY=... SERPAPI_API_KEY=...
python3 scripts/youtube-transcripts/pipeline.py daily
```
