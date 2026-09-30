import email.message
import io
import json
import urllib.error
import urllib.request

import pytest

from app.servicios.lector import (
    VALORES_DE_MAS,
    ErrorLectura,
    descargar,
    detectar_separador,
    leer_archivo,
)


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
    envuelto = json.dumps({"datos": [{"producto": "Agua"}, {"producto": "Pan"}]}).encode()
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


class RespuestaFalsa(io.BytesIO):
    """Imita la respuesta de urllib para probar descargas sin internet."""

    def __init__(self, contenido: bytes, tipo: str):
        super().__init__(contenido)
        self.headers = email.message.Message()
        self.headers["Content-Type"] = tipo


def test_descargar_desde_una_api(monkeypatch):
    datos = b'[{"producto": "Agua"}]'
    monkeypatch.setattr(
        urllib.request, "urlopen", lambda pedido, timeout: RespuestaFalsa(datos, "application/json")
    )
    nombre, contenido = descargar("https://api.ejemplo.com/registros?anio=2026", 1000)
    assert (nombre, contenido) == ("registros.json", datos)


@pytest.mark.parametrize(
    ("url", "mensaje"),
    [("ftp://servidor/datos.csv", "http"), ("archivo.csv", "http"), ("http://[::1", "descargar")],
)
def test_descargar_rechaza_direcciones_invalidas(url, mensaje):
    with pytest.raises(ErrorLectura, match=mensaje):
        descargar(url, 1000)


def test_descargar_limita_el_tamanio(monkeypatch):
    monkeypatch.setattr(
        urllib.request, "urlopen", lambda pedido, timeout: RespuestaFalsa(b"x" * 50, "text/csv")
    )
    with pytest.raises(ErrorLectura, match="demasiado grande"):
        descargar("https://ejemplo.com/datos.csv", 10)


def test_saltea_titulos_arriba_del_encabezado_en_csv_y_excel():
    csv_con_titulo = "Informe mensual;;\n;;\nfecha;producto;cantidad\n15/03/2026;Pan;2\n"
    filas = leer_archivo("reporte.csv", csv_con_titulo.encode())
    assert filas[0].datos == {"fecha": "15/03/2026", "producto": "Pan", "cantidad": "2"}
    assert filas[0].numero == 4

    openpyxl = pytest.importorskip("openpyxl")
    libro = openpyxl.Workbook()
    for fila in (["Informe mensual"], [], ["fecha", "cantidad"], ["15/03/2026", 2]):
        libro.active.append(fila)
    buffer = io.BytesIO()
    libro.save(buffer)
    assert leer_archivo("informe.xlsx", buffer.getvalue())[0].datos == {
        "fecha": "15/03/2026",
        "cantidad": 2,
    }


def test_archivo_de_una_sola_columna():
    filas = leer_archivo("nombres.csv", b"nombre\nAna\nBruno\n")
    assert [fila.datos for fila in filas] == [{"nombre": "Ana"}, {"nombre": "Bruno"}]


def test_json_de_api_con_lista_anidada():
    respuesta = {"estado": "ok", "data": {"total": 2, "items": [{"a": 1}, {"a": 2}]}}
    assert len(leer_archivo("api.json", json.dumps(respuesta).encode())) == 2
    ambiguo = {"altas": [{"a": 1}], "bajas": [{"b": 2}]}
    with pytest.raises(ErrorLectura, match="una sola lista"):
        leer_archivo("ambiguo.json", json.dumps(ambiguo).encode())
    with pytest.raises(ErrorLectura, match="no tiene filas"):
        leer_archivo("vacio.json", b'{"datos": []}')


def test_geojson_de_datos_abiertos():
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"Nombre Barrio": "Las Flores"}, "geometry": None}
        ],
    }
    filas = leer_archivo("barrios.json", json.dumps(geojson).encode())
    assert filas[0].datos == {"nombre_barrio": "Las Flores"}


def test_csv_utf16_de_excel_texto_unicode():
    contenido = "fecha\tproducto\n15/03/2026\tPan\n".encode("utf-16")
    assert leer_archivo("datos.txt", contenido)[0].datos == {
        "fecha": "15/03/2026",
        "producto": "Pan",
    }


def test_comillas_sin_cerrar_dan_error_claro():
    contenido = b'a,b\n"sin cerrar,' + b"x" * 200_000 + b"\n"
    with pytest.raises(ErrorLectura, match="comillas sin cerrar"):
        leer_archivo("roto.csv", contenido)


def test_separador_con_titulo_que_tiene_comas():
    texto = "Informe, marzo 2026\nfecha;producto;cantidad\n15/03/2026;Pan;2\n"
    filas = leer_archivo("informe.csv", texto.encode())
    assert filas[0].datos == {"fecha": "15/03/2026", "producto": "Pan", "cantidad": "2"}


def test_fila_con_valores_de_mas_se_marca():
    filas = leer_archivo("coma.csv", b"producto,precio\nPan,1200,50\nAgua,900\n")
    assert filas[0].datos[VALORES_DE_MAS] == 1
    assert VALORES_DE_MAS not in filas[1].datos


def test_json_con_claves_que_se_pisan():
    with pytest.raises(ErrorLectura, match="repetidas"):
        leer_archivo("a.json", b'[{"Precio": 1, "precio": 2}]')


def test_errores_de_descarga_con_mensajes_claros(monkeypatch):
    def sin_conexion(pedido, timeout):
        raise urllib.error.URLError("Name or service not known")

    monkeypatch.setattr(urllib.request, "urlopen", sin_conexion)
    with pytest.raises(ErrorLectura, match="Revisá que esté bien escrita y que haya conexión"):
        descargar("https://no-existe.example/datos.csv", 1000)

    def no_encontrado(pedido, timeout):
        raise urllib.error.HTTPError(pedido.full_url, 404, "Not Found", None, None)

    monkeypatch.setattr(urllib.request, "urlopen", no_encontrado)
    with pytest.raises(ErrorLectura, match="404"):
        descargar("https://ejemplo.com/falta.csv", 1000)
