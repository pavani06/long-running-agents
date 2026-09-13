"""Fase 2 — padrões: síntese sobre o output da Fase 1 (não relê o transcript).

Recebe a extração tipada da Fase 1 e devolve padrões reutilizáveis, cada um com
problema / mecanismo / trade-offs — a forma que a camada canônica do repo usa.

`build_messages` e `parse_patterns` são puros e testados.
"""
from __future__ import annotations

import json

from glm import GLMError, chat_json

PATTERN_KEYS = {"name", "problem", "mechanism", "tradeoffs"}

_SYSTEM = (
    "Você sintetiza padrões arquiteturais reutilizáveis a partir de uma extração "
    "de conhecimento já estruturada. Responda APENAS um objeto JSON válido (sem "
    'markdown) com a chave "patterns": um array de objetos '
    '{"name": string, "problem": string, "mechanism": string, "tradeoffs": string}. '
    "Cada padrão deve ser acionável e ancorado na extração fornecida — não invente "
    "padrões que a fonte não sustenta. Se a fonte não tiver padrões reutilizáveis, "
    'retorne {"patterns": []}.'
)


def build_messages(extraction: dict) -> list[dict]:
    """System + user for Fase 2. The Fase 1 extraction is passed as JSON context."""
    user = ("EXTRAÇÃO (Fase 1) — sintetize padrões a partir disto:\n"
            + json.dumps(extraction, ensure_ascii=False, indent=2))
    return [{"role": "system", "content": _SYSTEM},
            {"role": "user", "content": user}]


def parse_patterns(reply: dict) -> list[dict]:
    """Validate the reply's `patterns` array and each pattern's required fields."""
    patterns = reply.get("patterns")
    if not isinstance(patterns, list):
        raise GLMError("patterns: 'patterns' must be an array")
    for i, p in enumerate(patterns):
        if not isinstance(p, dict) or (PATTERN_KEYS - set(p)):
            raise GLMError(f"patterns[{i}] missing keys: {sorted(PATTERN_KEYS - set(p if isinstance(p, dict) else {}))}")
    return patterns


def run(extraction: dict, api_key: str, *, client=chat_json) -> list[dict]:
    """Fase 2 end to end: one GLM call, validated."""
    reply = client(build_messages(extraction), api_key)
    return parse_patterns(reply)
