"""Community detection on the weighted connections graph (networkx)."""
from __future__ import annotations

import networkx as nx


def build_graph(nodes: list[str], edges: list[tuple[str, str, float]]) -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(nodes)
    for a, b, w in edges:
        g.add_edge(a, b, weight=w)
    return g


def communities(nodes: list[str], edges: list[tuple[str, str, float]],
                *, resolution: float = 1.0) -> list[list[str]]:
    """Greedy-modularity communities, weighted. Deterministic.

    Returns communities as lists of video_ids, largest first, each sorted for
    stable output. Isolated nodes (no edges) each form a singleton community.
    """
    g = build_graph(nodes, edges)
    comms = nx.community.greedy_modularity_communities(g, weight="weight", resolution=resolution)
    result = [sorted(c) for c in comms]
    result.sort(key=lambda c: (-len(c), c[0] if c else ""))
    return result


def sizes(comms: list[list[str]]) -> list[int]:
    return [len(c) for c in comms]
