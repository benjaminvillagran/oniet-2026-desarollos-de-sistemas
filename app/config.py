"""Configuración general del sistema."""

import os
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent


class Config:
    # Datos que se muestran en la interfaz (cambiarlos el día de la competencia)
    NOMBRE_SISTEMA = "Sistema de Gestión de Ventas"
    NOMBRE_EQUIPO = "Equipo ONIET 2026"

    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")
    DATABASE = os.environ.get("DATABASE", str(CARPETA_PROYECTO / "instance" / "datos.db"))
    CARPETA_EJEMPLOS = CARPETA_PROYECTO / "data" / "ejemplos"

    # Login: False = el sistema se usa sin usuarios. Poner True si la consigna pide iniciar sesión.
    LOGIN_OBLIGATORIO = os.environ.get("LOGIN_OBLIGATORIO", "0") == "1"

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # tamaño máximo de archivo a importar: 5 MB
    REGISTROS_POR_PAGINA = 20
