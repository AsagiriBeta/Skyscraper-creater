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
    nodes, wall_layers, floor_height, total_height,
    partition_first_floor=False, partition_last_floor=False, partition_other_floors=False,
    x_parts=0, z_parts=0, partition_blocks=None,
    ceiling_blocks=None, light_block="minecraft:sea_lantern", light_density=4
):
    logging.info(f"build_skyscraper: nodes={nodes}, floor_height={floor_height}, total_height={total_height}, partition_first_floor={partition_first_floor}, partition_last_floor={partition_last_floor}, partition_other_floors={partition_other_floors}, x_parts={x_parts}, z_parts={z_parts}")
    # === 修正：所有坐标平移，使最小x/z为0 ===
    min_x, min_z, max_x, max_z = get_bounds(nodes)
    offset_x = min_x
    offset_z = min_z
    nodes_rel = [(x - offset_x, z - offset_z) for x, z in nodes]
    min_x_rel, min_z_rel, max_x_rel, max_z_rel = get_bounds(nodes_rel)
    wall_thickness = len(wall_layers)
    logging.debug(f"Bounds: min_x={min_x_rel}, min_z={min_z_rel}, max_x={max_x_rel}, max_z={max_z_rel}, wall_thickness={wall_thickness}")
    reg = Region(min_x_rel-wall_thickness+1, 0, min_z_rel-wall_thickness+1, max_x_rel+wall_thickness-1, total_height, max_z_rel+wall_thickness-1)
    ceiling_blocks = ceiling_blocks or ["minecraft:gray_concrete"]
    air = BlockState("minecraft:air")
    partition_blocks = partition_blocks or ["minecraft:stone_bricks"]
    light_state = BlockState(light_block)

    x_divs = []
    z_divs = []
    # 只在需要加隔断墙的楼层计算分割线
    if (partition_first_floor or partition_last_floor or partition_other_floors) and x_parts > 0:
        step = (max_x_rel - min_x_rel + 1) / x_parts
        if step < 1:
            x_divs = [min_x_rel]
        else:
            x_divs = [round(min_x_rel + step * i) for i in range(1, x_parts)]
    if (partition_first_floor or partition_last_floor or partition_other_floors) and z_parts > 0:
        step = (max_z_rel - min_z_rel + 1) / z_parts
        if step < 1:
            z_divs = [min_z_rel]
        else:
            z_divs = [round(min_z_rel + step * i) for i in range(1, z_parts)]

    wall_polys = []
    for i in range(wall_thickness):
        wall_polys.append(offset_polygon(nodes_rel, i))

    outer_wall_layers = set()
    if wall_thickness >= 2:
        outer_wall_layers = {0, 1}
    elif wall_thickness == 1:
        outer_wall_layers = {0}

    for y in range(total_height):
        if y % 10 == 0:
            logging.debug(f"Processing layer y={y}/{total_height}")
        slab_base = (y % floor_height == 0)
        # 修正：判断本层是否加隔断墙，整层都应加
        floor_idx = y // floor_height
        is_first_floor = (floor_idx == 0)
        is_last_floor = (floor_idx == (total_height // floor_height - 1))
        if is_first_floor:
            do_partition = partition_first_floor
        elif is_last_floor:
            do_partition = partition_last_floor
        else:
            do_partition = partition_other_floors
        for x in range(min_x_rel-wall_thickness+1, max_x_rel+wall_thickness):
            for z in range(min_z_rel-wall_thickness+1, max_z_rel+wall_thickness):
                wall_set = False
                for layer in reversed(range(wall_thickness)):
                    poly = wall_polys[layer]
                    on_edge = False
                    # 点到多边形边的距离小于0.5格即视为在边上
                    for i in range(len(poly)):
                        x1, z1 = poly[i]
                        x2, z2 = poly[(i+1)%len(poly)]
                        dx = x2 - x1
                        dz = z2 - z1
                        if dx == 0 and dz == 0:
                            if (x, z) == (x1, z1):
                                on_edge = True
                                break
                        else:
                            # 点到线段距离
                            px, pz = x, z
                            vx, vz = dx, dz
                            wx, wz = px - x1, pz - z1
                            c1 = vx * wx + vz * wz
                            c2 = vx * vx + vz * vz
                            if c2 == 0:
                                dist2 = (px - x1) ** 2 + (pz - z1) ** 2
                            else:
                                b = c1 / c2
                                b = max(0, min(1, b))
                                proj_x = x1 + b * vx
                                proj_z = z1 + b * dz
                                dist2 = (px - proj_x) ** 2 + (pz - proj_z) ** 2
                            if dist2 < 0.25:  # 距离小于0.5格
                                on_edge = True
                                break
                    if on_edge and layer in outer_wall_layers:
                        layer_info = wall_layers[layer]
                        pattern = layer_info.get("layer_pattern", "vertical") if isinstance(layer_info, dict) else "vertical"
                        if abs(x - min_x_rel) < 1e-6:
                            idx = (z // 1) if pattern == "vertical" else (y // 1)
                        elif abs(x - max_x_rel) < 1e-6:
                            idx = (z // 1) if pattern == "vertical" else (y // 1)
                        elif abs(z - min_z_rel) < 1e-6:
                            idx = (x // 1) if pattern == "vertical" else (y // 1)
                        elif abs(z - max_z_rel) < 1e-6:
                            idx = (x // 1) if pattern == "vertical" else (y // 1)
                        else:
                            idx = (x // 1) if pattern == "vertical" else (y // 1)
                        if isinstance(layer_info, dict) and "intervals" in layer_info:
                            blocks = [BlockState(b) for b in layer_info["blocks"]]
                            patterns = layer_info["block_patterns"]
                            intervals = layer_info["intervals"]
                            placed = False
                            # 修正斜墙条纹间隔逻辑
                            edge_idx = None
                            edge_pos = None
                            for i in range(len(poly)):
                                x1, z1 = poly[i]
                                x2, z2 = poly[(i+1)%len(poly)]
                                dx = x2 - x1
                                dz = z2 - z1
                                if dx == 0 and dz == 0:
                                    if (x, z) == (x1, z1):
                                        edge_idx = i
                                        edge_pos = 0
                                        break
                                else:
                                    px, pz = x, z
                                    vx, vz = dx, dz
                                    wx, wz = px - x1, pz - z1
                                    c1 = vx * wx + vz * wz
                                    c2 = vx * vx + vz * vz
                                    if c2 == 0:
                                        dist2 = (px - x1) ** 2 + (pz - z1) ** 2
                                        b = 0
                                    else:
                                        b = c1 / c2
                                        b = max(0, min(1, b))
                                        proj_x = x1 + b * vx
                                        proj_z = z1 + b * dz
                                        dist2 = (px - proj_x) ** 2 + (pz - proj_z) ** 2
                                    if dist2 < 0.25:
                                        edge_idx = i
                                        edge_pos = round(((x - x1) ** 2 + (z - z1) ** 2) ** 0.5)
                                        break
                            for b_idx, (block, pat, interval) in enumerate(zip(blocks, patterns, intervals)):
                                if edge_idx is not None:
                                    # 用edge_pos作为条纹编号，保证斜墙也有规律
                                    idx2 = edge_pos if pat == "vertical" else y
                                else:
                                    # 原逻辑
                                    idx2 = (z if pat == "vertical" else y) if (abs(x - min_x_rel) < 1e-6 or abs(x - max_x_rel) < 1e-6) else (x if pat == "vertical" else y)
                                if interval > 0 and idx2 % interval == 0 and block.id != "minecraft:air":
                                    reg[x, y, z] = block
                                    placed = True
                                    break
                            if not placed:
                                reg[x, y, z] = air
                        elif isinstance(layer_info, dict) and "ratios" in layer_info:
                            blocks = [BlockState(b) for b in layer_info["blocks"]]
                            ratios = layer_info["ratios"]
                            # 用点到当前墙边起点的距离作为比例交替依据
                            edge_length = None
                            for i in range(len(poly)):
                                x1, z1 = poly[i]
                                x2, z2 = poly[(i+1)%len(poly)]
                                dx = x2 - x1
                                dz = z2 - z1
                                if dx == 0 and dz == 0:
                                    if (x, z) == (x1, z1):
                                        edge_length = 0
                                        break
                                else:
                                    px, pz = x, z
                                    vx, vz = dx, dz
                                    wx, wz = px - x1, pz - z1
                                    c1 = vx * wx + vz * wz
                                    c2 = vx * vx + vz * vz
                                    if c2 == 0:
                                        b = 0
                                    else:
                                        b = c1 / c2
                                        b = max(0, min(1, b))
                                    proj_x = x1 + b * vx
                                    proj_z = z1 + b * dz
                                    dist2 = (px - proj_x) ** 2 + (pz - proj_z) ** 2
                                    if dist2 < 0.25:
                                        edge_length = ((proj_x - x1) ** 2 + (proj_z - z1) ** 2) ** 0.5
                                        break
                            idx_ratio = int(round(edge_length)) if edge_length is not None else 0
                            reg[x, y, z] = get_block_by_ratio(blocks, ratios, idx_ratio)
                        else:
                            blocks = [BlockState(b) for b in layer_info]
                            # 修正：南北侧用z，东西侧用x，均交替
                            if abs(x - min_x_rel) < 1e-6 or abs(x - max_x_rel) < 1e-6:
                                idx = z
                            elif abs(z - min_z_rel) < 1e-6 or abs(z - max_z_rel) < 1e-6:
                                idx = x
                            else:
                                idx = x  # 默认
                            reg[x, y, z] = blocks[idx % len(blocks)]
                        wall_set = True
                        break
                if wall_set:
                    continue
                inside = point_in_polygon(x, z, wall_polys[0])
                if inside:
                    # 优先生成隔断墙，不依赖 slab_base
                    if do_partition and partition_blocks and ((x_parts > 0 and x in x_divs) or (z_parts > 0 and z in z_divs)):
                        blocks = [BlockState(b) for b in partition_blocks]
                        idx = (x + z + y) % len(blocks)
                        reg[x, y, z] = blocks[idx]
                        continue
                    # 楼板和灯的生成逻辑
                    if slab_base:
                        if ((x - min_x_rel) % light_density == 0) and ((z - min_z_rel) % light_density == 0):
                            reg[x, y, z] = light_state
                        else:
                            blocks = [BlockState(b) for b in ceiling_blocks]
                            idx = (x + z) % len(blocks)
                            reg[x, y, z] = blocks[idx]
                    else:
                        reg[x, y, z] = air
    logging.info("build_skyscraper 完成")
    return reg
