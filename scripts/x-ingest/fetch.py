"""Fetch and clean the content a bookmark links to (layered, with fallback).

Layer 1: Jina Reader (`r.jina.ai/<url>`) — clean, LLM-ready markdown, renders JS
and clears soft-paywalls. Layer 2 (fallback): local requests + trafilatura.
Result carries provenance (fetch_status) so a failure is a first-class signal,
never silence.

V1 handles external articles/links only; YouTube and PDF are recognized and
recorded as `unsupported` (deferred to their own handlers). The tweet text and
links themselves are untrusted, but here we only fetch/store — no LLM sees this
content until the extract stage wraps it in <untrusted_source>.
"""
from __future__ import annotations

import hashlib
from urllib.parse import urlparse

import requests

JINA = "https://r.jina.ai/"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
MIN_TEXT = 400          # shorter than this ≈ blocked/paywalled/empty
MAX_TEXT = 200_000      # cap stored content defensively

# ── pure helpers (unit-tested; no network) ────────────────────────────────
def classify_url(url: str) -> str:
    """'youtube' | 'pdf' | 'article' — routes the fetch."""
    p = urlparse(url)
    host = p.netloc.lower().split("@")[-1].split(":")[0]
    if host in ("youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"):
        return "youtube"
    if p.path.lower().endswith(".pdf") or host in ("arxiv.org", "www.arxiv.org") and "/pdf/" in p.path.lower():
        return "pdf"
    return "article"


def classify_status(text: str) -> str:
    """'ok' vs 'paywall' from the extracted text length (heuristic)."""
    return "ok" if len((text or "").strip()) >= MIN_TEXT else "paywall"


def content_hash(text: str) -> str:
    return hashlib.sha1((text or "").encode("utf-8")).hexdigest()


# ── network ───────────────────────────────────────────────────────────────
def _via_jina(url: str, timeout: int) -> tuple[str, str] | None:
    try:
        r = requests.get(JINA + url, headers={"User-Agent": UA, "Accept": "text/plain"},
                         timeout=timeout)
    except requests.RequestException:
        return None
    if r.status_code == 200 and r.text.strip():
        return r.text[:MAX_TEXT], r.headers.get("X-URL", url)
    return None


def _via_trafilatura(url: str, timeout: int) -> tuple[str, str] | None:
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    except requests.RequestException:
        return None
    if r.status_code != 200 or not r.text:
        return None
    try:
        import trafilatura  # lazy: keeps pure-function tests import-free
    except ImportError:
        return None
    text = trafilatura.extract(r.text, include_comments=False, favor_recall=True)
    if text and text.strip():
        return text[:MAX_TEXT], r.url
    return None


def fetch_content(url: str, *, timeout: int = 40) -> dict:
    """Return provenance dict: {status, final_url, method, text, content_hash, text_len}."""
    kind = classify_url(url)
    if kind in ("youtube", "pdf"):
        return {"status": "unsupported", "final_url": url, "method": kind,
                "text": "", "content_hash": "", "text_len": 0}

    for method, fn in (("jina", _via_jina), ("trafilatura", _via_trafilatura)):
        got = fn(url, timeout)
        if got:
            text, final_url = got
            return {
                "status": classify_status(text),
                "final_url": final_url,
                "method": method,
                "text": text,
                "content_hash": content_hash(text),
                "text_len": len(text),
            }
    return {"status": "failed", "final_url": url, "method": "", "text": "",
            "content_hash": "", "text_len": 0}
