---
name: adaptar-plantilla
description: Adapta la plantilla de ventas del repositorio al dominio de la consigna (tablas, validaciones, cálculos, pantallas y tests), siguiendo el orden de AGENTS.md. Usar después de analizar la consigna, cuando hay que cambiar el ejemplo de ventas por el problema real.
---

# Adaptar la plantilla al problema

Precondición: existe `docs/ANALISIS.md` con entidades, campos, validaciones y cálculos.
Si no existe, pedí primero correr la skill `analizar-consigna`.

## Pasos (en este orden, verificando al final de cada uno)

1. **Base de datos**: cambiá `app/schema.sql` con las tablas del análisis. Mantené la tabla
   `importaciones`. Después: `flask --app run reiniciar-db`.
2. **Validación**: en `app/servicios/validacion.py` actualizá `COLUMNAS`, `ALIAS` y la función
   `validar_*` con las reglas del análisis. Usá `a_decimal`, `a_entero` y `a_fecha` de
   `app/utils/conversiones.py`.
3. **Procesamiento**: en `app/servicios/procesamiento.py` escribí los cálculos como funciones puras.
   Por cada una, agregá un test en `tests/test_procesamiento.py` con el ejemplo hecho a mano.
4. **Repositorio**: actualizá el SQL (columnas, filtros y `COLUMNAS_ORDENABLES`). Siempre con `?`.
5. **Servicios y rutas**: conectá importación, alta manual, listado, estadísticas y exportación.
6. **Plantillas**: actualizá columnas de las tablas, formularios, KPIs y gráficos. Links en `base.html`.
7. **Datos**: copiá los archivos de la consigna a `data/ejemplos/` e importalos para probar.
8. **Config**: `NOMBRE_SISTEMA` y `NOMBRE_EQUIPO` en `app/config.py`.
9. **Tests**: adaptá los tests que usaban ventas. Corré `python herramientas/verificar.py --arreglar`.

## Reglas

- Si el problema tiene varias entidades, copiá el patrón completo de ventas en archivos nuevos
  (`<entidad>_repositorio.py`, `<entidad>_servicio.py`, `<entidad>_rutas.py`, plantillas y tests).
- Renombrá con cuidado: buscá todas las apariciones antes de cambiar un nombre.
- Después de cada paso grande, verificá que la app arranca (`python run.py`) y avisá para hacer commit.
