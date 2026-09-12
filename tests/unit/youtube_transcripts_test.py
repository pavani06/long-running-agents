#!/usr/bin/env python3
"""Unit tests for the youtube-transcripts pipeline's pure logic.

Dependency-free: run with `python tests/unit/youtube_transcripts_test.py`
(or via pytest). No network, no secrets.
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "youtube-transcripts"))

from naming import build_filename, parse_video_id, slugify  # noqa: E402
from store import Corpus  # noqa: E402


def test_slugify_basic():
    assert slugify("Let's build GPT: from scratch") == "let-s-build-gpt-from-scratch"


def test_slugify_unicode_and_symbols():
    assert slugify("Café — AI's biggest problem!?") == "cafe-ai-s-biggest-problem"


def test_slugify_degenerate_titles():
    assert slugify("") == "untitled"
    assert slugify("日本語") == "untitled"
    assert slugify("---") == "untitled"


def test_slugify_length_cap():
    assert len(slugify("word " * 50)) <= 80


def test_build_filename():
    fn = build_filename("2026-09-12", "Let's build GPT", "kCc8FmEb1nY")
    assert fn == "2026-09-12-let-s-build-gpt--kCc8FmEb1nY.txt"


def test_build_filename_rejects_bad_id():
    try:
        build_filename("2026-09-12", "x", "short")
    except ValueError:
        return
    raise AssertionError("expected ValueError for invalid id")


def test_parse_new_scheme():
    assert parse_video_id("2026-09-12-let-s-build-gpt--kCc8FmEb1nY.txt") == "kCc8FmEb1nY"


def test_parse_legacy_scheme():
    assert parse_video_id("kCc8FmEb1nY.txt") == "kCc8FmEb1nY"


def test_parse_id_with_internal_dashes():
    # Real ids contain single dashes/underscores; the tail is still 11 chars.
    assert parse_video_id("2026-09-11-some-talk--Uvl-tRga98g.txt") == "Uvl-tRga98g"
    assert parse_video_id("-ubIUNA-zRA.txt") == "-ubIUNA-zRA"


def test_parse_rejects_non_transcript():
    assert parse_video_id("index.json") is None


def test_roundtrip():
    for vid, title in [("kCc8FmEb1nY", "Hello World"), ("Uvl-tRga98g", "Dashes - and : symbols")]:
        fn = build_filename("2026-09-11", title, vid)
        assert parse_video_id(fn) == vid


def test_store_scan_and_rename(tmp=None):
    with tempfile.TemporaryDirectory() as d:
        data = Path(d)
        (data / "transcripts").mkdir()
        # one legacy file, one already-migrated file
        (data / "transcripts" / "kCc8FmEb1nY.txt").write_text("legacy body", encoding="utf-8")
        (data / "transcripts" / "2026-09-11-already--Uvl-tRga98g.txt").write_text("new body", encoding="utf-8")
        corpus = Corpus(data)

        scanned = corpus.scan_disk()
        assert scanned["kCc8FmEb1nY"] == "kCc8FmEb1nY.txt"
        assert scanned["Uvl-tRga98g"] == "2026-09-11-already--Uvl-tRga98g.txt"

        renamed = corpus.rename_legacy({"kCc8FmEb1nY": "Lets build GPT"}, "2026-09-11")
        assert renamed == [("kCc8FmEb1nY.txt", "2026-09-11-lets-build-gpt--kCc8FmEb1nY.txt")]
        # migrated file untouched
        assert (data / "transcripts" / "2026-09-11-already--Uvl-tRga98g.txt").exists()

        n = corpus.regenerate_index()
        assert n == 2
        assert corpus.index_path.exists()


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
