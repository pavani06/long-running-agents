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
