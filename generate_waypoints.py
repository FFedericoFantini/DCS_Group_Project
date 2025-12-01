# generate_waypoints.py

class Node:
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos


def generate_warehouse_nodes(
        n_aisles, 
        coloums_per_shelf, 
        levels_per_shelf,
        aisle_width, 
        slot_length, 
        base_y,
        meeting_offset,
        shipping_offset
    ):

    nodes = {}

    # -------------------------------------------------------
    # 1) Calcolo zona centrale Y
    # -------------------------------------------------------
    y_center = base_y + (n_aisles * aisle_width) / 2.0

    # Coordinate X limite scaffali
    x_min = 0
    x_max = (coloums_per_shelf - 1) * slot_length

    # -------------------------------------------------------
    # 2) FRONT MEETING / SHIPPING (a distanza fissa fuori corsia)
    # -------------------------------------------------------
    FRONT_MARGIN = 0.5   # margine costante per NON entrare nella corsia

    x_front_meet = x_min - FRONT_MARGIN
    x_front_ship = x_max + FRONT_MARGIN

    # -------------------------------------------------------
    # 3) MEETING_AREA e SHIPPING_AREA con OFFSET
    # -------------------------------------------------------
    nodes["MEETING_AREA"] = Node(
        "MEETING_AREA",
        (x_front_meet - meeting_offset, y_center, 0)
    )

    nodes["SHIPPING_AREA"] = Node(
        "SHIPPING_AREA",
        (x_front_ship + shipping_offset, y_center, 0)
    )

    # -------------------------------------------------------
    # 4) NODI PER OGNI CORSIA
    # -------------------------------------------------------
    for a in range(n_aisles):

        y_shelf = base_y + a * aisle_width
        y_mid = y_shelf + aisle_width * 0.5

        # 1️⃣ SCAFFALI
        for j in range(coloums_per_shelf):
            x = j * slot_length
            for l in range(levels_per_shelf):
                z = l * 0.4
                nid = f"A{a}_X{j}_L{l}"
                nodes[nid] = Node(nid, (x, y_shelf, z))

        # 2️⃣ CORSIA
        for j in range(coloums_per_shelf):
            x = j * slot_length
            nid = f"A{a}_C_X{j}"
            nodes[nid] = Node(nid, (x, y_mid, 0))

        # 3️⃣ MIDPOINT
        for j in range(coloums_per_shelf - 1):
            x = (j + 0.5) * slot_length
            nid = f"A{a}_M_X{j}"
            nodes[nid] = Node(nid, (x, y_mid, 0))

        # 4️⃣ FRONT MEETING (posizione corretta e fissa, MAI dentro corsia)
        front_id = f"A{a}_F"
        nodes[front_id] = Node(front_id, (x_front_meet, y_mid, 0))

        # 5️⃣ FRONT SHIPPING (posizione corretta e fissa)
        fs_id = f"A{a}_FS"
        nodes[fs_id] = Node(fs_id, (x_front_ship, y_mid, 0))

    return nodes
