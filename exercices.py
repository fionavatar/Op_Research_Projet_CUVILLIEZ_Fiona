from affichage import *
from ford_fulkerson import *
from min_cost_flow import *
from utils import print_flow, print_cut
import copy


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
    print(matrice_flots)
    print(residuel)
    draw_flow_graph(graph, residuel, "graph_flow")
    cut = min_cut(graph, residuel, source)
    #avec la cut
    draw_flow_graph(graph, residuel, "graph_flow_cut", cut)
    print_cut(cut)
    return flot_max, residuel, matrice_flots, cut


def min_cost_bellman_ford (graph, cost, source, puit) :
    matrice_flots, residuel, flot_max, cout_tt = min_cost_flow_bellman_ford(graph, cost, source, puit)
    print("Flot :", flot_max)
    print("Coût :", cout_tt)
    print_flow(matrice_flots)
    draw_graph(residuel, "graph_residual_bf")
    draw_flow_cost_graph(graph, matrice_flots, cost, "graph_flow_cost_bf")

    return  matrice_flots, residuel, flot_max, cout_tt

def min_cost_dijkstra (graph, cost, source, sink) :
    matrice_flots, residuel, flot_max, cout_tt = min_cost_flow_dijkstra(graph, cost, source, sink)
    print("Flow :", flot_max)
    print("Cost :", cout_tt)
    print_flow(matrice_flots)
    draw_graph(residuel, "graph_residual_dij")
    draw_flow_cost_graph(graph, matrice_flots, cost, "graph_flow_cost_dij")

    return  matrice_flots, residuel, flot_max, cout_tt

def lists_to_matrix(start_nodes, end_nodes, capacities, unit_costs=None) :
    n = max(max(start_nodes), max(end_nodes)) + 1
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    cost_matrix = [[0 for _ in range(n)] for _ in range(n)]
    if unit_costs :
        assert len(start_nodes)==len(end_nodes)==len(capacities)==len(unit_costs)
    else :
        assert len(start_nodes)==len(end_nodes)==len(capacities)

    for i in range(len(start_nodes)) : 
        matrix[start_nodes[i]][end_nodes[i]] = capacities[i]
        if unit_costs :
            cost_matrix[start_nodes[i]][end_nodes[i]] = unit_costs[i]

        
    return matrix, cost_matrix

def link_assignements(costs, task_capacity):
    people = len(costs)
    tasks = len(costs[0])
    n = 1 + people + tasks + 1 # super-source +  10 personnes + 8 tâches + super-puits
    super_source = 0
    super_puit = n - 1

    capacity = [[0]*n for _ in range(n)]
    cost_matrix = [[0]*n for _ in range(n)]

    # source -> people
    for p in range(people):
        person_node = p + 1
        capacity[super_source][person_node] = 1

    # people -> tasks
    for p in range(people):
        person_node = p + 1
        for t in range(tasks):
            task_node = people + 1 + t
            capacity[person_node][task_node] = 1
            cost_matrix[person_node][task_node] = costs[p][t]

    # tasks -> sink
    for t in range(tasks):
        task_node = people + 1 + t
        capacity[task_node][super_puit] = task_capacity
    return capacity, cost_matrix, super_source, super_puit


def link_assignments_lower_bound(costs):
    people = len(costs)
    tasks = len(costs[0])

    n = 1 + people + tasks + 1 # super-source +  10 personnes + 8 tâches + super-puits
    super_source = 0
    super_puit = n - 1

    capacity = [[0]*n for _ in range(n)]
    cost_matrix = [[0]*n for _ in range(n)]

    task_nodes = [people + 1 + t for t in range(tasks)]

    # 1) source -> people
    for p in range(people):
        capacity[super_source][p+1] = 1

    # 2) people -> tasks
    for p in range(people):
        for t in range(tasks):
            u = p + 1
            v = task_nodes[t]
            capacity[u][v] = 1
            cost_matrix[u][v] = costs[p][t]

    # 3) LOWER BOUND = on force 1 personne par tâche
    for t in range(tasks):
        capacity[task_nodes[t]][super_puit] = 1   # reste après le "minimum"

    # 4) on ajoute un pré-flot obligatoire (1 par tâche)
    forced_flow_cost = 0

    return capacity, cost_matrix, super_source, super_puit, forced_flow_cost

def lower_upper_cap(costs, min_per_task=1, max_per_task=2):
    people = len(costs)
    tasks = len(costs[0])

    n = 1 + people + tasks + 1
    source = 0
    sink = n - 1

    capacity = [[0]*n for _ in range(n)]
    cost_matrix = [[0]*n for _ in range(n)]

    task_nodes = [people + 1 + t for t in range(tasks)]

    # source -> people
    for p in range(people):
        capacity[source][p+1] = 1

    # people -> tasks
    for p in range(people):
        for t in range(tasks):
            u = p + 1
            v = task_nodes[t]

            capacity[u][v] = 1
            cost_matrix[u][v] = costs[p][t]

    # tasks -> sink (capacité MAX - MIN)
    for t in range(tasks):
        capacity[task_nodes[t]][sink] = max_per_task - min_per_task

    return capacity, cost_matrix, source, sink, tasks * min_per_task


def exo1() :
    start_nodes = [0, 0, 0, 1, 1, 2, 2, 3, 3]
    end_nodes = [1, 2, 3, 2, 4, 3, 4, 2, 4]
    capacities = [20, 30, 10, 40, 30, 10, 20, 5, 20]

    """
    capacities = [
            [0, 20, 30, 10, 0],
            [0, 0, 40, 0, 30],
            [0, 0, 0, 10, 20],
            [0, 0, 5, 0, 20],
            [0, 0, 0, 0, 0]]
    """
    matrix_cap, _ = lists_to_matrix(start_nodes, end_nodes, capacities)
    print(matrix_cap)
    max_flow_min_cut_ford_fulkerson(matrix_cap, 0, 4)



def exo2():
    cost = [ 
        [90, 76, 75, 70, 50, 74, 12, 68], 
          [35, 85, 55, 65, 48, 101, 70, 83],
          [125, 95, 90, 105, 59, 120, 36, 73],
          [45, 110, 95, 115, 104, 83, 37, 71],
          [60, 105, 80, 75, 59, 62, 93, 88],
          [45, 65, 110, 95, 47, 31, 81, 34],
          [38, 51, 107, 41, 69, 99, 115, 48],
          [47, 85, 57, 71, 92, 77, 109, 36],
          [39, 63, 97, 49, 118, 56, 92, 61],
          [47, 101, 71, 60, 88, 109, 52, 90],]
    #2,1)
    #on suppose que une personne peut avoir toutes les tâches -> 10
    no_task_capacity, cost_matrix, super_source, super_puit = link_assignements(cost, 10)
    min_cost_bellman_ford (no_task_capacity, cost_matrix, 0, 19)
    # 2,2) With a task capacity of 2 for each task
    no_task_capacity, cost_matrix, super_source, super_puit = link_assignements(cost, 2)
    min_cost_bellman_ford (no_task_capacity, cost_matrix, 0, 19)
    # 2)Such that each task is taken at most one
    #no_task_capacity, cost_matrix, super_source, super_puit = link_assignements(cost, 1)
    #min_cost_bellman_ford (no_task_capacity, cost_matrix, 0, 19)
    # 2,3)	Such that each task is taken at least one
    cap, cost_m, s, t, forced = lower_upper_cap(cost)
    mat_flows, residual, flow, cost = min_cost_bellman_ford(cap,cost_m,s,t)
    print("Flot total:", flow + forced)
    print("Coût total:", cost)

"""
#exo3 
start_nodes_costs = [ 0, 0,  1, 1,  1,  2, 2,  3, 4]
end_nodes_costs = [ 1, 2,  2, 3,  4,  3, 4,  4, 2]
capacities_costs  = [15, 8, 20, 4, 10, 15, 4, 20, 5]
unit_costs  = [ 4, 4,  2, 2,  6,  1, 3,  2, 3]
"""
#Add a source s links to node 0 with a capacity 20
# a sink t with arc (3,t) with capacity 5 and arc (4,t) with capacity 15
start_nodes_costs = [ 0, 0,  1, 1,  1,  2, 2,  3, 4, 5, 3, 4] # 5-> s et 6 -> t
end_nodes_costs = [ 1, 2,  2, 3,  4,  3, 4,  4, 2, 0, 6, 6]
capacities_costs  = [15, 8, 20, 4, 10, 15, 4, 20, 5, 20, 5, 15]
unit_costs  = [ 4, 4,  2, 2,  6,  1, 3,  2, 3, 0, 0, 0]  


def exo3():

    matrix_cap, cost_matrix = lists_to_matrix(start_nodes_costs, end_nodes_costs, capacities_costs, unit_costs)
    print(matrix_cap)
    print(cost_matrix)
    #1)	Search for the max flow min cost in (t,s)
    min_cost_bellman_ford (matrix_cap, cost_matrix, 5, 6) #-> Flot : 20 et Coût : 150
    min_cost_dijkstra (matrix_cap, cost_matrix, 5, 6)
    #2) Search fpr the max flow min cost in (0,4)
    #min_cost_bellman_ford (matrix_cap, cost_matrix, 0, 4) #-> Flot : 23 et Coût : 187
    #min_cost_dijkstra (matrix_cap, cost_matrix, 0, 4)


def exo3_3(): 
    #3)	Compute the most vital arc for the max flow (t,s) : that is the arc thus such that it s removal reduces the flow by the maximum value
    #évidemment c'est s(5)->0 avec une capacité de 20 sans cette arête il n'y a pas de flot de s à t
    flot_maximal = float("inf")
    arrete = [0,0] #[u,v] = u->v
    for i in range(len(start_nodes_costs)) :
        start_nodes_costs_2  = copy.deepcopy(start_nodes_costs)
        end_nodes_costs_2  = copy.deepcopy(end_nodes_costs)
        capacities_costs_2  = copy.deepcopy(capacities_costs)
        unit_costs_2  = copy.deepcopy(unit_costs)

        capacities_costs_2[i] = 0 #on remplace par une capacité 0

        matrix_cap_2, cost_matrix_2 = lists_to_matrix(start_nodes_costs_2, end_nodes_costs_2, capacities_costs_2, unit_costs_2)
        matrice_flots, residuel, flot_max, cout_tt = min_cost_bellman_ford (matrix_cap_2, cost_matrix_2, 5, 6)
        print(flot_max)

        if flot_max<flot_maximal :
            flot_maximal = flot_max
            arrete = [start_nodes_costs[i], end_nodes_costs[i]]
    print(f"L'arrête vitale est {arrete[0]}->{arrete[1]} qui donne un flot maximal de {flot_maximal}")



if __name__ == "__main__":
    #1) Max flow pb
    #exo1()
    """
    Flot maximum : 60
    résultats :
    taille de la coupe : 3
    Min cut :
        0 -> 1
        0 -> 2
        0 -> 3

    flots = [[0, 20, 30, 10, 0], 
             [-20, 0, 0, 0, 20], 
             [-30, 0, 0, 10, 20], 
             [-10, 0, -10, 0, 20], 
             [0, -20, -20, -20, 0]]
    résiduel = [[0, 0, 0, 0, 0], 
                [20, 0, 40, 0, 10], 
                [30, 0, 0, 0, 0], 
                [10, 0, 15, 0, 0], 
                [0, 20, 20, 20, 0]]
    """
    #2) Min cost flow assignment problem
    exo2()
    #2,1) Flot : 10 et Coût : 370
    #2,2) Flot : 10 etCoût : 404
    #2,3) Flot : 16 et  Coût : 338

    #3) Min cost flow problem
    #exo3()
    #1 -> Flot : 20 et Coût : 150
    #2 -> -> Flot : 23 et Coût : 187
    #exo3_3()
    #c'est s(5)->0 avec une capacité de 20 sans cette arête il n'y a pas de flot de s à t

