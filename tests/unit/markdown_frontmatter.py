#!/usr/bin/env python3
"""Test helper: split a generated markdown document into its parsed YAML
frontmatter and body, so tests assert on the frontmatter contract semantically
instead of grepping the rendered text."""
from __future__ import annotations

import yaml


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    """(frontmatter, body); frontmatter is None when no `---` block opens line 1."""
    lines = (text or "").split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text or ""
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            loaded = yaml.safe_load("\n".join(lines[1:i]))
            return (loaded if isinstance(loaded, dict) else {}), "\n".join(lines[i + 1:])
    return None, text
