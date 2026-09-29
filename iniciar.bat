@echo off
REM Instala lo necesario (la primera vez) y levanta el sistema en http://127.0.0.1:5000
cd /d "%~dp0"
if not exist .venv (
    echo Creando entorno virtual...
    python -m venv .venv || py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements-dev.txt
echo.
echo Abri http://127.0.0.1:5000 en el navegador. Para cortar: Ctrl+C
python run.py
pause
