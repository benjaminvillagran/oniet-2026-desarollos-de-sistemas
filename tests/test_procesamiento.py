"""Pruebas de los cálculos de la consigna, con resultados calculados a mano."""

import random

from app.servicios.procesamiento import (
    asignar_posiciones,
    calcular_costo_total,
    completar_servicio,
    cumplimiento_por_operador,
    generar_informes,
    primeros_n,
    ranking_operadores,
    ranking_regiones,
    resumen_general,
)


def _servicio(operador, region, envios, costo_total, porcentaje):
    return {
        "operador_logistico": operador,
        "region": region,
        "cantidad_envios": envios,
        "costo_total": costo_total,
        "porcentaje_entregas_atiempo": porcentaje,
    }


# Ejemplo calculado a mano
SERVICIOS = [
    _servicio("A", "Norte", 10, 1000.0, 80),
    _servicio("B", "Sur", 5, 2000.0, 90),
    _servicio("A", "Sur", 20, 500.0, 100),
]


def test_costo_total_es_envios_por_costo():
    assert calcular_costo_total(314, 2707.33) == 850101.62
    servicio = completar_servicio({"cantidad_envios": 3, "costo_por_envio": 0.1})
    assert servicio["costo_total"] == 0.3  # sin errores de punto flotante


def test_ranking_operadores_por_costo_total():
    assert ranking_operadores(SERVICIOS) == [
        {"posicion": 1, "operador": "B", "total_envios": 5, "costo_total": 2000.0},
        {"posicion": 2, "operador": "A", "total_envios": 30, "costo_total": 1500.0},
    ]


def test_ranking_regiones_por_cantidad_de_envios():
    assert ranking_regiones(SERVICIOS) == [
        {"posicion": 1, "region": "Sur", "cantidad_envios": 25},
        {"posicion": 2, "region": "Norte", "cantidad_envios": 10},
    ]


def test_cumplimiento_promedio_con_empate():
    # A: (80 + 100) / 2 = 90 y B: 90 -> empatan: misma posición y orden alfabético
    assert cumplimiento_por_operador(SERVICIOS) == [
        {"posicion": 1, "operador": "A", "promedio": 90.0},
        {"posicion": 1, "operador": "B", "promedio": 90.0},
    ]


def test_posiciones_con_empate_saltean_el_siguiente_puesto():
    filas = [{"valor": 9}, {"valor": 5}, {"valor": 5}, {"valor": 1}]
    posiciones = [fila["posicion"] for fila in asignar_posiciones(filas, "valor")]
    assert posiciones == [1, 2, 2, 4]


def test_resumen_general():
    assert resumen_general(SERVICIOS) == {
        "registros": 3,
        "total_envios": 35,
        "costo_total": 3500.0,
        "promedio_a_tiempo": 90.0,
    }


def test_informes_sin_datos_no_fallan():
    informes = generar_informes([])
    assert informes["resumen"]["registros"] == 0
    assert informes["operadores"] == informes["regiones"] == informes["cumplimiento"] == []


BARRIOS = [
    {"nombre": "A", "proporcion": 0.5},
    {"nombre": "B", "proporcion": 0.1},
    {"nombre": "C", "proporcion": 0.1},
    {"nombre": "D", "proporcion": 0.9},
]


def test_primeros_n_ordena_y_respeta_n():
    mayores = primeros_n(BARRIOS, "proporcion", 2, azar=random.Random(1))
    assert [barrio["nombre"] for barrio in mayores] == ["D", "A"]
    assert primeros_n(BARRIOS, "proporcion", 0) == []


def test_primeros_n_desempata_al_azar_de_forma_reproducible():
    def menor(semilla):
        return primeros_n(
            BARRIOS, "proporcion", 1, mayor_primero=False, azar=random.Random(semilla)
        )[0]

    assert menor(7) == menor(7)  # con la misma semilla, siempre el mismo resultado
    elegidos = {menor(semilla)["nombre"] for semilla in range(30)}
    assert elegidos == {"B", "C"}  # solo los empatados, y los dos pueden salir
