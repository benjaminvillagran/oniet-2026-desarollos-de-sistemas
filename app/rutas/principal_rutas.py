"""Página de inicio y descarga de archivos de ejemplo."""

from flask import Blueprint, current_app, render_template, send_from_directory

from app.repositorios import importaciones_repositorio
from app.servicios import reportes_servicio

bp = Blueprint("principal", __name__)


@bp.route("/")
def inicio():
    informes = reportes_servicio.obtener_informes()
    return render_template(
        "inicio.html",
        resumen=informes["resumen"],
        operadores=informes["operadores"],
        importaciones=importaciones_repositorio.listar_recientes(5),
    )


@bp.route("/ejemplos/<path:nombre>")
def descargar_ejemplo(nombre: str):
    # send_from_directory impide salir de la carpeta (no se puede pedir ../../algo)
    return send_from_directory(current_app.config["CARPETA_EJEMPLOS"], nombre, as_attachment=True)
