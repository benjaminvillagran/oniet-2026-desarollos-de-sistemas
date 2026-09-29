"""Verificación completa del proyecto: ¿está todo bien para hacer push / entregar?

Uso (desde la carpeta del proyecto, con el entorno virtual activado):
    python herramientas/verificar.py            revisa todo
    python herramientas/verificar.py --arreglar primero corrige el formato automáticamente

Revisa lo mismo que el workflow de GitHub Actions (tests + estilo) y además que el sistema
arranque y que las páginas principales respondan. Termina con código 1 si algo falla.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
PAGINAS_PRINCIPALES = ["/", "/importar/", "/importar/historial", "/ventas/", "/estadisticas"]

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
    print(f"{marca} {nombre}" + (f" -> {detalle}" if detalle else ""))


def ejecutar(comando: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(comando, cwd=CARPETA_PROYECTO, capture_output=True, text=True)


def revisar_tests() -> None:
    proceso = ejecutar([sys.executable, "-m", "pytest"])
    resumen = re.findall(r"\d+ (?:passed|failed|errors?)[^\n]*", proceso.stdout)
    registrar("Tests automáticos (pytest)", proceso.returncode == 0, (resumen or [""])[-1])
    if proceso.returncode != 0:
        print(proceso.stdout[-3000:])


def revisar_estilo(arreglar: bool) -> None:
    ruff = shutil.which("ruff")
    if ruff is None:
        registrar("Estilo de código (ruff)", True, "ruff no instalado, se omite")
        return
    if arreglar:
        ejecutar([ruff, "format", "."])
        ejecutar([ruff, "check", "--fix", "."])
    chequeo = ejecutar([ruff, "check", "."])
    formato = ejecutar([ruff, "format", "--check", "."])
    ok = chequeo.returncode == 0 and formato.returncode == 0
    detalle = "" if ok else "corré: python herramientas/verificar.py --arreglar"
    registrar("Estilo de código (ruff)", ok, detalle)
    if chequeo.returncode != 0:
        print(chequeo.stdout[-3000:])


def revisar_arranque() -> None:
    """Levanta el sistema con una base temporal y pide las páginas principales."""
    sys.path.insert(0, str(CARPETA_PROYECTO))
    try:
        from app import create_app

        with tempfile.TemporaryDirectory() as carpeta:
            app = create_app({"TESTING": True, "DATABASE": str(Path(carpeta) / "verif.db")})
            cliente = app.test_client()
            fallidas = [url for url in PAGINAS_PRINCIPALES if cliente.get(url).status_code != 200]
        registrar("El sistema arranca y responde", not fallidas, ", ".join(fallidas))
    except Exception as error:  # cualquier error acá significa que el sistema no arranca
        registrar("El sistema arranca y responde", False, f"{type(error).__name__}: {error}")


def revisar_entrega() -> None:
    readme = CARPETA_PROYECTO / "README.md"
    pendientes = readme.read_text(encoding="utf-8").count("COMPLETAR") if readme.exists() else 1
    registrar(
        "README sin partes por completar", pendientes == 0, f"{pendientes} 'COMPLETAR'", False
    )

    if shutil.which("git"):
        estado = ejecutar(["git", "status", "--porcelain"])
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
