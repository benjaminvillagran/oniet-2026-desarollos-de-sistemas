# 10 · Verificación de datos contra fuentes oficiales

> **Estado:** las 18 correcciones de la sección 3 ya se aplicaron a la documentación del kit (30/09/2026).
> Este archivo queda como registro de qué se verificó, dónde y con qué cita.


Fecha de la verificación: **30/09/2026**. Cada dato se comprobó leyendo la página oficial directamente
(no resúmenes de búsqueda). Las citas son textuales y están en el idioma original.

Veredictos:

- **CONFIRMADA**: la fuente oficial dice lo mismo que el repositorio.
- **CORREGIDA**: el dato está mal, incompleto o desactualizado. La corrección está en la sección 3.
- **NO VERIFICABLE**: ninguna fuente oficial lo dice (ni a favor ni en contra).

Cuando la única fuente es el foro oficial (discuss.ai.google.dev) o un repositorio de un
participante, se aclara en la tabla con **(foro)** o **(secundaria)**.

## 1. Resumen

| | Cantidad |
|---|---|
| Afirmaciones revisadas | **118** |
| CONFIRMADAS | **94** |
| CORREGIDAS | **18** |
| NO VERIFICABLES | **6** |

Lo más importante, en orden de urgencia:

1. **Antigravity no está disponible para menores de 18 años** (FAQ oficial). Si B o C son menores,
   no pueden usar su propia cuenta y hay que rearmar los roles de `03_PLAN_DEL_DIA.md`.
2. **El reglamento 2026 dice que se usan las computadoras del laboratorio**, con entornos
   preinstalados. Ninguna fuente oficial habla de notebooks propias. Es imprescindible preguntar por
   el canal oficial (mensajería del Sistema ONIET u **oniet@ubp.edu.ar**) y tener listo el Plan B.
3. **Fecha confirmada**: Desarrollo de Sistemas es el **jueves 8 de octubre de 2026, de 14:00 a
   16:30**, presencial, en los **laboratorios 3 y 4** de la UBP.
4. **Plan Pro de Ollama**: cuesta **USD 20 por mes** e incluye USD 60 de crédito de uso.
   `docs/04` dice "USD 60/mes", y eso está mal.
5. **Antigravity, plan gratis**: el cupo se renueva **por semana**. La renovación cada 5 horas es de
   los planes Pro y Ultra. Además, algunas opciones de Settings tienen otro nombre ("Agent Decides"
   no existe, y "Ask/Deny" no es la opción de acceso fuera del proyecto).
6. **competencias.oniet@ubp.edu.ar** solo aparece en una página vieja (reglamento 2019). El
   reglamento 2026 da como canales oficiales la mensajería del Sistema ONIET y oniet@ubp.edu.ar.

## 2. Tablas por tema

### A. Ollama

| # | Afirmación | Archivo(s) | Veredicto | URL oficial | Cita textual breve |
|---|---|---|---|---|---|
| A1 | "Los términos de Ollama indican 'una cuenta por persona'" | docs/02 §5, docs/03 | CORREGIDA | https://ollama.com/pricing · https://ollama.com/terms | Pricing (FAQ): "Can I have multiple Ollama accounts? No. Ollama is one account per person." Terms: "You are responsible for maintaining the confidentiality of your account credentials" |
| A2 | Plan Pro: 3 pedidos simultáneos y USD 60 de uso por mes | docs/02 §5 | CONFIRMADA (falta el precio) | https://ollama.com/pricing | "$60 of usage credits per month" · "Free includes 1 concurrent request, Pro 3, and Max and Team 10." |
| A3 | "plan Pro de Ollama: USD 60/mes" | docs/04 | CORREGIDA | https://ollama.com/pricing | "$20 / mo. or $200/yr billed annually" |
| A4 | `ollama signin` abre el navegador para vincular la notebook | docs/02 §5, docs/09 | CONFIRMADA | https://docs.ollama.com/cli · https://github.com/ollama/ollama/blob/main/cmd/cmd.go | "_ = browser.OpenURL(aErr.SigninURL)" · "If your browser did not open, navigate to:" |
| A5 | `ollama launch claude --model deepseek-v4.1-flash:cloud` es válido | docs/02, 03, 04, CLAUDE.md | CONFIRMADA | https://ollama.com/library/deepseek-v4.1-flash | "Claude Code ollama launch claude --model deepseek-v4.1-flash:cloud" |
| A6 | `ollama launch` configura `ANTHROPIC_*` solo para esa ventana | docs/02 §5 | CONFIRMADA | https://github.com/ollama/ollama/blob/main/cmd/launch/claude.go | "cmd.Env = append(os.Environ(), c.envVars(model)...)" con "ANTHROPIC_AUTH_TOKEN=ollama" |
| A7 | Existe el modelo `deepseek-v4.1-flash:cloud` (`ollama run ...`) | docs/02, docs/09 | CONFIRMADA | https://ollama.com/library/deepseek-v4.1-flash | "ollama run deepseek-v4.1-flash:cloud" · "Context 1M tokens" |
| A8 | Instalar `OllamaSetup.exe` sin administrador | docs/02 §5 | CONFIRMADA | https://docs.ollama.com/windows | "It installs in your account without requiring Administrator rights." |
| A9 | Con Ollama, `/model sonnet` u `opus` siguen siendo DeepSeek | docs/04 | CONFIRMADA | https://github.com/ollama/ollama/blob/main/cmd/launch/claude.go | "ANTHROPIC_DEFAULT_OPUS_MODEL=" + model, "ANTHROPIC_DEFAULT_SONNET_MODEL=" + model |
| A10 | "Ollama no guarda caché" | docs/04 | CORREGIDA | https://docs.ollama.com/api/anthropic-compatibility · https://ollama.com/pricing | "Not supported": "Prompt caching \| `cache_control` blocks" · Pricing: "deepseek-v4.1-flash $0.30 $0.006 $1.20" (entrada / entrada en caché / salida) |
| A11 | Revisar el uso en ollama.com/settings/usage | docs/02, docs/09 | CONFIRMADA | https://ollama.com/pricing | La página de precios remite al uso de la cuenta en settings |

Datos de Ollama que el repositorio no menciona, pero que convienen:

- **¿deepseek-v4.1-flash está en el plan Free?** NO VERIFICABLE. Pricing solo dice "Free accounts
  include a starter amount of usage for a smaller set of starter models" y no dice cuáles son.
- **Nombre en la API directa**: `deepseek-v4.1-flash`, sin `:cloud` (https://docs.ollama.com/cloud:
  "For API requests to ollama.com, use the name returned by this list").
- **Clave pública**: en Windows está en `C:\Users\<usuario>\.ollama\id_ed25519.pub`
  (https://docs.ollama.com/faq). Las claves se revocan en https://ollama.com/settings/keys.
- **Ventana de contexto**: el issue abierto https://github.com/ollama/ollama/issues/18463 dice que
  "`ollama launch claude` starts 1M-context cloud models with a 200K window". En
  https://github.com/ollama/ollama/issues/17584 se propone `CLAUDE_CODE_MAX_CONTEXT_TOKENS`. No
  afecta el trabajo con esta plantilla: el proyecto entra en 200K.

### B. Google Antigravity

| # | Afirmación | Archivo(s) | Veredicto | URL oficial | Cita textual breve |
|---|---|---|---|---|---|
| B1 | Antigravity lee `AGENTS.md` de la raíz | README, docs/02, docs/04 | CONFIRMADA | https://antigravity.google/docs/rules/ | "Antigravity treats its entire content as plain Markdown and keeps it continuously active ( always_on )" |
| B2 | Reglas del workspace en `.agents/rules/` | README, docs/02, docs/04 | CONFIRMADA | https://antigravity.google/docs/rules/ | "<dir>/.agents/rules/*.md (and legacy <dir>/.agent/rules/*.md )" |
| B3 | Frontmatter `trigger: always_on` + `description:` | .agents/rules/proyecto.md | CONFIRMADA | https://antigravity.google/docs/rules/ | "trigger string Yes … model_decision , always_on , glob , or manual" |
| B4 | Skills en `.agents/skills/<nombre>/SKILL.md`, se invocan con `/nombre` | README, docs/04 | CONFIRMADA | https://antigravity.google/docs/skills/ | "Antigravity defaults to .agents/skills" · "type /<skill-name> in the prompt panel" |
| B5 | Hay que instalar Google Chrome para el agente de navegador | docs/02 §5 | CONFIRMADA (y tiene que ser el predeterminado) | https://antigravity.google/docs/ide/browser/ · codelab getting-started | "The /browser command requires Google Chrome browser to be your default browser" |
| B6 | "La primera vez aparece 'Setup' para instalar la extensión en Chrome" | docs/02 §5 | CORREGIDA | https://codelabs.developers.google.com/agentic-ui-automation-with-antigravity | "works directly via the Chrome DevTools Protocol (CDP), removing the need for any browser extensions" |
| B7 | Existe el comando `/browser` | docs/02, skill probar-en-navegador | CONFIRMADA | https://antigravity.google/docs/getting-started/ | "/browser Explicit slash command controlling browser debugging behaviors in Google Chrome." |
| B8 | Crear la variable `HOME=%USERPROFILE%` en Windows | docs/02 §5, docs/09 | CONFIRMADA (foro) | https://discuss.ai.google.dev/t/tip-fix-for-playwright-home-environment-variable-is-not-set-on-windows/121086 | Arreglo: "SetEnvironmentVariable('HOME', $env:USERPROFILE, 'User')" |
| B9 | Texto del error: "Failed to install playwright: $HOME is not set" | docs/02 §5, docs/09 | CORREGIDA | ídem B8 (foro) | "failed to install playwright: $HOME environment variable is not set" |
| B10 | Terminal en "Request Review", nunca "Turbo" / "Always Proceed" | docs/02 §5, docs/04 | CONFIRMADA (con matiz) | https://antigravity.google/docs/agent-settings/ | Windows: "Request Review", "Proceed in Sandbox", "Always Proceed". macOS/Linux (presets): "Default", "Request Review", "Turbo" |
| B11 | Revisión de artefactos: "Agent Decides" | docs/02 §5 | CORREGIDA | https://antigravity.google/docs/artifact-review/ | "Choose between two policies: 1. Request Review (Recommended) … 2. Always Proceed" |
| B12 | Acceso a archivos fuera del proyecto: "Ask" o "Deny" | docs/02 §5 | CORREGIDA | https://antigravity.google/docs/agent-settings/ | "Agent Non-Workspace File Access … Allows the agent to view and edit files outside of the active project folders." (es un interruptor) |
| B13 | Hay una lista de comandos permitidos | docs/02 §5 | CONFIRMADA | https://antigravity.google/docs/agent-settings/ | "except those explicitly added to your configurable Allow list" |
| B14 | Comando `/plan` para tareas grandes | docs/04 | CONFIRMADA | https://antigravity.google/docs/plan/ | "The /plan command facilitates structured planning" |
| B15 | Modelos del plan gratis: Gemini 3.8/3.7 Flash, Gemini 3.1 Pro, Claude Sonnet 4.6, Claude Opus 4.6 | docs/03, docs/04 | CONFIRMADA (con matiz) | https://antigravity.google/docs/models/ | Tabla "Free & Google AI Plus": ✅ en Gemini 3.8/3.7 Flash, 3.1 Pro, "Claude Sonnet 4.6 (thinking)", "Claude Opus 4.6 (thinking)". Ojo: https://antigravity.google/docs/plans/ dice "Access to third-party models" solo en Ultra |
| B16 | Dos grupos de cupo, "Gemini" y "Claude y GPT", en View Usage | docs/02, 03, 04 | CONFIRMADA | https://antigravity.google/docs/models/ | "View Usage Gemini Models Weekly Limit Remaining … Claude and GPT models Weekly Limit Remaining" |
| B17 | Cada grupo tiene límite de 5 horas y límite semanal (plan gratis) | docs/02 §5, docs/04 | CORREGIDA | https://antigravity.google/docs/plans/ | "Users not on AI Pro and Ultra plans receive: Meaningful quota, refreshed weekly · Weekly rate limit" |
| B18 | La cuota se consume por trabajo, no por mensaje | docs/04 | CONFIRMADA | https://antigravity.google/docs/plans/ | "the rate limits are correlated with the amount of work done by the agent" |
| B19 | Gemini 3.8 Flash: lentitud y errores 503 entre las 13:00 y las 19:00 (Argentina) | docs/04, docs/09 | CONFIRMADA (foro, responde Google) | https://discuss.ai.google.dev/t/issue-report-severe-slowdowns-and-frequent-503-errors-on-gemini-flash-3-8-during-specific-hours-are-server-resources-being-intentionally-throttled/184984 | "the 503 UNAVAILABLE errors and slowdowns between 16:00 and 22:00 UTC" (= 13 a 19 en Argentina) |
| B20 | Descarga en antigravity.google/download | docs/02 §5 | CONFIRMADA | https://antigravity.google/docs/getting-started/ | "Visit antigravity.google/download to download Google Antigravity 2.0." |
| B21 | El instalador de Windows no pide administrador (el repo no lo dice, pero lo supone) | docs/02 §5 | CONFIRMADA (foro, responde Google) | https://discuss.ai.google.dev/t/antigravity-system-wide-installation-on-windows/129740 | "The current Windows .exe is a User-Level installer" |
| B22 | Iniciar sesión con Gmail personal | docs/02 §5 | CONFIRMADA (falta la edad) | https://antigravity.google/docs/faq/ | "available for personal Google accounts in approved geographies … try using an @gmail.com email address" · "unavailable to under-18 users" |
| B23 | Source Control: Commit, Sync Changes, Accept Current/Incoming/Both, Resolve in Merge Editor | docs/06 | CONFIRMADA (docs de VS Code) | https://code.visualstudio.com/docs/sourcecontrol/overview | "Sync Changes" · "Accept Current Change" · "Accept Incoming Change" · "Accept Both Changes" · "Resolve in Merge Editor" |
| B24 | Error "Agent execution terminated due to error" | docs/09 | CONFIRMADA (foro) | https://discuss.ai.google.dev/t/antigravity-broken-getting-only-agent-execution-terminated-due-to-error/115443 | "Agent execution terminated due to error." |
| B25 | En Windows el agente queda en "Running…" | docs/04, docs/09, skill probar-en-navegador | CONFIRMADA (foro) | https://discuss.ai.google.dev/t/fix-antigravity-terminal-hanging-on-windows-how-to-stop-the-running-state-loop/123426 | "the terminal often gets stuck in a permanent 'Running…' state" |
| B26 | "El navegador abre Edge en vez de Chrome" | docs/09 | NO VERIFICABLE | — | Sin resultados en fuentes oficiales. Lo más cercano es el requisito de B5 |

Workflows: https://antigravity.google/docs/migration/workflows-to-skills/ dice "Workflows are
deprecated and will be retired on November 1, 2026". El repo no usa workflows, así que no hace falta
cambiar nada.

### C. Claude Code

| # | Afirmación | Archivo(s) | Veredicto | URL oficial | Cita textual breve |
|---|---|---|---|---|---|
| C1 | Skills en `.claude/skills/<nombre>/SKILL.md` con `name` y `description`, invocables con `/nombre` | README, CLAUDE.md, docs/04 | CONFIRMADA | https://code.claude.com/docs/en/skills | "Project \| `.claude/skills/<skill-name>/SKILL.md`" |
| C2 | `disable-model-invocation: true` = solo manual | skill entrega-final, README | CONFIRMADA | https://code.claude.com/docs/en/skills | "Use for workflows you want to trigger manually with `/name`." |
| C3 | `CLAUDE.md` importa `AGENTS.md` con `@AGENTS.md` | CLAUDE.md, README, docs/04 | CONFIRMADA | https://code.claude.com/docs/en/memory | "A `CLAUDE.md` that already imports `AGENTS.md` \| Your `CLAUDE.md`, with `AGENTS.md` included through the import" · "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md`" |
| C4 | `/context` muestra CLAUDE.md cargado | docs/02 §5 | CONFIRMADA | https://code.claude.com/docs/en/memory | "run `/context` … check the list under **Memory files**" |
| C5 | `/usage` = cupo, `/status` = cuenta y modelo | docs/02, 03, 04 | CONFIRMADA | https://code.claude.com/docs/en/commands | `/usage`: "Show session cost, plan usage limits" · `/status`: "showing version, model, account" |
| C6 | `/rewind` o `Esc Esc` deshace lo que hizo la IA, pero no los comandos de terminal | docs/04 | CONFIRMADA | https://code.claude.com/docs/en/checkpointing · /interactive-mode | "Checkpointing does not track files modified by Bash commands" · "double `Esc` opens the rewind menu" |
| C7 | `Shift+Tab`: normal → aceptar ediciones → plan | docs/04 | CONFIRMADA | https://code.claude.com/docs/en/interactive-mode | "Cycle through `default` …, `acceptEdits`, `plan`" |
| C8 | `Alt+V` pega una captura en Windows | docs/04 | CONFIRMADA | https://code.claude.com/docs/en/interactive-mode | "`Alt+V` (Windows and WSL) \| Paste image from clipboard" |
| C9 | `@archivo` menciona un archivo; `/clear` limpia el contexto | docs/04 | CONFIRMADA | https://code.claude.com/docs/en/interactive-mode | "`@` \| File path mention" |
| C10 | Con Claude Pro, el modelo por defecto es Opus | docs/04, CLAUDE.md | CONFIRMADA | https://code.claude.com/docs/en/model-config | "Pro, Max, Team, Enterprise, and Anthropic API: defaults to Opus 5.5" |
| C11 | Alias `sonnet` y `/model sonnet` | docs/04, claude_settings.json | CONFIRMADA | https://code.claude.com/docs/en/model-config | "`sonnet` \| Uses the latest Sonnet model for daily coding tasks" |
| C12 | `docs/plantillas/claude_settings.json` es válido (`$schema`, `model`, allow/ask/deny, `Bash(...)`, `PowerShell(...)`, `Read(./.env)`) | docs/plantillas | CONFIRMADA | https://code.claude.com/docs/en/permissions · /settings | "Rules are evaluated in order: deny, then ask, then allow" · "A `*` can go anywhere in the rule" · "PowerShell permission rules use the same shape as Bash rules" · "`Read(./.env)` \| Matches reading the `.env` file" |
| C13 | Ese archivo "**bloquea** `git push --force`, `git reset --hard` y borrados recursivos" | docs/04 | CORREGIDA | https://code.claude.com/docs/en/permissions | "Bash permission patterns that try to constrain command arguments are fragile" (no bloquea variantes como `rm -fr` o `git push origin +main`) |
| C14 | `irm https://claude.ai/install.ps1 \| iex`, sin administrador | docs/02 §5 | CONFIRMADA | https://code.claude.com/docs/en/setup | "You do not need to run as Administrator. Installing Git for Windows is optional." |
| C15 | `winget install Anthropic.ClaudeCode` | docs/02 §5 | CONFIRMADA | https://code.claude.com/docs/en/setup | "`winget install Anthropic.ClaudeCode`" |
| C16 | Si "claude no se reconoce", agregar `%USERPROFILE%\.local\bin` al PATH | docs/02 §5, docs/09 | CONFIRMADA | https://code.claude.com/docs/en/setup | "If your shell says `claude` isn't found or isn't recognized, the install directory isn't on your PATH yet" · `$env:USERPROFILE\.local\bin\claude.exe` |
| C17 | Claude Code en la terminal de Antigravity entra en un bucle instalando la extensión: problema conocido, sin solución oficial | docs/04, docs/09 | CONFIRMADA | https://github.com/anthropics/claude-code/issues/22360 | "CLI fails to start in Google Antigravity: "Error installing VS Code extension" loop" (cerrado como *not planned*) |
| C18 | `/plugin marketplace add anthropics/skills` y `/plugin install example-skills@anthropic-agent-skills` | docs/02 §5 | CONFIRMADA | https://github.com/anthropics/skills | "/plugin marketplace add anthropics/skills" · "/plugin install example-skills@anthropic-agent-skills" |
| C19 | Trae `webapp-testing` y `frontend-design`, con licencia Apache 2.0 | docs/02 §5 | CONFIRMADA | https://github.com/anthropics/skills (marketplace.json y LICENSE.txt de cada skill) | "./skills/frontend-design", "./skills/webapp-testing" · "Apache License Version 2.0" |
| C20 | Claude Pro: ventana de 5 h + límite semanal, compartido con claude.ai | docs/04 | CONFIRMADA | https://support.claude.com/en/articles/8325606-what-is-the-pro-plan · /11145838 | "Your session-based usage limit will reset every five hours." · "weekly usage limit" · "shared across Claude and Claude Code" |
| C21 | Los términos de Anthropic no permiten compartir la cuenta | docs/02 §5, docs/03 | CONFIRMADA | https://www.anthropic.com/legal/consumer-terms | "You may not share your Account login information … with anyone else." |
| C22 | Con variables `ANTHROPIC_*` configuradas, Claude Code no usa la cuenta Pro | docs/02 §5, docs/09 | CONFIRMADA | https://code.claude.com/docs/en/authentication | Precedencia: "2. `ANTHROPIC_AUTH_TOKEN` … 3. `ANTHROPIC_API_KEY` … 7. Subscription OAuth credentials" |

### D. Windows y Python

| # | Afirmación | Archivo(s) | Veredicto | URL oficial | Cita textual breve |
|---|---|---|---|---|---|
| D1 | Alias: "Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones" | docs/02 §2, docs/09 | CORREGIDA | https://docs.python.org/3/using/windows.html · https://learn.microsoft.com/es-es/windows/python/faqs | "Click Start, open "Manage app execution aliases"" · "abriendo "Administrar alias de ejecución de aplicaciones" en Inicio" |
| D2 | Casilla "Add python.exe to PATH" | docs/02 §2, docs/09 | NO VERIFICABLE (texto exacto) | https://docs.python.org/3.12/using/windows.html | La documentación la llama "Add Python to PATH" |
| D3 | `py` responde después de instalar desde python.org; el instalador tiene "Modify" | docs/02 §2, docs/09 | CONFIRMADA | https://docs.python.org/3.12/using/windows.html | "Include_launcher … Default: 1" · "“Modify” allows you to add or remove features" |
| D4 | "Instalar Python 3.12 o 3.13" | docs/02 §2 | CORREGIDA (recomendación) | https://devguide.python.org/versions/ · https://www.python.org/downloads/windows/ | 3.12: "security" (ya no tiene instaladores de Windows después de 3.12.10) · 3.13: "bugfix" · 3.14: "bugfix" |
| D5 | `winget install -e --id Python.Python.3.12 --source winget` | docs/02 §2 | CONFIRMADA | https://github.com/microsoft/winget-pkgs/tree/master/manifests/p/Python/Python/3/12 | Hay manifiestos de 3.12.0 a 3.12.10 (también existe `Python.Python.3.13`) |
| D6 | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` | docs/02 §2, docs/09 | CONFIRMADA | https://docs.python.org/3/library/venv.html | "it may be required to enable the Activate.ps1 script by setting the execution policy … Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" |
| D7 | `winget install --id Git.Git -e --source winget` | docs/02 §3 | CONFIRMADA | https://git-scm.com/install/windows | "winget install --id Git.Git -e --source winget" |
| D8 | Git Credential Manager viene con Git for Windows | docs/02 §3, docs/06 | CONFIRMADA | https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/install.md | "GCM is included with Git for Windows" |
| D9 | "El primer `git push` abre el navegador para iniciar sesión" | docs/02 §3, docs/06 | CORREGIDA | https://github.com/git-ecosystem/git-credential-manager | "a window will automatically open and walk you through the sign-in process" |
| D10 | Reloj: "Configuración → Hora e idioma → Fecha y hora" (Windows 10 y 11) | docs/02 §1, docs/06, docs/09 | CONFIRMADA | https://support.microsoft.com/es-es/windows/cómo-establecer-la-hora-y-la-zona-horaria-dfaa7122-479f-5b98-2a7b-fa0b6e01b261 | "Se aplica a Windows 11 Windows 10" · "Configuración > Hora & idioma > Fecha & hora" |
| D11 | Interruptor "Establecer la hora automáticamente" | docs/02 §1 | CORREGIDA | ídem D10 | "la opción Ajustar hora automáticamente está activada" |
| D12 | Botón "Sincronizar ahora" y zona "(UTC-03:00) Buenos Aires" | docs/02 §1, docs/06, docs/09 | NO VERIFICABLE | ídem D10 (es-es, es-mx, en-us) | No aparecen en la página oficial |
| D13 | SmartScreen: "Más información → Ejecutar de todas formas" | docs/02 §4, docs/09 | NO VERIFICABLE | https://learn.microsoft.com/en-us/windows/security/operating-system-security/virus-and-threat-protection/microsoft-defender-smartscreen/ | La página oficial no nombra esos botones |
| D14 | Propiedades → "Desbloquear" | docs/02 §4, docs/09 | CONFIRMADA | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/unblock-file | "the same operation as the Unblock button on the Properties dialog box" |
| D15 | `pip download -d wheels` y después instalar sin internet con `--no-index --find-links` | docs/02 §6, iniciar.bat | CONFIRMADA | https://pip.pypa.io/en/stable/user_guide/ · /cli/pip_download/ | "py -m pip install --no-index --find-links=DIR -r requirements.txt" · "these options all default to the current system/interpreter" |
| D16 | `Ctrl+Shift+P` → "Terminal: Select Default Profile" → "Command Prompt" | docs/02 §1 | CONFIRMADA (docs de VS Code) | https://code.visualstudio.com/docs/terminal/profiles | "Terminal: Select Default Profile" |
| D17 | `netstat -ano \| findstr :5000`; WinError 10013 y 10048 = puerto ocupado | docs/09 | CONFIRMADA | https://learn.microsoft.com/en-us/windows/win32/winsock/windows-sockets-error-codes-2 | "WSAEADDRINUSE 10048 Address already in use" · "WSAEACCES 10013 … bound to the same address with exclusive access" |
| D18 | "LF will be replaced by CRLF" es solo un aviso | docs/09 | CONFIRMADA | https://git-scm.com/docs/git-config (core.safecrlf) | "Git will only warn about an irreversible conversion but continue the operation" |

### E. Git y GitHub

| # | Afirmación | Archivo(s) | Veredicto | URL oficial | Cita textual breve |
|---|---|---|---|---|---|
| E1 | Hay un límite de invitaciones de colaboradores por día | docs/06 | CONFIRMADA | https://docs.github.com/en/rest/collaborators/collaborators | "You are limited to sending 50 invitations to a repository per 24 hour period." |
| E2 | En un repositorio personal privado no se puede dar acceso de solo lectura | docs/06 | CONFIRMADA | https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-user-account-settings/permission-levels-for-a-personal-account-repository | "Collaborators can't have read-only access to repositories owned by a personal account." |
| E3 | Settings → Collaborators → Add people | docs/06 | CONFIRMADA | https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository | "In the 'Access' section of the sidebar, click Collaborators" · "Click Add people" |
| E4 | `actions/checkout@v7` existe | .github/workflows/verificacion.yml | CONFIRMADA | https://github.com/actions/checkout/releases | v7.0.0 y v7.0.1 publicadas; el README usa `@v7` |
| E5 | `actions/setup-python@v7` existe | .github/workflows/verificacion.yml | CONFIRMADA | https://github.com/actions/setup-python/releases | v7.0.0 publicada; el README usa `@v7` |
| E6 | `cache: pip` y `cache-dependency-path` en setup-python | .github/workflows/verificacion.yml | CONFIRMADA | https://github.com/actions/setup-python | "Supported package managers are pip, pipenv and poetry" |
| E7 | `concurrency` + `cancel-in-progress`, `workflow_dispatch`, `permissions: contents: read` | .github/workflows/verificacion.yml | CONFIRMADA | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | `concurrency: group: … cancel-in-progress: true` · `permissions: contents: read` |
| E8 | Formato del badge `…/actions/workflows/verificacion.yml/badge.svg` | README, README_ENTREGA.md | CONFIRMADA | https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/monitoring-workflows/adding-a-workflow-status-badge | `https://github.com/OWNER/REPOSITORY/actions/workflows/WORKFLOW-FILE/badge.svg` |
| E9 | "Divergent branches" se resuelve con `git config pull.rebase false` | docs/06, docs/09 | CONFIRMADA | https://git-scm.com/docs/git-pull | "git pull --no-rebase runs git merge." · "You can also set the configuration options pull.rebase, pull.squash, or pull.ff" |
| E10 | Modelo de "repositorio compartido" que GitHub describe para equipos chicos | docs/06 | CONFIRMADA | https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models | "more common with small teams and organizations collaborating on private projects" |
| E11 | `git log -1 --format=fuller` muestra la fecha de autor y la de commit | docs/06, docs/09 | CONFIRMADA | https://git-scm.com/docs/git-log | "AuthorDate: … CommitDate:" |
| E12 | `git stash push -u -m`, `git revert … --no-edit`, `git merge --abort`, `git restore` | docs/06 | CONFIRMADA | https://git-scm.com/docs/git-stash · /git-revert · /git-merge · /git-restore | "[-u \| --include-untracked] … [(-m \| --message) <message>]" · "--no-edit" · "git merge (--continue \| --abort \| --quit)" |

Datos útiles que el repo no menciona:

- **Minutos de Actions**: en repos **públicos** con runners estándar no se cobra. En privados, el plan
  Free trae 2.000 minutos por mes y Windows cuesta más por minuto que Linux (USD 0,010 contra 0,006,
  https://docs.github.com/en/billing/concepts/product-billing/github-actions). La doc actual ya no
  habla de un "multiplicador 2x".
- **Vista Activity** (https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/using-the-activity-view-to-see-changes-to-a-repository):
  muestra "pushes, merges, force pushes" con usuario y hora. Sirve para comprobar la hora del
  último push el día de la entrega.

### F. ONIET 2026

Fuentes: reglamento de la competencia
http://oniet.ubp.edu.ar/wp-content/uploads/2026/06/012_Desarrollo_de_Sistemas_2026.pdf (enlazado
desde https://oniet.ubp.edu.ar/competencias/desarrollo-de-sistemas/), reglamento general
http://oniet.ubp.edu.ar/wp-content/uploads/2026/06/Reglamento-PROGRAMA-ONIET-2026-REV2-1-1.pdf y
cronograma https://oniet.ubp.edu.ar/cronograma/.

| # | Afirmación | Archivo(s) | Veredicto | URL oficial | Cita textual breve |
|---|---|---|---|---|---|
| F1 | ONIET 2026, 30.ª edición, del 2 al 9 de octubre de 2026 | README, docs/01 | CONFIRMADA | https://oniet.ubp.edu.ar/ · Reglamento general | "Olimpiadas Nacionales 30 años – 2 al 9 de Octubre" · "Edición 30° Aniversario" |
| F2 | "El cronograma ubica Desarrollo de Sistemas a las 14 h; confirmar el día" | docs/01 | CORREGIDA (ya hay día) | https://oniet.ubp.edu.ar/cronograma/ | "JUEVES 08 DE OCTUBRE" … "14:00 a 16:30 – (P) Desarrollo de Sistemas (LAB 3 y 4)" |
| F3 | Horario 14:00 a 16:30 (2 h 30 min) | README, AGENTS.md, docs/03 | CONFIRMADA | https://oniet.ubp.edu.ar/cronograma/ | "14:00 a 16:30 – (P) Desarrollo de Sistemas" |
| F4 | "La página de la competencia menciona una duración de unas 4 horas" | docs/01 | CORREGIDA | http://oniet.ubp.edu.ar/urbanismo_y_sociedad/desarrollo-de-sistemas/ (página vieja, reglamento 2019) · PDF 012 | Página vieja: "aproximadamente 4 horas". 012 (2026): "Trabajo presencial durante el tiempo asignado por cronograma" |
| F5 | Se rinde en computadoras de la Universidad | docs/01, docs/02 §0 | CONFIRMADA | PDF 012 | "Se utilizarán computadoras del laboratorio de informática de la Universidad con entornos de desarrollo preinstalados." |
| F6 | Se pueden llevar notebooks propias (el plan lo supone) | docs/01, docs/02, docs/03 | NO VERIFICABLE | PDF 012 · cronograma | Ninguna fuente oficial lo menciona. El 012 solo habla de las computadoras del laboratorio |
| F7 | Lenguajes: Java, JavaScript, PHP, Python, .NET | docs/01 | CONFIRMADA | PDF 012 | "Java, JavaScript, PHP, Python y .NET Framework/.NET Core, incluidos VB, C# o C++." |
| F8 | Grupal, hasta 4 integrantes | docs/01 | CONFIRMADA | PDF 012 | "Hasta 4 integrantes por equipo y hasta 2 equipos por escuela." |
| F9 | Se entrega un repositorio y vale la fecha y hora del último commit | README, docs/01, docs/06 | CONFIRMADA | PDF 012 | "La fecha y hora del último commit serán consideradas como momento de entrega." |
| F10 | Los docentes resuelven dudas técnicas, pero no dicen cómo resolver | docs/01 | CONFIRMADA | PDF 012, punto 6 | "podrán resolver dudas técnicas o de comprensión del entorno, pero no indicar cómo resolver el problema." |
| F11 | Internet permitido para consultas, sin copiar código de terceros | docs/01, AGENTS.md | CONFIRMADA | PDF 012 | "Podrá utilizarse Internet para consultas técnicas, sin copiar código de terceros sin autorización expresa del docente responsable." |
| F12 | IA permitida con uso responsable (punto 15) | README, docs/01, docs/08 | CONFIRMADA | PDF 012, punto 15 | "No se permitirá su uso para vulnerar la autoría, la transparencia, la seguridad o las condiciones propias de la competencia." |
| F13 | Presencial, en el laboratorio de la UBP | docs/01 | CONFIRMADA | PDF 012 | "La competencia será presencial, en el campus de la Universidad Blas Pascal" |
| F14 | Rúbrica 10 / 25 / 25 / 15 / 15 / 10 | AGENTS.md, docs/01, skill revisar-rubrica | CONFIRMADA | PDF 012, punto 10 | "Comprensión de la consigna… 10 / Procesamiento de datos… 25 / Funcionamiento integral… 25 / Calidad del código… 15 / Interfaz y usabilidad… 15 / Entrega y versionado… 10" |
| F15 | Escala 90–100 / 75–89 / 60–74 / menos de 60 | docs/01 | CONFIRMADA | PDF 012, punto 11 | "90 a 100 Desempeño sobresaliente… 75 a 89 … muy bueno… 60 a 74 … adecuado… Menos de 60 … insuficiente." |
| F16 | Canal oficial: oniet@ubp.edu.ar y mensajería del Sistema ONIET | docs/01, docs/02 §0 | CONFIRMADA | PDF 012 | "Los canales oficiales para consultas son la mensajería interna del Sistema ONIET y el correo electrónico oniet@ubp.edu.ar." |
| F17 | Contacto competencias.oniet@ubp.edu.ar | README, docs/01 | CORREGIDA | Solo en la página vieja /urbanismo_y_sociedad/… | No aparece en el reglamento 2026 |
| F18 | Consigna 2020: COVID-19 por API; login con último acceso 30 %, configuración 40 %, dashboard de 10 días 30 % | docs/07 | CONFIRMADA (secundaria) | https://raw.githubusercontent.com/joacru/ONIET2020-Escuela-de-Minas/master/ONIET-2020-Desarrollo-Sistemas-consigna.pdf | "tomar lectura del API COVID19 … fecha del último acceso… 30%… Configuración de usuario… 40%… últimos 10 días… 30%" |
| F19 | Consigna 2021: barrios populares, "CSV de datos.gob.ar", porcentajes 5/25/20/10/20/20, "desempate al azar" | docs/07 | CORREGIDA (menor) | https://raw.githubusercontent.com/facuro18/ONIET2021-Escuela-de-Minas/master/TECNOLOGIA-APLICADA--DESARROLLO-DE-SISTEMAS--CONSIGNA.pdf | Porcentajes confirmados. El enunciado dice "dataset de desarrollo social de la nación" (no dice CSV) y "Si hay muchos en la misma condición, seleccionar N al azar" |
| F20 | Consigna 2023: control de calidad de producción, JSON | docs/07 | NO VERIFICABLE | https://raw.githubusercontent.com/MateMar04/ONIET2023/master/ONIET2023app/utils.py | No se encontró el enunciado. Solo el código de un participante, con campos "Empresa", "Mes", "CantidaPiezasConFallas" |
| F21 | Consigna 2025: taller y aseguradoras; CSV y JSON (JSON con BOM y números como texto); dos rankings | docs/07 | CONFIRMADA (secundaria) | https://github.com/garaySantiago27/oniet/tree/main/consigna | "Reporte 1: Ranking de las compañías de seguro … Reporte 2: Ranking de Regiones según el número de servicios". El BOM y los números como texto están solo en el JSON |
| F22 | "Enunciados oficiales en PDF" | docs/07 | CORREGIDA (menor) | ídem F21 | El de 2025 es un .docx, y el de 2023 no se encontró |

### G. Versiones y licencias

| # | Afirmación | Archivo(s) | Veredicto | URL oficial | Cita textual breve |
|---|---|---|---|---|---|
| G1 | `flask>=3.0,<4` (Flask 3) | requirements.txt, AGENTS.md | CONFIRMADA | https://pypi.org/project/Flask/ | Última: "Flask 3.1.3" (19/02/2026) |
| G2 | Requisito: Python 3.10 o superior | README, AGENTS.md, README_ENTREGA.md | CONFIRMADA | https://pypi.org/project/Flask/ · https://pypi.org/project/pytest/ | Flask: "Requires: Python >=3.9" · pytest 9.1.1: "Requires: Python >=3.10" |
| G3 | Flask BSD-3 | README | CONFIRMADA | https://pypi.org/project/Flask/ | "License: BSD-3-Clause" |
| G4 | openpyxl MIT | README | CONFIRMADA | https://pypi.org/project/openpyxl/ | "MIT License (MIT)" · 3.1.5 · "Python >=3.8" |
| G5 | Chart.js 4.4.4, MIT | README, app/static/vendor/chartjs | CONFIRMADA | https://github.com/chartjs/Chart.js/releases/tag/v4.4.4 · LICENSE.md | "The MIT License (MIT)". La última es la v4.5.1, pero no hace falta actualizar |
| G6 | Jinja2 viene con Flask; `sqlite3` es de la librería estándar | README, AGENTS.md, docs/08 | CONFIRMADA | https://flask.palletsprojects.com/en/stable/installation/ · https://docs.python.org/3/library/sqlite3.html | "These distributions will be installed automatically when installing Flask" |
| G7 | `ruff>=0.5` funciona en todas las versiones que se prueban | requirements-dev.txt | CONFIRMADA | https://pypi.org/project/ruff/ | 0.16.9 · "Requires: Python >=3.7" |

Nota: Python 3.10 llega al fin de su vida útil en **octubre de 2026**
(https://devguide.python.org/versions/). Sigue siendo válido como mínimo, pero no hay que
recomendarlo para instalar.

## 3. Correcciones necesarias

Para cada corrección: archivo, texto actual (copiado del repo) y texto propuesto. Primero van las
críticas.

### Críticas (cambian el plan)

**1. Edad mínima de Antigravity** (B22). `docs/02_CONFIGURAR_NOTEBOOK.md`, §5 Antigravity, paso 1:

- Actual: `1. Instalar desde antigravity.google/download e iniciar sesión con **Gmail personal**.`
- Propuesto: `1. Instalar desde antigravity.google/download e iniciar sesión con **Gmail personal**.
  ⚠️ Antigravity no está disponible para menores de 18 años (FAQ oficial): si algún integrante es
  menor, no puede usar su cuenta y hay que reasignar su IA (ver Planes B en 03_PLAN_DEL_DIA.md).`

**2. Día y lugar de la competencia** (F2). `docs/01_REGLAMENTO_Y_RUBRICA.md`, primer recuadro:

- Actual: `El cronograma de ONIET ubica "Desarrollo de Sistemas" a las 14 h; confirmar el día.`
- Propuesto: `Según el cronograma oficial (oniet.ubp.edu.ar/cronograma), Desarrollo de Sistemas es el
  **jueves 8 de octubre de 2026, de 14:00 a 16:30**, presencial, en los laboratorios 3 y 4 de la UBP.`

**3. Computadoras y duración** (F4, F5, F6). `docs/01_REGLAMENTO_Y_RUBRICA.md`, segundo recuadro:

- Actual: `la página de la competencia dice que se rinde "en computadoras provistas por la Universidad" y
  menciona una duración de unas 4 horas. Nuestro plan asume notebooks propias y 14:00–16:30.`
- Propuesto: `el Reglamento 012 (2026) dice: "Se utilizarán computadoras del laboratorio de informática
  de la Universidad con entornos de desarrollo preinstalados". No menciona notebooks propias. La cifra
  de "unas 4 horas" es de una página vieja (reglamento 2019); el cronograma 2026 marca 14:00–16:30.
  Nuestro plan asume notebooks propias: hay que confirmarlo por escrito.`

**4. Canales de contacto** (F16, F17). En `README.md` (sección "Urgente", punto 1) y en
`docs/01_REGLAMENTO_Y_RUBRICA.md` (segundo recuadro):

- Actual: `(competencias.oniet@ubp.edu.ar u oniet@ubp.edu.ar)`
- Propuesto: `(mensajería interna del Sistema ONIET u oniet@ubp.edu.ar, los canales oficiales según el
  Reglamento 012)`

**5. Precio del plan Pro de Ollama** (A2, A3).

- `docs/04_IAS_Y_PROMPTS.md`, tabla "Qué IA para qué":
  - Actual: `Grande (plan Pro de Ollama: USD 60/mes, 3 pedidos a la vez)`
  - Propuesto: `Grande (plan Pro de Ollama: USD 20/mes con USD 60 de crédito de uso, 3 pedidos a la vez)`
- `docs/02_CONFIGURAR_NOTEBOOK.md`, §5 Ollama, paso 6:
  - Actual: `6. El plan Pro de Ollama permite **3 pedidos simultáneos** y USD 60 de uso por mes (revisar en
    ollama.com/settings/usage).`
  - Propuesto: `6. El plan Pro de Ollama cuesta USD 20 por mes (o USD 200 por año), incluye USD 60 de
    crédito de uso por mes y permite **3 pedidos simultáneos** (revisar en ollama.com/settings/usage).`

**6. Cupo de Antigravity en el plan gratis** (B17).

- `docs/02_CONFIGURAR_NOTEBOOK.md`, §5 Antigravity, paso 7:
  - Actual: `hay dos grupos con cupo separado ("Gemini" y "Claude y GPT"), cada uno con límite de 5 horas
    y **límite semanal**. **No gastar el cupo los días anteriores a la competencia**: el semanal no se
    repone con el de 5 horas. Anotar qué día se reinicia.`
  - Propuesto: `hay dos grupos con cupo separado ("Gemini" y "Claude y GPT"). En el plan gratis el cupo
    se renueva **una vez por semana** (la renovación cada 5 horas es de los planes Pro y Ultra, aunque
    View Usage muestre las dos barras). **No gastar el cupo los días anteriores a la competencia.**
    Anotar qué día se reinicia.`
- `docs/04_IAS_Y_PROMPTS.md`, tabla "Qué IA para qué", fila Gemini:
  - Actual: `Grupo "Gemini": límite de 5 h + **semanal**`
  - Propuesto: `Grupo "Gemini": cupo **semanal** (plan gratis)`

### Configuración de Antigravity

**7. Opciones de Settings** (B10, B11, B12). `docs/02_CONFIGURAR_NOTEBOOK.md`, §5 Antigravity, paso 5:

- Actual: `- Revisión de artefactos: **Agent Decides**.`
- Propuesto: `- Revisión de artefactos: **Request Review** (la otra opción es Always Proceed).`
- Actual: `- Acceso a archivos fuera del proyecto: **Ask** o **Deny**.`
- Propuesto: `- **Agent Non-Workspace File Access**: desactivado (así viene por defecto).`
- Agregar al renglón de la terminal: `En Windows: Settings → Agent → Terminal Command Auto Execution,
  con las opciones Request Review / Proceed in Sandbox / Always Proceed. En Mac/Linux, el preset se
  elige en Settings → General → Permission Settings (Default / Request Review / Turbo).`

**8. Agente de navegador** (B5, B6). `docs/02_CONFIGURAR_NOTEBOOK.md`, §5 Antigravity, pasos 2 y 6:

- Actual (paso 2): `2. Instalar **Google Chrome** (lo usa el agente de navegador).`
- Propuesto: `2. Instalar **Google Chrome** y ponerlo como **navegador predeterminado** (el comando
  /browser lo exige).`
- Actual (paso 6): `La primera vez aparece "Setup" para instalar la extensión en Chrome.`
- Propuesto: `No hace falta ninguna extensión: el agente controla Chrome con una sesión de depuración
  (CDP).`

**9. Texto del error de HOME** (B9). `docs/02_CONFIGURAR_NOTEBOOK.md` §5, paso 3, y
`docs/09_PROBLEMAS_COMUNES.md`, sección "Las IAs":

- Actual: `"Failed to install playwright: $HOME is not set"`
- Propuesto: `"failed to install playwright: $HOME environment variable is not set"`

**10. Edge en lugar de Chrome** (B26, NO VERIFICABLE). `docs/09_PROBLEMAS_COMUNES.md`:

- Actual: `| Antigravity: el navegador abre Edge en vez de Chrome | Instalar Chrome y ponerlo como navegador predeterminado |`
- Propuesto: `| Antigravity: el agente de navegador no arranca | Instalar Chrome y ponerlo como navegador predeterminado (requisito oficial de /browser) |`

### Ollama y Claude Code

**11. Caché de Ollama** (A10). `docs/04_IAS_Y_PROMPTS.md`:

- Actual: `Ollama no guarda caché: usar `/clear` seguido para no reenviar todo el contexto.`
- Propuesto: `Ollama no acepta el control de caché de Anthropic (`cache_control`): usar `/clear` entre
  tareas distintas para no reenviar todo el contexto.`

**12. "Una cuenta por persona"** (A1).

- `docs/02_CONFIGURAR_NOTEBOOK.md`, §5:
  - Actual: `los términos de Anthropic no lo permiten y los de Ollama indican "una cuenta por persona".`
  - Propuesto: `los términos de Anthropic no lo permiten y las preguntas frecuentes de Ollama
    (ollama.com/pricing) indican "una cuenta por persona".`
- `docs/03_PLAN_DEL_DIA.md`:
  - Actual: `los términos de Anthropic y de Ollama lo piden ("una cuenta por persona").`
  - Propuesto: `lo piden los términos de Anthropic y las preguntas frecuentes de Ollama ("una cuenta
    por persona").`

**13. Alcance de `claude_settings.json`** (C13). `docs/04_IAS_Y_PROMPTS.md`:

- Actual: `y **bloquea** `git push --force`, `git reset --hard` y borrados recursivos.`
- Propuesto: `y **bloquea** las formas más comunes de `git push --force`, `git reset --hard` y los
  borrados recursivos. No es una barrera total (por ejemplo, `rm -fr` no se detecta): igual hay que
  leer cada comando antes de aprobarlo.`
- Mejora opcional para `docs/plantillas/claude_settings.json`: agregar `"Bash(rm *)"` a `ask` para
  que cualquier `rm` pida confirmación. El archivo actual es válido tal como está.

### Windows, Python y Git

**14. Alias de ejecución** (D1). En `docs/02_CONFIGURAR_NOTEBOOK.md` §2, paso 3, y en
`docs/09_PROBLEMAS_COMUNES.md`, primera fila:

- Actual (02): `*Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de
  ejecución de aplicaciones* → desactivar `python.exe` y `python3.exe`.`
- Actual (09): `*Configuración → Aplicaciones → Configuración avanzada → Alias de ejecución de aplicaciones*: desactivar `python.exe` y `python3.exe`.`
- Propuesto (los dos): `Inicio → escribir **Administrar alias de ejecución de aplicaciones** →
  desactivar las entradas de Python del *Instalador de aplicaciones* (`python.exe` y `python3.exe`).`

**15. Versión de Python recomendada** (D4). `docs/02_CONFIGURAR_NOTEBOOK.md` §2, paso 1:

- Actual: `1. Instalar **Python 3.12 o 3.13** desde el instalador `.exe` de python.org, tildando
  **"Add python.exe to PATH"**. Alternativa: `winget install -e --id Python.Python.3.12 --source winget`.`
- Propuesto: `1. Instalar **Python 3.13** desde el instalador `.exe` de python.org, tildando la opción
  para agregar Python al PATH. Alternativa: `winget install -e --id Python.Python.3.13 --source winget`.
  (Python 3.12 solo recibe parches de seguridad y ya no tiene instaladores nuevos para Windows.)`

**16. Inicio de sesión de Git** (D9). En `docs/02_CONFIGURAR_NOTEBOOK.md` §3, paso 4, y en
`docs/06_GIT.md`, Preparación, paso 3:

- Actual (02): `El primer `git push` abre el navegador para iniciar sesión en GitHub (Git Credential Manager).`
- Actual (06): `El primer `push` abre el navegador para iniciar sesión (Git Credential Manager).`
- Propuesto: `El primer `git push` abre una ventana de Git Credential Manager para iniciar sesión en
  GitHub (conviene elegir la opción del navegador).`

**17. Nombre del interruptor del reloj** (D11). `docs/02_CONFIGURAR_NOTEBOOK.md` §1, paso 2:

- Actual: `"Establecer la hora automáticamente" activado`
- Propuesto: `"Ajustar hora automáticamente" activado`
- "Sincronizar ahora" y "(UTC-03:00) Buenos Aires" (D12) quedan como están: son NO VERIFICABLES en la
  página oficial, pero no hay una fuente que diga otra cosa. Probarlo en las notebooks.

### Consignas pasadas

**18.** `docs/07_PRACTICA.md` (F19, F20, F22):

- Actual: `Encontradas en repositorios públicos de participantes (enunciados oficiales en PDF):`
- Propuesto: `Encontradas en repositorios públicos de participantes (enunciados oficiales en PDF o Word;
  la de 2023 se deduce del código de un participante porque no se encontró el enunciado):`
- Fila 2021, actual: `| CSV de datos.gob.ar |` … `top N con menor proporción paquetes/familia y desempate al azar (20 %)`
- Propuesto: `| Dataset de datos.gob.ar (Registro Nacional de Barrios Populares) |` … `los N barrios con
  menor proporción paquetes/familia; si hay muchos en la misma condición, se eligen N al azar (20 %)`
- Fila 2023, actual: `| Control de calidad de producción (según repos de participantes) |`
- Propuesto: `| Control de calidad de producción (deducido del código de un participante) |`

### Mejoras opcionales (los datos del repo no están mal)

- `docs/01`, tabla del reglamento: completar `Lenguajes: Java, JavaScript, PHP, Python, .NET` con
  `(.NET Framework/.NET Core, incluidos VB, C# o C++)`, y `Grupal, hasta 4 integrantes` con
  `y hasta 2 equipos por escuela`.
- `docs/04`: en "Con Claude Pro, el modelo por defecto es Opus" se puede aclarar que `/model sonnet`
  queda guardado como predeterminado para las sesiones siguientes.
- `docs/03` y `docs/04`: dos páginas oficiales de Antigravity se contradicen sobre si Claude Sonnet 4.6
  y Opus 4.6 están en el plan gratis (Models dice que sí, Plans dice "third-party models" solo en
  Ultra). Probar con las cuentas reales antes del día.
- `docs/09`, fila del puerto ocupado: bien como está.

## 4. Prueba con datos reales: Registro Nacional de Barrios Populares

Dataset oficial: https://datos.gob.ar/dataset/registro-nacional-de-barrios-populares (lo encontré
con la API `package_search` de datos.gob.ar). Archivos descargados (no se commitearon):

| Archivo | Tamaño | Codificación |
|---|---|---|
| `20231205_info_publica_datos_barrios.csv` | 1.612.730 bytes | UTF-8 sin BOM |
| `20231205_info_publica.geojson` | 9.435.792 bytes | UTF-8 sin BOM |
| `20231205_info_publica_referencias.csv` | 6.369 bytes | UTF-8 sin BOM |

Entorno: `python3 -m venv .venv` + `pip install -r requirements-dev.txt` (Flask 3.1.3, openpyxl
3.1.5, pytest 9.1.1, ruff 0.16.9, Python 3.11). Los tests del kit pasan todos: `python -m pytest`
da 117 pasados.

### Con `app.servicios.lector.leer_archivo`

| Archivo | Filas leídas | Resultado |
|---|---|---|
| CSV de barrios | **6.467** (filas 2 a 6.468) en 0,04 s | Separador `,` detectado. Las 17 columnas en todas las filas. Todos los valores quedan como texto (`'44'`) |
| GeoJSON (leído como `.json`) | **6.467** (elementos 1 a 6.467) en 0,68 s | Detecta `FeatureCollection` y toma las `properties`. Los números quedan como `int` y las celdas vacías como `None` |
| CSV de referencias | 51 | No es una tabla de datos, es la leyenda de los códigos. El lector toma la fila 2 como encabezado (`si`, `mayoritariamente_las_familias_poseen_titulo_de_propiedad`). Sirve solo para leerlo, no para importarlo |

Encabezados normalizados (iguales en el CSV y en el GeoJSON): `id_renabap`, `nombre_barrio`,
`provincia`, `departamento`, `localidad`, `cantidad_viviendas_aproximadas`,
`cantidad_familias_aproximada`, `decada_de_creacion`, `anio_de_creacion`, `energia_electrica`,
`efluentes_cloacales`, `agua_corriente`, `cocina`, `calefaccion`, `titulo_propiedad`,
`clasificacion_barrio`, `superficie_m2`.

Otros datos: hay 24 provincias (Buenos Aires tiene 2.065 barrios, Santa Fe 469 y Chaco 442).
`anio_de_creacion` está vacío en 4.779 filas. Los acentos se leen bien ("Desagüe", "Década 1990").

### Con el sistema web (cliente de pruebas de Flask, pantalla Importar)

- **CSV** (1,6 MB): el sistema responde bien. Informa "Faltan columnas obligatorias: fecha, producto,
  categoria, cantidad, precio_unitario" y lista las columnas encontradas. Es lo esperado, porque
  todavía está el ejemplo de ventas.
- **GeoJSON** (9,4 MB): se rechaza con la página propia **413 "Archivo muy grande. El máximo
  permitido es 5 MB."** No hay error 500.
- **Importar desde URL**: el CSV se descarga y se leen 6.467 filas. El GeoJSON se rechaza con "Lo
  descargado es demasiado grande." por el mismo límite de 5 MB (`MAX_CONTENT_LENGTH` en
  `app/config.py`).

### Conclusiones para el equipo

1. El lector funciona con los datos oficiales reales: codificación, separador, acentos, encabezados
   y GeoJSON, sin errores.
2. Si la consigna trae un GeoJSON o un archivo de más de 5 MB, hay que subir `MAX_CONTENT_LENGTH`
   en `app/config.py` (por ejemplo, a `16 * 1024 * 1024`). Con el CSV alcanza.
3. `data/practica/barrios_populares.csv` (práctica 5) usa `id_barrio` y `cantidad_familias`, pero el
   archivo real usa `id_renabap` y `cantidad_familias_aproximada`. Al hacer la práctica 5, agregar
   esos nombres a `ALIAS` en `validacion.py`, o practicar directamente con el CSV oficial.
4. En el CSV todos los números llegan como texto. `a_entero` / `a_decimal` ya lo resuelven al validar.
