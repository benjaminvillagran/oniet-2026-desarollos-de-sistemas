"""Acceso a la tabla `usuarios`. Solo SQL. No hace commit (ver `transaccion()`)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.db import obtener_db


def _ahora() -> str:
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def crear(nombre_usuario: str, clave_hash: str) -> int:
    cursor = obtener_db().execute(
        "INSERT INTO usuarios (nombre_usuario, clave_hash, creado) VALUES (?, ?, ?)",
        (nombre_usuario, clave_hash, _ahora()),
    )
    return cursor.lastrowid


def obtener_por_nombre(nombre_usuario: str) -> dict[str, Any] | None:
    fila = (
        obtener_db()
        .execute("SELECT * FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,))
        .fetchone()
    )
    return dict(fila) if fila else None


def obtener_por_id(usuario_id: int) -> dict[str, Any] | None:
    fila = obtener_db().execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    return dict(fila) if fila else None


def registrar_acceso(usuario_id: int) -> None:
    obtener_db().execute(
        "UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?", (_ahora(), usuario_id)
    )


def actualizar_clave(usuario_id: int, clave_hash: str) -> None:
    obtener_db().execute(
        "UPDATE usuarios SET clave_hash = ? WHERE id = ?", (clave_hash, usuario_id)
    )
