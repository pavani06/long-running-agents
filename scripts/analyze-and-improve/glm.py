"""Generic GLM 5.3 chat client (zai-coding-plan, OpenAI-compatible), JSON-strict.

The judgment plane of analyze-and-improve v4 (Fases 0/1/2). One HTTP call per
phase; the model is instructed to answer a single JSON object, which
`chat_json` parses and returns. Retries 429/5xx with exponential backoff. The
JSON extraction (`extract_json`) is pure and unit-tested; the phase modules
supply the messages and validate the parsed shape.

Endpoint verified for the extract layer (2026-09-12):
`https://api.z.ai/api/coding/paas/v4/chat/completions`, model `glm-5.3`, Bearer.
"""
from __future__ import annotations

import json
import re
import time

import requests

BASE_URL = "https://api.z.ai/api/coding/paas/v4"
MODEL = "glm-5.3"


class AuthError(Exception):
    """401/403 — invalid or revoked ZAI key."""


class RateLimited(Exception):
    """429 persisted past retries."""


class GLMError(Exception):
    """The request failed, or the reply could not be parsed into JSON."""


def extract_json(content: str) -> dict:
    """Parse the model's reply into a dict — strips code fences, takes the outer
    `{...}`. Pure; the phases' parsers validate the resulting shape."""
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text).rstrip("`").strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise GLMError("no JSON object in GLM reply")
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as e:
        raise GLMError(f"unparseable JSON in GLM reply: {e}")


def content_from_sse_lines(lines) -> str:
    """Assemble the message content from OpenAI-compatible SSE `data:` lines.

    Each line is `data: {"choices":[{"delta":{"content":"..."}}]}` or `data: [DONE]`.
    Pure: malformed/keepalive lines are skipped. This is what makes streaming work —
    tokens arrive incrementally, so a long generation never trips the read timeout."""
    parts: list[str] = []
    for raw in lines:
        if not raw:
            continue
        line = raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw
        line = line.strip()
        if not line.startswith("data:"):
            continue
        data = line[len("data:"):].strip()
        if data == "[DONE]":
            break
        try:
            delta = json.loads(data)["choices"][0]["delta"].get("content")
        except (json.JSONDecodeError, KeyError, IndexError, TypeError):
            continue
        if delta:
            parts.append(delta)
    return "".join(parts)


def chat_json(messages: list[dict], api_key: str, *, model: str = MODEL,
              temperature: float = 0.2, timeout: int = 90, max_retries: int = 2,
              backoff_base: float = 4.0, sleep=time.sleep) -> dict:
    """POST a streaming chat completion and return the reply parsed as a JSON object.

    Streaming (`stream: True`) is deliberate: the read timeout then applies between
    chunks (tokens keep arriving during generation) instead of to the whole body,
    so a slow Fase-3 generation doesn't read-time-out. Raises AuthError (401/403),
    RateLimited (429 past retries), or GLMError (other HTTP failure, empty reply,
    or unparseable JSON)."""
    payload = {"model": model, "messages": messages,
               "temperature": temperature, "stream": True}
    url = f"{BASE_URL}/chat/completions"
    last = ""
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(
                url,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=timeout,
                stream=True,
            )
            if r.status_code in (401, 403):
                raise AuthError(f"GLM HTTP {r.status_code} (invalid/revoked key)")
            if r.status_code == 429:
                last = "HTTP 429"
                if attempt == max_retries:
                    raise RateLimited("GLM 429 after retries")
            elif r.status_code in (500, 502, 503, 504):
                last = f"HTTP {r.status_code}: {r.text[:200]}"     # transient — retry
            elif r.status_code != 200:
                # Other 4xx (400/404/422/…) are permanent; retrying just wastes calls.
                raise GLMError(f"GLM HTTP {r.status_code}: {r.text[:200]}")
            else:
                content = content_from_sse_lines(r.iter_lines(decode_unicode=True))
                if content.strip():
                    return extract_json(content)
                last = "empty stream response"
        except requests.RequestException as e:
            last = f"network error: {e}"
        if attempt < max_retries:
            sleep(backoff_base * (2 ** attempt))
    raise GLMError(f"GLM failed after {max_retries + 1} attempts: {last}")
