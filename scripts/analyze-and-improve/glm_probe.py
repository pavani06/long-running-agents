#!/usr/bin/env python3
"""Diagnostic probe for GLM-via-HTTP latency (#262 investigation).

The A/B run showed one full spine takes ~25 min, dominated by the GLM chat calls.
This probe isolates the endpoint: it lists the available models and times a small
and a large-output completion, reporting time-to-first-token, total time, and the
number of streamed chunks — so we can tell whether z.ai actually streams
(many chunks, low TTFT) or buffers the whole reply (one chunk, TTFT≈total), and
how latency scales with output size. Network only; run in Actions with the key.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from glm import BASE_URL, MODEL  # noqa: E402


def _summary(line: str) -> None:
    print(line)
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def list_models(api_key: str) -> list[str]:
    try:
        r = requests.get(f"{BASE_URL}/models",
                         headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
        if r.status_code == 200:
            data = r.json().get("data", r.json())
            return [m.get("id", str(m)) for m in data] if isinstance(data, list) else [str(data)]
        return [f"(models endpoint HTTP {r.status_code})"]
    except requests.RequestException as e:
        return [f"(models endpoint error: {e})"]


def probe(prompt: str, api_key: str, *, model: str = MODEL, timeout: int = 120,
          extra: dict | None = None) -> dict:
    """One streaming call, instrumented. Returns TTFT / total / chunks / chars.
    `extra` merges into the payload (to test reasoning/thinking toggles)."""
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.2, "stream": True}
    if extra:
        payload.update(extra)
    t0 = time.time()
    first = None
    chunks = 0
    chars = 0
    try:
        r = requests.post(f"{BASE_URL}/chat/completions",
                          headers={"Authorization": f"Bearer {api_key}",
                                   "Content-Type": "application/json"},
                          json=payload, timeout=timeout, stream=True)
        status = r.status_code
        if status == 200:
            for raw in r.iter_lines(decode_unicode=True):
                if not raw or not raw.startswith("data:"):
                    continue
                data = raw[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    delta = json.loads(data)["choices"][0]["delta"].get("content")
                except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                    continue
                if delta:
                    if first is None:
                        first = time.time() - t0
                    chunks += 1
                    chars += len(delta)
    except requests.RequestException as e:
        return {"model": model, "error": str(e), "total_s": round(time.time() - t0, 1)}
    return {"model": model, "status": status, "ttft_s": round(first, 1) if first else None,
            "total_s": round(time.time() - t0, 1), "chunks": chunks, "content_chars": chars}


def main() -> int:
    api_key = os.environ.get("ZAI_API_KEY")
    if not api_key:
        _summary("glm-probe: ZAI_API_KEY not set")
        return 1
    model = os.environ.get("GLM_PROBE_MODEL") or MODEL

    _summary(f"# GLM latency probe (model={model})\n")
    _summary("## Modelos disponíveis")
    for m in list_models(api_key):
        _summary(f"- {m}")

    _summary("\n## Latência por tamanho de output")
    cases = [
        ("tiny", 'Responda apenas: {"ok": true}'),
        ("small", "Liste 5 padrões de arquitetura de agentes como JSON "
                  '{"patterns": [{"name","problem"}]} — ~150 palavras.'),
        ("large", "Classifique 12 padrões de agentes contra um repo, cada um com "
                  'veredito e evidência, como JSON {"classifications": [{"pattern",'
                  '"verdict","evidence":[{"file","line","quote"}],"rationale"}]} — '
                  "seja detalhado, ~1200 palavras."),
    ]
    large_prompt = cases[-1][1]
    for label, prompt in cases:
        res = probe(prompt, api_key, model=model)
        _summary(f"- **{label}**: `{json.dumps(res, ensure_ascii=False)}`")

    # Isolate reasoning/prefill: same large-output prompt, different thinking toggles.
    # If disabling reasoning collapses TTFT, that is the latency fix for Fase 3.
    _summary("\n## Reasoning toggle no output grande (mesmo prompt)")
    variants = [
        ("baseline", {}),
        ("thinking.disabled", {"thinking": {"type": "disabled"}}),
        ("thinking.enabled", {"thinking": {"type": "enabled"}}),
        ("reasoning_effort.low", {"reasoning_effort": "low"}),
        ("reasoning_effort.minimal", {"reasoning_effort": "minimal"}),
    ]
    for label, extra in variants:
        res = probe(large_prompt, api_key, model=model, extra=extra)
        _summary(f"- **{label}**: `{json.dumps(res, ensure_ascii=False)}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
