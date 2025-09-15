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