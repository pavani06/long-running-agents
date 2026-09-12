#!/usr/bin/env python3
"""Unit tests for the x-extracts pipeline's pure logic.

Dependency-free (requests only, no network/secrets): run with
`python tests/unit/x_extracts_test.py` (or pytest).
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "x-extracts"))

import glm  # noqa: E402
from glm import ExtractError, _extract_json, _parse_reply  # noqa: E402
from naming import extract_name_for, status_id_from  # noqa: E402
from render import BookmarkMeta, build_note, normalize_extract  # noqa: E402
from store import ExtractStore  # noqa: E402
from taxonomy import build_vocabulary  # noqa: E402

VOCAB = ["evals", "performance", "harness-engineering"]
SID = "1798557144580735156"

SAMPLE = {
    "topic": "Context engineering",
    "summary": "Context, not model size, is the bottleneck.",
    "tags": ["evals", "not-a-real-tag", "performance"],
    "entities": ["Anthropic"],
    "content_type": "opinion",
    "revisit": "high",
}


# ── naming ──────────────────────────────────────────────────────────────
def test_status_id_from():
    assert status_id_from(f"2026-09-12-karpathy-x--{SID}.json") == SID
    assert status_id_from(f"2026-09-12-karpathy-x--{SID}.md") == SID
    assert status_id_from("2026-09-12-x--notanumber.json") is None


def test_extract_name_for():
    assert extract_name_for(f"2026-09-12-k-x--{SID}.json") == f"2026-09-12-k-x--{SID}.md"


# ── render ──────────────────────────────────────────────────────────────
def test_normalize_drops_offvocab_tags():
    e = normalize_extract(SAMPLE, VOCAB)
    assert e["tags"] == ["evals", "performance"]  # 'not-a-real-tag' dropped


def test_normalize_defaults_bad_enums():
    e = normalize_extract({"content_type": "bogus", "revisit": "sometimes"}, VOCAB)
    assert e["content_type"] == "other" and e["revisit"] == "low"


def test_build_note_frontmatter_valid_and_links_carried():
    meta = BookmarkMeta(SID, "karpathy", f"https://x.com/karpathy/status/{SID}",
                        "2026-09-11T00:00:00Z", f"2026-09-11-karpathy-x--{SID}.json",
                        "2026-09-12", links=["https://ex.com/a"], media=[])
    note = build_note(meta, SAMPLE, VOCAB, 1, "glm-5.3")
    fm = note.split("---")[1]
    for line in fm.strip().splitlines():
        _, _, value = line.partition(": ")
        json.loads(value)  # raises if any frontmatter value is malformed
    assert "not-a-real-tag" not in note
    assert "https://ex.com/a" in note          # factual link carried through
    assert "# Context engineering" in note


# ── glm parsing ─────────────────────────────────────────────────────────
def test_extract_json_fenced_and_prose():
    assert _extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert _extract_json('here:\n{"a": 1}\ndone') == {"a": 1}


def test_parse_reply_missing_keys():
    body = {"choices": [{"message": {"content": '{"topic": "x"}'}}]}
    try:
        _parse_reply(body)
    except ExtractError as e:
        assert "missing keys" in str(e)
        return
    raise AssertionError("expected ExtractError")


def test_parse_reply_invalid_revisit():
    bad = dict(SAMPLE, revisit="whenever")
    body = {"choices": [{"message": {"content": json.dumps(bad)}}]}
    try:
        _parse_reply(body)
    except ExtractError as e:
        assert "revisit" in str(e)
        return
    raise AssertionError("expected ExtractError for bad revisit")


def test_parse_reply_full():
    body = {"choices": [{"message": {"content": json.dumps(SAMPLE)}}]}
    assert _parse_reply(body)["content_type"] == "opinion"


# ── taxonomy ────────────────────────────────────────────────────────────
def test_build_vocabulary_reads_frontmatter_and_seeds():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs" / "canonical").mkdir(parents=True)
        (root / "docs" / "canonical" / "x.md").write_text(
            '---\ntags: ["investimentos"]\n---\n', encoding="utf-8")
        vocab = build_vocabulary(root)
        assert "investimentos" in vocab   # picked up from curated frontmatter
        assert "ciclismo" in vocab        # bookmarks seed always present


# ── store diff ──────────────────────────────────────────────────────────
def test_store_pending_diff():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        idir = root / "raw" / "x" / "bookmarks" / "items"
        edir = root / "extracts" / "x" / "bookmarks"
        idir.mkdir(parents=True)
        edir.mkdir(parents=True)
        (idir / f"2026-09-12-a-x--{SID}.json").write_text('{"text":"t"}', encoding="utf-8")
        (idir / "2026-09-12-b-y--222222.json").write_text('{"text":"u"}', encoding="utf-8")
        (edir / f"2026-09-12-a-x--{SID}.md").write_text("e", encoding="utf-8")
        store = ExtractStore(root)
        assert [sid for sid, _ in store.pending()] == ["222222"]   # only un-extracted
        assert len(store.pending(rebuild=True)) == 2               # rebuild = all
        assert store.read_item("2026-09-12-b-y--222222.json")["text"] == "u"


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
