import os
from app import create_app, db
from app.models.catalogs import CatalogItem

app = create_app('default')

catalogos_base = {
    'EVALUACION': [
        "Organoléptico/Organoleptic",
        "Físico/Physical",
        "Químico/Chemical",
        "Higiene/Hygiene",
        "Laboratorio/Laboratory",
    ],
    'PRERREQUISITO': [
        "Buenas Prácticas de Manufactura",
        "Control de Alérgenos",
        "Control de Almacenamiento y Distribución",
        "Control de Material Extraño",
        "Control de Procesos Operativos",
        "Control de Proveedores y Materia Prima",
        "Control de Químicos",
        "Control de Temperatura y Humedad Relativa",
        "Control Integral de Plagas",
        "Formación del Personal",
        "Gestión Ambiental de Residuos y Desechos",
        "Gestión de Desviaciones y Acciones Correctivas",
        "HACCP",
        "Higiene del Personal",
        "Limpieza y Desinfección (SSOP)",
        "Mantenimiento Preventivo",
        "Seguridad del Agua Potable",
        "Trazabilidad y Recall",
    ],
    'CAUSA': [
        "Mano de Obra",
        "Maquinaria",
        "Materia Prima",
        "Método",
    ]
}

def sembrar_catalogos():
    with app.app_context():
        # Crear todas las tablas si no existen según los Modelos SQLAlchemy
        db.create_all()
        print("Tablas de SQLAlchemy creadas/verificadas con éxito.")

        agregados = 0
        for categoria, valores in catalogos_base.items():
            for i, val in enumerate(valores):
                existe = CatalogItem.query.filter_by(category=categoria, value=val).first()
                if not existe:
                    nuevo_item = CatalogItem(category=categoria, value=val, sort_order=i)
                    db.session.add(nuevo_item)
                    agregados += 1
        
        if agregados > 0:
            db.session.commit()
            print(f"Éxito: Se sembraron {agregados} items nuevos en el catálogo.")
        else:
            print("No hubo ítems nuevos que agregar. Todo está al día.")

if __name__ == '__main__':
    sembrar_catalogos()
