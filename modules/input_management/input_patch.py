import win32gui
import win32con

class InputPatch:
    def __init__(self):
        pass

    def assign_controller(self, hwnd, controller_index):
        """Envia sinal para a janela"""
        try:
            WM_SET_GAMEPAD = win32con.WM_USER + 777
            
            win32gui.PostMessage(hwnd, WM_SET_GAMEPAD, controller_index, 0)
            
            print(f" [PATCH] Identidade enviada: Janela {hwnd} -> Player {controller_index + 1}")
            return True
        except Exception as e:
            print(f" [ERRO PATCH] Falha ao comunicar com a janela: {e}")
            return False