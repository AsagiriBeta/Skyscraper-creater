def get_polygon_nodes():
    n = int(input("请输入节点数量（>=3）："))
    nodes = []
    for i in range(n):
        coord = input(f"第{i+1}个节点的坐标（x,z）：").strip()
        # 支持英文逗号和中文逗号
        if ',' in coord:
            x_str, z_str = coord.split(',', 1)
            x = int(x_str.strip())
            z = int(z_str.strip())
        else:
            x = int(coord)
            z = int(input(f"第{i+1}个节点的z坐标："))
        nodes.append((x, z))
    return nodes

def choose_partition_block_style(prompt="选择隔断墙方块类型："):
    styles = {
        "1": "minecraft:white_concrete",
        "2": "minecraft:orange_concrete",
        "3": "minecraft:magenta_concrete",
        "4": "minecraft:light_blue_concrete",
        "5": "minecraft:yellow_concrete",
        "6": "minecraft:lime_concrete",
        "7": "minecraft:pink_concrete",
        "8": "minecraft:gray_concrete",
        "9": "minecraft:light_gray_concrete",
        "10": "minecraft:cyan_concrete",
        "11": "minecraft:purple_concrete",
        "12": "minecraft:blue_concrete",
        "13": "minecraft:brown_concrete",
        "14": "minecraft:green_concrete",
        "15": "minecraft:red_concrete",
        "16": "minecraft:black_concrete"
    }
    for k, v in styles.items():
        print(f"{k}: {v}")
    print("输入多个编号用英文逗号分隔（如4,5），直接回车默认。")
    choice = input(prompt).strip()
    blocks = []
    if not choice:
        return []
    for idx in choice.split(","):
        idx = idx.strip()
        if idx in styles:
            blocks.append(styles[idx])
    return blocks

def choose_slab_block_style(prompt="选择楼板/天花板方块类型："):
    styles = {
        "1": "minecraft:oak_planks",
        "2": "minecraft:spruce_planks",
        "3": "minecraft:birch_planks",
        "4": "minecraft:jungle_planks",
        "5": "minecraft:acacia_planks",
        "6": "minecraft:dark_oak_planks",
        "7": "minecraft:mangrove_planks",
        "8": "minecraft:bamboo_planks",
        "9": "minecraft:cherry_planks",
        "10": "minecraft:crimson_planks",
        "11": "minecraft:warped_planks",
        "12": "minecraft:white_concrete",
        "13": "minecraft:orange_concrete",
        "14": "minecraft:magenta_concrete",
        "15": "minecraft:light_blue_concrete",
        "16": "minecraft:yellow_concrete",
        "17": "minecraft:lime_concrete",
        "18": "minecraft:pink_concrete",
        "19": "minecraft:gray_concrete",
        "20": "minecraft:light_gray_concrete",
        "21": "minecraft:cyan_concrete",
        "22": "minecraft:purple_concrete",
        "23": "minecraft:blue_concrete",
        "24": "minecraft:brown_concrete",
        "25": "minecraft:green_concrete",
        "26": "minecraft:red_concrete",
        "27": "minecraft:black_concrete"
    }
    for k, v in styles.items():
        print(f"{k}: {v}")
    print("输入多个编号用英文逗号分隔（如4,5），直接回车默认。")
    choice = input(prompt).strip()
    blocks = []
    if not choice:
        return []
    for idx in choice.split(","):
        idx = idx.strip()
        if idx in styles:
            blocks.append(styles[idx])
    return blocks

def choose_light_block(prompt="请选择灯方块类型："):
    styles = {
        "1": "minecraft:sea_lantern",
        "2": "minecraft:glowstone",
        "3": "minecraft:verdant_froglight",
        "4": "minecraft:pearlescent_froglight",
        "5": "minecraft:ochre_froglight"
    }
    for k, v in styles.items():
        print(f"{k}: {v}")
    print("直接回车默认海晶灯。")
    choice = input(prompt).strip()
    if not choice:
        return "minecraft:sea_lantern"
    if choice in styles:
        return styles[choice]
    return "minecraft:sea_lantern"

def get_partition_params():
    partition = input("是否每层加隔断墙？(y/n)：").lower() == 'y'
    x_parts, z_parts, partition_blocks = 0, 0, None
    if partition:
        x_parts = int(input("x轴方向隔断几等分（输入0表示不分）："))
        z_parts = int(input("z轴方向隔断几等分（输入0表示不分）："))
        print("请选择隔断墙方块类型：")
        partition_blocks = choose_partition_block_style("输入编号（单个或多个，回车默认gray_concrete）：")
        if not partition_blocks:
            partition_blocks = ["minecraft:gray_concrete"]
    return partition, x_parts, z_parts, partition_blocks

def get_building_params():
    floor_height = int(input("请输入每层高度（格）："))
    total_height = int(input("请输入楼总高度（格）："))
    partition, x_parts, z_parts, partition_blocks = get_partition_params()
    slab_thickness = 1
    print("请选择楼板/天花板方块类型：")
    ceiling_blocks = choose_slab_block_style("输入编号（单个或多个，回车默认gray_concrete）：")
    if not ceiling_blocks:
        ceiling_blocks = ["minecraft:gray_concrete"]
    print("请选择嵌入楼板的灯方块类型：")
    light_block = choose_light_block()
    try:
        light_density = int(input("灯的密度（每几格一个，建议3~8）："))
        if light_density < 1:
            light_density = 4
    except:
        light_density = 4
    floor_block = None
    return floor_height, total_height, partition, x_parts, z_parts, partition_blocks, slab_thickness, ceiling_blocks, light_block, light_density, floor_block
