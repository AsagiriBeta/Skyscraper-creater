from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Regexp

# 第一层外墙专用选项：仅玻璃、混凝土、平滑石、不设置
WALL_LAYER_1_CHOICES = [
    ('none', '不设置'),
    ('air', '空气'),  # 修复：允许选择空气
    ('glass', '玻璃'),
    ('white_stained_glass', '白色染色玻璃'),
    ('orange_stained_glass', '橙色染色玻璃'),
    ('magenta_stained_glass', '品红色染色玻璃'),
    ('light_blue_stained_glass', '淡蓝色染色玻璃'),
    ('yellow_stained_glass', '黄色染色玻璃'),
    ('lime_stained_glass', '黄绿色染色玻璃'),
    ('pink_stained_glass', '粉色染色玻璃'),
    ('gray_stained_glass', '灰色染色玻璃'),
    ('light_gray_stained_glass', '淡灰色染色玻璃'),
    ('cyan_stained_glass', '青色染色玻璃'),
    ('purple_stained_glass', '紫色染色玻璃'),
    ('blue_stained_glass', '蓝色染色玻璃'),
    ('brown_stained_glass', '棕色染色玻璃'),
    ('green_stained_glass', '绿色染色玻璃'),
    ('red_stained_glass', '红色染色玻璃'),
    ('black_stained_glass', '黑色染色玻璃'),
    ('white_concrete', '白色混凝土'),
    ('orange_concrete', '橙色混凝土'),
    ('magenta_concrete', '品红色混凝土'),
    ('light_blue_concrete', '淡蓝色混凝土'),
    ('yellow_concrete', '黄色混凝土'),
    ('lime_concrete', '黄绿色混凝土'),
    ('pink_concrete', '粉色混凝土'),
    ('gray_concrete', '灰色混凝土'),
    ('light_gray_concrete', '淡灰色混凝土'),
    ('cyan_concrete', '青色混凝土'),
    ('purple_concrete', '紫色混凝土'),
    ('blue_concrete', '蓝色混凝土'),
    ('brown_concrete', '棕色混凝土'),
    ('green_concrete', '绿色混凝土'),
    ('red_concrete', '红色混凝土'),
    ('black_concrete', '黑色混凝土'),
    ('smooth_stone', '平滑石'),
]

# 第二层外墙专用选项：仅玻璃板、末地烛、铁链、铁活板门
WALL_LAYER_2_CHOICES = [
    ('none', '不设置'),
    ('air', '空气'),  # 修复：允许选择空气
    ('glass_pane', '玻璃板'),
    ('white_stained_glass_pane', '白色染色玻璃板'),
    ('orange_stained_glass_pane', '橙色染色玻璃板'),
    ('magenta_stained_glass_pane', '品红色染色玻璃板'),
    ('light_blue_stained_glass_pane', '淡蓝色染色玻璃板'),
    ('yellow_stained_glass_pane', '黄色染色玻璃板'),
    ('lime_stained_glass_pane', '黄绿色染色玻璃板'),
    ('pink_stained_glass_pane', '粉色染色玻璃板'),
    ('gray_stained_glass_pane', '灰色染色玻璃板'),
    ('light_gray_stained_glass_pane', '淡灰色染色玻璃板'),
    ('cyan_stained_glass_pane', '青色染色玻璃板'),
    ('purple_stained_glass_pane', '紫色染色玻璃板'),
    ('blue_stained_glass_pane', '蓝色染色玻璃板'),
    ('brown_stained_glass_pane', '棕色染色玻璃板'),
    ('green_stained_glass_pane', '绿色染色玻璃板'),
    ('red_stained_glass_pane', '红色染色玻璃板'),
    ('black_stained_glass_pane', '黑色染色玻璃板'),
    ('end_rod', '末地烛'),
    ('chain', '锁链'),
    ('iron_trapdoor', '铁活板门'),
]


class SkyscraperForm(FlaskForm):
    nodes = StringField('节点坐标（格式: x1,z1;x2,z2;...）', validators=[DataRequired()])
    floor_height = IntegerField('每层高度', validators=[DataRequired(), NumberRange(min=1)])
    total_height = IntegerField('总高度', validators=[DataRequired(), NumberRange(min=1)])
    partition = BooleanField('每层加隔断墙')
    x_parts = IntegerField('x轴等分数', default=0)
    z_parts = IntegerField('z轴等分数', default=0)
    wall_pattern = SelectField(
        '外墙条纹排列方式',
        choices=[('vertical', '竖直条纹'), ('horizontal', '水平条纹')],
        default='vertical'
    )
    wall_density = IntegerField('外墙疏密度', default=1)
    partition_blocks = SelectField(
        '隔断墙方块',
        choices=[
            ('white_concrete', '白色混凝土'),
            ('orange_concrete', '橙色混凝土'),
            ('magenta_concrete', '品红色混凝土'),
            ('light_blue_concrete', '蓝色混凝土'),
            ('yellow_concrete', '黄色混凝土'),
            ('lime_concrete', '黄绿色混凝土'),
            ('pink_concrete', '粉色混凝土'),
            ('gray_concrete', '灰色混凝土'),
            ('light_gray_concrete', '淡灰色混凝土'),
            ('cyan_concrete', '青色混凝土'),
            ('purple_concrete', '紫色混凝土'),
            ('blue_concrete', '蓝色混凝土'),
            ('brown_concrete', '棕色混凝土'),
            ('green_concrete', '绿色混凝土'),
            ('red_concrete', '红色混凝土'),
            ('black_concrete', '黑色混凝土'),
        ],
        default='gray_concrete'
    )
    ceiling_blocks = SelectField(
        '楼板/天花板方块',
        choices=[
            ('oak_planks', '橡木木板'),
            ('spruce_planks', '云杉木板'),
            ('birch_planks', '白桦木板'),
            ('jungle_planks', '丛林木板'),
            ('acacia_planks', '金合欢木板'),
            ('dark_oak_planks', '深色橡木木板'),
            ('mangrove_planks', '红树木板'),
            ('bamboo_planks', '竹板'),
            ('cherry_planks', '樱花木板'),
            ('crimson_planks', '绯红木板'),
            ('warped_planks', '诡异木板'),
            ('white_concrete', '白色混凝土'),
            ('orange_concrete', '橙色混凝土'),
            ('magenta_concrete', '品红色混凝土'),
            ('light_blue_concrete', '淡蓝色混凝土'),
            ('yellow_concrete', '黄色混凝土'),
            ('lime_concrete', '黄绿色混凝土'),
            ('pink_concrete', '粉色混凝土'),
            ('gray_concrete', '灰色混凝土'),
            ('light_gray_concrete', '淡灰色混凝土'),
            ('cyan_concrete', '青色混凝土'),
            ('purple_concrete', '紫色混凝土'),
            ('blue_concrete', '蓝色混凝土'),
            ('brown_concrete', '棕色混凝土'),
            ('green_concrete', '绿色混凝土'),
            ('red_concrete', '红色混凝土'),
            ('black_concrete', '黑色混凝土'),
        ],
        default='gray_concrete'
    )
    light_block = SelectField(
        '灯方块',
        choices=[
            ('minecraft:sea_lantern', '海晶灯'),
            ('minecraft:glowstone', '萤石'),
            ('minecraft:verdant_froglight', '青蛙灯(绿色)'),
            ('minecraft:pearlescent_froglight', '青蛙���(珍珠色)'),
            ('minecraft:ochre_froglight', '青蛙灯(赭色)'),
        ],
        default='minecraft:sea_lantern'
    )
    light_density = IntegerField('灯密度', default=4, validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('生成')
    wall_pattern_1 = SelectField(
        '第一层外墙条纹排列方式',
        choices=[('vertical', '竖直条纹'), ('horizontal', '水平条纹')],
        default='vertical'
    )
    wall_layer_1_a = SelectField(
        '第一层外墙方块1',
        choices=WALL_LAYER_1_CHOICES,
        default='glass',
        validators=[DataRequired()],
        coerce=str
    )
    wall_layer_1_b = SelectField(
        '第一层外墙方块2',
        choices=WALL_LAYER_1_CHOICES,
        default='air',
        coerce=str
    )
    wall_layer_1_c = SelectField(
        '第一层外墙方块3',
        choices=WALL_LAYER_1_CHOICES,
        default='air',
        coerce=str
    )
    wall_ratio_1 = StringField('第一层外墙方块比例（如1:1:1，最多3项，不设置则填0）', validators=[DataRequired(), Regexp(r'^(\d+:){0,2}\d+$', message='格式如1:1:1')])
    wall_layer_2_a = SelectField(
        '第二层外墙方块1',
        choices=WALL_LAYER_2_CHOICES,
        default='white_stained_glass',
        validators=[DataRequired()],
        coerce=str
    )
    wall_layer_2_a_pattern = SelectField(
        '方块1条纹排列',
        choices=[('vertical', '竖直条纹'), ('horizontal', '水平条纹')],
        default='vertical'
    )
    wall_layer_2_a_interval = IntegerField(
        '方块1条纹间隔（格）',
        default=1,
        validators=[NumberRange(min=1)]
    )
    wall_layer_2_b = SelectField(
        '第二层外墙方块2',
        choices=WALL_LAYER_2_CHOICES,
        default='none',
        coerce=str
    )
    wall_layer_2_b_pattern = SelectField(
        '方块2条纹排列',
        choices=[('vertical', '竖直条纹'), ('horizontal', '水平条纹')],
        default='vertical'
    )
    wall_layer_2_b_interval = IntegerField(
        '方块2条纹间隔（格）',
        default=1,
        validators=[NumberRange(min=1)]
    )
    wall_layer_2_c = SelectField(
        '第二层外墙方块3',
        choices=WALL_LAYER_2_CHOICES,
        default='none',
        coerce=str
    )
    wall_layer_2_c_pattern = SelectField(
        '方块3条纹排列',
        choices=[('vertical', '竖直条纹'), ('horizontal', '水平条纹')],
        default='vertical'
    )
    wall_layer_2_c_interval = IntegerField(
        '方块3条纹间隔（格）',
        default=1,
        validators=[NumberRange(min=1)]
    )
