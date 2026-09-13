"""Quarantine routing — decide whether an artifact lands or is held.

The gate report from the deterministic checks + the adversarial evaluator + the
dedup check decides the destination. What fails any gate goes to
`docs/analysis/<slug>/proposed/` and never touches the authoritative layers.
Pure and unit-tested.
"""
from __future__ import annotations

QUARANTINE_SUBDIR = "proposed"

# Each gate maps to the human-readable reason emitted when it fails.
_GATES = {
    "validate_obsidian": "validate-obsidian falhou",
    "citations_ok": "grep-verify de citações falhou",
    "not_duplicate": "duplicação por cosseno acima do limiar",
    "evaluation_passed": "evaluator adversarial abaixo do corte",
}


def decide(report: dict) -> dict:
    """{'accepted': bool, 'reasons': [str]} from a gate report.

    Accepted only when every known gate is True; a missing gate is treated as
    failed (fail-closed). `reasons` lists the gates that blocked landing."""
    reasons = [msg for key, msg in _GATES.items() if not report.get(key)]
    return {"accepted": not reasons, "reasons": reasons}


def destination_subdir(accepted: bool) -> str:
    """"" when accepted (lands in docs/analysis/<slug>/); the quarantine subdir otherwise."""
    return "" if accepted else QUARANTINE_SUBDIR


def report_from_gates(*, validate_obsidian: bool, citations_ok: bool,
                      duplicate: bool, evaluation_passed: bool) -> dict:
    """Assemble the gate report from individual gate outcomes (note the dedup
    inversion: a duplicate FAILS the not_duplicate gate)."""
    return {
        "validate_obsidian": validate_obsidian,
        "citations_ok": citations_ok,
        "not_duplicate": not duplicate,
        "evaluation_passed": evaluation_passed,
    }
