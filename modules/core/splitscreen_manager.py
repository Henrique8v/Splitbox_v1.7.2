import os
import time
import subprocess
import threading
import logging
from modules.core.launcher import GameLauncher as GL
from modules.core.dll_bridge import DLLBridge
from modules.core.injector_manager import CoreInjector
from modules.window_engine.layout_engine import LayoutEngine
from modules.window_engine.window_utils import WindowUtils
from modules.input_management.multiplayer_logic import MultiplayerLogic

logger = logging.getLogger(__name__)

class SplitscreenManager:
    def __init__(self):
        self.pids = []
        self.processes = []
        self.pids_to_paths_map = []   
        self.multi_logic = MultiplayerLogic()        
        self.bridge = DLLBridge()
        self.layout_engine = LayoutEngine(self.bridge)
        self.injector = CoreInjector() 
        self.forcer_active = True      
        threading.Thread(target=WindowUtils.forcer_loop, args=(self,), daemon=True).start()
        
                # 1. Inicializa a Ponte com as DLLs C++ (Foco e DWM)
        try:
            self.dll_bridge = DLLBridge()
            logger.info("[MANAGER] DLL_BRIDGE inicializado com sucesso")
            print("[SPLITBOX] ✓ DLLs do sistema carregadas")
        except Exception as e:
            logger.error(f"[MANAGER] Erro ao inicializar DLL_BRIDGE: {e}")
            print(f"[SPLITBOX] ✗ Erro ao carregar DLLs: {e}")
        
        # 2. Inicializa o Motor de Layout passando a ponte de comunicação
        try:
            self.layout_engine = LayoutEngine(self.dll_bridge)
            logger.info("[MANAGER] LayoutEngine inicializado")
            print("[SPLITBOX] ✓ LayoutEngine inicializado")
        except Exception as e:
            logger.error(f"[MANAGER] Erro ao inicializar LayoutEngine: {e}")
            print(f"[SPLITBOX] ✗ Erro ao inicializar LayoutEngine: {e}")

    def launch_game(self, exe_path, use_sandbox=False):
        """Foco: Injeção e Disparo"""
        if not exe_path or not os.path.exists(exe_path): 
            print(f"[ERRO] Executável não encontrado: {exe_path}")
            return None
        
        exe_dir = os.path.dirname(exe_path)
        exe_name = os.path.basename(exe_path)
        bat_path = os.path.join(exe_dir, "Windowed Mode.bat")
        
        # 1. Garante que o Batch existe
        if not os.path.exists(bat_path):
            try:
                from modules.window_engine.window_force import WindowForcer
                forcer = WindowForcer()
                forcer.create_windowed_batch(exe_path, exe_dir)
            except ImportError:
                print("[AVISO] WindowForcer não disponível.")

        # 2. Injeção de DLLs e Execução
        try:
            print(f"[SPLITBOX] Injetando suporte em: {exe_name}...")
            self.injector.injetar(exe_path)
            
            if use_sandbox:
                sbie_start = r"C:\Program Files\Sandboxie-Plus\Start.exe"
                if not os.path.exists(sbie_start): sbie_start = "Start.exe"
                print(f"[SPLITBOX] Executando em Sandboxie...")
                comando = f'"{sbie_start}" /box:DefaultBox "Windowed Mode.bat"'
                proc = subprocess.Popen(comando, shell=True, cwd=exe_dir, creationflags=0x08000000)
            else:
                print(f"[SPLITBOX] Executando via Window Force Batch...")
                proc = subprocess.Popen([bat_path], cwd=exe_dir, creationflags=0x08000000)
            
            # 3. Captura Dinâmica de PID
            time.sleep(3)
            game_pid = self._find_game_pid(exe_name, max_attempts=15)
            
            if game_pid:
                print(f"[SPLITBOX] ✓ Jogo detectado (PID: {game_pid})")
                self.pids.append(game_pid)
                # Note: pids_to_paths_map deve ser um dicionário {} e não lista [] no __init__
                self.pids_to_paths_map[game_pid] = exe_path
                self.injector.injetar(game_pid)
                return game_pid
            
        except Exception as e:
            print(f"[ERRO] Falha no lançamento: {e}")
            return None

        # Garante que o caminho está mapeado se não foi pego pelo PID
        if exe_path not in self.pids_to_paths_map:
             # Se pids_to_paths_map for lista, use .append(), se for dicionário use a chave
             if isinstance(self.pids_to_paths_map, list):
                 self.pids_to_paths_map.append(exe_path)       
                    
    def launch_game_with_dxw(self, exe_path, dxwnd_exe):
        """Modo DXWnd"""
        if not os.path.exists(dxwnd_exe): return
        
        game_dir = os.path.dirname(exe_path)
        for dll in ["xinput1_3.dll", "dinput8.dll"]:
            target = os.path.join(game_dir, dll)
            if os.path.exists(target):
                try: os.remove(target)
                except: pass

        if exe_path not in self.pids_to_paths_map:
            self.pids_to_paths_map.append(exe_path)

        dx_dir = os.path.dirname(dxwnd_exe)
        if GL.inject_dxwnd_ini(exe_path, dx_dir):
            proc = GL.start_process([dxwnd_exe, "/R:0"], dx_dir)
            if proc:
                self.processes.append(proc)
                self.pids.append(proc.pid)
                
    def _find_game_pid(self, exe_name, max_attempts=15):
        """Busca exaustiva do PID pelo nome do executável"""
        exe_name_lower = exe_name.lower()
        for attempt in range(max_attempts):
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if proc.info['name'].lower() == exe_name_lower:
                            return proc.info['pid']
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                time.sleep(0.8)
            except Exception as e:
                logger.debug(f"[FIND_PID] Erro na busca: {e}")
        return None   
        
    def register_pids(self, pids):
        """Registra PIDs externos e aplica o patch de foco simultâneo"""
        for pid in pids:
            if pid not in self.pids:
                self.pids.append(pid)
                # Garante que instâncias externas também recebam o patch de foco
                self.injector.injetar(pid)
    
    def force_multiplayer_input(self):
        """
        Coordena o isolamento de controles para todas as instâncias ativas.
        """
        # 1. Coleta os HWNDs das instâncias geridas pelos PIDs
        hwnds = WindowUtils.get_managed_hwnds(self.pids, self.pids_to_paths_map)
    
        if not hwnds:
            print(" [AVISO] Nenhuma janela ativa encontrada para isolamento.")
            return False

        # 2. Ordena para garantir que a ordem de abertura dite P1, P2, P3...
        hwnds.sort()
    
        print(f"\n[RC1] Iniciando isolamento de {len(hwnds)} controles...")
    
        for i, hwnd in enumerate(hwnds):
            # i = 0 (P1), 1 (P2), etc.
            success = self.multi_logic.bind_player_to_window(hwnd, i)
            if success:
                print(f" > Janela {hwnd} vinculada ao Slot de Controle {i+1}")
            
        print("[RC1] Processo de Multiplayer concluído na DLL.\n")
        return True

    def apply_layout(self, mode, clean_ui):
        """Repassa a ordem para a Engine"""
        hwnds = WindowUtils.get_managed_hwnds(self.pids, self.pids_to_paths_map)
        self.layout_engine.full_layout_workflow(hwnds, mode, clean_ui)

    def cleanup(self):
        """Limpa tudo: Sandboxie, DXWnd e Processos Nativos via Nome e PID"""
        print("\n[CLEANUP] Iniciando varredura de encerramento...")
        self.forcer_active = False
        
        sbie_path = r"C:\Program Files\Sandboxie-Plus\Start.exe"

        # 1. Mata via Objetos Popen (Sandboxie/DXWnd)
        from modules.window_engine.window_utils import WindowUtils
        WindowUtils.terminate_slots(self.processes, sbie_path)

        # 2. Mata via Nome do Executável (Resolve o problema da Janela Padrão)
        # Usamos o pids_to_paths_map para saber EXATAMENTE quais nomes de .exe fechar
        import subprocess
        target_names = set(os.path.basename(path).lower() for path in self.pids_to_paths_map)
        
        for exe_name in target_names:
            try:
                # O comando /IM mata pelo nome da imagem, /F força e /T mata processos filhos
                subprocess.call(['taskkill', '/F', '/T', '/IM', exe_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f" [CLEANUP] Processos '{exe_name}' encerrados.")
            except:
                pass

        # 3. Limpeza Residual via PID (Caso algo tenha sobrado)
        for pid in self.pids:
            try:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass

        # 4. Reset Total das Listas
        self.pids.clear()
        self.processes.clear()
        self.pids_to_paths_map.clear()
        
        # 5. Garantia de limpeza do Sandboxie (comando específico)
        try:
            subprocess.call([sbie_path, "/terminate_all"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
            
        time.sleep(1.0) # Aumentado para 1s para o Windows liberar os arquivos
        self.forcer_active = True
        print("[CLEANUP] Ambiente limpo e pronto.")