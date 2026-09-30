from datetime import date, datetime

import pytest

from app.utils.conversiones import (
    a_decimal,
    a_entero,
    a_fecha,
    normalizar_clave,
    normalizar_texto,
    redondear_dinero,
)
from app.utils.formato import formato_fecha, formato_mes, formato_moneda


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (10, 10.0),
        (2.5, 2.5),
        ("1234.5", 1234.5),
        ("1234,5", 1234.5),
        ("1.234,50", 1234.5),
        ("1,234.50", 1234.5),
        ("$ 1.234,50", 1234.5),
        ("1.234.567", 1234567.0),
        ("  -3,5 ", -3.5),
    ],
)
def test_a_decimal_acepta_formatos_argentinos_e_internacionales(valor, esperado):
    assert a_decimal(valor) == pytest.approx(esperado)


@pytest.mark.parametrize("valor", ["", "abc", "12a", None, "nan", True])
def test_a_decimal_rechaza_valores_invalidos(valor):
    with pytest.raises(ValueError):
        a_decimal(valor)


def test_a_entero():
    assert a_entero("7") == 7
    assert a_entero(3.0) == 3
    with pytest.raises(ValueError, match="entero"):
        a_entero("2,5")


@pytest.mark.parametrize(
    "valor", ["2026-03-15", "15/03/2026", "15-03-2026", "15/03/26", "2026-03-15 10:30:00"]
)
def test_a_fecha_acepta_varios_formatos(valor):
    assert a_fecha(valor) == date(2026, 3, 15)


def test_a_fecha_acepta_objetos_de_excel():
    assert a_fecha(datetime(2026, 3, 15, 9, 0)) == date(2026, 3, 15)


@pytest.mark.parametrize("valor", ["31/02/2026", "hoy", "", "2026-13-01"])
def test_a_fecha_rechaza_fechas_invalidas(valor):
    with pytest.raises(ValueError):
        a_fecha(valor)


def test_normalizar_clave_y_texto():
    assert normalizar_clave("Precio Unitario ($)") == "precio_unitario"
    assert normalizar_clave("  Categoría ") == "categoria"
    assert normalizar_clave("CompaniaSeguro") == "compania_seguro"
    assert normalizar_clave("NumeroRegistro") == "numero_registro"
    assert normalizar_clave("ID") == "id"
    assert normalizar_texto("  Juan   Pérez ") == "Juan Pérez"


def test_formatos_para_mostrar():
    assert formato_moneda(1234.5) == "$ 1.234,50"
    assert formato_fecha("2026-03-15") == "15/03/2026"
    assert formato_mes("2026-03") == "Mar 2026"


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        ("1.500", 1500),
        ("$ 1.500", 1500),
        ("100.000", 100000),
        ("0.500", 0.5),
        ("1.5", 1.5),
        ("3.14159", 3.14159),
        ("1,234", 1.234),
        ("1,234,567", 1234567),
    ],
)
def test_punto_de_miles_argentino(valor, esperado):
    assert a_decimal(valor) == pytest.approx(esperado)


def test_rechaza_formatos_mezclados_y_numeros_gigantes():
    with pytest.raises(ValueError, match="no es un número"):
        a_decimal("1.2.3,4")
    with pytest.raises(ValueError, match="demasiado grande"):
        a_decimal("99999999999999999999")
    assert a_entero("1.000") == 1000


def test_redondeo_de_dinero_como_en_un_comercio():
    assert redondear_dinero(1.005) == 1.01
    assert redondear_dinero(2.675) == 2.68
    assert redondear_dinero(3 * 0.1) == 0.3
