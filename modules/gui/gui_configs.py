import customtkinter as ctk
import json
import os

CONFIG_DIR = "settings"
CONFIG_FILE = os.path.join(CONFIG_DIR, "app_settings.json")

def load_settings():
    """Carrega configurações do JSON"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass

    return {
        "sbie_path": r"C:\Program Files\Sandboxie-Plus\SandMan.exe",
        "dxwnd_path": os.path.join(os.path.dirname(__file__), "dxwnd", "dxwnd.exe"),
        "auto_focus": True,
        "launch_delay": 2.0,
        "sidebar_opacity": 1.0,
        "show_logs": True
    }

def save_settings(data):
    """Salva configurações no JSON"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def render_config_tab(master):
    """Renderiza a aba de configurações"""
    settings = load_settings()
    scroll = ctk.CTkScrollableFrame(master.main_content, fg_color="transparent")
    scroll.pack(expand=True, fill="both", padx=5, pady=5)

    ctk.CTkLabel(scroll, text="PAINEL DE CONFIGURAÇÕES", font=("Segoe UI", 18, "bold"), text_color="#3b8ed0").pack(anchor="w", pady=(0, 20))

    # --- SEÇÃO: CAMINHOS ---
    path_frame = ctk.CTkFrame(scroll, fg_color="#1A1A1A", corner_radius=10)
    path_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(path_frame, text="CAMINHOS DO SISTEMA", font=("Segoe UI", 12, "bold"), text_color="#2b5c50").pack(pady=5, padx=10, anchor="w")
    
    ctk.CTkLabel(path_frame, text="Sandboxie Executável (SandMan.exe):").pack(padx=10, anchor="w")
    sbie_entry = ctk.CTkEntry(path_frame, width=450)
    sbie_entry.insert(0, settings.get("sbie_path", ""))
    sbie_entry.pack(fill="x", padx=10, pady=(0, 10))

    # --- SEÇÃO: ENGINE ---
    eng_frame = ctk.CTkFrame(scroll, fg_color="#1A1A1A", corner_radius=10)
    eng_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(eng_frame, text="MOTOR & PERFORMANCE", font=("Segoe UI", 12, "bold"), text_color="#2b5c50").pack(pady=5, padx=10, anchor="w")
    
    af_var = ctk.BooleanVar(value=settings.get("auto_focus", True))
    ctk.CTkCheckBox(eng_frame, text="Auto-Focus Loop (Forcer DLL)", variable=af_var).pack(padx=10, pady=5, anchor="w")
    
    ctk.CTkLabel(eng_frame, text="Delay entre Lançamentos (segundos):").pack(padx=10, anchor="w")
    delay_entry = ctk.CTkEntry(eng_frame, width=80)
    delay_entry.insert(0, str(settings.get("launch_delay", 2.0)))
    delay_entry.pack(padx=10, pady=(0, 10), anchor="w")

    def apply_changes():
        try:
            new_delay = float(delay_entry.get().replace(",", "."))
            new_data = {
                "sbie_path": sbie_entry.get(),
                "dxwnd_path": settings.get("dxwnd_path"),
                "auto_focus": af_var.get(),
                "launch_delay": new_delay,
                "sidebar_opacity": settings.get("sidebar_opacity", 1.0),
                "show_logs": settings.get("show_logs", True)
            }
            save_settings(new_data)
            master.settings = new_data
            master.sbie_path = new_data["sbie_path"]
            
            save_btn.configure(text="ALTERAÇÕES SALVAS!", fg_color="#1e3d35")
            def reset_button():
                try:
                    if save_btn.winfo_exists():
                        save_btn.configure(text="SALVAR PREFERÊNCIAS", fg_color="#2b5c50")
                except: pass
            master.after(2000, reset_button)
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("Erro de Valor", "O campo Delay deve ser um número válido.")

    save_btn = ctk.CTkButton(scroll, text="SALVAR PREFERÊNCIAS", fg_color="#2b5c50", hover_color="#1e3d35", command=apply_changes)
    save_btn.pack(pady=30)