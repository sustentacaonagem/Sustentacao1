@echo off
echo  Gerando executável...


cd /d "%~dp0"

where pyinstaller >nul 2>nul
if errorlevel 1 (
    echo [error] pyinstaller não encontrado. Instalando...
    pip install pyinstaller
)

pyinstaller --onefile --console --icon=Icone.ico "AutUpdt.py"

echo.
echo [Sucesso] Executável gerado em "dist"
pause