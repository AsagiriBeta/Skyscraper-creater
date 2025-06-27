def choose_wall_style_layers():
    print("你将依次设置两层外墙，每层可以有多种方块交替。")
    # 全局默认条纹方向
    pattern = ""
    while pattern not in ("1", "2"):
        pattern = input("外墙条纹排列方式：1=竖直条纹 2=水平条纹（默认1）：").strip() or "1"
    wall_pattern = "vertical" if pattern == "1" else "horizontal"

    styles = {
        "1": "minecraft:glass",
        "2": "minecraft:white_concrete",
        "3": "minecraft:stone_bricks",
        "4": "minecraft:black_stained_glass",
        "5": "minecraft:gray_stained_glass",
        "6": "minecraft:chain",
        "7": "minecraft:iron_trapdoor",
        "8": "minecraft:polished_diorite",
        "9": "minecraft:end_rod",
        # 新增玻璃
        "10": "minecraft:white_stained_glass",
        "11": "minecraft:orange_stained_glass",
        "12": "minecraft:magenta_stained_glass",
        "13": "minecraft:light_blue_stained_glass",
        "14": "minecraft:yellow_stained_glass",
        "15": "minecraft:lime_stained_glass",
        "16": "minecraft:pink_stained_glass",
        "17": "minecraft:light_gray_stained_glass",
        "18": "minecraft:cyan_stained_glass",
        "19": "minecraft:purple_stained_glass",
        "20": "minecraft:blue_stained_glass",
        "21": "minecraft:brown_stained_glass",
        "22": "minecraft:green_stained_glass",
        "23": "minecraft:red_stained_glass",
        # 新增混凝土
        "24": "minecraft:orange_concrete",
        "25": "minecraft:magenta_concrete",
        "26": "minecraft:light_blue_concrete",
        "27": "minecraft:yellow_concrete",
        "28": "minecraft:lime_concrete",
        "29": "minecraft:pink_concrete",
        "30": "minecraft:gray_concrete",
        "31": "minecraft:light_gray_concrete",
        "32": "minecraft:cyan_concrete",
        "33": "minecraft:purple_concrete",
        "34": "minecraft:blue_concrete",
        "35": "minecraft:brown_concrete",
        "36": "minecraft:green_concrete",
        "37": "minecraft:red_concrete",
        "38": "minecraft:black_concrete"
    }

    layers = []
    for i in range(2):
        print(f"设置第{i+1}层外墙：")
        for k, v in styles.items():
            print(f"{k}: {v}")
        print("输入多个编号用英文逗号分隔（如4,5），直接回车结束设置。")
        choice = input("输入编号（单个或多个，回车结束）：").strip()
        blocks = []
        block_patterns = {}
        for idx in choice.split(","):
            idx = idx.strip()
            if idx in styles:
                blocks.append(styles[idx])
        if blocks:
            # 对每个方块单独设置排列方式
            for block in blocks:
                b_pattern = ""
                while b_pattern not in ("", "1", "2"):
                    b_pattern = input(f"方块 {block} 条纹排列方式：1=竖直 2=水平（回车使用本层默认{wall_pattern}）：").strip()
                if b_pattern == "1":
                    block_patterns[block] = "vertical"
                elif b_pattern == "2":
                    block_patterns[block] = "horizontal"
                else:
                    block_patterns[block] = wall_pattern
            # 每层都可设置是否混杂空气
            mix_air = input("本层是否混杂空气？y/N（默认N）：").strip().lower() == "y"
            if mix_air:
                try:
                    density = int(input("本层疏密度（每几格一个方块，1为无空气，建议1~5，默认1）：").strip() or "1")
                    if density < 1:
                        density = 1
                except:
                    density = 1
            else:
                density = 1
            layers.append({
                "blocks": blocks,
                "block_patterns": block_patterns,
                "layer_pattern": wall_pattern,
                "density": density
            })
        else:
            print("未选择有效方块，跳过。")
        # 每层可选是否更改默认条纹方式（仅第1层后可选）
        if i == 0:
            change_layer_pattern = input("是否为下一层更改默认条纹排列方式？y/N：").strip().lower()
            if change_layer_pattern == "y":
                np = ""
                while np not in ("1", "2"):
                    np = input("新默认条纹排列方式：1=竖直 2=水平（默认1）：").strip() or "1"
                wall_pattern = "vertical" if np == "1" else "horizontal"

    if not layers:
        # 兼容旧返回
        return [["minecraft:glass"]], wall_pattern, 1

    return layers, None, None  # 每层已包含density
