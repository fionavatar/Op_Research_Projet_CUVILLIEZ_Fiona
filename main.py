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
    print("bellman ford")
    min_cost_bellman_ford(capacities7, cost7, 0, 3)

    # 2.2) Avec Dijkstra et renormalisation des coûts 
    print("dijkstra")
    min_cost_dijkstra(capacities7, cost7, 0, 3)
 











    

