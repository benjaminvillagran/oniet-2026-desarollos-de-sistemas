# Registro de uso de IA

> Registro de uso de asistentes de IA (punto 15 del reglamento ONIET 2026).

| Hora | Persona | Herramienta y modelo | Qué le pedimos | Qué revisamos o corregimos nosotros |
|---|---|---|---|---|
| Previa | Damián | Antigravity (Gemini Flash / Claude Sonnet) | Configuración del entorno, pruebas de Git y verificación de la plantilla | Diagnóstico sin fallas y push de prueba |
| 15:50 | Benjamín | Claude (Claude Code) | Analizar la consigna y los datos; calcular aparte los resultados esperados de los 3 informes | Usamos esos números para controlar la pantalla |
| 15:55 | Benjamín | Claude Code con DeepSeek (Ollama) | Adaptar la plantilla | Se abrió en otra carpeta y buscaba el proyecto en todo el disco: lo cortamos |
| 16:00 | Benjamín | Claude (Claude Code) | Adaptar la plantilla de ventas a servicios logísticos: validación, costo total, 3 informes, período y tests | Importamos el CSV real (180 filas) y comparamos los 3 informes y el filtro 2024 con los resultados esperados |
| 16:15 | Benjamín | Claude (Claude Code) | Botones de acceso rápido por año en Informes | Lo pegamos nosotros, lo probamos en el navegador y verificar.py dio OK |

## Un caso donde la IA se equivocó y lo detectamos

- Qué pasó: la página de detalle de un registro daba error 500 (el filtro `| mes` de Jinja se aplicaba antes que el formato del período).
- Cómo lo detectamos: probando todas las páginas con los datos reales importados.
- Cómo lo corregimos: con paréntesis, para formatear primero el período y después aplicar el filtro.