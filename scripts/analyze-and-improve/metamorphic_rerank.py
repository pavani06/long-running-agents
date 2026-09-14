"""Stage-2 reranker — an OpenAI judge for concept identity (#288, condition (c)).

The reranker runs on OpenAI on purpose: a DIFFERENT provider from the GLM that
generates the analysis and classifies verdicts, so the measurement instrument is
not the thing being measured. It answers, for a (variant, concept) pair, whether
they name the same underlying concept plus a granularity relation.

An LLM judge placed inside the measurement instrument is untrustworthy until
validated, so this module also ships its own sanity mini-eval: a small set of
known same/different pairs the reranker must classify correctly before its
verdicts on the real cases are believed.

`build_messages`, `parse_rerank`, `score_sanity` and `attach_stage1` are pure and
unit-tested; `rerank_pair` / `rerank_candidates` / `run_sanity` make the network
calls (OpenAI), exercised only in the Actions job that holds the key.
"""
from __future__ import annotations

import json

from glm import GLMError
from metamorphic_canon import GRANULARITY
from openai_chat import chat_json

_SYSTEM = (
    "Você é um juiz semântico rigoroso. Recebe DUAS descrições técnicas curtas e "
    "decide se elas se referem ao MESMO conceito subjacente (mesmo mecanismo/ideia), "
    "apesar de nome, granularidade ou redação diferentes. Uma formulação mais ampla "
    "ou mais restrita do mesmo mecanismo AINDA é o mesmo conceito. Descrições "
    "meramente relacionadas (mesmo domínio, mecanismo diferente) NÃO são o mesmo "
    "conceito. Seja cético: na dúvida entre 'mesmo' e 'relacionado-mas-distinto', "
    "escolha 'related_but_distinct'. Responda APENAS um objeto JSON válido:\n"
    '{"same_concept": bool, "confidence": number entre 0 e 1, '
    '"granularity_relation": um de '
    '["equivalent","broader_than","narrower_than","related_but_distinct","unrelated"]}\n'
    "granularity_relation descreve A em relação a B: equivalent (mesma amplitude), "
    "broader_than (A engloba B), narrower_than (A é um caso de B), "
    "related_but_distinct (relacionados, conceitos diferentes), unrelated."
)


def build_messages(text_a: str, text_b: str) -> list[dict]:
    """System (the identity rubric) + user (the two descriptions). Pure."""
    user = ("DESCRIÇÃO A:\n" + (text_a or "").strip()
            + "\n\nDESCRIÇÃO B:\n" + (text_b or "").strip())
    return [{"role": "system", "content": _SYSTEM},
            {"role": "user", "content": user}]


def parse_rerank(reply: dict) -> dict:
    """Validate the reranker's JSON shape. Pure.

    Returns {same_concept, confidence, granularity_relation}. Raises GLMError on a
    missing/ill-typed field or an out-of-range confidence, so a malformed judge
    reply is a hard error rather than a silently-wrong measurement."""
    same = reply.get("same_concept")
    if not isinstance(same, bool):
        raise GLMError("rerank: 'same_concept' must be a bool")
    conf = reply.get("confidence")
    if not isinstance(conf, (int, float)) or isinstance(conf, bool) or not 0 <= conf <= 1:
        raise GLMError("rerank: 'confidence' must be a number in [0, 1]")
    gran = reply.get("granularity_relation")
    if gran not in GRANULARITY:
        raise GLMError(f"rerank: 'granularity_relation' {gran!r} not in {sorted(GRANULARITY)}")
    return {"same_concept": same, "confidence": float(conf), "granularity_relation": gran}


def concept_description(concept: dict) -> str:
    """The concept side of a rerank pair: definition + its aliases. Pure."""
    aliases = ", ".join(concept.get("aliases", []) or [])
    desc = (concept.get("canonical_definition", "") or "").strip()
    return desc + (f"\n(Também chamado: {aliases}.)" if aliases else "")


def rerank_pair(text_a: str, text_b: str, api_key: str, *, client=chat_json) -> dict:
    """One reranker call over two texts (network). `client` is injectable."""
    return parse_rerank(client(build_messages(text_a, text_b), api_key))


def rerank_candidates(variant: str, candidates: list[dict], concept_by_id: dict,
                      api_key: str, *, client=chat_json) -> list[dict]:
    """Rerank a variant against each stage-1 candidate concept (network).

    `candidates` are the {concept_id, score} from stage-1. Returns each augmented
    with the reranker's verdict + the stage-1 score, ready for `decide_match`."""
    out: list[dict] = []
    for cand in candidates:
        concept = concept_by_id.get(cand["concept_id"])
        if not concept:
            continue
        verdict = rerank_pair(variant, concept_description(concept), api_key, client=client)
        out.append({"concept_id": cand["concept_id"], "stage1_score": cand.get("score"),
                    **verdict})
    return out


def score_sanity(pairs: list[dict], predictions: list[bool], *, min_accuracy: float = 0.8) -> dict:
    """Accuracy of the reranker on the known same/different sanity pairs. Pure.

    `pairs` are {a, b, same}; `predictions[i]` is the reranker's same_concept for
    pairs[i]. Returns {accuracy, correct, total, passed, mistakes[]}."""
    total = len(pairs)
    mistakes, correct = [], 0
    for p, pred in zip(pairs, predictions):
        if bool(pred) == bool(p.get("same")):
            correct += 1
        else:
            mistakes.append({"a": p.get("a"), "b": p.get("b"),
                             "expected": bool(p.get("same")), "got": bool(pred)})
    acc = (correct / total) if total else 0.0
    return {"accuracy": round(acc, 3), "correct": correct, "total": total,
            "passed": total > 0 and acc >= min_accuracy, "mistakes": mistakes}


def run_sanity(pairs: list[dict], api_key: str, *, client=chat_json,
               min_accuracy: float = 0.8) -> dict:
    """Run the sanity mini-eval (network) and score it. Condition (c) guard."""
    preds = [rerank_pair(p["a"], p["b"], api_key, client=client)["same_concept"] for p in pairs]
    return score_sanity(pairs, preds, min_accuracy=min_accuracy)
