import os
from tkinter import messagebox, filedialog
from modules.window_engine.window_force import WindowForcer 

class GUIEvents:
    @staticmethod
    def add_exe(app):
        """Adiciona executável à lista"""
        p = filedialog.askopenfilename(
            title="Selecionar Jogo",
            filetypes=[("Executáveis", "*.exe")]
        )
        if p:
            app.executables.append(p)
            app.update_listbox()
            print(f"[UI] Adicionado: {os.path.basename(p)}")

    @staticmethod
    def start_single_exe(app):
        """Lança os executáveis marcados"""
        try:
            active_items = [item for item in app.exe_check_vars if item["var"].get()]

            if not active_items:
                print("[AVISO] Nenhum jogo marcado!")
                return

            use_sandbox = app.use_sandbox_var.get()
            use_dxw = app.use_dxw_var.get()

            for item in active_items:
                target_path = item["path"]
                exe_name = os.path.basename(target_path)
                
                print(f" [MOTOR] Inicialização: {exe_name} (SBIE: {use_sandbox} | DXW: {use_dxw})")

                if use_dxw:
                    dxw_path = app.settings.get("dxwnd_path", "")
                    app.manager.launch_game_with_dxw(target_path, dxw_path)
                else:
                    app.manager.launch_game(target_path, use_sandbox=use_sandbox)
                    
        except Exception as e:
            print(f"[ERRO] Falha no evento de lançamento avulso: {e}")       

    @staticmethod
    def start_flow(app):
        """Workflow Conjunto"""
        active_exes = [item["path"] for item in app.exe_check_vars if item["var"].get()]
        if not active_exes: 
            print("[AVISO] Nada marcado para iniciar!")
            return
        
        app.workflow.start_process_workflow(
            active_exes, 
            app.use_sandbox_var.get(), 
            None, 
            app.clean_ui_var.get()
        )

    @staticmethod
    def quick_align(app, mode):
        """Chamada para botões de alinhamento rápido"""
        app.workflow.quick_align_workflow(mode, app.clean_ui_var.get())

    # ========================================================================
    # UTILITÁRIOS DE BATCH (WINDOW FORCE)
    # ========================================================================
    
    @staticmethod
    def create_batch_for_selected(app):
        """Cria um arquivo .bat na pasta do jogo para forçar o modo janela via argumentos"""
        try:
            active_items = [item for item in app.exe_check_vars if item["var"].get()]
            
            if not active_items:
                messagebox.showwarning("Aviso", "Selecione um jogo na lista acima primeiro!")
                return
            
            # Se houver vários marcados, cria para o primeiro da seleção
            exe_path = active_items[0]["path"]
            exe_name = os.path.basename(exe_path)
            exe_dir = os.path.dirname(exe_path)
            
            if not os.path.exists(exe_path):
                messagebox.showerror("Erro", f"Arquivo não encontrado: {exe_path}")
                return
            
            print(f"[BATCH] Gerando script para: {exe_name}")
            
            forcer = WindowForcer()
            bat_path = forcer.create_windowed_batch(exe_path, exe_dir)
            
            if bat_path and os.path.exists(bat_path):
                app.batch_info_label.configure(
                    text=f"✓ Batch criado em: {exe_name}",
                    text_color="#00FF64"
                )
                
                messagebox.showinfo(
                    "Sucesso!",
                    f"O arquivo 'Windowed Mode.bat' foi criado na pasta do jogo.\n\n"
                    f"Caminho: {exe_dir}\n\n"
                    f"O sistema agora priorizará este método de lançamento para este jogo."
                )
            else:
                app.batch_info_label.configure(
                    text="✗ Falha ao gerar arquivo .bat",
                    text_color="#FF6B6B"
                )
                messagebox.showerror("Erro", "Não foi possível gravar o arquivo na pasta do jogo (verifique permissões).")
                    
        except Exception as e:
            print(f"[BATCH] ✗ Erro crítico: {e}")
            messagebox.showerror("Erro", f"Erro ao processar Window Force: {e}")