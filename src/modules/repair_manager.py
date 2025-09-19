from pathlib import Path
import json
import subprocess

from .logger import ConsoleManager
from .utils import Utils

class Restorer:
    def __init__(self):
        self.extensions = {}
        self.try_action = 0
        self.base_dir = Path(".") / ".." / "Ryzor"
        self.console = ConsoleManager()
        self.utils = Utils()

    def _default_extension_to_use(self) -> None:
        JSON_PATH = self.base_dir / "src" / "protected" / "extensions_default.json"
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

        if JSON_PATH.exists():
            with JSON_PATH.open("r") as f:
                content = json.load(f)
                if content:
                    self.extensions = content
                    return

        # Caso o arquivo padrão não exista
        self.extensions = {
            "Effects": [".fx", ".ffx", ".aep", ".aepx", ".prfpset", ".mogrt", ".vfx", ".preset", ".action"],
            "Compactados": [".rar", ".zip", ".7zip", ".7z", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz", ".gz", ".bz2", ".xz", ".iso", ".dmg", ".jar", ".apk"],
            "Mc_addon": [".mcpack", ".mcaddon", ".mcworld", ".mcr", ".mce", ".mca"],
            "Codigos": [".py", ".pyc", ".ipynb", ".cs", ".java", ".cpp", ".c", ".h", ".hpp", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm", ".css", ".scss", ".sass", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".kts", ".m", ".mm", ".sh", ".bat", ".ps1"],
            "Installers": [".msi", ".exe", ".pkg", ".deb", ".rpm", ".app", ".apk", ".bin", ".run", ".dmg"],
            "Documentos": [".txt", ".doc", ".docx", ".odt", ".xls", ".xlsx", ".ods", ".csv", ".ppt", ".pptx", ".odp", ".pdf", ".xps", ".tex", ".ltx", ".rtf", ".md", ".markdown", ".html", ".htm", ".epub", ".mobi", ".log", ".json", ".xml", ".yml", ".yaml", ".ini", ".cfg", ".toml", ".db", ".sql", ".sqlite"],
            "Imagems": [".ico", ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".cur", ".bmp", ".png", ".gif", ".tiff", ".tif", ".webp", ".heic", ".heif", ".avif", ".dds", ".exr", ".raw", ".svg", ".ai", ".eps", ".cdr", ".psd", ".indd", ".pdf", ".kra", ".xcf", ".orf", ".nef", ".cr2", ".dng", ".arw"],
            "Videos": [".mp4", ".mov", ".mkv", ".avi", ".flv", ".wmv", ".3gp", ".3g2", ".mpg", ".mpeg", ".ogv", ".m4v", ".mts", ".ts", ".divx", ".vob", ".f4v", ".webm", ".rm", ".rmvb", ".m2ts"],
            "Audios": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".alac", ".aiff", ".opus", ".amr", ".dsd", ".pcm", ".aax", ".ra", ".mid", ".midi", ".aif", ".au", ".caf"],
            "Projetos": [".veg", ".vf", ".aep", ".aepx", ".prproject", ".pproj", ".ppj", ".drp", ".db", ".fcpxml", ".fcpbundle", ".imovieproj", ".kdenlive", ".mlt", ".osp", ".xsed", ".vpr", ".blend", ".c4d", ".max", ".mb", ".ma", ".skp", ".psd", ".prproj", ".aep", ".flp", ".als", ".logicx", ".musx", ".rpp", ".sib", ".cpr", ".tracktion", ".omf", ".aiffproj"]
        }

        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(self.extensions, f, indent=4)

    def repair_extensions(self):
        """Restaura os arquivos de extensões padrão."""
        JSON_PROD = self.base_dir / "src" / "modules" / "data" / "extensions.json"
        JSON_DEFAULT = self.base_dir / "protected" / "extensions_default.json"

        for json_file in [JSON_PROD, JSON_DEFAULT]:
            json_file.parent.mkdir(parents=True, exist_ok=True)
            with json_file.open("w", encoding="utf-8") as f:
                json.dump(self.extensions, f, indent=4)

        self.console.log("Extensions repaired successfully!", code=12)

    def repair_dependencies(self):
        """Instala dependências listadas no requirements.txt"""
        self.try_action += 1
        req_file = self.base_dir / "requirements.txt"

        if not req_file.exists():
            self.console.log(f"Creating requirements.txt at {req_file}", code=10)
            with req_file.open("w") as f:
                f.write("rich==13.9.4\npyfiglet==0.8.post1\nsend2trash==1.8.3")

        try:
            subprocess.run(["pip", "install", "-r", str(req_file)], check=True)
            self.console.log("Dependencies installed successfully!", code=12)
        except subprocess.CalledProcessError as e:
            self.console.log_error(f"Failed to install dependencies: {e}")

    def repair_modules(self):
        """Cria arquivos base dos módulos se estiverem ausentes"""
        # Conteúdo dos módulos seria preenchido aqui
        modules_content = {
            "definer": "",
            "file_manager": "",
            "logger": "",
            "remover": "",
            "utils": "",
            "cli": ""
        }

        DIR = self.base_dir / "src" / "modules"
        DIR.mkdir(parents=True, exist_ok=True)
        created_files = []

        for module, content in modules_content.items():
            path = DIR / f"{module}.py" if module != "cli" else self.base_dir / "src" / f"{module}.py"
            with path.open("w", encoding="utf-8-sig") as f:
                f.write(content)
            created_files.append(path)

        if created_files:
            self.console.log("Modules repaired successfully!", code=12)
        else:
            self.console.log_error("Error repairing modules.")

    def repair(self, r_extensions: bool = False, r_config: bool = False, r_modules: bool = False, y: bool = False):
        """Função principal de repair"""
        if not any([r_extensions, r_config, r_modules]):
            self.console.log("No arguments provided for <repair>, check `ryzor help`", code=10)
            return

        if self.utils.continue_action(y=y):
            if r_extensions:
                self.repair_extensions()
            if r_config:
                self.console.log("Configuration repair in development", code=11)
            if r_modules:
                self.repair_modules()
        else:
            self.console.log("Cancelling repair...", code=11)
