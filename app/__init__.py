"""Flask应用工厂"""
from flask import Flask, render_template
from config import Config
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.problems import problems_bp
    from app.routes.submissions import submissions_bp
    from app.routes.classes import classes_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(problems_bp, url_prefix='/problems')
    app.register_blueprint(submissions_bp, url_prefix='/submissions')
    app.register_blueprint(classes_bp, url_prefix='/classes')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 创建数据库表
    with app.app_context():
        from app import models  # noqa
        db.create_all()

    # 首页
    @app.route('/')
    def index():
        from app.models import Problem, Submission, User, Class
        stats = {
            'problems': Problem.query.count(),
            'submissions': Submission.query.count(),
            'users': User.query.count(),
            'classes': Class.query.count(),
        }
        recent_problems = Problem.query.filter_by(visible=True)\
            .order_by(Problem.id.desc()).limit(5).all()
        return render_template('index.html', stats=stats,
                               recent_problems=recent_problems)

    return app
