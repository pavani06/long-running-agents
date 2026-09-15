#!/usr/bin/env python3
"""Unit tests for the GLM client's bounded JSON-parse retry (#263 follow-up).

The real failure mode: a 200 reply whose body is not valid JSON aborted Fase 2 and a
First-Loop Fase 4. chat_json now re-asks ONCE (JSON-only reminder, same schema). No
network — the transport `poster` is injected."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import glm  # noqa: E402
from glm import GLMError  # noqa: E402

VALID = '{"ok": true}'
MALFORMED = '{bad json,,}'   # has braces so extract_json reaches json.loads → unparseable


class FakePoster:
    """Returns queued content strings; records calls + the messages it was given."""
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = 0
        self.seen: list[list[dict]] = []

    def __call__(self, messages, api_key, **kwargs):
        self.calls += 1
        self.seen.append(messages)
        return self.replies.pop(0)


# ── extract_json (unchanged parse surface) ────────────────────────────────
def test_extract_json_strips_fences_and_parses():
    assert glm.extract_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_extract_json_raises_on_unparseable():
    with pytest.raises(GLMError):
        glm.extract_json(MALFORMED)


# ── the three required retry cases ────────────────────────────────────────
def test_valid_first_response_is_one_call():
    p = FakePoster([VALID])
    out = glm.chat_json([{"role": "user", "content": "x"}], "KEY", poster=p, sleep=lambda s: None)
    assert out == {"ok": True}
    assert p.calls == 1                      # no retry when the first reply parses


def test_malformed_then_valid_is_two_calls_and_success():
    p = FakePoster([MALFORMED, VALID])
    out = glm.chat_json([{"role": "user", "content": "x"}], "KEY", poster=p, sleep=lambda s: None)
    assert out == {"ok": True}
    assert p.calls == 2                      # one corrective re-ask, then success
    # the corrective call re-asks for JSON-only, carrying the original messages + reminder
    assert p.seen[1][0] == {"role": "user", "content": "x"}
    assert any(glm._JSON_ONLY_REMINDER in m.get("content", "") for m in p.seen[1])


def test_malformed_twice_is_two_calls_and_hard_failure():
    p = FakePoster([MALFORMED, MALFORMED])
    with pytest.raises(GLMError):
        glm.chat_json([{"role": "user", "content": "x"}], "KEY", poster=p, sleep=lambda s: None)
    assert p.calls == 2                      # capped at one retry; then the hard failure stands


# ── guardrails: the retry is bounded and scoped ───────────────────────────
def test_max_json_retries_zero_disables_reask():
    p = FakePoster([MALFORMED])
    with pytest.raises(GLMError):
        glm.chat_json([{"role": "user", "content": "x"}], "KEY", poster=p,
                      max_json_retries=0, sleep=lambda s: None)
    assert p.calls == 1                      # no re-ask when disabled


def test_transport_glmerror_is_not_reasked():
    # a transport-level GLMError (not a parse failure) must NOT trigger the JSON re-ask
    def boom(messages, api_key, **kwargs):
        boom.calls += 1
        raise GLMError("GLM HTTP 400")
    boom.calls = 0
    with pytest.raises(GLMError):
        glm.chat_json([{"role": "user", "content": "x"}], "KEY", poster=boom, sleep=lambda s: None)
    assert boom.calls == 1                    # raised before parse → no corrective call
