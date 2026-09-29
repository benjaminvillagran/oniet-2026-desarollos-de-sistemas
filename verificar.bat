@echo off
REM Revisa tests, estilo y que el sistema arranque. Usar ANTES de cada push.
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python herramientas\verificar.py --arreglar
pause
