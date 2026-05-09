from typing import List, Tuple

#même principe que Bellman-Ford
def detection_cycle_neg(graph: List[List[int]],cost: List[List[int]]):
    n = len(graph)
    # étape 1 : on initialise les distances
    dist = [0] * n
    # relaxation des arêtes
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if graph[u][v] > 0:
                    if dist[u] + cost[u][v] < dist[v]:
                        dist[v] = dist[u] + cost[u][v]
    # détection cycle négatif
    for u in range(n):
        for v in range(n):
            if graph[u][v] > 0:
                if dist[u] + cost[u][v] < dist[v]:
                    return True
    

    return False