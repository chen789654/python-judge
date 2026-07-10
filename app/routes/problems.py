"""题库管理路由"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from markdown import markdown
from app.extensions import db
from app.models import Problem, TestCase, Submission

problems_bp = Blueprint('problems', __name__, template_folder='../templates/problems')


@problems_bp.route('/')
@login_required
def list():
    """题目列表"""
    page = request.args.get('page', 1, type=int)
    difficulty = request.args.get('difficulty', '')
    tag = request.args.get('tag', '')
    search = request.args.get('search', '').strip()

    query = Problem.query

    # 学生只能看到可见的题目
    if not current_user.is_teacher():
        query = query.filter_by(visible=True)

    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if tag:
        query = query.filter(Problem.tags.contains(tag))
    if search:
        query = query.filter(Problem.title.contains(search))

    problems = query.order_by(Problem.id.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('problems/list.html', problems=problems)


@problems_bp.route('/<int:problem_id>')
@login_required
def detail(problem_id):
    """题目详情"""
    problem = db.session.get(Problem, problem_id)
    if not problem:
        abort(404)
    if not problem.visible and not current_user.is_teacher():
        abort(404)

    # 渲染Markdown描述
    description_html = markdown(problem.description, extensions=['fenced_code', 'codehilite'])

    # 获取公开的测试用例（学生可见）
    public_cases = problem.test_cases.filter_by(is_public=True).all()

    # 获取当前用户对此题的提交记录
    user_submissions = Submission.query.filter_by(
        user_id=current_user.id, problem_id=problem_id
    ).order_by(Submission.submitted_at.desc()).limit(10).all()

    # 获取当前用户的最好成绩
    best = Submission.query.filter_by(
        user_id=current_user.id, problem_id=problem_id
    ).order_by(Submission.score.desc()).first()

    return render_template('problems/detail.html',
                           problem=problem,
                           description_html=description_html,
                           public_cases=public_cases,
                           submissions=user_submissions,
                           best=best)


@problems_bp.route('/<int:problem_id>/submit', methods=['GET', 'POST'])
@login_required
def submit(problem_id):
    """提交代码"""
    problem = db.session.get(Problem, problem_id)
    if not problem:
        abort(404)
    if not problem.visible and not current_user.is_teacher():
        abort(404)

    if request.method == 'POST':
        source_code = request.form.get('source_code', '')
        if not source_code.strip():
            flash('请输入代码', 'danger')
            return render_template('problems/editor.html', problem=problem)

        # 创建提交记录
        submission = Submission(
            user_id=current_user.id,
            problem_id=problem_id,
            source_code=source_code,
            language='python',
            status='pending',
        )
        db.session.add(submission)
        db.session.commit()

        # 异步或同步评测
        from app.services.judge import judge_submission
        try:
            judge_submission(submission)
        except Exception as e:
            submission.status = 'error'
            submission.compiler_message = f'系统错误: {str(e)}'
            db.session.commit()

        return redirect(url_for('submissions.result', submission_id=submission.id))

    return render_template('problems/editor.html', problem=problem)


# ─── 教师端：题目管理 ───

@problems_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建题目（教师）"""
    if not current_user.is_teacher():
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        input_desc = request.form.get('input_description', '').strip()
        output_desc = request.form.get('output_description', '').strip()
        sample_input = request.form.get('sample_input', '').strip()
        sample_output = request.form.get('sample_output', '').strip()
        difficulty = request.form.get('difficulty', 'easy')
        tags = request.form.get('tags', '').strip()
        visible = request.form.get('visible') == 'on'

        if not title or not description:
            flash('标题和描述不能为空', 'danger')
            return render_template('problems/form.html')

        problem = Problem(
            title=title,
            description=description,
            input_description=input_desc,
            output_description=output_desc,
            sample_input=sample_input,
            sample_output=sample_output,
            difficulty=difficulty,
            tags=tags,
            visible=visible,
            created_by=current_user.id,
        )
        db.session.add(problem)
        db.session.commit()
        flash('题目创建成功，请添加测试用例', 'success')
        return redirect(url_for('problems.edit', problem_id=problem.id))

    return render_template('problems/form.html', problem=None)


@problems_bp.route('/<int:problem_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(problem_id):
    """编辑题目（教师）"""
    if not current_user.is_teacher():
        abort(403)
    problem = db.session.get(Problem, problem_id)
    if not problem:
        abort(404)

    if request.method == 'POST':
        problem.title = request.form.get('title', '').strip()
        problem.description = request.form.get('description', '').strip()
        problem.input_description = request.form.get('input_description', '').strip()
        problem.output_description = request.form.get('output_description', '').strip()
        problem.sample_input = request.form.get('sample_input', '').strip()
        problem.sample_output = request.form.get('sample_output', '').strip()
        problem.difficulty = request.form.get('difficulty', 'easy')
        problem.tags = request.form.get('tags', '').strip()
        problem.visible = request.form.get('visible') == 'on'
        db.session.commit()
        flash('题目已更新', 'success')
        return redirect(url_for('problems.detail', problem_id=problem.id))

    return render_template('problems/form.html', problem=problem)


@problems_bp.route('/<int:problem_id>/delete', methods=['POST'])
@login_required
def delete(problem_id):
    """删除题目（教师）"""
    if not current_user.is_teacher():
        abort(403)
    problem = db.session.get(Problem, problem_id)
    if not problem:
        abort(404)
    db.session.delete(problem)
    db.session.commit()
    flash('题目已删除', 'success')
    return redirect(url_for('problems.list'))


@problems_bp.route('/<int:problem_id>/testcases', methods=['GET', 'POST'])
@login_required
def manage_testcases(problem_id):
    """管理测试用例（教师）"""
    if not current_user.is_teacher():
        abort(403)
    problem = db.session.get(Problem, problem_id)
    if not problem:
        abort(404)

    if request.method == 'POST':
        input_data = request.form.get('input_data', '')
        expected_output = request.form.get('expected_output', '').strip()
        is_public = request.form.get('is_public') == 'on'
        score_weight = request.form.get('score_weight', 1, type=float)

        if not expected_output:
            flash('期望输出不能为空', 'danger')
            return redirect(url_for('problems.manage_testcases', problem_id=problem_id))

        max_order = db.session.query(db.func.max(TestCase.sort_order))\
            .filter_by(problem_id=problem_id).scalar()
        next_order = (max_order or 0) + 1

        tc = TestCase(
            problem_id=problem_id,
            input_data=input_data,
            expected_output=expected_output,
            is_public=is_public,
            score_weight=score_weight,
            sort_order=next_order,
        )
        db.session.add(tc)
        db.session.commit()
        flash('测试用例已添加', 'success')
        return redirect(url_for('problems.manage_testcases', problem_id=problem_id))

    test_cases = problem.test_cases.order_by(TestCase.sort_order).all()
    return render_template('problems/testcases.html', problem=problem, test_cases=test_cases)
