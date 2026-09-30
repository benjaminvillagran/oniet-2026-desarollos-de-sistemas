# 07 · Práctica: simulacros con reloj

La única forma de llegar seguros es **haber hecho la competencia antes**. Hagan al menos **2
simulacros completos** de 2 h 30 min, con el reloj y el plan de `03_PLAN_DEL_DIA.md`, en las mismas
notebooks que van a llevar.

## Cómo hacer un simulacro

1. Crear un repositorio nuevo de práctica (por ejemplo `simulacro-1`) y clonarlo los 3.
   Copiar el archivo de la práctica de `data/practica/` a `data/ejemplos/` (la pantalla Importar
   solo lista esa carpeta) y borrar los de ventas.
2. Poner el cronómetro en 2:30 y arrancar como si fueran las 14:00.
3. Uno lee la consigna en voz alta; se completa el análisis con `/analizar-consigna`.
4. Seguir el plan del día al pie de la letra (roles, commits, cortes de tiempo).
5. A los 2:00 se congela: solo arreglos y entrega (`/entrega-final`).
6. Al terminar, comparar con `07_PRACTICA_SOLUCIONES.md` y anotar:
   - ¿Qué nos atrasó? ¿Qué IA respondió mejor para cada tarea? ¿Qué prompt funcionó?
   - ¿Hubo conflictos de git? ¿Por qué?
   - Puntaje estimado con `/revisar-rubrica`.
7. Mejorar las skills, prompts o este documento con lo aprendido.

> El número de fila de los errores cuenta la línea de encabezado: la primera fila de datos es la 2.
>
> Los datos de práctica están en `data/practica/` y tienen **errores a propósito** (como pasaría
> en la competencia): el sistema tiene que rechazarlos e informarlos sin romperse.

## Así fueron las consignas reales de ONIET

Encontradas en repositorios públicos de participantes (enunciados oficiales en PDF o Word; la de
2023 se deduce del código de un participante porque no se encontró el enunciado):

| Año | Tema | Datos | Qué pedía |
|---|---|---|---|
| 2020 | COVID-19 por país | API pública (JSON) | Login con fecha de último acceso (30 %), configuración de usuario (40 %), dashboard con casos e históricos de 10 días (30 %) |
| 2021 | ONG que asigna paquetes de ayuda a barrios populares | Dataset de datos.gob.ar (Registro Nacional de Barrios Populares) | Login (5 %), listado filtrado por provincia y localidad (25 %), detalle (20 %), asignar paquetes (10 %), sumatorias por localidad y provincia (20 %), los N barrios con menor proporción paquetes/familia; si hay muchos en la misma condición, se eligen N al azar (20 %) |
| 2023 | Control de calidad de producción (deducido del código de un participante) | JSON | Registros por empresa y mes con piezas fallidas |
| 2025 | Taller mecánico y compañías de seguro | CSV **y** JSON (con BOM y números como texto) | Ranking de compañías por total de cobertura; ranking de regiones por servicios |

Lo que se repite: **leer CSV/JSON (a veces una API), validar, guardar, filtrar, ver detalle,
modificar registros, sumar/agrupar y rankear**; a veces **login**. Los enunciados evaluaban también
diseño (simple, tolerante a fallos), prolijidad del código, UX intuitiva y **tiempo de entrega**.
La plantilla ya cubre todo eso (incluido login opcional e importación desde URL).

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
3. Muestre: goles totales, promedio de goles por partido y el partido con más goles (si hay
   empate, el primero por fecha).
4. Permita cargar un partido a mano y ver cómo se actualiza la tabla.
5. Muestre el historial de partidos de un equipo elegido.

> Esta práctica tiene una dificultad extra: la tabla de posiciones **no está en el archivo**, hay
> que calcularla (procesamiento puro). Es el tipo de cálculo que más puntos da en la rúbrica.

## Práctica 4 · Taller mecánico y aseguradoras (estilo ONIET 2025)

**Archivos:** `data/practica/taller_servicios_2024_2025.csv` (separado por `;`) y
`data/practica/taller_servicios_2026.json` (lista de objetos). Hay que cargar **los dos**.
Columnas: `NumeroRegistro`, `CompaniaSeguro`, `Anio`, `Mes`, `CantidadServicios`, `Region`,
`ValorPorServicio`, `PorcentajeCobertura`.

Trampas (como en la consigna real): el JSON viene con BOM y **todos los valores como texto**; el
porcentaje es un entero (`88` significa 88 %).

1. Importar ambos archivos a la base, sin duplicar registros (`NumeroRegistro` es único: usar
   `CLAVE_UNICA` en `validacion.py` y `UNIQUE` en `schema.sql`).
2. **Facturado** = `CantidadServicios × ValorPorServicio`; **total de cobertura** = facturado ×
   `PorcentajeCobertura` / 100.
3. **Reporte 1**: ranking de compañías por total de cobertura, de mayor a menor.
4. **Reporte 2**: ranking de regiones por cantidad de servicios.
5. Mostrar el período que abarcan los datos ("Período 01/2024 a 06/2026") calculado de los datos.
6. Filtros por año y por compañía.

## Práctica 5 · Barrios populares y paquetes de ayuda (estilo ONIET 2021)

**Archivo:** `data/practica/barrios_populares.csv` (separado por `,`).
Columnas: `id_barrio`, `nombre_barrio`, `provincia`, `localidad`, `cantidad_familias`.

1. **Login** de usuarios (activar `LOGIN_OBLIGATORIO` en `app/config.py`).
2. Listado de barrios filtrado por provincia y por localidad.
3. **Detalle** de un barrio con sus paquetes asignados.
4. **Asignar paquetes** a un barrio (cantidad y fecha): se guarda en una tabla nueva
   `asignaciones` relacionada con el barrio.
5. Sumatorias de familias y de paquetes por localidad y por provincia.
6. Los **N barrios con menor proporción paquetes/familias** (N lo elige el usuario); si hay empate,
   se desempata al azar (pista: `primeros_n()` de `procesamiento.py`, testeado con
   `random.Random(semilla)`).

> Para practicar con los **datos reales** de la consigna 2021: el dataset "Registro Nacional de
> Barrios Populares" de datos.gob.ar (CSV de ~6.500 barrios). Ahí las columnas se llaman
> `id_renabap` y `cantidad_familias_aproximada`: agregarlas a `ALIAS` en `validacion.py`.

> Esta práctica ejercita **dos entidades relacionadas** (barrios y asignaciones): seguir
> "Si el problema tiene más de una entidad" en `05_ADAPTAR_PLANTILLA.md`.
