from app import db

class ReporteMaestro(db.Model):
    """REPORTE MAESTRO - Listado de todos los productos y sus datos"""
    __tablename__ = 'reporte_maestro'
    
    itemcod = db.Column(db.String(64), primary_key=True)
    itemcodbarra = db.Column(db.String(64))
    itemnombre = db.Column(db.String(255))
    marcanomb = db.Column(db.String(255))
    areanombre = db.Column(db.String(255))
    departamentos = db.Column(db.String(255))
    categorianom = db.Column(db.String(255))
    grupo = db.Column(db.String(255))
    rechazado = db.Column(db.Boolean)
    fechacreacion = db.Column(db.DateTime)
    fechaultcompra = db.Column(db.DateTime)
    costo = db.Column(db.Numeric(18, 4))
    precio = db.Column(db.Numeric(18, 4))
    idmarca = db.Column(db.Integer)
    iddepartamento = db.Column(db.Integer)
    idcategoria = db.Column(db.Integer)
    idgrupo = db.Column(db.Integer)
    idarea = db.Column(db.Integer)
    nomsuplidor = db.Column(db.String(255))
    extranjero = db.Column(db.Boolean)
    idsuplidor = db.Column(db.String(64))
    empaque = db.Column(db.String(128))
    razonrechazado = db.Column(db.String(255))
    noseusa = db.Column(db.Boolean)
    unidaduso = db.Column(db.String(64))
    unidadalmacen = db.Column(db.String(64))
    unidadcompra = db.Column(db.String(64))
    pack = db.Column(db.Numeric(18, 4))
    idgrupo09 = db.Column(db.Integer)
    fechacambio = db.Column(db.DateTime)

    def __repr__(self):
        return f'<ReporteMaestro {self.itemcod} - {self.itemnombre}>'


class Suplidor(db.Model):
    """SUPLIDORES - Catálogo de Proveedores"""
    __tablename__ = 'rsi_cliente_suplidor'
    
    cliente_suplidor = db.Column(db.String(64), primary_key=True)
    nombre = db.Column(db.String(255))
    extranjero = db.Column(db.Boolean)
    ruc = db.Column(db.String(128))
    idtercero = db.Column(db.String(64))
    activo = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Suplidor {self.cliente_suplidor} - {self.nombre}>'

class RSBodega(db.Model):
    """BODEGAS - Catálogo central de sucursales y ubicaciones (Empresas)"""
    __tablename__ = 'rsi_bodegas'
    
    bodega = db.Column(db.String(64), primary_key=True)
    nombre = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<RSBodega {self.bodega} - {self.nombre}>'


class RSInvPorDia(db.Model):
    """Inventario diario por bodega y producto."""
    __tablename__ = 'rsi_inv_pordia'

    bodega = db.Column(db.String(64), primary_key=True)
    item = db.Column(db.String(64), primary_key=True)
    fecha = db.Column(db.DateTime, primary_key=True)
    cantidad = db.Column(db.Numeric(18, 4))
    costo = db.Column(db.Numeric(18, 4))
    precio = db.Column(db.Numeric(18, 4))
    ventapromedio = db.Column(db.Numeric(18, 4))
    cantidadcontabilidad = db.Column(db.Numeric(18, 4))
    fechaultentrada = db.Column(db.DateTime)
    fechaultcompra = db.Column(db.DateTime)
    cantidadultcompra = db.Column(db.Numeric(18, 4))

    def __repr__(self):
        return f'<RSInvPorDia {self.bodega} - {self.item} - {self.fecha}>'
