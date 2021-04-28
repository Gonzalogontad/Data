@echo off
echo.
echo Activar virtual env
echo.


python -m venv .venv

%~dp0.venv\Scripts\activate.bat && echo Instalacion de componentes && pip install -r %~dp0requirements.txt && echo Instalacion finalizada && deactivate



