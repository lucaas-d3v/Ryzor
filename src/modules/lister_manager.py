"""File responsible for managing the 'list' command"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from pprint import pprint

try:
    from .utils import Utils
    utils = Utils()

except (ModuleNotFoundError, ImportError):
    print("in lister_manager")
    print(f"[Debug] Error: utils module not found in Ryzor files, try `ryzor repair`")
    print("[Debug] Cancelling...")
        
    quit() 

if utils.validate_modules():
    from .definer import DefinitionManager
    from .logger import ConsoleManager

else:
    quit()

class Viewer:
    def __init__(self):
        self.definer = DefinitionManager()
        self.loger = ConsoleManager()

    def show_files(self, conteudo: list[Path], verbose: bool = False):
        for content in conteudo:
            tipo = "File" if content.is_file() else "Directory" if content.is_dir() else "Other"
            info = content.resolve() if verbose else content.name
            self.loger.log(f"{info} - Type: {tipo}")

    def list_files(self, caminho: Path, recursive_mode: bool = False, verbose: bool = False):
        if not caminho.exists():
            self.loger.log_error("Path does not exist")
            return
        
        if caminho.is_file():
            self.loger.log_error("[Ryzor] Path cannot be a file")
            return

        if recursive_mode:
            conteudo = list(caminho.rglob("*"))
        else:    
            conteudo = list(caminho.iterdir())

        self.show_files(conteudo, verbose)    

    def list_extensions(self):
        pprint(self.definer.ler_extensoes())