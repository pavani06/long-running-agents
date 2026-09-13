"""Filename helpers for the ingested-content layer.

Ingestion is keyed by URL (an article bookmarked twice is fetched once), so the
content file name is a readable domain slug plus a stable hash of the URL.
Pure functions — no network/disk.
"""
from __future__ import annotations

import hashlib
import re
from urllib.parse import urlparse


def url_key(url: str) -> str:
    """Stable 12-hex key for a URL (the diff key)."""
    return hashlib.sha1(url.strip().encode("utf-8")).hexdigest()[:12]


def _domain_slug(url: str) -> str:
    host = urlparse(url).netloc.lower().split("@")[-1].split(":")[0]
    host = host[4:] if host.startswith("www.") else host
    slug = re.sub(r"[^a-z0-9]+", "-", host).strip("-")
    return (slug[:40].rstrip("-") or "link")


def content_name(url: str) -> str:
    """`<domain-slug>--<url_key>.md` — readable + stable."""
    return f"{_domain_slug(url)}--{url_key(url)}.md"


def key_from_name(filename: str) -> str | None:
    stem = filename.rsplit(".", 1)[0]
    cand = stem.rsplit("--", 1)[-1] if "--" in stem else stem
    return cand if re.fullmatch(r"[0-9a-f]{12}", cand) else None
