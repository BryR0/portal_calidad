from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.routes import admin_bp
from app.models.user import User
import secrets
import string


def require_admin():
    if not current_user.is_authenticated or not current_user.is_admin():
        abort(403)


@admin_bp.route('/users')
@login_required
def users():
    require_admin()
    all_users = User.query.order_by(User.username).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/create', methods=['POST'])
@login_required
def create_user():
    require_admin()
    username = request.form.get('username', '').strip()
    email    = request.form.get('email', '').strip() or None
    role     = request.form.get('role', 'user')
    password = request.form.get('password', '')

    if not username or not password:
        flash('Usuario y contraseña son requeridos', 'error')
        return redirect(url_for('admin.users'))

    if User.query.filter_by(username=username).first():
        flash(f'El usuario "{username}" ya existe', 'error')
        return redirect(url_for('admin.users'))

    if role not in ('admin', 'calidad', 'user'):
        role = 'user'

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    from app import db
    db.session.add(user)
    db.session.commit()
    flash(f'Usuario "{username}" creado exitosamente', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_user(user_id):
    require_admin()
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes desactivarte a ti mismo', 'error')
        return redirect(url_for('admin.users'))
    user.is_active = not user.is_active
    from app import db
    db.session.commit()
    state = 'activado' if user.is_active else 'desactivado'
    flash(f'Usuario "{user.username}" {state}', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@login_required
def reset_password(user_id):
    require_admin()
    user = User.query.get_or_404(user_id)
    # Generate a random 12-char password
    alphabet = string.ascii_letters + string.digits
    new_pwd = ''.join(secrets.choice(alphabet) for _ in range(12))
    user.set_password(new_pwd)
    from app import db
    db.session.commit()
    flash(f'Nueva contraseña para "{user.username}": {new_pwd}  (cópiala ahora)', 'warning')
    return redirect(url_for('admin.users'))
