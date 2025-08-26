from pathlib import Path
import shutil as sh

def organizar(entrada: Path, saida: Path, backup: bool | None = False) -> bool:
    """ Função principal, papel: fazer backup/organizar os arquivos."""

    """Verifica se o diretório de entrada realmente existe."""
    if not entrada.exists():
        return False

    """Verifica se o diretório de entrada realmente é um diretório."""
    if not entrada.is_dir():
        return False

    """Verifica de o diretório de saída realmente existe."""
    if not saida.exists():

        """Cria caso não exista"""
        saida.mkdir(parents=True, exist_ok=True)

        """Caso, de alguma forma o diretorio de saída ainda n exista, retorna False."""
        if not saida.exists():
            return False

    """Verifica se o diretório de saída, realmente é um diretório."""
    if not saida.is_dir():
        return False
    
    def not_in_backup_folder(arquivo: Path) -> bool:
        """Verifica se a pasta é de backup"""
        return "backup" not in [p.lower() for p in arquivo.parts[:-1]]

    try:
        arquivos = [f for f in entrada.rglob("*") if f.is_file() and not_in_backup_folder(f)]

        for arquivo in arquivos:
            extensao = arquivo.suffix[1:] if arquivo.suffix else "#NoExtention"
            ex = extensao.upper()

            if ex != "#NoExtention":
                pasta_destino = Path(f"{saida}/{ex}")

            else:
                pasta_destino = Path(f"{saida}/Sem_Extensões")

            pasta_destino.mkdir(parents=True, exist_ok=True)

            destino = pasta_destino / arquivo.name

            if arquivo.resolve() == destino.resolve():
                continue

            if backup:
                sh.copy2(arquivo, destino)
            else:
                sh.move(arquivo, destino)

        return True
    
    except Exception as e:
        print(f"Erro: {e}")
        return False


"""Chamada clássica para teste"""
if __name__ == "__main__":
    if organizar(Path("tests/arquivos"), Path("tests/arquivos/")):
        print("organizado")

    else:
        print("Deu algum erro")    