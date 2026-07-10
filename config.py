import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'python-judge-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 代码执行沙箱配置
    JUDGE_MAX_CPU_TIME = 5          # 单用例最大CPU时间(秒)
    JUDGE_MAX_MEMORY = 256 * 1024   # 最大内存( KB)
    JUDGE_MAX_CODE_LENGTH = 10000   # 最大代码长度(字符)
    JUDGE_TEMP_DIR = os.path.join(basedir, 'sandbox')

    # 分页
    ITEMS_PER_PAGE = 20
