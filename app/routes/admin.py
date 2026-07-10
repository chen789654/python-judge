"""
管理面板路由

提供统计报表、成绩分析、查重检测等功能（教师专用）
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Problem, Submission, Class, TestCase
from app.services.plagiarism import find_plagiarism, highlight_diff
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')


@admin_bp.route('/')
@login_required
def dashboard():
    """管理仪表盘"""
    if not current_user.is_teacher():
        abort(403)

    stats = {
        'user_count': User.query.count(),
        'student_count': User.query.filter_by(role='student').count(),
        'teacher_count': User.query.filter_by(role='teacher').count(),
        'problem_count': Problem.query.count(),
        'visible_problems': Problem.query.filter_by(visible=True).count(),
        'submission_count': Submission.query.count(),
        'accepted_count': Submission.query.filter_by(status='accepted').count(),
        'class_count': Class.query.count(),
    }

    # 最近提交
    recent_submissions = Submission.query.order_by(
        Submission.submitted_at.desc()
    ).limit(10).all()

    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_submissions=recent_submissions)


@admin_bp.route('/statistics')
@login_required
def statistics():
    """成绩统计分析"""
    if not current_user.is_teacher():
        abort(403)

    problem_id = request.args.get('problem_id', type=int)

    # 所有题目
    problems = Problem.query.order_by(Problem.id).all()

    stats_data = []
    for p in problems:
        subs = Submission.query.filter_by(problem_id=p.id)
        total = subs.count()
        if total == 0:
            continue
        accepted = subs.filter_by(status='accepted').count()
        avg_score = subs.with_entities(func.avg(Submission.score)).scalar() or 0
        max_score = subs.with_entities(func.max(Submission.score)).scalar() or 0

        stats_data.append({
            'problem_id': p.id,
            'title': p.title,
            'difficulty': p.difficulty,
            'total': total,
            'accepted': accepted,
            'accept_rate': round(accepted / total * 100, 1) if total > 0 else 0,
            'avg_score': round(avg_score, 1),
            'max_score': max_score,
        })

    return render_template('admin/statistics.html',
                           stats_data=stats_data,
                           problems=problems)


@admin_bp.route('/student_stats')
@login_required
def student_stats():
    """每个学生每次实验的成绩明细"""
    if not current_user.is_teacher():
        abort(403)

    class_id = request.args.get('class_id', type=int)

    # 获取所有班级
    classes = Class.query.order_by(Class.name).all()

    # 获取所有实验题（按实验序号排序）
    experiments = Problem.query.filter(
        Problem.experiment_order > 0
    ).order_by(Problem.experiment_order).all()

    # 获取学生列表（可筛选班级）
    query = User.query.filter_by(role='student')
    if class_id:
        query = query.filter_by(class_id=class_id)
    students = query.order_by(User.real_name, User.username).all()

    # 构建成绩矩阵
    grade_colors = {
        '优': '#27ae60',
        '良': '#2ecc71',
        '中': '#f39c12',
        '及格': '#e67e22',
        '不及格': '#e74c3c',
    }

    student_rows = []
    for student in students:
        row = {
            'student': student,
            'scores': {},
            'total_score': 0,
            'total_max': 0,
            'experiment_count': 0,
        }
        for exp in experiments:
            # 找该生在该题的最高分提交
            best = Submission.query.filter_by(
                user_id=student.id,
                problem_id=exp.id,
            ).order_by(Submission.score.desc()).first()

            if best:
                level = best.grade_level or best.calc_grade_level()
                row['scores'][exp.id] = {
                    'score': best.score,
                    'max_score': best.max_score,
                    'level': level,
                    'submission_id': best.id,
                }
                row['total_score'] += best.score
                row['total_max'] += best.max_score
                row['experiment_count'] += 1
            else:
                row['scores'][exp.id] = None

        # 计算综合等级
        if row['experiment_count'] > 0 and row['total_max'] > 0:
            pct = row['total_score'] / row['total_max'] * 100
            if pct >= 90:
                row['final_level'] = '优'
            elif pct >= 80:
                row['final_level'] = '良'
            elif pct >= 70:
                row['final_level'] = '中'
            elif pct >= 60:
                row['final_level'] = '及格'
            else:
                row['final_level'] = '不及格'
            row['final_pct'] = round(pct, 1)
        else:
            row['final_level'] = '-'
            row['final_pct'] = 0

        student_rows.append(row)

    return render_template('admin/student_stats.html',
                           classes=classes,
                           class_id=class_id,
                           experiments=experiments,
                           student_rows=student_rows,
                           grade_colors=grade_colors)


@admin_bp.route('/plagiarism')
@login_required
def plagiarism():
    """查重检测页面"""
    if not current_user.is_teacher():
        abort(403)

    problems = Problem.query.order_by(Problem.id).all()
    results = []
    selected_problem = None
    problem_id = request.args.get('problem_id', type=int)
    threshold = request.args.get('threshold', 0.75, type=float)

    if problem_id:
        selected_problem = db.session.get(Problem, problem_id)
        if selected_problem:
            results = find_plagiarism(problem_id, threshold=threshold)

    return render_template('admin/plagiarism.html',
                           problems=problems,
                           results=results,
                           selected_problem=selected_problem,
                           threshold=threshold)


@admin_bp.route('/plagiarism/compare')
@login_required
def plagiarism_compare():
    """代码对比页面（并排显示两段代码diff）"""
    if not current_user.is_teacher():
        abort(403)

    sub_a_id = request.args.get('a', type=int)
    sub_b_id = request.args.get('b', type=int)

    from app.models import Submission

    sub_a = db.session.get(Submission, sub_a_id)
    sub_b = db.session.get(Submission, sub_b_id)

    if not sub_a or not sub_b:
        abort(404)

    lines_a, lines_b = highlight_diff(sub_a.source_code, sub_b.source_code)

    return render_template('admin/compare.html',
                           sub_a=sub_a, sub_b=sub_b,
                           lines_a=lines_a, lines_b=lines_b)


@admin_bp.route('/users')
@login_required
def users():
    """用户管理"""
    if not current_user.is_teacher():
        abort(403)

    users = User.query.order_by(User.role, User.username).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/<int:user_id>/set_role', methods=['POST'])
@login_required
def set_role(user_id):
    """设置用户角色（教师专用）"""
    if not current_user.is_teacher():
        abort(403)

    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    # 不能改自己的角色
    if user.id == current_user.id:
        flash('不能修改自己的角色', 'danger')
        return redirect(url_for('admin.users'))

    new_role = request.form.get('role', '')
    if new_role not in ('teacher', 'student'):
        flash('无效角色', 'danger')
        return redirect(url_for('admin.users'))

    user.role = new_role
    db.session.commit()
    flash(f'已将 {user.username} 设为{"教师" if new_role == "teacher" else "学生"}', 'success')
    return redirect(url_for('admin.users'))
