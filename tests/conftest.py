"""Configuración compartida de los tests: cada test usa una base de datos nueva y vacía."""

import io

import pytest

from app import create_app

CSV_VALIDO = (
    "fecha;producto;categoria;cantidad;precio_unitario\n"
    "15/03/2026;Alfajor;Kiosco;3;1200\n"
    "16/03/2026;Agua;Bebidas;2;900,50\n"
    "02/04/2026;Alfajor;kiosco;1;1200\n"
)


@pytest.fixture
def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "prueba.db"),
            "SECRET_KEY": "pruebas",
            # Los tests de páginas corren sin login aunque la consigna lo active en config.py
            # (el login se prueba aparte con la fixture cliente_con_login).
            "LOGIN_OBLIGATORIO": False,
        }
    )


@pytest.fixture
def cliente(app):
    return app.test_client()


@pytest.fixture
def cliente_con_login(tmp_path):
    """Cliente de un sistema con LOGIN_OBLIGATORIO activado."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "login.db"),
            "SECRET_KEY": "pruebas",
            "LOGIN_OBLIGATORIO": True,
        }
    )
    return app.test_client()


@pytest.fixture
def importar(cliente):
    """Sube un archivo a /importar/ como lo haría el navegador."""

    def _importar(contenido, nombre="ventas.csv"):
        if isinstance(contenido, str):
            contenido = contenido.encode("utf-8")
        return cliente.post(
            "/importar/",
            data={"archivo": (io.BytesIO(contenido), nombre)},
            content_type="multipart/form-data",
            follow_redirects=True,
        )

    return _importar
