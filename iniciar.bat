@echo off
REM Instala lo necesario (la primera vez) y levanta el sistema en http://127.0.0.1:5000
REM Otro puerto:  set PORT=5001  (antes de ejecutar este archivo)
REM Solo instalar, sin levantar el sistema:  iniciar.bat --solo-instalar
cd /d "%~dp0"

REM Si el entorno virtual quedo incompleto (instalacion cortada), se borra y se vuelve a crear
if exist .venv if not exist .venv\Scripts\python.exe rmdir /s /q .venv

if not exist .venv\Scripts\python.exe (
    echo Creando entorno virtual...
    python -m venv .venv || py -3 -m venv .venv
)
if not exist .venv\Scripts\python.exe (
    echo.
    echo ERROR: no se pudo crear el entorno virtual. Revisar que Python este instalado
    echo y en el PATH. Ver docs\02_CONFIGURAR_NOTEBOOK.md
    if not defined CI pause
    exit /b 1
)

REM Si hay una carpeta wheels (preparada con pip download), se instala sin internet
if exist wheels (
    .venv\Scripts\python.exe -m pip install --no-index --find-links=wheels -r requirements-dev.txt
) else (
    .venv\Scripts\python.exe -m pip install -r requirements-dev.txt
)
if errorlevel 1 (
    echo ERROR: no se pudieron instalar los paquetes. Revisar la conexion a internet.
    if not defined CI pause
    exit /b 1
)
if /i "%~1"=="--solo-instalar" exit /b 0

echo.
echo Abri http://127.0.0.1:5000 en el navegador. Para cortar: Ctrl+C
.venv\Scripts\python.exe run.py
pause
