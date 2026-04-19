import os
import ctypes
import sys

class MultiplayerLogic:
    def __init__(self):
        # 1. Caminhos Absolutos e Normalizados
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        bin_path = os.path.normpath(os.path.join(project_root, "modules", "core", "bin"))
        
        dll_multi = os.path.join(bin_path, "multiplayer.dll")
        dll_hook = os.path.join(bin_path, "dinputhook.dll")
        
        self.dll = None
        self._handler = None

        if not os.path.exists(dll_multi):
            print(f" [ERRO] Arquivo não encontrado: {dll_multi}")
            return

        try:
            # 2. Registrar o diretório para o Python 3.13
            if hasattr(os, 'add_dll_directory'):
                self._handler = os.add_dll_directory(bin_path)

            # 3. CARREGAMENTO EM CADEIA (O SEGREDO)
            # Primeiro carregamos a dependência que a multiplayer.dll precisa
            if os.path.exists(dll_hook):
                ctypes.WinDLL(dll_hook, winmode=0)
            
            # Agora carregamos a multiplayer.dll (ela já vai achar a dinputhook na memória)
            self.dll = ctypes.WinDLL(dll_multi, winmode=0)
            
            # 4. Configuração de Tipos
            self.dll.SetPlayerIdentity.argtypes = [ctypes.c_void_p, ctypes.c_int]
            self.dll.ClearPlayerIdentities.argtypes = []
            
            print(f" [DLL OK] Sistema Multiplayer 1.7.1 carregado (Python 3.13)")

        except Exception as e:
            print(f" [ERRO CRÍTICO] Falha na árvore de dependências: {e}")
            print(f" Verifique se ambas as DLLs em {bin_path} são x64.")

    def bind_player_to_window(self, hwnd, player_index):
        if self.dll and hwnd:
            try:
                self.dll.SetPlayerIdentity(ctypes.c_void_p(hwnd), player_index)
                return True
            except Exception as e:
                print(f" [ERRO] Falha no Bind: {e}")
        return False