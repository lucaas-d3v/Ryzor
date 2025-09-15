"""Arquivo responsável por gerenciar o comando 'list' """

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from pprint import pprint

try:
    from .utils import Utils
    utils = Utils()

except (ModuleNotFoundError, ImportError):
    print("em lister_manager")
    print(f"[Debug] Erro: Módulo utils não encontrado nos arquivos do ryzor, tente `ryzor repair`")
    print("[Debug] Cancelando...")
        
    quit() 

if utils.validate_modules():
    from .definer import DefinitionManager

else:
    quit()

class Viewer:
    def __init__(self):
        self.definer = DefinitionManager()

    def show_files(self, conteudo: list[Path], verbose: bool = False):
        for content in conteudo:
            tipo = "Arquivo" if content.is_file() else "Diretório" if content.is_dir() else "Outro"
            info = content.resolve() if verbose else content.name
            print(f"[Ryzor] {info} - Tipo: {tipo}")

    def list_files(self, caminho: Path, recursive_mode: bool = False, verbose: bool = False):
        if not caminho.exists():
            print("[Ryzor] Caminho não existe")
            return
        
        if caminho.is_file():
            print("[Ryzor] O caminho não pode ser um arquivo")
            return

        if recursive_mode:
            conteudo = list(caminho.rglob("*"))

        else:    
            conteudo = list(caminho.iterdir())

        self.show_files(conteudo, verbose)    

    def list_extensions(self):
        pprint(self.definer.ler_extensoes())