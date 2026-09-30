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
   `app/utils/conversiones.py`.
3. **Procesamiento**: en `app/servicios/procesamiento.py` escribí los cálculos como funciones puras.
   Por cada una, agregá un test en `tests/test_procesamiento.py` con el ejemplo hecho a mano.
   Lo que depende de una fila se calcula al importar (como `completar_venta`); lo agregado
   (rankings, tablas de posiciones) se calcula al consultar y no se guarda. Si no hay campos
   calculados por fila, se quita el paso PROCESAR de `importacion_servicio.py`.
4. **Repositorio**: actualizá el SQL (columnas, filtros y `COLUMNAS_ORDENABLES`). Siempre con `?`.
5. **Servicios y rutas**: conectá importación, alta manual, listado, estadísticas y exportación.
6. **Plantillas**: actualizá columnas de las tablas, formularios, KPIs y gráficos. Links en `base.html`.
7. **Datos**: copiá los archivos de la consigna a `data/ejemplos/` e importalos para probar.
8. **Config**: `NOMBRE_SISTEMA` y `NOMBRE_EQUIPO` en `app/config.py`.
9. **Tests**: adaptá los tests que usaban ventas. Corré `python herramientas/verificar.py --arreglar`.

## Partes atadas al ejemplo de ventas (revisarlas todas)

- `FiltrosVentas` en el repositorio y el macro `filtros_ventas` de `_macros.html`.
- La lista `datos_graficos` de `estadisticas.html` (gráficos) y los KPIs de `inicio.html`.
- `COLUMNAS_EXPORTACION` en `reportes_servicio.py` y la API en `api_rutas.py`.
- `CSV_VALIDO` en `tests/conftest.py` y los tests de rutas, validación y procesamiento.
- Los archivos de `data/ejemplos/` (borrar los de ventas y poner los de la consigna).

## Reglas

- Si el problema tiene **otra** entidad además de la principal, copiá el patrón completo en archivos
  nuevos (`<entidad>_repositorio.py`, `<entidad>_servicio.py`, `<entidad>_rutas.py`, plantillas y
  tests) y registrá el blueprint en `app/__init__.py`.
- Los tests de ventas se reemplazan por tests del problema real (es lo esperado).
- Renombrá con cuidado: buscá todas las apariciones antes de cambiar un nombre.
- Después de cada paso grande, verificá que la app arranca (`python run.py`) y avisá para hacer commit.
