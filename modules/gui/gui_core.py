import os
import customtkinter as ctk
from modules.gui.gui_configs import load_settings

PYTHON_313 = r"C:\Users\lorde\AppData\Local\Programs\Python\Python313\python.exe"

def setup_app_variables(master):
    """Lê o JSON e aplica as variáveis ao self (master) da GUI"""
    
    # 1. Carrega o dicionário real do JSON
    master.settings = load_settings()

    # 2. Aplica o Caminho do Sandboxie
    master.sbie_path = master.settings.get("sbie_path")
    
    if not master.sbie_path or not os.path.exists(master.sbie_path):
        default_paths = [
            r"C:\Program Files\Sandboxie-Plus\SandMan.exe",
            r"C:\Program Files\Sandboxie\SandMan.exe"
        ]
        for p in default_paths:
            if os.path.exists(p):
                master.sbie_path = p
                break
                
    master.use_dxw_var = ctk.BooleanVar(value=master.settings.get("use_dxw", False))            

    # 3. Aplica o Caminho do DXWnd
    default_dx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dxwnd", "dxwnd.exe")
    master.dxwnd_path = master.settings.get("dxwnd_path", default_dx)

    # 4. Estado dos Processos e Listas
    master.dxwnd_process = None
    master.sbie_process = None
    master.executables = []

    # 5. Variáveis de Interface
    master.use_sandbox_var = ctk.BooleanVar(value=False)
    master.clean_ui_var = ctk.BooleanVar(value=True)
    
    print(f" [CORE] Configurações aplicadas: Delay={master.settings.get('launch_delay')}s")