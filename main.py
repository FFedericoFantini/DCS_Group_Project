from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from generate_waypoints import generate_warehouse_nodes
from create_floor import create_floor_from_nodes
from export_nodes import export_nodes_to_coppeliasim, save_waypoints_to_csv
from create_area import create_area_zone
from create_shelves import create_shelves_from_waypoints
from save_scene import save_scene
from adjancency_matrix import save_weighted_adjacency_matrix
from create_graph import build_graph, save_graph_to_csv


# -------------------------------------------------------------
# Rimuove vecchi floor
# -------------------------------------------------------------
DEFAULT_OBJECT_NAMES = ["Floor","box"]

def clean(sim):
    for handle in range(1, 100):
        try:
            alias = sim.getObjectAlias(handle)
            # Floor originali
            if alias in DEFAULT_OBJECT_NAMES or any(name in alias for name in DEFAULT_OBJECT_NAMES):
                sim.removeObject(handle)
        except:
            pass



# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == "__main__":
    # -------- Parametri magazzino ------------
    n_aisles = 2
    coloums_per_shelf = 6
    levels_per_shelf = 3
    aisle_width = 2.0
    slot_length = 0.5
    base_y = 0.0
    shelf_depth = 0.5
    shelf_height = 0.4
    shelf_width = slot_length
    meeting_offset = 1.5       # OFFSET meeting area verso sinistra
    shipping_offset = 1.5      # OFFSET shipping area verso destra
    #----------------------------------------------

    # 1) --------- Crea Scena su Coppelia -------
    # Genera nodi
    nodes = generate_warehouse_nodes(n_aisles, coloums_per_shelf, levels_per_shelf, aisle_width, slot_length, base_y , meeting_offset, shipping_offset )

    # Connetti a CoppeliaSim
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    print("➡ Connessione stabilita con CoppeliaSim.\n")

    sim.loadScene("")   # Carica scena vuota
    clean(sim)          # Pulire Scena

    # Crea floor automatico
    create_floor_from_nodes(sim, nodes)

    # Crea Dummy per waypoint
    export_nodes_to_coppeliasim(sim, nodes)

    # salva i nodi nel CSV
    save_waypoints_to_csv(nodes, "File_CSV/waypoints.csv")

    # Crea rettangolo grafico sotto Meeting Area
    create_area_zone(sim, nodes["MEETING_AREA"].pos)

    # Crea rettangolo grafico sotto Shipping Area
    create_area_zone(sim, nodes["SHIPPING_AREA"].pos)

    # Crea scaffali dai waypoint
    create_shelves_from_waypoints(sim, nodes,shelf_width, shelf_depth, shelf_height)

    print("\n✔ Scena creata.")
    save_scene(sim,"Warehouse.ttt")
    # --------------------------------------------------------



    # 2) ----- Genera il grafo pesato -------------------------
    edges = build_graph(nodes)
    save_graph_to_csv(edges, "File_CSV/graph.csv")
    print("✔ Grafo creato.\n")
    # --------------------------------------------------------

    # 3) ------- Genera matrice di adiacenza -----------------
    save_weighted_adjacency_matrix(
    "File_CSV/graph.csv",
    "File_CSV/waypoints.csv",
    "File_CSV/adjacency_matrix.csv"
    )
    # ---------------------------------------------------------



