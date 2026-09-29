import pytest

from app.servicios.procesamiento import (
    calcular_total,
    completar_venta,
    facturacion_por_categoria,
    facturacion_por_mes,
    generar_estadisticas,
    ranking_productos,
    resumen_general,
)


def venta(fecha, producto, categoria, cantidad, precio):
    return completar_venta(
        {
            "fecha": fecha,
            "producto": producto,
            "categoria": categoria,
            "cantidad": cantidad,
            "precio_unitario": precio,
        }
    )


VENTAS = [
    venta("2026-03-10", "Alfajor", "Kiosco", 3, 1000),  # 3000
    venta("2026-03-20", "Agua", "Bebidas", 2, 500),  # 1000
    venta("2026-04-05", "Alfajor", "Kiosco", 1, 1000),  # 1000
    venta("2026-02-28", "Gaseosa", "Bebidas", 1, 5000),  # 5000
]


def test_calcular_total_redondea_a_centavos():
    assert calcular_total(3, 0.1) == 0.3
    assert calcular_total(2, 1250.555) == 2501.11


def test_resumen_general():
    resumen = resumen_general(VENTAS)
    assert resumen["cantidad_ventas"] == 4
    assert resumen["unidades"] == 7
    assert resumen["facturacion_total"] == 10000
    assert resumen["ticket_promedio"] == 2500
    assert resumen["venta_maxima"]["producto"] == "Gaseosa"
    assert (resumen["fecha_desde"], resumen["fecha_hasta"]) == ("2026-02-28", "2026-04-05")


def test_resumen_sin_ventas_no_falla():
    resumen = resumen_general([])
    assert resumen["cantidad_ventas"] == 0
    assert resumen["venta_maxima"] is None


def test_facturacion_por_categoria_con_porcentajes():
    grupos = facturacion_por_categoria(VENTAS)
    assert [g["nombre"] for g in grupos] == ["Bebidas", "Kiosco"]  # de mayor a menor
    assert [g["valor"] for g in grupos] == [6000, 4000]
    assert [g["porcentaje"] for g in grupos] == [60.0, 40.0]
    assert sum(g["porcentaje"] for g in grupos) == pytest.approx(100)


def test_facturacion_por_mes_en_orden_cronologico():
    assert facturacion_por_mes(VENTAS) == [
        {"mes": "2026-02", "valor": 5000},
        {"mes": "2026-03", "valor": 4000},
        {"mes": "2026-04", "valor": 1000},
    ]


def test_ranking_productos():
    ranking = ranking_productos(VENTAS, limite=2)
    assert ranking == [
        {"producto": "Gaseosa", "unidades": 1, "facturacion": 5000},
        {"producto": "Alfajor", "unidades": 4, "facturacion": 4000},
    ]


def test_generar_estadisticas_con_lista_vacia():
    estadisticas = generar_estadisticas([])
    assert estadisticas["por_categoria"] == []
    assert estadisticas["por_mes"] == []
    assert estadisticas["top_productos"] == []
