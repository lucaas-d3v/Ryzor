import sys
import os
from pathlib import Path
from send2trash import send2trash

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .utils import Utils
    util = Utils()

except (ModuleNotFoundError, ImportError):
    print("in remover")
    print("[Debug] Error: utils module not found, try `ryzor repair`")
    print("[Debug] Cancelling...")
    quit()    

if util.validate_modules():
    from .definer import DefinitionManager
    from .file_manager import FileController
    from .logger import ConsoleManager
    
else:
    quit()


class DeletionManager:
    def __init__(self):
        self.console_manager = ConsoleManager()
        self.definition_manager = DefinitionManager()
        self.file_controller = FileController()
        self.utils = util

    def remove_extensions(self, type_name, extensions, no_preview, y: bool = False):
        """Remove specific extensions or entire type from definitions."""
        data = self.definition_manager.read_extensions()

        if type_name not in data:
            self.console_manager.log_error(f"{type_name} does not exist. Use `ryzor define -t <type> -exts <extensions>` to add it.")
            return

        # Remove entire type if no extensions are provided
        if not extensions:
            if not no_preview:
                self.console_manager.log(f"The type {type_name} will be deleted.", code=12)
                if not self.file_controller.continue_action(y=y):
                    self.console_manager.log("Changes cancelled.", code=11)
                    return

            data.pop(type_name)
            self.definition_manager.save_extensions(data)
            self.console_manager.log(f"Type {type_name} deleted successfully!", code=12)
            return

        # Normalize extensions
        if isinstance(extensions, list):
            extensions = self.definition_manager.normalize_extensions_input(extensions)
            before = data[type_name].copy()
            for ext in extensions:
                if ext in data[type_name]:
                    data[type_name].remove(ext)
        else:
            # If single non-list extension, remove all
            before = data[type_name].copy()
            data[type_name] = []

        # Show preview
        if not no_preview:
            self.console_manager.log(f"""
Before:
{before}
-----
After:
{data[type_name]}
""")
            if not self.file_controller.continue_action(y=y):
                self.console_manager.log("Changes cancelled.", code=11)
                return

        self.definition_manager.save_extensions(data)
        self.console_manager.log("Modifications saved successfully!", code=12)

    def remove_file(self, target: Path, message: list[str], no_trash: bool = False):
        """Remove a single file or directory."""
        try:
            if no_trash:
                if target.is_file():
                    target.unlink()
                else:
                    target.rmdir()
            else:
                send2trash(str(target))

            self.console_manager.log(f"{message[0]} {message[1]} {target.name} {message[2]}", code=11)
            return True

        except PermissionError:
            self.console_manager.log_error(f"Ryzor does not have permission to remove {target.name}")
            return False

    def remove_list(self, targets: list[Path], message: list[str], no_trash: bool = False):
        """Remove a list of files or directories."""
        for target in targets:
            success = self.remove_file(target, message, no_trash)
            if not success:
                return False
        return True

    def remover(self, target, full: bool = False, y: bool = False, no_trash: bool = False):
        """Main removal method, handles files, directories, and confirmation."""
        if not target.exists():
            self.console_manager.log_error("Target does not exist.")
            return False

        # Determine type message
        message = ["The", "file", "was moved to trash."]
        if no_trash:
            message[2] = "deleted"

        if target.is_dir():
            message = ["The", "directory", "was moved to trash."]
            if no_trash:
                message[2] = "deleted"

        self.console_manager.log(f"{message[0]} {message[1]} {target.name} will be {message[2]}", code=11)

        if self.utils.continue_action(y=y):
            if isinstance(target, list):
                return self.remove_list(targets=target, no_trash=no_trash, message=message)
            return self.remove_file(target, message, no_trash)
        else:
            self.console_manager.log("Cancelling...", code=11)
            return False
