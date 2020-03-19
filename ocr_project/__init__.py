from flask import Flask


def create_app(config):
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(config)
    # 如果有环境变量，可以从环境变量中加载
    app.config.from_envvar('FLASK_CONFIG', silent=True)

    # 初始化db
    from settings.models import db
    db.init_app(app)
    # 注册用户蓝图
    from ocr_project.resource.user_views import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
