"""PASO 5 - SALIDA: los 3 informes de la consigna y la exportación de resultados."""

from __future__ import annotations

import csv
import io
from typing import Any

from app.repositorios import servicios_repositorio
from app.repositorios.servicios_repositorio import FiltrosServicios
from app.servicios import procesamiento

COLUMNAS_EXPORTACION = (
    "numero_registro",
    "operador_logistico",
    "anio",
    "mes",
    "cantidad_envios",
    "region",
    "costo_por_envio",
    "porcentaje_entregas_atiempo",
    "costo_total",
)


def obtener_informes(filtros: FiltrosServicios | None = None) -> dict[str, Any]:
    servicios = servicios_repositorio.listar_todas(filtros)
    return procesamiento.generar_informes(servicios)


def exportar_csv(filtros: FiltrosServicios | None = None) -> str:
    """CSV para Excel en español: separado por ';' y con coma decimal."""
    salida = io.StringIO()
    escritor = csv.writer(salida, delimiter=";", lineterminator="\n")
    escritor.writerow(COLUMNAS_EXPORTACION)
    for servicio in servicios_repositorio.listar_todas(filtros):
        escritor.writerow([celda_para_excel(servicio[columna]) for columna in COLUMNAS_EXPORTACION])
    return salida.getvalue()


def celda_para_excel(valor: Any) -> Any:
    """Prepara un valor para que Excel lo muestre bien y sin riesgos.

    - Decimales con coma (1200,5), que es lo que espera Excel configurado en español.
    - Un texto que empieza con = + - @ se antepone con ' para que Excel no lo ejecute como fórmula.
    """
    if isinstance(valor, float):
        return str(valor).replace(".", ",")
    if isinstance(valor, str) and valor[:1] in ("=", "+", "-", "@"):
        return "'" + valor
    return valor
