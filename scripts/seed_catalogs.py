"""
Pobla las tablas de catálogo con los datos del Excel (portal.xlsm).
Uso:
    cd portal_calidad
    python scripts/seed_catalogs.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.catalogs import Empresa, Seccion, Marca, ClasificacionNC, CatalogItem
from app.models.nc import Provider, Department
from app.data.catalogs import (
    CLASIFICACION_NC, EMPRESAS, EMPRESA_CODIGOS,
    MARCAS, PROVEEDORES_POR_TIPO,
    SECCIONES_POR_PROVEEDOR, SECCIONES_POR_RIMITH,
    CAUSA, PRERREQUISITO, EVALUACION,
    DEPARTAMENTOS_INTERNOS,
)

app = create_app()

# ── helpers ────────────────────────────────────────────────────────────────
def upsert_all(model, rows, key='name'):
    added = updated = 0
    for row in rows:
        obj = model.query.filter_by(**{key: row[key]}).first()
        if obj:
            for k, v in row.items():
                setattr(obj, k, v)
            updated += 1
        else:
            db.session.add(model(**row))
            added += 1
    db.session.commit()
    return added, updated


with app.app_context():
    db.create_all()

    # ── 1. Empresas ─────────────────────────────────────────────────────────
    codigo_inv = {v: k for k, v in EMPRESA_CODIGOS.items()}
    emp_rows = [{'name': n, 'codigo': codigo_inv.get(n, ''), 'is_active': True}
                for n in EMPRESAS]
    a, u = upsert_all(Empresa, emp_rows)
    print(f'  Empresas:         {a} nuevas, {u} actualizadas')

    # ── 2. Secciones ─────────────────────────────────────────────────────────
    sec_rows = []
    order = 0

    # Secciones para cada tipo de proveedor (no-Rimith)
    for tipo, secciones in SECCIONES_POR_PROVEEDOR.items():
        if tipo == 'Rimith':
            continue  # Rimith se maneja por sub-depto
        for name in secciones:
            sec_rows.append({
                'name': name.strip(),
                'provider_tipo': tipo,
                'rimith_dept': None,
                'is_active': True,
                'sort_order': order,
            })
            order += 1

    # Secciones Rimith organizadas por sub-depto
    for dept, secciones in SECCIONES_POR_RIMITH.items():
        for name in secciones:
            sec_rows.append({
                'name': name.strip(),
                'provider_tipo': 'Rimith',
                'rimith_dept': dept,
                'is_active': True,
                'sort_order': order,
            })
            order += 1

    # Upsert por (name + provider_tipo + rimith_dept)
    added = updated = 0
    for row in sec_rows:
        obj = Seccion.query.filter_by(
            name=row['name'],
            provider_tipo=row['provider_tipo'],
            rimith_dept=row['rimith_dept']
        ).first()
        if obj:
            for k, v in row.items():
                setattr(obj, k, v)
            updated += 1
        else:
            db.session.add(Seccion(**row))
            added += 1
    db.session.commit()
    print(f'  Secciones:        {added} nuevas, {updated} actualizadas')

    # ── 3. Marcas ────────────────────────────────────────────────────────────
    marca_rows = [{'name': m.strip(), 'is_active': True} for m in MARCAS]
    a, u = upsert_all(Marca, marca_rows)
    print(f'  Marcas:           {a} nuevas, {u} actualizadas')

    # ── 4. Clasificaciones NC ────────────────────────────────────────────────
    def _grupo(name):
        n = name.lower()
        if 'material extraño' in n:      return 'Material extraño'
        if 'perfil no conforme' in n:    return 'Perfil no conforme'
        if 'falla de etiquetado' in n:   return 'Etiquetado'
        if 'falla de empaque' in n:      return 'Empaque'
        if 'falla de embalaje' in n:     return 'Empaque'
        if 'falla de despacho' in n:     return 'Despacho'
        if 'falla de higiene' in n:      return 'Higiene'
        if 'falla de limpieza' in n:     return 'Higiene'
        if 'contaminación' in n:         return 'Contaminación'
        if 'temperatura' in n:           return 'Temperatura'
        if 'moho' in n:                  return 'Microbiología'
        if 'inocuidad' in n:             return 'Inocuidad'
        return 'Otro'

    cls_rows = []
    for i, name in enumerate(CLASIFICACION_NC):
        cls_rows.append({
            'name': name.strip(),
            'grupo': _grupo(name),
            'is_active': True,
            'sort_order': i,
        })
    a, u = upsert_all(ClasificacionNC, cls_rows)
    print(f'  Clasificaciones:  {a} nuevas, {u} actualizadas')

    # ── 5. CatalogItems: CAUSA / PRERREQUISITO / EVALUACION ─────────────────
    catalog_data = [
        ('CAUSA',        CAUSA),
        ('PRERREQUISITO', PRERREQUISITO),
        ('EVALUACION',   EVALUACION),
    ]
    for category, values in catalog_data:
        added = updated = 0
        for i, val in enumerate(values):
            obj = CatalogItem.query.filter_by(category=category, value=val).first()
            if obj:
                obj.sort_order = i
                updated += 1
            else:
                db.session.add(CatalogItem(
                    category=category, value=val,
                    is_active=True, sort_order=i
                ))
                added += 1
        db.session.commit()
        print(f'  CatalogItem [{category:<15}]: {added} nuevos, {updated} actualizados')

    # ── 6. Proveedores ───────────────────────────────────────────────────────
    added = updated = 0
    for tipo, nombres in PROVEEDORES_POR_TIPO.items():
        for name in nombres:
            name = name.strip()
            obj = Provider.query.filter_by(name=name, provider_type=tipo).first()
            if obj:
                obj.is_active = True
                updated += 1
            else:
                db.session.add(Provider(name=name, provider_type=tipo, is_active=True))
                added += 1
    db.session.commit()
    print(f'  Proveedores:      {added} nuevos, {updated} actualizados')

    # ── 7. Departments (para DE / FROM y usuarios) ──────────────────────────
    dept_rows = [{'name': d} for d in DEPARTAMENTOS_INTERNOS]
    a, u = upsert_all(Department, dept_rows)
    print(f'  Departments:      {a} nuevos, {u} actualizados')

    print()
    print('  OK - Catalogos listos.')
