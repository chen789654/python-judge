# Python在线编程评测系统

基于 Flask 的编程作业自动评测平台，专为高校 Python 程序设计课程设计。

## 技术栈

| 技术 | 用途 |
|------|------|
| **Python + Flask** | Web 框架 |
| **SQLAlchemy** | ORM 数据库 |
| **Flask-Login** | 用户认证（教师/学生双角色） |
| **Flask-WTF + WTForms** | 表单处理与 CSRF 保护 |
| **Markdown** | 题目描述渲染 |
| **SQLite / PostgreSQL** | 数据库（生产环境用 PostgreSQL） |
| **Gunicorn** | 生产部署 |

## 功能

### 双角色系统
- **教师**：管理题目、创建班级、发布考试/作业、查看学生提交、手动评语
- **学生**：查看题目、在线提交代码、查看评测结果、查看成绩统计

### 题库管理
- 题目 CRUD，支持 Markdown 描述
- 测试用例管理（支持公开用例和隐藏用例）
- 难度标签（easy / medium / hard）
- 题目搜索、筛选

### 自动评测引擎
- 安全沙箱执行：`subprocess` 隔离运行，限制 CPU 时间和内存
- 危险模块拦截：禁止 `os`、`sys`、`subprocess`、`socket` 等危险模块
- 逐用例比对输出，支持权重评分
- 自动生成评语和五级制等级（优/良/中/及格/不及格）

### 班级管理
- 教师创建班级，生成邀请码
- 学生通过邀请码加入班级
- 按班级布置作业和考试

### 考试/作业模式
- 支持限时考试、常规作业、自由练习
- 限制提交次数
- 可选立即显示结果或考试结束后公布

## 快速启动

```bash
# 1. 克隆
git clone https://github.com/chen789654/python-judge.git
cd python-judge

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化数据库
python
>>> from app import create_app
>>> from app.extensions import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()

# 4. 创建管理员
python create_admin.py

# 5. 启动
python run.py
# 访问 http://localhost:5000
```

## 部署

支持一键部署到 Render：

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

配置文件：`render.yaml`

## 项目结构

```
├── run.py                  # 应用入口
├── config.py               # 配置（数据库、沙箱、安全等）
├── requirements.txt        # Python 依赖
├── render.yaml             # Render 部署配置
├── create_admin.py         # 管理员创建脚本
├── seed_experiments.py     # 示例数据填充
├── app/
│   ├── __init__.py         # 应用工厂
│   ├── extensions.py       # Flask 扩展初始化
│   ├── models.py           # 数据模型
│   ├── routes/
│   │   ├── auth.py         # 注册/登录/登出
│   │   ├── problems.py     # 题库管理
│   │   ├── submissions.py  # 提交记录
│   │   ├── classes.py      # 班级管理
│   │   └── admin.py        # 管理后台
│   ├── services/
│   │   ├── judge.py        # 代码自动评测引擎
│   │   └── plagiarism.py   # 代码查重
│   ├── templates/          # Jinja2 模板
│   ├── static/             # 静态资源
│   └── utils/              # 工具函数
└── soft_copyright/         # 软件著作权申请材料
```

## 适用场景

- 高校 Python 程序设计课程在线作业评测
- 编程初学者在线练习平台
- 编程考试自动化阅卷

## License

MIT
