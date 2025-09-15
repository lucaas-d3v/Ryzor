"""Utils Module for Ryzor"""

from __future__ import annotations
import importlib.util
import os
from pathlib import Path
import shutil as sh
import json
from typing import Optional

# pasta onde este módulo vive (src/modules)
MODULE_DIR = Path(__file__).resolve().parent

# tenta importar rich, mas não quebra se não existir
console = None
try:
    from rich.console import Console
    console = Console()
except Exception:
    console = None


def show_module_missing(module_name: Optional[str] = None, modules_names: Optional[list[str]] = None) -> None:
    """
    Imprime mensagem de módulo(s) faltando.
    """
    if modules_names:
        for module in modules_names:
            print(f"[Debug] Erro: Módulo {module} não encontrado nos arquivos do ryzor...")

        print("[Debug] Tente `ryzor repair`")
        print("[Debug] Cancelando...")
        return

    if module_name:
        print(f"[Debug] Erro: Módulo {module_name} não encontrado nos arquivos do ryzor, tente `ryzor repair`")
        print("[Debug] Cancelando...")
    return


def _validate_modules() -> bool:
    """
    Verifica dependências externas e existência dos módulos internos sem importá-los,
    evitando import circular.
    """
    missing_modules: list[str] = []

    # checa pacote externo
    if importlib.util.find_spec("send2trash") is None:
        missing_modules.append("send2trash")
        
    # checa arquivos internos em src/modules (evita importar-os)
    expected_internal = ["definer.py", "file_manager.py", "logger.py", "utils.py"]
    for f in expected_internal:
        if not (MODULE_DIR / f).exists():
            missing_modules.append(f.replace(".py", ""))

    if not missing_modules:
        return True

    show_module_missing(modules_names=missing_modules)
    return False


class Utils:
    def __init__(self) -> None:
        super().__init__()

    def execute_changes(
        self,
        mudancas: dict[str, str],
        callback=None,
        backup: bool = False,
        verbose: bool = False,
        overwrite: bool = False,
        erro: bool = False,
    ):
        """
        Executa copiar/mover arquivos de acordo com o dicionário mudancas.
        Retorna (True, None) em sucesso ou (False, Exception) em falha.
        """
        try:
            total = len(mudancas)
            for i, (arquivo, destino) in enumerate(mudancas.items(), start=1):
                _arquivo = Path(arquivo)
                _destino = Path(destino)

                if _arquivo.resolve() == _destino.resolve():
                    continue

                _destino.parent.mkdir(parents=True, exist_ok=True)

                if backup:
                    sh.copy2(_arquivo, _destino)
                else:
                    # se overwrite == True, remove destino antes de mover
                    if overwrite and _destino.exists():
                        if _destino.is_dir():
                            sh.rmtree(_destino)
                        else:
                            _destino.unlink()
                    sh.move(_arquivo, _destino)

                if callback:
                    callback(
                        atual=i,
                        total=total,
                        nome_arquivo=_destino.name,
                        acao="Copiando" if backup else "Movendo",
                    )
            return True, None
        except Exception as e:
            return False, e

    @staticmethod
    def continue_action(mensagem: str = "Deseja continuar? (s/n):", y: bool = False) -> bool:
        """
        Pergunta ao usuário se quer continuar. Se y=True, retorna True imediatamente.
        Usa busca binária no conjunto de respostas aprovadas.
        """
        if y:
            return True

        aproveds = [
            # Português
            "sim", "s", "ss", "claro", "beleza", "ok", "vai", "simbora",
            # Inglês
            "yes", "y", "yeah", "yep", "sure", "yup",
            # Espanhol
            "sí", "si", "claro", "vale",
            # Francês
            "oui", "ouais", "d'accord",
            # Alemão
            "ja", "j", "klar",
            # Italiano
            "sì", "certo", "va bene",
            # Russo
            "да", "da", "ок", "конечно",
            # Japonês
            "はい", "hai", "うん",
            # Coreano
            "네", "예", "ㅇㅇ",
            # Árabe
            "نعم", "naʿam", "ايه",
        ]

        while True:
            try:
                # usa input com prompt direto (compatível com scripts)
                c = input(mensagem).lower().strip()
            except (KeyboardInterrupt, EOFError):
                # usuário cancelou via Ctrl+C/Ctrl+D
                return False

            if c == "":
                # repete a pergunta se vazio
                continue

            return Utils.busca_binaria(aproveds, c)

    @staticmethod
    def busca_binaria(lista: list[str], item: str) -> bool:
        """
        Busca binária simples numa cópia ordenada da lista.
        """
        lista_ordenada = sorted(lista)
        inicio = 0
        fim = len(lista_ordenada) - 1

        while inicio <= fim:
            meio = (fim + inicio) // 2
            if lista_ordenada[meio] == item:
                return True
            elif lista_ordenada[meio] > item:
                fim = meio - 1
            else:
                inicio = meio + 1

        return False

    @staticmethod
    def validate_modules():
        return _validate_modules()