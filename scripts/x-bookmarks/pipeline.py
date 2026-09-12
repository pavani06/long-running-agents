#!/usr/bin/env python3
"""Collect X bookmarks and version them under raw/x/bookmarks/.

Each run: refresh the OAuth2 access token, PERSIST the rotated refresh token
back to the secret (single-use!), fetch the bookmarks, diff against what is
already on disk (stateless), and write the new ones.

Modes:
  daily     write new bookmarks + regenerate index (default)
  dry-run   refresh + persist + fetch + diff, but write/commit nothing
            (still rotates the refresh token — that is unavoidable)
  reprocess re-fetch the current bookmark window and rewrite each fetched item
            in place (enrich existing + add new), preserving filename and date;
            items already aged out of the API window are not reprocessed

Environment:
  X_REFRESH_TOKEN  OAuth2 refresh token (rotated in place each run)  — required
  X_CLIENT_ID      OAuth2 client id                                   — required
  X_CLIENT_KEY     OAuth2 client secret (confidential app)            — required
  GH_TOKEN         PAT with secrets:write, for the refresh write-back — required
  GITHUB_REPOSITORY  owner/repo for `gh --repo` (set by Actions)      — required
  X_BOOKMARKS_CAP  per-run write cap (default 500)

Exit: 0 = success (incl. nothing-new, 429 partial); 1 = red (refresh failed,
persist failed, or fetch auth failed).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

import bookmarks as bm
from oauth import AuthError, PersistError, persist_refresh_token, refresh_access_token
from store import BookmarkStore

REPO_ROOT = Path(__file__).resolve().parents[2]
TZ = ZoneInfo("America/Sao_Paulo")
DEFAULT_CAP = 500


def today() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def run(mode: str, cap: int, *, refresh_token: str, client_id: str,
        client_secret: str, repo: str) -> int:
    # 1. Refresh — this consumes and rotates the single-use refresh token.
    try:
        tok = refresh_access_token(refresh_token, client_id, client_secret)
    except AuthError as e:
        summary(f"RED: OAuth refresh failed — re-consent needed. {e}")
        return 1

    # 2. Persist the NEW refresh token immediately, before anything can fail.
    #    If this fails the chain is broken, so it is a hard red.
    try:
        persist_refresh_token(tok["refresh_token"], repo)
    except PersistError as e:
        summary(f"RED: refresh rotated but could not be persisted — the stored "
                f"token is now STALE, re-consent needed. {e}")
        return 1
    summary("refresh ok; rotated refresh token persisted to X_REFRESH_TOKEN.")

    access = tok["access_token"]
    if "bookmark.read" not in tok.get("scope", ""):
        summary(f"WARNING: token scope lacks bookmark.read (scope={tok.get('scope')!r})")

    # 3. Fetch bookmarks.
    session = requests.Session()
    try:
        uid, uname = bm.resolve_user_id(session, access)
        fetched = bm.fetch_bookmarks(access, uid)
    except bm.AuthError as e:
        summary(f"RED: {e}")
        return 1
    except bm.RateLimited:
        summary("WARNING: rate-limited while fetching — leaving the rest for next run.")
        return 0
    except bm.FetchError as e:
        summary(f"RED: unexpected fetch response: {e}")
        return 1

    store = BookmarkStore(REPO_ROOT)
    disk_map = store.scan_disk()
    date = today()

    if mode == "reprocess":
        # Re-fetch everything and rewrite each item in place (enrich existing +
        # add any new). write_item preserves the original filename/date by id.
        seen: set[str] = set()
        written = 0
        for b in fetched:
            if b.status_id in seen:
                continue
            seen.add(b.status_id)
            store.write_item(date, b, disk_map)
            written += 1
        count = store.regenerate_index()
        summary(f"@{uname}: reprocess rewrote {written} item(s); corpus now {count}.")
        return 0

    new = store.new_bookmarks(fetched)
    summary(f"@{uname}: fetched {len(fetched)}, on disk {len(disk_map)}, "
            f"new {len(new)}")

    if not new:
        summary("nothing new to collect.")
        return 0
    if mode == "dry-run":
        summary(f"dry-run: would write {min(len(new), cap)} item(s); sample: "
                + ", ".join(f"@{b.handle}/{b.status_id}" for b in new[:5]))
        return 0

    targets = new[:cap]
    if len(new) > cap:
        summary(f"cap {cap}: writing {len(targets)} now, {len(new) - cap} left for next run")
    for b in targets:
        store.write_item(date, b, disk_map)
    count = store.regenerate_index()
    summary(f"done: wrote {len(targets)} new item(s); corpus now {count}.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", nargs="?", default="daily",
                    choices=["daily", "dry-run", "reprocess"])
    args = ap.parse_args()

    env = {k: os.environ.get(k) for k in
           ("X_REFRESH_TOKEN", "X_CLIENT_ID", "X_CLIENT_KEY", "GITHUB_REPOSITORY")}
    missing = [k for k, v in env.items() if not v]
    if missing:
        print(f"RED: missing env: {missing}", file=sys.stderr)
        return 1
    if not os.environ.get("GH_TOKEN"):
        print("RED: GH_TOKEN (PAT for refresh write-back) not set", file=sys.stderr)
        return 1
    cap = int(os.environ.get("X_BOOKMARKS_CAP") or DEFAULT_CAP)

    return run(args.mode, cap,
               refresh_token=env["X_REFRESH_TOKEN"], client_id=env["X_CLIENT_ID"],
               client_secret=env["X_CLIENT_KEY"], repo=env["GITHUB_REPOSITORY"])


if __name__ == "__main__":
    raise SystemExit(main())
