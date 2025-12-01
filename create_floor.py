# create_floor.py


def create_floor_from_nodes(sim, nodes, margin=1.0, transparency=0.6):
    # --- Calcolo dimensioni ---
    xs = [node.pos[0] for node in nodes.values()]
    ys = [node.pos[1] for node in nodes.values()]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    floor_x = (x_max - x_min) + 2 * margin
    floor_y = (y_max - y_min) + 2 * margin
    floor_z = 0.05

    # Centro del floor
    cx = (x_min + x_max) / 2
    cy = (y_min + y_max) / 2
    cz = -0.03  # leggermente sotto lo zero

    # --- Creazione cuboid floor ---
    floor = sim.createPureShape(
        0,           # cuboid
        0,           # options
        [floor_x, floor_y, floor_z],
        0            # statico
    )
    sim.setObjectInt32Param(floor, sim.shapeintparam_respondable, 1)
    sim.setObjectInt32Param(floor, sim.shapeintparam_static, 1)
    sim.setObjectAlias(floor, "AUTO_FLOOR")
    sim.setObjectPosition(floor, -1, [cx, cy, cz])

    # Colore e trasparenza
    sim.setShapeColor(floor, None, sim.colorcomponent_ambient_diffuse, [0.8, 0.8, 0.8])
    sim.setShapeColor(floor, None, sim.colorcomponent_transparency, [transparency])

    return floor
