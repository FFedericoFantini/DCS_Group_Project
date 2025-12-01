# create_area.py


def create_area_zone(sim, meeting_pos,
                             width=1.0, height=1.0,
                             color=[0.2, 0.2, 0.2],   # grigio scuro
                             transparency=0.15):       # quasi opaco
    """
    Crea un rettangolo (cuboid sottile) sotto la Meeting Area.
    """

    x, y, _ = meeting_pos

    # posizione leggermente sotto il dummy
    z = 0.01  # sopra il pavimento

    # POSIZIONE SOPRA IL FLOOR
    zone = sim.createPureShape(
        0,  # cuboid
        0,  # options
        [width, height, 0.02],  # molto sottile
        0   # statico
    )
    sim.setObjectInt32Param(zone, sim.shapeintparam_respondable, 1)
    sim.setObjectInt32Param(zone, sim.shapeintparam_static, 1)
    sim.setObjectAlias(zone, "MEETING_AREA_BASE")
    sim.setObjectPosition(zone, -1, [x, y, z])

    # colore scuro
    sim.setShapeColor(zone, None, sim.colorcomponent_ambient_diffuse, color)
    sim.setShapeColor(zone, None, sim.colorcomponent_transparency, [transparency])

    return zone
