from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.routes import admin_bp
from app.models.user import User, Role, Permission
from app.utils.decorators import permission_required
import secrets
import string


def require_admin():
    if not current_user.is_authenticated or not current_user.has_permission('user_manage'):
        abort(403)


@admin_bp.route('/users')
@login_required
@permission_required('user_manage')
def users():
    all_users = User.query.order_by(User.username).all()
    all_roles = Role.query.all()
    return render_template('admin/users.html', users=all_users, all_roles=all_roles)


@admin_bp.route('/users/create', methods=['POST'])
@login_required
@permission_required('user_manage')
def create_user():
    username = request.form.get('username', '').strip()
    email    = request.form.get('email', '').strip() or None
    role_names = request.form.getlist('roles')
    password = request.form.get('password', '')

    if not username or not password:
        flash('Usuario y contraseña son requeridos', 'error')
        return redirect(url_for('admin.users'))

    if User.query.filter_by(username=username).first():
        flash(f'El usuario "{username}" ya existe', 'error')
        return redirect(url_for('admin.users'))

    # Compatible with old 'role' string for now (optional)
    legacy_role = 'user'
    if 'admin' in role_names: legacy_role = 'admin'
    elif 'calidad' in role_names: legacy_role = 'calidad'

    user = User(username=username, email=email, role=legacy_role)
    user.set_password(password)
    
    # Assign new roles
    for rname in role_names:
        r = Role.query.filter_by(name=rname).first()
        if r:
            user.roles.append(r)

    from app import db
    db.session.add(user)
    db.session.commit()
    flash(f'Usuario "{username}" creado exitosamente', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@permission_required('user_manage')
def toggle_user(user_id):
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
@permission_required('user_manage')
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    # Generate a random 12-char password
    alphabet = string.ascii_letters + string.digits
    new_pwd = ''.join(secrets.choice(alphabet) for _ in range(12))
    user.set_password(new_pwd)
    from app import db
    db.session.commit()
    flash(f'Nueva contraseña para "{user.username}": {new_pwd}  (cópiala ahora)', 'warning')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/edit', methods=['POST'])
@login_required
@permission_required('user_manage')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip() or None
    role_names = request.form.getlist('roles')

    if not username:
        flash('El nombre de usuario es requerido', 'error')
        return redirect(url_for('admin.users'))

    existing_user = User.query.filter_by(username=username).first()
    if existing_user and existing_user.id != user.id:
        flash(f'El usuario "{username}" ya existe', 'error')
        return redirect(url_for('admin.users'))

    user.username = username
    user.email = email
    
    # Update roles
    user.roles = []
    for rname in role_names:
        r = Role.query.filter_by(name=rname).first()
        if r:
            user.roles.append(r)
            
    # Compatible with legacy 'role' column
    if 'admin' in role_names: user.role = 'admin'
    elif 'calidad' in role_names: user.role = 'calidad'
    else: user.role = 'user'

    from app import db
    db.session.commit()
    flash(f'Usuario "{username}" actualizado correctamente', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@permission_required('user_manage')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta', 'error')
        return redirect(url_for('admin.users'))
    
    from app import db
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario "{user.username}" eliminado permanentemente', 'success')
    return redirect(url_for('admin.users'))
