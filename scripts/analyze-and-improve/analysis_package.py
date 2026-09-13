"""Write the partial analysis package (Fases 0/1/2) to docs/analysis/<slug>/.

Naming mirrors the historical packages: `<slug>-mental-model.{md,yaml}`,
`<slug>-analysis.{md,yaml}`, `<slug>-patterns.{md,yaml}` (classification is
Etapa 2 / #260). Thin I/O over the pure serializers.
"""
from __future__ import annotations

from pathlib import Path

import serialize


def package_dir(repo_root: Path, slug: str) -> Path:
    return repo_root / "docs" / "analysis" / slug


def write_package(repo_root: Path, slug: str, *, mental_model: dict | None = None,
                  extraction: dict | None = None, patterns: list[dict] | None = None) -> list[str]:
    """Write the phase artifacts present; return the repo-relative paths written."""
    out = package_dir(repo_root, slug)
    out.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    def _write(suffix: str, text: str) -> None:
        path = out / f"{slug}-{suffix}"
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        written.append(str(path.relative_to(repo_root)))

    if mental_model is not None:
        _write("mental-model.yaml", serialize.to_yaml(mental_model))
        _write("mental-model.md", serialize.mental_model_md(mental_model))
    if extraction is not None:
        _write("analysis.yaml", serialize.to_yaml(extraction))
        _write("analysis.md", serialize.extraction_md(extraction))
    if patterns is not None:
        _write("patterns.yaml", serialize.to_yaml({"patterns": patterns}))
        _write("patterns.md", serialize.patterns_md(patterns))
    return sorted(written)
