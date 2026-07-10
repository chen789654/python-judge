"""提交记录路由"""
from flask import Blueprint, render_template, request, abort, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Submission, TestResult, Problem


submissions_bp = Blueprint('submissions', __name__,
                           template_folder='../templates/submissions')


@submissions_bp.route('/<int:submission_id>')
@login_required
def result(submission_id):
    """查看提交结果"""
    submission = db.session.get(Submission, submission_id)
    if not submission:
        abort(404)

    # 只能看自己的（教师可以看所有）
    if submission.user_id != current_user.id and not current_user.is_teacher():
        abort(403)

    problem = db.session.get(Problem, submission.problem_id)
    test_results = submission.test_results.order_by(TestResult.id).all()

    return render_template('submissions/result.html',
                           submission=submission,
                           problem=problem,
                           test_results=test_results)


@submissions_bp.route('/<int:submission_id>/comment', methods=['POST'])
@login_required
def comment(submission_id):
    """教师保存评语"""
    if not current_user.is_teacher():
        abort(403)

    submission = db.session.get(Submission, submission_id)
    if not submission:
        abort(404)

    teacher_comment = request.form.get('comment', '').strip()
    submission.teacher_comment = teacher_comment
    db.session.commit()

    flash('评语已保存', 'success')
    return redirect(url_for('submissions.result', submission_id=submission_id))

@submissions_bp.route('/history')
@login_required
def history():
    """提交历史"""
    page = request.args.get('page', 1, type=int)
    problem_id = request.args.get('problem_id', type=int)

    query = Submission.query

    if current_user.is_teacher() and request.args.get('all'):
        # 教师查看所有
        pass
    else:
        query = query.filter_by(user_id=current_user.id)

    if problem_id:
        query = query.filter_by(problem_id=problem_id)

    submissions = query.order_by(Submission.submitted_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('submissions/history.html', submissions=submissions)


@submissions_bp.route('/api/<int:submission_id>/status')
@login_required
def api_status(submission_id):
    """API: 查询提交状态（用于前端轮询）"""
    submission = db.session.get(Submission, submission_id)
    if not submission:
        return jsonify({'error': 'not found'}), 404

    return jsonify({
        'id': submission.id,
        'status': submission.status,
        'score': submission.score,
        'exec_time': submission.exec_time,
    })
