import threading
import time
import os 
import win32gui
import win32process
import psutil
import ctypes
from modules.window_engine.window_force import WindowForcer

class AlignManager:
    def __init__(self, gui_root, splitscreen_manager):
        self.root = gui_root
        self.manager = splitscreen_manager
        self.is_busy = False
        self.window_forcer = WindowForcer()  # ✅ NOVO

    def quick_align_workflow(self, mode, clean_ui):
        """Alinhamento manual imediato"""
        if self.is_busy: return
        target_mode = mode.strip().lower()
        threading.Thread(target=self._exec_align, args=(target_mode, clean_ui), daemon=True).start()

    def _exec_align(self, mode, clean_ui):
        self.is_busy = True
        try:
            self.manager.apply_layout(mode, clean_ui)
        
            from modules.window_engine.window_utils import WindowUtils
            hwnds = WindowUtils.get_managed_hwnds(self.manager.pids, self.manager.pids_to_paths_map)
        
            if hwnds:
                from modules.input_management.identity_manager import IdentityManager
                from modules.input_management.mouse_logic import MouseLogic
            
                IdentityManager.apply_identity(hwnds)
                MouseLogic.toggle_mouse_lock(hwnds, self.root.free_mouse_var.get())
            
                print(f" [OK] {len(hwnds)} instâncias sincronizadas.")
            
        except Exception as e:
            print(f" [ERRO] Falha no alinhamento rápido: {e}")
        finally:
            self.is_busy = False        

    def start_process_workflow(self, executables, use_sandbox, mode, clean_ui):
        """Workflow: Lançamento Híbrido com Window Force integrado"""
        if not executables or self.is_busy: return

        # Captura configurações
        try:
            l_delay = float(self.root.settings.get("launch_delay", 2.0))
            use_dxw = self.root.use_dxw_var.get()
            dx_path = self.root.settings.get("dxwnd_path", "")
            
            # ✅ NOVO: Capturar configurações do Window Force
            window_force_enabled = hasattr(self.root, 'force_remove_borders_var')
            window_force_strategy = self.root.window_force_strategy.get() if hasattr(self.root, 'window_force_strategy') else 'auto'
            remove_borders = self.root.force_remove_borders_var.get() if window_force_enabled else True
            remove_titlebar = self.root.force_remove_titlebar_var.get() if window_force_enabled else True
            
        except:
            l_delay, use_dxw, dx_path = 2.0, False, ""
            window_force_enabled = False
            window_force_strategy = 'auto'
            remove_borders = True
            remove_titlebar = True

        def run():
            self.is_busy = True
            try:
                # 1. Limpa o motor antes de começar
                self.manager.cleanup()
                
                # 2. Loop de Lançamento com Window Force
                launched_pids = []
                
                for exe in executables:
                    print(f" [MOTOR] Lançando: {os.path.basename(exe)}")
                    
                    # ✅ NOVO: Aplicar Window Force se habilitado
                    if window_force_enabled:
                        print(f"  [WINDOW_FORCE] Usando estratégia: {window_force_strategy}")
                        
                        wf_result = self.window_forcer.launch_windowed(
                            exe,
                            strategy=window_force_strategy,
                            remove_borders=remove_borders,
                            remove_titlebar=remove_titlebar
                        )
                        
                        if wf_result['success']:
                            print(f"  ✅ Window Force aplicado com sucesso")
                            launched_pids.extend(wf_result['pids'])
                        else:
                            print(f"  ⚠️  Window Force não conseguiu forçar, tentando método alternativo...")
                    
                    # Lançamento alternativo (se Window Force falhar ou estiver desabilitado)
                    if use_dxw:
                        print(f" [MOTOR] Método: DXWnd")
                        self.manager.launch_game_with_dxw(exe, dx_path)
                    else:
                        print(f" [MOTOR] Método: Sistema (SBIE: {use_sandbox})")
                        self.manager.launch_game(exe, use_sandbox=use_sandbox)
                    
                    time.sleep(l_delay)
                
                print(" [MOTOR] Lançamento concluído. Iniciando Identidade e Alinhamento...")

                # 3. Captura os HWNDs reais
                from modules.window_engine.window_utils import WindowUtils
                from modules.input_management.identity_manager import IdentityManager

                hwnds = WindowUtils.get_managed_hwnds(self.manager.pids, self.manager.pids_to_paths_map)

                if hwnds:
                    # 4. Carimba Player 1, 2, 3... via PostMessage
                    IdentityManager.apply_identity(hwnds)
                    
                    # 5. Aplica o layout (Grade, Vertical, etc.)
                    self.manager.apply_layout(mode, clean_ui)
                    
                    print(f" [OK] {len(hwnds)} instâncias alinhadas e identificadas.")
                else:
                    print(" [AVISO] Nenhuma janela detectada para alinhar.")

            except Exception as e:
                print(f" [ERRO WORKFLOW] {e}")
                import traceback
                traceback.print_exc()
            finally:
                self.is_busy = False

        threading.Thread(target=run, daemon=True).start()