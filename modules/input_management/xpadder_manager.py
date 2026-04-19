import subprocess
import os
import sys
import shutil
import time
import psutil

class XpadderManager:
    BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    XPADDER_DIR = os.path.join(BASE_DIR, "input", "Xpadder v2015")
    XPADDER_EXE = os.path.join(XPADDER_DIR, "Xpadder.exe")

    @staticmethod
    def is_running():
        """Verifica se o Xpadder já está operando"""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == "Xpadder.exe":
                return True
        return False

    @staticmethod
    def start_mapping(player_count):
        if XpadderManager.is_running():
            print(" [XPADDER] Já está em execução. Pulando comando.")
            return

        if not os.path.exists(XpadderManager.XPADDER_EXE):
            print(f" [ERRO] Xpadder ausente: {XpadderManager.XPADDER_EXE}")
            return

        active_players = min(player_count, 4)

        for i in range(active_players):
            player_id = i + 1
            profile_name = f"p{player_id}.xpadderprofile"
            
            cmd = [XpadderManager.XPADDER_EXE, "/C", profile_name, "/M", str(player_id)]
            
            try:
                subprocess.Popen(cmd, cwd=XpadderManager.XPADDER_DIR)
                print(f" [XPADDER] Slot {player_id} carregado.")
                time.sleep(0.5)
                
            except Exception as e:
                print(f" [ERRO XPADDER] Player {player_id}: {e}")

    @staticmethod
    def close_all():
        try:
            os.system("taskkill /f /im Xpadder.exe >nul 2>&1")
            print(" [XPADDER] Processo encerrado.")
        except:
            pass