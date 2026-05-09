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


if __name__ == "__main__":
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
    #run_ff(capacities0, 0, 5)
    #run_ff(capacities1, 0, 6)

    # 2) min cost flow algo pour repeated augmenting paths 
    capacities2 = [
    [0, 3, 4, 5, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 4, 1],
    [0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0]]
    cost2 = [
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]
    

    capacities3 = [
    [0, 1, 0, 0, 2],
    [0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]]

    cost5 = [
        [0, 3, 1, 0, 3],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 1, 6],
        [0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0]]

    capacities4 = [ 
            [ 0, 3, 1, 0, 3 ], 
            [ 0, 0, 2, 0, 0 ], 
            [ 0, 0, 0, 1, 6 ], 
            [ 0, 0, 0, 0, 2 ],
            [ 0, 0, 0, 0, 0 ] ]

    cost4 = [ [ 0, 1, 0, 0, 2 ], 
             [ 0, 0, 0, 3, 0 ], 
             [ 0, 0, 0, 0, 0 ], 
             [ 0, 0, 0, 0, 1 ],
             [ 0, 0, 0, 0, 0 ] ]  
    
    #coût négatif
    capacities5 = [
    [0, 5, 8, 0],
    [0, 0, 0, 6],
    [0, 2, 0, 5],
    [0, 0, 0, 0]]

    cost5 = [
    [0, 4, 1, 0],
    [0, 0, 0, 2],
    [0, -3, 0, 5],
    [0, 0, 0, 0]]

    #cycle négatif
    cost6 = [
    [0,  1,  0],
    [0,  0, -4],
    [2,  0,  0]]
    
    capacities6 = [
    [0,  5,  0],
    [0,  0, 5],
    [5,  0,  0]]

    capacities7 = [
    [0, 10, 8, 0],
    [0, 0, 5, 10],
    [0, 0, 0, 10],
    [0, 0, 0, 0]]

    cost7 = [
    [0, 2, 4, 0],
    [0, 0, 1, 2],
    [0, 0, 0, 1],
    [0, 0, 0, 0]]

    # 2.1) Avec algo de chemin et coût négatif 
    #resultat -> max flow 10 et min cost 1
    #run_mcf_bf(capacity0,cost0,0,4)
    #run_mcf_bf(capacity1, cost1, 0, 4)
    #resultat -> max flow 6 et min cost 8
    print("bellman ford")
    #min_cost_bellman_ford(capacities6, cost6, 0, 2) #ValueError("cycle négatif détecté")
    min_cost_bellman_ford(capacities5, cost5, 0, 3)
    min_cost_bellman_ford(capacities7, cost7, 0, 3)


    # 2.2) Avec Dijkstra et renormalisation des coûts 
    print("dijkstra")
    min_cost_dijkstra(capacities5, cost5, 0, 3)
    min_cost_dijkstra(capacities7, cost7, 0, 3)











    

