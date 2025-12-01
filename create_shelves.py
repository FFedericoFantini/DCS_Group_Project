# create_shelves.py

def create_shelves_from_waypoints(sim, nodes, shelf_width, shelf_depth, shelf_height):

    for node_id, node in nodes.items():
        # Only nodes that represent a shelf level
        if "_L" in node_id:
            x, y, z = node.pos

            # Create cuboid
            shelf = sim.createPureShape(
                0,                                 # cuboid
                0,                                 # options
                [shelf_width, shelf_depth, shelf_height],
                0                                  # static
            )
            sim.setObjectInt32Param(shelf, sim.shapeintparam_respondable, 0)
            sim.setObjectInt32Param(shelf, sim.shapeintparam_static, 1)
            sim.setObjectAlias(shelf, f"SHELF_{node_id}")

            # positioning
            sim.setObjectPosition(shelf, -1, [x, y, z + shelf_height/2])

            # color
            sim.setShapeColor(shelf, None, sim.colorcomponent_ambient_diffuse, [0.7, 0.7, 0.7])

            # transparency
            sim.setShapeColor(shelf, None, sim.colorcomponent_transparency, [0.3])
