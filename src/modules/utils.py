import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
import shutil as sh
from rich.console import Console

class Util:
    def __init__(self):
        super().__init__()
    
    def execute(self, mudancas: dict[str, str], callback=None, backup: bool = False, verbose: bool = False, overwrite: bool = False, erro: bool = False):
        """
        Executa copiar/mover arquivos de acordo com o dicionário mudancas.
        """
        try:
            total = len(mudancas)
            for i, (arquivo, destino) in enumerate(mudancas.items(), start=1):
                _arquivo = Path(arquivo)
                _destino = Path(destino)
                
                if _arquivo.resolve() == _destino.resolve():
                    continue
                
                if backup:
                    _destino.parent.mkdir(parents=True, exist_ok=True)
                    sh.copy2(_arquivo, _destino)
                else:
                    _destino.parent.mkdir(parents=True, exist_ok=True)
                    sh.move(_arquivo, _destino)
                
                if callback:
                    callback(
                        atual=i,
                        total=total,
                        nome_arquivo=_destino.name,
                        acao="Copiando" if backup else "Movendo"
                    )
            return True, None
        except Exception as e:
            return False, e
    
    @staticmethod
    def continuar(mensagem: str = "Deseja continuar? (s/n):", y: bool = False) -> bool:
        """
        Para evitar chamadas duplicadas, criei continuar() para perguntar ao usuário se quer confirmar a ação.
        """
        if y:
            return True
        
        console = Console()
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
            print(mensagem, end="")
            try:
                c = input().lower().strip()
                break
            except ValueError:
                inicio = "[FFC107 bold][Debug][/]"
                mensagem_erro = f"{inicio} [FF3B5C]{mensagem}[/]"
                console.print(mensagem_erro)
                continue
        
        return Util.busca_binaria(lista=aproveds, item=c)
    
    @staticmethod
    def busca_binaria(lista: list[str], item: str) -> bool:
        """Função de busca binária para encontrar um item em uma lista ordenada."""
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