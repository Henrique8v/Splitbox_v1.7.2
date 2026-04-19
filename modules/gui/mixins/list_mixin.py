import customtkinter as ctk
import os

class ListManagerMixin:
    """Mixin especializado no gerenciamento da lista de executáveis e limpeza."""

    def update_listbox(self):
        """Atualiza visualmente a lista de checkboxes na interface."""
        if not hasattr(self, 'exe_listbox'): 
            return
            
        # Limpa widgets antigos para evitar duplicação
        for widget in self.exe_listbox.winfo_children():
            widget.destroy()
            
        self.exe_check_vars = []
        for exe in self.executables:
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                self.exe_listbox, 
                text=os.path.basename(exe), 
                variable=var
            )
            cb.pack(anchor="w", padx=5, pady=2)
            self.exe_check_vars.append({"path": exe, "var": var})

    def clear_all_executables(self):
        """Limpa toda a lista de executáveis da memória e da interface."""
        self.executables.clear()
        self.update_listbox()
        if hasattr(self, 'batch_info_label'):
            self.batch_info_label.configure(
                text="ℹ️ Lista limpa", 
                text_color="#9DB4C4"
            )

    def remove_executable(self):
        """Remove o último item adicionado à lista."""
        if self.executables:
            self.executables.pop()
            self.update_listbox()

    def cleanup(self):
        """Finaliza processos e limpa o motor do sistema ao fechar."""
        if hasattr(self, 'manager'):
            self.manager.cleanup()