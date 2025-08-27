"""Arquivo principal do Ryzor"""

from pathlib import Path
import shutil as sh
import json
from os import name, system

def realocate_files(entrada: Path, saida: Path, backup: bool = False, no_preview: bool = False, verbose: bool = False) -> bool:
    """ Função principal, papel: fazer backup/organizar os arquivo
    Função principal do Ryzor

    args:
        entrada: caminho de entrada dos arquivos a serem organizados/backup.
        saida: caminho de saída onde os arquivos seram levados ao fim do processo.
        backup: informa será feito o backup pu apenas organização.
        preview: informa se o usuário quer o preview de tudo antes da ação.
        verbose: informa será o usuário quer ssber literalmente tudo, caminhos completos e demais.

    returns:
        retorna False caso o caminho seja um caminho ou n exista, etc, ou True caso tudo ocorra como esperado.
    """

    if not entrada.exists():
        """
        Medida de segurança caso o diretório informado não exista.
        """

        return False

    if not entrada.is_dir():
        """
        Medida de segurança caso o caminho especificado não seja um diretório.
        """

        return False

    if not saida.exists():
        """
        Medida de segurança caso a saida não exista.
        """

        saida.mkdir(parents=True, exist_ok=True)

    if not saida.is_dir():
        """
        Medida de segurança, caso a saida não seja um diretório.
        """

        return False

    def continuar() -> bool:
        """
        Para evitar chamadas duplicadas, criei continuar() para perguntar ao usuário se quer confirmar a ação.
        """

        aproveds = ["s", "yes", "sim", "ok"]
        c = input("Deseja continuar? (s/n): ").lower().trim()

        return c in aproveds

    def execute(mudancas: dict[str, str]):
        """
        Criei execute() para evitar repetição de código.

        args:
            mudancas: um dicionário com chave str, e valor str,
                      basicamente, o caminho onde o arquivo está, é onde ele deve ser levado.

        returns:
            retorna True caso as mudanças ocoram como esperadas.
        """

        try:
            if backup:

                for arquivo, destino in mudancas.items():
                    _arquivo = Path(arquivo)
                    _destino = Path(destino) / _arquivo.name

                    if _arquivo.resolve() == _destino.resolve():
                        continue

                    if verbose:
                        print(f"[Ryzor] Copiando {_arquivo} -> {_destino}")

                    else:
                        print(f"[Ryzor] Copiando {sep.join(_arquivo.parts[-2:])} -> {sep.join(_destino.parts[-2:])}")


                    sh.copy2(arquivo, destino)

                else:
                    return True

            else:
                for arquivo, destino in mudancas:
                    _arquivo = Path(arquivo)
                    _destino = Path(destino) / _arquivo.name

                    if _arquivo.resolve() == _destino.resolve():
                        continue

                    if verbose:
                        print(f"[Ryzor] Movendo {_arquivo} -> {_destino}")

                    else:
                        print(f"[Ryzor] Movendo {sep.join(_arquivo.parts[-2:])} -> {sep.join(_destino.parts[-2:])}")

                    sh.move(arquivo, destino)

                else:
                    return True

        except Exception as e:
            print("[Ryzor] Erro:", e)
            return False


    def not_in_backup_folder(arquivo: Path) -> bool:
        """
        Criei not_in_backup_folder(), para verificar se a pasta é de backup,
        assim, evitando fazer backup, de uma pasta de bakcup
        """

        return "backup" not in [p.lower() for p in arquivo.parts[:-1]]

    sep = '/' if name != 'nt' else '\\'

    try:
        system("cls" if name == "nt" else "clear")

        arquivos = [f for f in entrada.rglob("*") if f.is_file() and not_in_backup_folder(f)]
        arquivos_a_mudar = {}

        try:
            base_dir = Path(__file__).parent
            json_path = base_dir / "extensions.json"

            with json_path.open("r", encoding="utf-8-sig") as f:
                tipos_de_arquivos = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[Ryzor] Erro ao carregar JSON: {e}")
            return False

        if not isinstance(tipos_de_arquivos, dict):
            print("[Ryzor] JSON não é um dicionário válido")
            return False

        if not verbose:
            print(
                f"""\t\t\t\tComeçando em {entrada} ...
                \t\tModo: {'Backup' if backup else 'Organização'}\n
        Atual {'-' * 17} Pós-mudanças\n""")

        else:
            print(
                f"""Começando em {entrada} ...
                Modo: {'Backup' if backup else 'Organização'}
                Verbose: On
                Total de modificaçoes: {len(arquivos) + 1}
                \t    Atual {'-' * 17} Pós-mudanças\n""")

        for arquivo in arquivos:
            pasta_destino = Path(saida / arquivo.suffix[1:])

            for tipo, extensoes in tipos_de_arquivos.items():
                if any(arquivo.suffix.lower().endswith(ext) for ext in extensoes):
                    pasta_destino = Path(saida / tipo)
                    break

            else:
                pasta_destino = Path(f"{saida}/Sem_Extensões")

            pasta_destino.mkdir(parents=True, exist_ok=True)
            destino = pasta_destino / arquivo.name

            if backup:
                if not not_preview:
                    if verbose:
                        print(f"[Ryzor] {arquivo} -> {destino}")
                    else:
                        print(f"[Ryzor] {sep.join(arquivo.parts[-2:])} -> {sep.join(destino.parts[-2:])}")

                arquivos_a_mudar[str(arquivo)] = str(destino)

            else:
                if not not_preview:
                    if verbose:
                        print(f"[Ryzor] {arquivo} -> {destino}")
                    else:
                        print(f"[Ryzor] {sep.join(arquivo.parts[-2:])} -> {sep.join(destino.parts[-2:])}")


                arquivos_a_mudar[str(arquivo)] = str(destino)

        else:
            if continuar():
                return execute(arquivos_a_mudar)


        print("[Ryzor] Cancelando...")
        return False

    except Exception as e:
        print(f"Erro: {e}")
        return False