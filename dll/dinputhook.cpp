#include "InputBridge.h"
#include <stdio.h>
#include <mutex>

// Definições de Identidade e Mouse
#define WM_SET_GAMEPAD_IDENTITY (WM_USER + 777)
#define WM_SET_MOUSE_STATE      (WM_USER + 888)

// Variável global para controlar se o mouse deve ser ignorado ou não
static bool g_FreeMouseMode = false;

// Estrutura para busca de janela via EnumWindows
struct EnumData { 
    DWORD pid; 
    HWND hwnd; 
};

// Função auxiliar para prender o mouse na janela atual
void LockCursorToWindow(HWND hwnd) {
    if (hwnd && !g_FreeMouseMode) {
        RECT rect;
        GetClientRect(hwnd, &rect);
        MapWindowPoints(hwnd, NULL, (LPPOINT)&rect, 2);
        ClipCursor(&rect); // Restringe o cursor fisicamente à área da janela
    } else {
        ClipCursor(NULL); // Libera o cursor
    }
}

// Callback estático para compatibilidade i686
static BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam) {
    EnumData* d = (EnumData*)lParam;
    DWORD pid;
    GetWindowThreadProcessId(hwnd, &pid);
    if (pid == d->pid && GetWindow(hwnd, GW_OWNER) == NULL && IsWindowVisible(hwnd)) {
        d->hwnd = hwnd;
        return FALSE;
    }
    return TRUE;
}

static LRESULT CALLBACK ForceFocusWndProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_ACTIVATE:
            // Se a janela for ativada e não estivermos em modo livre, prendemos o mouse
            if (LOWORD(wParam) != WA_INACTIVE) {
                LockCursorToWindow(hwnd);
            } else {
                ClipCursor(NULL);
            }
            return CallWindowProc(g_OriginalWndProc, hwnd, WM_ACTIVATE, WA_ACTIVE, lParam);
        
        case WM_NCACTIVATE:
            return CallWindowProc(g_OriginalWndProc, hwnd, WM_NCACTIVATE, TRUE, lParam);

        case WM_SET_MOUSE_STATE:
            g_FreeMouseMode = (wParam == 1);
            LockCursorToWindow(hwnd); // Atualiza o estado do cursor imediatamente
            return 0;

        case WM_SET_GAMEPAD_IDENTITY: {
            std::lock_guard<std::mutex> lock(g_InputState.mtx);
            g_InputState.playerIndex = (int)wParam;
            g_InputState.myHwnd = hwnd;

            char title[256];
            if (GetWindowTextA(hwnd, title, 256) && title[0] != '[') {
                char newTitle[300];
                sprintf(newTitle, "[P%d] %s", g_InputState.playerIndex + 1, title);
                SetWindowTextA(hwnd, newTitle);
            }
            return 0;
        }

        case WM_INPUT:
            // Se estiver em modo livre, bloqueamos para não girar a câmera na UI
            if (g_FreeMouseMode) return 0;
            // Se NÃO estiver em modo livre, deixamos passar (devolve o movimento)
            break;

        case WM_SETCURSOR:
            // Se o mouse estiver preso, deixamos o jogo gerenciar o cursor (evita cursor duplo)
            if (!g_FreeMouseMode) {
                return CallWindowProc(g_OriginalWndProc, hwnd, uMsg, wParam, lParam);
            }
            break;

        case WM_LBUTTONDOWN:
            // Garante que o mouse prenda ao clicar na janela (caso ele escape)
            if (!g_FreeMouseMode) LockCursorToWindow(hwnd);
            break;
    }
    return CallWindowProc(g_OriginalWndProc, hwnd, uMsg, wParam, lParam);
}

extern "C" __declspec(dllexport) void InstallFocusHook() {
    if (g_InputState.isHooked) return;
    
    HWND h = GetActiveWindow();
    if (!h) h = GetForegroundWindow();
    
    if (!h) {
        EnumData data = { GetCurrentProcessId(), NULL };
        EnumWindows(EnumWindowsProc, (LPARAM)&data);
        h = data.hwnd;
    }

    if (h) {
        g_OriginalWndProc = (WNDPROC)SetWindowLongPtr(h, GWLP_WNDPROC, (LONG_PTR)ForceFocusWndProc);
        g_InputState.isHooked = true;
        g_InputState.myHwnd = h;
    }
}