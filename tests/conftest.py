"""Configuración compartida de los tests: cada test usa una base de datos nueva y vacía."""

import io

import pytest

from app import create_app

CSV_VALIDO = (
    "NumeroRegistro,OperadorLogistico,Anio,Mes,CantidadEnvios,Region,CostoPorEnvio,PorcentajeEntregasATiempo\n"
    "1,LogisticaSur,2024,1,10,Centro,100.5,80\n"
    "2,TransRuta,2024,2,5,Norte,1000,90\n"
    "3,LogisticaSur,2025,1,20,Norte,50,100\n"
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

    def _importar(contenido, nombre="servicios.csv"):
        if isinstance(contenido, str):
            contenido = contenido.encode("utf-8")
        return cliente.post(
            "/importar/",
            data={"archivo": (io.BytesIO(contenido), nombre)},
            content_type="multipart/form-data",
            follow_redirects=True,
        )

    return _importar
