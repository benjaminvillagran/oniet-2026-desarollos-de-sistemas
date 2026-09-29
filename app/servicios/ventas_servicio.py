"""Alta, baja y vaciado de ventas (operaciones que modifican datos)."""

from __future__ import annotations

from typing import Any

from app.db import transaccion
from app.repositorios import importaciones_repositorio, ventas_repositorio
from app.servicios import procesamiento, validacion


def crear_venta(datos: dict[str, Any]) -> tuple[int | None, dict[str, str]]:
    """Valida y guarda una venta cargada a mano. Devuelve (id_nuevo, {}) o (None, errores)."""
    venta, errores = validacion.validar_venta(datos)
    if errores:
        return None, errores
    with transaccion():
        nuevo_id = ventas_repositorio.insertar(procesamiento.completar_venta(venta))
    return nuevo_id, {}


def eliminar_venta(venta_id: int) -> bool:
    with transaccion():
        return ventas_repositorio.eliminar(venta_id)


def vaciar_datos() -> int:
    """Borra todas las ventas y el historial de importaciones. Devuelve cuántas ventas borró."""
    with transaccion():
        cantidad = ventas_repositorio.eliminar_todas()
        importaciones_repositorio.eliminar_todas()
    return cantidad
