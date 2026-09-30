"""Login opcional: registro, ingreso, último acceso, páginas protegidas y cambio de clave."""

# Una página cualquiera que existe en la plantilla y no depende del problema (no es de "ventas")
PAGINA_PROTEGIDA = "/importar/historial"


def registrar(cliente, nombre="ana", clave="secreta1", confirmacion=None):
    return cliente.post(
        "/registrarse",
        data={"nombre_usuario": nombre, "clave": clave, "confirmacion": confirmacion or clave},
        follow_redirects=True,
    )


def ingresar(cliente, nombre="ana", clave="secreta1", siguiente=None):
    url = "/ingresar" + (f"?siguiente={siguiente}" if siguiente else "")
    return cliente.post(url, data={"nombre_usuario": nombre, "clave": clave})


def test_sin_login_obligatorio_todo_es_accesible(cliente):
    assert cliente.get(PAGINA_PROTEGIDA).status_code == 200
    assert "Ingresar" not in cliente.get("/").get_data(as_text=True)


def test_registro_valida_los_datos(cliente):
    assert "al menos 6" in registrar(cliente, clave="123").get_data(as_text=True)
    assert "no coinciden" in registrar(cliente, confirmacion="otra-clave").get_data(as_text=True)
    assert "De 3 a 30" in registrar(cliente, nombre="a b").get_data(as_text=True)
    assert "Cuenta creada" in registrar(cliente).get_data(as_text=True)
    assert "ya existe" in registrar(cliente).get_data(as_text=True)


def test_ingreso_y_ultimo_acceso(cliente):
    registrar(cliente)
    assert "incorrectos" in cliente.post(
        "/ingresar", data={"nombre_usuario": "ana", "clave": "mala"}, follow_redirects=True
    ).get_data(as_text=True)

    primero = cliente.post(
        "/ingresar", data={"nombre_usuario": "ana", "clave": "secreta1"}, follow_redirects=True
    )
    assert "Es tu primer acceso" in primero.get_data(as_text=True)
    segundo = cliente.post(
        "/ingresar", data={"nombre_usuario": "ana", "clave": "secreta1"}, follow_redirects=True
    )
    assert "Tu último acceso fue el" in segundo.get_data(as_text=True)
    assert "Último acceso" in cliente.get("/cuenta").get_data(as_text=True)


def test_login_obligatorio_protege_las_paginas(cliente_con_login):
    respuesta = cliente_con_login.get(PAGINA_PROTEGIDA)
    assert respuesta.status_code == 302
    assert f"/ingresar?siguiente={PAGINA_PROTEGIDA}" in respuesta.headers["Location"]
    assert cliente_con_login.get("/registrarse").status_code == 200

    registrar(cliente_con_login)
    respuesta = ingresar(cliente_con_login, siguiente=PAGINA_PROTEGIDA)
    assert respuesta.headers["Location"] == PAGINA_PROTEGIDA
    assert cliente_con_login.get(PAGINA_PROTEGIDA).status_code == 200

    cliente_con_login.post("/salir")
    assert cliente_con_login.get(PAGINA_PROTEGIDA).status_code == 302


def test_no_redirige_a_sitios_externos(cliente):
    registrar(cliente)
    respuesta = ingresar(cliente, siguiente="//sitio-malicioso.com")
    assert respuesta.headers["Location"] == "/"


def test_cambiar_clave(cliente):
    registrar(cliente)
    ingresar(cliente)
    datos = {"clave_actual": "mala", "clave": "nueva123", "confirmacion": "nueva123"}
    assert "no es correcta" in cliente.post("/cuenta", data=datos).get_data(as_text=True)

    datos["clave_actual"] = "secreta1"
    assert "Clave actualizada" in cliente.post(
        "/cuenta", data=datos, follow_redirects=True
    ).get_data(as_text=True)
    cliente.post("/salir")
    assert ingresar(cliente, clave="nueva123").status_code == 302


def test_cuenta_sin_sesion_pide_ingresar(cliente):
    assert "/ingresar" in cliente.get("/cuenta").headers["Location"]


def test_la_clave_no_se_guarda_en_texto_plano(app, cliente):
    registrar(cliente)
    with app.app_context():
        from app.repositorios import usuarios_repositorio

        usuario = usuarios_repositorio.obtener_por_nombre("ana")
    assert usuario["clave_hash"] != "secreta1" and len(usuario["clave_hash"]) > 30
