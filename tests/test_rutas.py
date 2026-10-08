"""Pruebas de punta a punta: se usa el sistema como lo usaría una persona desde el navegador."""

from pathlib import Path

from tests.conftest import CSV_VALIDO

EJEMPLOS = Path(__file__).resolve().parent.parent / "data" / "ejemplos"


def test_todas_las_paginas_cargan_sin_datos(cliente):
    for url in ["/", "/importar/", "/importar/historial", "/servicios/", "/informes"]:
        assert cliente.get(url).status_code == 200, url


def test_pagina_inexistente_muestra_404(cliente):
    respuesta = cliente.get("/no-existe")
    assert respuesta.status_code == 404
    assert "no existe" in respuesta.get_data(as_text=True)


def test_importar_csv_guarda_y_calcula_el_costo_total(cliente, importar):
    html = importar(CSV_VALIDO).get_data(as_text=True)
    assert "Se guardaron 3 de 3 filas" in html
    servicios = cliente.get("/api/servicios").get_json()
    assert servicios[0]["costo_total"] == 1005.0  # 10 x 100,5


def test_archivo_real_de_la_consigna_csv_y_json(cliente, importar):
    """Los resultados esperados se calcularon aparte con el archivo de la consigna."""
    for nombre in ("ONIET-2026-Logistica.csv", "ONIET-2026-Logistica.json"):
        cliente.post("/servicios/vaciar")
        html = importar((EJEMPLOS / nombre).read_bytes(), nombre).get_data(as_text=True)
        assert "Se guardaron 180 de 180 filas" in html, nombre

        informes = cliente.get("/api/informes").get_json()
        assert informes["operadores"][0] == {
            "posicion": 1,
            "operador": "AndesLog",
            "total_envios": 12426,
            "costo_total": 37827869.23,
        }
        assert informes["regiones"][0] == {
            "posicion": 1,
            "region": "Centro",
            "cantidad_envios": 19383,
        }
        # EnvioExpress y TransRuta empatan exacto (3191 / 36 = 88,64): comparten la posición 1
        assert informes["cumplimiento"][:2] == [
            {"posicion": 1, "operador": "EnvioExpress", "promedio": 88.64},
            {"posicion": 1, "operador": "TransRuta", "promedio": 88.64},
        ]


def test_seleccionar_el_periodo(cliente, importar):
    importar((EJEMPLOS / "ONIET-2026-Logistica.csv").read_bytes(), "datos.csv")
    informes = cliente.get("/api/informes?desde=2024-01&hasta=2024-12").get_json()
    assert informes["resumen"]["registros"] == 60
    assert informes["operadores"][0]["operador"] == "CargaNacional"
    assert informes["operadores"][0]["costo_total"] == 11122666.02
    assert informes["cumplimiento"][0] == {
        "posicion": 1,
        "operador": "TransRuta",
        "promedio": 89.75,
    }

    html = cliente.get("/informes?desde=2024-01&hasta=2024-12").get_data(as_text=True)
    assert "$ 11.122.666,02" in html
    assert "Reporte 3" in html


def test_periodo_invalido_se_ignora(cliente, importar):
    importar(CSV_VALIDO)
    informes = cliente.get("/api/informes?desde=hola&hasta=2024-99").get_json()
    assert informes["resumen"]["registros"] == 3


def test_importar_informa_filas_con_error(importar):
    contenido = (EJEMPLOS / "servicios_con_errores.csv").read_bytes()
    html = importar(contenido, "errores.csv").get_data(as_text=True)
    assert "Se guardaron 1 de 7 filas" in html
    assert "Debe estar entre 1 y 12." in html
    assert "repetido en el archivo (igual que la fila 2)" in html


def test_importar_archivo_sin_columnas_obligatorias(importar):
    html = importar("nombre,edad\nAna,30\n").get_data(as_text=True)
    assert "Faltan columnas obligatorias" in html


def test_clave_unica_no_permite_repetidos_ya_guardados(cliente, importar):
    importar(CSV_VALIDO)
    otro = CSV_VALIDO.splitlines()[0] + "\n1,AndesLog,2026,5,1,Sur,1,50\n"
    assert "Ya existe un registro guardado" in importar(otro).get_data(as_text=True)
    assert len(cliente.get("/api/servicios").get_json()) == 3


def test_importar_dos_veces_el_mismo_archivo_no_duplica(cliente, importar):
    importar(CSV_VALIDO)
    assert "ya se importó" in importar(CSV_VALIDO).get_data(as_text=True)
    assert len(cliente.get("/api/servicios").get_json()) == 3


def test_listado_con_filtros_y_totales(cliente, importar):
    importar(CSV_VALIDO)
    html = cliente.get("/servicios/?operador=LogisticaSur").get_data(as_text=True)
    assert "2 registros" in html
    assert "TransRuta</a>" not in html
    assert "$ 2.005,00" in html  # 1005 + 1000


def test_detalle_eliminar_y_vaciar(cliente, importar):
    importar(CSV_VALIDO)
    assert "LogisticaSur" in cliente.get("/servicios/1").get_data(as_text=True)
    assert cliente.get("/servicios/9999").status_code == 404
    cliente.post("/servicios/1/eliminar")
    assert len(cliente.get("/api/servicios").get_json()) == 2
    cliente.post("/servicios/vaciar")
    assert cliente.get("/api/servicios").get_json() == []


def test_pagina_fuera_de_rango_muestra_la_ultima(cliente, importar):
    importar(CSV_VALIDO)
    assert cliente.get("/servicios/?pagina=999999").status_code == 200


def test_exportacion_para_excel_en_espanol(cliente, importar):
    importar(CSV_VALIDO)
    texto = cliente.get("/exportar.csv").get_data(as_text=True)
    assert "1;LogisticaSur;2024;1;10;Centro;100,5;80,0;1005,0" in texto


def test_descargar_ejemplo(cliente):
    respuesta = cliente.get("/ejemplos/ONIET-2026-Logistica.csv")
    assert respuesta.status_code == 200
    assert b"NumeroRegistro" in respuesta.data


def test_rechaza_formularios_enviados_desde_otro_sitio(cliente, importar):
    importar(CSV_VALIDO)
    ataque = cliente.post(
        "/servicios/vaciar", headers={"Origin": "https://sitio-malicioso.example"}
    )
    assert ataque.status_code == 403
    assert len(cliente.get("/api/servicios").get_json()) == 3


def test_error_interno_muestra_la_pagina_propia(app):
    app.config["PROPAGATE_EXCEPTIONS"] = False  # así corre run.py

    def ruta_que_falla():
        raise RuntimeError("detalle técnico que el jurado no tiene que ver")

    app.add_url_rule("/falla", view_func=ruta_que_falla)
    respuesta = app.test_client().get("/falla")
    assert respuesta.status_code == 500
    html = respuesta.get_data(as_text=True)
    assert "Error interno" in html and "detalle técnico" not in html
