# 09 · Problemas comunes y cómo resolverlos

Primero correr `python herramientas/diagnostico.py --rol A|B|C` y
`python herramientas/verificar.py`: casi siempre dicen dónde está el problema.

## Python y el entorno

| Síntoma | Solución |
|---|---|
| `python` abre la Microsoft Store o dice "Python was not found" | *Configuración → Aplicaciones → Configuración avanzada → Alias de ejecución de aplicaciones*: desactivar `python.exe` y `python3.exe`. O usar `py` en lugar de `python` |
| `python` no se reconoce | Reinstalar Python tildando "Add python.exe to PATH" (el instalador tiene la opción *Modify*). Mientras tanto, usar `py` |
| "running scripts is disabled on this system" al activar `.venv` | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, o usar la terminal **cmd**, o no activar y correr `.venv\Scripts\python.exe run.py` |
| `ModuleNotFoundError: No module named 'flask'` | El entorno no está activado o faltan paquetes: `iniciar.bat`, o `.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` |
| `iniciar.bat` falla a la mitad | Volver a ejecutarlo: si el `.venv` quedó incompleto, lo borra y lo crea de nuevo |
| "Windows protegió su PC" al abrir un `.bat` | *Más información → Ejecutar de todas formas*, o *Propiedades → Desbloquear* |
| No hay internet para `pip install` | Usar la carpeta `wheels/` del pendrive (ver `02_CONFIGURAR_NOTEBOOK.md`); `iniciar.bat` la usa sola |

## El sistema

| Síntoma | Solución |
|---|---|
| `Address already in use`, `WinError 10013` o `10048` | El puerto 5000 está ocupado: cerrar la otra ventana del servidor, o `set PORT=5001` y volver a iniciar. Ver quién lo usa: `netstat -ano \| findstr :5000` |
| Aviso del Firewall de Windows al iniciar | "Cancelar" alcanza: el sistema solo escucha en 127.0.0.1 |
| `sqlite3.OperationalError: no such column / no such table` | La base tiene el esquema viejo: `flask --app run reiniciar-db` (o borrar `instance/datos.db`) |
| Los cambios no se ven en el navegador | Guardar el archivo; el servidor en modo debug se recarga solo. Si no, Ctrl+C y `python run.py`. Para CSS: `Ctrl+F5` |
| `jinja2.exceptions.UndefinedError` | La plantilla usa una variable que la ruta no le pasa: revisar el `render_template(...)` |
| `werkzeug.routing.BuildError` | Un `url_for('...')` apunta a una ruta que se renombró: buscar el nombre viejo en `templates/` |
| "Faltan columnas obligatorias" al importar | Los encabezados del archivo no coinciden: agregar el nombre a `ALIAS` en `validacion.py` |
| Acentos raros (Ã©) al importar | El lector ya prueba UTF-8 y cp1252; si persiste, guardar el CSV como "UTF-8" desde Excel |
| Números mal leídos (1.500 → 1,5) | El archivo usa punto de miles sin coma decimal: ajustar `a_decimal` y agregar un test con ese caso |
| Error 500 | Mirar la terminal donde corre el servidor: ahí está el error completo. Copiarlo entero a la IA (prompt 6 de `04_IAS_Y_PROMPTS.md`) |

## Git y GitHub

| Síntoma | Solución |
|---|---|
| `rejected ... (fetch first)` al hacer push | Alguien pusheó antes: `git pull` y después `git push` |
| `fatal: Need to specify how to reconcile divergent branches` | `git config pull.rebase false` y repetir `git pull` |
| Conflicto (`<<<<<<<` en un archivo) | Ver "Conflictos" en `06_GIT.md`. Si no se entiende: `git merge --abort` y avisar a A |
| `Permission denied` / 403 al hacer push | La invitación de colaborador no se aceptó, o se inició sesión con otra cuenta. Revisar en GitHub |
| Los commits no aparecen con mi usuario | El `user.email` de git no es el de la cuenta de GitHub: `git config --global user.email "mail-de-github"` |
| La hora del commit está mal | Sincronizar el reloj de Windows (*Fecha y hora → Sincronizar ahora*). Revisar con `git log -1 --format=fuller` |
| "LF will be replaced by CRLF" | Es solo un aviso, no hay que hacer nada |
| El workflow de Actions está en rojo | Abrir la pestaña **Actions**, entrar a la ejecución y leer el paso que falló. En la notebook: `python herramientas/verificar.py --arreglar` |

## Las IAs

| Síntoma | Solución |
|---|---|
| Claude Code: "claude no se reconoce" | Agregar `%USERPROFILE%\.local\bin` al PATH del usuario y abrir una terminal nueva |
| Claude Code no usa la cuenta Pro | Hay variables `ANTHROPIC_*` configuradas. En una ventana nueva: `Remove-Item Env:ANTHROPIC_AUTH_TOKEN, Env:ANTHROPIC_BASE_URL, Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue` y `claude`; `/status` para confirmar |
| Claude Code en la terminal de Antigravity entra en bucle ("Error installing VS Code extension") | Usarlo en una ventana de PowerShell o Windows Terminal aparte |
| Se terminó el cupo de Claude Pro | Seguir con DeepSeek (`ollama launch claude ...`) o con Claude Sonnet 4.6 en Antigravity |
| Ollama: error de modelo o de sesión | `ollama signin` de nuevo; probar `ollama run deepseek-v4.1-flash:cloud`. Revisar el cupo en ollama.com/settings/usage |
| Antigravity: Gemini lento o error 503 | Cambiar a Gemini 3.7 Flash; si sigue, Claude Sonnet 4.6 (otro cupo) |
| Antigravity: "Agent execution terminated due to error" o sesión trabada | Cerrar sesión, esperar 30 segundos, volver a entrar. Si no, cerrar la app, esperar 15 segundos y reabrir |
| Antigravity: el agente queda en "Running…" | Cancelar. Si estaba iniciando el servidor, levantarlo a mano en tu terminal |
| Antigravity: "Failed to install playwright: $HOME is not set" | Crear la variable de usuario `HOME=%USERPROFILE%` y reiniciar |
| Antigravity: el navegador abre Edge en vez de Chrome | Instalar Chrome y ponerlo como navegador predeterminado |
| La IA entra en bucle o empeora las cosas | Cancelar, `/rewind` (Claude Code) o `git restore .`, `/clear` y pedir algo más chico |
| La IA quiere instalar una librería nueva | No. Pedir que lo resuelva con lo que hay en `requirements.txt` |
