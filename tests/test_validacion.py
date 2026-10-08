"""Pruebas de la validación de cada registro de servicio."""

from app.servicios.lector import FilaLeida
from app.servicios.validacion import columnas_faltantes, validar_filas, validar_servicio

VALIDO = {
    "numero_registro": "1",
    "operador_logistico": " LogisticaSur ",
    "anio": "2024",
    "mes": "1",
    "cantidad_envios": "314",
    "region": "Centro",
    "costo_por_envio": "2707.33",
    "porcentaje_entregas_a_tiempo": "73",  # nombre alternativo (alias)
}


def test_servicio_valido_queda_limpio():
    servicio, errores = validar_servicio(VALIDO)
    assert errores == {}
    assert servicio == {
        "numero_registro": 1,
        "operador_logistico": "LogisticaSur",
        "anio": 2024,
        "mes": 1,
        "cantidad_envios": 314,
        "region": "Centro",
        "costo_por_envio": 2707.33,
        "porcentaje_entregas_atiempo": 73.0,
    }


def test_campos_obligatorios():
    _, errores = validar_servicio({})
    assert errores["operador_logistico"] == "Es obligatorio."
    assert len(errores) == 8


def test_reglas_de_cada_campo():
    malos = {
        **VALIDO,
        "numero_registro": "0",
        "mes": "13",
        "cantidad_envios": "-5",
        "costo_por_envio": "abc",
        "porcentaje_entregas_a_tiempo": "150",
    }
    _, errores = validar_servicio(malos)
    assert errores["numero_registro"] == "Debe ser 1 o más."
    assert errores["mes"] == "Debe estar entre 1 y 12."
    assert errores["cantidad_envios"] == "Debe ser 0 o más."
    assert "no es un número válido" in errores["costo_por_envio"]
    assert errores["porcentaje_entregas_atiempo"] == "Debe estar entre 0 y 100."


def test_validar_filas_separa_validas_de_invalidas():
    filas = [FilaLeida(2, VALIDO), FilaLeida(3, {**VALIDO, "mes": "0"})]
    resultado = validar_filas(filas)
    assert len(resultado.validos) == 1
    assert resultado.filas_validas == [2]
    assert [(e.fila, e.campo) for e in resultado.errores] == [(3, "mes")]


def test_columnas_faltantes():
    assert columnas_faltantes([FilaLeida(2, {"numero_registro": "1"})])[0] == "operador_logistico"
    assert columnas_faltantes([FilaLeida(2, VALIDO)]) == []
