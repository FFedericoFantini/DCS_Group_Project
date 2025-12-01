import csv

def adjacency_matrix_from_edges(edges):
    # Unique nodes
    nodes = sorted(list(set([e[0] for e in edges] + [e[1] for e in edges])))

    # node -> index
    index = {node: i for i, node in enumerate(nodes)}

    # NxN zero matrix
    N = len(nodes)
    M = [[0.0 for _ in range(N)] for _ in range(N)]

    for u, v, d in edges:
        i = index[u]
        j = index[v]
        M[i][j] = d  # weighted adjacency

    return nodes, M


def save_matrix_to_csv(nodes, M, filename):
    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([""] + nodes)
        for node, row in zip(nodes, M):
            w.writerow([node] + row)

    print(f"📁 Adjacency matrix saved to {filename}\n")
