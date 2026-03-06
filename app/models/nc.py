from app import db
from datetime import datetime


class Department(db.Model):
    """Departamento interno — usado en User.department y como DE/FROM en la NC"""
    __tablename__ = 'departments'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    users        = db.relationship('User', backref='department', lazy='dynamic')
    ncs_reported = db.relationship('NonConformity', backref='reporting_department', lazy='dynamic')


class Provider(db.Model):
    """Local provider catalog grouped by provider type."""
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    provider_type = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Provider {self.provider_type or "-"} - {self.name}>'


class NonConformity(db.Model):
    __tablename__ = 'non_conformities'

    id        = db.Column(db.Integer, primary_key=True)
    nc_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # ── Fechas ───────────────────────────────────────────────────────────────
    date_detected = db.Column(db.Date, nullable=False)
    time_detected = db.Column(db.Time, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # ── Origen ───────────────────────────────────────────────────────────────
    detected_by_type = db.Column(db.String(50))   # Colaborador / Cliente / Recall / Redes Sociales
    empresa          = db.Column(db.String(150))  # EMPRESA: texto plano
    department_id    = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)  # DE/FROM

    # ── Proveedor ─────────────────────────────────────────────────────────
    provider_tipo = db.Column(db.String(50))   # T. PROVEEDOR: Directo/Local/Rimith/Interna/Riba Smith
    provider_id   = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=True)
    provider_name = db.Column(db.String(250))  # Nombre del proveedor
    rimith_dept   = db.Column(db.String(50))   # Depto Rimith: Artesanal/Cocina/IARSA/etc.
    section       = db.Column(db.String(100))  # SECCIÓN

    # ── Clasificación ─────────────────────────────────────────────────────
    deviation_type = db.Column(db.String(50))   # Correctiva / Preventiva
    gravity        = db.Column(db.String(50))   # Muy Alta / Alta / Media / Baja
    classification = db.Column(db.String(250))  # Clasificación NC (ClasificacionNC.name)
    cause          = db.Column(db.String(100))  # Causa (CatalogItem CAUSA)
    motive         = db.Column(db.String(100))  # Calidad / Inocuidad
    prerequisite   = db.Column(db.String(200))  # Prerrequisito (CatalogItem PRERREQUISITO)

    # ── Detalle del producto ──────────────────────────────────────────────
    title            = db.Column(db.String(200), nullable=False)
    description      = db.Column(db.Text, nullable=False)
    product_code     = db.Column(db.String(64))
    product_affected = db.Column(db.String(200)) # itemcod de ReporteMaestro (texto)
    marca            = db.Column(db.String(150)) # Marca recuperada desde ReporteMaestro
    barcode          = db.Column(db.String(100)) # Código de barra / ITMS
    lot              = db.Column(db.String(100))   # Lote
    expiration_date  = db.Column(db.Date, nullable=True)
    total_units      = db.Column(db.Float, default=0.0)  # Unidades no conformes
    total_usd        = db.Column(db.Float, default=0.0)  # Valor $ no conforme
    branch_total_units = db.Column(db.Float, default=0.0)  # Inventario en la sucursal
    branch_total_usd   = db.Column(db.Float, default=0.0)  # Valor inventario en la sucursal

    # ── Impacto ───────────────────────────────────────────────────────────
    affects_consumer = db.Column(db.Boolean, default=False)  # ¿Afectó satisfacción consumidor?
    affects_inocuity = db.Column(db.Boolean, default=False)  # ¿Afecta inocuidad?
    affects_quality  = db.Column(db.Boolean, default=False)  # ¿Afecta calidad?

    # Estado del producto NC (Producto no conforme / Mercancía congelada / etc.)
    nc_product_status = db.Column(db.String(100))

    # ── Evaluación y acciones ─────────────────────────────────────────────
    evaluations            = db.Column(db.Text)  # Tipo(s) de evaluación (CatalogItem EVALUACION)
    evaluation_description = db.Column(db.Text)  # Análisis y descripción de la evaluación
    action_1               = db.Column(db.Text)
    action_2               = db.Column(db.Text)
    action_3               = db.Column(db.Text)
    corrective_action      = db.Column(db.Text)

    # ── Estado del reporte ────────────────────────────────────────────────
    status       = db.Column(db.String(30), default='Abierta')  # Abierta / Cerrada
    closure_date = db.Column(db.Date, nullable=True)
    closed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    closed_by = db.relationship('User', foreign_keys=[closed_by_id])

    def __repr__(self):
        return f'<NC {self.nc_number} - {self.status}>'
