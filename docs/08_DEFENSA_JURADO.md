# 08 · Presentar y defender el sistema ante el jurado

El jurado evalúa "el sistema producido, el cumplimiento de la consigna, el funcionamiento, el código
fuente, la interfaz y la entrega". Si les preguntan, **los 3 tienen que poder explicar el sistema**.
Usar IA está permitido; no entender lo que entregamos, no.

## Demo de 3 minutos (practicarla en cada simulacro)

1. **El problema (20 s)**: "La consigna pedía… Nuestro sistema permite…".
2. **Lectura (40 s)**: importar el archivo de la consigna. Mostrar cuántas filas se leyeron y
   guardaron. Importar un archivo con errores y mostrar que el sistema **no se rompe** e informa
   fila, campo y motivo.
3. **Procesamiento y resultados (60 s)**: estadísticas o reporte. Mostrar un número y explicar
   cómo se calcula ("el total es cantidad × precio; lo verificamos a mano y con un test").
4. **Uso (30 s)**: filtros, orden, alta manual con validación, exportar CSV.
5. **Calidad y entrega (30 s)**: capas del código, tests en verde, workflow de GitHub Actions,
   commits de los 3.

## Arquitectura en una frase

> "Usamos Flask con SQLite. El código está en capas: las **rutas** reciben los pedidos, los
> **servicios** leen, validan y procesan los datos, y los **repositorios** guardan y consultan la
> base con SQL parametrizado."

```
Navegador ──► rutas/ ──► servicios/ ──────────────► repositorios/ ──► SQLite (instance/datos.db)
                         lector → validacion → procesamiento
```

## Preguntas probables y cómo responder

| Pregunta | Respuesta (adaptarla al problema real) |
|---|---|
| ¿Cómo leen los datos? | `lector.py` acepta CSV, JSON y Excel; detecta el separador y la codificación, y convierte todo a una lista de filas. |
| ¿Qué pasa si el archivo tiene errores? | Cada fila se valida en `validacion.py`. Las filas válidas se guardan y las inválidas se informan con fila, campo y motivo. Si faltan columnas, se rechaza todo el archivo con un mensaje claro. |
| ¿Dónde y cómo guardan? | En SQLite, que viene con Python. El esquema está en `schema.sql`, con restricciones `NOT NULL` y `CHECK`. Guardamos dentro de una transacción: si algo falla, no queda nada a medias. |
| ¿Cómo evitan la inyección SQL? | Todas las consultas usan parámetros `?`. El único dato variable en el `ORDER BY` se toma de una lista fija de columnas permitidas. |
| ¿Cómo saben que los cálculos están bien? | Los calculamos a mano con un ejemplo y escribimos tests con pytest (`tests/test_procesamiento.py`). Además, GitHub Actions corre los tests en cada push. |
| ¿Por qué Flask y SQLite? | Son simples, no requieren instalar servidores y alcanzan de sobra para el volumen de datos de la consigna. |
| ¿Qué hace esta función? | Leer el docstring y explicar entrada → proceso → salida. |
| ¿Usaron IA? | Sí, como dice el punto 15 del reglamento: la usamos como asistente. Nosotros definimos el análisis, revisamos cada cambio, probamos y entendemos el código. |
| ¿Qué mejorarían con más tiempo? | Tener 2 o 3 ideas concretas (por ejemplo: usuarios y permisos, más reportes, gráficos comparativos). |

## Reglas para la defensa

- Responde quien hizo esa parte; los otros completan.
- Si no saben algo: "No lo sabemos con certeza; lo que hace es…" y abrir el archivo. Nunca inventar.
- Tener el sistema **ya abierto** y con datos cargados antes de que llegue el jurado.
- Tener el repositorio de GitHub abierto en otra pestaña (commits, Actions en verde, README).
