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
    "destination_validated": "validador de destino indisponível — conteúdo não verificado",
    "destination_valid": "convenções obsidian no destino falharam",
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


def quarantine_relpath(slug: str, intended_destination: str) -> str:
    """The quarantine copy path for an artifact: `docs/analysis/<slug>/proposed/<dest>`.

    The intended destination is mirrored verbatim under the quarantine dir, so the
    quarantined file is self-describing and promotion is a prefix-strip move. The
    copy lives under docs/analysis/ — it can never collide with (or contaminate)
    the authoritative layers. Pure."""
    return f"docs/analysis/{slug}/{QUARANTINE_SUBDIR}/{intended_destination}"


def report_from_gates(*, validate_obsidian: bool, citations_ok: bool,
                      duplicate: bool, evaluation_passed: bool,
                      destination_validated: bool = True,
                      destination_valid: bool = True) -> dict:
    """Assemble the gate report from individual gate outcomes (note the dedup
    inversion: a duplicate FAILS the not_duplicate gate).

    The destination-scoped convention check the repo-wide validator cannot run
    while the artifact is quarantined is two separate gates on purpose:
    `destination_validated` (the validator actually ran) and `destination_valid`
    (it found no violations). Both hold the artifact, but a toolchain that could
    not run must never be reported as a content violation. Both default to True
    for callers whose artifact has no authoritative destination to check."""
    return {
        "validate_obsidian": validate_obsidian,
        "destination_validated": destination_validated,
        "destination_valid": destination_valid,
        "citations_ok": citations_ok,
        "not_duplicate": not duplicate,
        "evaluation_passed": evaluation_passed,
    }
