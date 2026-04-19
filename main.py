import os
import sys
import customtkinter as ctk
from modules.gui.gui_events import GUIEvents as events 
from splitscreen_gui import SPLITBOX_GUI

def main():
    # 1. Configurações de Aparência
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # 2. Suporte para High DPI 
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            print(f" [AVISO] Não foi possível ajustar DPI: {e}")

    # 3. Inicialização 
    try:
        app = SPLITBOX_GUI()
        
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            app.iconbitmap(icon_path)
            
        print(" [SISTEMA] Splitbox Pro 1.7.1 iniciado com sucesso (RC1).")
        app.mainloop()
        
    except Exception as e:
        print(f" [ERRO CRÍTICO] Falha ao iniciar aplicação: {e}")
        input("Pressione Enter para fechar...")

if __name__ == "__main__":
    main()