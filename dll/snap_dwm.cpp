#include <windows.h>
#include <dwmapi.h>

// Garante que as funções exportadas usem o padrão C para evitar "name mangling" no Python
extern "C" {

    // Função para redimensionar e mover a janela (Stretching/Moving)
    __declspec(dllexport) void MoveAndStretch(HWND hwnd, int x, int y, int w, int h) {
        if (!hwnd || !IsWindow(hwnd)) return;
        
        // Aplica a posição e o tamanho ignorando a ordem Z para não roubar o foco
        SetWindowPos(hwnd, NULL, x, y, w, h, SWP_NOACTIVATE | SWP_NOZORDER | SWP_FRAMECHANGED);
    }

    // Função principal para habilitar o Snap Layout e Win + Setas
    __declspec(dllexport) void EnableSnapFeatures(HWND hwnd) {
        if (!hwnd || !IsWindow(hwnd)) return;

        // Recupera o estilo atual
        LONG style = GetWindowLong(hwnd, GWL_STYLE);

        // Adiciona estilos essenciais para o Snap do Windows:
        // WS_THICKFRAME: Permite redimensionar (necessário para Snap)
        // WS_MAXIMIZEBOX: Habilita o menu de Snap ao passar o mouse no botão maximizar
        // WS_CAPTION: Garante que o Windows trate como uma janela padrão de desktop
        style |= (WS_THICKFRAME | WS_CAPTION | WS_SYSMENU | WS_MAXIMIZEBOX | WS_MINIMIZEBOX);
        
        SetWindowLong(hwnd, GWL_STYLE, style);

        // Notifica o sistema que o frame da janela mudou para atualizar o Snap Assist
        SetWindowPos(hwnd, NULL, 0, 0, 0, 0, 
                     SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED);

        // Ativa o suporte a cantos arredondados e comportamentos de borda do Windows 11
        COLORREF color = RGB(0, 255, 65); // Verde Korvado para a borda (opcional)
        DwmSetWindowAttribute(hwnd, DWMWA_BORDER_COLOR, &color, sizeof(color));
    }
}