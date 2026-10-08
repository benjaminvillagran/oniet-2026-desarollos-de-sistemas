"""Informes de la consigna (con selección de período) y exportación de resultados."""

from flask import Blueprint, Response, render_template, request

from app.repositorios import servicios_repositorio
from app.repositorios.servicios_repositorio import FiltrosServicios
from app.servicios import reportes_servicio

bp = Blueprint("reportes", __name__)


@bp.route("/informes")
def informes():
    filtros = FiltrosServicios.desde_diccionario(request.args)
    return render_template(
        "informes.html",
        datos=reportes_servicio.obtener_informes(filtros),
        filtros=filtros,
        operadores=servicios_repositorio.listar_distintos("operador_logistico"),
        regiones=servicios_repositorio.listar_distintos("region"),
        periodos=servicios_repositorio.listar_periodos(),
    )


@bp.route("/exportar.csv")
def exportar():
    filtros = FiltrosServicios.desde_diccionario(request.args)
    contenido = "﻿" + reportes_servicio.exportar_csv(filtros)  # BOM: Excel detecta UTF-8
    return Response(
        contenido,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=servicios.csv"},
    )
