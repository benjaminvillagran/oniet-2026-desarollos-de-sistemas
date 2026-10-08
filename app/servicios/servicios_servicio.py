"""Baja de servicios y vaciado de datos (coordinan las transacciones)."""

from __future__ import annotations

from app.db import transaccion
from app.repositorios import importaciones_repositorio, servicios_repositorio


def eliminar_servicio(servicio_id: int) -> bool:
    with transaccion():
        return servicios_repositorio.eliminar(servicio_id)


def vaciar_datos() -> int:
    """Borra todos los servicios y el historial de importaciones."""
    with transaccion():
        cantidad = servicios_repositorio.eliminar_todas()
        importaciones_repositorio.eliminar_todas()
    return cantidad
