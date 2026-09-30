"""Verificación completa del proyecto: ¿está todo bien para hacer push / entregar?

Uso (desde la carpeta del proyecto, con el entorno virtual activado):
    python herramientas/verificar.py            revisa todo
    python herramientas/verificar.py --arreglar primero corrige el formato automáticamente

Revisa lo mismo que el workflow de GitHub Actions (tests + estilo) y además que el sistema
arranque y que las páginas principales respondan. Termina con código 1 si algo falla.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent

fallas: list[str] = []


def registrar(nombre: str, ok: bool, detalle: str = "", obligatorio: bool = True) -> None:
    """Muestra el resultado. Lo no obligatorio se muestra como AVISO y no frena el push."""
    if ok:
        marca = "[ OK  ]"
    elif obligatorio:
        marca = "[FALLA]"
        fallas.append(nombre)
    else:
        marca = "[AVISO]"
    linea = f"{marca} {nombre}" + (f" -> {detalle}" if detalle else "")
    print(linea)
    resumen_github = os.environ.get("GITHUB_STEP_SUMMARY")  # resumen visible en GitHub Actions
    if resumen_github:
        with open(resumen_github, "a", encoding="utf-8") as archivo:
            archivo.write(f"- `{marca}` {nombre}" + (f": {detalle}" if detalle else "") + "\n")


def ejecutar(comando: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(comando, cwd=CARPETA_PROYECTO, capture_output=True, text=True)


def revisar_tests() -> None:
    proceso = ejecutar([sys.executable, "-m", "pytest"])
    resumen = re.findall(r"\d+ (?:passed|failed|errors?)[^\n]*", proceso.stdout)
    registrar("Tests automáticos (pytest)", proceso.returncode == 0, (resumen or [""])[-1])
    if proceso.returncode != 0:
        print(proceso.stdout[-3000:])


def revisar_estilo(arreglar: bool) -> None:
    ruff = [sys.executable, "-m", "ruff"]  # el ruff del mismo entorno que este Python
    if ejecutar([*ruff, "--version"]).returncode != 0:
        registrar(
            "Estilo de código (ruff)",
            False,
            "ruff no está instalado: pip install -r requirements-dev.txt",
            obligatorio=False,
        )
        return
    if arreglar:
        ejecutar([*ruff, "format", "."])
        ejecutar([*ruff, "check", "--fix", "."])
    chequeo = ejecutar([*ruff, "check", "."])
    formato = ejecutar([*ruff, "format", "--check", "."])
    ok = chequeo.returncode == 0 and formato.returncode == 0
    if ok:
        detalle = ""
    elif arreglar:
        detalle = "quedan errores que ruff no arregla solo: corregilos a mano (ver abajo)"
    else:
        detalle = "corré: python herramientas/verificar.py --arreglar"
    registrar("Estilo de código (ruff)", ok, detalle)
    if chequeo.returncode != 0:
        print(chequeo.stdout[-3000:])


def paginas_del_sistema(app) -> list[str]:
    """Todas las páginas GET sin parámetros (se toman de las rutas reales del sistema)."""
    return sorted(
        regla.rule
        for regla in app.url_map.iter_rules()
        if "GET" in regla.methods and not regla.arguments and regla.endpoint != "static"
    )


def revisar_arranque() -> None:
    """Levanta el sistema con una base temporal y pide todas sus páginas."""
    sys.path.insert(0, str(CARPETA_PROYECTO))
    try:
        from app import create_app

        with tempfile.TemporaryDirectory() as carpeta:
            # Con el login apagado para poder revisar las páginas (si no, todas redirigen al login)
            app = create_app(
                {
                    "TESTING": True,
                    "DATABASE": str(Path(carpeta) / "verif.db"),
                    "LOGIN_OBLIGATORIO": False,
                }
            )
            cliente = app.test_client()
            paginas = paginas_del_sistema(app)
            fallidas = [url for url in paginas if cliente.get(url).status_code >= 400]
        detalle = ", ".join(fallidas) if fallidas else f"{len(paginas)} páginas"
        registrar("El sistema arranca y responde", not fallidas, detalle)
    except Exception as error:  # cualquier error acá significa que el sistema no arranca
        registrar("El sistema arranca y responde", False, f"{type(error).__name__}: {error}")


SECCIONES_README = ("## Cómo ejecutarlo", "## Funcionalidades", "## Uso de inteligencia artificial")


def revisar_entrega() -> None:
    readme = CARPETA_PROYECTO / "README.md"
    texto = readme.read_text(encoding="utf-8") if readme.exists() else ""
    faltan = [seccion.lstrip("# ") for seccion in SECCIONES_README if seccion not in texto]
    pendientes = texto.count("COMPLETAR")
    problemas = []
    if pendientes:
        problemas.append(f"{pendientes} 'COMPLETAR'")
    if faltan:
        problemas.append(f"faltan secciones: {', '.join(faltan)}")
    registrar(
        "README de entrega completo",
        not problemas,
        "; ".join(problemas) + (" (usar docs/plantillas/README_ENTREGA.md)" if problemas else ""),
        obligatorio=False,
    )

    if shutil.which("git"):
        estado = ejecutar(["git", "status", "--porcelain"])
        if estado.returncode != 0:
            registrar("Todo commiteado", False, "no es un repositorio git", obligatorio=False)
            return
        cambios = [linea for linea in estado.stdout.splitlines() if linea.strip()]
        detalle = f"{len(cambios)} archivos sin commit" if cambios else ""
        registrar("Todo commiteado", not cambios, detalle, obligatorio=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica el proyecto antes de un push.")
    parser.add_argument("--arreglar", action="store_true", help="corrige el formato antes")
    parser.add_argument("--solo-codigo", action="store_true", help="omite README y git")
    argumentos = parser.parse_args()

    print("Verificando el proyecto...\n")
    revisar_tests()
    revisar_estilo(argumentos.arreglar)
    revisar_arranque()
    if not argumentos.solo_codigo:
        revisar_entrega()

    print()
    if fallas:
        print(f"HAY PROBLEMAS: {', '.join(fallas)}. No hagas push hasta arreglarlos.")
        return 1
    print("Todo en orden: podés hacer commit y push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
