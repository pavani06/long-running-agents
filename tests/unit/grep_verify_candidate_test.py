#!/usr/bin/env python3
"""#288 Track-D candidate: whole-file + min-length verifier. Recall (recover
mislocated real quotes) AND false-accept (adversarial negatives). Documents the
one class a presence-verifier cannot catch — semantic-wrongness — which is the
verdict/E-axis's job, NOT this gate's."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

from grep_verify import MIN_WHOLEFILE_QUOTE_CHARS, verify_citation  # noqa: E402

# a file with a long, distinctive sentence far from line 1, plus a short line
LONG = "the deterministic cosine duplication gate holds a proposed artifact above the threshold"  # 87 chars
FILE = ("preamble line\n" * 40) + LONG + "\n" + "short tail\n"   # LONG at line 41


# ── recall: whole-file recovers a real quote the model mis-located ──────────
def test_recall_wholefile_recovers_mislocated_long_quote():
    # cited at line 1, quote actually at line 41, >= min chars → recovered
    r = verify_citation(FILE, 1, LONG)
    assert r["ok"] is True and "whole-file" in r["reason"]


def test_recall_out_of_range_line_still_recovers_long_quote():
    r = verify_citation(FILE, 999, LONG)
    assert r["ok"] is True   # bad line number no longer fatal for a real long quote


# ── guard: short quote present-but-not-near-line is rejected ────────────────
def test_guard_rejects_short_quote_not_near_line():
    r = verify_citation(FILE, 1, "short tail")   # 10 chars < 40, present at line 42
    assert r["ok"] is False and "< " in r["reason"]


def test_precise_near_line_still_wins_for_short_quote():
    r = verify_citation(FILE, 42, "short tail")  # near the cited line → precise path
    assert r["ok"] is True and "near cited line" in r["reason"]


# ── adversarial negative set (5 categories) ─────────────────────────────────
def test_adv_wrong_file_quote_absent_rejected():
    # a real quote cited against the WRONG file (not present) → reject
    assert verify_citation("totally unrelated content here\n" * 5, 1, LONG)["ok"] is False


def test_adv_altered_word_rejected():
    # one word changed → not present verbatim → reject (not a paraphrase-accepter)
    altered = LONG.replace("cosine", "euclidean")
    assert verify_citation(FILE, 1, altered)["ok"] is False


def test_adv_common_long_string_present_is_accepted_presence_only():
    # a long generic string that genuinely occurs verifies on PRESENCE; the verifier
    # is a presence check, not a relevance judge (documented boundary).
    generic = "preamble line preamble line preamble line preamble line"  # >=40, present
    assert verify_citation(FILE, 1, generic)["ok"] is True


def test_adv_truncated_but_real_substring_accepted():
    # a truncated-yet-real >=40-char substring is real content → accepted
    assert verify_citation(FILE, 1, LONG[:60])["ok"] is True


def test_adv_semantically_wrong_but_present_is_a_known_limit():
    # KNOWN LIMIT: a real, present, >=40-char quote that does NOT semantically support
    # the claim still verifies. Presence != support; semantic correctness is the
    # verdict/E-axis's responsibility, out of scope for a deterministic presence gate.
    assert verify_citation(FILE, 1, LONG)["ok"] is True


def test_min_len_constant_is_the_guard():
    assert MIN_WHOLEFILE_QUOTE_CHARS == 40
