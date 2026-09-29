import io
import json

import pytest

from app.servicios.lector import ErrorLectura, detectar_separador, leer_archivo


def test_lee_csv_con_punto_y_coma_y_normaliza_encabezados():
    filas = leer_archivo("datos.csv", "Fecha;Precio Unitario\n15/03/2026;10,5\n".encode())
    assert len(filas) == 1
    assert filas[0].datos == {"fecha": "15/03/2026", "precio_unitario": "10,5"}
    assert filas[0].numero == 2  # la fila 1 es el encabezado


@pytest.mark.parametrize("separador", [",", ";", "\t", "|"])
def test_detecta_el_separador(separador):
    assert detectar_separador(f"a{separador}b{separador}c\n1{separador}2{separador}3") == separador


def test_csv_ignora_filas_vacias_y_conserva_el_numero_de_fila():
    filas = leer_archivo("datos.csv", b"\n\na,b\n1,2\n\n3,4\n")
    assert [fila.numero for fila in filas] == [4, 6]


def test_csv_guardado_por_excel_en_windows_cp1252():
    contenido = "categoria;cantidad\nLibrería;2\n".encode("cp1252")
    assert leer_archivo("datos.csv", contenido)[0].datos["categoria"] == "Librería"


def test_csv_con_campos_entre_comillas():
    filas = leer_archivo("datos.csv", b'nombre,precio\n"Gaseosa, 1,5 L","1.234,50"\n')
    assert filas[0].datos == {"nombre": "Gaseosa, 1,5 L", "precio": "1.234,50"}


def test_lee_json_lista_y_objeto_con_lista():
    lista = json.dumps([{"Producto": "Agua", "cantidad": 2}]).encode()
    envuelto = json.dumps({"ventas": [{"producto": "Agua"}, {"producto": "Pan"}]}).encode()
    assert leer_archivo("a.json", lista)[0].datos == {"producto": "Agua", "cantidad": 2}
    assert len(leer_archivo("b.json", envuelto)) == 2


def test_json_invalido_da_error_claro():
    with pytest.raises(ErrorLectura, match="JSON"):
        leer_archivo("a.json", b"[{'mal': 1}]")


def test_lee_excel():
    openpyxl = pytest.importorskip("openpyxl")
    libro = openpyxl.Workbook()
    hoja = libro.active
    hoja.append(["Fecha", "Cantidad"])
    hoja.append(["15/03/2026", 3])
    buffer = io.BytesIO()
    libro.save(buffer)
    filas = leer_archivo("datos.xlsx", buffer.getvalue())
    assert filas[0].datos == {"fecha": "15/03/2026", "cantidad": 3}
    assert filas[0].numero == 2


@pytest.mark.parametrize(
    ("nombre", "contenido", "mensaje"),
    [
        ("datos.pdf", b"algo", "no está soportado"),
        ("datos.csv", b"   \n", "vacío"),
        ("datos.csv", b"a,b\n", "no tiene filas"),
        ("datos.csv", b"a,a\n1,2\n", "repetidas"),
        ("datos.xlsx", b"no es un excel", "Excel"),
    ],
)
def test_errores_de_lectura(nombre, contenido, mensaje):
    with pytest.raises(ErrorLectura, match=mensaje):
        leer_archivo(nombre, contenido)
