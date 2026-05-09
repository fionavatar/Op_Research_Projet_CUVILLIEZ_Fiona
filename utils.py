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


