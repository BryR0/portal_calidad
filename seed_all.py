import os
from app import create_app, db
from app.models.catalogs import CatalogItem, ClasificacionNC, Seccion

app = create_app('default')

# 1. CATALOG ITEMS
catalogos = {
    'EVALUACION': [
        "Organoléptico/Organoleptic", "Físico/Physical", "Químico/Chemical",
        "Higiene/Hygiene", "Laboratorio/Laboratory"
    ],
    'PRERREQUISITO': [
        "Buenas Prácticas de Manufactura", "Control de Alérgenos",
        "Control de Almacenamiento y Distribución", "Control de Material Extraño",
        "Control de Procesos Operativos", "Control de Proveedores y Materia Prima",
        "Control de Químicos", "Control de Temperatura y Humedad Relativa",
        "Control Integral de Plagas", "Formación del Personal",
        "Gestión Ambiental de Residuos y Desechos",
        "Gestión de Desviaciones y Acciones Correctivas", "HACCP",
        "Higiene del Personal", "Limpieza y Desinfección (SSOP)",
        "Mantenimiento Preventivo", "Seguridad del Agua Potable",
        "Trazabilidad y Recall"
    ],
    'CAUSA': [
        "Mano de Obra", "Maquinaria", "Materia Prima", "Método"
    ]
}

# 2. SECCIONES
secciones_rimith = [
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

# 3. CLASIFICACION NC
clasificaciones = [
    "Artículo defectuoso", "Bajo contenido neto", "Contenido neto no conforme",
    "Contaminación biológica (gorgojo)", "Contaminación biológica (insecto)",
    "Contaminación cruzada", "Contaminación Química", "Falla de limpieza",
    "Falla de despacho (mercancía erronea)", "Falla de despacho (condensación)",
    "Falla de embalaje", "Falla de empaque (humedo)", "Falla de empaque (perdida de vacio)",
    "Falla de empaque (roto)", "Falla de empaque (oxido)", "Falla de empaque (se adhiere al producto)",
    "Falla de empaque (sellado)", "Falla de empaque (soplado)", "Falla de empaque (se abre)",
    "Falla de etiquetado (borrosa)", "Falla de etiquetado (falta de información)",
    "Falla de etiquetado (descripción incorrecta)", "Falla de etiquetado (sin fecha de vencimeinto)",
    "Falla de etiquetado (doble fecha)", "Falla de etiquetado (fecha corta)",
    "Falla de etiquetado (fecha tapada/cortada)", "Falla de etiquetado (fecha incorrecta)",
    "Falla de etiquetado (fecha no legible)", "Falla de etiquetado (precio incorrecto)",
    "Falla de etiquetado (se desprende)", "Falla de etiquetado (sin etiqueta)",
    "Falla de etiquetado (reetiquetado)", "Falla de etiquetado (No cumple con lo declarado)",
    "Falla de llenado", "Falla de higiene (material auxiliar de transporte)",
    "Falla de higiene (transporte)", "Falla de Rotación (fecha proxima a vencer)",
    "Falla en el empaque (oxido)", "Falla en dimensiones", "Inocuidad",
    "Material extraño", "material extraño (accesos)", "Material extraño (articulos del personal)",
    "Material extraño (astillas de madera)", "Material extraño (cabello)",
    "Material extraño (cartón)", "Material extraño (cascara)",
    "Material extraño (equipos y herramientas de mantenimiento)", "Material extraño (escama)",
    "Material extraño (hilo)", "Material extraño (hueso)", "material extraño (material vegetal)",
    "Material extraño (metal)", "Material extraño (orgánico)", "Material extraño (piedra)",
    "Material extraño (plástico)", "Material extraño (restos de carbón)",
    "Material extraño (sedimentos)", "Material extraño (vidrio)", "Material extraño (tornillo)",
    "Material extraño (papel)", "Moho", "Parámetros fisicoquímicos fuera de rango",
    "Perfil no conforme (sabor y olor)", "Perfil no conforme (Color y textura)",
    "Perfil no conforme (Sabor y color)", "Perfil no conforme (Sabor y textura)",
    "Perfil no conforme (sabor, textura y olor)", "Perfil no conforme (color y olor)",
    "Perfil no conforme (abiertas)", "Perfil no conforme (apariencia)", "Perfil no conforme (color)",
    "Perfil no conforme (crudo)", "Perfil no conforme (cuarteado, separación)",
    "Perfil no conforme (dañado)", "Perfil no conforme (dimensión)", "Perfil no conforme (espesor)",
    "Perfil no conforme (exceso de grasa)", "Perfil no conforme (Fermentado)",
    "Perfil no conforme (liberación de liquido)", "Perfil no conforme (limpieza de materia prima)",
    "Perfil no conforme (grasa)", "Perfil no conforme (Maduración)", "Perfil no conforme (Mancha)",
    "Perfil no conforme (microbiología)", "Perfil no conforme (olor)",
    "perfil no conforme (oxidación)", "Perfil no conforme (roto)", "Perfil no conforme (sabor)",
    "Perfil no conforme (se abren)", "Perfil No Conforme (Separación)",
    "Perfil no Conforme (Resistencia)", "Perfil no conforme (sin relleno)",
    "Perfil no conforme (textura)", "Perfil no conforme (volumen)", "Temperatura no conforme",
    "Sin Registro Sanitario", "Olor extraño (no conforme)",
    "Perfil no conforme (liberación de liquido y mal olor)",
    "Perfil no conforme (liberación de liquido y pérdida de vacío)", "Perfil no conforme (húmedo)",
    "Falla de empaque (traspaso de grasa)", "Perfil no conforme (quebrado)",
    "Perfil no conforme (sedimentos)", "Deterioro de etiqueta y empaque",
    "Perfil no conforme (solidificado)", "Perfil no conforme (cuarteado y sabor agrio)",
    "Pérdida de integridad de empaque",
    "Falla de etiquetado (Producto no declara registro Sanitario y pais de origen)",
    "Perfil no conforme (Carbonatación no percibida)"
]

def obtener_grupo(nombre):
    nl = nombre.lower()
    if 'falla de empaque' in nl or 'falla en el empaque' in nl: return 'Falla de empaque'
    if 'falla de etiquetado' in nl: return 'Falla de etiquetado'
    if 'falla de higiene' in nl: return 'Falla de higiene'
    if 'falla de despacho' in nl: return 'Falla de despacho'
    if 'material extraño' in nl: return 'Material extraño'
    if 'perfil no conforme' in nl: return 'Perfil no conforme'
    if 'contaminación' in nl: return 'Contaminación'
    return 'Otros'

def run_seed():
    with app.app_context():
        # 1. Catalog Items
        print("--- Sembrando ITEMS DE CATÁLOGO (Evaluación, Causa, Prerrequisito) ---")
        for categoria, items in catalogos.items():
            for i, val in enumerate(items):
                val = val.strip()
                ex = CatalogItem.query.filter_by(category=categoria, value=val).first()
                if not ex:
                    nuevo = CatalogItem(category=categoria, value=val, sort_order=i)
                    db.session.add(nuevo)

        # 2. Secciones
        print("--- Sembrando SECCIONES ---")
        secciones_unicas = list(set(secciones_rimith)) # Quitar duplicados
        for i, sec_name in enumerate(secciones_unicas):
            sec_name = sec_name.strip()
            # Asumimos provider_tipo='Rimith'
            ex_s = Seccion.query.filter_by(name=sec_name).first()
            if not ex_s:
                ns = Seccion(name=sec_name, provider_tipo='Rimith', rimith_dept='Produccion', sort_order=i)
                db.session.add(ns)

        # 3. Clasificaciones
        print("--- Sembrando CLASIFICACIÓN DE NO CONFORMIDADES ---")
        for i, c_name in enumerate(clasificaciones):
            c_name = c_name.strip()
            if c_name:
                c_name = c_name[0].upper() + c_name[1:]
                ex_c = ClasificacionNC.query.filter_by(name=c_name).first()
                if not ex_c:
                    grupo = obtener_grupo(c_name)
                    nc_c = ClasificacionNC(name=c_name, grupo=grupo, sort_order=i)
                    db.session.add(nc_c)
                    
        db.session.commit()
        print("=== SEMILLADO COMPLETADO ÉXITOSAMENTE ===")

if __name__ == '__main__':
    run_seed()
