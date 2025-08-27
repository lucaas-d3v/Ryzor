"""Arquivo responsável por geranciar o 'remove' """

from modules import (definer ,file_manager)

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
            
            if not file_manager.continuar(y):       
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
        
        if not file_manager.continuar(y):       
            print("[Ryzor] Alterações canceladas")
            return

    definer.salvar_extensoes(data)
    print("[Ryzor] Modificações slvas com sucesso!")
