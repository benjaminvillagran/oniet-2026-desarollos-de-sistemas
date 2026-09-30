"""Pruebas de punta a punta: se usa el sistema como lo usaría una persona desde el navegador."""

import io

from tests.conftest import CSV_VALIDO


def test_todas_las_paginas_cargan_sin_datos(cliente):
    for url in [
        "/",
        "/importar/",
        "/importar/historial",
        "/ventas/",
        "/ventas/nueva",
        "/estadisticas",
    ]:
        assert cliente.get(url).status_code == 200, url


def test_pagina_inexistente_muestra_404(cliente):
    respuesta = cliente.get("/no-existe")
    assert respuesta.status_code == 404
    assert "no existe" in respuesta.get_data(as_text=True)


def test_importar_csv_guarda_y_muestra_los_datos(cliente, importar):
    respuesta = importar(CSV_VALIDO)
    assert "Se guardaron 3 de 3 filas" in respuesta.get_data(as_text=True)

    listado = cliente.get("/ventas/").get_data(as_text=True)
    assert "Alfajor" in listado and "Bebidas" in listado

    historial = cliente.get("/importar/historial").get_data(as_text=True)
    assert "ventas.csv" in historial


def test_importar_informa_filas_con_error(importar):
    csv_con_error = CSV_VALIDO + "20/03/2026;Pan;Panadería;-2;500\n"
    html = importar(csv_con_error).get_data(as_text=True)
    assert "Se guardaron 3 de 4 filas" in html
    assert "Debe ser mayor a 0." in html


def test_muchos_errores_se_resumen_y_no_cuelgan_la_pagina(importar):
    filas = "".join(f"99/99/2026;P{i};C;x;1\n" for i in range(1000))
    respuesta = importar("fecha;producto;categoria;cantidad;precio_unitario\n" + filas)
    html = respuesta.get_data(as_text=True)
    assert "Resumen por campo" in html
    assert "errores más que no se muestran" in html
    assert len(respuesta.data) < 200_000


def test_importar_archivo_sin_columnas_obligatorias(importar):
    html = importar("fecha,producto\n15/03/2026,Pan\n").get_data(as_text=True)
    assert "Faltan columnas obligatorias" in html


# Propio del ejemplo de ventas (no tiene clave única). Si la consigna tiene un campo único,
# este test se reemplaza por uno como test_clave_unica_no_permite_repetidos.
def test_importar_dos_veces_el_mismo_archivo_no_duplica(cliente, importar):
    importar(CSV_VALIDO)
    html = importar(CSV_VALIDO).get_data(as_text=True)
    assert "ya se importó" in html
    assert len(cliente.get("/api/ventas").get_json()) == 3

    respuesta = cliente.post(
        "/importar/",
        data={"archivo": (io.BytesIO(CSV_VALIDO.encode()), "ventas.csv"), "forzar": "1"},
        content_type="multipart/form-data",
    )
    assert "Se guardaron 3 de 3 filas" in respuesta.get_data(as_text=True)
    assert len(cliente.get("/api/ventas").get_json()) == 6


def test_importar_sin_elegir_archivo(cliente):
    respuesta = cliente.post("/importar/", data={}, follow_redirects=True)
    assert "Elegí un archivo" in respuesta.get_data(as_text=True)


def test_importar_desde_url(cliente, monkeypatch):
    from app.servicios import lector

    monkeypatch.setattr(
        lector, "descargar", lambda url, limite: ("ventas.csv", CSV_VALIDO.encode("utf-8"))
    )
    respuesta = cliente.post("/importar/", data={"url": "https://ejemplo.com/api/ventas"})
    assert "Se guardaron 3 de 3 filas" in respuesta.get_data(as_text=True)


def test_estadisticas_calculadas_sobre_lo_importado(cliente, importar):
    importar(CSV_VALIDO)
    datos = cliente.get("/api/estadisticas").get_json()
    assert datos["resumen"]["cantidad_ventas"] == 3
    assert datos["resumen"]["facturacion_total"] == 3600 + 1801 + 1200
    assert datos["por_categoria"][0]["nombre"] == "Kiosco"  # 'kiosco' se normalizó a 'Kiosco'
    assert [fila["mes"] for fila in datos["por_mes"]] == ["2026-03", "2026-04"]
    assert "Estadísticas" in cliente.get("/estadisticas").get_data(as_text=True)


def test_filtros(cliente, importar):
    importar(CSV_VALIDO)
    assert len(cliente.get("/api/ventas?categoria=Bebidas").get_json()) == 1
    assert len(cliente.get("/api/ventas?busqueda=alfa").get_json()) == 2
    assert len(cliente.get("/api/ventas?desde=2026-04-01").get_json()) == 1
    assert len(cliente.get("/api/ventas?hasta=16/03/2026").get_json()) == 2
    assert cliente.get("/ventas/?orden=total&direccion=asc&pagina=1").status_code == 200


def test_listado_muestra_fila_de_totales_filtrada(cliente, importar):
    importar(CSV_VALIDO)
    html = cliente.get("/ventas/?categoria=Kiosco").get_data(as_text=True)
    assert "Total filtrado (2 ventas)" in html
    assert "$ 4.800,00" in html  # 3 x 1200 + 1 x 1200


def test_exportar_csv_y_volver_a_importar(cliente, importar):
    importar(CSV_VALIDO)
    exportado = cliente.get("/exportar.csv")
    assert exportado.mimetype == "text/csv"
    importar(exportado.data, nombre="exportado.csv")
    assert len(cliente.get("/api/ventas").get_json()) == 6


def test_alta_manual_valida_y_guarda(cliente):
    invalida = cliente.post("/ventas/nueva", data={"producto": "Pan"})
    assert "Revisá los campos" in invalida.get_data(as_text=True)

    datos = {
        "fecha": "2026-03-15",
        "producto": "Pan",
        "categoria": "Panadería",
        "cantidad": "2",
        "precio_unitario": "1500,5",
    }
    respuesta = cliente.post("/ventas/nueva", data=datos, follow_redirects=True)
    assert "Venta registrada" in respuesta.get_data(as_text=True)
    venta = cliente.get("/api/ventas").get_json()[0]
    assert venta["total"] == 3001


def test_eliminar_y_vaciar(cliente, importar):
    importar(CSV_VALIDO)
    primera = cliente.get("/api/ventas").get_json()[0]
    assert cliente.post(f"/ventas/{primera['id']}/eliminar").status_code == 302
    assert cliente.get(f"/api/ventas/{primera['id']}").status_code == 404
    assert cliente.post("/ventas/999/eliminar").status_code == 404

    cliente.post("/ventas/vaciar")
    assert cliente.get("/api/ventas").get_json() == []


def test_descargar_ejemplo(cliente):
    respuesta = cliente.get("/ejemplos/ventas_ejemplo.csv")
    assert respuesta.status_code == 200
    assert cliente.get("/ejemplos/../../run.py").status_code == 404


def test_detalle_y_edicion(cliente, importar):
    importar(CSV_VALIDO)
    venta = cliente.get("/api/ventas").get_json()[0]
    detalle = cliente.get(f"/ventas/{venta['id']}").get_data(as_text=True)
    assert venta["producto"] in detalle and "Importación #1" in detalle
    assert "Editar venta" in cliente.get(f"/ventas/{venta['id']}/editar").get_data(as_text=True)

    invalida = cliente.post(f"/ventas/{venta['id']}/editar", data={**venta, "cantidad": "0"})
    assert "Debe ser mayor a 0." in invalida.get_data(as_text=True)

    datos = {**venta, "cantidad": "10", "precio_unitario": "100"}
    respuesta = cliente.post(f"/ventas/{venta['id']}/editar", data=datos, follow_redirects=True)
    assert "Venta actualizada" in respuesta.get_data(as_text=True)
    actualizada = cliente.get(f"/api/ventas/{venta['id']}").get_json()
    assert (actualizada["cantidad"], actualizada["total"]) == (10, 1000)  # se recalcula el total

    assert cliente.get("/ventas/999").status_code == 404
    assert cliente.get("/ventas/999/editar").status_code == 404


def test_pagina_fuera_de_rango_muestra_la_ultima(cliente, importar):
    importar(CSV_VALIDO)
    for pagina in ("5", "99999999999999999999"):
        html = cliente.get(f"/ventas/?pagina={pagina}").get_data(as_text=True)
        assert "Alfajor" in html and "Todavía no hay ventas" not in html


def test_rechaza_formularios_enviados_desde_otro_sitio(cliente, importar):
    importar(CSV_VALIDO)
    ataque = cliente.post("/ventas/vaciar", headers={"Origin": "https://sitio-malicioso.example"})
    assert ataque.status_code == 403
    assert len(cliente.get("/api/ventas").get_json()) == 3

    propio = cliente.post("/ventas/vaciar", headers={"Origin": "http://localhost"})
    assert propio.status_code == 302


def test_exportacion_para_excel_en_espanol(cliente, importar):
    importar(
        "fecha;producto;categoria;cantidad;precio_unitario\n15/03/2026;=HYPERLINK(1);C;2;900,5\n"
    )
    texto = cliente.get("/exportar.csv").get_data(as_text=True)
    assert ";900,5;1801,0" in texto  # coma decimal
    assert "'=HYPERLINK(1)" in texto  # Excel no lo ejecuta como fórmula


def test_fila_con_valores_de_mas_no_se_guarda(importar):
    html = importar(
        "fecha,producto,categoria,cantidad,precio_unitario\n15/03/2026,Pan,K,2,1200,50\n"
    )
    assert "Se guardaron 0 de 1 filas" in html.get_data(as_text=True)
    assert "más valores que columnas" in html.get_data(as_text=True)


def test_clave_unica_no_permite_repetidos(cliente, importar, monkeypatch):
    from app.servicios import validacion

    monkeypatch.setattr(validacion, "CLAVE_UNICA", "producto")
    html = importar(CSV_VALIDO).get_data(as_text=True)  # "Alfajor" aparece 2 veces
    assert "Se guardaron 2 de 3 filas" in html
    assert "repetido en el archivo (igual que la fila 2)" in html

    otro = "fecha;producto;categoria;cantidad;precio_unitario\n01/05/2026;Agua;Bebidas;1;900\n"
    assert "Ya existe un registro guardado" in importar(otro).get_data(as_text=True)
    assert len(cliente.get("/api/ventas").get_json()) == 2


def test_error_interno_muestra_la_pagina_propia(app):
    app.config["PROPAGATE_EXCEPTIONS"] = False  # así corre run.py

    def ruta_que_falla():
        raise RuntimeError("detalle técnico que el jurado no tiene que ver")

    app.add_url_rule("/falla", view_func=ruta_que_falla)
    respuesta = app.test_client().get("/falla")
    assert respuesta.status_code == 500
    html = respuesta.get_data(as_text=True)
    assert "Error interno" in html and "detalle técnico" not in html
