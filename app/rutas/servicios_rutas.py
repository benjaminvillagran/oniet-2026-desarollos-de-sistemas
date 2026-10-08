"""Listado, detalle y baja de servicios logísticos."""

from __future__ import annotations

import math

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from app.repositorios import servicios_repositorio
from app.repositorios.servicios_repositorio import FiltrosServicios
from app.servicios import servicios_servicio

bp = Blueprint("servicios", __name__, url_prefix="/servicios")


@bp.route("/")
def listado():
    filtros = FiltrosServicios.desde_diccionario(request.args)
    orden = request.args.get("orden", "numero_registro")
    direccion = request.args.get("direccion", "asc")
    por_pagina = current_app.config["REGISTROS_POR_PAGINA"]
    totales = servicios_repositorio.totales(filtros)
    paginas = max(math.ceil(totales["registros"] / por_pagina), 1)
    # La página pedida se ajusta a las que existen (?pagina=999999 muestra la última)
    pagina = min(max(request.args.get("pagina", 1, type=int), 1), paginas)

    servicios, total = servicios_repositorio.listar_pagina(
        filtros, orden, direccion, pagina, por_pagina
    )
    return render_template(
        "servicios_listado.html",
        servicios=servicios,
        total=total,
        pagina=pagina,
        paginas=paginas,
        filtros=filtros,
        orden=orden,
        direccion=direccion,
        operadores=servicios_repositorio.listar_distintos("operador_logistico"),
        regiones=servicios_repositorio.listar_distintos("region"),
        periodos=servicios_repositorio.listar_periodos(),
        totales=totales,
    )


@bp.route("/<int:servicio_id>")
def detalle(servicio_id: int):
    servicio = servicios_repositorio.obtener_por_id(servicio_id)
    if servicio is None:
        abort(404)
    return render_template("servicios_detalle.html", servicio=servicio)


@bp.route("/<int:servicio_id>/eliminar", methods=["POST"])
def eliminar(servicio_id: int):
    if not servicios_servicio.eliminar_servicio(servicio_id):
        abort(404)
    flash("Registro eliminado.", "exito")
    return redirect(url_for(".listado"))


@bp.route("/vaciar", methods=["POST"])
def vaciar():
    cantidad = servicios_servicio.vaciar_datos()
    flash(f"Se borraron {cantidad} registros y el historial de importaciones.", "exito")
    return redirect(url_for("principal.inicio"))
