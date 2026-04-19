#ifndef INPUT_BRIDGE_H
#define INPUT_BRIDGE_H

#include <windows.h>
#include <mutex>
#include <cstdio>

// Código de mensagem customizado para o Splitbox (Legacy/Patch)
#define WM_SET_GAMEPAD_IDENTITY (WM_USER + 777)

// Estrutura global compartilhada entre os hooks de cada instância
struct GlobalInputState {
    int playerIndex = -1;  // ID do Player (0=P1, 1=P2...)
    bool isHooked = false;
    HWND myHwnd = NULL;    // HWND capturado desta instância específica
    std::mutex mtx;        // Thread-safety para acesso simultâneo
};

// Declarações Externas para os módulos C++
extern GlobalInputState g_InputState;
extern WNDPROC g_OriginalWndProc;

// Protótipos das funções core exportadas pela multiplayer.dll
extern "C" {
    // Instaladores e Capturadores de Janela
    __declspec(dllexport) void InstallFocusHook();
	__declspec(dllexport) int GetStoredPlayerIndex();
    __declspec(dllexport) HWND GetCurrentInstanceHWND();

    // Gestão de Identidade (Usado pelo Python e DLLs de Input)
    __declspec(dllexport) void SetPlayerIdentity(HWND hwnd, int index);
    __declspec(dllexport) int GetPlayerIdentity(HWND hwnd);
    __declspec(dllexport) int GetCurrentPlayerID(); // Retorna o ID da instância atual
    __declspec(dllexport) void ClearPlayerIdentities();
}

// Tipos de função para carregamento dinâmico (facilita o uso de GetProcAddress)
typedef void (*SetPlayerIdentityFn)(HWND, int);
typedef int (*GetPlayerIdentityFn)(HWND);
typedef int (*GetCurrentPlayerIDFn)();

#endif