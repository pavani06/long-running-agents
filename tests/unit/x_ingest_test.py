#!/usr/bin/env python3
"""Unit tests for the x-ingest pipeline's pure logic (no network).

Run with `python tests/unit/x_ingest_test.py` (or pytest). `requests` is
imported by fetch.py at module top (installed); trafilatura is lazy, so these
run without it.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "x-ingest"))

# Issue #269: sibling pipelines ship same-basename modules (naming, store,
# glm, ...); in a single pytest process the first import wins in sys.modules.
# Purge pipeline-local names so the imports below resolve from this file's dir.
for _mod in ("annotate_thin", "bookmarks", "cluster", "corpus", "embed",
             "extracts_io", "fetch", "fm", "frontmatter_io", "gitio", "glm",
             "graph", "label", "moc", "naming", "oauth", "pipeline", "projects",
             "rank", "render", "serpapi", "store", "taxonomy", "thin", "youtube"):
    sys.modules.pop(_mod, None)

from fetch import classify_status, classify_url, content_hash, is_blocked_host  # noqa: E402
from naming import content_name, key_from_name, url_key  # noqa: E402
from store import IngestStore  # noqa: E402


# ── naming ──────────────────────────────────────────────────────────────
def test_url_key_stable_and_name_roundtrip():
    u = "https://www.example.com/some/article?x=1"
    k = url_key(u)
    assert len(k) == 12 and url_key(u) == k          # stable
    name = content_name(u)
    assert name == f"example-com--{k}.md"            # www stripped, domain slug + key
    assert key_from_name(name) == k                  # round-trip


def test_url_key_differs_per_url():
    assert url_key("https://a.com/x") != url_key("https://a.com/y")


# ── classify ──────────────────────────────────────────────────────────────
def test_classify_url():
    assert classify_url("https://youtu.be/abc") == "youtube"
    assert classify_url("https://www.youtube.com/watch?v=x") == "youtube"
    assert classify_url("https://site.com/paper.pdf") == "pdf"
    assert classify_url("https://arxiv.org/pdf/2401.00001") == "pdf"
    assert classify_url("https://www.vox.com/story") == "article"


def test_classify_status_by_length():
    assert classify_status("x" * 500) == "ok"
    assert classify_status("short") == "paywall"
    assert classify_status("") == "paywall"


def test_content_hash_stable():
    assert content_hash("abc") == content_hash("abc")
    assert content_hash("abc") != content_hash("abd")


def test_is_blocked_host_ssrf_guard():
    assert is_blocked_host("http://127.0.0.1/x") is True
    assert is_blocked_host("http://169.254.169.254/latest/meta-data") is True   # cloud metadata
    assert is_blocked_host("http://10.0.0.5/") is True
    assert is_blocked_host("http://localhost:8080/") is True
    assert is_blocked_host("https://www.vox.com/story") is False               # normal host allowed


# ── store diff ──────────────────────────────────────────────────────────
def _seed_item(root: Path, sid: str, links: list[str]):
    d = root / "raw" / "x" / "bookmarks" / "items"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"2026-09-13-h-x--{sid}.json").write_text(
        json.dumps({"status_id": sid, "links": links}), encoding="utf-8")


def test_collect_links_dedups_across_items():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _seed_item(root, "111", ["https://a.com/1", "https://b.com/2"])
        _seed_item(root, "222", ["https://a.com/1"])  # dup of a.com/1
        links = IngestStore(root).collect_links()
        assert links == ["https://a.com/1", "https://b.com/2"]


def test_pending_incremental_and_retry():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _seed_item(root, "111", ["https://a.com/1", "https://b.com/2"])
        store = IngestStore(root)
        # ingest a.com/1 as failed, b.com/2 as ok
        store.write_entry("https://a.com/1", {"status": "failed"}, "2026-09-13")
        store.write_entry("https://b.com/2", {"status": "ok", "text": "x" * 500,
                                              "text_len": 500}, "2026-09-13")
        links = store.collect_links()
        assert store.pending(links, mode="incremental") == []          # both present
        assert store.pending(links, mode="retry") == ["https://a.com/1"]  # the failed one
        assert set(store.pending(links, mode="full")) == set(links)     # all


def test_write_entry_and_regenerate_index():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        store = IngestStore(root)
        store.write_entry("https://a.com/x", {"status": "ok", "text": "hello world",
                          "final_url": "https://a.com/x", "method": "jina",
                          "content_hash": "abc", "text_len": 11}, "2026-09-13")
        store.write_entry("https://v.com/y", {"status": "unsupported", "method": "pdf"}, "2026-09-13")
        counts = store.regenerate_index()
        assert counts == {"ok": 1, "unsupported": 1}
        idx = json.loads(store.index_path.read_text(encoding="utf-8"))
        assert idx["count"] == 2 and idx["status_counts"] == {"ok": 1, "unsupported": 1}


def _run_all():
    fns = [g for n, g in sorted(globals().items()) if n.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
