"""Transcript fetch via SerpApi (engine `youtube_video_transcript`).

Ported verbatim from the validated one-shot fetcher, plus explicit 429 backoff
so the daily/retry runs degrade gracefully under rate limiting instead of
failing the whole job.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

import requests

SEARCH_URL = "https://serpapi.com/search.json"
DEFAULT_LANG = "en"


@dataclass(frozen=True)
class Transcript:
    text: str
    lang: str
    segments: int


class RateLimited(Exception):
    """Raised when SerpApi keeps returning 429 after the configured retries."""


class AuthError(Exception):
    """Raised on 401/403 — invalid or revoked SerpApi key."""


def fetch_transcript(
    video_id: str,
    api_key: str,
    *,
    lang: str = DEFAULT_LANG,
    timeout: int = 90,
    max_retries: int = 4,
    backoff_base: float = 3.0,
) -> Transcript | None:
    """Return a Transcript, or None if the video has no captions.

    Raises AuthError on 401/403 and RateLimited if 429 persists past retries;
    both are surfaced to the caller so the run can go red / stop cleanly.
    """
    base = {"engine": "youtube_video_transcript", "v": video_id, "api_key": api_key}

    def call(extra: dict) -> list | None:
        params = {**base, **extra}
        for attempt in range(max_retries):
            r = requests.get(SEARCH_URL, params=params, timeout=timeout)
            if r.status_code in (401, 403):
                raise AuthError(f"SerpApi HTTP {r.status_code} (invalid/revoked key)")
            if r.status_code == 429:
                if attempt == max_retries - 1:
                    raise RateLimited("SerpApi 429 after retries")
                time.sleep(backoff_base * (2 ** attempt))
                continue
            if r.status_code != 200:
                raise RuntimeError(f"SerpApi HTTP {r.status_code}")
            transcript = r.json().get("transcript")
            return transcript if isinstance(transcript, list) and transcript else None
        return None

    # Preferred language, then fall back to whatever caption exists.
    segments = call({"language_code": lang})
    effective_lang = lang
    if segments is None:
        segments = call({})
        effective_lang = ""  # unknown; SerpApi picked whatever was available
    if segments is None:
        return None

    text = "\n".join(s.get("snippet", "").strip() for s in segments if s.get("snippet"))
    if not text:
        return None
    return Transcript(text=text, lang=effective_lang or lang, segments=len(segments))
