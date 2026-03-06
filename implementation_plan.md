# Portal de Gestión de Calidad - Plan de Implementación

Resolución y diseño de un portal web orientado a la gestión integral de desviaciones de calidad (No Conformidades - NC) en base a la información proporcionada.

## Modelo de Datos Propuesto

A partir de la data recibida, la entidad central será la **No Conformidad (NC)**, la cual abarca varios frentes de la gestión de calidad. Recomendamos normalizar estos datos separando parámetros repetitivos en tablas de catálogo.

**Estructura Base (Campos clave):**

*   **Identificación y Rastreo:**
    *   `N° NC` (ej. 03012026-900-PI)
    *   `Fecha` / `Hora`
*   **Origen del Reporte:**
    *   `Detectada por` (Colaborador, Cliente, etc.)
    *   `Departamento/Empresa` (Área que reporta)
*   **Información del Proveedor/Marca:**
    *   `Tipo de Proveedor` (Interno, Local, etc.)
    *   `Empresa` (Ej. Riba Smith, S.A., Proveedor Externo)
    *   `Marca`
*   **Clasificación del Evento:**
    *   `Desviación` (ej. Correctiva)
    *   `Gravedad` (Alta, Media, Baja)
    *   `Clasificación NC` (ej. Físico/Physical, Biológica)
    *   `Prerrequisito` / `Motivo` / `Causa`
*   **Detalle de la Incidencia:**
    *   `Sección` (Artesanal, Carimañolas, Carnicería, Chocolatería, etc.)
    *   `Título`
    *   `Descripción` detallada
    *   `Producto NC` (Relación con `ReporteMaestro`)

### Nuevas Tablas de Soporte (Autocompletado Rápido):
*   **Reporte Maestro (Catálogo de Productos):** Para rellenar rápidamente código de barras, descripción y otros datos del producto.
*   **Suplidores (Catálogo de Proveedores):** Para vincular los incidentes directamente con sus respectivos proveedores existentes.
*   **Impacto:**
    *   `Total NC (kg)`
    *   `Total NC ($)`
*   **Plan de Acción y Seguimiento:**
    *   `Evaluaciones`
    *   `Acciones (1, 2, 3)`
    *   `Acción Correctiva` (Plan final)
    *   `Estado` (Abierta, Cerrada, En Proceso)
    *   `Fecha de Cierre`

## Arquitectura Tecnológica (Basada en DocVersion)

Para mantener homogeneidad con los proyectos actuales (como `docversion`), el portal de calidad utilizará el siguiente stack tecnológico:

*   **Backend Framework:** Python con **Flask** (Flask-SQLAlchemy para ORM, Flask-Migrate, Flask-Login, Flask-WTF, utilerías como `itsdangerous` e integraciones para manejo y envío de correos).
*   **Base de Datos Relacional:** **MySQL** para almacenar las No Conformidades, catálogos (Secciones), y maestras (Reporte Maestro, Suplidores).
*   **Frontend y Diseño:** Plantillas Jinja2 integradas con **Tailwind CSS** (vía npm/npx) para un diseño moderno, limpio y responsivo.
*   **Procesamiento Asíncrono:** **Celery** con **Redis** como broker (gestión de envío de correos de recuperación de contraseña, notificaciones y exportaciones de reportes).
*   **Infraestructura Local:** Uso de docker-compose para levantar la base de datos (MySQL) y Redis en desarrollo.

## Hitos de Desarrollo

1.   **Diseño DB y API:** Crear todos los esquemas (Base de datos) y la API para conectar los datos.
2.   **Desarrollo del Frontend Core:** Esquemas de autenticación (Login, Recuperación de contraseña, Olvidé mi contraseña), diseño de plantillas HTML para correos y plantillas de navegación base.
3.   **Módulo de Captura (Formularios):** Traducción del Excel de captura de datos a un formulario web intuitivo, dividido por secciones.
4.   **Bandeja de Gestión:** Listado y filtros de las no conformidades. Panel para que los administradores / calidad dejen evidencia del cierre (Acción 1, 2, 3).
5.   **Dashboard Analítico:** Pantalla de resumen gerencial con indicadores sobre el volumen y estado de incidencias.

## User Review Required

> [!IMPORTANT]
> Se ha actualizado el plan para alinearlo con el proyecto `docversion` y añadir flujos de contraseña. Por favor confirmar:
> 1. **Creación del Proyecto:** ¿Desea que inicialice el proyecto creando un directorio nuevo llamado `portal_calidad` (o el nombre que prefiera) al mismo nivel que `docversion`?
> 2. **Roles de Usuario:** ¿Requerimos roles de negocio específicos en esta fase inicial (ej. "Admin/Calidad" para cerrar un evento, vs "Usuario Regular" que solo reporta)?
