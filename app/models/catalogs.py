"""
Catalog models used by the NC form.
"""
from app import db


class Empresa(db.Model):
    """Local company / branch catalog."""
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    codigo = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Empresa {self.codigo or "-"} - {self.name}>'


class Marca(db.Model):
    """Local brand catalog."""
    __tablename__ = 'marcas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Marca {self.name}>'


class Seccion(db.Model):
    """Catalog of sections shown in the NC form."""
    __tablename__ = 'secciones'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    provider_tipo = db.Column(db.String(50))
    rimith_dept = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Seccion {self.name}>'


class ClasificacionNC(db.Model):
    """Extended NC classification catalog."""
    __tablename__ = 'clasificaciones_nc'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    grupo = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ClasificacionNC {self.name}>'


class CatalogItem(db.Model):
    """Generic catalog for smaller dropdowns."""
    __tablename__ = 'catalog_items'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    value = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<CatalogItem {self.category}: {self.value}>'
