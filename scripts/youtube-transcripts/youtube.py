"""Playlist enumeration via the YouTube Data API v3 (`playlistItems.list`).

Official, paginated (nextPageToken), free within quota (~1 unit/call, 50 items
per page -> ~8 calls for the full playlist), and not IP-blocked from CI runners.
Chosen over yt-dlp (datacenter-IP bot blocks) and ScrapeCreators (hard 200-item
cap, no pagination) after both were ruled out empirically.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

import requests

API_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
PAGE_SIZE = 50

# Retry transient failures only. 404 is included because playlistItems.list was
# observed to return a spurious `playlistNotFound` that cleared on re-run; a
# genuinely bad playlist id still fails after the retries (still red, just later).
_RETRYABLE_STATUS = {404, 429, 500, 502, 503, 504}
# Deterministic failures — never retry (bad/invalid key, API not enabled, quota).
_FATAL_STATUS = {400, 401, 403}


@dataclass(frozen=True)
class PlaylistVideo:
    video_id: str
    title: str
    published_at: str  # when the item was added to the playlist (ISO 8601)
    channel: str = ""  # videoOwnerChannelTitle, when present


class EnumerationError(RuntimeError):
    """Raised when the playlist cannot be enumerated (bad key, API error)."""


def enumerate_playlist(
    playlist_id: str,
    api_key: str,
    *,
    timeout: int = 60,
    max_retries: int = 3,
    backoff_base: float = 2.0,
    sleep=time.sleep,
) -> list[PlaylistVideo]:
    """Return every video in the playlist, paginating until exhausted.

    Transient failures (5xx, 429, a spurious 404, network errors) are retried
    with exponential backoff; deterministic ones (bad key, API disabled, quota)
    fail fast. Raises EnumerationError once retries are exhausted. A successful
    call that yields zero videos returns [] (the caller treats that as red).
    """
    videos: list[PlaylistVideo] = []
    page_token: str | None = None
    seen_total: int | None = None

    while True:
        params = {
            "part": "snippet,contentDetails,status",
            "playlistId": playlist_id,
            "maxResults": PAGE_SIZE,
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        payload = _get_page(params, timeout, max_retries, backoff_base, sleep)
        seen_total = (payload.get("pageInfo") or {}).get("totalResults", seen_total)
        for item in payload.get("items", []):
            video = _parse_item(item)
            if video is not None:
                videos.append(video)

        page_token = payload.get("nextPageToken")
        if not page_token:
            break

    return videos


def _get_page(params: dict, timeout: int, max_retries: int, backoff_base: float, sleep) -> dict:
    """Fetch one page, retrying transient failures with exponential backoff."""
    last_err = ""
    for attempt in range(max_retries + 1):
        try:
            r = requests.get(API_URL, params=params, timeout=timeout)
        except requests.RequestException as e:
            last_err = f"network error: {e}"
        else:
            if r.status_code == 200:
                return r.json()
            detail = _error_detail(r)
            if r.status_code in _FATAL_STATUS:
                raise EnumerationError(f"playlistItems.list HTTP {r.status_code}: {detail}")
            last_err = f"HTTP {r.status_code}: {detail}"
            if r.status_code not in _RETRYABLE_STATUS:
                raise EnumerationError(f"playlistItems.list {last_err}")

        if attempt < max_retries:
            sleep(backoff_base * (2 ** attempt))

    raise EnumerationError(f"playlistItems.list failed after {max_retries + 1} attempts: {last_err}")


def _parse_item(item: dict) -> PlaylistVideo | None:
    content = item.get("contentDetails") or {}
    snippet = item.get("snippet") or {}
    video_id = content.get("videoId") or (snippet.get("resourceId") or {}).get("videoId")
    if not video_id:
        return None
    return PlaylistVideo(
        video_id=video_id,
        title=snippet.get("title") or "",
        published_at=content.get("videoPublishedAt") or snippet.get("publishedAt") or "",
        channel=snippet.get("videoOwnerChannelTitle") or "",
    )


def _error_detail(r: requests.Response) -> str:
    try:
        err = r.json().get("error", {})
        reasons = ", ".join(e.get("reason", "") for e in err.get("errors", []) if e.get("reason"))
        return f"{err.get('message', r.text[:200])}" + (f" [{reasons}]" if reasons else "")
    except Exception:
        return r.text[:200]
