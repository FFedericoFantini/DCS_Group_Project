import os
import numpy as np
import pandas as pd
import networkx as nx


def save_weighted_adjacency_matrix(graph_csv_path, waypoints_csv_path, output_csv_path):
    # ------------------------------
    # 1. Carica waypoints (ordine nodi)
    # ------------------------------
    wp = pd.read_csv(waypoints_csv_path)
    node_list = wp["id"].tolist()

    # ------------------------------
    # 2. Carica grafo pesato
    # ------------------------------
    G = nx.DiGraph()
    for node in node_list:
        G.add_node(node)

    edges_df = pd.read_csv(graph_csv_path)
    for _, row in edges_df.iterrows():
        G.add_edge(row["node_from"], row["node_to"], weight=row["distance"])

    # ------------------------------
    # 3. Genera matrice pesata NxN
    # ------------------------------
    N = len(node_list)
    A = np.zeros((N, N))

    for i, u in enumerate(node_list):
        for j, v in enumerate(node_list):
            if G.has_edge(u, v):
                A[i, j] = G[u][v]["weight"]

    # ------------------------------
    # 4. Crea cartella se non esiste
    # ------------------------------
    folder = os.path.dirname(output_csv_path)
    os.makedirs(folder, exist_ok=True)

    # ------------------------------
    # 5. Salva CSV
    # ------------------------------
    df_adj = pd.DataFrame(A, index=node_list, columns=node_list)
    df_adj.to_csv(output_csv_path)

    print(f"📘 Matrice di adiacenza pesata salvata in: {output_csv_path}\n")
