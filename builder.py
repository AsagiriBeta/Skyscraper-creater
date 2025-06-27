from litemapy import Region, BlockState
from geometry import point_in_polygon, get_bounds, offset_polygon
import logging

def get_block_by_ratio(blocks, ratios, idx):
    logging.debug(f"get_block_by_ratio called with idx={idx}, ratios={ratios}")
    # blocks: [BlockState,...], ratios: [int,...], idx: int
    total = sum(ratios)
    pos = idx % total
    acc = 0
    for i, r in enumerate(ratios):
        acc += r
        if pos < acc:
            return blocks[i]
    return blocks[0]

def build_skyscraper(
    nodes, wall_layers, floor_height, total_height, partition,
    x_parts=0, z_parts=0, partition_blocks=None,
    ceiling_blocks=None, light_block="minecraft:sea_lantern", light_density=4
):
    logging.info(f"build_skyscraper: nodes={nodes}, floor_height={floor_height}, total_height={total_height}, partition={partition}, x_parts={x_parts}, z_parts={z_parts}")
    min_x, min_z, max_x, max_z = get_bounds(nodes)
    wall_thickness = len(wall_layers)
    # 直接使用 wall_layers 顺序，不再反转
    logging.debug(f"Bounds: min_x={min_x}, min_z={min_z}, max_x={max_x}, max_z={max_z}, wall_thickness={wall_thickness}")
    reg = Region(min_x-wall_thickness+1, 0, min_z-wall_thickness+1, max_x+wall_thickness-1, total_height, max_z+wall_thickness-1)
    ceiling_blocks = ceiling_blocks or ["minecraft:gray_concrete"]
    air = BlockState("minecraft:air")
    partition_blocks = partition_blocks or ["minecraft:stone_bricks"]
    light_state = BlockState(light_block)

    x_divs = []
    z_divs = []
    if partition and x_parts > 0:
        step = (max_x - min_x + 1) / x_parts
        if step < 1:
            x_divs = [min_x]
        else:
            x_divs = [round(min_x + step * i) for i in range(1, x_parts)]
    if partition and z_parts > 0:
        step = (max_z - min_z + 1) / z_parts
        if step < 1:
            z_divs = [min_z]
        else:
            z_divs = [round(min_z + step * i) for i in range(1, z_parts)]

    wall_polys = []
    for i in range(wall_thickness):
        wall_polys.append(offset_polygon(nodes, i))

    outer_wall_layers = set()
    if wall_thickness >= 2:
        outer_wall_layers = {0, 1}
    elif wall_thickness == 1:
        outer_wall_layers = {0}

    for y in range(total_height):
        if y % 10 == 0:
            logging.debug(f"Processing layer y={y}/{total_height}")
        slab_base = (y % floor_height == 0)
        for x in range(min_x-wall_thickness+1, max_x+wall_thickness):
            for z in range(min_z-wall_thickness+1, max_z+wall_thickness):
                wall_set = False
                for layer in reversed(range(wall_thickness)):
                    poly = wall_polys[layer]
                    on_edge = False
                    # 修正：更健壮的点是否在多边形边上的判断
                    for i in range(len(poly)):
                        x1, z1 = poly[i]
                        x2, z2 = poly[(i+1)%len(poly)]
                        # 判断点(x,z)是否在(x1,z1)-(x2,z2)线段上
                        dx = x2 - x1
                        dz = z2 - z1
                        if dx == 0 and dz == 0:
                            if (x, z) == (x1, z1):
                                on_edge = True
                                break
                        else:
                            # 线段点判定：三点共线且在区间内
                            if (dx == 0 and x == x1 and min(z1, z2) <= z <= max(z1, z2)) or \
                               (dz == 0 and z == z1 and min(x1, x2) <= x <= max(x1, x2)) or \
                               (dx != 0 and dz != 0 and (x - x1) * dz == (z - z1) * dx and
                                min(x1, x2) <= x <= max(x1, x2) and min(z1, z2) <= z <= max(z1, z2)):
                                on_edge = True
                                break
                    if on_edge and layer in outer_wall_layers:
                        layer_info = wall_layers[layer]
                        pattern = layer_info.get("layer_pattern", "vertical") if isinstance(layer_info, dict) else "vertical"
                        if abs(x - min_x) < 1e-6:
                            idx = (z // 1) if pattern == "vertical" else (y // 1)
                        elif abs(x - max_x) < 1e-6:
                            idx = (z // 1) if pattern == "vertical" else (y // 1)
                        elif abs(z - min_z) < 1e-6:
                            idx = (x // 1) if pattern == "vertical" else (y // 1)
                        elif abs(z - max_z) < 1e-6:
                            idx = (x // 1) if pattern == "vertical" else (y // 1)
                        else:
                            idx = (x // 1) if pattern == "vertical" else (y // 1)
                        if isinstance(layer_info, dict) and "intervals" in layer_info:
                            blocks = [BlockState(b) for b in layer_info["blocks"]]
                            patterns = layer_info["block_patterns"]
                            intervals = layer_info["intervals"]
                            placed = False
                            for b_idx, (block, pat, interval) in enumerate(zip(blocks, patterns, intervals)):
                                idx2 = (z if pat == "vertical" else y) if (abs(x - min_x) < 1e-6 or abs(x - max_x) < 1e-6) else (x if pat == "vertical" else y)
                                if interval > 0 and idx2 % interval == 0 and block.id != "minecraft:air":
                                    reg[x, y, z] = block
                                    placed = True
                                    break
                            if not placed:
                                reg[x, y, z] = air
                        elif isinstance(layer_info, dict) and "ratios" in layer_info:
                            blocks = [BlockState(b) for b in layer_info["blocks"]]
                            ratios = layer_info["ratios"]
                            reg[x, y, z] = get_block_by_ratio(blocks, ratios, idx)
                        else:
                            blocks = [BlockState(b) for b in layer_info]
                            reg[x, y, z] = blocks[idx % len(blocks)]
                        wall_set = True
                        break
                if wall_set:
                    continue
                inside = point_in_polygon(x, z, wall_polys[0])
                if inside:
                    is_partition_wall = False
                    if partition and partition_blocks:
                        if (x_parts > 0 and x in x_divs) or (z_parts > 0 and z in z_divs):
                            blocks = [BlockState(b) for b in partition_blocks]
                            idx = (x + z + y) % len(blocks)
                            reg[x, y, z] = blocks[idx]
                            is_partition_wall = True
                    if not is_partition_wall:
                        if slab_base:
                            if ((x - min_x) % light_density == 0) and ((z - min_z) % light_density == 0):
                                reg[x, y, z] = light_state
                            else:
                                blocks = [BlockState(b) for b in ceiling_blocks]
                                idx = (x + z) % len(blocks)
                                reg[x, y, z] = blocks[idx]
                        else:
                            reg[x, y, z] = air
    logging.info("build_skyscraper 完成")
    return reg
