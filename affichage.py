import os

def draw_graph(graph, name):
    n = len(graph)
    lines = ["digraph " + name + " {", "    rankdir=LR;"]
    for u in range(n):
        for v in range(n):
            if graph[u][v] > 0:
                lines.append(f'    {u} -> {v} [label="{graph[u][v]}"];')
    lines.append("}")
    
    dot_path = f"graphes/{name}.dot"
    pdf_path = f"graphes/{name}"
    os.makedirs("graphes", exist_ok=True)
    with open(dot_path, "w") as f:
        f.write("\n".join(lines))
    os.system(f"dot -Tpdf {dot_path} -o {pdf_path}.pdf")


def draw_flow_graph(original, residual, name, cut=None):
    n = len(original)
    cut_set = set(cut) if cut else set()
    lines = ["digraph " + name + " {", "    rankdir=LR;"]
    for u in range(n):
        for v in range(n):
            if original[u][v] > 0:
                flow = max(0, original[u][v] - residual[u][v])
                capacity = original[u][v]
                label = f"{flow}/{capacity}"
                if (u, v) in cut_set:
                    lines.append(
                        f'    {u} -> {v} [label="{label}", color=red, penwidth=3];'
                    )
                else:
                    lines.append(f'    {u} -> {v} [label="{label}"];')
    lines.append("}")

    dot_path = f"graphes/{name}.dot"
    os.makedirs("graphes", exist_ok=True)
    with open(dot_path, "w") as f:
        f.write("\n".join(lines))
    os.system(f"dot -Tpdf {dot_path} -o graphes/{name}.pdf")


def draw_flow_cost_graph(original, flow, cost, name):
    n = len(original)
    lines = ["digraph " + name + " {", "    rankdir=LR;"]
    for u in range(n):
        for v in range(n):
            if original[u][v] > 0:
                flot = max(0, flow[u][v])
                capacity  = original[u][v]
                edge_cost = cost[u][v]
                label = f"{flot}/{capacity} | c={edge_cost}"
                lines.append(f'    {u} -> {v} [label="{label}"];')
    lines.append("}")

    dot_path = f"graphes/{name}.dot"
    os.makedirs("graphes", exist_ok=True)
    with open(dot_path, "w") as f:
        f.write("\n".join(lines))
    os.system(f"dot -Tpdf {dot_path} -o graphes/{name}.pdf")