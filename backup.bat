@echo off
setlocal enabledelayedexpansion

REM Obtém o diretório atual do .bat
set CURRENT_DIR=%~dp0
cd /d %CURRENT_DIR%

REM Verifica se o ambiente virtual existe
if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
    call .venv\Scripts\activate
    echo Instalando dependências...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate
)

echo Iniciando o monitoramento...
python main.py
