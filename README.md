# Skyscraper Creater

这是一个用于生成 Minecraft 高层建筑（摩天楼）litematic 文件的工具，支持命令行和 Web UI 两种模式。你可以自定义建筑外墙、楼层、隔断墙、天花板、灯光等参数，快速生成可导入 Litematica 的 .litematic 文件。

## 功能简介
- 支持多边形自定义建筑轮廓
- 外墙可分多层、多种方块混搭，支持条纹/间隔/比例等多种排列方式
- 支持每层自动添加隔断墙
- 支持自定义楼板/天花板方块和灯光密度
- 生成的文件可直接导入 Litematica 使用

## 安装依赖
建议使用 Python 3.8 及以上版本。

```bash
pip install flask flask-wtf litemapy
```

## 启动 Web UI
1. 运行 Web UI：
   ```bash
   python app.py
   ```
2. 打开浏览器访问 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
3. 按页面提示填写参数，点击“生成并下载litematic”即可获得建筑文件。

## 命令行模式
直接运行 `main.py` 按提示输入参数即可生成 litematic 文件：

```bash
python main.py
```

## 注意事项
- 生成的文件需配合 Litematica Mod 使用
- 若遇到依赖问题，请确保已正确安装 `litemapy` 和 `flask` 等库
- 生成的建筑可能需要根据实际情况调整细节

