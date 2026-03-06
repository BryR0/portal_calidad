# Portal de Calidad — Grupo Riba Smith

Sistema interno de gestión de **No Conformidades (NC)** para el Departamento de Gestión de Calidad. Permite registrar, clasificar, hacer seguimiento y cerrar desviaciones detectadas en sucursales, proveedores y procesos internos.

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12 + Flask (SQLAlchemy, Migrate, Login, WTF) |
| Base de datos | PostgreSQL 16 (Docker) |
| Frontend | Jinja2 + Tailwind CSS |
| Exportación | openpyxl (Excel), HTML print view |
| Async (futuro) | Celery + Redis |

---

## Estructura del proyecto

```
portal_calidad/
├── app/
│   ├── __init__.py          # Factory de la aplicación Flask
│   ├── models/              # SQLAlchemy models (nc.py, user.py, catalogs.py, maestras.py)
│   ├── routes/              # Blueprints (nc.py, auth.py, admin.py, main.py)
│   ├── templates/           # Jinja2 (base.html, nc/, admin/, auth/, main/)
│   ├── static/css/          # input.css (fuente Tailwind) → output.css (compilado)
│   └── data/                # Catálogos estáticos (catalogs.py)
├── migrations/              # Flask-Migrate (Alembic)
├── scripts/                 # seed_admin.py, seed_catalogs.py
├── config.py                # Configuración (Dev / Prod)
├── run.py                   # Punto de entrada
├── docker-compose.yml       # PostgreSQL + Redis
├── package.json             # Tailwind CSS (Node)
├── tailwind.config.js
└── compile_css.bat          # Compilar Tailwind en Windows
```

---

## Requisitos previos

- Python 3.12+
- Node.js 18+ (solo para compilar CSS)
- Docker Desktop (para la base de datos)

---

## Configuración inicial

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd portal_calidad
```

### 2. Entorno virtual Python

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

### 3. Variables de entorno

Copia el archivo de ejemplo y ajusta los valores:

```bash
cp .env.example .env
```

Variables clave en `.env`:

```env
SECRET_KEY=cambia-esto-en-produccion
DATABASE_URL=postgresql://root:root@localhost:5432/portal_calidad

# Opcional: MySQL en vez de PostgreSQL
# DB_ENGINE=mysql
# DB_USER=root
# DB_PASSWORD=root
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=portal_calidad
```

### 4. Levantar la base de datos con Docker

```bash
docker-compose up -d
```

Esto inicia PostgreSQL en el puerto `5432` y Redis en `6379`.

### 5. Migraciones

```bash
flask db upgrade
```

### 6. Seeds de catálogos y usuario admin

```bash
python scripts/seed_catalogs.py
python scripts/seed_admin.py
```

### 7. Compilar CSS (Tailwind)

```bat
compile_css.bat
```

O con Node directamente:

```bash
npx tailwindcss -i app/static/css/input.css -o app/static/css/output.css --watch
```

### 8. Correr el servidor de desarrollo

```bash
flask run
```

La aplicación queda disponible en `http://localhost:5000`.

---

## Funcionalidades principales

- **Registro de NCs** — formulario con identificación, hallazgo, producto, clasificación e impacto
- **Vista ejecutiva** — detalle completo con panels por sección, métricas de inventario y colores de impacto
- **Cierre de NC** — acciones inmediatas (×3) + acción correctiva, registra usuario y fecha
- **Bandeja de NCs** — tabla paginada con filtros por estado, gravedad, fecha y búsqueda libre
- **Vista de impresión individual** — HTML optimizado para A4 landscape, equivalente visual al sistema de fichas Excel
- **Vista de impresión de lista** — HTML imprimible con stats, filtros activos y tabla resumen
- **Exportación Excel individual** — workbook estructurado por secciones con colores de impacto y métricas destacadas
- **Exportación Excel de lista** — tabla plana con todos los campos, filtros y autofilter
- **Roles** — admin / calidad / user con permisos diferenciados

---

## Roles de usuario

| Rol | Puede crear | Puede editar | Puede cerrar | Acceso admin |
|---|:---:|:---:|:---:|:---:|
| `user` | ✓ | Solo NCs abiertas propias | — | — |
| `calidad` | ✓ | Todas | ✓ | — |
| `admin` | ✓ | Todas | ✓ | ✓ |

---

## Comandos útiles

```bash
# Crear nueva migración tras cambios en modelos
flask db migrate -m "descripcion"
flask db upgrade

# Acceder a la shell de Flask
flask shell

# Ver logs del contenedor de DB
docker logs portal_calidad_db
```

---

## Convenciones de código

- Rutas en `app/routes/nc.py` — blueprint `nc_bp`, prefijo `/nc`
- Templates en `app/templates/nc/` — `list.html`, `view.html`, `create.html`, `edit.html`, `print.html`, `print_list.html`
- Excel builders al final de `nc.py` — `_build_list_workbook()` y `_build_single_workbook()`
- Catálogos estáticos en `app/data/catalogs.py`; catálogos de DB en `app/models/catalogs.py`
