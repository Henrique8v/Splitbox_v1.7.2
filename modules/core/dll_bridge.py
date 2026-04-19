import ctypes
import os

class DLLBridge:
    def __init__(self, gui_root=None):
        self.gui = gui_root
        
        # ✅ CORRETO: Referencia modules/core/bin/
        self.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        
        print(f" [DLL_BRIDGE] Procurando DLLs em: {self.base_path}")
        
        # Carregamento das DLLs do sistema (hooks e audio)
        self.cleaner = self._load_dll("window_cleaner.dll")
        self.forcer = self._load_dll("window_forcer.dll")
        self.snap = self._load_dll("snap_dwm.dll")
        self.audio = self._load_dll("window_audio_ext.dll")
        self.multiplayer_dll = self._load_dll("multiplayer.dll")

    def _load_dll(self, name):
        path = os.path.join(self.base_path, name)
        if os.path.exists(path):
            try: 
                dll = ctypes.CDLL(path)
                print(f" [DLL OK] Carregada: {name}")
                return dll
            except Exception as e:
                print(f"[ERRO DLL] Falha ao carregar {name}: {e}")
        else:
            print(f"[AVISO DLL] Não encontrada: {path}")
        return None

    def apply_window_cleaner(self, hwnd):
        """Remove bordas e botões de controle"""
        if self.cleaner and hasattr(self.cleaner, "RemoveControlButtons"):
            self.cleaner.RemoveControlButtons(hwnd)
            return True
        return False

    def apply_forcer(self, hwnd):
        """Aplica Foco Simultâneo e Borda Vermelha"""
        if self.forcer:
            if hasattr(self.forcer, "ForceActivate"):
                self.forcer.ForceActivate(hwnd)
            if hasattr(self.forcer, "EnableVisualHook"):
                self.forcer.EnableVisualHook(hwnd, True)
            return True
        return False

    def set_window_pos(self, hwnd, x, y, w, h, clean_ui=False):
        """Manipulação via snap_dwm.dll"""
        if self.snap:
            if not clean_ui:
                if hasattr(self.snap, "EnableSnapFeatures"):
                    self.snap.EnableSnapFeatures(hwnd)
        
            if hasattr(self.snap, "MoveAndStretch"):
                self.snap.MoveAndStretch(hwnd, int(x), int(y), int(w), int(h))
                return True
        return False

    def toggle_mute(self, hwnd, mute_state):
        if self.audio and hasattr(self.audio, "SetMute"):
            self.audio.SetMute(hwnd, mute_state)
            return True
        return False