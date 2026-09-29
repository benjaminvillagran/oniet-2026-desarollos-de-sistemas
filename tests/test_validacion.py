from app.servicios.lector import FilaLeida
from app.servicios.validacion import columnas_faltantes, validar_filas, validar_venta

VENTA_OK = {
    "fecha": "15/03/2026",
    "producto": "  alfajor   triple ",
    "categoria": "KIOSCO",
    "cantidad": "3",
    "precio_unitario": "1.200,50",
}


def test_venta_valida_queda_limpia_y_normalizada():
    venta, errores = validar_venta(VENTA_OK)
    assert errores == {}
    assert venta == {
        "fecha": "2026-03-15",
        "producto": "Alfajor triple",
        "categoria": "Kiosco",
        "cantidad": 3,
        "precio_unitario": 1200.5,
    }


def test_campos_obligatorios():
    venta, errores = validar_venta({})
    assert venta is None
    assert set(errores) == {"fecha", "producto", "categoria", "cantidad", "precio_unitario"}


def test_reglas_de_cada_campo():
    _, errores = validar_venta({**VENTA_OK, "cantidad": "0", "precio_unitario": "-5"})
    assert errores == {
        "cantidad": "Debe ser mayor a 0.",
        "precio_unitario": "No puede ser negativo.",
    }

    _, errores = validar_venta({**VENTA_OK, "fecha": "31/02/2026", "cantidad": "dos"})
    assert set(errores) == {"fecha", "cantidad"}


def test_acepta_nombres_alternativos_de_columnas():
    datos = {
        "fecha": "2026-03-15",
        "articulo": "Pan",
        "rubro": "Panadería",
        "cant": 1,
        "precio": 10,
    }
    venta, errores = validar_venta(datos)
    assert errores == {}
    assert venta["producto"] == "Pan"


def test_validar_filas_separa_validas_de_invalidas():
    filas = [
        FilaLeida(2, VENTA_OK),
        FilaLeida(3, {**VENTA_OK, "cantidad": "-1", "fecha": "mal"}),
        FilaLeida(4, VENTA_OK),
    ]
    resultado = validar_filas(filas)
    assert len(resultado.validos) == 2
    assert resultado.filas_con_error == 1
    assert {error.campo for error in resultado.errores} == {"cantidad", "fecha"}
    assert all(error.fila == 3 for error in resultado.errores)


def test_columnas_faltantes():
    assert columnas_faltantes([FilaLeida(2, {"fecha": "x", "producto": "y"})]) == [
        "categoria",
        "cantidad",
        "precio_unitario",
    ]
    assert columnas_faltantes([FilaLeida(2, VENTA_OK)]) == []
