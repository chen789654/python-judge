"""
管理面板路由

提供统计报表、成绩分析、查重检测等功能（教师专用）
"""
from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Problem, Submission, Class, TestCase
from app.services.plagiarism import find_plagiarism
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


@admin_bp.route('/users')
@login_required
def users():
    """用户管理"""
    if not current_user.is_teacher():
        abort(403)

    users = User.query.order_by(User.role, User.username).all()
    return render_template('admin/users.html', users=users)
