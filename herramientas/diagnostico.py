"""Diagnóstico de la notebook: ¿está todo listo para la competencia?

Uso (desde la carpeta del proyecto, con el entorno virtual activado):
    python herramientas/diagnostico.py --rol A     integrador (Claude Code + Ollama + Antigravity)
    python herramientas/diagnostico.py --rol B     interfaz (Antigravity)
    python herramientas/diagnostico.py --rol C     pruebas y documentación (Antigravity)

Muestra [ OK  ], [FALLA] (hay que arreglarlo) o [AVISO] (conviene revisarlo).
Ejecutarlo en casa, la noche anterior y al llegar a la competencia.
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
SITIOS = {
    "GitHub": "https://github.com",
    "PyPI (instalar paquetes)": "https://pypi.org/simple/flask/",
    "Ollama": "https://ollama.com",
    "Claude": "https://api.anthropic.com",
    "Antigravity": "https://antigravity.google",
}
fallas: list[str] = []


def informar(nombre: str, ok: bool, detalle: str = "", obligatorio: bool = True) -> None:
    if ok:
        marca = "[ OK  ]"
    elif obligatorio:
        marca = "[FALLA]"
        fallas.append(nombre)
    else:
        marca = "[AVISO]"
    print(f"{marca} {nombre}" + (f" -> {detalle}" if detalle else ""))


def ejecutar(comando: list[str], segundos: int = 20) -> tuple[bool, str]:
    """Ejecuta un comando y devuelve (salió_bien, primera_línea_de_la_salida)."""
    try:
        proceso = subprocess.run(
            comando, cwd=CARPETA_PROYECTO, capture_output=True, text=True, timeout=segundos
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, type(error).__name__
    salida = (proceso.stdout or proceso.stderr).strip().splitlines()
    return proceso.returncode == 0, salida[0] if salida else ""


def revisar_python() -> None:
    version = sys.version_info
    texto = f"{version.major}.{version.minor}.{version.micro}"
    informar("Python 3.10 o superior", version >= (3, 10), texto)
    en_entorno = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    informar("Entorno virtual activado (.venv)", en_entorno, "" if en_entorno else "activalo")
    faltantes = [m for m in ("flask", "openpyxl", "pytest") if not importlib.util.find_spec(m)]
    informar(
        "Paquetes del proyecto instalados",
        not faltantes,
        f"faltan: {', '.join(faltantes)} -> pip install -r requirements-dev.txt"
        if faltantes
        else "",
    )
    informar("ruff instalado", shutil.which("ruff") is not None, obligatorio=False)


def revisar_git() -> None:
    if shutil.which("git") is None:
        informar("Git instalado", False, "instalar Git for Windows")
        return
    _, version = ejecutar(["git", "--version"])
    informar("Git instalado", True, version)
    _, nombre = ejecutar(["git", "config", "user.name"])
    _, correo = ejecutar(["git", "config", "user.email"])
    informar("Git: nombre y correo configurados", bool(nombre and correo), f"{nombre} <{correo}>")
    ok, remoto = ejecutar(["git", "remote", "get-url", "origin"])
    informar("Repositorio con remoto 'origin'", ok, remoto)
    if ok:
        # --dry-run no sube nada, pero pide a GitHub el permiso de escritura (push)
        acceso, detalle = ejecutar(["git", "push", "--dry-run", "origin", "HEAD"], segundos=60)
        informar("Permiso para hacer push a GitHub", acceso, "" if acceso else detalle)


def revisar_reloj() -> None:
    """La hora del commit sale del reloj de la notebook: tiene que estar bien."""
    try:
        pedido = urllib.request.Request("https://www.google.com", method="HEAD")
        try:
            with urllib.request.urlopen(pedido, timeout=8) as respuesta:
                encabezado_fecha = respuesta.headers["Date"]
        except urllib.error.HTTPError as respuesta_con_error:  # igual trae la fecha
            encabezado_fecha = respuesta_con_error.headers["Date"]
        hora_servidor = parsedate_to_datetime(encabezado_fecha)
    except Exception as error:  # sin internet no se puede comparar
        informar("Reloj de la notebook en hora", False, f"no se pudo comparar ({error})", False)
        return
    diferencia = abs((datetime.now(timezone.utc) - hora_servidor).total_seconds())
    informar(
        "Reloj de la notebook en hora",
        diferencia <= 120,
        f"diferencia de {int(diferencia)} s" + ("" if diferencia <= 120 else ": sincronizar hora"),
    )


def revisar_internet() -> None:
    for nombre, url in SITIOS.items():
        try:
            pedido = urllib.request.Request(url, method="HEAD")
            urllib.request.urlopen(pedido, timeout=8).close()
            ok, detalle = True, ""
        except urllib.error.HTTPError:  # respondió (aunque sea con error): hay conexión
            ok, detalle = True, ""
        except Exception as error:
            ok, detalle = False, type(error).__name__
        informar(f"Conexión a {nombre}", ok, detalle, obligatorio=nombre.startswith("GitHub"))


def revisar_puerto(puerto: int = 5000) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
        libre = conexion.connect_ex(("127.0.0.1", puerto)) != 0
    informar(
        f"Puerto {puerto} libre",
        libre,
        "" if libre else "ocupado: cerrá el otro servidor o usá PORT=5001",
        obligatorio=False,
    )


def revisar_herramientas_ia(rol: str) -> None:
    es_integrador = rol == "A"
    for nombre, comando in (("Claude Code", "claude"), ("Ollama", "ollama")):
        if shutil.which(comando) is None:
            informar(f"{nombre} instalado", False, "no encontrado", obligatorio=es_integrador)
            continue
        ok, version = ejecutar([comando, "--version"])
        informar(f"{nombre} instalado", ok, version, obligatorio=es_integrador)
    print("[MANUAL] Antigravity: abrirlo, iniciar sesión y revisar el cupo en View Usage.")
    print("[MANUAL] Google Chrome instalado (lo usa el agente de navegador de Antigravity).")


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnóstico de la notebook para ONIET.")
    parser.add_argument("--rol", choices=["A", "B", "C"], default="A", help="rol en el equipo")
    rol = parser.parse_args().rol

    print(f"Diagnóstico de la notebook (rol {rol})\n")
    revisar_python()
    revisar_git()
    revisar_reloj()
    revisar_internet()
    revisar_puerto()
    revisar_herramientas_ia(rol)

    print()
    if fallas:
        print(f"HAY QUE ARREGLAR: {', '.join(fallas)}. Ver docs/02_CONFIGURAR_NOTEBOOK.md")
        return 1
    print("Notebook lista. Ahora corré: python herramientas/verificar.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
