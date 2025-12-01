# create_area.py

def create_area_zone(sim, area, meeting_pos,
                             width=1.0, height=1.0,
                             color=[0.2, 0.2, 0.2],   # dark gray
                             transparency=0.15,       # almost opaque
                    ):      
    """
    Creates a rectangle (thin cuboid) under the Meeting Area.
    """

    x, y, _ = meeting_pos

    # position slightly below the dummy
    z = 0.01  # above the floor

    # POSITION ABOVE THE FLOOR
    zone = sim.createPureShape(
        0,  # cuboid
        0,  # options
        [width, height, 0.02],  # very thin
        0   # static
    )
    sim.setObjectInt32Param(zone, sim.shapeintparam_respondable, 1)
    sim.setObjectInt32Param(zone, sim.shapeintparam_static, 1)
    area_name = "AREA_BASE_" + area
    sim.setObjectAlias(zone, area_name)
    sim.setObjectPosition(zone, -1, [x, y, z])

    # dark color
    sim.setShapeColor(zone, None, sim.colorcomponent_ambient_diffuse, color)
    sim.setShapeColor(zone, None, sim.colorcomponent_transparency, [transparency])

    return zone
