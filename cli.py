def main():
    import argparse as ap
    from pathlib import Path
    import sys
    import os
# Adiciona o diretório src ao path
    src_dir = Path(__file__).parent
    sys.path.insert(0, str(src_dir))

    try:
        from rich.console import Console
        console = Console()

    except (ModuleNotFoundError, ImportError) as e:
            print("[Ryzor] Parece que o rich não está instalado em seu sistema, tente `ryzor repair`")
            quit()

    try:
        from modules.utils import Utils
        utils = Utils()

    except (ModuleNotFoundError, ImportError):
        print("em cli")
        print(f"[Debug] Erro: Módulo 'utils' não encontrado nos arquivos do ryzor...")

        print("[Debug] Tente `ryzor repair`")
        print("[Debug] Cancelando...")
        quit()

    if utils.validate_modules():
        from modules.logger import ConsoleManager
        from modules.remover import DeletionManager  
        from modules.definer import DefinitionManager
        from modules.file_manager import FileController
        from modules.lister_manager import Viewer
        from modules.repair_manager import Restorer

    else:
        quit()

    padrao = Path(".")

    console_manager = ConsoleManager()
    deletion_managerver = DeletionManager()
    file_controller = FileController()
    definition_manager = DefinitionManager()
    viewer = Viewer()

    # parser pai com flags "globais"
    parent = ap.ArgumentParser(add_help=False)
    parent.add_argument("--verbose", "-v", action="store_true", help=console_manager.help_log("```--verbose``` ou ```-v``` -> Modo Verboso."))
    parent.add_argument("--no_preview", "-n_pv", action="store_true", help=console_manager.help_log("``--no_preview```` ou ```-n_pv``` -> desativa o preview antes das mudanças."))
    parent.add_argument("--yes", "-y", action="store_true", help=console_manager.help_log("```--yes``` ou ```-y``` -> Pré-responde sim para continuar a ação escolhida."))
    parent.add_argument("--recursive", "-r", action="store_true", help=console_manager.help_log("```--recursive``` ou ```-r``` -> Ativa o modo de recursão."))
    parent.add_argument("--path", "-p", nargs="?", default=padrao, type=Path, help=console_manager.help_log("```--path``` ou ```-p``` -> Caminho dos arquivos."))
    parent.add_argument("--destination", "-d", nargs="?", default=padrao, type=Path, help=console_manager.help_log("```--destination``` ou ```-d``` -> Caminho de destino."))
    parent.add_argument("--type", "-t", type=str, help=console_manager.help_log("```-type``` ou ```-t``` -> Define o tipo de arquivo."))
    parent.add_argument("--extensions", "-exts", nargs="+", help=console_manager.help_log("```--extensions``` ou ```-exts``` -> Define as extensões que o tipo suporta."))
    parent.add_argument("--modules", "-m", action="store_true", help=console_manager.help_log("```--modules``` ou ```-m``` -> Avisa ao ryzor para reparar os módulos internos."))


    parent_remove = ap.ArgumentParser(add_help=False)

    parent_remove.add_argument("--directory", "-dir", type=str, default=padrao, help=console_manager.help_log("```--directory <diretório> ``` or ```-dir <diretório>``` -> Diretório a ser apagado."))
    parent_remove.add_argument("--folder", "-fdr", type=str, default=padrao.resolve(), help=console_manager.help_log("```--folder <pasta> ``` or ```-fdr <pasta>``` -> Pasta a ser apagada."))
    parent_remove.add_argument("--file", "-fl", action="store_true", help=console_manager.help_log("```--file``` or ```-fl``` -> Apaga um arquivo específico."))
    parent_remove.add_argument("--full", "-f", action="store_true", help=console_manager.help_log("```--full``` or ```-f``` -> Apaga tudo da pasta."))

    # parser principal
    parser = ap.ArgumentParser(description="Ryzor")
    subparsers = parser.add_subparsers(dest="comando", help=console_manager.help_log("\n[primary][Ryzor][/] [normal 2]---Comandos disponíveis---[/]\n"))

    # subparsers recebem o parent (herdam os flags)
    parser_help = subparsers.add_parser("help", parents=[parent])
    parser_organize = subparsers.add_parser("organize", parents=[parent], help=console_manager.help_log("```ryzor organize -p <pasta de origem> -d <pasta de destino>``` -> Apenas organiza os arquivos do caminho passado."))
    parser_backup = subparsers.add_parser("backup", parents=[parent], help=console_manager.help_log("```ryzor backup -p <pasta de origem> -d <pasta de destino>``` -> Faz o backup e organiza os arquivos do caminho passado."))
    parser_list = subparsers.add_parser("list", parents=[parent], help=console_manager.help_log("```ryzor list``` -> Lista arquivos.\n\t```ryzor list -e_exts``` -> Lista tipos de arquivos e extensões suportadas por cada um.\n"))
    parser_define = subparsers.add_parser("define", parents=[parent], help=console_manager.help_log("```ryzor define -t <tipo de arquivos> -e_exts <extensões que o arquivo suporta>``` -> Define um novo tipo de arquivo e extensões suportadas.\n"))
    parser_edit = subparsers.add_parser("remove", parents=[parent_remove], help=console_manager.help_log("```ryzor remove -t <tipo de arquivos>``` -> Remove o tipo de arquivos todo.\n\t```ryzor remove -t <tipo de arquivos> -exts <extensões ou '.' para todas>``` -> Remove todas as extensões do tipo passado...\n"))
    parser_version = subparsers.add_parser("version", help=console_manager.help_log("```ryzor version``` -> Informa a versão atual do Ryzor."))
    parser_repair = subparsers.add_parser("repair", help=console_manager.help_log("```ryzor repair``` -> Restaura o Ryzor para versão de fábrica."))

    parser_list.add_argument("--exists_extensions", "-e_exts", action="store_true", help=console_manager.help_log("```-e_exts (extensões existentes)``` -> Define que os tipos de arquivos/ extensões suportadas serão listadas."))
    parser_define.add_argument("--overwrite", "-ow", action="store_true", help=console_manager.help_log("```-ow``` -> Sobrescreve um tipo/extensão já existente.\n"))

    # parse args
    args = parser.parse_args()

    # dispatch
    match args.comando:
        case "version":
            console_manager.version()

        case "organize":
            file_controller.relocate_files(args.path, args.destination, backup=False, no_preview=args.no_preview, verbose=args.verbose, y=args.yes)

        case "backup":
            file_controller.relocate_files(args.path, args.destination, backup=True, no_preview=args.no_preview, verbose=args.verbose, y=args.yes)

        case "define":
            definition_manager.define_type(type_arg=args.type, extensions_suported=args.extensions, overwrite=args.overwrite)

        case "list":
            if args.exists_extensions:
                viewer.list_extensions()
            else:
                viewer.list_files(caminho=args.path, recursive_mode=args.recursive, verbose=args.verbose)

        case "remove":
            deletion_managerver.remove_extensions(type=args.type, extensions=args.extensions, no_preview=args.no_preview, y=args.yes)

        case "help":
            console_manager.show_help()

        case "repair":
            Restorer.repair(r_extesions=args.e_exts, r_config=False, r_modules=args.modules, y=args.yes)

        case _:
            console_manager.show_help()
            
main()