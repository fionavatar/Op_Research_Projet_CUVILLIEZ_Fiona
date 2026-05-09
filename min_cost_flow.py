from heapq import heappush, heappop
from typing import List, Tuple

"""
Implémentation min cost flow algo pour repeated augmenting paths 
Avec algo de chemin et coût négatif
"""
#Première approche avec l'algorithme de Bellman-Ford
#complexité O(NM**2)
def bellman_ford(graph: List[List[int]],cost: List[List[int]],s: int) -> Tuple[List[float], List[int]]:
    n = len(graph)
    # étape 1 : on initialise les distances
    dist = [float("inf")] * n
    dist[s] = 0
    # parents pour reconstruire chemin
    parent = [-1] * n
    # relaxation des arêtes
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                # arête existante
                if graph[u][v] > 0:
                    # relaxation
                    if dist[u] != float("inf") and dist[u] + cost[u][v] < dist[v]:
                        dist[v] = dist[u] + cost[u][v]
                        parent[v] = u
    # détection cycle négatif
    for u in range(n):
        for v in range(n):
            if graph[u][v] > 0:
                if dist[u] != float("inf") and dist[u] + cost[u][v] < dist[v]:
                    raise ValueError("cycle négatif détecté")
                
    return dist, parent


def min_cost_flow_bellman_ford(graph: List[List[int]],cost: List[List[int]],s: int, t:int) -> Tuple[List[List[int]], List[List[int]], int, int]:
    #étape 1 : initialisation
    n = len(graph)
    max_flow = 0
    total_cost = 0
    # matrice de flot
    flow = [[0]*n for _ in range(n)]

    #étape 2
    while True:
        dist, parent = bellman_ford(graph, cost, s) #plus court chemin
        #plus de chemin augmentant
        if parent[t] == -1:
            break
        #calcul du flot du chemin
        path_flow = float("inf")
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u
        max_flow += path_flow
        total_cost += path_flow * dist[t]
        #mise à jour du graphe résiduel
        v = t
        while v != s:
            u = parent[v]
            #capacité résiduel
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            #arête inverse ducoût oppposé
            cost[v][u] = -cost[u][v]
            #mise à jour du flot
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

    return flow, graph, max_flow, total_cost


#2ème approche avec l'algorithme de Dijkstra
def dijkstra(graph: List[List[int]],cost: List[List[int]],s: int, potential: List[int]) -> Tuple[List[float, List[int]]]:
    # étape 1 initialisation
    n = len(graph)
    dist = [float("inf")] * n #pour chaque simmet on initialise à +inf
    parent = [-1] * n
    dist[s] = 0 #sommet de départ à 0
    priority_queue = [(0, s)] #file de priorité

    while priority_queue:
        current_dist, u = heappop(priority_queue) #on retire le noeud
        #on ignore si plus la bonne distance
        if current_dist > dist[u]:
            continue
        for v in range(n):  #on regarde les voisins
            if graph[u][v] > 0: #arête dans le graphe
                # on normalise le cout
                new_cost = cost[u][v] + potential[u] - potential[v]
                new_dist = dist[u] + new_cost
                #relaxation
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heappush(priority_queue, (dist[v], v))

    return dist, parent



def min_cost_flow_dijkstra(graph: List[List[int]],cost: List[List[int]],s: int, t:int) -> Tuple[List[List[int]], List[List[int]], int, int]:
    n = len(graph)
    max_flow = 0
    total_cost = 0
    # potentiels pour normaliser
    potential = [0] * n
     # matrice de flot
    flow = [[0]*n for _ in range(n)]

    while True:
        dist, parent = dijkstra(graph, cost, s, potential)
        if parent[t] == -1:
            break
        # mise à jour des potentiels
        for i in range(n):
            if dist[i] < float("inf"):
                potential[i] += dist[i]
        # trouver flow minimum
        path_flow = float("inf")
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u
            
        max_flow += path_flow
        total_cost += path_flow * potential[t]
        # mise à jour du graphe
        v = t
        while v != s:
            u = parent[v]
            #capacité résiduel
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            #arête inverse ducoût oppposé
            cost[v][u] = -cost[u][v]
            #mise à jour du flot
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

    return flow, graph, max_flow, total_cost
