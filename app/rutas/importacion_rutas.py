"""Importación de archivos e historial de importaciones."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app.repositorios import importaciones_repositorio
from app.servicios import importacion_servicio, validacion
from app.servicios.lector import FORMATOS_SOPORTADOS, ErrorLectura

bp = Blueprint("importacion", __name__, url_prefix="/importar")


def _archivos_de_ejemplo() -> list[str]:
    carpeta = current_app.config["CARPETA_EJEMPLOS"]
    return sorted(archivo.name for archivo in carpeta.iterdir() if archivo.is_file())


@bp.route("/", methods=["GET", "POST"])
def importar():
    if request.method == "POST":
        archivo = request.files.get("archivo")
        if archivo is None or archivo.filename == "":
            flash("Elegí un archivo para importar.", "error")
            return redirect(url_for(".importar"))
        try:
            resumen = importacion_servicio.importar_archivo(archivo.filename, archivo.read())
        except ErrorLectura as error:
            flash(f"No se pudo importar «{archivo.filename}»: {error}", "error")
            return redirect(url_for(".importar"))

        categoria = "exito" if not resumen.errores else "aviso"
        flash(f"Se guardaron {resumen.filas_guardadas} de {resumen.filas_leidas} filas.", categoria)
        return render_template("importacion_resultado.html", resumen=resumen)

    return render_template(
        "importar.html",
        columnas=validacion.COLUMNAS,
        formatos=FORMATOS_SOPORTADOS,
        ejemplos=_archivos_de_ejemplo(),
    )


@bp.route("/historial")
def historial():
    return render_template(
        "importacion_historial.html", importaciones=importaciones_repositorio.listar_recientes()
    )
