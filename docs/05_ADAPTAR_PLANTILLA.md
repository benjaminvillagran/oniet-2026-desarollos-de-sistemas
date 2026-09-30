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
| 9 | `app/config.py` | `NOMBRE_SISTEMA`, `NOMBRE_EQUIPO` | Se ve en el encabezado |
| 10 | `tests/` | Datos de prueba del problema nuevo | `python herramientas/verificar.py` |

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

Ejemplo: alumnos y notas, productos y ventas, equipos y partidos.

- Crear una tabla por entidad, relacionadas con `REFERENCES` (clave foránea).
- Copiar el patrón completo por entidad: `<entidad>_repositorio.py`, `<entidad>_servicio.py`,
  `<entidad>_rutas.py` (registrarla en `app/__init__.py`), plantillas y tests.
- **Lo que se puede calcular no se guarda**: por ejemplo, la tabla de posiciones de un torneo se
  calcula en `procesamiento.py` a partir de los partidos guardados.

## Errores comunes al adaptar

| Síntoma | Causa probable | Solución |
|---|---|---|
| `no such column` / `no such table` | La base tiene el esquema viejo | Reiniciar la base |
| "Faltan columnas obligatorias" al importar | Encabezados del archivo distintos a `COLUMNAS` | Agregar el nombre a `ALIAS` |
| Números mal leídos (1.500 → 1,5) | Formato con punto de miles sin coma decimal | Revisar el archivo; ajustar `a_decimal` y agregar un test |
| `BuildError` en una plantilla | `url_for` con un nombre de ruta que ya no existe | Buscar el nombre viejo en `templates/` |
| La página muestra datos viejos | Faltó reiniciar el servidor | Cortar con Ctrl+C y volver a correr `python run.py` |
