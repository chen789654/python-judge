"""用户认证路由"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('problems.list'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('problems.list'))
        flash('用户名或密码错误', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('problems.list'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        role = request.form.get('role', 'student')
        # 教师注册码验证
        if role == 'teacher':
            teacher_code = request.form.get('teacher_code', '').strip()
            valid_code = current_app.config.get('TEACHER_REGISTER_CODE', '20251003')
            if teacher_code != valid_code:
                flash('教师注册码错误', 'danger')
                return render_template('auth/register.html')
        real_name = request.form.get('real_name', '').strip()
        student_id = request.form.get('student_id', '').strip()

        # 校验
        errors = []
        if not username or len(username) < 3:
            errors.append('用户名至少3个字符')
        if not email or '@' not in email:
            errors.append('请输入有效邮箱')
        if not password or len(password) < 6:
            errors.append('密码至少6个字符')
        if password != confirm:
            errors.append('两次密码输入不一致')
        if not real_name:
            errors.append('请输入真实姓名')
        if not student_id:
            errors.append('请输入学号/工号')
        if User.query.filter_by(username=username).first():
            errors.append('用户名已存在')
        if User.query.filter_by(email=email).first():
            errors.append('邮箱已被注册')

        if errors:
            for e in errors:
                flash(e, 'danger')
        else:
            user = User(
                username=username,
                email=email,
                role=role,
                real_name=real_name,
                student_id=student_id,
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
