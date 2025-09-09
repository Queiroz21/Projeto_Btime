@echo off
SETLOCAL

REM Nome da pasta da virtualenv
set VENV_DIR=venv_api

REM Caminho do interpretador dentro da venv
set PYTHON=%VENV_DIR%\Scripts\python.exe

REM 1. Cria a venv caso nao exista
if not exist %VENV_DIR% (
    echo [INFO] Criando ambiente virtual em %VENV_DIR%...
    python -m venv %VENV_DIR%
)

REM 2. Ativa a venv
call %VENV_DIR%\Scripts\activate.bat

REM 3. Instala dependencias
echo [INFO] Instalando dependencias do requirements.txt...
pip install --upgrade pip
pip install -r api_requirements.txt

REM 4. Executa o programa
if "%~1"=="" (
    echo [ERRO] Voce precisa informar a cidade. Exemplo:
    echo     start_program.bat "São Paulo"
    exit /b 1
)

%PYTHON% API_Main.py "%~1" 9a91536f9cc10327a689cdae29385073

ENDLOCAL
pause