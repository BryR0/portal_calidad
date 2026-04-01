from run import app
from app import db
from app.models.user import User

target_email = 'admin@rimith.com'
new_password = 'Admin123!'

with app.app_context():
    user = User.query.filter_by(email=target_email).first()
    if user is None:
        print(f'ERROR: usuario con email {target_email} no encontrado')
    else:
        user.set_password(new_password)
        db.session.commit()
        print(f'OK: contraseña actualizada para {target_email}')
