@echo off

::START /B %~dp0/.venv/Scripts/python.exe %~dp0/meliData.py
echo Inicio de captura de datos

%~dp0.venv\Scripts\activate.bat && %~dp0/.venv/Scripts/python.exe %~dp0/meliData.py && echo Fin de captura de datos && deactivate





