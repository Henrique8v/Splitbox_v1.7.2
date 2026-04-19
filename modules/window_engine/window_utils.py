import os
import time
import subprocess
import threading
import win32gui
import win32process
import psutil

class WindowUtils:
    @staticmethod
    def get_managed_hwnds(pids, paths_map):
        if not pids and not paths_map: return []
        hwnds = []
        target_names = [os.path.basename(p).lower() for p in paths_map]

        def cb(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd): return
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                title = win32gui.GetWindowText(hwnd)
                if not title: return

                if any(x in title.lower() for x in ["splitbox", "sandman", "sbiectrl"]): return

                if pid in pids:
                    hwnds.append(hwnd)
                else:
                    p_name = psutil.Process(pid).name().lower()
                    if p_name in target_names:
                        hwnds.append(hwnd)
            except: pass

        win32gui.EnumWindows(cb, None)
        return sorted(list(set(hwnds)))

    @staticmethod
    def forcer_loop(manager):
        """Loop de foco em thread separada"""
        while True:
            if manager.forcer_active and manager.pids_to_paths_map:
                hwnds = WindowUtils.get_managed_hwnds(manager.pids, manager.pids_to_paths_map)
                for hwnd in hwnds:
                    try: manager.bridge.apply_forcer(hwnd)
                    except: pass
                time.sleep(0.8)
            else:
                time.sleep(2.0)
             
    @staticmethod
    def terminate_slots(processes, sbie_path):
        """Limpa processos ativos"""
        for proc in processes:
            try:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except: pass
        
        try:
            if os.path.exists(sbie_path):
                subprocess.run([sbie_path, "/box:DefaultBox", "/terminate"], capture_output=True)
        except: pass