"""API JSON: los mismos datos que muestra la interfaz, para otros programas."""

from flask import Blueprint, abort, jsonify, request

from app.repositorios import servicios_repositorio
from app.repositorios.servicios_repositorio import FiltrosServicios
from app.servicios import reportes_servicio

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/servicios")
def servicios():
    filtros = FiltrosServicios.desde_diccionario(request.args)
    return jsonify(servicios_repositorio.listar_todas(filtros))


@bp.route("/servicios/<int:servicio_id>")
def servicio(servicio_id: int):
    encontrado = servicios_repositorio.obtener_por_id(servicio_id)
    if encontrado is None:
        abort(404)
    return jsonify(encontrado)


@bp.route("/informes")
def informes():
    filtros = FiltrosServicios.desde_diccionario(request.args)
    return jsonify(reportes_servicio.obtener_informes(filtros))
