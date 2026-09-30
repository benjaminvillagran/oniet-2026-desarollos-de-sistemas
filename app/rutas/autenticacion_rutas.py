"""Ingreso, registro, salida y cuenta de usuario.

Si LOGIN_OBLIGATORIO es True (config.py), todas las páginas piden haber iniciado sesión,
salvo las de esta lista pública.
"""

from __future__ import annotations

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.repositorios import usuarios_repositorio
from app.servicios import autenticacion_servicio
from app.utils.formato import formato_fecha

bp = Blueprint("autenticacion", __name__)

ENDPOINTS_PUBLICOS = {"autenticacion.ingresar", "autenticacion.registrarse", "static"}


@bp.before_app_request
def cargar_usuario():
    usuario_id = session.get("usuario_id")
    g.usuario = usuarios_repositorio.obtener_por_id(usuario_id) if usuario_id else None
    requiere_login = current_app.config["LOGIN_OBLIGATORIO"] and request.endpoint is not None
    if requiere_login and g.usuario is None and request.endpoint not in ENDPOINTS_PUBLICOS:
        return redirect(url_for("autenticacion.ingresar", siguiente=request.path))
    return None


def _destino_seguro(destino: str | None) -> str:
    """Solo se permite volver a una página de este mismo sistema (evita redirecciones externas)."""
    if destino and destino.startswith("/") and not destino.startswith("//"):
        return destino
    return url_for("principal.inicio")


@bp.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if request.method == "POST":
        usuario = autenticacion_servicio.autenticar(
            request.form.get("nombre_usuario", ""), request.form.get("clave", "")
        )
        if usuario is None:
            flash("Usuario o clave incorrectos.", "error")
        else:
            session.clear()
            session["usuario_id"] = usuario["id"]
            anterior = usuario["ultimo_acceso"]
            aviso = f"Tu último acceso fue el {formato_fecha(anterior)}." if anterior else ""
            flash(f"Hola, {usuario['nombre_usuario']}. {aviso or 'Es tu primer acceso.'}", "exito")
            return redirect(_destino_seguro(request.args.get("siguiente")))
    return render_template("autenticacion_ingresar.html")


@bp.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    datos: dict = {}
    errores: dict = {}
    if request.method == "POST":
        datos = request.form.to_dict()
        _, errores = autenticacion_servicio.registrar_usuario(
            datos.get("nombre_usuario", ""), datos.get("clave", ""), datos.get("confirmacion", "")
        )
        if not errores:
            flash("Cuenta creada. Ya podés ingresar.", "exito")
            return redirect(url_for(".ingresar"))
    return render_template("autenticacion_registrarse.html", datos=datos, errores=errores)


@bp.route("/salir", methods=["POST"])
def salir():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for(".ingresar"))


@bp.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if g.usuario is None:
        return redirect(url_for(".ingresar", siguiente=request.path))
    errores: dict = {}
    if request.method == "POST":
        errores = autenticacion_servicio.cambiar_clave(
            g.usuario["id"],
            request.form.get("clave_actual", ""),
            request.form.get("clave", ""),
            request.form.get("confirmacion", ""),
        )
        if not errores:
            flash("Clave actualizada.", "exito")
            return redirect(url_for(".cuenta"))
    return render_template("autenticacion_cuenta.html", errores=errores)
