import time
from modules.input_management.input_patch import InputPatch
from modules.input_management.xpadder_manager import XpadderManager
from modules.input_management.multiplayer_logic import MultiplayerLogic

class IdentityManager:
    @staticmethod
    def apply_identity(hwnds, bridge=None):
        patcher = InputPatch()
        # Inicializa a lógica da nova DLL
        multi_logic = MultiplayerLogic()
        
        # Inicia perfis do Xpadder baseado no número de janelas
        XpadderManager.start_mapping(len(hwnds))
        
        print(f"\n[IDENTITY] Iniciando atribuição dupla (Mensagem + Registro DLL)")
        
        for i, hwnd in enumerate(hwnds):
            try:
                # 1. MÉTODO TRADICIONAL (Via PostMessage/Hook de Mensagem)
                # Garante compatibilidade com o sistema de mensagens do dinputhook.cpp
                success_msg = patcher.assign_controller(hwnd, i)
                
                # 2. MÉTODO MULTIPLAYER (Registro Direto na Memória da DLL)
                # Garante que XInput e DInput saibam exatamente qual slot usar
                success_dll = multi_logic.bind_player_to_window(hwnd, i)
                
                if success_msg or success_dll:
                    print(f" [IDENTITY] Player {i+1} vinculado com sucesso -> Janela {hwnd}")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f" [ERRO] Falha crítica ao sinalizar identidade para Player {i+1}: {e}")
        
        print("[IDENTITY] Processo de vinculação P1-P4 concluído.\n")