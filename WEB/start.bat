@echo off
SETLOCAL

REM Nome da pasta da virtualenv
set VENV_DIR=venv_web

REM Caminho do interpretador dentro da venv
set PYTHON=%VENV_DIR%\Scripts\python.exe

REM 1. Cria a venv caso não exista
if not exist %VENV_DIR% (
    echo [INFO] Criando ambiente virtual em %VENV_DIR%...
    python -m venv %VENV_DIR%
)

REM 2. Ativa a venv
call %VENV_DIR%\Scripts\activate.bat

REM 3. Instala dependências
echo [INFO] Instalando dependencias do requirements.txt...
pip install --upgrade pip
pip install -r web_requirements.txt

REM 4. Executa o programa
if "%~1"=="" (
    echo [ERRO] Voce precisa informar a cidade. Exemplo:
    echo     start_program.bat "São Paulo - SP"
    pause
    exit /b 1
)

%PYTHON% main.py "%~1"

ENDLOCAL
pause