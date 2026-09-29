"""Punto de entrada del sistema.

Ejecutar:   python run.py
Abrir:      http://127.0.0.1:5000
Otro puerto (si el 5000 está ocupado, por ejemplo en Mac):  PORT=5001 python run.py
"""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))
