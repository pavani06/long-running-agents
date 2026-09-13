"""OpenAI chat client, JSON-strict — the adversarial evaluator's transport.

The evaluator is OpenAI on purpose: a different provider from the GLM generator,
so it cannot rubber-stamp its own output. Mirrors `glm.chat_json` (retry 429/5xx,
fatal 4xx, JSON reply) against the OpenAI Chat Completions endpoint. The model is
configurable via `OPENAI_EVAL_MODEL` (provisional default). Reuses `glm.extract_json`
for parsing; only the pure parser is unit-tested, never this network call.
"""
from __future__ import annotations

import os
import time

import requests

from glm import (AuthError, GLMError, RateLimited, content_from_sse_lines,
                 extract_json)

URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o"  # provisional; override with OPENAI_EVAL_MODEL


def model_from_env() -> str:
    return os.environ.get("OPENAI_EVAL_MODEL", DEFAULT_MODEL)


def chat_json(messages: list[dict], api_key: str, *, model: str | None = None,
              temperature: float = 0.0, timeout: int = 180, max_retries: int = 2,
              backoff_base: float = 3.0, sleep=time.sleep) -> dict:
    """POST an OpenAI chat completion; return the reply parsed as JSON.

    Raises AuthError (401/403), RateLimited (429 past retries) or GLMError
    (other HTTP failure, empty reply, unparseable JSON) — the same error
    contract as glm.chat_json, so callers handle one set of exceptions."""
    payload = {"model": model or model_from_env(), "messages": messages,
               "temperature": temperature,
               "response_format": {"type": "json_object"}, "stream": True}
    last = ""
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(
                URL,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=timeout,
                stream=True,
            )
            if r.status_code in (401, 403):
                raise AuthError(f"OpenAI HTTP {r.status_code} (invalid/revoked key)")
            if r.status_code == 429:
                last = "HTTP 429"
                if attempt == max_retries:
                    raise RateLimited("OpenAI 429 after retries")
            elif r.status_code in (500, 502, 503, 504):
                last = f"HTTP {r.status_code}: {r.text[:200]}"
            elif r.status_code != 200:
                raise GLMError(f"OpenAI HTTP {r.status_code}: {r.text[:200]}")
            else:
                content = content_from_sse_lines(r.iter_lines(decode_unicode=True))
                if content.strip():
                    return extract_json(content)
                last = "empty stream response"
        except requests.RequestException as e:
            last = f"network error: {e}"
        if attempt < max_retries:
            sleep(backoff_base * (2 ** attempt))
    raise GLMError(f"OpenAI chat failed after {max_retries + 1} attempts: {last}")
