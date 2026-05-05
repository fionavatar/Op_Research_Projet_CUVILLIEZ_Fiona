"""
Ford-Fulkerson (Edmonds-Karp) — implémentation pythonique
=========================================================
Complexité : O(V * E²)

Choix de conception :
- Graphe représenté par un dict de dicts (sparse, lisible)
- Fonctions pures : pas d'effet de bord sur le graphe original
- Générateur pour les chemins augmentants (lazy evaluation)
- Type hints + docstrings
- Nommage PEP 8
"""

from __future__ import annotations
from collections import deque, defaultdict
from typing import Generator


# ── Types ────────────────────────────────────────────────────────────────────

Graph = dict[int, dict[int, int]]   # {u: {v: capacité}}
Path  = list[int]


# ── Construction du graphe ───────────────────────────────────────────────────

def build_graph(
    starts: list[int],
    ends:   list[int],
    caps:   list[int],
) -> Graph:
    """Construit un graphe orienté pondéré depuis trois listes parallèles."""
    graph: Graph = defaultdict(lambda: defaultdict(int))
    for u, v, c in zip(starts, ends, caps):
        graph[u][v] += c
    return graph


# ── BFS : trouve un chemin augmentant ────────────────────────────────────────

def BFS(residual: Graph, source: int, sink: int) -> Path | None:
    """
    Retourne un chemin source→sink dans le graphe résiduel,
    ou None s'il n'en existe pas.
    """
    visited = {source}
    parent: dict[int, int] = {}
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v, cap in residual[u].items():
            if v not in visited and cap > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    # reconstitution du chemin
                    path, node = [], sink
                    while node != source:
                        path.append(node)
                        node = parent[node]
                    return [source] + path[::-1]
                queue.append(v)
    return None


# ── Générateur de chemins augmentants ────────────────────────────────────────

def _augmenting_paths(
    residual: Graph, source: int, sink: int
) -> Generator[tuple[Path, int], None, None]:
    """
    Génère (chemin, débit) tant qu'un chemin augmentant existe.
    Met à jour le graphe résiduel à chaque itération.
    """
    while path := BFS(residual, source, sink):
        # débit = goulot d'étranglement sur le chemin
        flow = min(residual[u][v] for u, v in zip(path, path[1:]))

        # mise à jour des capacités résiduelles
        for u, v in zip(path, path[1:]):
            residual[u][v] -= flow
            residual[v][u] += flow   # arc retour

        yield path, flow


# ── Algorithme principal ─────────────────────────────────────────────────────

def ford_fulkerson(graph: Graph, source: int, sink: int) -> tuple[int, list]:
    """
    Calcule le flot maximum de source vers sink (Edmonds-Karp).

    Paramètres
    ----------
    graph  : graphe original (non modifié)
    source : nœud source
    sink   : nœud puits

    Retourne
    --------
    (max_flow, augmenting_paths)
    """
    # copie profonde → pas d'effet de bord sur graph
    residual: Graph = defaultdict(lambda: defaultdict(int))
    for u, neighbors in graph.items():
        for v, cap in neighbors.items():
            residual[u][v] += cap

    paths_found = []
    max_flow = sum(
        flow
        for path, flow in _augmenting_paths(residual, source, sink)
        if not paths_found.append((path, flow))   # accumule en passant
    )
    return max_flow, paths_found


# ── Affichage ────────────────────────────────────────────────────────────────

def print_result(max_flow: int, paths: list, source: int, sink: int) -> None:
    print(f"Flot maximum ({source} → {sink}) : {max_flow}")
    print(f"Chemins augmentants ({len(paths)}) :")
    for path, flow in paths:
        print(f"  {'→'.join(map(str, path))}  [débit = {flow}]")


# ── Exemples ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # ── Exemple 1 : graphe original (matrice → dict) ──────────────────────
    print("=" * 55)
    print("Exemple 1 — graphe à 6 nœuds")
    print("=" * 55)

    matrix = [
        [0, 16, 13,  0,  0,  0],
        [0,  0, 10, 12,  0,  0],
        [0,  4,  0,  0, 14,  0],
        [0,  0,  9,  0,  0, 20],
        [0,  0,  0,  7,  0,  4],
        [0,  0,  0,  0,  0,  0],
    ]
    g1 = build_graph(
        [u for u, row in enumerate(matrix) for v, c in enumerate(row) if c],
        [v for row in matrix for v, c in enumerate(row) if c],
        [c for row in matrix for c in row if c],
    )
    flow1, paths1 = ford_fulkerson(g1, source=0, sink=5)
    print_result(flow1, paths1, 0, 5)

    # ── Exemple 2 : 5 nœuds, listes parallèles ────────────────────────────
    print("\n" + "=" * 55)
    print("Exemple 2 — réseau 5 nœuds")
    print("=" * 55)

    starts     = [0, 0, 0, 1, 1, 2, 2, 3, 3]
    ends       = [1, 2, 3, 2, 4, 3, 4, 2, 4]
    capacities = [20, 30, 10, 40, 30, 10, 20, 5, 20]

    g2 = build_graph(starts, ends, capacities)
    flow2, paths2 = ford_fulkerson(g2, source=0, sink=4)
    print_result(flow2, paths2, 0, 4)