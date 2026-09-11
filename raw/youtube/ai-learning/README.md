# raw/youtube/ai-learning

Transcripts crus dos vídeos da playlist **AI - Learning** (owner: Futan Bear / @Futanbear).

- Fonte do transcript: **SerpApi**, engine `youtube_video_transcript` (a chave conectada no treg).
- 1 arquivo `.txt` por vídeo em `transcripts/<video_id>.txt` — texto limpo (trechos unidos, sem timestamps).
- `index.json` — id, url, idioma, nº de trechos, nº de chars por vídeo.
- `missing.json` — vídeos sem transcript ou que falharam.

## Estado atual
`transcripts/` contém **1 vídeo de amostra** (`kCc8FmEb1nY`, Karpathy — "Let's build GPT"),
extraído e validado ponta a ponta. Os demais são preenchidos rodando o script abaixo.

## Preencher o resto (rodar no WSL)
```bash
pip install requests yt-dlp
export SERPAPI_API_KEY="sua_chave_serpapi"   # a mesma conectada no treg
python3 fetch_transcripts.py
```
O script enumera todos os vídeos da playlist com `yt-dlp` (sem teto — pega os 372),
puxa cada transcript pela SerpApi e grava direto aqui. É idempotente: pula os que já existem.

Custo SerpApi: ~US$0,015/vídeo (~US$5,6 pelos 372; ~US$3 por ~200).

## Chamada de referência (mesma coisa via treg, 1 vídeo)
```
engine=youtube_video_transcript  v=<VIDEO_ID>  language_code=en
```
No treg, chamada pelo endpoint `serpapi.youtube.search.videos` forçando o `engine`
(o engine de transcript não tem endpoint nomeado próprio no catálogo, mas responde).
