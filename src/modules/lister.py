"""Arquivo responsável por gerenciar o comando 'list' """

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from .definer import Definer
from pprint import pprint


class Lister:
    def __init__(self):
        self.definer = Definer()

    def mostrar(self, conteudo: list[Path], verbose: bool = False):
        for content in conteudo:
            tipo = "Arquivo" if content.is_file() else "Diretório" if content.is_dir() else "Outro"
            info = content.resolve() if verbose else content.name
            print(f"[Ryzor] {info} - Tipo: {tipo}")

    def lister(self, caminho: Path, recursive_mode: bool = False, verbose: bool = False):
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

        self.mostrar(conteudo, verbose)    

    def lister_extensionsself(self):
        pprint(self.definer.ler_extensoes())