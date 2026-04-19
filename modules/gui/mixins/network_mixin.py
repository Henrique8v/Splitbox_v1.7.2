import os
import json
import subprocess

class NetworkMixin:
    """Mixin para gestão de Virtual LAN e ZeroTier"""
    
    def load_network_id(self):
        if os.path.exists(self.net_config_path):
            try:
                with open(self.net_config_path, 'r') as f:
                    data = json.load(f)
                    saved_id = data.get("last_network_id", "")
                    if saved_id:
                        self.zt_id_entry.insert(0, saved_id)
                        print(f" [REDE] Network ID {saved_id} carregado.")
            except Exception as e:
                print(f" [ERRO] Falha ao carregar config de rede: {e}")

    def save_and_join(self):
        net_id = self.zt_id_entry.get().strip()
        if len(net_id) == 16:
            try:
                with open(self.net_config_path, 'w') as f:
                    json.dump({"last_network_id": net_id}, f)
            except Exception as e:
                print(f" [ERRO] Falha ao salvar config de rede: {e}")
            self.action_zt_join()
        else:
            self.zt_status_display.configure(text="ID Inválido (16 chars)", text_color="orange")

    def action_zt_join(self):
        net_id = self.zt_id_entry.get().strip()
        zt_path = r"C:\Program Files (x86)\ZeroTier\One\zerotier-cli.bat"
        if len(net_id) == 16:
            try:
                subprocess.run(f'"{zt_path}" join {net_id}', shell=True, check=True, creationflags=0x08000000)
                self.zt_status_display.configure(text=f"Join enviado: {net_id[-4:]}", text_color="yellow")
            except Exception:
                self.zt_status_display.configure(text="Erro: Caminho ZT inválido", text_color="red")

    def action_zt_status(self):
        zt_path = r"C:\Program Files (x86)\ZeroTier\One\zerotier-cli.bat"
        net_id = self.zt_id_entry.get().strip()
        try:
            output = subprocess.check_output(f'"{zt_path}" listnetworks', shell=True, text=True, creationflags=0x08000000)
            lines = output.splitlines()
            if len(lines) > 1:
                target_line = next((l for l in lines if net_id in l or "OK" in l), lines[1])
                data = target_line.split()
                status = data[5] if len(data) > 5 else "UNKNOWN"
                ip_full = next((item for item in reversed(data) if "/" in item), "-")
                if ip_full != "-":
                    ip = ip_full.split('/')[0]
                    self.zt_status_display.configure(text=f"Status: {status}\nIP: {ip}", text_color="#4CAF50")
                else:
                    self.zt_status_display.configure(text=f"Status: {status}\nSem IP (Autorize!)", text_color="cyan")
            else:
                self.zt_status_display.configure(text="Nenhuma rede ativa", text_color="white")
        except Exception:
            self.zt_status_display.configure(text="Erro ao ler CLI", text_color="red")