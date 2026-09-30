# Kit ONIET 2026 · Desarrollo de Sistemas

[![Verificación](https://github.com/benjaminvillagran/oniet-2026-desarollos-de-sistemas/actions/workflows/verificacion.yml/badge.svg)](https://github.com/benjaminvillagran/oniet-2026-desarollos-de-sistemas/actions/workflows/verificacion.yml)

Todo lo que un equipo de 3 necesita para la competencia **ONIET 2026 · Desarrollo de Sistemas**
(resolver una consigna con un sistema web que **lee datos, los procesa, los almacena y muestra
resultados** en 2 h 30 min, con ayuda de IA):

- **Una plantilla web funcionando** (Python + Flask + SQLite), probada con más de 100 tests automáticos, que ya
  resuelve de punta a punta un problema de ejemplo y se adapta a la consigna real.
- **Configuración para 3 IAs** (Claude Code con Claude Pro, Claude Code con Ollama/DeepSeek y
  Google Antigravity): reglas comunes y 6 skills del proyecto validadas contra la especificación
  oficial.
- **Guías** del reglamento, plan del día minuto a minuto, git, prompts, simulacros con soluciones
  y defensa ante el jurado.
- **Verificación automática**: script local y workflow de GitHub Actions en Windows y Linux.

## ⚠️ Urgente, antes de la competencia (2 al 9 de octubre)

1. **Confirmar con la organización** (competencias.oniet@ubp.edu.ar u oniet@ubp.edu.ar) si se
   pueden usar notebooks propias, IA y una plantilla preparada. Borrador del mail en
   [`docs/02_CONFIGURAR_NOTEBOOK.md`](docs/02_CONFIGURAR_NOTEBOOK.md).
2. **Configurar las 3 notebooks** y correr `python herramientas/diagnostico.py --rol A|B|C`.
3. **Hacer al menos 2 simulacros** completos con reloj ([`docs/07_PRACTICA.md`](docs/07_PRACTICA.md)).
4. **No gastar el cupo semanal de Antigravity** los días previos.

## Por dónde empezar

| # | Documento | Para qué | Quién |
|---|---|---|---|
| 1 | [Reglamento y rúbrica](docs/01_REGLAMENTO_Y_RUBRICA.md) | Qué se evalúa y checklist de 100 puntos | Todos |
| 2 | [Configurar la notebook](docs/02_CONFIGURAR_NOTEBOOK.md) | Instalar y probar todo en casa | Todos |
| 3 | [Plan del día](docs/03_PLAN_DEL_DIA.md) | Cronograma 14:00–16:30, roles, puntos de control, planes B | Todos |
| 4 | [IAs y prompts](docs/04_IAS_Y_PROMPTS.md) | Qué IA usar para qué y prompts listos | Todos |
| 5 | [Adaptar la plantilla](docs/05_ADAPTAR_PLANTILLA.md) | Pasar del ejemplo al problema real | A |
| 6 | [Git y GitHub](docs/06_GIT.md) | Trabajo en equipo, conflictos, emergencias, entrega | Todos |
| 7 | [Práctica](docs/07_PRACTICA.md) | 5 simulacros (2 al estilo de consignas reales) | Todos |
| 8 | [Defensa ante el jurado](docs/08_DEFENSA_JURADO.md) | Demo de 3 minutos y preguntas probables | Todos |
| 9 | [Problemas comunes](docs/09_PROBLEMAS_COMUNES.md) | Síntoma → solución | Todos |

Plantillas para el día: [análisis de la consigna](docs/plantillas/ANALISIS_CONSIGNA.md),
[README de entrega](docs/plantillas/README_ENTREGA.md),
[registro de uso de IA](docs/plantillas/USO_IA.md) y
[configuración de Claude Code](docs/plantillas/claude_settings.json) (opcional).

## Cómo ejecutarlo

Requisito: Python 3.10 o superior.

**Windows**: doble clic en `iniciar.bat` (crea el entorno, instala y levanta el sistema).
**Linux/Mac**: `./iniciar.sh`. A mano:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     Linux/Mac: source .venv/bin/activate
pip install -r requirements-dev.txt
python run.py
```

Abrir http://127.0.0.1:5000 e importar `data/ejemplos/ventas_ejemplo.csv`.
Antes de cada push: `verificar.bat` (o `python herramientas/verificar.py --arreglar`).

## Funcionalidades de la plantilla

| Rúbrica | Qué trae |
|---|---|
| Lectura de datos | Importa CSV, TXT, JSON y Excel, o desde una URL/API. Detecta separador (`;` `,` tab `\|`), codificación (UTF-8, BOM, cp1252 de Excel) y encabezados con acentos o camelCase. Alta manual con formulario |
| Procesamiento | Validación fila por fila con fila, campo y motivo; números y fechas en formato argentino; normalización; cálculos por fila; estadísticas, agrupaciones, porcentajes y rankings |
| Almacenamiento | SQLite con restricciones y transacciones; historial de importaciones; detección de archivos repetidos |
| Resultados | Listado con búsqueda, filtros, orden, paginación y fila de totales; detalle; edición y baja; estadísticas con gráficos; exportación CSV; API JSON |
| Usabilidad | Diseño propio y responsive, mensajes claros, estados vacíos, confirmación antes de borrar, páginas de error propias; gráficos sin depender de internet |
| Extras | Login opcional (`LOGIN_OBLIGATORIO`) con claves con hash y último acceso |

## Estructura

```
app/
  rutas/          páginas (sin lógica)
  servicios/      lector → validacion → procesamiento, y los servicios que coordinan
  repositorios/   SQL parametrizado (sin commit)
  utils/          conversiones (texto → número/fecha) y formato para mostrar
  templates/      HTML (Jinja2)        static/  CSS, JS y Chart.js local
  schema.sql      tablas               config.py  nombre del sistema, login, límites
data/ejemplos/    datos del ejemplo    data/practica/  datos de los simulacros
docs/             guías y plantillas
herramientas/     verificar.py, diagnostico.py, empaquetar_contexto.py, sincronizar_skills.py
tests/            más de 100 tests (pytest)
.github/workflows verificación en Windows y Linux en cada push
AGENTS.md         reglas para todas las IAs      CLAUDE.md  importa AGENTS.md
.claude/skills/   skills del proyecto (copia para Antigravity en .agents/skills/)
```

## Calidad y verificación

- `python herramientas/verificar.py --arreglar`: tests, estilo (ruff), que el sistema arranque y
  responda en todas sus páginas, README y commits pendientes.
- `python herramientas/diagnostico.py --rol A`: Python, paquetes, git, **permiso de push**, **reloj
  en hora** (la hora del commit es la hora de entrega), conexión, puerto y herramientas de IA.
- **GitHub Actions** (`.github/workflows/verificacion.yml`): en cada push corre ruff, pytest y el
  verificador en Windows (Python 3.12) y Ubuntu (3.10 y 3.13), y además prueba `iniciar.bat` y
  `verificar.bat` en Windows.

## Uso de inteligencia artificial

- [`AGENTS.md`](AGENTS.md) es la **fuente única de reglas** (stack, capas, convenciones, interfaz,
  tests, git). Claude Code la carga desde [`CLAUDE.md`](CLAUDE.md) (`@AGENTS.md`); Antigravity la
  lee directo y además [`.agents/rules/proyecto.md`](.agents/rules/proyecto.md).
- **Skills** (formato oficial `SKILL.md`, validadas por `tests/test_config_ia.py`):

  | Skill | Cuándo |
  |---|---|
  | `/analizar-consigna` | 14:00: de la consigna a un plan |
  | `/adaptar-plantilla` | Pasar del ejemplo de ventas al problema real |
  | `/verificar` | Antes de cada push |
  | `/probar-en-navegador` | Probar como el jurado |
  | `/revisar-rubrica` | 15:40: qué falta para sumar puntos |
  | `/entrega-final` | 16:00: entrega (solo manual) |

- Uso responsable (punto 15 del reglamento): se declara en el README de entrega y en
  `docs/USO_IA.md`; el equipo revisa, prueba y entiende todo el código.

## Tecnologías y licencias

Python, [Flask](https://flask.palletsprojects.com/) (BSD-3), SQLite, Jinja2,
[openpyxl](https://openpyxl.readthedocs.io/) (MIT), [Chart.js 4.4.4](https://www.chartjs.org/)
(MIT, incluido en `app/static/vendor/chartjs/` con su licencia), pytest y ruff.
