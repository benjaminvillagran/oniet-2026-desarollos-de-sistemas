---
name: adaptar-plantilla
description: Adapta la plantilla de ventas del repositorio al dominio de la consigna (tablas, validaciones, cálculos, pantallas y tests), siguiendo el orden de AGENTS.md. Usar después de analizar la consigna, cuando hay que cambiar el ejemplo de ventas por el problema real.
---

# Adaptar la plantilla al problema

Precondición: existe `docs/ANALISIS.md` con entidades, campos, validaciones y cálculos.
Si no existe, pedí primero correr la skill `analizar-consigna`.

## Paso 0: reemplazar, no duplicar

La entidad principal del problema **reemplaza** a "ventas". Renombrar los archivos con `git mv`:
`ventas_repositorio.py`, `ventas_servicio.py`, `ventas_rutas.py`, `ventas_listado.html`,
`ventas_formulario.html`, `ventas_detalle.html` → `<entidad>_*`. Al final del proceso,
`grep -ril venta app tests herramientas` no debería encontrar nada (salvo lo que se decida dejar).

## Pasos (en este orden, verificando al final de cada uno)

1. **Base de datos**: cambiá `app/schema.sql` con las tablas del análisis. Mantené la tabla
   `importaciones`. Después: `flask --app run reiniciar-db`.
2. **Validación**: en `app/servicios/validacion.py` actualizá `COLUMNAS`, `ALIAS` y la función
   `validar_*` con las reglas del análisis. Usá `a_decimal`, `a_entero` y `a_fecha` de
   `app/utils/conversiones.py`. Los nombres de `COLUMNAS` van en minúsculas con `_`: el lector
   normaliza los encabezados (`CompaniaSeguro` → `compania_seguro`). Si la consigna dice que un
   campo es único, poné `CLAVE_UNICA = "<campo>"` y agregá una restricción `UNIQUE` en `schema.sql`.
3. **Procesamiento**: en `app/servicios/procesamiento.py` escribí los cálculos como funciones puras.
   Por cada una, agregá un test en `tests/test_procesamiento.py` con el ejemplo hecho a mano.
   Lo que depende de una fila se calcula al importar (como `completar_venta`); lo agregado
   (rankings, tablas de posiciones) se calcula al consultar y no se guarda. Si no hay campos
   calculados por fila, se quita el paso PROCESAR de `importacion_servicio.py`.
4. **Repositorio**: actualizá el SQL (columnas, filtros y `COLUMNAS_ORDENABLES`). Siempre con `?`.
5. **Servicios y rutas**: conectá importación, alta manual, listado, estadísticas y exportación.
6. **Plantillas**: actualizá columnas de las tablas, formularios, KPIs y gráficos. Links en `base.html`.
7. **Datos**: borrá los archivos de ventas de `data/ejemplos/`, copiá ahí los de la consigna (la
   pantalla Importar solo lista esa carpeta) e importalos para probar. Si un archivo pesa más de
   5 MB (por ejemplo un GeoJSON), subí `MAX_CONTENT_LENGTH` en `app/config.py`.
8. **Config**: `NOMBRE_SISTEMA`, `NOMBRE_EQUIPO` y, si la consigna pide usuarios,
   `LOGIN_OBLIGATORIO = True` en `app/config.py` (los tests siguen sin login gracias a `conftest.py`).
9. **Tests**: adaptá los tests que usaban ventas. Corré `python herramientas/verificar.py --arreglar`.

## Partes atadas al ejemplo de ventas (revisarlas todas)

- `FiltrosVentas` en el repositorio y el macro `filtros_ventas` de `_macros.html`.
- La lista `datos_graficos` de `estadisticas.html` (gráficos), los KPIs de `inicio.html` y
  `principal_rutas.py`.
- El menú de `base.html` y el botón "Ver ventas" de `importacion_resultado.html`.
- `COLUMNAS_EXPORTACION` en `reportes_servicio.py`, `reportes_rutas.py` y la API en `api_rutas.py`.
- `CSV_VALIDO` en `tests/conftest.py` y los tests de rutas, validación y procesamiento.
- Los archivos de `data/ejemplos/` (borrar los de ventas y poner los de la consigna).

## Reglas

- Si el problema tiene **otra** entidad además de la principal, copiá el patrón completo en archivos
  nuevos (`<entidad>_repositorio.py`, `<entidad>_servicio.py`, `<entidad>_rutas.py`, plantillas y
  tests). Las rutas se registran solas si el archivo se llama `<entidad>_rutas.py` y tiene `bp`.
  Ver el ejemplo completo de dos tablas relacionadas en `docs/05_ADAPTAR_PLANTILLA.md`.
- Los tests de ventas se reemplazan por tests del problema real (es lo esperado). Si un test del
  ejemplo contradice la consigna (por ejemplo, espera filas duplicadas y la consigna dice que una
  clave es única), se reemplaza el test: nunca se cambia el esquema para que pase.
- "Los N primeros con desempate al azar": `primeros_n()` de `procesamiento.py`.
- Renombrá con cuidado: buscá todas las apariciones antes de cambiar un nombre.
- Después de cada paso grande, verificá que la app arranca (`python run.py`) y avisá para hacer commit.
