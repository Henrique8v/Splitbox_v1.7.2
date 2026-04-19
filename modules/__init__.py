"""
Splitbox Pro 1.7.0 - Módulo Principal
Organização: GUI | Core | Window Engine | Input Management | Patches
"""

__version__ = "1.7.0"
__author__ = "Lorde Raveno"

from modules.core.splitscreen_manager import SplitscreenManager
from modules.window_engine.align_manager import AlignManager
from modules.gui.gui_configs import load_settings, save_settings

__all__ = ['SplitscreenManager', 'AlignManager', 'load_settings', 'save_settings']