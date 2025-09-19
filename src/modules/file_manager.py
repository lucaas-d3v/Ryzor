"""Arquivo principal de gerenciamento de arquivos do Ryzor"""

import os
from pathlib import Path
import shutil as sh
import json

# caminho da pasta do próprio módulo (src/modules)
MODULE_DIR = Path(__file__).resolve().parent

try:
    from .utils import Utils
    utils = Utils()

except (ModuleNotFoundError, ImportError):
    print(f"[Debug] Error: Utils module not found in ryzor files, try `ryzor repair`")
    print("[Debug] Canceling...")
    quit()

# valida se os módulos estão ok
if utils.validate_modules():
    from .logger import ConsoleManager
    from .definer import DefinitionManager
else:
    quit()

logger = ConsoleManager()

class FileController:
    def __init__(self):
        self.sep = os.sep  # pega separador do sistema
        self.definer = DefinitionManager()
        self.logger = ConsoleManager

    def rename(self, file: Path, qtd: list[int] = [0]) -> Path:
        stem = file.stem            # nome do arquivo sem extensão
        extensao = "".join(file.suffixes)  # todas as extensões juntas (ex: ".tar.gz")

        ultimo = max(qtd)
        new_name = f"{stem} ({ultimo + 1}){extensao}"

        return file.with_name(new_name)

    def relocate_files(self, 
            entrada: Path, 
            saida: Path,
            backup: bool = False,
            no_preview: bool = False,
            verbose: bool = False,
            y: bool = False
        ) -> bool | None:
        
        """ 
        Função principal, papel: fazer backup/organizar os arquivo

        args:
            entrada: caminho de entrada dos arquivos a serem organizados/backup.
            saida: caminho de saída onde os arquivos seram levados ao fim do processo.
            backup: informa será feito o backup pu apenas organização.
            no_preview: informa se o usuário quer desativar o preview de tudo antes da ação.
            verbose: informa será o usuário quer ssber literalmente tudo, caminhos completos e demais.
            y: pré-responde sim para a ação escolhida.
            
        returns:
            retorna False caso o caminho seja um caminho ou n exista, etc, ou True caso tudo ocorra como esperado.
        """

        if not entrada.exists():
            """
            Medida de segurança caso o diretório informado não exista.
            """
            self.logger.log_error("The input path does not exist.")
            self.logger.log_error("Canceling")

            return False

        if not entrada.is_dir():
            """
            Medida de segurança caso o caminho especificado não seja um diretório.
            """
            self.logger.log_error("The specified path cannot be a file.")

            return False

        if not saida.exists():
            """
            Medida de segurança caso a saida não exista.
            """

            self.logger.log("The output path does not exist.", code=9, debug=True)
            self.logger.log("Trying to create...", debug=True, code=10)
            
            try:
                saida.mkdir(parents=True, exist_ok=True)
                self.logger.log("Output path created successfully.", code=11)
                self.logger.log("Continuing...", code=11)

            except PermissionError:
                print(saida)
                self.logger.log_error(f"Ryzor does not have permission to act on {saida}")
                return False
            
        if not saida.is_dir():
            """
            Medida de segurança, caso a saida não seja um diretório.
            """        
            self.self.logger.log_error("The specified path cannot be a file.")

            return False

        def not_in_backup_folder(arquivo: Path) -> bool:
            return "backup" not in [p.lower() for p in arquivo.parts[:-1]]
        
        def buscar_arquivos_generator():
            """Generator que faz a busca real dos arquivos"""
            
            contador = 0

            for arquivo in entrada.rglob("*"):
                if arquivo.is_file() and not_in_backup_folder(arquivo):
                    contador += 1
                    yield arquivo.resolve(), contador  # Retorna arquivo e total atual
        
        # Chama a barra passando o generator como callback
        arquivos = self.logger.barra_carregamento_com_callback(buscar_arquivos_generator, self.sep, verbose)
        
        if arquivos is None:
            self.logger.log_error("There are no files in the specified path.")
            
            return False

        try:
            arquivos_a_mudar = {}
            self.logger.log("Loading extensions...", code=10)
            
            try:
                tipos_de_arquivos = self.definer.ler_extensoes()
                self.logger.log("Extensions loaded successfully.", code=11)
            
            except (FileNotFoundError, json.JSONDecodeError) as e:
                self.logger.log_error(f"Error loading extensions: {e}", True)

                return False
            
            if not isinstance(tipos_de_arquivos, dict):
                self.logger.log_error("Extensions are not a valid dictionary", True)
    
                return False
            
            for arquivo in arquivos:
                pasta_destino = Path(saida / arquivo.suffix[1:])
            
                for tipo, extensoes in tipos_de_arquivos.items():
                    extensoes_do_arquivo: list = arquivo.suffixes
                    
                    # Verifica se há interseção entre as extensões
                    if any(ext in extensoes for ext in extensoes_do_arquivo):
                        pasta_destino = Path((saida / "backup" / tipo) if backup else (saida / tipo))
                        break

                else:
                    pasta_destino = Path(f"{saida}/No_Extensions")

                destino = pasta_destino / arquivo.name

                arquivos_a_mudar[str(arquivo)] = str(destino)
            
            self.logger.log_changes(arquivos_a_mudar, self.sep, verbose=verbose, backup=backup)

            
            if utils.continue_action(y=y):
                self.logger.log_changes(arquivos_a_mudar, backup=backup)
                return True
            
        except PermissionError:
            self.logger.log(f"Error: Ryzor does not have permission to act on {saida}", debug=True, code=9)
            return False