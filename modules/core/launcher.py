import os
import subprocess

class GameLauncher:
    @staticmethod
    def inject_dxwnd_ini(exe_path, dxwnd_dir):
        """Lógica de injeção DXWnd"""
        ini_path = os.path.join(dxwnd_dir, "dxwnd.ini")
        template_path = os.path.join(os.getcwd(), "settings", "default.dxw")
        try:
            folder = os.path.dirname(exe_path).replace("/", "\\")
            full_path = exe_path.replace("/", "\\")
            title = os.path.splitext(os.path.basename(exe_path))[0]

            new_ini = [
                "[window]\n", "showhelp=NO\n", "expert=1\n",
                f"exepath={folder}\\\n", "posx=0\n", "posy=0\n",
                "[target]\n", f"title0={title}\n", f"path0={full_path}\n",
                "startfolder0=\n", f"launchpath0=\"{full_path}\"\n"
            ]

            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='latin-1') as f:
                    fixed = ["title0", "path0", "startfolder0", "launchpath0", "[window]", "[target]", "exepath"]
                    new_ini.extend([line for line in f if not any(line.lower().startswith(k) for k in fixed)])

            with open(ini_path, 'w', encoding='latin-1') as f:
                f.writelines(new_ini)
            return True
        except Exception as e:
            print(f"[ERRO INJECT]: {e}")
            return False

    @staticmethod
    def start_process(cmd, cwd):
        return subprocess.Popen(cmd, cwd=cwd, creationflags=0x08000000)