"""OAuth2 refresh for the X API v2 (confidential client).

The access token lives ~2h, so each run trades the stored refresh token for a
fresh access token. X refresh tokens are SINGLE-USE and rotate: the response
carries a NEW refresh token and invalidates the old one immediately. The new
refresh token MUST be persisted back to the secret store before anything else,
or the next run has a dead token and the user must re-consent.

Secrets are never logged (Rule 9): the token is passed to `gh secret set` via
stdin, never as an argv the process list could expose.
"""
from __future__ import annotations

import base64
import subprocess

import requests

TOKEN_URL = "https://api.x.com/2/oauth2/token"


class AuthError(Exception):
    """Refresh grant failed (bad/expired refresh token, wrong client creds)."""


class PersistError(Exception):
    """Could not write the rotated refresh token back to the secret store."""


def refresh_access_token(refresh_token: str, client_id: str, client_secret: str,
                         *, timeout: int = 30) -> dict:
    """Trade a refresh token for a fresh access token + a NEW refresh token.

    Returns the token response dict (access_token, refresh_token, expires_in,
    scope). Raises AuthError on any non-200.
    """
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    try:
        r = requests.post(
            TOKEN_URL,
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
            },
            timeout=timeout,
        )
    except requests.RequestException as e:
        raise AuthError(f"network error contacting token endpoint: {e}")
    if r.status_code != 200:
        # Body carries the reason (e.g. invalid_grant) and never echoes our secret.
        raise AuthError(f"refresh failed HTTP {r.status_code}: {r.text[:300]}")
    body = r.json()
    if "access_token" not in body or "refresh_token" not in body:
        raise AuthError(f"token response missing fields: {sorted(body)}")
    return body


def persist_refresh_token(new_refresh_token: str, repo: str,
                          *, secret_name: str = "X_REFRESH_TOKEN") -> None:
    """Write the rotated refresh token back to the repo secret via `gh`.

    Requires GH_TOKEN in the environment to be a PAT with secrets:write. The
    value goes through stdin so it never appears in the process argv/logs.
    """
    proc = subprocess.run(
        ["gh", "secret", "set", secret_name, "--repo", repo],
        input=new_refresh_token, text=True, capture_output=True, check=False,
    )
    if proc.returncode != 0:
        # stderr may include a gh message but not our token value.
        raise PersistError(f"gh secret set exited {proc.returncode}: {proc.stderr.strip()[:200]}")
