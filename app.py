import logging
from flask import Flask
from views import main_bp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

app = Flask(__name__)
# 建议使用更安全的随机密钥
app.config['SECRET_KEY'] = 'a-very-strong-and-random-secret-key-20250627'
# 可选：延长CSRF令牌有效期（单位秒，默认3600=1小时）
app.config['WTF_CSRF_TIME_LIMIT'] = 7200  # 2小时
app.config['WTF_CSRF_ENABLED'] = False  # 临时关闭CSRF校验，便于本地调试
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
