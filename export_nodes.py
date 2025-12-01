# export_nodes.py
import csv
import os


# -------------------------------------------------------------
# Crea i dummy per i waypoint
# -------------------------------------------------------------
def export_nodes_to_coppeliasim(sim, nodes):
    for node_id, node in nodes.items():
        dummy = sim.createDummy(0.1)
        sim.setObjectAlias(dummy, f"WP_{node_id}")
        sim.setObjectPosition(dummy, -1, node.pos)

    print("✔ Dummy dei waypoint creati.")


def save_waypoints_to_csv(nodes, filename):
    
    # Crea cartella se non esiste
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "x", "y", "z"])  # header
        
        for node_id, node in nodes.items():
            x, y, z = node.pos
            writer.writerow([node_id, x, y, z])

    abs_path = os.path.abspath(filename)

    print(f"📁 Waypoints salvati in {filename}")