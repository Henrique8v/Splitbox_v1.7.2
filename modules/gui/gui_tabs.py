import os
import sys
import customtkinter as ctk
from tkinterweb import HtmlFrame
from modules.gui.gui_configs import render_config_tab
from modules.gui.gui_events import GUIEvents as events

def show_motor_content(master):
    master.clear_main_content()
    
    ctk.CTkLabel(master.main_content, text="Motor de Sistema", 
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(0, 10))

    # --- FRAME DA LISTA DE EXECUTÁVEIS ---
    prompt_frame = ctk.CTkFrame(master.main_content, corner_radius=8, border_width=1, border_color="#333")
    prompt_frame.pack(fill="x", pady=(0, 10))
    
    master.exe_listbox = ctk.CTkScrollableFrame(prompt_frame, height=120, fg_color="#1A1A1A", label_text="Executáveis")
    master.exe_listbox.pack(fill="x", padx=8, pady=8)
    
    # Barra de ferramentas da lista
    btn_f = ctk.CTkFrame(prompt_frame, fg_color="transparent")
    btn_f.pack(fill="x", padx=8, pady=(0, 8))
    
    ctk.CTkButton(btn_f, text="+ ADD", width=70, 
                  command=lambda: events.add_exe(master)).pack(side="left", padx=2)
    
    ctk.CTkButton(btn_f, text="- REM", width=70, 
                  command=master.remove_executable).pack(side="left", padx=2)
    
    ctk.CTkButton(btn_f, text="LANÇAR SELECIONADO", fg_color="#16a085", hover_color="#1abc9c", 
                  command=lambda: events.start_single_exe(master)).pack(side="left", padx=2, expand=True, fill="x")

    ctk.CTkButton(btn_f, text="LIMPAR", width=70, fg_color="#A51F1F", 
                  command=master.clear_all_executables).pack(side="right", padx=2)
    
    # --- SEÇÃO DE FERRAMENTAS RÁPIDAS (Substituindo a antiga checkbox do mouse) ---
    tools_f = ctk.CTkFrame(prompt_frame, fg_color="transparent")
    tools_f.pack(fill="x", padx=5, pady=(0, 5))

    # Botão DLL
    ctk.CTkButton(
        tools_f, 
        text="🎮 FORÇAR CONTROLES (DLL)",
        fg_color="#4A148C", 
        hover_color="#6A1B9A",
        height=28,
        font=("Segoe UI", 10, "bold"),
        command=lambda: master.manager.force_multiplayer_input()
    ).pack(side="left", padx=5, expand=True, fill="x")

    # Botão .BAT corrigido para chamar a ponte que criamos no master
    ctk.CTkButton(
        tools_f,
        text="📝 CRIAR WINDOWED.BAT",
        fg_color="#9B59B6",
        hover_color="#8E44AD",
        height=28,
        font=("Segoe UI", 10, "bold"),
        command=master.action_create_windowed_bat 
    ).pack(side="left", padx=5, expand=True, fill="x")

    # Label de Info
    master.batch_info_label = ctk.CTkLabel(
        prompt_frame,
        text="ℹ️ Selecione um jogo para gerar o atalho .bat",
        text_color="#9DB4C4",
        font=("Segoe UI", 9)
    )
    master.batch_info_label.pack(pady=(0, 5)) 
    master.update_listbox()

    # --- GRID DE CONFIGURAÇÕES E SISTEMA ---
    grid = ctk.CTkFrame(master.main_content, fg_color="transparent")
    grid.pack(fill="both", expand=True, pady=5)
    grid.columnconfigure((0, 1, 2), weight=1, uniform="col")

    # COLUNA 1: MODO JANELA
    c1 = _create_card(grid, 0, "MODO JANELA")

    ctk.CTkCheckBox(c1, text="Sandbox: Isolamento", 
                    variable=master.use_sandbox_var, 
                    text_color="#88cacf").pack(anchor="w", padx=10, pady=(5, 2))

    ctk.CTkCheckBox(c1, text="Clean UI: Sem bordas", 
                    variable=master.clean_ui_var, 
                    text_color="#88cacf").pack(anchor="w", padx=10, pady=2)

    ctk.CTkCheckBox(c1, text="DXWND: Forçar Modo Janela", 
                    variable=master.use_dxw_var, 
                    text_color="#88cacf").pack(anchor="w", padx=10, pady=(2, 5))

    ctk.CTkCheckBox(c1, text="Liberar Mouse (Menu Mode)", 
                    variable=master.free_mouse_var, 
                    command=master.update_mouse_state, 
                    text_color="#88cacf").pack(anchor="w", padx=10, pady=(10, 5)) 

    # COLUNA 2: ALINHAMENTO
    c2 = _create_card(grid, 1, "ALINHAMENTO")
    for label, mode in [("GRADE", "grid"), ("VERTICAL", "vertical"), ("HORIZONTAL", "horizontal")]:
        ctk.CTkButton(
            c2, text=label, height=28, 
            command=lambda m=mode: master.workflow.quick_align_workflow(m, master.clean_ui_var.get())
        ).pack(fill="x", pady=2, padx=10)
        
    # COLUNA 3: SISTEMA
    c3 = _create_card(grid, 2, "SISTEMA")  
    sub = ctk.CTkFrame(c3, fg_color="transparent")
    sub.pack(fill="x", padx=10, pady=(10, 2))
    ctk.CTkButton(sub, text="DXW", width=45, height=24, fg_color="#333", command=master.toggle_dxwnd).pack(side="left", expand=True, padx=1)
    ctk.CTkButton(sub, text="SBIE", width=45, height=24, fg_color="#333", command=master.toggle_sbie).pack(side="left", expand=True, padx=1)

    ctk.CTkButton(c3, text="TERMINATE ALL", fg_color="transparent", border_width=1, border_color="#A51F1F", 
                  text_color="#A51F1F", command=master.cleanup).pack(fill="x", padx=10, pady=10)

def _create_card(parent, col, title):
    f = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=8)
    f.grid(row=0, column=col, padx=5, sticky="nsew")
    ctk.CTkLabel(f, text=title, font=("Segoe UI", 11, "bold"), text_color="#3b8ed0").pack(pady=10)
    return f

def show_config_content(master):
    master.clear_main_content()
    render_config_tab(master)

def show_status_content(master):
    master.clear_main_content()
    render_html_tab(master.main_content, "status.html")

def show_help_content(master):
    master.clear_main_content()
    render_html_tab(master.main_content, "tutorial.html")

def show_about_content(master):
    master.clear_main_content()
    render_html_tab(master.main_content, "about.html")

def render_html_tab(parent_frame, file_name):
    container = ctk.CTkFrame(parent_frame, corner_radius=10)
    container.pack(expand=True, fill="both", padx=5, pady=5)
    
    try:
        browser = HtmlFrame(container, messages_enabled=False)
        browser.pack(expand=True, fill="both")
        
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(root_dir, "html", file_name)
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: 
                browser.load_html(f.read())
        else:
            browser.load_html("<body style='background:#1a1a1a;color:white;'><h2>HTML não encontrado.</h2></body>")
    except Exception as e:
        ctk.CTkLabel(container, text=f"Erro ao carregar aba: {file_name}").pack(pady=20)