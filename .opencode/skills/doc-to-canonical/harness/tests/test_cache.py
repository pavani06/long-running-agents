import sys, os, json, tempfile, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.expanduser("~/.opencode/skills/analyze-and-improve/harness"))
from cache_bridge import compute_source_hash, CacheStore, CACHE_ROOT


def test_doc_cache_namespace():
    """doc-to-canonical usa seu próprio namespace no cache root."""
    doc_hash = compute_source_hash("# Test document\n\nContent here.")
    store = CacheStore(doc_hash)
    assert len(doc_hash) == 64
    assert doc_hash == compute_source_hash("# Test document\n\nContent here.")


def test_doc_cache_write_phase_1_and_2():
    """Escreve Phase 1 (analysis) e Phase 2 (patterns) e lê de volta."""
    doc_hash = compute_source_hash("# Document about agent memory\n\nAgents need memory to persist state.")
    store = CacheStore(doc_hash)

    store.write_phase("phase-1", "analysis.md", "# Analysis\n\nThis document covers agent memory patterns.")
    store.write_phase("phase-1", "analysis.yaml", "frameworks:\n  - epistemic-memory-graph\n  - durable-facts")
    store.write_phase("phase-2", "patterns.md", "# Patterns\n\n1. Epistemic Memory Graph\n2. Durable Facts")
    store.write_phase("phase-2", "patterns.yaml", "patterns:\n  - name: Epistemic Memory Graph")

    assert store.has_phase("phase-1")
    assert store.has_phase("phase-2")

    phase1 = store.read_phase("phase-1")
    assert phase1 is not None
    assert "analysis.md" in phase1
    assert "agent memory" in phase1["analysis.md"].lower()

    phase2 = store.read_phase("phase-2")
    assert phase2 is not None
    assert "patterns.md" in phase2
    assert "Epistemic Memory" in phase2["patterns.md"]

    # Cleanup
    store.clear_phase("phase-1")
    store.clear_phase("phase-2")


def test_doc_cache_restore_phase():
    """Restore copia arquivos para output_dir."""
    doc_hash = compute_source_hash("# Restore test document")
    store = CacheStore(doc_hash)
    store.write_phase("phase-1", "test.md", "# Restored content")

    with tempfile.TemporaryDirectory() as td:
        written = store.restore_phase("phase-1", td)
        assert len(written) == 1
        restored = os.path.join(td, "test.md")
        assert os.path.exists(restored)
        with open(restored) as f:
            assert f.read() == "# Restored content"

    store.clear_phase("phase-1")


def test_doc_cache_clear():
    """Clear remove a fase cacheada."""
    doc_hash = compute_source_hash("# Clear test doc")
    store = CacheStore(doc_hash)
    store.write_phase("phase-1", "file.md", "content")
    assert store.has_phase("phase-1")
    store.clear_phase("phase-1")
    assert not store.has_phase("phase-1")
