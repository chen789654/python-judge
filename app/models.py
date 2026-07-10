"""数据库模型定义"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager


# ─────────────────────────────────────────────
# 用户模型
# ─────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(16), nullable=False, default='student')  # 'teacher' | 'student'
    student_id = db.Column(db.String(32))      # 学号（学生）
    real_name = db.Column(db.String(64))       # 真实姓名
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    submissions = db.relationship('Submission', backref='author', lazy='dynamic',
                                  foreign_keys='Submission.user_id')
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_teacher(self):
        return self.role == 'teacher'

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ─────────────────────────────────────────────
# 班级模型
# ─────────────────────────────────────────────
class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    invite_code = db.Column(db.String(8), unique=True, nullable=False, index=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    students = db.relationship('User', backref='class_', lazy='dynamic',
                               foreign_keys='User.class_id')
    exams = db.relationship('Exam', backref='class_', lazy='dynamic')

    teacher = db.relationship('User', foreign_keys=[teacher_id])

    def student_count(self):
        return self.students.count()

    def __repr__(self):
        return f'<Class {self.name}>'


# ─────────────────────────────────────────────
# 题目模型
# ─────────────────────────────────────────────
class Problem(db.Model):
    __tablename__ = 'problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)          # Markdown格式题目描述
    input_description = db.Column(db.Text, default='')
    output_description = db.Column(db.Text, default='')
    sample_input = db.Column(db.Text, default='')
    sample_output = db.Column(db.Text, default='')
    hint = db.Column(db.Text, default='')
    standard_answer = db.Column(db.Text, default='')          # 标准参考答案代码
    experiment_order = db.Column(db.Integer, default=0)       # 实验序号(1-16)
    difficulty = db.Column(db.String(16), default='easy')     # easy / medium / hard
    tags = db.Column(db.String(256), default='')              # 逗号分隔的标签
    visible = db.Column(db.Boolean, default=False)            # 是否对学生可见
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_submissions = db.Column(db.Integer, default=0)      # 总提交次数
    accepted_submissions = db.Column(db.Integer, default=0)   # 通过次数

    # 关系
    test_cases = db.relationship('TestCase', backref='problem', lazy='dynamic',
                                 cascade='all, delete-orphan', order_by='TestCase.sort_order')
    submissions = db.relationship('Submission', backref='problem', lazy='dynamic')

    creator = db.relationship('User', foreign_keys=[created_by])

    def accept_rate(self):
        if self.total_submissions == 0:
            return 0
        return round(self.accepted_submissions / self.total_submissions * 100, 1)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def __repr__(self):
        return f'<Problem {self.id}: {self.title}>'


# ─────────────────────────────────────────────
# 测试用例模型
# ─────────────────────────────────────────────
class TestCase(db.Model):
    __tablename__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    input_data = db.Column(db.Text, default='')               # 标准输入
    expected_output = db.Column(db.Text, nullable=False)       # 期望输出
    is_public = db.Column(db.Boolean, default=True)           # 是否对学生可见
    score_weight = db.Column(db.Float, default=1.0)           # 分值权重
    sort_order = db.Column(db.Integer, default=0)             # 排序
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TestCase {self.id} for Problem {self.problem_id}>'


# ─────────────────────────────────────────────
# 提交记录模型
# ─────────────────────────────────────────────
class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=True)
    source_code = db.Column(db.Text, nullable=False)          # 提交的源代码
    language = db.Column(db.String(16), default='python')     # 编程语言
    status = db.Column(db.String(32), default='pending')      # pending / judging / accepted / wrong / error
    score = db.Column(db.Float, default=0.0)                  # 得分
    max_score = db.Column(db.Float, default=100.0)            # 满分
    exec_time = db.Column(db.Float, default=0)                # 执行时间(ms)
    memory_used = db.Column(db.Float, default=0)              # 内存使用(KB)
    compiler_message = db.Column(db.Text, default='')         # 编译/运行错误信息
    teacher_comment = db.Column(db.Text, default='')          # 教师评语
    auto_comment = db.Column(db.Text, default='')             # 自动生成评语
    grade_level = db.Column(db.String(8), default='')         # 优/良/中/及格/不及格
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    judged_at = db.Column(db.DateTime)

    # 关系
    test_results = db.relationship('TestResult', backref='submission', lazy='dynamic',
                                   cascade='all, delete-orphan')
    exam = db.relationship('Exam', foreign_keys=[exam_id])

    def is_accepted(self):
        return self.status == 'accepted'

    def score_percent(self):
        if self.max_score == 0:
            return 0
        return round(self.score / self.max_score * 100, 1)

    def calc_grade_level(self):
        """根据得分百分比计算五级制等级"""
        pct = self.score_percent()
        if pct >= 90:
            return '优'
        elif pct >= 80:
            return '良'
        elif pct >= 70:
            return '中'
        elif pct >= 60:
            return '及格'
        else:
            return '不及格'

    def generate_auto_comment(self):
        """根据得分自动生成评语"""
        pct = self.score_percent()
        if pct >= 90:
            return '实验完成度很高，代码逻辑清晰，运行结果完全正确，表现优秀！'
        elif pct >= 80:
            return '实验完成良好，代码基本正确，部分细节可进一步优化，继续加油！'
        elif pct >= 70:
            return '实验基本完成，核心思路正确，但实现上还有改进空间，建议对照参考答案学习。'
        elif pct >= 60:
            return '实验勉强完成，核心功能已实现但存在较多问题，建议重新审视题目要求。'
        else:
            return '实验未达标，代码无法正确运行或存在较大偏差，需要重新完成。'

    def __repr__(self):
        return f'<Submission {self.id} by User {self.user_id}>'


# ─────────────────────────────────────────────
# 测试用例执行结果
# ─────────────────────────────────────────────
class TestResult(db.Model):
    __tablename__ = 'test_results'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=False)
    actual_output = db.Column(db.Text, default='')
    passed = db.Column(db.Boolean, default=False)
    score_earned = db.Column(db.Float, default=0.0)
    exec_time = db.Column(db.Float, default=0)

    test_case = db.relationship('TestCase', foreign_keys=[test_case_id])

    def __repr__(self):
        return f'<TestResult {self.id} {"PASS" if self.passed else "FAIL"}>'


# ─────────────────────────────────────────────
# 考试/作业模型
# ─────────────────────────────────────────────
class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, default='')
    exam_type = db.Column(db.String(16), default='homework')  # homework / exam / practice
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)                           # 考试时长(分钟)
    max_submissions = db.Column(db.Integer, default=0)         # 0表示不限
    shuffle_problems = db.Column(db.Boolean, default=False)
    show_result_immediately = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    problems = db.relationship('ExamProblem', backref='exam', lazy='dynamic',
                               cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='exam_ref', lazy='dynamic')

    creator = db.relationship('User', foreign_keys=[created_by])

    def problem_count(self):
        return self.problems.count()

    def __repr__(self):
        return f'<Exam {self.title}>'


# ─────────────────────────────────────────────
# 考试-题目关联
# ─────────────────────────────────────────────
class ExamProblem(db.Model):
    __tablename__ = 'exam_problems'

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    score = db.Column(db.Float, default=100.0)                # 该题满分
    sort_order = db.Column(db.Integer, default=0)

    problem = db.relationship('Problem', foreign_keys=[problem_id])

    def __repr__(self):
        return f'<ExamProblem Exam{self.exam_id} Prob{self.problem_id}>'


# ─────────────────────────────────────────────
# 系统通知
# ─────────────────────────────────────────────
class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pinned = db.Column(db.Boolean, default=False)

    creator = db.relationship('User', foreign_keys=[created_by])

    def __repr__(self):
        return f'<Announcement {self.title}>'
