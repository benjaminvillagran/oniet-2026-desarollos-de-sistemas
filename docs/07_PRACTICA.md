# 07 · Práctica: simulacros con reloj

La única forma de llegar seguros es **haber hecho la competencia antes**. Hagan al menos **2
simulacros completos** de 2 h 30 min, con el reloj y el plan de `03_PLAN_DEL_DIA.md`, en las mismas
notebooks que van a llevar.

## Cómo hacer un simulacro

1. Crear un repositorio nuevo de práctica (por ejemplo `simulacro-1`) y clonarlo los 3.
2. Poner el cronómetro en 2:30 y arrancar como si fueran las 14:00.
3. Uno lee la consigna en voz alta; se completa el análisis con `/analizar-consigna`.
4. Seguir el plan del día al pie de la letra (roles, commits, cortes de tiempo).
5. A los 2:00 se congela: solo arreglos y entrega (`/entrega-final`).
6. Al terminar, comparar con `07_PRACTICA_SOLUCIONES.md` y anotar:
   - ¿Qué nos atrasó? ¿Qué IA respondió mejor para cada tarea? ¿Qué prompt funcionó?
   - ¿Hubo conflictos de git? ¿Por qué?
   - Puntaje estimado con `/revisar-rubrica`.
7. Mejorar las skills, prompts o este documento con lo aprendido.

> Los datos de práctica están en `data/practica/` y tienen **errores a propósito** (como pasaría
> en la competencia): el sistema tiene que rechazarlos e informarlos sin romperse.

---

## Práctica 1 · Biblioteca escolar

**Archivo:** `data/practica/biblioteca_prestamos.csv` (separado por `;`).
Columnas: `socio`, `libro`, `fecha_prestamo`, `fecha_devolucion` (vacía si todavía no se devolvió).

La biblioteca necesita un sistema que:

1. Importe el archivo de préstamos y valide: `socio`, `libro` y `fecha_prestamo` obligatorios;
   fechas válidas (`DD/MM/AAAA`); la devolución no puede ser anterior al préstamo.
2. Calcule para cada préstamo:
   - **Días de préstamo**: devolución − préstamo. Si no se devolvió, se cuenta hasta la **fecha
     de corte 30/06/2026**.
   - **Días de atraso**: lo que exceda los **7 días** permitidos (mínimo 0).
   - **Multa**: **$150 por día de atraso**.
3. Muestre un listado con filtros por socio y por estado (devuelto / pendiente).
4. Muestre un reporte con: préstamos pendientes, cantidad y porcentaje de préstamos con atraso,
   total de multas, los 3 libros más prestados y los 3 socios con más multas.
5. Permita registrar un préstamo nuevo a mano y marcar una devolución.

## Práctica 2 · Estación meteorológica

**Archivo:** `data/practica/meteorologia_lecturas.json` (objeto con la lista `lecturas`).
Campos: `fecha_hora` (`AAAA-MM-DD HH:MM`), `estacion`, `temperatura` (°C), `humedad` (%),
`lluvia_mm`.

1. Importe las lecturas y descarte las inválidas: todos los campos obligatorios; temperatura entre
   −30 y 55 °C; humedad entre 0 y 100 %; lluvia mayor o igual a 0.
2. Para cada estación: temperatura promedio, máxima y mínima, y lluvia total.
3. **Alertas de calor**: listado de lecturas con temperatura mayor o igual a 35 °C.
4. **Día más lluvioso** (sumando todas las estaciones).
5. Gráfico de temperatura promedio por día para cada estación.
6. Filtros por estación y rango de fechas.

## Práctica 3 · Torneo intercolegial de fútbol

**Archivo:** `data/practica/torneo_partidos.csv` (separado por `,`).
Columnas: `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`.

1. Importe los resultados y rechace los inválidos: goles enteros mayores o iguales a 0; un equipo
   no puede jugar contra sí mismo.
2. Arme la **tabla de posiciones**: PJ, PG, PE, PP, GF, GC, DG y puntos (ganado 3, empate 1,
   perdido 0). Orden: puntos, después diferencia de gol, después goles a favor, después nombre.
3. Muestre: goles totales, promedio de goles por partido y el partido con más goles.
4. Permita cargar un partido a mano y ver cómo se actualiza la tabla.
5. Muestre el historial de partidos de un equipo elegido.

> Esta práctica tiene una dificultad extra: la tabla de posiciones **no está en el archivo**, hay
> que calcularla (procesamiento puro). Es el tipo de cálculo que más puntos da en la rúbrica.
