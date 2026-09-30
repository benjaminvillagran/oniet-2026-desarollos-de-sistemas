"""Punto de entrada del sistema.

Ejecutar:   python run.py
Abrir:      http://127.0.0.1:5000
Otro puerto (si el 5000 está ocupado, por ejemplo en Mac):  PORT=5001 python run.py
"""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Modo desarrollo: el servidor se reinicia solo al guardar cambios en el código.
    # Si algo falla, el navegador muestra la página propia de "Error interno" (nunca el detalle
    # técnico, que el jurado no tiene que ver) y el error completo queda escrito en esta terminal.
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.run(
        debug=True,
        use_debugger=False,
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
    )
