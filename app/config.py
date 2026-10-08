"""Configuración general del sistema."""

import os
import secrets
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_INSTANCIA = CARPETA_PROYECTO / "instance"  # datos locales: no se suben a git


def _clave_secreta() -> str:
    """Clave para firmar la sesión (login). Se genera al azar una sola vez y queda en instance/.

    Así no hay una clave fija publicada en el repositorio con la que alguien pueda falsificar
    una sesión.
    """
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    archivo = CARPETA_INSTANCIA / "clave_secreta.txt"
    try:
        if archivo.exists():
            return archivo.read_text(encoding="utf-8").strip()
        CARPETA_INSTANCIA.mkdir(parents=True, exist_ok=True)
        clave = secrets.token_hex(32)
        archivo.write_text(clave, encoding="utf-8")
        return clave
    except OSError:  # sin permiso de escritura: clave nueva en cada arranque
        return secrets.token_hex(32)


class Config:
    # Datos que se muestran en la interfaz (cambiarlos el día de la competencia)
    NOMBRE_SISTEMA = "Logística Nacional · Análisis de servicios"
    NOMBRE_EQUIPO = "Equipo 14 · Arena, Tapia, Villagrán"
    # Login: False = el sistema se usa sin usuarios. Cambiar a True si la consigna pide iniciar sesión.
    LOGIN_OBLIGATORIO = False

    SECRET_KEY = _clave_secreta()
    SESSION_COOKIE_SAMESITE = "Lax"  # el navegador no manda la sesión en pedidos de otros sitios
    DATABASE = os.environ.get("DATABASE", str(CARPETA_INSTANCIA / "datos.db"))
    CARPETA_EJEMPLOS = CARPETA_PROYECTO / "data" / "ejemplos"

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # tamaño máximo de archivo a importar: 5 MB
    REGISTROS_POR_PAGINA = 20
