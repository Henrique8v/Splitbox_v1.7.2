#include "InputBridge.h"
#include <map>
#include <mutex>
#include <vector>

// Estrutura para armazenar o mapeamento de HWND para PlayerIndex
static std::map<HWND, int> g_PlayerMap;
static std::mutex g_MapMutex;

extern "C" {
    // 1. Define a identidade da janela (Chamado pelo Python)
    __declspec(dllexport) void SetPlayerIdentity(HWND hwnd, int playerIndex) {
        if (!hwnd || !IsWindow(hwnd)) return;

        std::lock_guard<std::mutex> lock(g_MapMutex);
        g_PlayerMap[hwnd] = playerIndex;
        
        // Notifica o console para debug
        printf("[MULTIPLAYER] Vinculado: HWND %p -> Player %d\n", hwnd, playerIndex + 1);
    }

    // 2. Retorna o ID do Player para o processo atual
    // Usado pelas DLLs de Input (xinput/dinput8) para saber quem elas são
    __declspec(dllexport) int GetCurrentPlayerID() {
        std::lock_guard<std::mutex> lock(g_MapMutex);
        
        // Tenta encontrar pelo HWND registrado na GlobalInputState
        if (g_InputState.myHwnd && g_PlayerMap.count(g_InputState.myHwnd)) {
            return g_PlayerMap[g_InputState.myHwnd];
        }
        
        // Se não achou, retorna o valor do bridge padrão como fallback
        return GetStoredPlayerIndex();
    }

    // 3. Limpa os registros (Útil ao fechar o Splitbox)
    __declspec(dllexport) void ClearPlayerIdentities() {
        std::lock_guard<std::mutex> lock(g_MapMutex);
        g_PlayerMap.clear();
    }
}