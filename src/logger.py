"""Arquivo responsável pelas informações do terminal"""

from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.progress import SpinnerColumn, TimeElapsedColumn
from pathlib import Path
import time
from modules import file_manager as fm

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

def log(mensagem: str, debug: bool = False, code: int = 1, end: str = "\n") -> None:
    """
    args:
        mensagem: mensagem a ser escrita no terminal.
        debug: ativa o modo [Debug].
        code: codigo referente ao tipo de mensage, escrita
    """
    
    inicio = "[warning][Debug][/]" if debug else "[primary][Ryzor][/]"
    mensagem = f"{inicio} [{keys[code - 1]}]{mensagem}[/]" if code != 0 else mensagem
    
    console.print(f"{mensagem}", end=end)    

def barra_progresso(mudancas: dict[str, str], backup=True):
    """
    Cria barra de progresso Rich e executa arquivos via callback
    """
    if not mudancas:
        log("Nenhum arquivo para processar", code=10)
        return False
        
    total = len(mudancas)
    log(f"Iniciando {'backup' if backup else 'organização'} de {total} arquivos...", code=11)
    
    try:
        with Progress(
            SpinnerColumn(style="accent"),
            TextColumn("[primary]{task.fields[acao]}[/primary]"),
            TextColumn("[muted]{task.fields[nome_arquivo]}[/muted]"),
            BarColumn(bar_width=None, style="success", complete_style="primary"),
            TextColumn("[success]{task.percentage:>3.0f}%[/success]"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
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
                    completed=kwargs["atual"],
                    nome_arquivo=kwargs["nome_arquivo"],
                    acao=kwargs["acao"]
                )

            # Chamada para execute com o callback
            sucesso = fm.execute(mudancas, callback=atualizar, backup=backup)
            
            if sucesso:
                log("Operação concluída com sucesso!", code=11)
            else:
                log("Operação falhou!", code=9)
                
            return sucesso
            
    except Exception as e:
        log(f"Erro na barra de progresso: {e}", code=9)
        return False


def barra_carregamento_com_callback(callback_busca):
    """
    Barra de progresso que executa uma função callback para buscar arquivos.
    A barra só cuida da visualização, a lógica fica no callback.
    
    Args:
        callback_busca: função que retorna (arquivo, total_encontrados) a cada arquivo encontrado
                       deve ser um generator que yielda (arquivo, contador)
    
    Returns:
        Lista de arquivos retornados pelo callback
    """

    arquivos_encontrados = []
    
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
            contador="0 arquivos encontrados...",
            pasta="Iniciando..."
        )
        
        try:
            # Executa o callback que faz a busca real
            for arquivo, total in callback_busca():
                arquivos_encontrados.append(arquivo)
                
                progress.update(
                    task,
                    contador=f"{total} arquivos encontrados..."
                )
                
        except Exception as e:
            log(f"Erro durante carregamento: {e}", code=9)
            
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
                    progress.update(task, status=f"✨ {total}")
                    
            # Status final
            progress.update(task, status=f"✅ {len(arquivos_encontrados)}")
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