"""班级管理路由"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Class, User, Exam
from app.utils.helpers import generate_invite_code

classes_bp = Blueprint('classes', __name__, template_folder='../templates/classes')


@classes_bp.route('/')
@login_required
def dashboard():
    """班级面板"""
    if current_user.is_teacher():
        # 教师：自己创建的班级
        my_classes = Class.query.filter_by(teacher_id=current_user.id).all()
        return render_template('classes/teacher_dashboard.html', classes=my_classes)
    else:
        # 学生：所在的班级
        my_class = current_user.class_
        return render_template('classes/student_dashboard.html', class_=my_class)


@classes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建班级（教师）"""
    if not current_user.is_teacher():
        abort(403)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('班级名称不能为空', 'danger')
            return render_template('classes/create.html')

        # 生成唯一邀请码
        invite_code = generate_invite_code()
        while Class.query.filter_by(invite_code=invite_code).first():
            invite_code = generate_invite_code()

        class_ = Class(
            name=name,
            invite_code=invite_code,
            teacher_id=current_user.id,
        )
        db.session.add(class_)
        db.session.commit()
        flash(f'班级 "{name}" 创建成功！邀请码: {invite_code}', 'success')
        return redirect(url_for('classes.dashboard'))

    return render_template('classes/create.html')


@classes_bp.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    """加入班级（学生）"""
    if current_user.is_teacher():
        flash('教师无需加入班级', 'warning')
        return redirect(url_for('classes.dashboard'))

    if request.method == 'POST':
        code = request.form.get('invite_code', '').strip().upper()
        class_ = Class.query.filter_by(invite_code=code).first()

        if not class_:
            flash('邀请码无效', 'danger')
            return render_template('classes/join.html')

        # 如果已在该班级
        if current_user.class_id == class_.id:
            flash('你已在该班级中', 'info')
            return redirect(url_for('classes.dashboard'))

        current_user.class_id = class_.id
        db.session.commit()
        flash(f'成功加入班级: {class_.name}', 'success')
        return redirect(url_for('classes.dashboard'))

    return render_template('classes/join.html')


@classes_bp.route('/<int:class_id>')
@login_required
def detail(class_id):
    """班级详情"""
    class_ = db.session.get(Class, class_id)
    if not class_:
        abort(404)

    # 只有教师和班级成员可查看
    if class_.teacher_id != current_user.id and current_user.class_id != class_id:
        abort(403)

    students = class_.students.order_by(User.username).all()
    exams = class_.exams.order_by(Exam.created_at.desc()).all()

    return render_template('classes/detail.html',
                           class_=class_,
                           students=students,
                           exams=exams)
