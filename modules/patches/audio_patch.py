import ctypes
import os
from ctypes import wintypes 

class AudioPatch:
    def __init__(self):
        # ✅ CORRETO: Referencia modules/core/bin/
        self.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core", "bin")
        self.dll_name = "window_audio_ext.dll" 
        self.lib = self._load_module()
        
        if self.lib:
            try:
                self.lib.SetMute.argtypes = [wintypes.HWND, ctypes.c_bool]
                self.lib.SetMute.restype = ctypes.c_bool
                print(f" [AUDIO] DLL carregada com sucesso")
            except Exception as e:
                print(f"[AUDIO_PATCH] Erro ao definir tipos: {e}")

    def _load_module(self):
        path = os.path.join(self.base_path, self.dll_name)
        if os.path.exists(path):
            try:
                print(f" [AUDIO] Carregando: {path}")
                return ctypes.CDLL(path)
            except Exception as e:
                print(f"[ERRO AUDIO] Falha ao carregar {self.dll_name}: {e}")
        else:
            print(f"[AVISO AUDIO] DLL não encontrada: {path}")
        return None

    def set_mute_state(self, hwnd, mute=True):
        if self.lib:
            try:
                return self.lib.SetMute(hwnd, mute)
            except Exception as e:
                print(f"[AUDIO_PATCH] Erro na execução: {e}")
        return False