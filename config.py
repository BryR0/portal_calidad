import os
from dotenv import load_dotenv

# Carga .env desde la raíz del proyecto (funciona tanto con flask run como con scripts directos)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')

    # SQLite por defecto (ruta absoluta para evitar confusión de CWD)
    _db_url = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "portal_calidad.db")}')

    db_engine = os.environ.get('DB_ENGINE', 'sqlite').lower()
    if db_engine == 'mysql':
        db_user = os.environ.get('DB_USER', 'root')
        db_pass = os.environ.get('DB_PASSWORD', '')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '3306')
        db_name = os.environ.get('DB_NAME', 'portal_calidad')
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    else:
        # SQLAlchemy 2.x requiere postgresql:// en vez de postgres://
        SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de correo
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    PORTAL_CALIDAD_MAIL_SUBJECT_PREFIX = '[Portal Calidad]'
    PORTAL_CALIDAD_MAIL_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Portal Calidad Admin <noreply@portalcalidad.com>')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}
