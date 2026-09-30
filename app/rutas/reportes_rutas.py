"""Estadísticas y exportación de resultados."""

from flask import Blueprint, Response, render_template, request

from app.repositorios import ventas_repositorio
from app.repositorios.ventas_repositorio import FiltrosVentas
from app.servicios import reportes_servicio

bp = Blueprint("reportes", __name__)


@bp.route("/estadisticas")
def estadisticas():
    filtros = FiltrosVentas.desde_diccionario(request.args)
    return render_template(
        "estadisticas.html",
        datos=reportes_servicio.obtener_estadisticas(filtros),
        filtros=filtros,
        categorias=ventas_repositorio.listar_categorias(),
    )


@bp.route("/exportar.csv")
def exportar():
    filtros = FiltrosVentas.desde_diccionario(request.args)
    contenido = "\ufeff" + reportes_servicio.exportar_csv(filtros)  # BOM: Excel detecta UTF-8
    return Response(
        contenido,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=ventas.csv"},
    )
