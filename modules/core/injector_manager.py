import os
import shutil
import struct

class CoreInjector:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dll_path = os.path.join(self.script_dir, "..", "..", "dll")
        
    def get_exe_arch(self, exe_path):
        """Detecta se o jogo é x86 ou x64"""
        try:
            with open(exe_path, 'rb') as f:
                f.seek(60)
                pe_offset = struct.unpack('<I', f.read(4))[0]
                f.seek(pe_offset + 4)
                machine = struct.unpack('<H', f.read(2))[0]
                return "x86" if machine == 332 else "x64"
        except:
            return "x64"

    def injetar(self, game_exe_path):
        """Injeta baseada na arquitetura"""
        if not game_exe_path: return
        
        game_dir = os.path.dirname(game_exe_path)
        arch = self.get_exe_arch(game_exe_path)
        
        dlls_config = [
            {"file": "dinputhook.dll", "folder": f"core {arch}"},
            {"file": "xinput1_3.dll", "folder": f"xinput1_3 {arch}"},
            {"file": "multiplayer.dll", "folder": f"multiplayer {arch}"},
            {"file": "dinput8.dll", "folder": f"dinput8 {arch}"},
            {"file": "sdl2.dll", "folder": f"sdl2 {arch}"}
        ]
        
        print(f"\n[SPLITBOX] Deploy de Elite ({arch})")
        
        for item in dlls_config:
            source = os.path.join(self.base_dll_path, item["folder"], item["file"])
            target = os.path.join(game_dir, item["file"])
            
            if os.path.exists(source):
                try:
                    shutil.copy2(source, target)
                    print(f"  [+] Injetado: {item['folder']} -> Sucesso.")
                except Exception as e:
                    print(f"  [X] Erro de acesso em {item['file']}: {e}")
            else:
                print(f"  [!] Pasta ou DLL ausente: {source}")

    def limpar(self, game_exe_path):
        """Remove os rastros após a jogatina"""
        game_dir = os.path.dirname(game_exe_path)
        for dll in ["xinput1_3.dll", "dinput8.dll"]:
            target = os.path.join(game_dir, dll)
            if os.path.exists(target):
                try:
                    os.remove(target)
                    print(f"  [-] Removido: {dll}")
                except:
                    pass