from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from generate_waypoints import generate_warehouse_nodes

from create_floor import create_floor_from_nodes
from create_area import create_area_zone
from create_shelves import create_shelves_from_waypoints
from save_scene import save_scene

from export_nodes import export_nodes_to_coppeliasim, save_waypoints_to_csv

from create_graph import build_graph, save_graph_to_csv, edges_to_graph, save_graph_json
from adjacency_matrix import adjacency_matrix_from_edges, save_matrix_to_csv

import json
# -------------------------------------------------------------
# Removes old floors
# -------------------------------------------------------------
DEFAULT_OBJECT_NAMES = ["Floor","box"]

def clean(sim):
    for handle in range(1, 100):
        try:
            alias = sim.getObjectAlias(handle)
            # Original floors
            if alias in DEFAULT_OBJECT_NAMES or any(name in alias for name in DEFAULT_OBJECT_NAMES):
                sim.removeObject(handle)
        except:
            pass



# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == "__main__":
    # -------- Warehouse parameters ------------
    n_aisles = 5                    # numbero of aisles
    coloums_per_shelf = 20           # number of vertical coloums per each shelf
    levels_per_shelf = 10            # number of levels per each coloum
    aisle_width = 2.0               # width of aisle
    slot_length = 0.5               # lenght of each slot
    base_y = 0.0                    # y cordinates of the first aisle
    shelf_depth = 0.5               # depth of each slot
    shelf_height = 0.4              # height of each slot
    shelf_width = slot_length       # lenght of each slot
    meeting_offset = 1.5            # Meeting area OFFSET towards the left
    shipping_offset = 1.5           # Shipping area OFFSET towards the right

    #----------------------------------------------

    # 1) --------- Create Scene in Coppelia -------
    # Generate nodes
    nodes = generate_warehouse_nodes(
        n_aisles, coloums_per_shelf, levels_per_shelf,
        aisle_width, slot_length, base_y, meeting_offset, shipping_offset
    )
    save_waypoints_to_csv(nodes, "../File_CSV/waypoints.csv")       # Save nodes coordinates into CSV File

    # Connect to CoppeliaSim
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    print("➡ Connection established with CoppeliaSim.")

    sim.loadScene("")   # Load empty scene
    clean(sim)          # Clear scene

    export_nodes_to_coppeliasim(sim, nodes)                     # Create Dummy objects for waypoints

    # Graphic Part
    create_floor_from_nodes(sim, nodes)          # Create floor with correct dimension depends on the layout of the warehouse
    create_area_zone(sim, "MEETING_AREA",nodes["MEETING_AREA"].pos)            # Create graphic rectangle under Meeting Area
    create_area_zone(sim, "SHIPPING_AREA", nodes["SHIPPING_AREA"].pos)          # Create graphic rectangle under Shipping Area
    create_shelves_from_waypoints(sim, nodes, shelf_width, shelf_depth, shelf_height)   # Create shelves from waypoints

    save_scene(sim, "Warehouse.ttt")
    # --------------------------------------------------------

    # 2) ----- Generate the weighted graph -------------------
    edges = build_graph(nodes)
    graph = edges_to_graph(edges)
    save_graph_to_csv(edges, "../File_CSV/graph.csv")
    save_graph_json(graph, "../File_CSV/graph.json")
    # --------------------------------------------------------

    # 3) ------- Generate adjacency matrix -------------------
    nodes_order, M = adjacency_matrix_from_edges(edges)
    save_matrix_to_csv(nodes_order, M, "../File_CSV/adjacency_matrix.csv")
    # --------------------------------------------------------

    # 4) -------- Genera stato iniziale slot (tutti free)------
    slot_nodes = [nid for nid in nodes.keys() if "_X" in nid and "_L" in nid]
    slot_state = {slot: "free" for slot in slot_nodes}

    with open("../File_CSV/slots_state.json", "w") as f:
          json.dump(slot_state, f, indent=4)
    # --------------------------------------------------------


