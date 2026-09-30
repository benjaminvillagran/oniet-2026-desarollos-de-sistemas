"""Acceso a la tabla `importaciones` (historial de archivos cargados)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.db import obtener_db


def registrar(
    nombre_archivo: str,
    filas_leidas: int,
    filas_guardadas: int,
    filas_con_error: int,
    hash_contenido: str | None = None,
) -> int:
    cursor = obtener_db().execute(
        """
        INSERT INTO importaciones
            (nombre_archivo, fecha_hora, filas_leidas, filas_guardadas, filas_con_error,
             hash_contenido)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            nombre_archivo,
            datetime.now().isoformat(sep=" ", timespec="seconds"),
            filas_leidas,
            filas_guardadas,
            filas_con_error,
            hash_contenido,
        ),
    )
    return cursor.lastrowid


def buscar_por_hash(hash_contenido: str) -> dict[str, Any] | None:
    """La importación anterior de un archivo con exactamente el mismo contenido (si existe)."""
    fila = (
        obtener_db()
        .execute(
            "SELECT * FROM importaciones WHERE hash_contenido = ? ORDER BY id DESC LIMIT 1",
            (hash_contenido,),
        )
        .fetchone()
    )
    return dict(fila) if fila else None


def listar_recientes(limite: int = 50) -> list[dict[str, Any]]:
    filas = obtener_db().execute("SELECT * FROM importaciones ORDER BY id DESC LIMIT ?", (limite,))
    return [dict(fila) for fila in filas]


def eliminar_todas() -> int:
    return obtener_db().execute("DELETE FROM importaciones").rowcount
