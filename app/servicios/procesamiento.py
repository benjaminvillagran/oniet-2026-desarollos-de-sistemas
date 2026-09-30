"""PASO 3 - PROCESAMIENTO: cálculos y estadísticas sobre las ventas.

Son funciones "puras": reciben datos y devuelven resultados, sin tocar la base de datos.
Por eso son fáciles de probar (ver tests/test_procesamiento.py).
Al adaptar la plantilla, acá van los cálculos que pida la consigna.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.utils.conversiones import redondear_dinero

Venta = dict[str, Any]


def calcular_total(cantidad: int, precio_unitario: float) -> float:
    return redondear_dinero(cantidad * precio_unitario)


def completar_venta(venta: Venta) -> Venta:
    """Agrega los campos calculados a una venta ya validada."""
    return {**venta, "total": calcular_total(venta["cantidad"], venta["precio_unitario"])}


def resumen_general(ventas: list[Venta]) -> dict[str, Any]:
    if not ventas:
        return {
            "cantidad_ventas": 0,
            "unidades": 0,
            "facturacion_total": 0.0,
            "ticket_promedio": 0.0,
            "venta_maxima": None,
            "fecha_desde": None,
            "fecha_hasta": None,
        }
    facturacion = round(sum(venta["total"] for venta in ventas), 2)
    fechas = [venta["fecha"] for venta in ventas]
    return {
        "cantidad_ventas": len(ventas),
        "unidades": sum(venta["cantidad"] for venta in ventas),
        "facturacion_total": facturacion,
        "ticket_promedio": round(facturacion / len(ventas), 2),
        "venta_maxima": max(ventas, key=lambda venta: venta["total"]),
        "fecha_desde": min(fechas),
        "fecha_hasta": max(fechas),
    }


def sumar_por(ventas: list[Venta], clave: str, campo: str = "total") -> list[dict[str, Any]]:
    """Agrupa por `clave` y suma `campo`, con el porcentaje de cada grupo sobre el total.

    Devuelve [{"nombre", "valor", "porcentaje"}, ...] ordenado de mayor a menor valor.
    """
    acumulado: dict[str, float] = defaultdict(float)
    for venta in ventas:
        acumulado[venta[clave]] += venta[campo]
    total = sum(acumulado.values())
    grupos = [
        {
            "nombre": nombre,
            "valor": round(valor, 2),
            "porcentaje": round(valor * 100 / total, 1) if total else 0.0,
        }
        for nombre, valor in acumulado.items()
    ]
    grupos.sort(key=lambda grupo: (-grupo["valor"], grupo["nombre"]))
    return grupos


def facturacion_por_categoria(ventas: list[Venta]) -> list[dict[str, Any]]:
    return sumar_por(ventas, "categoria")


def facturacion_por_mes(ventas: list[Venta]) -> list[dict[str, Any]]:
    """[{"mes": "2026-03", "valor": ...}, ...] ordenado cronológicamente."""
    por_mes: dict[str, float] = defaultdict(float)
    for venta in ventas:
        por_mes[venta["fecha"][:7]] += venta["total"]
    return [{"mes": mes, "valor": round(valor, 2)} for mes, valor in sorted(por_mes.items())]


def ranking_productos(ventas: list[Venta], limite: int = 5) -> list[dict[str, Any]]:
    """Los productos que más facturaron, con sus unidades vendidas."""
    unidades: dict[str, int] = defaultdict(int)
    facturacion: dict[str, float] = defaultdict(float)
    for venta in ventas:
        unidades[venta["producto"]] += venta["cantidad"]
        facturacion[venta["producto"]] += venta["total"]
    ranking = [
        {"producto": producto, "unidades": unidades[producto], "facturacion": round(valor, 2)}
        for producto, valor in facturacion.items()
    ]
    ranking.sort(key=lambda fila: (-fila["facturacion"], fila["producto"]))
    return ranking[:limite]


def generar_estadisticas(ventas: list[Venta]) -> dict[str, Any]:
    """Todas las estadísticas juntas (las usan la página de estadísticas y la API)."""
    return {
        "resumen": resumen_general(ventas),
        "por_categoria": facturacion_por_categoria(ventas),
        "por_mes": facturacion_por_mes(ventas),
        "top_productos": ranking_productos(ventas),
    }
