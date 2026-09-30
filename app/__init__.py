"""Fábrica de la aplicación Flask.

El sistema está organizado en capas (cada una tiene una sola responsabilidad):

    rutas/        Reciben el pedido del navegador y devuelven la página. Sin lógica.
    servicios/    LEER archivos, VALIDAR, PROCESAR (cálculos) y coordinar el guardado.
    repositorios/ GUARDAR y consultar en la base de datos (solo SQL).
    utils/        Conversión de datos y formato para mostrar.
    templates/    Páginas HTML (Jinja2).  static/: CSS y JavaScript.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from flask import Flask, abort, g, render_template, request

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
    _proteger_formularios(app)
    _registrar_rutas(app)
    _registrar_paginas_de_error(app)

    @app.context_processor
    def datos_generales():
        return {
            "nombre_sistema": app.config["NOMBRE_SISTEMA"],
            "nombre_equipo": app.config["NOMBRE_EQUIPO"],
            "login_activo": app.config["LOGIN_OBLIGATORIO"],
            "usuario_actual": g.get("usuario"),
        }

    return app


def _registrar_rutas(app: Flask) -> None:
    """Registra solas todas las páginas: cada archivo app/rutas/*_rutas.py con una variable `bp`.

    Para agregar páginas nuevas alcanza con crear el archivo `<algo>_rutas.py` con su `bp`.
    """
    from app import rutas

    for modulo in sorted(pkgutil.iter_modules(rutas.__path__), key=lambda m: m.name):
        if modulo.name.endswith("_rutas"):
            app.register_blueprint(importlib.import_module(f"app.rutas.{modulo.name}").bp)


def _proteger_formularios(app: Flask) -> None:
    """Rechaza formularios enviados desde OTRA página web (protección básica contra CSRF).

    Los navegadores indican en el encabezado "Origin" desde qué sitio se envía un formulario.
    Si viene de otro sitio (por ejemplo, una página maliciosa abierta en otra pestaña que
    intenta borrar los datos), el pedido se rechaza.
    """

    @app.before_request
    def verificar_origen():
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            origen = request.headers.get("Origin")
            if origen and origen.rstrip("/") != request.host_url.rstrip("/"):
                abort(403)


def _registrar_paginas_de_error(app: Flask) -> None:
    def pagina_error(codigo: int, titulo: str, mensaje: str):
        return render_template("error.html", codigo=codigo, titulo=titulo, mensaje=mensaje), codigo

    @app.errorhandler(403)
    def prohibido(_error):
        return pagina_error(
            403, "Pedido rechazado", "El formulario no se envió desde este sistema."
        )

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
