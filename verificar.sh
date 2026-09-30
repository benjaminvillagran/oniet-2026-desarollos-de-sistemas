#!/usr/bin/env bash
# Revisa tests, estilo y que el sistema arranque. Usar ANTES de cada push.
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then echo "Primero ejecutá ./iniciar.sh"; exit 1; fi
PATH="$PWD/.venv/bin:$PATH" .venv/bin/python herramientas/verificar.py --arreglar
