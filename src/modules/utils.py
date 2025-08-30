
from pathlib import Path
import shutil as sh

def execute(mudancas: dict[str, str], callback=None, backup:bool = False, verbose:bool =False, overwrite: bool = False):
    """
    Executa copiar/mover arquivos de acordo com o dicionário mudancas.
    """
    from logger import log_error

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

        return True

    except Exception as e:
        log_error(f"Erro em execute: {e}")
        log_error("Cancelando...")

        return False
