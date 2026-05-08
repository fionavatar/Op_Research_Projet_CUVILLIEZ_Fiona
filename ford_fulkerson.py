from collections import deque
from typing import List, Tuple
from main import log


def bfs(graph : List[List[int]], s : int, t : int, parent : List[int]) -> bool: 
    n = len(graph)
    visited = [False] * n
    queue = deque([s])
    visited[s] = True

    log(f"BFS depuis {s} vers {t}", 1)

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and graph[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
                log(f"Visite: {u} -> {v} (capacité={graph[u][v]})", 2)
                if v == t:
                    log("Chemin augmentant trouvé", 2)
                    return True
    log("Aucun chemin trouvé", 2)
    return False


def ford_fulkerson(graph : List[List[int]], s : int, t : int) -> Tuple[int, List[List[int]], List[List[int]]] :
    n = len(graph)
    parent = [-1] * n
    max_flow = 0
    # matrice de flot
    flow = [[0]*n for _ in range(n)]
    step = 0

    log("Début algo ford-fulkerson", 0)

    while bfs(graph, s, t, parent):
        path_flow = float("inf")
        v = t
        # calcul goulot
        path = []
        # trouver le goulot d'étranglement
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            path.append((u,v))
            v = u

        path.reverse()
        log(f"\nétape {step}", 0)
        log(f"chemin : {path}", 1)
        log(f"flux du chemin : {path_flow}", 1)
        
        max_flow += path_flow
        # mise à jour du graphe résiduel et du flot
        v = t
        while v != s:
            u = parent[v]

            graph[u][v] -= path_flow
            graph[v][u] += path_flow

            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

        log(f"flot total actuel : {max_flow}", 1)
        step += 1

    log(f"flot total actuel : {max_flow}", 1)
    return max_flow, graph, flow


def min_cut(original : List[List[int]], residual : List[List[int]], source : int) -> List[Tuple[int,int]]:
    n = len(original)
    visited = [False]*n
    queue = deque([source])
    visited[source] = True

    log("min-cut", 0)
    log(f"source = {source}", 1)

    #bfs sur le graphe résiduel
    while queue:
        u = queue.popleft()
        log(f"visite du sommet {u}", 1)
        for v in range(n):
            if residual[u][v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)
                log(f"atteignable {u} -> {v}", 2)
    
    #construction de la cut
    cut = []
    log("\nconstruction de la min-cut", 0)
    for u in range(n):
        for v in range(n):
            if visited[u] and not visited[v] and original[u][v] > 0:
                cut.append((u, v))
                log(f"arête coupée: {u} -> {v}", 1)

    log(f"\ntaille de la coupe : {len(cut)}", 0)   

    return cut







