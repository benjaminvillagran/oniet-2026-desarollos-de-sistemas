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
        {"TESTING": True, "DATABASE": str(tmp_path / "prueba.db"), "SECRET_KEY": "pruebas"}
    )


@pytest.fixture
def cliente(app):
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
