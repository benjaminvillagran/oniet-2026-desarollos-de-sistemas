"""API JSON: los mismos datos que muestra la interfaz, para otros programas."""

from flask import Blueprint, abort, jsonify, request

from app.repositorios import ventas_repositorio
from app.repositorios.ventas_repositorio import FiltrosVentas
from app.servicios import reportes_servicio

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/ventas")
def ventas():
    filtros = FiltrosVentas.desde_diccionario(request.args)
    return jsonify(ventas_repositorio.listar_todas(filtros))


@bp.route("/ventas/<int:venta_id>")
def venta(venta_id: int):
    encontrada = ventas_repositorio.obtener_por_id(venta_id)
    if encontrada is None:
        abort(404)
    return jsonify(encontrada)


@bp.route("/estadisticas")
def estadisticas():
    filtros = FiltrosVentas.desde_diccionario(request.args)
    return jsonify(reportes_servicio.obtener_estadisticas(filtros))
