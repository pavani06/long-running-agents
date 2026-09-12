"""Playlist enumeration via the YouTube Data API v3 (`playlistItems.list`).

Official, paginated (nextPageToken), free within quota (~1 unit/call, 50 items
per page -> ~8 calls for the full playlist), and not IP-blocked from CI runners.
Chosen over yt-dlp (datacenter-IP bot blocks) and ScrapeCreators (hard 200-item
cap, no pagination) after both were ruled out empirically.
"""
from __future__ import annotations

from dataclasses import dataclass

import requests

API_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
PAGE_SIZE = 50


@dataclass(frozen=True)
class PlaylistVideo:
    video_id: str
    title: str
    published_at: str  # when the item was added to the playlist (ISO 8601)


class EnumerationError(RuntimeError):
    """Raised when the playlist cannot be enumerated (bad key, API error)."""


def enumerate_playlist(playlist_id: str, api_key: str, *, timeout: int = 60) -> list[PlaylistVideo]:
    """Return every video in the playlist, paginating until exhausted.

    Raises EnumerationError on auth/API failure. A successful call that yields
    zero videos returns an empty list (the caller treats that as a red flag).
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

        r = requests.get(API_URL, params=params, timeout=timeout)
        if r.status_code != 200:
            detail = _error_detail(r)
            raise EnumerationError(f"playlistItems.list HTTP {r.status_code}: {detail}")

        payload = r.json()
        seen_total = (payload.get("pageInfo") or {}).get("totalResults", seen_total)
        for item in payload.get("items", []):
            video = _parse_item(item)
            if video is not None:
                videos.append(video)

        page_token = payload.get("nextPageToken")
        if not page_token:
            break

    return videos


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
    )


def _error_detail(r: requests.Response) -> str:
    try:
        err = r.json().get("error", {})
        reasons = ", ".join(e.get("reason", "") for e in err.get("errors", []) if e.get("reason"))
        return f"{err.get('message', r.text[:200])}" + (f" [{reasons}]" if reasons else "")
    except Exception:
        return r.text[:200]
