from app import create_app, db
from sqlalchemy import MetaData, inspect

app = create_app('default')
with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('secciones')
    col_names = [col['name'] for col in columns]
    print(f"Columnas halladas en 'secciones': {col_names}")
