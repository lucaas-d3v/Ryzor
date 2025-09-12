import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
import shutil as sh
from rich.console import Console    

class Util:                    
    def __init__(self):
        super().__init__()

    def execute(self, mudancas: dict[str, str], callback=None, backup:bool = False, verbose:bool =False, overwrite: bool = False, erro: bool = False):
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


    def continuar(
                self,
                mensagem: str = "Deseja continuar? (s/n):",
                y: bool = False
            ) -> bool:
        
        """
        Para evitar chamadas duplicadas, criei continuar() para perguntar ao usuário se quer confirmar a ação.
        """

        if y:
            return True

        console = Console()

        aproveds = [
            # Português
            "sim", "s", "ss", "claro", "beleza", "ok", "vai", "simbora"

            # Inglês
            "yes", "y", "yeah", "yep", "ok", "sure", "yup",

            # Espanhol
            "sí", "si", "s", "claro", "vale", "ok",

            # Francês
            "oui", "ouais", "ok", "d’accord",

            # Alemão
            "ja", "j", "ok", "klar",

            # Italiano
            "sì", "si", "ok", "certo", "va bene",

            # Russo
            "да", "da", "ок", "конечно",

            # Japonês
            "はい", "hai", "うん", "ok",

            # Coreano
            "네", "예", "ㅇㅇ", "ok",

            # Árabe
            "نعم", "naʿam", "ايه", "ok",
        ]
        
        while True:
            print(mensagem, end="")
            
            try:
                c = input().lower().strip()
                break

            except ValueError:
                inicio = "[FFC107 bold][Debug][/]"

                mensagem = f"{inicio} [FF3B5C]{mensagem}[/]"

                console.print(mensagem)
                continue

        return self.busca_binaria(aproveds, c)

    def busca_binaria(lista: list[str], item: str):
        """Função de busca binária para encontrar um item em uma lista ordenada."""

        lista.sort()

        inicio = 0
        fim = len(lista) - 1

        while inicio < fim:
            meio = (fim + inicio) // 2    

            if lista[meio] == item:
                return True
            
            if lista[meio] > item:
                fim = meio - 1
                continue

            if lista[meio] < item:
                inicio = meio + 1
                continue

        return False
