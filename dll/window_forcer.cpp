#include <windows.h>

// Força a janela para o modo "Janela com Bordas" (Padrão)
extern "C" __declspec(dllexport) void ApplyForceWindowed(HWND hwnd) {
    if (!hwnd || !IsWindow(hwnd)) return;
    LONG style = GetWindowLong(hwnd, GWL_STYLE);
    style &= ~(WS_POPUP | WS_MAXIMIZE);
    style |= (WS_OVERLAPPEDWINDOW | WS_VISIBLE);
    SetWindowLong(hwnd, GWL_STYLE, style);
    SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, 
                 SWP_NOMOVE | SWP_NOSIZE | SWP_FRAMECHANGED | SWP_NOZORDER | SWP_NOACTIVATE);
}

// Nova funcionalidade: Força a janela a pensar que está sempre ativa visualmente
extern "C" __declspec(dllexport) void ForceActivate(HWND hwnd) {
    if (!hwnd || !IsWindow(hwnd)) return;
    SendMessage(hwnd, WM_NCACTIVATE, TRUE, 0);
    SendMessage(hwnd, WM_ACTIVATE, WA_ACTIVE, 0);
}