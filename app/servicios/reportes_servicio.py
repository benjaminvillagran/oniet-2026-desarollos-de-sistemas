"""PASO 5 - SALIDA: estadísticas y exportación de resultados."""

from __future__ import annotations

import csv
import io
from typing import Any

from app.repositorios import ventas_repositorio
from app.repositorios.ventas_repositorio import FiltrosVentas
from app.servicios import procesamiento

COLUMNAS_EXPORTACION = (
    "id",
    "fecha",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "total",
)


def obtener_estadisticas(filtros: FiltrosVentas | None = None) -> dict[str, Any]:
    ventas = ventas_repositorio.listar_todas(filtros)
    return procesamiento.generar_estadisticas(ventas)


def exportar_csv(filtros: FiltrosVentas | None = None) -> str:
    """CSV separado por ';' (lo abre bien Excel en español). Se puede volver a importar."""
    salida = io.StringIO()
    escritor = csv.writer(salida, delimiter=";", lineterminator="\n")
    escritor.writerow(COLUMNAS_EXPORTACION)
    for venta in ventas_repositorio.listar_todas(filtros):
        escritor.writerow([venta[columna] for columna in COLUMNAS_EXPORTACION])
    return salida.getvalue()
