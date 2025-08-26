import argparse as ap
from pathlib import Path
from core import organizar

# Parser principal
parser = ap.ArgumentParser(description="Ryzor")
parser.add_argument("--verbose", "-v", action="store_true", help="Modo Verboso")

# Subparsers
subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")

# Subparser: organize
parser_organize = subparsers.add_parser("organize", help="Apenas organiza os arquivos do caminho passado")
parser_organize.add_argument("--path", "-p", default=str(Path.cwd()), type=str, help="Caminho dos arquivos")
parser_organize.add_argument("--destination", "-d", type=str, help="Caminho de destino")

padrao = Path.cwd()

# Subparser: backup
parser_backup = subparsers.add_parser("backup", help="Faz o backup e organiza os arquivos do caminho passado")
parser_backup.add_argument("--path", "-p", default=str(padrao), type=str, help="Caminho dos arquivos")
parser_backup.add_argument("--destination", "-d", default=padrao, type=str, help="Caminho de destino")

# Pega todos os args
args = parser.parse_args()

# Exemplo de uso
if args.comando == "organize":
    print("Organizando:", args.path, "->", args.destination)
    organizar(Path(args.path), Path(args.destination), backup=False)

elif args.comando == "backup":
    print("Backup + organizar:", args.path, "->", args.destination)
    organizar(Path(args.path), Path(args.destination), backup=True)

else:
    parser.print_help()
