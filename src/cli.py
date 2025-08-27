import argparse as ap
from pathlib import Path
from modules import (file_manager, definer, lister, remover)
import pyfiglet

padrao = Path(".")

# parser pai com flags "globais"
parent = ap.ArgumentParser(add_help=False)
parent.add_argument("--verbose", "-v", action="store_true", help="[Ryzor] Modo Verboso")
parent.add_argument("--no_preview", "-n_pv", action="store_true", help="[Ryzor] Mostra o preview das mudanças")
parent.add_argument("--yes", "-y", action="store_true", help="[Ryzor] Pré-responde sim para continuar a ação escolhida.")
parent.add_argument("--recursive", "-r", action="store_true", help="[Ryzor] Ativa o modo de recursão")
parent.add_argument("--path", "-p", nargs="?", default=padrao, type=Path, help="[Ryzor] Caminho dos arquivos")
parent.add_argument("--destination", "-d", nargs="?", default=padrao, type=Path, help="[Ryzor] Caminho de destino")
parent.add_argument("--type", "-t", type=str, help="[Ryzor] Define o tipo de arquivo")
parent.add_argument("--extensions", "-exts", nargs="+", help="[Ryzor] Define as extensões que o tipo suporta")

# parser principal
parser = ap.ArgumentParser(description="Ryzor")
subparsers = parser.add_subparsers(dest="comando", help="[Ryzor] Comandos disponíveis")

# subparsers recebem o parent (herdam os flags)
parser_organize = subparsers.add_parser("organize", parents=[parent], help="[Ryzor] Apenas organiza os arquivos do caminho passado")
parser_backup = subparsers.add_parser("backup", parents=[parent], help="[Ryzor] Faz o backup e organiza os arquivos do caminho passado")
parser_list = subparsers.add_parser("list", parents=[parent], help="[Ryzor] Lista arquivos, tipos de arquivos e extensões suportadas por cada um.")
parser_define = subparsers.add_parser("define", parents=[parent], help="[Ryzor] Define um novo tipo de arquivo")
parser_edit = subparsers.add_parser("remove", parents=[parent], help="[Ryzor] Edita a propiedade passada.")
parser_version = subparsers.add_parser("version", help="[Ryzor] Informa a versão atual do Ryzor.")
parser_repair = subparsers.add_parser("repair", help="[Ryzor] Restaura o Ryzor para versão de fábrica.")

parser_list.add_argument("--exists_extensions", "-e_exts", action="store_true", help="[Ryzor] Define que os tipos de arquivos/ extensões suportadas serão listadas")
parser_define.add_argument("--overwrite", "-ow", action="store_true", help="[Ryzor] Sobre escreve um tipo/extensão já existente")

# parse args
args = parser.parse_args()

# dispatch
match args.comando:
    case "version":
        ascii_banner = pyfiglet.figlet_format("Ryzor")
        print(f"{ascii_banner}\n\nBy: Lucas Paulino\nVersion: 0.1.0")

    case "organize":
        file_manager.realocate_files(args.path, args.destination, backup=False, no_preview=args.no_preview, verbose=args.verbose, y=args.yes)

    case "backup":
        file_manager.realocate_files(args.path, args.destination, backup=True, no_preview=args.no_preview, verbose=args.verbose, y=args.yes)

    case "define":
        definer.definer(type_arg=args.type, extensions_suported=args.extensions, overwrite=args.overwrite)

    case "list":
        if args.exists_extensions:
            lister.lister_extensions()
        else:
            lister.lister(caminho=args.path, recursive_mode=args.recursive, verbose=args.verbose)

    case "remove":
        remover.remover_extensoes(type=args.type, extensions=args.extensions, no_preview=args.no_preview, y=args.yes)

    case _:
        parser.print_help()
