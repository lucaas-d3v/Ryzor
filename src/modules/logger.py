"""File responsible for terminal information"""

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
    from rich.text import Text

except (ModuleNotFoundError, ImportError):
    print(f"[Debug] Error: Rich module not found in Ryzor files, try `ryzor repair`")
    print("[Debug] Cancelling...")
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
            "logo":       "#FFFCDB bold",  
            "normal":     "#FFFCDB",      
            "normal 2":   "#FFFCDB bold",   
            "primary":    "#00FF84 bold",   
            "secondary":  "#00CFFF bold",   
            "background": "on #7F001F",     
            "text":       "#FFFCDB",      
            "muted":      "#CFC7B8",      
            "accent":     "#28F0D5",      
            "error":      "#FF3B5C bold",   
            "warning":    "#FFC107 bold",   
            "success":    "#00FF84"       
        })

        self.version_ = "0.2.9"

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
                self.console.print(Text(" " * left_pad + line.rstrip(), style="logo"))


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
        # usei o estilo do theme em vez de hex hardcoded
        version_table.add_row(f"[warning]Version: {self.version_}[/]")

        self.console.print(version_table, justify="center")
        self.console.print()
        self.console.rule(style="error")

    def show_help(self):
        ascii_banner = self.logo()
        ascii_logo = ascii_banner.rstrip("\n")
        lines = ascii_logo.splitlines()
        
        if lines:
            block_width = max(len(line) for line in lines)
            term_width = self.console.size.width
            left_pad = max((term_width - block_width) // 2, 0)
            for line in lines:
                self.console.print(Text(" " * left_pad + line.rstrip(), style="logo"))


        print()

        commands = Table(
            title="Commands",
            style="primary",
            title_justify="center",
            show_lines=True,       
            expand=False,
            box=box.SQUARE,        
            padding=(0,1),
            border_style="error"
        )

        commands.add_column("Command", style="secondary", no_wrap=True, justify="left")
        commands.add_column("Usage", style="warning", justify="left")
        commands.add_column("Description", style="primary", justify="left")

        commands.add_row("organize", "ryzor organize -p <source> -d <dest>", "Organizes the files in the given path (default = current directory).")
        commands.add_row("backup",   "ryzor backup -p <source> -d <dest>", "Backs up and organizes files in the given path (default = current directory).")
        commands.add_row("list",     "ryzor list -e_exts", "Lists files or supported file types and extensions if -e_exts is used (default = current directory).")
        commands.add_row("define",   "ryzor define -t <type> -exts <extensions>", "Defines a new file type and supported extensions.")
        commands.add_row("remove",   "ryzor remove -t <type> -exts <extensions>", "Removes the entire type or specific extensions (if no extensions passed, type will be removed).")
        commands.add_row("version",  "ryzor version",                        "Displays the current Ryzor version.")
        commands.add_row("repair",   "ryzor repair",                         "Restores Ryzor to factory version.")
        commands.add_row("help",     "ryzor help",                           "Displays this help menu.")

        self.console.print(commands, justify="center")
        self.console.print()

    def help_log(self, message: str) -> str:
        """
        Formats help message for argparse.
        IMPORTANT: Must RETURN string, do not print!
        """
        msg = message.split(" ")
        _msg = "[primary][Help][/] [warning]"
        for word in msg:
            if word == "->":
                _msg += f"[primary]{word}[/] [normal 2]"
            else:
                _msg += f"{word} "
        else:
            _msg += "[/][/]"

        return _msg

    def log_changes(self, changes: dict[str, str], sep: str, backup: bool, verbose: bool = False):
        changes_table = Table(
            title="[primary]Changes[/]",
            style="primary",
            title_justify="center",
            show_lines=True,       
            expand=False,
            box=box.SQUARE,        
            padding=(0,1)
        )

        self.console.rule(
        f"[warning]Mode:[/] {'Backup' if backup else 'Organization'}\n"
        f"[warning]Verbose:[/] {'on' if verbose else 'off'}\n"
        f"[warning]Total changes:[/] {len(changes)}"
    )

        changes_table.add_column("Source", style="secondary", no_wrap=True, justify="left")
        changes_table.add_column("Destination", style="warning", justify="left")
        changes_table.add_column("Type", style="primary", justify="left")

        for source, destination in changes.items():
            typ = Path(source)
            source = self.summary_path(source, sep, verbose=verbose)
            destination = self.summary_path(destination, sep, verbose)
            changes_table.add_row(source, destination, f"{'File' if typ.is_file() else 'Directory' if typ.is_dir() else 'Not specified'}")

        self.console.print(changes_table, justify="center")
        self.console.print()

    def log_error(self, message, repair: bool = False, cancel: bool = True):
        start = "[Error]"
        message = f"[error]{start} {message}[/]"
        if repair:
            message += ", try `ryzor repair`."
        self.console.print(message)
        if cancel:
            self.console.print(f"{start} [error]Cancelling...[/]")

    def log(self, message: str, debug: bool = False, code: int = 1, end: str = "\n") -> None:
        start = "[warning][Debug][/]" if (debug or code == 9) else "[primary][Ryzor][/]"
        message = f"{start} [{self.keys[code - 1]}]{message}[/]" if code != 0 else message
        self.console.print(f"{message}", end=end, justify="center")

    # All progress bar / callback functions have log messages translated to English
    def progress_bar(self, changes: dict[str, str], backup=True):
        """
        Creates a Rich progress bar and executes files via callback.
        """

        from .utils import execute

        if not changes:
            self.log("No files to process", code=10)
            return False

        total = len(changes)
        self.log(f"Starting {'backup' if backup else 'organization'} of {total} files...", code=11)

        try:
            progress = Progress(
                SpinnerColumn(style="accent"),
                TextColumn("[primary]{task.fields[action]}[/primary]", justify="center"),
                TextColumn("[muted]{task.fields[file_name]}[/muted]", justify="center"),
                BarColumn(bar_width=None, style="success", complete_style="primary"),
                TextColumn("[success]{task.percentage:>3.0f}%[/success]", justify="center"),
                TimeRemainingColumn(),
                console=self.console,
                transient=False,
            )

            with Live(Align(progress, "center"), refresh_per_second=10, console=self.console):
                progress.start()
                task = progress.add_task(
                    "",
                    total=total,
                    file_name="Preparing...",
                    action="Starting"
                )

                def update(self, **kwargs):
                    progress.update(
                        task,
                        completed=kwargs.get("current", 0),
                        file_name=kwargs.get("file_name", ""),
                        action=kwargs.get("action", ""),
                        error=kwargs.get("error", False)
                    )

                try:
                    success = execute(changes, callback=update, backup=backup)

                    if success[0]:
                        self.log("Operation completed successfully!", code=11)
                    else:
                        self.log_error(f"Error in execute: {success[1]}")
                        self.log_error("Cancelling...")

                except KeyboardInterrupt:
                    progress.stop()
                    self.log("Operation interrupted by user (Ctrl+C).", code=10)
                    return False
                except Exception as e:
                    progress.stop()
                    self.log(f"Error during operation: {e}", code=9)
                    return False
                finally:
                    progress.stop()

            return success

        except Exception as e:
            self.log(f"Error in progress bar: {e}", code=9)
            return False

    # Terminal input helpers
    @contextlib.contextmanager
    def stdin_cbreak(self):
        """
        Context manager that puts terminal in cbreak mode (char-by-char)
        and restores original flags on exit.
        Only works on Unix-like systems (ok for Debian).
        """
        fd = sys.stdin.fileno()
        old_attrs = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            yield
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)

    def key_pressed(self, key="q") -> bool:
        """
        Non-blocking check if a key was pressed.
        Returns True if the single character matches.
        Must be used while terminal is in cbreak mode (see stdin_cbreak).
        """
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            ch = sys.stdin.read(1)
            return ch.lower() == key.lower()
        return False

    def summary_path(self, path, sep="/", verbose=False):
        # normalize path (Path or ".")
        path = Path.cwd() if path == "." else Path(path)
        path = path.resolve()

        if verbose:
            return str(path)
        else:
            parts = path.parts
            if len(parts) <= 2:
                return sep.join(parts)
            return sep.join(parts[-2:])

def loading_bar_with_callback(self, callback_search, sep="/", verbose=False):
    """
    Progress bar that executes a callback function to search for files.
    Now allows interruption with 'q' (without Enter) or Ctrl+C.
    """
    found_files = []

    try:
        # Enable cbreak mode only during progress bar execution
        with self.stdin_cbreak():
            with Progress(
                SpinnerColumn(style="accent"),
                TextColumn("[accent]Loading files[/accent]"),
                TextColumn("[primary]{task.fields[counter]}[/primary]"),
                TextColumn("[muted]{task.fields[folder]}[/muted]"),
                TimeElapsedColumn(),
                console=self.console,
            ) as progress:

                task = progress.add_task(
                    "",
                    counter="0 files found... ('q' to quit)",
                    folder="Starting..."
                )

                try:
                    # Execute the callback that performs the actual search
                    for file, total in callback_search():
                        # Check key press without blocking
                        if self.key_pressed("q"):
                            progress.stop()
                            self.log("Search interrupted by user (key 'q')...", code=10)
                            return

                        found_files.append(file)
                        folder = self.summary_path(file, sep=sep, verbose=verbose)

                        progress.update(
                            task,
                            counter=f"{total} files found...",
                            folder=folder
                        )

                except KeyboardInterrupt:
                    progress.stop()
                    self.log("Search interrupted by user...", code=10)

                except Exception as e:
                    progress.stop()
                    self.log(f"Error during loading: {e}", code=9)

    except KeyboardInterrupt:
        self.log("Search interrupted by user (Ctrl+C).", code=10)
        return

    except Exception as e:
        self.log(f"Unexpected error: {e}", code=9)
        return

    return found_files


def simple_loading_bar_callback(self, callback_search):
    """
    Simpler version of the progress bar with callback.
    """
    found_files = []

    with Progress(
        SpinnerColumn(style="accent"),
        TextColumn("[accent bold]Discovering files...[/accent bold]"),
        TextColumn("[primary]{task.fields[status]}[/primary]"),
        console=self.console,
    ) as progress:

        task = progress.add_task("", status=" 0")

        try:
            for file, total in callback_search():
                found_files.append(file)

                # Update every 10 files for better performance
                if total % 10 == 0:
                    progress.update(task, status=f" {total}")

            # Final status
            progress.update(task, status=f" {len(found_files)}")
            time.sleep(0.3)

        except Exception as e:
            self.log(f"Error: {e}", code=9)

    return found_files


def advanced_loading_bar_callback(self, callback_search, title="Loading"):
    """
    More advanced version that allows custom title.
    """
    found_files = []

    with Progress(
        SpinnerColumn(style="accent", spinner_name="dots"),
        TextColumn(f"[accent]{title}[/accent]"),
        TextColumn("[primary]{task.fields[counter]}[/primary]"),
        TextColumn("[muted]{task.fields[info]}[/muted]"),
        TimeElapsedColumn(),
        console=self.console,
    ) as progress:

        task = progress.add_task(
            "",
            counter="0",
            info="Starting..."
        )

        start_time = time.time()

        try:
            for result in callback_search():
                # Callback can return tuple (file, total) or (file, total, extra_info)
                if len(result) == 2:
                    file, total = result
                else:
                    file, total, extra_info = result

                found_files.append(file)

                elapsed = time.time() - start_time
                progress.update(
                    task,
                    counter=f"{total}",
                    info=f"{elapsed:.1f}s"
                )

        except Exception as e:
            progress.update(task, info=self.log(f"Error: {str(e)[:30]}...", code=9))

    return found_files
