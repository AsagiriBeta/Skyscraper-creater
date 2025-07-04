import io

from flask import Blueprint, render_template, send_file, flash

from builder import build_skyscraper
from forms import SkyscraperForm

main_bp = Blueprint('main', __name__)

def parse_wall_layer(blocks, patterns, ratio_str, layer_pattern):
    # blocks: list of block names (最多3)
    # patterns: list of pattern for each block
    # ratio_str: '1:2:1' 形式
    # 返回 dict
    ratios = [int(x) for x in ratio_str.split(':')]
    if len(blocks) != len(ratios):
        raise ValueError('方块数量与比例数量不一致')
    block_ids = [f"minecraft:{b}" if b != 'air' else 'minecraft:air' for b in blocks]
    return {
        "blocks": block_ids,
        "ratios": ratios,
        "layer_pattern": layer_pattern,
        "block_patterns": patterns
    }

def parse_wall_layer_v2(blocks, patterns, intervals, layer_pattern):
    # blocks: list of block names (最多3)
    # patterns: list of pattern for each block
    # intervals: list of int, 每个方块的条纹间隔
    # 返回 dict，忽略 'none' 选项
    result_blocks = []
    result_patterns = []
    result_intervals = []
    for b, p, inter in zip(blocks, patterns, intervals):
        if b != 'none':
            result_blocks.append(f"minecraft:{b}" if b != 'air' else 'minecraft:air')
            result_patterns.append(p)
            result_intervals.append(inter)
    return {
        "blocks": result_blocks,
        "block_patterns": result_patterns,
        "intervals": result_intervals,
        "layer_pattern": layer_pattern
    }

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    import traceback
    form = SkyscraperForm()
    if form.validate_on_submit():
        try:
            print('[INFO] 表单已提交，开始解析参数')
            # 解析节点
            nodes = [tuple(map(int, pair.split(','))) for pair in form.nodes.data.split(';')]
            print(f'[DEBUG] nodes: {nodes}')
            # 组装两层外墙配置
            wall_layers = [
                parse_wall_layer_v2(
                    [form.wall_layer_2_a.data, form.wall_layer_2_b.data, form.wall_layer_2_c.data],
                    [form.wall_layer_2_a_pattern.data, form.wall_layer_2_b_pattern.data, form.wall_layer_2_c_pattern.data],
                    [form.wall_layer_2_a_interval.data, form.wall_layer_2_b_interval.data, form.wall_layer_2_c_interval.data],
                    None),  # 第二层
                parse_wall_layer(
                    [form.wall_layer_1_a.data, form.wall_layer_1_b.data, form.wall_layer_1_c.data],
                    [form.wall_pattern_1.data] * 3,
                    form.wall_ratio_1.data, form.wall_pattern_1.data)  # 第一层
            ]
            print(f'[DEBUG] wall_layers: {wall_layers}')
            reg = build_skyscraper(
                nodes=nodes,
                wall_layers=wall_layers,
                floor_height=form.floor_height.data,
                total_height=form.floor_height.data * form.total_floors.data,
                partition_first_floor=form.partition_first_floor.data,
                partition_last_floor=form.partition_last_floor.data,
                partition_other_floors=form.partition_other_floors.data,
                x_parts=form.x_parts.data,
                z_parts=form.z_parts.data,
                partition_blocks=[
                    f"minecraft:{form.partition_blocks.data}" if not form.partition_blocks.data.startswith("minecraft:") else form.partition_blocks.data
                ],
                ceiling_blocks=[
                    f"minecraft:{form.ceiling_blocks.data}" if not form.ceiling_blocks.data.startswith("minecraft:") else form.ceiling_blocks.data
                ],
                light_block=form.light_block.data,
                light_density=form.light_density.data
            )
            print('[INFO] build_skyscraper 执行完毕')
            # 读取表单自定义 schematic 元数据
            schem_name = form.schematic_name.data or "skyscraper"
            schem_author = form.schematic_author.data or "webui"
            schem_desc = form.schematic_description.data or "Generated by UI"
            schem = reg.as_schematic(name=schem_name, author=schem_author, description=schem_desc)
            print('[INFO] as_schematic 执行完毕')
            buf = io.BytesIO()
            schem.save(buf)
            print('[INFO] schematic 保存到 buffer 完毕')
            buf.seek(0)
            # 用自定义名称作为下载文件名
            safe_name = schem_name.strip().replace(' ', '_') or 'skyscraper'
            return send_file(buf, as_attachment=True, download_name=f"{safe_name}.litematic")
        except Exception as e:
            print('[ERROR] 生成失败:', e)
            traceback.print_exc()
            flash(f"生成失败: {e}", 'danger')
    return render_template('index.html', form=form)
