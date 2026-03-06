from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, or_
from app.routes import main_bp
from app.models.nc import NonConformity
from app.models.maestras import ReporteMaestro, RSBodega, RSInvPorDia


def _as_float(value):
    return float(value or 0)


def _latest_inventory_rows(item_code):
    rows = (RSInvPorDia.query
            .filter_by(item=item_code)
            .order_by(RSInvPorDia.bodega.asc(), RSInvPorDia.fecha.desc())
            .all())

    latest = {}
    for row in rows:
        latest.setdefault(row.bodega, row)
    return list(latest.values())


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total':        NonConformity.query.count(),
        'abiertas':     NonConformity.query.filter_by(status='Abierta').count(),
        'cerradas':     NonConformity.query.filter(NonConformity.status.in_(['Cerrada', 'Cerrado'])).count(),
        'alta_gravedad': NonConformity.query.filter(NonConformity.gravity.in_(['Alta', 'Muy Alta'])).count(),
    }
    recent_ncs = NonConformity.query.order_by(NonConformity.created_at.desc()).limit(8).all()

    top_sections = (
        NonConformity.query
        .with_entities(NonConformity.section, func.count(NonConformity.id).label('cnt'))
        .filter(NonConformity.section.isnot(None))
        .group_by(NonConformity.section)
        .order_by(func.count(NonConformity.id).desc())
        .limit(5)
        .all()
    )

    return render_template(
        'main/dashboard.html',
        stats=stats,
        recent_ncs=recent_ncs,
        top_sections=top_sections,
        open_nc_count=stats['abiertas'],
    )


@main_bp.route('/existencias')
@login_required
def stock_check():
    q = request.args.get('q', '').strip()
    results = []

    if q:
        products = (ReporteMaestro.query
                    .filter(
                        ReporteMaestro.rechazado == 0,
                        or_(
                            ReporteMaestro.itemcod.ilike(f'%{q}%'),
                            ReporteMaestro.itemcodbarra.ilike(f'%{q}%'),
                            ReporteMaestro.itemnombre.ilike(f'%{q}%'),
                        ),
                    )
                    .order_by(ReporteMaestro.itemnombre)
                    .limit(10)
                    .all())

        bodegas = {b.bodega: b.nombre for b in RSBodega.query.order_by(RSBodega.nombre).all()}

        for product in products:
            inventory_rows = _latest_inventory_rows(product.itemcod)
            inventory = []
            for row in inventory_rows:
                cantidad = _as_float(row.cantidad)
                precio = _as_float(row.precio)
                inventory.append({
                    'bodega': row.bodega,
                    'nombre': bodegas.get(row.bodega, ''),
                    'cantidad': cantidad,
                    'precio': precio,
                    'total': round(cantidad * precio, 2),
                    'fecha': row.fecha,
                })

            inventory.sort(key=lambda item: item['cantidad'], reverse=True)
            results.append({
                'itemcod': product.itemcod,
                'barcode': product.itemcodbarra or '',
                'nombre': product.itemnombre or '',
                'marca': product.marcanomb or '',
                'suplidor': product.nomsuplidor or '',
                'precio': _as_float(product.precio),
                'inventories': inventory,
                'total_unidades': round(sum(item['cantidad'] for item in inventory), 2),
                'total_valor': round(sum(item['total'] for item in inventory), 2),
            })

    return render_template(
        'main/stock_check.html',
        q=q,
        results=results,
        open_nc_count=NonConformity.query.filter_by(status='Abierta').count(),
    )
