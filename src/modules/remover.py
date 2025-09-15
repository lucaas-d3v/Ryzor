import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .utils import Utils
    util = Utils()

except (ModuleNotFoundError, ImportError):
    print(f"[Debug] Erro: Módulo utils não encontrado nos arquivos do ryzor, tente `ryzor repair`")
    print("[Debug] Cancelando...")
        
    quit()    

if util.validate_modules():
    from .definer import DefinitionManager
    from .file_manager import FileController
    from .logger import ConsoleManager
    from pathlib import Path
    from send2trash import send2trash   

else:
    quit()

class DeletionManager():
    def __init__(self):
        self.console_manager = ConsoleManager()
        self.definition_manager = DefinitionManager()
        self.file_controller = FileController()
        self.utils = util

    def remove_extensions(self, type, extensions, no_preview, y: bool = False):
        """
        args:
            type: tipo das extensões.
            extensions: extensoes para remover, caso seja '.', apaga todas as extensões do tipo específicado.
            y: continuar sem perguntar
        """

        data = self.definition_manager.read_extensions()

        if not type in data:
            print(f"[Ryzor] {type} não existe, use `ryzor define -t <tipo das extensoes> -exts <extensoes>` para adicionar uma nova extensao.")
            return

        if extensions is None:
            if not no_preview:
                print(f"[Ryzor] O tipo {type} sera apagado.")
            
                if not self.file_controller.continuar(y=y):       
                    print("[Ryzor] Alterações canceladas")
                    return
        
            data.pop(type)
            self.definition_manager.save_extensions(data)

            print(f"[Ryzor] O tipo {type} foi apagado com sucesso!")
            return

        if extensions[0] == ".":
            extensions = "."

        print("[DEBUG]", extensions)

        antes = []
        antes.extend(data[type])

        indices_remove = []

        if isinstance(extensions, list):
            extensions = self.definition_manager.normalize_extensions_input(extensions)
    
            for extensao in extensions:
                if extensao in data[type]:
                    indices_remove.append(data[type].index(extensao))

            for index in indices_remove:
                data[type].pop(index)

        else:
            data[type] = []

        if no_preview:
            self.definition_manager.save_extensions(data)

        else:     
            print(f"""
                  Antes
                  {antes}
                  -----
                  Depois
                  {data[type]}""")
        
            if not self.file_controller.continuar(y=y):       
                print("[Ryzor] Alterações canceladas")
                return

        self.definition_manager.save_extensions(data)
        print("[Ryzor] Modificações slvas com sucesso!")

    def remover_list(self, alvos: list[Path], mensagem: list[str], no_lixeira: bool = False) -> bool:
        if no_lixeira:
            for alvo in alvos:
                try:
                    if alvo.is_file():
                        alvo.unlink()
                    else:
                        alvo.rmdir()

                except PermissionError:
                    self.console_manager.log_error(f"Ryzor não tem permissão para apagar {alvo.name}")
            
                    break

        
            else:
            
                self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

                return True
    
            return False

        for alvo in alvos:
            try:
                send2trash(str(alvo))
    
            except PermissionError:
                self.console_manager.log_error(f"Ryzor não tem permissão para mover {alvo.name} a lixeira.")

                break

    
        else:
            self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)
            return True

        return False

    def remove_file(self, alvo: Path, mensagem: list[str], no_lixeira: bool = False):
        if no_lixeira:
            try:
                if alvo.is_file():
                    alvo.unlink()
            
                else:
                    alvo.rmdir()
        

                self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

                return True
        
            except PermissionError:
                self.console_manager.log_error(f"Ryzor não tem permissão para apagar {alvo.name}")
                return False

        try:
            send2trash(str(alvo))
            self.console_manager.log(f"{mensagem[0]} {mensagem[1]} foi {mensagem[2]} com sucesso!",code=11)

            return True

        except PermissionError:
            self.console_manager.log_error(f"Ryzor não tem permissão para mover {alvo.name} a lixeira.")
            return False

    def remover(self, alvo, full: bool = False, y: bool = False, no_lixeira: bool = False):

        if not alvo.exists():
            self.console_manager.log_error("Alvo da remoção não existe.")
        
            return False
    
        mensagem = ["O", "arquivo", "movido para a lixeira."] 

        if no_lixeira:
            mensagem[2] = "excluido"

        if alvo.is_dir():
            mensagem =["A", "pasta", "movida para a lixeira."] 

            if no_lixeira:
                mensagem[2] = "excluida"


        self.console_manager.log(f"{mensagem[0]} {mensagem[1]} {alvo.name} será {mensagem[2]} ",code=10)
        
        if self.utils.continue_action(y=y):
            if isinstance(alvo, list):
                return self.remover_list(alvos=alvo, no_lixeira=no_lixeira, mensagem=mensagem)

            return self.remove_file(alvo=alvo, mensagem=mensagem)

        else:    
            self.console_manager.log("Cancelando...", code=10)
            return False
