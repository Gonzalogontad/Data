@echo off
echo.
echo Activar virtual env
echo.


python -m venv .venv
START /B %~dp0/.venv/Scripts/activate.bat

echo Instalacion de componentes

pip install -r %~dp0/requirements.txt


START /B %~dp0/.venv/Scripts/deactivate.bat
