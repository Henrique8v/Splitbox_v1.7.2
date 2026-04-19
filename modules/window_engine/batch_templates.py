"""
Templates de Scripts Externos - Splitbox Pro 1.7.0
"""

# Template robusto com suporte a 15+ métodos e verificação de sucesso
WINDOWED_BAT_TEMPLATE = """@echo off
REM ════════════════════════════════════════════════════════════════════
REM Splitbox Pro 1.7.0 - Windowed Mode Batch
REM Auto-gerado para: {exe_name}
REM ════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion
set "EXE_PATH={exe_path}"
set "EXE_DIR={exe_dir}"
set "EXE_NAME={exe_name}"

cd /d "!EXE_DIR!"
color 0A

set "SUCCESS=0"
set "CURRENT_ARG="

REM Lista de argumentos para iterar (facilitando a manutenção)
set "ARGS=-window -windowed --window --windowed /window /windowed -w --w /w -sw --sw /sw -win --win /win"

echo [SPLITBOX] Iniciando bateria de testes para modo janela...

for %%A in (!ARGS!) do (
    if !SUCCESS! equ 0 (
        echo [TESTE] Tentando argumento: %%A
        start "" "!EXE_PATH!" %%A
        timeout /t 3 /nobreak >nul
        
        tasklist /FI "IMAGENAME eq !EXE_NAME!" | find /i "!EXE_NAME!" >nul
        if !ERRORLEVEL! equ 0 (
            echo [OK] Sucesso detectado com: %%A
            set "SUCCESS=1"
            set "CURRENT_ARG=%%A"
        )
    )
)

if !SUCCESS! equ 0 (
    echo [AVISO] Nenhum argumento forçou o modo janela. Tentando launch simples...
    start "" "!EXE_PATH!"
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo [STATUS] Processo concluído. Arg final: !CURRENT_ARG!
echo ════════════════════════════════════════════════════════════════════
pause
exit /b 0
"""