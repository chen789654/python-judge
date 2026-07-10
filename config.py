import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'python-judge-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # Render PostgreSQL 兼容处理：postgres:// → postgresql://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            'postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 代码执行沙箱配置
    JUDGE_MAX_CPU_TIME = 5          # 单用例最大CPU时间(秒)
    JUDGE_MAX_MEMORY = 256 * 1024   # 最大内存( KB)
    JUDGE_MAX_CODE_LENGTH = 10000   # 最大代码长度(字符)
    # Render 生产环境用 /tmp，本地开发用项目目录下的 sandbox
    JUDGE_TEMP_DIR = os.environ.get('JUDGE_TEMP_DIR') or \
        os.path.join(basedir, 'sandbox')

    # 教师注册码（学生选教师角色时需要输入此码）
    TEACHER_REGISTER_CODE = os.environ.get('TEACHER_REGISTER_CODE') or '20251003'

    # 分页
    ITEMS_PER_PAGE = 20
