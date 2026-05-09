from heapq import heappush, heappop
from typing import List, Tuple
import copy

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
    residual  = copy.deepcopy(graph) #copie du réseau d'origine pour créer le résiduel
    couts  = copy.deepcopy(cost) #copie des couts
    #étape 1 : initialisation
    n = len(residual)
    flot_max = 0
    cout_tt = 0
    # matrice de flot
    matrice_flots = [[0]*n for _ in range(n)]

    #étape 2
    while True:
        dist, parent = bellman_ford(residual, couts, s) #plus court chemin
        #plus de chemin augmentant
        if parent[t] == -1:
            break
        #calcul du flot du chemin
        chemin = float("inf")
        v = t
        while v != s:
            u = parent[v]
            chemin = min(chemin, residual[u][v])
            v = u
        flot_max += chemin
        cout_tt += chemin * dist[t]
        #mise à jour du graphe résiduel
        v = t
        while v != s:
            u = parent[v]
            #capacité résiduel
            residual[u][v] -= chemin
            residual[v][u] += chemin
            #arête inverse ducoût oppposé
            couts[v][u] = -couts[u][v]
            #mise à jour du flot
            matrice_flots[u][v] += chemin
            matrice_flots[v][u] -= chemin
            v = u

    return matrice_flots, residual, flot_max, cout_tt


#2ème approche avec l'algorithme de Dijkstra
def dijkstra(graph: List[List[int]], cost: List[List[int]],s: int, h: List[int]) -> Tuple[List[float], List[int]]:
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
                new_cost = cost[u][v] + h[u] - h[v]
                new_dist = dist[u] + new_cost
                #relaxation
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heappush(priority_queue, (dist[v], v))

    return dist, parent



def min_cost_flow_dijkstra(graph: List[List[int]],cost: List[List[int]],s: int, t:int) -> Tuple[List[List[int]], List[List[int]], int, int]:
    residual  = copy.deepcopy(graph) #copie du réseau d'origine pour créer le résiduel
    couts  = copy.deepcopy(cost) #copie des couts
    n = len(residual)
    flot_max = 0
    cout_tt = 0
    # pour normaliser les coûts négatifs
    h = [0]*n
     # matrice de flot
    matrice_flots = [[0]*n for _ in range(n)]

    while True:
        dist, parent = dijkstra(residual, couts, s, h)
        if parent[t] == -1:
            break
        # mise à jour normalisation
        for i in range(n):
            if dist[i] < float("inf"):
                h[i] += dist[i]
        # trouver flow minimum
        chemin = float("inf")
        v = t
        while v != s:
            u = parent[v]
            chemin = min(chemin, residual[u][v])
            v = u

        flot_max += chemin
        # mise à jour du graphe
        v = t
        while v != s:
            u = parent[v]
            cout_tt += chemin * couts[u][v]
            #capacité résiduel
            residual[u][v] -= chemin
            residual[v][u] += chemin
            #arête inverse du coût oppposé
            couts[v][u] = -couts[u][v]
            #mise à jour du flot
            matrice_flots[u][v] += chemin
            matrice_flots[v][u] -= chemin
            v = u

    return matrice_flots, residual, flot_max, cout_tt
