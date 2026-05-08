from graphviz import Digraph


def draw_graph(graph, name):
    dot = Digraph()
    n = len(graph)

    for u in range(n):
        for v in range(n):
            if graph[u][v] > 0:
                dot.edge(str(u), str(v), label=str(graph[u][v]))

    dot.render(name, view=True)



def draw_flow_graph(original, residual, name, cut=None):
    dot = Digraph()
    n = len(original)
    cut_set = set(cut) if cut else set()
    for u in range(n):
        for v in range(n):
            if original[u][v] > 0:
                flow = original[u][v] - residual[u][v]
                capacity = original[u][v]
                label = f"{flow}/{capacity}"

                edge = (u, v)

                # si dans min-cut
                if edge in cut_set:
                    dot.edge(str(u), str(v), label=label, color="red", penwidth="3")
                else:
                    dot.edge(str(u), str(v), label=label)

    dot.render(name, view=True)



def draw_flow_cost_graph(original, flow, cost, name):
    dot = Digraph()
    n = len(original)
    for u in range(n):
        for v in range(n):
            if original[u][v] > 0:
                # capacité initiale
                capacity = original[u][v]
                # coût
                edge_cost = cost[u][v]
                # label complet
                label = f"{flow[u][v]}/{capacity} | c={edge_cost}"
                dot.edge(
                    str(u),
                    str(v),
                    label=label
                )

    dot.render(name, view=True)