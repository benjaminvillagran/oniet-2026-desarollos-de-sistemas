# 03 · Plan del día de la competencia

Horario oficial: **14:00 a 16:30** (2 h 30 min). Nuestro plan termina a las **16:05** y deja
**25 minutos de margen**. Si la organización confirma otro horario, se corre todo igual.

## Reglas de oro

1. **Primero que funcione de punta a punta** (leer → procesar → guardar → mostrar); después, lindo.
2. **15:50: congelamiento.** No se agregan funciones nuevas; solo se arreglan errores.
3. **Commit y push cada 15 a 20 minutos**, y siempre antes de pedirle a la IA un cambio grande.
4. **Último push a las 16:05, límite 16:15.** Ningún commit después de las 16:30: la hora del
   último commit es la hora de entrega.
5. Un pedido chico por prompt, nombrando el archivo y qué significa "terminado".
6. La IA no reescribe lo que ya anda: "modificá solo X".
7. Nada entra sin probarlo (`python herramientas/verificar.py`) y sin que alguien lo entienda.
8. Si la IA falla 2 veces seguidas en lo mismo: `/clear` (contexto limpio) y reformular el pedido.
9. Cada requisito de la consigna tiene que verse en pantalla, con el mismo nombre que en la consigna.
10. Anotar el uso de IA en `docs/USO_IA.md` (1 línea por tarea importante).

## Roles y herramientas

| Persona | Rol | Archivos propios (evita conflictos) | IA |
|---|---|---|---|
| **A** (líder técnico) | Integración, base de datos, validación, procesamiento; resuelve conflictos de git | `app/schema.sql`, `app/servicios/`, `app/repositorios/`, `app/rutas/`, `app/config.py` | Claude Code + **Ollama DeepSeek** (volumen de código) · Claude Code **Claude Pro** (análisis, bugs difíciles, revisión final) · Antigravity (reserva) |
| **B** | Interfaz y usabilidad | `app/templates/`, `app/static/` | **Antigravity**: Gemini 3.8 Flash (cambios rápidos) · Claude Sonnet 4.6 (páginas complejas) · navegador para ver cómo queda |
| **C** | Datos, pruebas y documentación | `tests/`, `data/`, `README.md`, `docs/ANALISIS.md`, `docs/USO_IA.md` | **Antigravity**: Claude Sonnet 4.6 o Gemini 3.1 Pro (tests y README) · agente de navegador (`/probar-en-navegador`) |

Cada uno usa **su propia cuenta** de cada herramienta. No se comparten cuentas ni claves: los
términos de Anthropic y de Ollama lo piden ("una cuenta por persona").

## Antes de las 14:00 (llegar 13:15)

- [ ] Notebooks cargadas, cargadores y zapatilla. Celular con datos para hotspot de emergencia.
- [ ] Conectarse al Wi-Fi y correr `python herramientas/diagnostico.py --rol A|B|C`: todo OK.
- [ ] Reloj de la notebook sincronizado (lo revisa el diagnóstico).
- [ ] Repositorio de entrega creado, los 3 como colaboradores y clonado en las 3 notebooks.
- [ ] `python herramientas/verificar.py`: todo OK. `python run.py` abre el sistema.
- [ ] Claude Code abierto con Claude Pro (A); `/usage` para ver el cupo disponible.
- [ ] Ollama con sesión iniciada (A): `ollama launch claude --model deepseek-v4.1-flash:cloud`.
- [ ] Antigravity abierto en el repositorio con sesión iniciada (A, B, C); revisar **View Usage**.
- [ ] Tener abiertas: consigna, `docs/03_PLAN_DEL_DIA.md`, `docs/04_IAS_Y_PROMPTS.md`.

## Cronograma

| Hora | A (líder) | B (interfaz) | C (datos y pruebas) | Control |
|---|---|---|---|---|
| **14:00–14:15** | Lee la consigna en voz alta. `/analizar-consigna` con Claude Pro | Lee la consigna. Anota pantallas y textos que pide | Abre los archivos de datos: columnas, formatos, errores. Calcula **a mano** 2 o 3 resultados esperados | `docs/ANALISIS.md` listo y acordado por los 3 → **commit** |
| **14:15–14:25** | Escribe en `procesamiento.py` los nombres de las funciones (con docstring) para que C pueda testearlas | Cambia nombre del sistema, menú y títulos de páginas | Copia los datos a `data/ejemplos/` y arma `docs/USO_IA.md` | **commit + push** |
| **14:25–14:50** | `schema.sql` + `validacion.py` (DeepSeek). Reiniciar la base e importar | Adapta `importar.html` y el listado a las nuevas columnas | Tests de validación con filas buenas y malas | **14:50: se importa el archivo real** → commit |
| **14:50–15:15** | `procesamiento.py`, repositorio y servicios | Pantalla de resultados / estadísticas (tablas, KPIs) | Tests de procesamiento con los resultados calculados a mano | **15:15: MVP de punta a punta** → commit. Si no llega: recortar alcance |
| **15:15–15:40** | Filtros, alta manual y lo que falte de la consigna. Integra y resuelve conflictos | Gráficos, estados vacíos, mensajes, formato de números y fechas | `/probar-en-navegador` y reporta fallas a A y B. Borrador del README | commit cada 15 min |
| **15:40–15:50** | `/revisar-rubrica` con Claude Pro. Reparte las 3 mejoras más valiosas | Arregla lo que le toque | Arregla lo que le toque | — |
| **15:50** | **CONGELAMIENTO: solo errores** | | | commit + push |
| **15:50–16:00** | `/verificar` y arreglos | Pulido visual chico | README final (sin "COMPLETAR"), `docs/USO_IA.md` | — |
| **16:00–16:05** | `/entrega-final`: commit, tag `entrega-final`, push | Revisa GitHub en el navegador | Carga el link en el Sistema ONIET | **ENTREGADO** |
| **16:05–16:30** | **MARGEN.** Solo un error grave (push antes de 16:15). Ensayo de la demo | Ensayo | Ensayo | Nada después de 16:15 |

## Puntos de control (si no se cumplen, recortar)

- **14:50**: ¿se importa el archivo de la consigna y se guarda? Si no, A y C se concentran en eso.
- **15:15**: ¿hay un recorrido completo que funciona (importar → ver resultados)? Si no, **se
  abandona todo lo "deseable"** y se trabaja solo en el mínimo del análisis.
- **15:40**: lo que no esté andando a esta hora se saca de la interfaz (mejor no mostrarlo que
  mostrarlo roto) y se anota en "Limitaciones conocidas" del README.

## Planes B

| Problema | Qué hacemos |
|---|---|
| Se termina el cupo de Claude Pro | Seguir con DeepSeek (Ollama) o con Claude Opus/Sonnet 4.6 en Antigravity |
| Ollama no responde | Antigravity (A también lo tiene) |
| Se termina el cupo de Antigravity en un modelo | Cambiar al otro grupo de modelos (Gemini ↔ Claude/GPT tienen cupos separados) |
| Se cae el Wi-Fi | Hotspot del celular. El sistema funciona sin internet; los commits se hacen igual y se pushean al volver la conexión |
| Se rompe algo y no sabemos por qué | Volver al último commit que andaba (ver `06_GIT.md`, "Emergencias") |
| Conflicto de git | Lo resuelve A. Nunca `--force` |
| Se apaga una notebook | El código está en GitHub (por eso push seguido): seguir en otra |
| La IA inventa una librería | No se instala nada fuera de `requirements.txt` |
