"""PASO 3 - PROCESAMIENTO: cálculos e informes sobre los servicios logísticos.

Son funciones "puras": reciben datos y devuelven resultados, sin tocar la base de datos.
Por eso son fáciles de probar (ver tests/test_procesamiento.py).
"""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Any

from app.utils.conversiones import redondear_dinero

Servicio = dict[str, Any]


def calcular_costo_total(cantidad_envios: int, costo_por_envio: float) -> float:
    """Costo total = CantidadEnvios x CostoPorEnvio (fórmula de la consigna)."""
    return redondear_dinero(cantidad_envios * costo_por_envio)


def completar_servicio(servicio: Servicio) -> Servicio:
    """Agrega el campo calculado de cada fila (se guarda al importar)."""
    costo = calcular_costo_total(servicio["cantidad_envios"], servicio["costo_por_envio"])
    return {**servicio, "costo_total": costo}


def asignar_posiciones(filas: list[dict[str, Any]], campo: str) -> list[dict[str, Any]]:
    """Agrega "posicion" a filas YA ordenadas. Si empatan en `campo`, comparten posición (1, 2, 2, 4)."""
    for indice, fila in enumerate(filas):
        if indice > 0 and fila[campo] == filas[indice - 1][campo]:
            fila["posicion"] = filas[indice - 1]["posicion"]
        else:
            fila["posicion"] = indice + 1
    return filas


def ranking_operadores(servicios: list[Servicio]) -> list[dict[str, Any]]:
    """Reporte 1: operadores de mayor a menor costo total (con su total de envíos)."""
    envios: dict[str, int] = defaultdict(int)
    costos: dict[str, float] = defaultdict(float)
    for servicio in servicios:
        envios[servicio["operador_logistico"]] += servicio["cantidad_envios"]
        costos[servicio["operador_logistico"]] += servicio["costo_total"]
    filas = [
        {"operador": operador, "total_envios": envios[operador], "costo_total": round(costo, 2)}
        for operador, costo in costos.items()
    ]
    filas.sort(key=lambda fila: (-fila["costo_total"], fila["operador"]))
    return asignar_posiciones(filas, "costo_total")


def ranking_regiones(servicios: list[Servicio]) -> list[dict[str, Any]]:
    """Reporte 2: regiones de mayor a menor cantidad de envíos."""
    envios: dict[str, int] = defaultdict(int)
    for servicio in servicios:
        envios[servicio["region"]] += servicio["cantidad_envios"]
    filas = [{"region": region, "cantidad_envios": total} for region, total in envios.items()]
    filas.sort(key=lambda fila: (-fila["cantidad_envios"], fila["region"]))
    return asignar_posiciones(filas, "cantidad_envios")


def cumplimiento_por_operador(servicios: list[Servicio]) -> list[dict[str, Any]]:
    """Reporte 3: promedio simple del % de entregas a tiempo de cada operador, de mayor a menor."""
    porcentajes: dict[str, list[float]] = defaultdict(list)
    for servicio in servicios:
        porcentajes[servicio["operador_logistico"]].append(servicio["porcentaje_entregas_atiempo"])
    filas = [
        {"operador": operador, "promedio": round(sum(valores) / len(valores), 2)}
        for operador, valores in porcentajes.items()
    ]
    filas.sort(key=lambda fila: (-fila["promedio"], fila["operador"]))
    return asignar_posiciones(filas, "promedio")


def resumen_general(servicios: list[Servicio]) -> dict[str, Any]:
    """Totales del período: registros, envíos, costo total y promedio de entregas a tiempo."""
    if not servicios:
        return {"registros": 0, "total_envios": 0, "costo_total": 0.0, "promedio_a_tiempo": 0.0}
    promedio = sum(servicio["porcentaje_entregas_atiempo"] for servicio in servicios) / len(
        servicios
    )
    return {
        "registros": len(servicios),
        "total_envios": sum(servicio["cantidad_envios"] for servicio in servicios),
        "costo_total": round(sum(servicio["costo_total"] for servicio in servicios), 2),
        "promedio_a_tiempo": round(promedio, 2),
    }


def generar_informes(servicios: list[Servicio]) -> dict[str, Any]:
    """Los 3 informes de la consigna y el resumen (los usan la página de informes y la API)."""
    return {
        "resumen": resumen_general(servicios),
        "operadores": ranking_operadores(servicios),
        "regiones": ranking_regiones(servicios),
        "cumplimiento": cumplimiento_por_operador(servicios),
    }


def primeros_n(
    elementos: list[dict[str, Any]],
    clave: str,
    n: int,
    mayor_primero: bool = True,
    azar: random.Random | None = None,
) -> list[dict[str, Any]]:
    """Los N primeros según `clave`. Si hay empate, se desempata AL AZAR.

    Para que los tests den siempre lo mismo se pasa un azar con semilla fija:
    primeros_n(..., azar=random.Random(1)).
    """
    mezclados = list(elementos)
    (azar or random.Random()).shuffle(mezclados)  # primero se desordena al azar...
    mezclados.sort(key=lambda elemento: elemento[clave], reverse=mayor_primero)
    return mezclados[: max(n, 0)]  # ...y como sort es estable, los empates quedan al azar
