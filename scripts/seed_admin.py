"""
Crea el usuario administrador inicial en la base de datos.
Uso:
    cd portal_calidad
    python scripts/seed_admin.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()

    USERNAME = 'admin'
    EMAIL    = 'Admin@rimith.com'
    PASSWORD = 'Admin123!'
    ROLE     = 'admin'

    existing = User.query.filter_by(username=USERNAME).first()
    if existing:
        print(f'  Usuario "{USERNAME}" ya existe. Actualizando contraseña...')
        existing.set_password(PASSWORD)
        existing.email    = EMAIL
        existing.role     = ROLE
        existing.is_active = True
        db.session.commit()
        print(f'  Listo.')
    else:
        user = User(username=USERNAME, email=EMAIL, role=ROLE, is_active=True)
        user.set_password(PASSWORD)
        db.session.add(user)
        db.session.commit()
        print(f'  Usuario "{USERNAME}" creado con exito.')

    print()
    print('  ┌─────────────────────────────────┐')
    print(f'  │  Usuario : {USERNAME:<23}│')
    print(f'  │  Email   : {EMAIL:<23}│')
    print(f'  │  Password: {PASSWORD:<23}│')
    print(f'  │  Rol     : {ROLE:<23}│')
    print('  └─────────────────────────────────┘')
