"""Arquivo responsável por geranciar o 'remove' """

from modules import (definer ,file_manager)
from pathlib import Path
from logger import log_error, log
from utils import continuar
from send2trash import send2trash   

def remover_extensoes(type, extensions, no_preview, y: bool = False):
    """
    args:
        type: tipo das extensões.
        extensions: extensoes para remover, caso seja '.', apaga todas as extensões do tipo específicado.
        y: continuar sem perguntar
    """

    data = definer.ler_extensoes()

    if not type in data:
        print(f"[Ryzor] {type} não existe, use `ryzor define -t <tipo das extensoes> -exts <extensoes>` para adicionar uma nova extensao.")
        return

    if extensions is None:
        if not no_preview:
            print(f"[Ryzor] O tipo {type} sera apagado.")
            
            if not file_manager.continuar(y=y):       
                print("[Ryzor] Alterações canceladas")
                return
        
        data.pop(type)
        definer.salvar_extensoes(data)

        print(f"[Ryzor] O tipo {type} foi apagado com sucesso!")
        return

    if extensions[0] == ".":
        extensions = "."

    print("[DEBUG]", extensions)

    antes = []
    antes.extend(data[type])

    indices_remove = []

    if isinstance(extensions, list):
        extensions = definer._normalize_extensions_input(extensions)
    
        for extensao in extensions:
            if extensao in data[type]:
                indices_remove.append(data[type].index(extensao))

        for index in indices_remove:
            data[type].pop(index)

    else:
        data[type] = []

    if no_preview:
        definer.salvar_extensoes(data)

    else:     
        print(f"""
              Antes
              {antes}
              -----
              Depois
              {data[type]}""")
        
        if not file_manager.continuar(y=y):       
            print("[Ryzor] Alterações canceladas")
            return

    definer.salvar_extensoes(data)
    print("[Ryzor] Modificações slvas com sucesso!")

def remover_lista(alvos: list[Path], mensagem: list[str], no_lixeira: bool = False) -> bool:
    if no_lixeira:
        for alvo in alvos:
            try:
                if alvo.is_file():
                    alvo.unlink()
                else:
                    alvo.rmdir()

            except PermissionError:
                log_error(f"Ryzor não tem permissão para apagar {alvo.name}")
            
                break

        else:
            
            log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

            return True
    
        return False

    for alvo in alvos:
        try:
            send2trash(str(alvo))
    
        except PermissionError:
            log_error(f"Ryzor não tem permissão para mover {alvo.name} a lixeira.")

            break

    else:
        log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)
        return True

    return False

def remover_arquivo(alvo: Path, mensagem: list[str], no_lixeira: bool = False):
    if no_lixeira:
        try:
            if alvo.is_file():
                alvo.unlink()
            
            else:
                alvo.rmdir()
        

            log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

            return True
        
        except PermissionError:
            log_error(f"Ryzor não tem permissão para apagar {alvo.name}")
            return False

    try:
        send2trash(str(alvo))
        log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

        return True

    except PermissionError:
        log_error(f"Ryzor não tem permissão para mover {alvo.name} a lixeira.")
        return False

def remover(alvo, full: bool = False, y: bool = False, no_lixeira: bool = False):

    if not alvo.exists():
        log_error("Alvo da remoção não existe.")
        
        return False
    
    mensagem = ["O", "arquivo", "movido para a lixeira."] 

    if no_lixeira:
        mensagem[2] = "excluido"

    if alvo.is_dir():
        mensagem =["A", "pasta", "movida para a lixeira."] 

        if no_lixeira:
            mensagem[2] = "excluida"


    log(f"{mensagem[0]} {mensagem[1]} {alvo.name} será {mensagem[2]} ",code=10)
        
    if continuar(y=y):
        if isinstance(alvo, list):
            return remover_lista(alvos=alvo, no_lixeira=no_lixeira, mensagem=mensagem)

        return remover_arquivo(alvo=alvo, mensagem=mensagem)

    else:    
        log("Cancelando...", code=10)
        return False
