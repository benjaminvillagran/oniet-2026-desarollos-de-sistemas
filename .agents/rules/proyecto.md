---
trigger: always_on
description: Reglas generales del proyecto ONIET (Flask + SQLite)
---

# Reglas del proyecto

Las reglas completas están en `AGENTS.md`, en la raíz del repositorio. Leelo antes de cambiar código.
Resumen de lo más importante:

- Stack fijo: Python + Flask + SQLite (`sqlite3`, sin ORM) + Jinja2 + CSS propio. No agregar
  dependencias ni frameworks.
- Capas: `app/rutas/` (sin lógica) → `app/servicios/` (leer, validar, procesar) →
  `app/repositorios/` (solo SQL con `?`, sin commit) → `app/db.py`.
- Interfaz: cada página extiende `base.html` y usa las clases de `app/static/css/estilos.css`
  (`tarjeta`, `tabla`, `boton`, `alerta--*`, `vacio`, `kpi`). Nada de Bootstrap ni Tailwind.
- Todo en español. Mensajes claros para el usuario, nunca errores internos.
- Antes de decir "terminado": `python herramientas/verificar.py --arreglar` tiene que dar todo OK.
- Nunca borrar ni saltear tests. Nunca `git push --force`.
- El sistema corre con `python run.py` en http://127.0.0.1:5000.
