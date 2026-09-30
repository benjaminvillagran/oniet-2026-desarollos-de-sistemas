"""Listado, detalle, alta, edición y baja de ventas."""

from __future__ import annotations

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
    por_pagina = current_app.config["REGISTROS_POR_PAGINA"]
    totales = ventas_repositorio.totales(filtros)
    paginas = max(math.ceil(totales["ventas"] / por_pagina), 1)
    # La página pedida se ajusta a las que existen (?pagina=999999 muestra la última)
    pagina = min(max(request.args.get("pagina", 1, type=int), 1), paginas)

    ventas, total = ventas_repositorio.listar_pagina(filtros, orden, direccion, pagina, por_pagina)
    return render_template(
        "ventas_listado.html",
        ventas=ventas,
        total=total,
        pagina=pagina,
        paginas=paginas,
        filtros=filtros,
        orden=orden,
        direccion=direccion,
        categorias=ventas_repositorio.listar_categorias(),
        totales=totales,
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
    return _mostrar_formulario("Nueva venta", datos, errores)


@bp.route("/<int:venta_id>")
def detalle(venta_id: int):
    venta = ventas_repositorio.obtener_por_id(venta_id)
    if venta is None:
        abort(404)
    return render_template("ventas_detalle.html", venta=venta)


@bp.route("/<int:venta_id>/editar", methods=["GET", "POST"])
def editar(venta_id: int):
    venta = ventas_repositorio.obtener_por_id(venta_id)
    if venta is None:
        abort(404)
    datos: dict = venta
    errores: dict = {}
    if request.method == "POST":
        datos = request.form.to_dict()
        errores = ventas_servicio.editar_venta(venta_id, datos)
        if not errores:
            flash("Venta actualizada correctamente.", "exito")
            return redirect(url_for(".detalle", venta_id=venta_id))
        flash("Revisá los campos marcados en rojo.", "error")
    return _mostrar_formulario("Editar venta", datos, errores, venta_id)


def _mostrar_formulario(titulo: str, datos: dict, errores: dict, venta_id: int | None = None):
    return render_template(
        "ventas_formulario.html",
        titulo=titulo,
        venta_id=venta_id,
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
