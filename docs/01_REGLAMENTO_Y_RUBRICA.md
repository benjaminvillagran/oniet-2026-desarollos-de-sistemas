# 01 · Reglamento y rúbrica (resumen accionable)

Fuente: reglamento oficial *012 Desarrollo de Sistemas 2026* (ONIET · Universidad Blas Pascal).
Ante cualquier duda manda el reglamento original y lo que diga la organización.

> 📅 **ONIET 2026 (30.ª edición): del 2 al 9 de octubre de 2026** en el campus de la UBP, según la
> web de la UBP. El cronograma de ONIET ubica "Desarrollo de Sistemas" a las 14 h; confirmar el día.
>
> ⚠️ **Confirmar ya con la organización** (competencias.oniet@ubp.edu.ar u oniet@ubp.edu.ar):
> la página de la competencia dice que se rinde "en computadoras provistas por la Universidad" y
> menciona una duración de unas 4 horas. Nuestro plan asume notebooks propias y 14:00–16:30.
> Si no se permiten notebooks, ver "Plan B" en `04_IAS_Y_PROMPTS.md`.

## Lo que dice el reglamento y qué hacemos al respecto

| Regla | Qué hacemos |
|---|---|
| Resolver una consigna con un **sistema web que lea datos, los procese, los almacene y muestre resultados** | La plantilla ya tiene las 4 partes: importar (CSV/JSON/Excel) → validar y calcular → SQLite → listados, estadísticas y gráficos |
| Lenguajes: Java, JavaScript, PHP, Python, .NET | Python + Flask |
| Grupal, hasta 4 integrantes | Somos 3, con roles definidos (ver `03_PLAN_DEL_DIA.md`) |
| Entrega mediante un **repositorio**; **la fecha y hora del último commit es el momento de entrega** | Commits frecuentes; **último push antes de las 16:15**; ningún commit después de las 16:30 |
| Docentes resuelven dudas técnicas, pero no dicen cómo resolver | Preguntar dudas de la consigna temprano (lista del análisis) |
| Internet permitido para consultas técnicas, **sin copiar código de terceros sin autorización** | Código propio. Solo librerías declaradas (Flask, openpyxl, Chart.js) |
| IA permitida con **uso responsable**: no vulnerar autoría, transparencia, seguridad ni condiciones | Decimos que usamos IA, entendemos y podemos explicar cada parte del código |
| Presencial, en el laboratorio de la UBP | Llevamos nuestras notebooks: **confirmarlo por escrito con la organización** (ver `02_CONFIGURAR_NOTEBOOK.md`) |

> ⚠️ **Plantilla preparada antes del día**: el reglamento no lo menciona. Antes de la competencia,
> preguntar por el canal oficial (mensajería del Sistema ONIET u oniet@ubp.edu.ar) si se puede traer
> una base de código propia. Si **no** se permite, se usa este repositorio como práctica: el mismo
> diseño se arma de cero el día de la competencia con las skills y prompts (por eso practicamos).
> Si **sí** se permite, se declara en el README de entrega. Transparencia ante todo.

## Rúbrica oficial (100 puntos) → checklist

### Comprensión de la consigna · 10

- [ ] Hicimos el análisis (`docs/ANALISIS.md`) antes de programar.
- [ ] El sistema resuelve **exactamente** lo que se pide (todos los requisitos de la consigna).
- [ ] Nombres de pantallas, tablas y campos iguales a los de la consigna.
- [ ] El README explica qué problema resuelve y cómo cada requisito quedó cubierto.

### Procesamiento de datos · 25 (el más importante junto con funcionamiento)

- [ ] **Lectura**: se importa el archivo que da la consigna, tal como viene (formato, separador, acentos).
- [ ] **Validación**: filas con errores no rompen nada; se informa fila, campo y motivo.
- [ ] **Transformación**: normalización (mayúsculas, espacios, fechas) y campos calculados.
- [ ] **Almacenamiento**: SQLite con tablas bien definidas, restricciones (`NOT NULL`, `CHECK`) y transacciones.
- [ ] **Uso**: consultas con filtros, agrupaciones, totales, promedios, rankings.
- [ ] Cálculos verificados a mano y con tests.

### Funcionamiento integral · 25

- [ ] El sistema arranca con un solo comando (`python run.py` o `iniciar.bat`).
- [ ] Todas las funciones prometidas funcionan de punta a punta con los datos reales.
- [ ] Los resultados son **correctos** (comparados con un cálculo manual).
- [ ] No hay errores 500: probar datos vacíos, inválidos y repetidos.
- [ ] Probado con la skill `probar-en-navegador`.

### Calidad del código · 15

- [ ] Capas separadas (rutas / servicios / repositorios), sin código duplicado.
- [ ] Nombres claros en español, funciones cortas, docstrings.
- [ ] Tests pasando y estilo OK (`python herramientas/verificar.py`).
- [ ] Workflow de GitHub Actions en verde.
- [ ] Sin código muerto ni archivos basura (`.venv`, `.db`) en el repositorio.

### Interfaz y usabilidad · 15

- [ ] Menú claro, todas las pantallas accesibles.
- [ ] Resultados legibles: números con formato argentino, fechas `DD/MM/AAAA`, totales destacados.
- [ ] Mensajes de éxito/error, estados vacíos y confirmación antes de borrar.
- [ ] Gráficos o indicadores que resuman los resultados.
- [ ] Se ve bien en pantallas chicas.

### Entrega y versionado · 10

- [ ] Repositorio con commits frecuentes de **los 3 integrantes**, con mensajes claros (`feat:`, `fix:`...).
- [ ] README completo (sin "COMPLETAR").
- [ ] Último commit y push **antes del cierre**; tag `entrega-final`.
- [ ] Link cargado en el medio oficial (Sistema ONIET).

## Escala de valoración

| Puntaje | Nivel |
|---|---|
| 90 a 100 | Sobresaliente: cumple la consigna con alto nivel de precisión, calidad y autonomía |
| 75 a 89 | Muy bueno: resuelve la mayor parte con solidez y mínimos errores |
| 60 a 74 | Adecuado: cumple lo central con limitaciones |
| Menos de 60 | Insuficiente |

**Objetivo: 90+.** Procesamiento y funcionamiento suman 50 puntos: primero que los datos se lean,
se calculen y se muestren **bien**; después, lo demás.
