Implementação de WebView no Tkinter (Splitbox Alpha)
Este guia documenta o processo de integração de uma interface rica em HTML dentro de uma aplicação baseada em CustomTkinter.

1. Bibliotecas e Dependências
Para que o motor de renderização funcionasse, utilizamos a biblioteca tkinterweb, que permite embutir conteúdo web em janelas Tkinter.

Instalação:

Bash

python -m pip install tkinterweb

Principais Módulos Utilizados:

  - .tkinterweb.HtmlFrame: Widget de renderização.
  - .customtkinter: Container da interface.
  - .pathlib: Manipulação robusta de caminhos no Windows.

2. Estrutura de Arquivos e Lógica de Caminhos
Criamos o script tutorial_data.py para garantir que o sistema localize o arquivo HTML independentemente de onde o executável seja rodado.

tutorial_data.py

Python
import os
from pathlib import Path

def get_tutorial_path():
    # Localiza o arquivo tutorial.html no diretório do script
    file_path = Path(__file__).parent / "tutorial.html"
    
    # Converte o caminho para o formato URI (file:///...)
    return file_path.as_uri()
	
3. Implementação da Aba Help (Injeção de Código)
Para evitar o erro "Oops! The page could not be found" (comum em protocolos file:/// no Windows), optamos pela técnica de Injeção Direta de HTML. Em vez de carregar a URL, o Python lê o conteúdo do arquivo e o injeta no motor.

Trecho do splitscreen_gui.py:

Python
def show_help(self):
    self.clear_main_content()
    
    # Criar o container para o HTML dentro do CustomTkinter
    html_container = ctk.CTkFrame(self.main_content, corner_radius=10)
    html_container.pack(expand=True, fill="both", padx=5, pady=5)

    # Iniciar o motor de renderização
    self.browser = HtmlFrame(html_container, messages_enabled=False)
    self.browser.pack(expand=True, fill="both")

    try:
        # Obter o caminho físico do arquivo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "tutorial.html")
        
        # Ler o arquivo HTML como texto (UTF-8)
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                conteudo_html = f.read()
            
            # Carregar o código diretamente no widget (Estabiliza a renderização)
            self.browser.load_html(conteudo_html)
            print("[SISTEMA] Tutorial renderizado via Injeção Direta.")
    except Exception as e:
        self.browser.load_html(f"<h2 style='color:red;'>Erro: {e}</h2>")
		
4. Estilização do Tutorial (CSS)
O arquivo tutorial.html foi estilizado para seguir o padrão visual verde e preto do repositório, garantindo uma estética cibernética.

tutorial.html (Exemplo de Estilo):

HTML
<style>
    body {
        background-color: #0d0d0d; /* Fundo cinza escuro */
        color: #00ff41;           /* Verde clássico/positivo */
        font-family: 'Segoe UI';
        padding: 20px;
    }
    pre {
        background: #1a1a1a;
        border-left: 5px solid #00ff41;
        padding: 15px;
    }
</style>
Benefícios desta Abordagem:
Estabilidade: Elimina recarregamentos acidentais e erros de protocolo local.

Performance: O conteúdo é carregado instantaneamente da memória.

Design: Permite o uso de tabelas, listas e emojis (🎮) que seriam difíceis de alinhar em labels padrão do Tkinter.

Codigo usado:

###___________________turorial_data.py:
import os
from pathlib import Path

def get_tutorial_path():
    # Obtém o caminho absoluto do arquivo tutorial.html na pasta atual
    file_path = Path(__file__).parent / "tutorial.html"
    
    # .as_uri() converte automaticamente para o formato file:///C:/... 
    # que os navegadores e o tkinterweb entendem melhor
    return file_path.as_uri()

###___________________splitscreen_gui.py
from tkinterweb import HtmlFrame # Motor para o tutorial rico em HTML

#### Importação do conteúdo externo e funções de caminho:

#   CABEÇALHO
try:
    from tutorial_data import get_tutorial_path
except ImportError:
    def get_tutorial_path(): return ""

#	SPLITBOX_GUI
class SPLITBOX_GUI(ctk.CTk):

    def show_help(self):
        self.clear_main_content()
        
        # Container principal
        html_container = ctk.CTkFrame(self.main_content, corner_radius=10)
        html_container.pack(expand=True, fill="both", padx=5, pady=5)

        # Iniciar o motor
        self.browser = HtmlFrame(html_container, messages_enabled=False)
        self.browser.pack(expand=True, fill="both")
    
        try:
            # Em vez de carregar a URL, vamos carregar o CONTEÚDO do arquivo
            # Isso evita que o tkinterweb tente fazer requisições de rede ou disco após abrir
            current_dir = os.path.dirname(os.path.abspath(__file__))
            html_path = os.path.join(current_dir, "tutorial.html")
            
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    conteudo_html = f.read()
                
                # Injeta o HTML diretamente no motor
                self.browser.load_html(conteudo_html)
                print("[SISTEMA] Tutorial renderizado via Injeção Direta.")
            else:
                self.browser.load_html("<h2 style='color:red;'>Erro: tutorial.html não encontrado na raiz.</h2>")
                
        except Exception as e:
            print(f"[ERRO] Falha ao carregar Help: {e}")
            self.browser.load_html(f"<h2>Erro crítico</h2><p>{e}</p>")