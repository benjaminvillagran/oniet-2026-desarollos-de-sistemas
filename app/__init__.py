"""Fábrica de la aplicación Flask.

El sistema está organizado en capas (cada una tiene una sola responsabilidad):

    rutas/        Reciben el pedido del navegador y devuelven la página. Sin lógica.
    servicios/    LEER archivos, VALIDAR, PROCESAR (cálculos) y coordinar el guardado.
    repositorios/ GUARDAR y consultar en la base de datos (solo SQL).
    utils/        Conversión de datos y formato para mostrar.
    templates/    Páginas HTML (Jinja2).  static/: CSS y JavaScript.
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template

from app import db
from app.config import Config
from app.utils.formato import registrar_filtros


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    db.registrar(app)
    registrar_filtros(app)
    _registrar_rutas(app)
    _registrar_paginas_de_error(app)

    @app.context_processor
    def datos_generales():
        return {
            "nombre_sistema": app.config["NOMBRE_SISTEMA"],
            "nombre_equipo": app.config["NOMBRE_EQUIPO"],
        }

    return app


def _registrar_rutas(app: Flask) -> None:
    from app.rutas import (
        api_rutas,
        importacion_rutas,
        principal_rutas,
        reportes_rutas,
        ventas_rutas,
    )

    for modulo in (principal_rutas, importacion_rutas, ventas_rutas, reportes_rutas, api_rutas):
        app.register_blueprint(modulo.bp)


def _registrar_paginas_de_error(app: Flask) -> None:
    def pagina_error(codigo: int, titulo: str, mensaje: str):
        return render_template("error.html", codigo=codigo, titulo=titulo, mensaje=mensaje), codigo

    @app.errorhandler(404)
    def no_encontrado(_error):
        return pagina_error(404, "Página no encontrada", "La página que buscás no existe.")

    @app.errorhandler(413)
    def archivo_muy_grande(_error):
        limite_mb = app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)
        return pagina_error(413, "Archivo muy grande", f"El máximo permitido es {limite_mb} MB.")

    @app.errorhandler(500)
    def error_interno(_error):
        return pagina_error(500, "Error interno", "Ocurrió un error inesperado. Probá de nuevo.")
