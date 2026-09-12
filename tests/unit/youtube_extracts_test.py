#!/usr/bin/env python3
"""Unit tests for the youtube-extracts pipeline's pure logic.

Dependency-free: run with `python tests/unit/youtube_extracts_test.py` (or pytest).
No network, no secrets.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# Only this package's dir — it has no cross-package imports (the pipeline loads
# the transcripts enumerator by file path). Run this test file on its own.
sys.path.insert(0, str(ROOT / "scripts" / "youtube-extracts"))

import glm  # noqa: E402
from glm import ExtractError, _extract_json, _parse_reply  # noqa: E402
from naming import extract_name_for, title_from_transcript_name, video_id_from  # noqa: E402
from render import VideoMeta, build_note, normalize_extract  # noqa: E402
from store import ExtractStore  # noqa: E402
from taxonomy import build_vocabulary  # noqa: E402

VOCAB = ["evals", "harness-engineering", "context-engineering"]

SAMPLE = {
    "thesis": "Context engineering is the bottleneck.",
    "concepts": ["harness", "generator-evaluator"],
    "tools": ["Claude"],
    "people": ["Anthropic"],
    "claims": ["Budget your context window."],
    "tags": ["evals", "not-a-real-tag", "harness-engineering"],
    "deep_dive": "medium",
    "deep_dive_reason": "Solid architectural insight.",
}


# ── naming ──────────────────────────────────────────────────────────────
def test_video_id_from_new_scheme():
    assert video_id_from("2026-09-11-lets-build-gpt--kCc8FmEb1nY.md") == "kCc8FmEb1nY"
    assert video_id_from("2026-09-11-lets-build-gpt--kCc8FmEb1nY.txt") == "kCc8FmEb1nY"


def test_video_id_from_double_dash_id():
    assert video_id_from("2026-09-11-x--BrpB-h1e--k.md") == "BrpB-h1e--k"


def test_extract_name_for():
    assert extract_name_for("2026-09-11-lets-build-gpt--kCc8FmEb1nY.txt") == \
        "2026-09-11-lets-build-gpt--kCc8FmEb1nY.md"


def test_fallback_title():
    assert title_from_transcript_name("2026-09-11-lets-build-gpt--kCc8FmEb1nY.txt") == "Lets Build Gpt"


# ── render ──────────────────────────────────────────────────────────────
def test_normalize_drops_offvocab_tags():
    e = normalize_extract(SAMPLE, VOCAB)
    assert e["tags"] == ["evals", "harness-engineering"]  # 'not-a-real-tag' dropped


def test_normalize_coerces_lists():
    e = normalize_extract({"concepts": "notalist", "tags": []}, VOCAB)
    assert e["concepts"] == []


def test_build_note_frontmatter_is_valid():
    meta = VideoMeta("Let's build: GPT \"live\"", "kCc8FmEb1nY",
                     "https://www.youtube.com/watch?v=kCc8FmEb1nY", "Karpathy",
                     "2026-09-11-lets-build-gpt--kCc8FmEb1nY.txt", "2026-09-12")
    note = build_note(meta, SAMPLE, VOCAB, 1, "glm-5.3")
    # Frontmatter block: every "key: value" value must be valid JSON (=> valid YAML flow).
    fm = note.split("---")[1]
    for line in fm.strip().splitlines():
        key, _, value = line.partition(": ")
        json.loads(value)  # raises if a value is malformed
    assert '# Let\'s build: GPT "live"' in note
    assert "deep_dive" in fm and "medium" in fm
    assert "not-a-real-tag" not in note


# ── glm parsing ─────────────────────────────────────────────────────────
def test_extract_json_plain():
    assert _extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_fenced():
    assert _extract_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_extract_json_with_prose_around():
    assert _extract_json('Here you go:\n{"a": 1}\nDone.') == {"a": 1}


def test_extract_json_invalid_raises():
    try:
        _extract_json("no json here")
    except ExtractError:
        return
    raise AssertionError("expected ExtractError")


def test_parse_reply_missing_keys():
    body = {"choices": [{"message": {"content": '{"thesis": "x"}'}}]}
    try:
        _parse_reply(body)
    except ExtractError as e:
        assert "missing keys" in str(e)
        return
    raise AssertionError("expected ExtractError for missing keys")


def test_parse_reply_full():
    body = {"choices": [{"message": {"content": json.dumps(SAMPLE)}}]}
    assert _parse_reply(body)["deep_dive"] == "medium"


# ── taxonomy ────────────────────────────────────────────────────────────
def test_build_vocabulary_reads_frontmatter_and_extends():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs" / "canonical").mkdir(parents=True)
        (root / "docs" / "canonical" / "x.md").write_text(
            '---\ntags: ["custom-domain", "evals"]\n---\n# x\n', encoding="utf-8")
        vocab = build_vocabulary(root)
        assert "custom-domain" in vocab          # picked up from frontmatter
        assert "harness-engineering" in vocab    # theme extension always present


# ── store diff ──────────────────────────────────────────────────────────
def test_store_pending_diff():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        tdir = root / "raw" / "youtube" / "ai-learning" / "transcripts"
        edir = root / "extracts" / "youtube" / "ai-learning"
        tdir.mkdir(parents=True)
        edir.mkdir(parents=True)
        (tdir / "2026-09-11-a--kCc8FmEb1nY.txt").write_text("t1", encoding="utf-8")
        (tdir / "2026-09-11-b--Uvl-tRga98g.txt").write_text("t2", encoding="utf-8")
        (edir / "2026-09-11-a--kCc8FmEb1nY.md").write_text("e1", encoding="utf-8")
        store = ExtractStore(root)
        pending = store.pending()
        assert [vid for vid, _ in pending] == ["Uvl-tRga98g"]  # only the un-extracted one
        assert len(store.pending(rebuild=True)) == 2           # rebuild = all


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
