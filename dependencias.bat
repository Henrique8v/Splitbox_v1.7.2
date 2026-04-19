@echo off
title Splitbox Pro 1.7.0 - Setup Completo
echo =======================================================
echo   INSTALANDO DEPENDENCIAS - SPLITBOX PRO 1.7.0
echo =======================================================
echo.

:: Definindo o caminho do Python 3.13
set PY_PATH="C:\Users\lorde\AppData\Local\Programs\Python\Python313\python.exe"

echo [1/8] Atualizando o Gerenciador PIP...
python -m pip install --upgrade pip

echo [2/8] Instalando bibliotecas base (Requirements)...
python -m pip install -r requirements.txt

echo [3/8] Instalando Interface Moderna (CustomTkinter)...
python -m pip install customtkinter darkdetect packaging

echo [4/8] Instalando Motor WebView2 Chromium (pywebview + .NET)...
python -m pip install pywebview pythonnet bottle proxy_tools typing_extensions

echo [5/8] Instalando Ferramentas de Forja (PyInstaller ^& Auto-py-to-exe)...
python -m pip install pyinstaller auto-py-to-exe

echo [6/8] Configurando extensoes de sistema (PyWin32)...
python -m pip install pywin32>=305

echo [7/8] Instalando dependencias para controle de janelas e gamepads...
python -m pip install psutil pygame pillow

echo [8/8] Configurando PyWin32 Post-Install...
for /f "tokens=*" %%i in ('python -c "import os, sys; print(os.path.join(sys.prefix, 'Scripts', 'pywin32_postinstall.py'))"') do set POST_INSTALL=%%i 
if exist "%POST_INSTALL%" (
    python "%POST_INSTALL%" -install
) else (
    echo [AVISO] Script post-install manual nao localizado, tentando via modulo...
    python -m pywin32_postinstall -install
)

echo.
echo =======================================================
echo   SETUP 1.7.0 COMPLETO! SISTEMA PRONTO.
echo =======================================================
echo.
echo [INFO] Para iniciar: python main_.py
echo [INFO] Ou execute: splitscreen_gui.py diretamente
echo.
pause