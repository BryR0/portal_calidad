"""
Catálogos estáticos extraídos de portal.xlsm
  - hoja 'listas':  valores de los dropdowns configurados
  - hoja 'Datos':   valores REALES usados en las 1,500+ NCs históricas
Usados en formularios y validaciones.
"""

# ── Detección / Desviación / Causa / Motivo ────────────────────────────────
DETECTADA = ['Colaborador', 'Cliente', 'Recall', 'Redes Sociales']

DESVIACION = ['Correctiva', 'Preventiva']

GRAVEDAD = ['Muy Alta', 'Alta', 'Media', 'Baja']

CAUSA = [
    'Mano de Obra',
    'Maquinaria',
    'Materia Prima',
    'Método',
    'Accidente de tránsito',
]

MOTIVO = ['Calidad', 'Inocuidad']

# ── Prerrequisitos ─────────────────────────────────────────────────────────
PRERREQUISITO = [
    'Buenas Prácticas de Manufactura',
    'Control de Alérgenos',
    'Control de Almacenamiento y Distribución',
    'Control de Material Extraño',
    'Control de Procesos Operativos',
    'Control de Proveedores y Materia Prima',
    'Control de Químicos',
    'Control de Temperatura y Humedad Relativa',
    'Control Integral de Plagas',
    'Formación del Personal',
    'Gestión Ambiental de Residuos y Desechos',
    'Gestión de Desviaciones y Acciones Correctivas',
    'HACCP',
    'Higiene del Personal',
    'Limpieza y Desinfección (SSOP)',
    'Mantenimiento Preventivo',
    'Seguridad del Agua Potable',
    'Trazabilidad y Recall',
]

# ── Evaluaciones ───────────────────────────────────────────────────────────
EVALUACION = [
    'Organoléptico/Organoleptic',
    'Físico/Physical',
    'Químico/Chemical',
    'Higiene/Hygiene',
    'Laboratorio/Laboratory',
]

# ── Clasificación de NC ────────────────────────────────────────────────────
# Fuente: hoja 'listas' + valores reales de hoja 'Datos' normalizados
CLASIFICACION_NC = [
    # Artículo / Contenido
    'Artículo defectuoso',
    'Bajo contenido neto',
    'Contenido neto no conforme',
    # Canastas
    'Canastas no conformes (suciedad)',
    # Contaminación biológica
    'Contaminación biológica',
    'Contaminación biológica (gorgojo)',
    'Contaminación biológica (insecto)',
    'Contaminación biológica (moho)',
    'Contaminación biológica (restos de animal)',
    'Contaminación cruzada',
    'Contaminación Química',
    # Falla de limpieza / higiene
    'Deficiencia en la limpieza',
    'Falla de limpieza',
    'Falla de higiene (material auxiliar de transporte)',
    'Falla de higiene (transporte)',
    'Falla en la cadena de frío (presencia de escarcha)',
    # Falla de despacho
    'Falla de despacho (condensación)',
    'Falla de despacho (Especificaciones no aprobadas)',
    'Falla de despacho (mercancía errónea)',
    'Falla de despacho (mercancía en mal estado)',
    'Falla de despacho (producto condensado)',
    'Falla de despacho (vencido)',
    # Falla de embalaje / empaque
    'Falla de embalaje',
    'Falla de empaque (Abollado)',
    'Falla de empaque (débil)',
    'Falla de empaque (golpeado)',
    'Falla de empaque (húmedo)',
    'Falla de empaque (manchado)',
    'Falla de empaque (migración de tinta)',
    'Falla de empaque (óxido)',
    'Falla de empaque (pérdida de vacío)',
    'Falla de empaque (roto)',
    'Falla de empaque (se adhiere al producto)',
    'Falla de empaque (se abre)',
    'Falla de empaque (sellado)',
    'Falla de empaque (Sellado y fuga de contenido)',
    'Falla de empaque (soplado)',
    'Falla de empaque (traspaso de grasa)',
    'Falla de empaque-Cinta (alambre)',
    'Pérdida de integridad de empaque',
    # Falla de etiquetado
    'Falla de etiquetado (adulterado)',
    'Falla de etiquetado (borrosa)',
    'Falla de etiquetado (código incorrecto)',
    'Falla de etiquetado (descripción incorrecta)',
    'Falla de etiquetado (doble código y doble precio)',
    'Falla de etiquetado (doble fecha)',
    'Falla de etiquetado (fecha corta)',
    'Falla de etiquetado (fecha incorrecta)',
    'Falla de etiquetado (fecha no legible)',
    'Falla de etiquetado (fecha tapada/cortada)',
    'Falla de etiquetado (ingredientes no declarados)',
    'Falla de etiquetado (No cumple con lo declarado)',
    'Falla de etiquetado (no legible)',
    'Falla de etiquetado (precio incorrecto)',
    'Falla de etiquetado (Producto no declara Registro Sanitario y país de origen)',
    'Falla de etiquetado (reetiquetado)',
    'Falla de etiquetado (se desprende)',
    'Falla de etiquetado (sin declaración de peso)',
    'Falla de etiquetado (sin etiqueta)',
    'Falla de etiquetado (sin fecha)',
    'Falla de etiquetado (sin fecha de vencimiento)',
    'Deterioro de etiqueta y empaque',
    # Falla de llenado / rotación
    'Falla de llenado',
    'Falla de Rotación (fecha próxima a vencer)',
    # Inocuidad / Seguridad
    'Inocuidad',
    'Intoxicación Alimentaria',
    'Sin Registro Sanitario',
    # Material extraño
    'Material extraño',
    'Material extraño (artículos del personal)',
    'Material extraño (astillas de madera)',
    'Material extraño (alteraciones post-mortem/respuesta inflamatoria)',
    'Material extraño (cabello)',
    'Material extraño (cartón)',
    'Material extraño (cáscara)',
    'Material extraño (equipos y herramientas de mantenimiento)',
    'Material extraño (escama)',
    'Material extraño (hilo)',
    'Material extraño (hueso)',
    'Material extraño (material vegetal)',
    'Material extraño (metal)',
    'Material extraño (orgánico)',
    'Material extraño (papel)',
    'Material extraño (Partículas)',
    'Material extraño (piedra)',
    'Material extraño (plástico)',
    'Material extraño (restos de carbón)',
    'Material extraño (sedimentos)',
    'Material extraño (tachuela)',
    'Material extraño (tornillo)',
    'Material extraño (vidrio)',
    # Moho / manchas / roedores
    'Manchas',
    'Marcas de roedor',
    'Moho',
    'Parámetros fisicoquímicos fuera de rango',
    # Perfil no conforme
    'Perfil no conforme (abiertas)',
    'Perfil no conforme (apariencia)',
    'Perfil no conforme (apariencia de empaque)',
    'Perfil no conforme (Carbonatación no percibida)',
    'Perfil no conforme (color)',
    'Perfil no conforme (color y olor)',
    'Perfil no conforme (Color y textura)',
    'Perfil no conforme (crudo)',
    'Perfil no conforme (cuarteado, separación)',
    'Perfil no conforme (cuarteado y sabor agrio)',
    'Perfil no conforme (dañado)',
    'Perfil no conforme (descomposición)',
    'Perfil no conforme (dimensión)',
    'Perfil no conforme (espesor)',
    'Perfil no conforme (exceso de grasa)',
    'Perfil no conforme (Fermentado)',
    'Perfil no conforme (grasa)',
    'Perfil no conforme (húmedo)',
    'Perfil no conforme (liberación de contenido)',
    'Perfil no conforme (liberación de líquido)',
    'Perfil no conforme (liberación de líquido y mal olor)',
    'Perfil no conforme (liberación de líquido y pérdida de vacío)',
    'Perfil no conforme (limpieza de materia prima)',
    'Perfil no conforme (Maduración)',
    'Perfil no conforme (Mancha)',
    'Perfil no conforme (microbiología)',
    'Perfil no conforme (muy quebradizas)',
    'Perfil no conforme (olor)',
    'Perfil no conforme (oxidación)',
    'Perfil no conforme (quebrado)',
    'Perfil no conforme (rancidez)',
    'Perfil no conforme (Resistencia)',
    'Perfil no conforme (roto)',
    'Perfil no conforme (sabor)',
    'Perfil no conforme (Sabor y color)',
    'Perfil no conforme (Sabor y textura)',
    'Perfil no conforme (sabor y olor)',
    'Perfil no conforme (sabor, textura y olor)',
    'Perfil no conforme (se abren)',
    'Perfil No Conforme (Separación)',
    'Perfil no conforme (sedimentos)',
    'Perfil no conforme (sin relleno)',
    'Perfil no conforme (solidificado)',
    'Perfil no conforme (textura)',
    'Perfil no conforme (Textura y olor)',
    'Perfil no conforme (viscosidad)',
    'Perfil no conforme (volumen)',
    # Temperatura / olor
    'Temperatura no conforme',
    'Temperatura fuera de rango y mezcla de posturas sin división',
    'Olor extraño (no conforme)',
]

# ── Tipo de Proveedor ──────────────────────────────────────────────────────
# 'Riba Smith' = compras internas entre sucursales (aparece en datos reales)
PROVEEDOR_TIPO = ['Directo', 'Local', 'Rimith', 'Interna', 'Riba Smith']

# Abreviatura para el N° NC
PROVEEDOR_ABBREV = {
    'Directo':    'PD',
    'Local':      'PL',
    'Rimith':     'PR',
    'Interna':    'PI',
    'Riba Smith': 'RS',
}

# ── Secciones por Tipo de Proveedor ───────────────────────────────────────
SECCIONES_POR_PROVEEDOR = {
    'Directo': [
        'Compras directas', 'Compras local', 'Pedido Directo', 'Local', 'RS',
    ],
    'Local': [
        'Compras local',
    ],
    'Rimith': [
        # Artesanal
        'Artesanal', 'Pastelería Fina', 'Lácteos', 'Helados', 'Chocolatería',
        'Quesos', 'Proveeduría', 'Hojaldres', 'Snacks',
        # Cocina Industrial
        'Cocina Abierta', 'Congelados', 'Ensaladas', 'Postres', 'Tamales',
        'Empaque Artesanal', 'Simple step', 'Ceviche', 'Sanidad',
        # Frutas y Verduras
        'Zumos y Pulpas', 'Fruta picada', 'IV Gama', 'Granel', 'Maduración',
        'Empaque en mallas', 'Empaque en vitafilm', 'Empaque de hierbas',
        'Miel', 'Vinagres y Aderezos',
        # IARSA
        'Línea automática', 'Línea semi automática', 'Panes y dulces',
        'Panes de mesa', 'Panes congelados', 'Panes planos', 'Panadería',
        'Dulcería', 'Galletas',
        # Tortillería
        'Tortillas frescas', 'Tortillas congeladas', 'Empanadas de maíz',
        'Carimañolas', 'Gourmet', 'Prefrito',
        # VIPSA
        'Carnicería', 'Embutidos',
        # Común
        'Despacho', 'Transporte',
    ],
    'Interna': [
        'CEDI', 'Depósito Central', 'Supermercado AP', 'Supermercado BV',
        'Supermercado CE', 'Supermercado MP', 'Supermercado BG',
        'Transporte', 'Grupo Riba Smith', 'Compras',
    ],
    'Riba Smith': [
        'Despacho', 'Frío', 'Compras local', 'Neveras', 'Transporte', 'Recibo',
    ],
}

# Para cascade de 3 niveles en Rimith:
# T. Proveedor = Rimith → DEPTO (RIMITH_DEPTS) → SECCIÓN (SECCIONES_POR_RIMITH)
RIMITH_DEPTS = [
    'Artesanal', 'Cocina Industrial', 'Frutas y Verduras',
    'IARSA', 'Tortillería', 'VIPSA', 'Transporte',
]

SECCIONES_POR_RIMITH = {
    'Artesanal':         ['Artesanal', 'Pastelería Fina', 'Lácteos', 'Helados', 'Chocolatería', 'Quesos', 'Proveeduría', 'Hojaldres', 'Snacks', 'Despacho'],
    'Cocina Industrial': ['Cocina Abierta', 'Congelados', 'Ensaladas', 'Postres', 'Tamales', 'Empaque Artesanal', 'Simple step', 'Ceviche', 'Sanidad', 'Despacho'],
    'Frutas y Verduras': ['Zumos y Pulpas', 'Fruta picada', 'IV Gama', 'Granel', 'Maduración', 'Empaque en mallas', 'Empaque en vitafilm', 'Empaque de hierbas', 'Miel', 'Vinagres y Aderezos', 'Despacho'],
    'IARSA':             ['Línea automática', 'Línea semi automática', 'Panes y dulces', 'Panes de mesa', 'Panes congelados', 'Panes planos', 'Panadería', 'Dulcería', 'Galletas', 'Artesanal', 'Sanidad', 'Despacho'],
    'Tortillería':       ['Tortillas frescas', 'Tortillas congeladas', 'Empanadas de maíz', 'Carimañolas', 'Gourmet', 'Prefrito', 'Sanidad', 'Despacho'],
    'VIPSA':             ['Carnicería', 'Embutidos', 'Despacho'],
    'Transporte':        ['Transporte'],
}

# ── Empresas / Sucursales ──────────────────────────────────────────────────
# Códigos cortos usados en datos históricos y nombres completos
EMPRESA_CODIGOS = {
    'AL': 'Supermercado Riba Smith - Altaplaza',
    'BV': 'Supermercado Riba Smith - Bella Vista',
    'BG': 'Supermercado Riba Smith - Brisas del Golf',
    'CE': 'Supermercado Riba Smith - Costa del Este',
    'MK': 'Supermercado Riba Smith - Marketplaza',
    'MP': 'Supermercado Riba Smith - Multiplaza',
    'AB': 'Supermercado Riba Smith - Selecto Albrook',
    'CH': 'Supermercado Riba Smith - Selecto Chitré',
    'CO': 'Supermercado Riba Smith - Selecto Coronado',
    'PP': 'Supermercado Riba Smith - Selecto Panamá Pacífico',
    'VV': 'Supermercado Riba Smith - Selecto Versalles',
    'AP': 'Supermercado Riba Smith - Transistmica',
    'VZ': 'Mercadito Riba Smith Villa Zaita',
    'LS': 'Mercadito Riba Smith La Siesta',
    'DC': 'Centro de Distribución',
    'CEDI': 'CEDI (Centro de Distribución)',
    'RS': 'Riba Smith, S.A.',
}

EMPRESAS = [
    'Supermercado Riba Smith - Altaplaza',
    'Supermercado Riba Smith - Bella Vista',
    'Supermercado Riba Smith - Brisas del Golf',
    'Supermercado Riba Smith - Costa del Este',
    'Supermercado Riba Smith - Marketplaza',
    'Supermercado Riba Smith - Multiplaza',
    'Supermercado Riba Smith - Selecto Albrook',
    'Supermercado Riba Smith - Selecto Chitré',
    'Supermercado Riba Smith - Selecto Coronado',
    'Supermercado Riba Smith - Selecto Panamá Pacífico',
    'Supermercado Riba Smith - Selecto Versalles',
    'Supermercado Riba Smith - Transistmica',
    'Mercadito Riba Smith Villa Zaita',
    'Mercadito Riba Smith La Siesta',
    'Centro de Distribución',
    'CEDI (Centro de Distribución)',
    'Depósito Central',
    'Depósito de Casero',
    'Depósito de Empaque',
    'Food Service',
    'UCQ',
    'Riba Smith, S.A.',
]

# Departamentos internos (campo DE / FROM)
DEPARTAMENTOS_INTERNOS = [
    'Gestión de Calidad',
    'Compras',
    'Logística',
    'Transporte',
    'Operaciones',
    'Administración',
]

# ── Proveedores organizados por Tipo ──────────────────────────────────────
PROVEEDORES_POR_TIPO = {
    'Directo': [
        'Advantage Sales & Marketing', 'Allary Corporation', 'Amico Mio', 'Arcor A.I.C.',
        'Associated Grocers', 'Atlantic Grocery Supply', 'Auricchio', 'Bazic Product',
        'Belgian Delights Corp.', 'Beretta Italia', 'Bodegas Juan Gil', 'Campofrío España',
        'CEDI', 'Conchita Food Inc.', 'Damp Rip', 'Del Monte Pan American, inc',
        'Delvi Inc', 'Dima Trading (Royal Paella)', 'Dot Foods Congelado',
        'El Gran Cardenal', 'El Pozo', 'El Valle de Almodovar', 'El Valle Snack',
        'Empire Candle CO LLC', 'Galaxy Foods', 'García Baquero', 'Gianni Negrini',
        'Global Brands', 'Good Hair Day Pasta', 'Gordon Foods', 'Gourmet int Food',
        'Granarolo', 'Halperns Carnes', 'HapCor Inc.', 'Henry Lee',
        'Highland Coffee Inc', "I Am Foods Int'l.", 'Ibero Citterio Deli',
        'Ibero Foods Creminelli', 'Ibero Fresh Pet', 'Il Boschetto', 'Interfoods Usa',
        'Intern Design', 'International Dairy Farms', 'Jada Foods',
        'James Skinner Baking', 'Jet Set Foods', 'Kashi Company', 'Kehe Food',
        'Kings Ford', 'La Catedral de Navarra', 'La Española', 'La Real',
        'Lamar Hormel', 'Loison Época', 'LT. Blender Cocktails', 'Loving Pets',
        'Marcos Salamanca', 'Mariani Nut Company', 'Medina Baking & Powder Products, Inc',
        'Melii Baby Inc.', 'Merchants Distributors', 'Misi Home', 'Mondelez International',
        'Moritex Exports LTD', 'Naviera', 'Newell Rubbermaid', 'Non Foods Marketing',
        'Norpro Inc.', 'Panhellenic Enterprises', 'Pastificio Felicetti',
        'Perdomo Gran Sabana', 'Portal Pacific', 'Quirch Foods', 'Riso Pasini',
        'Russel Stover Candi', 'Sandwich Bros Congelado', 'Setton International',
        'Smithfield American Foods', 'Southeast', 'Supervalu Associated',
        'The Gorilla Glue Company', 'Titos Foods', 'Tropical Foods',
        'Turron 1880 Epoca', 'United Natural Food Inc.', 'Vini & Vino, S.A',
        'Viu Manent', 'Walton & Post, INC', 'Wise Foods Inc.',
    ],
    'Local': [
        'Adarisi, S.A.', 'Agasajos S.A.', 'Agencia Escofery, S.A',
        'Agencia Internacional de Marcas, S.A.', 'Agencias Benedicto Wong',
        'Agencias Feduro, S.A.', 'Agrícola La Lomita',
        'Agro Industrias de Veraguas S.A.', 'Agrosilos, S.A',
        'Aguas Cristalinas, S.A.', 'Alimentos Cárnicos de Panamá',
        'Alimentos Polar Panamá Inc.', 'Allied Chemical Industry De Panamá, S.A',
        'Anamary', 'Arce Avícola, S A.', 'Aros y Anillos El Pimpo',
        'Avipac, S.A.', 'BK Import, S.A.', 'Bolsas y Cartuchos de Papel S.A.',
        'Calesa', 'Calox Panameña', 'Canada Bakery', 'Carnes de Coclé',
        'Celebrity Products, Inc', 'Central de Granos de Coclé, S.A',
        'Centralam Distributors, Inc.', 'Cerro Punta',
        'Cesar Arrocha Graelle y CIA, S.A', 'Cevishop', 'Chez Mary',
        'Chorizos MUTU, S.A.', 'Colgate Palmolive Inc.', 'Comaca Foods',
        'Comercial Pozuelo Panamá, S A', 'Comercializadora Ancar S.A.',
        'Coosemans Panamá', 'Corporación IMPA-DOEL S.A.', 'De La Casa',
        'Del Alba Premium Nuts', 'Del Monte de Panamá, S.A.', 'Deli Fish Panamá S.A.',
        'Delicias Cantonesa', 'DG Trading S.A.', 'Dicarina Panamá, inc',
        'Dicasa (distribuidora centroamericana)', 'Dionellin Martínez',
        'Distribuidora Comercial MO, S.A.', 'Distribuidora Comercial S.A.',
        'Distribuidora Delicias Alina', 'Distribuidora Jonel, S.A.',
        'Distribuidora La Quincha', 'Distribuidora Ojel, S.A.',
        'Distribuidora Verde Azul, S.A.', 'Distribuidora Vikingo', 'Drago Corp.',
        'El Ceviche del Abuelo, S.A.', 'Embutidora Don Vincenzo S.A.',
        'Embutidos Colls', 'Empanaditas Raquelita', 'Empresa Doña Jose, S.A.',
        'Empresa Panameña de Alimentos', 'Empresas MELO S.A.',
        'Estrella Azul', 'Everyday Seafood, S.A.', 'Farallón Aquaculture, S.A',
        'Felipe Motta e Hijo, S.A.', 'Florencia Intercomercial S.A.',
        'Free Generation, S.A.', 'FruverTropik S.A.', 'FSEBS S.A.',
        'Gran Pacifico S.A.', 'Granjas del Este S.A.', 'Granos de Pedasí, S.A.',
        'Grupo Barsash, S.A.', 'Grupo Jagasa, S.A.', 'Grupo Melo, S.A.',
        'Grupo TWT INC', 'H. Tzanetatos, INC', 'Hacienda Santa Isabella',
        'Harinera Oro del Norte S.A.', 'Hermanos Gago', 'Hermanos Palacios',
        'Hermanos Zakay, S.A.', 'Highland Coffee Inc', 'Imar Import, S.A.',
        'Imperia Foods', 'Importaciones Internacionales MR, S.A.',
        'Importadora y exportadora Nimar, S.A', 'Importadora y exportadora Olay, S.A.',
        'Importadora Yasy', 'Industria Deca', 'Industrial Arrocera de Chiriquí S.A.',
        'Industrias El Antojo, S.A', 'Industrias HG y Cía',
        'Industrias Lácteas, S.A.', 'Industrias Panamá Boston, S.A',
        'Inquivepa, S.A.', 'Inversiones Makapana, S.A',
        'JV Associates S.A.', 'Jeffreys Bakery Inc.', 'La International Services, S.A',
        'La Lomita', 'La Marquesa Gourmet Bakery', 'Lago Sirino, S.A.',
        'Lamar Coke', 'Levapan Panamá S.A.', 'Lina Corporación',
        'M&R Distribuidor', 'Mafalda', 'Mariscos Tropicales S.A.',
        'Master Direct Panamá, S.A.', 'Medimex, S.A.', 'Miaris, S.A.',
        'Moderna Comercial S.A.', "Mukky's Falafel, S.A", 'Mutisa S.A.',
        'Negocios centroamericanos S.A.', 'Nestlé Panamá',
        'NHS (Nuevo Hung Chen)', 'Noritex Zona Libre', 'Nuba Bottling Company Inc',
        'Nuevo Hung Sheng, S.A.', 'Ocean Food', 'Ocean Gourmet',
        'Panama Springs S.A.', 'Panama Trade', 'Panchos Kitchen',
        'Papelería Comercial S.A.', 'Pastas Donadio, S.A.',
        'Pastas Frescas, S.A.', 'Pastas Oriental S.A.', 'Pedersen Fine Food, S.A',
        'Pekados Gourmet, S.A', 'Pesca Fresca', 'Plásticos Generales',
        'Pollo Caribeño', 'Pretelt Gourmet Meats', 'Procesadora Comaca Food, S.A.',
        'Procesadora de Granos Chiricanos, S.A.', 'Prohealth Shop S.A.',
        'Producto a tu Gusto', 'Productos Alimenticios Pascual S.A.',
        'Productos Azucena', 'Productos de Prestigio, S.A', 'Productos Diversos',
        'Productos La Doña', 'Productos Lácteos San Antonio (PROLACSA)',
        'Productos Lili S.A.', 'Productos Lux, S.A. (PROLUXSA)',
        'Productos Nevada S. DE R.L.', 'Productos Riando', 'Productos Selectos S.A.',
        'Productos Toledano, S.A.', 'Prolacsa', 'Puratos Panamá',
        'Quesos El CHE S.A.', 'Raspafresh, S.A', 'Riquezas del Mar',
        'Roma Distribution Service Corp', 'Salvamar, S.A', 'Samuray Mar S.A.',
        'Si, es Natural S.A.', 'Sierra Cantabria', 'Sociedad Alimentos de Primera',
        'South Indian S.A.', 'Tagarápulos, S.A.', 'Tavidia', 'Tecbite, INC',
        'Teque Chevere Internacional S.A.', 'Thermoenvases', 'Titos Foods',
        'Tornadi, S.A', 'Tortillas La Mexicana', 'Tropimar, S.A.',
        'Tzanetatos inc', 'Ultra Orion, S.A.', 'V.C. Products, Inc',
        'Varcom, S.A', 'Varela Hermanos S.A.', 'Ventas Buena Vista',
        'Ventas y Mercadeo, S.A.', 'Vima Food Panamá, S.A.',
        'Viveres Unidos, S.A.',
    ],
    'Rimith': [
        'Artesanal', 'Cocina Industrial', 'Frutas y Verduras',
        'IARSA', 'Tortillería', 'VIPSA', 'Transporte',
    ],
    'Interna': [
        'CEDI', 'Depósito Central', 'Supermercado AP', 'Supermercado BV',
        'Supermercado CE', 'Supermercado MP', 'Supermercado BG',
        'Transporte', 'Grupo Riba Smith',
    ],
    'Riba Smith': [
        'Supermercado Riba Smith - Altaplaza',
        'Supermercado Riba Smith - Bella Vista',
        'Supermercado Riba Smith - Brisas del Golf',
        'Supermercado Riba Smith - Costa del Este',
        'Supermercado Riba Smith - Marketplaza',
        'Supermercado Riba Smith - Multiplaza',
        'Supermercado Riba Smith - Selecto Albrook',
        'Supermercado Riba Smith - Selecto Chitré',
        'Supermercado Riba Smith - Selecto Coronado',
        'Supermercado Riba Smith - Selecto Panamá Pacífico',
        'Supermercado Riba Smith - Selecto Versalles',
        'Supermercado Riba Smith - Transistmica',
        'Mercadito Riba Smith Villa Zaita',
        'Mercadito Riba Smith La Siesta',
    ],
}

# ── Marcas ─────────────────────────────────────────────────────────────────
MARCAS = [
    'ACISA', 'Agrodely', 'Alessi', 'Anamary', 'Apima', 'Arcor', 'Ariana',
    'Arrossísimo', 'Avipac', 'Ancestral', 'Bajareque', 'Bakery on Main', 'Banza',
    'Barilla', 'Bazic Product', 'Belgian Chocolate', 'Belgioioso', 'Benedetto Cavalier',
    'Bertolli', 'Bio Baby', "Blaser's", 'Blue Diamond', 'Blue Ribbon', 'Blue River',
    'Bonlac', "Brach's", 'Breyers', 'Bubba', 'Butterball', 'Califia', 'California Valley',
    'Camellia', 'Campofrío', 'Canada Bakery', 'Canada Dry', 'Cantabria', 'CEDI',
    'Celebrity Products', 'Ceresina', 'Cerro Punta', 'Cevishop', 'Chameleon Coldbrew',
    'Cheerios', 'Chez Mary', 'Chips Ahoy', 'Chobani', 'Chorizos MUTU', 'Coca Cola',
    'ColdBrew', 'Colls', 'Colombina', 'Comaca Food', 'Coosemans', 'Conchita',
    'Crescent Valley', 'Crystal Farms', 'Dahlicious', 'Damp Rip', 'Dannon', 'Dasani',
    'Del Alba Premium Nuts', 'De Cecco', 'Del Día', 'Del Valle', 'Deli Fish',
    'Delicias Cantonesa', "Del'Oro", 'Dicarina', 'Dionelin', 'Divella', 'Diamante',
    'Dixie', 'Don Mariano', 'Don Pedro', 'Don Vincenzo', 'Don Vittorio', 'Doña José',
    'Dos Pinos', 'Dos Tigres', 'Durán', 'Eagle', 'El Antojo', 'El Coclesano',
    'El Gran Cardenal', 'El Pimpo', 'El Toro', 'El Valle', 'Enlightened', 'Enterex',
    'Essential Everyday', 'Estrella Azul', 'Farallón', 'Feduro', 'Felicetti',
    'Felipe Motta e Hijo', 'First Choice', 'Formaggio', 'Fratelli Beretta 1812',
    'Fresca', 'Galler', 'Gallito', 'Gerber', 'Gianni Negrini', 'Glade',
    'Go Veggie', 'Gold Mills', 'Good Health', 'Gourmar', 'Gourmet', 'Graham Ready Crust',
    'García Baquero', 'Gran Sabana', 'Granarolo', 'Green Line', 'H. Tzanetatos',
    'Hacienda Santa Isabella', 'Hallmark', 'Halo Top', 'Heinz', 'Hermanos Gago',
    "Hershey's", 'Highland Farm', 'Hill Valley', 'Hormel', "Hunt's", 'Il Boschetto',
    'Industria Deca', 'Inquivepa, S.A.', 'Intern Design', 'Inversiones Makapana',
    'Jeffreys', 'Juan Gil', 'Jugos Natalie', 'Keebler', "Kellogg's", 'Kinesia',
    'Kings Ford', 'Kist', 'Kitchen Maid', 'Klim', 'Knorr', 'Krunchy Melts',
    'La Chiricana', 'La Estrella', 'La Lomita', 'La Marquesa', 'La Mexicana',
    'La Oración', 'La Yogurt', 'La Real', 'La Vaquita Golosa', 'Lactaid', 'Lantana',
    'Lindt', 'Lorens', 'Lucky Strike', 'Lundberg', 'M&M', 'Madre Tierra', 'Mafalda',
    'Malta Vigor', 'Mama Elisa', 'Marcos Salamanca', 'McCormick', 'Medina', 'Melo',
    'Miller', 'Miro', 'Misi Home', 'Montchevre', 'Moritex', "Mukky's", 'Nabisco',
    'Nestlé', 'Nevada', 'NHS', 'Nimar', 'Noel', 'Noritex Zona Libre', 'Nuba',
    'Nutremas', 'Nutritos', 'Ocean Food', 'Oreo', 'Organic Valley', 'Organics',
    'Orgran', 'P.A.N', 'Paisa', 'Palo Alto', 'Pampa', 'Panchos Kitchen', 'Pantera',
    'Pacific', 'Pascual', 'Pasta del Levante', 'Pasta Fresca', 'Pastas Donadio',
    'Pastas Frescas', 'Pedersen Fine Food', 'Pekados Gourmet', 'Pesca Fresca',
    'Pillsbury', 'Pita Pal', 'Planters', 'Polar', 'Pollo Caribeños', 'Post',
    'Pozuelo', 'Premier', 'Pretelt', 'Pringles', 'Producto a tu Gusto', 'Prolacsa',
    'Proluxsa', 'Purissima', 'Quaker', 'Questbar', 'R/S', 'Raquelita', 'Raspafresh',
    'Ready Crust', 'RIANDO', 'Rimith', 'Riscossa', 'Riquezas del Mar', 'Ritz',
    'Roland', 'Royal Paella', 'Sabra', 'Salvamar', 'Sarah Lee', 'Schweppes',
    'Sensodyne', 'Seven Days', 'Smithfield', 'Solan de Cabras', 'Spam', 'Starkist',
    'Stella', 'Stella Artois', 'Sun Maid', 'Superior', 'Supremo', 'Suquinsa',
    'Swanson', 'TAVIDIA', 'Terroir', 'Thermoseal', "Tilton's", 'Tio Sam', 'Toledano',
]

# ── Colores Tailwind ───────────────────────────────────────────────────────
GRAVEDAD_COLOR = {
    'Muy Alta': 'badge-alta',
    'Alta':     'badge-alta',
    'Media':    'badge-media',
    'Baja':     'badge-baja',
}

STATUS_COLOR = {
    'Abierta': 'badge-abierta',
    'Cerrada': 'badge-cerrada',
    'Cerrado': 'badge-cerrada',
}
