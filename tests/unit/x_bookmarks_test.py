#!/usr/bin/env python3
"""Unit tests for the x-bookmarks pipeline's pure logic.

Dependency-free: run with `python tests/unit/x_bookmarks_test.py` (or pytest).
No network, no secrets.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "x-bookmarks"))

from naming import build_filename, clean_handle, parse_status_id, slugify  # noqa: E402
from store import Bookmark, BookmarkStore  # noqa: E402

SID = "1798557144580735156"


# ── naming ──────────────────────────────────────────────────────────────
def test_build_and_parse_roundtrip():
    fn = build_filename("2026-09-12", "@Karpathy", "Let's build GPT!", SID)
    assert fn == f"2026-09-12-karpathy-let-s-build-gpt--{SID}.json"
    assert parse_status_id(fn) == SID


def test_parse_status_id_rejects_nonnumeric():
    assert parse_status_id("2026-09-12-x-slug--kCc8FmEb1nY.json") is None


def test_build_filename_rejects_bad_id():
    try:
        build_filename("2026-09-12", "x", "y", "not-a-number")
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-numeric id")


def test_slug_and_handle_fold_ascii():
    assert slugify("Ação & Café — top!") == "acao-cafe-top"
    assert clean_handle("@José_Silva") == "jose_silva"  # underscores are valid in handles
    assert clean_handle("") == "unknown"


# ── store diff ──────────────────────────────────────────────────────────
def _bm(sid, handle="h", text="t", links=None, media=None):
    return Bookmark(sid, handle, text, "2026-09-12T00:00:00Z",
                    f"https://x.com/{handle}/status/{sid}",
                    links=links or [], media=media or [])


def test_new_bookmarks_diff_and_dedup():
    with tempfile.TemporaryDirectory() as d:
        store = BookmarkStore(Path(d))
        store.write_item("2026-09-12", _bm("111111"))
        fetched = [_bm("111111"), _bm("222222"), _bm("222222")]  # known, new, dup
        new = store.new_bookmarks(fetched)
        assert [b.status_id for b in new] == ["222222"]  # known + dup dropped


def test_write_item_and_regenerate_index():
    with tempfile.TemporaryDirectory() as d:
        store = BookmarkStore(Path(d))
        fn = store.write_item("2026-09-12", _bm(SID, handle="karpathy", text="hi"))
        assert fn.endswith(f"--{SID}.json")
        payload = json.loads((store.items_dir / fn).read_text(encoding="utf-8"))
        assert payload["status_id"] == SID and payload["collected"] == "2026-09-12"
        count = store.regenerate_index()
        assert count == 1
        idx = json.loads(store.index_path.read_text(encoding="utf-8"))
        assert idx["count"] == 1 and idx["items"][0]["status_id"] == SID


def test_write_item_persists_links_and_media():
    with tempfile.TemporaryDirectory() as d:
        store = BookmarkStore(Path(d))
        fn = store.write_item("2026-09-12", _bm(SID, links=["https://example.com/x"],
                                                media=["https://pbs.twimg.com/a.jpg"]))
        payload = json.loads((store.items_dir / fn).read_text(encoding="utf-8"))
        assert payload["links"] == ["https://example.com/x"]
        assert payload["media"] == ["https://pbs.twimg.com/a.jpg"]


def test_write_item_reprocess_preserves_name_and_date():
    with tempfile.TemporaryDirectory() as d:
        store = BookmarkStore(Path(d))
        # First write on an old date, no links (the pre-enrichment state).
        fn1 = store.write_item("2026-09-10", _bm(SID, text="hi"))
        # Reprocess on a later date with enriched content: same file, same date.
        fn2 = store.write_item("2026-09-99", _bm(SID, text="hi", links=["https://ex.com"]),
                               store.scan_disk())
        assert fn2 == fn1                                   # filename preserved
        payload = json.loads((store.items_dir / fn2).read_text(encoding="utf-8"))
        assert payload["collected"] == "2026-09-10"         # original date preserved
        assert payload["links"] == ["https://ex.com"]       # content enriched
        assert len(store.scan_disk()) == 1                  # no duplicate created


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
