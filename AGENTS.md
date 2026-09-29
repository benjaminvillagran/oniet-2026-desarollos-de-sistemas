# AGENTS.md — Reglas del proyecto para agentes de IA

Este archivo es la **fuente única de reglas** para cualquier IA que trabaje en el repositorio
(Claude Code con Claude Pro, Claude Code con Ollama/DeepSeek y Google Antigravity).

## Contexto

- Competencia **ONIET 2026 · Desarrollo de Sistemas**: 2 h 30 min para resolver una consigna con un
  **sistema web que lee datos, los procesa, los almacena y muestra resultados**.
- Equipo de 3 estudiantes con poca experiencia en programación: el código tiene que ser **simple,
  claro y explicable** frente al jurado.
- Rúbrica: comprensión de la consigna 10 · procesamiento de datos 25 · funcionamiento integral 25 ·
  calidad del código 15 · interfaz y usabilidad 15 · entrega y versionado 10.
- Prioridad: **que funcione con datos reales** > que el código sea claro > que se vea lindo > extras.

## Comandos

| Para qué | Comando |
|---|---|
| Instalar (primera vez) | `python -m venv .venv`, activar el entorno y `pip install -r requirements-dev.txt` |
| Ejecutar | `python run.py` → http://127.0.0.1:5000 (otro puerto: variable de entorno `PORT=5001`) |
| Tests | `python -m pytest` |
| Verificar todo antes de un push | `python herramientas/verificar.py --arreglar` |
| Reiniciar la base (después de cambiar `schema.sql`) | `flask --app run reiniciar-db` |

## Stack (no cambiar sin que el equipo lo pida)

Python 3.10+, Flask 3, SQLite con `sqlite3` de la librería estándar (sin ORM), plantillas Jinja2,
CSS propio en `app/static/css/estilos.css`, Chart.js local en `app/static/vendor/`.
**No agregar dependencias ni frameworks** (React, Bootstrap, SQLAlchemy, etc.).

## Arquitectura en capas

`rutas/` → `servicios/` → `repositorios/` → `db.py`

| Carpeta | Responsabilidad | Regla |
|---|---|---|
| `app/rutas/` | Recibir el pedido HTTP y devolver la página | Sin lógica: leer `request`, llamar a un servicio, `render_template`/`redirect` |
| `app/servicios/lector.py` | LEER archivos CSV/TXT/JSON/XLSX | Genérico: casi nunca hay que tocarlo |
| `app/servicios/validacion.py` | VALIDAR cada fila (columnas, alias, reglas) | Devuelve errores con fila, campo y motivo |
| `app/servicios/procesamiento.py` | PROCESAR: cálculos y estadísticas | Funciones puras (sin base de datos), con tests |
| `app/servicios/*_servicio.py` | Coordinar el recorrido y las transacciones | Usan `with transaccion():` para escribir |
| `app/repositorios/` | GUARDAR y consultar (solo SQL) | Siempre parámetros `?`; **no hacen commit** |
| `app/utils/conversiones.py` | Pasar texto a número/fecha (`a_decimal`, `a_entero`, `a_fecha`) | Lanzan `ValueError` con mensaje en español |
| `app/utils/formato.py` | Formato argentino para mostrar | Filtros Jinja: `moneda`, `numero`, `fecha`, `mes`, `porcentaje` |
| `app/templates/` | Páginas HTML | Todas extienden `base.html` |
| `tests/` | Pruebas con pytest | Un archivo por módulo |

## Adaptar la plantilla a la consigna (en este orden)

La plantilla trae un ejemplo completo de **ventas**. Para el problema real:

1. `app/schema.sql`: tablas y columnas del problema.
2. `app/servicios/validacion.py`: `COLUMNAS`, `ALIAS` y reglas de `validar_*`.
3. `app/servicios/procesamiento.py`: los cálculos que pide la consigna, con tests.
4. `app/repositorios/`: consultas SQL de las nuevas columnas y filtros.
5. `app/servicios/*_servicio.py` y `app/rutas/`: conectar todo.
6. `app/templates/` y el menú de `base.html`.
7. `data/ejemplos/`: poner los archivos de datos de la consigna.
8. `app/config.py`: `NOMBRE_SISTEMA` y `NOMBRE_EQUIPO`.
9. Actualizar los tests y correr `python herramientas/verificar.py --arreglar`.

Para una entidad nueva, **copiar el patrón de ventas** (repositorio + servicio + rutas + plantillas +
tests) en archivos nuevos. Después de cambiar `schema.sql`, reiniciar la base.

## Convenciones de código

- Todo en **español**: nombres en `snake_case` descriptivos, docstrings breves, type hints.
- Funciones cortas con una sola responsabilidad. Nada de código duplicado: reutilizar lo existente.
- Mensajes al usuario en español rioplatense, claros y sin tecnicismos. Nunca mostrar errores internos.
- Datos inválidos **nunca** rompen el sistema: se validan y se informa fila, campo y motivo.
- SQL con f-strings **solo** para nombres de columna tomados de una lista fija (ver `listar_pagina`).

## Interfaz

- Cada página nueva extiende `base.html` y tiene su link en el menú.
- Usar las clases existentes: `tarjeta`, `grilla-2`, `grilla-kpi` + macro `kpi`, `tabla` dentro de
  `tabla-contenedor`, `boton` (`--secundario`, `--peligro`, `--chico`), `formulario` / `campo` /
  `mensaje-error`, `alerta--exito|error|aviso|info`, `vacio`, `etiqueta`, `barra`.
- Siempre: estado vacío ("todavía no hay datos"), mensajes `flash`, y `data-confirmar` en formularios
  que borran.
- Números con `| moneda` o `| numero`, fechas con `| fecha`.

## Tests y verificación

- Toda función nueva de validación o procesamiento lleva su test en `tests/`.
- Antes de decir "terminado": `python herramientas/verificar.py --arreglar` tiene que dar todo OK.
- **Prohibido** borrar, saltear o debilitar tests para que pasen: se arregla el código.

## Git

- Commits chicos y frecuentes en español con Conventional Commits: `feat:`, `fix:`, `test:`,
  `docs:`, `style:`, `refactor:`.
- Hacer commit o push **solo cuando la persona lo pide**.
- Nunca `git push --force`, nunca reescribir historia, nunca commitear `.venv/`, `instance/` ni `*.db`.

## Forma de trabajar

- Respondé siempre en español.
- Antes de un cambio grande, explicá el plan en 3 a 5 líneas.
- Hacé cambios mínimos y enfocados en lo pedido. No reescribas archivos enteros sin necesidad.
- Al terminar, listá los archivos cambiados y explicá en 2 o 3 líneas qué hace el cambio: el equipo
  tiene que poder explicárselo al jurado.
- Si la consigna es ambigua, preguntá en vez de inventar.
- Reglamento ONIET: no copiar código de terceros. Escribí código propio; las librerías de
  `requirements.txt` están permitidas.
