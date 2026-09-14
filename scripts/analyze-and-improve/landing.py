"""Landing library — builds the PR body and the quarantine-Issue digest.

This is the LIBRARY, not the workflow: it constructs the text and carries the
`auto_merge` flag + `dry_run` switch, but never calls `gh` or pushes. The real
Actions wiring (open PR, auto-merge, update the rolling Issue) is #266. Pure and
unit-tested — the `auto_merge` freio (require-approval) is usable from day 1.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LandingPlan:
    """How a run should land. `auto_merge=False` is the require-approval brake."""
    auto_merge: bool = False
    dry_run: bool = True

    def describe(self) -> str:
        merge = "auto-merge ON" if self.auto_merge else "auto-merge OFF (require approval)"
        return f"{'DRY-RUN — ' if self.dry_run else ''}{merge}"


def _verdict_counts(classifications: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for c in classifications or []:
        counts[c.get("verdict", "?")] = counts.get(c.get("verdict", "?"), 0) + 1
    return counts


# Coverage verdicts: the ones that assert the concept is already present in the repo.
# `Exists` = "já coberto"; `Better` = "a fonte melhora o que existe" (so it exists to be
# improved). This matches the canon's own existence grouping (metamorphic_canon groups
# `("Exists", "Better")`). `Partial` ("existe parcialmente") and `Missing` are gaps.
COVERAGE_VERDICTS = {"Exists", "Better"}


def is_documentation_covered(classification: dict) -> bool:
    """The ONE documentation-coverage consumer guard (#288). POSITIVE-EVIDENCE.

    A documentation-coverage consumer asks: does this classification establish that
    the concept is DOCUMENTED, so a documentation gap can be suppressed? Coverage is
    granted ONLY on positive evidence — BOTH must hold:

    1. the verdict is a coverage verdict (`Exists`/`Better`); `Missing` and `Partial`
       are never coverage → they remain gaps; AND
    2. there is **at least one verified doc grounding** (`grounding["doc"] >= 1`).

    Everything else fails to cover: code-only, other-only, and zero-grounding verdicts
    all leave the documentation gap standing. Documentation coverage requires
    documentation evidence — implementation (code) or non-doc (other) evidence, however
    strong, does not substitute for it, and an unverified/empty verdict proves nothing.

    Derived-only — reads `verdict` and the derived `grounding` counts, mutates nothing.
    (`code_only_grounded` stays as observational metadata; the guard no longer keys on
    it.) Single current consumer; no generalized policy engine, no reverse-direction rule.
    """
    if classification.get("verdict", "?") not in COVERAGE_VERDICTS:
        return False
    grounding = classification.get("grounding") or {}
    return (grounding.get("doc") or 0) >= 1


def documentation_gaps(classifications: list[dict]) -> list[dict]:
    """Coverage-claiming verdicts (`Exists`/`Better`) that the guard refuses to treat as
    documented — no verified doc grounding (code-only, other-only, or zero grounding).
    A bare `Exists`/`Better` would otherwise have suppressed these documentation gaps.
    (`Partial`/`Missing` are gaps too, but visibly so in the verdict counts, and never
    claimed full coverage, so they are not re-listed here.)"""
    return [c for c in classifications or []
            if c.get("verdict", "?") in COVERAGE_VERDICTS and not is_documentation_covered(c)]


def pr_title(slug: str) -> str:
    return f"analyze-and-improve: {slug}"


def pr_body(summary: dict) -> str:
    """PR body for one run. `summary` = {slug, accepted, reasons[], classifications[],
    evaluation{mean,passed}, dedup{duplicate,score}, plan: LandingPlan}."""
    slug = summary.get("slug", "?")
    counts = _verdict_counts(summary.get("classifications", []))
    ev = summary.get("evaluation", {}) or {}
    dd = summary.get("dedup", {}) or {}
    plan = summary.get("plan")
    lines = [
        f"## analyze-and-improve — `{slug}`", "",
        f"**Destino:** {'✅ aceito' if summary.get('accepted') else '⚠️ quarentena (proposed/)'}",
        f"**Landing:** {plan.describe() if isinstance(plan, LandingPlan) else 'n/a'}", "",
        "### Classificação",
        (", ".join(f"{v}: {n}" for v, n in sorted(counts.items())) or "_(nenhuma)_"), "",
        "### Gates",
        f"- Evaluator adversarial: mean {ev.get('mean', 'n/a')} — "
        f"{'passou' if ev.get('passed') else 'reprovou'}",
        f"- Dedup por cosseno: score {dd.get('score', 'n/a')} — "
        f"{'DUPLICADO' if dd.get('duplicate') else 'ok'}",
    ]
    gaps = documentation_gaps(summary.get("classifications", []))
    if gaps:
        lines += ["", "### Lacuna de documentação (não suprimida por evidência só-de-código)",
                  "_Estes vereditos de existência foram fundamentados apenas em código verificado "
                  "(code>0, doc=0); a documentação continua ausente — a lacuna NÃO é suprimida._"]
        for c in gaps:
            g = c.get("grounding", {}) or {}
            lines.append(f"- `{c.get('pattern','?')}` — {c.get('verdict','?')} "
                         f"(code {g.get('code', 0)} / doc {g.get('doc', 0)})")
    if not summary.get("accepted"):
        lines += ["", "### Motivos da quarentena"] + [f"- {r}" for r in summary.get("reasons", [])]
    return "\n".join(lines)


def quarantine_digest(held: list[dict]) -> str:
    """Rolling quarantine-Issue body: each held artifact + why + link. `held` =
    [{slug, reasons[], link?}]."""
    lines = ["# Analyze-and-improve — quarantine digest", "",
             f"{len(held)} artefato(s) segurado(s).", ""]
    if not held:
        lines.append("_(nada em quarentena)_")
    for h in held:
        link = f" — {h['link']}" if h.get("link") else ""
        lines.append(f"## `{h.get('slug', '?')}`{link}")
        lines += [f"- {r}" for r in h.get("reasons", [])] or ["- (sem motivo registrado)"]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
