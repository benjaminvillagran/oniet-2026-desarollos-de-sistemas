#!/usr/bin/env bash
# Instala lo necesario (la primera vez) y levanta el sistema en http://127.0.0.1:5000
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
echo
echo "Abrí http://127.0.0.1:5000 en el navegador. Para cortar: Ctrl+C"
python run.py
