import logging
def point_in_polygon(x, z, poly):
    logging.debug(f"point_in_polygon: x={x}, z={z}, poly={poly}")
    n = len(poly)
    inside = False
    px, pz = x, z
    for i in range(n):
        x1, z1 = poly[i]
        x2, z2 = poly[(i+1)%n]
        if ((z1 > pz) != (z2 > pz)) and (px < (x2-x1)*(pz-z1)/(z2-z1)+x1):
            inside = not inside
    logging.debug(f"point_in_polygon result: {inside}")
    return inside

def get_bounds(nodes):
    logging.debug(f"get_bounds: nodes={nodes}")
    xs = [x for x, _ in nodes]
    zs = [z for _, z in nodes]
    bounds = (min(xs), min(zs), max(xs), max(zs))
    logging.debug(f"get_bounds result: {bounds}")
    return bounds

def offset_polygon(nodes, offset):
    import math
    logging.debug(f"offset_polygon: nodes={nodes}, offset={offset}")
    n = len(nodes)
    result = []
    for i in range(n):
        x0, z0 = nodes[i-1]
        x1, z1 = nodes[i]
        x2, z2 = nodes[(i+1)%n]
        dx1, dz1 = x1-x0, z1-z0
        dx2, dz2 = x2-x1, z2-z1
        len1 = math.hypot(dx1, dz1)
        len2 = math.hypot(dx2, dz2)
        nx1, nz1 = dz1/len1, -dx1/len1
        nx2, nz2 = dz2/len2, -dx2/len2
        nx, nz = (nx1+nx2)/2, (nz1+nz2)/2
        norm = math.hypot(nx, nz)
        if norm == 0:
            nx, nz = 0, 0
        else:
            nx, nz = nx/norm, nz/norm
        result.append((round(x1+nx*offset), round(z1+nz*offset)))
    logging.debug(f"offset_polygon result: {result}")
    return result
