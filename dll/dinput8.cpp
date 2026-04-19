#include "InputBridge.h"
#include <unknwn.h>
#include <cstdio>

// Tipos para as funções originais e ponte da DLL
typedef HRESULT (WINAPI *DirectInput8Create_t)(HINSTANCE, DWORD, REFIID, LPVOID*, LPUNKNOWN);
static DirectInput8Create_t pDirectInput8Create = NULL;

// Funções de ponte para a multiplayer.dll
typedef int (*GetCurrentPlayerID_t)();
typedef int (*GetPlayerIdentityFn)(HWND);

static GetPlayerIdentityFn GetPlayerID = nullptr;
static GetCurrentPlayerID_t GetID = nullptr;

void LoadRealDInput8() {
    if (pDirectInput8Create) return;
    char path[MAX_PATH];
    GetSystemDirectoryA(path, MAX_PATH);
    strcat(path, "\\dinput8.dll");
    HMODULE h = LoadLibraryA(path);
    if (h) pDirectInput8Create = (DirectInput8Create_t)GetProcAddress(h, "DirectInput8Create");
}

// Helper para carregar as funções da multiplayer.dll uma única vez
void EnsureMultiplayerBridge() {
    HMODULE hMulti = GetModuleHandleA("multiplayer.dll");
    if (hMulti) {
        if (!GetID) GetID = (GetCurrentPlayerID_t)GetProcAddress(hMulti, "GetCurrentPlayerID");
        if (!GetPlayerID) GetPlayerID = (GetPlayerIdentityFn)GetProcAddress(hMulti, "GetPlayerIdentity");
    }
}

extern "C" __declspec(dllexport) HRESULT WINAPI DirectInput8Create(
    HINSTANCE hinst, 
    DWORD dwVersion, 
    REFIID riidltf, 
    LPVOID* ppvOut, 
    LPUNKNOWN punkOuter
) {
    LoadRealDInput8();
    EnsureMultiplayerBridge();

    // 1. Garante que o FocusHook capture o HWND atual para a DLL
    InstallFocusHook(); 

    // 2. Identificação de Instância para Log e Filtro
    int myPlayerIndex = -1;
    if (GetID) {
        myPlayerIndex = GetID();
        if (myPlayerIndex != -1) {
            printf("[DINPUT8] Vinculado ao Slot de Controle: %d\n", myPlayerIndex + 1);
        }
    }

    // 3. Chamada original
    if (pDirectInput8Create) {
        HRESULT hr = pDirectInput8Create(hinst, dwVersion, riidltf, ppvOut, punkOuter);
        
        if (SUCCEEDED(hr)) {
            // AQUI: No RC2, o wrapper de interface (se implementado) 
            // usaria 'myPlayerIndex' para filtrar o Poll().
            printf("[RC2] DirectInput8 Interface criada com sucesso.\n");
        }
        return hr;
    }

    return E_FAIL;
}

// Função de utilidade para o Poll() interceptado (Wrapper)
// Deve ser chamada dentro do método Poll do seu dispositivo hookado
bool ShouldProcessInput(HWND hWindow) {
    if (GetPlayerID) {
        int assignedID = GetPlayerID(hWindow);
        // Se a janela atual tem um ID atribuído pelo Splitbox Manager
        // nós validamos se o dispositivo que está chamando pertence a este ID.
        if (assignedID != -1) {
            return true; // No RC2 completo, comparamos com o ID do Hardware
        }
    }
    return true; 
}