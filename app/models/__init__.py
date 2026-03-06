# Exponemos los modelos para Alembic y para importaciones globales
from app.models.user import User
from app.models.nc import NonConformity, Department, Provider
from app.models.catalogs import Empresa, Marca, Seccion, ClasificacionNC, CatalogItem
from app.models.maestras import ReporteMaestro, Suplidor, RSBodega, RSInvPorDia

__all__ = [
    'User',
    'NonConformity', 'Department', 'Provider',
    'Empresa', 'Marca', 'Seccion', 'ClasificacionNC', 'CatalogItem',
    'ReporteMaestro', 'Suplidor', 'RSBodega', 'RSInvPorDia',
]
