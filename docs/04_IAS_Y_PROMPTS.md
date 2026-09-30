# 04 · Las IAs: qué usar, cómo y con qué prompts

Todas las IAs leen las mismas reglas: `AGENTS.md` (Claude Code lo importa desde `CLAUDE.md`;
Antigravity lo lee directo y además `.agents/rules/`). Las **skills** del proyecto están en
`.claude/skills/` y `.agents/skills/` (misma copia) y se invocan con `/nombre`.

## Qué IA para qué

| Herramienta | Quién | Para qué | Cupo |
|---|---|---|---|
| Claude Code + **Claude Pro** (Sonnet) | A | Analizar la consigna, bugs difíciles, revisión final contra la rúbrica | **Limitado** (ventana de 5 h + semanal, compartido con claude.ai) |
| Claude Code + **Ollama DeepSeek V4.1 Flash** | A | Volumen: modelo de datos, validación, repositorios, rutas, tests | Grande (plan Pro de Ollama: USD 60/mes, 3 pedidos a la vez) |
| **Antigravity** · Gemini 3.8/3.7 Flash | B, C (y A) | HTML/CSS, cambios rápidos, planes | Grupo "Gemini": límite de 5 h + **semanal** |
| **Antigravity** · Claude Sonnet 4.6 | B, C | Páginas complejas, tests, README; reserva si Gemini falla | Grupo "Claude y GPT": cupo aparte |
| **Antigravity** · Claude Opus 4.6 / Gemini 3.1 Pro | B, C | Solo un bug muy difícil | Gastan mucho cupo |
| Antigravity · agente de navegador | B, C | Probar el sistema como el jurado (`/probar-en-navegador`) | — |

Datos verificados que cambian cómo trabajamos:

- **Gemini 3.8 Flash** tiene reportes de lentitud y errores 503 entre las 13:00 y las 19:00
  (hora argentina), justo durante la competencia. Si tarda o falla: **Gemini 3.7 Flash**, y si
  sigue: **Claude Sonnet 4.6** (otro grupo de cupo).
- En Antigravity la cuota se consume por trabajo, no por mensaje: prompts vagos disparan decenas de
  acciones. **Pedidos concretos con `@archivo`** gastan mucho menos.
- Con Claude Pro, el modelo por defecto es Opus, que gasta cupo mucho más rápido: usar
  **`/model sonnet`** siempre, salvo el análisis de la consigna.
- En Claude Code con Ollama, `/model sonnet` u `opus` **siguen siendo DeepSeek** (Ollama los
  reemplaza). Ollama no guarda caché: usar `/clear` seguido para no reenviar todo el contexto.

## Cómo lanzar cada una (A)

Usar **ventanas de PowerShell o Windows Terminal separadas**, fuera de Antigravity: en Windows,
Claude Code dentro de la terminal de Antigravity entra en un bucle intentando instalar su extensión
(problema conocido, sin solución oficial).

**Ventana 1: Claude Pro** (análisis y revisión):

```
cd C:\ruta\al\proyecto
claude
```

Adentro: `/status` (cuenta Pro), `/model sonnet`, `/usage`.

**Ventana 2: DeepSeek por Ollama** (escribir código):

```
cd C:\ruta\al\proyecto
ollama launch claude --model deepseek-v4.1-flash:cloud
```

Adentro: `/status` (tiene que decir el modelo de Ollama).

**Regla: una sola IA edita por vez.** Si Claude Pro y DeepSeek editan los mismos archivos al mismo
tiempo, se pisan. DeepSeek escribe; Claude Pro analiza o revisa en **modo plan** (`Shift+Tab`
hasta "plan mode"). Commit antes de cambiar de una a otra.

## Comandos útiles de Claude Code

| Comando | Para qué |
|---|---|
| `/analizar-consigna`, `/adaptar-plantilla`, `/verificar`, `/probar-en-navegador`, `/revisar-rubrica`, `/entrega-final` | Skills del proyecto |
| `/clear` | Contexto limpio entre tareas distintas (ahorra cupo) |
| `/rewind` o `Esc` `Esc` | Deshacer lo que hizo la IA (no deshace comandos de terminal; **no reemplaza a git**) |
| `Shift+Tab` | Cambiar de modo: normal → aceptar ediciones → plan |
| `/usage`, `/status`, `/context` | Cupo, cuenta y modelo, contexto cargado |
| `@app/servicios/validacion.py` | Mencionar un archivo |
| `Alt+V` | Pegar una captura de pantalla (Windows) |

Opcional: copiar `docs/plantillas/claude_settings.json` a `.claude/settings.json` en la notebook.
Fija el modelo en Sonnet, permite correr tests y el verificador sin preguntar, y **bloquea**
`git push --force`, `git reset --hard` y borrados recursivos. Probarlo antes del día.

## Antigravity: configuración y uso (B y C)

1. Abrir la carpeta del proyecto (lee `AGENTS.md` y `.agents/rules/proyecto.md`).
2. Configuración segura: terminal en **Request Review**, nunca **Turbo**. Ver `02_CONFIGURAR_NOTEBOOK.md`.
3. El sistema lo levanta la persona en **su** terminal (`iniciar.bat`). Decirle al agente: *"el
   servidor ya corre en http://127.0.0.1:5000, no lo inicies"* (en Windows se queda colgado).
4. Para tareas grandes, `/plan` primero; para cambios chicos de HTML/CSS, directo.
5. Si se cuelga o entra en bucle: **Cancel**, chat nuevo, tarea más chica.
6. **Nunca aprobar** comandos con `rm`, `del`, `rmdir`, `git reset --hard` o `--force`.

## Reglas para pedirle cosas a cualquier IA

1. **Un pedido chico por vez**, con el archivo y qué significa "terminado".
2. **"Modificá solo X"**: que no reescriba lo que ya anda.
3. **Pedir verificación**: "después corré `python herramientas/verificar.py`".
4. Si falla 2 veces en lo mismo: `/clear` y reformular con más detalle (el error exacto, el archivo).
5. No aceptar librerías nuevas: todo con lo que está en `requirements.txt`.
6. Leer lo que cambió antes del commit: tenemos que poder explicarlo.

## Prompts listos para copiar

### 1. Analizar la consigna (A, Claude Pro, 14:00)

```
/analizar-consigna
La consigna está en docs/CONSIGNA.md y los datos en data/ejemplos/. Completá docs/ANALISIS.md.
```

### 2. Adaptar la plantilla (A, DeepSeek)

```
/adaptar-plantilla
Hacé solo los pasos 1 y 2 (schema.sql y validacion.py) según docs/ANALISIS.md.
Después corré python herramientas/verificar.py --arreglar y mostrame qué cambiaste.
```

### 3. Un cálculo de la consigna (A, DeepSeek)

```
En @app/servicios/procesamiento.py agregá una función que calcule <CÁLCULO> según la regla
<REGLA DE LA CONSIGNA>. Ejemplo hecho a mano: con <DATOS> el resultado es <RESULTADO>.
Agregá un test con ese ejemplo en tests/test_procesamiento.py. No toques otros archivos.
```

### 4. Una pantalla (B, Antigravity)

```
En @app/templates/estadisticas.html mostrá <QUÉ> como una tabla con la clase "tabla" y una
tarjeta "kpi" arriba con <INDICADOR>. Usá los filtros | moneda y | fecha. Seguí AGENTS.md.
No cambies archivos .py. El servidor ya corre en http://127.0.0.1:5000, no lo inicies.
Cuando termines, abrí esa página con el navegador y mostrame una captura.
```

### 5. Tests (C, Antigravity con Claude Sonnet 4.6)

```
Escribí tests en @tests/test_procesamiento.py para <FUNCIÓN> con estos casos calculados a mano:
<CASO 1 → RESULTADO>, <CASO 2 → RESULTADO>, lista vacía. No cambies el código de app/.
Corré python -m pytest tests/test_procesamiento.py y mostrame el resultado.
```

### 6. Arreglar un error

```
Al hacer <ACCIÓN> aparece este error:
<PEGAR EL ERROR COMPLETO>
Encontrá la causa, explicala en 2 líneas y arreglala con el cambio mínimo.
Después corré python herramientas/verificar.py.
```

### 7. Probar como el jurado (C)

```
/probar-en-navegador
El servidor ya corre en http://127.0.0.1:5000. Usá los archivos de data/ejemplos/.
```

### 8. Revisión final (A, Claude Pro, 15:40)

```
/revisar-rubrica
La consigna está en docs/CONSIGNA.md. Quedan 20 minutos de desarrollo.
```

### 9. Explicar el código para la defensa

```
Explicame en lenguaje simple, para contárselo a un jurado en 1 minuto, qué hace
@app/servicios/procesamiento.py y cómo sabemos que los cálculos están bien.
```

## Plan B: sin herramientas instaladas (PC del laboratorio)

Si no dejan usar las notebooks y en las PCs no se pueden instalar Claude Code ni Antigravity:

1. `python herramientas/empaquetar_contexto.py` → genera `contexto_ia.txt` con todo el código.
2. Pegarlo en un chat web (claude.ai, gemini.google.com) y pedir cambios **archivo por archivo**,
   con la función completa a reemplazar.
3. Pegar el cambio, `python herramientas/verificar.py`, commit.
