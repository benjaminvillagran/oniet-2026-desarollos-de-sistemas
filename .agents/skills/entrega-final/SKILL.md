---
name: entrega-final
description: Guía la entrega final del repositorio (verificación, README, commit, tag y push) antes del cierre de ONIET. Usar solo cuando el equipo lo pide explícitamente, entre las 16:00 y las 16:15.
disable-model-invocation: true
---

# Entrega final

Regla de oro: **la hora del último commit es la hora de entrega**. El último push tiene que estar
hecho antes de las 16:15 (cierre oficial: 16:30). Después de eso no se hacen más commits.

1. `python herramientas/verificar.py --arreglar`: todo en `[ OK  ]`. Si hay una falla que no se
   arregla en 5 minutos, se deja como está y se anota en el README como "limitación conocida".
2. README (usar `docs/plantillas/README_ENTREGA.md`): sin textos "COMPLETAR", con integrantes, qué
   resuelve, cómo instalar y ejecutar, funcionalidades, decisiones tomadas y limitaciones.
3. Revisar que no se suban archivos que no van: `git status` sin `.venv/`, `instance/` ni `*.db`.
4. Commit final: `git add -A` y `git commit -m "docs: entrega final ONIET 2026"`.
5. Tag: `git tag -a entrega-final -m "Entrega ONIET 2026"`.
6. Push: `git push` y `git push origin entrega-final`.
7. Abrir el repositorio en GitHub desde el navegador y confirmar que se ven el último commit, el
   README y la pestaña Actions en verde.
8. Cargar el link del repositorio donde indique la organización (Sistema ONIET).
