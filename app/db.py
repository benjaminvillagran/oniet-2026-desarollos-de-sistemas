"""Conexión a la base de datos SQLite.

SQLite viene incluido en Python: no hay que instalar ningún servidor.
Los datos quedan guardados en el archivo instance/datos.db.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

import click
from flask import Flask, current_app, g

RUTA_ESQUEMA = Path(__file__).with_name("schema.sql")


def obtener_db() -> sqlite3.Connection:
    """Devuelve la conexión del pedido actual (se crea una sola vez por pedido)."""
    if "db" not in g:
        conexion = sqlite3.connect(current_app.config["DATABASE"])
        conexion.row_factory = sqlite3.Row  # permite leer columnas por nombre: fila["producto"]
        conexion.execute("PRAGMA foreign_keys = ON")
        g.db = conexion
    return g.db


def cerrar_db(_error=None) -> None:
    conexion = g.pop("db", None)
    if conexion is not None:
        conexion.close()


@contextmanager
def transaccion():
    """Agrupa operaciones de escritura: si alguna falla, se deshacen todas.

    Uso:
        with transaccion():
            repositorio.insertar(...)
            repositorio.eliminar(...)
    """
    conexion = obtener_db()
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise


def crear_tablas() -> None:
    conexion = obtener_db()
    conexion.executescript(RUTA_ESQUEMA.read_text(encoding="utf-8"))
    conexion.commit()


def reiniciar_db() -> None:
    """Borra TODAS las tablas y las vuelve a crear desde schema.sql (se pierden los datos)."""
    conexion = obtener_db()
    tablas = [
        fila["name"]
        for fila in conexion.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )
    ]
    conexion.execute("PRAGMA foreign_keys = OFF")
    for tabla in tablas:
        conexion.execute(f'DROP TABLE IF EXISTS "{tabla}"')
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.commit()
    crear_tablas()


@click.command("reiniciar-db")
def comando_reiniciar_db() -> None:
    """Comando de consola:  flask --app run reiniciar-db"""
    reiniciar_db()
    click.echo("Base de datos reiniciada.")


def registrar(app: Flask) -> None:
    app.teardown_appcontext(cerrar_db)
    app.cli.add_command(comando_reiniciar_db)
    with app.app_context():
        crear_tablas()
