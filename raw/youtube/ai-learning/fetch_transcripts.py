#!/usr/bin/env python3
"""
Extrai os transcripts de TODOS os vídeos da playlist "AI - Learning" via SerpApi
(engine `youtube_video_transcript`) e salva um .txt limpo por vídeo, direto nesta pasta.

Por que rodar aqui (WSL) e não no chat:
  cada transcript é 1 chamada, e o ambiente do chat só persiste em disco as respostas
  grandes (as menores voltam "inline" e não dá pra salvar em lote). Local resolve isso,
  roda em paralelo mental (sequencial mas rápido), pega os 372 sem o teto de ~200 e
  grava direto no repositório.

Como rodar:
  pip install requests yt-dlp
  export SERPAPI_API_KEY="sua_chave_serpapi"      # a mesma que você conectou no treg
  python3 fetch_transcripts.py

Saída (relativa a este arquivo):
  transcripts/<video_id>.txt   -> texto limpo (1 por vídeo)
  index.json                   -> id, url, idioma, nº de trechos, nº de chars
  missing.json                 -> vídeos sem transcript / falhas

Notas:
  - Idempotente: pula vídeos cujo .txt já existe (dá pra parar e retomar).
  - Custo SerpApi: ~US$0,015 por vídeo (~US$5,6 pelos 372 / ~US$3 por ~200).
  - yt-dlp só enumera os IDs (não precisa de chave); o transcript vem da SerpApi.
"""
import os
import sys
import json
import time
import pathlib
import subprocess

import requests

# ---- config -----------------------------------------------------------------
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLdJYvRCSB6rO2Mm_0wGnHgFfoy34OaC0S"
LANG = "en"                 # idioma preferido; se faltar, tenta o disponível
SLEEP = 0.4                 # pausa entre chamadas (respeita rate limit)
# -----------------------------------------------------------------------------

HERE = pathlib.Path(__file__).resolve().parent
TDIR = HERE / "transcripts"
KEY = os.environ.get("SERPAPI_API_KEY")


def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def playlist_ids(url: str) -> list[str]:
    """Enumera todos os IDs da playlist via yt-dlp (sem precisar de chave)."""
    try:
        out = subprocess.check_output(
            ["yt-dlp", "--flat-playlist", "--print", "%(id)s", url],
            text=True, stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        die("yt-dlp nao encontrado. Rode: pip install yt-dlp")
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def fetch_transcript(vid: str):
    """Retorna (dados, erro). dados = {text, lang, segments} ou None."""
    base = {"engine": "youtube_video_transcript", "v": vid, "api_key": KEY}

    def call(extra):
        p = {**base, **extra}
        r = requests.get("https://serpapi.com/search.json", params=p, timeout=90)
        if r.status_code != 200:
            return None, f"http {r.status_code}"
        j = r.json()
        tr = j.get("transcript")
        if isinstance(tr, list) and tr:
            return j, tr
        return j, None

    # 1) tenta com o idioma preferido
    j, tr = call({"language_code": LANG})
    if isinstance(tr, str):        # veio erro de http
        return None, tr
    # 2) se nao veio, tenta sem fixar idioma (pega o disponivel)
    if tr is None:
        j2, tr2 = call({})
        if isinstance(tr2, str):
            return None, tr2
        if tr2 is None:
            return None, "sem transcript"
        j, tr = j2, tr2

    text = "\n".join(
        seg.get("snippet", "").strip() for seg in tr if seg.get("snippet")
    )
    if not text:
        return None, "transcript vazio"
    lang = (j.get("search_parameters") or {}).get("language_code") or LANG
    return {"text": text, "lang": lang, "segments": len(tr)}, None


def main() -> None:
    if not KEY:
        die("Defina SERPAPI_API_KEY no ambiente antes de rodar.")
    TDIR.mkdir(parents=True, exist_ok=True)

    ids = playlist_ids(PLAYLIST_URL)
    print(f"{len(ids)} videos na playlist\n")

    index, missing = [], []
    for i, vid in enumerate(ids, 1):
        dest = TDIR / f"{vid}.txt"
        if dest.exists() and dest.stat().st_size > 0:
            print(f"[{i}/{len(ids)}] {vid} -- ja existe, pulando")
            index.append({"id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
                          "skipped": True})
            continue
        res, err = fetch_transcript(vid)
        if err:
            print(f"[{i}/{len(ids)}] {vid} -- FALHOU: {err}")
            missing.append({"id": vid, "reason": err,
                            "url": f"https://www.youtube.com/watch?v={vid}"})
        else:
            dest.write_text(res["text"], encoding="utf-8")
            index.append({"id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
                          "lang": res["lang"], "segments": res["segments"],
                          "chars": len(res["text"])})
            print(f"[{i}/{len(ids)}] {vid} -- ok ({len(res['text'])} chars)")
        time.sleep(SLEEP)

    (HERE / "index.json").write_text(
        json.dumps({"playlist_url": PLAYLIST_URL,
                    "source": "SerpApi youtube_video_transcript",
                    "count": len(index), "videos": index},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (HERE / "missing.json").write_text(
        json.dumps({"count": len(missing), "videos": missing},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nPronto: {len(index) - len(missing)} transcripts salvos, "
          f"{len(missing)} sem/falha.")
    print(f"Saida em: {TDIR}")


if __name__ == "__main__":
    main()
