@AGENTS.md

## Notas solo para Claude Code

- Las reglas del proyecto están en AGENTS.md (importado arriba). Aplican igual con Claude Pro
  y con Ollama/DeepSeek (`ollama launch claude --model deepseek-v4.1-flash:cloud`).
- Cupo limitado con Claude Pro: respuestas concisas y no releer todo el repositorio sin necesidad;
  usá el mapa de carpetas de AGENTS.md para ir directo al archivo.
- Con Claude Pro: `/model sonnet` para tareas comunes; Opus solo para analizar la consigna o
  resolver bugs difíciles. `/clear` entre tareas distintas y `/usage` para ver el cupo.
- Skills del proyecto: `.claude/skills/` (Antigravity usa la misma copia en `.agents/skills/`).
  Si cambiás una skill, corré `python herramientas/sincronizar_skills.py`.
