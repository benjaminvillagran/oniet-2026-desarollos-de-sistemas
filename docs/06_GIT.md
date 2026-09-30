# 06 · Git y GitHub para el equipo

La entrega es el repositorio y **la hora del último commit es la hora de entrega**. El versionado
vale 10 puntos: commits frecuentes de los 3, mensajes claros y entrega a tiempo.

## Estrategia: todos en `main`, cada uno con sus archivos

Es el modelo de "repositorio compartido" que GitHub describe para equipos chicos. Los conflictos
aparecen cuando dos personas cambian **las mismas líneas del mismo archivo**; por eso cada uno
trabaja en sus carpetas (ver roles en `03_PLAN_DEL_DIA.md`):

- **A**: `app/schema.sql`, `app/servicios/`, `app/repositorios/`, `app/rutas/`, `app/config.py`
- **B**: `app/templates/`, `app/static/`
- **C**: `tests/`, `data/`, `README.md`, `docs/`

No usamos ramas ni pull requests el día de la competencia: suman pasos y los conflictos aparecen
igual. El workflow de GitHub Actions avisa si un push rompió algo.

## Preparación (una sola vez, en casa)

1. **A** crea el repositorio de entrega en GitHub. Conviene **público** (sin claves ni `.env`):
   en un repositorio personal privado no se puede dar acceso de solo lectura al jurado. Confirmar
   con la organización.
2. **A** invita a B y C: *Settings → Collaborators → Add people*. Ellos aceptan desde el mail o las
   notificaciones de GitHub. Hacerlo días antes: hay un límite de invitaciones por día.
3. Cada uno, en su notebook (Git for Windows ya instalado):

   ```bash
   git config --global user.name "Nombre Apellido"
   git config --global user.email "el-mismo-mail-de-su-cuenta-de-github"
   git config --global pull.rebase false
   git clone https://github.com/USUARIO/REPOSITORIO.git
   ```

   Si el mail no es el de la cuenta de GitHub, los commits no aparecen como suyos.
   El primer `git push` abre una ventana de Git Credential Manager para iniciar sesión en
   GitHub (conviene elegir la opción del navegador).
4. Cada uno hace un **commit y push de prueba** para confirmar que tiene permiso.
5. Reloj sincronizado: *Configuración → Hora e idioma → Fecha y hora → Sincronizar ahora*.

## El ciclo de trabajo (cada 15 a 20 minutos)

Desde la terminal:

```bash
git add -A
git commit -m "feat: importación de préstamos con validación"
git pull
python herramientas/verificar.py
git push
```

Desde Antigravity (panel **Source Control**, el ícono de ramas): escribir el mensaje, **Commit**,
después **Sync Changes** (hace `pull` y `push`).

**Antes de pedirle a la IA un cambio grande: commit.** Si el cambio sale mal, se vuelve atrás.

## Mensajes de commit (Conventional Commits)

Formato: `tipo: descripción en minúscula`. Tipos que vamos a usar:

| Tipo | Para | Ejemplo |
|---|---|---|
| `feat` | Funcionalidad nueva | `feat: tabla de posiciones del torneo` |
| `fix` | Arreglo de un error | `fix: redondeo del total a 2 decimales` |
| `test` | Tests | `test: casos de goles negativos y equipo repetido` |
| `style` | Cambios visuales o de formato | `style: colores y espaciado del listado` |
| `refactor` | Reorganizar sin cambiar lo que hace | `refactor: separar consultas de partidos` |
| `docs` | README y documentación | `docs: instrucciones de ejecución en el README` |
| `chore` | Tareas varias | `chore: datos de ejemplo de la consigna` |

## Conflictos

Pasa cuando dos personas cambiaron las mismas líneas. Git marca el archivo así:

```
<<<<<<< HEAD
lo que tenías vos
=======
lo que venía de GitHub
>>>>>>> ...
```

1. En Antigravity, el archivo aparece en *Merge Changes*. Arriba de cada conflicto hay botones:
   **Accept Current** (lo tuyo), **Accept Incoming** (lo del compañero), **Accept Both** (las dos).
   También se puede abrir **Resolve in Merge Editor**.
2. Elegir, revisar que no queden marcas `<<<<<<<`, `=======` ni `>>>>>>>`, guardar.
3. `python herramientas/verificar.py`, commit y push.
4. Si no se entiende: `git merge --abort` (vuelve a como estaba antes del `pull`) y avisar a **A**.

## Emergencias

| Situación | Comando |
|---|---|
| Rompí un archivo y no lo commiteé | `git restore ruta/al/archivo` |
| Quiero descartar TODO lo que no commiteé | `git restore .` (pensarlo dos veces) |
| Tengo cambios a medias y necesito hacer `pull` | `git stash push -u -m "a medias"` → `git pull` → `git stash pop` |
| Un commit ya pusheado rompió todo | `git revert <código-del-commit> --no-edit` y `git push` |
| "Perdí" un commit | `git reflog` muestra todo lo que pasó; pedir ayuda a A |
| `fatal: Need to specify how to reconcile divergent branches` | `git config pull.rebase false` y repetir `git pull` |

**Prohibido**: `git push --force`, `git reset --hard`, borrar la carpeta y volver a clonar sin
avisar. Si la IA propone alguno de estos comandos, **no se aprueba**.

## Entrega final (16:00 a 16:05, lo hace A)

1. B y C hacen su último `pull` y `push` y avisan "listo".
2. A: `git pull`, `python herramientas/verificar.py`, commit final y `git push`.
3. A: `git tag -a entrega-final -m "Entrega ONIET 2026"` y `git push origin entrega-final`.
4. Revisar en GitHub: último commit, README y pestaña **Actions** en verde.
5. Comparar la hora: `git log -1 --format=fuller` (muestra la fecha de autor y la de commit).
6. **Después de las 16:15 nadie hace commits ni cambios en GitHub** (ni siquiera desde la web).
