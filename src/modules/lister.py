from pathlib import Path

def mostrar(conteudo: list[Path], verbose: bool = False):
    for content in conteudo:
        tipo = "Arquivo" if content.is_file() else "Diretório" if content.is_dir() else "Outro"
        info = content.resolve() if verbose else content.name
        print(f"[Ryzor] {info} - Tipo: {tipo}")


def lister(caminho: Path, recursive_mode: bool = False, verbose: bool = False):
    if not caminho.exists():
        print("[Ryzor] Caminho não existe")
        return
    
    if caminho.is_file():
        print("[Ryzor] O caminho não pode ser um arquivo")
        return

    if recursive_mode:
        conteudo = list(caminho.rglob("*"))

    else:    
        conteudo = list(caminho.iterdir())

    mostrar(conteudo, verbose)    