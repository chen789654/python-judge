"""创建/修复教师账号"""
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.role = 'teacher'
        admin.set_password('123456')
        db.session.commit()
        print(f'教师账号已更新: admin / 123456 (角色={admin.role})')
    else:
        user = User(
            username='admin',
            email='admin@test.com',
            role='teacher',
            real_name='管理员',
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        print('教师账号创建成功: admin / 123456')
