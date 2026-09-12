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

import youtube  # noqa: E402
from naming import build_filename, parse_video_id, slugify  # noqa: E402
from store import Corpus  # noqa: E402
from youtube import EnumerationError, enumerate_playlist  # noqa: E402


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


def test_parse_id_containing_double_dash():
    # base64url ids can contain "--"; recovered via the 11-char tail.
    assert parse_video_id("BrpB-h1e--k.txt") == "BrpB-h1e--k"
    assert parse_video_id("2026-09-11-some-talk--BrpB-h1e--k.txt") == "BrpB-h1e--k"


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
        # legacy file whose id itself contains "--"
        (data / "transcripts" / "BrpB-h1e--k.txt").write_text("dash body", encoding="utf-8")
        corpus = Corpus(data)

        scanned = corpus.scan_disk()
        assert scanned["kCc8FmEb1nY"] == "kCc8FmEb1nY.txt"
        assert scanned["Uvl-tRga98g"] == "2026-09-11-already--Uvl-tRga98g.txt"
        assert scanned["BrpB-h1e--k"] == "BrpB-h1e--k.txt"

        renamed = dict(corpus.rename_legacy(
            {"kCc8FmEb1nY": "Lets build GPT", "BrpB-h1e--k": "Dash Id"}, "2026-09-11"))
        assert renamed["kCc8FmEb1nY.txt"] == "2026-09-11-lets-build-gpt--kCc8FmEb1nY.txt"
        assert renamed["BrpB-h1e--k.txt"] == "2026-09-11-dash-id--BrpB-h1e--k.txt"
        # already-migrated file untouched
        assert (data / "transcripts" / "2026-09-11-already--Uvl-tRga98g.txt").exists()

        n = corpus.regenerate_index()
        assert n == 3
        assert corpus.index_path.exists()


# ── enumeration retry ────────────────────────────────────────────────────

class _FakeResp:
    def __init__(self, status, payload):
        self.status_code = status
        self._payload = payload
        self.text = str(payload)

    def json(self):
        return self._payload


class _FakeRequests:
    """Serves a queued sequence of responses/exceptions to requests.get."""
    RequestException = Exception  # matches youtube's `requests.RequestException`

    def __init__(self, queue):
        self.queue = list(queue)
        self.calls = 0

    def get(self, *a, **k):
        self.calls += 1
        item = self.queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _with_fake(queue):
    fake = _FakeRequests(queue)
    youtube.requests = fake  # monkeypatch
    return fake


def _one_video_page():
    return _FakeResp(200, {
        "pageInfo": {"totalResults": 1},
        "items": [{"contentDetails": {"videoId": "kCc8FmEb1nY"},
                   "snippet": {"title": "Hi", "resourceId": {"videoId": "kCc8FmEb1nY"}}}],
    })


def test_enumerate_retries_transient_404_then_succeeds():
    real = youtube.requests
    try:
        fake = _with_fake([_FakeResp(404, {}), _one_video_page()])
        vids = enumerate_playlist("PL", "key", sleep=lambda _s: None)
        assert [v.video_id for v in vids] == ["kCc8FmEb1nY"]
        assert fake.calls == 2  # one retry
    finally:
        youtube.requests = real


def test_enumerate_fatal_403_no_retry():
    real = youtube.requests
    try:
        fake = _with_fake([_FakeResp(403, {"error": {"message": "bad key"}}), _one_video_page()])
        try:
            enumerate_playlist("PL", "key", sleep=lambda _s: None)
        except EnumerationError:
            assert fake.calls == 1  # did not retry
            return
        raise AssertionError("expected EnumerationError on 403")
    finally:
        youtube.requests = real


def test_enumerate_gives_up_after_retries():
    real = youtube.requests
    try:
        fake = _with_fake([_FakeResp(500, {})] * 10)
        try:
            enumerate_playlist("PL", "key", max_retries=3, sleep=lambda _s: None)
        except EnumerationError:
            assert fake.calls == 4  # initial + 3 retries
            return
        raise AssertionError("expected EnumerationError after retries")
    finally:
        youtube.requests = real


def test_enumerate_retries_network_error():
    real = youtube.requests
    try:
        fake = _with_fake([ConnectionError("boom"), _one_video_page()])
        vids = enumerate_playlist("PL", "key", sleep=lambda _s: None)
        assert len(vids) == 1
        assert fake.calls == 2
    finally:
        youtube.requests = real


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
