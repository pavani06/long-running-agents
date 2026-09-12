"""Fetch the authenticated user's bookmarks from the X API v2.

`GET /2/users/:id/bookmarks` (OAuth2 user-context, scope bookmark.read). We
resolve the user id from /2/users/me, then page by `meta.next_token`. The API
exposes only a recent window of bookmarks, not the full history — fine for a
going-forward stateless diff.
"""
from __future__ import annotations

import time

import requests

from store import Bookmark

API = "https://api.x.com/2"


class AuthError(Exception):
    """401/403 — access token invalid/expired or missing scope."""


class RateLimited(Exception):
    """429 persisted — leave the rest for the next run."""


class FetchError(Exception):
    """Non-retryable unexpected response."""


def _get(session: requests.Session, url: str, token: str, params: dict | None,
         *, timeout: int) -> dict:
    r = session.get(url, headers={"Authorization": f"Bearer {token}"},
                    params=params or {}, timeout=timeout)
    if r.status_code == 401:
        raise AuthError(f"401 — access token invalid/expired: {r.text[:200]}")
    if r.status_code == 403:
        raise AuthError(f"403 — missing scope (bookmark.read) or tier: {r.text[:200]}")
    if r.status_code == 429:
        raise RateLimited("429")
    if r.status_code != 200:
        raise FetchError(f"HTTP {r.status_code}: {r.text[:200]}")
    return r.json()


def resolve_user_id(session: requests.Session, token: str, *, timeout: int = 30) -> tuple[str, str]:
    """Return (user_id, username) for the token's owner."""
    body = _get(session, f"{API}/users/me", token, None, timeout=timeout)
    data = body.get("data") or {}
    uid = data.get("id")
    if not uid:
        raise FetchError(f"/users/me returned no id: {str(body)[:200]}")
    return str(uid), data.get("username", "unknown")


def _pairs(body: dict) -> list[Bookmark]:
    users = {u["id"]: u for u in body.get("includes", {}).get("users", [])}
    out: list[Bookmark] = []
    for t in body.get("data", []) or []:
        sid = t.get("id")
        if not sid:
            continue
        user = users.get(t.get("author_id"), {})
        handle = user.get("username", "unknown")
        out.append(Bookmark(
            status_id=str(sid),
            handle=handle,
            text=t.get("text", ""),
            created_at=t.get("created_at", ""),
            url=f"https://x.com/{handle}/status/{sid}",
        ))
    return out


def fetch_bookmarks(token: str, user_id: str, *, max_pages: int = 50,
                    pacing: float = 1.0, timeout: int = 30,
                    sleep=time.sleep) -> list[Bookmark]:
    """Page through the user's bookmarks (most-recent first). Raises on auth."""
    session = requests.Session()
    url = f"{API}/users/{user_id}/bookmarks"
    out: list[Bookmark] = []
    next_token: str | None = None
    for _ in range(max_pages):
        params = {
            "max_results": 100,
            "expansions": "author_id",
            "tweet.fields": "created_at",
            "user.fields": "username",
        }
        if next_token:
            params["pagination_token"] = next_token
        body = _get(session, url, token, params, timeout=timeout)
        out.extend(_pairs(body))
        next_token = body.get("meta", {}).get("next_token")
        if not next_token:
            break
        sleep(pacing)
    return out
