import win32gui
import win32con

class MouseLogic:
    WM_SET_MOUSE_LOCK = win32con.WM_USER + 888
    
    @staticmethod
    def toggle_mouse_lock(hwnds, allow_freedom):
        """
        allow_freedom: True (Mouse solto)
        allow_freedom: False (Mouse preso)
        """
        state = 1 if allow_freedom else 0
        for hwnd in hwnds:
            try:
                win32gui.PostMessage(hwnd, MouseLogic.WM_SET_MOUSE_LOCK, state, 0)
            except Exception as e:
                print(f" [ERRO MOUSE] Falha ao comunicar com janela {hwnd}: {e}")