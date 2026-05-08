from affichage import *
from ford_fulkerson import *
from min_cost_flow import *
import copy

DEBUG = True

def log(msg: str, level: int) -> None:
    if DEBUG:
        print("    " * level + msg)


def print_flow(flow):
    log("\nFlot sur chaque arc :", 0)
    n = len(flow)
    for i in range(n):
        for j in range(n):
            if flow[i][j] > 0:
                log(f"{i} -> {j} : {flow[i][j]}", 1)


def print_cut(cut):
    log("\nMin cut :", 0)
    for u, v in cut:
        log(f"{u} -> {v}", 1)


def run_ff(graph, source, sink):
    log("FORD-FULKERSON", 0)
    # affichage initial
    draw_graph(graph, "graph_initial")
    #sauvegarde du graphe original
    original_graph = copy.deepcopy(graph) 
    max_flow, residual, flow = ford_fulkerson(graph, source, sink)
    # affichages graphiques
    draw_graph(residual, "graph_residual")
    log(f"\nFlux maximum : {max_flow}", 0)
    print_flow(flow)
    #sans la cut
    #draw_flow_graph(original_graph, residual, "graph_flow")
    cut = min_cut(original_graph, residual, source)
    #avec la cut
    draw_flow_graph(original_graph, residual, "graph_flow", cut)
    print_cut(cut)

    return max_flow, residual, flow, cut


def run_mcf_bf (graph, cost, source, sink) :
    original_graph = copy.deepcopy(graph) 
    flow, residual, maxflow, total_cost = min_cost_flow_bellman_ford(graph, cost, source, sink)
    print("Flow :", maxflow)
    print("Cost :", total_cost)
    print_flow(flow)
    draw_graph(residual, "graph_residual")
    draw_flow_cost_graph(original_graph, flow, cost, "graph_flow_cost")



if __name__ == "__main__":

    graph0 = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]

    graph1 = [
        [0, 20, 30, 10, 0],
        [0, 0, 40, 0, 30],
        [0, 0, 0, 10, 20],
        [0, 0, 5, 0, 20],
        [0, 0, 0, 0, 0]
    ]

    graph2 = [
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
    #run_ff(graph0, 0, 5)
    #run_ff(graph1, 0, 4)
    #run_ff(graph2, 0, 6)

    # 2) min cost flow algo pour repeated augmenting paths 
    capacity0 = [
    [0, 3, 4, 5, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 4, 1],
    [0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0]
    ]
    cost0 = [
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    
    capacity1 = [
    [0, 1, 0, 0, 2],
    [0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]
    ]
    cost1 = [
        [0, 3, 1, 0, 3],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 1, 6],
        [0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0]
    ]

    capacity2 = [ 
            [ 0, 3, 1, 0, 3 ], 
            [ 0, 0, 2, 0, 0 ], 
            [ 0, 0, 0, 1, 6 ], 
            [ 0, 0, 0, 0, 2 ],
            [ 0, 0, 0, 0, 0 ] ]

    cost2 = [ [ 0, 1, 0, 0, 2 ], 
             [ 0, 0, 0, 3, 0 ], 
             [ 0, 0, 0, 0, 0 ], 
             [ 0, 0, 0, 0, 1 ],
             [ 0, 0, 0, 0, 0 ] ]  
     
    # 2.1) Avec algo de chemin et coût négatif 
    #resultat -> max flow 10 et min cost 1
    #run_mcf_bf(capacity0,cost0,0,4)
    #run_mcf_bf(capacity1, cost1, 0, 4)
    #resultat -> max flow 6 et min cost 8
    run_mcf_bf(capacity2, cost2, 0, 4)


    # 2.2) Avec Dijkstra et renormalisation des coûts 











    

