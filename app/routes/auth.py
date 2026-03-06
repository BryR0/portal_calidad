from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models.user import User
from app.routes import auth_bp


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Dirección de correo no válida")])
    submit = SubmitField('Solicitar recuperación')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user is None:
            raise ValidationError('No hay una cuenta con ese correo electrónico. Registre una primero.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Nueva Contraseña', 
                                     validators=[DataRequired(), EqualTo('password', message="Las contraseñas deben coincidir")])
    submit = SubmitField('Restablecer Contraseña')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and user.is_active and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        flash('Usuario o contraseña inválidos', 'error')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def send_reset_email(user):
    from app import mail
    from flask_mail import Message
    from flask import current_app
    token = user.generate_reset_token()
    msg = Message('Petición de Restablecimiento de Contraseña',
                  sender=current_app.config['PORTAL_CALIDAD_MAIL_SENDER'],
                  recipients=[user.email])
    msg.body = f'''Para restablecer tu contraseña, haz clic en el siguiente enlace:
{url_for('auth.reset_token', token=token, _external=True)}

Si no realizaste esta petición, puedes ignorar este correo sin que se modifique tu cuenta.
'''
    msg.html = render_template('auth/email/reset_password.html', user=user, token=token)
    mail.send(msg)


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user:
            send_reset_email(user)
        flash('Se ha enviado un correo con instrucciones para restablecer tu contraseña.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title='Restablecer Contraseña', form=form)


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('El enlace es inválido o ha expirado.', 'error')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        from app import db
        db.session.commit()
        flash('Tu contraseña ha sido actualizada. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Restablecer Contraseña', form=form)
