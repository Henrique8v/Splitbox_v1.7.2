#include "InputBridge.h"

typedef void* (*SDL_JoystickOpen_t)(int);
SDL_JoystickOpen_t pSDL_JoystickOpen = NULL;

void LoadRealSDL2() {
    if (pSDL_JoystickOpen) return;
    HMODULE h = LoadLibraryA("sdl2_real.dll"); 
    if (!h) h = LoadLibraryA("SDL2.dll");
    if (h) pSDL_JoystickOpen = (SDL_JoystickOpen_t)GetProcAddress(h, "SDL_JoystickOpen");
}

extern "C" {
    __declspec(dllexport) void* SDL_JoystickOpen(int device_index) {
        LoadRealSDL2();
        InstallFocusHook(); // Alterado de InstallUniversalHook para InstallFocusHook

        int pIndex = GetStoredPlayerIndex();
        if (pIndex != -1 && device_index != pIndex) {
            return NULL; 
        }

        if (pSDL_JoystickOpen) return pSDL_JoystickOpen(device_index);
        return NULL;
    }
}