import customtkinter as ctk
import os
import json

def render_network_tab(master):
    """Renderiza a interface de rede (ZeroTier) no container principal."""
    master.clear_main_content()
    
    f = ctk.CTkFrame(master.main_content, corner_radius=10)
    f.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(f, text="Gerenciador de Rede Virtual (ZeroTier)", 
                 font=("Segoe UI", 18, "bold")).pack(pady=20)
    
    # Campo de entrada de ID
    master.zt_id_entry = ctk.CTkEntry(f, placeholder_text="Network ID (16 caracteres)", width=300)
    master.zt_id_entry.pack(pady=10)

    # Lógica de carregamento do JSON
    if os.path.exists(master.net_config_path):
        try:
            with open(master.net_config_path, "r") as j:
                data = json.load(j)
                saved_id = data.get("last_network_id", "")
                if saved_id:
                    master.zt_id_entry.insert(0, saved_id)
        except Exception as e:
            print(f" [ERRO] Falha ao carregar ID de rede: {e}")

    # Grade de Botões
    btn_grid = ctk.CTkFrame(f, fg_color="transparent")
    btn_grid.pack(pady=10)

    # Comandos vindo dos Mixins herdados no master
    ctk.CTkButton(btn_grid, text="CONECTAR / JOIN", fg_color="#16a085", 
                  command=master.save_and_join).pack(side="left", padx=5)
    
    ctk.CTkButton(btn_grid, text="VERIFICAR STATUS", 
                  command=master.action_zt_status).pack(side="left", padx=5)

    master.zt_status_display = ctk.CTkLabel(f, text="Status: Aguardando...", text_color="gray")
    master.zt_status_display.pack(pady=20)