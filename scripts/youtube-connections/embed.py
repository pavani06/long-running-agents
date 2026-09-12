"""OpenAI embeddings (text-embedding-3-large), batched.

Verified 2026-09-12: /v1/embeddings returns 3072-dim vectors; batching multiple
inputs in one request works. Re-embeds the whole corpus each run (cheap: ~1-2
cents; a few batched requests) — no cache, keeping the job stateless.
"""
from __future__ import annotations

import time

import requests

URL = "https://api.openai.com/v1/embeddings"
MODEL = "text-embedding-3-large"
BATCH = 100


class AuthError(Exception):
    """401/403 — invalid or revoked OpenAI key."""


class EmbedError(Exception):
    """Embeddings request failed after retries."""


def embed_texts(texts: list[str], api_key: str, *, timeout: int = 120,
                max_retries: int = 3, backoff_base: float = 3.0, sleep=time.sleep) -> list[list[float]]:
    """Return one vector per input text, preserving order. Batches internally."""
    vectors: list[list[float]] = []
    for start in range(0, len(texts), BATCH):
        chunk = texts[start:start + BATCH]
        vectors.extend(_embed_chunk(chunk, api_key, timeout, max_retries, backoff_base, sleep))
    return vectors


def _embed_chunk(chunk, api_key, timeout, max_retries, backoff_base, sleep):
    last = ""
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(
                URL,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": MODEL, "input": chunk},
                timeout=timeout,
            )
        except requests.RequestException as e:
            last = f"network error: {e}"
        else:
            if r.status_code in (401, 403):
                raise AuthError(f"OpenAI HTTP {r.status_code} (invalid/revoked key)")
            if r.status_code == 200:
                data = sorted(r.json()["data"], key=lambda d: d["index"])
                return [d["embedding"] for d in data]
            last = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code not in (429, 500, 502, 503, 504):
                raise EmbedError(f"OpenAI embeddings {last}")
        if attempt < max_retries:
            sleep(backoff_base * (2 ** attempt))
    raise EmbedError(f"OpenAI embeddings failed after {max_retries + 1} attempts: {last}")
