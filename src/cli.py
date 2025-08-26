import argparse as ap
from pathlib import Path
from core import organizar

# Parser principal
parser = ap.ArgumentParser(description="Ryzor")
parser.add_argument("--verbose", "-v", action="store_true", help="[Ryzer] Modo Verboso")
parser.add_argument("--preview", "-pv", action="store_true", help="[Ryzer] Mostra o preview das mudanças")

# Subparsers
subparsers = parser.add_subparsers(dest="comando", help="[Ryzer] Comandos disponíveis")

padrao = Path.cwd()

# Subparser: organize
parser_organize = subparsers.add_parser("organize", help="[Ryzer] Apenas organiza os arquivos do caminho passado")
parser_organize.add_argument("--path", "-p", default=str(padrao), type=str, help="[Ryzer] Caminho dos arquivos")
parser_organize.add_argument("--destination", "-d", default=str(padrao),type=str, help="[Ryzer] Caminho de destino")


# Subparser: backup
parser_backup = subparsers.add_parser("backup", help="[Ryzer] Faz o backup e organiza os arquivos do caminho passado")
parser_backup.add_argument("--path", "-p", default=str(padrao), type=str, help="[Ryzer] Caminho dos arquivos")
parser_backup.add_argument("--destination", "-d", default=f"{padrao}/Backup", type=str, help="[Ryzer] Caminho de destino")

# Pega todos os args
args = parser.parse_args()

# Exemplo de uso
if args.comando == "organize":
    if args.preview:
        organizar(Path(args.path), Path(args.destination), backup=False, preview=args.preview, verbose=args.verbose)
        

elif args.comando == "backup":
    organizar(Path(args.path), Path(args.destination), backup=True, preview=args.preview, verbose=args.verbose)

else:
    parser.print_help()
