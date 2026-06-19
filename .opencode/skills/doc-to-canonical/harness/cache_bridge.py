"""Cache bridge for doc-to-canonical — reuses CacheStore from analyze-and-improve.

The analyze-and-improve harness already implements CacheStore with the exact
contract needed (source_hash → phase outputs). This module re-exports it
so doc-to-canonical can use it without code duplication.

Uses importlib to avoid name collision between the local module name and
the analyze-and-improve cache.py module.

Usage:
    from harness.cache_bridge import compute_source_hash, CacheStore
    store = CacheStore(compute_source_hash(source_content))
    if store.has_phase("phase-1") and store.has_phase("phase-2"):
        store.restore_phase("phase-1", output_dir)
        store.restore_phase("phase-2", output_dir)
"""

import importlib
import sys
from pathlib import Path

# Find the analyze-and-improve harness — try multiple possible locations
# because $HOME and workspace root differ in WSL environments
_CANDIDATES = [
    Path.home() / ".opencode/skills/analyze-and-improve/harness",
    Path("/mnt/c/Users/pavan/.opencode/skills/analyze-and-improve/harness"),
]
_AI_HARNESS = None
for _c in _CANDIDATES:
    if (_c / "cache.py").exists():
        _AI_HARNESS = str(_c)
        break
if _AI_HARNESS is None:
    raise ImportError(
        "Cannot find analyze-and-improve harness cache.py. "
        f"Searched: {_CANDIDATES}"
    )
if _AI_HARNESS not in sys.path:
    sys.path.insert(0, _AI_HARNESS)

_cache_mod = importlib.import_module("cache")

compute_source_hash = _cache_mod.compute_source_hash
CacheStore = _cache_mod.CacheStore
CACHE_ROOT = _cache_mod.CACHE_ROOT

__all__ = ["compute_source_hash", "CacheStore", "CACHE_ROOT"]
