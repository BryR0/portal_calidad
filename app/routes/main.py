from collections import Counter, defaultdict
from datetime import date

from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.routes import main_bp
from app.models.nc import NonConformity
from app.models.maestras import ReporteMaestro, RSBodega, RSInvPorDia


CLOSED_STATUSES = ('Cerrada', 'Cerrado')
HIGH_GRAVITY = {'Alta', 'Muy Alta'}
MONTH_LABELS = ('Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic')
LONG_MONTH_LABELS = ('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')
ANALYTICS_COLORS = ('#4338ca', '#0ea5e9', '#14b8a6', '#f59e0b', '#ef4444', '#8b5cf6')


def _as_float(value):
    return float(value or 0)


def _safe_label(value, fallback='Sin dato'):
    if value is None:
        return fallback
    if isinstance(value, str):
        value = value.strip()
        return value or fallback
    return value


def _is_closed(status):
    return _safe_label(status, '').lower() in {'cerrada', 'cerrado'}


def _pct(part, total):
    return round((part / total) * 100, 1) if total else 0


def _format_decimal(value, decimals=2):
    formatted = f'{value:,.{decimals}f}'
    return formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted


def _month_start(value):
    return date(value.year, value.month, 1)


def _shift_month(value, delta):
    month_index = (value.year * 12 + value.month - 1) + delta
    year, month = divmod(month_index, 12)
    return date(year, month + 1, 1)


def _month_label(value):
    return f'{MONTH_LABELS[value.month - 1]} {value.year}'


def _build_breakdown(counter, colors, limit=None):
    total = sum(counter.values())
    items = []

    for index, (label, count) in enumerate(counter.most_common(limit)):
        share = (count / total) * 100 if total else 0
        items.append({
            'label': label,
            'count': count,
            'pct': round(share, 1),
            'share': share,
            'color': colors[index % len(colors)],
        })

    return items


def _build_donut_gradient(items):
    if not items:
        return 'conic-gradient(#e5e7eb 0 100%)'

    start = 0.0
    segments = []
    for item in items:
        end = min(100.0, start + item['share'])
        segments.append(f"{item['color']} {start:.2f}% {end:.2f}%")
        start = end

    if start < 100.0:
        segments.append(f'#e5e7eb {start:.2f}% 100%')

    return f"conic-gradient({', '.join(segments)})"


def _normalize_filter_value(value):
    value = _safe_label(value, '').strip()
    return value if value and value.lower() != 'all' else ''


def _extract_branch_code(empresa_value):
    empresa = _normalize_filter_value(empresa_value)
    if ' - ' in empresa:
        return empresa.split(' - ', 1)[0].strip()
    return empresa


def _short_label(value, max_len=18):
    value = _safe_label(value)
    return value if len(value) <= max_len else f'{value[:max_len - 1]}...'


def _branch_short_label(value):
    label = _safe_label(value)
    code = _extract_branch_code(label)
    if code and code != label and len(code) <= 8:
        return code
    return _short_label(label, 14)


def _bar_height(value, max_value, min_height=12):
    if not value or not max_value:
        return 0
    return max(min_height, int((value / max_value) * 100))


def _build_month_axis(counter):
    max_count = max(counter.values(), default=0)
    items = []
    for month in range(1, 13):
        count = counter.get(month, 0)
        items.append({
            'month': month,
            'label': LONG_MONTH_LABELS[month - 1],
            'short_label': MONTH_LABELS[month - 1],
            'count': count,
            'height': _bar_height(count, max_count, min_height=16),
        })
    return items


def _build_stacked_month_axis(counter_map):
    totals = {month: sum(counter.get(month, 0) for counter in counter_map.values()) for month in range(1, 13)}
    max_total = max(totals.values(), default=0)
    items = []

    for month in range(1, 13):
        total = totals[month]
        preventiva = counter_map['Preventiva'].get(month, 0)
        correctiva = counter_map['Correctiva'].get(month, 0)
        otra = counter_map['Otra'].get(month, 0)
        items.append({
            'month': month,
            'label': LONG_MONTH_LABELS[month - 1],
            'short_label': MONTH_LABELS[month - 1],
            'total': total,
            'height': _bar_height(total, max_total, min_height=16),
            'preventiva': preventiva,
            'correctiva': correctiva,
            'otra': otra,
            'preventiva_pct': round((preventiva / total) * 100, 1) if total else 0,
            'correctiva_pct': round((correctiva / total) * 100, 1) if total else 0,
            'otra_pct': round((otra / total) * 100, 1) if total else 0,
        })

    return items


def _build_series(counter_map, labels, short_label_fn=None):
    max_value = 0
    for label in labels:
        for month in range(1, 13):
            max_value = max(max_value, counter_map[label].get(month, 0))

    items = []
    for index, label in enumerate(labels):
        month_items = []
        total = 0
        for month in range(1, 13):
            count = counter_map[label].get(month, 0)
            total += count
            month_items.append({
                'month': month,
                'short_label': MONTH_LABELS[month - 1],
                'count': count,
                'height': _bar_height(count, max_value, min_height=12),
            })
        items.append({
            'label': label,
            'short_label': short_label_fn(label) if short_label_fn else _short_label(label, 16),
            'color': ANALYTICS_COLORS[index % len(ANALYTICS_COLORS)],
            'total': total,
            'months': month_items,
        })

    return items


def _build_ranking(counter, limit=10):
    total = sum(counter.values())
    max_count = max(counter.values(), default=0)
    items = []

    for index, (label, count) in enumerate(counter.most_common(limit)):
        items.append({
            'rank': index + 1,
            'label': label,
            'count': count,
            'pct_total': _pct(count, total),
            'bar_pct': max(10, int((count / max_count) * 100)) if max_count else 0,
        })

    return items


def _analytics_filter_options():
    option_rows = (NonConformity.query
                   .with_entities(
                       NonConformity.date_detected,
                       NonConformity.provider_tipo,
                       NonConformity.deviation_type,
                       NonConformity.empresa,
                   )
                   .all())

    years = sorted({row.date_detected.year for row in option_rows if row.date_detected}, reverse=True)
    provider_types = sorted({_normalize_filter_value(row.provider_tipo) for row in option_rows if _normalize_filter_value(row.provider_tipo)})
    deviation_types = sorted({_normalize_filter_value(row.deviation_type) for row in option_rows if _normalize_filter_value(row.deviation_type)})
    bodegas = sorted({_normalize_filter_value(row.empresa) for row in option_rows if _normalize_filter_value(row.empresa)})

    return {
        'years': years,
        'provider_types': provider_types,
        'deviation_types': deviation_types,
        'bodegas': bodegas,
        'months': [{'value': month, 'label': LONG_MONTH_LABELS[month - 1]} for month in range(1, 13)],
    }


def _analytics_filters_from_request(args, options):
    valid_years = set(options['years'])
    valid_provider_types = set(options['provider_types'])
    valid_deviation_types = set(options['deviation_types'])
    valid_bodegas = set(options['bodegas'])

    selected_year = args.get('year', type=int)
    if selected_year not in valid_years:
        selected_year = options['years'][0] if options['years'] else date.today().year

    selected_month = args.get('month', type=int)
    if selected_month not in range(1, 13):
        selected_month = None

    provider_tipo = _normalize_filter_value(args.get('provider_tipo'))
    if provider_tipo not in valid_provider_types:
        provider_tipo = ''

    deviation_type = _normalize_filter_value(args.get('deviation_type'))
    if deviation_type not in valid_deviation_types:
        deviation_type = ''

    bodega = _normalize_filter_value(args.get('bodega'))
    if bodega not in valid_bodegas:
        bodega = ''

    return {
        'year': selected_year,
        'month': selected_month,
        'provider_tipo': provider_tipo,
        'deviation_type': deviation_type,
        'bodega': bodega,
    }


def _analytics_filter_summary(filters):
    parts = [f"Ano {filters['year']}"]

    if filters['month']:
        parts.append(LONG_MONTH_LABELS[filters['month'] - 1])
    if filters['provider_tipo']:
        parts.append(filters['provider_tipo'])
    if filters['deviation_type']:
        parts.append(filters['deviation_type'])
    if filters['bodega']:
        parts.append(_short_label(filters['bodega'], 28))

    return ' · '.join(parts)


def _latest_inventory_rows(item_code):
    rows = (RSInvPorDia.query
            .filter_by(item=item_code)
            .order_by(RSInvPorDia.bodega.asc(), RSInvPorDia.fecha.desc())
            .all())

    latest = {}
    for row in rows:
        latest.setdefault(row.bodega, row)
    return list(latest.values())


def _build_stock_result(product, bodegas):
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
    return {
        'itemcod': product.itemcod,
        'barcode': product.itemcodbarra or '',
        'nombre': product.itemnombre or '',
        'marca': product.marcanomb or '',
        'suplidor': product.nomsuplidor or '',
        'precio': _as_float(product.precio),
        'inventories': inventory,
        'total_unidades': round(sum(item['cantidad'] for item in inventory), 2),
        'total_valor': round(sum(item['total'] for item in inventory), 2),
    }


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    current_month = _month_start(today)
    previous_month = _shift_month(current_month, -1)
    month_range = [_shift_month(current_month, offset) for offset in range(-5, 1)]
    month_buckets = {
        month.strftime('%Y-%m'): {
            'label': _month_label(month),
            'short_label': MONTH_LABELS[month.month - 1],
            'count': 0,
            'high_risk': 0,
        }
        for month in month_range
    }

    rows = (NonConformity.query
            .with_entities(
                NonConformity.status,
                NonConformity.gravity,
                NonConformity.section,
                NonConformity.provider_tipo,
                NonConformity.motive,
                NonConformity.affects_inocuity,
                NonConformity.affects_consumer,
                NonConformity.affects_quality,
                NonConformity.date_detected,
                NonConformity.closure_date,
                NonConformity.total_units,
                NonConformity.total_usd,
            )
            .all())

    total = len(rows)
    abiertas = 0
    cerradas = 0
    alta_gravedad = 0
    inocuidad_flags = 0
    consumer_flags = 0
    quality_flags = 0
    stale_open = 0
    total_units = 0.0
    total_usd = 0.0
    close_days = []

    section_counter = Counter()
    provider_counter = Counter()
    motive_counter = Counter()
    status_counter = Counter()
    gravity_counter = Counter()

    for row in rows:
        status_label = 'Cerradas' if _is_closed(row.status) else 'Abiertas'
        gravity_label = _safe_label(row.gravity, 'Sin gravedad')
        section_label = _safe_label(row.section)
        provider_label = _safe_label(row.provider_tipo)
        motive_label = _safe_label(row.motive)
        detected_on = row.date_detected

        status_counter[status_label] += 1
        gravity_counter[gravity_label] += 1
        if section_label != 'Sin dato':
            section_counter[section_label] += 1
        if provider_label != 'Sin dato':
            provider_counter[provider_label] += 1
        if motive_label != 'Sin dato':
            motive_counter[motive_label] += 1

        if status_label == 'Abiertas':
            abiertas += 1
        else:
            cerradas += 1

        if row.gravity in HIGH_GRAVITY:
            alta_gravedad += 1

        if row.affects_inocuity or motive_label == 'Inocuidad':
            inocuidad_flags += 1
        if row.affects_consumer:
            consumer_flags += 1
        if row.affects_quality:
            quality_flags += 1

        total_units += _as_float(row.total_units)
        total_usd += _as_float(row.total_usd)

        if detected_on:
            month_key = detected_on.strftime('%Y-%m')
            if month_key in month_buckets:
                month_buckets[month_key]['count'] += 1
                if row.gravity in HIGH_GRAVITY:
                    month_buckets[month_key]['high_risk'] += 1

            if status_label == 'Abiertas' and (today - detected_on).days >= 30:
                stale_open += 1

        if row.closure_date and detected_on and _is_closed(row.status):
            close_days.append((row.closure_date - detected_on).days)

    max_month_count = max((item['count'] for item in month_buckets.values()), default=0)
    max_high_risk = max((item['high_risk'] for item in month_buckets.values()), default=0)
    monthly_trend = []
    for month in month_range:
        key = month.strftime('%Y-%m')
        bucket = month_buckets[key]
        monthly_trend.append({
            **bucket,
            'bar_height': max(16, int((bucket['count'] / max_month_count) * 100)) if bucket['count'] and max_month_count else 0,
            'high_bar_height': max(16, int((bucket['high_risk'] / max_high_risk) * 100)) if bucket['high_risk'] and max_high_risk else 0,
            'is_current': key == current_month.strftime('%Y-%m'),
        })

    this_month_total = month_buckets[current_month.strftime('%Y-%m')]['count']
    previous_month_total = month_buckets[previous_month.strftime('%Y-%m')]['count']
    month_delta = this_month_total - previous_month_total
    month_delta_pct = round((month_delta / previous_month_total) * 100, 1) if previous_month_total else None
    avg_close_days = round(sum(close_days) / len(close_days), 1) if close_days else None

    stats = {
        'total': total,
        'abiertas': abiertas,
        'cerradas': cerradas,
        'alta_gravedad': alta_gravedad,
        'closure_rate': _pct(cerradas, total),
        'avg_close_days': avg_close_days,
        'avg_close_days_display': _format_decimal(avg_close_days, 1) if avg_close_days is not None else None,
        'stale_open': stale_open,
        'this_month_total': this_month_total,
        'previous_month_total': previous_month_total,
        'month_delta': month_delta,
        'month_delta_pct': month_delta_pct,
        'impact_units': round(total_units, 2),
        'impact_units_display': _format_decimal(total_units, 2),
        'impact_usd': round(total_usd, 2),
        'impact_usd_display': _format_decimal(total_usd, 2),
        'inocuidad_flags': inocuidad_flags,
        'consumer_flags': consumer_flags,
        'quality_flags': quality_flags,
    }
    recent_ncs = (NonConformity.query
                  .order_by(NonConformity.created_at.desc())
                  .limit(8)
                  .all())
    oldest_open = (NonConformity.query
                   .filter(or_(
                       NonConformity.status.is_(None),
                       NonConformity.status.notin_(CLOSED_STATUSES),
                   ))
                   .order_by(NonConformity.date_detected.asc(), NonConformity.created_at.asc())
                   .limit(5)
                   .all())
    recently_closed = (NonConformity.query
                       .filter(
                           NonConformity.status.in_(CLOSED_STATUSES),
                           NonConformity.closure_date.isnot(None),
                       )
                       .order_by(NonConformity.closure_date.desc(), NonConformity.created_at.desc())
                       .limit(5)
                       .all())

    for nc in oldest_open:
        nc.open_age_days = (today - nc.date_detected).days if nc.date_detected else None

    top_sections = _build_breakdown(
        section_counter,
        ['#4338ca', '#6366f1', '#818cf8', '#38bdf8', '#14b8a6', '#f59e0b'],
        limit=6,
    )
    provider_breakdown = _build_breakdown(
        provider_counter,
        ['#0f766e', '#0ea5e9', '#4f46e5', '#f97316', '#ef4444'],
        limit=5,
    )
    motive_breakdown = _build_breakdown(
        motive_counter,
        ['#f59e0b', '#4338ca', '#0ea5e9', '#64748b'],
        limit=4,
    )
    status_breakdown = _build_breakdown(
        status_counter,
        ['#2563eb', '#16a34a', '#94a3b8'],
        limit=3,
    )
    gravity_breakdown = _build_breakdown(
        gravity_counter,
        ['#dc2626', '#ea580c', '#eab308', '#16a34a', '#94a3b8'],
        limit=5,
    )

    headline = {
        'current_label': _month_label(current_month),
        'delta_direction': 'up' if month_delta > 0 else 'down' if month_delta < 0 else 'flat',
    }

    return render_template(
        'main/dashboard.html',
        stats=stats,
        headline=headline,
        recent_ncs=recent_ncs,
        oldest_open=oldest_open,
        recently_closed=recently_closed,
        top_sections=top_sections,
        provider_breakdown=provider_breakdown,
        motive_breakdown=motive_breakdown,
        status_breakdown=status_breakdown,
        gravity_breakdown=gravity_breakdown,
        status_chart_gradient=_build_donut_gradient(status_breakdown),
        gravity_chart_gradient=_build_donut_gradient(gravity_breakdown),
        monthly_trend=monthly_trend,
        has_trend_data=any(item['count'] for item in monthly_trend),
        open_nc_count=stats['abiertas'],
    )


@main_bp.route('/analytics')
@login_required
def analytics():
    options = _analytics_filter_options()
    filters = _analytics_filters_from_request(request.args, options)

    start_date = date(filters['year'], filters['month'] or 1, 1)
    end_date = _shift_month(start_date, 1) if filters['month'] else date(filters['year'] + 1, 1, 1)

    query = (NonConformity.query
             .with_entities(
                 NonConformity.date_detected,
                 NonConformity.provider_tipo,
                 NonConformity.deviation_type,
                 NonConformity.empresa,
                 NonConformity.rimith_dept,
                 NonConformity.section,
                 NonConformity.provider_name,
                 NonConformity.gravity,
                 NonConformity.status,
             )
             .filter(
                 NonConformity.date_detected >= start_date,
                 NonConformity.date_detected < end_date,
             ))

    if filters['provider_tipo']:
        query = query.filter(NonConformity.provider_tipo == filters['provider_tipo'])
    if filters['deviation_type']:
        query = query.filter(NonConformity.deviation_type == filters['deviation_type'])
    if filters['bodega']:
        query = query.filter(NonConformity.empresa == filters['bodega'])

    rows = query.all()

    monthly_totals = Counter()
    monthly_deviation = defaultdict(Counter)
    provider_type_monthly = defaultdict(Counter)
    branch_monthly = defaultdict(Counter)
    provider_type_totals = Counter()
    branch_totals = Counter()
    rimith_sections = Counter()
    local_providers = Counter()
    supermarket_detection = Counter()
    provider_stats = defaultdict(lambda: {'total': 0, 'high': 0, 'open': 0, 'provider_type': ''})

    preventiva_total = 0
    correctiva_total = 0

    for row in rows:
        month = row.date_detected.month
        monthly_totals[month] += 1

        provider_type_label = _safe_label(row.provider_tipo)
        branch_label = _safe_label(row.empresa)
        provider_name_label = _safe_label(row.provider_name, '')

        raw_deviation = _safe_label(row.deviation_type, '').lower()
        if raw_deviation == 'preventiva':
            deviation_label = 'Preventiva'
            preventiva_total += 1
        elif raw_deviation == 'correctiva':
            deviation_label = 'Correctiva'
            correctiva_total += 1
        else:
            deviation_label = 'Otra'
        monthly_deviation[deviation_label][month] += 1

        if provider_type_label != 'Sin dato':
            provider_type_monthly[provider_type_label][month] += 1
            provider_type_totals[provider_type_label] += 1

        if branch_label != 'Sin dato':
            branch_monthly[branch_label][month] += 1
            branch_totals[branch_label] += 1
            supermarket_detection[branch_label] += 1

        if provider_type_label == 'Rimith' and _safe_label(row.section) != 'Sin dato':
            rimith_key = f"{_safe_label(row.section)}||{_safe_label(row.rimith_dept)}"
            rimith_sections[rimith_key] += 1

        if provider_type_label == 'Local' and provider_name_label:
            local_providers[provider_name_label] += 1

        if provider_name_label:
            provider_stats[provider_name_label]['total'] += 1
            provider_stats[provider_name_label]['provider_type'] = '' if provider_type_label == 'Sin dato' else provider_type_label
            if row.gravity in HIGH_GRAVITY:
                provider_stats[provider_name_label]['high'] += 1
            if not _is_closed(row.status):
                provider_stats[provider_name_label]['open'] += 1

    month_axis = _build_month_axis(monthly_totals)
    stacked_month_axis = _build_stacked_month_axis(monthly_deviation)

    top_provider_type_labels = [label for label, _ in provider_type_totals.most_common(4)]
    provider_type_series = _build_series(provider_type_monthly, top_provider_type_labels)

    top_branch_labels = [label for label, _ in branch_totals.most_common(5)]
    branch_series = _build_series(branch_monthly, top_branch_labels, short_label_fn=_branch_short_label)

    rimith_section_items = []
    rimith_ranking = _build_ranking(rimith_sections, limit=12)
    for item in rimith_ranking:
        section, dept = item['label'].split('||', 1)
        rimith_section_items.append({
            **item,
            'label': section,
            'dept': dept if dept != 'Sin dato' else 'Sin depto',
        })

    local_provider_items = _build_ranking(local_providers, limit=10)
    supermarket_items = _build_ranking(supermarket_detection, limit=10)

    worst_provider_items = []
    sorted_providers = sorted(
        provider_stats.items(),
        key=lambda item: (-item[1]['total'], -item[1]['high'], -item[1]['open'], item[0].lower()),
    )[:10]
    max_provider_total = max((stats['total'] for _, stats in sorted_providers), default=0)
    for index, (label, stats) in enumerate(sorted_providers, start=1):
        worst_provider_items.append({
            'rank': index,
            'label': label,
            'provider_type': stats['provider_type'],
            'count': stats['total'],
            'high': stats['high'],
            'open': stats['open'],
            'bar_pct': max(10, int((stats['total'] / max_provider_total) * 100)) if max_provider_total else 0,
            'high_pct': _pct(stats['high'], stats['total']),
        })

    analytics_summary = {
        'total': len(rows),
        'preventiva': preventiva_total,
        'correctiva': correctiva_total,
        'provider_types': len(provider_type_totals),
        'bodegas': len(branch_totals),
        'providers': len(provider_stats),
        'filter_summary': _analytics_filter_summary(filters),
        'selected_month_label': LONG_MONTH_LABELS[filters['month'] - 1] if filters['month'] else 'Todos los meses',
        'has_filters': any((filters['provider_tipo'], filters['deviation_type'], filters['bodega'], filters['month'])),
    }

    return render_template(
        'main/analytics.html',
        filters=filters,
        options=options,
        analytics_summary=analytics_summary,
        month_axis=month_axis,
        stacked_month_axis=stacked_month_axis,
        provider_type_series=provider_type_series,
        branch_series=branch_series,
        rimith_section_items=rimith_section_items,
        local_provider_items=local_provider_items,
        supermarket_items=supermarket_items,
        worst_provider_items=worst_provider_items,
        open_nc_count=NonConformity.query.filter_by(status='Abierta').count(),
    )


@main_bp.route('/existencias')
@login_required
def stock_check():
    q = request.args.get('q', '').strip()
    selected_item = request.args.get('item', '').strip()
    results = []
    product_options = []

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
        results = [_build_stock_result(product, bodegas) for product in products]
        product_options = [{
            'itemcod': result['itemcod'],
            'barcode': result['barcode'],
            'nombre': result['nombre'],
            'marca': result['marca'],
            'suplidor': result['suplidor'],
            'label': ' | '.join(filter(None, [
                result['itemcod'],
                result['nombre'],
                result['marca'],
                result['barcode'],
            ])),
        } for result in results]

        if not any(result['itemcod'] == selected_item for result in results) and results:
            selected_item = results[0]['itemcod']

    return render_template(
        'main/stock_check.html',
        q=q,
        selected_item=selected_item,
        results=results,
        product_options=product_options,
        open_nc_count=NonConformity.query.filter_by(status='Abierta').count(),
    )
