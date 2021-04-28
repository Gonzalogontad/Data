@echo off

::START /B %~dp0/.venv/Scripts/python.exe %~dp0/meliData.py

%~dp0.venv\Scripts\activate.bat && %~dp0/.venv/Scripts/python.exe %~dp0/meliData.py && echo Instalacion finalizada && deactivate





