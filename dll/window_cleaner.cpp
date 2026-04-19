#include <windows.h>

extern "C" {
    __declspec(dllexport) void RemoveControlButtons(HWND hwnd) {
        if (!hwnd || !IsWindow(hwnd)) return;
        LONG style = GetWindowLong(hwnd, GWL_STYLE);
        
        // Remove bordas, barra de título e botões de sistema
        style &= ~WS_MAXIMIZEBOX;
        style &= ~WS_MINIMIZEBOX;
        style &= ~WS_SYSMENU;
        style &= ~WS_CAPTION; 

        SetWindowLong(hwnd, GWL_STYLE, style);
        // SWP_FRAMECHANGED força o Windows a redesenhar a janela sem os controles
        SetWindowPos(hwnd, NULL, 0, 0, 0, 0, 
                     SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED);
    }

    __declspec(dllexport) void RestoreControlButtons(HWND hwnd) {
        if (!hwnd || !IsWindow(hwnd)) return;
        LONG style = GetWindowLong(hwnd, GWL_STYLE);
        style |= (WS_CAPTION | WS_SYSMENU | WS_MAXIMIZEBOX | WS_MINIMIZEBOX);

        SetWindowLong(hwnd, GWL_STYLE, style);
        SetWindowPos(hwnd, NULL, 0, 0, 0, 0, 
                     SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED);
    }
}