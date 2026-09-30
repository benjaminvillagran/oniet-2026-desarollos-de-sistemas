@echo off
REM Revisa tests, estilo y que el sistema arranque. Usar ANTES de cada push.
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    echo Primero ejecuta iniciar.bat para instalar el entorno.
    if not defined CI pause
    exit /b 1
)
set PATH=%~dp0.venv\Scripts;%PATH%
.venv\Scripts\python.exe herramientas\verificar.py --arreglar
set RESULTADO=%errorlevel%
if not defined CI pause
exit /b %RESULTADO%
