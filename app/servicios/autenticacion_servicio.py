"""Registro, inicio de sesión y cambio de clave de usuarios.

Las claves se guardan con hash (werkzeug.security, que viene con Flask): si alguien lee la base
de datos, no puede ver las claves reales.
"""

from __future__ import annotations

import re
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import transaccion
from app.repositorios import usuarios_repositorio
from app.utils.conversiones import normalizar_texto

LARGO_MINIMO_CLAVE = 6
NOMBRE_VALIDO = re.compile(r"^[A-Za-z0-9._-]{3,30}$")


def _errores_de_clave(clave: str, confirmacion: str) -> dict[str, str]:
    if len(clave) < LARGO_MINIMO_CLAVE:
        return {"clave": f"Tiene que tener al menos {LARGO_MINIMO_CLAVE} caracteres."}
    if clave != confirmacion:
        return {"confirmacion": "Las claves no coinciden."}
    return {}


def registrar_usuario(
    nombre_usuario: str, clave: str, confirmacion: str
) -> tuple[int | None, dict[str, str]]:
    """Crea un usuario. Devuelve (id, {}) o (None, {campo: mensaje})."""
    nombre_usuario = normalizar_texto(nombre_usuario)
    errores: dict[str, str] = {}
    if not NOMBRE_VALIDO.match(nombre_usuario):
        errores["nombre_usuario"] = "De 3 a 30 caracteres: letras, números, punto, guion o _."
    elif usuarios_repositorio.obtener_por_nombre(nombre_usuario):
        errores["nombre_usuario"] = "Ese nombre de usuario ya existe."
    errores.update(_errores_de_clave(clave, confirmacion))
    if errores:
        return None, errores
    with transaccion():
        nuevo_id = usuarios_repositorio.crear(nombre_usuario, generate_password_hash(clave))
    return nuevo_id, {}


def autenticar(nombre_usuario: str, clave: str) -> dict[str, Any] | None:
    """Devuelve el usuario si la clave es correcta (con su acceso ANTERIOR), o None.

    Registra la fecha y hora de este acceso como el nuevo "último acceso".
    """
    usuario = usuarios_repositorio.obtener_por_nombre(normalizar_texto(nombre_usuario))
    if usuario is None or not check_password_hash(usuario["clave_hash"], clave):
        return None
    with transaccion():
        usuarios_repositorio.registrar_acceso(usuario["id"])
    return usuario


def cambiar_clave(
    usuario_id: int, clave_actual: str, clave_nueva: str, confirmacion: str
) -> dict[str, str]:
    usuario = usuarios_repositorio.obtener_por_id(usuario_id)
    if usuario is None or not check_password_hash(usuario["clave_hash"], clave_actual):
        return {"clave_actual": "La clave actual no es correcta."}
    errores = _errores_de_clave(clave_nueva, confirmacion)
    if errores:
        return errores
    with transaccion():
        usuarios_repositorio.actualizar_clave(usuario_id, generate_password_hash(clave_nueva))
    return {}
