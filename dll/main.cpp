#include "InputBridge.h"

// Instanciação das variáveis globais
GlobalInputState g_InputState;
WNDPROC g_OriginalWndProc = NULL;

// Função para retornar o índice para as outras DLLs
extern "C" __declspec(dllexport) int GetStoredPlayerIndex() {
    std::lock_guard<std::mutex> lock(g_InputState.mtx);
    return g_InputState.playerIndex;
}

extern "C" BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            DisableThreadLibraryCalls(hinstDLL);
            break;

        case DLL_PROCESS_DETACH:
            // Restaura a janela se o jogo fechar
            if (g_InputState.isHooked && g_InputState.myHwnd && g_OriginalWndProc) {
                SetWindowLongPtr(g_InputState.myHwnd, GWLP_WNDPROC, (LONG_PTR)g_OriginalWndProc);
            }
            break;
    }
    return TRUE;
}