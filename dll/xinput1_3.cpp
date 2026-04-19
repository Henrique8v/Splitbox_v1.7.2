#include "InputBridge.h"
#include <xinput.h>

typedef DWORD (WINAPI *XInputGetState_t)(DWORD, XINPUT_STATE*);
XInputGetState_t pXInputGetState = NULL;

// Importamos a função da nossa nova DLL
typedef int (*GetCurrentPlayerID_t)();
static GetCurrentPlayerID_t pGetCurrentPlayerID = NULL;

void LoadMultiplayerProvider() {
    if (pGetCurrentPlayerID) return;
    HMODULE hMulti = GetModuleHandleA("multiplayer.dll");
    if (!hMulti) hMulti = LoadLibraryA("multiplayer.dll");
    if (hMulti) {
        pGetCurrentPlayerID = (GetCurrentPlayerID_t)GetProcAddress(hMulti, "GetCurrentPlayerID");
    }
}

void LoadRealXInput() {
    if (pXInputGetState) return;
    char path[MAX_PATH];
    GetSystemDirectoryA(path, MAX_PATH);
    strcat(path, "\\xinput1_3.dll");
    HMODULE h = LoadLibraryA(path);
    if (h) pXInputGetState = (XInputGetState_t)GetProcAddress(h, "XInputGetState");
}

extern "C" __declspec(dllexport) DWORD WINAPI XInputGetState(DWORD dwUserIndex, XINPUT_STATE* pState) {
    LoadRealXInput();
    LoadMultiplayerProvider();
    InstallFocusHook();

    int pIndex = -1;
    
    // Tenta pegar o ID da multiplayer.dll, se falhar, usa o bridge básico
    if (pGetCurrentPlayerID) {
        pIndex = pGetCurrentPlayerID();
    } else {
        pIndex = GetStoredPlayerIndex();
    }

    if (pIndex != -1) {
        // Se o jogo pede o "P1" (index 0), entregamos o estado do controle vinculado (pIndex)
        if (dwUserIndex == 0) {
            return pXInputGetState((DWORD)pIndex, pState);
        }
        // Para as outras requisições do jogo, dizemos que o controle está desconectado
        // Isso evita que o jogo "veja" os outros controles dos seus amigos
        return ERROR_DEVICE_NOT_CONNECTED;
    }

    // Comportamento padrão se não estiver em modo multiplayer
    if (pXInputGetState) return pXInputGetState(dwUserIndex, pState);
    return ERROR_DEVICE_NOT_CONNECTED;
}