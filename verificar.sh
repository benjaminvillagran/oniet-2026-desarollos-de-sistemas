#!/usr/bin/env bash
# Revisa tests, estilo y que el sistema arranque. Usar ANTES de cada push.
cd "$(dirname "$0")"
source .venv/bin/activate
python herramientas/verificar.py --arreglar
