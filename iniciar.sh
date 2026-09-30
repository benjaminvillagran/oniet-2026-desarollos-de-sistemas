#!/usr/bin/env bash
# Instala lo necesario (la primera vez) y levanta el sistema en http://127.0.0.1:5000
# Otro puerto:  PORT=5001 ./iniciar.sh
set -e
cd "$(dirname "$0")"
# Si el entorno virtual quedó incompleto (instalación cortada), se borra y se vuelve a crear
if [ -d .venv ] && [ ! -x .venv/bin/python ]; then rm -rf .venv; fi
if [ ! -x .venv/bin/python ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi
# Si hay una carpeta wheels (preparada con pip download), se instala sin internet
if [ -d wheels ]; then
    .venv/bin/python -m pip install --no-index --find-links=wheels -r requirements-dev.txt
else
    .venv/bin/python -m pip install -r requirements-dev.txt
fi
echo
echo "Abrí http://127.0.0.1:5000 en el navegador. Para cortar: Ctrl+C"
.venv/bin/python run.py
