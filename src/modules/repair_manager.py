"""Classe repair"""

from pathlib import Path
import json
import subprocess

from .logger import ConsoleManager
from .utils import Utils

class Restorer:
    def __init__(self):
        self.extensions = {}
        self.try_action = 0
        self.base_dir = Path(".") / ".." / "Ryzor"
                
                
    def _default_extension_to_use(self) -> None:
        JSON_PATH = self.base_dir / "src" / "protected" / "extensions_default.json"
        
        if JSON_PATH.exists():
            with JSON_PATH.open("r") as f:
                content = json.load(f)
                
                if content:
                    self.extensions = content 
                    
                    return
            
        else:    
            self.extensions = {
            "Effects": [
            ".fx",
            ".ffx",
            ".aep",
            ".aepx",
            ".prfpset",
            ".mogrt",
            ".vfx",
            ".preset",
            ".action"
            ],
            "Compactados": [
            ".rar",
            ".zip",
            ".7zip",
            ".7z",
            ".tar",
            ".tar.gz",
            ".tgz",
            ".tar.bz2",
            ".tbz",
            ".gz",
            ".bz2",
            ".xz",
            ".iso",
            ".dmg",
            ".jar",
            ".apk"
            ],
            "Mc_addon": [".mcpack", ".mcaddon", ".mcworld", ".mcr", ".mce", ".mca"],
            "Codigos": [
            ".py",
            ".pyc",
            ".ipynb",
            ".cs",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".hpp",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".html",
            ".htm",
            ".css",
            ".scss",
            ".sass",
            ".php",
            ".rb",
            ".go",
            ".rs",
            ".swift",
            ".kt",
            ".kts",
            ".m",
            ".mm",
            ".sh",
            ".bat",
            ".ps1"
            ],
            "Installers": [
            ".msi",
            ".exe",
            ".pkg",
            ".deb",
            ".rpm",
            ".app",
            ".apk",
            ".bin",
            ".run",
            ".dmg"
            ],
            "Documentos": [
            ".txt",
            ".doc",
            ".docx",
            ".odt",
            ".xls",
            ".xlsx",
            ".ods",
            ".csv",
            ".ppt",
            ".pptx",
            ".odp",
            ".pdf",
            ".xps",
            ".tex",
            ".ltx",
            ".rtf",
            ".md",
            ".markdown",
            ".html",
            ".htm",
            ".epub",
            ".mobi",
            ".log",
            ".json",
            ".xml",
            ".yml",
            ".yaml",
            ".ini",
            ".cfg",
            ".toml",
            ".db",
            ".sql",
            ".sqlite"
            ],
            "Imagems": [
            ".ico",
            ".jpg",
            ".jpeg",
            ".jfif",
            ".pjpeg",
            ".pjp",
            ".cur",
            ".bmp",
            ".png",
            ".gif",
            ".tiff",
            ".tif",
            ".webp",
            ".heic",
            ".heif",
            ".avif",
            ".dds",
            ".exr",
            ".raw",
            ".svg",
            ".ai",
            ".eps",
            ".cdr",
            ".psd",
            ".indd",
            ".pdf",
            ".kra",
            ".xcf",
            ".orf",
            ".nef",
            ".cr2",
            ".dng",
            ".arw"
            ],
            "Videos": [
            ".mp4",
            ".mov",
            ".mkv",
            ".avi",
            ".flv",
            ".wmv",
            ".3gp",
            ".3g2",
            ".mpg",
            ".mpeg",
            ".ogv",
            ".m4v",
            ".mts",
            ".ts",
            ".divx",
            ".vob",
            ".f4v",
            ".webm",
            ".rm",
            ".rmvb",
            ".m2ts"
            ],
            "Audios": [
            ".mp3",
            ".wav",
            ".flac",
            ".aac",
            ".ogg",
            ".m4a",
            ".wma",
            ".alac",
            ".aiff",
            ".opus",
            ".amr",
            ".dsd",
            ".pcm",
            ".aax",
            ".ra",
            ".mid",
            ".midi",
            ".aif",
            ".au",
            ".caf"
            ],
            "Projetos": [
            ".veg",
            ".vf",
            ".aep",
            ".aepx",
            ".prproject",
            ".pproj",
            ".ppj",
            ".drp",
            ".db",
            ".fcpxml",
            ".fcpbundle",
            ".imovieproj",
            ".kdenlive",
            ".mlt",
            ".osp",
            ".xsed",
            ".vpr",
            ".blend",
            ".c4d",
            ".max",
            ".mb",
            ".ma",
            ".skp",
            ".psd",
            ".prproj",
            ".aep",
            ".flp",
            ".als",
            ".logicx",
            ".musx",
            ".rpp",
            ".sib",
            ".cpr",
            ".tracktion",
            ".omf",
            ".aiffproj"
            ]
        }
            
            
        Path(JSON_PATH).mkdir(exist_ok=True, parents=True)
        
        with JSON_PATH.open("w") as f:
            json.dump(self.extensions, f, indent=4)
                       
                
    def repair_extensions(self):
        JSON_IN_PRODUCTION = self.base_dir / "src" / "modules" / "data" / "extensions.json"
        JSON_DEFAULT = self.base_dir / "protected" / "extensions_default.json"

        jsons = [JSON_IN_PRODUCTION, JSON_DEFAULT]

        for i in jsons:
            Path(i).mkdir(exist_ok=True, parents=True)
        
            with i.open("w") as f:
                json.dump(self.extensions, f, indent=4)  
                       
    def repair_dependencies(self):
        try:
            self.try_action += 1
            req_file = self.base_dir / "requirements.txt"

            if req_file.exists():
                try:
                    subprocess.run(
                        ["pip", "install", "-r", str(req_file)],
                        check=True
                    )
                    ConsoleManager.log("Dependências instaladas com sucesso.", code=13)
                except subprocess.CalledProcessError as e:
                    ConsoleManager.log_error(f"Falha ao instalar dependências: {e}")

            else:
                ConsoleManager.log_error("Arquivo requirements.txt não encontrado.")
                ConsoleManager.log(f"Tentando criar requiriments.txt em {req_file}.", code=12)

                with open(str(req_file), "w") as f:
                    f.write("rich==13.9.4\npyfiglet==0.8.post1\nsend2trash==1.8.3")

                self.repair_dependencies()
                
        except RecursionError:
            ConsoleManager.log_error(f"Não foi possível criar requiriments.txt em {req_file}.")  
            ConsoleManager.log_error(f"A quantidade de tentativas explodiu em {self.try_action} tentativas.")  
            ConsoleManager.log(f"Cancelando instalação automática, por favor, tente `pip install rich==13.9.4 send2trash==1.8.3 pyfiglet==0.8.post1`.", code=12)
            
            
    def repair_modules(self):
        DEFINER_CONTENT = '''
"""Arquivo responsável por geranciar o comando 'define' """

import json
from pathlib import Path
from typing import Iterable, List, Union

class DefinitionManager:
    def __init__(self):
        pass

    def normalize_extensions_input(self, exts: Union[str, Iterable]) -> List[str]:
        """
        Garante que o input de extensões vire uma lista de strings correta.
        Aceita: lista, tupla, string '.xml', string '[".xml",".py"]' ou '.xml,.py'.
        """
        
        if isinstance(exts, (list, tuple)):
            return [str(x) for x in exts]
        
        if isinstance(exts, str):
            s = exts.strip()
        
            if (s.startswith("[") and s.endswith("]")):
                try:
                    parsed = json.loads(s)
                    if isinstance(parsed, list):
                        return [str(x) for x in parsed]
                except Exception:
            
                    pass
            
            if "," in s:
                parts = [p.strip().strip('"').strip("'") for p in s.split(",") if p.strip()]
                return parts

            return [s]

        return [str(exts)]

    def save_extensions(self, data: dict[str, list[str]]):
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "extensions.json"

        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        

    def read_extensions(self, json_path: Path) -> dict[str, list[str]]:
        base_dir = Path(__file__).parent
        
        if not json_path:
            JSON_PATH = base_dir / "data" / "extensions.json"

        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

        with JSON_PATH.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        return data

    def write_extensions(self, extensoes: dict[str, list[str]], overwrite: bool = False) -> bool:
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "extensions.json"

        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            try:
                data = self.read_extensions()

                if not isinstance(data, dict):
                    data = {}
            
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            add = {}
            for tipo, _extensoes in extensoes.items():
                # garante que _extensoes é lista
                novos = _extensoes if isinstance(_extensoes, list) else [ _extensoes ]
                if overwrite or (tipo not in data):
                    add[tipo] = novos
                else:
                    # mescla mantendo ordem e sem duplicatas
                    atuais = list(data.get(tipo, []))
                    for ext in novos:
                        if ext not in atuais:
                            atuais.append(ext)
                    add[tipo] = atuais

            data.update(add)

            with json_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return True

        except PermissionError as e:
            print(f"[Ryzor] Erro de permissão: {e}")
            return False
        except Exception as e:
            print(f"[Ryzor] Erro inesperado ao escrever JSON: {e}")
            return False


    def define_type(self, type_arg: Union[str, Iterable[str]], extensions_suported: Union[str, Iterable], overwrite: bool = False):
        """
        type_arg: string 'Codigos' ou lista de tipos ['Codigos','Imagens']
        extensions_suported: lista ou string que representa extensões
        exemplos válidos:
            - ".xml"
            - ".xml .py"  (se usar nargs='+')
            - '[".xml", ".py"]' (string JSON)
            - [".xml", ".py"]
        """

        if isinstance(type_arg, (list, tuple)):
            tipos = [str(t) for t in type_arg]
        else:
            tipos = [str(type_arg)]

        exts = self.normalize_extensions_input(extensions_suported)

        data_to_add: dict[str, list[str]] = {}

        if len(tipos) == 1:
            
            data_to_add[tipos[0]] = exts
        elif len(tipos) == len(exts):
            
            for t, e in zip(tipos, exts):
                data_to_add[t] = [e] if isinstance(e, str) else list(e)
        else:
            for t in tipos:
                data_to_add[t] = list(exts)

        if self.write_extensions(data_to_add, overwrite):
            print(f"[Ryzor] extensões {data_to_add} adicionadas com sucesso")
        else:
            print("[Ryzor] Falha ao salvar extensões")
        '''
        
        FILE_MANAGER_CONTENT = '''
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
    print(f"[Debug] Erro: Módulo utils não encontrado nos arquivos do ryzor, tente `ryzor repair`")
    print("[Debug] Cancelando...")
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

    def rename(self, file: Path, qtd: list[int] = [0]) -> Path:
        stem = file.stem            # nome do arquivo sem extensão
        extensao = "".join(file.suffixes)  # todas as extensões juntas (ex: ".tar.gz")

        ultimo = max(qtd)
        new_name = f"{stem} ({ultimo + 1}){extensao}"

        return file.with_name(new_name)

    def relocate_files(self, 
            entrada: Path, saida: Path,
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
            logger.log_error("O caminho de entrada não existe.")
            logger.log_error("Cancelando")

            return False

        if not entrada.is_dir():
            """
            Medida de segurança caso o caminho especificado não seja um diretório.
            """
            logger.log_error("O caminho informado não pode ser um arquivo.")

            return False

        if not saida.exists():
            """
            Medida de segurança caso a saida não exista.
            """

            logger.log("O caminho de saida não existe.", code=9, debug=True)
            logger.log("Tentando Criar...", debug=True, code=10)
            
            try:

                saida.mkdir(parents=True, exist_ok=True)
                logger.log("Caminho de saída criado com sucesso.", code=11)
                logger.log("Continuando...", code=11)

            except PermissionError:
                logger.log_error(f"Erro, o Ryzor não tem permissão para atuar em {saida}")
                return False
            
        if not saida.is_dir():
            """
            Medida de segurança, caso a saida não seja um diretório.
            """        
            logger.log_error("O caminho informado não pode ser um arquivo.")

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
        arquivos = logger.barra_carregamento_com_callback(buscar_arquivos_generator, self.sep, verbose)
        
        if arquivos is None:
            logger.log_error("Não existem arquivos no caminho informado.")
            
            return False

        try:
            arquivos_a_mudar = {}
            logger.log("Carregando extensões...", code=10)
            
            try:
                tipos_de_arquivos = self.definer.ler_extensoes()
                logger.log("Extensões carregadas com sucesso.", code=11)
            
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.log_error(f"Erro ao carregar as extensões: {e}", True)

                return False
            
            if not isinstance(tipos_de_arquivos, dict):
                logger.log_error("As extensões não são um dicionário válido", True)
    
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
                    pasta_destino = Path(f"{saida}/Sem_Extensões")

                destino = pasta_destino / arquivo.name

                arquivos_a_mudar[str(arquivo)] = str(destino)
            
            logger.log_mudancas(arquivos_a_mudar, self.sep, verbose=verbose, backup=backup)

            
            if utils.continue_action(y=y):
                try:
                    from src.modules.logger import barra_progresso

                except (ModuleNotFoundError, ImportError):
                    logger.log_error("Erro: O módulo logger não encontrado nos arquivos do ryzor",True)
                    logger.log_error("Cancelando...")

                    return False

                barra_progresso(arquivos_a_mudar, backup=backup)
                return True
            
            else:
                logger.log("Cancelando...", code=10)
                return False

        except PermissionError:
            logger.log(f"Erro: O Ryzor não tem permissão para atuar em {saida}", debug=True, code=9)
            return False
        '''
        
        LOGGER_CONTENT = '''
"""Arquivo responsável pelas informações do terminal"""                                                         

try:
    from rich import box                                    
    from rich.table import Table                            
    from rich.console import Console                        
    from rich.theme import Theme                            
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn                                  
    from rich.progress import SpinnerColumn, TimeElapsedColumn                                                      
    from rich.live import Live                              
    from rich.align import Align                            
    from rich.progress import SpinnerColumn, BarColumn      
    from rich.theme import Theme

except (ModuleNotFoundError, ImportError):
    print(f"[Debug] Erro: Módulo Rich não encontrado nos arquivos do ryzor, tente `ryzor repair`")
    print("[Debug] Cancelando...")
        
    quit() 

from pathlib import Path                                
import time

import pyfiglet
import sys
import select
import termios
import tty
import contextlib

class ConsoleManager:
    def __init__(self):
        self.ryzor_theme = Theme({
            "logo":       "#FFFCDB bold",   #1
            "normal":     "#FFFCDB",      #2
            "normal 2":   "#FFFCDB bold",   #3
            "primary":    "#00FF84 bold",   #4
            "secondary":  "#00CFFF bold",   #6
            "background": "on #7F001F",     #7
            "text":       "#FFFCDB",      #8
            "muted":      "#CFC7B8",      #9
            "accent":     "#28F0D5",      #10
            "error":      "#FF3B5C bold",   #11
            "warning":    "#FFC107 bold",   #12
            "success":    "#00FF84"       #13
        })

        self.keys = list(self.ryzor_theme.styles.keys())
        
        self.console = Console(theme=self.ryzor_theme)

    def logo(self):
        return pyfiglet.figlet_format("Ryzor", font="isometric1")

    def version(self):
        ascii_banner = self.logo()
        ascii_logo = ascii_banner.rstrip("\n")
        lines = ascii_logo.splitlines()

        if lines:
            block_width = max(len(line) for line in lines)
            term_width = self.console.size.width
            left_pad = max((term_width - block_width) // 2, 0)
            for line in lines:
                self.console.print(" " * left_pad + f"[logo]{line.rstrip()}[/]")

        print()

        self.console.rule(style="error")

        version_table = Table(
            title="",
            style="primary",
            title_justify="center",
            show_lines=False,
            expand=False,
            box=None,
            padding=(0,1),
        )
        version_table.add_row("[normal]By:[/] [primary]~K'[/]")
        version_table.add_row("[#FFC107]Version: 0.2.5[/]")


        self.console.print(version_table, justify="center")
        self.console.print()

        self.console.rule(style="error")

    def show_help(self):
        ascii_logo = self.logo().rstrip("\n")

        lines = ascii_logo.splitlines()
        if lines:
            block_width = max(len(line) for line in lines)
            term_width = self.console.size.width
            left_pad = max((term_width - block_width) // 2, 0)
            for line in lines:
                self.console.print(" " * left_pad + line.rstrip(), style="primary")

        self.console.print()

        # tabela com linhas horizontais entre cada entrada
        comandos = Table(
            title="Comandos",
            style="primary",
            title_justify="center",
            show_lines=True,       # desenha linha horizontal entre as linhas
            expand=False,
            box=box.SQUARE,        # experimente box.SIMPLE, box.SQUARE ou box.SIMPLE_HEAVY
            padding=(0,1),
        )

        comandos.add_column("Comando", style="secondary", no_wrap=True, justify="left")
        comandos.add_column("Uso", style="warning", justify="left")
        comandos.add_column("Descrição", style="primary", justify="left")

        comandos.add_row("organize", "ryzor organize -p <origem> -d <destino>", "Apenas organiza os arquivos do caminho passado (padrao = diretório atual).")
        comandos.add_row("backup",   "ryzor backup -p <origem> -d <destino>", "Faz o backup e organiza os arquivos do caminho passado (padrao = diretório atual).")
        comandos.add_row("list",     "ryzor list -e_exts", "Lista arquivos ou tipos de arquivos e extensões suportadas se usar -e_exts (padrao = diretório atual).")
        comandos.add_row("define",   "ryzor define -t <tipo> -exts <extensões>", "Define um novo tipo de arquivo e extensões suportadas.")
        comandos.add_row("remove",   "ryzor remove -t <tipo> -exts <extensões>", "Remove o tipo todo ou extensões específicas (se não passar extensoes, o tipo sera removido).")
        comandos.add_row("version",  "ryzor version",                        "Informa a versão atual do Ryzor.")
        comandos.add_row("repair",   "ryzor repair",                         "Restaura o Ryzor para versão de fábrica.")
        comandos.add_row("help",     "ryzor help",                           "Mostra este menu de ajuda.")

        self.console.print(comandos, justify="center")
        self.console.print()

    def help_log(self, mensagem: str) -> str:
        """
        Formata mensagem de ajuda para o argparse.
        IMPORTANTE: Esta função deve RETORNAR a string, não imprimir!
        """
        msg = mensagem.split(" ")

        _msg = "[primary][Help][/] [warning]"

        for palavra in msg:
            if palavra == "->":
                _msg += f"[primary]{palavra}[/] [normal 2]"
            else:
                _msg += f"{palavra} "
        else:
            _msg += "[/][/]"

        return _msg

    def log_mudancas(self, mudancas: dict[str, str], sep: str, backup: bool, verbose: bool = False):
        mudancas_table = Table(
            title="[primary]Mudanças[/]",
            style="primary",
            title_justify="center",
            show_lines=True,       # desenha linha horizontal entre as linhas
            expand=False,
            box=box.SQUARE,        # experimente box.SIMPLE, box.SQUARE ou box.SIMPLE_HEAVY
            padding=(0,1)
        )

        self.console.rule(
        f"[warning]Modo:[/] {'Backup' if backup else 'Organização'}\n"
        f"[warning]Verbose:[/] {'on' if verbose else 'off'}\n"
        f"[warning]Total de modificações:[/] {len(mudancas)}"
    )

        mudancas_table.add_column("Origem", style="secondary", no_wrap=True, justify="left")
        mudancas_table.add_column("Destino", style="warning", justify="left")
        mudancas_table.add_column("Tipo", style="primary", justify="left")


        for origem, destino in mudancas.items():
            tipo = Path(origem)

            origem = self.resumo_pasta(origem, sep, verbose=verbose)
            destino = self.resumo_pasta(destino, sep, verbose)


            mudancas_table.add_row(origem, destino, f"{'Arquivo' if tipo.is_file() else 'Diretório' if tipo.is_dir() else 'Não específicado'}")

        self.console.print(mudancas_table, justify="center")
        self.console.print()

    def log_error(self, mensagem, repair: bool = False, cancel: bool = True):
        inicio = "[Erro]"

        mensagem = f"[error]{inicio} {mensagem}[/]"

        if repair:
            mensagem += ", tente `ryzor repair`."

        self.console.print(mensagem)

        if cancel:
            self.console.print(f"{inicio} [error]Cancelando...[/]")


    def log(self, mensagem: str, debug: bool = False, code: int = 1, end: str = "\n") -> None:
        """
        args:
            mensagem: mensagem a ser escrita no terminal.
            debug: ativa o modo [Debug].
            code: codigo referente ao tipo de mensage, escrita
        """

        inicio = "[warning][Debug][/]" if (debug or code == 9) else "[primary][Ryzor][/]"
        mensagem = f"{inicio} [{self.keys[code - 1]}]{mensagem}[/]" if code != 0 else mensagem

        self.console.print(f"{mensagem}", end=end, justify="center")

    def progress_bar(self, mudancas: dict[str, str], backup=True):
        """
        Cria barra de progresso Rich centralizada e executa arquivos via callback.
        """

        from .utils import execute

        if not mudancas:
            self.log("Nenhum arquivo para processar", code=10)
            return False

        total = len(mudancas)
        self.log(f"Iniciando {'backup' if backup else 'organização'} de {total} arquivos...", code=11)

        # montar o Progress (não como context manager)

        try:
            progress = Progress(
                SpinnerColumn(style="accent"),
                TextColumn("[primary]{task.fields[acao]}[/primary]", justify="center"),
                TextColumn("[muted]{task.fields[nome_arquivo]}[/muted]", justify="center"),
                BarColumn(bar_width=None, style="success", complete_style="primary"),
                TextColumn("[success]{task.percentage:>3.0f}%[/success]", justify="center"),
                TimeRemainingColumn(),
                console=self.console,
                transient=False,
            )

            # Live + Align centralizam todo o render do Progress
            with Live(Align(progress, "center"), refresh_per_second=10, console=self.console):
                progress.start()
                task = progress.add_task(
                    "",
                    total=total,
                    nome_arquivo="Preparando...",
                    acao="Iniciando"
                )

                # Callback que será passado para execute()
                def atualizar(self, **kwargs):
                    progress.update(
                        task,
                        completed=kwargs.get("atual", 0),
                        nome_arquivo=kwargs.get("nome_arquivo", ""),
                        acao=kwargs.get("acao", ""),
                        erro=kwargs.get("erro", False)
                    )

                try:
                    # Chamada para execute com o callback
                    sucesso = execute(mudancas, callback=atualizar, backup=backup)

                    if sucesso[0]:
                        self.log("Operação concluída com sucesso!", code=11)
                    
                    else:
                        self.log_error(f"Erro em execute: {sucesso[1]}")
                        self.log_error("Cancelando...")

                except KeyboardInterrupt:
                    # garante parada limpa se Ctrl+C
                    progress.stop()
                    self.log("Operação interrompida pelo usuário (Ctrl+C).", code=10)
                    return False
                except Exception as e:
                    progress.stop()
                    self.log(f"Erro durante operação: {e}", code=9)
                    return False
                finally:
                    # sempre para o progress antes de sair do Live
                    progress.stop()

            return sucesso


        except Exception as e:
            self.log(f"Erro na barra de progresso: {e}", code=9)
            return False


    @contextlib.contextmanager
    def stdin_cbreak(self, ):
        """
        Context manager que coloca o terminal em modo cbreak (caractere-a-caractere)
        e restaura as flags originais ao sair.
        Só funciona em Unix-like (ok pro seu Debian).
        """
        fd = sys.stdin.fileno()
        old_attrs = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            yield
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)


    def tecla_pressionada(self, tecla="q") -> bool:
        """
        Checa sem bloqueio se uma tecla foi pressionada.
        Retorna True se a tecla (único caractere) corresponde.
        Deve ser usada enquanto o terminal estiver em cbreak (veja stdin_cbreak).
        """
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            ch = sys.stdin.read(1)
            return ch.lower() == tecla.lower()
        return False

    from pathlib import Path

    def resumo_pasta(self, arquivo, sep="/", verbose=False):
        # normaliza arquivo (Path ou ".")
        path = Path.cwd() if arquivo == "." else Path(arquivo)
        path = path.resolve()

        if verbose:
            # caminho completo
            return str(path)
        else:
            parts = path.parts
            if len(parts) <= 2:
                return sep.join(parts)
            return sep.join(parts[-2:])


    def loading_bar_with_callback(self, callback_busca, sep, verbose = False):
        """
        Barra de progresso que executa uma função callback para buscar arquivos.
        Agora permite interromper com 'q' (sem Enter) ou com Ctrl+C.
        """
        arquivos_encontrados = []

        try:
            # ativa modo cbreak só durante a execução da barra
            with self.stdin_cbreak():
                with Progress(
                    SpinnerColumn(style="accent"),
                    TextColumn("[accent]Carregando arquivos[/accent]"),
                    TextColumn("[primary]{task.fields[contador]}[/primary]"),
                    TextColumn("[muted]{task.fields[pasta]}[/muted]"),
                    TimeElapsedColumn(),
                    console=self.console,
                ) as progress:

                    task = progress.add_task(
                        "",
                        contador="0 arquivos encontrados... ('q' para sair)",
                        pasta="Iniciando..."
                    )

                    try:
                        # Executa o callback que faz a busca real
                        for arquivo, total in callback_busca():
                            # checa tecla sem bloquear
                            if self.tecla_pressionada("q"):
                                progress.stop()
                                self.log("Busca interrompida pelo usuário (tecla 'q')...", code=10)
                                return

                            arquivos_encontrados.append(arquivo)

                            arquivo_ = Path(arquivo)

                            pasta = self.resumo_pasta(arquivo, sep=sep, verbose=verbose)

                            progress.update(
                                task,
                                contador=f"{total} arquivos encontrados...",
                                pasta=pasta
                            )

                    except KeyboardInterrupt:
                        # Ctrl+C
                        progress.stop()
                        self.log("Busca interrompida pelo usuário...", code=10)

                    except Exception as e:
                        progress.stop()
                        self.log(f"Erro durante carregamento: {e}", code=9)

        except KeyboardInterrupt:
            # Caso o KeyboardInterrupt ocorra fora do with (segurança extra)
            self.log("Busca interrompida pelo usuário (Ctrl+C).", code=10)
            return

        except Exception as e:
            self.log(f"Erro inesperado: {e}", code=9)
            return

        return arquivos_encontrados


    def barra_carregamento_simples_callback(self, callback_busca):
        """
        Versão mais simples da barra com callback
        """
        arquivos_encontrados = []

        with Progress(
            SpinnerColumn(style="accent"),
            TextColumn("[accent bold]Descobrindo arquivos...[/accent bold]"),
            TextColumn("[primary]{task.fields[status]}[/primary]"),
            console=self.console,
        ) as progress:

            task = progress.add_task("", status=" 0")

            try:
                for arquivo, total in callback_busca():
                    arquivos_encontrados.append(arquivo)

                    # Atualiza a cada 10 arquivos para melhor performance
                    if total % 10 == 0:
                        progress.update(task, status=f" {total}")

                # Status final
                progress.update(task, status=f" {len(arquivos_encontrados)}")
                time.sleep(0.3)

            except Exception as e:
                self.log(f"Erro: {e}", code=9)

        return arquivos_encontrados


    def barra_carregamento_avancada_callback(self, callback_busca, titulo="Carregando"):
        """
        Versão mais avançada que permite customizar o título
        """
        arquivos_encontrados = []

        with Progress(
            SpinnerColumn(style="accent", spinner_name="dots"),
            TextColumn(f"[accent]{titulo}[/accent]"),
            TextColumn("[primary]{task.fields[contador]}[/primary]"),
            TextColumn("[muted]{task.fields[info]}[/muted]"),
            TimeElapsedColumn(),
            console=self.console,
        ) as progress:

            task = progress.add_task(
                "",
                contador="0",
                info="Iniciando..."
            )

            start_time = time.time()

            try:
                for resultado in callback_busca():
                    # Callback pode retornar tupla (arquivo, total) ou (arquivo, total, info_extra)
                    if len(resultado) == 2:
                        arquivo, total = resultado
                    else:
                        arquivo, total, info_extra = resultado

                    arquivos_encontrados.append(arquivo)

                    elapsed = time.time() - start_time
                    progress.update(
                        task,
                        contador=f"{total}",
                        info=f"{elapsed:.1f}s"
                    )

            except Exception as e:
                progress.update(task, info=self.log(f"Erro: {str(e)[:30]}...", code=9))

        return arquivos_encontrados 
        '''
        
        REMOVER_CONTENT = '''
"""Remover module"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .utils import Utils
    util = Utils()

except (ModuleNotFoundError, ImportError):
    print(f"[Debug] Erro: Módulo utils não encontrado nos arquivos do ryzor, tente `ryzor repair`")
    print("[Debug] Cancelando...")
        
    quit()    

if util.validate_modules():
    from .definer import DefinitionManager
    from .file_manager import FileController
    from .logger import ConsoleManager
    from pathlib import Path
    from send2trash import send2trash   

else:
    quit()

class DeletionManager():
    def __init__(self):
        self.console_manager = ConsoleManager()
        self.definition_manager = DefinitionManager()
        self.file_controller = FileController()
        self.utils = util

    def remove_extensions(self, type, extensions, no_preview, y: bool = False):
        """
        args:
            type: tipo das extensões.
            extensions: extensoes para remover, caso seja '.', apaga todas as extensões do tipo específicado.
            y: continuar sem perguntar
        """

        data = self.definition_manager.read_extensions()

        if not type in data:
            print(f"[Ryzor] {type} não existe, use `ryzor define -t <tipo das extensoes> -exts <extensoes>` para adicionar uma nova extensao.")
            return

        if extensions is None:
            if not no_preview:
                print(f"[Ryzor] O tipo {type} sera apagado.")
            
                if not self.file_controller.continuar(y=y):       
                    print("[Ryzor] Alterações canceladas")
                    return
        
            data.pop(type)
            self.definition_manager.save_extensions(data)

            print(f"[Ryzor] O tipo {type} foi apagado com sucesso!")
            return

        if extensions[0] == ".":
            extensions = "."

        print("[DEBUG]", extensions)

        antes = []
        antes.extend(data[type])

        indices_remove = []

        if isinstance(extensions, list):
            extensions = self.definition_manager.normalize_extensions_input(extensions)
    
            for extensao in extensions:
                if extensao in data[type]:
                    indices_remove.append(data[type].index(extensao))

            for index in indices_remove:
                data[type].pop(index)

        else:
            data[type] = []

        if no_preview:
            self.definition_manager.save_extensions(data)

        else:     
            print(f"""
                  Antes
                  {antes}
                  -----
                  Depois
                  {data[type]}""")
        
            if not self.file_controller.continuar(y=y):       
                print("[Ryzor] Alterações canceladas")
                return

        self.definition_manager.save_extensions(data)
        print("[Ryzor] Modificações slvas com sucesso!")

    def remover_list(self, alvos: list[Path], mensagem: list[str], no_lixeira: bool = False) -> bool:
        if no_lixeira:
            for alvo in alvos:
                try:
                    if alvo.is_file():
                        alvo.unlink()
                    else:
                        alvo.rmdir()

                except PermissionError:
                    self.console_manager.log_error(f"Ryzor não tem permissão para apagar {alvo.name}")
            
                    break

        
            else:
            
                self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

                return True
    
            return False

        for alvo in alvos:
            try:
                send2trash(str(alvo))
    
            except PermissionError:
                self.console_manager.log_error(f"Ryzor não tem permissão para mover {alvo.name} a lixeira.")

                break

    
        else:
            self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)
            return True

        return False

    def remove_file(self, alvo: Path, mensagem: list[str], no_lixeira: bool = False):
        if no_lixeira:
            try:
                if alvo.is_file():
                    alvo.unlink()
            
                else:
                    alvo.rmdir()
        

                self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

                return True
        
            except PermissionError:
                self.console_manager.log_error(f"Ryzor não tem permissão para apagar {alvo.name}")
                return False

        try:
            send2trash(str(alvo))
            self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

            return True

        except PermissionError:
            self.console_manager.log_error(f"Ryzor não tem permissão para mover {alvo.name} a lixeira.")
            return False

    def remover(self, alvo, full: bool = False, y: bool = False, no_lixeira: bool = False):

        if not alvo.exists():
            self.console_manager.log_error("Alvo da remoção não existe.")
        
            return False
    
        mensagem = ["O", "arquivo", "movido para a lixeira."] 

        if no_lixeira:
            mensagem[2] = "excluido"

        if alvo.is_dir():
            mensagem =["A", "pasta", "movida para a lixeira."] 

            if no_lixeira:
                mensagem[2] = "excluida"


        self.console_manager.log(f"{mensagem[0]} {mensagem[1]} {alvo.name} será {mensagem[2]} ",code=10)
        
        if self.utils.continue_action(y=y):
            if isinstance(alvo, list):
                return self.remover_list(alvos=alvo, no_lixeira=no_lixeira, mensagem=mensagem)

            return self.remove_file(alvo=alvo, mensagem=mensagem)

        else:    
            self.console_manager.log("Cancelando...", code=10)
            return False

        '''
        
        UTILS_CONTENT = '''
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
        '''
        
        CLI_CONTENTS = '''
        
        '''
        
        CONTENTS = {
            "definer": DEFINER_CONTENT,
            "file_manager": FILE_MANAGER_CONTENT,
            "logger": LOGGER_CONTENT,
            "remover": REMOVER_CONTENT,
            "utils": UTILS_CONTENT,
            "cli": CLI_CONTENTS
        }
        
        ConsoleManager.log("Reparando módulos...", code=12)
        
        DIR = self.base_dir / "src" / "modules"
        created_files = []
        Path(DIR).mkdir(exist_ok=True, parents=True)
        
        for module in CONTENTS:
            ConsoleManager.log(f"Reparando {module[:-3]}", code=12)
        
            module_to_repair: Path = dir / f"{module}.py" if module != "cli" else self.base_dir / "src" / f"{module}.py"  
        
            with open(str(module_to_repair), "w", encoding="utf-8-sig") as f:
                f.write(CONTENTS[module])
                
            if module_to_repair.exists():
                created_files.append(module_to_repair)
                                    
        else:
            if created_files:
                ConsoleManager.log("Módulos reparados com sucesso!", code=13)
                return
            
            ConsoleManager.log("Ocorreu eu erro ao reparar os módulos do ryzor...", code=11)
            
    def repair(self, r_extesions: bool = False, r_config: bool = False, r_modules: bool = False, y:bool = False):
        if all(list(r_extesions, r_config, r_config, r_modules)):
            ConsoleManager.log("nõ há argumentos para <repair>, consulte em `ryzor help`", code=12)
            return   
            
        if Utils.continue_action(y=y):
            if r_extesions:
                self.repair_extensions()
            
            if r_config:
                    ConsoleManager.log("Reparação de configuração em desenvolvimento", code=12)

            if r_modules:
                    self.repair_modules()

            return
        
        ConsoleManager.log("Cancelando", code=12)                    