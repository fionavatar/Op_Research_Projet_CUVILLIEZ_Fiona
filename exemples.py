from affichage import *
from ford_fulkerson import *
from min_cost_flow import *
from detection_cycle_negatif import detection_cycle_neg
from utils import print_flow, print_cut


def max_flow_min_cut_ford_fulkerson(graph, source, puit):
    log("FORD-FULKERSON", 0)
    # affichage initial
    draw_graph(graph, "graph_initial")
    #sauvegarde du graphe original
    flot_max, residuel, matrice_flots = ford_fulkerson(graph, source, puit)
    # affichages graphiques
    draw_graph(residuel, "graph_residual")
    log(f"\nFlux maximum : {flot_max}", 0)
    print_flow(matrice_flots)
    #sans la cut
    draw_flow_graph(graph, residuel, "graph_flow")
    cut = min_cut(graph, residuel, source)
    #avec la cut
    draw_flow_graph(graph, residuel, "graph_flow", cut)
    print_cut(cut)

    return flot_max, residuel, matrice_flots, cut


def min_cost_bellman_ford (graph, cost, source, puit) :
    matrice_flots, residuel, flot_max, cout_tt = min_cost_flow_bellman_ford(graph, cost, source, puit)
    print("Flot :", flot_max)
    print("Coût :", cout_tt)
    print_flow(matrice_flots)
    draw_graph(residuel, "graph_residual")
    draw_flow_cost_graph(graph, matrice_flots, cost, "graph_flow_cost")


def min_cost_dijkstra (graph, cost, source, sink) :
    if detection_cycle_neg(graph,cost) :
        raise ValueError("cycle négatif détecté")
    matrice_flots, residuel, flot_max, cout_tt = min_cost_flow_dijkstra(graph, cost, source, sink)
    print("Flow :", flot_max)
    print("Cost :", cout_tt)
    print_flow(matrice_flots)
    draw_graph(residuel, "graph_residual")
    draw_flow_cost_graph(graph, matrice_flots, cost, "graph_flow_cost")



def exempleFF():
    capacities0 = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]

    capacities1 = [
       # s, a, b, c, d, e, t
        [0, 4, 0, 0, 0, 9, 0], #s
        [0, 0, 2, 0, 3, 0, 0], #a
        [0, 0, 0, 4, 0, 0, 10], #b
        [0, 0, 0, 0, 0, 0, 1], #c
        [0, 0, 0, 1, 0, 0, 3], #d
        [0, 0, 0, 0, 8, 0, 0], #e
        [0, 0, 0, 0, 0, 0, 0] #t
    ]
    # 1) FORD_FULKERSON
    max_flow_min_cut_ford_fulkerson(capacities0, 0, 5)
    max_flow_min_cut_ford_fulkerson(capacities1, 0, 6)

def exempleMinCostPosD() :
    # 2) min cost flow algo pour repeated augmenting paths 
    capacities = [
    [0, 3, 4, 5, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 4, 1],
    [0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0]]
    cost = [
    [0, 1, 2, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 4, 9],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]]

    print("dijkstra")
    min_cost_dijkstra(capacities, cost, 0, 4)

def exempleMinCostPosB() :
    # 2) min cost flow algo pour repeated augmenting paths 
    capacities = [
    [0, 3, 4, 5, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 4, 1],
    [0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0]]
    cost = [
    [0, 1, 2, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 4, 9],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]]

    print("bellman ford")
    min_cost_bellman_ford(capacities, cost, 0, 4) 


def exempleMinCostNegD() :
    #coût négatif
    capacities = [
    [0, 5, 8, 0],
    [0, 0, 0, 6],
    [0, 2, 0, 5],
    [0, 0, 0, 0]]

    cost = [
    [0, 4, 1, 0],
    [0, 0, 0, 2],
    [0, -3, 0, 5],
    [0, 0, 0, 0]]

    print("dijkstra")
    min_cost_dijkstra(capacities, cost, 0, 3) 

def exempleMinCostNegB() :
    #coût négatif
    capacities = [
    [0, 5, 8, 0],
    [0, 0, 0, 6],
    [0, 2, 0, 5],
    [0, 0, 0, 0]]

    cost = [
    [0, 4, 1, 0],
    [0, 0, 0, 2],
    [0, -3, 0, 5],
    [0, 0, 0, 0]]

    print("bellmanford")
    min_cost_bellman_ford(capacities, cost, 0, 3) 

def exempleMinCostCycleD() :
    #cycle négatif
    cost = [
    [0,  1,  0],
    [0,  0, -4],
    [2,  0,  0]]
    
    capacities = [
    [0,  5,  0],
    [0,  0, 5],
    [5,  0,  0]]

    print("dijkstra")
    min_cost_dijkstra(capacities, cost, 0, 2) 

def exempleMinCostCycleB() :
    #cycle négatif
    cost = [
    [0,  1,  0],
    [0,  0, -4],
    [2,  0,  0]]
    
    capacities = [
    [0,  5,  0],
    [0,  0, 5],
    [5,  0,  0]]

    print("bellmanford")
    min_cost_bellman_ford(capacities, cost, 0, 2) 


if __name__ == "__main__":
    #1) Ford Fulkerson - MaxFlow MinCut
    exempleFF()
    #2) Dijkstra - Coûts Positifs
    exempleMinCostPosD()
    #2) BellmanFord - Coûts Positifs
    exempleMinCostPosB()
    #2) Dijkstra - Coûts Négatifs
    exempleMinCostNegD()
    #2) BellmanFord - Coûts Négatifs
    exempleMinCostNegB()
    #2) Dijkstra - Cycle négatif
    exempleMinCostCycleD()
    #2) BellmanFord - Cycle négatif
    exempleMinCostCycleB()












    

