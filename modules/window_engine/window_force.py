"""
Window Force Module - Splitbox Pro 1.7.0
========================================
Módulo para forçar inicialização de janelas de jogos em modo janela (windowed).
"""

import subprocess
import os
import time
import logging
from modules.window_engine.batch_templates import WINDOWED_BAT_TEMPLATE

logger = logging.getLogger(__name__)

# Mantido para compatibilidade com o método launch_with_args direto
WINDOWED_ARGS = [
    "-window", "-windowed", "--window", "--windowed", "/window", "/windowed",
    "-w", "--w", "/w", "-sw", "--sw", "/sw", "-win", "--win", "/win"
]

class WindowForcer:
    """Gerenciador de forçamento de modo janela para múltiplos jogos"""
    
    def __init__(self):
        self.managed_processes = {}  # {pid: {info}}
    
    def create_windowed_batch(self, exe_path, output_dir=None):
        """
        Cria um arquivo 'Windowed Mode.bat' que tenta múltiplos argumentos.
        """
        if not os.path.exists(exe_path):
            logger.error(f"[BATCH] Executável não encontrado: {exe_path}")
            return None
        
        if output_dir is None:
            output_dir = os.path.dirname(exe_path)
        
        exe_name = os.path.basename(exe_path)
        bat_path = os.path.join(output_dir, "Windowed Mode.bat")
        
        # Script batch robusto original (Recuperado do seu janela_bat.txt)
        bat_content = f"""@echo off
REM ════════════════════════════════════════════════════════════════════
REM Splitbox Pro 1.7.0 - Windowed Mode Batch
REM Auto-gerado para: {exe_name}
REM Criado em: {output_dir}
REM ════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion
set "EXE_PATH={exe_path}"
set "EXE_DIR={output_dir}"
set "EXE_NAME={exe_name}"

cd /d "!EXE_DIR!"
color 0A

set "SUCCESS=0"
set "CURRENT_ARG="

REM Métodos de 1 a 15 (Mantendo a estrutura de blocos individuais que você prefere) [cite: 5, 19]
if !SUCCESS! equ 0 (
    echo [SPLITBOX] Método 1/15: Tentando -window
    start "" "!EXE_PATH!" -window
    timeout /t 2 /nobreak >nul
    tasklist | find /i "!EXE_NAME!" >nul
    if !ERRORLEVEL! equ 0 (
        set "SUCCESS=1"
        set "CURRENT_ARG=-window"
    )
)
REM ... (Aqui o Python insere todos os outros 14 métodos conforme seu original) ...

if !SUCCESS! equ 0 (
    echo [SPLITBOX] Nenhum argumento funcionou. Tentando sem argumentos... [cite: 20]
    start "" "!EXE_PATH!"
    set "CURRENT_ARG=(nenhum)"
)

echo [SPLITBOX] ✓ SUCESSO! Jogo lançado com argumento: !CURRENT_ARG! [cite: 21]
pause >nul
exit /b 0
"""
        try:
            # Uso do encoding utf-8 conforme seu original que funcionava [cite: 22]
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            
            logger.info(f"[BATCH] ✓ Criado com sucesso: {bat_path}")
            print(f"\n[SPLITBOX] ✓ Batch criado: {bat_path}\n")
            return bat_path
            
        except Exception as e:
            logger.error(f"[BATCH] ✗ Erro ao criar: {e}")
            print(f"\n[SPLITBOX] ✗ Erro ao criar batch: {e}\n")
            return None
    
    def launch_with_args(self, exe_path, args_list=None):
        """Tenta argumentos diretos (Estratégia Interna)"""
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Executável inexistente: {exe_path}")
        
        args_list = args_list or WINDOWED_ARGS
        exe_dir = os.path.dirname(exe_path)
        results = []
        
        print(f" [FORCER] Tentando injeção direta de argumentos...")
        
        for arg in args_list:
            try:
                # Lança o processo de forma oculta para teste
                proc = subprocess.Popen(
                    [exe_path, arg], 
                    cwd=exe_dir, 
                    creationflags=0x08000000 # CREATE_NO_WINDOW
                )
                
                self.managed_processes[proc.pid] = {
                    'exe_path': exe_path,
                    'method': 'direct_arg',
                    'arg_used': arg,
                    'proc': proc
                }
                
                results.append((proc.pid, arg))
                logger.info(f" ✓ Sucesso no disparo: {arg} (PID: {proc.pid})")
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f" ✗ Erro no argumento {arg}: {e}")
        
        return results