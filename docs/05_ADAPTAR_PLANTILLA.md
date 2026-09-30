# 05 · Adaptar la plantilla a la consigna

La plantilla resuelve un problema de ejemplo (**ventas**) de punta a punta. El día de la competencia
se reemplaza "ventas" por el problema real. Con IA: `/adaptar-plantilla` después de
`/analizar-consigna`. Esta guía explica qué hace ese proceso, para poder revisarlo y corregirlo.

## Qué NO hay que tocar (ya funciona para cualquier problema)

- `app/servicios/lector.py`: lee CSV, TXT, JSON y Excel, detecta el separador y la codificación.
- `app/utils/conversiones.py`: `a_decimal`, `a_entero`, `a_fecha` (formatos argentinos).
- `app/utils/formato.py`: filtros `moneda`, `numero`, `fecha`, `mes`, `porcentaje`.
- `app/db.py`, `app/repositorios/importaciones_repositorio.py`, historial de importaciones.
- `app/static/css/estilos.css`, `base.html`, `_macros.html`, `error.html`.
- `herramientas/`, `.github/workflows/`, `AGENTS.md`, skills.

## Qué SÍ hay que cambiar, en orden

| Paso | Archivo | Qué cambia | Cómo verificar |
|---|---|---|---|
| 1 | `app/schema.sql` | Tablas y columnas del problema | `flask --app run reiniciar-db` sin errores |
| 2 | `app/servicios/validacion.py` | `COLUMNAS`, `ALIAS`, `validar_*` | Tests de validación |
| 3 | `app/servicios/procesamiento.py` | Cálculos de la consigna | Tests con ejemplos hechos a mano |
| 4 | `app/repositorios/*_repositorio.py` | SQL: columnas, filtros, orden | La página de listado carga |
| 5 | `app/servicios/*_servicio.py` | Importar, crear, eliminar | Importar el archivo de la consigna |
| 6 | `app/rutas/*.py` | Páginas y parámetros | Todas las páginas cargan |
| 7 | `app/templates/*.html` | Columnas, formularios, KPIs, gráficos, menú | `/probar-en-navegador` |
| 8 | `data/ejemplos/` | Archivos de la consigna | Aparecen en la pantalla Importar |
| 9 | `app/config.py` | `NOMBRE_SISTEMA`, `NOMBRE_EQUIPO`, `LOGIN_OBLIGATORIO` | Se ve en el encabezado |
| 10 | `tests/` | Datos de prueba del problema nuevo | `python herramientas/verificar.py` |

**Reemplazar, no duplicar.** La entidad principal ocupa el lugar de "ventas": renombrar los
archivos con `git mv` (`ventas_repositorio.py` → `partidos_repositorio.py`, etc.) y al final
buscar restos con `grep -ril venta app tests herramientas` (Windows: `findstr /s /i /m venta app\*.* tests\*.*`).

**Partes atadas al ejemplo que se olvidan fácil**: `FiltrosVentas`, el macro `filtros_ventas`, la
lista de gráficos en `estadisticas.html`, los KPIs de `inicio.html`, `COLUMNAS_EXPORTACION`,
`CSV_VALIDO` en `tests/conftest.py` y `data/ejemplos/`.

**Tests**: los de ventas se **reemplazan** por tests del problema real (es lo esperado). Lo que no se
hace nunca es borrar o debilitar un test para que "pase".

> **Importante:** después de cambiar `schema.sql` hay que reiniciar la base
> (`flask --app run reiniciar-db` o borrar `instance/datos.db`). Si no, las tablas viejas siguen ahí.

## Ejemplo: de "ventas" a "préstamos de biblioteca" (práctica 1)

| Ventas (plantilla) | Préstamos (práctica) |
|---|---|
| Tabla `ventas` | Tabla `prestamos` |
| `fecha`, `producto`, `categoria`, `cantidad`, `precio_unitario` | `socio`, `libro`, `fecha_prestamo`, `fecha_devolucion` (opcional) |
| Validación: cantidad > 0, precio ≥ 0 | Validación: devolución ≥ préstamo; devolución puede estar vacía |
| Calculado al importar: `total = cantidad × precio` | Calculados: `dias`, `dias_atraso`, `multa` (con fecha de corte) |
| Estadísticas: por categoría, por mes, top productos | Reporte: pendientes, % con atraso, total multas, top libros, top socios |
| Filtro por categoría | Filtro por socio y por estado (devuelto / pendiente) |

Prompt sugerido (después del análisis):

```
Seguí la skill adaptar-plantilla para convertir el ejemplo de ventas en préstamos de
biblioteca según docs/ANALISIS.md. Hacelo paso por paso y después de cada paso corré
python herramientas/verificar.py. No cambies lector.py ni conversiones.py.
```

## Si el problema tiene más de una entidad

Ejemplo: barrios y asignaciones de paquetes (consigna 2021), alumnos y notas, equipos y partidos.
La entidad principal reemplaza a "ventas"; la otra se agrega copiando el patrón en archivos nuevos
(`asignaciones_repositorio.py`, `asignaciones_servicio.py`, `asignaciones_rutas.py` con su `bp`,
plantillas y tests). **Las rutas se registran solas**: no hay que tocar `app/__init__.py`.

**1. Tablas relacionadas** (`schema.sql`). La tabla hija va después de la padre:

```sql
CREATE TABLE IF NOT EXISTS barrios (
    id                INTEGER PRIMARY KEY,           -- el id que trae el archivo (único)
    nombre_barrio     TEXT    NOT NULL,
    provincia         TEXT    NOT NULL,
    localidad         TEXT    NOT NULL,
    cantidad_familias INTEGER NOT NULL CHECK (cantidad_familias > 0)
);

CREATE TABLE IF NOT EXISTS asignaciones (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    barrio_id INTEGER NOT NULL REFERENCES barrios (id) ON DELETE CASCADE,  -- si se borra el barrio, se borran sus asignaciones
    fecha     TEXT    NOT NULL,
    paquetes  INTEGER NOT NULL CHECK (paquetes > 0)
);
```

`db.py` ya activa las claves foráneas (`PRAGMA foreign_keys = ON`). Como el id viene del archivo,
poner `CLAVE_UNICA = "id_barrio"` (o el nombre que tenga) en `validacion.py`.

**2. Listado del padre con un total del hijo** (repositorio):

```python
SQL_BARRIOS = """
    SELECT b.*, COALESCE(SUM(a.paquetes), 0) AS paquetes
    FROM barrios AS b
    LEFT JOIN asignaciones AS a ON a.barrio_id = b.id
    GROUP BY b.id
"""
```

Para ordenar por la columna calculada, `COLUMNAS_ORDENABLES` puede ser un diccionario
`{"paquetes": "paquetes", "familias": "b.cantidad_familias", ...}` (nombre en la URL → expresión SQL).

**3. Detalle con las filas hijas y un formulario para agregar** (rutas):

```python
@bp.route("/<int:barrio_id>")
def detalle(barrio_id):
    barrio = barrios_repositorio.obtener_por_id(barrio_id) or abort(404)
    return render_template(
        "barrios_detalle.html",
        barrio=barrio,
        asignaciones=asignaciones_repositorio.del_barrio(barrio_id),
        datos={},
        errores={},
    )


@bp.route("/<int:barrio_id>/asignar", methods=["POST"])
def asignar(barrio_id):
    barrio = barrios_repositorio.obtener_por_id(barrio_id) or abort(404)
    datos = request.form.to_dict()
    errores = asignaciones_servicio.asignar(barrio_id, datos)  # valida y guarda en transacción
    if not errores:
        flash("Paquetes asignados.", "exito")
        return redirect(url_for(".detalle", barrio_id=barrio_id))
    return render_template(
        "barrios_detalle.html",
        barrio=barrio,  # se vuelve a mostrar con errores
        asignaciones=asignaciones_repositorio.del_barrio(barrio_id),
        datos=datos,
        errores=errores,
    )
```

**4. Ranking con desempate al azar** (procesamiento): calcular la proporción y usar
`primeros_n(barrios, "proporcion", n, mayor_primero=False)`. En el test se pasa
`azar=random.Random(1)` para que el resultado sea siempre el mismo.

**5. Lo que se puede calcular no se guarda**: la proporción, la tabla de posiciones de un torneo o
los totales por provincia se calculan en `procesamiento.py` a partir de lo guardado.

## Si la consigna pide login

`LOGIN_OBLIGATORIO = True` en `app/config.py`. Queda protegida toda página salvo ingresar y
registrarse (la primera vez hay que crear un usuario en `/registrarse`). Los tests siguen corriendo
sin login porque `tests/conftest.py` lo apaga; el login se prueba con la fixture `cliente_con_login`.

## Errores comunes al adaptar

| Síntoma | Causa probable | Solución |
|---|---|---|
| `no such column` / `no such table` | La base tiene el esquema viejo | Reiniciar la base |
| "Faltan columnas obligatorias" al importar | Encabezados del archivo distintos a `COLUMNAS` | Agregar el nombre a `ALIAS` |
| Números mal leídos (1.500 → 1,5) | Formato con punto de miles sin coma decimal | Revisar el archivo; ajustar `a_decimal` y agregar un test |
| `BuildError` en una plantilla | `url_for` con un nombre de ruta que ya no existe | Buscar el nombre viejo en `templates/` |
| La página muestra datos viejos | Faltó reiniciar el servidor | Cortar con Ctrl+C y volver a correr `python run.py` |
