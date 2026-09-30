# NOMBRE DEL SISTEMA (COMPLETAR)

![Verificación](https://github.com/USUARIO/REPOSITORIO/actions/workflows/verificacion.yml/badge.svg)

Sistema web desarrollado para **ONIET 2026 · Desarrollo de Sistemas** por el equipo COMPLETAR
(escuela COMPLETAR).

| Integrante | Rol |
|---|---|
| COMPLETAR | Integración y procesamiento de datos |
| COMPLETAR | Interfaz y usabilidad |
| COMPLETAR | Pruebas, datos y documentación |

## Problema que resuelve

COMPLETAR: 3 a 5 líneas con el problema de la consigna y qué hace el sistema.

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Abrir http://127.0.0.1:5000. En Windows también se puede hacer doble clic en `iniciar.bat`.
Para probar: importar el archivo `data/ejemplos/COMPLETAR`.

## Funcionalidades

| Requisito de la consigna | Dónde se cumple |
|---|---|
| Lectura de datos: COMPLETAR | Pantalla *Importar* (`app/servicios/lector.py`, `validacion.py`) |
| Procesamiento: COMPLETAR | `app/servicios/procesamiento.py` |
| Almacenamiento | SQLite (`app/schema.sql`, `app/repositorios/`) |
| Resultados: COMPLETAR | Pantallas COMPLETAR |

## Cómo está hecho

- **Python + Flask + SQLite**: SQLite viene con Python, así que no hace falta instalar un servidor
  de base de datos.
- **Capas**: `rutas/` (páginas) → `servicios/` (leer, validar, procesar) → `repositorios/` (SQL).
- **Validación fila por fila**: los datos con errores no se guardan y se informa fila, campo y motivo.
- **Seguridad**: consultas SQL con parámetros (sin inyección SQL) y transacciones.
- **Calidad**: tests automáticos con pytest (`python -m pytest`) y workflow de GitHub Actions en
  cada push.

## Decisiones y supuestos

- COMPLETAR (por ejemplo: "si la fecha viene vacía, la fila se rechaza").

## Limitaciones conocidas

- COMPLETAR (o "ninguna conocida").

## Uso de inteligencia artificial

Usamos asistentes de IA (Claude Code, DeepSeek vía Ollama y Google Antigravity) como herramienta de
apoyo, de acuerdo con el punto 15 del reglamento. Todo el código fue revisado, probado y entendido
por el equipo.
