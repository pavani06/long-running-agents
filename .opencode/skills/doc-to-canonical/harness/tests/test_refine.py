import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from refine import CanonicalEntry, CanonicalRefinementSession, save_session, load_session


def test_canonical_entry_creation():
    entry = CanonicalEntry(
        entry_id="epistemic-memory-graph",
        canonical_type="canonical",
        grounding_prompt="Source: paper about agent memory...",
        current_text="""---
id: epistemic-memory-graph
type: canonical
---
# Epistemic Memory Graph
## Problem
Agents forget between sessions.
## Solution
Maintain a graph of entities and relationships.
""",
    )
    assert entry.entry_id == "epistemic-memory-graph"
    assert entry.canonical_type == "canonical"
    assert entry.refinement_history == []
    assert "Agents forget" in entry.current_text


def test_canonical_entry_invalid_type():
    try:
        CanonicalEntry(entry_id="x", canonical_type="invalid", grounding_prompt="g", current_text="t")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_canonical_entry_add_refinement():
    entry = CanonicalEntry(
        entry_id="test-doc", canonical_type="canonical",
        grounding_prompt="source...", current_text="# Test",
    )
    entry.add_refinement("add a con about token cost")
    entry.add_refinement("update Implementation section")
    assert len(entry.refinement_history) == 2
    assert "token cost" in entry.refinement_history[0]


def test_session_save_and_load():
    entry1 = CanonicalEntry(
        entry_id="doc-1", canonical_type="canonical",
        grounding_prompt="source 1", current_text="# Doc 1",
    )
    entry1.add_refinement("make more concise")
    entry2 = CanonicalEntry(
        entry_id="doc-2", canonical_type="principle",
        grounding_prompt="source 2", current_text="# Doc 2",
    )
    session = CanonicalRefinementSession(source_slug="agent-memory-paper", entries={"doc-1": entry1, "doc-2": entry2})
    with tempfile.TemporaryDirectory() as td:
        save_session(session, td)
        loaded = load_session(td)
        assert loaded is not None
        assert loaded.source_slug == "agent-memory-paper"
        assert len(loaded.entries) == 2
        e1 = loaded.entries["doc-1"]
        assert len(e1.refinement_history) == 1


def test_load_session_not_found():
    with tempfile.TemporaryDirectory() as td:
        assert load_session(td) is None
