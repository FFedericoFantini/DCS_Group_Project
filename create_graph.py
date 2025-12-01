# generate_graph.py

import csv
import math
import json



# ------------------------------------------------------------
# 2D DISTANCE (XY) — Z IGNORED
# ------------------------------------------------------------
def distance(p1, p2):
    return math.dist((p1[0], p1[1]), (p2[0], p2[1]))


# ------------------------------------------------------------
# WEIGHTED GRAPH CONSTRUCTION
# ------------------------------------------------------------
def build_graph(nodes):

    edges = []

    # --------------------------------------------------------
    # Group nodes by A0, A1, A2...
    # --------------------------------------------------------
    aisles = {}
    for node_id, node in nodes.items():
        if node_id.startswith("A"):
            aisle = node_id.split("_")[0]   # "A0"
            aisles.setdefault(aisle, []).append(node)

    aisle_numbers = sorted([int(a[1:]) for a in aisles.keys()])

    # EXTRACT MEETING AND SHIPPING
    meeting = nodes["MEETING_AREA"]
    shipping = nodes["SHIPPING_AREA"]

    # --------------------------------------------------------
    # 1) MEETING_AREA ↔ Ai_F
    # --------------------------------------------------------
    front_meeting_nodes = []
    for a in aisle_numbers:
        fid = f"A{a}_F"
        if fid in nodes:
            fnode = nodes[fid]
            d = distance(meeting.pos, fnode.pos)
            edges.append(("MEETING_AREA", fid, d))
            edges.append((fid, "MEETING_AREA", d))
            front_meeting_nodes.append(fnode)

    # --------------------------------------------------------
    # 2) Connections Ai_F ↔ A(i+1)_F (yellow line)
    # --------------------------------------------------------
    front_meeting_nodes.sort(key=lambda n: n.pos[1])
    for i in range(len(front_meeting_nodes)-1):
        a = front_meeting_nodes[i]
        b = front_meeting_nodes[i+1]
        d = distance(a.pos, b.pos)
        edges.append((a.id, b.id, d))
        edges.append((b.id, a.id, d))

    # --------------------------------------------------------
    # 3) Ai_F ↔ Ai_C_X0
    # --------------------------------------------------------
    for a in aisle_numbers:
        fid = f"A{a}_F"
        cid = f"A{a}_C_X0"
        if fid in nodes and cid in nodes:
            d = distance(nodes[fid].pos, nodes[cid].pos)
            edges.append((fid, cid, d))
            edges.append((cid, fid, d))

    # --------------------------------------------------------
    # 4) Aisle connections Ai_C_Xj ↔ Ai_C_X(j+1) (blue line)
    # --------------------------------------------------------
    for a in aisle_numbers:
        corridor_nodes = [n for n in aisles[f"A{a}"] if "_C_X" in n.id]
        corridor_nodes.sort(key=lambda n: n.pos[0])

        for i in range(len(corridor_nodes)-1):
            c1 = corridor_nodes[i]
            c2 = corridor_nodes[i+1]
            d = distance(c1.pos, c2.pos)
            edges.append((c1.id, c2.id, d))
            edges.append((c2.id, c1.id, d))

    # --------------------------------------------------------
    # 5) Ai_C_Xj ↔ Ai_Xj_Lk (shelves — same aisle)
    # --------------------------------------------------------
    for node_id, node in nodes.items():
        if "_C_X" in node_id:
            aisle = node_id.split("_")[0]   # A0
            x_index = int(node_id.split("_X")[1])
            cnode = node

            # all real shelf levels
            for sid, snode in nodes.items():
                if sid.startswith(aisle) and f"_X{x_index}_L" in sid:
                    d = distance(cnode.pos, snode.pos)
                    edges.append((cnode.id, sid, d))
                    edges.append((sid, cnode.id, d))

    # --------------------------------------------------------
    # 6) Ai_C_Xj ↔ A(i+1)_Xj_Lk (shelves in next aisle)
    # --------------------------------------------------------
    for a in aisle_numbers:
        next_a = a + 1
        if f"A{next_a}" not in aisles:
            continue

        for cid, cnode in nodes.items():
            if cid.startswith(f"A{a}_C_X"):

                j = int(cid.split("_X")[1])

                for sid, snode in nodes.items():
                    if sid.startswith(f"A{next_a}_X{j}_L"):
                        d = distance(cnode.pos, snode.pos)
                        edges.append((cid, sid, d))
                        edges.append((sid, cid, d))

    # --------------------------------------------------------
    # 7) Last aisle node Ai_C_X(max) ↔ Ai_FS
    # --------------------------------------------------------
    for a in aisle_numbers:
        corridor_nodes = [n for n in aisles[f"A{a}"] if "_C_X" in n.id]
        corridor_nodes.sort(key=lambda n: n.pos[0])
        last = corridor_nodes[-1]

        fsid = f"A{a}_FS"
        if fsid in nodes:
            d = distance(last.pos, nodes[fsid].pos)
            edges.append((last.id, fsid, d))
            edges.append((fsid, last.id, d))

    # --------------------------------------------------------
    # 8) Connections Ai_FS ↔ A(i+1)_FS (orange line)
    # --------------------------------------------------------
    front_ship_nodes = [nodes[f"A{a}_FS"] for a in aisle_numbers]
    front_ship_nodes.sort(key=lambda n: n.pos[1])

    for i in range(len(front_ship_nodes)-1):
        a = front_ship_nodes[i]
        b = front_ship_nodes[i+1]
        d = distance(a.pos, b.pos)
        edges.append((a.id, b.id, d))
        edges.append((b.id, a.id, d))

    # --------------------------------------------------------
    # 9) Ai_FS ↔ SHIPPING_AREA
    # --------------------------------------------------------
    for a in aisle_numbers:
        fsid = f"A{a}_FS"
        if fsid in nodes:
            d = distance(nodes[fsid].pos, shipping.pos)
            edges.append((fsid, "SHIPPING_AREA", d))
            edges.append(("SHIPPING_AREA", fsid, d))

    return edges


# ------------------------------------------------------------
# CSV EXPORT
# ------------------------------------------------------------
def save_graph_to_csv(edges, filename):
    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["node_from", "node_to", "distance"])
        for e in edges:
            w.writerow(e)

    print(f"📁 Graph saved to {filename}")

# ------------------------------------------------------------
# ADIACENCY DICTONARY
# ------------------------------------------------------------
def edges_to_graph(edges):
    graph = {}
    for u, v, d in edges:
        if u not in graph:
            graph[u] = {}
        graph[u][v] = d
    return graph

# ------------------------------------------------------------
# SAVED DICTONARY
# ------------------------------------------------------------
def save_graph_json(graph, filename):
    with open(filename, "w") as f:
        json.dump(graph, f, indent=4)
    print(f"📁 Graph saved to {filename}")
