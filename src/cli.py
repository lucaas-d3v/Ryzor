import argparse as ap
from pathlib import Path
from modules import (file_manager, definer)

# Parser principal
parser = ap.ArgumentParser(description="Ryzor")
parser.add_argument("--verbose", "-v", action="store_true", help="[Ryzor] Modo Verboso")
parser.add_argument("--no_preview", "-n_pv", action="store_true", help="[Ryzor] Mostra o preview das mudanças")
parser.add_argument("--yes", "-y", action="store_true", help="[Ryzor] Pré-responde sim para continuar a ação ecolhida.")

# Subparsers
subparsers = parser.add_subparsers(dest="comando", help="[Ryzor] Comandos disponíveis")

padrao = Path.cwd()

# Subparser: organize
parser_organize = subparsers.add_parser("organize", help="[Ryzor] Apenas organiza os arquivos do caminho passado")
parser_organize.add_argument("--path", "-p", nargs="?",default=str(padrao), type=str, help="[Ryzor] Caminho dos arquivos")
parser_organize.add_argument("--destination", "-d", nargs="?",default=str(padrao),type=str, help="[Ryzor] Caminho de destino")

# Subparser: backup
parser_backup = subparsers.add_parser("backup", help="[Ryzor] Faz o backup e organiza os arquivos do caminho passado")
parser_backup.add_argument("--path", "-p", nargs="?", default=str(padrao), type=str, help="[Ryzor] Caminho dos arquivos")
parser_backup.add_argument("--destination", "-d", nargs="?", default=f"{padrao}/Backup", type=str, help="[Ryzor] Caminho de destino")

# Subparser: define
parser_define = subparsers.add_parser("define", help="[Ryzor] Define um novo tipo de arquivo")
parser_define.add_argument("--type", "-t", type=str, help="[Ryzor] Define o tipo de arquivo")
parser_define.add_argument("--extensions", "-exts", nargs="+", help="[Ryzor] define as extensoes que o tipo suporta")
parser_define.add_argument("--overwrite", "-ow", action="store_true", help="[Ryzor] Sobre escreve um tipo/extensao ja existente")

# Pega todos os args
args, unknown = parser.parse_known_args()

# Exemplo de uso
match args.comando:
    case"organize":
        file_manager.realocate_files(Path(args.path), Path(args.destination), backup=False, no_preview=args.no_preview, verbose=args.verbose, y=args.yes)

    case "backup":
        file_manager.realocate_files(Path(args.path), Path(args.destination), backup=True, no_preview=args.no_preview, verbose=args.verbose, y=args.yes)

    case "define":
        definer.definer(type_arg=args.type, extensions_suported=args.extensions, overwrite=args.overwrite)

    case _:
        parser.print_help()
