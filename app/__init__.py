from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder.'
    login_manager.login_message_category = 'info'

    @app.context_processor
    def inject_url_helpers():
        from flask import request, url_for as _url_for
        def url_keep_args(endpoint, **overrides):
            args = dict(request.args)
            args.update(overrides)
            return _url_for(endpoint, **args)
        return dict(url_keep_args=url_keep_args)

    from app.routes import auth_bp, nc_bp, main_bp, admin_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(nc_bp, url_prefix='/nc')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp)

    return app
