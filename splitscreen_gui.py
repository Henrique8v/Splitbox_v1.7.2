import customtkinter as ctk
import os
import ctypes
import sys
import json

# Imports dos Mixins (Certifique-se de que o __init__.py na pasta mixins exporta ambos)
from modules.gui.mixins import NetworkMixin, ToolsMixin, ListManagerMixin

# Imports de Core/GUI
from modules.gui.gui_core import setup_app_variables
from modules.gui.gui_tabs import (
    show_config_content, show_help_content, 
    show_about_content, show_status_content, show_motor_content
)
from modules.core.splitscreen_manager import SplitscreenManager
from modules.window_engine.align_manager import AlignManager
from modules.gui.gui_network import render_network_tab # Nova importação

class SPLITBOX_GUI(NetworkMixin, ToolsMixin, ListManagerMixin, ctk.CTk): 
    def __init__(self):
        ctk.CTk.__init__(self) 

        # Configurações iniciais de variáveis e estado
        setup_app_variables(self)
        self.title("Splitbox Alpha 1.7.2 - Lorde Raveno")
        self.geometry("900x750") 
        self.resizable(True, True)

        # Caminhos e variáveis de controle
        self.net_config_path = os.path.join(os.path.dirname(__file__), "network_settings.json")
        self.free_mouse_var = ctk.BooleanVar(value=False)        
        
        try:
            self.manager = SplitscreenManager()
            self.workflow = AlignManager(self, self.manager)
            print(" [OK] Motores sincronizados.")
        except Exception as e:
            print(f"[ERRO] Falha crítica ao iniciar motores: {e}")

        # Construção do layout principal (Sidebar + Content)
        self._setup_main_layout()

    def _setup_main_layout(self):
        """Restaura a estrutura de Sidebar e Grade Principal"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (NAVEGAÇÃO LATERAL) ---
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="SPLITBOX PRO", font=("Segoe UI", 16, "bold")).pack(pady=20)

        # Botões de Navegação
        nav_items = [
            ("CENTRAL", self.show_motor),
            ("NETWORK", self.show_network),
            ("SETTINGS", lambda: show_config_content(self)),
            ("STATUS", lambda: show_status_content(self)),
            ("HELP", lambda: show_help_content(self)),
            ("ABOUT", lambda: show_about_content(self))
        ]

        for text, cmd in nav_items:
            ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", anchor="w", command=cmd).pack(fill="x", padx=10, pady=5)

        # --- CONTAINER DE CONTEÚDO ---
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        
        self.show_motor()

    # --- MÉTODOS DE NAVEGAÇÃO E LIMPEZA ---
    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()            

    def show_motor(self):
        show_motor_content(self)

    def show_network(self):
        render_network_tab(self)        

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        app = SPLITBOX_GUI()
        app.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)