"""Split a markdown doc into sections by heading — the unit that gets embedded.

Retrieval is per-section (per the v4 design): a section is an ATX heading plus
the body until the next heading. Pure and deterministic. Fenced code blocks are
tracked so a `# comment` inside ``` ``` is never mistaken for a heading — this
matters for `.opencode/skills` docs, which are heavy with code fences.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


@dataclass(frozen=True)
class Section:
    heading: str   # heading text, or "" for the preamble before the first heading
    level: int     # 1..6, or 0 for the preamble
    text: str      # the heading line plus its body, trimmed


def strip_frontmatter(text: str) -> str:
    """Drop a leading `---` frontmatter block; return the body unchanged otherwise."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    nl = text.find("\n", end + 1)   # end of the closing `---` line
    return text[nl + 1:] if nl != -1 else ""


def split_sections(text: str) -> list[Section]:
    """Body split into sections at each ATX heading (code fences excluded)."""
    body = strip_frontmatter(text)
    sections: list[Section] = []
    cur_lines: list[str] = []
    cur_heading = ""
    cur_level = 0
    in_fence = False

    def flush() -> None:
        chunk = "\n".join(cur_lines).strip("\n")
        if chunk.strip():
            sections.append(Section(cur_heading, cur_level, chunk))

    for line in body.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            cur_lines.append(line)
            continue
        m = None if in_fence else _HEADING.match(line)
        if m:
            flush()
            cur_lines = [line]
            cur_heading = m.group(2).strip()
            cur_level = len(m.group(1))
        else:
            cur_lines.append(line)
    flush()
    return sections
