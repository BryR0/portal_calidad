import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

db_user = os.environ.get('DB_USER', 'root')
db_pass = os.environ.get('DB_PASSWORD', '')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = int(os.environ.get('DB_PORT', '3306'))
db_name = os.environ.get('DB_NAME', 'portalcalidad')

secciones = [
    "Artesanal", "Carimañolas", "Carnicería", "Chocolatería", "Cocina Abierta",
    "Congelados", "Despacho", "Dulcería", "Embutidos", "Empanadas de maíz",
    "Empaque Artesanal", "Empaque de hierbas", "Empaque en mallas", "Empaque en vitafilm",
    "Ensaladas", "Fruta picada", "Galletas", "Gourmet", "Granel", "Helados",
    "IV Gama", "Lácteos", "Línea automática", "Línea semi automática", "Maduración",
    "Panes de mesa", "Panes y dulces", "Pastelería Fina", "Postres", "Prefrito",
    "Proveeduría", "Sanidad", "Simple step", "Tamales", "Tortillas congeladas",
    "Tortillas frescas", "Zumos y Pulpas", "Miel", "Vinagres y Aderezoz",
    "Panes congelados", "Snacks", "Hojaldres", "Ceviche"
]

# Eliminar duplicados manteniendo el orden
secciones_unicas = list(dict.fromkeys(secciones))


def limpiar_y_sembrar():
    try:
        conn = pymysql.connect(
            host=db_host, user=db_user, password=db_pass,
            database=db_name, port=db_port, cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        # 1. Eliminar tablas redundantes (si existen)
        tablas_a_eliminar = ['marcas', 'catalogos', 'proveedores', 'marca', 'catalogo', 'proveedor']
        for tabla in tablas_a_eliminar:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {tabla}")
                print(f"Tabla '{tabla}' eliminada o no existía.")
            except Exception as e:
                print(f"No se pudo eliminar {tabla}: {e}")

        # 2. Crear tabla de secciones si no existe (independientemente de SQLAlchemy por ahora)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS secciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                activa BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        print("Tabla 'secciones' verificada/creada.")

        # 3. Insertar secciones únicas
        agregadas = 0
        for sec in secciones_unicas:
            try:
                cursor.execute("INSERT IGNORE INTO secciones (nombre) VALUES (%s)", (sec,))
                if cursor.rowcount > 0:
                    agregadas += 1
            except Exception as e:
                print(f"Error insertando '{sec}': {e}")

        conn.commit()
        print(f"Éxito: Se insertaron {agregadas} secciones nuevas de un total de {len(secciones_unicas)} proporcionadas.")

    except Exception as e:
        print(f"Error general en BD: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


if __name__ == '__main__':
    limpiar_y_sembrar()
