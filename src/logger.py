"""Arquivo responsável pelas informações do terminal"""

from rich import box
from rich.table import Table
from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.progress import SpinnerColumn, TimeElapsedColumn
from rich.live import Live
from rich.align import Align
from rich.progress import SpinnerColumn, BarColumn
from pathlib import Path
import time
from modules.utils import execute
import pyfiglet
import sys
import select
import termios
import tty
import contextlib

ryzor_theme = Theme({
    "normal":     "#efefef",
    "normal 2":      "#efefef bold",
    "primary":      "#01bb88 bold",
    "secondary":    "#1E2489 bold",
    "background":   "on #191d27",
    "text":         "#efefef",
    "muted":        "#94a3b8",
    "accent":       "#00ffff",
    "error":        "#e43e5a bold",
    "warning":      "#f1a802 bold",
    "success":      "#01bb88",
})

keys = ["normal", # 1
        "normal 2", # 2
        "primary", # 3
        "secondary", # 4
        "background", # 5
        "text", # 6
        "muted", # 7
        "accent", # 8
        "error", # 9
        "warning", # 10
        "success" # 11
    ]

console = Console(theme=ryzor_theme)

def logo():
    return pyfiglet.figlet_format("Ryzor")

def version():
    ascii_banner = logo()
    ascii_logo = ascii_banner.rstrip("\n")
    lines = ascii_logo.splitlines()

    if lines:
        block_width = max(len(line) for line in lines)
        term_width = console.size.width
        left_pad = max((term_width - block_width) // 2, 0)
        for line in lines:
            console.print(" " * left_pad + line.rstrip(), style="#01bb88 bold")

    print()

    console.rule(style="#01bb88")

    version_table = Table(
        title="",
        style="#01bb88",
        title_justify="center",
        show_lines=False,
        expand=False,
        box=None,
        padding=(0,1),
    )

    version_table.add_row("[#00ffff]By: Lucas Paulino[/]")
    version_table.add_row("[#00ffff]Version: 0.1.7[/]")

    console.print(version_table, justify="center")
    console.print()
    
    console.rule(style="#01bb88")

def show_help():
    ascii_logo = logo().rstrip("\n")

    lines = ascii_logo.splitlines()
    if lines:
        block_width = max(len(line) for line in lines)
        term_width = console.size.width
        left_pad = max((term_width - block_width) // 2, 0)
        for line in lines:
            console.print(" " * left_pad + line.rstrip(), style="#01bb88 bold")
    
    console.print()

    # tabela com linhas horizontais entre cada entrada
    comandos = Table(
        title="Comandos",
        style="#01bb88",
        title_justify="center",
        show_lines=True,       # desenha linha horizontal entre as linhas
        expand=False,
        box=box.SQUARE,        # experimente box.SIMPLE, box.SQUARE ou box.SIMPLE_HEAVY
        padding=(0,1),
    )
    
    comandos.add_column("Comando", style="#00ffff bold", no_wrap=True, justify="left")
    comandos.add_column("Uso", style="#EEAD2D bold", justify="left")
    comandos.add_column("Descrição", style="#00804b bold", justify="left")

    comandos.add_row("organize", "ryzor organize -p <origem> -d <destino>", "Apenas organiza os arquivos do caminho passado (padrao = diretório atual).")
    comandos.add_row("backup",   "ryzor backup -p <origem> -d <destino>", "Faz o backup e organiza os arquivos do caminho passado (padrao = diretório atual).")
    comandos.add_row("list",     "ryzor list -e_exts", "Lista arquivos ou tipos de arquivos e extensões suportadas se usar -e_exts (padrao = diretório atual).")
    comandos.add_row("define",   "ryzor define -t <tipo> -exts <extensões>", "Define um novo tipo de arquivo e extensões suportadas.")
    comandos.add_row("remove",   "ryzor remove -t <tipo> -exts <extensões>", "Remove o tipo todo ou extensões específicas (se não passar extensoes, o tipo sera removido).")
    comandos.add_row("version",  "ryzor version",                        "Informa a versão atual do Ryzor.")
    comandos.add_row("repair",   "ryzor repair",                         "Restaura o Ryzor para versão de fábrica.")
    comandos.add_row("help",     "ryzor help",                           "Mostra este menu de ajuda.")

    console.print(comandos, justify="center")
    console.print()

def help_log(mensagem: str) -> str:
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

def log_mudancas(mudancas: dict[str, str], sep: str, backup: bool, verbose: bool = False):
    mudancas_table = Table(
        title="[#01bb88 bold]Mudanças[/]",
        style="#01bb88",
        title_justify="center",
        show_lines=True,       # desenha linha horizontal entre as linhas
        expand=False,
        box=box.SQUARE,        # experimente box.SIMPLE, box.SQUARE ou box.SIMPLE_HEAVY
        padding=(0,1)
    )

    console.rule(
    f"[#EEAD2D bold]Modo:[/] {'Backup' if backup else 'Organização'}\n"
    f"[#EEAD2D bold]Verbose:[/] {'on' if verbose else 'off'}\n"
    f"[#EEAD2D bold]Total de modificações:[/] {len(mudancas)}"
)

    mudancas_table.add_column("Origem", style="#00ffff bold", no_wrap=True, justify="left")
    mudancas_table.add_column("Destino", style="#EEAD2D bold", justify="left")
    mudancas_table.add_column("Tipo", style="#00804b bold", justify="left")

    
    for origem, destino in mudancas.items():
        tipo = Path(origem)

        origem = resumo_pasta(origem, sep, verbose=verbose)
        destino = resumo_pasta(destino, sep, verbose)
        

        mudancas_table.add_row(origem, destino, f"{'Arquivo' if tipo.is_file() else 'Diretório' if tipo.is_dir() else 'Não específicado'}")

    console.print(mudancas_table, justify="center")
    console.print()

def log_error(mensagem, repair: bool = False, cancel: bool = True):
    inicio = "[warning][Debug][/]"

    mensagem = f"{inicio} [error]{mensagem}[/]"

    if repair:
        mensagem += ", tente `ryzor repair`."

    console.print(mensagem)    
    
    if cancel:
        console.print(f"{inicio} [error]Cancelando...[/]")


def log(mensagem: str, debug: bool = False, code: int = 1, end: str = "\n") -> None:
    """
    args:
        mensagem: mensagem a ser escrita no terminal.
        debug: ativa o modo [Debug].
        code: codigo referente ao tipo de mensage, escrita
    """
    
    inicio = "[warning][Debug][/]" if (debug or code == 9) else "[primary][Ryzor][/]"
    mensagem = f"{inicio} [{keys[code - 1]}]{mensagem}[/]" if code != 0 else mensagem
    
    console.print(f"{mensagem}", end=end, justify="center")    

def barra_progresso(mudancas: dict[str, str], backup=True):
    """
    Cria barra de progresso Rich centralizada e executa arquivos via callback.
    """

    if not mudancas:
        log("Nenhum arquivo para processar", code=10)
        return False

    total = len(mudancas)
    log(f"Iniciando {'backup' if backup else 'organização'} de {total} arquivos...", code=11)

    # montar o Progress (não como context manager)

    try:
        progress = Progress(
            SpinnerColumn(style="accent"),
            TextColumn("[primary]{task.fields[acao]}[/primary]", justify="center"),
            TextColumn("[muted]{task.fields[nome_arquivo]}[/muted]", justify="center"),
            BarColumn(bar_width=None, style="success", complete_style="primary"),
            TextColumn("[success]{task.percentage:>3.0f}%[/success]", justify="center"),
            TimeRemainingColumn(),
            console=console,
            transient=False,
        )

        # Live + Align centralizam todo o render do Progress
        with Live(Align(progress, "center"), refresh_per_second=10, console=console):
            progress.start()
            task = progress.add_task(
                "",
                total=total,
                nome_arquivo="Preparando...",
                acao="Iniciando"
            )

            # Callback que será passado para execute()
            def atualizar(**kwargs):
                progress.update(
                    task,
                    completed=kwargs.get("atual", 0),
                    nome_arquivo=kwargs.get("nome_arquivo", ""),
                    acao=kwargs.get("acao", "")
                )

            try:
                # Chamada para execute com o callback
                sucesso = execute(mudancas, callback=atualizar, backup=backup)

                if sucesso[0]:
                    log("Operação concluída com sucesso!", code=11)
                else:

                    log_error(f"Erro em execute: {sucesso[1]}")
                    log_error("Cancelando...")
            
            except KeyboardInterrupt:
                # garante parada limpa se Ctrl+C
                progress.stop()
                log("Operação interrompida pelo usuário (Ctrl+C).", code=10)
                return False
            except Exception as e:
                progress.stop()
                log(f"Erro durante operação: {e}", code=9)
                return False
            finally:
                # sempre para o progress antes de sair do Live
                progress.stop()

        return sucesso

            
    except Exception as e:
        log(f"Erro na barra de progresso: {e}", code=9)
        return False


@contextlib.contextmanager
def stdin_cbreak():
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


def tecla_pressionada(tecla="q") -> bool:
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

def resumo_pasta(arquivo, sep="/", verbose=False):
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


def barra_carregamento_com_callback(callback_busca, sep, verbose = False):
    """
    Barra de progresso que executa uma função callback para buscar arquivos.
    Agora permite interromper com 'q' (sem Enter) ou com Ctrl+C.
    """
    arquivos_encontrados = []

    try:
        # ativa modo cbreak só durante a execução da barra
        with stdin_cbreak():
            with Progress(
                SpinnerColumn(style="accent"),
                TextColumn("[accent]Carregando arquivos[/accent]"),
                TextColumn("[primary]{task.fields[contador]}[/primary]"),
                TextColumn("[muted]{task.fields[pasta]}[/muted]"),
                TimeElapsedColumn(),
                console=console,
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
                        if tecla_pressionada("q"):
                            progress.stop()
                            log("Busca interrompida pelo usuário (tecla 'q')...", code=10)
                            return

                        arquivos_encontrados.append(arquivo)

                        arquivo_ = Path(arquivo)

                        pasta = resumo_pasta(arquivo, sep=sep, verbose=verbose)

                        progress.update(
                            task,
                            contador=f"{total} arquivos encontrados...",
                            pasta=pasta
                        )

                except KeyboardInterrupt:
                    # Ctrl+C
                    progress.stop()
                    log("Busca interrompida pelo usuário...", code=10)

                except Exception as e:
                    progress.stop()
                    log(f"Erro durante carregamento: {e}", code=9)

    except KeyboardInterrupt:
        # Caso o KeyboardInterrupt ocorra fora do with (segurança extra)
        log("Busca interrompida pelo usuário (Ctrl+C).", code=10)
        return 
    
    except Exception as e:
        log(f"Erro inesperado: {e}", code=9)
        return 

    return arquivos_encontrados


def barra_carregamento_simples_callback(callback_busca):
    """
    Versão mais simples da barra com callback
    """
    arquivos_encontrados = []
    
    with Progress(
        SpinnerColumn(style="accent"),
        TextColumn("[accent bold]Descobrindo arquivos...[/accent bold]"),
        TextColumn("[primary]{task.fields[status]}[/primary]"),
        console=console,
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
            log(f"Erro: {e}", code=9)
            
    return arquivos_encontrados


def barra_carregamento_avancada_callback(callback_busca, titulo="Carregando"):
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
        console=console,
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
            progress.update(task, info=log(f"Erro: {str(e)[:30]}...", code=9))
            
    return arquivos_encontrados