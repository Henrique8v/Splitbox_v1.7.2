# 🎮 Splitbox Pro 1.7.0

**Lorde Raveno ©2026** - Sistema profissional de split-screen com múltiplas estratégias de modo janela forçado.

O **Splitbox Pro** é uma ferramenta de elite para criar ambientes split-screen (1-4 jogadores) com isolamento de processos, injeção de DLLs customizadas e controle avançado de janelas.

---

## ✨ Funcionalidades Principais (v1.7.0)

### 🪟 Window Force (NOVO)
- ✅ **4 Estratégias:** Argumentos, DXWnd, WinAPI, Auto
- ✅ **UI Integrada:** Frame dedicado com controles
- ✅ **Workflow Automático:** Integrado no lançamento de jogos

### 🎮 Split-Screen
- ✅ **1-4 Jogadores:** Grade, Vertical, Horizontal
- ✅ **Detecção Automática:** Renomeação Player 1, 2, 3, 4
- ✅ **Sincronização:** Foco contínuo via forcer loop

### 🔌 Injeção de DLLs
- ✅ **Suporte DirectInput8, XInput, SDL2**
- ✅ **Controle de Mouse:** Lock/Unlock por janela
- ✅ **Controle de Áudio:** Mute por processo

### 🛡️ Isolamento de Processos
- ✅ **Sandboxie Plus:** Sandbox padrão incluído
- ✅ **DXWnd:** Modo janela forçado portátil
- ✅ **Detecção de Gamepads:** Mapeamento automático

---

## 📜 Motor Gráfico Web

* **Webkinter (Legado - 1.6.3):** Utiliza `tkinterweb` baseado no motor `tkhtml` de 1998. Leve, sem CSS3 moderno, ideal para interface limpa.

* **CustomTkinter:** Interface moderna padrão em todos os abas.

---

## 📋 Especificações Técnicas

| Item | Especificação |
|------|---------------|
| **SO** | Windows XP SP3 até 11 (x86 e x64) |
| **Python** | 3.13.0+ |
| **Interface** | CustomTkinter v5.2.2 |
| **Motor Gráfico** | DXWnd v2.06.13 (Portátil) |
| **Isolamento** | Sandboxie-Plus v1.17.2 |
| **Input Mapper** | Xpadder v2015 + Xoutput v3.31 |
| **Compilador** | MinGW g++ (x86/x64) |

---

## 🛠️ Infraestrutura de Compilação

### DLLs do Sistema (`modules/core/bin/`)
- `window_cleaner.dll` - Remove bordas/barra
- `window_forcer.dll` - Foco simultâneo
- `snap_dwm.dll` - Posicionamento
- `window_audio_ext.dll` - Controle de áudio

### DLLs de Injeção (`dll/core x86/` e `dll/core x64/`)
- `dinputhook.dll` - Hook de foco + mouse
- `dinput8.dll` - Wrapper DirectInput8
- `xinput1_3.dll` - Wrapper XInput
- `sdl2.dll` - Wrapper SDL2

**Compiladas com:** MinGW g++ (C++)

---

## 🚀 Instalação Rápida

### 1. Setup Automático
```batch
dependencias.bat