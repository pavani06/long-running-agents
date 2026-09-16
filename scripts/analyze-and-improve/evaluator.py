"""Adversarial evaluator (OpenAI) — the machine gate that replaces the operator.

Scores a generated artifact against a FIXED rubric (fidelity to source, real
evidence, non-duplication, format adherence), each 0-5. A mean below the
provisional minimum holds the artifact (quarantine). The generator is GLM and
the evaluator is OpenAI on purpose — different providers, so the judge is not
grading its own homework.

`build_messages` and `parse_evaluation` are pure and unit-tested; `run` makes
the single OpenAI call. The minimum score is provisional (final cut is #262).
"""
from __future__ import annotations

import json

from glm import GLMError
from openai_chat import chat_json

RUBRIC = {
    "fidelity": "Fidelidade à fonte: o artefato reflete a fonte sem distorção nem invenção.",
    "evidence": "Evidência real: as citações file:line existem e sustentam as afirmações.",
    "non_duplication": "Não-duplicação: não recria o que o repo já cobre.",
    "format": "Aderência ao formato: estrutura e campos corretos para o tipo de artefato.",
}
CRITERIA = tuple(RUBRIC)
SCORE_MAX = 5
# Provisional pass bar (mean over the 4 criteria, 0-5). Final cut calibrated in #262.
PROVISIONAL_MIN_MEAN = 3.0

_SYSTEM = (
    "Você é um avaliador adversarial e rigoroso de artefatos gerados por outro "
    "modelo. Pontue o artefato de 0 a 5 em cada critério da rubrica (5 = "
    "excelente, 0 = falha grave). Seja cético: penalize invenção, citação frágil "
    "e duplicação. Responda APENAS um objeto JSON válido:\n"
    '{"scores": {"fidelity": n, "evidence": n, "non_duplication": n, '
    '"format": n}, "rationale": string}\n'
    "Rubrica:\n" + "\n".join(f"- {k}: {v}" for k, v in RUBRIC.items())
)


def build_messages(artifact: dict, *, scope_note: str | None = None) -> list[dict]:
    """System (rubric) + user (the artifact to score, as JSON).

    `scope_note` narrows the rubric's frame for callers whose artifact is not
    net-new (an in-place revision restates the very section it replaces, which
    `non_duplication` would otherwise read as re-creating repo coverage). It
    scopes a criterion; it never relaxes one."""
    system = _SYSTEM if scope_note is None else f"{_SYSTEM}\nEscopo desta avaliação: {scope_note}"
    user = "ARTEFATO A AVALIAR:\n" + json.dumps(artifact, ensure_ascii=False, indent=2)
    return [{"role": "system", "content": system},
            {"role": "user", "content": user}]


def parse_evaluation(reply: dict, *, min_mean: float = PROVISIONAL_MIN_MEAN) -> dict:
    """Validate the rubric scores and compute pass/fail. Pure.

    Every criterion must be present and a number in [0, SCORE_MAX]. Returns
    {scores, mean, passed, rationale}."""
    scores = reply.get("scores")
    if not isinstance(scores, dict):
        raise GLMError("evaluation: 'scores' must be an object")
    clean: dict[str, float] = {}
    for c in CRITERIA:
        v = scores.get(c)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise GLMError(f"evaluation: score '{c}' must be a number")
        if not 0 <= v <= SCORE_MAX:
            raise GLMError(f"evaluation: score '{c}'={v} out of range 0..{SCORE_MAX}")
        clean[c] = float(v)
    mean = sum(clean.values()) / len(clean)
    return {"scores": clean, "mean": round(mean, 3),
            "passed": mean >= min_mean, "rationale": reply.get("rationale", "")}


def run(artifact: dict, api_key: str, *, min_mean: float = PROVISIONAL_MIN_MEAN,
        client=chat_json, scope_note: str | None = None) -> dict:
    """Evaluate one artifact: one OpenAI call, validated. `client` is injectable."""
    reply = client(build_messages(artifact, scope_note=scope_note), api_key)
    return parse_evaluation(reply, min_mean=min_mean)
