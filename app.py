import logging
import os
from flask import Flask
from views import main_bp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

app = Flask(__name__)
# 从环境变量读取 SECRET_KEY，若未设置则自动生成随机密钥
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
# 延长CSRF令牌有效期（单位秒，默认3600=1小时），如需灵活可用环境变量控制
app.config['WTF_CSRF_TIME_LIMIT'] = int(os.environ.get('WTF_CSRF_TIME_LIMIT', 7200))  # 2小时
#app.config['WTF_CSRF_ENABLED'] = False
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
