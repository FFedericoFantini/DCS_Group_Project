# create_shelves.py


def create_shelves_from_waypoints(sim, nodes, shelf_width, shelf_depth, shelf_height):
    """
    Crea scaffali in CoppeliaSim in base ai waypoint.
    """
    for node_id, node in nodes.items():
        # Solo i nodi che rappresentano un livello di scaffale
        if "_L" in node_id:
            x, y, z = node.pos

            # Crea il cuboid
            shelf = sim.createPureShape(
                0,                                 # cuboid
                0,                                 # options
                [shelf_width, shelf_depth, shelf_height],
                0                                  # statico
            )
            sim.setObjectInt32Param(shelf, sim.shapeintparam_respondable, 0)
            sim.setObjectInt32Param(shelf, sim.shapeintparam_static, 1)
            sim.setObjectAlias(shelf, f"SHELF_{node_id}")

            # posizionamento
            sim.setObjectPosition(shelf, -1, [x, y, z + shelf_height/2])

            # colore
            sim.setShapeColor(shelf, None, sim.colorcomponent_ambient_diffuse, [0.7, 0.7, 0.7])

            # trasparenza
            sim.setShapeColor(shelf, None, sim.colorcomponent_transparency, [0.3])
