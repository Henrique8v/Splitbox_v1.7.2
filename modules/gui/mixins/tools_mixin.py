import os
import subprocess
from modules.input_management.mouse_logic import MouseLogic
from modules.window_engine.window_utils import WindowUtils

class ToolsMixin:
    """Mixin para ferramentas de automação e injeção"""

    def action_create_windowed_bat(self):
        selected_exes = [item["path"] for item in self.exe_check_vars if item["var"].get()]
        if not selected_exes:
            if hasattr(self, 'batch_info_label'):
                self.batch_info_label.configure(text="⚠️ Selecione um jogo na lista acima!", text_color="orange")
            return

        for exe_path in selected_exes:
            try:
                from modules.window_engine.window_force import WindowForcer
                forcer = WindowForcer()
                result = forcer.create_windowed_batch(exe_path)
                if result and hasattr(self, 'batch_info_label'):
                    self.batch_info_label.configure(text=f"✅ BAT criado em: {os.path.basename(exe_path)}", text_color="#4CAF50")
            except Exception as e:
                print(f"[ERRO] Falha ao gerar BAT: {e}")

    def update_mouse_state(self):   
        hwnds = WindowUtils.get_managed_hwnds(self.manager.pids, self.manager.pids_to_paths_map)
        if hwnds:
            state = self.free_mouse_var.get()
            MouseLogic.toggle_mouse_lock(hwnds, state)
            status = "LIVRE" if state else "PRESO (GAMEPLAY)"
            print(f" [MOUSE] Modo alterado para: {status}")

    def toggle_sbie(self):
        sbie_path = self.settings.get("sbie_path", r"C:\Program Files\Sandboxie-Plus\SandMan.exe")
        if os.path.exists(sbie_path):
            subprocess.Popen([sbie_path], creationflags=0x08000000)
            print("[SISTEMA] Painel Sandboxie acionado.")

    def toggle_dxwnd(self):
        dxw_path = self.settings.get("dxwnd_path", "")
        if dxw_path and os.path.exists(dxw_path):
            subprocess.Popen([dxw_path], cwd=os.path.dirname(dxw_path), creationflags=0x08000000)
            print("[SISTEMA] Painel DXWnd acionado.")