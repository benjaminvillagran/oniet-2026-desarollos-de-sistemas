# 02 · Configurar las notebooks (antes de la competencia)

Objetivo: que el día de la competencia **nada dependa de instalar algo**. Hacerlo en casa, en las
mismas notebooks que se llevan, y terminar corriendo:

```
python herramientas/diagnostico.py --rol A      (o B, o C)
```

hasta que no quede ninguna `[FALLA]`.

> Comandos verificados con la documentación oficial (Python, PowerShell, Git, Claude Code, Ollama).
> Las notebooks se asumen con **Windows 10/11**. En Mac/Linux los pasos son equivalentes.

## 0. Confirmar con la organización (por el canal oficial)

El reglamento habla de "computadoras del laboratorio". Antes de configurar nada, escribir a la
mensajería del Sistema ONIET u oniet@ubp.edu.ar. Borrador:

> Hola, somos el equipo ___ de la escuela ___ (Desarrollo de Sistemas). Queríamos consultar:
> 1. ¿Podemos usar nuestras propias notebooks?
> 2. ¿Hay Wi-Fi para los participantes? ¿Podemos usar datos del celular si se corta?
> 3. ¿Podemos usar asistentes de IA (Claude Code, Google Antigravity)?
> 4. ¿Podemos traer una base de código propia preparada antes (plantilla) o hay que empezar de cero?
> 5. ¿La entrega es con un repositorio de GitHub? ¿Público o privado? ¿Dónde se carga el link?
> 6. ¿Cuál es el horario exacto de la competencia y cuándo se considera el cierre?
> Muchas gracias.

## 1. Windows y reloj (las 3 notebooks)

1. Actualizar Windows.
2. **Reloj**: *Configuración → Hora e idioma → Fecha y hora* → "Ajustar hora automáticamente"
   activado, zona horaria de Buenos Aires (UTC-03:00) y, si aparece, el botón **Sincronizar ahora**.
   La hora de cada commit sale de este reloj, y **la hora del último commit es la hora de entrega**.
3. Terminal por defecto **Símbolo del sistema (cmd)** en Antigravity/VS Code:
   `Ctrl+Shift+P` → *Terminal: Select Default Profile* → *Command Prompt*.
   Evita el bloqueo de scripts de PowerShell y funciona igual que los `.bat`.

## 2. Python (las 3)

1. Instalar **Python 3.13** desde el instalador `.exe` de python.org, tildando la opción para
   agregar Python al PATH. Alternativa: `winget install -e --id Python.Python.3.13 --source winget`.
   (Python 3.12 solo recibe parches de seguridad y ya no tiene instaladores nuevos para Windows.)
   Usar la **misma versión** en las 3. No usar la versión de Microsoft Store.
2. Cerrar y abrir la terminal: `python --version` y `py --version` tienen que responder.
3. Si `python` abre la Microsoft Store: Inicio → escribir **Administrar alias de ejecución de
   aplicaciones** → desactivar las entradas de Python del *Instalador de aplicaciones*
   (`python.exe` y `python3.exe`).
   Si igual falla, usar `py` en lugar de `python`.
4. Si se usa PowerShell: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
   (sin esto, activar el entorno virtual da "running scripts is disabled").

## 3. Git y GitHub (las 3)

1. `winget install --id Git.Git -e --source winget` (o el instalador de git-scm.com). Reabrir la
   terminal.
2. Configurar identidad (con el **mail de la cuenta de GitHub**) y la forma de hacer `pull`:

   ```
   git config --global user.name "Nombre Apellido"
   git config --global user.email "mail-de-github"
   git config --global pull.rebase false
   ```

3. Aceptar la invitación de colaborador al repositorio de entrega (ver `06_GIT.md`).
4. `git clone` del repositorio (no descargar ZIP). El primer `git push` abre una ventana de Git
   Credential Manager para iniciar sesión en GitHub (conviene elegir la opción del navegador).

## 4. El proyecto (las 3)

1. Doble clic en `iniciar.bat` (o `iniciar.bat` desde la terminal). Crea `.venv`, instala todo y
   abre el sistema en http://127.0.0.1:5000.
2. Doble clic en `verificar.bat`: todo en `[ OK  ]`.
3. Si Windows muestra "Windows protegió su PC": *Más información → Ejecutar de todas formas*, o
   clic derecho en el archivo → *Propiedades* → *Desbloquear*.
4. Si el puerto 5000 está ocupado: `set PORT=5001` y después `iniciar.bat`.

## 5. Herramientas de IA

**Edad mínima (verificada en los términos oficiales el 30/09/2026): 18 años** para Claude
(claude.ai y Claude Code), Ollama y Antigravity. El equipo cumple (los 3 tienen 18).

**Reserva opcional:** como son estudiantes secundarios, cada uno puede pedir **GitHub Education**
(docs.github.com, "Apply to GitHub Education as a student") y usar **GitHub Copilot Student**
gratis en VS Code. La aprobación puede tardar días: pedirlo ya si lo quieren tener.

Cada persona usa **su propia cuenta**. No se comparten cuentas ni claves: los términos de
Anthropic no lo permiten y las preguntas frecuentes de Ollama (ollama.com/pricing) indican "una
cuenta por persona". La persona A además
responde por todo lo que se haga con su cuenta.

### A: Claude Code (Claude Pro)

1. PowerShell: `irm https://claude.ai/install.ps1 | iex` (sin permisos de administrador).
   Alternativas: `winget install Anthropic.ClaudeCode`.
2. Terminal nueva: `claude --version`. Si dice "no se reconoce", agregar
   `%USERPROFILE%\.local\bin` al PATH del usuario.
3. En la carpeta del proyecto: `claude`, iniciar sesión con la cuenta Pro, `/status` y `/usage`.
4. Probar `/verificar` y `/context` (tiene que aparecer CLAUDE.md cargado).
5. **Skills oficiales de Anthropic** (opcional, probadas antes): dentro de Claude Code,
   `/plugin marketplace add anthropics/skills` y después
   `/plugin install example-skills@anthropic-agent-skills` (trae `webapp-testing` y
   `frontend-design`, licencia Apache 2.0).

### A: Claude Code con Ollama (DeepSeek, cupo grande)

1. Instalar Ollama para Windows (`OllamaSetup.exe` de ollama.com, sin administrador).
2. `ollama signin` (abre el navegador para vincular la notebook a la cuenta).
3. Probar el modelo: `ollama run deepseek-v4.1-flash:cloud` → escribir "hola" → `/bye`.
4. Lanzar Claude Code con DeepSeek, en la carpeta del proyecto y **en otra terminal** distinta a
   la de Claude Pro:

   ```
   ollama launch claude --model deepseek-v4.1-flash:cloud
   ```

5. Adentro, `/status`: tiene que mostrar el modelo de Ollama. `/context`: CLAUDE.md cargado.
6. El plan Pro de Ollama cuesta USD 20 por mes (o USD 200 por año), incluye USD 60 de crédito de
   uso por mes y permite **3 pedidos simultáneos** (revisar en ollama.com/settings/usage).

> ⚠️ Nunca configurar `ANTHROPIC_AUTH_TOKEN` o `ANTHROPIC_BASE_URL` de forma permanente (`setx`):
> Claude Code dejaría de usar la cuenta Pro. `ollama launch` los configura solo para esa ventana.

### A, B y C: Google Antigravity

1. Instalar desde antigravity.google/download e iniciar sesión con **Gmail personal**.
   Requisito oficial: Antigravity **no está disponible para menores de 18 años** (FAQ). El equipo
   cumple (los 3 tienen 18).
2. Instalar **Google Chrome** y ponerlo como **navegador predeterminado** (el comando `/browser`
   lo exige).
3. Crear la variable de entorno de usuario `HOME` con el valor `%USERPROFILE%` y reiniciar
   (evita el error "failed to install playwright: $HOME environment variable is not set" del
   navegador en Windows):
   *Buscar "variables de entorno" → Editar las variables de entorno de esta cuenta → Nueva*.
4. Abrir la carpeta del proyecto. Antigravity lee `AGENTS.md` y las reglas de `.agents/rules/`.
5. **Configuración segura**:
   - Terminal: en Windows, *Settings → Agent → Terminal Command Auto Execution* en **Request
     Review** (las opciones son Request Review / Proceed in Sandbox / Always Proceed). En Mac/Linux
     el preset se elige en *Settings → General → Permission Settings* (Default / Request Review /
     Turbo). Agregar a la lista permitida (Allow list): `python`, `pip`, `git status`, `git diff`.
     **Nunca "Always Proceed" ni "Turbo"** (hay casos documentados de agentes que borraron archivos).
   - Revisión de artefactos: **Request Review** (la otra opción es Always Proceed).
   - **Agent Non-Workspace File Access**: desactivado (así viene por defecto).
6. Probar el agente de navegador: con el sistema corriendo (`iniciar.bat` en **su** terminal),
   pedir `/browser Abrí http://127.0.0.1:5000 y sacá una captura`. No hace falta ninguna
   extensión: el agente controla Chrome con una sesión de depuración (CDP).
7. Revisar el cupo en **View Usage** (menú de modelos): hay dos grupos con cupo separado
   ("Gemini" y "Claude y GPT"). En el plan gratis el cupo se renueva **una vez por semana** (la
   renovación cada 5 horas es de los planes Pro y Ultra, aunque View Usage muestre las dos barras).
   **No gastar el cupo los días anteriores a la competencia.** Anotar qué día se reinicia.
   Ojo: la página oficial de modelos marca Claude Sonnet/Opus 4.6 en el plan gratis, pero la de
   planes dice "third-party models" solo en Ultra: comprobar con las cuentas reales que aparecen.

### Prueba: ¿cada IA cargó las reglas del proyecto?

Abrir cada herramienta **en la carpeta del proyecto** y preguntar:

```
Sin leer archivos nuevos: ¿qué reglas del proyecto tenés cargadas? Resumilas en 5 líneas
y decime qué comando hay que correr antes de hacer push. ¿Qué skills del proyecto conocés?
```

La respuesta correcta menciona **Flask + SQLite**, las **capas** (rutas → servicios →
repositorios), **todo en español** y `python herramientas/verificar.py`, y lista skills como
`analizar-consigna` y `verificar`. Si la IA no sabe nada de esto:

- **Claude Code** (Pro o Ollama): `/context` tiene que mostrar `CLAUDE.md`. Si no aparece, revisar
  que la terminal esté en la carpeta del proyecto.
- **Antigravity**: revisar en *Customizations* que aparezcan la regla `proyecto` y las skills.
  Mientras tanto, empezar cada chat con "Leé AGENTS.md antes de empezar".

Hacer también una prueba real chica: pedir `/verificar` (o "seguí la skill verificar") y comprobar
que ejecuta `python herramientas/verificar.py --arreglar` y reporta el resultado.

## 6. Plan sin internet (pendrive)

Con internet, en la carpeta del proyecto:

```
py -m pip download -d wheels -r requirements-dev.txt
```

Copiar la carpeta `wheels/` y los instaladores de Python y Git a un pendrive. Si el día de la
competencia no hay internet, `iniciar.bat` instala desde `wheels/` automáticamente.

Sin internet **funcionan**: el sistema, los tests, `git commit`. **No funcionan**: `git push` y
las IAs. Llevar un celular con datos para usar como hotspot.

## 7. Prueba final (la semana anterior)

- [ ] `python herramientas/diagnostico.py --rol A|B|C` sin fallas en las 3 notebooks.
- [ ] Un simulacro completo de 2 h 30 min (ver `07_PRACTICA.md`) **con estas notebooks**.
- [ ] Cada uno hizo al menos un commit y push al repositorio de práctica.
- [ ] `git log -1 --format=fuller` muestra la hora correcta.
- [ ] Cargadores, zapatilla, pendrive y celular con datos listos para llevar.
