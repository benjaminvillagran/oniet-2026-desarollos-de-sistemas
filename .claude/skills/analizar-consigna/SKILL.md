---
name: analizar-consigna
description: Analiza la consigna de la competencia ONIET y arma el plan de trabajo (entidades, campos, validaciones, cálculos, pantallas y reparto de tareas para 3 personas). Usar apenas se recibe la consigna, antes de escribir código.
---

# Analizar la consigna

Objetivo: en 10 minutos pasar de la consigna a un plan concreto sobre la plantilla del repositorio.
**No escribas código en este paso.**

## Entrada

- El texto de la consigna (pegado en el chat o guardado en `docs/CONSIGNA.md`).
- Los archivos de datos que la acompañen (si hay, mirá los encabezados y las primeras 5 filas).

## Pasos

1. Leé `AGENTS.md` y `docs/plantillas/ANALISIS_CONSIGNA.md`.
2. Copiá la plantilla a `docs/ANALISIS.md` y completala:
   - Resumen del problema en 3 líneas y qué espera ver el jurado.
   - Entidades (tablas) con sus campos, tipo de dato y si son obligatorios.
   - Reglas de validación de cada campo (rangos, formatos, valores permitidos).
   - Cálculos y procesamiento pedidos, con un ejemplo numérico hecho a mano de cada uno.
   - Pantallas y salidas (listados, filtros, estadísticas, gráficos, exportación).
   - Mínimo indispensable vs. extras (si no alcanza el tiempo, se hace solo el mínimo).
3. Hacé una tabla **requisito → archivo de la plantilla que hay que cambiar**.
4. Listá hasta 5 dudas o ambigüedades para preguntarle al docente.
5. Repartí el trabajo en 3 personas según `docs/03_PLAN_DEL_DIA.md`, en tareas de 20 a 30 minutos,
   tocando archivos distintos para evitar conflictos de git.

## Salida

`docs/ANALISIS.md` completo y un resumen corto en el chat. Todo en español.
