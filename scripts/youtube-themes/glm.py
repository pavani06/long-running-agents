"""GLM polish for a theme label: a concise name + one-line description.

One chat call per community. Failures are non-fatal — the caller falls back to
the deterministic label_auto and the run stays green with a warning.
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


def polish_label(titles: list[str], theses: list[str], auto_label: str, api_key: str,
                 *, timeout: int = 90, max_retries: int = 2, backoff_base: float = 3.0,
                 sleep=time.sleep) -> dict | None:
    """Return {'name': str, 'description': str} or None on failure (caller falls back)."""
    sample = "\n".join(f"- {t}" for t in titles[:12])
    theses_sample = "\n".join(f"- {t}" for t in theses[:6] if t)
    system = (
        "Você nomeia temas de um corpus de vídeos sobre agentes de IA. "
        "Dado os títulos e teses de um cluster, responda APENAS um objeto JSON "
        '{"name": "<nome curto do tema, 2-5 palavras>", "description": "<1 frase>"}. '
        f"Tags dominantes do cluster (dica): {auto_label}. Sem markdown, sem cercas."
    )
    user = f"Títulos:\n{sample}\n\nTeses:\n{theses_sample}"
    payload = {"model": MODEL, "temperature": 0.3, "stream": False,
               "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    url = f"{BASE_URL}/chat/completions"
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(url, headers={"Authorization": f"Bearer {api_key}",
                                            "Content-Type": "application/json"},
                              json=payload, timeout=timeout)
        except requests.RequestException:
            r = None
        if r is not None:
            if r.status_code in (401, 403):
                raise AuthError(f"GLM HTTP {r.status_code} (invalid/revoked key)")
            if r.status_code == 200:
                parsed = _parse(r.json())
                if parsed:
                    return parsed
        if attempt < max_retries:
            sleep(backoff_base * (2 ** attempt))
    return None


def _parse(body: dict) -> dict | None:
    try:
        content = body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return None
    if content.startswith("```"):
        content = re.sub(r"^```[a-zA-Z]*\n?", "", content).rstrip("`").strip()
    start, end = content.find("{"), content.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        obj = json.loads(content[start:end + 1])
    except json.JSONDecodeError:
        return None
    name = str(obj.get("name", "")).strip()
    if not name:
        return None
    return {"name": name, "description": str(obj.get("description", "")).strip()}
