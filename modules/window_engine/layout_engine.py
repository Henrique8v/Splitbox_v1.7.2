import time
import math
import win32gui
import win32con
from modules.input_management.identity_manager import IdentityManager

class LayoutEngine:
    def __init__(self, bridge):
        self.bridge = bridge

    def calculate_and_apply(self, hwnds, mode, clean_ui):
        if not hwnds: return
        
        hwnds = list(dict.fromkeys(hwnds))
        num = len(hwnds)
        
        rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        sw = rect[2] - rect[0]
        sh = rect[3] - rect[1]

        if not clean_ui:
            sh -= 40 

        print(f" [DEBUG ENGINE] Modo: {mode} | Resolução: {sw}x{sh} | Janelas: {num}")

        for i, hwnd in enumerate(hwnds):
            if mode == "vertical":
                w, h = sw // num, sh
                x, y = i * w, 0
            elif mode == "horizontal":
                w, h = sw, sh // num
                x, y = 0, i * h
            else: # modo grid
                cols = math.ceil(math.sqrt(num))
                rows = math.ceil(num / cols)
                w, h = sw // cols, sh // rows
                x, y = (i % cols) * w, (i // cols) * h

            try:
                self.bridge.set_window_pos(hwnd, x, y, w, h, clean_ui=clean_ui)
                
                if clean_ui:
                    self.bridge.apply_window_cleaner(hwnd)
                    
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    style |= win32con.WS_THICKFRAME
                    
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
                else:
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    style |= (win32con.WS_CAPTION | win32con.WS_THICKFRAME | win32con.WS_SYSMENU)
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, int(x), int(y), int(w), int(h), 
                                     win32con.SWP_SHOWWINDOW | win32con.SWP_FRAMECHANGED | win32con.SWP_NOACTIVATE)
                                      
            except Exception as e:
                print(f" [ERRO ENGINE] Falha na janela {hwnd}: {e}")
    
    def full_layout_workflow(self, hwnds, mode, clean_ui):
        """Coordena todo o pós-alinhamento"""
        if not hwnds:
            print(" [AVISO] Alinhamento ignorado: Nenhuma janela encontrada.")
            return

        print(f" [MOTOR] Janelas detectadas: {hwnds}")

        self.calculate_and_apply(hwnds, mode.lower(), clean_ui)
        
        time.sleep(0.2)
        
        IdentityManager.apply_identity(hwnds)

        for hwnd in hwnds:
            self.bridge.apply_forcer(hwnd)