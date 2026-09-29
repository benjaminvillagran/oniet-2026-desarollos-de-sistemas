"""Listado, alta manual y baja de ventas."""

import math

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.repositorios import ventas_repositorio
from app.repositorios.ventas_repositorio import FiltrosVentas
from app.servicios import validacion, ventas_servicio

bp = Blueprint("ventas", __name__, url_prefix="/ventas")


@bp.route("/")
def listado():
    filtros = FiltrosVentas.desde_diccionario(request.args)
    orden = request.args.get("orden", "fecha")
    direccion = request.args.get("direccion", "desc")
    pagina = max(request.args.get("pagina", 1, type=int), 1)
    por_pagina = current_app.config["REGISTROS_POR_PAGINA"]

    ventas, total = ventas_repositorio.listar_pagina(filtros, orden, direccion, pagina, por_pagina)
    return render_template(
        "ventas_listado.html",
        ventas=ventas,
        total=total,
        pagina=pagina,
        paginas=max(math.ceil(total / por_pagina), 1),
        filtros=filtros,
        orden=orden,
        direccion=direccion,
        categorias=ventas_repositorio.listar_categorias(),
    )


@bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    datos: dict = {}
    errores: dict = {}
    if request.method == "POST":
        datos = request.form.to_dict()
        _, errores = ventas_servicio.crear_venta(datos)
        if not errores:
            flash("Venta registrada correctamente.", "exito")
            return redirect(url_for(".listado"))
        flash("Revisá los campos marcados en rojo.", "error")
    return render_template(
        "ventas_formulario.html",
        datos=datos,
        errores=errores,
        columnas=validacion.COLUMNAS,
        categorias=ventas_repositorio.listar_categorias(),
    )


@bp.route("/<int:venta_id>/eliminar", methods=["POST"])
def eliminar(venta_id: int):
    if not ventas_servicio.eliminar_venta(venta_id):
        abort(404)
    flash("Venta eliminada.", "exito")
    return redirect(url_for(".listado"))


@bp.route("/vaciar", methods=["POST"])
def vaciar():
    cantidad = ventas_servicio.vaciar_datos()
    flash(f"Se borraron {cantidad} ventas y el historial de importaciones.", "exito")
    return redirect(url_for("principal.inicio"))
